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


def pros_and_cons() -> SlideWithBlocks:
    """
    Create a slide with two blocks: one for the advantages and one for the disadvantages of
    deep neural networks (DNNs).

    Returns:
        The slide with the two blocks.
    """
    bib = BibTexManager()
    example_block = ExampleBlock(
        title="Advantages of NFNs",
        content=AdvantagesList(
            items=[
                "Transparent",
                ItemizedList(
                    items=[
                        'Historically designed by human experts (i.e., "expert-designed").',
                        bib.slide_short_cite("lee_supervised_1992"),
                    ]
                ),
                "Sample efficient",
                ItemizedList(
                    items=[
                        'Due to "expert design", they [typically] require less training.',
                        bib.slide_short_cite("berenji_learning_1992"),
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
                bib.slide_short_cite("lee_flc_12"),
                ItemizedList(
                    items=[
                        "Subconscious decision-making hard to articulate",
                        "Requires domain expertise",
                        "Time-consuming",
                    ]
                ),
                "Unable to readily adapt to changes (e.g., add new knowledge)",
                bib.slide_short_cite("klir_yuan"),
                ItemizedList(
                    items=[
                        "Self-organizing NFNs may achieve this but with restrictions",
                        bib.slide_short_cite("zhou_pseudo_1996"),
                        bib.slide_short_cite("er_online_2004"),
                    ]
                ),
                "NFN research is often specific to a certain task",
                ItemizedList(
                    items=[
                        "(e.g., supervised or reinforcement learning)",
                        bib.slide_short_cite("aghaeipoor_mokblmoms_2019"),
                        bib.slide_short_cite("zhou_reinforcement_2009"),
                    ]
                ),
            ]
        ),
    )
    return SlideWithBlocks(
        title="Neuro-Fuzzy Networks (NFNs)",
        subtitle=None,
        blocks=[example_block, alert_block],
    )
