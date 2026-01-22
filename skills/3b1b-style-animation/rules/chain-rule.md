---
name: chain-rule
description: Chain rule animation and derivation for backpropagation
metadata:
  tags: chain-rule, calculus, backpropagation, derivatives
---

# Chain Rule Visualization

## Basic Chain Rule

```python
from manim import *

class ChainRuleBasic(Scene):
    def construct(self):
        # Title
        title = Text("The Chain Rule", font_size=48)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))

        # Function composition visualization
        # y = f(g(x))

        # Create boxes representing functions
        x_box = Rectangle(width=1.5, height=1, color=BLUE)
        x_label = MathTex("x").move_to(x_box)
        x_group = VGroup(x_box, x_label)

        g_box = Rectangle(width=1.5, height=1, color=GREEN)
        g_label = MathTex("g").move_to(g_box)
        g_group = VGroup(g_box, g_label)

        f_box = Rectangle(width=1.5, height=1, color=RED)
        f_label = MathTex("f").move_to(f_box)
        f_group = VGroup(f_box, f_label)

        y_box = Rectangle(width=1.5, height=1, color=YELLOW)
        y_label = MathTex("y").move_to(y_box)
        y_group = VGroup(y_box, y_label)

        # Arrange
        boxes = VGroup(x_group, g_group, f_group, y_group)
        boxes.arrange(RIGHT, buff=0.5)

        # Arrows
        arrows = VGroup(
            Arrow(x_group.get_right(), g_group.get_left(), buff=0.1),
            Arrow(g_group.get_right(), f_group.get_left(), buff=0.1),
            Arrow(f_group.get_right(), y_group.get_left(), buff=0.1),
        )

        # Intermediate labels
        u_label = MathTex("u = g(x)", font_size=24).next_to(arrows[0], UP, buff=0.1)

        self.play(
            *[GrowFromCenter(b) for b in [x_group, g_group, f_group, y_group]],
        )
        self.play(
            *[GrowArrow(a) for a in arrows],
            Write(u_label)
        )
        self.wait()

        # Chain rule equation
        chain_rule = MathTex(
            r"\frac{dy}{dx}",
            r"=",
            r"\frac{dy}{du}",
            r"\cdot",
            r"\frac{du}{dx}"
        )
        chain_rule.shift(DOWN * 2)

        # Color code parts
        chain_rule[0].set_color(YELLOW)  # dy/dx
        chain_rule[2].set_color(RED)     # dy/du (through f)
        chain_rule[4].set_color(GREEN)   # du/dx (through g)

        self.play(Write(chain_rule))
        self.wait()

        # Show the multiplication visually
        brace_f = Brace(f_box, DOWN, color=RED)
        brace_g = Brace(g_box, DOWN, color=GREEN)

        self.play(
            GrowFromCenter(brace_f),
            GrowFromCenter(brace_g)
        )
        self.wait()
```

## Neural Network Chain Rule

```python
class NeuralNetworkChainRule(Scene):
    def construct(self):
        # Simple 3-layer network
        layers = VGroup()
        for i, (name, color) in enumerate([("x", BLUE), ("h", GREEN), ("y", RED)]):
            circle = Circle(radius=0.4, fill_color=color, fill_opacity=0.7)
            label = MathTex(name).move_to(circle)
            group = VGroup(circle, label)
            group.shift(RIGHT * i * 2.5)
            layers.add(group)

        layers.center()

        # Connections with weights
        w1_line = Arrow(layers[0].get_right(), layers[1].get_left(), buff=0.1)
        w1_label = MathTex("w_1", font_size=28).next_to(w1_line, UP, buff=0.1)

        w2_line = Arrow(layers[1].get_right(), layers[2].get_left(), buff=0.1)
        w2_label = MathTex("w_2", font_size=28).next_to(w2_line, UP, buff=0.1)

        network = VGroup(layers, w1_line, w1_label, w2_line, w2_label)
        network.to_edge(UP, buff=1)

        self.play(Create(network))
        self.wait()

        # Forward equations
        forward_eqs = VGroup(
            MathTex(r"h = \sigma(w_1 \cdot x)"),
            MathTex(r"y = \sigma(w_2 \cdot h)"),
            MathTex(r"L = (y - t)^2")
        )
        forward_eqs.arrange(DOWN, aligned_edge=LEFT)
        forward_eqs.shift(LEFT * 3 + DOWN)

        self.play(Write(forward_eqs), run_time=2)
        self.wait()

        # Backpropagation chain
        title = Text("Backpropagation via Chain Rule", font_size=32)
        title.to_edge(DOWN, buff=2)
        self.play(Write(title))

        # dL/dw2
        eq1 = MathTex(
            r"\frac{\partial L}{\partial w_2}",
            r"=",
            r"\frac{\partial L}{\partial y}",
            r"\cdot",
            r"\frac{\partial y}{\partial w_2}"
        )
        eq1.shift(RIGHT * 2 + DOWN * 0.5)

        # dL/dw1 (longer chain)
        eq2 = MathTex(
            r"\frac{\partial L}{\partial w_1}",
            r"=",
            r"\frac{\partial L}{\partial y}",
            r"\cdot",
            r"\frac{\partial y}{\partial h}",
            r"\cdot",
            r"\frac{\partial h}{\partial w_1}"
        )
        eq2.next_to(eq1, DOWN, buff=0.5, aligned_edge=LEFT)

        # Animate with highlighting
        self.play(Write(eq1))
        self.wait()

        # Highlight path in network for eq2
        path_highlight = Arrow(
            layers[2].get_left(),
            layers[0].get_right(),
            color=YELLOW,
            stroke_width=4,
            buff=0.1
        ).set_z_index(-1)

        self.play(
            GrowArrow(path_highlight),
            Write(eq2),
            run_time=1.5
        )
        self.wait()
```

