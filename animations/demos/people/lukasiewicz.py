from manim import *
from manim_slides import Slide

from animations.demos.people.einstein import person_with_quote
from soft.utilities.reproducibility import path_to_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class Lukasiewicz(Slide):
    def construct(self):
        paragraph, source_text, person, signature_group = self.draw(
            self, origin=ORIGIN, scale=1.0
        )
        self.wait(10)
        self.play(
            FadeOut(Group(VGroup(paragraph, person), signature_group), run_time=2)
        )
        self.wait(2)

    @staticmethod
    def draw(scene, origin, scale, animate: bool = True):
        signature = Text(
            "Jan Łukasiewicz", font="TeX Gyre Termes", color=BLACK
        )  # .scale(0.7)
        person_svg = SVGMobject(
            path_to_project_root()
            / "animations"
            / "demos"
            / "assets"
            / "people"
            / "Jan_Łukasiewicz.svg"
            # / "kurt_godel.svg",
            # color=BLACK,
            # fill_color=WHITE,
            # stroke_color=BLACK
        ).scale(2.0)
        paragraph, source_text, person, signature_group = person_with_quote(
            scene,
            person_svg=person_svg,
            quote=(
                """
                \"Therefore the proposition considered is at 
                the moment neither true nor false and 
                must possess a third value, different 
                from “0” or falsity and “1” or truth. 
                This value we can designate by “1/2”. 
                It represents “the possible,” and joins 
                “the true” and “the false” as a third value.\"
                """
            ),
            # https://builds.openlogicproject.org/content/many-valued-logic/three-valued-logics/three-valued-logics.pdf
            source="(On Three-Valued Logic, 1921)",
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1.25,
            animate=animate,
        )
        return paragraph, source_text, person, signature_group


if __name__ == "__main__":
    c = Lukasiewicz()
    c.render()
