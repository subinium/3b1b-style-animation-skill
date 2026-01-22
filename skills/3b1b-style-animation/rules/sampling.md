---
name: sampling
description: Monte Carlo and sampling methods visualization
metadata:
  tags: sampling, monte-carlo, statistics, simulation
---

# Sampling Methods Visualization

## Monte Carlo Integration

```python
from manim import *
import numpy as np

class MonteCarloIntegration(Scene):
    def construct(self):
        # Estimate π using random points in square

        # Square boundary
        square = Square(side_length=4, color=WHITE)

        # Quarter circle (radius 2)
        circle = Arc(
            radius=2,
            start_angle=0,
            angle=PI / 2,
            color=BLUE,
            stroke_width=3
        )
        circle.move_to(square.get_corner(DL), aligned_edge=DL)

        self.play(Create(square), Create(circle))

        # Sample points
        n_points = 500
        np.random.seed(42)

        inside_count = 0
        inside_dots = VGroup()
        outside_dots = VGroup()

        for i in range(n_points):
            x = np.random.uniform(0, 2)
            y = np.random.uniform(0, 2)

            # Check if inside quarter circle
            is_inside = x**2 + y**2 <= 4

            dot = Dot(
                square.get_corner(DL) + RIGHT * x + UP * y,
                radius=0.03,
                color=BLUE if is_inside else RED
            )

            if is_inside:
                inside_count += 1
                inside_dots.add(dot)
            else:
                outside_dots.add(dot)

            # Animate in batches
            if (i + 1) % 50 == 0:
                batch_inside = inside_dots[-50:] if len(inside_dots) >= 50 else inside_dots
                batch_outside = outside_dots[-50:] if len(outside_dots) >= 50 else outside_dots

                self.play(
                    *[FadeIn(d) for d in batch_inside],
                    *[FadeIn(d) for d in batch_outside],
                    run_time=0.3
                )

                # Update π estimate
                pi_estimate = 4 * inside_count / (i + 1)
                estimate_text = MathTex(
                    f"\\hat{{\\pi}} = 4 \\times \\frac{{{inside_count}}}{{{i + 1}}} \\approx {pi_estimate:.4f}",
                    font_size=24
                )
                estimate_text.to_corner(UR)

                if i == 49:
                    self.play(Write(estimate_text))
                else:
                    self.play(Transform(estimate_text, estimate_text.copy()), run_time=0.1)

        # Final result
        final_pi = 4 * inside_count / n_points
        final_text = MathTex(
            f"\\pi \\approx {final_pi:.4f} \\quad (\\text{{true: }} 3.1416)",
            font_size=28,
            color=GREEN
        )
        final_text.to_edge(DOWN)
        self.play(Write(final_text))
        self.wait()
```

## Rejection Sampling

```python
class RejectionSampling(Scene):
    def construct(self):
        # Target distribution (unnormalized)
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 1, 0.2],
            x_length=8,
            y_length=4
        )
        self.play(Create(axes))

        # Target distribution
        def target(x):
            return 0.3 * np.exp(-x**2) + 0.7 * np.exp(-(x - 1)**2 / 0.5)

        target_graph = axes.plot(target, color=BLUE, stroke_width=3)
        target_label = Text("Target p(x)", font_size=20, color=BLUE)
        target_label.to_corner(UL)

        self.play(Create(target_graph), Write(target_label))

        # Proposal distribution (uniform envelope)
        M = 1.1  # Scaling constant
        envelope = axes.plot(lambda x: M, color=RED, x_range=[-3, 3])
        envelope_label = Text("Envelope Mq(x)", font_size=20, color=RED)
        envelope_label.next_to(target_label, DOWN, aligned_edge=LEFT)

        self.play(Create(envelope), Write(envelope_label))
        self.wait()

        # Rejection sampling animation
        np.random.seed(42)
        accepted_dots = VGroup()
        rejected_dots = VGroup()

        for i in range(100):
            # Sample from proposal (uniform)
            x = np.random.uniform(-3, 3)
            u = np.random.uniform(0, M)

            # Accept/reject
            point_pos = axes.c2p(x, u)

            if u <= target(x):
                dot = Dot(point_pos, color=GREEN, radius=0.05)
                accepted_dots.add(dot)
            else:
                dot = Dot(point_pos, color=RED, radius=0.03, fill_opacity=0.5)
                rejected_dots.add(dot)

            if (i + 1) % 20 == 0:
                self.play(
                    *[FadeIn(d) for d in accepted_dots[-20:]],
                    *[FadeIn(d) for d in rejected_dots[-20:]],
                    run_time=0.3
                )

        # Show acceptance rate
        accept_rate = len(accepted_dots) / 100
        rate_text = MathTex(
            f"\\text{{Acceptance rate}} = {accept_rate:.0%}",
            font_size=24
        )
        rate_text.to_edge(DOWN)
        self.play(Write(rate_text))
        self.wait()
```

