from functools import partial
from itertools import groupby
from dataclasses import dataclass
from typing import Tuple, Set, Dict as DictType, List as ListType, Union as UnionType

import torch
from manim import *
import igraph as ig

from animations.common import make_axes, AxisConfig, MANIM_BLUE
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
from soft.fuzzy.sets.continuous.impl import Gaussian, Lorentzian
from soft.fuzzy.sets.continuous.abstract import ContinuousFuzzySet
from soft.utilities.reproducibility import load_configuration

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


# https://stackoverflow.com/questions/76175939/manim-add-labels-near-vertices
def get_self_organize(input_size: int = 4, output_size: int = 1) -> SelfOrganize:
    soft_config = load_configuration()
    with soft_config.unfreeze():
        soft_config.clustering.distance_threshold = 0.2
    return SystematicDesignProcess(
        algorithms=["clip", "ecm", "wang_mendel"], config=soft_config
    ).build(
        training_data=SupervisedDataset(
            inputs=torch.rand((250, input_size)), targets=torch.rand((250, output_size))
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

        # display the individual layers

        self.play(digraph.animate.shift(direction * 3))

        layer_colors = [BLUE, GREEN, RED, YELLOW, PURPLE]
        animations = []
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

    @staticmethod
    def get_vertices_and_edges_for_dnn(
        input_size: int = 4, hidden_size: int = 16, output_size: int = 1
    ) -> Tuple[DictType[str, int], Set[Tuple[str, str]]]:
        vs = {}
        all_vertices = []

        all_vertices.extend(
            [f"V{i}" for i in range(0, input_size)]
        )  # layer 1: 4-inputs
        all_vertices.extend([f"P{i}" for i in range(0, hidden_size)])  # layer 2
        all_vertices.extend([f"R{i}" for i in range(0, hidden_size)])  # layer 3
        all_vertices.extend([f"C{i}" for i in range(0, hidden_size)])  # layer 4
        all_vertices.extend(
            [f"O{i}" for i in range(0, output_size)]
        )  # layer 5: 1-output

        for vertex in all_vertices:
            vs[vertex] = int(vertex[1:])

        edges = set()
        for i in range(input_size):
            for j in range(hidden_size):
                edges.add((f"V{i}", f"P{j}"))
        for i in range(hidden_size):
            for j in range(hidden_size):
                edges.add((f"P{i}", f"R{j}"))
        for i in range(hidden_size):
            for j in range(hidden_size):
                edges.add((f"R{i}", f"C{j}"))
        for i in range(hidden_size):
            for j in range(output_size):
                edges.add((f"C{i}", f"O{j}"))
        return vs, edges

    @staticmethod
    def get_vertices_and_edges_for_flc(
        input_size: int = 4, hidden_size: int = 16, output_size: int = 1
    ) -> Tuple[DictType[str, int], Set[Tuple[str, str]]]:
        """
        Create a set of vertices and edges for a graph of an example fuzzy logic controller.

        Returns:
            A tuple containing the vertices and edges of the graph.
        """
        self_organize: SelfOrganize = get_self_organize(
            input_size=input_size, output_size=output_size
        )
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
                    input=SpaceConfiguration(
                        dim=input_size, max_terms=3, expandable=True
                    ),
                    output=SpaceConfiguration(
                        dim=output_size, max_terms=3, expandable=True
                    ),
                ),
                number_of_rules=hidden_size,
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

    def animate_code(
        self,
        model_type: str,
        input_size: int = 4,
        hidden_size: int = 16,
        output_size: int = 1,
    ):
        if model_type == "dnn":
            texts: List[str] = [
                f"""
            import torch
            
            input_size, hidden_size, output_size = {input_size}, {hidden_size}, {output_size}
            deep_neural_network = torch.nn.Sequential(
                torch.nn.Linear(input_size, hidden_size),
                torch.nn.ReLU(),
                torch.nn.Linear(hidden_size, hidden_size),
                torch.nn.ReLU(),
                torch.nn.Linear(hidden_size, output_size)
            )
            """
            ]
        elif model_type == "flc":
            texts: List[str] = [
                f"""
            from soft.computing.organize import SelfOrganize
            from soft.computing.knowledge import KnowledgeBase
            from soft.computing.blueprints.factory import SystematicDesignProcess

            self_organize: SelfOrganize = SystematicDesignProcess(
                algorithms=["clip", "ecm", "wang_mendel"], config=my_config
            ).build(
                training_data=LabeledDataset(
                    inputs=torch.rand((250, {input_size})), targets=torch.rand((250, {output_size}))
                )
            )
            knowledge_base: KnowledgeBase = self_organize.start()
            """,
                f"""
            neuro_fuzzy_network = ZeroOrderTSK(
                specifications=Specifications(
                    t_norm="algebraic_product",
                    engine=Engine(
                        type="tsk",
                        defuzzification="product",
                        confidences=False,
                        ignore_missing=False,
                    ),
                    mapping=Mapping(
                        input=SpaceConfiguration(dim={input_size}, max_terms=3, expandable=False),
                        output=SpaceConfiguration(dim={output_size}, max_terms=3, expandable=False),
                    ),
                    number_of_rules={hidden_size},
                ),
                knowledge_base=knowledge_base,
            )
            """,
            ]
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        for text in texts:
            # create the manim code object and animate it
            code: Code = Code(
                code=text,
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
            self.play(
                Write(code),
                self.camera.frame.animate.move_to(code.get_center()),
                run_time=5,
            )
            self.wait(10)
            self.play(FadeOut(code))
            self.wait()

    def construct(self):
        # iterate over creating each type of model and plotting its graph
        model_graphs = {}
        all_models: UnionType[None, Group] = None
        for model_type in ["dnn", "flc"]:
            if model_type == "dnn":
                displayed_model_name = "Dense Feed-Forward Artificial Neural Network"
                vs, edges = self.get_vertices_and_edges_for_dnn()
                layer_types = ["input", "hidden", "hidden", "hidden", "output"]
            elif model_type == "flc":
                displayed_model_name = "Neuro-Fuzzy Network"
                vs, edges = self.get_vertices_and_edges_for_flc()
                layer_types = ["input", "premise", "rule", "consequence", "output"]
            else:
                raise ValueError(f"Unknown model type: {model_type}")

            # display the model name
            displayed_model_text: Text = Text(
                displayed_model_name, font_size=24, color=BLACK
            )
            self.play(
                self.camera.frame.animate.move_to(displayed_model_text.get_center()),
                Write(displayed_model_text),
                run_time=2,
            )
            self.wait(5)
            self.play(Unwrite(displayed_model_text, run_time=2))

            # animate example code for the model
            self.animate_code(model_type, input_size=4, hidden_size=16, output_size=1)

            # create the igraph.Graph representation of the model
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

            # check that the edges are added correctly
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

            # plot the graph and retain a reference to it as well as its igraph.Graph representation
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
                all_models: UnionType[None, Group] = Group(
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

        # focus on the Deep Neural Network
        self.wait(5)
        self.play(
            self.camera.frame.animate.move_to(model_graphs["dnn"].digraph.get_center())
        )
        self.wait(5)

        # now focus on a single neuron in the Deep Neural Network's hidden layer
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
                (AxisConfig(-6.0, 6.0, step=2.0), AxisConfig(-1.1, 1.1, step=0.2)),
                (AxisConfig(-6.0, 6.0, step=2.0), AxisConfig(-1.1, 1.1, step=0.2)),
                (AxisConfig(-6.0, 6.0, step=2.0), AxisConfig(0.0, 6.0, step=1.0)),
            ],
        )
        # focus on the Neuro-Fuzzy Network
        self.wait(5)
        self.play(
            self.camera.frame.animate.move_to(model_graphs["flc"].digraph.get_center())
        )
        self.wait(5)

        # then focus on a single linguistic term in the Neuro-Fuzzy Network's premise layer
        self.sample_neuron_and_show(
            model_graphs["flc"],
            next_graph=None,
            activation_funcs=[
                ("Gaussian", Gaussian(centers=0.0, widths=1.0)),
                ("Lorentzian", Lorentzian(centers=0.0, widths=1.0)),
            ],
            axis_configs=[
                (AxisConfig(-6.0, 6.0, step=2.0), AxisConfig(0.0, 1.1, step=0.1)),
                (AxisConfig(-6.0, 6.0, step=2.0), AxisConfig(0.0, 1.1, step=0.1)),
            ],
        )
        self.wait(5)

        if all_models is not None:  # both models exist
            # then show the comparison between the two models
            self.play(all_models.animate.move_to(ORIGIN))
            self.play(
                self.camera.frame.animate.move_to(all_models.get_center()),
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

        prev_axes = None
        prev_title = None
        prev_func_label = None
        prev_axis_labels = None
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

            # result is the labels (VGroup of length 2 with two axis labels as Tex objects)
            axis_labels: VGroup = axes.get_axis_labels(
                x_label="Input", y_label="Response"
            )
            title = Text(activation_func_name, color=WHITE).next_to(axes, UP)
            axis_labels[0].shift(1 * DOWN)
            axis_labels[1].rotate(PI / 2).shift(3 * LEFT)
            VGroup(axes, axis_labels[0], axis_labels[1], title).move_to(
                example_neuron
            ).scale(0.0025)

            plotting_animations = []
            # create or update the plot axes
            if prev_axes is None:
                plotting_animations.append(Create(VGroup(axes, axis_labels, title)))
            else:
                plotting_animations.append(
                    Succession(
                        Uncreate(VGroup(prev_axis_labels, prev_title)),
                        AnimationGroup(
                            Transform(
                                mobject=prev_axes,
                                target_mobject=axes,
                                replace_mobject_with_target_in_scene=True,
                            ),
                            Create(VGroup(axis_labels, title)),
                        ),
                    )
                )

            # self.play(
            #     self.camera.frame.animate.set(
            #         width=axes.width + 0.001, height=axes.height + 0.001
            #     ).move_to(axes),
            #     # Write(Text(activation_func_name, color=ORANGE).next_to(axes, UP).scale(0.005)),
            # )

            use_smoothing = True
            center_value, width_value = ValueTracker(0.0), ValueTracker(1.0)

            step_val: float = (
                x_axis_config.max_value - x_axis_config.min_value
            ) / 1000  # the default is 1.0
            if isinstance(activation_func, ContinuousFuzzySet):
                # lambda_func: callable = lambda x: activation_func(
                #     torch.Tensor([x])
                # ).degrees.item()
                lambda_func: callable = (
                    lambda x: activation_func.internal_calculate_membership(
                        observations=torch.Tensor([x]),
                        centers=torch.Tensor([center_value.get_value()]),
                        widths=torch.Tensor([width_value.get_value()]),
                    ).item()
                )
            else:
                lambda_func: callable = lambda x: activation_func(
                    torch.Tensor([x])
                ).item()
                if idx == 0:
                    use_smoothing = (
                        False  # disable smoothing for heaviside step function
                    )

            activation_plot_func = axes.plot(
                lambda_func,
                x_range=(x_axis_config.min_value, x_axis_config.max_value, step_val),
                stroke_color=MANIM_BLUE,
                stroke_width=0.02,
                use_smoothing=use_smoothing,
                # color=ORANGE
            )

            # display the membership function formula
            # membership_formula: Text = Text(
            #     f"μ(x) = {activation_func.latex_formula()}",
            #     color=WHITE
            # ).scale(0.0025).next_to(axes, 0.0025 * DOWN)

            if isinstance(activation_func, ContinuousFuzzySet):
                myTemplate = TexTemplate()
                myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
                func_label = axes.get_graph_label(
                    activation_plot_func,
                    # Text(activation_func_name, font_size=8, color=ORANGE),
                    r"\mu(x) = " + activation_func.latex_formula(),
                    # Text(activation_func_name, color=ORANGE).next_to(axes, UP).scale(0.005),
                    color=MANIM_BLUE,
                    direction=UP,
                )
                func_label.scale(0.0025 * 2.5).move_to(axes.c2p(9, 1.1))
            else:
                func_label = None

            # plot or transform the activation function to the new function
            if prev_activation_plot_func is None:
                plotting_animations.append(Create(activation_plot_func))
                if (
                    isinstance(activation_func, ContinuousFuzzySet)
                    and func_label is not None
                ):
                    plotting_animations.append(Create(func_label))
            else:
                transform_animations = [
                    TransformMatchingShapes(
                        mobject=prev_activation_plot_func,
                        target_mobject=activation_plot_func,
                        replace_mobject_with_target_in_scene=True,
                    )
                ]

                if (
                    isinstance(activation_func, ContinuousFuzzySet)
                    and func_label is not None
                ):
                    transform_animations.append(
                        Succession(
                            Uncreate(prev_func_label),
                            Create(func_label),
                        )
                    )

                plotting_animations.append(AnimationGroup(*transform_animations))

            # add an updater to the plotted function in order to update it
            activation_plot_func.add_updater(
                lambda m: m.become(
                    axes.plot(
                        lambda_func,
                        x_range=(
                            x_axis_config.min_value,
                            x_axis_config.max_value,
                            step_val,
                        ),
                        stroke_color=MANIM_BLUE,
                        stroke_width=0.02,
                        use_smoothing=use_smoothing,
                    )
                )
            )

            # draw axes and the activation function
            self.play(Succession(*plotting_animations))

            if isinstance(activation_func, ContinuousFuzzySet):
                # demonstrate how ContinuousFuzzySet is essentially a tunable activation function
                # display the current parameters
                param_header_text: Text = (
                    Text("Tunable Parameters:", color=WHITE)
                    .scale(0.0025)
                    .next_to(axes, 0.0025 * DOWN)
                )
                center_decimal_number: DecimalNumber = (
                    DecimalNumber(
                        center_value.get_value(), num_decimal_places=2, color=WHITE
                    )
                    .scale(0.0025)
                    .next_to(param_header_text, 0.0025 * DOWN)
                )
                center_decimal_number.add_updater(
                    lambda m_object: m_object.set_value(center_value.get_value())
                )
                center_param_text: Text = (
                    Text("Center: ", color=WHITE)
                    .scale(0.0025)
                    .next_to(center_decimal_number, 0.0025 * LEFT)
                )
                width_decimal_number: DecimalNumber = (
                    DecimalNumber(
                        width_value.get_value(), num_decimal_places=2, color=WHITE
                    )
                    .scale(0.0025)
                    .next_to(center_decimal_number, 0.0025 * DOWN)
                )
                width_decimal_number.add_updater(
                    lambda m_object: m_object.set_value(width_value.get_value())
                )
                width_param_text: Text = (
                    Text("Width: ", color=WHITE)
                    .scale(0.0025)
                    .next_to(width_decimal_number, 0.0025 * LEFT)
                )

                # draw the center and width parameters
                self.play(
                    LaggedStart(
                        Create(param_header_text),
                        Create(center_param_text),
                        Create(center_decimal_number),
                        Create(width_param_text),
                        Create(width_decimal_number),
                    )
                )

                # show that the fuzzy set being tuned well within domain

                return_to_default_setting: AnimationGroup = AnimationGroup(
                    center_param_text.animate.set_color(YELLOW),
                    width_param_text.animate.set_color(YELLOW),
                    center_value.animate.set_value(0),
                    width_value.animate.set_value(1),
                )

                reset_param_text_color: AnimationGroup = AnimationGroup(
                    center_param_text.animate.set_color(WHITE),
                    width_param_text.animate.set_color(WHITE),
                )

                first_succession: Succession = Succession(
                    AnimationGroup(
                        center_param_text.animate.set_color(YELLOW),
                        width_param_text.animate.set_color(YELLOW),
                        center_value.animate.set_value(x_axis_config.max_value / 2),
                        width_value.animate.set_value(4),
                    ),
                    reset_param_text_color,
                    AnimationGroup(
                        center_param_text.animate.set_color(YELLOW),
                        width_param_text.animate.set_color(YELLOW),
                        center_value.animate.set_value(x_axis_config.min_value / 2),
                        width_value.animate.set_value(3),
                    ),
                    reset_param_text_color,
                    AnimationGroup(
                        width_param_text.animate.set_color(YELLOW),
                        width_value.animate.set_value(0.5),
                    ),
                    reset_param_text_color,
                    AnimationGroup(
                        width_param_text.animate.set_color(YELLOW),
                        width_value.animate.set_value(2),
                    ),
                    return_to_default_setting,
                    reset_param_text_color,
                )
                # show the fuzzy set being tuned toward the extreme of a domain
                second_succession: Succession = Succession(
                    AnimationGroup(
                        center_param_text.animate.set_color(YELLOW),
                        center_value.animate.set_value(x_axis_config.max_value),
                    ),
                    reset_param_text_color,
                    AnimationGroup(
                        width_param_text.animate.set_color(YELLOW),
                        width_value.animate.set_value(0.5),
                    ),
                    reset_param_text_color,
                    AnimationGroup(
                        center_param_text.animate.set_color(YELLOW),
                        center_value.animate.set_value(x_axis_config.min_value),
                    ),
                    reset_param_text_color,
                    AnimationGroup(
                        width_param_text.animate.set_color(YELLOW),
                        width_value.animate.set_value(x_axis_config.max_value),
                    ),
                    reset_param_text_color,
                    return_to_default_setting,
                    reset_param_text_color,
                )  # this is more to highlight the shortcomings of fuzzy sets

                for succession in [first_succession, second_succession]:
                    self.play(succession, run_time=20)
                    self.wait(5)
            prev_axes = axes
            prev_title = title
            prev_func_label = func_label
            prev_axis_labels = axis_labels
            self.wait(5)
            # self.play(FadeOut(func_label))
            prev_activation_plot_func = activation_plot_func
        # get the bounding box of the DiGraph
        if next_graph is not None:
            frame_box = SurroundingRectangle(
                next_graph.digraph, buff=0.2, corner_radius=0.1
            )
            self.play(
                self.camera.frame.animate.move_to(next_graph.digraph.get_center()).set(
                    height=frame_box.height * 1.5
                ),
                run_time=3,
            )
        else:
            frame_box = SurroundingRectangle(
                focused_graph.digraph, buff=0.2, corner_radius=0.1
            )
            self.play(
                self.camera.frame.animate.move_to(
                    focused_graph.digraph.get_center()
                ).set(height=frame_box.height * 1.5),
                run_time=3,
            )


if __name__ == "__main__":
    c = MyGraph()
    c.render()
