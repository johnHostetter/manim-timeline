from manim import *
from manim_slides import Slide

from animations.demos.people.einstein import person_with_quote
from soft.utilities.reproducibility import path_to_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class BertrandRussellQuote(Slide):
    def construct(self):
        # load the PySoft logo as a manim SVGMobject
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
            path_to_project_root()
            / "animations"
            / "demos"
            / "assets"
            / "signatures"
            / "Bertrand_Russell_signature.svg"
        ).scale(0.5)
        person_svg = SVGMobject(
            path_to_project_root()
            / "animations"
            / "demos"
            / "assets"
            / "people"
            / "Bertrand_Russell_1949.svg"
        ).scale(2.0)
        paragraph, source, person, signature_group = person_with_quote(
            scene,
            person_svg=person_svg,
            quote=(
                '"All traditional logic habitually assumes that \nprecise symbols are being employed. '
                "It is \ntherefore not applicable to this terrestrial life, \n"
                'but only to an imagined celestial existence."'
                # '"Vagueness and accuracy are important \n notions, '
                # 'which it is very necessary \nto understand."'
            ),
            # http://astrofrelat.fcaglp.unlp.edu.ar/filosofia_cientifica/media/papers/Russell-Vagueness.pdf
            source="(Vagueness, 1923)",
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1.25,
            animate=animate,
        )
        # all quotes are from:
        # http://astrofrelat.fcaglp.unlp.edu.ar/filosofia_cientifica/media/papers/Russell-Vagueness.pdf
        quote_1 = (
            '"The law of excluded middle is true when \nprecise symbols are employed, '
            'but it is \nnot true when symbols are vague, as, \nin fact, all symbols are."'
        )
        quote_2 = (
            '"Vagueness, clearly, is a matter of degree, \ndepending upon the extent of '
            "the possible \ndifferences between different systems \nrepresented by the same "
            'representation. \nAccuracy, on the contrary, is an ideal limit."'
        )
        paragraph_1 = (
            Text(quote_1, font="TeX Gyre Termes", color=BLACK, slant=ITALIC)
            .scale(0.7)
            .scale(scale_factor=scale)
            .move_to(paragraph.get_center())
            .next_to(source, UP)
        )
        paragraph_2 = (
            Text(quote_2, font="TeX Gyre Termes", color=BLACK, slant=ITALIC)
            .scale(0.7)
            .scale(scale_factor=scale)
            .move_to(paragraph.get_center())
            .next_to(source, UP)
        )
        if animate:
            # cycle through some other quotes
            scene.wait(1)
            scene.next_slide()
            scene.play(
                Transform(
                    paragraph, paragraph_1, replace_mobject_with_target_in_scene=True
                )
            )
            scene.wait(2)
            scene.next_slide()
            scene.play(
                Transform(
                    paragraph_1, paragraph_2, replace_mobject_with_target_in_scene=True
                )
            )
        return paragraph, source, person, signature_group


if __name__ == "__main__":
    c = BertrandRussellQuote()
    c.render()
