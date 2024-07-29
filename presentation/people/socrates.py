from manim import *

from manim_timeline.utils import get_project_root
from manim_timeline.quotes import quotable_person

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class Socrates(Scene):
    def construct(self):
        paragraph, source, person, signature_group = self.draw(
            self, origin=ORIGIN, scale=1.0
        )
        self.wait(10)
        self.play(
            FadeOut(Group(VGroup(paragraph, person), signature_group), run_time=2)
        )
        self.wait(2)

    @staticmethod
    def draw(scene, origin, scale, animate=True):
        signature = Text(
            "Σωκράτης (Socrates)", font="TeX Gyre Termes", color=BLACK
        )  # .scale(0.7)
        person_svg = SVGMobject(
            get_project_root() / "assets" / "people" / "socrates.svg"
        ).scale(2.0)
        paragraph, source, person, signature_group = quotable_person(
            scene,
            person_svg=person_svg,
            quote=(
                '"The unexamined life is not worth living \nfor a human being."\n\n\nThe beginning of wisdom is a \ndefinition of terms.'
            ),
            source="(Plato's Apology, 399 BCE) & (Plato's Charmides [paraphrased])",
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1.0,
            animate=animate,
        )
        return paragraph, source, person, signature_group


if __name__ == "__main__":
    c = Socrates()
    c.render()
