"""Learn section articles (WHY? explainers). Each article pairs with a WHY? reel.

Fields:
  slug       URL: /learn/<slug>.html
  reel       WHY? reel module name (finds the video in formula-posts/why/queue or /posted and its thumbnail)
  published  YYYY-MM-DD — the article goes live on the site on/after this date (lets articles roll out with the reels)
  body       article HTML (h2 / p / ul / ol / table / pre allowed)
  practice   [(question, answer)] shown as "Try it yourself"
  related    [(label, href relative to site root)]
"""

AUTHOR = "Biswarup Mukherjee"
AUTHOR_ROLE = "Teaching Administrator, CBSEMock"

ARTICLES = [
{
"slug": "why-is-area-of-circle-pi-r-squared",
"reel": "circle_area",
"title": "Why is the area of a circle πr²? A picture proof for Class 10",
"h1": "Why is the area of a circle πr²?",
"description": "See why the area of a circle is πr² by unrolling it into a triangle — a picture proof for CBSE Class 10 Maths, with a worked example and practice questions.",
"category": "Maths", "class_label": "Class 10", "published": "2026-11-15", "read_min": 5,
"body": """
<p>Every Class 10 student can write <b>A = πr²</b>. Far fewer can say <i>why</i> it is true — and that is exactly what an examiner is testing when a question asks you to “justify” a formula or when a word problem looks unfamiliar. The good news: the reason fits into one picture.</p>

<h2>The short answer</h2>
<p>Cut a circle into very thin rings, straighten every ring into a strip and stack the strips. They form a triangle whose base is the circumference, <b>2πr</b>, and whose height is the radius, <b>r</b>. The area of that triangle is ½ × 2πr × r = <b>πr²</b>. Nothing was added or removed, so the circle has the same area.</p>

<h2>Step 1: think of a circle as rings</h2>
<p>Imagine the circle is made of very thin rings, like the layers of an onion or the grooves of a vinyl record. The innermost ring is tiny; the outermost ring runs right around the edge. The length of any ring is its circumference, so a ring at distance x from the centre has length <b>2πx</b>. The outermost ring, at distance r, has length <b>2πr</b>.</p>

<h2>Step 2: cut and straighten every ring</h2>
<p>Snip each ring at the bottom and pull it out straight. Each ring becomes a thin strip. Lay the strips on top of one another, the longest (outermost ring) at the bottom and the shortest (centre) at the top. Because the ring lengths grow evenly — 2πx grows in direct proportion to x — the stack narrows evenly from bottom to top. In other words, the stack is a <b>triangle</b>.</p>

<h2>Step 3: read off the base and height</h2>
<ul>
  <li><b>Base</b> = length of the outermost ring = <b>2πr</b>.</li>
  <li><b>Height</b> = number of rings × thickness = the distance from centre to edge = <b>r</b>.</li>
</ul>
<p>So the area of the triangle is ½ × base × height = ½ × 2πr × r = <b>πr²</b>. Since we only rearranged the pieces of the circle, the circle's area is also πr².</p>

<h2>Why is this more than a trick?</h2>
<p>This “slice it thin and add up the pieces” idea is the heart of <b>integration</b>, which you will meet properly in Class 12. Adding up rings of area 2πx · dx from x = 0 to x = r gives exactly πr². The picture you just saw is the integral in disguise. It also explains why area always involves <i>r²</i>: one factor of r comes from the size of the rings and the other from how many rings there are.</p>

<h2>A worked example</h2>
<p><b>Q.</b> A circular park has a radius of 21 m. Find its area. (Take π = 22/7.)</p>
<p><b>A.</b> Area = πr² = (22/7) × 21 × 21 = 22 × 3 × 21 = <b>1386 m²</b>.</p>
<p>Notice how choosing π = 22/7 makes the arithmetic clean when the radius is a multiple of 7 — a hint the board often gives deliberately.</p>

<h2>Common mistakes to avoid</h2>
<ul>
  <li><b>Using the diameter in place of the radius.</b> If the question gives d = 14 cm, the radius is 7 cm, so the area is 154 cm², not 616 cm².</li>
  <li><b>Mixing up area and circumference.</b> Area (πr²) is in square units; circumference (2πr) is in plain units. Check your units.</li>
  <li><b>Forgetting to square only the radius.</b> πr² means π × r × r, not (πr)².</li>
</ul>
""",
"practice": [
  ("Find the area of a circle whose circumference is 44 cm. (Take π = 22/7.)", "2πr = 44 ⇒ r = 7 cm. Area = (22/7) × 7 × 7 = 154 cm²."),
  ("If the radius of a circle is doubled, what happens to its area?", "Area becomes π(2r)² = 4πr², so it becomes four times as large."),
  ("A wheel has a diameter of 28 cm. Find its area.", "r = 14 cm. Area = (22/7) × 14 × 14 = 616 cm²."),
],
"related": [("Class 10 Maths Standard mock tests", "cbse-class-10-maths-standard-mock-tests.html"),
            ("Class 10 Maths Basic mock tests", "cbse-class-10-maths-basic-mock-tests.html"),
            ("Formula Board: quick revision cards", "formula-board/")],
},
{
"slug": "how-does-a-computer-see-an-image",
"reel": "computer_vision",
"title": "How does a computer see an image? Computer Vision explained simply",
"h1": "How does a computer see an image?",
"description": "Pixels, RGB numbers, filters and edges — how computer vision lets a machine recognise a face. A clear explainer for the CBSE AI curriculum (Class 10 and 12).",
"category": "AI", "class_label": "Class 10 · 12", "published": "2026-11-15", "read_min": 5,
"body": """
<p>When you look at a photo of a friend, you recognise them instantly. A computer looking at the same photo starts with something much less helpful: a long list of numbers. <b>Computer Vision</b>, one of the three domains of AI in the CBSE syllabus, is the art of turning those numbers back into meaning.</p>

<h2>The short answer</h2>
<p>A digital image is a grid of <b>pixels</b>, and every pixel is stored as numbers. A computer “sees” by sliding small <b>filters</b> over these numbers to find places where they change sharply — edges. Layer by layer, edges combine into shapes and shapes into objects such as eyes, wheels or faces.</p>

<h2>Step 1: an image is a grid of pixels</h2>
<p>Zoom far enough into any picture and it breaks into tiny squares called pixels. A 1080 × 1080 image has over a million of them. Each pixel holds a single colour, and the computer stores that colour as a number.</p>

<h2>Step 2: every pixel is a number</h2>
<p>In a <b>grayscale</b> image each pixel is one number from <b>0 (black) to 255 (white)</b>; values in between are shades of grey. A <b>colour</b> image stores three numbers per pixel — the amounts of <b>Red, Green and Blue (RGB)</b>, each from 0 to 255. Pure red is (255, 0, 0); white is (255, 255, 255). So a colour photo is really three grids of numbers stacked together.</p>

<h2>Step 3: filters find edges</h2>
<p>To find shapes, the computer slides a small grid of weights — a <b>filter</b> or <b>kernel</b>, often 3 × 3 — across the image. At each position it multiplies the filter's weights by the pixel values underneath and adds them up. In smooth regions the total stays small; where the numbers jump suddenly, such as the border between a dark eye and light skin, the total becomes large. Those large values mark <b>edges</b>.</p>

<h2>Step 4: layers build understanding</h2>
<p>A <b>Convolutional Neural Network (CNN)</b> stacks many such filter layers. The first layers detect simple edges and corners. Later layers combine edges into textures and parts (an eye, a nose), and the final layers combine parts into whole objects (a face). The network is not told which filters to use — it learns them from thousands of labelled example images during training.</p>

<h2>Where you meet computer vision every day</h2>
<ul>
  <li>Face unlock on phones and face-tagging in photo apps.</li>
  <li>Scanning documents and reading text from images (OCR).</li>
  <li>Self-driving cars detecting lanes, signs and pedestrians.</li>
  <li>Medical imaging that highlights possible problems in X-rays and scans.</li>
</ul>

<h2>How this appears in exams</h2>
<p>Board questions typically ask you to define a pixel, explain resolution, state what an RGB value represents, or identify the AI domain of an application (“A phone that unlocks when it sees your face uses which domain of AI?” — Computer Vision). Case-study questions may describe a scenario and ask how images are turned into data the model can use.</p>
""",
"practice": [
  ("What is the range of values for a pixel in an 8-bit grayscale image, and what do the ends represent?", "0 to 255; 0 is black and 255 is white."),
  ("How many numbers are needed to store one pixel of a colour (RGB) image?", "Three — one each for the red, green and blue intensity."),
  ("Name the AI domain used by a traffic camera that reads number plates.", "Computer Vision (reading text from images is optical character recognition, a computer-vision task)."),
],
"related": [("Class 10 AI mock papers", "cbse-class-10-ai-mock-papers.html"),
            ("Neural Networks & AI Ethics quiz", "chapters/neural-networks-10.html"),
            ("Introduction to AI quiz", "chapters/ai-introduction-10.html")],
},
{
"slug": "why-is-binary-search-so-fast",
"reel": "binary_search",
"title": "Why is binary search so fast? log₂ n explained for Class 12 CS",
"h1": "Why is binary search so fast?",
"description": "How binary search finds one item among 1,000 in about 10 steps — halving, log₂ n, a Python implementation and exam tips for CBSE Class 12 Computer Science.",
"category": "Computer Science", "class_label": "Class 12", "published": "2026-11-15", "read_min": 6,
"body": """
<p>Suppose a list holds 1,000 sorted roll numbers and you want to know whether 741 is among them. Checking one by one might take all 1,000 comparisons. <b>Binary search</b> needs at most <b>10</b>. Here is why.</p>

<h2>The short answer</h2>
<p>Binary search looks at the <b>middle</b> element of a <b>sorted</b> list. If that is not the target, it throws away the half that cannot contain the target and repeats on the other half. Every step halves what is left, so 1,000 → 500 → 250 → … → 1 takes about <b>log₂ 1000 ≈ 10</b> steps.</p>

<h2>Linear search: the slow way</h2>
<p>Linear search checks elements one after another from the start. In the worst case — the item is last or missing — it makes <b>n</b> comparisons. Its time complexity is <b>O(n)</b>. It works on unsorted lists, which is its one advantage.</p>

<h2>Binary search: the fast way</h2>
<ol>
  <li>Set <code>low</code> to the first index and <code>high</code> to the last.</li>
  <li>Find <code>mid = (low + high) // 2</code>.</li>
  <li>If <code>L[mid]</code> equals the target, you are done.</li>
  <li>If the target is bigger, it can only be to the right: set <code>low = mid + 1</code>.</li>
  <li>If the target is smaller, set <code>high = mid - 1</code>.</li>
  <li>Repeat while <code>low ≤ high</code>. If the range becomes empty, the item is not present.</li>
</ol>

<pre><code>def binary_search(L, target):
    low, high = 0, len(L) - 1
    while low &lt;= high:
        mid = (low + high) // 2
        if L[mid] == target:
            return mid            # found: return its index
        elif L[mid] &lt; target:
            low = mid + 1         # discard the left half
        else:
            high = mid - 1        # discard the right half
    return -1                     # not found</code></pre>

<h2>Where does log₂ n come from?</h2>
<p>After k steps, at most n ÷ 2ᵏ elements remain. The search ends when only one is left, i.e. when 2ᵏ ≥ n, so k = log₂ n. Doubling the list adds just <b>one</b> extra step: a million items need only about 20.</p>
<table>
  <tr><th>List size n</th><th>Linear search (worst)</th><th>Binary search (worst)</th></tr>
  <tr><td>16</td><td>16</td><td>4–5</td></tr>
  <tr><td>1,000</td><td>1,000</td><td>10</td></tr>
  <tr><td>1,000,000</td><td>1,000,000</td><td>20</td></tr>
</table>

<h2>The catch</h2>
<p>Binary search only works on a <b>sorted</b> list. If the data is unsorted, you must sort it first (which itself takes time) or fall back on linear search. For a list you search only once, linear search can be the better choice; for a list you search again and again, sorting once and using binary search wins easily.</p>

<h2>Exam tips</h2>
<ul>
  <li>Be ready to <b>trace</b> the values of low, mid and high for a given list and target — a favourite 3-mark question.</li>
  <li>State the precondition (sorted data) whenever you describe binary search.</li>
  <li>Use integer division <code>//</code> for mid; <code>/</code> gives a float and breaks list indexing.</li>
</ul>
""",
"practice": [
  ("How many comparisons, at most, does binary search need for a sorted list of 64 elements?", "log₂ 64 = 6, so about 6–7 comparisons in the worst case."),
  ("Trace binary search for 23 in [3, 8, 15, 23, 42, 57, 61]: list the mid values checked.", "low=0, high=6 → mid=3 → L[3]=23, found in one step."),
  ("Why can't binary search be used directly on [9, 2, 7, 4]?", "The list is not sorted, so discarding half the list after one comparison is not valid."),
],
"related": [("Class 12 Computer Science mock papers", "cbse-class-12-computer-science-mock-papers.html"),
            ("Data Structures (Stack) quiz", "chapters/data-structures-12.html"),
            ("Python Functions & Modules quiz", "chapters/python-functions-12.html")],
},
{
"slug": "why-is-sin2-plus-cos2-equal-to-1",
"reel": "trig_identity",
"title": "Why is sin²θ + cos²θ = 1? The unit-circle proof for Class 10",
"h1": "Why is sin²θ + cos²θ = 1?",
"description": "Prove sin²θ + cos²θ = 1 with one unit-circle picture and Pythagoras — plus the two related identities, worked examples and practice for CBSE Class 10.",
"category": "Maths", "class_label": "Class 10", "published": "2026-11-15", "read_min": 5,
"body": """
<p><b>sin²θ + cos²θ = 1</b> is the most used identity in trigonometry. It appears in proofs, simplifications and “find the value” questions in almost every Class 10 paper. It is also one of the easiest formulas to <i>see</i>.</p>

<h2>The short answer</h2>
<p>In a right-angled triangle with hypotenuse 1, the two shorter sides are cos θ and sin θ. Pythagoras' theorem then says cos²θ + sin²θ = 1² = 1.</p>

<h2>Step 1: draw a unit circle</h2>
<p>Draw a circle of radius 1 with its centre at the origin. Mark a point P on the circle so that the radius OP makes an angle θ with the x-axis.</p>

<h2>Step 2: make a right-angled triangle</h2>
<p>Drop a perpendicular from P to the x-axis at M. Triangle OMP is right-angled at M, with:</p>
<ul>
  <li>hypotenuse OP = 1 (the radius),</li>
  <li>base OM = OP cos θ = <b>cos θ</b>,</li>
  <li>height MP = OP sin θ = <b>sin θ</b>.</li>
</ul>

<h2>Step 3: apply Pythagoras</h2>
<p>OM² + MP² = OP² gives <b>cos²θ + sin²θ = 1</b>. As P moves round the circle the triangle changes shape, but the hypotenuse is always the radius, 1 — so the identity holds for every angle.</p>

<h2>The same proof without a circle</h2>
<p>In any right triangle ABC (right angle at B), sin A = BC/AC and cos A = AB/AC. Then sin²A + cos²A = (BC² + AB²)/AC² = AC²/AC² = 1, using Pythagoras (AB² + BC² = AC²). This is the version CBSE expects in a written proof.</p>

<h2>Two more identities for free</h2>
<p>Divide sin²θ + cos²θ = 1 by cos²θ and you get <b>tan²θ + 1 = sec²θ</b>. Divide it by sin²θ and you get <b>1 + cot²θ = cosec²θ</b>. Remember one identity and you have all three.</p>

<h2>A worked example</h2>
<p><b>Q.</b> If sin θ = 3/5 and θ is acute, find cos θ and tan θ.</p>
<p><b>A.</b> cos²θ = 1 − sin²θ = 1 − 9/25 = 16/25, so cos θ = 4/5 (positive, since θ is acute). tan θ = sin θ / cos θ = (3/5) ÷ (4/5) = <b>3/4</b>.</p>

<h2>Common mistakes</h2>
<ul>
  <li>Writing sin²θ as sin(θ²). sin²θ means (sin θ)².</li>
  <li>Forgetting that cos θ could be negative for angles beyond 90°. In Class 10, angles are acute, so take the positive root — but say so.</li>
  <li>Starting a “prove that” question from the result. Begin from one side (usually the more complicated one) and work towards the other.</li>
</ul>
""",
"practice": [
  ("If cos θ = 12/13 (θ acute), find sin θ.", "sin²θ = 1 − 144/169 = 25/169, so sin θ = 5/13."),
  ("Simplify (1 − sin²θ) sec²θ.", "1 − sin²θ = cos²θ, and cos²θ × sec²θ = 1."),
  ("Prove that sec²θ − tan²θ = 1.", "Divide sin²θ + cos²θ = 1 by cos²θ: tan²θ + 1 = sec²θ, so sec²θ − tan²θ = 1."),
],
"related": [("Class 10 Maths Standard mock tests", "cbse-class-10-maths-standard-mock-tests.html"),
            ("Triangles quiz", "chapters/triangles-10.html"),
            ("Formula Board: quick revision cards", "formula-board/")],
},
{
"slug": "how-does-an-ai-neuron-make-a-decision",
"reel": "neuron",
"title": "How does an AI neuron make a decision? Weights and thresholds explained",
"h1": "How does an AI neuron make a decision?",
"description": "Inputs, weights, weighted sum and threshold — how a single artificial neuron decides, with a worked example. Neural networks explained for CBSE AI Class 10 and 12.",
"category": "AI", "class_label": "Class 10 · 12", "published": "2026-11-15", "read_min": 5,
"body": """
<p>Neural networks power voice assistants, image recognition and chatbots, yet each one is built from a very simple unit: the <b>artificial neuron</b>. Understand one neuron and the rest of a neural network stops being mysterious.</p>

<h2>The short answer</h2>
<p>A neuron takes several <b>inputs</b>, multiplies each by a <b>weight</b> that says how important it is, adds the results, and compares the total with a <b>threshold</b>. If the total crosses the threshold, the neuron “fires” (outputs 1); otherwise it stays off (outputs 0).</p>

<h2>An everyday example: should I go out to play?</h2>
<p>Suppose the decision depends on three yes/no inputs (1 = yes, 0 = no), each with a weight:</p>
<table>
  <tr><th>Input</th><th>Value</th><th>Weight</th><th>Value × weight</th></tr>
  <tr><td>Is it sunny?</td><td>1</td><td>0.4</td><td>0.4</td></tr>
  <tr><td>Are friends free?</td><td>1</td><td>0.3</td><td>0.3</td></tr>
  <tr><td>Is homework done?</td><td>0</td><td>0.6</td><td>0</td></tr>
</table>
<p>The <b>weighted sum</b> is 0.4 + 0.3 + 0 = <b>0.7</b>. With a threshold of 1.0, the neuron stays off: stay home. Now finish the homework: the sum becomes 0.4 + 0.3 + 0.6 = <b>1.3</b>, which crosses the threshold, so the neuron fires: go and play. Homework has the largest weight, so it matters most to the decision — exactly what the weights are for.</p>

<h2>The general rule</h2>
<p>For inputs x₁, x₂, …, xₙ with weights w₁, w₂, …, wₙ:</p>
<p><b>z = w₁x₁ + w₂x₂ + … + wₙxₙ + b</b>, and the output is 1 if z crosses the threshold, otherwise 0.</p>
<p>The <b>bias b</b> shifts the threshold, making the neuron easier or harder to fire. In modern networks the hard yes/no step is replaced by a smooth <b>activation function</b> (such as sigmoid or ReLU), which lets the network learn gradually.</p>

<h2>How a neuron learns</h2>
<p>Nobody sets the weights by hand. During <b>training</b>, the network sees many examples with known answers. Each time its output is wrong, the weights are nudged slightly in the direction that would have reduced the error. After thousands of examples, the weights settle on values that give good decisions — this is what “learning from data” means.</p>

<h2>From one neuron to a network</h2>
<p>One neuron can only draw a straight dividing line between “yes” and “no”. Connect many neurons in <b>layers</b> — an input layer, one or more hidden layers and an output layer — and the network can learn curved, complex boundaries. That is how it recognises faces, voices and handwriting.</p>

<h2>How this appears in exams</h2>
<p>Expect questions that ask you to label the input, hidden and output layers, explain the role of weights, or calculate a weighted sum and decide the output for a given threshold — exactly like the example above.</p>
""",
"practice": [
  ("Inputs (1, 0, 1) with weights (0.5, 0.2, 0.4) and threshold 0.8. Does the neuron fire?", "Sum = 0.5 + 0 + 0.4 = 0.9 ≥ 0.8, so yes, it fires (output 1)."),
  ("What does a larger weight on an input tell you?", "That input has more influence on the neuron's decision."),
  ("Name the three types of layers in a basic neural network.", "Input layer, hidden layer(s) and output layer."),
],
"related": [("Neural Networks & AI Ethics quiz", "chapters/neural-networks-10.html"),
            ("Machine Learning Concepts quiz", "chapters/ml-concepts-10.html"),
            ("Class 10 AI mock papers", "cbse-class-10-ai-mock-papers.html")],
},
{
"slug": "why-is-0-1-plus-0-2-not-0-3-in-python",
"reel": "float_sum",
"title": "Why is 0.1 + 0.2 not 0.3 in Python? Floating point explained",
"h1": "Why is 0.1 + 0.2 not equal to 0.3 in Python?",
"description": "Why Python prints 0.30000000000000004 for 0.1 + 0.2 — binary fractions, floating-point rounding, and the right way to compare decimals (round, math.isclose). CBSE Class 12 CS.",
"category": "Computer Science", "class_label": "Class 12", "published": "2026-11-15", "read_min": 5,
"body": """
<p>Open Python and type <code>0.1 + 0.2</code>. You expect <code>0.3</code>. Python prints <code>0.30000000000000004</code>, and <code>0.1 + 0.2 == 0.3</code> gives <code>False</code>. Python is not broken — this happens in almost every programming language, and the reason is a lovely piece of number theory.</p>

<h2>The short answer</h2>
<p>Computers store numbers in <b>binary</b>. Just as 1/3 never ends in decimal (0.333…), <b>1/10 never ends in binary</b>. The computer must cut it off after a fixed number of bits, so 0.1 and 0.2 are stored as numbers a tiny bit away from their true values. Adding them makes the tiny errors visible.</p>

<h2>Step 1: some fractions never end</h2>
<p>In decimal (base 10), a fraction terminates only if its denominator has no prime factors other than 2 and 5. That is why 1/4 = 0.25 ends but 1/3 = 0.333… goes on forever. In binary (base 2), a fraction terminates only if its denominator is a power of 2. So 1/2 = 0.1₂ and 1/4 = 0.01₂ are exact, but <b>1/10 = 0.0001100110011…₂</b> repeats forever, because 10 = 2 × 5 contains the factor 5.</p>

<h2>Step 2: the computer has to round</h2>
<p>Python's <code>float</code> uses the IEEE-754 double-precision format, which keeps about <b>53 significant binary digits</b>. The endless binary pattern for 0.1 is cut off and rounded, so what is stored is actually 0.1000000000000000055511151231257827… Similarly 0.2 is stored slightly above 0.2.</p>

<h2>Step 3: the errors add up</h2>
<p>When you add the two stored values, their tiny errors add too. The result is the double closest to 0.30000000000000004, which is <i>not</i> the same double that Python uses for 0.3. Python prints enough digits to tell them apart — hence the surprise.</p>

<h2>How to compare decimals safely</h2>
<pre><code>import math

a = 0.1 + 0.2
print(a == 0.3)                 # False  — avoid == with floats
print(round(a, 2) == 0.3)       # True   — round to the precision you need
print(math.isclose(a, 0.3))     # True   — the recommended way</code></pre>
<p>For money, where every paisa must be exact, use the <code>decimal</code> module (<code>from decimal import Decimal</code>) or store amounts as whole numbers of paise.</p>

<h2>Why this matters for exams</h2>
<ul>
  <li>Output-prediction questions sometimes include float arithmetic — remember that results like 0.1 + 0.2 do not print as 0.3.</li>
  <li>When writing conditions on calculated decimal values, use <code>round()</code> rather than <code>==</code>.</li>
  <li>The underlying idea — binary representation and its limits — links to the number-system topics in Class 11.</li>
</ul>
""",
"practice": [
  ("Which of these fractions can be stored exactly in binary: 1/2, 1/5, 3/8?", "1/2 and 3/8 (denominators are powers of 2); 1/5 cannot."),
  ("What does print(round(0.1 + 0.2, 1)) display?", "0.3"),
  ("Write a condition that safely checks whether the float x equals 1.1.", "math.isclose(x, 1.1)  — or round(x, 2) == 1.1"),
],
"related": [("Class 12 Computer Science mock papers", "cbse-class-12-computer-science-mock-papers.html"),
            ("Python Functions & Modules quiz", "chapters/python-functions-12.html"),
            ("Informatics Practices practice papers", "cbse-class-12-informatics-practices-practice-papers.html")],
},
]
