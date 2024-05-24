from manim import *

from animations.beamer.slides import SlideWithList, SlideWithBlocks
from animations.beamer.presentation.bibtex import BibTexManager

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def high_dim_trick() -> SlideWithList:
    """
    Create a slide discussing how to use the Gumbel-Max Trick.

    Returns:
        The slide describing how Gumbel noise is used to add stochasticity.
    """
    bibtex_manager = BibTexManager()
    return SlideWithBlocks(
        title="High-Dimensional Inference",
        subtitle=bibtex_manager.cite_entry(
            bibtex_manager["cui_curse_2021"], num_of_words=8
        ),
        blocks=[
            Text("GaussianNoExp", color=BLACK, slant=ITALIC),
            VGroup(
                MathTex(
                    r"""
                    \mu_{v, t}(x_{v}) = -\Bigg(
                    \frac{(x_{v} - \texttt{core}_{v, t})^2}
                    {2\sigma_{v, t}^2}
                    \Bigg)
                    """,
                    color=BLACK,
                )
            ),
        ],
    )


if __name__ == "__main__":
    high_dim_trick().render()
