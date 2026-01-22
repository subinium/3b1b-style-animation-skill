---
name: distributions
description: Probability distribution visualization (PDF/CDF)
metadata:
  tags: probability, distribution, pdf, cdf, statistics
---

# Probability Distribution Visualization

## Gaussian Distribution

```python
from manim import *
import numpy as np
from scipy import stats

class GaussianDistribution(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": True}
        )

        x_label = MathTex("x").next_to(axes.x_axis, RIGHT)
        y_label = MathTex("f(x)").next_to(axes.y_axis, UP)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # Gaussian PDF
        mu, sigma = 0, 1
        gaussian = axes.plot(
            lambda x: stats.norm.pdf(x, mu, sigma),
            color=BLUE
        )

        # Formula
        formula = MathTex(
            r"f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}",
            font_size=28
        )
        formula.to_corner(UR)

        self.play(Create(gaussian), Write(formula))
        self.wait()

        # Show mean line
        mean_line = axes.get_vertical_line(axes.c2p(mu, stats.norm.pdf(mu, mu, sigma)))
        mean_line.set_color(YELLOW)
        mean_label = MathTex(r"\mu", color=YELLOW, font_size=24)
        mean_label.next_to(mean_line, DOWN)

        self.play(Create(mean_line), Write(mean_label))

        # Show standard deviation regions
        for n_sigma, opacity in [(1, 0.4), (2, 0.2), (3, 0.1)]:
            region = axes.get_area(
                gaussian,
                x_range=[mu - n_sigma * sigma, mu + n_sigma * sigma],
                color=BLUE,
                opacity=opacity
            )
            self.play(FadeIn(region), run_time=0.5)

        # Percentage labels
        labels = VGroup(
            MathTex(r"68.3\%", font_size=20).move_to(axes.c2p(0, 0.2)),
            MathTex(r"95.4\%", font_size=18).move_to(axes.c2p(0, 0.08)),
            MathTex(r"99.7\%", font_size=16).move_to(axes.c2p(0, 0.02)),
        )
        self.play(Write(labels))
        self.wait()
```

## Discrete to Continuous Transition (3b1b CLT style)

```python
class DiscreteToContinuous(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-5, 15, 1],
            y_range=[0, 0.3, 0.1],
            x_length=10,
            y_length=4
        )
        self.play(Create(axes))

        # Start with histogram (binomial approximation)
        n_trials = 10
        p = 0.5

        bars = VGroup()
        for k in range(n_trials + 1):
            prob = stats.binom.pmf(k, n_trials, p)
            bar = Rectangle(
                width=0.8,
                height=prob * 10,
                fill_color=BLUE,
                fill_opacity=0.7
            )
            bar.move_to(axes.c2p(k, prob / 2), DOWN)
            bars.add(bar)

        self.play(Create(bars))
        self.wait()

        # Transition to continuous (increase n)
        for new_n in [20, 50, 100]:
            new_bars = VGroup()
            bar_width = 10 / new_n

            for k in range(new_n + 1):
                prob = stats.binom.pmf(k, new_n, p)
                scaled_k = k * 10 / new_n  # Scale x position

                bar = Rectangle(
                    width=bar_width * 0.9,
                    height=prob * new_n / 3,  # Scale height
                    fill_color=BLUE,
                    fill_opacity=0.7
                )
                bar.move_to(axes.c2p(scaled_k, prob * new_n / 6), DOWN)
                new_bars.add(bar)

            self.play(Transform(bars, new_bars), run_time=1)
            self.wait(0.5)

        # Overlay continuous gaussian
        mu = n_trials * p
        sigma = np.sqrt(n_trials * p * (1 - p))

        gaussian = axes.plot(
            lambda x: stats.norm.pdf(x, 5, sigma * 10 / n_trials),
            color=YELLOW,
            stroke_width=3
        )
        self.play(Create(gaussian))
        self.wait()
```

## Distribution Sampling Animation (3b1b style)

