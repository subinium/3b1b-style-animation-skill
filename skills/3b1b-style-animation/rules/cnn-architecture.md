---
name: cnn-architecture
description: Full CNN structure visualization
metadata:
  tags: cnn, architecture, layers, classification
---

# CNN Architecture Visualization

## Complete CNN Structure

```python
from manim import *
import numpy as np

class CNNArchitecture(Scene):
    def construct(self):
        title = Text("Convolutional Neural Network", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Layer specifications
        layers = [
            {"type": "input", "size": (32, 32, 3), "color": BLUE, "name": "Input"},
            {"type": "conv", "size": (30, 30, 32), "color": GREEN, "name": "Conv1"},
            {"type": "pool", "size": (15, 15, 32), "color": TEAL, "name": "Pool1"},
            {"type": "conv", "size": (13, 13, 64), "color": GREEN, "name": "Conv2"},
            {"type": "pool", "size": (6, 6, 64), "color": TEAL, "name": "Pool2"},
            {"type": "flatten", "size": (2304,), "color": ORANGE, "name": "Flatten"},
            {"type": "fc", "size": (128,), "color": PURPLE, "name": "FC1"},
            {"type": "fc", "size": (10,), "color": RED, "name": "Output"},
        ]

        layer_objects = VGroup()

        for i, layer in enumerate(layers):
            if layer["type"] in ["conv", "pool", "input"]:
                obj = self.create_feature_map_stack(
                    layer["size"],
                    layer["color"],
                    layer["name"]
                )
            elif layer["type"] == "flatten":
                obj = self.create_flatten_repr(layer["color"], layer["name"])
            else:  # fc
                obj = self.create_fc_layer(
                    layer["size"][0],
                    layer["color"],
                    layer["name"]
                )

            layer_objects.add(obj)

        layer_objects.arrange(RIGHT, buff=0.3)
        layer_objects.scale(0.9)
        layer_objects.shift(DOWN * 0.5)

        # Animate layer by layer
        for i, obj in enumerate(layer_objects):
            self.play(Create(obj), run_time=0.4)

            if i > 0:
                # Connection arrow
                prev = layer_objects[i - 1]
                curr = obj
                arrow = Arrow(
                    prev.get_right(),
                    curr.get_left(),
                    color=WHITE,
                    stroke_width=2,
                    buff=0.1,
                    max_stroke_width_to_length_ratio=10
                )
                self.play(GrowArrow(arrow), run_time=0.2)

        self.wait()

        # Add operation labels
        operation_labels = VGroup(
            Text("3x3 Conv", font_size=10),
            Text("2x2 MaxPool", font_size=10),
            Text("3x3 Conv", font_size=10),
            Text("2x2 MaxPool", font_size=10),
            Text("", font_size=10),  # flatten
            Text("ReLU", font_size=10),
            Text("Softmax", font_size=10),
        )

        for label, obj in zip(operation_labels, layer_objects[1:]):
            label.next_to(obj, UP, buff=0.1)
            label.set_color(GRAY)

        self.play(
            AnimationGroup(*[Write(l) for l in operation_labels], lag_ratio=0.1)
        )
        self.wait()

    def create_feature_map_stack(self, size, color, name):
        """Create 3D-looking stack of feature maps"""
        h, w, c = size
        scale = 0.02

        stack = VGroup()
        num_slices = min(4, max(1, c // 16))

        for i in range(num_slices):
            rect = Rectangle(
                width=w * scale,
                height=h * scale,
                fill_color=color,
                fill_opacity=0.6 - i * 0.1,
                stroke_width=1
            )
            rect.shift(UP * i * 0.08 + RIGHT * i * 0.08)
            stack.add(rect)

        # Size label
        size_label = Text(f"{h}x{w}x{c}", font_size=10)
        size_label.next_to(stack, DOWN, buff=0.15)

        # Name label
        name_label = Text(name, font_size=12)
        name_label.next_to(size_label, DOWN, buff=0.05)

        return VGroup(stack, size_label, name_label)

    def create_flatten_repr(self, color, name):
        """Create flatten layer representation"""
        rect = Rectangle(
            width=0.2,
            height=1.5,
            fill_color=color,
            fill_opacity=0.6,
            stroke_width=1
        )

        label = Text(name, font_size=12)
        label.next_to(rect, DOWN, buff=0.1)

        return VGroup(rect, label)

    def create_fc_layer(self, num_neurons, color, name):
        """Create fully connected layer representation"""
        max_shown = min(8, num_neurons)

        neurons = VGroup()
        for i in range(max_shown):
            neuron = Circle(
                radius=0.1,
                fill_color=color,
                fill_opacity=0.7,
                stroke_width=1
            )
            neurons.add(neuron)

        neurons.arrange(DOWN, buff=0.1)

        if num_neurons > max_shown:
            dots = VGroup(*[Dot(radius=0.02) for _ in range(3)])
            dots.arrange(DOWN, buff=0.05)
            dots.move_to(neurons.get_center())
            neurons = VGroup(neurons[:3], dots, neurons[-3:])
            neurons.arrange(DOWN, buff=0.05)

        label = Text(f"{name}\n({num_neurons})", font_size=10)
        label.next_to(neurons, DOWN, buff=0.1)

        return VGroup(neurons, label)
```

