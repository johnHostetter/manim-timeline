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
        title="Advantages of DNNs",
        content=AdvantagesList(
            items=[
                "Reliable",
                ItemizedList(
                    items=[
                        "Applications to robotics, medicine, etc.",
                    ]
                ),
                "Flexible",
                ItemizedList(
                    items=[
                        "Network morphism (e.g., add neurons or layers)",
                    ]
                ),
                "Generalizable",
                ItemizedList(
                    items=[
                        "Supervised learning",
                        "Online/offline reinforcement learning",
                        "and more...",
                    ]
                ),
            ]
        ),
    )
    alert_block = AlertBlock(
        title="Disadvantages of DNNs",
        content=DisadvantagesList(
            items=[
                "Relies upon large quantities of data",
                "Difficult to interpret (i.e., black-box)",
            ]
        ),
    )
    return SlideWithBlocks(
        title="Deep Neural Networks (DNNs)",
        blocks=[example_block, alert_block],
    )
