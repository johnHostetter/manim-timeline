from typing import Tuple
from manim import Axes, StealthTip, Text, DOWN, LEFT

from manim_timeline import ItemColor


class AxisConfig:
    def __init__(
        self, min_value: float, max_value: float, step: float, length: float = 10.0
    ):
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.length = length

    def get_range(self) -> Tuple[float, float, float]:
        return self.min_value, self.max_value, self.step


def make_axes(
    scene,
    x_axis_config: AxisConfig,
    y_axis_config: AxisConfig,
    stroke_width=3,
    axes_color=ItemColor.BACKGROUND,
):
    axes = Axes(
        x_range=x_axis_config.get_range(),
        y_range=y_axis_config.get_range(),
        x_length=x_axis_config.length,
        y_length=y_axis_config.length,
        # The axes will be stretched to match the specified
        # height and width
        # Axes is made of two NumberLine objects.  You can specify
        # their configuration with axis_config
        axis_config=dict(
            tip_shape=StealthTip,
            stroke_color=axes_color,
            stroke_width=stroke_width,
            numbers_to_exclude=[0],
            include_numbers=True,
            decimal_number_config=dict(color=axes_color),
        ),
        # # Alternatively, you can specify configuration for just one
        # # of them, like this.
        # y_axis_config=dict(
        #     numbers_with_elongated_ticks=[-2, 2],
        # )
    )

    # scene.add(axes)
    return axes


def add_labels_to_axes(ax, x_label, y_label, text_color=ItemColor.BACKGROUND):
    x_axis_lbl = Text(x_label, font_size=24, color=str(text_color))
    y_axis_lbl = Text(y_label, font_size=24, color=str(text_color))

    x_axis_lbl.next_to(ax, DOWN)
    y_axis_lbl.rotate(1.5708)
    y_axis_lbl.next_to(ax, LEFT)
    return x_axis_lbl, y_axis_lbl
