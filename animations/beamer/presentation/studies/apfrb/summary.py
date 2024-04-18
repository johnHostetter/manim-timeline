from manim import *

from animations.beamer.slides import SlideWithList
from animations.beamer.presentation.bibtex import BibTexManager
from animations.beamer.lists import ItemizedList, BulletedList as BL

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def apfrb_summary() -> SlideWithList:
    """
    Create a slide with my proposed studies for the completion of my dissertation.

    Returns:
        The slide with a list of studies.
    """
    bibtex_manager = BibTexManager()
    return SlideWithList(
        title="Leveraging All-Permutations Fuzzy Rule Base (APFRB)",
        subtitle="Exploring the Potential of Fuzzy Logic in Real-World Applications",
        beamer_list=BL(
            items=[
                bibtex_manager.cite_entry(bibtex_manager["hostetter2023leveraging"]),
                "Primary Intuition",
                ItemizedList(
                    items=[
                        "APFRB offers a mathematical equivalence between DNNs and FLCs",
                        "Train the more complex DNN, then convert to FLC for inference",
                    ]
                ),
                "Summary",
                ItemizedList(
                    items=[
                        "The FLC significantly helped students learn probability",
                    ]
                ),
                "Contributions",
                ItemizedList(
                    items=[
                        "First pedagogical policy using FLCs to teach students",
                    ]
                ),
                "Limitations",
                ItemizedList(
                    items=[
                        "Works only for some DNNs (e.g., hyperbolic tangent required)",
                        "Number of rules grows exponentially with the number of neurons in the DNN",
                        "The rules are not interpretable by humans",
                    ]
                ),
            ]
        ),
    )


if __name__ == "__main__":
    beamer_slide = apfrb_summary()
    beamer_slide.render()
