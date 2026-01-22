---
name: eigenvalues
description: Eigenvalue and eigenvector visualization
metadata:
  tags: eigenvalue, eigenvector, linear-algebra, transformation
---

# Eigenvalue and Eigenvector Visualization

## Basic Eigenvector Concept

```python
from manim import *
import numpy as np

class EigenvectorDemo(Scene):
    def construct(self):
        # Create plane
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.5}
        )
        self.play(Create(plane))

        # Matrix with known eigenvectors
        # A = [[3, 1], [0, 2]]
        # Eigenvectors: [1, 0] (λ=3), [1, -1] (λ=2)
        matrix = np.array([[3, 1], [0, 2]])

        # Regular vector (will rotate and scale)
        regular_vec = Arrow(ORIGIN, [1, 1, 0], color=GRAY, buff=0)
        regular_label = Text("Regular vector", font_size=20, color=GRAY)
        regular_label.next_to(regular_vec, UP)

        # Eigenvector (will only scale)
        eigen_vec = Arrow(ORIGIN, [1, 0, 0], color=YELLOW, buff=0)
        eigen_label = Text("Eigenvector", font_size=20, color=YELLOW)
        eigen_label.next_to(eigen_vec, DOWN)

        self.play(
            GrowArrow(regular_vec), Write(regular_label),
            GrowArrow(eigen_vec), Write(eigen_label)
        )
        self.wait()

        # Apply transformation
        new_regular = matrix @ np.array([1, 1])
        new_eigen = matrix @ np.array([1, 0])  # Should be [3, 0]

        self.play(
            regular_vec.animate.put_start_and_end_on(ORIGIN, [*new_regular, 0]),
            eigen_vec.animate.put_start_and_end_on(ORIGIN, [*new_eigen, 0]),
            plane.animate.apply_matrix(matrix),
            run_time=2,
            rate_func=smooth
        )

        # Highlight that eigenvector stayed on its line
        eigen_line = Line(LEFT * 4, RIGHT * 4, color=YELLOW, stroke_opacity=0.5)
        self.play(Create(eigen_line))

        # Show eigenvalue equation
        equation = MathTex(r"A\vec{v} = \lambda\vec{v}", font_size=36)
        equation.to_corner(UL)
        self.play(Write(equation))

        eigenvalue_text = MathTex(r"\lambda = 3", font_size=28, color=YELLOW)
        eigenvalue_text.next_to(equation, DOWN)
        self.play(Write(eigenvalue_text))
        self.wait()
```

## Multiple Eigenvectors

```python
class MultipleEigenvectors(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.4}
        )
        self.play(Create(plane))

        # Symmetric matrix: has orthogonal eigenvectors
        # A = [[2, 1], [1, 2]]
        # Eigenvalues: 3, 1
        # Eigenvectors: [1, 1], [1, -1]
        matrix = np.array([[2, 1], [1, 2]])

        # Eigenvector 1: λ = 3, v = [1, 1]
        v1 = np.array([1, 1, 0]) / np.sqrt(2)
        eigen1 = Arrow(ORIGIN, v1 * 2, color=BLUE, buff=0)
        label1 = MathTex(r"\lambda_1 = 3", color=BLUE, font_size=24)
        label1.next_to(eigen1, UR, buff=0.1)

        # Eigenvector 2: λ = 1, v = [1, -1]
        v2 = np.array([1, -1, 0]) / np.sqrt(2)
        eigen2 = Arrow(ORIGIN, v2 * 2, color=GREEN, buff=0)
        label2 = MathTex(r"\lambda_2 = 1", color=GREEN, font_size=24)
        label2.next_to(eigen2, DR, buff=0.1)

        self.play(
            GrowArrow(eigen1), Write(label1),
            GrowArrow(eigen2), Write(label2)
        )

        # Show eigenspaces (lines)
        line1 = Line(v1 * -4, v1 * 4, color=BLUE, stroke_opacity=0.3)
        line2 = Line(v2 * -4, v2 * 4, color=GREEN, stroke_opacity=0.3)
        self.play(Create(line1), Create(line2))

        self.wait()

        # Apply transformation - eigenvectors scale by their eigenvalues
        self.play(
            plane.animate.apply_matrix(matrix),
            eigen1.animate.put_start_and_end_on(ORIGIN, v1 * 2 * 3),  # scaled by λ=3
            eigen2.animate.put_start_and_end_on(ORIGIN, v2 * 2 * 1),  # scaled by λ=1
            run_time=2,
            rate_func=smooth
        )
        self.wait()
```

## Eigendecomposition Animation

