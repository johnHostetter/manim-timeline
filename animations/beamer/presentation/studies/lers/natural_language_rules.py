from manim import *

from animations.beamer.slides import SlideWithTable

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def get_lers_rules() -> SlideWithTable:
    """
    Create a slide showing the rules from the LERS study.

    Returns:
        The slide with the study results.
    """
    data = [
        [
            "1",
            """
            There is a high number of principles, a low number of
            tutor concepts per session, a high number of steps
            since the last wrong KC in the session, and a high
            percentage of correct applications for Addition
            Theorem of 3 Events.
            """,
            "Example"
        ],
        [
            "2",
            """
            The student spent a high amount of time on the
            tutoring session, had a typical number of correctly
            learned knowledge concepts, showed a high success
            rate in correctly applying the Addition Theorem
            for 2 events, and an average success rate in correctly
            applying the Addition Theorem for 3 events.
            """,
            "Solve Alone"
        ],
        [
            "3",
            """
            The number of knowledge components per problem
            solving session is high, and the proportion of
            correctly answered DeMorgan’s theorem select
            questions is most, while the proportion of correctly
            answered DeMorgan’s theorem apply questions is
            about half.
            """,
            "Work Together"
        ],
    ]
    table = Table(
        data,
        # row_labels=[Text("FYD"), Text("ECLAIRE")],
        col_labels=[
            Text("Rule", weight=BOLD),
            Text("IF", weight=BOLD),
            Text("THEN", weight=BOLD)
        ]
    )

    table.get_col_labels().set_weight("bold")
    table.get_horizontal_lines().set_color(BLACK)
    table.get_vertical_lines().set_color(BLACK)
    for entry in table.get_entries():
        entry.set_color(BLACK)

    return SlideWithTable(
        title="Computing With Words",
        subtitle=None,
        table=table.scale(scale_factor=0.75),
        caption="KC is a knowledge component (e.g., Complement Theorem).",
        highlighted_columns=[],
        width_buffer=6.0
    )


if __name__ == "__main__":
    get_lers_rules().render()
