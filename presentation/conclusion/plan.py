from manim import *

from manim_beamer.slides import SlideWithList
from manim_beamer.lists import ItemizedList, BulletedList as BL

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def proposed_plan() -> SlideWithList:
    """
    Create a slide with my proposed timeline for the completion of my dissertation.

    Returns:
        The slide with a list of expected milestones.
    """
    return SlideWithList(
        title="Expected Milestones",
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
        ),
    )


if __name__ == "__main__":
    beamer_slide = proposed_plan()
    beamer_slide.render()
