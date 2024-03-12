import math
import torch
from manim import *
import igraph as ig
from igraph import Layout

from soft.computing.blueprints.factory import SystematicDesignProcess
from soft.computing.knowledge import KnowledgeBase
from soft.computing.organize import SelfOrganize
from soft.datasets import SupervisedDataset
from soft.fuzzy.logic.controller import Specifications, Engine, Mapping, SpaceConfiguration
from soft.fuzzy.logic.controller.impl import ZeroOrderTSK
from soft.utilities.reproducibility import load_configuration


# https://stackoverflow.com/questions/76175939/manim-add-labels-near-vertices
def get_self_organize() -> SelfOrganize:
    config = load_configuration()
    with config.unfreeze():
        config.clustering.distance_threshold = 0.25
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
        max_y_pos: float = 5.0
        for vertex_type in ["variable", "premise", "rule", "consequence"]:
            vertices = graph.vs.select(type_eq=vertex_type)
            for i, v in enumerate(vertices):
                print(v)
                if v["type"] == "premise":
                    y_pos = (int(v["name"][1:]) / len(vertices)) * max_y_pos
                else:
                    y_pos = v["data"] / len(vertices) * max_y_pos
                my_layout[v.index] = [v["layer"], y_pos, 0]
                # lt[v] = [lt[v][0], lt[v][1], i]
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
            layout=my_layout,
            vertex_config={
                # "fill_color": BLUE,
                # "stroke_color": WHITE,
                # "stroke_width": 2,
                "radius": 0.025,
            },
            edge_config={
                "stroke_width": 2,
                "tip_config": {"tip_length": 0.05, "tip_width": 0.05}
            }
        )
        g.shift(DOWN, LEFT)
        g.scale(2)
        g.rotate(PI / 2)

        self.add(g)

        # Save the state of camera
        self.camera.frame.save_state()

        self.play(
            Create(g),
            # self.camera.frame.animate.set_width(g.get_width() * 0.7),
            self.camera.frame.animate.move_to(g.get_center()),
            run_time=5
        )
        self.wait()

        # get a new layout for this graph
        new_layout: Layout = graph.layout_sugiyama()
        move_vertices = [
            g[v].animate.move_to(pos + [0.0])
            for v, pos in zip(g.vertices, new_layout.coords)
        ]
        self.play(*move_vertices, run_time=1)

        # move the camera to the new graph location
        self.camera.frame.save_state()
        animation_to_move_camera = self.camera.frame.animate.scale(1.5).move_to(
            g.get_center()
        )  # 1.5 zoom out
        move_vertices += [animation_to_move_camera]
        self.play(*move_vertices, run_time=5)
        self.wait()

        # tex_labels = []
        # for v in g.vertices:
        #     # label = MathTex(label_dict[v]).scale(0.5).next_to(g.vertices[v], UR)
        #     label = Text(label_dict[v]).scale(0.25).next_to(g.vertices[v], UR)
        #     tex_labels.append(label)
        # self.play(Create(VGroup(*tex_labels)))
        # self.wait()

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
                    type="tsk", defuzzification="product",
                    confidences=False, ignore_missing=False
                ),
                mapping=Mapping(
                    input=SpaceConfiguration(dim=4, max_terms=3, expandable=True),
                    output=SpaceConfiguration(dim=1, max_terms=3, expandable=True),
                ),
                number_of_rules=32
            ),
            knowledge_base=knowledge_base
        )
        print("Number of fuzzy logic rules: ", len(flc.knowledge_base.get_fuzzy_logic_rules()))
        print(flc)

        # each column is a in the form of (variable index, term index, rule index)
        rule_premise_indices: torch.Tensor = flc.engine.input_links.to_sparse().indices().transpose(
            0, 1
        )
        sorted_rule_premise_indices: torch.Tensor = rule_premise_indices[
            rule_premise_indices[:, -1].argsort()]
        from itertools import groupby
        grouped_premise_indices: Dict[int, torch.Tensor] = {
            rule_idx.item(): torch.vstack(list(group))[:, :-1]
            for rule_idx, group in groupby(sorted_rule_premise_indices, lambda x: x[-1])
        }
        max_terms: int = flc.granulation_layers["input"].centers.shape[-1]

        vs = {}
        edges = set()
        for rule_idx, premise_indices in grouped_premise_indices.items():
            print(f"Rule {rule_idx + 1}:")
            for var_idx, term_idx in premise_indices:
                print(f"Variable {var_idx + 1} with term {term_idx + 1}")
                vertex_id: torch.Tensor = var_idx * max_terms + term_idx  # 1d tensor
                var_id = "V" + str(var_idx.item())
                source_id = "P" + str(vertex_id.item())
                target_id = "R" + str(rule_idx)
                consequence_id = "C" + str(rule_idx)
                vs[var_id] = var_idx.item()
                vs[source_id] = (var_idx.item(), term_idx.item())
                vs[target_id] = rule_idx
                vs[consequence_id] = rule_idx
                edges.add((var_id, source_id))  # connect the variable to the premise term
                edges.add((source_id, target_id))  # connect the term to the rule
                edges.add((target_id, consequence_id))  # connect the rule to the consequence
            print()

        graph = ig.Graph()
        for vertex_id, vertex_data in vs.items():
            vertex_type = "variable"
            layer_order = -1
            if vertex_id[0] == "V":
                vertex_type = "variable"
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
            graph.add_vertex(str(vertex_id), type=vertex_type, data=vertex_data, layer=layer_order)
        for edge in edges:
            graph.add_edge(*edge)
        self.plot_graph(graph)


if __name__ == "__main__":
    c = MyGraph()
    c.render()
