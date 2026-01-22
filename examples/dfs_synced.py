"""
DFS (Depth-First Search) - Creative Maze Exploration
Animation synced to audio timing.
"""

from manim import *
import numpy as np

# Audio timing
TIMING = {
    "01_hook": {"start": 0, "end": 2.82},
    "02_insight": {"start": 2.82, "end": 9.94},
    "03_name": {"start": 9.94, "end": 12.86},
    "04_start": {"start": 12.86, "end": 17.75},
    "05_deep": {"start": 17.75, "end": 22.06},
    "06_stuck": {"start": 22.06, "end": 26.23},
    "07_try": {"start": 26.23, "end": 29.97},
    "08_found": {"start": 29.97, "end": 33.63},
    "09_takeaway": {"start": 33.63, "end": 39.41},
}


class Colors:
    BG = "#0f0f0f"
    TEXT = "#ffffff"
    TEXT_DIM = "#6b7280"

    # Maze colors
    WALL = "#374151"
    PATH = "#1e3a5f"

    # Explorer colors
    EXPLORER = "#fbbf24"  # Yellow - the explorer
    VISITED = "#22c55e"   # Green - visited
    CURRENT = "#fbbf24"   # Yellow - current
    BACKTRACK = "#ef4444" # Red - backtracking

    # Stack
    STACK_BG = "#1f2937"

    # Goal
    GOAL = "#a855f7"  # Purple - exit


