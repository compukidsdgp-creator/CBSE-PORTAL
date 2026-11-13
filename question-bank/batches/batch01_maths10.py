"""Batch 01 — Class 10 Mathematics: one paper's worth (plus spare) of original questions. Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("maths10")
RN, PO, LE, QE, AP = "Real Numbers", "Polynomials", "Pair of Linear Equations in Two Variables", "Quadratic Equations", "Arithmetic Progressions"
TR, CG, TG, AT = "Triangles", "Coordinate Geometry", "Introduction to Trigonometry", "Some Applications of Trigonometry"
CI, AC, SV, ST, PR = "Circles", "Areas Related to Circles", "Surface Areas and Volumes", "Statistics", "Probability"

# ── SECTION A — MCQ ──
b.m("A", RN, "The HCF of 72 and 120 is 24. Their LCM is:", "240", "720", "360", "1440", "C")
b.m("A", RN, "The number 7 × 11 × 13 + 13 is:", "a prime number", "a composite number", "an odd number", "neither prime nor composite", "B")
b.m("A", PO, "The zeroes of the polynomial x² − 5x + 6 are:", "2 and 3", "−2 and −3", "1 and 6", "−1 and −6", "A")
b.m("A", PO, "If α and β are the zeroes of the polynomial x² − 4x + 3, then the value of 1/α + 1/β is:", "3/4", "−4/3", "−3/4", "4/3", "D")
b.m("A", LE, "The pair of equations x + 2y = 5 and 3x + 6y = 15 has:", "a unique solution", "no solution", "infinitely many solutions", "exactly two solutions", "C")
b.m("A", LE, "The value of k for which the equations 2x + 3y = 5 and 4x + ky = 10 have infinitely many solutions is:", "3", "6", "12", "1", "B")
b.m("A", QE, "The discriminant of the quadratic equation 2x² − 4x + 3 = 0 is:", "−8", "8", "40", "−40", "A")
b.m("A", QE, "The roots of the equation x² − 7x + 12 = 0 are:", "−3 and −4", "2 and 6", "3 and 4", "1 and 12", "C")
b.m("A", AP, "The 10th term of the AP 2, 7, 12, 17, ... is:", "52", "47", "45", "50", "B")
b.m("A", AP, "The sum of the first 20 natural numbers is:", "200", "190", "420", "210", "D")
b.m("A", TR, "In ΔABC, D and E are points on AB and AC such that DE ∥ BC. If AD = 2 cm, DB = 3 cm and AE = 4 cm, then EC is:", "5 cm", "8 cm", "6 cm", "1.5 cm", "C")
b.m("A", CG, "The distance of the point (3, 4) from the origin is:", "5 units", "7 units", "1 unit", "12 units", "A")
b.m("A", CG, "The mid-point of the line segment joining the points (−2, 5) and (6, −1) is:", "(4, 4)", "(2, 2)", "(−4, 3)", "(2, 3)", "B")
b.m("A", TG, "If sin θ = 3/5 and θ is an acute angle, then tan θ is equal to:", "4/5", "4/3", "3/4", "5/3", "C")
b.m("A", TG, "The value of sin² 30° + cos² 60° is:", "1/2", "1", "1/4", "3/4", "A")
b.m("A", AT, "A vertical pole 6 m high casts a shadow 2√3 m long on the ground. The angle of elevation of the Sun is:", "30°", "45°", "90°", "60°", "D")
b.m("A", CI, "Two tangents drawn to a circle from an external point are inclined to each other at an angle of 60°. The angle between the radii drawn to the points of contact is:", "60°", "120°", "90°", "30°", "B")
b.m("A", AC, "The area of a sector of a circle of radius 14 cm and central angle 90° is: (Use π = 22/7)", "77 cm²", "308 cm²", "154 cm²", "616 cm²", "C")
b.m("A", SV, "The volume of a right circular cone of base radius 3 cm and height 4 cm is:", "12π cm³", "36π cm³", "15π cm³", "48π cm³", "A")
b.m("A", ST, "For a certain distribution, the mean is 18 and the median is 20. Using the empirical relationship, the mode is:", "22", "19", "16", "24", "D")
b.m("A", PR, "A die is thrown once. The probability of getting a prime number is:", "1/3", "1/2", "2/3", "1/6", "B")
b.m("A", PR, "One card is drawn at random from a well-shuffled pack of 52 cards. The probability that it is a red king is:", "1/13", "1/52", "1/26", "1/4", "C")

b.ar("A", RN, "√3 is an irrational number.", "The square root of every positive integer is an irrational number.", "C")
b.ar("A", AP, "The sum of the first n odd natural numbers is n².", "The sum of the first n terms of an AP is given by Sₙ = (n/2)[2a + (n − 1)d].", "A")
b.ar("A", CI, "The tangent at any point of a circle is perpendicular to the radius through the point of contact.", "The lengths of the two tangents drawn from an external point to a circle are equal.", "B")

# ── SECTION B — VSA ──
b.q("VSA", "B", RN, "Given that √3 is irrational, prove that 5 − √3 is an irrational number.")
b.q("VSA", "B", LE, "Solve the following pair of linear equations:\n2x + 3y = 11\n2x − 4y = −24")
b.q("VSA", "B", QE, "Find the value of k for which the quadratic equation kx² − 2kx + 6 = 0 has two equal roots.")
b.q("VSA", "B", CG, "Find the ratio in which the y-axis divides the line segment joining the points (5, −6) and (−1, −4).")
b.q("VSA", "B", TG, "Evaluate: 2 tan² 45° + cos² 30° − sin² 60°")
b.q("VSA", "B", PR, "Two dice are thrown at the same time. Find the probability that the sum of the two numbers appearing on them is 8.")
b.q("VSA", "B", CI, "Prove that the tangents drawn at the ends of a diameter of a circle are parallel.")

# ── SECTION C — SA ──
b.q("SA", "C", PO, "Find the zeroes of the polynomial 6x² − 7x − 3 and verify the relationship between the zeroes and the coefficients.")
b.q("SA", "C", LE, "The sum of the digits of a two-digit number is 9. Nine times this number is twice the number obtained by reversing the order of its digits. Find the number.")
b.q("SA", "C", AP, "Which term of the AP 3, 15, 27, 39, ... will be 132 more than its 54th term?")
b.q("SA", "C", TR, "In ΔABC, D and E are points on the sides AB and AC respectively such that DE ∥ BC. If AD = x, DB = x − 2, AE = x + 2 and EC = x − 1, find the value of x.")
b.q("SA", "C", TG, "Prove that: (sin θ − 2 sin³ θ) / (2 cos³ θ − cos θ) = tan θ")
b.q("SA", "C", CI, "Prove that a parallelogram circumscribing a circle is a rhombus.")
b.q("SA", "C", AC, "In a circle of radius 21 cm, an arc subtends an angle of 60° at the centre. Find (a) the length of the arc, (b) the area of the sector formed by the arc and (c) the perimeter of the sector. (Use π = 22/7)")
b.q("SA", "C", ST, "Find the mean of the following frequency distribution:\nClass: 0-10, 10-20, 20-30, 30-40, 40-50\nFrequency: 5, 8, 15, 16, 6")

# ── SECTION D — LA ──
b.q("LA", "D", QE, "A train travels a distance of 480 km at a uniform speed. If the speed had been 8 km/h more, it would have taken 3 hours less for the same journey. Find the speed of the train.\nOR\nTwo water taps together can fill a tank in 6 hours. The tap of larger diameter takes 5 hours less than the smaller one to fill the tank separately. Find the time in which each tap can separately fill the tank.")
b.q("LA", "D", AT, "From the top of a 9 m high building, the angle of elevation of the top of a cable tower is 60° and the angle of depression of its foot is 45°. Determine the height of the tower.\nOR\nAs observed from the top of a 60 m high lighthouse above sea level, the angles of depression of two ships are 30° and 45°. If one ship is exactly behind the other on the same side of the lighthouse, find the distance between the two ships.")
b.q("LA", "D", SV, "A toy is in the form of a cone of radius 7 cm mounted on a hemisphere of the same radius. The total height of the toy is 31 cm. Find the total surface area of the toy. (Use π = 22/7)\nOR\nA tent is in the shape of a cylinder surmounted by a conical top. The height and diameter of the cylindrical part are 3 m and 7 m respectively, and the slant height of the top is 5 m. Find the area of the canvas used for making the tent. Also find the cost of the canvas at the rate of ₹400 per m². (Use π = 22/7)")
b.q("LA", "D", ST, "Find the median and the mode of the following frequency distribution:\nClass: 0-20, 20-40, 40-60, 60-80, 80-100, 100-120, 120-140\nFrequency: 6, 8, 10, 12, 6, 5, 3")

# ── SECTION E — CASE STUDY ──
b.q("CBQ", "E", AP, "Riya decides to save money from her pocket money to buy a gift for her grandmother. She saves ₹50 in the first week and then increases her weekly saving by ₹20 every week.\n(a) Write the common difference of the AP formed by her weekly savings.\n(b) How much does she save in the 10th week?\n(c) Find the total amount she saves in the first 12 weeks.\nOR\n(c) In which week will her saving for that week be ₹410?")
b.q("CBQ", "E", CG, "A town planner marks three places on a coordinate grid, in which each unit represents 1 km: the school at A(2, 3), the library at B(6, 7) and the park at C(8, 3).\n(a) Find the distance between the school and the library.\n(b) Find the coordinates of the point exactly midway between the school and the park.\n(c) A bus stop is to be built on the road AB such that it divides AB in the ratio 1 : 3 from the school's side. Find the coordinates of the bus stop.\nOR\n(c) Find the lengths BC and AC and state whether triangle ABC is isosceles.")
b.q("CBQ", "E", PR, "At a school fair, a game stall has a spinner with eight equal sectors numbered 1 to 8. A player spins the arrow once, and it is equally likely to stop on any one of the eight numbers.\n(a) Find the probability that the arrow stops on an odd number.\n(b) Find the probability that it stops on a number greater than 6.\n(c) A prize is given if the arrow stops on a prime number. Find the probability of winning a prize.\nOR\n(c) Find the probability that the arrow stops on (i) a multiple of 3 and (ii) a factor of 8.")

b.save()
