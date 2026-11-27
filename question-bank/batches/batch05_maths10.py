"""Batch 05 — Class 10 Mathematics: two more papers' worth (plus spares). Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("maths10")
RN, PO, LE, QE, AP = "Real Numbers", "Polynomials", "Pair of Linear Equations in Two Variables", "Quadratic Equations", "Arithmetic Progressions"
TR, CG, TG, AT = "Triangles", "Coordinate Geometry", "Introduction to Trigonometry", "Some Applications of Trigonometry"
CI, AC, SV, ST, PR = "Circles", "Areas Related to Circles", "Surface Areas and Volumes", "Statistics", "Probability"

# ── SECTION A — MCQ ──
b.m("A", RN, "The HCF of 2³ × 3² × 5 and 2² × 3³ × 7 is:", "36", "72", "108", "180", "A")
b.m("A", RN, "The LCM of 18, 24 and 30 is:", "120", "180", "360", "720", "C")
b.m("A", RN, "Which of the following is a rational number?", "3 + √5", "√2 × √18", "√7 / 2", "2π", "B")
b.m("A", PO, "If α and β are the zeroes of the polynomial x² − 7x + 10, then the value of α²β + αβ² is:", "17", "70", "49", "100", "B")
b.m("A", PO, "A quadratic polynomial, the sum of whose zeroes is 5 and the product of whose zeroes is −6, is:", "x² + 5x − 6", "x² − 5x + 6", "x² + 5x + 6", "x² − 5x − 6", "D")
b.m("A", LE, "The value of k for which the lines kx + 3y = 7 and 2x + 6y = 5 are parallel is:", "1", "2", "3", "6", "A")
b.m("A", LE, "The pair of linear equations y = 0 and y = −5 has:", "exactly one solution", "exactly two solutions", "infinitely many solutions", "no solution", "D")
b.m("A", QE, "The sum of the roots of the quadratic equation 2x² − 9x + 4 = 0 is:", "9/2", "−9/2", "2", "4", "A")
b.m("A", QE, "If x = 2 is a root of the equation 3x² + px − 8 = 0, then the value of p is:", "−2", "2", "4", "−4", "A")
b.m("A", QE, "The quadratic equation x² − 4x + k = 0 has no real roots when:", "k < 4", "k = 4", "k > 4", "k ≤ 4", "C")
b.m("A", AP, "The sum of the first 10 terms of the AP 4, 9, 14, 19, ... is:", "245", "255", "265", "275", "C")
b.m("A", AP, "The number of terms in the AP 5, 9, 13, ..., 81 is:", "20", "19", "21", "18", "A")
b.m("A", AP, "The 8th term of an AP whose first term is −5 and common difference is 3 is:", "16", "19", "13", "21", "A")
b.m("A", TR, "ΔABC ~ ΔPQR and AB/PQ = 2/3. If the perimeter of ΔPQR is 45 cm, then the perimeter of ΔABC is:", "20 cm", "67.5 cm", "30 cm", "15 cm", "C")
b.m("A", TR, "In ΔDEF, a line parallel to EF meets DE at X and DF at Y. If DX : XE = 3 : 4 and DF = 14 cm, then DY is equal to:", "8 cm", "6 cm", "10.5 cm", "7 cm", "B")
b.m("A", CG, "If the distance between the points (4, p) and (1, 0) is 5 units, then the value of p is:", "4 only", "±4", "−4 only", "0", "B")
b.m("A", CG, "If (2, 3) is the mid-point of the line segment joining the points (a, 5) and (6, b), then the value of a + b is:", "1", "3", "5", "−1", "D")
b.m("A", TG, "If 5 cot θ = 12, where θ is an acute angle, then cosec θ is equal to:", "12/13", "5/12", "13/12", "13/5", "D")
b.m("A", TG, "The value of tan 60° × cot 30° − sec 0° is:", "0", "1", "2", "3", "C")
b.m("A", AT, "A kite is flying on a string 80 m long. If the string is straight and makes an angle of 30° with the level ground, the height of the kite above the ground is:", "40 m", "40√3 m", "80√3 m", "20 m", "A")
b.m("A", AT, "The height of a vertical tower and the length of its shadow on level ground are in the ratio 1 : √3. The angle of elevation of the sun is:", "45°", "60°", "90°", "30°", "D")
b.m("A", CI, "PA and PB are tangents drawn from an external point P to a circle with centre O. If ∠APB = 80°, then ∠POA is equal to:", "40°", "50°", "80°", "100°", "B")
b.m("A", CI, "A quadrilateral ABCD is drawn so that each of its sides touches a circle. If AB = 7 cm, BC = 8 cm and CD = 9 cm, then the length of AD is:", "6 cm", "10 cm", "8 cm", "7 cm", "C")
b.m("A", AC, "A sector of a circle of radius 21 cm has an arc of length 22 cm. The central angle of the sector is: (Use π = 22/7)", "30°", "60°", "90°", "120°", "B")
b.m("A", AC, "If the circumference of a circle and its area are numerically equal, then the radius of the circle is:", "4 units", "π units", "1 unit", "2 units", "D")
b.m("A", SV, "The volume of a solid hemisphere of radius 3 cm is:", "18π cm³", "36π cm³", "27π cm³", "9π cm³", "A")
b.m("A", SV, "A right circular cylinder and a right circular cone have equal base radii and equal heights. The ratio of the volume of the cylinder to that of the cone is:", "1 : 3", "1 : 1", "2 : 1", "3 : 1", "D")
b.m("A", ST, "The class mark of the class interval 25 − 35 is:", "10", "25", "30", "35", "C")
b.m("A", ST, "In the assumed mean method, the mean is found using x̄ = a + (Σfᵢdᵢ)/(Σfᵢ). Here dᵢ stands for:", "xᵢ + a", "xᵢ − a", "a − xᵢ", "xᵢ / a", "B")
b.m("A", ST, "For the distribution\nClass: 0-10, 10-20, 20-30, 30-40, 40-50\nFrequency: 5, 8, 12, 10, 5\nthe median class is:", "10-20", "30-40", "0-10", "20-30", "D")
b.m("A", PR, "Two coins are tossed together. The probability of getting at least one head is:", "1/4", "1/2", "3/4", "1", "C")
b.m("A", PR, "The six letters of the word SCHOOL are written on six identical cards, one letter on each card. If one card is picked at random, the probability that it shows the letter O is:", "1/2", "2/3", "1/6", "1/3", "D")
b.m("A", PR, "One card is drawn at random from a well-shuffled deck of 52 playing cards. The probability of drawing a red king is:", "1/13", "1/26", "1/52", "2/13", "B")

b.ar("A", RN, "The HCF of 18 and 25 is 1.", "Two numbers whose HCF is 1 are called co-prime numbers.", "B")
b.ar("A", TG, "For some acute angle θ, the value of sec θ can be 1/2.", "For every acute angle θ, 0 < cos θ < 1, so sec θ = 1/cos θ is always greater than 1.", "D")
b.ar("A", SV, "If the radius of a sphere is doubled, its volume becomes eight times the original volume.", "The volume of a sphere is directly proportional to the square of its radius.", "C")

# ── SECTION B — VSA ──
b.q("VSA", "B", RN, "Express 156 and 234 as products of their prime factors. Hence find their HCF and LCM.")
b.q("VSA", "B", PO, "If one zero of the polynomial 2x² + kx − 6 is 2, find the value of k and the other zero of the polynomial.")
b.q("VSA", "B", CG, "Using the distance formula, show that the points A(1, 2), B(4, 6) and C(7, 10) are collinear.")
b.q("VSA", "B", TG, "If 2 sin(A − B) = 1 and 2 cos(A + B) = 1, where A and B are acute angles and A > B, find the values of A and B.")
b.q("VSA", "B", CI, "From an external point P, two tangents PA and PB are drawn to a circle with centre O. If PA = 12 cm and ∠APB = 60°, find the length of the chord AB. Give reasons.")
b.q("VSA", "B", AC, "A sector of a circle of radius 10.5 cm has a central angle of 60°. Find the length of its arc and the area of the sector. (Use π = 22/7)")
b.q("VSA", "B", PR, "A bag contains 6 red balls, 4 green balls and some blue balls. If the probability of drawing a blue ball at random from the bag is 1/3, find the number of blue balls in the bag.")
b.q("VSA", "B", QE, "Find the roots of the quadratic equation 2x² − 7x + 3 = 0 by the method of factorisation.")
b.q("VSA", "B", AP, "The 5th term of an AP is 22 and its 9th term is 38. Find the AP and its 15th term.")

# ── SECTION C — SA ──
b.q("SA", "C", RN, "Prove that √5 is an irrational number. Hence show that 4 − 3√5 is also irrational.")
b.q("SA", "C", PO, "If α and β are the zeroes of the polynomial p(x) = x² − 6x + 8, find a quadratic polynomial whose zeroes are 2α + 1 and 2β + 1.")
b.q("SA", "C", LE, "A parking lot charges a fixed amount for the first two hours and a further fixed amount for every additional hour. Rahul paid ₹50 for parking his scooter for 5 hours and Sita paid ₹70 for 9 hours. Find the fixed charge for the first two hours and the charge for each additional hour. How much will a person pay for 12 hours?")
b.q("SA", "C", QE, "The sum of a positive number and its reciprocal is 17/4. Form a quadratic equation and find the number.")
b.q("SA", "C", AP, "How many terms of the AP 27, 24, 21, ... must be taken so that their sum is 126? Explain why there are two answers.")
b.q("SA", "C", TR, "In ΔPQR, ∠PQR = 90° and QS is perpendicular to PR, meeting it at S. Prove that ΔPSQ ~ ΔQSR. If PS = 4 cm and SR = 9 cm, find the length of QS.")
b.q("SA", "C", CG, "Find the point P on the y-axis which is equidistant from the points A(6, 3) and B(−2, −1). Also find the length PA.")
b.q("SA", "C", TG, "Prove that cos A/(1 − sin A) + cos A/(1 + sin A) = 2 sec A. Hence find the value of the left-hand side when A = 60°.")
b.q("SA", "C", CI, "Prove that the line segment joining the points of contact of two parallel tangents to a circle passes through the centre of the circle.")
b.q("SA", "C", AC, "The pendulum of a clock is 42 cm long. It swings through an angle of 30° from one extreme position to the other. Find the length of the arc described by the tip of the pendulum and the area of the sector swept by the pendulum in one swing. (Use π = 22/7)")
b.q("SA", "C", ST, "Find the mean of the following frequency distribution using the step-deviation method:\nClass: 10-20, 20-30, 30-40, 40-50, 50-60\nFrequency: 6, 8, 12, 10, 4")

# ── SECTION D — LA ──
b.q("LA", "D", QE, "A tourist plans a trip with a budget of ₹6000 for daily expenses. If she extends her trip by 5 days, she has to reduce her daily expenses by ₹100. Find the original duration of the trip.\nOR\nThe hypotenuse of a right-angled triangle is 25 cm and the difference between the lengths of the other two sides is 5 cm. Form a quadratic equation and find the lengths of the other two sides.")
b.q("LA", "D", LE, "Two towns A and B are 160 km apart on a straight highway. One car starts from A and another from B at the same time. If the cars travel in the same direction, they meet after 8 hours. If they travel towards each other, they meet after 1 hour 20 minutes. Find the speeds of the two cars.\nOR\nA fraction becomes 7/10 if 2 is added to both its numerator and denominator. If 4 is added to both its numerator and denominator, it becomes 3/4. Find the fraction.")
b.q("LA", "D", AT, "A man standing on one bank of a river observes that the angle of elevation of the top of a tree standing on the opposite bank is 60°. When he moves 30 m away from the bank in the same straight line, the angle of elevation becomes 30°. Find the height of the tree and the width of the river. (Use √3 = 1.732)\nOR\nFrom a point 20 m above the surface of a still lake, the angle of elevation of a cloud is 30° and the angle of depression of its reflection in the lake is 60°. Find the height of the cloud above the lake.")
b.q("LA", "D", SV, "A model rocket is made of a solid right circular cylinder of radius 6 cm and height 10 cm, with a solid cone of the same radius and height 8 cm fixed on top of it. Find (a) the total surface area and (b) the volume of the model. (Use π = 3.14)\nOR\nA solid is made up of a right circular cylinder with a hemisphere fixed at one end and a cone fixed at the other end. The common radius is 7 cm, the height of the cylinder is 10 cm and the height of the cone is 24 cm. Find (a) the total surface area of the solid and (b) the volume of its cylindrical and conical parts together. (Use π = 22/7)")
b.q("LA", "D", ST, "Find the mean and the mode of the following frequency distribution:\nClass: 10-25, 25-40, 40-55, 55-70, 70-85\nFrequency: 6, 10, 16, 12, 6\nOR\nThe median of the following distribution is 32.5 and the sum of all the frequencies is 40. Find the values of x and y.\nClass: 0-10, 10-20, 20-30, 30-40, 40-50, 50-60\nFrequency: 4, x, 10, 12, y, 3")
b.q("LA", "D", AP, "An auditorium has 20 seats in the first row, 24 seats in the second row, 28 seats in the third row, and so on, for 25 rows.\n(a) How many seats are there in the auditorium?\n(b) Which row has 72 seats?\n(c) How many seats are there in the last five rows together?\nOR\nThe sum of the first 8 terms of an AP is 136 and the sum of its first 15 terms is 465. Find the AP and the sum of its first n terms.")
b.q("LA", "D", CI, "(a) Prove that the tangent at any point of a circle is perpendicular to the radius through the point of contact.\n(b) PQ is a chord of length 24 cm of a circle of radius 13 cm with centre O. The tangents at P and Q meet at a point T. Find the length TP.")

# ── SECTION E — CASE STUDY ──
b.q("CBQ", "E", RN, "For the school sports day, 144 students of Class IX and 180 students of Class X are to march in a parade. The PT teacher wants them to march in columns so that every column has the same number of students, all the students in a column are from the same class, and the number of columns is as small as possible.\n(a) What is the largest number of students that can march in each column?\n(b) How many columns will be formed in all?\n(c) Write 144 and 180 as products of prime factors and find their LCM.\nOR\n(c) Two bells in the school ring at intervals of 12 minutes and 18 minutes. If they ring together at 8:00 a.m., at what time will they next ring together?")
b.q("CBQ", "E", CG, "On a city map drawn on a coordinate grid, the hospital is at H(−2, 3) and the school is at S(4, −5). Each unit on the grid represents 1 km. A straight road joins the hospital and the school.\n(a) Find the distance between the hospital and the school.\n(b) A bus stop is to be built exactly midway between H and S. Find its coordinates.\n(c) A post office P lies on the road HS such that HP : PS = 1 : 3. Find the coordinates of P.\nOR\n(c) The road HS crosses the x-axis at a point. Find the ratio in which the x-axis divides HS and the coordinates of this point.")
b.q("CBQ", "E", AT, "A lighthouse stands 75 m high on a rocky coast. The keeper at the top watches a ship sailing straight towards the base of the lighthouse. At first, the angle of depression of the ship is 30°. A little later, it is 45°.\n(a) How far was the ship from the base of the lighthouse when the angle of depression was 30°?\n(b) How far is the ship from the base when the angle of depression is 45°?\n(c) Find the distance travelled by the ship between the two observations. (Use √3 = 1.732)\nOR\n(c) How far from the base will the ship be when the angle of depression becomes 60°? (Use √3 = 1.732)")
b.q("CBQ", "E", SV, "A farmer stores grain in a metal silo. The silo is a right circular cylinder of radius 3 m and height 10 m with a conical roof of the same radius and height 4 m.\n(a) Find the slant height of the conical roof.\n(b) Find the area of metal sheet needed to make the conical roof. (Use π = 3.14)\n(c) Find the volume of grain the cylindrical part can hold. (Use π = 3.14)\nOR\n(c) Find the total area of the outer curved surface of the silo (cylinder and roof together) that is to be painted. (Use π = 3.14)")
b.q("CBQ", "E", PR, "At a school fete, a box contains 40 tokens numbered 11 to 50, one number on each token. A visitor draws one token at random and wins a prize depending on the number drawn.\n(a) Find the probability that the number on the token is a multiple of 5.\n(b) Find the probability that the number is a perfect square.\n(c) Find the probability that the number is a prime number.\nOR\n(c) Find the probability that the number is divisible by both 2 and 3.")
b.q("CBQ", "E", AC, "A rotating garden sprinkler is fixed at a point O on a lawn. It throws water up to a distance of 21 m and turns back and forth through an angle of 60°, so that the region it waters is a sector of a circle.\n(a) Find the area of the lawn watered by the sprinkler. (Use π = 22/7)\n(b) Find the length of the curved outer edge of the watered region.\n(c) If the angle of turning is increased to 120°, how much more area will be watered?\nOR\n(c) Find the perimeter of the watered region.")

b.save()
