from typing import Union

import numpy as np
from manim import (
    Scene,
    SVGMobject,
    Text,
    Paragraph,
    ITALIC,
    BLACK,
    VGroup,
    AnimationGroup,
    Create,
    Write,
    UP,
    DOWN,
    LEFT,
)


def quotable_person(
    scene: Scene,
    person_svg: SVGMobject,
    quote: str,
    source: str,
    signature: Union[SVGMobject, Text],
    origin: np.ndarray,
    scale: float,
    left_shift: float = 0.5,
    animate: bool = True,
) -> (Paragraph, Text, SVGMobject, VGroup):
    paragraph = (
        Paragraph(quote, font="TeX Gyre Termes", slant=ITALIC, color=BLACK)
        .scale(0.7)
        .next_to(signature, UP)
    )
    source_text = (
        Text(source, font="TeX Gyre Termes", color=BLACK)
        .scale(0.5)
        .next_to(paragraph, DOWN)
    )
    person_and_quote = VGroup(paragraph, person_svg, source_text)
    person_and_quote.scale(scale_factor=scale)
    # person_bound = person_svg.get_bounding_box()
    # person_svg.next_to(paragraph, scale*LEFT, buff=0.0*scale)
    person_svg.move_to(paragraph, aligned_edge=LEFT).shift(
        person_svg.width * left_shift * LEFT
    )
    person_and_quote.move_to(origin)
    # person_svg.move_to(paragraph, ((4 * DOWN) + (12 * LEFT))).scale(2)
    # scene.play(Write(paragraph), run_time=3)

    # scene.play(paragraph.animate.shift(RIGHT * 2), run_time=1)
    if animate:
        scene.play(
            AnimationGroup(
                Create(person_svg, run_time=2),
                Write(VGroup(paragraph, source_text), run_time=2),
                lag_ratio=0.5,
            )
        )
    else:
        scene.add(person_and_quote)

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
    if animate:
        scene.play(Create(signature_combo, run_time=2))
        scene.wait(1)
    else:
        scene.add(signature_combo)
    return paragraph, source_text, person_svg, signature_combo
