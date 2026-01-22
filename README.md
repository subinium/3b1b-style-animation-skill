# 3Blue1Brown Style Math Animations

<div align="center">

<img src="https://www.3blue1brown.com/content/lessons/2020/lockdown-math/thumbnail.png" alt="3b1b style" width="400"/>

**Create pedagogically-focused mathematical animations in the 3Blue1Brown style**

*A tribute to Grant Sanderson and the 3Blue1Brown channel*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Manim](https://img.shields.io/badge/Manim-Community-blue)](https://www.manim.community/)

</div>

---

## A Note of Gratitude

This skill is an **unofficial tribute** to [3Blue1Brown](https://www.3blue1brown.com/), the extraordinary YouTube channel created by **Grant Sanderson**.

3Blue1Brown has fundamentally changed how millions of people understand mathematics. The channel's unique approach—building visual intuition before introducing formulas, asking "why" before "what"—has made complex topics like linear algebra, calculus, and neural networks accessible to learners worldwide.

> *"The goal is not to animate math, but to build understanding. Animation is just the medium."*

This skill attempts to capture and codify the pedagogical philosophy behind 3Blue1Brown videos, making it easier for anyone to create educational math content with the same clarity and elegance.

**This is not affiliated with or endorsed by 3Blue1Brown.** It's simply a fan's attempt to learn from and share the teaching principles that have helped so many.

---

## What This Skill Does

Helps Claude Code create mathematical animations that prioritize **understanding over aesthetics**:

| Philosophy | Implementation |
|------------|----------------|
| Intuition before formalism | Build visual understanding before showing formulas |
| Why before what | Motivate concepts before defining them |
| Concrete before abstract | Start with examples, then generalize |
| Show, don't tell | Let the visual do the explaining |

## Topics Covered

- **Linear Algebra** — Matrix transformations, eigenvalues, vector spaces
- **Deep Learning** — Neural networks, backpropagation, attention mechanisms
- **Statistics** — Probability distributions, Bayesian inference
- **Number Theory** — GCD, LCM, prime numbers
- **Algorithms** — Dijkstra, sorting, graph algorithms
- **3D Visualization** — Surfaces, loss landscapes

## Installation

```bash
# Install Manim (required)
pip install manim

# Add this skill to Claude Code
npx skills add subinium/3b1b-style-animation-skill
```

## Usage

Once installed, Claude Code will follow these guidelines when you ask:

```
"Explain eigenvalues with a 3-minute animation"
"Create a visualization of how backpropagation works"
"Show why matrix multiplication isn't commutative"
"Animate the Dijkstra algorithm step by step"
```

## Quick Example

```python
from manim import *

class WhyPythagorean(Scene):
    """Start with WHY, not WHAT."""

    def construct(self):
        self.camera.background_color = "#1c1c1c"

        # Hook: Pose the question
        question = Text("Why does a² + b² = c²?", font_size=36)
        self.play(Write(question))
        self.wait()

        # The rest builds visual intuition...
```

## Structure

```
3b1b-style-animation-skill/
├── package.json
├── README.md
├── skills/
│   └── 3b1b-style-animation/
│       ├── SKILL.md          # Main skill definition
│       └── rules/            # 38 detailed guideline files
└── examples/                 # Working demonstrations
```

## The 3Blue1Brown Visual Style

| Element | Value |
|---------|-------|
| Background | `#1c1c1c` (dark gray) |
| Primary accent | `#3b82f6` (blue) |
| Secondary accent | `#fbbf24` (yellow/gold) |
| Positive values | Blue tones |
| Negative values | Red tones |
| Neutral/zero | Gray |

## Contributing

Contributions that improve the pedagogical quality are welcome. Please ensure any additions follow the "understanding first" philosophy.

## Resources

- [3Blue1Brown YouTube](https://www.youtube.com/c/3blue1brown)
- [Manim Community](https://www.manim.community/)
- [Grant's Summer of Math Exposition](https://www.3blue1brown.com/blog/some1)

## License

MIT License — Use freely, teach generously.

---

<div align="center">

*Thank you, Grant, for showing us that math can be beautiful.*

</div>
