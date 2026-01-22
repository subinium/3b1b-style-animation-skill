---
name: vector-space
description: Vector and embedding space visualization
metadata:
  tags: vector, space, embedding, transformation
---

# Vector Space Visualization

## Basic Vector Operations

```python
from manim import *
import numpy as np

class VectorOperations(Scene):
    def construct(self):
        # Create coordinate plane
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        )
        self.play(Create(plane))

        # Vector a
        a = np.array([2, 1, 0])
        vec_a = Arrow(ORIGIN, a, color=BLUE, buff=0)
        label_a = MathTex(r"\vec{a}", color=BLUE).next_to(vec_a, UP, buff=0.1)

        # Vector b
        b = np.array([1, 2, 0])
        vec_b = Arrow(ORIGIN, b, color=GREEN, buff=0)
        label_b = MathTex(r"\vec{b}", color=GREEN).next_to(vec_b, RIGHT, buff=0.1)

        self.play(
            GrowArrow(vec_a), Write(label_a),
            GrowArrow(vec_b), Write(label_b)
        )
        self.wait()

        # Vector addition
        vec_b_shifted = Arrow(a, a + b, color=GREEN, buff=0)
        sum_vec = Arrow(ORIGIN, a + b, color=YELLOW, buff=0)
        sum_label = MathTex(r"\vec{a} + \vec{b}", color=YELLOW)
        sum_label.next_to(sum_vec, RIGHT)

        self.play(
            Transform(vec_b.copy(), vec_b_shifted),
            run_time=1
        )
        self.play(GrowArrow(sum_vec), Write(sum_label))
        self.wait()
```

## Linear Transformation

```python
class LinearTransformation(Scene):
    def construct(self):
        # Create number plane with grid
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_opacity": 0.6
            }
        )

        # Basis vectors
        i_hat = Arrow(ORIGIN, RIGHT, color=GREEN, buff=0)
        j_hat = Arrow(ORIGIN, UP, color=RED, buff=0)

        i_label = MathTex(r"\hat{i}", color=GREEN, font_size=24)
        i_label.next_to(i_hat, DOWN, buff=0.1)

        j_label = MathTex(r"\hat{j}", color=RED, font_size=24)
        j_label.next_to(j_hat, LEFT, buff=0.1)

        self.play(Create(plane))
        self.play(
            GrowArrow(i_hat), Write(i_label),
            GrowArrow(j_hat), Write(j_label)
        )
        self.wait()

        # Transformation matrix
        matrix = np.array([[2, 1], [1, 2]])

        # Show matrix
        matrix_tex = MathTex(
            r"A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}"
        )
        matrix_tex.to_corner(UL)
        self.play(Write(matrix_tex))

        # Apply transformation
        self.play(
            plane.animate.apply_matrix(matrix),
            i_hat.animate.put_start_and_end_on(ORIGIN, matrix @ np.array([1, 0, 0])[:2].tolist() + [0]),
            j_hat.animate.put_start_and_end_on(ORIGIN, matrix @ np.array([0, 1, 0])[:2].tolist() + [0]),
            run_time=2,
            rate_func=smooth
        )

        # Update labels
        self.play(
            i_label.animate.next_to(i_hat, DOWN),
            j_label.animate.next_to(j_hat, LEFT)
        )
        self.wait()
```

## 3D Embedding Space

```python
class EmbeddingSpace3D(ThreeDScene):
    def construct(self):
        # 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )

        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(axes))

        # Word embeddings as points
        embeddings = {
            "king": np.array([1, 2, 1]),
            "queen": np.array([1.5, 2.5, 0.5]),
            "man": np.array([0.5, 1, 1.5]),
            "woman": np.array([1, 1.5, 1]),
        }

        dots = VGroup()
        labels = VGroup()

        for word, vec in embeddings.items():
            dot = Dot3D(axes.c2p(*vec), color=BLUE, radius=0.1)
            label = Text(word, font_size=20)
            label.next_to(dot, RIGHT + UP, buff=0.1)
            self.add_fixed_orientation_mobjects(label)

            dots.add(dot)
            labels.add(label)

        self.play(Create(dots), Write(labels))

        # Show vector arithmetic: king - man + woman ≈ queen
        king_vec = embeddings["king"]
        man_vec = embeddings["man"]
        woman_vec = embeddings["woman"]

        result_vec = king_vec - man_vec + woman_vec

        # Arrows showing the computation
        arrow1 = Arrow3D(
            axes.c2p(*king_vec),
            axes.c2p(*(king_vec - man_vec)),
            color=RED
        )
        arrow2 = Arrow3D(
            axes.c2p(*(king_vec - man_vec)),
            axes.c2p(*result_vec),
            color=GREEN
        )

        self.play(Create(arrow1))
        self.wait(0.5)
        self.play(Create(arrow2))

        # Highlight result near queen
        result_dot = Dot3D(axes.c2p(*result_vec), color=YELLOW, radius=0.15)
        self.play(GrowFromCenter(result_dot))

        # Rotate to show 3D structure
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(4)
        self.stop_ambient_camera_rotation()
```

## Span Visualization

```python
class SpanVisualization(Scene):
    def construct(self):
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1]
        )
        self.play(Create(plane))

        # Two vectors
        v1 = np.array([1, 0.5, 0])
        v2 = np.array([0.5, 1, 0])

        vec1 = Arrow(ORIGIN, v1, color=BLUE, buff=0)
        vec2 = Arrow(ORIGIN, v2, color=GREEN, buff=0)

        label1 = MathTex(r"\vec{v}_1", color=BLUE).next_to(vec1, UP)
        label2 = MathTex(r"\vec{v}_2", color=GREEN).next_to(vec2, RIGHT)

        self.play(
            GrowArrow(vec1), Write(label1),
            GrowArrow(vec2), Write(label2)
        )
        self.wait()

        # Show span as shaded region
        # For 2 linearly independent vectors in 2D, span is entire plane
        span_region = Rectangle(
            width=8, height=8,
            fill_color=YELLOW,
            fill_opacity=0.2,
            stroke_width=0
        )

        span_label = MathTex(r"\text{Span}(\vec{v}_1, \vec{v}_2) = \mathbb{R}^2")
        span_label.to_edge(UP)

        self.play(FadeIn(span_region), Write(span_label))
        self.wait()

        # Show linear combination
        coeff1 = ValueTracker(1)
        coeff2 = ValueTracker(1)

        combination_vec = always_redraw(
            lambda: Arrow(
                ORIGIN,
                coeff1.get_value() * v1 + coeff2.get_value() * v2,
                color=YELLOW,
                buff=0
            )
        )

        self.add(combination_vec)

        # Animate changing coefficients
        self.play(coeff1.animate.set_value(2), run_time=1)
        self.play(coeff2.animate.set_value(-1), run_time=1)
        self.play(
            coeff1.animate.set_value(0.5),
            coeff2.animate.set_value(2),
            run_time=1
        )
        self.wait()
```

## Guidelines

- Use distinct colors for different vectors (blue, green, red)
- Show coordinate grid for reference
- Animate transformations smoothly
- Label all vectors with proper notation
- Use 3D for embedding space visualizations

## Forbidden

- Do NOT use same color for multiple vectors
- Do NOT skip showing the coordinate system
- Do NOT apply instant transformations (always animate)
- Do NOT forget basis vector labeling (î, ĵ)
