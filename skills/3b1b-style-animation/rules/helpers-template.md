---
name: helpers-template
description: Helper function patterns from 3b1b video organization
metadata:
  tags: helpers, organization, reusable, functions, template
priority: high
---

# Helper Function Patterns

Organization patterns from 3Blue1Brown's video code structure.

## Project Structure

**MUST** organize complex projects with separate helper files.

```
my_video_project/
├── main.py           # Main scene file
├── helpers.py        # Reusable helper functions
├── custom_mobjects.py # Custom visual elements
└── constants.py      # Colors, sizes, configuration
```

---

## Pattern 1: Constants File

Centralize configuration values.

```python
# constants.py

# Colors (3b1b style)
BACKGROUND = "#1c1c1c"
PRIMARY = "#3b82f6"    # Blue
SECONDARY = "#fbbf24"  # Yellow
POSITIVE = "#22c55e"   # Green
NEGATIVE = "#ef4444"   # Red
NEUTRAL = "#6b7280"    # Gray

# Sizes
NODE_RADIUS = 0.3
EDGE_WIDTH = 2
FONT_SIZE_TITLE = 48
FONT_SIZE_BODY = 24
FONT_SIZE_LABEL = 20

# Spacing
MARGIN = 0.5
NODE_SPACING = 1.5
LAYER_SPACING = 2.0
```

## Pattern 2: Helper Functions

Reusable creation functions.

```python
# helpers.py
from manim import *
from constants import *


def create_node(label: str, position=ORIGIN, color=PRIMARY) -> VGroup:
    """Create a labeled node."""
    circle = Circle(radius=NODE_RADIUS, color=color, fill_opacity=0.3)
    circle.move_to(position)

    text = Text(label, font_size=FONT_SIZE_LABEL)
    text.move_to(circle.get_center())

    node = VGroup(circle, text)
    node.label = label  # Store for reference
    return node


def create_edge(start: VGroup, end: VGroup, weight=None, color=NEUTRAL) -> VGroup:
    """Create an edge between two nodes."""
    line = Line(
        start.get_center(),
        end.get_center(),
        color=color,
        stroke_width=EDGE_WIDTH
    )

    edge = VGroup(line)

    if weight is not None:
        mid = line.get_center()
        weight_label = Text(str(weight), font_size=FONT_SIZE_LABEL, color=NEUTRAL)
        weight_label.move_to(mid + UP * 0.2 + RIGHT * 0.2)
        edge.add(weight_label)

    return edge


def create_array(values: list, start_x=-4, box_size=0.7) -> VGroup:
    """Create an array visualization."""
    boxes = []
    labels = []

    for i, val in enumerate(values):
        box = Square(side_length=box_size, color=PRIMARY, fill_opacity=0.3)
        box.move_to([start_x + i * (box_size + 0.1), 0, 0])

        label = Text(str(val), font_size=FONT_SIZE_LABEL)
        label.move_to(box.get_center())

        boxes.append(box)
        labels.append(label)

    array = VGroup(*boxes, *labels)
    array.boxes = boxes
    array.labels = labels
    return array
```

## Pattern 3: Custom Mobject Class

Encapsulate complex visual elements.