```python
class RepeatedSampling(Scene):
    """
    Based on 3b1b's CLT visualization pattern.
    Show distribution emerging from repeated samples.
    """

    def construct(self):
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            x_length=8,
            y_length=4
        )
        self.play(Create(axes))

        # Collect samples
        np.random.seed(42)
        samples = []
        n_bins = 30
        histogram = VGroup()

        for batch in range(20):
            # Add batch of samples
            new_samples = np.random.normal(0, 1, 50)
            samples.extend(new_samples)

            # Update histogram
            hist, bin_edges = np.histogram(samples, bins=n_bins, range=(-4, 4), density=True)

            new_bars = VGroup()
            bin_width = 8 / n_bins

            for i, h in enumerate(hist):
                bar = Rectangle(
                    width=bin_width * 0.9,
                    height=h * 4 / 0.5,  # Scale to axes
                    fill_color=BLUE,
                    fill_opacity=0.6
                )
                x_pos = bin_edges[i] + (bin_edges[i + 1] - bin_edges[i]) / 2
                bar.move_to(axes.c2p(x_pos, h / 2), DOWN)
                new_bars.add(bar)

            if len(histogram) == 0:
                self.play(Create(new_bars), run_time=0.3)
                histogram = new_bars
            else:
                self.play(Transform(histogram, new_bars), run_time=0.1)

        # Overlay true distribution
        true_gaussian = axes.plot(
            lambda x: stats.norm.pdf(x, 0, 1),
            color=YELLOW,
            stroke_width=3
        )
        self.play(Create(true_gaussian))

        # Sample count
        count_label = MathTex(f"n = {len(samples)}", font_size=24)
        count_label.to_corner(UL)
        self.play(Write(count_label))
        self.wait()
```

## CDF Visualization

```python
class CDFVisualization(Scene):
    def construct(self):
        # PDF axes (top)
        pdf_axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            x_length=6,
            y_length=2.5
        )
        pdf_axes.to_edge(UP, buff=1)

        # CDF axes (bottom)
        cdf_axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 1, 0.2],
            x_length=6,
            y_length=2.5
        )
        cdf_axes.to_edge(DOWN, buff=1)

        # Labels
        pdf_label = Text("PDF", font_size=24).next_to(pdf_axes, LEFT)
        cdf_label = Text("CDF", font_size=24).next_to(cdf_axes, LEFT)

        self.play(
            Create(pdf_axes), Create(cdf_axes),
            Write(pdf_label), Write(cdf_label)
        )

        # Draw PDF
        pdf = pdf_axes.plot(lambda x: stats.norm.pdf(x, 0, 1), color=BLUE)
        self.play(Create(pdf))

        # Draw CDF
        cdf = cdf_axes.plot(lambda x: stats.norm.cdf(x, 0, 1), color=GREEN)
        self.play(Create(cdf))

        # Show relationship: area under PDF up to x = CDF(x)
        x_tracker = ValueTracker(-3)

        # Shaded area in PDF
        shaded_area = always_redraw(
            lambda: pdf_axes.get_area(
                pdf,
                x_range=[-4, x_tracker.get_value()],
                color=BLUE,
                opacity=0.5
            )
        )

        # Point on CDF
        cdf_dot = always_redraw(
            lambda: Dot(
                cdf_axes.c2p(
                    x_tracker.get_value(),
                    stats.norm.cdf(x_tracker.get_value(), 0, 1)
                ),
                color=YELLOW
            )
        )

        # Vertical line on PDF
        pdf_line = always_redraw(
            lambda: DashedLine(
                pdf_axes.c2p(x_tracker.get_value(), 0),
                pdf_axes.c2p(x_tracker.get_value(), stats.norm.pdf(x_tracker.get_value(), 0, 1)),
                color=YELLOW
            )
        )

        self.add(shaded_area, cdf_dot, pdf_line)

        # Animate x moving
        self.play(x_tracker.animate.set_value(2), run_time=4, rate_func=linear)
        self.wait()
```

## Multiple Distributions Comparison

```python
class DistributionComparison(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-5, 10, 1],
            y_range=[0, 0.5, 0.1],
            x_length=10,
            y_length=4
        )
        self.play(Create(axes))

        distributions = [
            ("Normal(0,1)", lambda x: stats.norm.pdf(x, 0, 1), BLUE),
            ("Exponential(1)", lambda x: stats.expon.pdf(x, 0, 1), GREEN),
            ("Uniform(-2,2)", lambda x: stats.uniform.pdf(x, -2, 4), RED),
        ]

        legend = VGroup()
        graphs = VGroup()

        for name, func, color in distributions:
            graph = axes.plot(func, color=color, x_range=[-4, 9])
            graphs.add(graph)

            legend_item = VGroup(
                Line(ORIGIN, RIGHT * 0.5, color=color, stroke_width=3),
                Text(name, font_size=16)
            ).arrange(RIGHT, buff=0.2)
            legend.add(legend_item)

        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_corner(UR)

        for graph in graphs:
            self.play(Create(graph), run_time=1)

        self.play(Create(legend))
        self.wait()
```

## Guidelines

- Always label axes (x, f(x) for PDF; x, F(x) for CDF)
- Show formula alongside the graph
- Use consistent colors across related visualizations
- Animate sampling to show distribution emergence
- Highlight mean, variance, standard deviation visually

## Forbidden

- Do NOT forget to normalize probability distributions
- Do NOT use bars that overlap (leave small gaps)
- Do NOT skip axis labels
- Do NOT show PDF values > 1 without explanation
- Do NOT mix discrete and continuous without transition
