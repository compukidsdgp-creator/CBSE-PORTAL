"""Batch 05 — Class 12 Mathematics: one more paper's worth (plus spares). Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("maths12")
RF, IT, MA, DE, CD = "Relations and Functions", "Inverse Trigonometric Functions", "Matrices", "Determinants", "Continuity and Differentiability"
AD, IN, AI, DQ = "Application of Derivatives", "Integrals", "Application of Integrals", "Differential Equations"
VE, TD, LP, PR = "Vector Algebra", "Three Dimensional Geometry", "Linear Programming", "Probability"

# ── SECTION A — MCQ ──
b.m("A", IT, "The value of sin⁻¹(sin 2π/3) is:", "2π/3", "−π/3", "π/6", "π/3", "D")
b.m("A", IT, "The domain of the function f(x) = sin⁻¹(2x) is:", "[−1, 1]", "[0, 1/2]", "[−1/2, 1/2]", "[−2, 2]", "C")
b.m("A", DE, "If A is a square matrix of order 3 and |A| = 2, then the value of |A (adj A)| is:", "2", "4", "8", "16", "C")
b.m("A", DE, "The matrix with rows [2, k] and [3, 6] is singular. The value of k is:", "4", "3", "2", "6", "A")
b.m("A", LP, "The objective function Z = 3x + 4y is evaluated at the vertices O(0, 0), A(5, 0), B(3, 4) and C(0, 5) of a bounded feasible region. The maximum value of Z is:", "25", "20", "15", "30", "A")
b.m("A", LP, "Which of the following points does NOT lie in the half-plane 2x + 3y ≤ 12?", "(0, 0)", "(3, 2)", "(6, 0)", "(4, 2)", "D")
b.m("A", AI, "Using integration, the area of the part of the circle x² + y² = 4 that lies in the first quadrant is:", "4π sq units", "π sq units", "2π sq units", "π/2 sq units", "B")
b.m("A", CD, "If y = e^(sin x), then the value of dy/dx at x = 0 is:", "0", "e", "1", "−1", "C")
b.m("A", AD, "The function f(x) = x³ + 3x is strictly increasing on:", "R", "(0, ∞) only", "(−∞, 0) only", "(−1, 1) only", "A")
b.m("A", IN, "∫ dx / (x log x), x > 1, is equal to:", "log |x| + C", "log |log x| + C", "(log x)²/2 + C", "1/(log x) + C", "B")
b.m("A", DQ, "Which of the following differential equations is homogeneous?", "dy/dx = x² + y", "dy/dx = y + 1", "dy/dx = sin x + y", "dy/dx = (x² + y²)/(xy)", "D")
b.m("A", VE, "The scalar projection of the vector a = i + 2j + 2k on the vector b = 3i + 4k is:", "11/3", "11/5", "3", "5", "B")
b.m("A", TD, "A line makes angles of 90°, 60° and 30° with the positive directions of the x-, y- and z-axes respectively. Its direction cosines are:", "0, 1/2, √3/2", "1, √3/2, 1/2", "0, √3/2, 1/2", "1/2, 0, √3/2", "A")
b.m("A", PR, "A and B are independent events with P(A) = 0.6 and P(B) = 0.3. Then P(A ∪ B) is equal to:", "0.9", "0.18", "0.72", "0.82", "C")
b.m("A", MA, "The 3 × 3 matrix with rows [0, 3, −5], [−3, 0, 2] and [5, −2, 0] is:", "symmetric", "a diagonal matrix", "a scalar matrix", "skew-symmetric", "D")

# ── SECTION B — VSA ──
b.q("VSA", "B", IT, "Find the value of tan⁻¹(√3) − sec⁻¹(−2).")
b.q("VSA", "B", DE, "If A is the 2 × 2 matrix with rows [3, 1] and [2, 4], find adj A and verify that A (adj A) = |A| I.")
b.q("VSA", "B", CD, "If y = log(sec x + tan x), 0 < x < π/2, show that dy/dx = sec x.")
b.q("VSA", "B", AD, "Find the local maximum and the local minimum values of the function f(x) = x³ − 12x, and the points at which they occur.")

# ── SECTION C — SA ──
b.q("SA", "C", IN, "Evaluate: ∫ (2x + 3) / √(x² + 4x + 5) dx")
b.q("SA", "C", DQ, "Show that the differential equation x (dy/dx) = y + x sec(y/x) is homogeneous and find its general solution.")
b.q("SA", "C", VE, "The points A, B and C have position vectors i + j + 2k, 2i + 3j + 5k and i + 5j + 5k respectively. Using the vector product, find the area of triangle ABC.")
b.q("SA", "C", PR, "A fair die is thrown twice. Let X denote the number of times a six appears. Find the probability distribution of X and hence find the mean of X.")

# ── SECTION D — LA ──
b.q("LA", "D", LP, "Solve the following linear programming problem graphically:\nMinimise Z = 4x + 6y\nsubject to the constraints x + 2y ≥ 8, 3x + 2y ≥ 12, x ≥ 0, y ≥ 0.\nOR\nSolve the following linear programming problem graphically:\nMaximise Z = 2x + 5y\nsubject to the constraints x + 3y ≤ 15, x + y ≤ 7, 2x + y ≤ 12, x ≥ 0, y ≥ 0.")
b.q("LA", "D", AI, "Using integration, find the area of the region in the first quadrant bounded by the curve y² = 9x, the lines x = 1 and x = 4 and the x-axis. Also, using integration, find the area enclosed by the circle x² + y² = 25.\nOR\nUsing integration, find the area of the region bounded by the line y = 2x + 1, the x-axis and the lines x = −2 and x = 1.")
b.q("LA", "D", DE, "Using matrices, solve the following system of linear equations:\nx + y + 2z = 9\n2x − y + z = 3\n3x + 2y − z = 4")
b.q("LA", "D", TD, "Find the vector and Cartesian equations of the line passing through the point (2, −1, 3) and perpendicular to both the lines (x − 1)/1 = (y + 2)/2 = (z − 3)/3 and (x + 1)/2 = y/(−1) = (z − 2)/1. Also find the angle between the two given lines.\nOR\nFind the shortest distance between the lines r = (i + 2k) + λ(i − j + k) and r = (2i + j − k) + μ(2i + j + 2k).")

# ── SECTION E — CASE STUDY ──
b.q("CBQ", "E", RF, "For a quiz contest, nine teams are given the numbers 1 to 9. The organiser forms the set A = {1, 2, 3, 4, 5, 6, 7, 8, 9} and wants to seat teams together in groups using the relation R on A defined by R = {(a, b) : |a − b| is even}.\n(a) Show that R is reflexive and symmetric.\n(b) Show that R is transitive.\n(c) Write the equivalence classes [1] and [2].\nOR\n(c) The function f : A → A is defined by f(x) = 10 − x. Show that f is both one-one and onto.")
b.q("CBQ", "E", DQ, "In a laboratory, a culture of bacteria grows at a rate proportional to the number of bacteria present, so that dN/dt = kN, where N is the number of bacteria at time t hours and k is a positive constant. At the start there were 1000 bacteria, and the number doubled in 2 hours.\n(a) Write the order and the degree of the differential equation dN/dt = kN.\n(b) Solve the differential equation to find N in terms of t and k.\n(c) Find the number of bacteria present after 6 hours.\nOR\n(c) After how many hours will there be 16000 bacteria?")
b.q("CBQ", "E", LP, "A handicraft unit makes baskets and mats. Each basket needs 2 hours of weaving and 1 hour of finishing, while each mat needs 1 hour of weaving and 2 hours of finishing. Each day at most 20 hours of weaving and 16 hours of finishing are available. The profit is ₹40 on a basket and ₹30 on a mat. Let x baskets and y mats be made in a day.\n(a) Write the constraints of this linear programming problem.\n(b) Find the corner points of the feasible region.\n(c) How many baskets and mats should be made each day to earn the maximum profit? Find the maximum profit.\nOR\n(c) If the profit on a mat rises to ₹60 (with ₹40 on a basket), find the new maximum profit.")

b.save()
