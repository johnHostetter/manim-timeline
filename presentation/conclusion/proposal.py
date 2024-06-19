from manim import *

from mbeamer.slides import SlideShow
from presentation.conclusion.plan import proposed_plan
from presentation.conclusion.new_horizons import proposed_studies
from presentation.conclusion.existing_issues import curr_limitations

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class Proposal(SlideShow):
    def __init__(self, **kwargs):
        super().__init__(
            slides=[
                curr_limitations(),
                proposed_plan(),
                proposed_studies(),
            ],
            **kwargs
        )


if __name__ == "__main__":
    Proposal().render()
