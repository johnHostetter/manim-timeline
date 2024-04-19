from manim import *

from animations.beamer.slides import SlideWithTable

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def get_fyd_rules() -> SlideWithTable:
    """
    Create a slide showing the rules from the FYD study.

    Returns:
        The slide with the study results.
    """
    data = [
        [
            "FYD", "IF the student only has a FEW hints\n"
                   "∧ student’s performance on this KC is AVERAGE\n"
                   "∧ they correctly answer De Morgan’s Law OFTEN"
        ],
        [
            "ECLAIRE", "IF [(s1 > 0) ∧ (s113 > 0.5) ∧ (s115 > 0.857)\n"
                       "∧ (s6 > 0.931) ∧ (s86 ≤ 0.056) ∧ (s93 ≤ 0.262)]\n"
                       "...\n"
                       "∨ [(s1 > 0) ∧ (s113 > 0) ∧ (s6 ≤ 0.962)\n"
                       "∧ (s6 > 0.956) ∧ (s76 > 0.925)]"
        ]
    ]
    table = Table(
        data,
        # row_labels=[Text("FYD"), Text("ECLAIRE")],
        col_labels=[
            Text("Condition", weight=BOLD),
            Text("Example Rule Premise", weight=BOLD)
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
        caption="KC is a knowledge component (e.g., Complement Theorem)."
    )


if __name__ == "__main__":
    get_fyd_rules().render()
