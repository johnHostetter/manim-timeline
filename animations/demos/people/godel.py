from manim import *

from animations.demos.people.einstein import person_with_quote
from soft.utilities.reproducibility import path_to_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class GodelQuote(Scene):
    def construct(self):
        paragraph, person, signature_group = self.draw(self, origin=ORIGIN, scale=1.0)
        self.wait(10)
        self.play(
            FadeOut(Group(VGroup(paragraph, person), signature_group), run_time=2)
        )
        self.wait(2)

    @staticmethod
    def draw(scene, origin, scale):
        signature = SVGMobject(
            path_to_project_root()
            / "animations"
            / "demos"
            / "assets"
            / "signatures"
            / "Kurt_Gödel_signature.svg",
            # color=WHITE
        ).scale(1.0)
        person_svg = SVGMobject(
            path_to_project_root()
            / "animations"
            / "demos"
            / "assets"
            / "people"
            / "Young_Kurt_Gödel_as_a_student_in_1925.svg"
            # / "kurt_godel.svg",
            # color=BLACK,
            # fill_color=WHITE,
            # stroke_color=BLACK
        ).scale(2.0)
        paragraph, person, signature_group = person_with_quote(
            scene,
            person_svg=person_svg,
            quote=(
                '"The more I think about language,\nthe more it amazes me that people\never understand each other at all."'
                # '"So far as the laws of mathematics refer to reality,\nthey are not certain. '
                # 'And so far as they are certain, \nthey do not refer to reality."'
            ),
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1.25,
        )
        return paragraph, person, signature_group


if __name__ == "__main__":
    c = GodelQuote()
    c.render()