```python
class EigenDecomposition(Scene):
    def construct(self):
        title = Text("Eigendecomposition", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # A = PDP^(-1)
        main_eq = MathTex(r"A = PDP^{-1}")
        main_eq.shift(UP * 2)
        self.play(Write(main_eq))

        # Matrix A
        A = Matrix([[3, 1], [0, 2]], left_bracket="[", right_bracket="]")
        A_label = MathTex("A =").next_to(A, LEFT)
        A_group = VGroup(A_label, A).shift(LEFT * 3 + DOWN)

        # Matrix P (eigenvectors as columns)
        P = Matrix([[1, 1], [0, -1]], left_bracket="[", right_bracket="]")
        P_label = MathTex("P =").next_to(P, LEFT)
        P_group = VGroup(P_label, P).next_to(A_group, RIGHT, buff=1)

        # Matrix D (eigenvalues on diagonal)
        D = Matrix([[3, 0], [0, 2]], left_bracket="[", right_bracket="]")
        D_label = MathTex("D =").next_to(D, LEFT)
        D_group = VGroup(D_label, D).next_to(P_group, RIGHT, buff=1)

        self.play(
            Create(A_group),
            Create(P_group),
            Create(D_group),
            run_time=2
        )

        # Highlight eigenvectors in P
        eigenvec_rect1 = SurroundingRectangle(
            VGroup(P.get_entries()[0], P.get_entries()[2]),
            color=BLUE, buff=0.1
        )
        eigenvec_rect2 = SurroundingRectangle(
            VGroup(P.get_entries()[1], P.get_entries()[3]),
            color=GREEN, buff=0.1
        )

        self.play(Create(eigenvec_rect1))
        eigenvec_label1 = MathTex(r"\vec{v}_1", color=BLUE, font_size=24)
        eigenvec_label1.next_to(eigenvec_rect1, DOWN)
        self.play(Write(eigenvec_label1))

        self.play(Create(eigenvec_rect2))
        eigenvec_label2 = MathTex(r"\vec{v}_2", color=GREEN, font_size=24)
        eigenvec_label2.next_to(eigenvec_rect2, DOWN)
        self.play(Write(eigenvec_label2))

        # Highlight eigenvalues in D
        eigenval_rect1 = SurroundingRectangle(D.get_entries()[0], color=BLUE, buff=0.1)
        eigenval_rect2 = SurroundingRectangle(D.get_entries()[3], color=GREEN, buff=0.1)

        self.play(Create(eigenval_rect1), Create(eigenval_rect2))

        eigenval_labels = VGroup(
            MathTex(r"\lambda_1 = 3", color=BLUE, font_size=20),
            MathTex(r"\lambda_2 = 2", color=GREEN, font_size=20)
        )
        eigenval_labels[0].next_to(eigenval_rect1, UP)
        eigenval_labels[1].next_to(eigenval_rect2, DOWN)
        self.play(Write(eigenval_labels))
        self.wait()
```

## Geometric Interpretation

```python
class EigenGeometric(Scene):
    def construct(self):
        # Show how transformation stretches along eigenvector directions

        plane = NumberPlane(
            x_range=[-4, 4],
            y_range=[-4, 4],
            background_line_style={"stroke_opacity": 0.3}
        )
        self.play(Create(plane))

        # Unit circle
        circle = Circle(radius=1, color=WHITE, stroke_width=2)
        self.play(Create(circle))

        # Eigenvector directions
        eigen_dir1 = Arrow(ORIGIN, [1, 1, 0] / np.sqrt(2) * 1.5, color=BLUE, buff=0)
        eigen_dir2 = Arrow(ORIGIN, [1, -1, 0] / np.sqrt(2) * 1.5, color=GREEN, buff=0)

        self.play(GrowArrow(eigen_dir1), GrowArrow(eigen_dir2))

        # Transformation turns circle into ellipse
        # with semi-axes along eigenvector directions
        matrix = np.array([[2, 1], [1, 2]])

        # Transform
        self.play(
            circle.animate.apply_matrix(matrix),
            plane.animate.apply_matrix(matrix),
            eigen_dir1.animate.scale(3),  # λ1 = 3
            eigen_dir2.animate.scale(1),  # λ2 = 1
            run_time=3,
            rate_func=smooth
        )

        # Label the ellipse axes
        axis_label1 = MathTex(r"\lambda_1 = 3", color=BLUE, font_size=24)
        axis_label1.next_to(eigen_dir1, UP)
        axis_label2 = MathTex(r"\lambda_2 = 1", color=GREEN, font_size=24)
        axis_label2.next_to(eigen_dir2, DOWN)

        self.play(Write(axis_label1), Write(axis_label2))
        self.wait()
```

## Guidelines

- Show eigenvectors as special directions that don't rotate
- Use different colors for different eigenvalues
- Demonstrate scaling factor visually
- Show unit circle → ellipse transformation
- Always include the eigenvalue equation Av = λv

## Forbidden

- Do NOT show eigenvector rotation (they only scale!)
- Do NOT use same color for different eigenvectors
- Do NOT skip the geometric interpretation
- Do NOT forget to label eigenvalues
