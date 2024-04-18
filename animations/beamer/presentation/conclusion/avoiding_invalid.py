from manim import *

from animations.beamer.slides import SlideWithBlocks
from animations.beamer.blocks import AlertBlock, ExampleBlock, RemarkBlock
from animations.beamer.lists import DisadvantagesList, AdvantagesList, ItemizedList

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def avoiding_invalid_selections() -> SlideWithBlocks:
    """
    Create a slide discussing how to avoid invalid selections according to
    the epsilon-completeness property.

    Returns:
        The slide with the formula, remark, solution and word of caution.
    """
    remark_block = RemarkBlock(
        title="Remarks",
        content=ItemizedList(
            items=[
                "Recall the importance of frequency from FYD.",
                "Recall a cutoff threshold was found w/ FYD.",
            ]
        ),
    )
    example_block = ExampleBlock(
        title="Proposed Solution",
        content=AdvantagesList(
            items=[
                VGroup(
                    Text("Calculate ", color=BLACK),
                    MathTex(r"{\theta}^{th}", color=BLACK),
                    Text(" percentile of each linguistic variable.", color=BLACK),
                ),
                VGroup(
                    Text("Ignore premises w/ scalar cardinality below ", color=BLACK),
                    MathTex(r"{\theta}^{th}", color=BLACK),
                    Text(" percentile.", color=BLACK),
                ),
                VGroup(
                    Text("Temporarily modify binary mask "),
                    MathTex(r"B' = (B \odot S) > \theta."),
                ),
            ]
        ),
    )
    alert_block = AlertBlock(
        title="Caution",
        content=DisadvantagesList(
            items=[
                VGroup(
                    Text("Higher values of ", color=BLACK),
                    MathTex(r"{\theta}", color=BLACK),
                    Text(" encourage myopic behavior (SL).", color=BLACK),
                ),
                VGroup(
                    Text("Lower values of ", color=BLACK),
                    MathTex(r"{\theta}", color=BLACK),
                    Text(" encourage exploratory behavior (RL).", color=BLACK),
                ),
            ]
        ),
    )
    sentence_1 = Tex(
        r"Restrict logits to $[-\kappa, \kappa]$ by modifying \texttt{Sigmoid} such that",
        color=BLACK,
    )

    myTemplate = TexTemplate()
    myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
    formula = MathTex(
        r"""
        S = \begin{bmatrix} 
        \sum_{\mathbf{x}} \mu_{1, 1}(x_{1}) & \sum_{\mathbf{x}} \mu_{1, 2}(x_{1}) & \dots \\
        \vdots & \ddots & \\
        \sum_{\mathbf{x}} \mu_{n, 1}(x_{n}) &        & \sum_{\mathbf{x}} \mu_{n, \max_{i} \mid \mu_i \mid }(x_{n}) 
        \end{bmatrix}
        \qquad
        """,
        color=BLACK,
    )
    sentence_2 = Tex(
        r"applies a simple bounding operation to $\tilde{L}'$.", color=BLACK
    ).next_to(formula, DOWN)
    return SlideWithBlocks(
        title="Fix Numerical Instability",
        subtitle=None,
        blocks=[
            formula,
            remark_block,
            example_block,
            alert_block,
            # VGroup(sentence_1, formula, sentence_2)
        ],
    )


if __name__ == "__main__":
    avoiding_invalid_selections().render()
