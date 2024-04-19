from manim import *

from animations.beamer.slides import SlideWithTable

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def get_lers_results() -> SlideWithTable:
    """
    Create a slide showing the results of the LERS study.

    Returns:
        The slide with the study results.
    """
    data = [
        [
            "CEW w/ LERS (N = 52)", ".765 (.149)", ".791 (.160)", ".026 (.609)", "1.35 (.51)"
        ],
        [
            "CEW (N = 58)", ".749 (.164)", ".769 (.206)", ".073 (.597)", "1.31 (.57)"
        ],
        [
            "Expert (N = 54)", ".754 (.184)", ".716 (.213)", "-.247 (.605)", "1.62 (.61)"
        ],
    ]

    table = Table(
        data,
        # row_labels=[
        #     Text("FYD (N = 39)"), Text("ECLAIRE (N = 52)"),
        #     Text("CEW (N = 38)"), Text("CQL (N = 44)")
        # ],
        col_labels=[
            Text("Condition", weight=BOLD),
            Text("Pre-Test", weight=BOLD),
            Text("Post-Test", weight=BOLD),
            Text("NLG", weight=BOLD),
            Text("Time", weight=BOLD)
        ]
    )

    table.get_col_labels().set_weight("bold")
    table.get_horizontal_lines().set_color(BLACK)
    table.get_vertical_lines().set_color(BLACK)
    for entry in table.get_entries():
        entry.set_color(BLACK)

    return SlideWithTable(
        title="Intelligent Tutoring System Results",
        subtitle=None,
        table=table.scale(0.75),
        caption="Mean (Standard Deviation) of learning performance & training time (in hours).",
        highlighted_columns=[2, 3]
    )


if __name__ == "__main__":
    get_lers_results().render()
