from manim import *

from manim_timeline.utils import get_project_root
from manim_timeline.quotes import quotable_person

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class Einstein(Scene):
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
        signature = SVGMobject(
            get_project_root()
            / "assets"
            / "signatures"
            / "Albert_Einstein_signature_1934.svg"
        ).scale(0.5)
        person_svg = SVGMobject(
            get_project_root() / "assets" / "people" / "Einstein1.svg"
        ).scale(2.0)
        paragraph, source, person, signature_group = quotable_person(
            scene,
            person_svg=person_svg,
            quote=(
                '"As far as the laws of mathematics refer to reality,\nthey are not certain; '
                'And as far as they are certain, \nthey do not refer to reality."'
            ),
            # originally published in 1921 as a lecture delivered by Einstein at the Prussian Academy of Sciences
            source="(Geometry and Experience, 1921)",
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1,
            animate=animate,
        )
        return paragraph, source, person, signature_group


if __name__ == "__main__":
    c = Einstein()
    c.render()
