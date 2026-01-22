---
name: convolution
description: Convolution operation animation for CNNs
metadata:
  tags: convolution, cnn, kernel, filter
---

# Convolution Operation Visualization

## Basic 2D Convolution

```python
from manim import *
import numpy as np

class ConvolutionDemo(Scene):
    def construct(self):
        # Input image (5x5 grid)
        input_size = 5
        input_data = np.random.randint(0, 10, (input_size, input_size))

        input_grid = self.create_grid(input_data, cell_size=0.6, color=BLUE)
        input_label = Text("Input", font_size=24).next_to(input_grid, UP)
        input_group = VGroup(input_grid, input_label)
        input_group.shift(LEFT * 3)

        # Kernel (3x3)
        kernel = np.array([
            [1, 0, -1],
            [2, 0, -2],
            [1, 0, -1]
        ])  # Sobel edge detector

        kernel_grid = self.create_grid(kernel, cell_size=0.5, color=YELLOW)
        kernel_label = Text("Kernel", font_size=24).next_to(kernel_grid, UP)
        kernel_group = VGroup(kernel_grid, kernel_label)

        # Output (3x3 for valid padding)
        output_size = input_size - 2
        output_grid = self.create_empty_grid(output_size, cell_size=0.6, color=GREEN)
        output_label = Text("Output", font_size=24).next_to(output_grid, UP)
        output_group = VGroup(output_grid, output_label)
        output_group.shift(RIGHT * 3)

        self.play(Create(input_group))
        self.play(Create(kernel_group))
        self.play(Create(output_group))
        self.wait()

        # Animate convolution sliding
        for i in range(output_size):
            for j in range(output_size):
                # Highlight kernel position on input
                highlight = Square(
                    side_length=0.6 * 3,
                    stroke_color=YELLOW,
                    stroke_width=4,
                    fill_opacity=0.2,
                    fill_color=YELLOW
                )
                highlight.move_to(input_grid[0][0].get_center())
                highlight.shift(RIGHT * j * 0.6 + DOWN * i * 0.6)
                highlight.shift(RIGHT * 0.6 + DOWN * 0.6)  # Center offset

                self.play(FadeIn(highlight), run_time=0.2)

                # Calculate convolution value
                conv_value = 0
                for ki in range(3):
                    for kj in range(3):
                        conv_value += input_data[i + ki, j + kj] * kernel[ki, kj]

                # Show calculation
                calc_text = MathTex(f"= {conv_value}", font_size=24, color=GREEN)
                calc_text.to_edge(DOWN)
                self.play(Write(calc_text), run_time=0.2)

                # Fill output cell
                output_cell = output_grid[i][j]
                output_cell.set_fill(GREEN, opacity=0.7)
                cell_value = MathTex(str(conv_value), font_size=18)
                cell_value.move_to(output_cell)

                self.play(
                    FadeIn(cell_value),
                    FadeOut(highlight),
                    FadeOut(calc_text),
                    run_time=0.2
                )

        self.wait()

    def create_grid(self, data, cell_size, color):
        rows, cols = data.shape
        grid = VGroup()

        for i in range(rows):
            row = VGroup()
            for j in range(cols):
                cell = Square(side_length=cell_size, stroke_color=color)
                cell.shift(RIGHT * j * cell_size + DOWN * i * cell_size)
                value = MathTex(str(data[i, j]), font_size=16)
                value.move_to(cell)
                row.add(VGroup(cell, value))
            grid.add(row)

        grid.move_to(ORIGIN)
        return grid

    def create_empty_grid(self, size, cell_size, color):
        grid = VGroup()
        for i in range(size):
            row = VGroup()
            for j in range(size):
                cell = Square(side_length=cell_size, stroke_color=color)
                cell.shift(RIGHT * j * cell_size + DOWN * i * cell_size)
                row.add(cell)
            grid.add(row)
        grid.move_to(ORIGIN)
        return grid
```

## Kernel Sliding Animation

