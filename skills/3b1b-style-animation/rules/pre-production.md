---
name: pre-production
description: AI-guided planning with user interaction for creating animations
metadata:
  tags: planning, workflow, interactive, flexible
priority: highest
---

# Pre-Production: AI-Guided Planning

**Core principle: AI plans, asks user preferences, then adapts the workflow.**

## Step 1: AI Creates Initial Plan

When user requests an animation, AI should:

1. **Understand the topic** - What concept to explain?
2. **Draft a content plan** - Structure, key points, visuals
3. **Ask user for preferences** - Before any code or audio generation

---

## Step 2: AI Recommends Duration Based on Content

**Before asking user, AI should analyze the topic and recommend appropriate duration.**

### Content Complexity Analysis

| Topic Type | Recommended Duration | Reason |
|------------|---------------------|--------|
| Simple concept (variable, loop) | 30-60s | Single idea, quick demo |
| Basic algorithm (linear search) | 1-2 min | Few steps to show |
| Standard algorithm (binary search, BFS) | 1-2 min | Multiple steps, one key insight |
| Complex algorithm (Dijkstra, DP) | 2-3 min | Multiple concepts, state tracking |
| Advanced topic (Transformer, backprop) | 3-5 min | Many interconnected ideas |

### How to Recommend

```python
# AI analyzes topic and recommends
def recommend_duration(topic):
    complexity = analyze_complexity(topic)

    if complexity == "simple":
        return "Short (30-60s)", "This is a simple concept"
    elif complexity == "standard":
        return "Medium (1-2 min)", "This needs proper explanation"
    elif complexity == "complex":
        return "Medium-Long (2-3 min)", "Multiple concepts to cover"
    elif complexity == "advanced":
        return "Long (3-5 min)", "Deep topic requiring careful build-up"
```

### Example Recommendations

| Topic | AI Recommendation |
|-------|-------------------|
| "DFS" | "Medium (1-2 min) - DFS is simple but needs backtracking demo" |
| "Dijkstra" | "Medium-Long (2-3 min) - Priority queue + multiple iterations" |
| "Quick Sort" | "Medium (1-2 min) - Partition concept + recursion" |
| "Attention mechanism" | "Long (3-5 min) - Q/K/V, dot product, softmax, multi-head" |
| "What is a stack?" | "Short (30-60s) - Simple data structure" |

---

## Step 3: Ask User with AI Recommendation

**Show AI recommendation, let user confirm or adjust:**

```python
# Include AI recommendation in the question
questions = [
    {
        "question": "Do you want narration audio?",
        "header": "Audio",
        "options": [
            {"label": "With Audio (Recommended)", "description": "TTS narration synced to animation"},
            {"label": "Without Audio", "description": "Animation only"}
        ],
        "multiSelect": False
    },
    {
        "question": "Duration: AI recommends Medium (1-2 min) for this topic. Adjust?",
        "header": "Duration",
        "options": [
            {"label": "Accept AI Recommendation", "description": "Medium (1-2 min) - good for this complexity"},
            {"label": "Shorter", "description": "Quick overview only"},
            {"label": "Longer", "description": "More detailed explanation"}
        ],
        "multiSelect": False
    }
]
```

### What to Include in Question

1. **AI's recommendation** - What AI thinks is appropriate
2. **Reason** - Why this duration makes sense
3. **User override** - Option to adjust if needed

**Note:** AI should guide, not just ask. Provide informed recommendations.

---

## Step 3: Present Plan for Approval

After gathering preferences, show the plan:

```markdown
## 📋 Animation Plan: [TOPIC]

### Content Structure
1. **Hook** (5s): [Opening question]
2. **Setup** (15s): [Context]
3. **Core** (30s): [Main explanation]
4. **Example** (20s): [Demonstration]
5. **Takeaway** (10s): [Conclusion]

### Settings
- Audio: With TTS narration
- Duration: ~80 seconds (auto from content)
- Voice: en-US-GuyNeural

### Visual Elements
- [ ] Element 1
- [ ] Element 2

Shall I proceed with this plan?
```

---

## Step 4: Adaptive Workflow

Based on user choices, follow the appropriate workflow:

### With Audio (Explanation-First)
```
Plan → Script → Generate TTS → Measure Duration → Code Animation → Render → Combine
```

Duration is determined by the narration content, not pre-set.

### Without Audio
```
Plan → Estimate Timing from Content → Code Animation → Render
```

Duration is estimated based on content complexity.

---

## Duration Guidelines (Not Fixed!)

Duration should be **content-driven**, not arbitrary:

