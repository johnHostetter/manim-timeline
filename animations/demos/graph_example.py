from itertools import groupby

import math
import torch
from manim import *
import igraph as ig
from igraph import Layout

from soft.computing.blueprints.factory import SystematicDesignProcess
from soft.computing.knowledge import KnowledgeBase
from soft.computing.organize import SelfOrganize
from soft.datasets import SupervisedDataset
from soft.fuzzy.logic.controller import (
    Specifications,
    Engine,
    Mapping,
    SpaceConfiguration,
)
from soft.fuzzy.logic.controller.impl import ZeroOrderTSK
from soft.utilities.reproducibility import load_configuration

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


# https://stackoverflow.com/questions/76175939/manim-add-labels-near-vertices
def get_self_organize() -> SelfOrganize:
    config = load_configuration()
    with config.unfreeze():
        config.clustering.distance_threshold = 0.2
    return SystematicDesignProcess(
        algorithms=["clip", "ecm", "wang_mendel"], config=config
    ).build(
        training_data=SupervisedDataset(
            inputs=torch.rand((250, 4)), targets=torch.rand((250, 1))
        )
    )


class MyGraph(MovingCameraScene):
    def plot_graph(self, graph: ig.Graph):
        # get a layout for this graph
        # layout: Layout = graph.layout_auto()
        # lt = {v: [layout[v][0], layout[v][1], 0] for v in range(len(layout))}
        my_layout = {}
        max_consequence_term_y_pos: float = 0.0
        grouped_vertices = {}
        label_dict = {}
        layer_types = ["input", "premise", "rule", "consequence", "output"]
        for vertex_type in layer_types:
            vertices: ig.VertexSeq = graph.vs.select(type_eq=vertex_type)
            vertex_indices: List[int] = [int(v["name"][1:]) for v in vertices]
            num_of_min_vertices: int = min(vertex_indices)
            num_of_max_vertices: int = max(vertex_indices) + 1

            grouped_vertices[vertex_type] = []
            for v in vertices:
                print(v)
                y_pos: float = (
                   int(v["name"][1:]) - num_of_min_vertices
                ) / (num_of_max_vertices - num_of_min_vertices)
                y_pos *= 3.0
                if v["type"] == "consequence":
                    # get the maximum y position of the consequence vertices
                    # so the output node can be centered with respect to them
                    max_consequence_term_y_pos = max(max_consequence_term_y_pos, y_pos)
                if v["type"] == "output":
                    # place the output vertex in the center of the graph
                    idx: int = v["data"]
                    if len(vertices) == 1:
                        idx = 1
                    y_pos: float = (idx / len(vertices)) * (max_consequence_term_y_pos / 2)
                my_layout[v.index] = [v["layer"], y_pos, 0]
                label_dict[v.index] = v["name"]
                grouped_vertices[vertex_type].append(v.index)
        # try:
        #     labels = [
        #         func if isinstance(func, str) else func.__name__.replace("_", " ")
        #         for func in graph.vs["function"]
        #     ]
        # except KeyError:
        #     labels = [str(v) for v in graph.vs.indices]
        # label_dict = {
        #     v: label for v, label in zip(graph.vs.indices, labels)
        # }
        g = DiGraph(
            graph.vs.indices,
            graph.get_edgelist(),
            label_fill_color=BLACK,
            layout=my_layout,
            vertex_config={
                "fill_color": BLACK,
                "stroke_color": BLACK,
                "stroke_width": 2,
                "radius": 0.025,
            },
            edge_config={
                "stroke_color": "BLACK",
                "stroke_width": 1,
                "tip_config": {"tip_length": 0.035, "tip_width": 0.035},
            },

        )
        g.shift(DOWN, LEFT)
        g.scale(1.35)
        g.rotate(PI / 2)

        self.add(g)

        # Save the state of camera
        self.camera.frame.save_state()

        self.play(
            Create(g),
            # self.camera.frame.animate.set_width(g.get_width() * 0.7),
            self.camera.frame.animate.move_to(g.get_center()),
            run_time=5,
        )
        self.wait()

        self.play(g.animate.shift(RIGHT * 2))

        layer_colors = [BLUE, GREEN, RED, YELLOW, PURPLE]
        animations = [
            # self.camera.frame.animate.set(width=g.get_width() * 3.0),
        ]
        for layer_type, layer_color in zip(layer_types, layer_colors):
            layer_vertices = [g.vertices[v] for v in grouped_vertices[layer_type]]
            surrounding_rectangle = SurroundingRectangle(
                VGroup(*layer_vertices),
                color=layer_color,
                buff=0.25,
                corner_radius=0.25,
            )
            layer_label = Text(
                layer_type.capitalize() + " Layer", color=BLACK, font_size=24
            ).next_to(
                surrounding_rectangle, LEFT
            )
            animation = AnimationGroup(
                *[
                    Create(surrounding_rectangle, run_time=2),
                    Write(layer_label, run_time=1),
                    AnimationGroup(
                        *[v.animate.set_color(layer_color) for v in layer_vertices],
                        run_time=0.5
                    )
                ],
            )
            animations.append(animation)

        for animation in animations:
            self.play(animation)
            self.wait()

        # # get a new layout for this graph
        # new_layout: Layout = graph.layout_sugiyama()
        # move_vertices = [
        #     g[v].animate.move_to(pos + [0.0])
        #     for v, pos in zip(g.vertices, new_layout.coords)
        # ]
        # self.play(*move_vertices, run_time=1)
        #
        # # move the camera to the new graph location
        # self.camera.frame.save_state()
        # animation_to_move_camera = self.camera.frame.animate.scale(1.5).move_to(
        #     g.get_center()
        # )  # 1.5 zoom out
        # move_vertices += [animation_to_move_camera]
        # self.play(*move_vertices, run_time=5)
        # self.wait()

        # # label the graph's vertices
        # tex_labels = []
        # for v in g.vertices:
        #     # label = MathTex(label_dict[v]).scale(0.5).next_to(g.vertices[v], UR)
        #     label = Text(label_dict[v], color=BLACK).scale(0.25).next_to(g.vertices[v], UR)
        #     tex_labels.append(label)
        # self.play(Create(VGroup(*tex_labels)))
        # self.wait()
        # print(g.edges)

    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6]
        labels = "ABCDEF"
        label_dict = {i: label for i, label in zip(vertices, labels)}
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 5), (5, 2), (2, 6), (6, 3)]
        lt = {
            1: [0, 0, 0],
            2: [2, 0, 0],
            3: [2, 2, 0],
            4: [0, 2, 0],
            5: [1, math.sqrt(3), 0],
            6: [2 + math.sqrt(3), 1, 0],
        }
        # g = Graph(vertices, edges, layout=lt)
        self_organize: SelfOrganize = get_self_organize()
        # self.plot_graph(self_organize.graph)
        # use the SelfOrganize plan and plot the resulting fuzzy logic controller
        knowledge_base: KnowledgeBase = self_organize.start()
        flc = ZeroOrderTSK(
            specifications=Specifications(
                t_norm="algebraic_product",
                engine=Engine(
                    type="tsk",
                    defuzzification="product",
                    confidences=False,
                    ignore_missing=False,
                ),
                mapping=Mapping(
                    input=SpaceConfiguration(dim=4, max_terms=3, expandable=True),
                    output=SpaceConfiguration(dim=1, max_terms=3, expandable=True),
                ),
                number_of_rules=32,
            ),
            knowledge_base=knowledge_base,
        )
        print(
            "Number of fuzzy logic rules: ",
            len(flc.knowledge_base.get_fuzzy_logic_rules()),
        )
        print(flc)

        # each column is in the form of (input index, term index, rule index)
        rule_premise_indices: torch.Tensor = (
            flc.engine.input_links.to_sparse().indices().transpose(0, 1)
        )
        sorted_rule_premise_indices: torch.Tensor = rule_premise_indices[
            rule_premise_indices[:, -1].argsort()
        ]

        grouped_premise_indices: Dict[int, torch.Tensor] = {
            rule_idx.item(): torch.vstack(list(group))[:, :-1]
            for rule_idx, group in groupby(sorted_rule_premise_indices, lambda x: x[-1])
        }
        max_terms: int = flc.granulation_layers["input"].centers.shape[-1]

        vs = {}
        edges = set()
        for rule_idx, premise_indices in grouped_premise_indices.items():
            print(f"Rule {rule_idx + 1}:")
            target_name: str = "R" + str(rule_idx)
            consequence_name: str = "C" + str(rule_idx)
            output_id = "O" + str(0)

            for var_idx, term_idx in premise_indices:
                print(f"Variable {var_idx + 1} with term {term_idx + 1}")
                vertex_id: torch.Tensor = var_idx * max_terms + term_idx  # 1d tensor
                var_name: str = "V" + str(var_idx.item())
                source_name: str = "P" + str(vertex_id.item())
                vs[var_name] = var_idx.item()
                vs[source_name] = (var_idx.item(), term_idx.item())
                vs[target_name] = rule_idx
                vs[consequence_name] = rule_idx
                vs[output_id] = 0
                edges.add(
                    (var_name, source_name)
                )  # connect the input to the premise term
                edges.add((source_name, target_name))  # connect the term to the rule
            edges.add(
                (target_name, consequence_name)
            )  # connect the rule to the consequence
            edges.add((consequence_name, output_id))  # connect the consequence to the output node
            print()

        graph = ig.Graph(directed=True)
        for vertex_id, vertex_data in vs.items():
            vertex_type = "input"
            layer_order = -1
            if vertex_id[0] == "V":
                vertex_type = "input"
                layer_order = 0
            elif "P" in vertex_id:
                vertex_type = "premise"
                layer_order = 1
            elif "R" in vertex_id:
                vertex_type = "rule"
                layer_order = 2
            elif "C" in vertex_id:
                vertex_type = "consequence"
                layer_order = 3
            elif "O" in vertex_id:
                vertex_type = "output"
                layer_order = 4
            graph.add_vertex(
                str(vertex_id), type=vertex_type, data=vertex_data, layer=layer_order
            )
        for edge in edges:
            source_id: int = graph.vs.find(name=str(edge[0])).index
            target_id: int = graph.vs.find(name=str(edge[1])).index
            added_edge = graph.add_edge(source=source_id, target=target_id)
            assert source_id == added_edge.source, \
                f"Incorrect edge source: {source_id, added_edge.source}"
            assert target_id == added_edge.target, \
                f"Incorrect edge target: {target_id, added_edge.target}"
        self.plot_graph(graph)


if __name__ == "__main__":
    c = MyGraph()
    c.render()
