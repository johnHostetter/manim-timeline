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
            "nPrincipleInProblem is high ∧ nTutorConceptsSession is low\n"
            "∧ nStepSinceLastWrongKCSession is high\n"
            "∧ pctCorrectAdd3Apply is high",
            "Example"
        ],
        [
            "2",
            "timeOnTutoringSessionPS is high ∧ nCorrectKC is typical\n"
            "∧ pctCorrectAdd2Apply is high ∧ pctCorrectAdd3All is average",
            "Solve Alone"
        ],
        [
            "3",
            "nKCsSessionPS is high ∧ pctCorrectDeMorSelect is most\n"
            "∧ pctCorrectDeMorApply is about half",
            "Work Together"
        ]
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
        title="Example of Model Complexity",
        subtitle=None,
        table=table.scale(scale_factor=0.75),
        caption="KC is a knowledge component (e.g., Complement Theorem).",
        highlighted_columns=[]
    )


if __name__ == "__main__":
    get_lers_rules().render()
