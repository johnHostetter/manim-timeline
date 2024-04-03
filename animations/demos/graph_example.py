from functools import partial
from itertools import groupby
from dataclasses import dataclass
from typing import Tuple, Set, Dict as DictType, List as ListType, Union as UnionType

import math
import torch
from manim import *
import igraph as ig
from igraph import Layout

from animations.common import make_axes, add_labels_to_axes, AxisConfig
from soft.datasets import SupervisedDataset
from soft.computing.organize import SelfOrganize
from soft.computing.knowledge import KnowledgeBase
from soft.computing.blueprints.factory import SystematicDesignProcess
from soft.fuzzy.logic.controller import (
    Specifications,
    Engine,
    Mapping,
    SpaceConfiguration,
)
from soft.fuzzy.logic.controller.impl import ZeroOrderTSK
from soft.fuzzy.sets.continuous.abstract import ContinuousFuzzySet
from soft.fuzzy.sets.continuous.impl import Gaussian
from soft.utilities.reproducibility import load_configuration

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


# https://stackoverflow.com/questions/76175939/manim-add-labels-near-vertices
def get_self_organize() -> SelfOrganize:
    soft_config = load_configuration()
    with soft_config.unfreeze():
        soft_config.clustering.distance_threshold = 0.2
    return SystematicDesignProcess(
        algorithms=["clip", "ecm", "wang_mendel"], config=soft_config
    ).build(
        training_data=SupervisedDataset(
            inputs=torch.rand((250, 4)), targets=torch.rand((250, 1))
        )
    )


@dataclass
class GraphPair:
    igraph: ig.Graph  # the igraph.Graph representation of the graph
    digraph: DiGraph  # the manim representation of the igraph.Graph

    def __len__(self) -> int:
        return len(self.igraph.vs)

    def __getitem__(self, item: UnionType[str, int]) -> Tuple[ig.Vertex, Dot]:
        index = item  # assume the given item is a vertex index
        if isinstance(item, str):
            # the given item is a vertex name, get its index
            index = self.igraph.vs.select(name_eq=item).indices[0]
        return self.igraph.vs[index], self.digraph.vertices[index]


