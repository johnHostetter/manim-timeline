from manim import *

from animations.beamer.presentation.bibtex import BibTexManager
from animations.beamer.presentation.conclusion.avoiding_invalid import get_scalar_cardinality
from animations.beamer.slides import SlideWithBlocks
from animations.beamer.blocks import AlertBlock, ExampleBlock, RemarkBlock
from animations.beamer.lists import DisadvantagesList, AdvantagesList, ItemizedList

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def get_fyd_formula() -> SlideWithBlocks:
    """
    Create a slide discussing how to avoid invalid selections according to
    the epsilon-completeness property.

    Returns:
        The slide with the formula, remark, solution and word of caution.
    """
    # remark_block = RemarkBlock(
    #     title="Remarks",
    #     content=ItemizedList(
    #         items=[
    #             "Recall the importance of frequency from FYD.",
    #             "Recall a cutoff threshold was found w/ FYD.",
    #         ]
    #     ),
    # )
    bibtex_manager = BibTexManager()
    myTemplate = TexTemplate()
    myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
    alert_block = AlertBlock(
        title="Issue",
        content=DisadvantagesList(
            items=[
                "Rule simplification with LERS is costly",
                "Assumes binary truth values",
            ]
        ),
    )

    example_block = ExampleBlock(
        title="Proposed Solution",
        content=AdvantagesList(
            items=[
                "Mimic the behavior of LERs but incorporate fuzziness",
                "Zadeh\'s f-granulation theory to build graphs",
                bibtex_manager.slide_short_cite("tfig"),
                "Use the graph\'s structure to simplify rules",
                ItemizedList(
                    items=[
                        VGroup(
                            Text("Calculate closeness centrality", color=BLACK),
                            MathTex(r"C", color=BLACK),
                            Text(" for each vertex", color=BLACK),
                        ),
                        VGroup(
                            Text("Matrix ", color=BLACK),
                            MathTex(r"C", color=BLACK),
                            Text(
                                " is how reachable other premises are from shared rules",
                                color=BLACK
                            ),
                        ),
                        VGroup(
                            Text("Input variable ", color=BLACK),
                            Text("usage", color=BLACK, slant=ITALIC),
                            Text(" is its frequency across rules: ", color=BLACK),
                            MathTex(r"\deg(\mu_{v, t}) / |\mathcal{R}|", color=BLACK),
                        ),
                        VGroup(
                            Text(
                                "Premise term activation frequency is from ", color=BLACK
                            ),
                            Text("scalar cardinality", color=BLACK, slant=ITALIC),
                            MathTex(r"S", color=BLACK),
                        ),
                    ]
                )
            ]
        ),
    )
    myTemplate = TexTemplate()
    myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
    fyd_formula = MathTex(
        r"""
        \textit{FYD}(\mu_{v, t}) = 
        \overbrace{\frac{S_{v, t}}{\max(S)}}^{\text{Frequent}} 
        \overbrace{\wedge}^{\text{Yet}} \overbrace{\big ( 1 - (C_{v, t} 
        \wedge 
        (\deg(\mu_{v, t}) / |\mathcal{R}|) \big ))}^{\text{Discernible}}
        """,
        color=BLACK,
    )
    return SlideWithBlocks(
        title="Frequent-Yet-Discernible Formula",
        subtitle=None,
        blocks=[
            alert_block,
            example_block,
            get_scalar_cardinality(),
            fyd_formula,
        ],
    )


if __name__ == "__main__":
    get_fyd_formula().render()