```python
# custom_mobjects.py
from manim import *
from constants import *


class GraphNode(VGroup):
    """A graph node with label and state tracking."""

    def __init__(self, label: str, position=ORIGIN, **kwargs):
        super().__init__(**kwargs)

        self.node_label = label
        self.visited = False
        self.distance = float('inf')

        # Visual elements
        self.circle = Circle(radius=NODE_RADIUS, color=PRIMARY, fill_opacity=0.3)
        self.circle.move_to(position)

        self.label = Text(label, font_size=FONT_SIZE_LABEL)
        self.label.move_to(self.circle.get_center())

        self.add(self.circle, self.label)

    def highlight(self):
        """Highlight this node."""
        self.circle.set_stroke(SECONDARY, width=4)

    def unhighlight(self):
        """Remove highlight."""
        self.circle.set_stroke(PRIMARY, width=2)

    def mark_visited(self):
        """Mark as visited."""
        self.visited = True
        self.circle.set_fill(POSITIVE, opacity=0.4)


class DPTable(VGroup):
    """A dynamic programming table visualization."""

    def __init__(self, headers: list, rows: list, **kwargs):
        super().__init__(**kwargs)

        self.cells = {}
        self.header_texts = []
        self.row_texts = []

        # Create header
        header_group = VGroup()
        for i, h in enumerate(headers):
            text = Text(h, font_size=FONT_SIZE_LABEL, color=NEUTRAL)
            text.move_to([i * 1.2, 0, 0])
            header_group.add(text)
            self.header_texts.append(text)

        # Create rows
        row_groups = VGroup()
        for r_idx, row in enumerate(rows):
            row_group = VGroup()
            for c_idx, val in enumerate(row):
                text = Text(str(val), font_size=FONT_SIZE_LABEL)
                text.move_to([c_idx * 1.2, -(r_idx + 1) * 0.6, 0])
                row_group.add(text)
                self.cells[(r_idx, c_idx)] = text
            row_groups.add(row_group)
            self.row_texts.append(row_group)

        self.add(header_group, row_groups)

    def update_cell(self, row: int, col: int, value, scene: Scene):
        """Animate updating a cell value."""
        old_text = self.cells[(row, col)]
        new_text = Text(str(value), font_size=FONT_SIZE_LABEL, color=POSITIVE)
        new_text.move_to(old_text.get_center())

        scene.play(Transform(old_text, new_text), run_time=0.3)
        self.cells[(row, col)] = old_text
```

## Pattern 4: Animation Helper Functions

Reusable animation patterns.

```python
# helpers.py (continued)

def cascade_fade_in(scene: Scene, elements: list, lag=0.1):
    """Fade in elements with cascade effect."""
    scene.play(
        LaggedStartMap(FadeIn, VGroup(*elements), lag_ratio=lag),
        run_time=1
    )


def highlight_path(scene: Scene, nodes: list, color=SECONDARY):
    """Highlight a path through nodes."""
    for node in nodes:
        if hasattr(node, 'circle'):
            node.circle.set_fill(color, opacity=0.5)

    scene.play(
        *[Indicate(n, color=color) for n in nodes],
        run_time=0.8
    )


def pulse_element(scene: Scene, element, scale=1.1):
    """Subtle pulse animation."""
    scene.play(
        element.animate.scale(scale),
        rate_func=there_and_back,
        run_time=0.4
    )


def transition_text(scene: Scene, old_text, new_text_str, color=WHITE):
    """Smoothly transition to new text."""
    new_text = Text(new_text_str, color=color)
    new_text.move_to(old_text.get_center())
    scene.play(TransformMatchingStrings(old_text, new_text))
    return new_text
```

## Pattern 5: Main Scene Using Helpers

Clean main scene file.

```python
# main.py
from manim import *
from helpers import create_node, create_edge, cascade_fade_in
from custom_mobjects import GraphNode, DPTable
from constants import *


class DijkstraScene(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND

        # Create graph using helpers
        nodes = {
            'A': GraphNode('A', LEFT * 3),
            'B': GraphNode('B', UP * 1.5),
            'C': GraphNode('C', DOWN * 1.5),
        }

        edges = [
            create_edge(nodes['A'], nodes['B'], weight=4),
            create_edge(nodes['A'], nodes['C'], weight=2),
            create_edge(nodes['B'], nodes['C'], weight=1),
        ]

        # Use animation helpers
        cascade_fade_in(self, list(nodes.values()))
        cascade_fade_in(self, edges, lag=0.2)

        # Algorithm visualization
        nodes['A'].highlight()
        self.wait()
        nodes['A'].mark_visited()
        nodes['A'].unhighlight()
```

---

## Checklist

```
□ Constants centralized in constants.py
□ Helper functions in helpers.py
□ Custom mobjects in custom_mobjects.py
□ Main scene file imports from helpers
□ Functions have clear docstrings
□ Reusable patterns extracted
□ State tracked separately from visuals
```

---

## Benefits

| Benefit | Description |
|---------|-------------|
| **Reusability** | Use same helpers across multiple videos |
| **Consistency** | Same visual style everywhere |
| **Maintainability** | Update once, applies everywhere |
| **Readability** | Main scene focuses on logic, not details |
| **Testing** | Helper functions can be tested independently |
