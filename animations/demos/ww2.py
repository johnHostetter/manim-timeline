from manim import *

from animations.demos.einstein import person_with_quote
from soft.utilities.reproducibility import path_to_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class WW2(MovingCameraScene):
    def construct(self):
        svg_file_names: List[str] = [
            "germans_in_poland_1939",
            "germans_after_invading_poland_sept_1_1939",
            "first_mass_bombing_in_london_sept_7_1940",
            "germans_attack_soviets_eastern_front_june_22_1941",
            "soviet_offensive_against_germans_in_stalingrad_feb_1943",
            "us_marines_iwo_jima_feb_23_1945",
            "russians_in_reichstag_berlin_april_30_1945",
            "nagasaki_aug_9_1945",
        ]
        captions = [
            "Germans invading Poland, 1939",
            "Germans after invading Poland, Sept 1, 1939",
            "First mass bombing in London, Sept 7, 1940",
            "Germans attack Soviets, Eastern Front, June 22, 1941",
            "Soviet offensive against Germans in Stalingrad, Feb 1943",
            "US Marines, Iwo Jima, Feb 23, 1945",
            "Russians in Reichstag, Berlin, April 30, 1945",
            "Nagasaki, Aug 9, 1945",
        ]

        last_svg = None
        for svg_file_name, caption in zip(svg_file_names, captions):
            svg = SVGMobject(
                path_to_project_root() / "animations" / "demos" / "ww2" / f"{svg_file_name}.svg"
            ).scale(2)
            text = Text(caption, font="TeX Gyre Termes", color=BLACK).scale(0.7).next_to(svg, DOWN)

            if last_svg is None:
                self.play(Create(svg, run_time=3), Write(text, run_time=3))
            else:
                self.play(ReplacementTransform(last_svg, svg, run_time=3), Write(text, run_time=3))
            self.play(Succession(Wait(2), FadeOut(text)))
            last_svg = svg
        self.wait(3)


if __name__ == "__main__":
    c = WW2()
    c.render()
