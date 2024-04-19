import igraph as ig
from manim import *
from manim_slides import Slide

from animations.demos.graph_example import MyGraph, GraphPair


class APFRBDiagram(Slide, MovingCameraScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graphs = {}

    def construct(self):
        self.draw(origin=ORIGIN, scale=1.0, target_scene=self, animate=True)

    def draw(self, origin=ORIGIN, scale=1.0, target_scene=None, animate=True) -> VGroup:
        if target_scene is None:
            target_scene = self
        # note to self I copied this code directly from MyGraph and only kept the relevant parts
        for model_type in ["dnn", "flc"]:
            if model_type == "dnn":
                displayed_model_name = "Deep Neural Network"
                vs, edges = MyGraph.get_vertices_and_edges_for_dnn()
                layer_types = ["input", "hidden", "hidden", "hidden", "output"]
            elif model_type == "flc":
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

        # code specific to APFRB diagram

        # v_group = VGroup(*[value.digraph for value in self.graphs.values()])
        v_group: VGroup = VGroup()
        for key, value in self.graphs.items():
            new_item = VGroup(
                Text(
                    key, font_size=18, color=BLACK
                ).scale(scale_factor=scale).next_to(value.digraph, UP),
                value.digraph
            )
            if len(v_group) != 0:
                arrow = Arrow(
                    LEFT, RIGHT,
                    color=BLACK, stroke_width=6 * scale, max_stroke_width_to_length_ratio=0.5
                ).scale(2.5 * scale)

                v_group.add(arrow.next_to(v_group[-1], RIGHT))
                v_group.add(
                    Text(
                    "Distill & APFRB", font_size=18, color=BLACK
                    ).scale(scale_factor=scale).next_to(arrow, UP)
                )
                new_item.next_to(arrow, RIGHT)
            v_group.add(new_item)

        v_group.scale(scale_factor=scale).move_to(origin)
        if animate:
            target_scene.camera.frame.move_to(v_group.get_center()).set(width=v_group.width * 1.5)
            target_scene.play(Create(v_group))
            target_scene.wait(1)
            target_scene.next_slide()
        else:
            target_scene.add(v_group)

        return v_group


if __name__ == "__main__":
    APFRBDiagram().render()
