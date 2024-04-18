import igraph as ig
from manim import *
from manim_slides import Slide

from animations.beamer.slides import SlideWithBlocks, PromptSlide, SlideWithList
from animations.common import MANIM_BLUE
from animations.demos.graph_example import GraphPair
from animations.demos.methods.clip import CLIPDemo
from animations.demos.timeline_helper import get_noteworthy_events, TimelineEvent
from animations.demos.ww2 import CaptionedSVG, CaptionedJPG

config.disable_caching = True  # may need to disable caching for the timeline
config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class Timeline(Slide, MovingCameraScene):
    def construct(self):
        # introduction to presentation
        # self.greeting()

        timeline_igraph: ig.Graph = ig.Graph(directed=True)

        timeline_events = get_noteworthy_events()

        # get the layout for the possible graph which will implement the timeline
        prev_x_location: float = 0
        prev_timeline_event = None
        digraph_layout = {0: (prev_x_location, 0, 0)}
        global_idx = 0
        for timeline_event in timeline_events:
            if not isinstance(timeline_event, dict):
                spacing = 5  # a good spacing for the timeline I found works well
                if isinstance(prev_timeline_event, str) and isinstance(
                    timeline_event, str
                ):
                    # two consecutive strings do not need as much spacing
                    spacing = 1
                # technically we never use the vertex located at index 0
                new_x_location = prev_x_location + spacing
                digraph_layout[max(digraph_layout.keys()) + 1] = (new_x_location, 0, 0)
                prev_timeline_event = timeline_event
                prev_x_location = new_x_location
            else:
                # this is a dictionary, which means we breeze over the timeline,
                # but we still need to account for the spacing and timeline pins
                for publication in list(timeline_event.values())[0]:
                    spacing = 5  # a good spacing for the timeline I found works well
                    if isinstance(prev_timeline_event, str) and isinstance(
                        publication, str
                    ):
                        # two consecutive strings do not need as much spacing
                        spacing = 1
                    # technically we never use the vertex located at index 0
                    new_x_location = prev_x_location + spacing
                    digraph_layout[max(digraph_layout.keys()) + 1] = (
                        new_x_location,
                        0,
                        0,
                    )
                    prev_timeline_event = publication
                    prev_x_location = new_x_location

        # now create the necessary graph components based on the above needed layout
        # num_of_vertices = len(timeline_events) + 1
        num_of_vertices = len(digraph_layout)
        timeline_igraph.add_vertices(num_of_vertices)
        # timeline_igraph.vs["name"] = ["2010", "2015", "2020", "2025", "2030"]
        edges = list(zip(range(0, num_of_vertices - 1), range(1, num_of_vertices)))
        timeline_igraph.add_edges(edges)

        # consistent spacing for the timeline
        # spacing = 5  # a good spacing for the timeline I found works well
        # digraph_layout = {idx: (idx * spacing, 0, 0) for idx in range(num_of_vertices)}
        # spacing relative to timeline events' start and end years
        # def get_loc_from_start_end_years(start_year, end_year):
        #     return (start_year + end_year) / 2

        # def get_event_plot_coords(timeline_event: TimelineEvent):
        #     spacing = 5  # a good spacing for the timeline I found works well
        #
        #     if timeline_event.poi is not None:
        #         return timeline_event.poi + spacing, 0, 0
        #     return (
        #         timeline_event.start_year + spacing, 0, 0
        #     ) if timeline_event.era_notation == "CE" else (
        #         -1 * (timeline_event.start_year + spacing), 0, 0
        #     )
        #
        # digraph_layout = {
        #     idx: get_event_plot_coords(timeline_events[idx - 1])
        #     for idx in range(1, num_of_vertices)
        # }
        # digraph_layout[0] = (timeline_events[0].start_year - 10, 0, 0)

        timeline_manim = DiGraph(
            timeline_igraph.vs.indices,
            timeline_igraph.get_edgelist(),
            label_fill_color=BLACK,
            layout=digraph_layout,
            vertex_config={
                "fill_color": BLACK,
                "stroke_color": BLACK,
                "stroke_width": 2,
                "radius": 0.05,
            },
            edge_config={
                "stroke_color": "BLACK",
                "stroke_width": 2,
                "tip_config": {"tip_length": 0.07, "tip_width": 0.07},
            },
        )

        timeline = GraphPair(timeline_igraph, digraph=timeline_manim)
        self.camera.frame.move_to(timeline.digraph.get_center()).set(width=10)

        # start_loc = timeline.digraph.vertices[0].get_center()
        # end_loc = timeline.digraph.vertices[num_of_vertices - 1].get_center()
        source_vertex_idx = 0
        source_vertex = timeline.digraph.vertices[source_vertex_idx]
        self.play(self.camera.frame.animate.move_to(source_vertex).set(width=10))
        self.camera.frame.save_state()

        running_offset: float = (
            0  # offset for the timeline events to account for thought slides
        )
        idx = -1
        # for idx, edge in enumerate(edges):
        timeline_lookup = {}  # stores the index in relation to the manim objects
        next_brace_direction = (
            DOWN  # alternate the direction of the braces to avoid overlap
        )
        for slides in timeline_events:
            # slides = timeline_events[idx]
            print(
                f"Processing slide {idx + 1} of {len(timeline_events)}: {type(slides)}"
            )

            if isinstance(slides, dict):
                # then this is an era with multiple publications
                overview_str: str = list(slides.keys())[
                    0
                ]  # get the high-level overview string
                slides = list(slides.values())[0]  # get the list of publications
                play_as_ready = False  # play the animations once all slides are ready
                default_run_time = 0.25  # speed up the animations for publications
                v_group_to_render = VGroup()  # the group of manim objects to render
            else:
                slides = [slides]  # convert to a list for consistency
                play_as_ready = (
                    True  # play the animations as soon as the slide is ready
                )
                default_run_time = 1  # default speed for the animations
                v_group_to_render = None

            slide_animations = []  # the list of animations to play for these slides

            for slide in slides:
                idx += 1
                print(idx, slide, len(edges))
                edge = edges[idx]
                source_vertex_idx, target_vertex_idx = edge[0], edge[1]
                target_vertex = timeline.digraph.vertices[target_vertex_idx]

                line: Line = timeline.digraph.edges[edge[0], edge[1]]
                # apply a slight offset to the target vertex, to account for thought slides, if any
                if running_offset > 0:
                    target_vertex.shift(running_offset * RIGHT)
                    line.shift(running_offset * RIGHT)

                if play_as_ready and v_group_to_render is None:
                    self.play(
                        AnimationGroup(
                            Create(line),
                            self.camera.frame.animate.move_to(target_vertex),
                            run_time=default_run_time,
                        )
                    )
                    self.play(Create(target_vertex, run_time=default_run_time))
                else:
                    v_group_to_render.add(line)
                    v_group_to_render.add(target_vertex)

                # store the manim objects so far
                timeline_lookup[idx] = VGroup(line, target_vertex)

                vertex_coords = target_vertex.get_center()

                if isinstance(slide, TimelineEvent) or isinstance(slide, str):
                    # draw a time-stamped event from the timeline
                    direction = UP if idx % 2 == 0 else DOWN
                    pin: Line = Line(
                        vertex_coords,
                        vertex_coords + direction,
                        color=BLACK,
                        stroke_width=2,
                    )

                    if play_as_ready:
                        slide_animations.append(
                            AnimationGroup(
                                Create(pin, run_time=default_run_time),
                                self.camera.frame.animate.move_to(
                                    vertex_coords + direction
                                ).set(width=10),
                                run_time=default_run_time,
                            )
                        )
                    else:
                        slide_animations.append(Create(pin, run_time=default_run_time))

                    # store the pin
                    timeline_lookup[idx].add(pin)

                    if v_group_to_render is not None:
                        v_group_to_render.add(pin)

                    if isinstance(slide, TimelineEvent):
                        boundary = self.make_boundary_at_coords(
                            direction, vertex_coords
                        )
                        if slide.poi is not None:  # point of interest takes precedence
                            timestamp_str = f"{slide.poi} {slide.era_notation}"
                        elif slide.start_year == slide.end_year:
                            timestamp_str = f"{slide.start_year} {slide.era_notation}"
                        else:
                            timestamp_str = f"{slide.start_year} - {slide.end_year} {slide.era_notation}"
                        timestamp = Text(
                            timestamp_str,
                            font="TeX Gyre Termes",
                            color=BLACK,
                        ).next_to(boundary, direction)

                        # store the boundary and timestamp
                        timeline_lookup[idx].add(boundary)
                        timeline_lookup[idx].add(timestamp)

                        if v_group_to_render is not None:
                            v_group_to_render.add(boundary)
                            v_group_to_render.add(timestamp)

                        slide_animations.append(
                            Create(
                                VGroup(boundary, timestamp), run_time=default_run_time
                            )
                        )
                    else:
                        # this is a string, treat it as a publication citation
                        amount_to_rotate: float = (PI / 4) * (1 if idx % 2 == 0 else -1)
                        publication = (
                            Text(
                                slide,
                                font="TeX Gyre Termes",
                                color=BLACK,
                            )
                            .rotate(amount_to_rotate)
                            .scale(0.15)
                            .next_to(pin, direction)
                            .shift(0.5 * RIGHT)
                        )
                        #     0.5 * (RIGHT if idx % 2 == 0 else LEFT)
                        # )  # shift it to the right if UP else shift to the left if DOWN

                        if play_as_ready:
                            # save the state of the publication
                            publication.save_state()
                            old_width = publication.width
                            old_height = publication.height

                            # temporarily undo publication flip for easier reading and scale it
                            publication.rotate(-1 * amount_to_rotate)
                            publication.scale(0.25)
                            publication.next_to(pin, direction)

                            slide_animations.append(
                                AnimationGroup(
                                    Create(publication),
                                    self.camera.frame.animate.move_to(
                                        publication.get_center()
                                    ).set(
                                        width=publication.width + 0.5,
                                        height=publication.height + 0.5,
                                    ),
                                    run_time=default_run_time,
                                )
                            )
                            self.play(Succession(*slide_animations))
                            self.wait(1)
                            self.next_slide()

                            self.play(
                                Restore(publication),
                                self.camera.frame.animate.move_to(
                                    publication.get_center()
                                ).set(width=old_width + 2, height=old_height + 2),
                                # rotate with respect to the publication's center
                                # self.camera.frame.animate.rotate(
                                #     amount_to_rotate, axis=np.array([0, 1, 0]), #about_point=publication.get_center()
                                # ).move_to(publication.get_center()).set(
                                #     width=old_width, height=old_height
                                # ),
                            )
                        else:
                            slide_animations.append(Create(publication))

                        # store the publication
                        timeline_lookup[idx].add(publication)

                        if v_group_to_render is not None:
                            v_group_to_render.add(publication)

                        continue  # done with this slide
                else:
                    direction = RIGHT
                    # we assume that the slide is more of a thought experiment/bubble
                    boundary = self.make_boundary_at_coords(direction, vertex_coords)
                    running_offset += boundary.width

                    # store the boundary
                    timeline_lookup[idx].add(boundary)

                    if v_group_to_render is not None:
                        v_group_to_render.add(boundary)

                    slide_animations.append(
                        AnimationGroup(
                            GrowFromPoint(boundary, vertex_coords),
                            self.camera.frame.animate.move_to(vertex_coords).set(
                                width=10
                            ),
                            run_time=default_run_time,
                        )
                    )
                    # uncomment to show a dot at the vertex, but this causes issues
                    # dot = Dot(vertex_coords + (boundary.width * RIGHT), color=BLACK)
                    # self.play(Create(dot, run_time=0.1))

                if play_as_ready:  # has no effect at this time
                    self.play(Succession(*slide_animations))

                self.wait(1)
                self.next_slide()

                ######################################################################
                # the rest of this code is for how to zoom in on certain events/slides
                ######################################################################

                if isinstance(slide, TimelineEvent) or isinstance(slide, PromptSlide):
                    if not slide.skip:
                        # now zoom in on the event
                        self.play(
                            self.camera.frame.animate.move_to(
                                boundary.get_center()
                            ).set(width=boundary.width)
                        )
                else:
                    # now zoom in on the event
                    self.play(
                        self.camera.frame.animate.move_to(boundary.get_center()).set(
                            width=boundary.width
                        )
                    )

                # show the event
                origin_to_draw_at = self.camera.frame.get_center()
                if isinstance(slide, TimelineEvent):
                    event = slide.animation
                    if slide.skip:
                        origin_to_draw_at = boundary.get_center()
                    if isinstance(event, CaptionedSVG) or isinstance(
                        event, CaptionedJPG
                    ):
                        event.draw(
                            origin=origin_to_draw_at, scale=0.25, target_scene=self
                        )
                    else:
                        event.draw(self, origin=origin_to_draw_at, scale=0.25)
                elif isinstance(slide, SlideWithBlocks) or isinstance(
                    slide, SlideWithList
                ):
                    slide.draw(
                        origin=boundary.get_top() - (boundary.height / 10),
                        scale=0.15,
                        target_scene=self,
                    )
                elif isinstance(slide, PromptSlide):
                    if slide.skip:
                        origin_to_draw_at = boundary.get_center()
                    slide.draw(origin=origin_to_draw_at, scale=0.2, target_scene=self)
                else:  # e.g., CLIPDemo
                    # try:
                    slide.draw(origin=origin_to_draw_at, scale=0.25, target_scene=self)
                    # except TypeError:
                    #     print(type(slide), slide)
                    #     raise TypeError("The slide is not a recognized type.")
                # event.draw(self, origin=self.camera.frame.get_center(), scale=0.25)
                self.wait(1)
                self.next_slide()
                # move to the next location
                self.play(
                    self.camera.frame.animate.move_to(origin_to_draw_at).set(width=10)
                )

            if not play_as_ready:
                # create a brace for everything but the line (located at index 0)
                brace = Brace(
                    v_group_to_render[1:],
                    direction=next_brace_direction,
                    color=BLACK,
                    fill_opacity=0.75,
                )
                brace_text = (
                    Text(overview_str, color=BLACK, opacity=0.75)
                    .scale(scale_factor=0.5)
                    .next_to(brace, next_brace_direction)
                )
                v_group_to_render.add(brace)
                v_group_to_render.add(brace_text)
                # alternate brace's direction to avoid overlap if another publication overview comes
                next_brace_direction = (
                    UP if (next_brace_direction == DOWN).all() else DOWN
                )

                # fade in the group of manim objects
                self.play(
                    FadeIn(v_group_to_render, run_time=1),
                    self.camera.frame.animate.move_to(
                        v_group_to_render[1:].get_center()
                    ).set(
                        width=v_group_to_render[1:].width + 2,
                        height=v_group_to_render[1:].height + 2,
                    ),
                )
                # now play everything
                # self.play(Succession(*slide_animations))
                self.wait(1)

                # self.play(Create(brace), Create(brace_text))
                # self.play(self.camera.frame.animate.move_to(brace.get_center()).set(width=10))
                self.next_slide(loop=True)
                # now highlight it
                # self.play(
                #     AnimationGroup(
                #         *[ApplyMethod(obj.set_color, RED) for obj in v_group_to_render]
                #     )
                # )
                self.play(
                    # do not circumscribe:
                    # (1) the line (v_group_to_render[0]), (2) the brace (v_group_to_render[-2])
                    # (3) or the brace's text (v_group_to_render[-1])
                    Circumscribe(v_group_to_render[1:-2], color=MANIM_BLUE, run_time=2)
                )

                self.wait(1)
                self.next_slide()

        self.wait(1)
        self.next_slide()
        self.play(self.camera.frame.animate.set(width=10))
        # self.play(Restore(self.camera.frame, run_time=15))
        # origin_vertex: Dot = timeline.digraph.vertices[0]
        # self.play(
        #     Succession(
        #         Create(origin_vertex),
        #         GrowFromPoint(
        #             self.make_boundary_at_coords(
        #                 direction=LEFT, vertex_coords=origin_vertex.get_center()
        #             ),
        #             origin_vertex.get_center()
        #         ), run_time=2
        #     )
        # )
        # self.play(
        #     Write(
        #         Text(
        #             "Q&A", font="TeX Gyre Termes", color=BLACK
        #         ).move_to(origin_vertex.get_center() + (2 * LEFT))
        #     )
        # )
        self.wait(1)

    @staticmethod
    def make_boundary_at_coords(direction, vertex_coords) -> Rectangle:
        """
        A helper method to create a boundary around the vertex coordinates.

        Args:
            direction: The direction to move the boundary.
            vertex_coords: The coordinates of the vertex to create the boundary around.

        Returns:
            A rectangle boundary around the vertex coordinates.
        """
        return Rectangle(color=BLACK, stroke_width=2).move_to(
            vertex_coords + (2 * direction)
        )

    def greeting(self):
        standby_text = [
            Text(
                "Morphetic Epsilon-Delayed\nNeuro-Fuzzy Networks",
                font="TeX Gyre Termes",
                color=BLACK,
            ),
            Text(
                "A General Architecture for Transparent\nRule-Based Decision-Making",
                font="TeX Gyre Termes",
                color=BLACK,
            ),
            Text("Timeline of Noteworthy Events", font="TeX Gyre Termes", color=BLACK),
            Text("© 2024 John Wesley Hostetter", font="TeX Gyre Termes", color=BLACK),
            # Text(
            #     "Presented by John Wesley Hostetter",
            #     font="TeX Gyre Termes",
            #     color=BLACK,
            # ),
            Text(
                "The presentation will begin shortly.",
                font="TeX Gyre Termes",
                color=BLACK,
            ),
        ]
        indications = [
            Circumscribe,  # (title, color=BLACK),
            ShowPassingFlash,  # (Underline(title)),
            Circumscribe,  # (title, color=BLACK),
            ShowPassingFlash,  # (Underline(title)),
            Circumscribe,  # (title, color=BLACK),
        ]
        self.play(Write(standby_text[0]))
        # self.wait(10)
        self.next_slide(loop=True)
        last_idx: int = -1
        for idx, (message, indication) in enumerate(zip(standby_text, indications)):
            if indication is Circumscribe:
                self.play(indication(message, color=BLACK))
            elif indication is ShowPassingFlash:
                self.play(indication(Underline(message, color=BLACK)))
            else:
                self.play(indication(message))
            self.wait(3)
            last_idx = (idx + 1) % len(standby_text)
            self.play(
                AnimationGroup(
                    FadeOut(message, shift=UP * 1.5),
                    FadeIn(standby_text[last_idx], shift=UP * 1.5),
                )
            )
        self.wait(1)
        self.next_slide()
        self.play(FadeOut(standby_text[last_idx]))


if __name__ == "__main__":
    c = Timeline()
    c.render()
