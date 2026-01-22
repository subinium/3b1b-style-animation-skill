---
name: mathematical-rigor
description: Ensuring mathematical correctness and theoretical validity
metadata:
  tags: math, rigor, validation, correctness
priority: highest
---

# Mathematical Rigor Guidelines

**Every animation must be mathematically correct.** Visual beauty means nothing if the math is wrong.

## Pre-Production Checklist

Before writing ANY animation code, verify:

### 1. Definition Accuracy

```
□ Is the definition I'm using standard and correct?
□ Am I using the most pedagogically useful equivalent definition?
□ Are there edge cases I need to handle (zero, infinity, empty set)?
```

### 2. Formula Verification

```
□ Is the formula correct? (Check multiple sources)
□ Are the variable names consistent throughout?
□ Do the dimensions/units match on both sides?
□ Is the formula valid for the domain I'm showing?
```

### 3. Visual-Math Correspondence

```
□ Does my visual accurately represent the math?
□ Are proportions correct? (If showing area, is the area accurate?)
□ Is color mapping consistent? (Same value = same color)
□ Do animations preserve mathematical relationships?
```

## Common Mathematical Errors to Avoid

### Linear Algebra

```python
# ❌ WRONG: Matrix multiplication is commutative
A @ B == B @ A  # FALSE in general!

# ✅ RIGHT: Show that order matters
# First show AB, then show BA, then show they differ

# ❌ WRONG: Determinant of product
det(A + B) == det(A) + det(B)  # FALSE!

# ✅ RIGHT: det(AB) = det(A) * det(B)

# ❌ WRONG: Eigenvector visualization
# Showing eigenvector rotating after transformation

# ✅ RIGHT: Eigenvector only scales, never rotates
# The direction is preserved, only magnitude changes
```

### Number Theory

```python
# ❌ WRONG: GCD definition
gcd(0, 0)  # Undefined, not 0!

# ✅ RIGHT: Handle edge cases
gcd(a, 0) = a  for a > 0
gcd(0, 0) is undefined (or defined as 0 by convention)

# ❌ WRONG: LCM calculation
lcm(a, b) = a * b  # Only true if gcd(a,b) = 1!

# ✅ RIGHT:
lcm(a, b) = (a * b) / gcd(a, b)

# ❌ WRONG: Modular arithmetic
-7 % 3 = -1  # Python gives -1, math convention is 2!

# ✅ RIGHT: Be consistent about negative modulo
# Either always use positive remainder, or explain the convention
```

### Probability & Statistics

```python
# ❌ WRONG: Probability can exceed 1
# (This happens with probability DENSITY, not probability)

# ✅ RIGHT: Distinguish clearly
# Probability: P(X = x) ≤ 1
# Probability Density: f(x) can exceed 1, but ∫f(x)dx = 1

# ❌ WRONG: Bayes' theorem application
P(A|B) = P(B|A)  # FALSE!

# ✅ RIGHT: Full Bayes
P(A|B) = P(B|A) * P(A) / P(B)

# ❌ WRONG: Independence assumption
P(A ∩ B) = P(A) * P(B)  # Only if A, B independent!

# ✅ RIGHT: General case
P(A ∩ B) = P(A) * P(B|A)  # Always valid
```

### Calculus

```python
# ❌ WRONG: Derivative of |x| at x=0
d/dx |x| at x=0 exists  # FALSE! Not differentiable at 0

# ✅ RIGHT: Show the corner/cusp

# ❌ WRONG: Integral of 1/x
∫(1/x)dx = ln(x)  # Only for x > 0!

# ✅ RIGHT:
∫(1/x)dx = ln|x| + C  # For x ≠ 0

# ❌ WRONG: Chain rule visualization
# Showing incorrect factor relationships

# ✅ RIGHT: d/dx f(g(x)) = f'(g(x)) * g'(x)
# Visually: outer derivative * inner derivative
```

## Visual Accuracy Standards

### Scale and Proportion

