from manim import *

from animations.demos.einstein import person_with_quote
from soft.utilities.reproducibility import path_to_project_root


config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class PlatoTheoryOfForms(MovingCameraScene):
    def construct(self):
        signature = Text(
            "Πλάτων (Plato)", font="TeX Gyre Termes", color=BLACK
        )#.scale(0.7)

        person_svg = SVGMobject(
            path_to_project_root() / "animations" / "demos" / "Plato.svg"
        )

        paragraph, person, signature_group = person_with_quote(
            self,
            person_svg=person_svg,
            quote=(
                "\"Reality is created by the mind, we can \n"
                "change our reality by changing our mind.\""
            ),
            signature=signature,
        )

        self.wait(10)
        self.play(
            FadeOut(
                Group(
                    paragraph,
                    signature_group
                ), run_time=2
            )
        )
        self.wait(2)

        header = Text(
            "Plato's Theory of Forms", font="TeX Gyre Termes", color=BLACK
        ).scale(1.0)
        header.next_to(person, RIGHT)
        self.wait(2)
        subheader = Text(
            "The Allegory of the Cave", font="TeX Gyre Termes", color=BLACK
        ).scale(0.7)

        cave = SVGMobject(
            path_to_project_root() / "animations" / "demos" / "images" / "plato_cave_colored.svg"
        ).scale(2.5)

        VGroup(header, subheader.next_to(header, DOWN)).to_corner(UP, buff=0.5)
        cave.next_to(person, RIGHT).next_to(subheader, DOWN)

        self.play(Write(VGroup(header, subheader), run_time=3), Create(cave, run_time=5))

        imperfect_circle = SVGMobject(
            path_to_project_root() / "animations" / "demos" / "imperfect_circle.svg"
        ).scale(2.5)
        perfect_circle = Circle(
            radius=imperfect_circle.height / 2, color=BLACK
        ).next_to(imperfect_circle, RIGHT, buff=0.75)

        self.compare_imperfect_with_form(cave, imperfect_circle, perfect_circle)

        self.wait(5)

        imperfect_sphere = SVGMobject(
            path_to_project_root() / "animations" / "demos" / "Earth.svg"
        ).scale(2.5)

        perfect_sphere = Sphere(
            radius=perfect_circle.radius, color=BLACK
        ).next_to(perfect_circle, DOWN, buff=0.75)

        # self.set_camera_orientation(phi=PI / 6, theta=PI / 6)

        self.compare_imperfect_with_form(
            VGroup(imperfect_circle, perfect_circle), imperfect_sphere, perfect_sphere
        )

        # earth = SVGMobject(
        #     path_to_project_root() / "animations" / "demos" / "Earth.svg"
        # )

        # self.play(Create(earth, run_time=3))

    def compare_imperfect_with_form(self, last_object, imperfect_object, perfect_object):
        # draw an imperfect circle
        # imperfect_circle = SVGMobject(
        #     path_to_project_root() / "animations" / "demos" / "imperfect_circle.svg"
        # ).scale(2.5)
        imperfect_object.next_to(last_object, DOWN).shift(DOWN)
        perfect_object.next_to(imperfect_object, RIGHT, buff=0.75)
        # move the camera to focus on the imperfect circle
        self.play(
            self.camera.frame.animate.move_to(
                imperfect_object.get_center()
            ).set(height=imperfect_object.height * 1.5)
        )
        self.play(Create(imperfect_object, run_time=5))
        imperfect_circle_lbl = Text(
            "Reality", font="TeX Gyre Termes", color=BLACK
        ).scale(0.7).next_to(imperfect_object, DOWN)
        self.play(Write(imperfect_circle_lbl))
        # draw a perfect circle
        # perfect_circle = Circle(
        #     radius=imperfect_circle.height / 2, color=BLACK
        # ).next_to(imperfect_circle, RIGHT, buff=0.75)
        perfect_circle_lbl = Text(
            "Idea", font="TeX Gyre Termes", color=BLACK
        ).scale(0.7).next_to(perfect_object, DOWN)
        circles = VGroup(imperfect_object, perfect_object)
        self.play(
            self.camera.frame.animate.move_to(
                circles.get_center()
            ).set(height=circles.height * 1.5)
        )
        self.play(Create(perfect_object, run_time=5))
        self.play(Write(perfect_circle_lbl))
        # write out the formula for a circle
        formula = MathTex(
            r"x^2 + y^2 = r^2", color=BLACK
        ).next_to(VGroup(circles, imperfect_circle_lbl, perfect_circle_lbl), DOWN)
        self.play(
            self.camera.frame.animate.move_to(
                VGroup(circles, formula).get_center()
            ).set(height=VGroup(circles, formula).height * 1.5)
        )
        self.play(Write(formula, run_time=3))


if __name__ == "__main__":
    c = PlatoTheoryOfForms()
    c.render()
