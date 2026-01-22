---
name: network-architecture
description: Full neural network layout and structure visualization
metadata:
  tags: neural-network, architecture, layout, mlp
---

# Network Architecture Visualization

## Complete Network Class

```python
from manim import *
import numpy as np

class NeuralNetwork(VGroup):
    def __init__(
        self,
        layer_sizes,  # e.g., [784, 128, 64, 10]
        layer_colors=None,
        max_neurons_per_layer=8,
        layer_spacing=3.0,
        neuron_radius=0.25,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes)

        # Default colors: input blue, hidden purple, output green
        if layer_colors is None:
            layer_colors = self._default_colors()

        # Create layers
        self.layers = VGroup()
        self.connections = VGroup()

        total_width = (self.num_layers - 1) * layer_spacing
        start_x = -total_width / 2

        for i, (size, color) in enumerate(zip(layer_sizes, layer_colors)):
            layer = self._create_layer(
                size, max_neurons_per_layer, neuron_radius, color
            )
            layer.move_to(RIGHT * (start_x + i * layer_spacing))
            self.layers.add(layer)

        # Create connections between adjacent layers
        for i in range(len(self.layers) - 1):
            conns = self._create_connections(self.layers[i], self.layers[i + 1])
            self.connections.add(conns)

        self.add(self.connections, self.layers)

    def _default_colors(self):
        colors = ["#60a5fa"]  # Input: blue
        for _ in range(self.num_layers - 2):
            colors.append("#a78bfa")  # Hidden: purple
        colors.append("#34d399")  # Output: green
        return colors

    def _create_layer(self, num_neurons, max_visible, radius, color):
        """Create a layer with optional ellipsis for large layers"""
        layer = VGroup()
        layer.num_neurons = num_neurons

        if num_neurons <= max_visible:
            visible_count = num_neurons
            show_ellipsis = False
        else:
            visible_count = max_visible - 1
            show_ellipsis = True

        # Calculate spacing
        spacing = min(0.8, 6 / visible_count)
        total_height = (visible_count - 1) * spacing
        start_y = total_height / 2

        neurons = VGroup()

        if show_ellipsis:
            top_count = visible_count // 2 + 1
            bottom_count = visible_count - top_count

            # Top neurons
            for i in range(top_count):
                n = Circle(radius=radius, fill_color=color, fill_opacity=0.8,
                          stroke_color=WHITE, stroke_width=2)
                n.move_to(UP * (start_y - i * spacing))
                neurons.add(n)

            # Ellipsis
            dots = VGroup(*[Dot(radius=0.05) for _ in range(3)])
            dots.arrange(DOWN, buff=0.15)
            layer.add(dots)

            # Bottom neurons
            for i in range(bottom_count):
                n = Circle(radius=radius, fill_color=color, fill_opacity=0.8,
                          stroke_color=WHITE, stroke_width=2)
                n.move_to(DOWN * (start_y - (visible_count - 1 - bottom_count + i) * spacing) * -1)
                n.move_to(DOWN * (1.5 + i * spacing))
                neurons.add(n)
        else:
            for i in range(num_neurons):
                n = Circle(radius=radius, fill_color=color, fill_opacity=0.8,
                          stroke_color=WHITE, stroke_width=2)
                n.move_to(UP * (start_y - i * spacing))
                neurons.add(n)

        layer.neurons = neurons
        layer.add(neurons)
        return layer

    def _create_connections(self, layer1, layer2):
        """Create connection lines between two layers"""
        connections = VGroup()

        for n1 in layer1.neurons:
            for n2 in layer2.neurons:
                line = Line(
                    n1.get_right(),
                    n2.get_left(),
                    stroke_color=WHITE,
                    stroke_width=0.5,
                    stroke_opacity=0.2
                )
                connections.add(line)

        return connections

    def get_layer(self, index):
        return self.layers[index]
```

## Network Creation Animation

```python
class NetworkCreationDemo(Scene):
    def construct(self):
        # Create network
        network = NeuralNetwork([4, 8, 6, 3])

        # Title
        title = Text("Fully Connected Neural Network", font_size=36)
        title.to_edge(UP)

        self.play(Write(title))
        self.wait(0.5)

        # Animate layers appearing left to right
        for i, layer in enumerate(network.layers):
            self.play(
                AnimationGroup(
                    *[GrowFromCenter(n) for n in layer.neurons],
                    lag_ratio=0.1
                ),
                run_time=0.8
            )

            # Draw connections to this layer (if not first)
            if i > 0:
                self.play(
                    Create(network.connections[i - 1]),
                    run_time=0.5
                )

        self.wait()

        # Add layer labels
        labels = ["Input", "Hidden 1", "Hidden 2", "Output"]
        label_group = VGroup()
        for layer, text in zip(network.layers, labels):
            label = Text(text, font_size=20)
            label.next_to(layer, DOWN, buff=0.5)
            label_group.add(label)

        self.play(
            AnimationGroup(*[Write(l) for l in label_group], lag_ratio=0.2)
        )
        self.wait()
```

## Forward Pass Animation

```python
def animate_forward_pass(self, scene, network, input_values):
    """Animate data flowing through the network"""

    # Activate input layer
    input_layer = network.get_layer(0)
    scene.play(
        AnimationGroup(
            *[n.animate.set_fill("#4af0ff", opacity=0.9)
              for n, v in zip(input_layer.neurons, input_values) if v > 0.5],
            lag_ratio=0.05
        ),
        run_time=0.5
    )

    # Flow through each subsequent layer
    for i in range(len(network.layers) - 1):
        # Create flowing dots
        flow_dots = VGroup()
        for n1 in network.layers[i].neurons:
            dot = Dot(color=YELLOW, radius=0.05)
            dot.move_to(n1.get_right())
            flow_dots.add(dot)

        scene.add(flow_dots)

        # Move dots to next layer
        scene.play(
            AnimationGroup(
                *[d.animate.move_to(n2.get_left())
                  for d, n2 in zip(flow_dots, network.layers[i + 1].neurons)],
                lag_ratio=0.02
            ),
            run_time=0.6
        )

        # Activate next layer neurons
        scene.play(
            AnimationGroup(
                *[n.animate.set_fill("#4af0ff", opacity=0.7)
                  for n in network.layers[i + 1].neurons],
                lag_ratio=0.05
            ),
            run_time=0.3
        )

        scene.remove(flow_dots)

    scene.wait(0.5)
```

## Network with Size Labels

```python
class LabeledNetwork(VGroup):
    def __init__(self, layer_sizes, **kwargs):
        super().__init__(**kwargs)

        self.network = NeuralNetwork(layer_sizes)
        self.add(self.network)

        # Add size labels
        self.size_labels = VGroup()
        for layer, size in zip(self.network.layers, layer_sizes):
            label = MathTex(str(size), font_size=28)
            label.next_to(layer, UP, buff=0.3)
            self.size_labels.add(label)

        self.add(self.size_labels)
```

## Guidelines

- Maximum layers visible: 6-7 (use abstraction for deeper networks)
- Layer spacing: proportional to complexity being explained
- Always show layer sizes for educational context
- Use distinct colors for input, hidden, and output layers
- Connection density: reduce opacity for clarity

## Forbidden

- Do NOT show fully connected network with more than 100 visible connections
- Do NOT use same color for all layers
- Do NOT animate all connections simultaneously for large networks
- Do NOT forget to label layer sizes
- Do NOT make network too wide for screen (scale appropriately)
