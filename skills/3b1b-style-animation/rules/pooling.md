---
name: pooling
description: Max/Average pooling animations
metadata:
  tags: pooling, max-pooling, average-pooling, downsampling
---

# Pooling Layer Visualization

## Max Pooling

```python
from manim import *
import numpy as np

class MaxPoolingDemo(Scene):
    def construct(self):
        title = Text("Max Pooling (2x2, stride=2)", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Input feature map (4x4)
        input_data = np.array([
            [1, 3, 2, 4],
            [5, 6, 7, 8],
            [3, 2, 1, 0],
            [1, 2, 3, 4]
        ])

        input_grid = self.create_grid(input_data, cell_size=0.7, color=BLUE)
        input_label = Text("Input (4x4)", font_size=20).next_to(input_grid, DOWN)
        input_group = VGroup(input_grid, input_label)
        input_group.shift(LEFT * 3)

        # Output (2x2)
        output_grid = self.create_empty_grid(2, cell_size=0.7, color=GREEN)
        output_label = Text("Output (2x2)", font_size=20).next_to(output_grid, DOWN)
        output_group = VGroup(output_grid, output_label)
        output_group.shift(RIGHT * 3)

        self.play(Create(input_group), Create(output_group))

        # Pooling regions (2x2 windows)
        regions = [
            ((0, 0), (0, 1, 4, 5)),   # Top-left
            ((0, 1), (2, 3, 6, 7)),   # Top-right
            ((1, 0), (8, 9, 12, 13)), # Bottom-left
            ((1, 1), (10, 11, 14, 15)) # Bottom-right
        ]

        flat_input = input_data.flatten()

        for (out_i, out_j), indices in regions:
            # Highlight pooling region
            region_cells = [input_grid[idx // 4][idx % 4] for idx in indices]
            highlight = SurroundingRectangle(
                VGroup(*[c[0] for c in region_cells]),
                color=YELLOW,
                buff=0.05,
                stroke_width=3
            )

            self.play(Create(highlight), run_time=0.3)

            # Find max value
            values = [flat_input[idx] for idx in indices]
            max_val = max(values)
            max_idx = indices[values.index(max_val)]

            # Highlight max cell
            max_cell = input_grid[max_idx // 4][max_idx % 4]
            self.play(
                max_cell[0].animate.set_fill(RED, opacity=0.7),
                run_time=0.3
            )

            # Show max value moving to output
            max_text = MathTex(str(max_val), font_size=24, color=RED)
            max_text.move_to(max_cell)

            output_cell = output_grid[out_i][out_j]
            output_text = MathTex(str(max_val), font_size=24).move_to(output_cell)

            self.play(
                max_text.animate.move_to(output_cell),
                output_cell.animate.set_fill(GREEN, opacity=0.6),
                run_time=0.4
            )

            self.play(
                FadeOut(highlight),
                max_cell[0].animate.set_fill(BLUE, opacity=0.3),
                FadeIn(output_text),
                FadeOut(max_text),
                run_time=0.3
            )

        self.wait()

        # Summary
        summary = MathTex(
            r"\text{Max Pool: } 4 \times 4 \rightarrow 2 \times 2",
            font_size=28
        )
        summary.to_edge(DOWN, buff=0.5)
        self.play(Write(summary))
        self.wait()

    def create_grid(self, data, cell_size, color):
        rows, cols = data.shape
        grid = VGroup()

        for i in range(rows):
            row = VGroup()
            for j in range(cols):
                cell = Square(
                    side_length=cell_size,
                    fill_color=color,
                    fill_opacity=0.3,
                    stroke_color=color
                )
                cell.shift(RIGHT * j * cell_size + DOWN * i * cell_size)
                value = MathTex(str(data[i, j]), font_size=18)
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
                cell = Square(
                    side_length=cell_size,
                    stroke_color=color,
                    fill_opacity=0
                )
                cell.shift(RIGHT * j * cell_size + DOWN * i * cell_size)
                row.add(cell)
            grid.add(row)
        grid.move_to(ORIGIN)
        return grid
```

## Average Pooling