class DFSSynced(Scene):
    def construct(self):
        self.camera.background_color = Colors.BG

        # Run segments
        self.segment("01_hook", self.anim_hook)
        self.segment("02_insight", self.anim_insight)
        self.segment("03_name", self.anim_name)
        self.segment("04_start", self.anim_start)
        self.segment("05_deep", self.anim_deep)
        self.segment("06_stuck", self.anim_stuck)
        self.segment("07_try", self.anim_try)
        self.segment("08_found", self.anim_found)
        self.segment("09_takeaway", self.anim_takeaway)

    def segment(self, seg_id, anim_func):
        """Run animation and pad to match audio."""
        t = TIMING[seg_id]
        target = t["end"] - t["start"]

        start = self.renderer.time
        anim_func()
        elapsed = self.renderer.time - start

        if elapsed < target:
            self.wait(target - elapsed)

    # ============================================================
    # MAZE GRAPH SETUP
    # ============================================================

    def create_maze_graph(self):
        """Create a maze-like graph structure."""
        # Node positions - maze-like layout
        #
        #     1 --- 2
        #     |     |
        # 0 --+     3 --- 6 (EXIT)
        #     |     |
        #     4 --- 5
        #
        self.positions = {
            0: np.array([-5, 0, 0]),      # Start (entrance)
            1: np.array([-2.5, 1.5, 0]),
            2: np.array([0, 1.5, 0]),
            3: np.array([0, 0, 0]),
            4: np.array([-2.5, -1.5, 0]),
            5: np.array([0, -1.5, 0]),
            6: np.array([3, 0, 0]),       # Exit (goal)
        }

        # Edges (maze paths)
        self.edges_list = [
            (0, 1), (0, 4),  # From start
            (1, 2),          # Upper path
            (2, 3),          # Connect to middle
            (3, 5), (3, 6),  # Middle connections
            (4, 5),          # Lower path
        ]

        # Create nodes
        self.nodes = {}
        self.node_labels = {}

        for i, pos in self.positions.items():
            # Node as rounded square (maze cell feel)
            if i == 0:
                node = Circle(radius=0.35, stroke_color=Colors.VISITED, stroke_width=3)
                node.set_fill(Colors.VISITED, opacity=0.3)
                label_text = "S"
            elif i == 6:
                node = Circle(radius=0.35, stroke_color=Colors.GOAL, stroke_width=3)
                node.set_fill(Colors.GOAL, opacity=0.3)
                label_text = "E"
            else:
                node = Circle(radius=0.3, stroke_color=Colors.WALL, stroke_width=2)
                node.set_fill(Colors.PATH, opacity=0.6)
                label_text = str(i)

            node.move_to(pos)

            label = Text(label_text, font_size=20, color=Colors.TEXT, weight=BOLD)
            label.move_to(pos)

            self.nodes[i] = node
            self.node_labels[i] = label

        # Create edges (paths)
        self.edges = {}
        for (a, b) in self.edges_list:
            pa, pb = self.positions[a], self.positions[b]
            direction = (pb - pa) / np.linalg.norm(pb - pa)

            line = Line(
                pa + direction * 0.4,
                pb - direction * 0.4,
                stroke_color=Colors.WALL,
                stroke_width=4
            )
            self.edges[(a, b)] = line

        # Create explorer (the moving dot)
        self.explorer = Dot(
            self.positions[0],
            radius=0.15,
            color=Colors.EXPLORER
        )
        self.explorer.set_z_index(10)

        # Glow effect for explorer
        self.explorer_glow = Circle(
            radius=0.25,
            stroke_color=Colors.EXPLORER,
            stroke_width=2,
            stroke_opacity=0.5
        )
        self.explorer_glow.move_to(self.positions[0])
        self.explorer_glow.set_z_index(9)

        # Trail (visited path)
        self.trail = VGroup()

        # Stack visualization
        self.stack_box = Rectangle(
            width=1.2, height=3,
            stroke_color=Colors.WALL,
            stroke_width=2,
            fill_color=Colors.STACK_BG,
            fill_opacity=0.8
        )
        self.stack_box.to_edge(RIGHT, buff=0.5)
        self.stack_box.shift(DOWN * 0.5)

        self.stack_label = Text("Stack", font_size=18, color=Colors.TEXT_DIM)
        self.stack_label.next_to(self.stack_box, UP, buff=0.2)

        self.stack_items = VGroup()
        self.stack_data = []

    def push_stack(self, node_id):
        """Push to stack visualization."""
        self.stack_data.append(node_id)
        self.update_stack_visual()

    def pop_stack(self):
        """Pop from stack visualization."""
        if self.stack_data:
            self.stack_data.pop()
            self.update_stack_visual()

    def update_stack_visual(self):
        """Update stack visualization."""
        new_items = VGroup()

        for i, node_id in enumerate(self.stack_data):
            item = Rectangle(
                width=0.8, height=0.4,
                stroke_color=Colors.EXPLORER,
                stroke_width=1,
                fill_color=Colors.EXPLORER,
                fill_opacity=0.3
            )
            label = Text(str(node_id), font_size=16, color=Colors.EXPLORER)

            item.move_to(self.stack_box.get_bottom() + UP * (0.3 + i * 0.45))
            label.move_to(item)

            new_items.add(VGroup(item, label))

        if len(self.stack_items) > 0:
            self.play(Transform(self.stack_items, new_items), run_time=0.3)
        else:
            self.stack_items = new_items
            self.add(self.stack_items)

    def move_explorer(self, from_node, to_node, leave_trail=True):
        """Move explorer from one node to another."""
        if leave_trail:
            # Leave footprint
            footprint = Dot(
                self.positions[from_node],
                radius=0.08,
                color=Colors.VISITED,
                fill_opacity=0.6
            )
            self.trail.add(footprint)
            self.add(footprint)

        # Highlight edge
        edge_key = (from_node, to_node) if (from_node, to_node) in self.edges else (to_node, from_node)
        if edge_key in self.edges:
            self.play(
                self.edges[edge_key].animate.set_stroke(Colors.VISITED, width=5),
                run_time=0.2
            )

        # Move explorer
        self.play(
            self.explorer.animate.move_to(self.positions[to_node]),
            self.explorer_glow.animate.move_to(self.positions[to_node]),
            run_time=0.4
        )

        # Mark node as visited
        if to_node not in [0, 6]:  # Don't change start/exit
            self.play(
                self.nodes[to_node].animate.set_stroke(Colors.VISITED),
                run_time=0.2
            )

    def backtrack_explorer(self, from_node, to_node):
        """Backtrack with red trail."""
        # Red backtrack line
        pa, pb = self.positions[from_node], self.positions[to_node]
        backtrack_line = DashedLine(
            pa, pb,
            stroke_color=Colors.BACKTRACK,
            stroke_width=2,
            dash_length=0.1
        )
        self.play(Create(backtrack_line), run_time=0.3)

        # Move explorer back
        self.play(
            self.explorer.animate.move_to(self.positions[to_node]),
            self.explorer_glow.animate.move_to(self.positions[to_node]),
            self.explorer.animate.set_color(Colors.BACKTRACK),
            run_time=0.3
        )

        # Restore color
        self.play(
            self.explorer.animate.set_color(Colors.EXPLORER),
            run_time=0.2
        )

    # ============================================================
    # ANIMATIONS
    # ============================================================

    def anim_hook(self):
        """[2.82s] How do you escape a maze?"""
        text = Text(
            "How do you escape a maze?",
            font_size=44, color=Colors.TEXT
        )
        self.play(Write(text), run_time=2)
        self.hook_text = text

    def anim_insight(self):
        """[7.12s] Go deep, backtrack if stuck."""
        # Transform to insight
        insight = Text(
            "Go deep.\nHit a wall? Backtrack.",
            font_size=36, color=Colors.EXPLORER,
            line_spacing=1.3
        )
        self.play(Transform(self.hook_text, insight), run_time=1.5)

        # Show simple visual metaphor
        arrow_down = Arrow(
            UP * 0.5, DOWN * 1.5,
            color=Colors.VISITED,
            stroke_width=6
        ).shift(LEFT * 3)

        arrow_back = Arrow(
            DOWN * 1.5 + LEFT * 0.3, UP * 0.5 + LEFT * 1,
            color=Colors.BACKTRACK,
            stroke_width=4
        ).shift(LEFT * 3)

        deep_label = Text("Deep", font_size=20, color=Colors.VISITED)
        deep_label.next_to(arrow_down, RIGHT, buff=0.2)

        back_label = Text("Back", font_size=20, color=Colors.BACKTRACK)
        back_label.next_to(arrow_back, LEFT, buff=0.2)

        self.play(GrowArrow(arrow_down), Write(deep_label), run_time=1)
        self.wait(0.5)
        self.play(GrowArrow(arrow_back), Write(back_label), run_time=1)

        self.arrows = VGroup(arrow_down, arrow_back, deep_label, back_label)

    def anim_name(self):
        """[2.92s] This is DFS."""
        # Clear and show name
        self.play(
            FadeOut(self.hook_text),
            FadeOut(self.arrows),
            run_time=0.5
        )

        dfs_name = Text(
            "Depth-First Search",
            font_size=48, color=Colors.EXPLORER, weight=BOLD
        )
        self.play(Write(dfs_name), run_time=1.5)
        self.play(FadeOut(dfs_name), run_time=0.5)

    def anim_start(self):
        """[4.89s] Start at entrance."""
        # Create maze graph
        self.create_maze_graph()

        # Animate graph appearance
        all_nodes = VGroup(*[VGroup(self.nodes[i], self.node_labels[i])
                           for i in self.positions])
        all_edges = VGroup(*self.edges.values())

        self.play(
            LaggedStart(*[FadeIn(e) for e in all_edges], lag_ratio=0.1),
            run_time=1
        )
        self.play(
            LaggedStart(*[GrowFromCenter(n) for n in all_nodes], lag_ratio=0.1),
            run_time=1.5
        )

        # Show stack
        self.play(
            FadeIn(self.stack_box),
            Write(self.stack_label),
            run_time=0.5
        )

        # Add explorer at start
        self.play(
            FadeIn(self.explorer),
            FadeIn(self.explorer_glow),
            run_time=0.5
        )

        # Push start to stack
        self.push_stack(0)

    def anim_deep(self):
        """[4.31s] Keep going deeper."""
        # DFS path: 0 -> 1 -> 2 -> 3
        self.move_explorer(0, 1)
        self.push_stack(1)

        self.move_explorer(1, 2)
        self.push_stack(2)

        self.move_explorer(2, 3)
        self.push_stack(3)

    def anim_stuck(self):
        """[4.17s] Dead end! Backtrack."""
        # Try to go to 5, but let's say it's a dead end for drama
        self.move_explorer(3, 5)
        self.push_stack(5)

        # Dead end indicator
        dead_end = Text("Dead end!", font_size=24, color=Colors.BACKTRACK)
        dead_end.next_to(self.nodes[5], DOWN, buff=0.4)
        self.play(Write(dead_end), run_time=0.5)

        # Backtrack
        self.pop_stack()
        self.backtrack_explorer(5, 3)

        self.play(FadeOut(dead_end), run_time=0.3)
        self.dead_end_text = dead_end

    def anim_try(self):
        """[3.74s] Try next unexplored path."""
        # From 3, try going to 6 (the exit!)
        # Show "trying another path" visually

        # Highlight unexplored edge
        edge_key = (3, 6)
        self.play(
            self.edges[edge_key].animate.set_stroke(Colors.EXPLORER, width=6),
            run_time=0.5
        )

    def anim_found(self):
        """[3.66s] Found the exit!"""
        # Move to exit
        self.move_explorer(3, 6)
        self.push_stack(6)

        # Celebration!
        self.play(
            self.nodes[6].animate.set_fill(Colors.GOAL, opacity=0.8),
            Flash(self.nodes[6], color=Colors.GOAL, line_length=0.4),
            run_time=0.8
        )

        found_text = Text("Exit found!", font_size=28, color=Colors.GOAL, weight=BOLD)
        found_text.next_to(self.nodes[6], UP, buff=0.5)
        self.play(Write(found_text), run_time=0.8)

        self.found_text = found_text

    def anim_takeaway(self):
        """[5.78s] DFS: Dive deep, retreat."""
        # Clean up and show takeaway
        self.play(FadeOut(self.found_text), run_time=0.3)

        # Fade graph slightly
        graph_group = VGroup(
            *self.nodes.values(),
            *self.node_labels.values(),
            *self.edges.values(),
            self.explorer,
            self.explorer_glow,
            self.trail,
            self.stack_box,
            self.stack_label,
            self.stack_items
        )
        self.play(graph_group.animate.set_opacity(0.3), run_time=0.5)

        # Final takeaway
        takeaway = Text(
            "Depth-First Search",
            font_size=40, color=Colors.EXPLORER, weight=BOLD
        )
        subtitle = Text(
            "Dive deep, then retreat",
            font_size=28, color=Colors.TEXT
        )

        VGroup(takeaway, subtitle).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(Write(takeaway), run_time=1)
        self.play(Write(subtitle), run_time=1)


# manim -qh dfs_synced.py DFSSynced
