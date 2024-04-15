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


def proposal() -> SlideWithBlocks:
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
    return SlideWithBlocks(
        title="Overall Proposal",
        subtitle="Address each major disadvantage of NFNs",
        blocks=[
            alert_block_1,
            example_block_1,
            alert_block_2,
            example_block_2,
            alert_block_3,
            example_block_3,
        ],
    )
