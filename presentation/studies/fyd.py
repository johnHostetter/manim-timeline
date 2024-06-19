from typing import Set, Tuple

import igraph as ig
from manim import *
from manim_slides import Slide

from mbeamer.blocks import AlertBlock, ExampleBlock
from animations.demos.graph_example import MyGraph, GraphPair
from mbeamer.slides import (
    SlideShow,
    SlideWithList,
    SlideWithBlocks,
    SlideWithTable,
)
from mbeamer.bibtex import BibTexManager
from mbeamer.lists import (
    ItemizedList,
    BulletedList as BL,
    DisadvantagesList,
    AdvantagesList,
)
from presentation.studies.pyrenees import (
    IntelligentTutoringSystemResults,
)

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class FYD(SlideShow):
    def __init__(self, **kwargs):
        super().__init__(
            slides=[
                FYDDiagram(),
                get_fyd_formula(),
                FYDResults(),
                get_fyd_rules(),
                fyd_summary(),
            ],
            **kwargs,
        )


def get_scalar_cardinality() -> MathTex:
    return MathTex(
        r"""
        S = \begin{bmatrix} 
        \sum_{\mathbf{x}} \mu_{1, 1}(x_{1}) & \sum_{\mathbf{x}} \mu_{1, 2}(x_{1}) & \dots \\
        \vdots & \ddots & \\
        \sum_{\mathbf{x}} \mu_{n, 1}(x_{n}) &        
        & \sum_{\mathbf{x}} \mu_{n, \max_{v} \mid \mathcal{T}_{v} \mid }(x_{n}) 
        \end{bmatrix}
        \qquad
        """,
        color=BLACK,
    )


def get_fyd_formula() -> SlideWithBlocks:
    """
    Create a slide discussing how to avoid invalid selections according to
    the epsilon-completeness property.

    Returns:
        The slide with the formula, remark, solution and word of caution.
    """
    # remark_block = RemarkBlock(
    #     title="Remarks",
    #     content=ItemizedList(
    #         items=[
    #             "Recall the importance of frequency from FYD.",
    #             "Recall a cutoff threshold was found w/ FYD.",
    #         ]
    #     ),
    # )
    bibtex_manager = BibTexManager()
    myTemplate = TexTemplate()
    myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
    alert_block = AlertBlock(
        title="Issue",
        content=DisadvantagesList(
            items=[
                "Rule simplification with LERS is costly",
                "Assumes binary truth values",
            ]
        ),
    )

    example_block = ExampleBlock(
        title="Proposed Solution",
        content=AdvantagesList(
            items=[
                "Mimic the behavior of LERs but incorporate fuzziness",
                "Zadeh's f-granulation theory to build graphs",
                bibtex_manager.slide_short_cite("tfig"),
                "Use the graph's structure to simplify rules",
                ItemizedList(
                    items=[
                        VGroup(
                            Text("Calculate closeness centrality", color=BLACK),
                            MathTex(r"C", color=BLACK),
                            Text(" for each vertex", color=BLACK),
                        ),
                        VGroup(
                            Text("Matrix ", color=BLACK),
                            MathTex(r"C", color=BLACK),
                            Text(
                                " is how reachable other premises are from shared rules",
                                color=BLACK,
                            ),
                        ),
                        VGroup(
                            Text("Input variable ", color=BLACK),
                            Text("usage", color=BLACK, slant=ITALIC),
                            Text(" is its frequency across rules: ", color=BLACK),
                            MathTex(r"\deg(\mu_{v, t}) / |\mathcal{R}|", color=BLACK),
                        ),
                        VGroup(
                            Text(
                                "Premise term activation frequency is from ",
                                color=BLACK,
                            ),
                            Text("scalar cardinality", color=BLACK, slant=ITALIC),
                            MathTex(r"S", color=BLACK),
                        ),
                    ]
                ),
            ]
        ),
    )
    myTemplate = TexTemplate()
    myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
    fyd_formula = MathTex(
        r"""
        \textit{FYD}(\mu_{v, t}) = 
        \overbrace{\frac{S_{v, t}}{\max(S)}}^{\text{Frequent}} 
        \overbrace{\wedge}^{\text{Yet}} \overbrace{\big ( 1 - (C_{v, t} 
        \wedge 
        (\deg(\mu_{v, t}) / |\mathcal{R}|) \big ))}^{\text{Discernible}}
        """,
        color=BLACK,
    )
    return SlideWithBlocks(
        title="Frequent-Yet-Discernible Formula",
        subtitle=None,
        blocks=[
            alert_block,
            example_block,
            get_scalar_cardinality(),
            fyd_formula,
        ],
    )


