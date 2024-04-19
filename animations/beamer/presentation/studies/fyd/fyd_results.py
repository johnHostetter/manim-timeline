from manim import *

from animations.beamer.slides import SlideWithTable

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def get_fyd_results() -> SlideWithTable:
    """
    Create a slide showing the results of the FYD study.

    Returns:
        The slide with the study results.
    """
    data = [
        [
            "FYD (N = 39)", ".677 (.202)", ".746 (.160)", ".079 (.278)", "1.26 (.41)"
        ],
        [
            "ECLAIRE (N = 52)", ".675 (.183)", ".736 (.206)", ".080 (.320)", "1.89 (.51)"
        ],
        [
            "CEW (N = 38)", ".645 (.217)", ".733 (.189)", ".104 (.290)", "1.98 (.67)"
        ],
        [
            "CQL (N = 44)", ".635 (.210)", ".708 (.175)", ".094 (.248)", "1.89 (.71)"
        ]
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
        highlighted_columns=[4]
    )


if __name__ == "__main__":
    get_fyd_results().render()
