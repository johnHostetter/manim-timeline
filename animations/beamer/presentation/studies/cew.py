from manim import *

from animations.beamer.slides import SlideDiagram
from animations.beamer.slides import SlideShow, SlideWithList
from animations.beamer.presentation.bibtex import BibTexManager
from animations.beamer.lists import ItemizedList, BulletedList as BL
from animations.beamer.presentation.studies.pyrenees import IntelligentTutoringSystemResults

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class CEW(SlideShow):
    def __init__(self, **kwargs):
        super().__init__(slides=[CEWDiagram(), CEWResults(), cew_summary()], **kwargs)


class CEWDiagram(SlideDiagram):
    def __init__(self, **kwargs):
        super().__init__(
            path="images/cew_diagram.png",
            caption="A diagram of the CLIP-ECM-Wang-Mendel (CEW)\n"
                    "systematic design process of NFNs.",
            original_image_scale=1.00,
            **kwargs
        )


class CEWResults(IntelligentTutoringSystemResults):
    def __init__(self):
        data: List[List[str]] = [
            [
                "CEW (N = 45)", ".744 (.138)", ".803 (.163)", ".187 (.658)", "1.58 (.680)"
            ],
            [
                "Expert (N = 47)", ".761 (.189)", ".683 (.165)", "-1.55 (3.80)", "1.80 (.946)"
            ],
        ]
        super().__init__(data, highlighted_columns=[2, 3])


def cew_summary() -> SlideWithList:
    """
    Create a slide summarizing my AAMAS 2023 paper.

    Returns:
        The slide with a short summary.
    """
    bibtex_manager = BibTexManager()
    return SlideWithList(
        title="Offline Model-Free Fuzzy Reinforcement Learning",
        subtitle="A Preliminary Systematic Design Process of NFNs",
        width_buffer=6.0,
        beamer_list=BL(
            items=[
                bibtex_manager.cite_entry(bibtex_manager["hostetter2023self"], num_of_words=8),
                "Primary Intuition",
                ItemizedList(
                    items=[
                        "CLIP constructs fuzzy sets & ECM identifies exemplars",
                        "Wang-Mendel algorithm constructs fuzzy rules from exemplars",
                        "Modify Fuzzy Q-Learning w/ CQL augmentation and train the NFN offline",
                    ]
                ),
                "Summary",
                ItemizedList(
                    items=[
                        "Effectiveness shown in Cart Pole & ITS",
                        "Great potential for offline RL if:",
                        BL(
                            items=[
                                "Limited data is available",
                                "Possible human expert knowledge",
                                "Need interpretation & accuracy",
                            ]
                        ),
                    ]
                ),
                "Contributions",
                ItemizedList(
                    items=[
                        "First dedicated offline model-free RL process w/ NFNs",
                        "Works well in high-dimensional spaces",
                    ]
                ),
                "Limitations",
                ItemizedList(
                    items=[
                        "The premises of fuzzy logic rule grows linear w/ number of inputs",
                        "Evaluated only on Cart Pole and our ITS",
                        "Computer vision",
                    ]
                ),
            ]
        ),
    )


if __name__ == "__main__":
    CEW().render()
