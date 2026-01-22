---
name: narrative-flow
description: Ensuring smooth transitions, complete explanations, and user-friendly narrative
metadata:
  tags: narrative, transitions, flow, completeness, user-experience
priority: highest
---

# Narrative Flow and Completeness

Every video should feel like a complete journey, not a fragmented collection of scenes.

## The Completeness Checklist

Before considering a video "done," verify:

### Opening (Hook)
- [ ] Does it grab attention in the first 5 seconds?
- [ ] Is the "why should I care?" question answered?
- [ ] Is the problem/goal clearly stated?

### Middle (Explanation)
- [ ] Is every new concept introduced before being used?
- [ ] Are there smooth transitions between topics?
- [ ] Is each step justified ("Here's why we do this...")?
- [ ] Are there enough examples?

### Ending (Resolution)
- [ ] Is there a clear conclusion/summary?
- [ ] Does it answer the opening question?
- [ ] Is there a satisfying "aha!" moment?
- [ ] Does it connect back to the bigger picture?

## Transition Techniques

### Between Concepts

```python
# ❌ BAD: Abrupt jump
self.play(FadeOut(concept_A))
self.play(FadeIn(concept_B))  # Where did this come from?

# ✅ GOOD: Bridge with explanation
self.play(FadeOut(concept_A))

bridge = Text("Now that we understand X, let's see how it connects to Y...")
self.play(Write(bridge))
self.wait(2)

self.play(FadeOut(bridge))
self.play(FadeIn(concept_B))
```

### Verbal Bridges (for Narration)

Use transitional phrases:

| From → To | Bridge Phrase |
|-----------|---------------|
| Problem → Solution | "So how do we solve this?" |
| Theory → Practice | "Let's see this in action..." |
| Simple → Complex | "Now let's extend this idea..." |
| Step N → Step N+1 | "With that done, we can now..." |
| Example → Generalization | "This pattern holds in general..." |
| Confusion → Clarity | "Here's the key insight..." |

### Visual Bridges

```python
def visual_transition(self, from_obj, to_obj, bridge_text=None):
    """Smooth transition between concepts."""

    if bridge_text:
        text = Text(bridge_text, font_size=24, color=GRAY)
        text.to_edge(DOWN)
        self.play(Write(text), from_obj.animate.scale(0.8).set_opacity(0.5))
        self.wait(1.5)
        self.play(FadeOut(from_obj), FadeOut(text))
    else:
        self.play(FadeOut(from_obj))

    self.wait(0.5)  # Brief pause
    self.play(FadeIn(to_obj))
```

## Ensuring Complete Explanations

### The "Why-What-How" Framework

Every concept needs all three:

```python
class CompleteExplanation:
    """Structure for a complete explanation."""

    def explain_concept(self, concept_name):
        # 1. WHY - Motivation (don't skip this!)
        self.show_why_we_need_this()

        # 2. WHAT - Definition/Description
        self.show_what_it_is()

        # 3. HOW - Mechanics/Process
        self.show_how_it_works()

        # 4. VERIFY - Example/Application
        self.show_example()

        # 5. CONNECT - Link to bigger picture
        self.connect_to_context()
```

### Required Elements for Each Concept

```python
CONCEPT_REQUIREMENTS = {
    "definition": {
        "must_have": ["intuitive_explanation", "formal_definition", "example"],
        "nice_to_have": ["counter_example", "edge_cases"]
    },
    "algorithm": {
        "must_have": ["problem_statement", "key_insight", "step_by_step", "example_run"],
        "nice_to_have": ["complexity_analysis", "optimization"]
    },
    "theorem": {
        "must_have": ["statement", "intuition", "proof_sketch", "application"],
        "nice_to_have": ["full_proof", "generalizations"]
    }
}
```

## Scene Structure Templates

### Minimum Viable Explanation (2-3 min)

```
[0:00-0:15] HOOK: Interesting question or problem
[0:15-0:30] SETUP: What we need to understand
[0:30-1:30] CORE: Main concept with visual
[1:30-2:00] EXAMPLE: Concrete demonstration
[2:00-2:30] SUMMARY: Key takeaway
```

### Standard Explanation (5-7 min)

```
[0:00-0:30] HOOK: Why this matters
[0:30-1:00] CONTEXT: What we already know
[1:00-2:00] PROBLEM: What we're trying to solve
[2:00-3:30] INSIGHT: The key idea
[3:30-5:00] MECHANICS: How it works step-by-step
[5:00-6:00] EXAMPLES: See it in action
[6:00-6:30] EXTENSIONS: What else can we do?
[6:30-7:00] SUMMARY: Wrap up
```

