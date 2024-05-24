from manim import *
from manim_slides import ThreeDSlide

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class BlackBox(ThreeDSlide):
    def construct(self):
        self.greeting()
        self.wait(1)
        black_box_txt = Text('"Black Box"', font_size=36, color=BLACK)
        intro_prefix = Text(
            "A Deep Neural Network is often referred to as a ",
            font_size=36,
            color=BLACK,
        )
        black_box_txt.next_to(intro_prefix, DOWN, buff=0.2)
        intro = VGroup(intro_prefix, black_box_txt)
        intro.to_corner(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(intro)
        self.play(Write(intro), run_time=2)
        self.wait(3)
        self.next_slide()
        blackbox = Cube(
            side_length=3, fill_opacity=1, stroke_width=5, **light_theme_style
        )
        whitebox = Cube(
            side_length=3,
            fill_opacity=0,
            stroke_width=5,
            stroke_color=BLACK,  # background_stroke_color=BLACK
        )

        self.begin_ambient_camera_rotation(rate=0.3)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.play(
            LaggedStart(
                FadeOut(intro_prefix), FadeOut(black_box_txt), lag_ratio=0.8, run_time=5
            ),
            Write(blackbox, run_time=5),
            run_time=5,
        )
        self.wait(1)
        self.next_slide()
        self.simulate_input_output(blackbox)

        question = Text("What's inside the black box?", font_size=36, color=BLACK)
        question.to_corner(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(question)

        self.play(
            Write(question),
            Circumscribe(
                blackbox,
                Rectangle,
                color=ManimColor("#58C4DD"),
                buff=1.0,
                stroke_width=5,
            ),
            run_time=2,
        )

        self.wait(3)
        self.next_slide()
        self.play(FadeOut(question), run_time=2)

        question = Text(
            'What if we could "look inside" the black box?', font_size=36, color=BLACK
        )
        question.to_corner(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(question)

        self.play(
            Write(question),
            TransformMatchingShapes(
                blackbox, whitebox, replace_mobject_with_target_in_scene=True
            ),
            run_time=2,
        )
        self.wait(3)
        self.next_slide()
        self.simulate_input_output(whitebox)
        self.wait(3)
        self.next_slide()
        self.play(FadeOut(question, run_time=2), Uncreate(whitebox, run_time=5))
        self.wait(3)

    def simulate_input_output(self, box: Cube):
        # input going into the black box
        # for outcome_color, outcome_shape in zip([RED, GREEN, BLUE], [Cone, Sphere, Cylinder]):
        for outcome_color, outcome_shape in zip([RED, GREEN], [Cone, Sphere]):
            print(outcome_shape)
            input_arrow = Arrow3D(
                start=np.array([-7, 0, 0]),
                end=np.array([-4, 0, 0]),
                base_radius=0.2,
                thickness=0.1,
                color=ManimColor("#58C4DD"),
            )
            self.play(Create(input_arrow), run_time=2)
            self.wait(1)
            self.next_slide()
            self.play(input_arrow.animate.shift(5.5 * RIGHT), run_time=1)

            # vertex_coords = [
            #     [1, 1, 0],
            #     [1, -1, 0],
            #     [-1, -1, 0],
            #     [-1, 1, 0],
            #     [0, 0, 2]
            # ]
            # faces_list = [
            #     [0, 1, 4],
            #     [1, 2, 4],
            #     [2, 3, 4],
            #     [3, 0, 4],
            #     [0, 1, 2, 3]
            # ]
            # pyramid = Polyhedron(
            #     vertex_coords, faces_list
            # ).set_color(outcome_color).shift(DOWN).scale(0.25)
            # self.play(DrawBorderThenFill(pyramid), run_time=2)
            # self.play(Uncreate(pyramid), run_time=2)

            self.wait(1)
            self.next_slide()
            self.play(
                AnimationGroup(
                    # Succession(
                    # Transform(box, box.copy().set_fill(ORANGE), run_time=0.5),
                    Wiggle(box, run_time=2),
                    # ShowPassingFlash(box, time_width=0.1, run_time=2),
                    # ),
                    # Succession(
                    Transform(
                        input_arrow,
                        outcome_shape().set_color(outcome_color).move_to(input_arrow),
                        run_time=2,
                    ),
                    # Flash(input_arrow, run_time=0.5),
                    # ),
                )
            )

            self.play(
                input_arrow.animate.shift(5.5 * RIGHT).set_color(outcome_color),
                run_time=1,
            )

            self.wait(1)
            self.next_slide()
            self.play(
                Transform(box, box.copy().set_fill(BLACK), run_time=0.5),
                Uncreate(input_arrow, run_time=2),
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
            self.add_fixed_in_frame_mobjects(message)
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
    c = BlackBox()
    c.render()
