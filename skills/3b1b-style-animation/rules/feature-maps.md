---
name: feature-maps
description: Feature map visualization in CNNs
metadata:
  tags: feature-map, cnn, activation, channels
---

# Feature Map Visualization

## Single Feature Map

```python
from manim import *
import numpy as np

class FeatureMapDemo(Scene):
    def construct(self):
        # Original "image" representation
        image = Square(side_length=3, fill_color=BLUE, fill_opacity=0.3, stroke_width=2)
        image_label = Text("Input Image", font_size=24).next_to(image, UP)
        image.shift(LEFT * 4)
        image_label.shift(LEFT * 4)

        self.play(Create(image), Write(image_label))

        # Arrow and convolution operation
        arrow1 = Arrow(image.get_right(), ORIGIN + LEFT, color=WHITE)
        conv_label = MathTex(r"\text{Conv}", font_size=24).next_to(arrow1, UP)

        self.play(GrowArrow(arrow1), Write(conv_label))

        # Feature map (smaller, representing detected features)
        feature_map = Square(side_length=2.5, fill_color=GREEN, fill_opacity=0.4, stroke_width=2)
        feature_label = Text("Feature Map", font_size=24).next_to(feature_map, UP)

        self.play(Create(feature_map), Write(feature_label))

        # Show what the feature map detects
        detection_text = Text("Edges / Patterns", font_size=20, color=YELLOW)
        detection_text.next_to(feature_map, DOWN)

        self.play(Write(detection_text))
        self.wait()

        # Visualize activation pattern inside feature map
        # Simulate detected edge pattern
        pattern = VGroup()
        for i in range(5):
            line = Line(
                feature_map.get_corner(UL) + DOWN * 0.4 * i + RIGHT * 0.2,
                feature_map.get_corner(UL) + DOWN * 0.4 * i + RIGHT * 2.3,
                stroke_color=YELLOW,
                stroke_width=2
            )
            pattern.add(line)

        self.play(
            AnimationGroup(*[Create(l) for l in pattern], lag_ratio=0.1),
            run_time=1
        )
        self.wait()
```

## Multiple Feature Maps (Channels)

```python
class MultipleFeatureMaps(Scene):
    def construct(self):
        # Input
        input_img = Square(side_length=2.5, fill_color=BLUE, fill_opacity=0.4)
        input_img.shift(LEFT * 5)
        input_label = Text("Input", font_size=20).next_to(input_img, UP)

        self.play(Create(input_img), Write(input_label))

        # Multiple kernels producing multiple feature maps
        num_filters = 4
        filter_colors = [RED, GREEN, YELLOW, PURPLE]
        filter_names = ["Edges", "Corners", "Textures", "Shapes"]

        feature_maps = VGroup()

        for i in range(num_filters):
            # Create stacked feature map appearance
            fm = Square(
                side_length=2,
                fill_color=filter_colors[i],
                fill_opacity=0.5,
                stroke_width=2
            )
            fm.shift(RIGHT * 3 + UP * (1.5 - i) * 0.3 + RIGHT * i * 0.2)
            feature_maps.add(fm)

        # Arrows from input to each feature map
        arrows = VGroup()
        for fm in feature_maps:
            arrow = Arrow(
                input_img.get_right(),
                fm.get_left(),
                color=WHITE,
                stroke_width=1
            )
            arrows.add(arrow)

        self.play(
            *[GrowArrow(a) for a in arrows],
            run_time=0.5
        )

        self.play(
            AnimationGroup(
                *[Create(fm) for fm in feature_maps],
                lag_ratio=0.2
            ),
            run_time=1
        )

        # Label showing number of channels
        channel_label = MathTex(r"\text{4 channels}", font_size=24)
        channel_label.next_to(feature_maps, UP, buff=0.5)
        self.play(Write(channel_label))

        # Show what each detects
        for i, (fm, name) in enumerate(zip(feature_maps, filter_names)):
            label = Text(name, font_size=14, color=filter_colors[i])
            label.next_to(fm, RIGHT, buff=0.1)
            self.play(Write(label), run_time=0.3)

        self.wait()
```

## Feature Map Progression Through Layers