### Deep Dive (10-15 min)

```
[0:00-1:00] HOOK + ROADMAP
[1:00-3:00] BACKGROUND: Required concepts
[3:00-5:00] PROBLEM: Detailed problem statement
[5:00-7:00] APPROACH: Building intuition
[7:00-10:00] SOLUTION: Full explanation
[10:00-12:00] EXAMPLES: Multiple examples
[12:00-14:00] IMPLICATIONS: What this means
[14:00-15:00] SUMMARY + NEXT STEPS
```

## User-Friendly Practices

### Anticipate Confusion

```python
def explain_with_anticipation(self):
    """Address likely confusion points proactively."""

    # Main explanation
    self.show_main_concept()

    # Anticipate question
    question = Text("You might wonder: why not just...?", font_size=24, color=YELLOW)
    self.play(Write(question))
    self.wait(1)

    # Address it
    answer = Text("The reason is...", font_size=24)
    self.play(Transform(question, answer))
    self.show_reason()
```

### Provide Anchors

```python
def show_progress(self, current_step, total_steps, step_name):
    """Show viewers where they are in the explanation."""

    progress = Text(f"Step {current_step}/{total_steps}: {step_name}",
                   font_size=20, color=GRAY)
    progress.to_corner(UL)
    return progress
```

### Summarize Periodically

```python
def periodic_summary(self, points_so_far):
    """Recap what we've learned so far."""

    summary_title = Text("So far we've seen:", font_size=24)
    summary_title.to_edge(UP)

    points = VGroup()
    for i, point in enumerate(points_so_far):
        bullet = Text(f"• {point}", font_size=20)
        points.add(bullet)

    points.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    points.next_to(summary_title, DOWN, buff=0.5)

    self.play(Write(summary_title))
    for point in points:
        self.play(Write(point), run_time=0.5)

    self.wait(2)
    self.play(FadeOut(summary_title), FadeOut(points))
```

## Connecting Ideas

### Explicit Connections

```python
# Always connect new ideas to familiar ones

# ❌ BAD: Introduce without context
self.play(Write(Text("Dijkstra's algorithm uses a priority queue")))

# ✅ GOOD: Connect to what they know
connection = VGroup(
    Text("Remember how we always pick the closest node?", font_size=22),
    Text("↓", font_size=28),
    Text("A priority queue makes this fast!", font_size=22, color=GREEN)
).arrange(DOWN, buff=0.3)
self.play(Write(connection))
```

### Visual Callbacks

```python
def callback_to_earlier(self, earlier_mobject, connection_text):
    """Visually connect back to something shown earlier."""

    # Bring back earlier visual (faded)
    ghost = earlier_mobject.copy()
    ghost.set_opacity(0.3)
    ghost.to_edge(LEFT)

    self.play(FadeIn(ghost))

    # Show connection
    arrow = Arrow(ghost.get_right(), current.get_left(), color=YELLOW)
    label = Text(connection_text, font_size=18)
    label.next_to(arrow, UP)

    self.play(Create(arrow), Write(label))
```

## Avoiding Incomplete Explanations

### Signs of Incomplete Explanation

1. **"Just trust me"** - Never say this; always explain why
2. **Undefined terms** - Every term must be introduced first
3. **Magic steps** - Every step needs justification
4. **Missing examples** - Abstract ideas need concrete instances
5. **No summary** - Always conclude with key takeaways

### Self-Review Checklist

```python
COMPLETENESS_CHECK = """
Before finalizing, ask:

□ Could someone with no background follow this?
□ Did I explain WHY before HOW?
□ Is every symbol/term defined before use?
□ Are there enough pauses for comprehension?
□ Did I provide at least one concrete example?
□ Is there a clear beginning, middle, and end?
□ Does the ending resolve the opening question?
□ Are transitions smooth, not jarring?
□ Would I understand this if I saw it for the first time?
"""
```

## Common Flow Problems and Fixes

| Problem | Symptom | Fix |
|---------|---------|-----|
| Abrupt start | No context given | Add hook + problem statement |
| Lost viewer | Confused expressions | Add more transitions, slower pace |
| Missing "why" | Feels arbitrary | Add motivation before each concept |
| Jarring transitions | Sudden topic changes | Add bridge text/visuals |
| Weak ending | Fizzles out | Add summary + connection to bigger picture |
| Too fast | Can't process | Add pauses, repeat key points |
| No examples | Too abstract | Add concrete demonstration |
