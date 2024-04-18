from manim import *

from animations.beamer.slides import SlideWithList
from animations.beamer.presentation.bibtex import BibTexManager
from animations.beamer.lists import ItemizedList, BulletedList as BL

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def llm_summary() -> SlideWithList:
    """
    Create a slide with my proposed studies for the completion of my dissertation.

    Returns:
        The slide with a list of studies.
    """
    bibtex_manager = BibTexManager()
    return SlideWithList(
        title="The Latent Lockstep Method",
        subtitle="Identifying Exemplars by Leveraging Latent Representations",
        beamer_list=BL(
            items=[
                bibtex_manager.cite_entry(bibtex_manager["hostetter2023latent"]),
                "Primary Intuition",
                ItemizedList(
                    items=[
                        "If the latent representations are similar, the input data is similar",
                        "If data is unique in the latent space, it is unique in the original space",
                    ]
                ),
                "Summary",
                ItemizedList(
                    items=[
                        "Latent representations are used to identify exemplars",
                        "The method is simple, yet effective",
                        "The method is problem-independent",
                    ]
                ),
                "Contributions",
                ItemizedList(
                    items=[
                        "Simple & quick",
                        "Problem independent exemplar identification",
                        "Works well in high-dimensional spaces",
                    ]
                ),
                "Limitations",
                ItemizedList(
                    items=[
                        "The premises of fuzzy logic rule grows linear with the number of inputs",
                        "Chosen encoder architecture may not be ideal",
                    ]
                ),
            ]
        ),
    )


if __name__ == "__main__":
    beamer_slide = llm_summary()
    beamer_slide.render()
