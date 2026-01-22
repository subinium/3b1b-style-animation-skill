---
name: gradient-flow
description: Visualizing gradient descent and optimization
metadata:
  tags: gradient, descent, optimization, learning
---

# Gradient Flow Visualization

## 2D Gradient Descent Animation

```python
from manim import *
import numpy as np

class GradientDescent2D(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True}
        )

        # Loss function (parabola)
        loss_curve = axes.plot(lambda x: x**2, color=BLUE)

        # Labels
        x_label = MathTex("w").next_to(axes.x_axis, RIGHT)
        y_label = MathTex("L(w)").next_to(axes.y_axis, UP)

        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(Create(loss_curve))
        self.wait()

        # Starting point
        x_val = 2.5
        learning_rate = 0.3

        point = Dot(axes.c2p(x_val, x_val**2), color=YELLOW, radius=0.1)
        point_label = MathTex(f"w = {x_val:.2f}").next_to(point, UR, buff=0.1)
        point_label.scale(0.7)

        self.play(GrowFromCenter(point), Write(point_label))
        self.wait()

        # Gradient descent steps
        for step in range(8):
            # Calculate gradient
            gradient = 2 * x_val  # d/dx(x^2) = 2x

            # Show gradient arrow
            grad_arrow = Arrow(
                axes.c2p(x_val, x_val**2),
                axes.c2p(x_val + 0.5 * np.sign(gradient), x_val**2),
                color=RED,
                buff=0
            )
            grad_label = MathTex(r"\nabla L", color=RED, font_size=24)
            grad_label.next_to(grad_arrow, UP, buff=0.1)

            self.play(GrowArrow(grad_arrow), Write(grad_label), run_time=0.5)

            # Update x
            new_x = x_val - learning_rate * gradient

            # Move point
            new_point_pos = axes.c2p(new_x, new_x**2)
            new_label = MathTex(f"w = {new_x:.2f}").next_to(new_point_pos, UR, buff=0.1)
            new_label.scale(0.7)

            self.play(
                point.animate.move_to(new_point_pos),
                Transform(point_label, new_label),
                FadeOut(grad_arrow),
                FadeOut(grad_label),
                run_time=0.6
            )

            x_val = new_x

            if abs(gradient) < 0.1:
                break

        self.wait()

        # Final annotation
        minimum = MathTex(r"\text{Minimum: } w^* = 0", color=GREEN)
        minimum.to_edge(DOWN)
        self.play(Write(minimum))
        self.wait()
```

## Gradient Vector Field

```python
class GradientVectorField(Scene):
    def construct(self):
        # 2D loss surface as contour plot
        def loss_function(x, y):
            return x**2 + y**2

        # Create vector field showing gradient direction
        vector_field = ArrowVectorField(
            lambda p: -np.array([2*p[0], 2*p[1], 0]),  # Negative gradient
            x_range=[-3, 3, 0.5],
            y_range=[-3, 3, 0.5],
            length_func=lambda norm: 0.3 * sigmoid(norm)
        )

        # Contour lines
        contours = VGroup()
        for r in [0.5, 1, 1.5, 2, 2.5]:
            circle = Circle(radius=r, stroke_color=BLUE, stroke_opacity=0.5)
            contours.add(circle)

        self.play(Create(contours))
        self.play(Create(vector_field), run_time=2)
        self.wait()

        # Trace gradient descent path
        path_points = []
        x, y = 2.5, 2.0
        lr = 0.1

        for _ in range(30):
            path_points.append([x, y, 0])
            grad_x, grad_y = 2*x, 2*y
            x -= lr * grad_x
            y -= lr * grad_y

        path = VMobject()
        path.set_points_smoothly([np.array(p) for p in path_points])
        path.set_stroke(YELLOW, width=3)

        self.play(Create(path), run_time=2)

        # Final point
        final_dot = Dot(path_points[-1], color=GREEN, radius=0.15)
        self.play(GrowFromCenter(final_dot))
        self.wait()
```

## Learning Rate Comparison

```python
class LearningRateComparison(Scene):
    def construct(self):
        # Create three side-by-side demonstrations
        learning_rates = [0.01, 0.1, 0.5]
        colors = [RED, GREEN, BLUE]
        labels = ["Too Small", "Just Right", "Too Large"]

        axes_group = VGroup()
        for i, (lr, color, label) in enumerate(zip(learning_rates, colors, labels)):
            ax = Axes(
                x_range=[-2, 2, 1],
                y_range=[0, 4, 1],
                x_length=3,
                y_length=2.5
            )
            curve = ax.plot(lambda x: x**2, color=WHITE, stroke_width=2)

            title = Text(f"lr = {lr}", font_size=20)
            title.next_to(ax, UP, buff=0.2)

            subtitle = Text(label, font_size=16, color=color)
            subtitle.next_to(title, DOWN, buff=0.1)

            group = VGroup(ax, curve, title, subtitle)
            axes_group.add(group)

        axes_group.arrange(RIGHT, buff=0.8)
        self.play(Create(axes_group), run_time=2)
        self.wait()

        # Animate gradient descent for each
        for i, (lr, ax_group) in enumerate(zip(learning_rates, axes_group)):
            ax = ax_group[0]
            x_val = 1.8
            point = Dot(ax.c2p(x_val, x_val**2), color=YELLOW, radius=0.08)
            self.add(point)

            for _ in range(15):
                gradient = 2 * x_val
                new_x = x_val - lr * gradient

                # Clamp for visualization
                new_x = max(-2, min(2, new_x))

                new_pos = ax.c2p(new_x, new_x**2)
                self.play(point.animate.move_to(new_pos), run_time=0.15)

                x_val = new_x

        self.wait()
```

## Gradient Magnitude Visualization

```python
def visualize_gradient_magnitude(scene, network, gradients):
    """Color neurons and connections based on gradient magnitude"""

    max_grad = max(abs(g) for layer_grads in gradients for g in layer_grads)

    for layer_idx, layer_grads in enumerate(gradients):
        for neuron_idx, grad in enumerate(layer_grads):
            neuron = network.layers[layer_idx].neurons[neuron_idx]

            # Color based on gradient magnitude
            normalized = abs(grad) / max_grad
            color = interpolate_color("#1e3a5f", "#ff6b6b", normalized)

            scene.play(
                neuron.animate.set_stroke(color, width=2 + normalized * 4),
                run_time=0.2
            )
```

## Guidelines

- Always show the loss function/surface first
- Use arrows to clearly indicate gradient direction
- Animate step-by-step, not all at once
- Show learning rate effects with comparison
- Color code: red for gradient direction, yellow for current position, green for minimum

## Forbidden

- Do NOT use instantaneous jumps in gradient descent visualization
- Do NOT skip showing the gradient vector
- Do NOT use uniform step sizes when demonstrating learning rate
- Do NOT forget to label axes (w for weights, L for loss)