class MyGraph(MovingCameraScene):
    def plot_graph(
        self, graph: ig.Graph, layer_types: ListType[str], direction
    ) -> GraphPair:
        # get a layout for this graph
        # layout: Layout = graph.layout_auto()
        # lt = {v: [layout[v][0], layout[v][1], 0] for v in range(len(layout))}
        if (direction == RIGHT).all():
            opposite_direction = LEFT
        else:
            opposite_direction = RIGHT

        my_layout = {}
        max_consequence_term_y_pos: float = 0.0
        grouped_vertices = {}
        label_dict = {}
        for layer_order in range(len(layer_types)):
            # vertices: ig.VertexSeq = graph.vs.select(type_eq=vertex_type)
            vertices: ig.VertexSeq = graph.vs.select(layer_eq=layer_order)
            vertex_indices: ListType[int] = [int(v["name"][1:]) for v in vertices]
            num_of_min_vertices: int = min(vertex_indices)
            num_of_max_vertices: int = max(vertex_indices) + 1

            grouped_vertices[layer_order] = []
            for v in vertices:
                print(v)
                y_pos: float = (int(v["name"][1:]) - num_of_min_vertices) / (
                    num_of_max_vertices - num_of_min_vertices
                )
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
                    y_pos: float = (idx / len(vertices)) * (
                        max_consequence_term_y_pos / 2
                    )
                my_layout[v.index] = [v["layer"], y_pos, 0]
                label_dict[v.index] = v["name"]
                grouped_vertices[layer_order].append(v.index)
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
        digraph = DiGraph(
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
        digraph.shift(DOWN, opposite_direction)
        digraph.scale(1.35)
        digraph.rotate(PI / 2)

        self.add(digraph)

        # Save the state of camera
        self.camera.frame.save_state()

        self.play(
            Create(digraph),
            # self.camera.frame.animate.set_width(digraph.get_width() * 0.7),
            self.camera.frame.animate.move_to(digraph.get_center()),
            run_time=5,
        )
        self.wait()

        self.play(digraph.animate.shift(direction * 3))

        layer_colors = [BLUE, GREEN, RED, YELLOW, PURPLE]
        animations = [
            # self.camera.frame.animate.set(width=digraph.get_width() * 3.0),
        ]
        rewind_animations = []
        for layer_order, (layer_type, layer_color) in enumerate(
            zip(layer_types, layer_colors)
        ):
            layer_vertices = [
                digraph.vertices[v] for v in grouped_vertices[layer_order]
            ]
            surrounding_rectangle = SurroundingRectangle(
                VGroup(*layer_vertices),
                color=layer_color,
                buff=0.25,
                corner_radius=0.25,
            )
            layer_str: str = layer_type.capitalize() + " Layer"
            layer_str += f" {layer_order}" if layer_type == "hidden" else ""
            layer_label = Text(layer_str, color=BLACK, font_size=24).next_to(
                surrounding_rectangle, opposite_direction
            )
            animation = AnimationGroup(
                *[
                    Create(surrounding_rectangle, run_time=2),
                    Write(layer_label, run_time=1),
                    AnimationGroup(
                        *[v.animate.set_color(layer_color) for v in layer_vertices],
                        run_time=0.5,
                    ),
                ],
            )
            rewind_animation = AnimationGroup(
                *[
                    FadeOut(surrounding_rectangle, run_time=2),
                    Unwrite(layer_label, run_time=1),
                    AnimationGroup(
                        *[v.animate.set_color(BLACK) for v in layer_vertices],
                        run_time=0.5,
                    ),
                ],
            )
            animations.append(animation)
            rewind_animations.append(rewind_animation)

        for animation in animations:
            self.play(animation)
            self.wait()

        self.wait(5)

        for rewind_animation in rewind_animations:
            self.play(rewind_animation)
            self.wait()

        return GraphPair(graph, digraph=digraph)

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

    def get_vertices_and_edges_for_dnn(
        self,
    ) -> Tuple[DictType[str, int], Set[Tuple[str, str]]]:
        model_type = Text(
            "Dense Feed-Forward Artificial Neural Network", font_size=24, color=BLACK
        )
        self.play(Write(model_type, run_time=2))
        self.wait(3)
        self.play(Unwrite(model_type, run_time=2))

        input_size: int = 4
        hidden_size: int = 16
        output_size: int = 1
        NN_text = f"""
        import torch
        hidden_size: int = {hidden_size}
        model = torch.nn.Sequential(
            torch.nn.Linear({input_size}, {hidden_size}),
            torch.nn.ReLU(),
            torch.nn.Linear({hidden_size}, {hidden_size}),
            torch.nn.ReLU(),
            torch.nn.Linear({hidden_size}, {output_size})
        )
        """
        code_text = Code(
            code=NN_text,
            tab_width=4,
            background_stroke_width=1,
            background_stroke_color=WHITE,
            insert_line_no=False,
            style=Code.styles_list[15],
            background="window",
            language="python",
            font="consolas",
            font_size=18,
        )
        self.play(Write(code_text), run_time=5)
        self.wait(3)
        self.play(FadeOut(code_text))
        self.wait()
        # render a dense neural network
        vs = {}
        all_vertices = []
        layer_0_vertices = [f"V{i}" for i in range(0, input_size)]  # 4-inputs
        layer_1_vertices = [f"P{i}" for i in range(0, hidden_size)]
        layer_2_vertices = [f"R{i}" for i in range(0, hidden_size)]
        layer_3_vertices = [f"C{i}" for i in range(0, hidden_size)]
        layer_4_vertices = [f"O{i}" for i in range(0, output_size)]  # 1-output

        all_vertices.extend(layer_0_vertices)
        all_vertices.extend(layer_1_vertices)
        all_vertices.extend(layer_2_vertices)
        all_vertices.extend(layer_3_vertices)
        all_vertices.extend(layer_4_vertices)

        for vertex in all_vertices:
            vs[vertex] = int(vertex[1:])

        edges = []
        for i in range(4):
            for j in range(16):
                edges.append((f"V{i}", f"P{j}"))
        for i in range(16):
            for j in range(16):
                edges.append((f"P{i}", f"R{j}"))
        for i in range(16):
            for j in range(16):
                edges.append((f"R{i}", f"C{j}"))
        for i in range(16):
            edges.append((f"C{i}", "O0"))
        return vs, edges

    def get_vertices_and_edges_for_flc(
        self,
    ) -> Tuple[DictType[str, int], Set[Tuple[str, str]]]:
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
            edges.add(
                (consequence_name, output_id)
            )  # connect the consequence to the output node
            print()
        return vs, edges

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

        model_graphs = {}
        for model_type in ["dnn", "flc"]:
            if model_type == "dnn":
                vs, edges = self.get_vertices_and_edges_for_dnn()
                layer_types = ["input", "hidden", "hidden", "hidden", "output"]
            elif model_type == "flc":
                vs, edges = self.get_vertices_and_edges_for_flc()
                layer_types = ["input", "premise", "rule", "consequence", "output"]
            else:
                raise ValueError(f"Unknown model type: {model_type}")

            graph = ig.Graph(directed=True)
            for vertex_id, vertex_data in vs.items():
                vertex_type: str = "input"
                layer_order: int = -1
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
                    str(vertex_id),
                    type=vertex_type,
                    data=vertex_data,
                    layer=layer_order,
                )

            for edge in edges:
                source_id: int = graph.vs.find(name=str(edge[0])).index
                target_id: int = graph.vs.find(name=str(edge[1])).index
                added_edge: ig.Edge = graph.add_edge(source=source_id, target=target_id)
                assert (
                    source_id == added_edge.source
                ), f"Incorrect edge source: {source_id, added_edge.source}"
                assert (
                    target_id == added_edge.target
                ), f"Incorrect edge target: {target_id, added_edge.target}"

            graph_pair: GraphPair = self.plot_graph(
                graph, layer_types, LEFT if model_type == "dnn" else RIGHT
            )
            model_graphs[model_type] = graph_pair
            if model_type == "dnn":
                # move the DNN graph to the left and temporarily hide it
                self.play(
                    # digraph.animate.to_edge(LEFT),
                    FadeOut(graph_pair.digraph),
                )
            elif model_type == "flc":
                # bring the DNN graph back for side-by-side comparison
                all_models: Group = Group(
                    model_graphs["dnn"].digraph, model_graphs["flc"].digraph
                )
                self.play(
                    # digraph.animate.to_edge(RIGHT),
                    model_graphs["flc"].digraph.animate.next_to(
                        model_graphs["dnn"].digraph, RIGHT, buff=3.0
                    ),
                    Create(model_graphs["dnn"].digraph),
                )
                self.play(all_models.animate.move_to(ORIGIN))
                self.play(
                    self.camera.frame.animate.move_to(all_models.get_center()),
                )

        self.wait(5)
        self.play(
            self.camera.frame.animate.move_to(model_graphs["dnn"].digraph.get_center())
        )
        self.wait(5)

        # now show each graph's neuron activation
        self.sample_neuron_and_show(
            model_graphs["dnn"],
            next_graph=model_graphs["flc"],
            activation_funcs=[
                ("Unit Step", partial(torch.heaviside, values=torch.zeros(1))),
                ("Hard Sigmoid", torch.nn.Hardsigmoid()),
                ("Sigmoid", torch.nn.Sigmoid()),
                ("Hard Hyperbolic Tangent", torch.nn.Hardtanh()),
                ("Hyperbolic Tangent", torch.nn.Tanh()),
                ("ReLU", torch.nn.ReLU()),
            ],
            axis_configs=[
                (AxisConfig(-6.0, 6.0, step=2.0), AxisConfig(0.0, 1.1, step=0.1)),
                (AxisConfig(-6.0, 6.0, step=2.0), AxisConfig(0.0, 1.1, step=0.1)),
                (AxisConfig(-6.0, 6.0, step=2.0), AxisConfig(0.0, 1.1, step=0.1)),
                (AxisConfig(-6.0, 6.0, step=2.0), AxisConfig(-1.1, 1.1, step=0.1)),
                (AxisConfig(-6.0, 6.0, step=2.0), AxisConfig(-1.1, 1.1, step=0.1)),
                (AxisConfig(-6.0, 6.0, step=2.0), AxisConfig(0.0, 6.0, step=1.0)),
            ]
        )
        self.sample_neuron_and_show(
            model_graphs["flc"],
            next_graph=None,
            activation_funcs=[
                ("Gaussian", Gaussian(centers=0.0, widths=1.0))
            ],
            axis_configs=[
                (AxisConfig(-6.0, 6.0, step=2.0), AxisConfig(0.0, 1.1, step=0.1))
            ]
        )
        self.wait(5)

    def sample_neuron_and_show(
        self,
        focused_graph: GraphPair,
        next_graph: UnionType[None, GraphPair],
        activation_funcs: List[Tuple[str, torch.nn.Module]],
        axis_configs: List[Tuple[AxisConfig, AxisConfig]],
    ):
        _, example_neuron = focused_graph[
            "P0"
        ]  # sample the first neuron in the first hidden layer
        self.play(
            self.camera.frame.animate.move_to(example_neuron).set(width=0.075),
            run_time=3,
        )
        # min_x: float = -6.0
        # max_x: float = 6.0
        # place axes at this neuron
        # axes = make_axes(
        #     self,
        #     x_axis_config=AxisConfig(-6.0, 6.0, step=2.0),
        #     y_axis_config=AxisConfig(0.0, 1.1, step=0.1),
        #     stroke_width=0.02,
        #     axes_color=WHITE,
        # )
        # x_axis_lbl, y_axis_lbl = add_labels_to_axes(
        #     axes, x_label="Input", y_label="Degree of Activation", text_color=WHITE
        # )
        # activation_plot_group = (
        #     VGroup(axes, x_axis_lbl, y_axis_lbl).move_to(example_neuron).scale(0.005)
        # )
        # self.play(
        #     Create(activation_plot_group),
        # )
        prev_axes = None
        prev_activation_plot_func = None
        for idx, (axis_config_pair, activation_func_pair) in enumerate(
                zip(axis_configs, activation_funcs)
        ):
            # place axes at this neuron
            activation_func_name, activation_func = activation_func_pair
            x_axis_config, y_axis_config = axis_config_pair[0], axis_config_pair[1]
            axes = make_axes(
                self,
                x_axis_config=x_axis_config,
                y_axis_config=y_axis_config,
                stroke_width=0.02,
                axes_color=WHITE,
            )
            # x_axis_lbl, y_axis_lbl = add_labels_to_axes(
            #     axes, x_label="Input", y_label="Degree of Activation", text_color=WHITE
            # )

            axes.move_to(example_neuron).scale(0.005)
            # the result is the labels (VGroup of length 2 with two axis labels as Tex objects)
            axis_labels = axes.get_axis_labels(x_label="Input", y_label="Degree of Activation")
            # activation_plot_group = (
            #     VGroup(axes, x_axis_lbl, y_axis_lbl).move_to(example_neuron).scale(0.005)
            # )

            # create or update the plot axes
            if prev_axes is None:
                self.play(
                    Create(axes),
                    Create(axis_labels),
                )
            else:
                self.play(
                    TransformMatchingShapes(
                        mobject=prev_axes,
                        target_mobject=axes,
                        replace_mobject_with_target_in_scene=True,
                    ),
                )

            self.play(
                self.camera.frame.animate.set(
                    width=axes.width + 0.001, height=axes.height + 0.001
                ).move_to(axes),
                Write(Text(activation_func_name, color=ORANGE).next_to(axes, UP)),
            )

            use_smoothing = True
            if isinstance(activation_func, ContinuousFuzzySet):
                lambda_func: callable = lambda x: activation_func(torch.Tensor([x])).degrees.item()
            else:
                lambda_func: callable = lambda x: activation_func(torch.Tensor([x])).item()
                if idx == 0:
                    use_smoothing = False  # disable smoothing for heaviside step function
            step_val: float = (
                                      x_axis_config.max_value - x_axis_config.min_value
                              ) / 1000  # the default is 1.0

            activation_plot_func = axes.plot(
                lambda_func,
                x_range=(x_axis_config.min_value, x_axis_config.max_value, step_val),
                stroke_color=ORANGE,
                stroke_width=0.02,
                use_smoothing=use_smoothing,
                # color=ORANGE
            )

            func_label = axes.get_graph_label(
                activation_plot_func,
                Text(activation_func_name),
                color=ORANGE,
                direction=UP,
            )

            # plot or transform the activation function to the new function
            if prev_activation_plot_func is None:
                self.play(
                    AnimationGroup(
                        Create(activation_plot_func),
                        FadeIn(func_label),
                    )
                )
            else:
                self.play(
                    AnimationGroup(
                        TransformMatchingShapes(
                            mobject=prev_activation_plot_func,
                            target_mobject=activation_plot_func,
                            replace_mobject_with_target_in_scene=True,
                        ),
                        FadeIn(func_label),
                    )
                )
            prev_axes = axes
            self.wait(5)
            self.play(FadeOut(func_label))
            prev_activation_plot_func = activation_plot_func
        # get the bounding box of the DiGraph
        if next_graph is not None:
            framebox = SurroundingRectangle(
                next_graph.digraph, buff=0.2, corner_radius=0.1
            )
            self.play(
                self.camera.frame.animate.move_to(next_graph.digraph.get_center()).set(
                    height=framebox.height * 1.5
                )
            )
            self.wait(5)


if __name__ == "__main__":
    c = MyGraph()
    c.render()
