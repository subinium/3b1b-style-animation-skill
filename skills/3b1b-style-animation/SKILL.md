---
name: 3b1b-style-animation
description: Create pedagogically-focused mathematical animations in 3Blue1Brown style using Manim
metadata:
  author: subinium
  version: 1.1.0
  tags: manim, 3b1b, math, education, pedagogy, visualization, animation
---

# 3Blue1Brown Style Mathematical Animations

Use this skill when creating mathematical animations, visualizations, or educational videos about math, algorithms, or deep learning concepts.

> "The goal is not to animate math, but to build understanding." — Grant Sanderson

---

## Core Philosophy

| Principle | Implementation |
|-----------|----------------|
| **Intuition Before Formalism** | Build visual understanding before showing formulas |
| **Why Before What** | Motivate concepts before defining them |
| **Concrete Before Abstract** | Start with specific examples, then generalize |
| **Show, Don't Tell** | Let the visual do the explaining |

---

## Quick Start

**Installation:**
```bash
pip install manim
```

**Basic Scene:**
```python
from manim import *

class MyScene(Scene):
    def construct(self):
        self.camera.background_color = "#1c1c1c"
        # Your animation code here
```

---

## Rules Index

### Setup & Configuration
| Rule | Description |
|------|-------------|
| `rules/manim-setup.md` | Installation and environment setup |
| `rules/color-scheme.md` | 3b1b color palette and semantic meaning |

### Animation Fundamentals (CRITICAL)
| Rule | Description |
|------|-------------|
| `rules/scene-basics.md` | Scene class structure and animation timing |
| `rules/animation-patterns.md` | **LaggedStartMap, state save/restore, progressive complexity** |
| `rules/seamless-transitions.md` | **Overlapped transitions, persistent elements** |
| `rules/mobject-grouping.md` | **VGroup organization and dictionary patterns** |
| `rules/updaters.md` | **add_updater for real-time animations** |

### Audio & Sync
| Rule | Description |
|------|-------------|
| `rules/audio-sync.md` | Synchronizing narration with visuals |
| `rules/strict-sync.md` | **StrictSyncScene base class for automatic timing** |
| `rules/narration.md` | TTS integration and script writing |

### Video Quality (HIGHEST PRIORITY)
| Rule | Description |
|------|-------------|
| `rules/visual-quality.md` | **No overlaps, readable text, clear hierarchy** |
| `rules/layout-spacing.md` | Screen zones, spacing, margins |
| `rules/video-completion.md` | **Duration and content completion checks** |
| `rules/verify-completion-template.md` | Verification script template |

### Pedagogy & Content
| Rule | Description |
|------|-------------|
| `rules/pre-production.md` | AI-guided planning with user interaction |
| `rules/pedagogy.md` | Teaching philosophy and explanation structures |
| `rules/mathematical-rigor.md` | Ensuring mathematical correctness |
| `rules/narrative-flow.md` | Smooth transitions and completeness |
| `rules/video-structure.md` | Hook, setup, core, example, takeaway |
| `rules/completeness-check.md` | Validation checklist before rendering |

### Visual Techniques
| Rule | Description |
|------|-------------|
| `rules/camera-work.md` | Focus, zoom, and visual hierarchy |
| `rules/equations.md` | LaTeX and mathematical notation |
| `rules/graphs.md` | Graph and chart visualization |
| `rules/3d-surfaces.md` | 3D visualization techniques |
| `rules/text-transforms.md` | **TransformMatchingStrings patterns** |

### Domain: Linear Algebra
| Rule | Description |
|------|-------------|
| `rules/linear-transformations.md` | Geometric interpretation of transforms |
| `rules/matrix-operations.md` | Matrix multiplication visualization |
| `rules/eigenvalues.md` | Eigenvector and eigenvalue intuition |
| `rules/vector-space.md` | Vector operations and spaces |

