from manim import *

from manim_timeline.utils import get_project_root
from manim_timeline.quotes import quotable_person

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class MaxBlack(Scene):
    def construct(self):
        paragraph, source, person, signature_group = self.draw(
            self, origin=ORIGIN, scale=1.0
        )
        self.wait(10)
        self.play(
            FadeOut(
                Group(VGroup(paragraph, source, person), signature_group), run_time=2
            )
        )
        self.wait(2)

    @staticmethod
    def draw(scene, origin, scale, animate: bool = True):
        signature = Text(
            "Max Black", font="TeX Gyre Termes", color=BLACK
        )  # .scale(0.7)
        person_svg = SVGMobject(
            get_project_root() / "assets" / "people" / "MaxBlack.svg"
        ).scale(2.0)
        paragraph, source, person, signature_group = quotable_person(
            scene,
            person_svg=person_svg,
            quote=(
                '"It is a paradox, whose importance \nfamiliarity fails to diminish, \nthat '
                "the most highly developed \nand useful scientific theories are \nostensibly "
                'expressed in terms of \nobjects never encountered in experience."'
            ),
            source="(Vagueness. An Exercise in Logical Analysis, 1937)",
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1.5,
            animate=animate,
        )
        return paragraph, source, person, signature_group


if __name__ == "__main__":
    c = MaxBlack()
    c.render()
