from manim import *

from animations.beamer.slides import SlideWithBlocks
from animations.beamer.blocks import AlertBlock, ExampleBlock
from animations.beamer.lists import ItemizedList, AdvantagesList, DisadvantagesList

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def pros_and_cons() -> SlideWithBlocks:
    """
    Create a slide with two blocks: one for the advantages and one for the disadvantages of
    deep neural networks (DNNs).

    Returns:
        The slide with the two blocks.
    """
    example_block = ExampleBlock(
        title="Advantages of NFNs",
        content=AdvantagesList(
            items=[
                "Transparent",
                ItemizedList(
                    items=[
                        "Historically designed by human experts (i.e., ``expert-designed'').",
                    ]
                ),
                "Sample efficient",
                ItemizedList(
                    items=[
                        'Due to "expert design", they [typically] require less training.',
                    ]
                ),
            ]
        ),
    )
    alert_block = AlertBlock(
        title="Disadvantages of NFNs",
        content=DisadvantagesList(
            items=[
                "Difficult & expensive to design",
                ItemizedList(
                    items=[
                        "Subconscious decision-making hard to articulate",
                        "Requires domain expertise",
                        "Time-consuming",
                    ]
                ),
                "NFN research is often specific to a certain task",
                ItemizedList(
                    items=[
                        "(e.g., supervised or reinforcement learning)",
                    ]
                ),
            ]
        ),
    )
    return SlideWithBlocks(
        title="Neuro-Fuzzy Networks (NFNs)",
        blocks=[example_block, alert_block],
    )
