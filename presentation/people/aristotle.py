from manim import *
from manim_slides import Slide

from manim_timeline.utils import get_project_root
from manim_timeline.quotes import quotable_person

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class Aristotle(Slide):
    def construct(self):
        paragraph, source, person, signature_group = self.draw(
            self, origin=ORIGIN, scale=1.0
        )
        self.wait(10)
        self.play(
            FadeOut(Group(VGroup(paragraph, person), signature_group), run_time=2)
        )
        self.wait(2)

    @staticmethod
    def draw(scene, origin, scale, animate: bool = True):
        signature = Text(
            "Ἀριστοτέλης (Aristotle)", font="TeX Gyre Termes", color=BLACK
        )  # .scale(0.7)
        person_svg = SVGMobject(
            get_project_root() / "assets" / "people" / "aristotle-2.svg"
        ).scale(2.0)
        paragraph, source, person, signature_group = quotable_person(
            scene,
            person_svg=person_svg,
            quote=(
                # "All people are mortal. \nSocrates is a person. \nTherefore, Socrates is mortal."
                # real version of the above quote:
                # https://dn790002.ca.archive.org/0/items/AristotleOrganon/AristotleOrganoncollectedWorks.pdf
                '"...we may say that Socrates is Socrates and a man, \n'
                "and that therefore he is the man Socrates, or that \n"
                "Socrates is a man and a biped, and that \n"
                'therefore he is a two-footed man."'
            ),
            source="(On Interpretation [Translated by E.M. Edghill] Chapter 11, pg. 67)",
            signature=signature,
            origin=origin,
            scale=scale,
            left_shift=1.0,
            animate=animate,
        )
        quote_1 = (
            '"A sea-fight must either take place tomorrow or not, \n'
            "but it is not necessary that it should take place \ntomorrow, "
            "neither is it necessary that it should not \ntake place, yet "
            'it is necessary that it either \nshould or should not take place tomorrow."'
        )
        quote_2 = (
            '"One of the two propositions in such instances \n'
            "must be true and the other false, but we cannot \n"
            "say determinately that this or that is false, \n"
            'but must leave the alternative undecided."'
        )
        paragraph_1 = (
            Text(quote_1, font="TeX Gyre Termes", color=BLACK, slant=ITALIC)
            .scale(0.7)
            .scale(scale_factor=scale)
            .move_to(paragraph.get_center())
            .next_to(source, UP)
        )
        new_source = (
            Text(
                "(On Interpretation [Translated by E.M. Edghill] Chapter 9, pg. 59-60)",
                font="TeX Gyre Termes",
                color=BLACK,
            )
            .scale(0.5)
            .scale(scale_factor=scale)
            .next_to(paragraph_1, DOWN)
        )
        paragraph_2 = (
            Text(quote_2, font="TeX Gyre Termes", color=BLACK, slant=ITALIC)
            .scale(0.7)
            .scale(scale_factor=scale)
            .move_to(paragraph.get_center())
            .next_to(source, UP)
        )
        if animate:
            # cycle through some other quotes
            scene.wait(1)
            scene.next_slide()
            scene.play(
                Transform(
                    paragraph, paragraph_1, replace_mobject_with_target_in_scene=True
                ),
                Transform(
                    source, new_source, replace_mobject_with_target_in_scene=True
                ),
            )
            scene.wait(2)

            scene.next_slide()
            scene.play(
                Transform(
                    paragraph_1, paragraph_2, replace_mobject_with_target_in_scene=True
                )
            )
        return paragraph, source, person, signature_group


if __name__ == "__main__":
    c = Aristotle()
    c.render()
