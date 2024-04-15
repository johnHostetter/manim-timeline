import igraph as ig
from manim import *
from manim_slides import Slide

from animations.beamer.slides import SlideWithBlocks, PromptSlide
from animations.demos.graph_example import GraphPair
from animations.demos.timeline_helper import get_noteworthy_events, TimelineEvent
from animations.demos.ww2 import CaptionedSVG

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
        num_of_vertices = len(timeline_events) + 1
        timeline_igraph.add_vertices(num_of_vertices)
        # timeline_igraph.vs["name"] = ["2010", "2015", "2020", "2025", "2030"]

        edges = list(zip(range(0, num_of_vertices - 1), range(1, num_of_vertices)))

        timeline_igraph.add_edges(edges)

        # consistent spacing for the timeline
        spacing = 5  # a good spacing for the timeline I found works well
        digraph_layout = {idx: (idx * spacing, 0, 0) for idx in range(num_of_vertices)}
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
        self.camera.frame.save_state()

        # start_loc = timeline.digraph.vertices[0].get_center()
        # end_loc = timeline.digraph.vertices[num_of_vertices - 1].get_center()
        source_vertex_idx = 0
        source_vertex = timeline.digraph.vertices[source_vertex_idx]
        self.play(Create(source_vertex.set_opacity(0.0)))
        self.play(self.camera.frame.animate.move_to(source_vertex).set(width=10))

        running_offset: float = (
            0  # offset for the timeline events to account for thought slides
        )
        for idx, edge in enumerate(edges):
            slide = timeline_events[idx]
            source_vertex_idx, target_vertex_idx = edge[0], edge[1]
            target_vertex = timeline.digraph.vertices[target_vertex_idx]

            line: Line = timeline.digraph.edges[edge[0], edge[1]]
            # apply a slight offset to the target vertex, to account for the thought slides, if any
            if running_offset > 0:
                target_vertex.shift(running_offset * RIGHT)
                line.shift(running_offset * RIGHT)
            self.play(Create(line), self.camera.frame.animate.move_to(target_vertex))
            self.play(Create(target_vertex))

            vertex_coords = target_vertex.get_center()

            if isinstance(slide, TimelineEvent):
                # draw a time-stamped event from the timeline
                direction = UP if idx % 2 == 0 else DOWN
                # source_vertex_idx, target_vertex_idx = edge[0], edge[1]
                # target_vertex = timeline.digraph.vertices[target_vertex_idx]
                # line: Line = timeline.digraph.edges[edge[0], edge[1]]
                # self.play(Create(line), self.camera.frame.animate.move_to(target_vertex))
                # self.play(Create(target_vertex))
                # self.play(self.camera.frame.animate.move_to(target_vertex).set(width=0.075))

                # vertex_coords = target_vertex.get_center()
                pin: Line = Line(vertex_coords, vertex_coords + direction, color=BLACK)

                self.play(
                    Create(pin),
                    self.camera.frame.animate.move_to(vertex_coords + direction).set(
                        width=10
                    ),
                )
                boundary = Rectangle(color=BLACK).move_to(
                    vertex_coords + (2 * direction)
                )
                self.play(Create(boundary))
                if slide.poi is not None:  # point of interest takes precedence
                    timestamp_str = f"{slide.poi} {slide.era_notation}"
                elif slide.start_year == slide.end_year:
                    timestamp_str = f"{slide.start_year} {slide.era_notation}"
                else:
                    timestamp_str = (
                        f"{slide.start_year} - {slide.end_year} {slide.era_notation}"
                    )
                timestamp = Text(
                    timestamp_str,
                    font="TeX Gyre Termes",
                    color=BLACK,
                ).next_to(boundary, direction)
                self.play(Create(timestamp))
            else:
                direction = RIGHT
                # we assume that the slide is more of a thought experiment/bubble
                boundary = Rectangle(color=BLACK).move_to(
                    vertex_coords + (2 * direction)
                )
                running_offset += boundary.width
                self.play(
                    GrowFromPoint(boundary, vertex_coords),
                    self.camera.frame.animate.move_to(vertex_coords).set(width=10),
                )
                # dot = Dot(vertex_coords + (boundary.width * RIGHT), color=BLACK)
                # self.play(Create(dot, run_time=0.1))

            self.wait(2)
            self.next_slide()

            if isinstance(slide, TimelineEvent) or isinstance(slide, PromptSlide):
                if not slide.skip:
                    # now zoom in on the event
                    self.play(
                        self.camera.frame.animate.move_to(boundary.get_center()).set(
                            width=boundary.width
                        )
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
                if isinstance(event, CaptionedSVG):
                    event.draw(origin=origin_to_draw_at, scale=0.25, target_scene=self)
                else:
                    event.draw(self, origin=origin_to_draw_at, scale=0.25)
            elif isinstance(slide, SlideWithBlocks):
                slide.draw(
                    origin=boundary.get_top() - (boundary.height / 10),
                    scale=0.2,
                    target_scene=self,
                )
            elif isinstance(slide, PromptSlide):
                if slide.skip:
                    origin_to_draw_at = boundary.get_center()
                slide.draw(origin=origin_to_draw_at, scale=0.2, target_scene=self)
            else:
                slide.draw(origin=origin_to_draw_at, scale=0.25, target_scene=self)
            # event.draw(self, origin=self.camera.frame.get_center(), scale=0.25)
            self.next_slide()
            # move to the next location
            self.play(
                self.camera.frame.animate.move_to(target_vertex.get_center()).set(
                    width=timeline.digraph.width
                )
            )

        self.play(Restore(self.camera.frame))
        # self.play(Create(timeline.digraph, run_time=1))
        self.wait(10)

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
        self.next_slide()
        self.play(FadeOut(standby_text[last_idx]))


if __name__ == "__main__":
    c = Timeline()
    c.render()
