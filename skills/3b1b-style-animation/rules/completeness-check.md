---
name: completeness-check
description: Validation checklist to ensure explanations are complete before rendering
metadata:
  tags: validation, completeness, quality, checklist
priority: highest
---

# Completeness Validation

**Before rendering, every explanation must pass this checklist.**

## Mandatory Completeness Criteria

### 1. Narrative Arc (All Required)

```
□ HOOK: Does it start with an engaging question or problem?
□ SETUP: Is the context/background established?
□ CORE: Is the main concept fully explained?
□ EXAMPLE: Is there at least one concrete demonstration?
□ CONCLUSION: Does it wrap up with a clear takeaway?
```

### 2. No Dangling Concepts

```
□ Every term used is defined or commonly known
□ Every symbol is explained before use
□ Every step is justified ("because...", "this works since...")
□ No "magic" happens without explanation
```

### 3. Visual Completeness

```
□ All elements properly visible (no cut-off text/objects)
□ No overlapping elements
□ Important elements have visual emphasis
□ Animation ends in a clean state (not mid-transition)
```

### 4. Logical Flow

```
□ Can follow from start to finish without confusion
□ Transitions between topics are smooth
□ Order makes sense (prerequisites before dependencies)
□ No unexplained jumps
```

## Automated Validation Script

```python
#!/usr/bin/env python3
"""
completeness_validator.py - Check if explanation is complete
"""

class CompletenessValidator:
    """Validate explanation completeness before rendering."""

    def __init__(self, scene_script: str):
        self.script = scene_script
        self.issues = []
        self.warnings = []

    def validate(self) -> bool:
        """Run all validation checks."""
        self.check_narrative_arc()
        self.check_timing()
        self.check_visual_elements()
        self.check_text_content()

        return len(self.issues) == 0

    def check_narrative_arc(self):
        """Verify narrative structure exists."""

        required_sections = {
            'hook': ['question', 'problem', 'why', 'how does'],
            'setup': ['let\'s', 'consider', 'start with', 'given'],
            'explanation': ['because', 'this means', 'notice', 'key'],
            'conclusion': ['therefore', 'so we', 'result', 'takeaway', 'summary']
        }

        script_lower = self.script.lower()

        for section, keywords in required_sections.items():
            if not any(kw in script_lower for kw in keywords):
                self.issues.append(f"Missing {section.upper()} section")

    def check_timing(self):
        """Check for appropriate pacing."""

        # Count wait() calls
        wait_count = self.script.count('self.wait')
        play_count = self.script.count('self.play')

        if play_count > 0 and wait_count < play_count / 3:
            self.warnings.append(
                f"Low pause ratio: {wait_count} waits for {play_count} animations. "
                "Viewers may not have time to process."
            )

    def check_visual_elements(self):
        """Check for proper visual handling."""

        # Check for edge placement without buffer
        if 'to_edge(' in self.script and 'buff=' not in self.script:
            self.warnings.append(
                "Edge placement without explicit buffer - may crowd screen edge"
            )

        # Check for proper cleanup
        if 'FadeOut' not in self.script and 'self.clear()' not in self.script:
            self.warnings.append(
                "No FadeOut or clear() - scene may end cluttered"
            )

    def check_text_content(self):
        """Check text/narration completeness."""

        # Look for incomplete sentences
        incomplete_patterns = ['...', 'etc', 'and so on', 'you get the idea']
        for pattern in incomplete_patterns:
            if pattern in self.script:
                self.warnings.append(
                    f"Found '{pattern}' - may indicate incomplete explanation"
                )

    def report(self):
        """Print validation report."""
        print("\n" + "=" * 50)
        print("COMPLETENESS VALIDATION REPORT")
        print("=" * 50)

        if self.issues:
            print("\n❌ ISSUES (must fix):")
            for issue in self.issues:
                print(f"   • {issue}")

        if self.warnings:
            print("\n⚠️  WARNINGS (should review):")
            for warning in self.warnings:
                print(f"   • {warning}")

        if not self.issues and not self.warnings:
            print("\n✅ All checks passed!")

        print("\n" + "=" * 50)
        return len(self.issues) == 0
```

## Per-Topic Completeness Requirements

### Algorithm Explanations

