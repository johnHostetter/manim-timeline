from manim import *

class DynamicAxes(Scene):
    def construct(self):
        # Create Axes object
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": BLUE},
        )

        # Add the Axes object to the scene
        self.add(axes)

        # Function to update y-axis dynamically
        def update_y_axis(axes):
            t = self.time # Current time in animation
            y_min = -5 + 2 * np.sin(t)  # Example dynamic update for y_min
            y_max = 5 + 2 * np.sin(t)   # Example dynamic update for y_max
            axes.y_range = [y_min, y_max, 1]  # Update y_range
            axes.update_y_axis()  # Manually update y-axis

        # Always redraw function to continuously update y-axis
        self.add_updater(update_y_axis, axes=axes)

        # Animate for some duration
        self.wait(5)

        # Remove updater
        self.remove_updater(update_y_axis)


if __name__ == "__main__":
    c = DynamicAxes()
    c.render()
