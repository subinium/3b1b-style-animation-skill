"""
Dijkstra's Algorithm v2 - Comprehensive Version (2-3 min)
GPS shortest path metaphor with detailed step-by-step explanation.
"""

from manim import *
import numpy as np

# Audio timing
TIMING = {
    "01_hook": {"start": 0, "end": 3.81},
    "02_answer": {"start": 3.81, "end": 7.14},
    "03_graph": {"start": 7.14, "end": 15.04},
    "04_problem": {"start": 15.04, "end": 19.88},
    "05_insight": {"start": 19.88, "end": 25.13},
    "06_why": {"start": 25.13, "end": 31.03},
    "07_init": {"start": 31.03, "end": 37.32},
    "08_begin": {"start": 37.32, "end": 42.81},
    "09_step1": {"start": 42.81, "end": 49.09},
    "10_pick_c": {"start": 49.09, "end": 54.87},
    "11_from_c": {"start": 54.87, "end": 61.56},
    "12_update_b": {"start": 61.56, "end": 68.18},
    "13_visit_b": {"start": 68.18, "end": 73.34},
    "14_from_b": {"start": 73.34, "end": 80.03},
    "15_visit_d": {"start": 80.03, "end": 86.08},
    "16_visit_e": {"start": 86.08, "end": 90.92},
    "17_result": {"start": 90.92, "end": 95.36},
    "18_path": {"start": 95.36, "end": 101.16},
    "19_takeaway": {"start": 101.16, "end": 106.87},
    "20_complexity": {"start": 106.87, "end": 112.22},
}


class Colors:
    BG = "#1a1a2e"
    TEXT = "#ffffff"
    TEXT_DIM = "#8892b0"

    NODE_DEFAULT = "#4a5568"
    NODE_CURRENT = "#fbbf24"
    NODE_VISITED = "#10b981"
    NODE_START = "#3b82f6"

    EDGE_DEFAULT = "#4a5568"
    EDGE_ACTIVE = "#fbbf24"
    EDGE_PATH = "#10b981"

    WEIGHT = "#f59e0b"
    INFINITY = "#ef4444"
    DISTANCE = "#10b981"


