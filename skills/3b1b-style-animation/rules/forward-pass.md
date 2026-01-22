---
name: forward-pass
description: Animating data flow through the neural network
metadata:
  tags: forward-pass, inference, data-flow, animation
---

# Forward Pass Visualization

## Basic Forward Pass Animation

```python
from manim import *
import numpy as np

class ForwardPassDemo(Scene):
    def construct(self):
        # Create simple network
        network = self.create_network([3, 4, 2])
        self.add(network)

        # Animate forward pass
        self.animate_forward_pass(network, input_values=[0.8, 0.3, 0.9])

    def create_network(self, layer_sizes):
        # ... (use NeuralNetwork class from network-architecture.md)
        pass

    def animate_forward_pass(self, network, input_values):
        """Full forward pass animation with signal propagation"""

        # 1. Highlight input values
        input_layer = network.layers[0]
        input_labels = VGroup()

        for i, (neuron, val) in enumerate(zip(input_layer.neurons, input_values)):
            # Show input value
            label = MathTex(f"{val:.1f}", font_size=20)
            label.next_to(neuron, LEFT)
            input_labels.add(label)

            # Activate neuron based on value
            neuron.set_fill(
                interpolate_color("#2a4a7f", "#4af0ff", val),
                opacity=0.3 + 0.7 * val
            )

        self.play(
            *[Write(l) for l in input_labels],
            run_time=0.5
        )
        self.wait(0.3)

        # 2. Propagate through each layer
        for layer_idx in range(len(network.layers) - 1):
            self.animate_layer_to_layer(
                network,
                layer_idx,
                layer_idx + 1
            )

    def animate_layer_to_layer(self, network, from_idx, to_idx):
        """Animate signal from one layer to the next"""

        from_layer = network.layers[from_idx]
        to_layer = network.layers[to_idx]
        connections = network.connections[from_idx]

        # Create pulse effects along connections
        pulses = VGroup()
        pulse_paths = []

        for conn in connections:
            pulse = Dot(color=YELLOW, radius=0.06)
            pulse.move_to(conn.get_start())
            pulses.add(pulse)
            pulse_paths.append(conn)

        self.add(pulses)

        # Animate pulses moving along connections
        self.play(
            *[MoveAlongPath(pulse, path) for pulse, path in zip(pulses, pulse_paths)],
            run_time=0.8,
            rate_func=linear
        )

        # Highlight connections momentarily
        self.play(
            connections.animate.set_stroke(opacity=0.8),
            run_time=0.2
        )

        # Activate target neurons
        activations = [np.random.random() for _ in to_layer.neurons]
        self.play(
            *[n.animate.set_fill(
                interpolate_color("#2a4a7f", "#4af0ff", a),
                opacity=0.3 + 0.7 * a
            ) for n, a in zip(to_layer.neurons, activations)],
            run_time=0.5
        )

        # Fade connections back
        self.play(
            connections.animate.set_stroke(opacity=0.2),
            run_time=0.2
        )

        self.remove(pulses)
        self.wait(0.2)
```

## Signal Pulse Effect

```python
class SignalPulse(VGroup):
    """A glowing pulse that travels along a path"""

    def __init__(self, color=YELLOW, radius=0.08, **kwargs):
        super().__init__(**kwargs)

        # Core dot
        self.core = Dot(radius=radius, color=color)

        # Glow effect
        self.glow = Dot(
            radius=radius * 2,
            color=color,
            fill_opacity=0.3
        )

        self.add(self.glow, self.core)

    def move_along(self, path, scene, run_time=0.5):
        """Animate pulse moving along a path"""
        scene.play(
            MoveAlongPath(self, path),
            run_time=run_time,
            rate_func=smooth
        )
```

## Weighted Sum Visualization

