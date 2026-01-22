---
name: 3b1b-style-animation-skill
description: Create pedagogically-focused mathematical animations in 3Blue1Brown style using Manim
metadata:
  author: subinium
  version: 1.0.0
  tags: manim, 3b1b, math, education, pedagogy, visualization
---

# 3Blue1Brown Style Mathematical Animations

Use this skill when creating mathematical animations, visualizations, or educational videos about math, algorithms, or deep learning.

## Core Philosophy

> "The goal is not to animate math, but to build understanding."

1. **Intuition Before Formalism** — Build visual understanding before showing formulas
2. **Why Before What** — Motivate concepts before defining them
3. **Concrete Before Abstract** — Start with specific examples, then generalize
4. **Show, Don't Tell** — Let the visual do the explaining

## When to Use

- Creating mathematical animations with Manim
- Explaining algorithms visually
- Building deep learning visualizations
- Producing educational video content

---

## AI-Guided Planning (REQUIRED)

**Before starting any video, follow this workflow:**

### Step 1: Draft Plan Internally

When user requests an animation:
- Understand the topic
- Draft content structure
- Identify visual elements needed

### Step 2: Ask User Preferences

**Use AskUserQuestion tool to gather preferences:**

```python
questions = [
    {
        "question": "Do you want narration audio in this video?",
        "header": "Audio",
        "options": [
            {"label": "With Audio (Recommended)", "description": "TTS narration synced to animation"},
            {"label": "Without Audio", "description": "Animation only, add your own audio later"}
        ],
        "multiSelect": False
    },
    {
        "question": "How long should the video be?",
        "header": "Duration",
        "options": [
            {"label": "Short (30-60s)", "description": "Quick concept overview"},
            {"label": "Medium (1-2 min)", "description": "Standard explanation"},
            {"label": "Long (3+ min)", "description": "Deep dive with examples"},
            {"label": "Auto (Recommended)", "description": "Let content determine length"}
        ],
        "multiSelect": False
    }
]
```

### Step 3: Present Plan for Approval

Show the content plan before coding:

```
📋 Animation Plan: [Topic]

1. Hook: [Opening question]
2. Setup: [Context]
3. Core: [Main explanation]
4. Example: [Demonstration]
5. Takeaway: [Conclusion]

Settings: Audio=Yes, Duration=Auto (~70s)

Shall I proceed?
```

### Step 4: Execute Based on Choices

| Choice | Workflow |
|--------|----------|
| With Audio | Script → TTS → Measure Duration → Code Animation → Render → Combine |
| Without Audio | Estimate Timing → Code Animation → Render |

---

## Key Principles

### Duration is NOT Fixed

```python
# ❌ WRONG: Force fixed duration
duration = 60  # arbitrary

# ✅ RIGHT: Content determines duration
script = write_explanation(topic)
duration = measure(script)  # natural length
```

### Always Ask, Never Assume

- Audio preference
- Duration preference
- Detail level (if relevant)

---

## Rules Index

### Highest Priority: Quality & Planning

| Rule | Description |
|------|-------------|
| `rules/visual-quality.md` | **CRITICAL** - No overlaps, readable text, clear hierarchy |
| `rules/pre-production.md` | AI-guided planning with user interaction |
| `rules/layout-spacing.md` | Screen zones, spacing, margins |

### High Priority: Pedagogy & Content

| Rule | Description |
|------|-------------|
| `rules/pedagogy.md` | Teaching philosophy and explanation structures |
| `rules/mathematical-rigor.md` | Ensuring mathematical correctness |
| `rules/narrative-flow.md` | Smooth transitions and completeness |
| `rules/audio-sync.md` | Synchronizing narration with visuals |

### Visual Design

| Rule | Description |
|------|-------------|
| `rules/color-scheme.md` | 3b1b color palette and semantic meaning |
| `rules/scene-basics.md` | Animation timing and sequencing |
| `rules/camera-work.md` | Focus, zoom, and visual hierarchy |

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
| `rules/attention.md` | Attention mechanism |
| `rules/transformer-block.md` | Transformer architecture |

### Domain: CNN

| Rule | Description |
|------|-------------|
| `rules/convolution.md` | Convolution operation |
| `rules/feature-maps.md` | Feature map visualization |
| `rules/pooling.md` | Pooling operations |

### Technical

| Rule | Description |
|------|-------------|
| `rules/manim-setup.md` | Installation and configuration |
| `rules/narration.md` | TTS integration and script writing |

---

## Example Interaction

```
User: "quick sort 애니메이션 만들어줘"

AI: [Internal: Draft plan for QuickSort]

AI: [AskUserQuestion]
    "I'll create a QuickSort animation. Quick questions:

    1. Audio: With narration / Without
    2. Duration: Short / Medium / Auto"

User: "audio 있고, auto로"

AI: "Here's my plan:

    📋 QuickSort Animation

    1. Hook: How do we sort efficiently?
    2. Setup: Unsorted array
    3. Core: Pivot selection, partitioning
    4. Example: Sort [8,3,7,1,5,2]
    5. Takeaway: O(n log n) average

    Duration: ~90s (based on narration)

    Proceed?"

User: "네"

AI: [Executes workflow]
    → Generates TTS
    → Measures timing
    → Creates animation
    → Renders & combines
    → Shows result
```

---

## Quick Start Code

```python
from manim import *

class ExplanationScene(Scene):
    def construct(self):
        self.camera.background_color = "#1c1c1c"

        # Sync to audio timing (if audio enabled)
        # TIMING = {...}  # from TTS generation

        # 1. Hook: Pose the question
        # 2. Intuition: Build visual understanding
        # 3. Formalize: Show the math
        # 4. Verify: Demonstrate with example
```
