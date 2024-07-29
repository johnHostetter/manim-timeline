from manim import *
from manim_slides import Slide

from manim_beamer import MANIM_BLUE

config.background_color = WHITE


class CQLDemo(Slide):
    def construct(self):
        self.draw(origin=ORIGIN, scale=1.0)

    def draw(self, origin, scale, target_scene=None, animate: bool = True):
        if target_scene is None:
            target_scene = self
        cql_header = (
            Text("Conservative Q-Learning", color=BLACK)
            .move_to(origin)
            .scale(scale_factor=scale)
        )
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
        ).move_to(
            origin
        )  # .move_to((0.0, 1.0, 0.0))
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
        ).next_to(
            upper_text, DOWN
        )  # .move_to((0.0, -1.0, 0.0))

        cql_formula = (
            VGroup(upper_text, lower_text).move_to(origin).scale(scale_factor=scale)
        )

        if not animate:
            cql_header.next_to(cql_formula, 5 * UP * scale)
            target_scene.add(cql_header, cql_formula)
        else:
            target_scene.play(Write(cql_header))
            target_scene.wait(3)
            target_scene.next_slide()
            target_scene.play(cql_header.animate.next_to(cql_formula, 5 * UP * scale))
            target_scene.play(Write(cql_formula, run_time=2))

            cql_lbl = Text(
                "Augmentation by Conservative Q-Learning",
                font_size=24,
                color=BLACK,
                slant=ITALIC,
            ).scale(scale_factor=scale)

            # attach text to above the framebox
            # cql_lbl.next_to(upper_text, UP)
            std_bellman_error_lbl = Text(
                "Standard Bellman Error", font_size=24, color=BLACK, slant=ITALIC
            ).scale(scale_factor=scale)
            # attach text to below the framebox
            # std_bellman_error_lbl.next_to(lower_text, DOWN)
            cql_frame = SurroundingRectangle(
                upper_text,
                buff=0.2 * scale,
                corner_radius=0.1,
                color=MANIM_BLUE,
                stroke_width=5 * scale,
            )
            bellman_frame = SurroundingRectangle(
                lower_text,
                buff=0.2 * scale,
                corner_radius=0.1,
                color=MANIM_BLUE,
                stroke_width=5 * scale,
            )

            # format the labels for the frame boxes
            cql_lbl.next_to(cql_frame, UP * scale)
            std_bellman_error_lbl.next_to(bellman_frame, DOWN * scale)

            target_scene.wait(1)
            target_scene.next_slide()
            target_scene.play(
                AnimationGroup(Create(cql_frame), FadeIn(cql_lbl), run_time=2)
            )
            target_scene.wait(5)
            target_scene.next_slide()
            target_scene.play(
                AnimationGroup(
                    FadeOut(cql_lbl),
                    ReplacementTransform(cql_frame, bellman_frame),
                    FadeIn(std_bellman_error_lbl),
                    run_time=2,
                )
            )
            target_scene.wait(5)
            target_scene.next_slide()

            target_scene.play(
                AnimationGroup(
                    Uncreate(bellman_frame), FadeOut(std_bellman_error_lbl), run_time=2
                ),
            )
            target_scene.wait(5)
            target_scene.next_slide()
            move_formula = Group(upper_text, lower_text).animate.shift(UP * 0.5 * scale)
            target_scene.play(move_formula)

            ###############################################
            # write the paragraph discussing the parameters
            ###############################################

            # param_fragments = MathTex(r"2x - 3 & = -7 \\ 2x & = -4 \\ x & = -2")
            param_fragments = [
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

            #########################################
            # format the paragraph for the parameters
            #########################################

            parameter_paragraph = VGroup()
            param_fragments[0].next_to(std_bellman_error_lbl, DOWN)
            param_fragments[1].next_to(param_fragments[0], RIGHT)
            param_fragments[2].next_to(param_fragments[1], RIGHT)
            parameter_sentence_1 = VGroup(*param_fragments[:3])
            parameter_paragraph.add(parameter_sentence_1)

            param_fragments[3].next_to(param_fragments[0], DOWN)
            param_fragments[4].next_to(param_fragments[3], RIGHT)
            param_fragments[5].next_to(param_fragments[4], RIGHT)
            param_fragments[6].next_to(param_fragments[5], RIGHT)
            param_fragments[7].next_to(param_fragments[6], RIGHT)
            param_fragments[8].next_to(param_fragments[7], RIGHT)

            parameter_sentence_2 = VGroup(*param_fragments[3:9])
            parameter_paragraph.add(parameter_sentence_2)

            param_fragments[9].next_to(param_fragments[3], DOWN)
            param_fragments[10].next_to(param_fragments[9], RIGHT)
            param_fragments[11].next_to(param_fragments[10], RIGHT)
            param_fragments[12].next_to(param_fragments[11], RIGHT)
            param_fragments[13].next_to(param_fragments[12], RIGHT)
            param_fragments[14].next_to(param_fragments[13], RIGHT)
            parameter_sentence_3 = VGroup(*param_fragments[9:15])
            parameter_paragraph.add(parameter_sentence_3)

            # left align the paragraph
            parameter_paragraph.arrange(
                DOWN * scale, aligned_edge=cql_formula.get_left(), buff=0.5
            ).scale(scale_factor=scale).move_to(origin).next_to(cql_formula, DOWN)

            target_scene.play(Write(parameter_paragraph, run_time=3))
            target_scene.wait(10)
            target_scene.next_slide()


if __name__ == "__main__":
    c = CQLDemo()
    c.render()
    # c.construct()
