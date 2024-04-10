from manim import *

from animations.common import MANIM_BLUE

config.background_color = WHITE


class MovingFrameBox(Scene):
    def construct(self):
        cql_header = Text("Conservative Q-Learning", font_size=36, color=BLACK)
        self.play(Write(cql_header))
        self.wait(3)
        self.play(cql_header.animate.to_edge(UP))
        self.wait()
        myTemplate = TexTemplate()
        myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
        upper_text = MathTex(
            "\min_{Q} \\alpha",
            "\mathbb{E}_{\mathbf{s} \sim \mathcal{D}}",
            "\Bigg [ " "\log \sum_{a} \exp \\big(Q(\mathbf{s}, a)\\big)" "-",
            "\mathbb{E}_{a^{\dag} \sim \hat{\pi}_{\\beta}(a^{\dag} \mid \mathbf{s})} "
            "[Q(\mathbf{s}, a^{\dag})] "
            "\Bigg ]",
            color=BLACK,
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
            "\Bigg ]",
            color=BLACK,
        ).move_to((0.0, -1.0, 0.0))
        self.play(Write(upper_text, run_time=2))
        self.play(Write(lower_text, run_time=2))
        text1 = Text(
            "Augmentation by Conservative Q-Learning", font_size=24, color=BLACK
        )
        # attach text to above the framebox
        text1.next_to(upper_text, UP)
        text2 = Text("Standard Bellman Error", font_size=24, color=BLACK)
        # attach text to below the framebox
        text2.next_to(lower_text, DOWN)
        framebox1 = SurroundingRectangle(
            upper_text, buff=0.2, corner_radius=0.1, color=MANIM_BLUE
        )
        framebox2 = SurroundingRectangle(
            lower_text, buff=0.2, corner_radius=0.1, color=MANIM_BLUE
        )
        self.play(
            Create(framebox1),
            Write(text1, run_time=2),
        )
        self.wait(5)
        self.play(Unwrite(text1))
        self.play(ReplacementTransform(framebox1, framebox2), Write(text2, run_time=2))
        self.wait(5)

        self.play(AnimationGroup(FadeOut(framebox2), Unwrite(text2)))
        self.wait(5)
        move_formula = Group(upper_text, lower_text).animate.shift(UP * 0.5)
        self.play(move_formula)
        # MoveAlongPath(upper_text, Line(ORIGIN, UP * 2))
        # MoveAlongPath(lower_text, Line(ORIGIN, DOWN * 2))
        # self.play(Write(parameters))
        # eqns = MathTex(r"2x - 3 & = -7 \\ 2x & = -4 \\ x & = -2")
        eqns = [
            Text("where ", font_size=24, color=BLACK),
            MathTex(r"\alpha \geq 0", font_size=36, color=BLACK),
            Text(
                "is a trade-off factor determining the magnitude of the adjustment. ",
                font_size=24,
                color=BLACK,
            ),
            Text("A behavior policy ", font_size=24, color=BLACK),
            MathTex(r"\hat{\pi}_{\beta}", font_size=36, color=BLACK),
            Text("collected training data ", font_size=24, color=BLACK),
            MathTex(r"\mathcal{D},", font_size=36, color=BLACK),
            MathTex(r"\gamma \in [0, 1]", font_size=36, color=BLACK),
            Text("is the discount factor, ", font_size=24, color=BLACK),
            MathTex(r"\mathbf{s}'", font_size=36, color=BLACK),
            Text(
                "is the next state after state ",
                font_size=24,
                color=BLACK,
                t2s={"after": ITALIC},
            ),
            MathTex(r"\mathbf{s}", font_size=36, color=BLACK),
            Text("and ", font_size=24, color=BLACK),
            MathTex(r"\mathcal{R}", font_size=36, color=BLACK),
            Text("is the reward function.", font_size=24, color=BLACK),
        ]
        new_loc = text2.get_center() + DOWN
        new_loc[0] = text2.get_x(LEFT)
        eqns[0].to_corner(DL)
        eqns[0].shift(UP)
        eqns[1].next_to(eqns[0], RIGHT)
        eqns[2].next_to(eqns[1], RIGHT)
        eqns[3].next_to(eqns[2], RIGHT)

        eqns[3].to_corner(DL)
        eqns[3].shift(UP * 0.45)
        # eqns[4].next_to(eqns[0], DOWN)
        eqns[4].next_to(eqns[3], RIGHT)
        eqns[5].next_to(eqns[4], RIGHT)
        eqns[6].next_to(eqns[5], RIGHT)
        eqns[7].next_to(eqns[6], RIGHT)
        eqns[8].next_to(eqns[7], RIGHT)

        eqns[9].to_corner(DL)
        eqns[10].next_to(eqns[9], RIGHT)
        eqns[11].next_to(eqns[10], RIGHT)
        eqns[12].next_to(eqns[11], RIGHT)
        eqns[13].next_to(eqns[12], RIGHT)
        eqns[14].next_to(eqns[13], RIGHT)
        # eqns[9].next_to(eqns[8], RIGHT)

        # MathTex("\\alpha \\geq 0"
        # "\\text{where \;} \\alpha \\geq 0 \\text{ is a trade-off factor,} \\ "
        # + "\\text{the magnitude of the adjustment} \\ \\text{lessens. The behavior policy, } \\"
        # + "\\hat{\\pi}_{\\beta} \\ \\text{, collected the training data } \\mathcal{D}"
        # + "\\gamma \\in [0, 1] \\text{is the discount factor, } \\", "\\mathbf{s}'"
        # + "\\text{is the next state \\emph{after} state } \\mathbf{s}", "\\text{and }"
        # + "\\mathcal{R} \\text{is the reward function.}")
        # eqns.next_to(text2, DOWN)
        for eqn in eqns:
            self.play(Write(eqn))
        # self.play(FadeIn(Group(*eqns)))
        self.wait(60)


if __name__ == "__main__":
    c = MovingFrameBox()
    c.render()
    # c.construct()
