from manim import *


class ValueTrackerPlot(Scene):
    def construct(self):
        a = ValueTracker(1)
        ax = Axes(
            x_range=[-2, 2, 1],
            y_range=[-8.5, 8.5, 1],
            x_length=4,
            y_length=6,
            axis_config={"color": BLUE},
        )
        parabola = ax.plot(lambda x: x**2, color=RED)  # does not get used
        parabola.add_updater(
            lambda m_object: m_object.become(
                ax.plot(lambda x: a.get_value() * x**2, color=RED)
            )
        )
        a_number = DecimalNumber(
            a.get_value(), color=RED, num_decimal_places=3, show_ellipsis=True
        )
        a_number.add_updater(
            lambda m_object: m_object.set_value(a.get_value())
        ).next_to(ax, UP)
        self.add(ax, parabola, a_number)
        self.play(a.animate.set_value(2), run_time=2)
        self.play(a.animate.set_value(-2), run_time=2)
        self.play(a.animate.set_value(1), run_time=2)


if __name__ == "__main__":
    c = ValueTrackerPlot()
    c.render()
