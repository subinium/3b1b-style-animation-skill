"""
Binary Search - Synced to Audio Timing
Animation duration matches audio exactly.
"""

from manim import *
import numpy as np

# Audio timing (from timing.json)
TIMING = {
    "01_hook": {"start": 0, "end": 3.52},
    "02_answer": {"start": 3.52, "end": 6.09},
    "03_setup": {"start": 6.09, "end": 12.32},
    "04_naive": {"start": 12.32, "end": 17.72},
    "05_insight": {"start": 17.72, "end": 23.64},
    "06_step1": {"start": 23.64, "end": 29.59},
    "07_step2": {"start": 29.59, "end": 36.07},
    "08_step3": {"start": 36.07, "end": 41.44},
    "09_example": {"start": 41.44, "end": 49.93},
    "10_example2": {"start": 49.93, "end": 57.34},
    "11_complexity": {"start": 57.34, "end": 63.58},
    "12_takeaway": {"start": 63.58, "end": 68.54},
}


class Colors:
    BG = "#1c1c1c"
    TEXT = "#ffffff"
    TEXT_DIM = "#9ca3af"
    ARRAY_DEFAULT = "#3b82f6"
    ARRAY_HIGHLIGHT = "#fbbf24"
    ARRAY_FOUND = "#22c55e"
    ARRAY_ELIMINATED = "#374151"
    ACCENT = "#fbbf24"
    POINTER = "#ef4444"


