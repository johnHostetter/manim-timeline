from manim import *

from animations.beamer.slides import SlideWithList
from animations.beamer.presentation.bibtex import BibTexManager
from animations.beamer.lists import ItemizedList, BulletedList as BL

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def lers_summary() -> SlideWithList:
    """
    Create a slide summarizing my M-FCQL study.

    Returns:
        The slide with a short summary.
    """
    bibtex_manager = BibTexManager()
    return SlideWithList(
        title="A Minimal Discriminant Description of Fuzzy Rules",
        subtitle="Testing the Viability of Human-Readable Fuzzy Rules in Reinforcement Learning",
        beamer_list=BL(
            items=[
                "Hostetter, John Wesley et al., Self-Organizing Computing with Words:\n"
                "Automatic Discovery of Natural Language Control\nwithin an Intelligent Tutoring System (In Review)",
                "Primary Intuition",
                ItemizedList(
                    items=[
                        "Construct & train a model using CEW & FCQL",
                        bibtex_manager.slide_short_cite("hostetter2023self"),
                        "Simplify the NFN\'s rules using LERS from rough set theory",
                        bibtex_manager.slide_short_cite("new_lers")
                    ]
                ),
                "Summary",
                ItemizedList(
                    items=[
                        "No loss in performance with human-readable NFN",
                        "Reduced 2,883 to only 757 rules",
                        "21 features globally eliminated (from 142)",
                        "Mean 6.896 (S.D. 2.101) premises per rule afterward (from 142)",
                    ]
                ),
                "Contributions",
                ItemizedList(
                    items=[
                        "First published use of rough theory with fuzzy RL",
                        "Works well in high-dimensional spaces",
                    ]
                ),
                "Limitations",
                ItemizedList(
                    items=[
                        "Computationally expensive",
                        "Evaluated only on our ITS",
                        "Computer vision"
                    ]
                ),
            ]
        )
    )


if __name__ == "__main__":
    beamer_slide = lers_summary()
    beamer_slide.render()
