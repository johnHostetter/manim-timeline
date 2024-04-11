from manim import *

from animations.demos.einstein import person_with_quote
from soft.utilities.reproducibility import path_to_project_root


class MaxBlack(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = ImageMobject("background.png").scale(2).set_color("#FFFFFF")
        self.add(background)

    def construct(self):
        # load the PySoft logo as a manim SVGMobject
        signature = Text(
            "Max Black", font="TeX Gyre Termes", color=BLACK
        )#.scale(0.7)

        person_svg = SVGMobject(
            path_to_project_root() / "animations" / "demos" / "people" / "MaxBlack.svg"
        )

        paragraph, person, signature_group = person_with_quote(
            self,
            person_svg=person_svg,
            quote=(
                '"It is a paradox, whose importance \nfamiliarity fails to diminish, \nthat '
                'the most highly developed \nand useful scientific theories are \nostensibly '
                'expressed in terms of \nobjects never encountered in experience."'
            ),
            signature=signature,
        )
        self.wait(10)
        self.play(
            FadeOut(Group(VGroup(paragraph, person), signature_group), run_time=2)
        )
        self.wait(2)


if __name__ == "__main__":
    c = MaxBlack()
    c.render()
