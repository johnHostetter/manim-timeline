from manim import *


class DynamicAxes(MovingCameraScene):
    def construct(self):
        # Create Axes object
        axes_1 = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": BLUE},
        )

        axes_2 = Axes(
            x_range=[-50, 50, 1],
            y_range=[-50, 50, 1],
            x_length=25,
            y_length=25,
            axis_config={"color": BLUE},
        )

        # Add the Axes object to the scene
        self.add(axes_1)

        # Function to update y-axis dynamically
        # def update_y_axis(axes):
        #     t = self.time # Current time in animation
        #     y_min = -5 + 2 * np.sin(t)  # Example dynamic update for y_min
        #     y_max = 5 + 2 * np.sin(t)   # Example dynamic update for y_max
        #     axes.y_range = [y_min, y_max, 1]  # Update y_range
        #     axes.update_y_axis()  # Manually update y-axis

        # Always redraw function to continuously update y-axis
        # self.add_updater(update_y_axis, axes=axes)

        # axes.add_updater(update_y_axis)

        # Animate for some duration
        self.wait(5)

        self.play(
            TransformMatchingShapes(axes_1, axes_2, replace_mobject_with_target_in_scene=True),
            self.camera.frame.animate.set(
                width=axes_2.width + 1, height=axes_2.height + 1
            ).move_to(axes_2),
        )

        self.wait(5)

        # Remove updater
        # axes.remove_updater(update_y_axis)


if __name__ == "__main__":
    c = DynamicAxes()
    c.render()
