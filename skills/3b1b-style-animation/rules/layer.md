---
name: layer
description: Neural network layer representation and connections
metadata:
  tags: layer, neural-network, connections, visualization
---

# Layer Visualization

## Basic Layer Structure

A layer is a vertical arrangement of neurons with proper spacing.

```python
from manim import *

class NeuralLayer(VGroup):
    def __init__(
        self,
        num_neurons,
        neuron_radius=0.25,
        neuron_spacing=0.8,
        layer_color="#4a9eff",
        **kwargs
    ):
        super().__init__(**kwargs)

        self.neurons = VGroup()
        self.num_neurons = num_neurons

        # Calculate vertical positions
        total_height = (num_neurons - 1) * neuron_spacing
        start_y = total_height / 2

        for i in range(num_neurons):
            neuron = Circle(
                radius=neuron_radius,
                fill_color=layer_color,
                fill_opacity=0.8,
                stroke_color=WHITE,
                stroke_width=2
            )
            neuron.move_to(UP * (start_y - i * neuron_spacing))
            self.neurons.add(neuron)

        self.add(self.neurons)

    def get_neuron(self, index):
        return self.neurons[index]

    def get_neuron_centers(self):
        return [n.get_center() for n in self.neurons]
```

## Layer with Labels

```python
class LabeledLayer(VGroup):
    def __init__(self, num_neurons, label_text, layer_color="#4a9eff", **kwargs):
        super().__init__(**kwargs)

        self.layer = NeuralLayer(num_neurons, layer_color=layer_color)
        self.add(self.layer)

        # Layer label below
        self.label = Text(label_text, font_size=24, color=WHITE)
        self.label.next_to(self.layer, DOWN, buff=0.5)
        self.add(self.label)
```

## Connections Between Layers

```python
class LayerConnections(VGroup):
    def __init__(self, layer1, layer2, weights=None, **kwargs):
        super().__init__(**kwargs)

        self.connections = VGroup()
        num_from = layer1.num_neurons
        num_to = layer2.num_neurons

        for i in range(num_from):
            for j in range(num_to):
                # Get weight for this connection
                if weights is not None:
                    weight = weights[j][i]
                else:
                    weight = 0.5

                # Color based on weight sign and magnitude
                if weight >= 0:
                    color = interpolate_color(WHITE, GREEN, min(abs(weight), 1))
                else:
                    color = interpolate_color(WHITE, RED, min(abs(weight), 1))

                line = Line(
                    layer1.get_neuron(i).get_right(),
                    layer2.get_neuron(j).get_left(),
                    stroke_color=color,
                    stroke_width=0.5 + abs(weight) * 2,
                    stroke_opacity=0.3 + abs(weight) * 0.5
                )
                self.connections.add(line)

        self.add(self.connections)
```

## Layer Animation Patterns

### Layer Appearance

```python
def animate_layer_creation(scene, layer):
    """Animate neurons appearing one by one"""
    scene.play(
        AnimationGroup(
            *[GrowFromCenter(n) for n in layer.neurons],
            lag_ratio=0.1
        ),
        run_time=1
    )
```

### Layer Activation Wave

```python
def animate_layer_activation(scene, layer, activations):
    """Animate activation spreading through layer"""
    animations = []
    for neuron, activation in zip(layer.neurons, activations):
        new_color = interpolate_color("#2a4a7f", "#4af0ff", activation)
        animations.append(
            neuron.animate.set_fill(new_color, opacity=0.3 + 0.7 * activation)
        )

    scene.play(
        AnimationGroup(*animations, lag_ratio=0.05),
        run_time=0.8
    )
```

### Connection Drawing

```python
def animate_connections(scene, connections):
    """Draw connections between layers"""
    scene.play(
        AnimationGroup(
            *[Create(c) for c in connections.connections],
            lag_ratio=0.01
        ),
        run_time=1.5
    )
```

## Handling Large Layers

For layers with many neurons (>10), use ellipsis pattern:

```python
class CompactLayer(VGroup):
    def __init__(self, num_neurons, max_visible=5, **kwargs):
        super().__init__(**kwargs)

        if num_neurons <= max_visible:
            # Show all neurons
            self.layer = NeuralLayer(num_neurons)
        else:
            # Show first few, ellipsis, last few
            visible = max_visible - 1
            top_neurons = visible // 2 + 1
            bottom_neurons = visible - top_neurons

            self.neurons = VGroup()

            # Top neurons
            for i in range(top_neurons):
                n = Circle(radius=0.25, fill_color="#4a9eff", fill_opacity=0.8)
                n.move_to(UP * (2 - i * 0.8))
                self.neurons.add(n)

            # Ellipsis dots
            dots = VGroup(*[Dot() for _ in range(3)])
            dots.arrange(DOWN, buff=0.15)
            dots.move_to(ORIGIN)
            self.add(dots)

            # Bottom neurons
            for i in range(bottom_neurons):
                n = Circle(radius=0.25, fill_color="#4a9eff", fill_opacity=0.8)
                n.move_to(DOWN * (1.2 + i * 0.8))
                self.neurons.add(n)

            self.add(self.neurons)

        # Label showing actual count
        self.count_label = Text(f"({num_neurons})", font_size=20)
        self.count_label.next_to(self, RIGHT, buff=0.3)
        self.add(self.count_label)
```

## Guidelines

- Standard neuron spacing: 0.7-1.0 units
- Layer horizontal spacing: 2.5-3.5 units
- Maximum visible neurons per layer: 8-10 (use ellipsis for more)
- Connection opacity: scale with weight magnitude
- Always add labels for layer identification

## Forbidden

- Do NOT show all neurons for layers > 10 (use CompactLayer)
- Do NOT use uniform connection colors (visualize weight values)
- Do NOT skip connection animations for initial network reveal
- Do NOT overlap neurons within a layer
