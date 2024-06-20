import random
from typing import Set, Tuple

import igraph as ig
from manim import *
from manim_slides import Slide

from mtimeline.graph import GraphPair
from mbeamer.bibtex import BibTexManager
from mbeamer.lists import ItemizedList, BulletedList as BL
from mbeamer.slides import (
    SlideShow,
    SlideWithList,
    SlideWithTable,
    SlideWithTables,
)
from presentation.graph.demo import MyGraph
from presentation.studies.pyrenees import (
    IntelligentTutoringSystemResults,
)

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


class LERS(SlideShow):
    def __init__(self, **kwargs):
        super().__init__(
            slides=[
                LERSDiagram(),
                get_example_of_lers(),
                LERSResults(),
                get_original_rules(),
                get_natural_language_rules(),
                lers_summary(),
            ],
            **kwargs,
        )


def gather_items_to_remove(
    grouped_vertices,
    digraph: DiGraph,
    all_vertices_to_remove: Set[int],
    all_edges_to_remove: Set[Tuple[int]],
):
    edges_to_remove: Set[Tuple[int]] = set()
    vertices_to_remove: Set[int] = set()
    for premise in all_vertices_to_remove:
        inner_edge_keys_to_remove: Set[Tuple[int]] = {
            e for e in digraph.edges.keys() if e[0] == premise or e[1] == premise
        }
        inner_vertices_indices_to_remove: Set[int] = {
            vertex_index for edge in inner_edge_keys_to_remove for vertex_index in edge
        } - set(
            grouped_vertices[0]
        )  # remove any input vertices from being faded out
        inner_vertices_indices_to_remove -= set(
            grouped_vertices[2]
        )  # do not remove rule vertices

        edges_to_remove.update(inner_edge_keys_to_remove)
        vertices_to_remove.update(inner_vertices_indices_to_remove)

    # if (
    #         len(edges_to_remove.intersection(all_edges_to_remove)) != len(edges_to_remove)
    # ) or (
    #         vertices_to_remove.intersection(all_vertices_to_remove) != len(vertices_to_remove)
    # ):
    #     # we found new vertices or edges to remove
    #     return gather_items_to_remove(
    #         grouped_vertices, digraph=digraph,
    #         all_vertices_to_remove=all_vertices_to_remove.union(vertices_to_remove),
    #         all_edges_to_remove=all_edges_to_remove.union(edges_to_remove)
    #     )

    return (
        all_vertices_to_remove.union(vertices_to_remove),
        all_edges_to_remove.union(edges_to_remove),
    )


class LERSDiagram(Slide, MovingCameraScene):
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
        premise_terms = grouped_vertices[1]
        premises_to_remove: Set[int] = set(
            random.choices(premise_terms, k=int(len(premise_terms) / 2))
        )

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
            target_scene.wait(3)
            vs, es = gather_items_to_remove(
                grouped_vertices,
                digraph=value.digraph,
                all_vertices_to_remove=premises_to_remove,
                all_edges_to_remove=set(),
            )
            objects_to_fade_out = VGroup(*[digraph.vertices[i] for i in vs])
            indications = [
                Flash(digraph.vertices[i], color=RED, line_stroke_width=3) for i in vs
            ]
            objects_to_fade_out.add(*[digraph.edges[e] for e in es])

            target_scene.wait(1)
            target_scene.next_slide(loop=True)
            # color the vertices red
            for v in vs:
                indications.append(digraph.vertices[v].animate.set_color(RED))

            # color the edges red
            for e in es:
                indications.append(digraph.edges[e].animate.set_color(RED))

            target_scene.play(AnimationGroup(*indications), run_time=2)
            target_scene.wait(1)
            target_scene.next_slide(loop=True)
            target_scene.play(FadeOut(objects_to_fade_out, run_time=3))
        else:
            target_scene.add(v_group)

        return v_group


def get_example_of_lers():
    return SlideWithTables(
        title="Rule Simplification with Rough Set Theory",
        subtitle="Example of LERS",
        tables=[
            Table(
                [
                    ["1", "1", "0", "0", "1", "1"],
                    ["2", "1", "0", "0", "0", "1"],
                    ["3", "0", "0", "0", "0", "0"],
                    ["4", "1", "1", "0", "1", "0"],
                    ["5", "1", "1", "0", "2", "2"],
                    ["6", "2", "1", "0", "2", "2"],
                    ["7", "2", "2", "2", "2", "2"],
                ],
                col_labels=[
                    Text("Rule"),
                    MathTex(r"\mu_1").scale(1.5),
                    MathTex(r"\mu_2").scale(1.5),
                    MathTex(r"\mu_3").scale(1.5),
                    MathTex(r"\mu_4").scale(1.5),
                    Text("Decision"),
                ],
            ),
            Table(
                [
                    ["1, 2", "1", "0", "", "1"],
                    ["3", "0", "", "", "0"],
                    ["4", "", "1", "1", "0"],
                    ["5, 6, 7", "", "", "2", "2"],
                ],
                col_labels=[
                    Text("Rule"),
                    MathTex(r"\mu_1").scale(1.5),
                    MathTex(r"\mu_2").scale(1.5),
                    MathTex(r"\mu_4").scale(1.5),
                    Text("Decision"),
                ],
            ),
        ],
        captions=["Before", "After"],
        highlighted_columns=[],
    )