```python
class FeatureMapProgression(Scene):
    def construct(self):
        # Show how feature maps change through layers

        title = Text("Feature Hierarchy in CNN", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Layer representations
        layers_info = [
            ("Input", (224, 224, 3), BLUE),
            ("Conv1", (112, 112, 64), GREEN),
            ("Conv2", (56, 56, 128), YELLOW),
            ("Conv3", (28, 28, 256), ORANGE),
            ("Conv4", (14, 14, 512), RED),
        ]

        layer_groups = VGroup()

        for i, (name, (h, w, c), color) in enumerate(layers_info):
            # Size proportional representation
            scale = 0.015
            rect_h = h * scale
            rect_w = w * scale

            # Stack to show channels
            stack = VGroup()
            num_shown = min(3, c // 32)  # Show representative slices

            for j in range(num_shown):
                slice_rect = Rectangle(
                    width=rect_w,
                    height=rect_h,
                    fill_color=color,
                    fill_opacity=0.6 - j * 0.15,
                    stroke_width=1
                )
                slice_rect.shift(UP * j * 0.1 + RIGHT * j * 0.1)
                stack.add(slice_rect)

            # Size label
            size_label = Text(f"{h}x{w}x{c}", font_size=12)
            size_label.next_to(stack, DOWN, buff=0.2)

            # Layer name
            name_label = Text(name, font_size=16)
            name_label.next_to(stack, UP, buff=0.2)

            group = VGroup(stack, size_label, name_label)
            layer_groups.add(group)

        layer_groups.arrange(RIGHT, buff=0.5)
        layer_groups.shift(DOWN * 0.5)

        # Animate layer by layer
        for i, group in enumerate(layer_groups):
            self.play(Create(group), run_time=0.5)

            if i > 0:
                # Arrow from previous layer
                prev_group = layer_groups[i - 1]
                arrow = Arrow(
                    prev_group.get_right() + LEFT * 0.1,
                    group.get_left() + RIGHT * 0.1,
                    color=WHITE,
                    stroke_width=2,
                    buff=0.1
                )
                self.play(GrowArrow(arrow), run_time=0.3)

        self.wait()

        # Annotations about what each layer detects
        annotations = [
            "Pixels",
            "Edges, Colors",
            "Textures, Patterns",
            "Object Parts",
            "Objects"
        ]

        for group, ann in zip(layer_groups, annotations):
            label = Text(ann, font_size=10, color=GRAY)
            label.next_to(group, DOWN, buff=0.5)
            self.play(Write(label), run_time=0.3)

        self.wait()
```

## Activation Heatmap

```python
class ActivationHeatmap(Scene):
    def construct(self):
        # Simulate feature map activation as heatmap

        # Create grid representing feature map
        grid_size = 7
        cell_size = 0.5

        # Generate activation values (simulated)
        np.random.seed(42)
        activations = np.random.rand(grid_size, grid_size)
        # Add a "hot spot" for detected feature
        activations[2:5, 2:5] += 0.5
        activations = np.clip(activations, 0, 1)

        grid = VGroup()
        for i in range(grid_size):
            for j in range(grid_size):
                val = activations[i, j]
                cell = Square(
                    side_length=cell_size,
                    fill_color=interpolate_color(BLUE_E, RED, val),
                    fill_opacity=0.8,
                    stroke_width=0.5
                )
                cell.shift(RIGHT * j * cell_size + DOWN * i * cell_size)
                grid.add(cell)

        grid.move_to(ORIGIN)

        title = Text("Feature Map Activation", font_size=28)
        title.to_edge(UP)

        self.play(Write(title))
        self.play(
            AnimationGroup(
                *[FadeIn(cell) for cell in grid],
                lag_ratio=0.02
            ),
            run_time=2
        )

        # Color bar legend
        color_bar = VGroup()
        for i in range(10):
            segment = Rectangle(
                width=0.3,
                height=0.3,
                fill_color=interpolate_color(BLUE_E, RED, i / 9),
                fill_opacity=0.8,
                stroke_width=0
            )
            color_bar.add(segment)

        color_bar.arrange(RIGHT, buff=0)
        color_bar.next_to(grid, DOWN, buff=0.5)

        low_label = Text("Low", font_size=14).next_to(color_bar, LEFT)
        high_label = Text("High", font_size=14).next_to(color_bar, RIGHT)

        self.play(Create(color_bar), Write(low_label), Write(high_label))

        # Highlight detected region
        highlight = Square(
            side_length=cell_size * 3,
            stroke_color=YELLOW,
            stroke_width=3,
            fill_opacity=0
        )
        highlight.move_to(grid[2 * grid_size + 2].get_center())
        highlight.shift(RIGHT * cell_size + DOWN * cell_size)

        detected_label = Text("Detected Feature", font_size=16, color=YELLOW)
        detected_label.next_to(highlight, RIGHT, buff=0.3)

        self.play(Create(highlight), Write(detected_label))
        self.wait()
```

## Guidelines

- Use color intensity to represent activation strength
- Show channel stacking with slight offset for 3D effect
- Include size labels (HxWxC) for each feature map
- Demonstrate feature hierarchy (edges → textures → parts → objects)
- Use heatmaps for detailed activation visualization

## Forbidden

- Do NOT show all channels individually (use representative slices)
- Do NOT use uniform colors - always show activation variation
- Do NOT forget dimension labels
- Do NOT skip showing the progression through layers
