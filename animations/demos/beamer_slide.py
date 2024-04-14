from manim import *

from animations.beamer.presentation.introduction.dnn import (
    pros_and_cons as dnn_pros_and_cons,
)
from animations.beamer.presentation.introduction.nfn import (
    pros_and_cons as nfn_pros_and_cons,
)

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


if __name__ == "__main__":
    beamer_slide = nfn_pros_and_cons()
    beamer_slide.render()
