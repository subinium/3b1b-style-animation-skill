---
name: weight-update
description: Animating weight updates during training
metadata:
  tags: weights, training, update, optimization
---

# Weight Update Visualization

## Single Weight Update

```python
from manim import *
import numpy as np

class WeightUpdateDemo(Scene):
    def construct(self):
        # Connection between two neurons
        n1 = Circle(radius=0.4, fill_color=BLUE, fill_opacity=0.7)
        n1.shift(LEFT * 2)

        n2 = Circle(radius=0.4, fill_color=GREEN, fill_opacity=0.7)
        n2.shift(RIGHT * 2)

        connection = Line(
            n1.get_right(), n2.get_left(),
            stroke_width=4, color=WHITE
        )

        # Weight value
        weight_value = ValueTracker(0.5)

        weight_label = always_redraw(lambda: MathTex(
            f"w = {weight_value.get_value():.3f}",
            font_size=32
        ).next_to(connection, UP))

        self.play(
            GrowFromCenter(n1),
            GrowFromCenter(n2),
            Create(connection),
            Write(weight_label)
        )
        self.wait()

        # Show update equation
        equation = MathTex(
            r"w_{\text{new}} = w_{\text{old}} - \eta \cdot \frac{\partial L}{\partial w}",
            font_size=32
        )
        equation.to_edge(DOWN, buff=1)
        self.play(Write(equation))
        self.wait()

        # Simulate updates
        learning_rate = 0.1
        gradients = [0.3, 0.2, 0.15, 0.08, 0.03, 0.01]

        for i, grad in enumerate(gradients):
            # Show gradient
            grad_text = MathTex(
                f"\\nabla w = {grad:.2f}",
                font_size=24,
                color=RED
            )
            grad_text.next_to(connection, DOWN, buff=0.3)

            # Calculate new weight
            old_w = weight_value.get_value()
            new_w = old_w - learning_rate * grad

            # Animate connection color based on gradient
            self.play(
                Write(grad_text),
                connection.animate.set_color(
                    interpolate_color(WHITE, RED, min(grad * 3, 1))
                ),
                run_time=0.4
            )

            # Update weight with smooth animation
            self.play(
                weight_value.animate.set_value(new_w),
                run_time=0.5
            )

            # Reset connection color
            self.play(
                FadeOut(grad_text),
                connection.animate.set_color(WHITE),
                run_time=0.3
            )

        self.wait()

        # Final state indicator
        converged = Text("Converged!", font_size=32, color=GREEN)
        converged.next_to(equation, UP)
        self.play(Write(converged))
        self.wait()
```

## Batch Weight Update

```python
class BatchWeightUpdate(Scene):
    def construct(self):
        # Create mini network
        network = self.create_simple_network()
        network.scale(0.7).to_edge(UP, buff=1)
        self.add(network)

        # Training samples
        samples = VGroup()
        for i in range(4):
            sample = Square(side_length=0.5, fill_color=BLUE, fill_opacity=0.6)
            sample_label = MathTex(f"x_{i+1}", font_size=16).move_to(sample)
            samples.add(VGroup(sample, sample_label))

        samples.arrange(RIGHT, buff=0.3)
        samples.shift(DOWN * 1.5)

        self.play(Create(samples))
        self.wait()

        # Process each sample and accumulate gradients
        gradient_arrows = VGroup()

        for i, sample in enumerate(samples):
            # Highlight current sample
            self.play(sample.animate.set_fill(YELLOW, opacity=0.8), run_time=0.3)

            # Show forward pass (simplified)
            pulse = Dot(color=YELLOW, radius=0.1)
            pulse.move_to(network.get_left())
            self.add(pulse)
            self.play(
                pulse.animate.move_to(network.get_right()),
                run_time=0.5
            )
            self.remove(pulse)

            # Accumulate gradient (show arrow growing)
            grad_arrow = Arrow(
                DOWN * 2.5, DOWN * 2.5 + DOWN * 0.3 * (i + 1),
                color=RED, buff=0
            )
            gradient_arrows.add(grad_arrow)

            self.play(
                sample.animate.set_fill(BLUE, opacity=0.6),
                Transform(
                    gradient_arrows,
                    Arrow(DOWN * 2.5, DOWN * 2.5 + DOWN * 0.3 * (i + 1), color=RED, buff=0)
                ),
                run_time=0.3
            )

        # Average gradients
        avg_label = MathTex(
            r"\nabla w = \frac{1}{n}\sum_i \nabla w_i",
            font_size=28
        ).shift(DOWN * 3.5)
        self.play(Write(avg_label))

        # Apply update
        update_arrow = Arrow(
            gradient_arrows.get_bottom(),
            network.get_bottom(),
            color=GREEN,
            stroke_width=4
        )
        update_label = Text("Update", font_size=20, color=GREEN)
        update_label.next_to(update_arrow, RIGHT)

        self.play(GrowArrow(update_arrow), Write(update_label))

        # Flash network to show update
        self.play(
            network.animate.set_stroke(GREEN, width=4),
            run_time=0.3
        )
        self.play(
            network.animate.set_stroke(WHITE, width=2),
            run_time=0.3
        )
        self.wait()

    def create_simple_network(self):
        layers = VGroup()
        for i in range(3):
            layer = VGroup(*[Circle(radius=0.2, fill_opacity=0.6) for _ in range(3)])
            layer.arrange(DOWN, buff=0.3)
            layers.add(layer)
        layers.arrange(RIGHT, buff=1)
        return layers
```

