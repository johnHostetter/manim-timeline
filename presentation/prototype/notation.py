from manim import *

from manim_beamer.slides import SlideWithList
from manim_beamer.lists import ItemizedList, BulletedList as BL

config.background_color = WHITE
light_theme_style = {
    "fill_color": BLACK,
    "background_stroke_color": WHITE,
}


def get_notation() -> SlideWithList:
    """
    Create a slide discussing the notation that will be used.

    Returns:
        The slide describing the notation.
    """
    myTemplate = TexTemplate()
    myTemplate.add_to_preamble(r"\usepackage{mathrsfs}")
    return SlideWithList(
        title="Necessary Notation",
        subtitle=None,
        width_buffer=12.0,
        beamer_list=ItemizedList(
            items=[
                "Membership Matrix",
                BL(
                    items=[
                        VGroup(
                            Text("Let  ", color=BLACK),
                            MathTex(r"M(\mathbf{x})", color=BLACK),
                            Text(" be the resulting membership matrix.", color=BLACK),
                        ),
                        VGroup(
                            Text("Shape of  ", color=BLACK),
                            MathTex(r"M(\mathbf{x})", color=BLACK),
                            Text(" is ", color=BLACK),
                            VGroup(
                                MathTex(r"|{\mathcal{V}}|", color=BLACK),
                                Cross(color=BLACK, stroke_width=3).scale(
                                    scale_factor=0.1
                                ),
                                MathTex(r"{\max_{v} |\mathcal{T}}|", color=BLACK),
                            ),
                        ),
                    ]
                ),
                "Mask Matrix",
                BL(
                    items=[
                        VGroup(
                            Text("A binary mask matrix  ", color=BLACK),
                            MathTex(r"B", color=BLACK),
                            Text(
                                " contains a 1 iff linguistic term exists at ",
                                color=BLACK,
                            ),
                            MathTex(r"v, t.", color=BLACK),
                        ),
                        VGroup(
                            Text("Shape of  ", color=BLACK),
                            MathTex(r"B", color=BLACK),
                            Text(" is ", color=BLACK),
                            VGroup(
                                MathTex(r"|{\mathcal{V}}|", color=BLACK),
                                Cross(color=BLACK, stroke_width=3).scale(
                                    scale_factor=0.1
                                ),
                                MathTex(r"{\max_{v} |\mathcal{T}}|", color=BLACK),
                            ),
                        ),
                    ]
                ),
                "Premise Calculation",
                BL(
                    items=[
                        "Non-existing memberships are dropped by Hadamard product",
                        VGroup(MathTex(r"M(\mathbf{x}) \odot B", color=BLACK)),
                    ]
                ),
                "Rule Connection Matrix",
                BL(
                    items=[
                        VGroup(
                            Text("Let  ", color=BLACK),
                            MathTex(r"L", color=BLACK),
                            Text(
                                " be the link matrix between premise and rule layer.",
                                color=BLACK,
                            ),
                        ),
                        VGroup(
                            Text("Shape of  ", color=BLACK),
                            MathTex(r"L", color=BLACK),
                            Text(" is ", color=BLACK),
                            VGroup(
                                MathTex(r"|{\mathcal{V}}|", color=BLACK),
                                Cross(color=BLACK, stroke_width=3).scale(
                                    scale_factor=0.1
                                ),
                                MathTex(r"{\max_{v} |\mathcal{T}}|", color=BLACK),
                                Cross(color=BLACK, stroke_width=3).scale(
                                    scale_factor=0.1
                                ),
                                MathTex(r"|{\mathcal{R}}|", color=BLACK),
                            ),
                        ),
                        VGroup(
                            Text("Entry at  ", color=BLACK),
                            MathTex(r"L_{v, t, r}", color=BLACK),
                            Text(" is 0 or 1 iff the ", color=BLACK),
                            MathTex(r"t^{th}", color=BLACK),
                            Text(" term of ", color=BLACK),
                            MathTex(r"v^{th}", color=BLACK),
                            Text(" variable is in ", color=BLACK),
                            MathTex(r"r^{th}", color=BLACK),
                            Text(" rule' premise.", color=BLACK),
                        ),
                    ]
                ),
            ]
        ),
    )


if __name__ == "__main__":
    get_notation().render()
