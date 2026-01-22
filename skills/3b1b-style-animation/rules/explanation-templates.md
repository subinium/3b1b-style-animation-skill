---
name: explanation-templates
description: Ready-to-use templates for explaining common mathematical concepts
metadata:
  tags: templates, explanation, patterns, topics
priority: high
---

# Explanation Templates

These templates provide proven structures for explaining mathematical concepts visually.

## Linear Algebra Templates

### Explaining a Linear Transformation

```
STRUCTURE:
1. "What does this transformation DO?" (visual first)
2. Show grid/shape before transformation
3. Animate the transformation slowly
4. "Notice how [key property]..."
5. Show what happens to basis vectors
6. NOW show the matrix

VISUAL ELEMENTS:
- Grid lines (shows distortion)
- Basis vectors î, ĵ (shows column meaning)
- Sample vectors (shows general behavior)
- Unit square/circle (shows area/determinant)
```

```python
def explain_linear_transformation(self, matrix, name="A"):
    """Template for explaining any 2D linear transformation."""

    # 1. Setup: Grid and basis vectors
    grid = NumberPlane(...)
    i_hat = Arrow(ORIGIN, RIGHT, color=GREEN)
    j_hat = Arrow(ORIGIN, UP, color=RED)

    self.play(Create(grid), GrowArrow(i_hat), GrowArrow(j_hat))
    self.wait(1)

    # 2. Pose the question
    question = Text(f"What does {name} do to space?")
    self.play(Write(question))
    self.wait(1)
    self.play(FadeOut(question))

    # 3. Apply transformation (the key moment)
    self.play(
        grid.animate.apply_matrix(matrix),
        i_hat.animate.put_start_and_end_on(ORIGIN, [matrix[0][0], matrix[1][0], 0]),
        j_hat.animate.put_start_and_end_on(ORIGIN, [matrix[0][1], matrix[1][1], 0]),
        run_time=3  # Slow! Let them watch
    )
    self.wait(2)

    # 4. Point out key features
    # (customize based on transformation type)
```

### Explaining Eigenvectors

```
STRUCTURE:
1. "Most vectors change direction when transformed"
2. Show several vectors getting rotated/distorted
3. "But SOME vectors only get stretched..."
4. Highlight eigenvector staying on its line
5. "The stretch factor is the eigenvalue"
6. Show eigenvalue equation Av = λv

KEY INSIGHT TO CONVEY:
- Eigenvectors are "special directions"
- They don't rotate, only scale
- Eigenvalue = how much they scale
```

### Explaining Determinants

```
STRUCTURE:
1. Start with unit square
2. Apply transformation
3. "The area changed by a factor of..."
4. Show area computation
5. "This factor IS the determinant"
6. Show negative determinant = orientation flip

VISUAL:
- Unit square → parallelogram
- Show area values
- For 3D: cube → parallelepiped (volume)
```

## Number Theory Templates

### Explaining GCD/Euclidean Algorithm

```
STRUCTURE:
1. PROBLEM: "Given two piles, make equal groups"
2. VISUAL: Show physical division/grouping
3. KEY INSIGHT: "Remainders share the same GCD"
4. ALGORITHM: Step through with actual numbers
5. WHY IT WORKS: Visual proof
6. FORMULA: Mathematical summary

VISUAL APPROACHES (choose one):
- Rectangle division (geometric)
- Bar/pile subtraction (physical)
- Number line with jumps (arithmetic)
```

```python
def explain_gcd(self, a, b):
    """Template for GCD explanation."""

    # 1. Motivate
    self.play(Write(Text(f"What's the largest number that divides both {a} and {b}?")))

    # 2. Naive approach (optional, for longer videos)
    # Show listing divisors...

    # 3. The clever insight
    self.play(Write(Text("Key insight: if d divides a and b, it also divides a-b")))

    # 4. Visual algorithm
    # (choose representation: bars, rectangles, etc.)

    # 5. Step through
    while b != 0:
        self.show_step(a, b, a % b)
        a, b = b, a % b

    # 6. Result
    self.show_result(a)
```

### Explaining Modular Arithmetic

```
STRUCTURE:
1. "Clock arithmetic" analogy
2. Show number line wrapping into circle
3. Examples: 7 + 8 ≡ 3 (mod 12)
4. "Same remainder = same position on clock"
5. Properties (addition, multiplication)

VISUAL:
- Circle/clock face
- Number line wrapping around
- Color-coded equivalence classes
```