## Weight Matrix Visualization

```python
class WeightMatrixUpdate(Scene):
    def construct(self):
        # Weight matrix
        matrix_values = [[0.1, 0.3], [-0.2, 0.4], [0.5, -0.1]]
        matrix = Matrix(
            [[f"{v:.1f}" for v in row] for row in matrix_values],
            left_bracket="[",
            right_bracket="]"
        )

        matrix_label = MathTex("W =").next_to(matrix, LEFT)
        matrix_group = VGroup(matrix_label, matrix)
        matrix_group.to_edge(UP, buff=1)

        self.play(Write(matrix_group))
        self.wait()

        # Gradient matrix
        grad_values = [[0.05, -0.02], [0.01, 0.03], [-0.04, 0.02]]

        grad_matrix = Matrix(
            [[f"{v:.2f}" for v in row] for row in grad_values],
            left_bracket="[",
            right_bracket="]",
            element_to_mobject_config={"color": RED}
        )
        grad_label = MathTex(r"\nabla W =", color=RED).next_to(grad_matrix, LEFT)
        grad_group = VGroup(grad_label, grad_matrix)
        grad_group.next_to(matrix_group, DOWN, buff=0.8)

        self.play(Write(grad_group))
        self.wait()

        # Update equation
        eta = 0.1
        update_eq = MathTex(
            r"W_{\text{new}} = W - \eta \nabla W",
            font_size=36
        ).shift(DOWN)

        self.play(Write(update_eq))
        self.wait()

        # Calculate new matrix
        new_values = [
            [w - eta * g for w, g in zip(w_row, g_row)]
            for w_row, g_row in zip(matrix_values, grad_values)
        ]

        new_matrix = Matrix(
            [[f"{v:.2f}" for v in row] for row in new_values],
            left_bracket="[",
            right_bracket="]",
            element_to_mobject_config={"color": GREEN}
        )
        new_label = MathTex(r"W_{\text{new}} =", color=GREEN).next_to(new_matrix, LEFT)
        new_group = VGroup(new_label, new_matrix)
        new_group.next_to(update_eq, DOWN, buff=0.5)

        self.play(Write(new_group))
        self.wait()

        # Highlight changes
        for i in range(3):
            for j in range(2):
                old_entry = matrix.get_entries()[i * 2 + j]
                new_entry = new_matrix.get_entries()[i * 2 + j]

                self.play(
                    old_entry.animate.set_color(YELLOW),
                    new_entry.animate.set_color(YELLOW),
                    run_time=0.2
                )
                self.play(
                    old_entry.animate.set_color(WHITE),
                    new_entry.animate.set_color(GREEN),
                    run_time=0.2
                )

        self.wait()
```

## Guidelines

- Show old weight value, gradient, and new weight value
- Use ValueTracker for smooth weight value animations
- Color code: white for current weights, red for gradients, green for updated weights
- Visualize the update equation alongside the animation
- For batch updates, show gradient accumulation

## Forbidden

- Do NOT show instant weight changes - always animate
- Do NOT use same color for weights and gradients
- Do NOT skip showing the learning rate in equations
- Do NOT update all weights at exact same time (use slight delays)
