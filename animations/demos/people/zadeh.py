from manim import *

from animations.demos.people.einstein import person_with_quote
from soft.utilities.reproducibility import path_to_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class Zadeh(Scene):
    def construct(self):
        paragraph, source, person, signature_group = self.draw(self, origin=ORIGIN, scale=1.0)
        self.wait(10)
        self.play(
            FadeOut(Group(VGroup(paragraph, source, person), signature_group), run_time=2)
        )
        self.wait(2)

    @staticmethod
    def draw(scene, origin, scale):
        signature = Text(
            "Lotfi A. Zadeh", font="TeX Gyre Termes", color=BLACK
        )  # .scale(0.7)
        person_svg = SVGMobject(
            path_to_project_root()
            / "animations"
            / "demos"
            / "assets"
            / "people"
            / "Lotfi-Zadeh-in-the-year-1958-a-young-professor-of-Electrical-Engineering-in-New-York-3_W640.svg"
        ).scale(2.0)
        paragraph, source, person, signature_group = person_with_quote(
            scene,
            person_svg=person_svg,
            quote=(
                # '"As complexity rises, precise statements \nlose meaning '
                # 'and meaningful \nstatements lose precision."'
                "\"Fuzzy logic is not fuzzy. Basically, fuzzy logic is a \n"
                "precise logic of imprecision and approximate \nreasoning.\""
            ),
            # source="(Is there a need for fuzzy logic?, 2008)",
            source="(Zadeh, 2008)",
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1.25,
        )
        return paragraph, source, person, signature_group


if __name__ == "__main__":
    c = Zadeh()
    c.render()
