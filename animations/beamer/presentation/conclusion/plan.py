from typing import Union as U

from manim import *

from animations.beamer.presentation.bibtex import BibTexManager
from animations.beamer.slides import SlideWithBlocks, SlideWithList
from animations.beamer.blocks import AlertBlock, ExampleBlock
from animations.beamer.lists import ItemizedList, BulletedList as BL
from soft.utilities.reproducibility import path_to_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def proposed_plan() -> SlideWithBlocks:
    """
    Create a slide with two blocks: one for the advantages and one for the disadvantages of
    deep neural networks (DNNs).

    Returns:
        The slide with the two blocks.
    """
    return SlideWithList(
        title="Expected Timeline",
        subtitle="I expect this work to take one year.",
        beamer_list=BL(
            items=[
                "Experiment Setup",
                ItemizedList(
                    items=[
                        "Computer vision",
                        "Septic shock",
                    ]
                ),
                "Fatherhood",
                ItemizedList(
                    items=[
                        "(June 29) Baby Evelyn",
                        "(July) Learn to be a father",
                    ]
                ),
                "Model Development & Evaluation",
                ItemizedList(
                    items=[
                        "(August) Attempt proof & begin job search",
                        "(September & October) Implement proposed changes",
                    ]
                ),
                "Data Collection",
                ItemizedList(
                    items=[
                        "(November & December) Run experiments",
                        "(January & February) Run and analyze ITS study",
                        "(March) Prepare dissertation & slides",
                        "(April) Defend dissertation",
                        "(May) Graduate (hopefully)",
                    ]
                ),
                "Writing and Submission",
                ItemizedList(
                    items=[
                        "(March) Prepare dissertation & slides",
                        "(April) Defend dissertation",
                        "(May) Graduate (hopefully)",
                    ]
                ),
            ]
        )
    )
