---
name: bayes-theorem
description: Bayesian inference visualization
metadata:
  tags: bayes, probability, inference, statistics
---

# Bayes Theorem Visualization

## Bayes Formula Animation

```python
from manim import *
import numpy as np

class BayesFormula(Scene):
    def construct(self):
        # Bayes' theorem formula
        formula = MathTex(
            r"P(A|B)",
            r"=",
            r"\frac{P(B|A) \cdot P(A)}{P(B)}"
        )
        formula.scale(1.2)

        self.play(Write(formula))
        self.wait()

        # Color code components
        colors = {
            0: YELLOW,   # P(A|B) - Posterior
            2: BLUE,     # Numerator (likelihood × prior)
        }

        for idx, color in colors.items():
            self.play(formula[idx].animate.set_color(color))

        # Labels
        posterior_label = Text("Posterior", font_size=20, color=YELLOW)
        posterior_label.next_to(formula[0], UP)

        likelihood_label = Text("Likelihood × Prior", font_size=18, color=BLUE)
        likelihood_label.next_to(formula[2], DOWN)

        self.play(Write(posterior_label), Write(likelihood_label))
        self.wait()

        # Expanded form
        expanded = MathTex(
            r"P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B|A) \cdot P(A) + P(B|\neg A) \cdot P(\neg A)}"
        )
        expanded.scale(0.9)
        expanded.to_edge(DOWN, buff=1)

        self.play(Write(expanded))
        self.wait()
```

## Visual Probability Update

```python
class BayesVisualUpdate(Scene):
    def construct(self):
        # Prior probability bar
        prior_bar = Rectangle(
            width=4, height=0.5,
            fill_color=BLUE, fill_opacity=0.5
        )
        prior_label = Text("Prior P(A)", font_size=20)
        prior_label.next_to(prior_bar, UP)

        prior_value = 0.3
        filled_prior = Rectangle(
            width=4 * prior_value, height=0.5,
            fill_color=BLUE, fill_opacity=0.8
        )
        filled_prior.align_to(prior_bar, LEFT)

        prior_group = VGroup(prior_bar, filled_prior, prior_label)
        prior_group.shift(UP * 2)

        self.play(Create(prior_bar), Write(prior_label))
        self.play(Create(filled_prior))

        prior_text = MathTex(f"P(A) = {prior_value}", font_size=24)
        prior_text.next_to(prior_bar, RIGHT)
        self.play(Write(prior_text))

        # Evidence arrives
        evidence_text = Text("Evidence B observed", font_size=24, color=YELLOW)
        evidence_text.shift(DOWN * 0.5)
        self.play(Write(evidence_text))
        self.wait()

        # Likelihood
        likelihood = 0.8  # P(B|A)
        false_positive = 0.1  # P(B|¬A)

        likelihood_text = MathTex(
            f"P(B|A) = {likelihood}, \\quad P(B|\\neg A) = {false_positive}",
            font_size=22
        )
        likelihood_text.next_to(evidence_text, DOWN)
        self.play(Write(likelihood_text))

        # Calculate posterior
        marginal = likelihood * prior_value + false_positive * (1 - prior_value)
        posterior = (likelihood * prior_value) / marginal

        # Posterior bar
        posterior_bar = Rectangle(
            width=4, height=0.5,
            fill_color=GREEN, fill_opacity=0.5
        )
        posterior_label = Text("Posterior P(A|B)", font_size=20)
        posterior_label.next_to(posterior_bar, UP)

        filled_posterior = Rectangle(
            width=4 * posterior, height=0.5,
            fill_color=GREEN, fill_opacity=0.8
        )
        filled_posterior.align_to(posterior_bar, LEFT)

        posterior_group = VGroup(posterior_bar, filled_posterior, posterior_label)
        posterior_group.shift(DOWN * 2.5)

        self.play(Create(posterior_bar), Write(posterior_label))

        # Animate the update
        transform_arrow = Arrow(
            prior_group.get_bottom(),
            posterior_group.get_top(),
            color=YELLOW
        )
        self.play(GrowArrow(transform_arrow))

        self.play(Create(filled_posterior))

        posterior_text = MathTex(f"P(A|B) = {posterior:.3f}", font_size=24)
        posterior_text.next_to(posterior_bar, RIGHT)
        self.play(Write(posterior_text))
        self.wait()
```

## Area-Based Bayes Visualization

