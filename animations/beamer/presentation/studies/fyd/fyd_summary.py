from manim import *

from animations.beamer.slides import SlideWithList
from animations.beamer.presentation.bibtex import BibTexManager
from animations.beamer.lists import ItemizedList, BulletedList as BL

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def fyd_summary() -> SlideWithList:
    """
    Create a slide summarizing my FYD study.

    Returns:
        The slide with a short summary.
    """
    bibtex_manager = BibTexManager()
    return SlideWithList(
        title="Exploiting Frequent-Yet-Discernible Patterns",
        subtitle="Improving the Viability of Human-Readable Fuzzy Rules in Reinforcement Learning",
        beamer_list=BL(
            items=[
                "Hostetter, John Wesley et al., "
                "Self-Organizing Epsilon-Complete Neuro-Fuzzy Q-Networks\n"
                "from Frequent Yet Discernible Patterns in Reward-Based Scenarios (Draft)",
                "Primary Intuition",
                ItemizedList(
                    items=[
                        "Construct & train a model using CEW & FCQL",
                        bibtex_manager.slide_short_cite("hostetter2023self"),
                        "Simplify the NFN's rules using FYD",
                    ]
                ),
                "Summary",
                ItemizedList(
                    items=[
                        "No loss in performance with human-readable NFN",
                        "Mean 9.734 (S.D. 3.993) premises per rule afterward (from 142)",
                    ]
                ),
                "Contributions",
                ItemizedList(
                    items=[
                        "Exploit\'s Zadeh\'s f-granulation theory to simplify rules",
                        "Quick mimic of rule simplification in LERS",
                        "Avoids violating ϵ-completeness",
                    ]
                ),
                "Limitations",
                ItemizedList(
                    items=[
                        "Evaluated only on our ITS and classic control tasks",
                        "Computer vision",
                    ]
                ),
            ]
        ),
    )


if __name__ == "__main__":
    beamer_slide = fyd_summary()
    beamer_slide.render()
