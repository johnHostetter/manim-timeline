from typing import Union as U, Type

from manim import *
from manim_slides import Slide

from animations.beamer.blocks import AlertBlock, ExampleBlock, Block
from animations.beamer.lists import ItemizedList, AdvantagesList, DisadvantagesList

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class SlideWithBlocks(MovingCameraScene, Slide):
    def __init__(self, title: str, blocks: List[Type[Block]], **kwargs):
        super().__init__(**kwargs)
        self.slide_title = title
        self.blocks = blocks

    def make_block_and_focus(self, block: Block, below: U[None, Text, Block]):
        self.play(
            block.get_animation(below=below),
            self.camera.frame.animate.move_to(block.block_background.get_center()).set(
                width=block.block_background.width + 3,
                # height=block.block_background.height + 3
            )
        )

    def construct(self):
        slide_title = Text(
            self.slide_title,
            font="TeX Gyre Termes",
            color=BLACK,
            font_size=60,
            weight=BOLD
        )
        slide_title.to_edge(UP)
        self.wait(1)
        self.next_slide()
        self.play(Write(slide_title))

        slide_vgroup = VGroup(slide_title)
        self.wait(1)
        self.next_slide()
        # self.make_block_and_focus(example_block, below=None)
        m_object_to_be_below = slide_title
        for block in self.blocks:
            if isinstance(block, Block):
                self.make_block_and_focus(block, below=m_object_to_be_below)
                slide_vgroup.add(block.block_background)
                m_object_to_be_below = block.block_background
            else:
                raise ValueError(
                    "Invalid block type. Must be a 'Block' object"
                )
            self.wait(1)
            self.next_slide()
        # self.make_block_and_focus(example_block, below=slide_title)
        # self.wait(1)
        # self.next_slide()

        # self.next_slide()
        # self.make_block_and_focus(alert_block, below=example_block)
        # slide_vgroup.add(example_block.block_background, alert_block.block_background)
        # self.wait(1)
        # self.next_slide()
        self.play(
            self.camera.frame.animate.move_to(slide_vgroup.get_center()).set(
                height=slide_vgroup.height + 1
            )
        )
        self.wait(3)


if __name__ == "__main__":
    example_block = ExampleBlock(
        title="Advantages",
        content=AdvantagesList(
            items=[
                "Reliable",
                ItemizedList(
                    items=[
                        "Applications to robotics, medicine, etc.",
                    ]
                ),
                "Flexible",
                ItemizedList(
                    items=[
                        "Network morphism (e.g., add neurons or layers)",
                    ]
                ),
                "Generalizable",
                ItemizedList(
                    items=[
                        "Supervised learning",
                        "Online/offline reinforcement learning",
                        "and more..."
                    ]
                ),
            ]
        )
    )
    alert_block = AlertBlock(
        title="Disadvantages",
        content=DisadvantagesList(
            items=[
                "Relies upon large quantities of data",
                "Difficult to interpret (i.e., black-box)"
            ]
        )
    )
    beamer_slide = SlideWithBlocks(
        title="Deep Neural Networks (DNNs)",
        blocks=[example_block, alert_block],
    )
    beamer_slide.render()
