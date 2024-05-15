from manim import *

from animations.beamer.presentation.prototype.avoiding_invalid import (
    avoiding_invalid_selections,
)
from animations.beamer.presentation.prototype.constrained_gumbel_softmax import (
    constrained_gumbel_softmax,
)
from animations.beamer.presentation.prototype.gumbel_max_trick import gumbel_max_trick
from animations.beamer.presentation.prototype.issue_with_logits import issue_with_logits
from animations.beamer.presentation.prototype.notation import get_notation
from animations.beamer.presentation.prototype.numerical_instability import (
    fix_numerical_stability,
)
from animations.beamer.presentation.prototype.relax_links import relax_links
from animations.beamer.presentation.prototype.why_e_delayed import why_e_delayed
from animations.beamer.presentation.prototype.why_modify_gumbel import why_modify_gumbel
from animations.beamer.slides import SlideShow

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class MED(SlideShow):
    def __init__(self, **kwargs):
        super().__init__(
            slides=[
                # introduce necessary notation & formula
                get_notation(),
                # introduce the overall idea, make NFN more like DNN for flexibility
                relax_links(),
                # use gumbel max-trick to sample from a categorical distribution (the rules)
                issue_with_logits(),
                # how to avoid violating epsilon-completeness w/ gumbel max-trick
                why_modify_gumbel(),
                avoiding_invalid_selections(),
                # introduce the gumbel max-trick formula
                gumbel_max_trick(),
                # bound the logits used for it to prevent numerical instability
                fix_numerical_stability(),
                # constrain gumbel-softmax to avoid invalid rules that violate epsilon-completeness
                constrained_gumbel_softmax(),
                # briefly mention epsilon-delayed update to premise layer
                why_e_delayed(),
            ],
            **kwargs
        )


if __name__ == "__main__":
    MED().render()