```python
class BayesAreaDiagram(Scene):
    def construct(self):
        # Total population square
        total = Square(side_length=4, fill_color=WHITE, fill_opacity=0.1)
        total_label = Text("Total Population", font_size=18)
        total_label.next_to(total, UP)

        self.play(Create(total), Write(total_label))

        # P(A) region
        p_a = 0.3
        a_region = Rectangle(
            width=4 * p_a, height=4,
            fill_color=BLUE, fill_opacity=0.5
        )
        a_region.align_to(total, LEFT + DOWN)

        a_label = MathTex(f"P(A) = {p_a}", font_size=20, color=BLUE)
        a_label.next_to(a_region, DOWN)

        self.play(Create(a_region), Write(a_label))

        # P(B|A) within A (vertical slice)
        p_b_given_a = 0.8
        b_given_a = Rectangle(
            width=4 * p_a,
            height=4 * p_b_given_a,
            fill_color=YELLOW, fill_opacity=0.7
        )
        b_given_a.align_to(a_region, LEFT + DOWN)

        # P(B|¬A) in ¬A region
        p_b_given_not_a = 0.1
        b_given_not_a = Rectangle(
            width=4 * (1 - p_a),
            height=4 * p_b_given_not_a,
            fill_color=YELLOW, fill_opacity=0.7
        )
        b_given_not_a.align_to(total, RIGHT)
        b_given_not_a.align_to(total, DOWN)

        self.play(Create(b_given_a), Create(b_given_not_a))

        # Label B regions
        b_label = Text("B observed", font_size=16, color=YELLOW)
        b_label.move_to(total.get_center() + DOWN * 0.5)
        self.play(Write(b_label))

        # Calculate and show posterior
        area_a_and_b = p_a * p_b_given_a
        area_b = p_a * p_b_given_a + (1 - p_a) * p_b_given_not_a
        posterior = area_a_and_b / area_b

        # Highlight A∩B
        self.play(
            b_given_a.animate.set_stroke(color=RED, width=4),
            run_time=0.5
        )

        result = MathTex(
            f"P(A|B) = \\frac{{\\text{{Yellow in Blue}}}}{{\\text{{All Yellow}}}} = {posterior:.3f}",
            font_size=22
        )
        result.to_edge(DOWN)
        self.play(Write(result))
        self.wait()
```

## Sequential Bayesian Update

```python
class SequentialBayesUpdate(Scene):
    def construct(self):
        # Show how posterior becomes prior for next update

        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 5, 1],
            x_length=8,
            y_length=4
        )
        x_label = MathTex(r"\theta").next_to(axes.x_axis, RIGHT)
        y_label = MathTex(r"p(\theta)").next_to(axes.y_axis, UP)

        self.play(Create(axes), Write(x_label), Write(y_label))

        # Initial prior (uniform)
        prior = axes.plot(lambda x: 1, color=BLUE, x_range=[0.01, 0.99])
        prior_label = Text("Prior", font_size=20, color=BLUE)
        prior_label.to_corner(UL)

        self.play(Create(prior), Write(prior_label))
        self.wait()

        # Simulated data updates
        observations = [1, 1, 0, 1, 1, 1, 0, 1]  # 1 = success, 0 = failure

        alpha, beta = 1, 1  # Beta distribution parameters

        for i, obs in enumerate(observations):
            # Update parameters
            alpha += obs
            beta += (1 - obs)

            # New posterior (Beta distribution)
            from scipy import stats as sp_stats
            new_posterior = axes.plot(
                lambda x, a=alpha, b=beta: sp_stats.beta.pdf(x, a, b),
                color=interpolate_color(BLUE, RED, i / len(observations)),
                x_range=[0.01, 0.99]
            )

            # Observation label
            obs_text = Text(f"Obs {i + 1}: {'✓' if obs else '✗'}", font_size=18)
            obs_text.to_corner(UR).shift(DOWN * i * 0.4)

            self.play(
                Transform(prior, new_posterior),
                Write(obs_text),
                run_time=0.5
            )

        # Final posterior
        final_label = Text("Posterior after 8 observations", font_size=18, color=RED)
        final_label.next_to(axes, DOWN)
        self.play(Write(final_label))
        self.wait()
```

## Guidelines

- Show prior → evidence → posterior flow clearly
- Use area diagrams for intuitive understanding
- Color code: prior (blue), likelihood (green), posterior (yellow/red)
- Animate probability updates sequentially
- Always verify that probabilities sum/integrate to 1

## Forbidden

- Do NOT show posterior without showing prior first
- Do NOT skip the evidence step
- Do NOT use inconsistent probability values
- Do NOT forget to show the mathematical formula
- Do NOT make probability bars exceed 1