```python
class AveragePoolingDemo(Scene):
    def construct(self):
        title = Text("Average Pooling (2x2, stride=2)", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Input (4x4)
        input_data = np.array([
            [4, 2, 6, 8],
            [2, 4, 2, 4],
            [8, 6, 4, 2],
            [6, 8, 2, 4]
        ])

        input_grid = self.create_grid(input_data, 0.6, BLUE)
        input_grid.shift(LEFT * 3)

        output_grid = self.create_empty_grid(2, 0.6, GREEN)
        output_grid.shift(RIGHT * 3)

        self.play(Create(input_grid), Create(output_grid))

        # Process each 2x2 region
        regions = [
            ((0, 0), [0, 1, 4, 5]),
            ((0, 1), [2, 3, 6, 7]),
            ((1, 0), [8, 9, 12, 13]),
            ((1, 1), [10, 11, 14, 15])
        ]

        flat_input = input_data.flatten()

        for (out_i, out_j), indices in regions:
            # Highlight region
            highlight = Rectangle(
                width=0.6 * 2,
                height=0.6 * 2,
                stroke_color=YELLOW,
                stroke_width=3
            )
            center_x = (indices[0] % 4 + indices[1] % 4) / 2 * 0.6
            center_y = (indices[0] // 4 + indices[2] // 4) / 2 * 0.6
            highlight.move_to(input_grid[0][0][0].get_center())
            highlight.shift(RIGHT * center_x + DOWN * center_y + RIGHT * 0.3 + DOWN * 0.3)

            self.play(Create(highlight), run_time=0.3)

            # Calculate average
            values = [flat_input[idx] for idx in indices]
            avg_val = sum(values) / len(values)

            # Show calculation
            calc = MathTex(
                f"\\frac{{{values[0]}+{values[1]}+{values[2]}+{values[3]}}}{{4}} = {avg_val:.1f}",
                font_size=20
            )
            calc.to_edge(DOWN, buff=1)
            self.play(Write(calc), run_time=0.5)

            # Fill output
            output_cell = output_grid[out_i][out_j]
            output_text = MathTex(f"{avg_val:.0f}", font_size=20)
            output_text.move_to(output_cell)

            self.play(
                output_cell.animate.set_fill(GREEN, opacity=0.6),
                FadeIn(output_text),
                run_time=0.3
            )

            self.play(FadeOut(highlight), FadeOut(calc), run_time=0.2)

        self.wait()

    # ... (same helper methods as above)
```

## Pooling Comparison

```python
class PoolingComparison(Scene):
    def construct(self):
        # Side by side comparison

        title = Text("Max vs Average Pooling", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Same input for both
        input_data = np.array([
            [1, 9],
            [2, 3]
        ])

        # Max pooling result
        max_result = 9
        max_label = Text("Max Pooling", font_size=24, color=RED)

        max_grid = self.create_small_grid(input_data, RED)
        max_arrow = Arrow(ORIGIN, RIGHT, color=RED)
        max_output = Square(side_length=0.6, fill_color=RED, fill_opacity=0.5)
        max_output_text = MathTex("9", font_size=24).move_to(max_output)

        max_group = VGroup(max_grid, max_arrow, max_output, max_output_text)
        max_group.arrange(RIGHT, buff=0.5)
        max_label.next_to(max_group, UP)
        max_full = VGroup(max_label, max_group)

        # Average pooling result
        avg_result = 3.75
        avg_label = Text("Average Pooling", font_size=24, color=GREEN)

        avg_grid = self.create_small_grid(input_data, GREEN)
        avg_arrow = Arrow(ORIGIN, RIGHT, color=GREEN)
        avg_output = Square(side_length=0.6, fill_color=GREEN, fill_opacity=0.5)
        avg_output_text = MathTex("3.75", font_size=20).move_to(avg_output)

        avg_group = VGroup(avg_grid, avg_arrow, avg_output, avg_output_text)
        avg_group.arrange(RIGHT, buff=0.5)
        avg_label.next_to(avg_group, UP)
        avg_full = VGroup(avg_label, avg_group)

        # Arrange
        comparison = VGroup(max_full, avg_full)
        comparison.arrange(DOWN, buff=1)

        self.play(Create(comparison), run_time=2)
        self.wait()

        # Highlight difference
        diff_text = Text(
            "Max: preserves strongest feature\nAvg: smooths activation",
            font_size=18,
            color=YELLOW
        )
        diff_text.to_edge(DOWN)
        self.play(Write(diff_text))
        self.wait()

    def create_small_grid(self, data, color):
        grid = VGroup()
        for i in range(2):
            for j in range(2):
                cell = Square(side_length=0.5, stroke_color=color, fill_opacity=0.2, fill_color=color)
                cell.shift(RIGHT * j * 0.5 + DOWN * i * 0.5)
                text = MathTex(str(data[i, j]), font_size=16)
                text.move_to(cell)
                grid.add(VGroup(cell, text))
        return grid
```

## Guidelines

- Clearly show the pooling window moving over the input
- Highlight which value is selected (max) or show calculation (average)
- Use color coding: input (blue), selected value (red for max), output (green)
- Show dimensionality reduction (4x4 → 2x2)
- Compare max vs average pooling effects

## Forbidden

- Do NOT skip showing the selection/calculation process
- Do NOT use same color for all stages
- Do NOT forget stride visualization
- Do NOT animate too quickly - pooling concept needs clarity
