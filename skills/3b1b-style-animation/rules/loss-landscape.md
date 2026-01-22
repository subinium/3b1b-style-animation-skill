---
name: loss-landscape
description: 3D loss surface visualization
metadata:
  tags: loss, landscape, 3d, surface, optimization
---

# Loss Landscape Visualization

## Basic 3D Loss Surface

```python
from manim import *
import numpy as np

class LossLandscape3D(ThreeDScene):
    def construct(self):
        # Set up 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 10, 2],
            x_length=6,
            y_length=6,
            z_length=4
        )

        # Labels
        x_label = MathTex("w_1").next_to(axes.x_axis, RIGHT)
        y_label = MathTex("w_2").next_to(axes.y_axis, UP)
        z_label = MathTex("L").next_to(axes.z_axis, OUT)

        # Loss function: simple convex bowl
        def loss_func(u, v):
            return u**2 + v**2

        surface = Surface(
            lambda u, v: axes.c2p(u, v, loss_func(u, v)),
            u_range=[-2.5, 2.5],
            v_range=[-2.5, 2.5],
            resolution=(30, 30),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )

        # Set camera
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        # Animate
        self.play(Create(axes))
        self.play(Create(surface), run_time=2)
        self.wait()

        # Rotate camera for full view
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        # Show minimum point
        min_point = Dot3D(axes.c2p(0, 0, 0), color=GREEN, radius=0.15)
        min_label = MathTex(r"w^*", color=GREEN).next_to(min_point, OUT + RIGHT)

        self.play(GrowFromCenter(min_point), Write(min_label))
        self.wait()
```

## Non-Convex Loss Landscape

```python
class NonConvexLoss(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 4, 1],
            x_length=6,
            y_length=6,
            z_length=4
        )

        # Non-convex function with local minima
        def loss_func(u, v):
            return (
                np.sin(u * 1.5) * np.cos(v * 1.5) +
                0.1 * (u**2 + v**2) +
                np.cos(u + v)
            )

        surface = Surface(
            lambda u, v: axes.c2p(u, v, loss_func(u, v)),
            u_range=[-2.5, 2.5],
            v_range=[-2.5, 2.5],
            resolution=(50, 50),
            fill_opacity=0.8,
            checkerboard_colors=[PURPLE_D, PURPLE_E]
        )

        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES)

        self.play(Create(axes))
        self.play(Create(surface), run_time=3)
        self.wait()

        # Mark local minima
        local_minima = [
            (-1.5, -1.0, "Local"),
            (1.2, 1.5, "Local"),
            (-0.3, 0.2, "Global")
        ]

        for x, y, label_text in local_minima:
            z = loss_func(x, y)
            point = Dot3D(axes.c2p(x, y, z), color=YELLOW if "Local" in label_text else GREEN, radius=0.1)
            self.play(GrowFromCenter(point), run_time=0.5)

        # Rotate for exploration
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(6)
        self.stop_ambient_camera_rotation()
```

## Gradient Descent on 3D Surface

```python
class GradientDescent3D(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 10, 2],
            x_length=6,
            y_length=6,
            z_length=4
        )

        def loss_func(u, v):
            return u**2 + v**2

        surface = Surface(
            lambda u, v: axes.c2p(u, v, loss_func(u, v)),
            u_range=[-2.5, 2.5],
            v_range=[-2.5, 2.5],
            resolution=(30, 30),
            fill_opacity=0.6,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.add(axes, surface)

        # Gradient descent path
        x, y = 2.0, 2.0
        lr = 0.15
        path_points = []

        for _ in range(25):
            z = loss_func(x, y)
            path_points.append(axes.c2p(x, y, z))

            # Gradient
            grad_x, grad_y = 2 * x, 2 * y

            # Update
            x -= lr * grad_x
            y -= lr * grad_y

        # Create path
        path = VMobject()
        path.set_points_smoothly(path_points)
        path.set_stroke(YELLOW, width=4)

        # Animate ball rolling down
        ball = Dot3D(path_points[0], color=RED, radius=0.12)
        self.add(ball)

        self.play(
            MoveAlongPath(ball, path),
            Create(path),
            run_time=4,
            rate_func=linear
        )

        # Show final position
        final_label = MathTex(r"\approx w^*", color=GREEN)
        final_label.next_to(ball, OUT + RIGHT)
        self.add_fixed_in_frame_mobjects(final_label)
        self.play(Write(final_label))
        self.wait()
```