## CNN Forward Pass Animation

```python
class CNNForwardPass(Scene):
    def construct(self):
        # Simplified CNN showing data transformation

        # Input image
        input_img = ImageMobject("path/to/image.png")  # Or create synthetic
        input_img.scale(0.5)
        input_img.shift(LEFT * 5)

        # If no image, create colored grid
        input_grid = self.create_image_grid()
        input_grid.shift(LEFT * 5)

        self.play(Create(input_grid))

        # Conv layer - show kernel sliding
        conv_output = self.create_feature_maps(4, GREEN)
        conv_output.shift(LEFT * 2)

        self.play(
            input_grid.animate.scale(0.8),
            Create(conv_output),
            run_time=1
        )

        # Pool layer
        pool_output = self.create_feature_maps(4, TEAL, scale=0.7)
        pool_output.shift(RIGHT * 1)

        self.play(Create(pool_output))

        # Flatten
        flatten = Rectangle(width=0.3, height=2, fill_color=ORANGE, fill_opacity=0.6)
        flatten.shift(RIGHT * 3)

        self.play(
            conv_output.animate.scale(0.5).shift(UP * 0.5),
            pool_output.animate.scale(0.5).shift(UP * 0.5),
            Create(flatten)
        )

        # FC output
        output = VGroup(*[
            Circle(radius=0.15, fill_color=RED if i == 3 else GRAY, fill_opacity=0.7)
            for i in range(5)
        ])
        output.arrange(DOWN, buff=0.2)
        output.shift(RIGHT * 5)

        labels = ["Cat", "Dog", "Bird", "Fish", "Car"]
        for circle, label in zip(output, labels):
            text = Text(label, font_size=12)
            text.next_to(circle, RIGHT, buff=0.1)
            circle.add(text)

        self.play(Create(output))

        # Highlight prediction
        pred_box = SurroundingRectangle(output[3], color=GREEN, buff=0.1)
        self.play(Create(pred_box))

        pred_text = Text("Prediction: Fish", font_size=24, color=GREEN)
        pred_text.to_edge(DOWN)
        self.play(Write(pred_text))
        self.wait()

    def create_image_grid(self):
        """Create synthetic image representation"""
        grid = VGroup()
        np.random.seed(42)

        for i in range(8):
            for j in range(8):
                color = interpolate_color(BLUE, RED, np.random.random())
                cell = Square(
                    side_length=0.15,
                    fill_color=color,
                    fill_opacity=0.8,
                    stroke_width=0
                )
                cell.shift(RIGHT * j * 0.15 + DOWN * i * 0.15)
                grid.add(cell)

        grid.move_to(ORIGIN)
        return grid

    def create_feature_maps(self, num_maps, color, scale=1.0):
        maps = VGroup()
        for i in range(num_maps):
            rect = Rectangle(
                width=0.8 * scale,
                height=0.8 * scale,
                fill_color=color,
                fill_opacity=0.5 - i * 0.1,
                stroke_width=1
            )
            rect.shift(UP * i * 0.1 + RIGHT * i * 0.1)
            maps.add(rect)
        return maps
```

## LeNet-5 Architecture

```python
class LeNet5(Scene):
    def construct(self):
        title = Text("LeNet-5 Architecture", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Classic LeNet-5 layers
        architecture = [
            ("Input", "32x32x1", BLUE),
            ("C1: Conv", "28x28x6", GREEN),
            ("S2: Pool", "14x14x6", TEAL),
            ("C3: Conv", "10x10x16", GREEN),
            ("S4: Pool", "5x5x16", TEAL),
            ("C5: Conv", "1x1x120", GREEN),
            ("F6: FC", "84", PURPLE),
            ("Output", "10", RED),
        ]

        layers = VGroup()

        for name, size, color in architecture:
            layer = self.create_layer_block(name, size, color)
            layers.add(layer)

        layers.arrange(RIGHT, buff=0.2)
        layers.scale(0.8)

        self.play(Create(layers), run_time=3)
        self.wait()

    def create_layer_block(self, name, size, color):
        if "x" in size and size.count("x") == 2:
            # Feature map
            parts = size.split("x")
            h, w, c = int(parts[0]), int(parts[1]), int(parts[2])
            scale = 0.03
            block = Rectangle(
                width=w * scale,
                height=h * scale,
                fill_color=color,
                fill_opacity=0.6
            )
        else:
            # FC layer
            num = int(size)
            block = Rectangle(
                width=0.3,
                height=min(2, num * 0.02),
                fill_color=color,
                fill_opacity=0.6
            )

        name_label = Text(name, font_size=10)
        name_label.next_to(block, UP, buff=0.1)

        size_label = Text(size, font_size=8, color=GRAY)
        size_label.next_to(block, DOWN, buff=0.05)

        return VGroup(block, name_label, size_label)
```

## Guidelines

- Show layer progression from left to right
- Use distinct colors for different layer types (conv, pool, fc)
- Display dimensions at each layer
- Animate data flow through the network
- Include operation labels (kernel size, stride)

## Forbidden

- Do NOT overcrowd the visualization with too many details
- Do NOT use same color for all layer types
- Do NOT skip dimension labels
- Do NOT forget to show the classification output clearly
