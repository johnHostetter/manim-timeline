from manim import *

from animations.beamer.slides import SlideWithList
from animations.beamer.presentation.bibtex import BibTexManager
from animations.beamer.lists import ItemizedList, BulletedList as BL

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def cew_summary() -> SlideWithList:
    """
    Create a slide summarizing my AAMAS 2023 paper.

    Returns:
        The slide with a short summary.
    """
    bibtex_manager = BibTexManager()
    return SlideWithList(
        title="The Latent Lockstep Method",
        subtitle="Identifying Exemplars by Leveraging Latent Representations",
        beamer_list=BL(
            items=[
                bibtex_manager.cite_entry(bibtex_manager["hostetter2023self"]),
                "Primary Intuition",
                ItemizedList(
                    items=[
                        "CLIP may construct fuzzy sets",
                        "ECM can identify exemplars",
                        "Wang-Mendel algorithm can construct fuzzy rules from exemplars",
                        "Modify Fuzzy Q-Learning w/ CQL augmentation and train the NFN offline"
                    ]
                ),
                "Summary",
                ItemizedList(
                    items=[
                        "Effectiveness shown in Cart Pole & ITS",
                        "Great potential for offline RL if:",
                        BL(
                            items=[
                                "Limited data is available",
                                "Possible human expert knowledge",
                                "Need interpretation & accuracy"
                            ]
                        ),
                    ]
                ),
                "Contributions",
                ItemizedList(
                    items=[
                        "First dedicated offline model-free RL process with NFNs",
                        "Works well in high-dimensional spaces",
                    ]
                ),
                "Limitations",
                ItemizedList(
                    items=[
                        "The premises of fuzzy logic rule grows linear with the number of inputs",
                        "Evaluated only on Cart Pole and our ITS",
                        "Computer vision"
                    ]
                ),
            ]
        )
    )


if __name__ == "__main__":
    beamer_slide = cew_summary()
    beamer_slide.render()
