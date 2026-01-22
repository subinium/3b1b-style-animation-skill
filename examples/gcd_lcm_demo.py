"""
GCD & LCM Algorithm Visualization
유클리드 알고리즘을 시각적으로 보여주는 애니메이션
"""

from manim import *
import numpy as np


class EuclideanAlgorithmVisual(Scene):
    """유클리드 호제법 시각화 - 직사각형 나누기 방식"""

    def construct(self):
        # Title
        title = Text("Euclidean Algorithm: GCD(48, 18)", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        a, b = 48, 18
        scale = 0.12  # 스케일 조정

        # 초기 직사각형 (a x b)
        rect = Rectangle(
            width=a * scale,
            height=b * scale,
            color=BLUE,
            fill_opacity=0.3,
            stroke_width=2
        )
        rect.shift(DOWN * 0.5)

        dim_label = Text(f"{a} × {b}", font_size=24)
        dim_label.next_to(rect, UP, buff=0.3)

        self.play(Create(rect), Write(dim_label))
        self.wait(0.5)

        steps = []
        current_a, current_b = a, b

        # 유클리드 알고리즘 실행
        while current_b > 0:
            quotient = current_a // current_b
            remainder = current_a % current_b
            steps.append((current_a, current_b, quotient, remainder))
            current_a, current_b = current_b, remainder

        gcd = current_a

        # Step-by-step 텍스트
        step_texts = VGroup()
        for i, (aa, bb, q, r) in enumerate(steps):
            step_text = Text(f"{aa} = {bb} × {q} + {r}", font_size=22)
            step_texts.add(step_text)

        step_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        step_texts.to_edge(RIGHT, buff=1)

        # 각 단계 애니메이션
        current_rect = rect
        colors = [BLUE, GREEN, YELLOW, ORANGE, RED, PURPLE]

        for i, (aa, bb, q, r) in enumerate(steps):
            # 현재 단계 텍스트 표시
            self.play(Write(step_texts[i]), run_time=0.5)

            # 정사각형들로 나누기 시각화
            if r > 0:
                # 나눈 부분 하이라이트
                squares = VGroup()
                for j in range(q):
                    sq = Square(
                        side_length=bb * scale,
                        color=colors[i % len(colors)],
                        fill_opacity=0.5,
                        stroke_width=2
                    )
                    squares.add(sq)

                squares.arrange(RIGHT, buff=0)
                squares.move_to(current_rect.get_left() + RIGHT * (q * bb * scale / 2), aligned_edge=LEFT)
                squares.align_to(current_rect, DOWN)

                self.play(
                    *[Create(sq) for sq in squares],
                    run_time=0.8
                )

            self.wait(0.3)

        # 결과 표시
        result = Text(f"GCD(48, 18) = {gcd}", font_size=32, color=YELLOW)
        result.to_edge(DOWN, buff=1)

        result_box = SurroundingRectangle(result, color=YELLOW, buff=0.2)

        self.play(Write(result), Create(result_box))
        self.wait()


class GCDBarVisualization(Scene):
    """GCD를 막대 그래프로 시각화"""

    def construct(self):
        title = Text("GCD: Greatest Common Divisor", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        a, b = 48, 18

        # 두 숫자를 막대로 표시
        scale = 0.1
        bar_height = 0.8

        bar_a = Rectangle(
            width=a * scale,
            height=bar_height,
            color=BLUE,
            fill_opacity=0.7
        )
        bar_a.shift(UP * 1.5)

        bar_b = Rectangle(
            width=b * scale,
            height=bar_height,
            color=GREEN,
            fill_opacity=0.7
        )
        bar_b.shift(UP * 0.3)
        bar_b.align_to(bar_a, LEFT)

        label_a = Text(f"a = {a}", font_size=24, color=BLUE)
        label_a.next_to(bar_a, LEFT, buff=0.3)

        label_b = Text(f"b = {b}", font_size=24, color=GREEN)
        label_b.next_to(bar_b, LEFT, buff=0.3)

        self.play(
            Create(bar_a), Write(label_a),
            Create(bar_b), Write(label_b),
            run_time=1
        )
        self.wait(0.5)

        # 유클리드 알고리즘 단계
        steps_data = []
        current_a, current_b = a, b
        while current_b > 0:
            remainder = current_a % current_b
            steps_data.append((current_a, current_b, remainder))
            current_a, current_b = current_b, remainder

        gcd = current_a

        # 단계별 표시
        step_group = VGroup()
        y_offset = -1

        for i, (aa, bb, r) in enumerate(steps_data):
            step_text = Text(f"Step {i+1}: {aa} mod {bb} = {r}", font_size=20)
            step_text.move_to([0, y_offset - i * 0.5, 0])
            step_group.add(step_text)

            # 나머지 막대 표시
            if r > 0:
                remainder_bar = Rectangle(
                    width=r * scale,
                    height=0.3,
                    color=YELLOW,
                    fill_opacity=0.7
                )
                remainder_bar.next_to(step_text, RIGHT, buff=0.3)

                self.play(Write(step_text), Create(remainder_bar), run_time=0.6)
            else:
                self.play(Write(step_text), run_time=0.6)

        self.wait(0.5)

        # GCD 결과
        gcd_bar = Rectangle(
            width=gcd * scale,
            height=bar_height,
            color=YELLOW,
            fill_opacity=0.9,
            stroke_color=WHITE,
            stroke_width=3
        )
        gcd_bar.shift(DOWN * 2.5)
        gcd_bar.align_to(bar_a, LEFT)

        gcd_label = Text(f"GCD = {gcd}", font_size=28, color=YELLOW)
        gcd_label.next_to(gcd_bar, RIGHT, buff=0.3)

        self.play(
            Create(gcd_bar),
            Write(gcd_label),
            run_time=1
        )

        # GCD가 두 수를 나눈다는 것 표시
        dividers_a = VGroup()
        for i in range(a // gcd):
            line = Line(
                bar_a.get_left() + RIGHT * (i + 1) * gcd * scale + UP * bar_height / 2,
                bar_a.get_left() + RIGHT * (i + 1) * gcd * scale + DOWN * bar_height / 2,
                color=WHITE,
                stroke_width=2
            )
            dividers_a.add(line)

        dividers_b = VGroup()
        for i in range(b // gcd):
            line = Line(
                bar_b.get_left() + RIGHT * (i + 1) * gcd * scale + UP * bar_height / 2,
                bar_b.get_left() + RIGHT * (i + 1) * gcd * scale + DOWN * bar_height / 2,
                color=WHITE,
                stroke_width=2
            )
            dividers_b.add(line)

        self.play(Create(dividers_a), Create(dividers_b), run_time=1)

        # 설명
        explain = Text(f"{a} = {gcd} × {a//gcd},  {b} = {gcd} × {b//gcd}", font_size=20)
        explain.to_edge(DOWN, buff=0.5)
        self.play(Write(explain))

        self.wait()


class LCMVisualization(Scene):
    """LCM 시각화 - 숫자선 위의 배수들"""

    def construct(self):
        title = Text("LCM: Least Common Multiple", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        a, b = 6, 8

        # 숫자선 (LaTeX 없이)
        number_line = NumberLine(
            x_range=[0, 50, 5],
            length=12,
            include_numbers=False,  # LaTeX 숫자 비활성화
        )
        number_line.shift(UP * 0.5)

        # 숫자 라벨을 Text로 직접 추가
        num_labels = VGroup()
        for n in [0, 10, 20, 30, 40, 50]:
            label = Text(str(n), font_size=16)
            label.next_to(number_line.n2p(n), DOWN, buff=0.2)
            num_labels.add(label)

        self.play(Create(number_line), Write(num_labels), run_time=1)

        # a의 배수들 (위쪽)
        multiples_a = VGroup()
        dots_a = VGroup()
        for i in range(1, 9):
            mult = a * i
            if mult <= 50:
                dot = Dot(
                    number_line.n2p(mult) + UP * 0.5,
                    color=BLUE,
                    radius=0.12
                )
                label = Text(str(mult), font_size=16, color=BLUE)
                label.next_to(dot, UP, buff=0.1)
                dots_a.add(dot)
                multiples_a.add(VGroup(dot, label))

        label_a = Text(f"Multiples of {a}", font_size=20, color=BLUE)
        label_a.to_edge(LEFT, buff=0.5)
        label_a.shift(UP * 1.5)

        # b의 배수들 (아래쪽)
        multiples_b = VGroup()
        dots_b = VGroup()
        for i in range(1, 7):
            mult = b * i
            if mult <= 50:
                dot = Dot(
                    number_line.n2p(mult) + DOWN * 0.5,
                    color=GREEN,
                    radius=0.12
                )
                label = Text(str(mult), font_size=16, color=GREEN)
                label.next_to(dot, DOWN, buff=0.1)
                dots_b.add(dot)
                multiples_b.add(VGroup(dot, label))

        label_b = Text(f"Multiples of {b}", font_size=20, color=GREEN)
        label_b.to_edge(LEFT, buff=0.5)
        label_b.shift(DOWN * 1.5)

        # 애니메이션
        self.play(Write(label_a))
        self.play(
            LaggedStart(*[FadeIn(m, scale=0.5) for m in multiples_a], lag_ratio=0.15),
            run_time=2
        )

        self.play(Write(label_b))
        self.play(
            LaggedStart(*[FadeIn(m, scale=0.5) for m in multiples_b], lag_ratio=0.15),
            run_time=2
        )

        self.wait(0.5)

        # 공통 배수 찾기
        lcm = (a * b) // np.gcd(a, b)

        # LCM 하이라이트
        lcm_circle = Circle(
            radius=0.3,
            color=YELLOW,
            stroke_width=4
        )
        lcm_circle.move_to(number_line.n2p(lcm))

        lcm_label = Text(f"LCM = {lcm}", font_size=28, color=YELLOW)
        lcm_label.next_to(lcm_circle, UP, buff=0.8)

        arrow = Arrow(
            lcm_label.get_bottom(),
            lcm_circle.get_top(),
            color=YELLOW,
            buff=0.1
        )

        self.play(
            Create(lcm_circle),
            Write(lcm_label),
            Create(arrow),
            run_time=1
        )

        # 공식 표시
        formula = Text(f"LCM({a}, {b}) = ({a} × {b}) / GCD({a}, {b}) = {a*b} / {np.gcd(a,b)} = {lcm}", font_size=20)
        formula.to_edge(DOWN, buff=0.8)
        self.play(Write(formula))

        self.wait()


class GCDLCMRelationship(Scene):
    """GCD와 LCM의 관계"""

    def construct(self):
        title = Text("GCD × LCM = a × b", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        a, b = 12, 18
        gcd = np.gcd(a, b)
        lcm = (a * b) // gcd

        # 벤 다이어그램 스타일
        circle_a = Circle(radius=1.5, color=BLUE, fill_opacity=0.3)
        circle_a.shift(LEFT * 1)

        circle_b = Circle(radius=1.5, color=GREEN, fill_opacity=0.3)
        circle_b.shift(RIGHT * 1)

        label_a = Text(f"a = {a}", font_size=24, color=BLUE)
        label_a.next_to(circle_a, LEFT, buff=0.3)

        label_b = Text(f"b = {b}", font_size=24, color=GREEN)
        label_b.next_to(circle_b, RIGHT, buff=0.3)

        self.play(
            Create(circle_a), Create(circle_b),
            Write(label_a), Write(label_b),
            run_time=1
        )

        # 소인수분해 표시
        # 12 = 2² × 3
        # 18 = 2 × 3²

        factors_a_only = Text("2²", font_size=20, color=BLUE)
        factors_a_only.move_to(circle_a.get_center() + LEFT * 0.8)

        factors_common = Text("2 × 3", font_size=20, color=YELLOW)
        factors_common.move_to(ORIGIN)

        factors_b_only = Text("3²", font_size=20, color=GREEN)
        factors_b_only.move_to(circle_b.get_center() + RIGHT * 0.8)

        # GCD는 교집합
        gcd_text = Text(f"GCD = 2 × 3 = {gcd}", font_size=22, color=YELLOW)
        gcd_text.shift(DOWN * 2)

        # LCM은 합집합
        lcm_text = Text(f"LCM = 2² × 3² = {lcm}", font_size=22, color=PURPLE)
        lcm_text.shift(DOWN * 2.7)

        self.play(
            Write(factors_a_only),
            Write(factors_common),
            Write(factors_b_only),
            run_time=1
        )
        self.wait(0.5)

        # GCD 하이라이트
        gcd_highlight = Ellipse(width=1.5, height=2, color=YELLOW, stroke_width=3)
        gcd_highlight.move_to(ORIGIN)

        self.play(Create(gcd_highlight), Write(gcd_text), run_time=1)
        self.wait(0.3)

        # LCM 하이라이트 (전체 합집합)
        self.play(Write(lcm_text), run_time=0.5)

        # 관계식
        relation = Text(f"GCD × LCM = {gcd} × {lcm} = {gcd * lcm} = {a} × {b} = a × b", font_size=20)
        relation.to_edge(DOWN, buff=0.5)

        box = SurroundingRectangle(relation, color=WHITE, buff=0.15)

        self.play(Write(relation), Create(box))
        self.wait()


class EuclideanAlgorithmCode(Scene):
    """유클리드 알고리즘 코드와 실행 과정"""

    def construct(self):
        title = Text("Euclidean Algorithm", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))

        # 의사코드 (Text로 표현)
        code_lines = [
            "def gcd(a, b):",
            "    while b != 0:",
            "        a, b = b, a % b",
            "    return a"
        ]

        code_group = VGroup()
        for i, line in enumerate(code_lines):
            code_text = Text(line, font_size=20, font="Menlo")
            code_text.set_color(WHITE)
            code_group.add(code_text)

        code_group.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        code_group.to_edge(LEFT, buff=1)
        code_group.shift(UP * 0.5)

        code_box = SurroundingRectangle(code_group, color=GRAY, buff=0.3)

        self.play(Create(code_box))
        for line in code_group:
            self.play(Write(line), run_time=0.4)

        self.wait(0.5)

        # 실행 과정 시뮬레이션
        a, b = 48, 18

        execution_title = Text(f"gcd({a}, {b})", font_size=24, color=YELLOW)
        execution_title.to_edge(RIGHT, buff=2)
        execution_title.shift(UP * 2)

        self.play(Write(execution_title))

        # 각 단계 표시
        steps = []
        current_a, current_b = a, b
        while current_b > 0:
            steps.append((current_a, current_b))
            current_a, current_b = current_b, current_a % current_b
        steps.append((current_a, current_b))

        step_texts = VGroup()
        y_pos = 1

        for i, (aa, bb) in enumerate(steps):
            if bb == 0:
                step_str = f"a={aa}, b={bb} → return {aa}"
                color = GREEN
            else:
                new_a, new_b = bb, aa % bb
                step_str = f"a={aa}, b={bb} → a={new_a}, b={new_b}"
                color = WHITE

            step_text = Text(step_str, font_size=18, color=color)
            step_text.move_to([3, y_pos - i * 0.5, 0])
            step_texts.add(step_text)

            # 해당 코드 라인 하이라이트
            if bb != 0:
                highlight = SurroundingRectangle(code_group[2], color=YELLOW, buff=0.05)
                self.play(Create(highlight), Write(step_text), run_time=0.5)
                self.play(FadeOut(highlight), run_time=0.2)
            else:
                highlight = SurroundingRectangle(code_group[3], color=GREEN, buff=0.05)
                self.play(Create(highlight), Write(step_text), run_time=0.5)

        # 결과
        result = Text(f"GCD({a}, {b}) = {steps[-1][0]}", font_size=28, color=YELLOW)
        result.to_edge(DOWN, buff=1)
        result_box = SurroundingRectangle(result, color=YELLOW, buff=0.15)

        self.play(Write(result), Create(result_box))
        self.wait()


# Run:
# manim -pql gcd_lcm_demo.py EuclideanAlgorithmVisual
# manim -pql gcd_lcm_demo.py GCDBarVisualization
# manim -pql gcd_lcm_demo.py LCMVisualization
# manim -pql gcd_lcm_demo.py GCDLCMRelationship
# manim -pql gcd_lcm_demo.py EuclideanAlgorithmCode
