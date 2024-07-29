from manim import *

from manim_beamer.bibtex import BibTexManager
from manim_beamer.lists import ItemizedList, BulletedList as BL
from manim_beamer.slides import SlideShow, SlideWithList, SlideDiagram

from manim_timeline.utils import get_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class LLM(SlideShow):
    def __init__(self, **kwargs):
        super().__init__(slides=[LLMDiagram(), llm_summary()], **kwargs)


class LLMDiagram(SlideDiagram):
    def __init__(self, **kwargs):
        super().__init__(
            path=get_project_root() / "assets" / "images" / "llm_diagram.png",
            caption="A diagram of the Latent Lockstep Method (LLM)\n"
            "systematic design process of NFNs.",
            original_image_scale=1.00,
            **kwargs
        )


def llm_summary() -> SlideWithList:
    """
    Create a slide with my proposed studies for the completion of my dissertation.

    Returns:
        The slide with a list of studies.
    """
    bibtex_manager = BibTexManager(path=get_project_root() / "presentation" / "ref.bib")
    return SlideWithList(
        title="Identifying Exemplars by Leveraging Latent Representations",
        subtitle="The Latent Lockstep Method (LLM)",
        beamer_list=BL(
            items=[
                bibtex_manager.cite_entry(
                    bibtex_manager["hostetter2023latent"], num_of_words=8
                ),
                "Primary Intuition",
                ItemizedList(
                    items=[
                        "Data is unique if the latent encoding is unique",
                    ]
                ),
                "Summary",
                ItemizedList(
                    items=[
                        "Latent representations identify exemplars",
                        "Simple, yet effective problem-independent method",
                    ]
                ),
                "Contributions",
                ItemizedList(
                    items=[
                        "Problem independent exemplar identification",
                        "Works well in high-dimensional spaces",
                    ]
                ),
                "Limitations",
                ItemizedList(
                    items=[
                        "Fuzzy rules' premises grows linear w/ number of inputs",
                        "Chosen encoder architecture may not be ideal",
                    ]
                ),
            ]
        ),
    )


if __name__ == "__main__":
    LLM().render()
