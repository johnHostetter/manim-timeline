from manim import *

from manim_beamer.slides import SlideWithList
from manim_beamer.lists import ItemizedList, BulletedList as BL

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def define_linguistics() -> SlideWithList:
    """
    Create a slide defining what we mean by linguistics, such as linguistic terms and variables.

    Returns:
        The slide with definitions and examples.
    """
    myTemplate = TexTemplate()
    myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
    MathTex("\mathcal{T}")
    return SlideWithList(
        title="A Brief Tour of Linguistics",
        subtitle=None,
        beamer_list=ItemizedList(
            items=[
                VGroup(
                    Text("Linguistic terms, "),
                    MathTex(" \mathcal{T} "),
                    Text(
                        ", are constrained fuzzy sets w/ semantic meaning of some concept"
                    ),
                ),
                BL(
                    items=[
                        '"blue", "tall", "warm", "old", etc.',
                    ]
                ),
                VGroup(
                    Text("Linguistic variables, "),
                    MathTex(" \mathcal{V} "),
                    Text(", can take on values from a set of linguistic terms"),
                ),
                BL(
                    items=[
                        '"color"',
                        '"height"',
                        '"temperature", "age", etc.',
                    ]
                ),
                "Degree to which a linguistic term applies to a linguistic variable is calculated "
                "\nby an atomic fuzzy proposition",
                BL(
                    items=[
                        VGroup(
                            Text(
                                'Written as "',
                            ),
                            MathTex("x"),
                            Text(" is "),
                            MathTex("\mu"),
                            Text('" where '),
                            MathTex("\mu \in \mathcal{T}"),
                        ),
                        ItemizedList(
                            items=[
                                'e.g., "the sky is blue", "the temperature is hot", '
                                '\n"the person is tall", "the car is old", etc.',
                            ]
                        ),
                        "More complex (compound) propositions can be formed by combining atomic "
                        "\npropositions with logical operators (e.g., AND, OR, NOT, etc.)",
                        ItemizedList(
                            items=[
                                'e.g., "the sky is blue OR the temperature is hot", '
                                '\n"the person is tall AND the car is old", etc.'
                            ]
                        ),
                    ]
                ),
            ]
        ),
    )


if __name__ == "__main__":
    beamer_slide = define_linguistics()
    beamer_slide.render()
