---
name: attention
description: Self-attention mechanism visualization for transformers
metadata:
  tags: attention, transformer, self-attention, nlp
---

# Attention Mechanism Visualization

## Self-Attention Overview

```python
from manim import *
import numpy as np

class SelfAttentionDemo(Scene):
    def construct(self):
        title = Text("Self-Attention Mechanism", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Input sequence (tokens)
        tokens = ["The", "cat", "sat", "on", "mat"]
        token_boxes = VGroup()

        for i, token in enumerate(tokens):
            box = Rectangle(width=1, height=0.6, fill_color=BLUE, fill_opacity=0.5)
            label = Text(token, font_size=18)
            label.move_to(box)
            token_group = VGroup(box, label)
            token_boxes.add(token_group)

        token_boxes.arrange(RIGHT, buff=0.3)
        token_boxes.shift(UP * 1.5)

        self.play(Create(token_boxes))
        self.wait()

        # Show attention from "cat" to all other tokens
        source_idx = 1  # "cat"
        source = token_boxes[source_idx]

        # Highlight source
        self.play(source[0].animate.set_fill(YELLOW, opacity=0.8))

        # Attention weights (example)
        attention_weights = [0.1, 0.3, 0.4, 0.15, 0.05]

        # Draw attention arrows
        arrows = VGroup()
        weight_labels = VGroup()

        for i, (target, weight) in enumerate(zip(token_boxes, attention_weights)):
            if i != source_idx:
                arrow = Arrow(
                    source.get_bottom(),
                    target.get_top(),
                    color=interpolate_color(GRAY, RED, weight * 2),
                    stroke_width=1 + weight * 5,
                    buff=0.1
                )
                arrows.add(arrow)

                # Weight label
                w_label = MathTex(f"{weight:.2f}", font_size=16)
                w_label.next_to(arrow, UP if i < source_idx else DOWN, buff=0.05)
                weight_labels.add(w_label)

        self.play(
            AnimationGroup(*[GrowArrow(a) for a in arrows], lag_ratio=0.1),
            run_time=1
        )
        self.play(
            AnimationGroup(*[Write(l) for l in weight_labels], lag_ratio=0.1),
            run_time=0.8
        )

        self.wait()
```

## Query-Key-Value Visualization

```python
class QKVVisualization(Scene):
    def construct(self):
        # Single token transformation to Q, K, V

        # Input embedding
        input_box = Rectangle(width=1.5, height=3, fill_color=BLUE, fill_opacity=0.5)
        input_label = Text("x", font_size=24).move_to(input_box)
        input_group = VGroup(input_box, input_label)
        input_group.shift(LEFT * 4)

        self.play(Create(input_group))

        # Weight matrices
        w_q = Rectangle(width=1, height=1, fill_color=RED, fill_opacity=0.5)
        w_k = Rectangle(width=1, height=1, fill_color=GREEN, fill_opacity=0.5)
        w_v = Rectangle(width=1, height=1, fill_color=PURPLE, fill_opacity=0.5)

        w_q_label = MathTex("W_Q", font_size=20).move_to(w_q)
        w_k_label = MathTex("W_K", font_size=20).move_to(w_k)
        w_v_label = MathTex("W_V", font_size=20).move_to(w_v)

        weights = VGroup(
            VGroup(w_q, w_q_label),
            VGroup(w_k, w_k_label),
            VGroup(w_v, w_v_label)
        )
        weights.arrange(DOWN, buff=0.5)
        weights.shift(LEFT * 1)

        self.play(Create(weights))

        # Arrows from input to weights
        arrows_in = VGroup()
        for w in weights:
            arrow = Arrow(input_box.get_right(), w.get_left(), buff=0.1, color=WHITE)
            arrows_in.add(arrow)

        self.play(*[GrowArrow(a) for a in arrows_in])

        # Output Q, K, V
        q_box = Rectangle(width=1.2, height=2.5, fill_color=RED, fill_opacity=0.5)
        k_box = Rectangle(width=1.2, height=2.5, fill_color=GREEN, fill_opacity=0.5)
        v_box = Rectangle(width=1.2, height=2.5, fill_color=PURPLE, fill_opacity=0.5)

        q_label = MathTex("Q", font_size=24).move_to(q_box)
        k_label = MathTex("K", font_size=24).move_to(k_box)
        v_label = MathTex("V", font_size=24).move_to(v_box)

        outputs = VGroup(
            VGroup(q_box, q_label),
            VGroup(k_box, k_label),
            VGroup(v_box, v_label)
        )
        outputs.arrange(DOWN, buff=0.3)
        outputs.shift(RIGHT * 2.5)

        # Arrows from weights to outputs
        arrows_out = VGroup()
        for w, o in zip(weights, outputs):
            arrow = Arrow(w.get_right(), o.get_left(), buff=0.1, color=WHITE)
            arrows_out.add(arrow)

        self.play(*[GrowArrow(a) for a in arrows_out], Create(outputs))

        # Equation
        equation = MathTex(
            r"Q = xW_Q, \quad K = xW_K, \quad V = xW_V",
            font_size=28
        )
        equation.to_edge(DOWN)
        self.play(Write(equation))
        self.wait()
```