class DijkstraV2Synced(Scene):
    def construct(self):
        self.camera.background_color = Colors.BG

        # Run all segments
        for seg_id in TIMING.keys():
            method_name = f"anim_{seg_id}"
            if hasattr(self, method_name):
                self.segment(seg_id, getattr(self, method_name))

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
    # GRAPH SETUP
    # ============================================================

    def create_graph(self):
        """Create the weighted graph."""
        # Node positions
        self.positions = {
            'A': np.array([-4.5, 0, 0]),
            'B': np.array([-1.5, 1.8, 0]),
            'C': np.array([-1.5, -1.8, 0]),
            'D': np.array([1.5, 0, 0]),
            'E': np.array([4.5, 0, 0]),
        }

        # Edges with weights
        self.edges_data = [
            ('A', 'B', 4),
            ('A', 'C', 2),
            ('B', 'C', 1),
            ('B', 'D', 5),
            ('C', 'D', 8),
            ('D', 'E', 2),
        ]

        # Create nodes
        self.nodes = {}
        self.node_labels = {}

        for name, pos in self.positions.items():
            node = Circle(radius=0.4, stroke_width=3)
            node.set_stroke(WHITE)
            node.set_fill(Colors.NODE_DEFAULT, opacity=0.8)
            node.move_to(pos)

            label = Text(name, font_size=26, color=WHITE, weight=BOLD)
            label.move_to(pos)

            self.nodes[name] = node
            self.node_labels[name] = label

        # Create edges
        self.edges = {}
        self.weights = {}

        for (a, b, w) in self.edges_data:
            pa, pb = self.positions[a], self.positions[b]
            direction = (pb - pa) / np.linalg.norm(pb - pa)

            line = Line(
                pa + direction * 0.45,
                pb - direction * 0.45,
                stroke_color=Colors.EDGE_DEFAULT,
                stroke_width=3
            )

            # Weight label
            mid = (pa + pb) / 2
            perp = np.array([-direction[1], direction[0], 0])
            if perp[1] < 0:
                perp = -perp

            weight = Text(str(w), font_size=20, color=Colors.WEIGHT)
            weight.move_to(mid + perp * 0.35)

            self.edges[(a, b)] = line
            self.weights[(a, b)] = weight

    def create_distance_table(self):
        """Create distance tracking table."""
        self.distances = {'A': 0, 'B': '∞', 'C': '∞', 'D': '∞', 'E': '∞'}
        self.dist_mobjects = {}

        # Table background
        table_bg = Rectangle(
            width=2.8, height=3.2,
            stroke_color=Colors.TEXT_DIM,
            stroke_width=1,
            fill_color=Colors.BG,
            fill_opacity=0.9
        )
        table_bg.to_corner(UR, buff=0.3)

        title = Text("Distances", font_size=20, color=Colors.TEXT_DIM)
        title.next_to(table_bg, UP, buff=0.15)

        self.table_group = VGroup(table_bg, title)

        # Distance entries
        for i, (node, dist) in enumerate(self.distances.items()):
            row = VGroup()

            node_label = Text(f"{node}:", font_size=22, color=WHITE)
            dist_text = Text(
                str(dist),
                font_size=22,
                color=Colors.DISTANCE if dist != '∞' else Colors.INFINITY
            )

            node_label.move_to(table_bg.get_left() + RIGHT * 0.6 + DOWN * (i * 0.5 - 0.8))
            dist_text.move_to(table_bg.get_left() + RIGHT * 1.8 + DOWN * (i * 0.5 - 0.8))

            row.add(node_label, dist_text)
            self.dist_mobjects[node] = dist_text
            self.table_group.add(row)

    def update_distance(self, node, new_dist, highlight=True):
        """Update distance in table."""
        new_text = Text(
            str(new_dist),
            font_size=22,
            color=Colors.WEIGHT if highlight else Colors.DISTANCE
        )
        new_text.move_to(self.dist_mobjects[node])

        self.play(
            Transform(self.dist_mobjects[node], new_text),
            run_time=0.4
        )
        self.distances[node] = new_dist

    def highlight_edge(self, a, b, color=Colors.EDGE_ACTIVE):
        """Highlight an edge."""
        key = (a, b) if (a, b) in self.edges else (b, a)
        self.play(
            self.edges[key].animate.set_stroke(color, width=5),
            run_time=0.3
        )

    def visit_node(self, name):
        """Mark node as visited (green)."""
        self.play(
            self.nodes[name].animate.set_fill(Colors.NODE_VISITED, opacity=0.9),
            self.nodes[name].animate.set_stroke(Colors.NODE_VISITED),
            run_time=0.5
        )

    def current_node(self, name):
        """Mark node as current (yellow)."""
        self.play(
            self.nodes[name].animate.set_fill(Colors.NODE_CURRENT, opacity=0.9),
            self.nodes[name].animate.set_stroke(Colors.NODE_CURRENT),
            run_time=0.4
        )

    # ============================================================
    # ANIMATIONS
    # ============================================================

    def anim_01_hook(self):
        """How does your GPS find the shortest route?"""
        # GPS icon metaphor
        gps_icon = SVGMobject("map-pin").scale(0.8) if False else Circle(
            radius=0.3, color=Colors.NODE_START
        ).shift(LEFT * 2)

        text = Text(
            "How does your GPS\nfind the shortest route?",
            font_size=42, color=Colors.TEXT,
            line_spacing=1.3
        )
        self.play(Write(text), run_time=2.5)
        self.hook_text = text

    def anim_02_answer(self):
        """Dijkstra's algorithm."""
        answer = Text(
            "Dijkstra's Algorithm",
            font_size=48, color=Colors.NODE_CURRENT, weight=BOLD
        )
        self.play(Transform(self.hook_text, answer), run_time=1.5)
        self.wait(0.5)
        self.play(FadeOut(self.hook_text), run_time=0.5)

    def anim_03_graph(self):
        """Imagine a map as a graph."""
        # Create and show graph
        self.create_graph()

        # Title
        title = Text("Graph = Map", font_size=32, color=Colors.TEXT)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1)

        # Animate graph
        edges_group = VGroup(*self.edges.values())
        nodes_group = VGroup(*[VGroup(self.nodes[n], self.node_labels[n])
                              for n in self.positions])
        weights_group = VGroup(*self.weights.values())

        self.play(Create(edges_group), run_time=1.5)
        self.play(
            LaggedStart(*[GrowFromCenter(n) for n in nodes_group], lag_ratio=0.15),
            run_time=2
        )
        self.play(FadeIn(weights_group), run_time=1)

        # Labels
        node_label = Text("Cities = Nodes", font_size=20, color=Colors.TEXT_DIM)
        edge_label = Text("Roads = Edges", font_size=20, color=Colors.TEXT_DIM)
        node_label.to_edge(DOWN, buff=0.8).shift(LEFT * 2)
        edge_label.to_edge(DOWN, buff=0.8).shift(RIGHT * 2)

        self.play(Write(node_label), Write(edge_label), run_time=1)

        self.title = title
        self.subtitle_labels = VGroup(node_label, edge_label)

    def anim_04_problem(self):
        """Shortest path from start to all others."""
        # Highlight start node
        self.play(
            self.nodes['A'].animate.set_fill(Colors.NODE_START, opacity=0.9),
            self.nodes['A'].animate.set_stroke(Colors.NODE_START),
            run_time=0.5
        )

        start_label = Text("Start", font_size=18, color=Colors.NODE_START)
        start_label.next_to(self.nodes['A'], DOWN, buff=0.3)
        self.play(Write(start_label), run_time=0.5)

        # Update title
        new_title = Text("Find shortest paths from A", font_size=28, color=Colors.TEXT)
        new_title.to_edge(UP, buff=0.5)
        self.play(
            Transform(self.title, new_title),
            FadeOut(self.subtitle_labels),
            run_time=1
        )

        self.start_label = start_label

    def anim_05_insight(self):
        """Key insight: visit closest unvisited first."""
        insight_box = Rectangle(
            width=9, height=0.8,
            stroke_color=Colors.NODE_CURRENT,
            stroke_width=2,
            fill_color=Colors.BG,
            fill_opacity=0.95
        )
        insight_box.to_edge(DOWN, buff=0.5)

        insight_text = Text(
            "Key: Always visit the closest unvisited node first",
            font_size=24, color=Colors.NODE_CURRENT
        )
        insight_text.move_to(insight_box)

        self.play(Create(insight_box), Write(insight_text), run_time=2)

        self.insight_box = insight_box
        self.insight_text = insight_text

    def anim_06_why(self):
        """Why? No shorter path possible."""
        # Add explanation
        why_text = Text(
            "If it's closest, no other path can be shorter!",
            font_size=22, color=Colors.DISTANCE
        )
        why_text.next_to(self.insight_box, UP, buff=0.3)

        self.play(Write(why_text), run_time=2)
        self.wait(1)
        self.play(FadeOut(why_text), run_time=0.5)

    def anim_07_init(self):
        """Initialize: start=0, others=infinity."""
        # Show distance table
        self.create_distance_table()
        self.play(FadeIn(self.table_group), run_time=1)

        # Highlight A=0
        self.play(
            Flash(self.dist_mobjects['A'], color=Colors.DISTANCE),
            run_time=0.5
        )

    def anim_08_begin(self):
        """From A, we can reach B and C."""
        # Highlight edges from A
        self.highlight_edge('A', 'B')
        self.highlight_edge('A', 'C')

    def anim_09_step1(self):
        """Distance to B=4, C=2."""
        self.update_distance('B', 4)
        self.update_distance('C', 2)

        # Reset edge colors
        self.play(
            self.edges[('A', 'B')].animate.set_stroke(Colors.EDGE_DEFAULT, width=3),
            self.edges[('A', 'C')].animate.set_stroke(Colors.EDGE_DEFAULT, width=3),
            run_time=0.3
        )

    def anim_10_pick_c(self):
        """C is closer. Visit C first."""
        self.current_node('C')
        self.wait(0.5)
        self.visit_node('C')

    def anim_11_from_c(self):
        """From C, reach B in 2+1=3."""
        self.highlight_edge('B', 'C')

        # Show calculation
        calc = Text("2 + 1 = 3 < 4", font_size=24, color=Colors.NODE_CURRENT)
        calc.next_to(self.nodes['B'], UP, buff=0.5)
        self.play(Write(calc), run_time=1)

        self.calc = calc

    def anim_12_update_b(self):
        """Update B to 3, also reach D=10."""
        self.update_distance('B', 3)
        self.play(FadeOut(self.calc), run_time=0.3)

        self.highlight_edge('C', 'D')
        self.update_distance('D', 10)

        # Reset edges
        self.play(
            self.edges[('B', 'C')].animate.set_stroke(Colors.EDGE_DEFAULT, width=3),
            self.edges[('C', 'D')].animate.set_stroke(Colors.EDGE_DEFAULT, width=3),
            run_time=0.3
        )

    def anim_13_visit_b(self):
        """B is closest. Visit B."""
        self.current_node('B')
        self.wait(0.3)
        self.visit_node('B')

    def anim_14_from_b(self):
        """From B, reach D in 3+5=8 < 10."""
        self.highlight_edge('B', 'D')

        calc = Text("3 + 5 = 8 < 10", font_size=24, color=Colors.NODE_CURRENT)
        calc.next_to(self.nodes['D'], UP, buff=0.5)
        self.play(Write(calc), run_time=1)

        self.update_distance('D', 8)
        self.play(FadeOut(calc), run_time=0.3)

        self.play(
            self.edges[('B', 'D')].animate.set_stroke(Colors.EDGE_DEFAULT, width=3),
            run_time=0.3
        )

    def anim_15_visit_d(self):
        """Visit D. Reach E in 8+2=10."""
        self.current_node('D')
        self.wait(0.3)
        self.visit_node('D')

        self.highlight_edge('D', 'E')
        self.update_distance('E', 10)

        self.play(
            self.edges[('D', 'E')].animate.set_stroke(Colors.EDGE_DEFAULT, width=3),
            run_time=0.3
        )

    def anim_16_visit_e(self):
        """Visit E. All done."""
        self.visit_node('E')

        # Done!
        done = Text("✓ All visited!", font_size=24, color=Colors.NODE_VISITED)
        done.next_to(self.table_group, DOWN, buff=0.3)
        self.play(Write(done), run_time=0.8)

        self.done_text = done

    def anim_17_result(self):
        """Shortest distances from A to all nodes."""
        # Highlight all distances
        self.play(
            *[self.dist_mobjects[n].animate.set_color(Colors.NODE_VISITED)
              for n in self.distances],
            run_time=0.8
        )

    def anim_18_path(self):
        """Shortest path to E: A→C→B→D→E = 10."""
        # Highlight the shortest path
        path_edges = [('A', 'C'), ('B', 'C'), ('B', 'D'), ('D', 'E')]

        for edge in path_edges:
            key = edge if edge in self.edges else (edge[1], edge[0])
            self.play(
                self.edges[key].animate.set_stroke(Colors.EDGE_PATH, width=6),
                run_time=0.5
            )

        # Path label
        path_text = Text(
            "A → C → B → D → E = 10",
            font_size=26, color=Colors.EDGE_PATH, weight=BOLD
        )
        path_text.move_to(self.insight_text)
        self.play(Transform(self.insight_text, path_text), run_time=0.8)

    def anim_19_takeaway(self):
        """Greedy choice = optimal path."""
        # Clean up
        self.play(
            FadeOut(self.title),
            FadeOut(self.done_text),
            FadeOut(self.start_label),
            run_time=0.5
        )

        # Final message
        takeaway = Text(
            "Always pick the closest → Optimal path guaranteed",
            font_size=28, color=Colors.NODE_CURRENT
        )
        takeaway.to_edge(UP, buff=0.5)
        self.play(Write(takeaway), run_time=2)

        self.takeaway = takeaway

    def anim_20_complexity(self):
        """O(V²) or O(E log V) with priority queue."""
        complexity = Text(
            "Time: O(V²) or O(E log V) with priority queue",
            font_size=22, color=Colors.TEXT_DIM
        )
        complexity.next_to(self.takeaway, DOWN, buff=0.5)
        self.play(Write(complexity), run_time=2)


# manim -qh dijkstra_v2_synced.py DijkstraV2Synced
