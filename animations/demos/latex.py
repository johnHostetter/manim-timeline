from manim import *
from manim.typing import Point3D


class MovingFrameBox(Scene):
    def construct(self):
        text = MathTex(
            "\\frac{d}{dx}f(x)g(x)=", "f(x)\\frac{d}{dx}g(x)", "+",
            "g(x)\\frac{d}{dx}f(x)"
        )
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
        upper_text = MathTex(
            "\min_{Q} \\alpha",
            "\mathbb{E}_{\mathbf{s} \sim \mathcal{D}}",
            "\Bigg [ "
            "\log \sum_{a} \exp \\big(Q(\mathbf{s}, a)\\big)"
            "-",
            "\mathbb{E}_{a^{\dag} \sim \hat{\pi}_{\\beta}(a^{\dag} \mid \mathbf{s})} "
            "[Q(\mathbf{s}, a^{\dag})] "
            "\Bigg ]",
            # "+ \\frac{1}{2} \mathbb{E}_{\mathbf{s}, a^{\dag}, \mathbf{s}' \sim \mathcal{D}} "
            # "\Bigg [ \Big(Q(\mathbf{s}, a^{\dag}) - \\big( \mathscr{R}(\mathbf{s}, a^{\dag}) + "
            # "\gamma [\max_{a \in \mathscr{A}} Q(\mathbf{s}', a)] \\big ) \Big)^{2} \Bigg ]"
        ).move_to((0.0, 1.0, 0.0))
        lower_text = MathTex(
            "+ \\frac{1}{2} "
            "\mathbb{E}_{\mathbf{s}, a^{\dag}, \mathbf{s}' \sim \mathcal{D}}",
            "\Bigg [ "
            "\Big("
            "Q(\mathbf{s}, a^{\dag}) - "
            "\\big( "
            "\mathcal{R}(\mathbf{s}, a^{\dag}) + "
            "\gamma [\max_{a \in \mathcal{A}} Q(\mathbf{s}', a)] "
            "\\big ) "
            "\Big)^{2} "
            "\Bigg ]"
        ).move_to((0.0, -1.0, 0.0))
        self.play(Write(upper_text))
        self.play(Write(lower_text))
        text1 = Text("Augmentation by Conservative Q-Learning", font_size=24)
        # attach text to above the framebox
        text1.next_to(upper_text, UP)
        text2 = Text("Standard Bellman Error", font_size=24)
        # attach text to below the framebox
        text2.next_to(lower_text, DOWN)
        framebox1 = SurroundingRectangle(upper_text, buff=.2, corner_radius=0.1)
        framebox2 = SurroundingRectangle(lower_text, buff=.2, corner_radius=0.1)
        self.play(
            Create(framebox1), Write(text1),
        )
        self.wait()
        self.play(
            ReplacementTransform(framebox1, framebox2), Write(text2), FadeOut(text1)
        )
        self.wait()

        parameters = Text(
            text="\\justifying {where $\\alpha \\geq 0$ is a trade-off factor, "
            + "the magnitude of the adjustment lessens. The behavior policy, $\hat{\pi}_{\\beta}$, "
            + "collected the training data $\mathcal{D}$, "
            + "$\gamma \in [0, 1]$ is the discount factor, "
            + "$\mathbf{s}'$ is the next state \emph{after} state $\mathbf{s}$ and $\mmathcal{R}$ is "
            + "the reward function.}",
            font_size=24
        )
        parameters.next_to(text2, DOWN)
        self.play(FadeOut(framebox2, text2))
        Group(upper_text, lower_text).shift(UP * 0.5)
        self.play(Write(parameters))


if __name__ == "__main__":
    c = MovingFrameBox()
    c.render()
    # c.construct()
