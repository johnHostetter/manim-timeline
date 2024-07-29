from typing import Type

from manim import *

from manim_beamer.slides import SlideWithBlocks
from manim_beamer.blocks import AlertBlock, ExampleBlock, Block
from manim_beamer.lists import AdvantagesList, DisadvantagesList

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def get_proposal() -> SlideWithBlocks:
    """
    Create a slide with two blocks: one for the advantages and one for the disadvantages of
    deep neural networks (DNNs).

    Returns:
        The slide with the two blocks.
    """
    alert_block_1 = AlertBlock(
        title=None,
        content=DisadvantagesList(
            items=[
                "Difficult & expensive to design",
            ]
        ),
    )
    example_block_1 = ExampleBlock(
        title=None,
        content=AdvantagesList(
            items=[
                "Self-organizing, data-driven algorithms",
            ]
        ),
    )
    alert_block_2 = AlertBlock(
        title=None,
        content=DisadvantagesList(
            items=[
                "Unable to readily adapt to changes (e.g., add new knowledge)",
            ]
        ),
    )
    example_block_2 = ExampleBlock(
        title=None,
        content=AdvantagesList(
            items=[
                "Capable of adding new knowledge just in time (network morphism)",
            ]
        ),
    )
    alert_block_3 = AlertBlock(
        title=None,
        content=DisadvantagesList(
            items=[
                "NFN research is often specific to a certain task",
            ]
        ),
    )
    example_block_3 = ExampleBlock(
        title=None,
        content=AdvantagesList(
            items=[
                "A task-independent solution",
            ]
        ),
    )

    # gather all the blocks together
    blocks: List[Type[Block]] = [
        alert_block_1,
        example_block_1,
        alert_block_2,
        example_block_2,
        alert_block_3,
        example_block_3,
    ]

    return SlideWithBlocks(
        title="Overall Proposal",
        subtitle="Address each major disadvantage of NFNs",
        blocks=blocks,
    )


def pad_block_text_with_spacing(blocks):
    # get the max length of the text content (assuming only first item is used) in each block
    max_len = max([len(block.content.items[0]) for block in blocks])
    for block in blocks:
        curr_len = len(block.content.items[0])
        # pad the content with spaces to make them all the same length
        if curr_len < max_len:
            block.content.items[0] += " " * (max_len - curr_len)

    return blocks


if __name__ == "__main__":
    beamer_slide = get_proposal()
    beamer_slide.render()