## Saddle Point Visualization

```python
class SaddlePoint(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            x_length=5,
            y_length=5,
            z_length=4
        )

        # Saddle function: z = x^2 - y^2
        def saddle_func(u, v):
            return u**2 - v**2

        surface = Surface(
            lambda u, v: axes.c2p(u, v, saddle_func(u, v)),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(30, 30),
            fill_opacity=0.7,
            checkerboard_colors=[ORANGE, RED_E]
        )

        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        self.play(Create(axes))
        self.play(Create(surface), run_time=2)

        # Mark saddle point
        saddle_point = Dot3D(axes.c2p(0, 0, 0), color=YELLOW, radius=0.15)
        self.play(GrowFromCenter(saddle_point))

        # Label
        label = Text("Saddle Point", font_size=24, color=YELLOW)
        label.to_corner(UR)
        self.add_fixed_in_frame_mobjects(label)
        self.play(Write(label))

        # Show gradient is zero at saddle
        grad_eq = MathTex(r"\nabla L = 0", color=YELLOW)
        grad_eq.next_to(label, DOWN)
        self.add_fixed_in_frame_mobjects(grad_eq)
        self.play(Write(grad_eq))

        # Rotate to show shape
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
```

## Contour Plot (2D projection)

```python
class LossContours(Scene):
    def construct(self):
        # Create contour representation
        def loss_func(x, y):
            return x**2 + 2 * y**2

        # Draw contour ellipses
        contours = VGroup()
        colors = color_gradient([BLUE, PURPLE, RED], 8)

        for i, level in enumerate(np.linspace(0.5, 4, 8)):
            # For x^2 + 2y^2 = c, this is an ellipse
            ellipse = Ellipse(
                width=2 * np.sqrt(level),
                height=2 * np.sqrt(level / 2),
                stroke_color=colors[i],
                stroke_width=2,
                fill_opacity=0
            )
            contours.add(ellipse)

        self.play(Create(contours), run_time=2)

        # Add level labels
        for i, (ellipse, level) in enumerate(zip(contours[::2], np.linspace(0.5, 4, 8)[::2])):
            label = MathTex(f"L={level:.1f}", font_size=16)
            label.next_to(ellipse, RIGHT)
            self.play(Write(label), run_time=0.3)

        # Show gradient descent path
        x, y = 1.8, 1.2
        path_points = [[x, y, 0]]
        lr = 0.1

        for _ in range(20):
            x -= lr * 2 * x
            y -= lr * 4 * y
            path_points.append([x, y, 0])

        path = VMobject()
        path.set_points_smoothly([np.array(p) for p in path_points])
        path.set_stroke(YELLOW, width=3)

        self.play(Create(path), run_time=2)

        # Final point
        final = Dot(path_points[-1][:2], color=GREEN, radius=0.1)
        self.play(GrowFromCenter(final))
        self.wait()
```

## Guidelines

- Use checkerboard colors for better 3D depth perception
- Always rotate camera to show surface from multiple angles
- Mark critical points (minima, maxima, saddle points)
- Animate gradient descent path on surface
- Use contour plots for 2D projection when needed

## Forbidden

- Do NOT use flat colors on 3D surfaces (hard to perceive depth)
- Do NOT skip camera rotation for complex surfaces
- Do NOT make camera rotation too fast (causes motion sickness)
- Do NOT forget axis labels (w1, w2, L)
