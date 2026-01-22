---
name: neuron
description: Single neuron visualization with weights, bias, and activation
metadata:
  tags: neuron, neural-network, visualization, weights, bias
---

# Neuron Visualization

## Basic Neuron Structure

A neuron is visualized as a circle with incoming connections (weights) and an outgoing connection.

```python
from manim import *

class Neuron(VGroup):
    def __init__(
        self,
        radius=0.3,
        fill_color="#4a9eff",
        stroke_color=WHITE,
        activation=0.0,
        **kwargs
    ):
        super().__init__(**kwargs)

        # Main body
        self.body = Circle(
            radius=radius,
            fill_color=fill_color,
            fill_opacity=0.8,
            stroke_color=stroke_color,
            stroke_width=2
        )
        self.add(self.body)

        # Activation indicator (inner glow)
        self.activation_value = activation
        self.update_activation(activation)

    def update_activation(self, value):
        """Update visual based on activation value [0, 1]"""
        self.activation_value = value
        # Brighter fill for higher activation
        new_color = interpolate_color("#2a4a7f", "#4af0ff", value)
        self.body.set_fill(new_color, opacity=0.3 + 0.7 * value)

    def get_input_point(self):
        return self.body.get_left()

    def get_output_point(self):
        return self.body.get_right()
```

## Neuron with Label

```python
class LabeledNeuron(VGroup):
    def __init__(self, label_text="", **kwargs):
        super().__init__(**kwargs)

        self.neuron = Neuron()
        self.add(self.neuron)

        if label_text:
            self.label = MathTex(label_text, font_size=24)
            self.label.move_to(self.neuron)
            self.add(self.label)
```

## Neuron Creation Animation

```python
class NeuronDemo(Scene):
    def construct(self):
        neuron = Neuron()

        # Dramatic entrance
        self.play(
            GrowFromCenter(neuron.body),
            run_time=0.8
        )
        self.wait(0.5)

        # Show activation change
        for activation in [0.3, 0.7, 1.0, 0.5]:
            self.play(
                neuron.body.animate.set_fill(
                    interpolate_color("#2a4a7f", "#4af0ff", activation),
                    opacity=0.3 + 0.7 * activation
                ),
                run_time=0.5
            )
            self.wait(0.3)
```

## Weighted Input Visualization

```python
class NeuronWithInputs(VGroup):
    def __init__(self, num_inputs=3, **kwargs):
        super().__init__(**kwargs)

        self.neuron = Neuron()
        self.inputs = VGroup()
        self.weights = []
        self.connections = VGroup()

        # Create input dots
        for i in range(num_inputs):
            input_dot = Dot(color=WHITE, radius=0.1)
            input_dot.move_to(LEFT * 2 + UP * (1 - i))
            self.inputs.add(input_dot)

            # Connection line
            connection = Line(
                input_dot.get_center(),
                self.neuron.get_input_point(),
                stroke_width=2,
                stroke_opacity=0.6
            )
            self.connections.add(connection)
            self.weights.append(0.5)

        self.add(self.inputs, self.connections, self.neuron)

    def animate_forward_pass(self, scene, input_values):
        """Animate data flowing through weights to neuron"""
        pulses = []
        for i, (val, conn) in enumerate(zip(input_values, self.connections)):
            pulse = Dot(color=YELLOW, radius=0.08)
            pulse.move_to(conn.get_start())
            pulses.append(pulse)

        scene.play(*[FadeIn(p) for p in pulses])
        scene.play(
            *[p.animate.move_to(c.get_end()) for p, c in zip(pulses, self.connections)],
            run_time=0.8
        )
        scene.play(*[FadeOut(p) for p in pulses])

        # Update neuron activation
        weighted_sum = sum(v * w for v, w in zip(input_values, self.weights))
        activation = 1 / (1 + np.exp(-weighted_sum))  # Sigmoid
        scene.play(
            self.neuron.body.animate.set_fill(
                interpolate_color("#2a4a7f", "#4af0ff", activation),
                opacity=0.5 + 0.5 * activation
            ),
            run_time=0.5
        )
```

## Bias Visualization

```python
class NeuronWithBias(Neuron):
    def __init__(self, bias=0.0, show_bias=True, **kwargs):
        super().__init__(**kwargs)
        self.bias = bias

        if show_bias:
            # Small indicator for bias
            self.bias_indicator = MathTex(
                f"+{bias:.1f}" if bias >= 0 else f"{bias:.1f}",
                font_size=16,
                color=YELLOW
            )
            self.bias_indicator.next_to(self.body, DOWN, buff=0.1)
            self.add(self.bias_indicator)
```

## Guidelines

- Neuron radius: 0.2-0.4 depending on network complexity
- Use consistent sizing across all neurons in a network
- Activation visualization: darker = inactive, brighter = active
- Always show activation changes with smooth animations

## Forbidden

- Do NOT use rectangles for neurons (circles are standard)
- Do NOT make neurons too small (< 0.15 radius) - illegible
- Do NOT skip activation visualization in forward pass animations
- Do NOT use harsh color transitions - always interpolate
