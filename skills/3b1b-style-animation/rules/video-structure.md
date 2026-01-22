---
name: video-structure
description: Guidelines for structuring videos of different lengths
metadata:
  tags: structure, pacing, length, chapters
priority: high
---

# Video Structure and Length Guidelines

From 10-second clips to 30-minute deep dives, structure changes everything.

## Video Length Categories

### Micro (10-30 seconds)
**Purpose**: Single concept, visual proof, or "aha" moment

```python
class MicroVideo(Scene):
    """Single concept, no setup needed."""

    def construct(self):
        # Immediate hook - show the interesting thing
        self.show_key_visual()      # 5-10 sec

        # The transformation/insight
        self.show_transformation()   # 10-15 sec

        # Result/punchline
        self.show_result()          # 5 sec
```

**Example**: "Watch what happens when you square a complex number on the unit circle"

### Short (1-3 minutes)
**Purpose**: Explain one concept with context

```python
class ShortVideo(Scene):
    """One concept with proper setup."""

    def construct(self):
        # Hook: Why should I care? (10-15 sec)
        self.pose_question()

        # Build intuition (30-60 sec)
        self.build_visual_intuition()

        # Show the math (30-60 sec)
        self.formalize_concept()

        # Verify/apply (15-30 sec)
        self.demonstrate_application()
```

**Example**: "Why does the GCD algorithm work?"

### Medium (5-10 minutes)
**Purpose**: Complete topic coverage with multiple sub-concepts

```python
class MediumVideo(Scene):
    """Multiple related concepts, chapter structure."""

    def construct(self):
        # Chapter 1: Setup & Motivation (1-2 min)
        self.chapter_1_introduction()

        # Chapter 2: Core Concept (2-3 min)
        self.chapter_2_main_idea()

        # Chapter 3: Going Deeper (2-3 min)
        self.chapter_3_implications()

        # Chapter 4: Summary & Connections (1-2 min)
        self.chapter_4_wrap_up()
```

**Example**: "Understanding Eigenvectors and Eigenvalues"

### Long (15-30+ minutes)
**Purpose**: Deep dive, multiple interconnected topics

```
Structure:
1. Opening hook (30 sec - 1 min)
2. Roadmap: "Here's what we'll cover..." (30 sec)
3. Chapter 1 with mini-summary (3-5 min)
4. Chapter 2 with mini-summary (3-5 min)
5. Chapter 3 with mini-summary (3-5 min)
6. [More chapters as needed]
7. Grand synthesis: connecting everything (2-3 min)
8. Closing thoughts & next steps (1 min)
```

## Pacing Guidelines

### Time Per Concept

| Concept Complexity | Minimum Time | Recommended Time |
|-------------------|--------------|------------------|
| Simple definition | 10 sec | 20-30 sec |
| Visual transformation | 15 sec | 30-45 sec |
| Step-by-step process | 30 sec | 1-2 min |
| Proof/derivation | 1 min | 2-4 min |
| Complex insight | 45 sec | 1.5-3 min |

### Animation Timing Rules

```python
# Timing constants for different video lengths

# For MICRO videos (fast-paced)
MICRO_TIMING = {
    "create_object": 0.5,
    "transform": 1.0,
    "wait_after_key_point": 0.5,
    "fade_transition": 0.3,
}

# For SHORT videos (moderate pace)
SHORT_TIMING = {
    "create_object": 0.8,
    "transform": 1.5,
    "wait_after_key_point": 1.0,
    "fade_transition": 0.5,
}

# For MEDIUM/LONG videos (relaxed pace)
STANDARD_TIMING = {
    "create_object": 1.0,
    "transform": 2.0,
    "wait_after_key_point": 1.5,
    "fade_transition": 0.7,
}

# For COMPLEX explanations (extra time to think)
DEEP_TIMING = {
    "create_object": 1.2,
    "transform": 2.5,
    "wait_after_key_point": 2.0,
    "fade_transition": 0.8,
}
```

## Scene Organization for Long Videos

### Multi-Scene Architecture

```python
# config.py - Shared configuration
VIDEO_CONFIG = {
    "video_length": "medium",  # micro, short, medium, long
    "target_duration_minutes": 8,
    "chapters": [
        {"name": "Introduction", "duration": 1.5},
        {"name": "Core Concept", "duration": 3},
        {"name": "Applications", "duration": 2.5},
        {"name": "Summary", "duration": 1},
    ]
}

# chapter_1.py
class Chapter1_Introduction(Scene):
    def construct(self):
        self.section_title("Chapter 1: Introduction")
        # ... content

# chapter_2.py
class Chapter2_CoreConcept(Scene):
    def construct(self):
        self.section_title("Chapter 2: The Core Idea")
        # ... content

# main.py - Combines all chapters
# manim -pqh chapter_1.py chapter_2.py ... -o full_video.mp4
```

