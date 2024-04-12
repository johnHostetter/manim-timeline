from manim import *

from animations.demos.people.einstein import person_with_quote
from soft.utilities.reproducibility import path_to_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class BertrandRussellQuote(Scene):
    def construct(self):
        # load the PySoft logo as a manim SVGMobject
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
            / "Bertrand_Russell_signature.svg"
        ).scale(0.5)
        person_svg = SVGMobject(
            path_to_project_root()
            / "animations"
            / "demos"
            / "assets"
            / "people"
            / "Bertrand_Russell_1949.svg"
        ).scale(2.0)
        paragraph, person, signature_group = person_with_quote(
            scene,
            person_svg=person_svg,
            quote=(
                '"Vagueness and accuracy are important \n notions, '
                "which it is very necessary \nto understand."
            ),
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1.25,
        )
        return paragraph, person, signature_group


if __name__ == "__main__":
    c = BertrandRussellQuote()
    c.render()
