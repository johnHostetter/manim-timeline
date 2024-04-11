from manim import *
from typing import Union as U

from soft.utilities.reproducibility import path_to_project_root


class SoritesParadox(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = ImageMobject("background.png").scale(2).set_color("#FFFFFF")
        self.add(background)

    def construct(self):
        # load the PySoft logo as a manim SVGMobject
        heap_svg = SVGMobject(
            path_to_project_root() / "animations" / "demos" / "images" / "Tannin_heap.svg"
        ).scale(2.0)

        self.play(Create(heap_svg, run_time=3))

        self.play(
            Write(
                Text("Sorites Paradox", font="TeX Gyre Termes", color=BLACK).scale(2).to_edge(UP)
            )
        )

        self.wait(2)


if __name__ == "__main__":
    c = SoritesParadox()
    c.render()
