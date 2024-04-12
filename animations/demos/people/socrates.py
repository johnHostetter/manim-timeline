from manim import *

from animations.demos.people.einstein import person_with_quote
from soft.utilities.reproducibility import path_to_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class Socrates(Scene):
    def construct(self):
        paragraph, person, signature_group = self.draw(self, origin=ORIGIN, scale=1.0)
        self.wait(10)
        self.play(
            FadeOut(Group(VGroup(paragraph, person), signature_group), run_time=2)
        )
        self.wait(2)

    @staticmethod
    def draw(scene, origin, scale):
        signature = Text(
            "Σωκράτης (Socrates)", font="TeX Gyre Termes", color=BLACK
        )  # .scale(0.7)
        person_svg = SVGMobject(
            path_to_project_root()
            / "animations"
            / "demos"
            / "assets"
            / "people"
            / "socrates.svg"
        ).scale(2.0)
        paragraph, person, signature_group = person_with_quote(
            scene,
            person_svg=person_svg,
            quote=(
                '"The unexamined life is not worth living \nfor a human being."\n\n\n"The beginning of wisdom is a \ndefinition of terms."'
            ),
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1.0,
        )
        return paragraph, person, signature_group


if __name__ == "__main__":
    c = Socrates()
    c.render()
