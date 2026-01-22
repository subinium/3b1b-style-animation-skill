---
name: activation-functions
description: Visualizing activation functions (ReLU, Sigmoid, Tanh, etc.)
metadata:
  tags: activation, relu, sigmoid, tanh, visualization
---

# Activation Function Visualization

## Activation Function Graphs

```python
from manim import *
import numpy as np

class ActivationFunctions(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=8,
            y_length=5,
            axis_config={"include_tip": True, "color": WHITE}
        )

        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        self.play(Create(axes), Write(labels))
        self.wait()

        # Sigmoid
        sigmoid = axes.plot(
            lambda x: 1 / (1 + np.exp(-x)),
            color="#3b82f6",
            x_range=[-4, 4]
        )
        sigmoid_label = MathTex(r"\sigma(x) = \frac{1}{1+e^{-x}}", color="#3b82f6")
        sigmoid_label.to_corner(UR)

        self.play(Create(sigmoid), Write(sigmoid_label))
        self.wait()
```

## Individual Activation Functions

### Sigmoid

```python
def create_sigmoid_visualization(self):
    axes = Axes(x_range=[-5, 5], y_range=[-0.5, 1.5], x_length=6, y_length=4)

    # The function
    sigmoid_graph = axes.plot(
        lambda x: 1 / (1 + np.exp(-x)),
        color=BLUE
    )

    # Key points
    midpoint = Dot(axes.c2p(0, 0.5), color=YELLOW)
    midpoint_label = MathTex(r"(0, 0.5)").next_to(midpoint, UR, buff=0.1)

    # Asymptotes
    upper_asymptote = DashedLine(
        axes.c2p(-5, 1), axes.c2p(5, 1),
        color=GRAY, stroke_width=2
    )
    lower_asymptote = DashedLine(
        axes.c2p(-5, 0), axes.c2p(5, 0),
        color=GRAY, stroke_width=2
    )

    # Equation
    equation = MathTex(r"\sigma(x) = \frac{1}{1 + e^{-x}}", color=YELLOW)
    equation.to_corner(UR)

    return VGroup(axes, sigmoid_graph, midpoint, upper_asymptote, lower_asymptote, equation)
```

### ReLU

```python
def create_relu_visualization(self):
    axes = Axes(x_range=[-3, 3], y_range=[-1, 3], x_length=6, y_length=4)

    # ReLU function (piecewise)
    relu_left = axes.plot(lambda x: 0, color=GREEN, x_range=[-3, 0])
    relu_right = axes.plot(lambda x: x, color=GREEN, x_range=[0, 3])

    # Highlight the kink point
    kink = Dot(axes.c2p(0, 0), color=YELLOW, radius=0.1)

    # Equation
    equation = MathTex(r"\text{ReLU}(x) = \max(0, x)", color=YELLOW)
    equation.to_corner(UR)

    # Annotation for "dead region"
    dead_region = axes.get_area(relu_left, color=RED, opacity=0.2)
    dead_label = Text("Dead Region", font_size=20, color=RED)
    dead_label.move_to(axes.c2p(-1.5, 0.5))

    return VGroup(axes, relu_left, relu_right, kink, equation)
```

### Tanh

```python
def create_tanh_visualization(self):
    axes = Axes(x_range=[-4, 4], y_range=[-1.5, 1.5], x_length=6, y_length=4)

    tanh_graph = axes.plot(lambda x: np.tanh(x), color=PURPLE)

    # Asymptotes at y = -1 and y = 1
    upper = DashedLine(axes.c2p(-4, 1), axes.c2p(4, 1), color=GRAY)
    lower = DashedLine(axes.c2p(-4, -1), axes.c2p(4, -1), color=GRAY)

    equation = MathTex(r"\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}", color=YELLOW)
    equation.to_corner(UR)

    return VGroup(axes, tanh_graph, upper, lower, equation)
```

### Leaky ReLU

```python
def create_leaky_relu_visualization(self, alpha=0.1):
    axes = Axes(x_range=[-3, 3], y_range=[-1, 3], x_length=6, y_length=4)

    leaky_left = axes.plot(lambda x: alpha * x, color=TEAL, x_range=[-3, 0])
    leaky_right = axes.plot(lambda x: x, color=TEAL, x_range=[0, 3])

    equation = MathTex(
        r"\text{LeakyReLU}(x) = \begin{cases} x & x > 0 \\ \alpha x & x \leq 0 \end{cases}",
        color=YELLOW
    )
    equation.scale(0.8).to_corner(UR)

    return VGroup(axes, leaky_left, leaky_right, equation)
```

## Activation Comparison Animation

```python
class ActivationComparison(Scene):
    def construct(self):
        axes = Axes(x_range=[-4, 4], y_range=[-1.5, 2], x_length=8, y_length=5)
        self.play(Create(axes))

        # Create all functions
        functions = {
            "Sigmoid": (lambda x: 1/(1+np.exp(-x)), BLUE),
            "ReLU": (lambda x: max(0, x), GREEN),
            "Tanh": (lambda x: np.tanh(x), PURPLE),
        }

        graphs = {}
        for name, (func, color) in functions.items():
            graphs[name] = axes.plot(func, color=color, x_range=[-4, 4])

        # Show one by one
        legend = VGroup()
        for i, (name, graph) in enumerate(graphs.items()):
            self.play(Create(graph), run_time=1)

            label = Text(name, font_size=24, color=functions[name][1])
            label.to_corner(UR).shift(DOWN * i * 0.5)
            legend.add(label)
            self.play(Write(label))
            self.wait(0.5)

        self.wait()
```

## Neuron with Activation

```python
class NeuronActivation(Scene):
    def construct(self):
        # Neuron representation
        neuron = Circle(radius=0.5, fill_color=BLUE, fill_opacity=0.5)

        # Input arrow
        input_arrow = Arrow(LEFT * 2, neuron.get_left(), color=WHITE)
        input_label = MathTex("x").next_to(input_arrow, UP)

        # Activation function inside neuron
        sigma = MathTex(r"\sigma").move_to(neuron)

        # Output arrow
        output_arrow = Arrow(neuron.get_right(), RIGHT * 2, color=WHITE)
        output_label = MathTex(r"\sigma(x)").next_to(output_arrow, UP)

        self.play(
            GrowFromCenter(neuron),
            Write(sigma)
        )
        self.play(
            GrowArrow(input_arrow),
            Write(input_label)
        )
        self.play(
            GrowArrow(output_arrow),
            Write(output_label)
        )
        self.wait()

        # Show different activations
        activations = [
            (r"\sigma", "Sigmoid"),
            (r"\text{ReLU}", "ReLU"),
            (r"\tanh", "Tanh"),
        ]

        for symbol, name in activations:
            new_sigma = MathTex(symbol).move_to(neuron)
            self.play(Transform(sigma, new_sigma))
            self.wait(0.5)
```

## Guidelines

- Always show x and y axis labels
- Include asymptotes as dashed lines
- Display the equation prominently (yellow color)
- Animate the function being drawn (Create)
- Use consistent axis ranges for comparison

## Forbidden

- Do NOT use different scales when comparing activation functions
- Do NOT skip showing the mathematical formula
- Do NOT use colors too similar between functions in comparison
- Do NOT forget to highlight key points (kinks, asymptotes, midpoints)
