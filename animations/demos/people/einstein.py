from manim import *
from typing import Union as U

from soft.utilities.reproducibility import path_to_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def person_with_quote(
    scene: Scene,
    person_svg: SVGMobject,
    quote: str,
    source: str,
    signature: U[SVGMobject, Text],
    origin: np.ndarray,
    scale: float,
    left_shift: float = 0.5,
    animate: bool = True,
):
    paragraph = (
        Paragraph(quote, font="TeX Gyre Termes", slant=ITALIC, color=BLACK)
        .scale(0.7)
        .next_to(signature, UP)
    )
    source_text = (
        Text(source, font="TeX Gyre Termes", color=BLACK)
        .scale(0.5)
        .next_to(paragraph, DOWN)
    )
    person_and_quote = VGroup(paragraph, person_svg, source_text)
    person_and_quote.scale(scale_factor=scale)
    # person_bound = person_svg.get_bounding_box()
    # person_svg.next_to(paragraph, scale*LEFT, buff=0.0*scale)
    person_svg.move_to(paragraph, aligned_edge=LEFT).shift(
        person_svg.width * left_shift * LEFT
    )
    person_and_quote.move_to(origin)
    # person_svg.move_to(paragraph, ((4 * DOWN) + (12 * LEFT))).scale(2)
    # scene.play(Write(paragraph), run_time=3)

    # scene.play(paragraph.animate.shift(RIGHT * 2), run_time=1)
    if animate:
        scene.play(
            AnimationGroup(
                Create(person_svg, run_time=2),
                Write(VGroup(paragraph, source_text), run_time=2),
                lag_ratio=0.5,
            )
        )
    else:
        scene.add(person_and_quote)

    signature_dash = (
        Text("- ", font="TeX Gyre Termes")
        .scale(2)
        .next_to(signature, LEFT)
        # .next_to(paragraph, (1.5 * DOWN) + RIGHT)
        .set_color(BLACK)
    )
    signature_combo = VGroup(signature_dash, signature).scale(scale_factor=scale)
    signature_combo.next_to(VGroup(paragraph, person_svg), scale * DOWN)
    # signature.next_to(signature_dash, RIGHT).set_color(BLACK)

    # add the signature to the scene
    if animate:
        scene.play(Create(signature_combo, run_time=2))
        scene.wait(1)
    else:
        scene.add(signature_combo)
    return paragraph, source_text, person_svg, signature_combo


class EinsteinQuote(Scene):
    def construct(self):
        paragraph, source, person, signature_group = self.draw(
            self, origin=ORIGIN, scale=1.0
        )
        self.wait(10)
        self.play(
            FadeOut(
                Group(VGroup(paragraph, source, person), signature_group), run_time=2
            )
        )
        self.wait(2)

    @staticmethod
    def draw(scene, origin, scale, animate: bool = True):
        signature = SVGMobject(
            path_to_project_root()
            / "animations"
            / "demos"
            / "assets"
            / "signatures"
            / "Albert_Einstein_signature_1934.svg"
        ).scale(0.5)
        person_svg = SVGMobject(
            path_to_project_root()
            / "animations"
            / "demos"
            / "assets"
            / "people"
            / "Einstein1.svg"
        ).scale(2.0)
        paragraph, source, person, signature_group = person_with_quote(
            scene,
            person_svg=person_svg,
            quote=(
                '"As far as the laws of mathematics refer to reality,\nthey are not certain; '
                'And as far as they are certain, \nthey do not refer to reality."'
            ),
            # originally published in 1921 as a lecture delivered by Einstein at the Prussian Academy of Sciences
            source="(Geometry and Experience, 1921)",
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1,
            animate=animate,
        )
        return paragraph, source, person, signature_group


if __name__ == "__main__":
    c = EinsteinQuote()
    c.render()
