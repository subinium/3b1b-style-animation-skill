---
name: linear-transformations
description: Geometric interpretation of linear transformations
metadata:
  tags: linear-transformation, geometry, matrix, visualization
---

# Linear Transformation Visualization

## Basic Transformation Types

```python
from manim import *
import numpy as np

class TransformationTypes(Scene):
    def construct(self):
        # Grid and basis vectors
        plane = NumberPlane(x_range=[-4, 4], y_range=[-3, 3])
        i_hat = Arrow(ORIGIN, RIGHT, color=GREEN, buff=0)
        j_hat = Arrow(ORIGIN, UP, color=RED, buff=0)

        self.play(Create(plane))
        self.play(GrowArrow(i_hat), GrowArrow(j_hat))
        self.wait()

        # Different transformation types
        transformations = [
            ("Rotation", np.array([[np.cos(PI/4), -np.sin(PI/4)],
                                   [np.sin(PI/4), np.cos(PI/4)]])),
            ("Scaling", np.array([[2, 0], [0, 0.5]])),
            ("Shear", np.array([[1, 1], [0, 1]])),
            ("Reflection", np.array([[1, 0], [0, -1]])),
        ]

        for name, matrix in transformations:
            # Show transformation name
            title = Text(name, font_size=36).to_edge(UP)
            self.play(Write(title))

            # Show matrix
            mat_tex = Matrix(matrix.tolist(), left_bracket="[", right_bracket="]")
            mat_tex.scale(0.8).to_corner(UL)
            self.play(Write(mat_tex))

            # Apply transformation
            self.play(
                plane.animate.apply_matrix(matrix),
                i_hat.animate.put_start_and_end_on(ORIGIN, [*matrix[:, 0], 0]),
                j_hat.animate.put_start_and_end_on(ORIGIN, [*matrix[:, 1], 0]),
                run_time=2
            )
            self.wait()

            # Reset
            self.play(
                plane.animate.apply_matrix(np.linalg.inv(matrix)),
                i_hat.animate.put_start_and_end_on(ORIGIN, RIGHT),
                j_hat.animate.put_start_and_end_on(ORIGIN, UP),
                FadeOut(title),
                FadeOut(mat_tex),
                run_time=1
            )
```

## Composition of Transformations

```python
class TransformationComposition(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-4, 4],
            y_range=[-3, 3],
            background_line_style={"stroke_opacity": 0.5}
        )
        self.play(Create(plane))

        # First transformation: rotation by 45 degrees
        theta = PI / 4
        R = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta), np.cos(theta)]
        ])

        # Second transformation: scaling
        S = np.array([[2, 0], [0, 1]])

        # Show first transformation
        r_label = MathTex(r"R_{45°}").to_corner(UL)
        self.play(Write(r_label))
        self.play(plane.animate.apply_matrix(R), run_time=2)
        self.wait()

        # Show second transformation
        s_label = MathTex(r"\times S").next_to(r_label, RIGHT)
        self.play(Write(s_label))
        self.play(plane.animate.apply_matrix(S), run_time=2)
        self.wait()

        # Show composition matrix
        composition = S @ R  # Note: right to left
        comp_label = MathTex(r"= SR").next_to(s_label, RIGHT)
        self.play(Write(comp_label))

        comp_matrix = Matrix(
            [[f"{composition[i,j]:.2f}" for j in range(2)] for i in range(2)],
            left_bracket="[", right_bracket="]"
        )
        comp_matrix.to_corner(UR)
        self.play(Write(comp_matrix))
        self.wait()
```

## Determinant Visualization

