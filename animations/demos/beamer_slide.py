from abc import abstractmethod

from manim import *

from animations.beamer import AlertBlock, BeamerList
from soft.utilities.reproducibility import path_to_project_root

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class BulletedList(Scene):
    def construct(self):
        # Create each item in the bulleted list
        items = [
            "Item 1",
            "Item 2",
            "Item 3"
        ]

        # Create a VGroup to contain the bulleted list items
        list_group = VGroup(*[Text(f"• {item}", color=BLACK) for item in items])

        # Align the items vertically
        list_group.arrange(DOWN, aligned_edge=LEFT)

        # Add the bulleted list to the scene
        self.play(Write(list_group))
        self.wait()


class BeamerSlide(Scene):
    def construct(self):
        lst = BeamerList(items=[
            "Item 1",
            "Item 2",
            BeamerList(items=[
                "Subitem 1",
                "Subitem 2",
                BeamerList(items=[
                    "Subsubitem 1",
                    "Subsubitem 2"
                ])
            ])
        ])
        AlertBlock("PySoft", lst).add_to_scene(self)
        self.wait(2)


if __name__ == "__main__":
    # lst = BeamerList(items=[
    #     "Item 1",
    #     "Item 2",
    #     BeamerList(items=[
    #         "Subitem 1",
    #         "Subitem 2",
    #         BeamerList(items=[
    #             "Subsubitem 1",
    #             "Subsubitem 2"
    #         ])
    #     ])
    # ])
    # render_list = lst.get_list()
    beamer_slide = BeamerSlide()
    # lst.add_to_scene(beamer_slide, write=True)
    # beamer_slide.add(render_list)
    beamer_slide.render()
