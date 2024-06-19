from manim import *

from presentation.introduction.proposal import get_proposal

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


if __name__ == "__main__":
    beamer_slide = get_proposal()
    beamer_slide.render()
