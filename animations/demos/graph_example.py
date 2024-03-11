import math
import torch
from igraph import Layout
from manim import *

from soft.computing.blueprints.factory import SystematicDesignProcess
from soft.computing.organize import SelfOrganize
from soft.datasets import SupervisedDataset
from soft.utilities.reproducibility import load_configuration


# https://stackoverflow.com/questions/76175939/manim-add-labels-near-vertices
class MyGraph(MovingCameraScene):
    def get_self_organize_graph(self):
        self_organize: SelfOrganize = SystematicDesignProcess(
            algorithms=["clip", "ecm", "wang_mendel"], config=load_configuration()
        ).build(
            training_data=SupervisedDataset(
                inputs=torch.rand((10, 4)), targets=torch.rand((10, 1))
            )
        )
        return self_organize.graph

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
        self_organize_graph = self.get_self_organize_graph()
        # get a layout for this graph
        layout: Layout = self_organize_graph.layout_auto()
        lt = {v: [layout[v][0], layout[v][1], 0] for v in range(len(layout))}
        labels = [
            func if isinstance(func, str) else func.__name__.replace("_", " ")
            for func in self_organize_graph.vs["function"]
        ]
        label_dict = {
            v: label for v, label in zip(self_organize_graph.vs.indices, labels)
        }
        g = DiGraph(
            self_organize_graph.vs.indices,
            self_organize_graph.get_edgelist(),
            layout=lt,
        )
        g.shift(DOWN, LEFT)
        self.play(Create(g), run_time=5)
        self.wait()

        # get a new layout for this graph
        new_layout: Layout = self_organize_graph.layout_sugiyama()
        move_vertices = [
            g[v].animate.move_to(pos + [0.0])
            for v, pos in zip(g.vertices, new_layout.coords)
        ]
        self.play(*move_vertices, run_time=5)

        # move the camera to the new graph location
        self.camera.frame.save_state()
        animation_to_move_camera = self.camera.frame.animate.scale(1.5).move_to(
            g
        )  # 1.5 zoom out
        self.play(animation_to_move_camera, run_time=1)
        self.wait()

        tex_labels = []
        for v in g.vertices:
            # label = MathTex(label_dict[v]).scale(0.5).next_to(g.vertices[v], UR)
            label = Text(label_dict[v]).scale(0.25).next_to(g.vertices[v], UR)
            tex_labels.append(label)
        self.play(Create(VGroup(*tex_labels)))
        self.wait()


if __name__ == "__main__":
    c = MyGraph()
    c.render()