## Random Walk / Markov Chain

```python
class RandomWalkVisualization(Scene):
    def construct(self):
        # 2D random walk
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={"stroke_opacity": 0.3}
        )
        self.play(Create(plane))

        # Random walk path
        np.random.seed(42)
        n_steps = 100
        step_size = 0.3

        positions = [(0, 0)]
        for _ in range(n_steps):
            angle = np.random.uniform(0, 2 * np.pi)
            dx = step_size * np.cos(angle)
            dy = step_size * np.sin(angle)
            new_pos = (positions[-1][0] + dx, positions[-1][1] + dy)
            positions.append(new_pos)

        # Animate walk
        path = VMobject()
        path.set_stroke(YELLOW, width=2)

        dot = Dot(ORIGIN, color=BLUE, radius=0.1)
        self.add(dot)

        for i, pos in enumerate(positions[1:]):
            new_point = np.array([pos[0], pos[1], 0])

            # Extend path
            if i == 0:
                path.set_points_as_corners([ORIGIN, new_point])
            else:
                path.add_line_to(new_point)

            self.play(
                dot.animate.move_to(new_point),
                Create(path.copy()),
                run_time=0.05
            )

        self.add(path)

        # Show final distance from origin
        final_pos = positions[-1]
        distance = np.sqrt(final_pos[0]**2 + final_pos[1]**2)

        dist_line = DashedLine(ORIGIN, [final_pos[0], final_pos[1], 0], color=RED)
        dist_label = MathTex(f"d = {distance:.2f}", font_size=24, color=RED)
        dist_label.next_to(dist_line, UP)

        self.play(Create(dist_line), Write(dist_label))
        self.wait()
```

## Importance Sampling

```python
class ImportanceSampling(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.6, 0.1],
            x_length=8,
            y_length=4
        )
        self.play(Create(axes))

        # Target distribution (where we want to sample)
        from scipy import stats

        def target(x):
            return stats.norm.pdf(x, 2, 0.5)  # Narrow gaussian at x=2

        # Original proposal (standard normal)
        def proposal(x):
            return stats.norm.pdf(x, 0, 1)

        # Better proposal (closer to target)
        def better_proposal(x):
            return stats.norm.pdf(x, 2, 1)

        target_graph = axes.plot(target, color=BLUE, x_range=[-1, 4])
        proposal_graph = axes.plot(proposal, color=RED, x_range=[-4, 4])

        target_label = Text("Target", font_size=18, color=BLUE).to_corner(UL)
        proposal_label = Text("Proposal", font_size=18, color=RED).next_to(target_label, DOWN)

        self.play(
            Create(target_graph), Write(target_label),
            Create(proposal_graph), Write(proposal_label)
        )
        self.wait()

        # Show mismatch problem
        mismatch_text = Text(
            "Poor overlap → high variance",
            font_size=20,
            color=YELLOW
        )
        mismatch_text.to_edge(DOWN)
        self.play(Write(mismatch_text))
        self.wait()

        # Better proposal
        better_graph = axes.plot(better_proposal, color=GREEN, x_range=[-2, 6])
        better_label = Text("Better Proposal", font_size=18, color=GREEN)
        better_label.next_to(proposal_label, DOWN)

        self.play(
            Transform(proposal_graph, better_graph),
            Write(better_label)
        )

        good_text = Text(
            "Good overlap → low variance",
            font_size=20,
            color=GREEN
        )
        good_text.to_edge(DOWN)
        self.play(Transform(mismatch_text, good_text))
        self.wait()
```

## Guidelines

- Use distinct colors for accepted/rejected samples
- Show convergence over time with counters
- Animate individual samples for small N, batches for large N
- Include variance/error estimates
- Label all distributions clearly

## Forbidden

- Do NOT show too many points at once (batch animations)
- Do NOT skip showing the acceptance criterion
- Do NOT use same color for target and proposal
- Do NOT forget to show the mathematical formula/algorithm
- Do NOT make random walks too fast to follow
