from manim import *

from manim_beamer.slides import SlideWithList
from manim_beamer.lists import ItemizedList, BulletedList as BL

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def proposed_studies() -> SlideWithList:
    """
    Create a slide with my proposed studies for the completion of my dissertation.

    Returns:
        The slide with a list of studies.
    """
    return SlideWithList(
        title="Proposed Studies",
        subtitle="Explore new horizons for NFN",
        beamer_list=BL(
            items=[
                "Prove Morphetic ϵ-Delayed NFN are universal approximators",
                ItemizedList(
                    items=[
                        "If time permits, inspect graph invariants",
                        "Explore if the training boundary is fractal",
                    ]
                ),
                "Expand the experiments",
                ItemizedList(
                    items=[
                        "Intelligent Tutoring Systems",
                        "Healthcare (e.g., Septic shock detection)",
                    ]
                ),
                "Neural architecture search",
                ItemizedList(
                    items=[
                        "Selection of ideal new fuzzy set(s)",
                    ]
                ),
                "Hierarchical NFN",
                ItemizedList(
                    items=[
                        "Use Morphetic ϵ-Delayed NFN to learn the hierarchy",
                    ]
                ),
                "Computer vision",
                ItemizedList(
                    items=[
                        "Atari games",
                        "Use NFN to detect objects in images",
                    ]
                ),
            ]
        ),
    )


if __name__ == "__main__":
    beamer_slide = proposed_studies()
    beamer_slide.render()