## Attention Score Computation

```python
class AttentionScoreMatrix(Scene):
    def construct(self):
        title = Text("Attention Scores", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # Q and K^T matrices
        q_matrix = Matrix([
            ["q_1"],
            ["q_2"],
            ["q_3"],
        ], left_bracket="[", right_bracket="]")
        q_label = MathTex("Q").next_to(q_matrix, UP)
        q_group = VGroup(q_matrix, q_label)
        q_group.shift(LEFT * 4)

        k_matrix = Matrix([
            ["k_1", "k_2", "k_3"],
        ], left_bracket="[", right_bracket="]")
        k_label = MathTex("K^T").next_to(k_matrix, UP)
        k_group = VGroup(k_matrix, k_label)
        k_group.shift(LEFT * 1)

        self.play(Create(q_group), Create(k_group))

        # Multiplication sign
        times = MathTex(r"\times").next_to(q_matrix, RIGHT, buff=0.3)
        self.play(Write(times))

        # Result: attention scores
        scores = Matrix([
            ["s_{11}", "s_{12}", "s_{13}"],
            ["s_{21}", "s_{22}", "s_{23}"],
            ["s_{31}", "s_{32}", "s_{33}"],
        ], left_bracket="[", right_bracket="]")
        scores.shift(RIGHT * 3)

        equals = MathTex("=").next_to(k_matrix, RIGHT, buff=0.3)

        self.play(Write(equals), Create(scores))

        # Show softmax
        softmax_eq = MathTex(
            r"\text{Attention} = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V",
            font_size=28
        )
        softmax_eq.to_edge(DOWN)
        self.play(Write(softmax_eq))
        self.wait()

        # Highlight diagonal for self-attention
        diag_highlight = VGroup()
        for i in range(3):
            entry = scores.get_entries()[i * 3 + i]
            highlight = SurroundingRectangle(entry, color=YELLOW, buff=0.05)
            diag_highlight.add(highlight)

        self.play(Create(diag_highlight))

        diag_label = Text("Self-attention", font_size=20, color=YELLOW)
        diag_label.next_to(scores, RIGHT)
        self.play(Write(diag_label))
        self.wait()
```

## Attention Heatmap

```python
class AttentionHeatmap(Scene):
    def construct(self):
        # Visualize attention weights as heatmap

        tokens = ["I", "love", "machine", "learning"]
        n = len(tokens)

        # Simulated attention weights
        np.random.seed(42)
        weights = np.random.rand(n, n)
        weights = weights / weights.sum(axis=1, keepdims=True)  # Softmax-like

        # Create grid
        cell_size = 0.8
        grid = VGroup()

        for i in range(n):
            for j in range(n):
                cell = Square(
                    side_length=cell_size,
                    fill_color=interpolate_color(BLUE_E, RED, weights[i, j]),
                    fill_opacity=0.8,
                    stroke_width=1
                )
                cell.shift(RIGHT * j * cell_size + DOWN * i * cell_size)

                # Weight value
                val_text = MathTex(f"{weights[i,j]:.2f}", font_size=14, color=WHITE)
                val_text.move_to(cell)
                grid.add(VGroup(cell, val_text))

        grid.move_to(ORIGIN)

        # Row labels (query tokens)
        row_labels = VGroup()
        for i, token in enumerate(tokens):
            label = Text(token, font_size=16)
            label.next_to(grid[i * n], LEFT, buff=0.2)
            row_labels.add(label)

        # Column labels (key tokens)
        col_labels = VGroup()
        for j, token in enumerate(tokens):
            label = Text(token, font_size=16)
            label.next_to(grid[j], UP, buff=0.2)
            col_labels.add(label)

        # Title
        title = Text("Attention Weights Heatmap", font_size=28)
        title.to_edge(UP)

        query_label = Text("Query", font_size=16, color=GRAY)
        query_label.next_to(row_labels, LEFT, buff=0.5)

        key_label = Text("Key", font_size=16, color=GRAY)
        key_label.next_to(col_labels, UP, buff=0.3)

        self.play(Write(title))
        self.play(Create(grid), run_time=2)
        self.play(Write(row_labels), Write(col_labels))
        self.play(Write(query_label), Write(key_label))
        self.wait()
```

## Guidelines

- Use color intensity to show attention weight magnitude
- Animate attention flow with arrows from query to keys
- Show Q, K, V transformations step by step
- Use heatmaps for multi-token attention patterns
- Highlight self-attention (diagonal) when relevant

## Forbidden

- Do NOT show all attention connections simultaneously (overwhelming)
- Do NOT use uniform arrow thickness - scale by weight
- Do NOT skip the softmax normalization concept
- Do NOT forget to explain d_k scaling
