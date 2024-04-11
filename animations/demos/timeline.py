from functools import partial
from dataclasses import dataclass
from typing import Tuple, List as ListType, Union as UnionType

import torch
from manim import *
from manim_slides import Slide
import igraph as ig

from animations.demos.einstein import EinsteinQuote
from animations.demos.graph_example import MyGraph
from animations.common import make_axes, AxisConfig, MANIM_BLUE
from soft.datasets import SupervisedDataset
from soft.computing.organize import SelfOrganize
from soft.computing.blueprints.factory import SystematicDesignProcess
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


class Timeline(Slide, MovingCameraScene):
    def construct(self):
        # iterate over creating each type of model and plotting its graph
        model_graphs = {}
        all_models: UnionType[None, Group] = None

        timeline_igraph: ig.Graph = ig.Graph(directed=True)

        num_of_vertices = 5
        timeline_igraph.add_vertices(num_of_vertices)
        timeline_igraph.vs["name"] = ["2010", "2015", "2020", "2025", "2030"]

        edges = list(zip(range(0, num_of_vertices - 1), range(1, num_of_vertices)))

        timeline_igraph.add_edges(edges)

        digraph_layout = {idx: (idx * 5, 0, 0) for idx in range(num_of_vertices)}

        timeline_manim = DiGraph(
            timeline_igraph.vs.indices,
            timeline_igraph.get_edgelist(),
            label_fill_color=BLACK,
            layout=digraph_layout,
            vertex_config={
                "fill_color": BLACK,
                "stroke_color": BLACK,
                "stroke_width": 2,
                "radius": 0.05,
            },
            edge_config={
                "stroke_color": "BLACK",
                "stroke_width": 2,
                "tip_config": {"tip_length": 0.07, "tip_width": 0.07},
            },
        )

        timeline = GraphPair(timeline_igraph, digraph=timeline_manim)

        # start_loc = timeline.digraph.vertices[0].get_center()
        # end_loc = timeline.digraph.vertices[num_of_vertices - 1].get_center()
        source_vertex_idx = 0
        source_vertex = timeline.digraph.vertices[source_vertex_idx]
        self.play(Create(source_vertex.set_opacity(0.0)))
        self.play(self.camera.frame.animate.move_to(source_vertex).set(width=10))
        for idx, edge in enumerate(edges):
            source_vertex_idx, target_vertex_idx = edge[0], edge[1]
            target_vertex = timeline.digraph.vertices[target_vertex_idx]
            line: Line = timeline.digraph.edges[edge[0], edge[1]]
            self.play(Create(line), self.camera.frame.animate.move_to(target_vertex))
            self.play(Create(target_vertex))
            # self.play(self.camera.frame.animate.move_to(target_vertex).set(width=0.075))

            vertex_coords = target_vertex.get_center()
            pin: Line = Line(vertex_coords, vertex_coords + UP, color=BLACK)

            self.play(
                Create(pin),
                self.camera.frame.animate.move_to(vertex_coords + UP).set(width=10)
            )
            boundary = Rectangle(color=BLACK).move_to(vertex_coords + (2 * UP))
            self.play(Create(boundary))
            self.next_slide()
            # EinsteinQuote.draw(self)
            self.play(self.camera.frame.animate.move_to(target_vertex.get_center()).set(width=10))

        # self.play(Create(timeline.digraph, run_time=1))
        self.wait(10)


if __name__ == "__main__":
    c = Timeline()
    c.render()
