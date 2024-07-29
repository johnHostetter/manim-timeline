from manim import *

from manim_beamer.slides import SlideWithBlocks
from manim_beamer.lists import BulletedList as BL
from manim_beamer.blocks import AlertBlock, ExampleBlock, RemarkBlock

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def constrained_gumbel_softmax() -> SlideWithBlocks:
    """
    Create a slide discussing why we need to constrain the Gumbel-softmax.

    Returns:
        The slide with the issue, proposed solution, formula and remarks.
    """
    alert_block = AlertBlock(
        title="Issue",
        content="Gumbel-softmax may allow invalid selections to have non-zero probability\n"
        "as it approximates a categorical distribution.",
    )
    example_block = ExampleBlock(
        title="Proposed Solution",
        content="Constrain the Gumbel-softmax to ensure valid selections.",
    )
    remark_block = RemarkBlock(
        title="Remarks",
        content=BL(
            items=[
                "Constrained Gumbel-softmax distribution pushes invalid\n"
                "options to zero probability.",
                "Sum over linguistic term dimension (in denominator to\n"
                "sample and assign one term per variable for each fuzzy\n"
                "logic rules' premises.",
            ]
        ),
    )

    # Use the custom command in a LaTeX expression
    myTemplate = TexTemplate()
    myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
    formula = MathTex(
        r"\tilde{L''} = \frac{"
        r"\exp{(\texttt{BoundSigmoid}(\tilde{L'}))} \odot B'}"
        r"{\sum_{t=1}^{\max_{v} |\mathcal{T}|} "
        r"\exp{(\texttt{BoundSigmoid}(\tilde{L'}))} \odot B'}",
        color=BLACK,
    )
    return SlideWithBlocks(
        title="Constrained Gumbel-Softmax",
        subtitle=None,
        blocks=[alert_block, example_block, formula, remark_block],
    )


if __name__ == "__main__":
    constrained_gumbel_softmax().render()