### Chapter Transitions

```python
def chapter_transition(self, title, subtitle=None):
    """Smooth transition between chapters."""
    # Fade out current content
    self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)

    # Chapter card
    chapter_title = Text(title, font_size=48)
    if subtitle:
        chapter_subtitle = Text(subtitle, font_size=28, color=GRAY)
        chapter_subtitle.next_to(chapter_title, DOWN, buff=0.3)
        chapter_group = VGroup(chapter_title, chapter_subtitle)
    else:
        chapter_group = chapter_title

    self.play(FadeIn(chapter_group, scale=0.9), run_time=0.8)
    self.wait(1.5)
    self.play(FadeOut(chapter_group), run_time=0.5)
```

### Progress Indicators for Long Videos

```python
def add_progress_bar(self, current_chapter, total_chapters):
    """Show viewer where they are in the video."""
    bar_width = 10
    progress = current_chapter / total_chapters

    background = Rectangle(
        width=bar_width, height=0.1,
        color=GRAY, fill_opacity=0.3
    )
    fill = Rectangle(
        width=bar_width * progress, height=0.1,
        color=BLUE, fill_opacity=0.8
    )
    fill.align_to(background, LEFT)

    progress_bar = VGroup(background, fill)
    progress_bar.to_edge(DOWN, buff=0.2)

    return progress_bar
```

## Content Scaling Strategies

### Expanding a Concept (More Time)

```python
# Original 30-second version
def quick_gcd(self):
    self.show_algorithm()
    self.show_result()

# Expanded 3-minute version
def detailed_gcd(self):
    self.motivate_problem()           # Why do we need GCD?
    self.show_naive_approach()        # Listing all divisors
    self.introduce_euclidean()        # Better way
    self.step_by_step_walkthrough()   # Detailed steps
    self.visual_proof()               # Why it works
    self.show_result()                # Final answer
```

### Compressing a Concept (Less Time)

```python
# If short on time, prioritize:
# 1. The key visual insight (KEEP)
# 2. One concrete example (KEEP)
# 3. The formula/algorithm (KEEP if essential)
# 4. Proof details (COMPRESS or CUT)
# 5. Multiple examples (CUT)
# 6. Historical context (CUT)
```

## User Prompting Guidelines

### Specifying Video Length

When a user requests a video, they should specify:

```
"Create a [LENGTH] video explaining [TOPIC]"

LENGTH options:
- "quick/micro" → 10-30 seconds
- "short" → 1-3 minutes
- "standard" → 5-10 minutes
- "detailed/long" → 15-30 minutes
- "comprehensive" → 30+ minutes
- Explicit: "5 minute video"
```

### Prompting for Structure

```
"Create a 5-minute video on eigenvalues with:
- 1 min intro/motivation
- 2 min core concept with examples
- 1.5 min applications
- 30 sec summary"
```

### Prompting for Pacing

```
"Create a video on GCD with slow pacing for beginners"
"Create a rapid overview of linear transformations for review"
```

## Length Estimation

### Rule of Thumb

```python
def estimate_video_length(script):
    """Estimate video duration from content."""

    # Count elements
    n_concepts = count_new_concepts(script)
    n_examples = count_examples(script)
    n_proofs = count_proofs(script)
    n_transitions = count_scene_changes(script)

    # Time estimates (in seconds)
    time = (
        n_concepts * 45 +      # 45 sec per new concept
        n_examples * 30 +      # 30 sec per example
        n_proofs * 120 +       # 2 min per proof
        n_transitions * 5 +    # 5 sec per transition
        30                     # Buffer for intro/outro
    )

    return time / 60  # Return in minutes
```

### Self-Check

After writing, estimate if your video will be:
- Too short? Add examples, deeper explanations
- Too long? Cut redundancy, simplify proofs
- Just right? Verify pacing feels natural

## Output Format Guidelines

### Render Quality by Purpose

```bash
# Preview/draft (fast)
manim -pql scene.py ClassName

# Review quality
manim -pqm scene.py ClassName

# Final production
manim -pqh scene.py ClassName

# 4K production
manim -qk scene.py ClassName
```

### Combining Multiple Scenes

```bash
# Render chapters separately, combine with ffmpeg
manim -qh chapter1.py Chapter1 -o chapter1.mp4
manim -qh chapter2.py Chapter2 -o chapter2.mp4

# Combine
ffmpeg -f concat -i filelist.txt -c copy full_video.mp4
```
