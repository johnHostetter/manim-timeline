from typing import Union, Tuple
from dataclasses import dataclass

import igraph as ig
from manim import (
    DiGraph,
    Dot,
)


@dataclass
class GraphPair:
    """
    Pair of igraph.Graph and manim.DiGraph representations of a graph.
    """

    igraph: ig.Graph  # the igraph.Graph representation of the graph
    digraph: DiGraph  # the manim representation of the igraph.Graph

    def __len__(self) -> int:
        return len(self.igraph.vs)

    def __getitem__(self, item: Union[str, int]) -> Tuple[ig.Vertex, Dot]:
        index = item  # assume the given item is a vertex index
        if isinstance(item, str):
            # the given item is a vertex name, get its index
            index = self.igraph.vs.select(name_eq=item).indices[0]
        return self.igraph.vs[index], self.digraph.vertices[index]
