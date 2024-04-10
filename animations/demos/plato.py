from manim import *

from animations.demos.einstein import person_with_quote
from soft.utilities.reproducibility import path_to_project_root


class PlatoTheoryOfForms(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        background = ImageMobject("background.png").scale(2).set_color("#FFFFFF")
        self.add(background)

    def construct(self):
        # signature = Text(
        #     "Πλάτων (Plato)", font="TeX Gyre Termes", color=BLACK
        # )#.scale(0.7)
        #
        # paragraph, person, signature_group = person_with_quote(
        #     self,
        #     path_to_person_svg=(
        #         path_to_project_root()
        #         / "animations"
        #         / "demos"
        #         / "Plato.svg"
        #     ),
        #     quote=(
        #         "\"Reality is created by the mind, we can \n"
        #         "change our reality by changing our mind.\""
        #     ),
        #     signature=signature,
        # )
        #
        # self.wait(10)
        # self.play(
        #     FadeOut(
        #         Group(
        #             paragraph,
        #             signature_group
        #         ), run_time=2
        #     )
        # )
        # self.wait(2)
        #
        # header = Text("Plato's Theory of Forms", font="TeX Gyre Termes").scale(1.0)
        # self.play(Write(header), run_time=3)
        # self.wait(2)
        # subheader = Text("The Allegory of the Cave", font="TeX Gyre Termes").scale(0.7)

        earth = SVGMobject(
            path_to_project_root() / "animations" / "demos" / "Earth.svg"
        )

        self.play(Create(earth, run_time=3))


if __name__ == "__main__":
    c = PlatoTheoryOfForms()
    c.render()