class LERSResults(IntelligentTutoringSystemResults):
    def __init__(self):
        data: List[List[str]] = [
            [
                "CEW w/ LERS (N = 52)",
                ".765 (.149)",
                ".791 (.160)",
                ".026 (.609)",
                "1.35 (.51)",
            ],
            ["CEW (N = 58)", ".749 (.164)", ".769 (.206)", ".073 (.597)", "1.31 (.57)"],
            [
                "Expert (N = 54)",
                ".754 (.184)",
                ".716 (.213)",
                "-.247 (.605)",
                "1.62 (.61)",
            ],
        ]
        super().__init__(data, highlighted_columns=[2, 3])


def format_rule_table(data: list[list[str]]) -> Table:
    """
    Format the data into a table.

    Args:
        data: The data to format.

    Returns:
        The table with the data.
    """
    table = Table(
        data,
        # row_labels=[Text("FYD"), Text("ECLAIRE")],
        col_labels=[
            Text("Rule", weight=BOLD),
            Text("IF", weight=BOLD),
            Text("THEN", weight=BOLD),
        ],
    )

    return table


def make_rule_slide(
    title: str, data: list[list[str]], caption: str, width_buffer: float = 3.0
) -> SlideWithTable:
    """
    Create a slide showing the rules from the LERS study.

    Args:
        title: The title of the slide.
        data: The data to format.
        caption: The caption for the slide.
        width_buffer: The buffer to add to the width of the table.

    Returns:
        The slide with the study results.
    """
    table = format_rule_table(data)

    return SlideWithTable(
        title=title,
        subtitle=None,
        table=table.scale(scale_factor=0.75),
        caption=caption,
        highlighted_columns=[],
        width_buffer=width_buffer,
    )


def get_original_rules() -> SlideWithTable:
    """
    Create a slide showing the original rules from the LERS study.

    Returns:
        The slide with the study results.
    """
    data = [
        [
            "1",
            """
            nPrincipleInProblem is high ∧ nTutorConceptsSession is low
            ∧ nStepSinceLastWrongKCSession is high
            ∧ pctCorrectAdd3Apply is high
            """,
            "Example",
        ],
        [
            "2",
            """
            timeOnTutoringSessionPS is high ∧ nCorrectKC is typical
            ∧ pctCorrectAdd2Apply is high ∧ pctCorrectAdd3All is average
            """,
            "Solve Alone",
        ],
        [
            "3",
            """
            nKCsSessionPS is high ∧ pctCorrectDeMorSelect is most
            ∧ pctCorrectDeMorApply is about half
            """,
            "Work Together",
        ],
    ]

    return make_rule_slide(
        title="Example of Model Complexity",
        data=data,
        caption="KC is a knowledge component (e.g., Complement Theorem).",
        width_buffer=3.0,
    )


def get_natural_language_rules() -> SlideWithTable:
    """
    Create a slide showing the rules from the LERS study after converting to natural language.

    Returns:
        The slide with the study results.
    """
    data = [
        [
            "1",
            """
            There is a high number of principles, a low number of
            tutor concepts per session, a high number of steps
            since the last wrong KC in the session, and a high
            percentage of correct applications for Addition
            Theorem of 3 Events.
            """,
            "Example",
        ],
        [
            "2",
            """
            The student spent a high amount of time on the
            tutoring session, had a typical number of correctly
            learned knowledge concepts, showed a high success
            rate in correctly applying the Addition Theorem
            for 2 events, and an average success rate in correctly
            applying the Addition Theorem for 3 events.
            """,
            "Solve Alone",
        ],
        [
            "3",
            """
            The number of knowledge components per problem
            solving session is high, and the proportion of
            correctly answered DeMorgan’s theorem select
            questions is most, while the proportion of correctly
            answered DeMorgan’s theorem apply questions is
            about half.
            """,
            "Work Together",
        ],
    ]

    return make_rule_slide(
        title="Computing With Words",
        data=data,
        caption="KC is a knowledge component (e.g., Complement Theorem).",
        width_buffer=6.0,
    )


def lers_summary() -> SlideWithList:
    """
    Create a slide summarizing my M-FCQL study.

    Returns:
        The slide with a short summary.
    """
    bibtex_manager = BibTexManager()
    return SlideWithList(
        title="A Minimal Discriminant Description of Fuzzy Rules",
        subtitle="Testing the Viability of Human-Readable Fuzzy Rules in Reinforcement Learning",
        width_buffer=6.0,
        beamer_list=BL(
            items=[
                "Hostetter, John Wesley et al., Self-Organizing Computing with Words:\n"
                "Automatic Discovery of Natural Language Control\nwithin an Intelligent Tutoring System (In Review)",
                "Primary Intuition",
                ItemizedList(
                    items=[
                        "Construct & train a model using CEW & FCQL",
                        bibtex_manager.slide_short_cite("hostetter2023self"),
                        "Simplify the NFN's rules using LERS from rough set theory",
                        bibtex_manager.slide_short_cite("new_lers"),
                    ]
                ),
                "Summary",
                ItemizedList(
                    items=[
                        "No loss in performance with human-readable NFN",
                        "Reduced 2,883 to only 757 rules",
                        "21 features globally eliminated (from 142)",
                        "Mean 6.896 (S.D. 2.101) premises per rule afterward (from 142)",
                    ]
                ),
                "Contributions",
                ItemizedList(
                    items=[
                        "First published use of rough theory with fuzzy RL",
                        "Works well in high-dimensional spaces",
                    ]
                ),
                "Limitations",
                ItemizedList(
                    items=[
                        "Computationally expensive",
                        "Evaluated only on our ITS",
                        "Computer vision",
                    ]
                ),
            ]
        ),
    )


if __name__ == "__main__":
    LERS().render()
