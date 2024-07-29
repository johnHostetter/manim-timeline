from manim import *

from manim_beamer.slides import SlideWithBlocks
from manim_beamer.blocks import AlertBlock, ExampleBlock, RemarkBlock

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def why_e_delayed() -> SlideWithBlocks:
    """
    Create a slide discussing why we need epsilon-delayed NFNs.

    Returns:
        The slide with the issue, remark and proposed solution.
    """
    alert_block = AlertBlock(
        title="Issue", content="Naively adding a new fuzzy set will not work."
    )
    remark_block = RemarkBlock(
        title="Remark",
        content="It causes membership thrashing downstream during Gumbel Max Trick.",
    )
    example_block = ExampleBlock(
        title="Proposed Solution", content="Batch-delayed morphism."
    )
    return SlideWithBlocks(
        title="Why ϵ-Delayed?",
        subtitle="ϵ-completeness is required to avoid numerical underflow.",
        blocks=[alert_block, remark_block, example_block],
    )


if __name__ == "__main__":
    why_e_delayed().render()