```python
class KernelSliding(Scene):
    def construct(self):
        # Simplified visualization focusing on the sliding window

        # Input representation
        input_rect = Rectangle(width=4, height=4, color=BLUE, fill_opacity=0.3)
        input_label = Text("Input Image", font_size=20).next_to(input_rect, UP)

        # Kernel (smaller rectangle)
        kernel = Square(side_length=1.5, color=YELLOW, fill_opacity=0.5, stroke_width=3)
        kernel.move_to(input_rect.get_corner(UL) + RIGHT * 0.75 + DOWN * 0.75)

        self.play(Create(input_rect), Write(input_label))
        self.play(Create(kernel))

        # Output dot that appears as kernel moves
        output_dots = VGroup()
        output_rect = Rectangle(width=2.5, height=2.5, color=GREEN, fill_opacity=0.1)
        output_rect.shift(RIGHT * 4)
        output_label = Text("Feature Map", font_size=20).next_to(output_rect, UP)

        self.play(Create(output_rect), Write(output_label))

        # Stride animation
        positions = []
        stride = 1.0

        for i in range(3):  # rows
            for j in range(3):  # cols
                # Kernel position on input
                new_pos = input_rect.get_corner(UL) + RIGHT * (0.75 + j * stride) + DOWN * (0.75 + i * stride)
                positions.append(new_pos)

                # Output dot position
                output_pos = output_rect.get_corner(UL) + RIGHT * (0.4 + j * 0.8) + DOWN * (0.4 + i * 0.8)

                self.play(
                    kernel.animate.move_to(new_pos),
                    run_time=0.3
                )

                # Create output dot
                dot = Dot(output_pos, color=GREEN, radius=0.15)
                self.play(GrowFromCenter(dot), run_time=0.2)
                output_dots.add(dot)

        self.wait()

        # Show stride=2 effect
        stride_text = Text("Stride = 2", font_size=24, color=YELLOW)
        stride_text.to_edge(DOWN)
        self.play(Write(stride_text))

        # Reset and show stride 2
        self.play(FadeOut(output_dots))

        stride = 2.0
        for i in range(2):
            for j in range(2):
                new_pos = input_rect.get_corner(UL) + RIGHT * (0.75 + j * stride) + DOWN * (0.75 + i * stride)

                self.play(
                    kernel.animate.move_to(new_pos),
                    run_time=0.4
                )

                output_pos = output_rect.get_corner(UL) + RIGHT * (0.6 + j * 1.0) + DOWN * (0.6 + i * 1.0)
                dot = Dot(output_pos, color=YELLOW, radius=0.2)
                self.play(GrowFromCenter(dot), run_time=0.2)

        self.wait()
```

## Multiple Channel Convolution

```python
class MultiChannelConv(Scene):
    def construct(self):
        # RGB input (3 channels)
        channels = VGroup()
        colors = [RED, GREEN, BLUE]
        labels = ["R", "G", "B"]

        for i, (color, label) in enumerate(zip(colors, labels)):
            channel = Square(side_length=2, fill_color=color, fill_opacity=0.5)
            channel.shift(LEFT * 4 + UP * (1 - i) * 0.3 + RIGHT * i * 0.3)
            ch_label = Text(label, font_size=20).move_to(channel)
            channels.add(VGroup(channel, ch_label))

        input_label = Text("Input (3 channels)", font_size=20)
        input_label.next_to(channels, UP, buff=0.5)

        self.play(Create(channels), Write(input_label))

        # 3D kernel representation
        kernel_3d = VGroup()
        for i in range(3):
            k = Square(side_length=0.8, stroke_color=YELLOW, stroke_width=2)
            k.shift(UP * (1 - i) * 0.15 + RIGHT * i * 0.15)
            kernel_3d.add(k)

        kernel_label = Text("3x3x3 Kernel", font_size=18)
        kernel_label.next_to(kernel_3d, UP)

        self.play(Create(kernel_3d), Write(kernel_label))

        # Arrow to output
        arrow = Arrow(kernel_3d.get_right(), RIGHT * 2, color=WHITE)
        self.play(GrowArrow(arrow))

        # Single output channel
        output = Square(side_length=1.5, fill_color=PURPLE, fill_opacity=0.6)
        output.shift(RIGHT * 3.5)
        output_label = Text("Feature Map", font_size=18).next_to(output, UP)

        self.play(Create(output), Write(output_label))

        # Equation
        equation = MathTex(
            r"\text{Output} = \sum_{c=1}^{3} (\text{Input}_c * \text{Kernel}_c)",
            font_size=24
        )
        equation.to_edge(DOWN)
        self.play(Write(equation))
        self.wait()
```

## Edge Detection Example

```python
class EdgeDetection(Scene):
    def construct(self):
        # Show different kernels and their effects

        kernels = {
            "Horizontal": np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]),
            "Vertical": np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]),
            "Sobel X": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
        }

        title = Text("Edge Detection Kernels", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        kernel_displays = VGroup()
        for i, (name, kernel) in enumerate(kernels.items()):
            # Create kernel visualization
            grid = self.create_kernel_grid(kernel)
            label = Text(name, font_size=20).next_to(grid, UP)
            group = VGroup(grid, label)
            kernel_displays.add(group)

        kernel_displays.arrange(RIGHT, buff=1)
        self.play(Create(kernel_displays), run_time=2)
        self.wait()

    def create_kernel_grid(self, kernel):
        grid = VGroup()
        for i in range(3):
            for j in range(3):
                val = kernel[i, j]
                cell = Square(side_length=0.5)

                # Color based on value
                if val > 0:
                    cell.set_fill(GREEN, opacity=abs(val) / 2)
                elif val < 0:
                    cell.set_fill(RED, opacity=abs(val) / 2)
                else:
                    cell.set_fill(GRAY, opacity=0.2)

                cell.shift(RIGHT * j * 0.5 + DOWN * i * 0.5)

                text = MathTex(str(val), font_size=14)
                text.move_to(cell)

                grid.add(VGroup(cell, text))

        grid.move_to(ORIGIN)
        return grid
```

## Guidelines

- Show the kernel sliding over the input clearly
- Use color coding: input (blue), kernel (yellow), output (green)
- Animate element-wise multiplication and summation
- Show stride effects by comparing different stride values
- For RGB, stack channels visually in 3D-like arrangement

## Forbidden

- Do NOT skip the sliding animation - it's key to understanding
- Do NOT use same colors for input and kernel
- Do NOT animate too fast - viewers need time to follow
- Do NOT forget to show the mathematical operation
