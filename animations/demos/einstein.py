import numpy as np
from manim import *
from typing import Union as U

from soft.utilities.reproducibility import path_to_project_root


def person_with_quote(
        scene: Scene,
        person_svg: SVGMobject,
        quote: str,
        signature: U[SVGMobject, Text],
        origin: np.ndarray,
        scale: float,
        left_shift: float = 0.5,
):
    # signature = SVGMobject(
    #     path_to_project_root()
    #     / "animations"
    #     / "demos"
    #     / "Albert_Einstein_signature_1934.svg"
    # ).scale(0.5)
    # person = SVGMobject(path_to_person_svg)
    paragraph = (
        Paragraph(quote, font="TeX Gyre Termes", slant=ITALIC, color=BLACK)
        .scale(0.7)
        .next_to(signature, UP)
    )
    person_and_quote = VGroup(paragraph, person_svg)
    person_and_quote.scale(scale_factor=scale)
    # person_bound = person_svg.get_bounding_box()
    # person_svg.next_to(paragraph, scale*LEFT, buff=0.0*scale)
    person_svg.move_to(paragraph, aligned_edge=LEFT).shift(person_svg.width * left_shift * LEFT)
    person_and_quote.move_to(origin)
    # person_svg.move_to(paragraph, ((4 * DOWN) + (12 * LEFT))).scale(2)
    scene.play(Write(paragraph), run_time=3)

    # scene.play(paragraph.animate.shift(RIGHT * 2), run_time=1)
    scene.play(Create(person_svg, run_time=3))

    signature_dash = (
        Text("- ", font="TeX Gyre Termes")
        .scale(2)
        .next_to(signature, LEFT)
        # .next_to(paragraph, (1.5 * DOWN) + RIGHT)
        .set_color(BLACK)
    )
    signature_combo = VGroup(signature_dash, signature).scale(scale_factor=scale)
    signature_combo.next_to(VGroup(paragraph, person_svg), scale * DOWN)
    # signature.next_to(signature_dash, RIGHT).set_color(BLACK)

    # add the signature to the scene
    scene.play(Create(signature_combo, run_time=2))
    return paragraph, person_svg, signature_combo


class EinsteinQuote(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = ImageMobject("background.png").scale(2).set_color("#FFFFFF")
        self.add(background)

    def construct(self):
        paragraph, person, signature_group = self.draw(self, origin=ORIGIN, scale=1.0)
        self.wait(10)
        self.play(
            FadeOut(Group(VGroup(paragraph, person), signature_group), run_time=2)
        )
        self.wait(2)

    @staticmethod
    def draw(scene, origin, scale):
        signature = SVGMobject(
            path_to_project_root()
            / "animations"
            / "demos"
            / "Albert_Einstein_signature_1934.svg"
        ).scale(0.5)
        person_svg = SVGMobject(
            path_to_project_root() / "animations" / "demos" / "people" / "Einstein1.svg"
        ).scale(2.0)
        paragraph, person, signature_group = person_with_quote(
            scene,
            person_svg=person_svg,
            quote=(
                '"So far as the laws of mathematics refer to reality,\nthey are not certain. '
                'And so far as they are certain, \nthey do not refer to reality."'
            ),
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1,
        )
        return paragraph, person, signature_group


if __name__ == "__main__":
    c = EinsteinQuote()
    c.render()