class BinarySearchSynced(Scene):
    def construct(self):
        self.camera.background_color = Colors.BG

        # Run each segment with exact timing
        self.segment("01_hook", self.anim_hook)
        self.segment("02_answer", self.anim_answer)
        self.segment("03_setup", self.anim_setup)
        self.segment("04_naive", self.anim_naive)
        self.segment("05_insight", self.anim_insight)
        self.segment("06_step1", self.anim_step1)
        self.segment("07_step2", self.anim_step2)
        self.segment("08_step3", self.anim_step3)
        self.segment("09_example", self.anim_example)
        self.segment("10_example2", self.anim_example2)
        self.segment("11_complexity", self.anim_complexity)
        self.segment("12_takeaway", self.anim_takeaway)

    def segment(self, seg_id, anim_func):
        """Run animation and pad to match audio segment duration."""
        t = TIMING[seg_id]
        target = t["end"] - t["start"]

        start = self.renderer.time
        anim_func()
        elapsed = self.renderer.time - start

        if elapsed < target:
            self.wait(target - elapsed)

    # ============================================================
    # HELPER METHODS
    # ============================================================

    def create_array_boxes(self, values, width=0.8, height=0.7):
        """Create array visualization with boxes and values."""
        boxes = VGroup()
        texts = VGroup()

        for i, val in enumerate(values):
            box = Rectangle(
                width=width, height=height,
                stroke_color=WHITE, stroke_width=2,
                fill_color=Colors.ARRAY_DEFAULT, fill_opacity=0.8
            )
            box.shift(RIGHT * i * width)

            text = Text(str(val), font_size=22, color=WHITE)
            text.move_to(box)

            boxes.add(box)
            texts.add(text)

        group = VGroup(boxes, texts)
        group.move_to(ORIGIN)
        return boxes, texts

    def create_index_labels(self, boxes, font_size=16):
        """Create index labels below boxes."""
        labels = VGroup()
        for i, box in enumerate(boxes):
            label = Text(str(i), font_size=font_size, color=Colors.TEXT_DIM)
            label.next_to(box, DOWN, buff=0.15)
            labels.add(label)
        return labels

    def create_pointer(self, box, label_text, color=Colors.POINTER):
        """Create a pointer arrow above a box."""
        arrow = Arrow(
            box.get_top() + UP * 0.8,
            box.get_top() + UP * 0.1,
            color=color, stroke_width=3
        )
        label = Text(label_text, font_size=18, color=color)
        label.next_to(arrow, UP, buff=0.1)
        return VGroup(arrow, label)

    # ============================================================
    # ANIMATIONS
    # ============================================================

    def anim_hook(self):
        """[3.52s] How do you find a word in a dictionary?"""
        self.hook_text = Text(
            "How do you find a word\nin a dictionary?",
            font_size=42, color=Colors.TEXT,
            line_spacing=1.2
        )
        self.play(Write(self.hook_text), run_time=2.5)

    def anim_answer(self):
        """[2.57s] Binary Search."""
        answer = Text(
            "Binary Search",
            font_size=52, color=Colors.ACCENT, weight=BOLD
        )
        self.play(Transform(self.hook_text, answer), run_time=1.2)
        self.wait(0.5)
        self.play(FadeOut(self.hook_text), run_time=0.5)

    def anim_setup(self):
        """[6.23s] Imagine a sorted array of numbers."""
        # Title
        title = Text("Sorted Array", font_size=32, color=Colors.TEXT)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title), run_time=1)

        # Create sorted array
        self.array_values = [3, 7, 11, 15, 19, 23, 27, 31]
        self.boxes, self.texts = self.create_array_boxes(self.array_values)
        self.index_labels = self.create_index_labels(self.boxes)

        array_group = VGroup(self.boxes, self.texts, self.index_labels)
        array_group.move_to(ORIGIN)

        self.play(
            LaggedStart(*[GrowFromCenter(VGroup(b, t))
                         for b, t in zip(self.boxes, self.texts)],
                        lag_ratio=0.1),
            run_time=2
        )
        self.play(FadeIn(self.index_labels), run_time=0.8)

        # Target label
        self.target_label = Text("Target: 23", font_size=28, color=Colors.ACCENT)
        self.target_label.to_edge(DOWN, buff=1)
        self.play(Write(self.target_label), run_time=1)

        self.title = title

    def anim_naive(self):
        """[5.4s] We could check every element one by one."""
        # Show linear scan
        for i in range(6):  # Check first 6 elements
            self.play(
                self.boxes[i].animate.set_fill(Colors.ARRAY_HIGHLIGHT, opacity=0.9),
                run_time=0.4
            )
            self.play(
                self.boxes[i].animate.set_fill(Colors.ARRAY_DEFAULT, opacity=0.8),
                run_time=0.2
            )

        # Show "slow" indicator
        slow_text = Text("O(n) - Slow!", font_size=24, color=Colors.POINTER)
        slow_text.next_to(self.boxes, UP, buff=0.8)
        self.play(Write(slow_text), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(slow_text), run_time=0.5)

    def anim_insight(self):
        """[5.92s] Key insight: eliminate half at once."""
        # Clear previous and show insight
        insight_box = Rectangle(
            width=10, height=0.8,
            stroke_color=Colors.ACCENT, stroke_width=2,
            fill_color=Colors.BG, fill_opacity=0.95
        )
        insight_box.to_edge(UP, buff=0.5)

        insight_text = Text(
            "Eliminate half the elements at once!",
            font_size=26, color=Colors.ACCENT
        )
        insight_text.move_to(insight_box)

        self.play(
            FadeOut(self.title),
            Create(insight_box),
            Write(insight_text),
            run_time=1.5
        )

        # Visual: show half being grayed out
        left_half = VGroup(*self.boxes[:4])
        self.play(
            left_half.animate.set_fill(Colors.ARRAY_ELIMINATED, opacity=0.5),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            left_half.animate.set_fill(Colors.ARRAY_DEFAULT, opacity=0.8),
            run_time=0.5
        )

        self.insight_box = insight_box
        self.insight_text = insight_text

    def anim_step1(self):
        """[5.95s] Start in the middle."""
        # Point to middle
        mid_idx = len(self.boxes) // 2 - 1  # index 3 (value 15)
        mid_pointer = self.create_pointer(self.boxes[mid_idx], "mid", Colors.ACCENT)

        self.play(FadeIn(mid_pointer), run_time=0.8)
        self.play(
            self.boxes[mid_idx].animate.set_fill(Colors.ARRAY_HIGHLIGHT, opacity=0.9),
            run_time=0.5
        )

        # Question mark
        question = Text("23 > 15?", font_size=28, color=Colors.TEXT)
        question.next_to(self.boxes, DOWN, buff=1.5)
        self.play(Write(question), run_time=1)

        self.mid_pointer = mid_pointer
        self.question = question

    def anim_step2(self):
        """[6.48s] If greater, go right. If less, go left."""
        # Answer: Yes, go right
        answer = Text("Yes! → Go Right", font_size=28, color=Colors.ARRAY_FOUND)
        answer.move_to(self.question)
        self.play(Transform(self.question, answer), run_time=0.8)

        # Gray out left half
        left_half = VGroup(*self.boxes[:4])
        self.play(
            left_half.animate.set_fill(Colors.ARRAY_ELIMINATED, opacity=0.4),
            run_time=0.8
        )

        # Move pointer to right half middle
        self.play(FadeOut(self.mid_pointer), run_time=0.3)
        self.boxes[3].set_fill(Colors.ARRAY_ELIMINATED, opacity=0.4)

        # New mid in right half (index 5, value 23)
        new_mid = self.create_pointer(self.boxes[5], "mid", Colors.ACCENT)
        self.play(FadeIn(new_mid), run_time=0.5)
        self.play(
            self.boxes[5].animate.set_fill(Colors.ARRAY_HIGHLIGHT, opacity=0.9),
            run_time=0.5
        )

        # New question
        new_q = Text("23 = 23?", font_size=28, color=Colors.ACCENT)
        new_q.move_to(self.question)
        self.play(Transform(self.question, new_q), run_time=0.8)

        self.mid_pointer = new_mid

    def anim_step3(self):
        """[5.37s] Repeat. Each step cuts in half."""
        # Show found!
        found = Text("Found!", font_size=32, color=Colors.ARRAY_FOUND, weight=BOLD)
        found.move_to(self.question)
        self.play(Transform(self.question, found), run_time=0.6)

        self.play(
            self.boxes[5].animate.set_fill(Colors.ARRAY_FOUND, opacity=0.9),
            run_time=0.8
        )

        # Clean up for next example
        self.play(
            FadeOut(self.mid_pointer),
            FadeOut(self.question),
            FadeOut(self.insight_box),
            FadeOut(self.insight_text),
            run_time=0.8
        )

        # Reset array colors
        for box in self.boxes:
            box.set_fill(Colors.ARRAY_DEFAULT, opacity=0.8)

    def anim_example(self):
        """[8.49s] Let's find 23. Middle is 15. Go right."""
        # Reset and show fresh example
        example_title = Text("Example: Find 23", font_size=32, color=Colors.ACCENT)
        example_title.to_edge(UP, buff=0.5)
        self.play(Write(example_title), run_time=1)

        # Reset colors
        for box in self.boxes:
            self.play(
                box.animate.set_fill(Colors.ARRAY_DEFAULT, opacity=0.8),
                run_time=0.05
            )

        # Step 1: mid = 15
        left_ptr = self.create_pointer(self.boxes[0], "L", Colors.TEXT_DIM)
        right_ptr = self.create_pointer(self.boxes[7], "R", Colors.TEXT_DIM)
        mid_ptr = self.create_pointer(self.boxes[3], "M", Colors.ACCENT)

        self.play(FadeIn(left_ptr), FadeIn(right_ptr), run_time=0.5)
        self.play(FadeIn(mid_ptr), run_time=0.5)
        self.play(
            self.boxes[3].animate.set_fill(Colors.ARRAY_HIGHLIGHT, opacity=0.9),
            run_time=0.5
        )

        # Compare
        compare = Text("15 < 23 → Go Right", font_size=24, color=Colors.TEXT)
        compare.next_to(self.boxes, DOWN, buff=1.2)
        self.play(Write(compare), run_time=1)

        # Eliminate left half
        self.play(
            *[self.boxes[i].animate.set_fill(Colors.ARRAY_ELIMINATED, opacity=0.4)
              for i in range(4)],
            run_time=0.8
        )

        self.example_title = example_title
        self.left_ptr = left_ptr
        self.right_ptr = right_ptr
        self.mid_ptr = mid_ptr
        self.compare = compare

    def anim_example2(self):
        """[7.41s] New middle is 27. Go left. Found it!"""
        # Update pointers
        new_left = self.create_pointer(self.boxes[4], "L", Colors.TEXT_DIM)
        new_mid = self.create_pointer(self.boxes[5], "M", Colors.ACCENT)

        self.play(
            FadeOut(self.left_ptr),
            FadeOut(self.mid_ptr),
            FadeIn(new_left),
            FadeIn(new_mid),
            run_time=0.6
        )

        self.play(
            self.boxes[5].animate.set_fill(Colors.ARRAY_HIGHLIGHT, opacity=0.9),
            run_time=0.5
        )

        # Compare
        new_compare = Text("23 = 23 → Found!", font_size=24, color=Colors.ARRAY_FOUND)
        new_compare.move_to(self.compare)
        self.play(Transform(self.compare, new_compare), run_time=0.8)

        self.play(
            self.boxes[5].animate.set_fill(Colors.ARRAY_FOUND, opacity=0.9),
            run_time=0.8
        )

        # Celebrate
        check = Text("✓", font_size=48, color=Colors.ARRAY_FOUND)
        check.next_to(self.boxes[5], UP, buff=1.2)
        self.play(
            FadeOut(new_mid),
            FadeOut(new_left),
            FadeOut(self.right_ptr),
            FadeIn(check),
            run_time=0.8
        )

        self.check = check

    def anim_complexity(self):
        """[6.24s] 16 elements, at most 4 steps. Log n."""
        # Clean up
        self.play(
            FadeOut(self.example_title),
            FadeOut(self.compare),
            FadeOut(self.check),
            run_time=0.5
        )

        # Show complexity
        complexity_text = VGroup(
            Text("16 elements", font_size=28, color=Colors.TEXT),
            Text("↓", font_size=28, color=Colors.ACCENT),
            Text("4 steps max", font_size=28, color=Colors.ACCENT),
            Text("log₂(16) = 4", font_size=32, color=Colors.ARRAY_FOUND, weight=BOLD),
        ).arrange(DOWN, buff=0.3)
        complexity_text.to_edge(UP, buff=0.5)

        self.play(Write(complexity_text), run_time=2)

        # O(log n) big
        big_o = Text("O(log n)", font_size=48, color=Colors.ACCENT, weight=BOLD)
        big_o.next_to(self.boxes, DOWN, buff=1.5)
        self.play(Write(big_o), run_time=1)

        self.complexity_text = complexity_text
        self.big_o = big_o

    def anim_takeaway(self):
        """[4.96s] Divide and conquer."""
        # Final takeaway
        self.play(
            FadeOut(self.complexity_text),
            FadeOut(self.boxes),
            FadeOut(self.texts),
            FadeOut(self.index_labels),
            FadeOut(self.target_label),
            run_time=0.5
        )

        self.big_o.generate_target()
        self.big_o.target.move_to(UP * 0.5)
        self.play(MoveToTarget(self.big_o), run_time=0.5)

        takeaway = Text(
            "Divide and Conquer\nturns O(n) into O(log n)",
            font_size=36, color=Colors.TEXT,
            line_spacing=1.3
        )
        takeaway.next_to(self.big_o, DOWN, buff=0.8)
        self.play(Write(takeaway), run_time=2)


# manim -pqh binary_search_synced.py BinarySearchSynced
