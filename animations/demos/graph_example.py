import math
from manim import *


# https://stackoverflow.com/questions/76175939/manim-add-labels-near-vertices
class MyGraph(Scene):
    def construct(self):
        vertices = [1, 2, 3, 4, 5, 6]
        labels = "ABCDEF"
        label_dict = {i: label for i, label in zip(vertices, labels)}
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (1, 5), (5, 2), (2, 6), (6, 3)]
        lt = {1: [0, 0, 0], 2: [2, 0, 0], 3: [2, 2, 0], 4: [0, 2, 0], 5: [1, math.sqrt(3), 0],
              6: [2 + math.sqrt(3), 1, 0]}
        g = Graph(vertices, edges, layout=lt)
        g.shift(DOWN, LEFT)
        self.play(Create(g), run_time=5)
        tex_labels = []
        for v in g.vertices:
            label = MathTex(label_dict[v]).scale(0.5).next_to(g.vertices[v], UR)
            tex_labels.append(label)
        self.play(Create(VGroup(*tex_labels)))
        self.wait()


if __name__ == "__main__":
    c = MyGraph()
    c.render()