class FYDResults(IntelligentTutoringSystemResults):
    def __init__(self):
        data: List[List[str]] = [
            ["FYD (N = 39)", ".677 (.202)", ".746 (.160)", ".079 (.278)", "1.26 (.41)"],
            [
                "ECLAIRE (N = 52)",
                ".675 (.183)",
                ".736 (.206)",
                ".080 (.320)",
                "1.89 (.51)",
            ],
            ["CEW (N = 38)", ".645 (.217)", ".733 (.189)", ".104 (.290)", "1.98 (.67)"],
            ["CQL (N = 44)", ".635 (.210)", ".708 (.175)", ".094 (.248)", "1.89 (.71)"],
        ]
        super().__init__(data, highlighted_columns=[4])


def fyd_summary() -> SlideWithList:
    """
    Create a slide summarizing my FYD study.

    Returns:
        The slide with a short summary.
    """
    bibtex_manager = BibTexManager()
    return SlideWithList(
        title="Exploiting Frequent-Yet-Discernible Patterns",
        subtitle="Improving the Viability of Human-Readable Fuzzy Rules in Reinforcement Learning",
        width_buffer=6.0,
        beamer_list=BL(
            items=[
                "Hostetter, John Wesley et al., "
                "Self-Organizing Epsilon-Complete Neuro-Fuzzy Q-Networks\n"
                "from Frequent Yet Discernible Patterns in Reward-Based Scenarios (Draft)",
                "Primary Intuition",
                ItemizedList(
                    items=[
                        "Construct & train a model using CEW & FCQL",
                        bibtex_manager.slide_short_cite("hostetter2023self"),
                        "Simplify the NFN's rules using FYD",
                    ]
                ),
                "Summary",
                ItemizedList(
                    items=[
                        "No loss in performance with human-readable NFN",
                        "Mean 9.734 (S.D. 3.993) premises per rule afterward (from 142)",
                    ]
                ),
                "Contributions",
                ItemizedList(
                    items=[
                        "Exploit's Zadeh's f-granulation theory to simplify rules",
                        "Quick mimic of rule simplification in LERS",
                        "Avoids violating ϵ-completeness",
                    ]
                ),
                "Limitations",
                ItemizedList(
                    items=[
                        "Evaluated only on our ITS and classic control tasks",
                        "Computer vision",
                    ]
                ),
            ]
        ),
    )


def get_fyd_rules() -> SlideWithTable:
    """
    Create a slide showing the rules from the FYD study.

    Returns:
        The slide with the study results.
    """
    data = [
        [
            "FYD",
            "IF the student only has a FEW hints\n"
            "∧ student’s performance on this KC is AVERAGE\n"
            "∧ they correctly answer De Morgan’s Law OFTEN",
        ],
        [
            "ECLAIRE",
            "IF [(s1 > 0) ∧ (s113 > 0.5) ∧ (s115 > 0.857)\n"
            "∧ (s6 > 0.931) ∧ (s86 ≤ 0.056) ∧ (s93 ≤ 0.262)]\n"
            "...\n"
            "∨ [(s1 > 0) ∧ (s113 > 0) ∧ (s6 ≤ 0.962)\n"
            "∧ (s6 > 0.956) ∧ (s76 > 0.925)]",
        ],
    ]
    table = Table(
        data,
        # row_labels=[Text("FYD"), Text("ECLAIRE")],
        col_labels=[
            Text("Condition", weight=BOLD),
            Text("Example Rule Premise", weight=BOLD),
        ],
    )

    return SlideWithTable(
        title="Example of Model Complexity",
        subtitle=None,
        table=table.scale(scale_factor=0.75),
        caption="KC is a knowledge component (e.g., Complement Theorem).",
        highlighted_columns=[],
    )