```python
# If representing numerical values visually, be EXACT

# ❌ BAD: Approximate sizing
bar_a = Rectangle(width=3, ...)  # for value 48
bar_b = Rectangle(width=2, ...)  # for value 18
# 3/2 = 1.5, but 48/18 = 2.67!

# ✅ GOOD: Proportional sizing
scale = 0.1
bar_a = Rectangle(width=48 * scale, ...)
bar_b = Rectangle(width=18 * scale, ...)
# Now bars accurately represent the ratio
```

### Color-Value Mapping

```python
# Color must accurately represent value

def value_to_color(val, min_val, max_val):
    """Linearly interpolate color based on value."""
    # Normalize to [0, 1]
    t = (val - min_val) / (max_val - min_val)
    t = np.clip(t, 0, 1)

    if val < 0:
        return interpolate_color(RED, GRAY, ...)
    else:
        return interpolate_color(GRAY, BLUE, ...)

# ❌ BAD: Arbitrary color assignment
# ✅ GOOD: Consistent, proportional color mapping
```

### Transformation Accuracy

```python
# When showing matrix transformations, use the ACTUAL matrix

matrix = [[2, 1], [1, 1]]  # The matrix we're explaining

# ❌ BAD: Manually positioning transformed vectors
new_i = Arrow(ORIGIN, [2.5, 1, 0], ...)  # Guessed position

# ✅ GOOD: Compute actual transformation
i_hat = np.array([1, 0])
new_i_coords = matrix @ i_hat  # [2, 1]
new_i = Arrow(ORIGIN, [*new_i_coords, 0], ...)
```

## Notation Standards

### Consistent Symbol Usage

| Concept | Standard Notation | Avoid |
|---------|------------------|-------|
| Vectors | **v**, v̄, or →v | Plain v (ambiguous) |
| Matrices | A, B (capital) | a, b (lowercase) |
| Scalars | a, b, λ (lowercase/Greek) | A, B (confusion with matrices) |
| Sets | S, A, B (calligraphic if possible) | |
| Functions | f, g, h | F, G (unless standard) |

### Unit Consistency

If showing physical quantities, units must be consistent and correct.

```python
# ❌ BAD: Mixing units
distance = 5  # meters
time = 2      # seconds
speed = distance * time  # WRONG: should be division

# ✅ GOOD: Correct physics
speed = distance / time  # m/s
```

## Verification Procedures

### Self-Check Questions

After writing animation code, ask:

1. **Limiting cases**: Does the animation show correct behavior at extremes (0, ∞, etc.)?
2. **Known values**: For test inputs, does the animation produce correct outputs?
3. **Invariants**: Are mathematical invariants preserved throughout animations?
4. **Symmetry**: If the math has symmetry, does the visual reflect it?

### Numerical Verification

```python
# Always verify numerical computations

# Example: Verifying GCD animation
a, b = 48, 18
assert gcd(a, b) == 6

# Verify each step of Euclidean algorithm
assert 48 == 18 * 2 + 12
assert 18 == 12 * 1 + 6
assert 12 == 6 * 2 + 0
# 6 is correct GCD
```

### Edge Case Testing

```python
# Test animations with edge cases

# For GCD:
# - gcd(a, a) = a
# - gcd(a, 1) = 1
# - gcd(a, 0) = a (or undefined)
# - gcd of coprime numbers = 1

# For matrices:
# - Identity matrix transformation
# - Zero matrix
# - Singular matrix (det = 0)
```

## When Mathematical and Visual Simplicity Conflict

Sometimes accurate math is visually complex. Rules:

1. **Never sacrifice correctness for visual simplicity**
2. **Simplify by breaking into steps**, not by approximating
3. **Use annotations** to clarify complex visuals
4. **Acknowledge simplifications** when unavoidable

```python
# If you must simplify:
note = Text("(Simplified for clarity)", font_size=16, color=GRAY)
note.to_corner(DR)
self.add(note)
```

## Mathematical Writing Style

### In Labels and Annotations

- Use precise mathematical language
- Define terms before using them
- Be explicit about assumptions

### Avoid Ambiguity

```
❌ "Multiply the matrices"  # Which order?
✅ "Compute A times B (in that order)"

❌ "The derivative"  # Of what? With respect to what?
✅ "The derivative of f with respect to x"

❌ "Divide by zero"  # Undefined!
✅ "As x approaches 0..." (if discussing limits)
```
