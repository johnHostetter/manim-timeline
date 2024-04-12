from manim import *

from animations.demos.people.einstein import person_with_quote
from soft.utilities.reproducibility import path_to_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class Aristotle(Scene):
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
            "Ἀριστοτέλης (Aristotle)", font="TeX Gyre Termes", color=BLACK
        )  # .scale(0.7)
        person_svg = SVGMobject(
            path_to_project_root()
            / "animations"
            / "demos"
            / "assets"
            / "people"
            / "aristotle-2.svg"
        ).scale(2.0)
        paragraph, person, signature_group = person_with_quote(
            scene,
            person_svg=person_svg,
            quote=(
                "All people are mortal. \nSocrates is a person. \nTherefore, Socrates is mortal."
            ),
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1.0,
        )
        return paragraph, person, signature_group


if __name__ == "__main__":
    c = Aristotle()
    c.render()
