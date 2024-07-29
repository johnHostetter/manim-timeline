from manim import *
from manim_timeline.utils import get_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class SoritesParadox(Scene):
    def construct(self):
        # load the PySoft logo as a manim SVGMobject
        heap_svg = SVGMobject(
            get_project_root()
            / "animations"
            / "demos"
            / "images"
            / "Tannin_heap.svg"
        ).scale(2.0)

        self.play(Create(heap_svg, run_time=3))

        self.play(
            Write(
                Text("Sorites Paradox", font="TeX Gyre Termes", color=BLACK)
                .scale(2)
                .to_edge(UP)
            )
        )

        self.wait(2)


if __name__ == "__main__":
    c = SoritesParadox()
    c.render()