### Explaining Prime Factorization

```
STRUCTURE:
1. "Every number is built from primes"
2. Factor tree visualization
3. Show uniqueness
4. Connect to GCD/LCM: "shared vs combined factors"
```

## Probability Templates

### Explaining Bayes' Theorem

```
STRUCTURE:
1. SCENARIO: Concrete example (medical test, etc.)
2. INTUITION: "Flip the conditional"
3. VISUAL: Venn diagram or tree diagram
4. CALCULATION: Step by step with numbers
5. INSIGHT: "Prior → Posterior"
6. FORMULA: P(A|B) = P(B|A)P(A)/P(B)

KEY MISTAKE TO ADDRESS:
- P(A|B) ≠ P(B|A) -- show counterexample
```

```python
def explain_bayes(self, scenario):
    """Template for Bayes theorem explanation."""

    # 1. Setup scenario
    self.describe_scenario(scenario)

    # 2. Show naive confusion
    self.play(Write(Text("Common mistake: confusing P(A|B) with P(B|A)")))

    # 3. Visual: probability tree or area diagram
    self.draw_probability_tree()

    # 4. Walk through calculation
    self.step_by_step_calculation()

    # 5. Reveal the formula
    self.show_bayes_formula()
```

### Explaining Expected Value

```
STRUCTURE:
1. "If you played this game many times..."
2. Simulate many trials visually
3. Show average converging
4. "This average IS the expected value"
5. Formula: E[X] = Σ x·P(x)
```

### Explaining Distributions

```
STRUCTURE:
1. SCENARIO: What random process generates this?
2. HISTOGRAM: Show samples building up
3. CURVE: Smooth limit as n→∞
4. KEY PROPERTIES: Mean, variance, shape
5. FORMULA: PDF/PMF expression
```

## Calculus Templates

### Explaining Derivatives

```
STRUCTURE:
1. VISUAL: Curve with a point
2. SECANT: Draw secant line through two points
3. LIMIT: Move second point closer
4. TANGENT: Secant becomes tangent
5. SLOPE: "Derivative = slope of tangent"
6. FORMULA: lim (f(x+h)-f(x))/h

KEY VISUAL:
- Zooming into the curve (local linearity)
```

### Explaining Integrals

```
STRUCTURE:
1. PROBLEM: "How do we find area under a curve?"
2. RECTANGLES: Approximate with bars
3. REFINE: More rectangles = better approximation
4. LIMIT: Infinite rectangles = exact area
5. FORMULA: ∫f(x)dx
6. CONNECTION: Antiderivative relationship
```

### Explaining Chain Rule

```
STRUCTURE:
1. NESTED FUNCTION: "Function inside a function"
2. ANALOGY: Gears with different rates
3. VISUAL: Show how changes propagate
4. FORMULA: d/dx f(g(x)) = f'(g(x)) · g'(x)
5. EXAMPLE: With actual functions
```

## Algorithm Templates

### Explaining Recursive Algorithms

```
STRUCTURE:
1. PROBLEM: What are we solving?
2. BASE CASE: Simplest case (trivial solution)
3. RECURSIVE CASE: "Assume we can solve smaller version"
4. COMBINATION: How to use smaller solution
5. TRACE: Walk through with example
6. TREE: Show call tree structure
```

### Explaining Divide and Conquer

```
STRUCTURE:
1. PROBLEM: Too big to solve directly
2. DIVIDE: Split into smaller pieces
3. CONQUER: Solve pieces (recursively)
4. COMBINE: Merge solutions
5. VISUAL: Tree of subproblems
6. COMPLEXITY: Why this is efficient
```

## Using These Templates

### In Natural Language Prompts

Users can request:

```
"Explain [CONCEPT] using the [TEMPLATE_NAME] template"
"Create a video on eigenvalues following the standard linear algebra structure"
"Use the Bayes theorem template but with a different scenario"
```

### Customization Points

Each template has customization points:
- **Examples**: Choose numbers/scenarios
- **Depth**: Add/remove steps
- **Pacing**: Adjust wait times
- **Visuals**: Choose representation style

### Template Composition

For complex topics, combine templates:

```
"Explain matrix diagonalization by:
1. First explaining eigenvectors (eigenvector template)
2. Then showing how eigendecomposition works (transformation template)
3. Finally demonstrating an application (algorithm template)"
```
