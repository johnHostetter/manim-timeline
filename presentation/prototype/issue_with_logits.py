from manim import *

from manim_beamer.slides import SlideWithBlocks
from manim_beamer.lists import AdvantagesList, DisadvantagesList
from manim_beamer.blocks import AlertBlock, ExampleBlock, RemarkBlock

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def issue_with_logits() -> SlideWithBlocks:
    """
    Create a slide discussing why we need to modify the Gumbel-Max Trick.

    Returns:
        The slide with the issue, remark and proposed solution.
    """
    alert_block = AlertBlock(
        title="Issue",
        content=DisadvantagesList(
            items=["NFN cannot have real-numbered weight matrices."]
        ),
    )
    example_block = ExampleBlock(
        title="Proposed Solution",
        content=AdvantagesList(
            items=[
                "Use a (Modified) Gumbel-Max Trick.",
                VGroup(
                    MathTex(r"\tilde{L}", color=BLACK),
                    Text(
                        " are logits or raw non-normalized probabilities.", color=BLACK
                    ),
                ),
                VGroup(
                    Text("Differentiable sample from ", color=BLACK),
                    MathTex(r"\tilde{L}", color=BLACK),
                    Text(" to yield ", color=BLACK),
                    MathTex(r"L.", color=BLACK),
                ),
            ]
        ),
    )
    remark_block = RemarkBlock(
        title="Remark",
        content="The Gumbel Max Trick allows us to differentiably sample from a\n"
        "categorical distribution.",
    )
    return SlideWithBlocks(
        title="Why the Gumbel-Max Trick?",
        subtitle=None,
        blocks=[alert_block, remark_block, example_block],
    )


if __name__ == "__main__":
    issue_with_logits().render()
