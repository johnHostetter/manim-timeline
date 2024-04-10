from manim import *
from typing import Union as U

from soft.utilities.reproducibility import path_to_project_root


def person_with_quote(
    scene: Scene, path_to_person_svg: Path, quote: str, signature: U[SVGMobject, Text]
):
    # signature = SVGMobject(
    #     path_to_project_root()
    #     / "animations"
    #     / "demos"
    #     / "Albert_Einstein_signature_1934.svg"
    # ).scale(0.5)
    person = SVGMobject(path_to_person_svg)
    paragraph = (
        Paragraph(quote, font="TeX Gyre Termes", slant=ITALIC, color=BLACK)
        .scale(0.7)
        .next_to(signature, UP)
    )
    paragraph.move_to(ORIGIN)
    person.move_to(paragraph, ((4 * DOWN) + (8 * LEFT))).scale(2)
    scene.play(Write(paragraph), run_time=3)

    scene.play(paragraph.animate.shift(RIGHT * 2), run_time=1)
    scene.play(Create(person, run_time=3))

    signature_dash = (
        Text("- ", font="TeX Gyre Termes")
        .scale(2)
        .next_to(signature, LEFT)
        # .next_to(paragraph, (1.5 * DOWN) + RIGHT)
        .set_color(BLACK)
    )
    VGroup(signature_dash, signature).next_to(VGroup(paragraph, person), DOWN)
    # signature.next_to(signature_dash, RIGHT).set_color(BLACK)

    # add the signature to the scene
    scene.play(Create(VGroup(signature_dash, signature), run_time=2))
    return paragraph, person, VGroup(signature_dash, signature)


class EinsteinQuote(Scene):
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
            / "Albert_Einstein_signature_1934.svg"
        ).scale(0.5)
        paragraph, person, signature_group = person_with_quote(
            self,
            path_to_person_svg=(
                path_to_project_root() / "animations" / "demos" / "Albert_Einstein.svg"
            ),
            quote=(
                '"So far as the laws of mathematics refer to reality,\nthey are not certain. '
                'And so far as they are certain, \nthey do not refer to reality."'
            ),
            signature=signature,
        )
        self.wait(10)
        self.play(
            FadeOut(Group(VGroup(paragraph, person), signature_group), run_time=2)
        )
        self.wait(2)

        # person = SVGMobject(
        #     path_to_project_root()
        #     / "animations"
        #     / "demos"
        #     / "Albert_Einstein.svg"
        # ).scale(2)
        # quote = (
        #     Paragraph(
        #         "\"So far as the laws of mathematics refer to reality,\nthey are not certain. "
        #         "And so far as they are certain, \nthey do not refer to reality.\"",
        #         font="TeX Gyre Termes",
        #         slant=ITALIC,
        #         color=BLACK,
        #     )
        #     .scale(0.7)
        #     .next_to(signature, UP)
        # )
        # quote.move_to(ORIGIN)
        # person.move_to(quote, ((4 * DOWN) + (8 * LEFT)))
        #
        # # introduction.set_color("#000000")
        # # introduction.set_stroke(width=1.0)  # uncomment to add a stroke to the text
        # # introduction.set_fill("#FFFFFF")
        # self.play(Write(quote), run_time=3)
        #
        # self.play(quote.animate.shift(RIGHT * 2), run_time=1)
        # self.play(Create(person, run_time=3))

        # Text("- Albert Einstein", font="TeX Gyre Termes").scale(0.7).next_to(quote, DOWN).set_color(BLACK)
        # signature_dash = (
        #     Text("- ", font="TeX Gyre Termes")
        #     .scale(0.7)
        #     .next_to(quote, (1.5 * DOWN) + LEFT)
        #     .set_color(BLACK)
        # )
        # signature.next_to(signature_dash, RIGHT).set_color(BLACK)
        #
        # # add the signature to the scene
        # self.play(Create(VGroup(signature_dash, signature), run_time=2))
        # self.wait(10)
        # self.play(FadeOut(Group(quote, signature), run_time=2))
        # self.wait(2)


if __name__ == "__main__":
    c = EinsteinQuote()
    c.render()
