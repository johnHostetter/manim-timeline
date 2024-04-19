from manim import *

from animations.beamer.slides import SlideWithTable

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def format_rule_table(data: list[list[str]]) -> Table:
    """
    Format the data into a table.

    Args:
        data: The data to format.

    Returns:
        The table with the data.
    """
    table = Table(
        data,
        # row_labels=[Text("FYD"), Text("ECLAIRE")],
        col_labels=[
            Text("Rule", weight=BOLD),
            Text("IF", weight=BOLD),
            Text("THEN", weight=BOLD)
        ]
    )

    return table


def make_rule_slide(
        title: str, data: list[list[str]], caption: str, width_buffer: float = 3.0
) -> SlideWithTable:
    """
    Create a slide showing the rules from the LERS study.

    Args:
        title: The title of the slide.
        data: The data to format.
        caption: The caption for the slide.
        width_buffer: The buffer to add to the width of the table.

    Returns:
        The slide with the study results.
    """
    table = format_rule_table(data)

    return SlideWithTable(
        title=title,
        subtitle=None,
        table=table.scale(scale_factor=0.75),
        caption=caption,
        highlighted_columns=[]
    )


def get_original_rules() -> SlideWithTable:
    """
    Create a slide showing the original rules from the LERS study.

    Returns:
        The slide with the study results.
    """
    data = [
        [
            "1",
            """
            nPrincipleInProblem is high ∧ nTutorConceptsSession is low
            ∧ nStepSinceLastWrongKCSession is high
            ∧ pctCorrectAdd3Apply is high
            """,
            "Example"
        ],
        [
            "2",
            """
            timeOnTutoringSessionPS is high ∧ nCorrectKC is typical
            ∧ pctCorrectAdd2Apply is high ∧ pctCorrectAdd3All is average
            """,
            "Solve Alone"
        ],
        [
            "3",
            """
            nKCsSessionPS is high ∧ pctCorrectDeMorSelect is most
            ∧ pctCorrectDeMorApply is about half
            """,
            "Work Together"
        ]
    ]

    return make_rule_slide(
        title="Example of Model Complexity",
        data=data,
        caption="KC is a knowledge component (e.g., Complement Theorem).",
        width_buffer=3.0
    )


def get_natural_language_rules() -> SlideWithTable:
    """
    Create a slide showing the rules from the LERS study after converting to natural language.

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

    return make_rule_slide(
        title="Computing With Words",
        data=data,
        caption="KC is a knowledge component (e.g., Complement Theorem).",
        width_buffer=6.0
    )


if __name__ == "__main__":
    get_original_rules().render()