### Domain: Statistics & Probability
| Rule | Description |
|------|-------------|
| `rules/distributions.md` | PDF/CDF visualization |
| `rules/bayes-theorem.md` | Bayesian reasoning |
| `rules/sampling.md` | Monte Carlo methods |

### Domain: Deep Learning
| Rule | Description |
|------|-------------|
| `rules/neuron.md` | Single neuron visualization |
| `rules/layer.md` | Layer representations |
| `rules/network-architecture.md` | Full network diagrams |
| `rules/forward-pass.md` | Data flow visualization |
| `rules/gradient-flow.md` | Backpropagation visualization |
| `rules/chain-rule.md` | Chain rule explanation |
| `rules/weight-update.md` | Weight update visualization |
| `rules/loss-landscape.md` | Loss surface visualization |
| `rules/attention.md` | Attention mechanism |
| `rules/transformer-block.md` | Transformer architecture |

### Domain: CNN
| Rule | Description |
|------|-------------|
| `rules/convolution.md` | Convolution operation |
| `rules/feature-maps.md` | Feature map visualization |
| `rules/pooling.md` | Pooling operations |
| `rules/cnn-architecture.md` | CNN architecture diagrams |

### Templates & Helpers
| Rule | Description |
|------|-------------|
| `rules/explanation-templates.md` | Common explanation patterns |
| `rules/helpers-template.md` | **Helper function patterns from 3b1b** |

---

## AI-Guided Workflow (REQUIRED)

### Step 1: Understand Request
When user requests an animation, internally draft:
- Topic and scope
- Content structure
- Visual elements needed

### Step 2: Ask User Preferences
**MUST use AskUserQuestion tool:**
- Audio preference (With TTS / Without)
- Duration preference (Short / Medium / Long / Auto)

### Step 3: Present Plan
Show content plan before coding:
```
📋 Animation Plan: [Topic]

1. Hook: [Opening question]
2. Setup: [Context]
3. Core: [Main explanation]
4. Example: [Demonstration]
5. Takeaway: [Conclusion]

Settings: Audio=Yes, Duration=~90s

Proceed?
```

### Step 4: Execute Workflow

| With Audio | Without Audio |
|------------|---------------|
| Script → TTS → Measure → Animate → Render → Combine | Estimate → Animate → Render |

---

## Critical Rules Summary

### MUST DO
- Use `#1c1c1c` background color
- Group related elements with VGroup
- Use LaggedStartMap for cascading effects
- Save/restore state for reversible transforms
- Build complexity progressively
- Add end padding (1.5-2s) to video
- Verify video duration >= audio duration

### MUST NOT
- Create static frames (always have subtle motion)
- Recreate elements each segment (keep persistent)
- Use sequential FadeOut then FadeIn (overlap them)
- End with play() without wait()
- Hardcode arbitrary durations

---

## Example Scene Pattern

```python
from manim import *

class ExplanationScene(Scene):
    """3b1b style explanation with seamless transitions."""

    def construct(self):
        self.camera.background_color = "#1c1c1c"

        # Persistent elements - created ONCE
        self.main_group = self._setup()

        # Segments modify existing elements
        self.seg_hook()
        self.seg_setup()
        self.seg_core()
        self.seg_example()
        self.seg_takeaway()

        # End padding
        self.wait(2)

    def _setup(self):
        """Create all persistent visual elements."""
        pass

    def seg_hook(self):
        """Pose the opening question."""
        pass

    def seg_setup(self):
        """Establish context."""
        pass

    def seg_core(self):
        """Main explanation with progressive complexity."""
        pass

    def seg_example(self):
        """Concrete demonstration."""
        pass

    def seg_takeaway(self):
        """Conclusion and cleanup."""
        pass
```

---

## Version History

- **1.1.0**: Added animation-patterns, seamless-transitions, mobject-grouping, updaters, text-transforms, helpers-template based on 3b1b/videos and remotion-dev/skills analysis
- **1.0.0**: Initial release
