from manim import *
from soft.datasets import SupervisedDataset
from soft.fuzzy.logic.rules import LinguisticVariables
from soft.utilities.reproducibility import set_rng, load_configuration
from animations.common import (
    ItemColor,
    make_axes,
    get_data_and_env,
    AxisConfig,
)
from soft.fuzzy.sets.continuous.impl import Gaussian
from soft.fuzzy.unsupervised.granulation.online.clip import (
    apply_categorical_learning_induced_partitioning as CLIP,
)

set_rng(1)


class CLIPDemo(Scene):
    def __init__(self, **kwargs):
        super().__init__()
        background = ImageMobject("background.png").scale(2).set_color("#FFFFFF")
        self.add(background)
        self.fuzzy_sets = None

    def add_fuzzy_set(
        self,
        axes,
        center,
        width,
        element: float,
        dot,
        new_terms,
        x_axis_config: AxisConfig,
    ):
        if width < 0.1:
            # width is too small for animation
            width = 0.1
        temp_gaussian: Gaussian = Gaussian(centers=center, widths=width)
        print(center, width)
        step_val: float = (
            x_axis_config.max_value - x_axis_config.min_value
        ) / 1000  # the default is 1.0
        gaussian_graph = axes.plot(
            lambda x: temp_gaussian(x).degrees.item(),
            x_range=(x_axis_config.min_value, x_axis_config.max_value, step_val),
            stroke_color=ItemColor.ACTIVE_2,
            use_smoothing=True,
            # color=ORANGE
        )
        gaussian_label = axes.get_graph_label(
            gaussian_graph,
            Text("New Fuzzy Set"),
            color=ItemColor.ACTIVE_2,
            direction=UP,
        )
        self.fuzzy_sets.append(gaussian_graph)
        # self.add(gaussian_graph)
        self.play(
            Create(gaussian_graph),
            FadeIn(gaussian_label),
            dot.animate.move_to(
                axes.c2p(element, new_terms(element).degrees.max().item())
            ),
        )
        self.wait()
        self.play(
            FadeOut(gaussian_label),
            gaussian_graph.animate.set_color(ItemColor.INACTIVE_2),
            dot.animate.set_color(ItemColor.INACTIVE_1),
            # dot.animate.set_glow_factor(1.0)
        )

    def revise_fuzzy_sets(self, axes, new_terms, X):
        if new_terms is not None:
            animations = []
            for idx, center in enumerate(new_terms.centers.flatten()):
                gaussian_graph = axes.plot(
                    lambda x: new_terms(x).degrees[idx].detach().numpy().item(),
                    stroke_color=ItemColor.INACTIVE_2,
                    # use_smoothing=True,
                    # color=GREEN
                )
                try:
                    animations.append(
                        self.fuzzy_sets[idx].animate.become(gaussian_graph)
                    )
                    animations.extend(self.revise_data_points(axes, new_terms, X))
                except IndexError:  # there is no fuzzy set located at 'idx'
                    continue
            if len(animations) > 0:
                self.play(*animations)

    def revise_data_points(self, axes, new_terms, X):
        animations = []
        if self.data_dots is not None:
            for idx, dot in enumerate(self.data_dots):
                x = X[idx]
                animations.append(
                    dot.animate.move_to(
                        axes.c2p(x.flatten().item(), new_terms(x).degrees.max().item())
                    ),
                )
        return animations

    def construct(self):
        method = Text("Categorical Learning-Induced Partitioning", color=BLACK)
        self.play(Write(method, run_time=1))
        self.wait(3)
        # X, env = get_data_and_env(n_samples=1000)
        # X = X[:, 1]
        import torch

        # X = 2 * (torch.rand(10) - 0.5)
        X = torch.tensor(
            [
                0.2794,
                0.9486,
                0.6601,
                -0.9111,
                -0.9508,
                -0.4823,
                0.8781,
                -0.1666,
                0.4280,
                -0.4647,
            ]
        )
        # config = {
        #     "minimums": X.min(0).values,
        #     "maximums": X.max(0).values,
        #     "eps": 0.2,
        #     "kappa": 0.6,
        # }

        self.fuzzy_sets, self.data_dots = [], []
        x_axis_config = AxisConfig(X.min().item(), X.max().item(), step=0.1, length=8)
        axes = make_axes(
            self,
            x_axis_config=x_axis_config,
            y_axis_config=AxisConfig(0, 1.1, step=0.1, length=5),
            # stroke_width=0.02,
            axes_color=BLACK,
        )
        # x_axis_lbl, y_axis_lbl = add_labels_to_axes(
        #     axes, x_label="Cart Position", y_label="Degree of Membership"
        # )
        axis_labels: VGroup = axes.get_axis_labels(
            # axis labels are in math mode already
            x_label="x",
            y_label=r"\mu(x)",
            # x_label=r"\textit{Cart Position}",
            # y_label=r"\textit{Membership Degree}",
        ).set_color(BLACK)
        # rotate y label 90 degrees and move it to the left
        axis_labels[1].rotate(PI / 2).shift(1.5 * LEFT)

        self.play(
            RemoveTextLetterByLetter(method, run_time=1),
            Create(VGroup(axes, axis_labels)),
            # Create(VGroup(axes, x_axis_lbl, y_axis_lbl)),
        )

        old_terms, new_terms = None, None
        for idx, x in enumerate(X):
            x: float = x.item()  # x is a 1D tensor
            dot = Dot(color=str(ItemColor.ACTIVE_1))
            self.data_dots.append(dot)
            dot.move_to(axes.c2p(0, 0))

            # get the attention of the viewer to focus on the data point
            self.play(
                LaggedStart(
                    Create(dot),
                    Indicate(dot, scale_factor=1.5),
                    AnimationGroup(
                        dot.animate.set_glow_factor(1.0),
                        Flash(dot, color=ItemColor.ACTIVE_1),
                    ),
                )
            )

            self.play(dot.animate.move_to(axes.c2p(x, 0)))

            if old_terms is not None:
                degree = old_terms(x).degrees.max().item()
                self.play(dot.animate.move_to(axes.c2p(x, degree)))
                self.play(Circumscribe(dot, color=ItemColor.ACTIVE_2, run_time=3))
                line_graph = axes.plot(
                    lambda x: config.fuzzy.partition.epsilon, stroke_color=RED
                )
                dashed_line_graph = DashedVMobject(line_graph)
                self.play(Create(dashed_line_graph), run_time=2)
                self.wait()
                message = Text("Not Satisfied")
                if degree >= config.fuzzy.partition.epsilon:
                    message = Text("Satisfied")
                dashed_line_label = axes.get_graph_label(
                    line_graph, message, color=RED, direction=UP
                )
                self.play(FadeIn(dashed_line_label))
                self.wait()
                self.play(FadeOut(VGroup(dashed_line_label, dashed_line_graph)))

            selected_X = X[: idx + 1]
            if selected_X.ndim == 1:
                selected_X = selected_X.unsqueeze(dim=1)
            config = load_configuration()
            with config.unfreeze():
                config.fuzzy.partition.adjustment = 0.2
            linguistic_variables: LinguisticVariables = CLIP(
                dataset=SupervisedDataset(inputs=selected_X, targets=None),
                config=config,
            )
            new_terms = linguistic_variables.inputs[0]
            self.revise_fuzzy_sets(axes, new_terms, X)

            if (
                old_terms is None
                or new_terms.centers.flatten().shape[0]
                > old_terms.centers.flatten().shape[0]
            ):
                # new fuzzy set
                if new_terms.centers.ndim == 0:
                    center, width = new_terms.centers.item(), new_terms.widths.item()
                else:
                    center, width = (
                        new_terms.centers[-1].item(),
                        new_terms.widths[-1].item(),
                    )

                self.add_fuzzy_set(
                    axes, center, width, x, dot, new_terms, x_axis_config=x_axis_config
                )

            else:
                self.play(
                    dot.animate.move_to(axes.c2p(x, new_terms(x).degrees.max().item())),
                    # dot.animate.set_color(PURPLE_A),
                    dot.animate.set_glow_factor(1.0),
                )
            # self.revise_fuzzy_sets(axes, new_terms, X)
            self.play(dot.animate.set_color(str(ItemColor.INACTIVE_1)))
            self.wait()
            old_terms = new_terms
        self.wait(1)


if __name__ == "__main__":
    c = CLIPDemo()
    c.render()
    # c.construct()
