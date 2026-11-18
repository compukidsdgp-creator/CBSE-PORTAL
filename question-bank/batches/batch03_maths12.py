"""Batch 03 — Class 12 Mathematics: one more paper's worth (plus spares). Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("maths12")
RF, IT, MA, DE, CD = "Relations and Functions", "Inverse Trigonometric Functions", "Matrices", "Determinants", "Continuity and Differentiability"
AD, IN, AI, DQ = "Application of Derivatives", "Integrals", "Application of Integrals", "Differential Equations"
VE, TD, LP, PR = "Vector Algebra", "Three Dimensional Geometry", "Linear Programming", "Probability"

# ── SECTION A — MCQ ──
b.m("A", RF, "The number of one-one functions from the set {a, b, c} to itself is:", "3", "9", "27", "6", "D")
b.m("A", RF, "The relation R on the set N of natural numbers defined by R = {(a, b) : a ≤ b} is:", "symmetric only", "reflexive and transitive but not symmetric", "an equivalence relation", "symmetric and transitive but not reflexive", "B")
b.m("A", IT, "The principal value of cos⁻¹(−√3/2) is:", "5π/6", "π/6", "2π/3", "−π/6", "A")
b.m("A", MA, "A = [aᵢⱼ] is a 2 × 2 matrix whose elements are given by aᵢⱼ = i + 2j. The element a₂₁ is:", "3", "5", "4", "6", "C")
b.m("A", MA, "If the matrix with rows [x + y, 2] and [5, x − y] is equal to the matrix with rows [6, 2] and [5, 2], then the values of x and y are:", "x = 2, y = 4", "x = 3, y = 3", "x = 4, y = −2", "x = 4, y = 2", "D")
b.m("A", DE, "If the determinant with rows [x, 2] and [3, x] is equal to the determinant with rows [4, 1] and [2, 3], then x is equal to:", "±2", "4", "±4", "±√6", "C")
b.m("A", DE, "If A is an invertible matrix of order 2 and |A| = 3, then |A⁻¹| is equal to:", "3", "1/3", "9", "1/9", "B")
b.m("A", CD, "The derivative of tan⁻¹(eˣ) with respect to x is:", "eˣ/(1 + e²ˣ)", "1/(1 + e²ˣ)", "eˣ/(1 + eˣ)", "e²ˣ/(1 + e²ˣ)", "A")
b.m("A", CD, "The function f defined by f(x) = kx + 1 for x ≤ 2 and f(x) = 3x − 1 for x > 2 is continuous at x = 2. The value of k is:", "1", "5/2", "3", "2", "D")
b.m("A", AD, "The function f(x) = e²ˣ is:", "strictly decreasing on R", "strictly increasing on R", "increasing only for x > 0", "neither increasing nor decreasing on R", "B")
b.m("A", AD, "The minimum value of the function f(x) = x² − 6x + 10 is:", "3", "10", "1", "−1", "C")
b.m("A", IN, "∫ (sec² x / tan x) dx is equal to:", "log |sec x| + C", "log |tan x| + C", "tan x + C", "log |sin x| + C", "B")
b.m("A", IN, "The value of the definite integral of 1/(1 + x²) from x = 0 to x = 1 is:", "π/4", "π/2", "1", "π/3", "A")
b.m("A", AI, "The area of the region bounded by the line y = 2x, the x-axis and the line x = 3 is:", "6 sq units", "18 sq units", "3 sq units", "9 sq units", "D")
b.m("A", DQ, "Separating the variables in eʸ (dy/dx) = eˣ and integrating both sides, we obtain:", "eˣ + eʸ = C", "e⁻ʸ = eˣ + C", "eʸ = eˣ + C", "eʸ = e⁻ˣ + C", "C")
b.m("A", VE, "The value of p for which the vectors 2i + pj + k and i − 2j + 3k are perpendicular is:", "−5/2", "2", "3/2", "5/2", "D")
b.m("A", TD, "The direction ratios of the line (x − 1)/2 = (3 − y)/1 = (z + 2)/4 are:", "2, 1, 4", "2, −1, 4", "1, 3, −2", "−2, 1, 4", "B")
b.m("A", LP, "The corner points of the bounded feasible region of a linear programming problem are (0, 0), (5, 0), (3, 4) and (0, 6). The maximum value of Z = 3x + 2y is:", "17", "15", "12", "18", "A")
b.m("A", PR, "A random variable X takes the values 0, 1, 2 and 3 with probabilities k, 2k, 3k and 4k respectively. The value of k is:", "1/4", "1/6", "1/10", "1/12", "C")

b.ar("A", IN, "The definite integral of x³ cos x from x = −2 to x = 2 is equal to 0.", "If f is an odd function, then the integral of f(x) from x = −a to x = a is 0.", "A")
b.ar("A", AD, "The function f(x) = x³ has a local minimum at x = 0.", "For f(x) = x³, the derivative f′(0) = 0.", "D")
b.ar("A", RF, "The map g(x) = 3x + 2 from the set of real numbers to itself is a bijection.", "Every injective map is also surjective.", "C")

# ── SECTION B — VSA ──
b.q("VSA", "B", IT, "Find the values of (a) sin⁻¹(sin 3π/5) and (b) cos⁻¹(cos 4π/3).")
b.q("VSA", "B", CD, "Find dy/dx if x² + xy + y² = 7.")
b.q("VSA", "B", DQ, "Solve: (x − 1) dy = (y + 1) dx, where x ≠ 1 and y ≠ −1.")
b.q("VSA", "B", TD, "Show that the line (x − 2)/1 = (y + 1)/(−2) = z/2 is perpendicular to the line (x + 3)/2 = (y − 4)/2 = (z − 1)/1.")
b.q("VSA", "B", PR, "For two events A and B, P(A) = 0.5, P(B) = 0.4 and P(A ∪ B) = 0.7. Find P(A | B) and state whether A and B are independent.")

# ── SECTION C — SA ──
b.q("SA", "C", IN, "Evaluate: ∫ x² log x dx")
b.q("SA", "C", IN, "Evaluate the definite integral of |x − 2| from x = 0 to x = 5.")
b.q("SA", "C", DQ, "Find the particular solution of the differential equation x (dy/dx) − y = x², x > 0, given that y = 3 when x = 1.")
b.q("SA", "C", AD, "Find the absolute maximum and the absolute minimum values of the function f(x) = x³ − 6x² + 9x + 1 on the interval [0, 5].")
b.q("SA", "C", VE, "Find a unit vector perpendicular to both the vectors a = i + 2j − k and b = 2i − j + k. Also find the sine of the angle between a and b.")
b.q("SA", "C", PR, "A coin is biased so that a head is twice as likely to occur as a tail. The coin is tossed three times. Find the probability distribution of the number of tails and hence find its mean.")

# ── SECTION D — LA ──
b.q("LA", "D", DE, "Solve the following system of equations by the matrix method:\nx + 2y + z = 8\n2x − y + z = 3\nx + y − z = 0")
b.q("LA", "D", AI, "Using integration, find the area of the region enclosed by the ellipse 4x² + 25y² = 100.\nOR\nUsing integration, find the area of the region in the first quadrant enclosed by the x-axis, the line y = x and the circle x² + y² = 8.")
b.q("LA", "D", TD, "Find the coordinates of the foot of the perpendicular drawn from the point P(4, 1, 7) to the line (x − 1)/1 = (y − 2)/(−1) = (z − 3)/2. Hence find the perpendicular distance of P from the line and the image of P in the line.\nOR\nShow that the lines (x − 1)/1 = (y + 1)/2 = (z − 2)/(−1) and (x − 4)/1 = (y − 3)/1 = (z + 1)/(−1) intersect. Also find their point of intersection.")
b.q("LA", "D", LP, "A carpenter makes chairs and tables. Each chair needs 1 hour on the cutting machine and 2 hours on the polishing machine, while each table needs 1 hour on the cutting machine and 1 hour on the polishing machine. The cutting machine is available for at most 8 hours a day and the polishing machine for at most 12 hours a day. The profit is ₹400 on a chair and ₹300 on a table. Formulate this as a linear programming problem and solve it graphically to find how many chairs and tables should be made each day to get the maximum profit.\nOR\nSolve the following linear programming problem graphically:\nMinimise Z = 2x + 3y\nsubject to the constraints x + 2y ≥ 6, 3x + y ≥ 8, x ≥ 0, y ≥ 0.")

# ── SECTION E — CASE STUDY ──
b.q("CBQ", "E", AD, "A farmer has 200 m of fencing wire. He wants to fence a rectangular field that lies along a straight river. No fence is needed along the river bank, so the wire is used only for the other three sides. Let x metres be the length of each of the two sides perpendicular to the river.\n(a) Express the area A of the field as a function of x.\n(b) Find dA/dx and the value of x at which dA/dx = 0.\n(c) Find the maximum area that can be enclosed and the dimensions of the field.\nOR\n(c) Use the second derivative test to show that the area found is a maximum.")
b.q("CBQ", "E", PR, "In a school, 60% of the students play cricket, 40% play football and 25% play both games. A student is selected at random.\n(a) Find the probability that the student plays football, given that the student plays cricket.\n(b) Find the probability that the student plays neither game.\n(c) Are the events 'plays cricket' and 'plays football' independent? Justify your answer.\nOR\n(c) Find the probability that the student plays cricket, given that the student does not play football.")
b.q("CBQ", "E", VE, "A delivery drone takes off from its base O, taken as the origin, and flies in a straight line to a point A with position vector 2i + 3j + 6k. It then flies in a straight line to a point B with position vector 5i + 7j + 6k. All distances are in kilometres.\n(a) Find the distance OA.\n(b) Find the vector AB and the distance AB.\n(c) Find the cosine of the angle between OA and AB.\nOR\n(c) Find the projection of the vector AB on the vector OA.")

b.save()
