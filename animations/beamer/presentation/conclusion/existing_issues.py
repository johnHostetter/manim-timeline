from typing import Union as U

from manim import *

from animations.beamer.presentation.bibtex import BibTexManager
from animations.beamer.slides import SlideWithBlocks
from animations.beamer.blocks import AlertBlock, ExampleBlock
from animations.beamer.lists import ItemizedList, AdvantagesList, DisadvantagesList
from soft.utilities.reproducibility import path_to_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def curr_limitations() -> SlideWithBlocks:
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
                "Unable to remove knowledge",
            ]
        ),
    )
    example_block_1 = ExampleBlock(
        title=None,
        content=AdvantagesList(
            items=[
                "Prune with built-in heuristics",
            ]
        ),
    )
    alert_block_2 = AlertBlock(
        title=None,
        content=DisadvantagesList(
            items=[
                "Fixed number of fuzzy logic rules",
            ]
        ),
    )
    example_block_2 = ExampleBlock(
        title=None,
        content=AdvantagesList(
            items=[
                "Dynamic rule generation",
            ]
        ),
    )
    alert_block_3 = AlertBlock(
        title=None,
        content=DisadvantagesList(
            items=[
                "Relative subpar performance in supervised learning tasks",
            ]
        ),
    )
    example_block_3 = ExampleBlock(
        title=None,
        content=AdvantagesList(
            items=[
                "Learn from and mimic DNNs",
            ]
        ),
    )
    return SlideWithBlocks(
        title="Current Limitations",
        subtitle="I propose to improve my Morphetic Epsilon-Delayed NFNs",
        blocks=[
            alert_block_1,
            example_block_1,
            alert_block_2,
            example_block_2,
            alert_block_3,
            example_block_3,
        ],
    )
