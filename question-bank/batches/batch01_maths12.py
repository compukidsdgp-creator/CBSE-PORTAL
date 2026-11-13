"""Batch 01 — Class 12 Mathematics: one paper's worth (plus spare) of original questions. Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("maths12")
RF, IT, MA, DE, CD = "Relations and Functions", "Inverse Trigonometric Functions", "Matrices", "Determinants", "Continuity and Differentiability"
AD, IN, AI, DQ = "Application of Derivatives", "Integrals", "Application of Integrals", "Differential Equations"
VE, TD, LP, PR = "Vector Algebra", "Three Dimensional Geometry", "Linear Programming", "Probability"

# ── SECTION A — MCQ ──
b.m("A", RF, "The relation R = {(1, 1), (2, 2), (3, 3), (1, 2), (2, 1)} on the set {1, 2, 3} is:", "reflexive only", "symmetric only", "reflexive and symmetric but not transitive", "an equivalence relation", "D")
b.m("A", RF, "The function f : R → R defined by f(x) = x² is:", "one-one and onto", "one-one but not onto", "neither one-one nor onto", "onto but not one-one", "C")
b.m("A", IT, "The principal value of sin⁻¹(−1/2) is:", "π/6", "−π/6", "5π/6", "7π/6", "B")
b.m("A", IT, "The value of tan⁻¹(1) + cos⁻¹(−1/2) is:", "7π/12", "5π/12", "11π/12", "π/12", "C")
b.m("A", MA, "If A is a matrix of order 3 × 4 and B is a matrix of order 4 × 2, then the order of AB is:", "3 × 2", "2 × 3", "4 × 4", "3 × 4", "A")
b.m("A", MA, "If A is a skew-symmetric matrix, then every element on its principal diagonal is:", "1", "0", "−1", "any real number", "B")
b.m("A", DE, "If A is a square matrix of order 3 and |A| = 4, then |2A| is equal to:", "8", "16", "32", "64", "C")
b.m("A", DE, "If A is a square matrix of order 3 and |A| = 5, then |adj A| is equal to:", "5", "125", "15", "25", "D")
b.m("A", CD, "The derivative of sin² x with respect to x is:", "sin 2x", "cos² x", "2 sin x", "−sin 2x", "A")
b.m("A", CD, "The derivative of log(log x) with respect to x, for x > 1, is:", "1/log x", "1/(x log x)", "log x / x", "x/log x", "B")
b.m("A", CD, "The function f(x) = |x| at x = 0 is:", "differentiable but not continuous", "neither continuous nor differentiable", "continuous but not differentiable", "both continuous and differentiable", "C")
b.m("A", AD, "The rate of change of the area of a circle with respect to its radius r, when r = 5 cm, is:", "10π cm²/cm", "25π cm²/cm", "5π cm²/cm", "20π cm²/cm", "A")
b.m("A", AD, "The function f(x) = x³ − 3x has a local maximum at:", "x = 1", "x = −1", "x = 0", "x = 3", "B")
b.m("A", IN, "∫ eˣ (1/x − 1/x²) dx is equal to:", "eˣ/x² + C", "−eˣ/x + C", "eˣ log x + C", "eˣ/x + C", "D")
b.m("A", IN, "The value of the definite integral of cos x from x = 0 to x = π/2 is:", "1", "0", "−1", "π/2", "A")
b.m("A", IN, "The value of the definite integral of x³ from x = −1 to x = 1 is:", "1/2", "1/4", "0", "2", "C")
b.m("A", DQ, "The order and degree of the differential equation (d²y/dx²)³ + (dy/dx)² + y = 0 are respectively:", "3 and 2", "2 and 3", "2 and 2", "3 and 3", "B")
b.m("A", DQ, "The integrating factor of the differential equation dy/dx + y/x = x², for x > 0, is:", "x", "1/x", "eˣ", "log x", "A")
b.m("A", VE, "If |a| = 3, |b| = 4 and a · b = 6 for two vectors a and b, then the angle between them is:", "30°", "45°", "60°", "90°", "C")
b.m("A", VE, "The unit vector in the direction of the vector i + 2j + 2k is:", "(i + 2j + 2k)/9", "(i + 2j + 2k)/5", "i + 2j + 2k", "(i + 2j + 2k)/3", "D")
b.m("A", TD, "The direction cosines of the z-axis are:", "1, 0, 0", "0, 0, 1", "0, 1, 0", "1, 1, 1", "B")
b.m("A", TD, "The angle between two lines whose direction ratios are 1, 1, 0 and 0, 1, 1 is:", "30°", "45°", "60°", "90°", "C")
b.m("A", LP, "In a linear programming problem with a bounded feasible region, the maximum value of the objective function occurs at:", "a corner point of the feasible region", "the origin only", "the centre of the feasible region", "any point outside the feasible region", "A")
b.m("A", PR, "If A and B are independent events with P(A) = 0.4 and P(B) = 0.5, then P(A ∩ B) is:", "0.9", "0.1", "0.45", "0.2", "D")
b.m("A", PR, "If P(A ∩ B) = 0.2 and P(B) = 0.5, then P(A | B) is equal to:", "0.1", "0.4", "0.7", "2.5", "B")

b.ar("A", MA, "For any two square matrices A and B of the same order, (A + B)² = A² + 2AB + B².", "Matrix multiplication is not commutative in general.", "D")
b.ar("A", CD, "Every differentiable function is continuous.", "Every continuous function is differentiable.", "C")
b.ar("A", VE, "For two non-zero, non-parallel vectors a and b, the vector a × b is perpendicular to both a and b.", "a × b = |a| |b| sin θ n, where n is a unit vector perpendicular to the plane containing a and b.", "A")

# ── SECTION B — VSA ──
b.q("VSA", "B", IT, "Find the value of cos⁻¹(cos 7π/6).")
b.q("VSA", "B", MA, "If A is the 2 × 2 matrix with rows [2, 3] and [1, 2], show that A² − 4A + I = O. Hence find A⁻¹.")
b.q("VSA", "B", CD, "Find dy/dx if y = xˣ, x > 0.")
b.q("VSA", "B", AD, "The radius of a spherical balloon is increasing at the rate of 0.2 cm/s. Find the rate at which its volume is increasing when the radius is 5 cm.")
b.q("VSA", "B", IN, "Evaluate: ∫ dx / (x² + 4x + 8)")
b.q("VSA", "B", VE, "Find the area of the parallelogram whose adjacent sides are given by the vectors a = i + j − k and b = i − j + k.")
b.q("VSA", "B", PR, "A bag contains 4 red and 6 black balls. Two balls are drawn at random one after the other without replacement. Find the probability that both the balls are red.")

# ── SECTION C — SA ──
b.q("SA", "C", RF, "Show that the relation R on the set Z of integers, given by R = {(a, b) : 5 divides (a − b)}, is an equivalence relation.")
b.q("SA", "C", CD, "If y = Ae²ˣ + Be⁻³ˣ, where A and B are constants, show that d²y/dx² + dy/dx − 6y = 0.")
b.q("SA", "C", AD, "Find the intervals in which the function f(x) = 2x³ − 9x² + 12x + 15 is (a) strictly increasing and (b) strictly decreasing.")
b.q("SA", "C", IN, "Evaluate: ∫ x / ((x + 1)(x + 2)) dx")
b.q("SA", "C", IN, "Using a property of definite integrals, evaluate the integral of sin x / (sin x + cos x) from x = 0 to x = π/2.")
b.q("SA", "C", DQ, "Find the general solution of the differential equation dy/dx = (1 + x²)(1 + y²).")
b.q("SA", "C", VE, "Three vectors a, b and c satisfy a + b + c = 0. If |a| = 3, |b| = 5 and |c| = 7, find the angle between a and b.")
b.q("SA", "C", PR, "Bag I contains 4 red and 2 black balls, and Bag II contains 3 red and 5 black balls. One bag is chosen at random and a ball is drawn from it. The ball is found to be red. Find the probability that it was drawn from Bag II.")

# ── SECTION D — LA ──
b.q("LA", "D", DE, "Solve the following system of equations by the matrix method:\nx + y + z = 6\nx − y + z = 2\n2x + y − z = 1")
b.q("LA", "D", AI, "Using integration, find the area of the region bounded by the parabola y² = 4x and the line x = 3.\nOR\nUsing integration, find the area of the region enclosed by the ellipse x²/16 + y²/9 = 1.")
b.q("LA", "D", TD, "Find the shortest distance between the lines whose vector equations are\nr = (i + j) + λ(i + k) and\nr = (2j + k) + μ(j + k).")
b.q("LA", "D", LP, "Solve the following linear programming problem graphically:\nMaximise Z = 3x + 2y\nsubject to the constraints x + 2y ≤ 10, 3x + y ≤ 15, x ≥ 0, y ≥ 0.")

# ── SECTION E — CASE STUDY ──
b.q("CBQ", "E", AD, "A craft teacher gives each student a square sheet of cardboard of side 24 cm. An open box is to be made by cutting a square of side x cm from each corner and folding up the flaps. The teacher asks the students to make the box that can hold the maximum volume.\n(a) Express the volume V of the box in terms of x.\n(b) Find dV/dx.\n(c) Find the value of x for which the volume is maximum, and find the maximum volume.\nOR\n(c) Find the values of x for which dV/dx = 0 and explain why one of them cannot be the side of the square that is cut off.")
b.q("CBQ", "E", PR, "A factory has two machines, A and B. Machine A produces 60% of the items and machine B produces the remaining 40%. It is found that 2% of the items produced by machine A and 1% of the items produced by machine B are defective. An item is picked at random from the day's production.\n(a) Find the probability that the item was produced by machine A and is defective.\n(b) Find the probability that the item is defective.\n(c) If the item is found to be defective, find the probability that it was produced by machine A.\nOR\n(c) If the item is found to be defective, find the probability that it was produced by machine B.")
b.q("CBQ", "E", MA, "A bookshop sells Physics, Chemistry and Mathematics guide books. On Monday it sold 10, 8 and 12 copies of the three books respectively, and on Tuesday it sold 6, 10 and 9 copies. The selling prices of the three books are ₹300, ₹250 and ₹400 per copy respectively.\n(a) Write the sales of the two days as a matrix with one row for each day, and state its order.\n(b) Using matrix multiplication, find the amount collected on Monday.\n(c) Find the total amount collected on the two days together.\nOR\n(c) If the price of each book is increased by 10%, find the amount that would have been collected on Monday.")

b.save()
