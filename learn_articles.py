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
{
"slug": "why-does-adding-resistors-in-parallel-lower-resistance",
"reel": "parallel_resistors",
"title": "Why does adding a resistor in parallel lower the resistance?",
"h1": "Why does adding a resistor in parallel lower the total resistance?",
"description": "Adding a resistor in parallel gives current an extra path, so total resistance falls. The road analogy, the 1/R formula derived, worked examples and exam traps for CBSE Class 10 and 12 Physics.",
"category": "Physics", "class_label": "Class 10 · 12", "published": "2026-11-18", "read_min": 6,
"body": """
<p>It feels wrong at first. You add <i>more</i> resistors to a circuit and the total resistance goes <i>down</i>. Yet that is exactly what happens when resistors are connected in parallel — and it is why every appliance in your home is wired in parallel. Once you see current as traffic, the result becomes obvious.</p>

<h2>The short answer</h2>
<p>A resistor in parallel does not sit in the way of the current — it opens a <b>new path</b> beside the old one. With the same battery voltage pushing, more paths let more current flow. Since <b>R = V / I</b>, a bigger current at the same voltage means a <b>smaller</b> total resistance.</p>

<h2>Think of current as cars on roads</h2>
<p>Picture the battery as a city that sends cars (charge) out, and each resistor as a road. With one narrow road, only so many cars get through each second — say 1 ampere. Now build a second, identical road right beside the first. Each road still carries 1 A, because each one still has the full voltage across it. Together they carry <b>2 A</b>. The city sees twice the traffic flowing for the same push, so the combination behaves like a road with <b>half</b> the resistance.</p>
<p>Compare this with <b>series</b>: putting a second road at the end of the first makes one longer road. Every car must travel both, so traffic slows and resistance adds up: R = R₁ + R₂.</p>

<h2>Deriving the formula</h2>
<ol>
  <li>In parallel, every resistor is connected across the same two points, so each has the <b>same voltage V</b>.</li>
  <li>The current through each is given by Ohm's law: I₁ = V/R₁ and I₂ = V/R₂.</li>
  <li>The main current splits and rejoins, so <b>I = I₁ + I₂</b> (charge is conserved).</li>
  <li>Write I = V/R for the whole combination: V/R = V/R₁ + V/R₂.</li>
  <li>Divide by V: <b>1/R = 1/R₁ + 1/R₂</b>.</li>
</ol>
<p>Because you are adding positive fractions, 1/R is bigger than either 1/R₁ or 1/R₂ alone — so R is always <b>smaller than the smallest resistor</b> in the group. That single fact lets you check your answers instantly.</p>

<h2>Worked examples</h2>
<p><b>Q1.</b> Two 6 Ω resistors are connected in parallel. Find the equivalent resistance.</p>
<p><b>A.</b> 1/R = 1/6 + 1/6 = 2/6, so R = <b>3 Ω</b>. Two equal resistors in parallel always give half of one: n equal resistors give R/n.</p>
<p><b>Q2.</b> 3 Ω and 6 Ω are in parallel across a 6 V battery. Find the total current.</p>
<p><b>A.</b> 1/R = 1/3 + 1/6 = 3/6, so R = 2 Ω. I = V/R = 6/2 = <b>3 A</b>. Check: 6/3 = 2 A through one branch and 6/6 = 1 A through the other, total 3 A. ✔</p>
<p>A handy shortcut for exactly two resistors: <b>R = R₁R₂ / (R₁ + R₂)</b> — “product over sum”. For 3 Ω and 6 Ω: 18/9 = 2 Ω.</p>

<h2>Why homes are wired in parallel</h2>
<ul>
  <li>Every appliance gets the full mains voltage (220 V in India).</li>
  <li>Each appliance can be switched on or off without affecting the others.</li>
  <li>If one bulb fuses, the others keep working — unlike old series fairy lights.</li>
</ul>
<p>The flip side: every appliance you switch on adds another path and the total current drawn from the mains rises. That is why overloading a socket is dangerous and why circuits need fuses or MCBs.</p>

<h2>Common mistakes</h2>
<ul>
  <li><b>Forgetting to flip at the end.</b> If 1/R = 1/2, then R = 2 Ω, not 0.5 Ω.</li>
  <li><b>Adding resistances in parallel.</b> Only series resistances add directly.</li>
  <li><b>Getting an answer larger than the smallest resistor.</b> In parallel that is impossible — recheck.</li>
</ul>
""",
"practice": [
  ("Three 9 Ω resistors are connected in parallel. What is the equivalent resistance?", "n equal resistors in parallel give R/n = 9/3 = 3 Ω."),
  ("A 4 Ω and a 12 Ω resistor are in parallel. Find the equivalent resistance.", "Product over sum: (4 × 12)/(4 + 12) = 48/16 = 3 Ω."),
  ("Why does a fused bulb not switch off the other bulbs in a house?", "House wiring is parallel, so each bulb is on its own path across the mains; breaking one path leaves the others complete."),
],
"related": [("Class 10 Science mock tests", "cbse-class-10-science-mock-tests.html"),
            ("Electricity (Class 10) quiz", "chapters/electricity-10.html"),
            ("Current Electricity (Class 12) quiz", "chapters/current-electricity-12.html"),
            ("Class 12 Physics mock papers", "cbse-class-12-physics-mock-papers.html")],
},
{
"slug": "why-can-ai-be-biased",
"reel": "ai_bias",
"title": "Why can AI be biased? Data, fairness and AI ethics explained",
"h1": "Why can an AI be biased?",
"description": "AI learns only from its training data, so biased data produces biased decisions. A hiring-AI example, types of bias and how to reduce them — AI ethics for CBSE AI Class 10 and 12.",
"category": "AI", "class_label": "Class 10 · 12", "published": "2026-11-22", "read_min": 5,
"body": """
<p>We often imagine computers as perfectly neutral: they just follow the numbers. So how can an AI system be unfair? The surprising answer is that an AI is only as fair as the <b>data</b> it learns from. This is one of the central ideas of <b>AI Ethics</b> in the CBSE AI curriculum.</p>

<h2>The short answer</h2>
<p>A machine-learning model has no opinions of its own. It finds patterns in its training examples and copies them. If the examples carry an unfair pattern from the past, the model learns that pattern too — and then repeats it automatically, at scale, on new people.</p>

<h2>A hiring example</h2>
<p>Imagine a company trains an AI to shortlist job applicants. It feeds the AI ten years of old hiring records. In those years, for reasons that had nothing to do with ability, almost everyone hired came from one group — call it Group A.</p>
<ol>
  <li>The AI studies the records and notices a strong pattern: applicants from Group A were usually hired.</li>
  <li>It quietly learns the rule “Group A means a good candidate”.</li>
  <li>A brilliant applicant from Group B, with top marks, applies. The AI scores them low and rejects them.</li>
</ol>
<p>The AI did exactly what it was trained to do. The problem was never the algorithm's arithmetic; it was the history baked into the data. This really happened with a large technology company's experimental recruiting tool, which was scrapped after it was found to favour male candidates.</p>

<h2>Where bias comes from</h2>
<ul>
  <li><b>Historical bias</b> — the data reflects unfair decisions people made in the past.</li>
  <li><b>Sampling (representation) bias</b> — some groups are missing or rare in the data. A face-recognition system trained mostly on light-skinned faces makes more errors on darker-skinned faces.</li>
  <li><b>Measurement bias</b> — the thing recorded is a poor stand-in for what we care about, such as using arrests as a measure of crime.</li>
  <li><b>Hidden proxies</b> — even if you delete a sensitive column such as gender, other columns (a hobby, a school, a postcode) can carry the same information.</li>
</ul>

<h2>Why it matters more for AI</h2>
<p>One biased human interviewer affects the people they meet. A biased AI can screen millions of applications, loan requests or medical scans, repeating the same mistake every time — and people may trust it more because “the computer said so”. That is why fairness is treated as a design requirement, not an afterthought.</p>

<h2>How to reduce bias</h2>
<ul>
  <li><b>Balanced, representative data</b> that covers all the groups the system will serve.</li>
  <li><b>Fairness testing</b> — check accuracy and outcomes separately for each group before deployment.</li>
  <li><b>Transparency</b> — be able to explain which factors drove a decision.</li>
  <li><b>Human oversight</b> — keep people in the loop for high-stakes decisions such as jobs, loans and healthcare.</li>
  <li><b>Diverse teams</b> who are more likely to notice problems early.</li>
</ul>

<h2>How this appears in exams</h2>
<p>Expect short questions such as “What is AI bias? Give one example”, “Name two ways to reduce bias”, or a case study describing a system that treats some users unfairly and asking you to identify the cause. Always link your answer to the <b>training data</b>.</p>
""",
"practice": [
  ("Define AI bias in one sentence.", "AI bias is when an AI system produces unfair results for some people or groups because of patterns in its training data or design."),
  ("A voice assistant understands some accents far worse than others. What is the most likely cause?", "Sampling/representation bias — those accents were under-represented in the training data."),
  ("Give two ways to reduce bias in an AI system.", "Any two: use balanced and representative data; test fairness for each group; keep human oversight; make decisions explainable; build diverse teams."),
],
"related": [("Neural Networks & AI Ethics quiz", "chapters/neural-networks-10.html"),
            ("Introduction to AI quiz", "chapters/ai-introduction-10.html"),
            ("Class 10 AI mock papers", "cbse-class-10-ai-mock-papers.html")],
},
{
"slug": "why-is-dy-dx-zero-at-maximum-and-minimum",
"reel": "slope_zero",
"title": "Why is dy/dx = 0 at a maximum or minimum? Class 12 Maths",
"h1": "Why is dy/dx = 0 at a maximum or minimum?",
"description": "Slide a tangent along a curve and watch its slope change sign — why maxima and minima occur where dy/dx = 0, with the first and second derivative tests and a worked example for CBSE Class 12.",
"category": "Maths", "class_label": "Class 12", "published": "2026-11-25", "read_min": 6,
"body": """
<p>“Put dy/dx = 0 and solve” is the first step of almost every maxima–minima question in Class 12. But why does a maximum or minimum have to be at a point where the derivative is zero? The answer is a picture of a tangent sliding along a hill.</p>

<h2>The short answer</h2>
<p>The derivative dy/dx is the <b>slope of the tangent</b>. On the way up a hill the slope is positive; on the way down it is negative. At the very top it must switch from positive to negative, and a smooth curve can only do that by passing through <b>zero</b> — a flat tangent. The same happens, in reverse, at the bottom of a valley.</p>

<h2>Watch the tangent</h2>
<p>Take the curve <b>y = x³ − 3x</b>. It rises, reaches a peak, falls into a valley and rises again. Slide a tangent line along it from left to right:</p>
<ul>
  <li>Climbing towards the peak, the tangent tilts upward: <b>dy/dx &gt; 0</b>.</li>
  <li>At the peak, the tangent lies perfectly flat: <b>dy/dx = 0</b>.</li>
  <li>Going downhill, the tangent tilts downward: <b>dy/dx &lt; 0</b>.</li>
  <li>At the bottom of the valley it is flat again: <b>dy/dx = 0</b>.</li>
  <li>Climbing out, the slope becomes positive once more.</li>
</ul>
<p>So the turning points — the local maximum and local minimum — are exactly where the tangent is horizontal. These are called <b>critical</b> or <b>stationary points</b>.</p>

<h2>Finding them for y = x³ − 3x</h2>
<p>dy/dx = 3x² − 3. Setting it to zero: 3x² − 3 = 0 ⇒ x² = 1 ⇒ <b>x = −1 or x = 1</b>.</p>
<p>At x = −1, y = −1 + 3 = 2 (the peak). At x = 1, y = 1 − 3 = −2 (the valley).</p>

<h2>Which is the maximum? Two tests</h2>
<p><b>First derivative test.</b> Check the sign of dy/dx just before and just after the point. Positive → negative means a <b>maximum</b>; negative → positive means a <b>minimum</b>. For x = −1: at x = −2, dy/dx = 9 &gt; 0; at x = 0, dy/dx = −3 &lt; 0, so x = −1 is a local maximum.</p>
<p><b>Second derivative test.</b> d²y/dx² measures how the slope is changing. Here d²y/dx² = 6x. At x = −1 it is −6 &lt; 0: the slope is decreasing, the curve bends downward, so it is a <b>maximum</b>. At x = 1 it is 6 &gt; 0: the curve bends upward, a <b>minimum</b>. If the second derivative is 0, the test fails and you fall back on the first derivative test.</p>

<h2>A warning: zero slope is not always a turning point</h2>
<p>For y = x³, dy/dx = 3x² is zero at x = 0, but the curve keeps rising on both sides — the slope is positive, touches zero, and stays positive. This is a <b>point of inflection</b>, not a maximum or minimum. dy/dx = 0 tells you <i>where to look</i>; the tests tell you <i>what you found</i>.</p>

<h2>Exam tips</h2>
<ul>
  <li>In word problems (largest area, least cost), write the quantity as a function of one variable before differentiating.</li>
  <li>Always justify a maximum or minimum with the second derivative or a sign check — answers without justification lose marks.</li>
  <li>For a closed interval, also compare the values at the endpoints to find the absolute maximum or minimum.</li>
</ul>
""",
"practice": [
  ("Find the critical points of f(x) = x² − 6x + 5 and classify them.", "f′(x) = 2x − 6 = 0 ⇒ x = 3. f″(x) = 2 > 0, so x = 3 is a local minimum, with f(3) = −4."),
  ("For f(x) = −x² + 4x, find the maximum value.", "f′(x) = −2x + 4 = 0 ⇒ x = 2; f″ = −2 < 0 so it is a maximum. f(2) = 4."),
  ("Is x = 0 a maximum or minimum of f(x) = x³? Why?", "Neither. f′(0) = 0, but f′(x) = 3x² ≥ 0 on both sides, so the function keeps increasing — it is a point of inflection."),
],
"related": [("Class 12 Maths mock papers", "cbse-class-12-maths-mock-papers.html"),
            ("Application of Derivatives quiz", "chapters/application-derivatives-12.html"),
            ("Formula Board: quick revision cards", "formula-board/")],
},
{
"slug": "why-does-a-neural-network-need-layers",
"reel": "nn_layers",
"title": "Why does a neural network need layers? Hidden layers explained",
"h1": "Why does a neural network need layers?",
"description": "One neuron can only draw a straight line. See how hidden layers combine many lines to solve problems no single neuron can — deep learning explained for CBSE AI Class 10 and 12.",
"category": "AI", "class_label": "Class 10 · 12", "published": "2026-11-29", "read_min": 5,
"body": """
<p>Diagrams of neural networks show columns of circles joined by lines: an input layer, some hidden layers, an output layer. Why not just use one big neuron? Because a single neuron has a strict limit — it can only ever draw a <b>straight line</b>.</p>

<h2>The short answer</h2>
<p>One neuron splits data with a single straight boundary. Many real problems cannot be split that way. A <b>hidden layer</b> lets many neurons each draw their own line, and the next layer <b>combines</b> those lines into curved or closed shapes. More layers allow ever more complex patterns — that is what “deep” learning means.</p>

<h2>What one neuron can do</h2>
<p>An artificial neuron computes a weighted sum of its inputs, such as w₁x₁ + w₂x₂ + b, and fires if the sum crosses a threshold. On a graph of x₁ against x₂, the points where the sum exactly equals the threshold form a <b>straight line</b>. Everything on one side gets “yes”; everything on the other side gets “no”. Training can move and rotate that line, but it can never bend it.</p>

<h2>A problem one line cannot solve</h2>
<p>Imagine blue dots clustered in the middle of a chart, with pink dots all around them. Try to separate them with one straight line: however you turn it, some pink dots end up on the blue side. The data is <b>not linearly separable</b>. A famous small example is the <b>XOR</b> function, which outputs 1 when exactly one of its two inputs is 1 — no single straight line can separate its yes and no cases.</p>

<h2>Adding a hidden layer</h2>
<ol>
  <li>Put several neurons in a hidden layer. Each one learns its own straight line — one above the blue cluster, one below, one to the left, one to the right.</li>
  <li>Each hidden neuron reports which side of its line a point is on.</li>
  <li>An output neuron combines these reports: “yes only if the point is inside <i>all</i> the lines”.</li>
</ol>
<p>Together the lines form a boundary that wraps around the blue dots. A problem that was impossible for one neuron becomes easy for a small network.</p>

<h2>Why go deeper?</h2>
<p>Each extra layer works with the patterns found by the layer before. In image recognition, early layers detect edges, middle layers combine edges into shapes such as eyes or wheels, and later layers combine shapes into whole objects such as faces or cars. Deep networks can therefore model very complex relationships — but they also need more data and more computing power to train, and they are harder to explain.</p>

<h2>One important detail</h2>
<p>Layers only help because each neuron applies a <b>non-linear activation function</b> (such as ReLU or sigmoid) to its sum. Without it, stacking layers would just produce another straight-line rule, no matter how many layers you added.</p>

<h2>How this appears in exams</h2>
<p>You may be asked to name and describe the three types of layers, explain what a hidden layer does, or state the difference between a simple neural network and a deep neural network (deep networks have many hidden layers).</p>
""",
"practice": [
  ("What is the role of the hidden layer in a neural network?", "It transforms the inputs into intermediate features, letting the network combine simple patterns into complex ones that a single neuron cannot represent."),
  ("Why can't a single neuron learn the XOR function?", "A single neuron can only draw one straight decision boundary, and XOR's outputs are not linearly separable."),
  ("What makes a neural network 'deep'?", "Having many hidden layers between the input and output layers."),
],
"related": [("Neural Networks & AI Ethics quiz", "chapters/neural-networks-10.html"),
            ("Machine Learning Concepts quiz", "chapters/ml-concepts-10.html"),
            ("Class 10 AI mock papers", "cbse-class-10-ai-mock-papers.html")],
},
{
"slug": "why-does-a-stack-reverse-things",
"reel": "stack_lifo",
"title": "Why does a stack reverse things? LIFO explained for Class 12 CS",
"h1": "Why does a stack reverse things?",
"description": "Push A, B, C and pop gives C, B, A. Why a stack is Last In First Out, how to implement push and pop with a Python list, and where stacks are used — CBSE Class 12 Computer Science.",
"category": "Computer Science", "class_label": "Class 12", "published": "2026-12-02", "read_min": 6,
"body": """
<p>The <b>stack</b> is the one data structure in the CBSE Class 12 Computer Science syllabus, and it reliably earns marks in the board exam: a 3–4 mark program to push and pop, plus short questions on its uses. Everything about it follows from a single rule you already know from a pile of plates.</p>

<h2>The short answer</h2>
<p>In a stack you can only add or remove items at <b>one end — the top</b>. The last item you put in sits on top, so it is the first to come out. Push A, B, C and you pop C, B, A. That rule is called <b>LIFO: Last In, First Out</b>, and it is why a stack naturally reverses order.</p>

<h2>The pile of plates</h2>
<p>Stack three plates: A first, then B on top of it, then C on top of B. You cannot pull A out from the bottom without lifting the others. The only plate you can reach is C. Take it off and B becomes the top; take that off and finally A. In went A, B, C; out came C, B, A.</p>

<h2>The stack operations</h2>
<ul>
  <li><b>PUSH</b> — add an element to the top.</li>
  <li><b>POP</b> — remove and return the top element.</li>
  <li><b>PEEK</b> (or TOP) — look at the top element without removing it.</li>
  <li><b>isEmpty</b> — check whether the stack has no elements.</li>
</ul>
<p>Trying to pop from an empty stack is called <b>underflow</b>. In a fixed-size stack, pushing onto a full stack is called <b>overflow</b>.</p>

<h2>A stack in Python</h2>
<p>A Python list makes a perfect stack if you treat its <b>end</b> as the top: <code>append()</code> pushes and <code>pop()</code> pops.</p>
<pre><code>stack = []

def push(stack, item):
    stack.append(item)

def pop_item(stack):
    if not stack:                 # check for underflow
        return "Underflow"
    return stack.pop()

def peek(stack):
    return stack[-1] if stack else None

for ch in "ABC":
    push(stack, ch)
print(stack)              # ['A', 'B', 'C']   top is 'C'
print(pop_item(stack))    # C
print(pop_item(stack))    # B</code></pre>

<h2>Reversing a string with a stack</h2>
<p>Push every character, then pop them all. Because of LIFO, they come out backwards:</p>
<pre><code>def reverse(text):
    s = []
    for ch in text:
        s.append(ch)
    out = ""
    while s:
        out += s.pop()
    return out

print(reverse("CBSE"))    # ESBC</code></pre>

<h2>Where stacks are used</h2>
<ul>
  <li><b>Undo (Ctrl+Z)</b> — each action is pushed; undo pops the most recent one.</li>
  <li><b>The browser Back button</b> — pages you visit are pushed; Back pops the last page.</li>
  <li><b>Function calls</b> — Python keeps a call stack; the most recently called function finishes first.</li>
  <li><b>Checking brackets</b> in an expression, and converting or evaluating postfix expressions.</li>
</ul>

<h2>Exam tips</h2>
<ul>
  <li>Board questions often say “push only the numbers divisible by 5 from a list” or “push records meeting a condition”, then pop and display until empty. Practise that pattern.</li>
  <li>Always handle underflow (empty stack) before popping — examiners look for it.</li>
  <li>Use <code>pop()</code> without an argument. <code>pop(0)</code> removes from the bottom and breaks LIFO.</li>
</ul>
""",
"practice": [
  ("The elements 10, 20, 30 are pushed onto an empty stack in that order. What does the first pop return?", "30 — the last element pushed is on top (LIFO)."),
  ("What is stack underflow?", "Attempting to pop (or peek) from an empty stack."),
  ("Which Python list methods implement push and pop?", "append() for push and pop() (with no argument) for pop."),
],
"related": [("Data Structures (Stack) quiz", "chapters/data-structures-12.html"),
            ("Class 12 Computer Science mock papers", "cbse-class-12-computer-science-mock-papers.html"),
            ("Python Functions & Modules quiz", "chapters/python-functions-12.html")],
},
{
"slug": "why-does-a-convex-lens-focus-light",
"reel": "convex_lens",
"title": "Why does a convex lens focus light? The prism picture explained",
"h1": "Why does a convex lens bring light to a focus?",
"description": "A convex lens is like a stack of prisms, thick in the middle and thin at the edges. See why parallel rays meet at the focus, plus lens formula, power and sign-convention tips for CBSE Class 10 and 12.",
"category": "Physics", "class_label": "Class 10 · 12", "published": "2026-12-06", "read_min": 6,
"body": """
<p>Hold a magnifying glass in sunlight and you can gather the light into one tiny, bright spot. Why does a curved piece of glass send all those parallel rays to the same point? The trick is to think of the lens as a stack of <b>prisms</b>.</p>

<h2>The short answer</h2>
<p>A prism always bends light towards its <b>thicker end</b>. A convex lens is like a set of prisms that are thick in the middle and thin at the edges. Rays near the top bend down, rays near the bottom bend up, and the central ray goes straight through. Because the edges are angled more steeply, outer rays bend more — just enough for all of them to meet at one point, the <b>principal focus</b>.</p>

<h2>Step 1: a prism bends light towards its base</h2>
<p>When light enters glass it slows down and bends towards the normal; when it leaves it speeds up and bends away from the normal. In a triangular prism both bends push the ray the same way: <b>towards the base</b>, the thick end.</p>

<h2>Step 2: stack the prisms</h2>
<p>Place one prism above the middle with its base facing down, one below with its base facing up, and a flat slab in the centre. Now send in parallel rays:</p>
<ul>
  <li>The top prism bends its ray <b>down</b>.</li>
  <li>The bottom prism bends its ray <b>up</b>.</li>
  <li>The ray through the centre goes <b>straight</b> on.</li>
</ul>
<p>The rays converge. Make the steps smaller and smaller and the outline smooths into a curved surface — a <b>convex lens</b>. Near the edges the surfaces meet at a steeper angle, so outer rays bend more, and the rays meet at a single point.</p>

<h2>Step 3: the focus and focal length</h2>
<p>Rays parallel to the principal axis meet at the <b>principal focus F</b>. The distance from the optical centre to F is the <b>focal length f</b>. A more strongly curved (fatter) lens bends light more and has a <b>shorter</b> focal length. A concave lens is the opposite stack — thin in the middle, thick at the edges — so it spreads rays apart and is called a diverging lens.</p>

<h2>Power of a lens</h2>
<p>The <b>power</b> of a lens measures how strongly it bends light: <b>P = 1/f</b>, with f in metres. The unit is the <b>dioptre (D)</b>. A convex lens of focal length 25 cm has P = 1/0.25 = <b>+4 D</b>. Convex lenses have positive power; concave lenses have negative power.</p>

<h2>A worked example</h2>
<p><b>Q.</b> An object is placed 30 cm in front of a convex lens of focal length 20 cm. Where is the image?</p>
<p><b>A.</b> Lens formula: 1/v − 1/u = 1/f. With u = −30 cm and f = +20 cm: 1/v = 1/20 + 1/(−30) = 3/60 − 2/60 = 1/60, so <b>v = +60 cm</b>. The image is real, formed 60 cm behind the lens, inverted, and magnified (m = v/u = −2).</p>

<h2>Common mistakes</h2>
<ul>
  <li><b>Sign convention.</b> Distances are measured from the optical centre; those against the incoming light (object side) are negative. For a convex lens, f is positive.</li>
  <li><b>Units in power.</b> Convert f to metres before using P = 1/f.</li>
  <li><b>Mixing up the formulas.</b> The lens formula is 1/v − 1/u = 1/f; the mirror formula is 1/v + 1/u = 1/f.</li>
</ul>
""",
"practice": [
  ("Find the power of a convex lens of focal length 50 cm.", "P = 1/f = 1/0.5 m = +2 D."),
  ("Why is a convex lens called a converging lens?", "It is thicker in the middle, so like a stack of prisms it bends parallel rays towards each other until they meet at the focus."),
  ("A lens has power −2.5 D. What type of lens is it, and what is its focal length?", "Concave (negative power); f = 1/P = −0.4 m = −40 cm."),
],
"related": [("Light – Reflection & Refraction quiz", "chapters/light-optics-10.html"),
            ("Ray Optics (Class 12) quiz", "chapters/ray-optics-12.html"),
            ("Class 10 Science mock tests", "cbse-class-10-science-mock-tests.html"),
            ("Class 12 Physics mock papers", "cbse-class-12-physics-mock-papers.html")],
},
{
"slug": "why-is-ap-sum-n-by-2-first-plus-last",
"reel": "ap_sum",
"title": "Why is the AP sum Sₙ = n/2 (a + l)? The staircase proof",
"h1": "Why is the sum of an AP equal to n/2 × (first + last)?",
"description": "Two copies of an AP staircase make a perfect rectangle — the picture behind Sₙ = n/2 (a + l) and Sₙ = n/2 [2a + (n − 1)d], with Gauss's trick, worked examples and tips for CBSE Class 10.",
"category": "Maths", "class_label": "Class 10", "published": "2026-12-09", "read_min": 5,
"body": """
<p>Arithmetic Progressions carry some of the easiest marks in the Class 10 board paper, and the sum formula sits at the centre of them. Instead of memorising <b>Sₙ = n/2 (a + l)</b>, you can <i>see</i> it — with a staircase of blocks.</p>

<h2>The short answer</h2>
<p>Draw the terms of an AP as columns of blocks and you get a staircase. Make a copy, turn it upside down and fit it on top: the two staircases form a perfect rectangle that is <b>n</b> columns wide and <b>(first + last)</b> blocks tall. The staircase is exactly half of that rectangle, so Sₙ = n/2 × (a + l).</p>

<h2>Step 1: build the staircase</h2>
<p>Take the AP 1, 2, 3, 4, 5, 6. Draw a column of 1 block, then 2 blocks, then 3, up to 6. The columns rise evenly — because in an AP every term goes up by the same common difference — so the shape is a neat staircase.</p>

<h2>Step 2: copy, flip and fit</h2>
<p>Make an identical staircase, turn it upside down, and place it on top of the first. The tallest column of the copy (6) sits on the shortest column of the original (1); the next pair is 5 on 2; then 4 on 3, and so on. Every column now has the same height: 1 + 6 = 2 + 5 = 3 + 4 = <b>7</b>, which is first + last.</p>

<h2>Step 3: halve the rectangle</h2>
<p>The two staircases together make a rectangle of 6 columns × 7 blocks = 42 blocks. One staircase is exactly half: <b>21</b>. In general, with n terms, first term a and last term l, the rectangle has n × (a + l) blocks and the sum is</p>
<p><b>Sₙ = n/2 (a + l)</b>.</p>

<h2>The same idea with numbers: Gauss's trick</h2>
<p>A famous story says the young mathematician Carl Friedrich Gauss was asked to add 1 to 100. He wrote the sum forwards and backwards and added the two rows: each pair (1 + 100, 2 + 99, …) makes 101, and there are 100 pairs, so twice the sum is 10,100. The sum is <b>5050</b>. That is the flipped staircase, written in numbers.</p>

<h2>The second form of the formula</h2>
<p>The last term of an AP is l = a + (n − 1)d. Substitute it in:</p>
<p><b>Sₙ = n/2 [2a + (n − 1)d]</b>.</p>
<p>Use the first form when you know the last term, and the second when you know the common difference.</p>

<h2>A worked example</h2>
<p><b>Q.</b> Find the sum of the first 20 terms of the AP 3, 7, 11, …</p>
<p><b>A.</b> a = 3, d = 4, n = 20. S₂₀ = 20/2 [2(3) + 19(4)] = 10 × (6 + 76) = <b>820</b>.</p>

<h2>Exam tips</h2>
<ul>
  <li>Write down a, d and n clearly before substituting — most errors come from a wrong n.</li>
  <li>To find how many terms are needed for a given sum, set Sₙ equal to it and solve the quadratic in n; reject negative or fractional values.</li>
  <li>Remember: the nth term can be found from sums using aₙ = Sₙ − Sₙ₋₁.</li>
</ul>
""",
"practice": [
  ("Find the sum of the first 50 natural numbers.", "S = 50/2 × (1 + 50) = 25 × 51 = 1275."),
  ("Find the sum of the AP 2, 5, 8, …, 29.", "29 = 2 + (n − 1)3 ⇒ n = 10. S = 10/2 × (2 + 29) = 155."),
  ("If Sₙ = n² + 2n, find the first term and the common difference.", "a₁ = S₁ = 3; S₂ = 8 so a₂ = 5; d = 2."),
],
"related": [("Arithmetic Progressions quiz", "chapters/arithmetic-progressions-10.html"),
            ("Class 10 Maths Standard mock tests", "cbse-class-10-maths-standard-mock-tests.html"),
            ("Class 10 Maths Basic mock tests", "cbse-class-10-maths-basic-mock-tests.html")],
},
{
"slug": "why-split-data-into-training-and-testing-sets",
"reel": "train_test",
"title": "Why split data into training and testing sets? Overfitting explained",
"h1": "Why do we split data into training and testing sets?",
"description": "A model that memorises its training data fails on new data — that is overfitting. Why we hold back a test set, the 80/20 split, accuracy and evaluation for CBSE AI Class 10 and 12.",
"category": "AI", "class_label": "Class 10 · 12", "published": "2026-12-13", "read_min": 5,
"body": """
<p>Imagine a student who somehow gets the exact exam questions a week early and memorises the answers. They score 100%. Have they learnt the subject? You would only find out by giving them <i>new</i> questions. Machine learning has exactly the same problem — and the training/testing split is the solution.</p>

<h2>The short answer</h2>
<p>We train a model on one part of the data and keep another part <b>locked away</b>. After training, we test the model on this unseen data. Good performance on the test set shows the model has learnt general patterns; good performance only on the training set shows it has merely <b>memorised</b> — a problem called <b>overfitting</b>.</p>

<h2>What overfitting looks like</h2>
<p>A flexible model can fit its training examples almost perfectly — including their noise and accidents. Suppose you train a model to recognise cats, and by chance most cat photos in your data were taken indoors. The model may learn “indoor background = cat”. It scores brilliantly on the training photos, then fails on a cat photographed in a garden. It learnt the quirks of the data, not the idea of a cat.</p>
<p>The opposite problem is <b>underfitting</b>: a model too simple to capture the pattern, which does badly on both training and test data.</p>

<h2>How the split works</h2>
<ol>
  <li><b>Collect and shuffle</b> the labelled data so both parts are representative.</li>
  <li><b>Split</b> it — commonly about <b>80% for training</b> and <b>20% for testing</b> (70/30 is also common).</li>
  <li><b>Train</b> the model using only the training set.</li>
  <li><b>Evaluate</b> on the test set, which the model has never seen, using measures such as accuracy.</li>
</ol>
<p>The test set acts like the real board exam: fresh questions that show whether learning really happened.</p>

<h2>Reading the results</h2>
<table>
  <tr><th>Training accuracy</th><th>Test accuracy</th><th>What it means</th></tr>
  <tr><td>High</td><td>High</td><td>Good fit — the model generalises</td></tr>
  <tr><td>High</td><td>Low</td><td>Overfitting — memorised the training data</td></tr>
  <tr><td>Low</td><td>Low</td><td>Underfitting — model too simple</td></tr>
</table>

<h2>Golden rules</h2>
<ul>
  <li><b>Never train on the test data.</b> Even a peek makes the test score meaningless, like the student who saw the paper.</li>
  <li><b>Keep the split representative.</b> If all examples of one class end up in the test set, the model never learns them.</li>
  <li>Many projects also keep a third <b>validation set</b> to tune the model before the final test.</li>
</ul>

<h2>Where this fits in the AI project cycle</h2>
<p>In the CBSE AI project cycle — Problem Scoping, Data Acquisition, Data Exploration, Modelling and Evaluation — the split happens before modelling, and the test set is used in the <b>Evaluation</b> stage. Questions on evaluation often ask why a model must be tested on data it has not seen, and how to calculate accuracy from correct and total predictions.</p>
""",
"practice": [
  ("A model scores 99% on training data but 60% on test data. What is the problem called?", "Overfitting — it has memorised the training data instead of learning general patterns."),
  ("Why shouldn't a model be evaluated on the same data it was trained on?", "It may simply have memorised those examples, so the score would not show how it performs on new, unseen data."),
  ("A model makes 170 correct predictions out of 200 test cases. What is its accuracy?", "170/200 × 100 = 85%."),
],
"related": [("Machine Learning Concepts quiz", "chapters/ml-concepts-10.html"),
            ("Data Handling quiz", "chapters/data-handling-10.html"),
            ("Class 10 AI mock papers", "cbse-class-10-ai-mock-papers.html")],
},
]
