"""Batch 02 — Class 10 Mathematics: two more papers' worth of questions. Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("maths10")
RN, PO, LE, QE, AP = "Real Numbers", "Polynomials", "Pair of Linear Equations in Two Variables", "Quadratic Equations", "Arithmetic Progressions"
TR, CG, TG, AT = "Triangles", "Coordinate Geometry", "Introduction to Trigonometry", "Some Applications of Trigonometry"
CI, AC, SV, ST, PR = "Circles", "Areas Related to Circles", "Surface Areas and Volumes", "Statistics", "Probability"

# ── SECTION A — MCQ ──
b.m("A", RN, "The LCM of the smallest prime number and the smallest composite number is:", "2", "4", "6", "8", "B")
b.m("A", RN, "If p and q are two co-prime numbers, then their HCF is:", "1", "p", "q", "pq", "A")
b.m("A", RN, "The exponent of 2 in the prime factorisation of 144 is:", "2", "3", "4", "5", "C")
b.m("A", PO, "A quadratic polynomial whose zeroes are −3 and 4 is:", "x² + x − 12", "x² − x + 12", "x² + 7x + 12", "x² − x − 12", "D")
b.m("A", PO, "The graph of a polynomial p(x) cuts the x-axis at exactly three points. The number of zeroes of p(x) is:", "2", "3", "1", "4", "B")
b.m("A", PO, "If one zero of the polynomial x² + 3x + k is 2, then the value of k is:", "−10", "10", "5", "−5", "A")
b.m("A", LE, "The lines represented by the equations x = a and y = b (a, b ≠ 0) are:", "parallel", "coincident", "intersecting at the point (a, b)", "intersecting at the point (b, a)", "C")
b.m("A", LE, "The pair of equations 2x + y = 5 and 4x + 2y = 9 has:", "a unique solution", "no solution", "infinitely many solutions", "exactly two solutions", "B")
b.m("A", LE, "If x + y = 14 and x − y = 4, then the value of x is:", "5", "7", "8", "9", "D")
b.m("A", QE, "Which of the following is a quadratic equation?", "x(x + 3) = x² + 5", "(x + 2)² = x² + 7", "(x + 1)² = 2(x − 3)", "x(2x + 1) = 2x² − 9", "C")
b.m("A", QE, "If x = 3 is a root of the equation x² − kx + 6 = 0, then the value of k is:", "5", "−5", "3", "6", "A")
b.m("A", QE, "The roots of the quadratic equation x² + x + 1 = 0 are:", "real and equal", "real and distinct", "rational", "not real", "D")
b.m("A", AP, "The common difference of the AP 3, 1, −1, −3, ... is:", "2", "−2", "4", "−4", "B")
b.m("A", AP, "If the nth term of an AP is 3n + 2, then its common difference is:", "2", "5", "3", "1", "C")
b.m("A", AP, "The number of two-digit numbers that are divisible by 7 is:", "13", "14", "12", "15", "A")
b.m("A", TR, "ΔABC ~ ΔDEF. If AB = 4 cm, DE = 6 cm and BC = 5 cm, then EF is equal to:", "3.3 cm", "6 cm", "8 cm", "7.5 cm", "D")
b.m("A", TR, "Which of the following pairs of figures are always similar?", "Two rectangles", "Two equilateral triangles", "Two isosceles triangles", "Two rhombuses", "B")
b.m("A", CG, "The distance between the points (2, 3) and (−1, −1) is:", "3 units", "4 units", "5 units", "7 units", "C")
b.m("A", CG, "The point which divides the line segment joining (1, 2) and (7, 8) in the ratio 1 : 2 is:", "(3, 4)", "(5, 6)", "(4, 5)", "(2, 3)", "A")
b.m("A", CG, "The distance of the point (−6, 8) from the x-axis is:", "6 units", "8 units", "10 units", "14 units", "B")
b.m("A", TG, "If tan θ = 1 and θ is acute, then the value of sin θ + cos θ is:", "1", "2", "1/√2", "√2", "D")
b.m("A", TG, "The value of (1 + tan² θ)(1 − sin² θ) is:", "1", "0", "2", "tan² θ", "A")
b.m("A", TG, "If cos A = 4/5, then sec A is equal to:", "3/5", "4/3", "5/4", "5/3", "C")
b.m("A", AT, "A ladder 10 m long just reaches a window 5 m above the ground. The angle made by the ladder with the ground is:", "60°", "30°", "45°", "90°", "B")
b.m("A", AT, "The angle of elevation of the top of a tower from a point 30 m away from its foot is 45°. The height of the tower is:", "15 m", "30√3 m", "30 m", "60 m", "C")
b.m("A", CI, "The number of tangents that can be drawn to a circle from a point lying inside it is:", "0", "1", "2", "infinitely many", "A")
b.m("A", CI, "From a point P, the length of the tangent to a circle is 24 cm and the distance of P from the centre is 25 cm. The radius of the circle is:", "12 cm", "24.5 cm", "15 cm", "7 cm", "D")
b.m("A", AC, "The circumference of a circle is 44 cm. Its area is: (Use π = 22/7)", "77 cm²", "154 cm²", "308 cm²", "616 cm²", "B")
b.m("A", AC, "The length of an arc of a circle of radius 21 cm that subtends an angle of 60° at the centre is: (Use π = 22/7)", "11 cm", "44 cm", "22 cm", "66 cm", "C")
b.m("A", SV, "The total surface area of a solid hemisphere of radius r is:", "2πr²", "4πr²", "πr²", "3πr²", "D")
b.m("A", SV, "Two cubes, each of side 4 cm, are joined end to end. The surface area of the resulting cuboid is:", "160 cm²", "192 cm²", "128 cm²", "176 cm²", "A")
b.m("A", ST, "If the mean of 5, 7, 9 and x is 9, then the value of x is:", "12", "15", "13", "17", "B")
b.m("A", ST, "The mode of the data 2, 3, 3, 5, 3, 5, 7, 5, 3 is:", "3", "5", "7", "2", "A")
b.m("A", PR, "For any event E, the value of P(E) + P(not E) is:", "0", "2", "1", "1/2", "C")
b.m("A", PR, "A bag contains 3 red and 5 blue balls. One ball is drawn at random. The probability that it is blue is:", "3/8", "3/5", "5/3", "5/8", "D")
b.m("A", PR, "A letter is chosen at random from the letters of the word MATHEMATICS. The probability that it is a vowel is:", "7/11", "4/11", "3/11", "5/11", "B")

b.ar("A", PO, "The polynomial x² + 4 has no real zeroes.", "A quadratic polynomial can have at most two zeroes.", "B")
b.ar("A", TG, "sin θ = 4/3 is not possible for any angle θ.", "In a right triangle, the hypotenuse is the longest side.", "A")
b.ar("A", PR, "The probability of a sure event is 1.", "The probability of every event is greater than 0 and less than 1.", "C")

# ── SECTION B — VSA ──
b.q("VSA", "B", RN, "Explain why the number 6ⁿ cannot end with the digit 0 for any natural number n.")
b.q("VSA", "B", PO, "Find a quadratic polynomial, the sum and product of whose zeroes are −3 and 2 respectively. Also find its zeroes.")
b.q("VSA", "B", AP, "Find the sum of the first 20 positive multiples of 6.")
b.q("VSA", "B", TR, "A vertical pole of height 3 m casts a shadow 2 m long on the ground. At the same time, a tower casts a shadow 24 m long. Find the height of the tower.")
b.q("VSA", "B", CG, "Find the values of y for which the distance between the points A(3, y) and B(−1, 2) is 5 units.")
b.q("VSA", "B", TG, "If tan A = 4/3, find the values of sin A and sec A.")
b.q("VSA", "B", AC, "The circumference of a circle is 88 cm. Find the area of a quadrant of this circle. (Use π = 22/7)")
b.q("VSA", "B", PR, "A box contains cards numbered from 1 to 25. One card is drawn at random. Find the probability that the number on the card is a multiple of 3 or 5.")

# ── SECTION C — SA ──
b.q("SA", "C", RN, "Prove that √7 is an irrational number.")
b.q("SA", "C", PO, "If α and β are the zeroes of the polynomial 2x² − 5x + 3, find the values of (a) α² + β² and (b) 1/α + 1/β, without finding the zeroes.")
b.q("SA", "C", LE, "Five years ago, a father was seven times as old as his son. Five years from now, he will be three times as old as his son. Find their present ages.")
b.q("SA", "C", QE, "The sum of the squares of two consecutive odd positive integers is 290. Find the integers.")
b.q("SA", "C", AP, "The sum of the first n terms of an AP is given by Sₙ = 3n² + 5n. Find its nth term and hence its 15th term.")
b.q("SA", "C", TR, "ABCD is a trapezium in which AB ∥ DC and its diagonals intersect each other at the point O. Show that AO/BO = CO/DO.")
b.q("SA", "C", CG, "Find the coordinates of the points of trisection of the line segment joining the points A(1, −2) and B(−5, 7).")
b.q("SA", "C", TG, "Prove that: (1 + cot A − cosec A)(1 + tan A + sec A) = 2")
b.q("SA", "C", CI, "Two concentric circles have radii 13 cm and 5 cm. Find the length of the chord of the larger circle which touches the smaller circle.")
b.q("SA", "C", PR, "A bag contains 5 red, 8 white and 7 black balls. A ball is drawn at random from the bag. Find the probability that the ball drawn is (a) red or white, (b) not black and (c) neither white nor black.")
b.q("SA", "C", ST, "Find the mode of the following frequency distribution:\nClass: 0-10, 10-20, 20-30, 30-40, 40-50\nFrequency: 5, 9, 16, 12, 8")

# ── SECTION D — LA ──
b.q("LA", "D", LE, "A boat covers 24 km upstream and 28 km downstream in 6 hours. It can cover 30 km upstream and 21 km downstream in 6 hours 30 minutes. Find the speed of the boat in still water and the speed of the stream.")
b.q("LA", "D", QE, "The diagonal of a rectangular field is 16 m more than its shorter side. If the longer side is 14 m more than the shorter side, find the sides of the field.\nOR\nTwo positive numbers differ by 4 and their product is 192. Find the numbers.")
b.q("LA", "D", AP, "The 4th term of an AP is 11 and the sum of its 5th and 7th terms is 34. Find the AP and the sum of its first 20 terms.\nOR\nHow many terms of the AP 27, 24, 21, ... should be taken so that their sum is zero? Also find the last of these terms.")
b.q("LA", "D", TR, "Sides AB and BC and median AD of a triangle ABC are respectively proportional to sides PQ and QR and median PM of another triangle PQR. Show that ΔABC ~ ΔPQR.")
b.q("LA", "D", AT, "From a point on a bridge across a river, the angles of depression of the banks on opposite sides of the river are 30° and 45° respectively. If the bridge is at a height of 12 m above the banks, find the width of the river.\nOR\nAn observer 1.6 m tall is standing at some distance from a building 41.6 m high. The angle of elevation of the top of the building from his eyes increases from 30° to 60° as he walks towards the building. Find the distance he walked.")
b.q("LA", "D", CI, "(a) Prove that the angle between the two tangents drawn from an external point to a circle is supplementary to the angle subtended by the line segment joining the points of contact at the centre.\n(b) PQ is a chord of length 16 cm of a circle of radius 10 cm. The tangents at P and Q intersect at a point T. Find the length TP.")
b.q("LA", "D", SV, "A medicine capsule is in the shape of a cylinder with two hemispheres stuck to each of its ends. The length of the entire capsule is 20 mm and its diameter is 7 mm. Find its surface area. (Use π = 22/7)\nOR\nA vessel is in the form of a hollow hemisphere mounted by a hollow cylinder. The diameter of the hemisphere is 28 cm and the total height of the vessel is 20 cm. Find the inner surface area of the vessel. (Use π = 22/7)")
b.q("LA", "D", ST, "The mean of the following frequency distribution is 50 and the sum of all the frequencies is 120. Find the missing frequencies f₁ and f₂.\nClass: 0-20, 20-40, 40-60, 60-80, 80-100\nFrequency: 17, f₁, 32, f₂, 19")

# ── SECTION E — CASE STUDY ──
b.q("CBQ", "E", QE, "A school wants to build a rectangular vegetable garden. The gardener has 60 m of wire to fence all four sides of the garden, and the garden must have an area of 216 m².\n(a) If the length of the garden is x metres, express its breadth in terms of x.\n(b) Write the quadratic equation in x that represents this situation.\n(c) Find the length and breadth of the garden.\nOR\n(c) Find the length of the diagonal of the garden, correct to one decimal place.")
b.q("CBQ", "E", TR, "On a sunny afternoon, Meena, who is 1.5 m tall, notices that her shadow on the level playground is 2 m long. At the same time, the shadow of the school flagpole is 12 m long. Her teacher explains that the Sun's rays make the same angle with the ground for both, so two similar triangles are formed.\n(a) Name the criterion by which the two triangles are similar.\n(b) Find the height of the flagpole.\n(c) Later in the day, Meena's shadow becomes 1 m long. What will be the length of the shadow of the flagpole at that time?\nOR\n(c) At the time when Meena's shadow is 2 m long, find the distance between the top of her head and the tip of her shadow.")
b.q("CBQ", "E", AT, "During a kite festival, Arjun flies a kite at a height of 60 m above the ground. The string attached to the kite is tied to a peg on the ground and makes an angle of 60° with the ground. Assume that there is no slack in the string.\n(a) Which trigonometric ratio connects the height of the kite with the length of the string?\n(b) Find the length of the string.\n(c) Find the horizontal distance of the kite from the peg.\nOR\n(c) If the string were 120 m long and the kite were still at a height of 60 m, find the angle that the string would make with the ground.")
b.q("CBQ", "E", SV, "An ice-cream seller serves ice cream in a cone of radius 3 cm and height 12 cm. The cone is filled completely and then topped with a hemispherical scoop of the same radius.\n(a) Find the volume of the conical part in terms of π.\n(b) Find the volume of the hemispherical scoop in terms of π.\n(c) Find the total volume of ice cream in one serving. (Use π = 3.14)\nOR\n(c) Find the slant height of the cone and the area of the paper needed to wrap its curved surface, correct to one decimal place. (Use π = 3.14)")
b.q("CBQ", "E", ST, "The heights of 50 students of Class X were measured during a health check-up and recorded as follows:\nHeight (in cm): 140-145, 145-150, 150-155, 155-160, 160-165\nNumber of students: 5, 10, 20, 10, 5\n(a) Write the modal class of the data.\n(b) Find the cumulative frequency of the class 150-155.\n(c) Find the median height of the students.\nOR\n(c) Find the mean height of the students.")
b.q("CBQ", "E", AC, "A circular pizza of radius 14 cm is cut into 8 equal slices through its centre for a birthday party. Each slice is a sector of the circle.\n(a) Find the angle of each slice at the centre.\n(b) Find the area of the top surface of one slice. (Use π = 22/7)\n(c) Find the length of the curved edge (crust) of one slice.\nOR\n(c) Find the perimeter of one slice.")

b.save()
