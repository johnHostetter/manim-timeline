from manim import *

from animations.beamer.slides import SlideWithTable

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class IntelligentTutoringSystemResults(SlideWithTable):
    def __init__(self, data: List[List[str]], highlighted_columns: List[int]):
        table = Table(
            data,
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

        super().__init__(
            title="Intelligent Tutoring System Results",
            subtitle=None,
            table=table.scale(0.75),
            caption="Mean (Standard Deviation) of learning performance & training time (in hours).",
            highlighted_columns=highlighted_columns
        )


if __name__ == "__main__":
    APFRBResults().render()
