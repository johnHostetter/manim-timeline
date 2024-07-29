from manim import *

from manim_beamer.slides import SlideWithList
from manim_beamer.lists import ItemizedList, BulletedList as BL

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def get_outline() -> SlideWithList:
    """
    Create a slide with my proposed studies for the completion of my dissertation.

    Returns:
        The slide with a list of studies.
    """
    return SlideWithList(
        title="Outline",
        subtitle=None,
        width_buffer=12.0,
        beamer_list=ItemizedList(
            items=[
                "Introduction & Background",
                "Methodology",
                BL(
                    items=[
                        "Part I: Translation",
                        "Part II: Self-Organization",
                        "Part III: Morphism",
                    ]
                ),
                "Proposal",
                BL(
                    items=[
                        "Existing Prototype",
                        "Current Limitations",
                        "Proposed Modifications & Studies",
                    ]
                ),
                "Expected Timeline",
            ]
        ),
    )


if __name__ == "__main__":
    beamer_slide = get_outline()
    beamer_slide.render()
