from manim import *
from manim_slides import Slide
from soft.datasets import LabeledDataset
from soft.fuzzy.logic.rules import LinguisticVariables
from soft.utilities.reproducibility import set_rng, load_configuration
from soft.fuzzy.sets.continuous.impl import Gaussian
from soft.fuzzy.unsupervised.granulation.online.clip import (
    apply_categorical_learning_induced_partitioning as CLIP,
)
from unit_tests.computing.test_self_organize import get_cart_pole_example_data
from examples.common import (
    ItemColor,
    make_axes,
    get_data_and_env,
    AxisConfig,
)

set_rng(1)

config.disable_caching = True  # may need to disable caching for the timeline
config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class CLIPDemo(Slide, MovingCameraScene):
    def __init__(self, **kwargs):
        super().__init__()
        # background = ImageMobject("background.png").scale(2).set_color("#FFFFFF")
        # self.add(background)
        self.fuzzy_sets = None
        self.default_text_scale_multiplier: float = 1.0  # use 5.0 if in timeline
        self.default_scale_multiplier: float = 5.0

    def add_fuzzy_set(
        self,
        axes,
        center,
        width,
        element: float,
        dot,
        new_terms,
        x_axis_config: AxisConfig,
        scale,
        target_scene=None,
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
            stroke_width=(3 * scale),
            use_smoothing=True,
            # color=ORANGE
        )
        gaussian_label = axes.get_graph_label(
            gaussian_graph,
            Text("New Fuzzy Set").scale(scale_factor=scale),
            color=ItemColor.ACTIVE_2,
            direction=UP * scale,
        )
        self.fuzzy_sets.append(gaussian_graph)
        # self.add(gaussian_graph)
        target_scene.play(
            Create(gaussian_graph),
            FadeIn(gaussian_label),
            dot.animate.move_to(
                axes.c2p(element, new_terms(element).degrees.max().item())
            ),
        )
        target_scene.wait()
        target_scene.play(
            FadeOut(gaussian_label),
            gaussian_graph.animate.set_color(ItemColor.INACTIVE_2),
            dot.animate.set_color(ItemColor.INACTIVE_1),
            # dot.animate.set_glow_factor(1.0)
        )

    def revise_fuzzy_sets(self, axes, new_terms, X, scale, target_scene):
        if new_terms is not None:
            animations = []
            for idx, center in enumerate(new_terms.centers.flatten()):
                gaussian_graph = axes.plot(
                    lambda x: new_terms(x).degrees[idx].detach().numpy().item(),
                    stroke_color=ItemColor.INACTIVE_2,
                    stroke_width=(self.default_scale_multiplier * scale),
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
                target_scene.play(*animations)

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
        self.draw(origin=ORIGIN, scale=1.0)

    def draw(self, origin=ORIGIN, scale=1.0, target_scene=None, animate: bool = True):
        if target_scene is None:
            target_scene = self
        method = (
            Text("Categorical Learning-Induced Partitioning", color=BLACK)
            .scale(scale_factor=scale)
            .move_to(origin)
        )
        if not animate:
            # do not animate the demo
            target_scene.add(method)
        else:
            # target_scene.camera.frame.move_to(method.get_center()).set(width=method.width + 1)
            target_scene.play(Write(method, run_time=1))
            target_scene.wait(3)
            target_scene.next_slide()
            # X, env = get_data_and_env(n_samples=1000)
            # X = X[:, 1]
            import torch

            # X = 2 * (torch.rand(10) - 0.5)
            X = torch.tensor(
                [
                    0.2794,
                    0.9486,
                    0.6301,
                    # -0.9111,
                    -0.9508,
                    -0.4823,
                    # 0.8781,
                    # -0.1666,
                    # 0.4280,
                    # -0.4647,
                ]
            )
            X = get_cart_pole_example_data()[:, 0]
            # config = {
            #     "minimums": X.min(0).values,
            #     "maximums": X.max(0).values,
            #     "eps": 0.2,
            #     "kappa": 0.6,
            # }

            self.fuzzy_sets, self.data_dots = [], []
            x_axis_config = AxisConfig(
                X.min().item(), X.max().item(), step=0.1, length=8
            )  # step was 0.1
            axes = make_axes(
                target_scene,
                x_axis_config=x_axis_config,
                y_axis_config=AxisConfig(0, 1.1, step=0.1, length=5),
                stroke_width=1 * scale,
                axes_color=BLACK,
            )
            # x_axis_lbl, y_axis_lbl = add_labels_to_axes(
            #     axes, x_label="Cart Position", y_label="Degree of Membership"
            # )
            axis_labels: VGroup = axes.get_axis_labels(
                # axis labels are in math mode already
                x_label="s_{1}",
                y_label=r"\mu(s_{1})",
                # x_label=r"\textit{Cart Position}",
                # y_label=r"\textit{Membership Degree}",
            ).set_color(BLACK)
            axis_labels[0].scale(
                scale_factor=(self.default_text_scale_multiplier * scale)
            )
            # rotate y label 90 degrees and move it to the left
            axis_labels[1].rotate(PI / 2).shift(1.5 * LEFT * scale).scale(
                scale_factor=(self.default_text_scale_multiplier * scale)
            )
            axis_group = (
                VGroup(axes, axis_labels).scale(scale_factor=scale).move_to(origin)
            )

            target_scene.play(
                Succession(
                    FadeOut(method),
                    Create(axis_group),
                    target_scene.camera.frame.animate.move_to(
                        axis_group.get_center()
                    ).set(
                        width=axis_group.width + 1, height=axis_group.height + 1
                    ),  # height originally not included
                    run_time=2,
                )
                # Create(VGroup(axes, x_axis_lbl, y_axis_lbl)),
            )

            target_scene.next_slide()

            old_terms, new_terms = None, None
            for idx, x in enumerate(X):
                x: float = x.item()  # x is a 1D tensor
                dot = Dot(color=str(ItemColor.ACTIVE_1)).scale(
                    scale_factor=((self.default_scale_multiplier / 3) * scale)
                )
                self.data_dots.append(dot)
                dot.move_to(axes.c2p(0, 0))

                target_scene.wait()
                target_scene.next_slide()

                # get the attention of the viewer to focus on the data point
                target_scene.play(
                    LaggedStart(
                        Create(dot),
                        Indicate(dot, scale_factor=1.5),
                        AnimationGroup(
                            dot.animate.set_glow_factor(1.0),
                            Flash(dot, color=ItemColor.ACTIVE_1),
                        ),
                    )
                )

                target_scene.play(dot.animate.move_to(axes.c2p(x, 0)))

                if old_terms is not None:
                    degree = old_terms(x).degrees.max().item()
                    target_scene.play(dot.animate.move_to(axes.c2p(x, degree)))
                    target_scene.wait()
                    target_scene.next_slide(loop=True)
                    target_scene.play(
                        Circumscribe(
                            dot,
                            color=ItemColor.ACTIVE_2,
                            stroke_width=(self.default_scale_multiplier * scale),
                            run_time=2,
                        )
                    )
                    target_scene.wait()
                    target_scene.next_slide()
                    line_graph = axes.plot(
                        lambda x: config.fuzzy.partition.epsilon,
                        stroke_color=RED,
                        stroke_width=(self.default_scale_multiplier * scale),
                    )
                    dashed_line_graph = DashedVMobject(line_graph)
                    target_scene.wait()
                    target_scene.next_slide()
                    target_scene.play(Create(dashed_line_graph), run_time=2)
                    target_scene.wait()
                    message_str = "Not Satisfied"
                    if degree >= config.fuzzy.partition.epsilon:
                        message_str = "Satisfied"
                    # message_str = ''
                    dashed_line_label = axes.get_graph_label(
                        line_graph,
                        Text(message_str).scale(scale_factor=scale),
                        color=RED,
                        direction=UP * scale,
                    )
                    target_scene.play(FadeIn(dashed_line_label))
                    target_scene.wait()
                    target_scene.next_slide()
                    target_scene.play(
                        # FadeOut(dashed_line_graph)
                        FadeOut(VGroup(dashed_line_label, dashed_line_graph))
                    )

                selected_X = X[: idx + 1]
                if selected_X.ndim == 1:
                    selected_X = selected_X.unsqueeze(dim=1)
                config = load_configuration()
                with config.unfreeze():
                    config.fuzzy.partition.adjustment = 0.2
                linguistic_variables: LinguisticVariables = CLIP(
                    dataset=LabeledDataset(data=selected_X, labels=None),
                    config=config,
                )
                new_terms = linguistic_variables.inputs[0]
                self.revise_fuzzy_sets(
                    axes, new_terms, X, scale=scale, target_scene=target_scene
                )

                if (
                    old_terms is None
                    or new_terms.centers.flatten().shape[0]
                    > old_terms.centers.flatten().shape[0]
                ):
                    # new fuzzy set
                    if new_terms.centers.ndim == 0:
                        center, width = (
                            new_terms.centers.item(),
                            new_terms.widths.item(),
                        )
                    else:
                        center, width = (
                            new_terms.centers[-1].item(),
                            new_terms.widths[-1].item(),
                        )

                    self.add_fuzzy_set(
                        axes,
                        center,
                        width,
                        x,
                        dot,
                        new_terms,
                        x_axis_config=x_axis_config,
                        scale=scale,
                        target_scene=target_scene,
                    )

                else:
                    target_scene.play(
                        dot.animate.move_to(
                            axes.c2p(x, new_terms(x).degrees.max().item())
                        ),
                        # dot.animate.set_color(PURPLE_A),
                        dot.animate.set_glow_factor(1.0),
                    )
                # self.revise_fuzzy_sets(axes, new_terms, X)
                target_scene.play(dot.animate.set_color(str(ItemColor.INACTIVE_1)))
                target_scene.wait()
                old_terms = new_terms
            target_scene.wait(1)


if __name__ == "__main__":
    c = CLIPDemo()
    c.render()
    # c.construct()