```python
class DeterminantVisualization(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-4, 4],
            y_range=[-3, 3],
            background_line_style={"stroke_opacity": 0.3}
        )
        self.play(Create(plane))

        # Unit square
        unit_square = Square(side_length=1, fill_color=BLUE, fill_opacity=0.5)
        unit_square.move_to(RIGHT * 0.5 + UP * 0.5)
        unit_square_label = MathTex(r"\text{Area} = 1", font_size=24)
        unit_square_label.next_to(unit_square, DOWN)

        self.play(Create(unit_square), Write(unit_square_label))
        self.wait()

        # Transformation matrix
        matrix = np.array([[3, 1], [0, 2]])
        det = np.linalg.det(matrix)  # = 6

        matrix_tex = MathTex(
            r"A = \begin{bmatrix} 3 & 1 \\ 0 & 2 \end{bmatrix}"
        )
        matrix_tex.to_corner(UL)
        self.play(Write(matrix_tex))

        det_tex = MathTex(f"\\det(A) = {det:.0f}")
        det_tex.next_to(matrix_tex, DOWN)
        self.play(Write(det_tex))

        # Apply transformation
        self.play(
            plane.animate.apply_matrix(matrix),
            unit_square.animate.apply_matrix(matrix),
            run_time=2
        )

        # Update area label
        new_label = MathTex(f"\\text{{Area}} = {det:.0f}", font_size=24)
        new_label.next_to(unit_square, DOWN)
        self.play(Transform(unit_square_label, new_label))

        # Explanation
        explanation = Text(
            "Determinant = Area scaling factor",
            font_size=24
        ).to_edge(DOWN)
        self.play(Write(explanation))
        self.wait()


class NegativeDeterminant(Scene):
    """Show orientation reversal with negative determinant"""

    def construct(self):
        plane = NumberPlane(x_range=[-4, 4], y_range=[-3, 3])
        self.play(Create(plane))

        # Oriented triangle
        triangle = Polygon(
            ORIGIN, RIGHT, RIGHT + UP,
            fill_color=BLUE, fill_opacity=0.5
        )
        # Label vertices
        labels = VGroup(
            MathTex("1").move_to(ORIGIN + DOWN * 0.3 + LEFT * 0.3),
            MathTex("2").move_to(RIGHT + DOWN * 0.3 + RIGHT * 0.3),
            MathTex("3").move_to(RIGHT + UP + UP * 0.3)
        )

        self.play(Create(triangle), Write(labels))

        # Reflection matrix (negative determinant)
        matrix = np.array([[1, 0], [0, -1]])

        det_label = MathTex(r"\det(A) = -1", color=RED)
        det_label.to_corner(UL)
        self.play(Write(det_label))

        # Apply - orientation reverses
        self.play(
            plane.animate.apply_matrix(matrix),
            triangle.animate.apply_matrix(matrix),
            labels.animate.apply_matrix(matrix),
            run_time=2
        )

        # Highlight orientation change
        orientation_text = Text("Orientation reversed!", color=RED, font_size=28)
        orientation_text.to_edge(DOWN)
        self.play(Write(orientation_text))
        self.wait()
```

## Null Space Visualization

```python
class NullSpaceVisualization(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-4, 4],
            y_range=[-3, 3],
            background_line_style={"stroke_opacity": 0.3}
        )
        self.play(Create(plane))

        # Rank-deficient matrix (maps to a line)
        matrix = np.array([[1, 2], [0.5, 1]])  # Columns are linearly dependent

        # Show what gets mapped to zero
        null_direction = np.array([2, -1, 0])  # In null space
        null_line = Line(null_direction * -3, null_direction * 3, color=RED)
        null_label = Text("Null Space", font_size=20, color=RED)
        null_label.next_to(null_line, UP)

        self.play(Create(null_line), Write(null_label))

        # Show transformation
        self.play(plane.animate.apply_matrix(matrix), run_time=2)

        # The null space collapses to origin
        collapse_text = Text("Entire line maps to origin", font_size=24)
        collapse_text.to_edge(DOWN)
        self.play(Write(collapse_text))
        self.wait()
```

## Guidelines

- Always show basis vectors (î, ĵ) transforming
- Use grid lines to show area/angle changes
- Color code different transformation types
- Show determinant as area scaling factor
- Animate transformations smoothly (2+ seconds)

## Forbidden

- Do NOT show instant transformations
- Do NOT forget to show basis vectors
- Do NOT skip determinant interpretation
- Do NOT use same color for different transformations
