from manim import *

from manim_beamer.slides import SlideWithBlocks
from manim_beamer.blocks import AlertBlock, ExampleBlock
from manim_beamer.lists import AdvantagesList, DisadvantagesList

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def relax_links() -> SlideWithBlocks:
    """
    Create a slide discussing why we need to modify the Gumbel-Max Trick.

    Returns:
        The slide with the issue, remark and proposed solution.
    """
    alert_block = AlertBlock(
        title="Issue",
        content=DisadvantagesList(
            items=[
                VGroup(
                    Text("Sparse, constrained, binary matrix "),
                    MathTex(r"L", color=BLACK),
                ),
                "Rules' premises cannot change",
            ]
        ),
    )
    example_block = ExampleBlock(
        title="Proposed Solution",
        content=AdvantagesList(
            items=[
                VGroup(
                    Text("Relax "),
                    MathTex(r"L", color=BLACK),
                    Text(" to be real-valued, ", color=BLACK),
                    MathTex(r"\tilde{L}", color=BLACK),
                )
            ]
        ),
    )
    return SlideWithBlocks(
        title="Relax NFN Constraints",
        subtitle=None,
        blocks=[alert_block, example_block],
        height_buffer=3.0,
    )


if __name__ == "__main__":
    relax_links().render()