class FYDDiagram(Slide, MovingCameraScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graphs = {}

    def construct(self):
        self.draw(origin=ORIGIN, scale=1.0, target_scene=self, animate=True)

    def draw(self, origin=ORIGIN, scale=1.0, target_scene=None, animate=True) -> VGroup:
        if target_scene is None:
            target_scene = self
        # note to self I copied this code directly from MyGraph and only kept the relevant parts
        for model_type in ["flc"]:
            if model_type == "flc":
                displayed_model_name = "Neuro-Fuzzy Network"
                vs, edges = MyGraph.get_vertices_and_edges_for_flc()
                layer_types = ["input", "premise", "rule", "consequence", "output"]
            else:
                raise ValueError(f"Unknown model type: {model_type}")

            # create the igraph.Graph representation of the model
            graph: ig.Graph = MyGraph.create_igraph_digraph(edges, vs)

            digraph, grouped_vertices = MyGraph.create_manim_digraph(graph, layer_types)
            digraph.rotate(PI / 2)
            self.graphs[displayed_model_name] = GraphPair(igraph=graph, digraph=digraph)

        # code specific to LERS diagram
        premise_nodes = grouped_vertices[1]
        rule_nodes = grouped_vertices[2]
        # premises_to_remove: Set[int] = set(
        #     random.choices(premise_terms, k=int(len(premise_terms) / 2))
        # )

        # v_group = VGroup(*[value.digraph for value in self.graphs.values()])
        v_group: VGroup = VGroup()
        for key, value in self.graphs.items():
            new_item = VGroup(
                Text(key, font_size=18, color=BLACK)
                .scale(scale_factor=scale)
                .next_to(value.digraph, UP),
                value.digraph,
            )
            v_group.add(new_item)

        v_group.scale(scale_factor=scale).move_to(origin)
        if animate:
            target_scene.camera.frame.move_to(v_group.get_center()).set(
                width=v_group.width * 3.0
            )
            target_scene.play(Create(v_group))
            self.illustrate_fyd_idea(digraph, rule_nodes, target_scene)
            target_scene.wait(1)
        else:
            target_scene.add(v_group)

        return v_group

    def illustrate_fyd_idea(self, digraph, rule_nodes, target_scene):
        # an idx of 0 means we are checking for the nodes to appear in the edge's source
        # an idx of 1 means we are checking for the nodes to appear in the edge's target
        target_scene.wait(1)
        target_scene.next_slide(loop=True)
        for r in rule_nodes[:2]:
            vertices_colored: Set[Dot] = set()
            edges_colored: Set[Line] = set()
            edges_to_use_for_highlighted_rule: Set[Tuple[int]] = {
                edge for edge in digraph.edges if edge[1] == r
            }
            rule_vertex: Dot = digraph.vertices[r]
            indications = [digraph.vertices[r].animate.set_color(GREEN)]
            vertices_colored.add(rule_vertex)
            for edge_key in edges_to_use_for_highlighted_rule:
                edge = digraph.edges[edge_key]
                indications.append(edge.animate.set_color(GREEN))
                edges_colored.add(edge)
            target_scene.play(AnimationGroup(*indications), run_time=2)
            premise_nodes = {edge[0] for edge in edges_to_use_for_highlighted_rule}
            vertex_colors = [ORANGE, PURPLE, BLUE, PINK]
            for v, vertex_highlight_color in zip(premise_nodes, vertex_colors):
                premise_vertex: Dot = digraph.vertices[v]
                indications = [premise_vertex.animate.set_color(vertex_highlight_color)]
                vertices_colored.add(premise_vertex)
                edges_to_use_for_highlighted_vertex: Set[Tuple[int]] = {
                    edge for edge in digraph.edges if edge[0] == v
                } - edges_to_use_for_highlighted_rule  # remove the edges we already highlighted
                for edge in edges_to_use_for_highlighted_vertex:
                    edge = digraph.edges[edge]
                    indications.append(edge.animate.set_color(vertex_highlight_color))
                    edges_colored.add(edge)
                target_scene.play(AnimationGroup(*indications), run_time=2)
                self.wait(1)

            self.next_slide()
            undo_indications = [v.animate.set_color(BLACK) for v in vertices_colored]
            undo_indications += [e.animate.set_color(BLACK) for e in edges_colored]
            target_scene.play(AnimationGroup(*undo_indications), run_time=2)


if __name__ == "__main__":
    FYD().render()
