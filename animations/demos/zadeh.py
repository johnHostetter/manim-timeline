from manim import *

from animations.demos.einstein import person_with_quote
from soft.utilities.reproducibility import path_to_project_root


class Zadeh(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = ImageMobject("background.png").scale(2).set_color("#FFFFFF")
        self.add(background)

    def construct(self):
        # load the PySoft logo as a manim SVGMobject
        signature = Text(
            "Lotfi A. Zadeh", font="TeX Gyre Termes", color=BLACK
        )#.scale(0.7)

        person_svg = SVGMobject(
            path_to_project_root() / "animations" / "demos" / "people" / "Lotfi-Zadeh-in-the-year-1958-a-young-professor-of-Electrical-Engineering-in-New-York-3_W640.svg"
        ).scale(0.8)

        paragraph, person, signature_group = person_with_quote(
            self,
            person_svg=person_svg,
            quote=(
                '"As complexity rises, precise statements \nlose meaning '
                'and meaningful \nstatements lose precision."'
            ),
            signature=signature,
        )
        self.wait(10)
        self.play(
            FadeOut(Group(VGroup(paragraph, person), signature_group), run_time=2)
        )
        self.wait(2)


if __name__ == "__main__":
    c = Zadeh()
    c.render()