## Computational Graph

```python
class ComputationalGraph(Scene):
    def construct(self):
        # Build computational graph
        nodes = {}

        # Input nodes
        nodes['x'] = self.create_node("x", BLUE).shift(LEFT * 4 + UP * 1.5)
        nodes['w'] = self.create_node("w", BLUE).shift(LEFT * 4 + DOWN * 1.5)

        # Intermediate nodes
        nodes['mult'] = self.create_node(r"\times", GREEN).shift(LEFT * 1.5)
        nodes['sigma'] = self.create_node(r"\sigma", GREEN).shift(RIGHT * 1)
        nodes['loss'] = self.create_node("L", RED).shift(RIGHT * 4)

        # Edges
        edges = VGroup(
            Arrow(nodes['x'].get_right(), nodes['mult'].get_left(), buff=0.1),
            Arrow(nodes['w'].get_right(), nodes['mult'].get_left(), buff=0.1),
            Arrow(nodes['mult'].get_right(), nodes['sigma'].get_left(), buff=0.1),
            Arrow(nodes['sigma'].get_right(), nodes['loss'].get_left(), buff=0.1),
        )

        all_nodes = VGroup(*nodes.values())
        self.play(Create(all_nodes), Create(edges))
        self.wait()

        # Forward pass values
        forward_values = {
            'x': "2",
            'w': "3",
            'mult': "6",
            'sigma': "0.997",
            'loss': "0.003"
        }

        for name, val in forward_values.items():
            label = MathTex(f"= {val}", font_size=20, color=YELLOW)
            label.next_to(nodes[name], DOWN, buff=0.1)
            self.play(Write(label), run_time=0.3)

        self.wait()

        # Backward pass - show gradients flowing back
        self.play(
            edges.animate.set_color(RED),
            run_time=0.5
        )

        # Gradient annotations
        grad_labels = [
            (r"\frac{\partial L}{\partial \sigma}", nodes['sigma']),
            (r"\frac{\partial L}{\partial (\cdot)}", nodes['mult']),
            (r"\frac{\partial L}{\partial w}", nodes['w']),
        ]

        for tex, node in grad_labels:
            label = MathTex(tex, font_size=20, color=RED)
            label.next_to(node, UP, buff=0.3)
            self.play(Write(label), run_time=0.4)

        self.wait()

    def create_node(self, text, color):
        circle = Circle(radius=0.4, fill_color=color, fill_opacity=0.6)
        label = MathTex(text, font_size=28).move_to(circle)
        return VGroup(circle, label)
```

## Guidelines

- Use boxes/circles to represent functions
- Color-code: inputs blue, intermediate green, output red
- Show forward pass first, then backward pass
- Use arrows to indicate direction of computation
- Always show the mathematical equation alongside the graph

## Forbidden

- Do NOT skip showing intermediate variables
- Do NOT use same color for forward and backward passes
- Do NOT show all gradients at once - animate sequentially
- Do NOT forget to label edges with weights/operations