```python
class WeightedSumDemo(Scene):
    def construct(self):
        # Create a single neuron with 3 inputs
        neuron = Circle(radius=0.5, fill_color=BLUE, fill_opacity=0.5)
        neuron.shift(RIGHT * 2)

        # Input neurons
        inputs = VGroup(*[
            Circle(radius=0.3, fill_color=GREEN, fill_opacity=0.7)
            for _ in range(3)
        ])
        inputs.arrange(DOWN, buff=0.8).shift(LEFT * 2)

        # Connections with weights
        weights = [0.5, -0.3, 0.8]
        connections = VGroup()
        weight_labels = VGroup()

        for i, (inp, w) in enumerate(zip(inputs, weights)):
            conn = Line(inp.get_right(), neuron.get_left(),
                       stroke_width=1 + abs(w) * 3,
                       color=GREEN if w > 0 else RED)
            connections.add(conn)

            label = MathTex(f"w_{i+1}={w}", font_size=24)
            label.move_to(conn.get_center() + UP * 0.3)
            weight_labels.add(label)

        # Input values
        input_values = [1.0, 0.5, 0.7]
        input_labels = VGroup(*[
            MathTex(f"x_{i+1}={v}", font_size=20).next_to(inp, LEFT)
            for i, (inp, v) in enumerate(zip(inputs, input_values))
        ])

        # Build scene
        self.play(
            *[GrowFromCenter(inp) for inp in inputs],
            GrowFromCenter(neuron)
        )
        self.play(
            *[Create(c) for c in connections],
            *[Write(l) for l in weight_labels]
        )
        self.play(*[Write(l) for l in input_labels])
        self.wait()

        # Show weighted sum calculation
        weighted_sum = sum(w * x for w, x in zip(weights, input_values))

        equation = MathTex(
            r"\sum_{i} w_i x_i = ",
            f"({weights[0]})(1.0) + ({weights[1]})(0.5) + ({weights[2]})(0.7)",
            f" = {weighted_sum:.2f}"
        )
        equation.scale(0.7).to_edge(DOWN)

        self.play(Write(equation))
        self.wait()

        # Activate neuron based on weighted sum
        activation = 1 / (1 + np.exp(-weighted_sum))
        self.play(
            neuron.animate.set_fill(
                interpolate_color("#2a4a7f", "#4af0ff", activation),
                opacity=0.8
            )
        )
        self.wait()
```

## Matrix Form Animation

```python
class MatrixForwardPass(Scene):
    def construct(self):
        # Show vector-matrix multiplication form
        input_vec = Matrix([[r"x_1"], [r"x_2"], [r"x_3"]], left_bracket="[", right_bracket="]")

        weight_matrix = Matrix([
            [r"w_{11}", r"w_{12}", r"w_{13}"],
            [r"w_{21}", r"w_{22}", r"w_{23}"],
        ], left_bracket="[", right_bracket="]")

        output_vec = Matrix([[r"y_1"], [r"y_2"]], left_bracket="[", right_bracket="]")

        # Arrange equation
        equation = VGroup(
            output_vec,
            MathTex("="),
            weight_matrix,
            input_vec
        ).arrange(RIGHT)

        self.play(Write(equation), run_time=2)
        self.wait()

        # Add activation function
        sigma = MathTex(r"\sigma(")
        sigma_close = MathTex(r")")

        new_equation = VGroup(
            output_vec.copy(),
            MathTex("="),
            sigma,
            weight_matrix.copy(),
            input_vec.copy(),
            sigma_close
        ).arrange(RIGHT)

        self.play(Transform(equation, new_equation))
        self.wait()
```

## Guidelines

- Use yellow/gold color for signal pulses
- Pulse speed: 0.5-1.0 seconds per layer
- Show weighted sum calculation for educational clarity
- Activate neurons sequentially with slight delays (lag_ratio)
- Always visualize the activation function effect

## Forbidden

- Do NOT animate all signals simultaneously (loses clarity)
- Do NOT skip showing intermediate layer activations
- Do NOT use instant teleportation - always animate movement
- Do NOT forget to reset neuron states before new forward pass
