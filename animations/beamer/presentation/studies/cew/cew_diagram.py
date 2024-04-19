from abc import abstractmethod

from manim import *
from manim_slides import Slide

from animations.demos.ww2 import CaptionedJPG

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class SlideDiagram(Slide):
    def __init__(self, path, caption, original_image_scale, **kwargs):
        super().__init__(**kwargs)
        self.path = path
        self.caption = caption
        self.original_image_scale = original_image_scale
        self.captioned_jpg: CaptionedJPG = self.get_diagram()

    def construct(self, origin=ORIGIN, scale=1.0):
        self.draw(origin, scale, target_scene=self)

    def draw(self, origin, scale, target_scene=None, animate=True):
        self.captioned_jpg.draw(origin, scale, target_scene=target_scene, animate=animate)

    def get_diagram(self) -> CaptionedJPG:
        """
        Create a slide showing the diagram of the CEW systematic design process of NFNs.

        Returns:
            The slide with the diagram shown.
        """
        return CaptionedJPG(
            path=self.path,
            caption=self.caption,
            original_image_scale=self.original_image_scale
        )


class CEWDiagram(SlideDiagram):
    def __init__(self, **kwargs):
        super().__init__(
            path="images/cew_diagram.png",
            caption="A diagram of the CLIP-ECM-Wang-Mendel (CEW)\n"
                    "systematic design process of NFNs.",
            original_image_scale=1.00,
            **kwargs
        )


class LLMDiagram(SlideDiagram):
    def __init__(self, **kwargs):
        super().__init__(
            path="images/llm_diagram.png",
            caption="A diagram of the Latent Lockstep Method (LLM)\n"
                    "systematic design process of NFNs.",
            original_image_scale=1.00,
            **kwargs
        )


if __name__ == "__main__":
    LLMDiagram().render()