```
□ Problem statement clearly defined
□ Input/output specification
□ Why naive approach doesn't work (if applicable)
□ Key insight that makes algorithm work
□ Step-by-step walkthrough with example
□ Time/space complexity mentioned
□ Edge cases addressed (or noted as out of scope)
```

### Mathematical Concept Explanations

```
□ Intuitive explanation before formal definition
□ At least 2 examples (one simple, one slightly complex)
□ Visual representation of the concept
□ Connection to related/familiar concepts
□ Common misconceptions addressed
□ When/why to use this concept
```

### Proof Explanations

```
□ Theorem statement in plain language
□ Why we should believe it (intuition)
□ Proof strategy overview
□ Each step justified
□ Key insight highlighted
□ Implications discussed
```

## Scene Completeness Checklist Template

```python
"""
Copy this to your scene file and fill in before rendering.
"""

COMPLETENESS_CHECKLIST = """
Scene: [SCENE_NAME]
Topic: [TOPIC]
Duration: [TARGET_DURATION]

NARRATIVE:
[x] Hook/Question posed at start
[x] Context established
[x] Core concept explained
[x] Example demonstrated
[ ] Summary/takeaway at end       ← INCOMPLETE

CONTENT:
[x] All terms defined
[x] All steps justified
[ ] No unexplained jumps          ← NEEDS REVIEW

VISUAL:
[x] No overlapping elements
[x] Proper spacing
[x] Clean ending state

NOTES:
- Need to add final summary section
- Consider adding second example
"""
```

## Quick Pre-Render Validation

Before running `manim -pqh`:

```bash
# 1. Read through your script and answer:

# Does it answer "why should I care"?
# YES / NO

# Does it explain "what it is"?
# YES / NO

# Does it show "how it works"?
# YES / NO

# Does it have a clear ending?
# YES / NO

# If any NO → fix before rendering
```

## Common Incompleteness Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Abrupt ending | Scene stops without summary | Add conclusion section |
| Missing "why" | Dives into "what" without motivation | Add hook at start |
| Assumed knowledge | Uses undefined terms | Add brief definitions |
| Visual clutter | Elements pile up | Add FadeOut/cleanup |
| No examples | Pure abstraction | Add concrete demonstration |
| Rushed finale | Summary too brief | Extend conclusion, add recap |

## Enforcing Completeness

### Scene Template with Built-in Checks

```python
class CompleteExplanationScene(Scene):
    """Base class that enforces completeness."""

    # Override these in subclass
    TOPIC = "Unnamed Topic"
    TARGET_DURATION = 60  # seconds

    REQUIRED_SECTIONS = [
        "hook",
        "setup",
        "explanation",
        "example",
        "conclusion"
    ]

    def __init__(self):
        super().__init__()
        self.completed_sections = set()

    def mark_section(self, section_name):
        """Mark a section as complete."""
        if section_name in self.REQUIRED_SECTIONS:
            self.completed_sections.add(section_name)

    def construct(self):
        """Main construct - calls section methods."""
        self.section_hook()
        self.mark_section("hook")

        self.section_setup()
        self.mark_section("setup")

        self.section_explanation()
        self.mark_section("explanation")

        self.section_example()
        self.mark_section("example")

        self.section_conclusion()
        self.mark_section("conclusion")

        # Validate at end
        self.validate_completeness()

    def validate_completeness(self):
        """Check all sections were completed."""
        missing = set(self.REQUIRED_SECTIONS) - self.completed_sections
        if missing:
            print(f"⚠️  WARNING: Missing sections: {missing}")

    # Override these in subclass
    def section_hook(self):
        raise NotImplementedError("Must implement hook section")

    def section_setup(self):
        raise NotImplementedError("Must implement setup section")

    def section_explanation(self):
        raise NotImplementedError("Must implement explanation section")

    def section_example(self):
        raise NotImplementedError("Must implement example section")

    def section_conclusion(self):
        raise NotImplementedError("Must implement conclusion section")
```

### Usage

```python
class MyExplanation(CompleteExplanationScene):
    TOPIC = "Dijkstra's Algorithm"
    TARGET_DURATION = 60

    def section_hook(self):
        # Your hook code...
        pass

    def section_setup(self):
        # Your setup code...
        pass

    # ... etc
```

If any section is missing, you'll get a warning before render completes.
