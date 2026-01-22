---
name: matrix-operations
description: Matrix multiplication and operations visualization
metadata:
  tags: matrix, multiplication, linear-algebra, visualization
---

# Matrix Operations Visualization

## Matrix-Vector Product

```python
from manim import *
import numpy as np

class MatrixVectorProduct(Scene):
    def construct(self):
        # Matrix A (2x3)
        A = np.array([[1, 2, 3], [4, 5, 6]])

        # Vector v (3x1)
        v = np.array([[1], [2], [1]])

        # Create matrix mobject
        matrix_mob = Matrix(A, left_bracket="[", right_bracket="]")
        vector_mob = Matrix(v, left_bracket="[", right_bracket="]")

        # Arrange
        matrix_mob.shift(LEFT * 2)
        vector_mob.next_to(matrix_mob, RIGHT, buff=0.5)

        self.play(Write(matrix_mob), Write(vector_mob))
        self.wait()

        # Animate row-by-row multiplication
        result_entries = []
        for i, row in enumerate(matrix_mob.get_rows()):
            # Highlight row
            row_rect = SurroundingRectangle(row, color=YELLOW, buff=0.1)
            self.play(Create(row_rect), run_time=0.3)

            # Calculate dot product
            dot_product = sum(A[i, j] * v[j, 0] for j in range(3))
            result_entries.append(dot_product)

            # Show calculation
            calc = MathTex(
                f"{A[i,0]} \\cdot {v[0,0]} + {A[i,1]} \\cdot {v[1,0]} + {A[i,2]} \\cdot {v[2,0]} = {dot_product}",
                font_size=24
            )
            calc.to_edge(DOWN)
            self.play(Write(calc), run_time=0.5)
            self.wait(0.3)

            self.play(FadeOut(row_rect), FadeOut(calc), run_time=0.2)

        # Show result vector
        result_mob = Matrix([[e] for e in result_entries], left_bracket="[", right_bracket="]")
        result_mob.set_color(GREEN)
        equals = MathTex("=").next_to(vector_mob, RIGHT)
        result_mob.next_to(equals, RIGHT)

        self.play(Write(equals), Write(result_mob))
        self.wait()
```

## Matrix-Matrix Product

```python
class MatrixMatrixProduct(Scene):
    def construct(self):
        # A (2x3) @ B (3x2) = C (2x2)
        A = np.array([[1, 2, 3], [4, 5, 6]])
        B = np.array([[7, 8], [9, 10], [11, 12]])

        A_mob = Matrix(A, left_bracket="[", right_bracket="]")
        B_mob = Matrix(B, left_bracket="[", right_bracket="]")

        A_mob.shift(LEFT * 3)
        B_mob.next_to(A_mob, RIGHT, buff=1)

        self.play(Write(A_mob), Write(B_mob))

        # Result placeholder
        C = A @ B
        C_mob = Matrix(
            [["?", "?"], ["?", "?"]],
            left_bracket="[", right_bracket="]"
        )
        equals = MathTex("=").next_to(B_mob, RIGHT)
        C_mob.next_to(equals, RIGHT)
        C_mob.set_color(GREEN)

        self.play(Write(equals), Write(C_mob))
        self.wait()

        # Animate each entry computation
        for i in range(2):
            for j in range(2):
                # Highlight row of A
                row_rect = SurroundingRectangle(
                    A_mob.get_rows()[i],
                    color=YELLOW, buff=0.1
                )

                # Highlight column of B
                col_entries = [B_mob.get_entries()[k * 2 + j] for k in range(3)]
                col_rect = SurroundingRectangle(
                    VGroup(*col_entries),
                    color=BLUE, buff=0.1
                )

                self.play(Create(row_rect), Create(col_rect), run_time=0.3)

                # Update result entry
                result_entry = C_mob.get_entries()[i * 2 + j]
                new_value = MathTex(str(C[i, j]))
                new_value.move_to(result_entry)

                self.play(Transform(result_entry, new_value), run_time=0.3)
                self.play(FadeOut(row_rect), FadeOut(col_rect), run_time=0.2)

        self.wait()
```

## Colored Weight Matrix (3b1b style)

```python
class ColoredMatrixVisualization(Scene):
    def construct(self):
        # Weight matrix with positive/negative coloring
        weights = np.random.randn(4, 5) * 0.5

        matrix_vis = self.create_colored_matrix(weights)
        self.play(Create(matrix_vis), run_time=2)

        # Add color legend
        legend = VGroup(
            VGroup(Square(0.3, fill_color=BLUE, fill_opacity=0.8), Text("Positive", font_size=16)),
            VGroup(Square(0.3, fill_color=RED, fill_opacity=0.8), Text("Negative", font_size=16)),
        )
        for item in legend:
            item.arrange(RIGHT, buff=0.2)
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UR)

        self.play(Create(legend))
        self.wait()

    def create_colored_matrix(self, matrix, cell_size=0.6):
        rows, cols = matrix.shape
        grid = VGroup()

        for i in range(rows):
            for j in range(cols):
                val = matrix[i, j]

                # Color based on sign and magnitude
                if val >= 0:
                    color = interpolate_color(GRAY, BLUE, min(abs(val) * 2, 1))
                else:
                    color = interpolate_color(GRAY, RED, min(abs(val) * 2, 1))

                cell = Square(
                    side_length=cell_size,
                    fill_color=color,
                    fill_opacity=0.8,
                    stroke_width=1
                )
                cell.shift(RIGHT * j * cell_size + DOWN * i * cell_size)

                # Value label
                label = MathTex(f"{val:.2f}", font_size=14)
                label.move_to(cell)

                grid.add(VGroup(cell, label))

        grid.center()
        return grid
```

## Matrix Transpose Animation

```python
class MatrixTranspose(Scene):
    def construct(self):
        A = np.array([[1, 2, 3], [4, 5, 6]])

        A_mob = self.create_colored_grid(A)
        A_mob.shift(LEFT * 2)

        A_label = MathTex("A").next_to(A_mob, UP)

        self.play(Create(A_mob), Write(A_label))
        self.wait()

        # Create transpose positions
        A_T = A.T
        A_T_mob = self.create_colored_grid(A_T)
        A_T_mob.shift(RIGHT * 2)

        A_T_label = MathTex("A^T").next_to(A_T_mob, UP)

        # Animate elements moving to transposed positions
        original_cells = list(A_mob)
        animations = []

        for i in range(2):
            for j in range(3):
                original_idx = i * 3 + j
                target_idx = j * 2 + i

                original_cell = original_cells[original_idx].copy()
                target_pos = A_T_mob[target_idx].get_center()

                animations.append(
                    original_cell.animate.move_to(target_pos)
                )

        self.play(
            *animations,
            Write(A_T_label),
            run_time=2
        )
        self.wait()

    def create_colored_grid(self, matrix, cell_size=0.6):
        # Similar to create_colored_matrix
        pass
```

## Guidelines

- Use row highlighting for matrix-vector products
- Color code positive (blue) and negative (red) values
- Animate one computation at a time
- Show intermediate calculations
- Use consistent cell sizes across matrices

## Forbidden

- Do NOT show all multiplications simultaneously
- Do NOT use same color for all matrix entries
- Do NOT skip showing dimension matching
- Do NOT forget to label matrices (A, B, C, etc.)
