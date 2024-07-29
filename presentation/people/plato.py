from manim import *

from manim_timeline.quotes import quotable_person
from manim_timeline.utils import get_project_root


config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class PlatoTheoryOfForms(MovingCameraScene):
    def construct(self):
        # paragraph, source, person, person_svg, signature_group = self.quote(
        #     self, origin=ORIGIN, scale=1.0
        # )
        # self.wait(10)
        # self.play(
        #     FadeOut(Group(paragraph, signature_group), run_time=2),
        #     ReplacementTransform(person_svg, bust_svg),
        # )
        # self.wait(2)
        self.draw(self, origin=ORIGIN, scale=1.0)

    @staticmethod
    def draw(scene, origin, scale, animate: bool = True):
        bust_svg = SVGMobject(
            get_project_root() / "assets" / "people" / "plato_bust.svg"
        ).scale(2.5)

        header = Text(
            "Plato's Theory of Forms", font="TeX Gyre Termes", color=BLACK, font_size=60
        ).next_to(bust_svg, RIGHT)

        sub_header = Text(
            "The Allegory of the Cave",
            font="TeX Gyre Termes",
            color=BLACK,
            slant=ITALIC,
            font_size=40,
        )

        cave = SVGMobject(
            get_project_root() / "assets" / "plato_cave_colored.svg"
        ).scale(2.5)

        VGroup(header, sub_header.next_to(header, DOWN)).to_corner(UP, buff=0.5)
        cave.next_to(bust_svg, RIGHT).next_to(sub_header, DOWN)

        all_content = (
            VGroup(header, sub_header, bust_svg, cave)
            .scale(scale_factor=scale)
            .move_to(origin)
        )

        if animate:
            scene.play(
                Write(VGroup(header, sub_header), run_time=3),
                Create(bust_svg, run_time=5),
                Create(cave, run_time=5),
            )
        else:
            scene.add(all_content)

        # imperfect_circle = SVGMobject(
        #     path_to_project_root()
        #     / "assets"
        #     / "imperfect_circle.svg"
        # ).scale(2.5)
        # perfect_circle = Circle(
        #     radius=imperfect_circle.height / 2, color=BLACK
        # ).next_to(imperfect_circle, RIGHT, buff=0.75)
        #
        # VGroup(imperfect_circle, perfect_circle).scale(scale_factor=scale).move_to(
        #     origin
        # )

        # scene.next_slide()
        # scene.compare_imperfect_with_form(cave, imperfect_circle, perfect_circle)
        # scene.wait(1)

        # imperfect_sphere = SVGMobject(
        #     path_to_project_root() / "animations" / "demos" / "Earth.svg"
        # ).scale(2.5)
        #
        # perfect_sphere = Sphere(
        #     radius=perfect_circle.radius, color=BLACK
        # ).next_to(perfect_circle, DOWN, buff=0.75)
        #
        # # self.set_camera_orientation(phi=PI / 6, theta=PI / 6)
        #
        # self.compare_imperfect_with_form(
        #     VGroup(imperfect_circle, perfect_circle), imperfect_sphere, perfect_sphere
        # )

        # earth = SVGMobject(
        #     path_to_project_root() / "animations" / "demos" / "Earth.svg"
        # )

        # self.play(Create(earth, run_time=3))

    @staticmethod
    def quote(scene, origin, scale, animate=True):
        signature = Text(
            "Πλάτων (Plato)", font="TeX Gyre Termes", color=BLACK
        )  # .scale(0.7)
        person_svg = SVGMobject(
            get_project_root() / "assets" / "people" / "plato.svg"
        ).scale(2.0)
        paragraph, source, person, signature_group = quotable_person(
            scene,
            person_svg=person_svg,
            quote=(
                '"Reality is created by the mind, we can \n'
                'change our reality by changing our mind."'
            ),
            source="(Attributed to Plato)",
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1.0,
            animate=True,
        )
        return paragraph, source, person, person_svg, signature_group

    def compare_imperfect_with_form(
        self, last_object, imperfect_object, perfect_object
    ):
        # draw an imperfect circle
        # imperfect_circle = SVGMobject(
        #     path_to_project_root() / "animations" / "demos" / "imperfect_circle.svg"
        # ).scale(2.5)
        imperfect_object.next_to(last_object, DOWN).shift(DOWN)
        perfect_object.next_to(imperfect_object, RIGHT, buff=0.75)
        # move the camera to focus on the imperfect circle
        self.play(
            self.camera.frame.animate.move_to(imperfect_object.get_center()).set(
                height=imperfect_object.height * 1.5
            )
        )
        self.play(Create(imperfect_object, run_time=5))
        imperfect_circle_lbl = (
            Text("Reality", font="TeX Gyre Termes", color=BLACK)
            .scale(0.7)
            .next_to(imperfect_object, DOWN)
        )
        self.play(Write(imperfect_circle_lbl))
        # draw a perfect circle
        # perfect_circle = Circle(
        #     radius=imperfect_circle.height / 2, color=BLACK
        # ).next_to(imperfect_circle, RIGHT, buff=0.75)
        perfect_circle_lbl = (
            Text("Form", font="TeX Gyre Termes", color=BLACK)
            .scale(0.7)
            .next_to(perfect_object, DOWN)
        )
        circles = VGroup(imperfect_object, perfect_object)
        self.play(
            self.camera.frame.animate.move_to(circles.get_center()).set(
                height=circles.height * 1.5
            )
        )
        self.play(Create(perfect_object, run_time=5))
        self.play(Write(perfect_circle_lbl))
        # write out the formula for a circle
        formula = MathTex(r"x^2 + y^2 = r^2", color=BLACK).next_to(
            VGroup(circles, imperfect_circle_lbl, perfect_circle_lbl), DOWN
        )
        self.play(
            self.camera.frame.animate.move_to(
                VGroup(circles, formula).get_center()
            ).set(height=VGroup(circles, formula).height * 1.5)
        )
        self.play(Write(formula, run_time=3))


if __name__ == "__main__":
    c = PlatoTheoryOfForms()
    c.render()
