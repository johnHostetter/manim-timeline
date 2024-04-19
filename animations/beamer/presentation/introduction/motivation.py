from manim import *

from animations.beamer.presentation.introduction.dnn import pros_and_cons as dnn_pros_and_cons
from animations.beamer.presentation.introduction.nfn import pros_and_cons as nfn_pros_and_cons
from animations.beamer.presentation.introduction.proposal import get_proposal
from animations.beamer.presentation.introduction.outline import get_outline
from animations.beamer.slides import SlideShow

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class Motivation(SlideShow):
    def __init__(self, **kwargs):
        super().__init__(
            slides=[
                dnn_pros_and_cons(),
                nfn_pros_and_cons(),
                get_proposal(),
                get_outline(),
            ], **kwargs
        )


if __name__ == "__main__":
    Motivation().render()
