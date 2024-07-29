from manim import *

from manim_beamer.slides import SlideWithList
from manim_beamer.lists import ItemizedList, BulletedList as BL

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def gumbel_max_trick() -> SlideWithList:
    """
    Create a slide discussing how to use the Gumbel-Max Trick.

    Returns:
        The slide describing how Gumbel noise is used to add stochasticity.
    """
    # alert_block = AlertBlock(
    #     title="Issue",
    #     content=DisadvantagesList(
    #         items=[
    #             "NFN training may cause logits to grow too large.",
    #             "Subsequent calculations (e.g., exp) may yield NaNs\nor infinities.",
    #         ]
    #     )
    # )
    # example_block = ExampleBlock(
    #     title="Proposed Solution",
    #     content=AdvantagesList(
    #         items=[
    #             "Bound the logits."
    #         ]
    #     )
    # )

    # sentence_1 = Tex(
    #     r"Restrict logits to $[-\kappa, \kappa]$ by modifying \texttt{Sigmoid} such that",
    #     color=BLACK
    # )

    myTemplate = TexTemplate()
    myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
    # formula = MathTex(
    #     r"\texttt{BoundSigmoid}(\tilde{L'}) = \frac{2\kappa}"
    #     r"{1 + \exp^{(-\tilde{L'} / {2\kappa})}} - \kappa",
    #     color=BLACK
    # ).next_to(sentence_1, DOWN)
    # sentence_2 = Tex(
    #     r"applies a simple bounding operation to $\tilde{L}'$.", color=BLACK
    # ).next_to(formula, DOWN)
    return SlideWithList(
        title="Gumbel Noise for Stochasticity",
        subtitle=None,
        beamer_list=ItemizedList(
            items=[
                VGroup(
                    Text("For stochasticity, we add Gumbel noise, ", color=BLACK),
                    MathTex(r"N", color=BLACK),
                ),
                VGroup(
                    Text("Soften distribution w/ temperature parameter ", color=BLACK),
                    MathTex(r"\tau", color=BLACK),
                ),
                VGroup(
                    Text("For noise matrix ", color=BLACK),
                    MathTex(r"N", color=BLACK),
                ),
                BL(
                    items=[
                        "If training, sample from Gumbel distribution",
                        ItemizedList(
                            items=[
                                VGroup(
                                    Text("Let ", color=BLACK),
                                    MathTex(r"N", color=BLACK),
                                    Text(" be a matrix of sampled noise", color=BLACK),
                                    # MathTex(r"\mathcal{R}", color=BLACK)
                                ),
                                VGroup(
                                    Text("Shape is", color=BLACK),
                                    VGroup(
                                        MathTex(r"|{\mathcal{R}}|", color=BLACK),
                                        Cross(color=BLACK, stroke_width=3).scale(
                                            scale_factor=0.1
                                        ),
                                        MathTex(r"|{\mathcal{V}}|", color=BLACK),
                                        Cross(color=BLACK, stroke_width=3).scale(
                                            scale_factor=0.1
                                        ),
                                        MathTex(
                                            r"{\max_{v} |\mathcal{T}|}|", color=BLACK
                                        ),
                                    ),
                                ),
                            ]
                        ),
                        VGroup(
                            Text("If evaluating, let ", color=BLACK),
                            MathTex(r"N", color=BLACK),
                            Text(" contain all zeros", color=BLACK),
                        ),
                    ]
                ),
            ]
        ),
    )


if __name__ == "__main__":
    gumbel_max_trick().render()
