from manim import *

from animations.demos.einstein import person_with_quote
from soft.utilities.reproducibility import path_to_project_root


class BertrandRussellQuote(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = ImageMobject("background.png").scale(2).set_color("#FFFFFF")
        self.add(background)

    def construct(self):
        # load the PySoft logo as a manim SVGMobject
        signature = SVGMobject(
            path_to_project_root()
            / "animations"
            / "demos"
            / "signatures"
            / "Bertrand_Russell_signature.svg"
        ).scale(0.5)
        person_svg = SVGMobject(
            path_to_project_root() / "animations" / "demos" / "people" / "Bertrand_Russell_1949.svg"
        ).scale(0.8)
        paragraph, person, signature_group = person_with_quote(
            self,
            person_svg=person_svg,
            quote=(
                '"Vagueness and accuracy are important \n notions, '
                'which it is very necessary \nto understand.'
            ),
            signature=signature,
        )
        self.wait(10)
        self.play(
            FadeOut(Group(VGroup(paragraph, person), signature_group), run_time=2)
        )
        self.wait(2)


if __name__ == "__main__":
    c = BertrandRussellQuote()
    c.render()
