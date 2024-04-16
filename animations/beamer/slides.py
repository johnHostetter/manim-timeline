from typing import Union as U, Type

from manim import *
from manim_slides import Slide

from animations.beamer.blocks import Block
from animations.beamer.lists import BeamerList


class PromptSlide(Slide):
    def __init__(self, prompt: str, skip: bool = False, **kwargs):
        super().__init__(**kwargs)
        # self.title_str: str = title
        self.prompt_str: str = prompt
        self.skip: bool = skip  # whether to not focus on the slide

        # # create the manim objects for the slide title
        # self.title_text: Text = Text(
        #     self.title_str,
        #     font="TeX Gyre Termes",
        #     color=BLACK,
        #     font_size=60,
        #     weight=BOLD,
        # ).to_edge(UP)
        # # create the overall contents of the slide
        # self.contents: VGroup = VGroup(self.title_text)

    def construct(self):
        self.draw(origin=ORIGIN, scale=1.0)
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(2)

    def draw(self, origin, scale, target_scene=None):
        if target_scene is None:
            target_scene = self
        target_scene.play(
            Write(
                Text(self.prompt_str, color=BLACK, slant=ITALIC)
                .move_to(origin)
                .scale(scale)
            )
        )
        target_scene.wait(2)


class BeamerSlide(MovingCameraScene, Slide):
    def __init__(self, title: str, subtitle: U[None, str], **kwargs):
        super().__init__(**kwargs)
        self.title_str: str = title
        self.subtitle_str: str = subtitle

        # create the manim objects for the slide title
        self.title_text: Text = Text(
            self.title_str,
            font="TeX Gyre Termes",
            color=BLACK,
            font_size=60,
            weight=BOLD,
        ).to_edge(UP)
        if self.subtitle_str is not None:
            self.subtitle_text: Text = Text(
                self.subtitle_str,
                font="TeX Gyre Termes",
                color=BLACK,
                font_size=30,
                slant=ITALIC,
            ).next_to(self.title_text, DOWN)
        # create the overall contents of the slide
        self.contents: VGroup = VGroup(self.title_text)
        if self.subtitle_str is not None:
            self.contents.add(self.subtitle_text)

    def inner_draw(self, origin, scale, target_scene=None) -> Text:
        """
        Draw the slide contents (title and subtitle - if applicable) on the scene
        and then return the last displayed text object.

        Args:
            origin: The origin of the slide.
            scale: The scale factor to apply to the slide contents.
            target_scene: The scene to draw the slide on. If None, the current scene is used.

        Returns:
            The last displayed text object.
        """
        if target_scene is None:
            target_scene = self

        # position the slide correctly
        self.contents.move_to(origin)
        self.contents.scale(scale)

        target_scene.wait(1)
        target_scene.next_slide()
        target_scene.play(Write(self.title_text))

        if self.subtitle_str is not None:
            target_scene.play(Write(self.subtitle_text))
            target_scene.wait(1)
            target_scene.next_slide()

        self.wait(1)
        self.next_slide()
        return (
            self.title_text if self.subtitle_str is None else self.subtitle_text
        )


class SlideWithList(BeamerSlide):
    def __init__(self, title: str, subtitle: U[None, str], beamer_list: BeamerList):
        super().__init__(title=title, subtitle=subtitle)
        self.beamer_list: BeamerList = beamer_list

    def construct(self):
        self.draw(ORIGIN, 1.0, target_scene=self)

    def draw(self, origin, scale: float, target_scene: U[None, Slide]):
        m_object_to_be_below = self.inner_draw(origin, scale, target_scene=target_scene)
        # create the list object
        list_group = self.beamer_list.get_list(scale_factor=scale, scale_down_text=False)
        buffer_with_prev_object = 0.5
        list_group.scale(scale_factor=scale).next_to(
            m_object_to_be_below, DOWN, buff=buffer_with_prev_object * scale
        )
        target_scene.play(Create(list_group))
        target_scene.wait(2)
        target_scene.next_slide()
        target_scene.wait(2)


class SlideWithBlocks(BeamerSlide):
    def __init__(
        self, title: str, subtitle: U[None, str], blocks: List[Type[Block]]
    ):
        super().__init__(title=title, subtitle=subtitle)
        self.blocks: List[Type[Block]] = blocks

    def make_block_and_focus(
        self,
        block: Block,
        scale: float,
        below: U[None, Text, Block],
        target_scene: U[None, Slide],
    ):
        if target_scene is None:
            target_scene = self
        target_scene.play(
            block.get_animation(scale_factor=scale, below=below),
            target_scene.camera.frame.animate.move_to(
                block.block_background.get_center()
            ).set(
                width=block.block_background.width + 3,
                # height=block.block_background.height + 3
            ),
        )

    def construct(self):
        self.draw(ORIGIN, 1.0, target_scene=self)

    def draw(self, origin, scale, target_scene: U[None, Slide]):
        m_object_to_be_below = self.inner_draw(origin, scale, target_scene=target_scene)
        # iterate over the blocks and create them
        for block in self.blocks:
            # for block in self.contents[1:]:
            if isinstance(block, Block):
                self.make_block_and_focus(
                    block,
                    scale=scale,
                    below=m_object_to_be_below,
                    target_scene=target_scene,
                )
                self.contents.add(block.get_vgroup())
                m_object_to_be_below = block.block_background
            else:
                # raise an error if the block is not a 'Block' object
                raise ValueError("Invalid block type. Must be a 'Block' object")
            target_scene.wait(1)
            target_scene.next_slide()
        # focus the camera on the entire slide
        target_scene.play(
            target_scene.camera.frame.animate.move_to(self.contents.get_center()).set(
                height=self.contents.height + 1
            )
        )
        target_scene.wait(3)
