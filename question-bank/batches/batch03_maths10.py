"""Batch 03 — Class 10 Mathematics: one more paper's worth (plus spares). Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("maths10")
RN, PO, LE, QE, AP = "Real Numbers", "Polynomials", "Pair of Linear Equations in Two Variables", "Quadratic Equations", "Arithmetic Progressions"
TR, CG, TG, AT = "Triangles", "Coordinate Geometry", "Introduction to Trigonometry", "Some Applications of Trigonometry"
CI, AC, SV, ST, PR = "Circles", "Areas Related to Circles", "Surface Areas and Volumes", "Statistics", "Probability"

# ── SECTION A — MCQ ──
b.m("A", RN, "Two numbers a and b have HCF 6 and their product a × b is 1080. Their LCM is:", "90", "360", "180", "6480", "C")
b.m("A", RN, "The largest number that divides 89 and 158 leaving remainders 5 and 4 respectively is:", "7", "14", "28", "42", "B")
b.m("A", PO, "If the sum of the zeroes of the polynomial kx² + 6x − 4 is 3, then the value of k is:", "2", "3", "−3", "−2", "D")
b.m("A", PO, "The product of the zeroes of the polynomial 3x² − 12 is:", "−4", "4", "0", "−12", "A")
b.m("A", LE, "The lines represented by the equations 3x − 5y = 7 and 6x − 10y = 3 are:", "intersecting at exactly one point", "coincident", "perpendicular to each other", "parallel", "D")
b.m("A", LE, "If x = 2, y = 3 is a solution of the equation 3x − ky = 3, then the value of k is:", "−1", "1", "2", "3", "B")
b.m("A", QE, "The positive value of k for which the equation x² + kx + 16 = 0 has two equal roots is:", "8", "4", "16", "2", "A")
b.m("A", QE, "Which of the following equations has two distinct real roots?", "x² + 2x + 5 = 0", "x² − 6x + 9 = 0", "2x² − 3x − 4 = 0", "3x² + x + 1 = 0", "C")
b.m("A", AP, "If 2k + 1, 13 and 5k − 3 are three consecutive terms of an AP, then the value of k is:", "3", "5", "4", "6", "C")
b.m("A", AP, "The 15th term from the last term of the AP 7, 10, 13, ..., 184 is:", "139", "145", "148", "142", "D")
b.m("A", TR, "In ΔPQR, S and T are points on PQ and PR respectively such that ST ∥ QR. If PS = 3 cm, SQ = 6 cm and PT = 2.5 cm, then the length of PR is:", "7.5 cm", "5 cm", "6 cm", "9 cm", "A")
b.m("A", CG, "The point on the x-axis which is equidistant from the points (3, 4) and (−1, 2) is:", "(2, 0)", "(5/2, 0)", "(0, 5/2)", "(−5/2, 0)", "B")
b.m("A", TG, "If sec θ − tan θ = 1/3, then the value of sec θ + tan θ is:", "1/3", "2/3", "9", "3", "D")
b.m("A", TG, "The value of (sin 45° + cos 45°)² is:", "1", "√2", "2", "1/2", "C")
b.m("A", AT, "From the top of a cliff 50 m high, the angle of depression of a boat on the sea is 30°. The distance of the boat from the foot of the cliff is:", "50√3 m", "50 m", "50/√3 m", "100 m", "A")
b.m("A", CI, "AB and CD are two parallel tangents to a circle of radius 5 cm. The distance between AB and CD is:", "5 cm", "10 cm", "15 cm", "2.5 cm", "B")
b.m("A", AC, "The area of a sector of a circle of radius 6 cm whose central angle is 120° is:", "6π cm²", "18π cm²", "12π cm²", "36π cm²", "C")
b.m("A", SV, "The curved surface area of a right circular cylinder of base radius 7 cm and height 10 cm is: (Use π = 22/7)", "220 cm²", "880 cm²", "154 cm²", "440 cm²", "D")
b.m("A", ST, "For the frequency distribution\nClass: 0-5, 5-10, 10-15, 15-20, 20-25\nFrequency: 10, 15, 12, 20, 9\nthe lower limit of the modal class is:", "15", "10", "20", "25", "A")
b.m("A", PR, "A number is chosen at random from the numbers 1 to 30. The probability that it is a perfect square is:", "1/5", "1/6", "1/10", "2/15", "B")

b.ar("A", QE, "The equation x² + 3x + 5 = 0 has no real roots.", "A quadratic equation ax² + bx + c = 0 has no real roots when b² − 4ac < 0.", "A")
b.ar("A", AP, "The list of numbers 1, 4, 9, 16, ... forms an AP.", "In an AP, the difference between any two consecutive terms is the same.", "D")
b.ar("A", CG, "The point (0, −4) lies on the y-axis.", "The x-coordinate of every point on the x-axis is zero.", "C")

# ── SECTION B — VSA ──
b.q("VSA", "B", RN, "Using prime factorisation, find the HCF and LCM of 84 and 126. Verify that HCF × LCM = product of the two numbers.")
b.q("VSA", "B", LE, "Solve the following pair of equations for x and y:\nx/2 + y/3 = 5\nx/3 − y/6 = 1")
b.q("VSA", "B", QE, "Find the discriminant of the quadratic equation 4x² − 12x + 9 = 0. Hence state the nature of its roots and find them.")
b.q("VSA", "B", TR, "In ΔABC, D is a point on AB and E is a point on AC such that DE ∥ BC. If AD : DB = 3 : 5 and AC = 12 cm, find the length of AE.")
b.q("VSA", "B", AC, "A chord of a circle of radius 14 cm subtends a right angle at the centre. Find the area of the corresponding minor segment. (Use π = 22/7)")
b.q("VSA", "B", CI, "A tangent at a point P of a circle with centre O and radius 6 cm meets a line through O at the point Q such that OQ = 10 cm. Find the length of PQ, giving a reason for each step.")

# ── SECTION C — SA ──
b.q("SA", "C", PO, "One zero of the quadratic polynomial x² − 8x + k is three times the other. Find both the zeroes and the value of k.")
b.q("SA", "C", LE, "A shopkeeper sells 3 pens and 2 notebooks for ₹110, and 4 pens and 3 notebooks for ₹155. Find the cost of one pen and the cost of one notebook.")
b.q("SA", "C", TG, "Prove that sec⁴ A − sec² A = tan⁴ A + tan² A. Hence find the value of sec⁴ 45° − sec² 45°.")
b.q("SA", "C", CG, "Find the ratio in which the point P(m, 6) divides the line segment joining A(−4, 3) and B(6, 8). Hence find the value of m.")
b.q("SA", "C", CI, "A circle is inscribed in ΔABC and touches the sides AB, BC and CA at the points P, Q and R respectively. If AB = 10 cm, BC = 8 cm and CA = 12 cm, find the lengths AP, BQ and CR.")
b.q("SA", "C", AC, "The minute hand of a wall clock is 21 cm long. Find the area swept by the minute hand in 20 minutes and the distance moved by its tip in that time. (Use π = 22/7)")

# ── SECTION D — LA ──
b.q("LA", "D", QE, "Two water taps together can fill a tank in 6 hours. The tap of larger diameter takes 5 hours less than the smaller one to fill the tank alone. Find the time in which each tap can separately fill the tank.\nOR\nThe product of Ravi's age 4 years ago and his age 6 years from now is 299. Form a quadratic equation and find Ravi's present age.")
b.q("LA", "D", AP, "The sum of the first 6 terms of an AP is 69 and the sum of the next 6 terms is 177. Find the AP and its 20th term.\nOR\nFind the number of three-digit numbers that leave a remainder 2 when divided by 5. Also find the sum of all such numbers.")
b.q("LA", "D", TR, "(a) State and prove the Basic Proportionality Theorem.\n(b) In ΔPQR, M and N are points on the sides PQ and PR respectively such that PM = 6 cm, MQ = 9 cm, PN = 4 cm and NR = 6 cm. Is MN ∥ QR? Justify your answer.")
b.q("LA", "D", AT, "A man standing on the deck of a ship, 12 m above the water level, observes that the angle of elevation of the top of a cliff is 60° and the angle of depression of its base is 30°. Find the distance of the cliff from the ship and the height of the cliff.\nOR\nFrom the top of a lighthouse 60 m high, the angles of depression of two ships on the same side of the lighthouse and in line with its base are 30° and 60°. Find the distance between the two ships. (Use √3 = 1.732)")
b.q("LA", "D", SV, "From a solid cylinder of height 15 cm and diameter 7 cm, a conical cavity of the same diameter and height 12 cm is hollowed out at one end. Find (a) the total surface area of the remaining solid and (b) the volume of the remaining solid. (Use π = 22/7)")

# ── SECTION E — CASE STUDY ──
b.q("CBQ", "E", LE, "At a school canteen, Aman bought 2 sandwiches and 3 glasses of juice for ₹130. His friend Bela bought 3 sandwiches and 2 glasses of juice for ₹145. The prices of a sandwich and of a glass of juice are the same for both of them.\n(a) Taking the cost of a sandwich as ₹x and the cost of a glass of juice as ₹y, write the pair of linear equations that describes this situation.\n(b) Find the cost of one sandwich and of one glass of juice.\n(c) Find the total cost of 4 sandwiches and 5 glasses of juice.\nOR\n(c) Chirag has ₹200. He buys 3 sandwiches. What is the greatest number of glasses of juice he can buy with the money left?")
b.q("CBQ", "E", PO, "In a park, a water fountain throws a stream of water that follows a curved path. Taking the point O on the ground as origin, the height of the water (in metres) at a horizontal distance of x metres from O is given by the polynomial p(x) = −x² + 8x − 12. The water leaves the ground and falls back to the ground at the points where p(x) = 0.\n(a) Find the zeroes of p(x). What do they represent in this situation?\n(b) Find the sum and the product of the zeroes and verify their relationship with the coefficients of p(x).\n(c) The water reaches its greatest height exactly midway between the two points found in (a). Find this greatest height.\nOR\n(c) Find a quadratic polynomial whose zeroes are each 1 more than the zeroes of p(x).")
b.q("CBQ", "E", CI, "A circular running track has its centre at O and an inner radius of 15 m. A lamp post P stands outside the track at a distance of 25 m from O. Two straight paths PA and PB are laid from the lamp post so that each just touches the inner edge of the track, at A and B respectively.\n(a) What is the measure of ∠OAP? Give a reason.\n(b) Find the length of the path PA.\n(c) If ∠APB = 70°, find ∠AOB.\nOR\n(c) Find the area of the quadrilateral OAPB.")

b.save()
