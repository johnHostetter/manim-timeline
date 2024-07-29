from manim import *

from manim_beamer.slides import SlideWithBlocks
from manim_beamer.blocks import AlertBlock, ExampleBlock
from manim_beamer.lists import DisadvantagesList, AdvantagesList

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def fix_numerical_stability() -> SlideWithBlocks:
    """
    Create a slide discussing how to fix the numerical instability.

    Returns:
        The slide with the issue and proposed solution (w/ formula).
    """
    alert_block = AlertBlock(
        title="Issue",
        content=DisadvantagesList(
            items=[
                "NFN training may cause logits to grow too large.",
                "Subsequent calculations (e.g., exp) may yield NaNs\nor infinities.",
            ]
        ),
    )
    example_block = ExampleBlock(
        title="Proposed Solution", content=AdvantagesList(items=["Bound the logits."])
    )

    sentence_1 = Tex(
        r"Restrict logits to $[-\kappa, \kappa]$ by modifying \texttt{Sigmoid} such that",
        color=BLACK,
    )

    myTemplate = TexTemplate()
    myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
    formula = MathTex(
        r"\texttt{BoundSigmoid}(\tilde{L'}) = \frac{2\kappa}"
        r"{1 + \exp^{(-\tilde{L'} / {2\kappa})}} - \kappa",
        color=BLACK,
    ).next_to(sentence_1, DOWN)
    sentence_2 = Tex(
        r"applies a simple bounding operation to $\tilde{L}'$.", color=BLACK
    ).next_to(formula, DOWN)
    return SlideWithBlocks(
        title="Fix Numerical Instability",
        subtitle=None,
        blocks=[alert_block, example_block, VGroup(sentence_1, formula, sentence_2)],
    )


if __name__ == "__main__":
    fix_numerical_stability().render()