| Content Type | Typical Duration | Adjust By |
|--------------|------------------|-----------|
| Simple concept | 30-60s | User preference |
| Algorithm walkthrough | 1-2 min | Number of steps |
| Deep explanation | 3-5 min | Depth requested |
| Quick demo | 15-30s | Scope |

**Key: Let the explanation determine length, not the other way around.**

```python
# BAD: Force content into fixed duration
def plan_video():
    duration = 60  # Fixed!
    squeeze_content_into(duration)  # ❌

# GOOD: Let content determine duration
def plan_video():
    script = write_natural_explanation()
    duration = measure_script_duration(script)  # ✅
```

---

## Workflow Decision Tree

```
User requests animation
        │
        ▼
┌───────────────────┐
│  AI drafts plan   │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  Ask preferences  │◄── AskUserQuestion
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  Show plan for    │
│    approval       │
└─────────┬─────────┘
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
  Audio?      No Audio?
    │           │
    ▼           ▼
  Script     Estimate
  + TTS      timing
    │           │
    ▼           ▼
  Measure    Code
  duration   animation
    │           │
    ▼           ▼
  Code       Render
  animation     │
    │           │
    ▼           │
  Render        │
    │           │
    ▼           │
  Combine ◄─────┘
    │
    ▼
  Show result
```

---

## Example Interaction

```
User: "binary search 애니메이션 만들어줘"

AI: [Creates draft plan internally]

AI: [Uses AskUserQuestion]
    "I'll create a Binary Search animation. A few questions:"

    1. Audio: With narration (Recommended) / Without
    2. Duration: Short (30-60s) / Medium (1-2min) / Auto
    3. Language: English / Korean

User: "With audio, auto duration, English"

AI: [Shows plan]
    "Here's my plan:

    1. Hook: How do you find a word in a dictionary?
    2. Setup: Sorted array visualization
    3. Core: Binary search steps
    4. Example: Find 23 in [3,7,11,15,19,23,27,31]
    5. Takeaway: O(log n) complexity

    Estimated: ~70 seconds based on narration

    Shall I proceed?"

User: "네, 진행해"

AI: [Executes workflow]
    - Generates TTS
    - Measures actual timing (68.5s)
    - Creates synced animation
    - Renders and combines
    - Shows result
```

---

## Code Implementation

### Asking Preferences

```python
# Use AskUserQuestion tool
questions = [
    {
        "question": "Do you want narration audio?",
        "header": "Audio",
        "options": [
            {"label": "With Audio", "description": "TTS narration synced to animation"},
            {"label": "Without Audio", "description": "Animation only"}
        ],
        "multiSelect": False
    }
]
```

### With Audio Workflow

```python
# 1. Write script based on content (not fixed duration)
SCRIPT = [
    {"id": "01_hook", "text": "..."},
    {"id": "02_setup", "text": "..."},
    # Length determined by what needs to be explained
]

# 2. Generate TTS and get real durations
async def generate_audio(script):
    timing = []
    for seg in script:
        # Generate and measure
        duration = await tts_generate(seg["text"])
        timing.append({"id": seg["id"], "duration": duration, ...})
    return timing  # Actual durations, not estimates

# 3. Animation matches measured audio
TIMING = {...}  # From step 2

def segment(self, seg_id, anim_func):
    target = TIMING[seg_id]["end"] - TIMING[seg_id]["start"]
    # Animation pads to match audio
```

### Without Audio Workflow

```python
# Estimate based on content complexity
def estimate_section_duration(section_type, content_complexity):
    base = {"hook": 5, "setup": 15, "core": 30, "example": 20, "takeaway": 10}
    multiplier = {"simple": 0.7, "medium": 1.0, "detailed": 1.5}
    return base[section_type] * multiplier[content_complexity]
```

---

## Key Principles

1. **Plan first** - Understand content before coding
2. **Ask, don't assume** - Get user preferences
3. **Content drives duration** - Don't force arbitrary lengths
4. **Adapt workflow** - Different needs, different approaches
5. **Show before doing** - Get approval on plan

---

## Anti-Patterns to Avoid

```python
# ❌ BAD: Fixed 60-second video
total_duration = 60
sections = divide_equally(total_duration, 5)

# ❌ BAD: Skip asking preferences
def create_video():
    # Just start coding without asking

# ❌ BAD: Stretch content to fill time
animation_time = 60
actual_content = 30
padding = 30  # Awkward silence

# ✅ GOOD: Let content determine length
script = write_natural_explanation(topic)
audio = generate_tts(script)
duration = measure_audio(audio)  # Whatever it naturally is
```
