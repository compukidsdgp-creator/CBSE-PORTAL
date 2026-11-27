"""Class 10 Science — Chapter 8: Heredity (NCERT, rationalised 2026–27 syllabus)."""

CHAPTER = {
"slug": "heredity",
"class": "10", "subject": "Science", "subject_slug": "science", "number": 8,
"title": "Heredity",
"status": "draft",                     # draft = hidden preview; live = published after approval
"updated": "2026-11-27",
"unit": "Unit II · World of Living",
"description": "CBSE Class 10 Science Chapter 8 notes: accumulation of variation, inherited traits, Mendel's monohybrid and dihybrid crosses, dominant and recessive traits, how genes control traits, and sex determination in humans — with cross diagrams, worked board questions and common mistakes.",
"glance": """
<p>Every generation passes on a body design that is almost — but never exactly — the same. <b>Heredity</b> is the passing of traits from parents to offspring; <b>variation</b> is the small difference that creeps in each time. Gregor Mendel worked out the rules by crossing pea plants: each trait is controlled by a pair of factors (genes), one from each parent, and one form can hide the other. This short chapter is scoring if you can draw and explain the crosses and the sex-determination chart.</p>
<ul>
  <li>Monohybrid cross (tall × short): F₁ all tall; F₂ ratio <b>3 : 1</b> (genotype 1 : 2 : 1).</li>
  <li>Dihybrid cross (round yellow × wrinkled green): F₂ ratio <b>9 : 3 : 3 : 1</b> and independent inheritance.</li>
  <li>Dominant and recessive traits; genotype vs phenotype.</li>
  <li>How a gene controls a trait: gene → protein (enzyme) → hormone → height.</li>
  <li>Sex determination in humans: XX and XY, and why the father's sperm decides.</li>
</ul>
""",
"concepts": [
("Accumulation of variation during reproduction", """
<p>Inheritance from the previous generation gives each new generation a <b>common basic body design</b> along with small changes in it. These changes build up, generation after generation.</p>
<ul>
  <li>In <b>asexual reproduction</b>, a bacterium that divides gives two daughter cells that are nearly identical; when each divides again, the four cells differ only by the minor errors made while copying DNA. Variation accumulates very slowly.</li>
  <li>In <b>sexual reproduction</b>, DNA from two different parents is combined in every offspring, so the diversity is far greater.</li>
</ul>
<p>Not all variants are equally likely to survive. Depending on the surroundings, some variations give an advantage — for example, bacteria that can withstand heat survive a heat wave while the others die. The environment thus selects which variants carry on, and this is the basis of evolution.</p>
"""),
("Heredity and inherited traits", """
<p><b>Heredity</b> is the transmission of traits from one generation to the next; the rules of heredity decide how traits and characteristics are reliably inherited. A child shows all the basic features of a human being, yet does not look exactly like either parent.</p>
<p><b>Activity — earlobes:</b> if the students of a class examine their earlobes, two kinds are found: a <b>free</b> earlobe that hangs below the point where it joins the head, and an <b>attached</b> earlobe that is joined to the side of the head. When the numbers are counted and the parents of a few students are checked, it is seen that the earlobe type of a child depends on the parents. Earlobe type is an inherited trait, with some variation in how it shows.</p>
"""),
("Mendel's experiments with the garden pea", """
<p><b>Gregor Johann Mendel</b> (1822–1884), an Austrian monk who had studied science and mathematics, experimented with the garden pea (<i>Pisum sativum</i>). The pea was a good choice because it has many easily seen <b>contrasting traits</b>, a short life cycle, produces many seeds, and normally self-pollinates, though it can also be cross-pollinated by hand.</p>
<p>He studied seven pairs of contrasting characters, among them: tall/short plant, round/wrinkled seed, yellow/green seed, and violet/white flower. Two features made his work different from earlier attempts: he looked at <b>one or two traits at a time</b>, and he <b>counted</b> the number of offspring of each type in every generation, which revealed definite ratios.</p>
"""),
("Monohybrid cross: dominant and recessive traits", """
<p>A cross that follows a single pair of contrasting traits is a <b>monohybrid cross</b>. Mendel crossed a pure-breeding tall pea plant with a pure-breeding short (dwarf) one.</p>
<ul>
  <li><b>F₁ (first filial) generation:</b> every plant was tall. There were no plants of medium height, and the short trait seemed to have vanished.</li>
  <li>He then allowed the F₁ tall plants to <b>self-pollinate</b>. In the <b>F₂ generation</b>, about three-quarters of the plants were tall and one-quarter were short.</li>
</ul>
<p class="eq">F₂ phenotypic ratio — tall : short = 3 : 1</p>
<p>Since the short trait reappeared unchanged in F₂, the F₁ plants must have inherited <b>both</b> the tallness and the shortness traits, but only tallness was expressed. Mendel's explanation:</p>
<ol>
  <li>Each trait is controlled by a pair of factors, now called <b>genes</b>. Every individual carries <b>two copies</b>, one inherited from each parent.</li>
  <li>A trait that is expressed when one copy is present is <b>dominant</b> (tall, written T); a trait that is expressed only when both copies are of that kind is <b>recessive</b> (short, written t).</li>
  <li>A <b>germ cell carries only one copy</b> of each gene, chosen from the pair.</li>
</ol>
<p>So pure tall plants are TT and pure short plants are tt. Their germ cells are T and t, and every F₁ plant is <b>Tt</b> — tall, because T is dominant. When Tt is selfed, T and t germ cells combine at random:</p>
<p class="eq">Tt × Tt → 1 TT : 2 Tt : 1 tt  (genotypic ratio 1 : 2 : 1)</p>
<p>TT and Tt both look tall, giving the 3 : 1 appearance. The genetic make-up (TT, Tt, tt) is the <b>genotype</b>; the visible trait (tall, short) is the <b>phenotype</b>. A plant with two identical copies (TT or tt) is pure, or homozygous; a plant with two different copies (Tt) is a hybrid, or heterozygous.</p>
<p><b>To tell whether a tall F₂ plant is TT or Tt</b>, self-pollinate it: a TT plant gives only tall offspring, while a Tt plant gives tall and short offspring in about a 3 : 1 ratio.</p>
"""),
("Dihybrid cross: traits are inherited independently", """
<p>A cross that follows two pairs of traits together is a <b>dihybrid cross</b>. Mendel crossed a plant with <b>round, yellow</b> seeds (RRYY) with one having <b>wrinkled, green</b> seeds (rryy). Round (R) and yellow (Y) are dominant.</p>
<ul>
  <li><b>F₁:</b> all seeds were round and yellow (RrYy).</li>
  <li><b>F₂</b> (F₁ selfed): each F₁ plant forms four kinds of germ cells — RY, Ry, rY and ry — in equal numbers. Combining them gives 16 equally likely combinations.</li>
</ul>
<p class="eq">F₂ — round yellow : round green : wrinkled yellow : wrinkled green = 9 : 3 : 3 : 1</p>
<p>Two of these four types (round green and wrinkled yellow) were <b>new combinations</b> not seen in either parent. This shows that the seed-shape trait and the seed-colour trait are inherited <b>independently</b> of each other. Each pair on its own still gives 3 : 1 — round : wrinkled is 12 : 4 and yellow : green is 12 : 4.</p>
"""),
("How do these traits get expressed?", """
<p>Cellular DNA is the information source for making proteins. A section of DNA that provides the information for one protein is called a <b>gene</b>. Take plant height: plants have hormones that trigger growth, and the amount of hormone made depends on how efficiently an <b>enzyme</b> works. If the gene for that enzyme makes an efficient enzyme, plenty of hormone is made and the plant is tall. If a change in the gene makes the enzyme less efficient, less hormone is made and the plant is short.</p>
<p class="eq">gene → protein (enzyme) → amount of growth hormone → height of plant</p>
<p>Both parents contribute equally to the DNA of the offspring, so each child gets two copies of every gene — one from each parent. For this to happen, each germ cell must carry only <b>one set</b> of genes. Genes are present on separate, independent pieces of DNA called <b>chromosomes</b>. Each body cell has two copies of every chromosome, one from each parent; each germ cell takes only one chromosome of each pair. When two germ cells fuse, the zygote gets back the normal number of chromosomes, so the <b>number of chromosomes stays constant</b> from generation to generation.</p>
<p>Because the chromosomes of each pair are sorted into germ cells independently, a gene on one chromosome is passed on independently of a gene on another — this is the reason behind the independent inheritance seen in the dihybrid cross.</p>
"""),
("Sex determination", """
<p>Different species use different methods to decide whether a newborn will be male or female.</p>
<ul>
  <li>In some reptiles, the <b>temperature</b> at which the fertilised egg is kept decides the sex of the young.</li>
  <li>Some animals, such as certain snails, can <b>change sex</b>, so sex is not fixed genetically.</li>
  <li>In human beings, sex is determined <b>genetically</b> — by the genes inherited from the parents.</li>
</ul>
<p>Human body cells have <b>23 pairs</b> of chromosomes. Twenty-two pairs are matched in both sexes (autosomes). The remaining pair, the <b>sex chromosomes</b>, differs: females have a perfect pair, <b>XX</b>; males have a mismatched pair, one normal-sized <b>X</b> and one short <b>Y</b>.</p>
<ul>
  <li>Every egg made by the mother carries an X chromosome.</li>
  <li>Half the sperms made by the father carry X and half carry Y.</li>
</ul>
<p class="eq">X-sperm + X-egg → XX (girl)   ·   Y-sperm + X-egg → XY (boy)</p>
<p>So the sex of the child depends on which kind of sperm fertilises the egg — the child inherits its X from the mother in every case, and an X or a Y from the father. There is an equal (50%) chance of a boy or a girl, and the mother cannot be held responsible for the sex of the child.</p>
"""),
],
"diagrams": [
("variation", "Variation accumulates over generations: each copy keeps the changes of its parent and may add a new one. Sexual reproduction mixes DNA of two parents, so variation is far greater.", """
<svg viewBox="0 0 680 360" role="img" aria-labelledby="t-va" xmlns="http://www.w3.org/2000/svg">
<title id="t-va">Accumulation of variation over three generations of asexual reproduction</title>
<g font-family="Inter,Segoe UI,sans-serif" font-size="13" fill="#1f2937">
<!-- connecting lines -->
<g stroke="#94a3b8" stroke-width="2" fill="none">
<path d="M380 78 L250 150"/><path d="M380 78 L510 150"/>
<path d="M250 188 L170 260"/><path d="M250 188 L320 260"/>
<path d="M510 188 L440 260"/><path d="M510 188 L590 260"/>
</g>
<!-- cells -->
<g fill="#e0f2fe" stroke="#0369a1" stroke-width="2">
<ellipse cx="380" cy="56" rx="40" ry="24"/>
<ellipse cx="250" cy="168" rx="40" ry="24"/><ellipse cx="510" cy="168" rx="40" ry="24"/>
<ellipse cx="170" cy="282" rx="40" ry="24"/><ellipse cx="320" cy="282" rx="40" ry="24"/>
<ellipse cx="440" cy="282" rx="40" ry="24"/><ellipse cx="590" cy="282" rx="40" ry="24"/>
</g>
<g fill="#c7d2fe" stroke="#4338ca" stroke-width="1.6">
<circle cx="372" cy="56" r="8"/>
<circle cx="242" cy="168" r="8"/><circle cx="502" cy="168" r="8"/>
<circle cx="162" cy="282" r="8"/><circle cx="312" cy="282" r="8"/>
<circle cx="432" cy="282" r="8"/><circle cx="582" cy="282" r="8"/>
</g>
<!-- variation marks: triangle = change a, square = change b, diamond = change c, dot = change d -->
<g fill="#dc2626"><path d="M266 160 L273 172 L259 172Z"/><path d="M186 274 L193 286 L179 286Z"/><path d="M336 274 L343 286 L329 286Z"/></g>
<g fill="#16a34a"><rect x="519" y="161" width="12" height="12"/><rect x="449" y="275" width="12" height="12"/><rect x="599" y="275" width="12" height="12"/></g>
<path d="M198 276 L204 282 L198 288 L192 282Z" fill="#ea580c" transform="translate(4 0)"/>
<circle cx="469" cy="281" r="5" fill="#9333ea"/>
<!-- generation labels -->
<text x="12" y="61" font-weight="700">Generation I</text>
<text x="12" y="173" font-weight="700">Generation II</text>
<text x="12" y="287" font-weight="700">Generation III</text>
<!-- legend -->
<line x1="12" y1="320" x2="668" y2="320" stroke="#e5e7eb" stroke-width="1.5"/>
<path d="M18 337 L25 349 L11 349Z" fill="#dc2626"/><rect x="32" y="337" width="12" height="12" fill="#16a34a"/>
<path d="M58 337 L64 343 L58 349 L52 343Z" fill="#ea580c"/><circle cx="76" cy="343" r="5" fill="#9333ea"/>
<text x="92" y="348">= small changes from DNA copying errors; each new cell keeps its parent's changes</text>
</g>
</svg>
"""),
("monohybrid", "Monohybrid cross: pure tall (TT) × pure short (tt). F₁ plants are all tall (Tt); selfing F₁ gives tall and short plants in a 3 : 1 ratio.", """
<svg viewBox="0 0 640 520" role="img" aria-labelledby="t-mo" xmlns="http://www.w3.org/2000/svg">
<title id="t-mo">Monohybrid cross between tall and short pea plants up to the F2 generation</title>
<defs><marker id="mo-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#475569"/></marker></defs>
<g font-family="Inter,Segoe UI,sans-serif" font-size="13" fill="#1f2937">
<!-- P generation -->
<text x="16" y="100" font-weight="700">Parents (P)</text>
<g stroke="#92400e" stroke-width="2"><line x1="196" y1="140" x2="244" y2="140"/><line x1="396" y1="140" x2="444" y2="140"/></g>
<line x1="220" y1="140" x2="220" y2="38" stroke="#15803d" stroke-width="3"/>
<g fill="#4ade80" stroke="#15803d" stroke-width="1.4">
<path d="M220 118 C206 108 196 110 190 102 C202 98 214 104 220 118Z"/>
<path d="M220 94 C234 84 244 86 250 78 C238 74 226 80 220 94Z"/>
<path d="M220 68 C208 60 200 60 194 54 C204 50 214 56 220 68Z"/>
</g>
<circle cx="220" cy="36" r="6" fill="#a78bfa" stroke="#6d28d9" stroke-width="1.4"/>
<line x1="420" y1="140" x2="420" y2="104" stroke="#15803d" stroke-width="3"/>
<g fill="#4ade80" stroke="#15803d" stroke-width="1.4">
<path d="M420 132 C406 122 396 124 390 116 C402 112 414 118 420 132Z"/>
<path d="M420 118 C434 108 444 110 450 102 C438 98 426 104 420 118Z"/>
</g>
<circle cx="420" cy="102" r="6" fill="#a78bfa" stroke="#6d28d9" stroke-width="1.4"/>
<text x="320" y="104" text-anchor="middle" font-size="22" font-weight="700">×</text>
<text x="220" y="160" text-anchor="middle" font-weight="700">Tall (TT)</text>
<text x="420" y="160" text-anchor="middle" font-weight="700">Short (tt)</text>
<!-- gametes -->
<text x="16" y="200" font-weight="700">Germ cells</text>
<g fill="#fef3c7" stroke="#b45309" stroke-width="1.6"><circle cx="220" cy="195" r="15"/><circle cx="420" cy="195" r="15"/></g>
<text x="220" y="200" text-anchor="middle" font-weight="700">T</text>
<text x="420" y="200" text-anchor="middle" font-weight="700">t</text>
<g stroke="#475569" stroke-width="2"><line x1="232" y1="208" x2="306" y2="240" marker-end="url(#mo-ar)"/><line x1="408" y1="208" x2="334" y2="240" marker-end="url(#mo-ar)"/></g>
<!-- F1 -->
<text x="16" y="290" font-weight="700">F₁ generation</text>
<line x1="296" y1="340" x2="344" y2="340" stroke="#92400e" stroke-width="2"/>
<line x1="320" y1="340" x2="320" y2="250" stroke="#15803d" stroke-width="3"/>
<g fill="#4ade80" stroke="#15803d" stroke-width="1.4">
<path d="M320 320 C306 310 296 312 290 304 C302 300 314 306 320 320Z"/>
<path d="M320 298 C334 288 344 290 350 282 C338 278 326 284 320 298Z"/>
<path d="M320 276 C308 268 300 268 294 262 C304 258 314 264 320 276Z"/>
</g>
<circle cx="320" cy="248" r="6" fill="#a78bfa" stroke="#6d28d9" stroke-width="1.4"/>
<text x="372" y="292" font-weight="700">All tall (Tt)</text>
<text x="372" y="310" fill="#475569">short trait hidden, not lost</text>
<text x="320" y="364" text-anchor="middle" fill="#475569">Self-pollination: Tt × Tt</text>
<!-- F2 Punnett square -->
<text x="16" y="452" font-weight="700">F₂ generation</text>
<text x="300" y="402" text-anchor="middle" font-weight="700">T</text>
<text x="380" y="402" text-anchor="middle" font-weight="700">t</text>
<text x="246" y="433" text-anchor="middle" font-weight="700">T</text>
<text x="246" y="469" text-anchor="middle" font-weight="700">t</text>
<g stroke="#475569" stroke-width="1.2">
<rect x="260" y="410" width="80" height="36" fill="#dcfce7"/><rect x="340" y="410" width="80" height="36" fill="#dcfce7"/>
<rect x="260" y="446" width="80" height="36" fill="#dcfce7"/><rect x="340" y="446" width="80" height="36" fill="#fef9c3"/>
</g>
<text x="300" y="433" text-anchor="middle">TT tall</text><text x="380" y="433" text-anchor="middle">Tt tall</text>
<text x="300" y="469" text-anchor="middle">Tt tall</text><text x="380" y="469" text-anchor="middle">tt short</text>
<text x="438" y="432" font-weight="700">Phenotype 3 tall : 1 short</text>
<text x="438" y="452">Genotype</text>
<text x="438" y="470">1 TT : 2 Tt : 1 tt</text>
<text x="320" y="508" text-anchor="middle" fill="#475569">Germ cells of one F₁ parent across the top, of the other down the side</text>
</g>
</svg>
"""),
("dihybrid", "Dihybrid cross: F₂ from selfing round yellow F₁ plants (RrYy). 16 combinations give 9 round yellow : 3 round green : 3 wrinkled yellow : 1 wrinkled green.", """
<svg viewBox="0 0 640 450" role="img" aria-labelledby="t-di" xmlns="http://www.w3.org/2000/svg">
<title id="t-di">Dihybrid cross checkerboard for seed shape and seed colour</title>
<g font-family="Inter,Segoe UI,sans-serif" font-size="13" fill="#1f2937">
<text x="16" y="26" font-weight="700">P: Round yellow (RRYY) × Wrinkled green (rryy)</text>
<text x="16" y="46">F₁: all round yellow (RrYy) → selfed (RrYy × RrYy)</text>
<text x="16" y="66" fill="#475569">Each F₁ plant forms four kinds of germ cells: RY, Ry, rY, ry</text>
<text x="378" y="100" text-anchor="middle" font-weight="700" fill="#475569">Germ cells of one F₁ parent →</text>
<text x="16" y="124" font-weight="700" fill="#475569">Germ cells of</text>
<text x="16" y="140" font-weight="700" fill="#475569">other parent ↓</text>
<text x="156" y="162" text-anchor="end" font-weight="700">RY</text>
<text x="156" y="212" text-anchor="end" font-weight="700">Ry</text>
<text x="156" y="262" text-anchor="end" font-weight="700">rY</text>
<text x="156" y="312" text-anchor="end" font-weight="700">ry</text>
<text x="222" y="122" text-anchor="middle" font-weight="700">RY</text>
<text x="326" y="122" text-anchor="middle" font-weight="700">Ry</text>
<text x="430" y="122" text-anchor="middle" font-weight="700">rY</text>
<text x="534" y="122" text-anchor="middle" font-weight="700">ry</text>
<rect x="170" y="132" width="104" height="50" fill="#fef08a" stroke="#475569" stroke-width="1.2"/><text x="222" y="154" text-anchor="middle" font-weight="700">RRYY</text><text x="222" y="171" text-anchor="middle" font-size="11" fill="#a16207">round yellow</text>
<rect x="274" y="132" width="104" height="50" fill="#fef08a" stroke="#475569" stroke-width="1.2"/><text x="326" y="154" text-anchor="middle" font-weight="700">RRYy</text><text x="326" y="171" text-anchor="middle" font-size="11" fill="#a16207">round yellow</text>
<rect x="378" y="132" width="104" height="50" fill="#fef08a" stroke="#475569" stroke-width="1.2"/><text x="430" y="154" text-anchor="middle" font-weight="700">RrYY</text><text x="430" y="171" text-anchor="middle" font-size="11" fill="#a16207">round yellow</text>
<rect x="482" y="132" width="104" height="50" fill="#fef08a" stroke="#475569" stroke-width="1.2"/><text x="534" y="154" text-anchor="middle" font-weight="700">RrYy</text><text x="534" y="171" text-anchor="middle" font-size="11" fill="#a16207">round yellow</text>
<rect x="170" y="182" width="104" height="50" fill="#fef08a" stroke="#475569" stroke-width="1.2"/><text x="222" y="204" text-anchor="middle" font-weight="700">RRYy</text><text x="222" y="221" text-anchor="middle" font-size="11" fill="#a16207">round yellow</text>
<rect x="274" y="182" width="104" height="50" fill="#bbf7d0" stroke="#475569" stroke-width="1.2"/><text x="326" y="204" text-anchor="middle" font-weight="700">RRyy</text><text x="326" y="221" text-anchor="middle" font-size="11" fill="#15803d">round green</text>
<rect x="378" y="182" width="104" height="50" fill="#fef08a" stroke="#475569" stroke-width="1.2"/><text x="430" y="204" text-anchor="middle" font-weight="700">RrYy</text><text x="430" y="221" text-anchor="middle" font-size="11" fill="#a16207">round yellow</text>
<rect x="482" y="182" width="104" height="50" fill="#bbf7d0" stroke="#475569" stroke-width="1.2"/><text x="534" y="204" text-anchor="middle" font-weight="700">Rryy</text><text x="534" y="221" text-anchor="middle" font-size="11" fill="#15803d">round green</text>
<rect x="170" y="232" width="104" height="50" fill="#fef08a" stroke="#475569" stroke-width="1.2"/><text x="222" y="254" text-anchor="middle" font-weight="700">RrYY</text><text x="222" y="271" text-anchor="middle" font-size="11" fill="#a16207">round yellow</text>
<rect x="274" y="232" width="104" height="50" fill="#fef08a" stroke="#475569" stroke-width="1.2"/><text x="326" y="254" text-anchor="middle" font-weight="700">RrYy</text><text x="326" y="271" text-anchor="middle" font-size="11" fill="#a16207">round yellow</text>
<rect x="378" y="232" width="104" height="50" fill="#fed7aa" stroke="#475569" stroke-width="1.2"/><text x="430" y="254" text-anchor="middle" font-weight="700">rrYY</text><text x="430" y="271" text-anchor="middle" font-size="11" fill="#c2410c">wrinkled yellow</text>
<rect x="482" y="232" width="104" height="50" fill="#fed7aa" stroke="#475569" stroke-width="1.2"/><text x="534" y="254" text-anchor="middle" font-weight="700">rrYy</text><text x="534" y="271" text-anchor="middle" font-size="11" fill="#c2410c">wrinkled yellow</text>
<rect x="170" y="282" width="104" height="50" fill="#fef08a" stroke="#475569" stroke-width="1.2"/><text x="222" y="304" text-anchor="middle" font-weight="700">RrYy</text><text x="222" y="321" text-anchor="middle" font-size="11" fill="#a16207">round yellow</text>
<rect x="274" y="282" width="104" height="50" fill="#bbf7d0" stroke="#475569" stroke-width="1.2"/><text x="326" y="304" text-anchor="middle" font-weight="700">Rryy</text><text x="326" y="321" text-anchor="middle" font-size="11" fill="#15803d">round green</text>
<rect x="378" y="282" width="104" height="50" fill="#fed7aa" stroke="#475569" stroke-width="1.2"/><text x="430" y="304" text-anchor="middle" font-weight="700">rrYy</text><text x="430" y="321" text-anchor="middle" font-size="11" fill="#c2410c">wrinkled yellow</text>
<rect x="482" y="282" width="104" height="50" fill="#c7d2fe" stroke="#475569" stroke-width="1.2"/><text x="534" y="304" text-anchor="middle" font-weight="700">rryy</text><text x="534" y="321" text-anchor="middle" font-size="11" fill="#4338ca">wrinkled green</text>
<!-- legend -->
<g stroke="#475569" stroke-width="1"><rect x="40" y="356" width="16" height="16" fill="#fef08a"/><rect x="330" y="356" width="16" height="16" fill="#bbf7d0"/><rect x="40" y="386" width="16" height="16" fill="#fed7aa"/><rect x="330" y="386" width="16" height="16" fill="#c7d2fe"/></g>
<text x="64" y="369">Round yellow — 9</text>
<text x="354" y="369">Round green — 3</text>
<text x="64" y="399">Wrinkled yellow — 3</text>
<text x="354" y="399">Wrinkled green — 1</text>
<text x="320" y="434" text-anchor="middle" font-weight="700">F₂ ratio 9 : 3 : 3 : 1 (two new combinations appear)</text>
</g>
</svg>
"""),
("sex-determination", "Sex determination in human beings: all eggs carry X; a sperm carrying X gives a girl (XX), a sperm carrying Y gives a boy (XY).", """
<svg viewBox="0 0 600 410" role="img" aria-labelledby="t-sd" xmlns="http://www.w3.org/2000/svg">
<title id="t-sd">Sex determination in human beings</title>
<g font-family="Inter,Segoe UI,sans-serif" font-size="13" fill="#1f2937">
<!-- parents -->
<rect x="80" y="20" width="140" height="58" rx="10" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>
<text x="150" y="44" text-anchor="middle" font-weight="700">Father</text>
<text x="150" y="64" text-anchor="middle">22 pairs + XY</text>
<rect x="380" y="20" width="140" height="58" rx="10" fill="#fce7f3" stroke="#be185d" stroke-width="2"/>
<text x="450" y="44" text-anchor="middle" font-weight="700">Mother</text>
<text x="450" y="64" text-anchor="middle">22 pairs + XX</text>
<text x="300" y="58" text-anchor="middle" font-size="22" font-weight="700">×</text>
<!-- parent to germ cells -->
<g stroke="#94a3b8" stroke-width="2"><line x1="130" y1="78" x2="104" y2="132"/><line x1="170" y1="78" x2="196" y2="132"/><line x1="450" y1="78" x2="450" y2="132"/></g>
<!-- germ cells -->
<g stroke-width="2"><circle cx="100" cy="162" r="30" fill="#eff6ff" stroke="#1d4ed8"/><circle cx="200" cy="162" r="30" fill="#eff6ff" stroke="#1d4ed8"/><circle cx="450" cy="162" r="30" fill="#fdf2f8" stroke="#be185d"/></g>
<text x="100" y="167" text-anchor="middle" font-weight="700">22 + X</text>
<text x="200" y="167" text-anchor="middle" font-weight="700">22 + Y</text>
<text x="450" y="167" text-anchor="middle" font-weight="700">22 + X</text>
<text x="62" y="158" text-anchor="end" fill="#1d4ed8" font-weight="700">Sperms</text>
<text x="62" y="176" text-anchor="end" fill="#1d4ed8">½ X, ½ Y</text>
<text x="490" y="158" fill="#be185d" font-weight="700">Eggs: all</text>
<text x="490" y="176" fill="#be185d">carry X</text>
<!-- fertilisation lines -->
<g stroke-width="2" fill="none">
<path d="M100 192 L150 296" stroke="#1d4ed8"/><path d="M200 192 L430 296" stroke="#1d4ed8"/>
<path d="M440 192 L170 296" stroke="#be185d" stroke-dasharray="6 4"/><path d="M455 192 L450 296" stroke="#be185d" stroke-dasharray="6 4"/>
</g>
<!-- offspring -->
<rect x="90" y="296" width="140" height="58" rx="10" fill="#fce7f3" stroke="#be185d" stroke-width="2"/>
<text x="160" y="320" text-anchor="middle" font-weight="700">Girl (XX)</text>
<text x="160" y="340" text-anchor="middle">22 pairs + XX</text>
<rect x="380" y="296" width="140" height="58" rx="10" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>
<text x="450" y="320" text-anchor="middle" font-weight="700">Boy (XY)</text>
<text x="450" y="340" text-anchor="middle">22 pairs + XY</text>
<text x="300" y="390" text-anchor="middle" fill="#475569">Each child: 50% chance of either sex — decided by the sperm</text>
</g>
</svg>
"""),
],
"formulas": [
("Monohybrid cross — F₁", "TT (tall) × tt (short) → all Tt", "All F₁ plants tall; short trait hidden"),
("Monohybrid cross — F₂ phenotype", "Tt × Tt → 3 dominant : 1 recessive", "3 tall : 1 short (e.g. 600 : 200 out of 800)"),
("Monohybrid cross — F₂ genotype", "1 TT : 2 Tt : 1 tt", "Out of 800: 200 TT, 400 Tt, 200 tt"),
("Dihybrid cross — F₁", "RRYY × rryy → all RrYy", "All round yellow seeds"),
("Dihybrid cross — F₂", "9 : 3 : 3 : 1 (16 combinations)", "Round yellow 9 · round green 3 · wrinkled yellow 3 · wrinkled green 1"),
("Germ cells of a dihybrid", "RrYy → RY, Ry, rY, ry (equal numbers)", "Each germ cell has one copy of each gene"),
("Checking TT vs Tt", "Self-pollinate the tall plant", "All tall → TT · some short (3 : 1) → Tt"),
("Gene action", "gene → protein (enzyme) → hormone → trait", "Efficient enzyme → more growth hormone → tall plant"),
("Human chromosomes", "23 pairs = 22 pairs autosomes + 1 pair sex chromosomes", "Female XX · male XY"),
("Sex determination", "X-sperm + X-egg → XX · Y-sperm + X-egg → XY", "Probability of a boy = probability of a girl = ½"),
],
"worked": [
("A tall pea plant with violet flowers is crossed with a short plant with white flowers. All the offspring have violet flowers, but about half of them are short. Which is the genotype of the tall parent: (a) TTWW (b) TTww (c) TtWW (d) TtWw? (1 mark)", """
<p class="ans"><b>(c) TtWW.</b> All offspring are violet, so the tall parent gives only W (it is WW). Half the offspring are short (tt), so the tall parent must also carry t — it is Tt.</p>
"""),
("How is the equal genetic contribution of the male and female parents ensured in the progeny? (2 marks)", """
<p class="ans">Body cells carry two sets of chromosomes, but each germ cell (sperm or egg) receives only <b>one chromosome of each pair</b>, i.e. half the number. At fertilisation one set from the father and one set from the mother come together, so the zygote has two copies of every chromosome — one from each parent — and the chromosome number is restored.</p>
"""),
("A man with blood group A marries a woman with blood group O, and their daughter has blood group O. Is this enough to tell whether trait A or trait O is dominant? Give a reason. (2 marks)", """
<p class="ans"><b>No.</b> If A were dominant, the father could carry one A and one O copy and pass the O copy to the daughter, who would then be O. If O were dominant, the daughter would also be O. Both explanations fit one child, so the result of a single cross cannot decide dominance; a large number of offspring would have to be studied.</p>
"""),
("With the help of a cross, explain how Mendel showed that some traits are dominant and others recessive. (3 marks)", """
<ol>
<li>Parents: pure tall (TT) × pure short (tt). Germ cells: T and t.</li>
<li>F₁: all <b>Tt</b> and all tall — only one of the two traits is expressed; this is the <b>dominant</b> trait.</li>
<li>F₁ selfed (Tt × Tt) → TT, Tt, Tt, tt. F₂ shows tall : short = <b>3 : 1</b>.</li>
</ol>
<p class="ans">The short trait, absent in F₁, reappears in F₂ unchanged. So F₁ plants carried it without showing it — shortness is <b>recessive</b> and is expressed only when both copies are t.</p>
"""),
("In a monohybrid cross between pure tall and pure short pea plants, 800 plants were raised in the F₂ generation. (a) How many would be tall and how many short? (b) How many of the tall plants are expected to be pure-breeding? (c) How would you check whether a given tall F₂ plant is pure? (3 marks)", """
<ol>
<li>(a) Tall : short = 3 : 1 → tall = ¾ × 800 = <b>600</b>; short = ¼ × 800 = <b>200</b>.</li>
<li>(b) Genotypes 1 TT : 2 Tt : 1 tt → TT = ¼ × 800 = <b>200</b>. So 200 of the 600 tall plants are pure (the other 400 are Tt).</li>
<li>(c) Self-pollinate the plant. If all its offspring are tall it is <b>TT</b>; if some short plants appear (about one in four) it is <b>Tt</b>.</li>
</ol>
"""),
("“The sex of a child is decided by the mother.” Is this statement correct? Explain sex determination in human beings with a flow chart. (3 marks)", """
<p>No, the statement is wrong.</p>
<ol>
<li>Females have XX sex chromosomes, so every egg carries <b>X</b>.</li>
<li>Males have XY, so half the sperms carry <b>X</b> and half carry <b>Y</b>.</li>
<li>X-sperm + X-egg → <b>XX, girl</b>; Y-sperm + X-egg → <b>XY, boy</b>.</li>
</ol>
<p class="ans">The child's sex depends on whether an X-bearing or a Y-bearing sperm fertilises the egg — that is, on the chromosome inherited from the <b>father</b>. The chance of a boy or a girl is 50% each.</p>
"""),
("How do genes control the characteristics (traits) of an organism? Explain with the example of plant height. (3 marks)", """
<p class="ans">A gene is a section of DNA that carries the information to make a particular <b>protein</b>, often an enzyme. Plant height depends on a growth hormone, and the amount of this hormone made depends on the efficiency of an enzyme. If the gene makes an efficient enzyme, more hormone is made and the plant grows tall. If the gene is altered so the enzyme works less efficiently, less hormone forms and the plant is short. Thus <b>gene → protein (enzyme) → hormone → trait</b>.</p>
"""),
("(a) Mendel crossed pea plants having round yellow seeds (RRYY) with plants having wrinkled green seeds (rryy). Write the phenotype and genotype of the F₁ generation. (b) Name the kinds of germ cells formed by an F₁ plant. (c) Give the phenotypic ratio of the F₂ generation. If 160 F₂ seeds were obtained, how many of each kind would be expected? (d) What does this cross prove? (5 marks)", """
<ol>
<li>(a) F₁: all <b>round yellow</b>, genotype <b>RrYy</b> (round and yellow are dominant).</li>
<li>(b) Four kinds, in equal numbers: <b>RY, Ry, rY, ry</b>.</li>
<li>(c) F₂ ratio = round yellow 9 : round green 3 : wrinkled yellow 3 : wrinkled green 1 (total 16 parts). For 160 seeds, one part = 160 ÷ 16 = 10: round yellow <b>90</b>, round green <b>30</b>, wrinkled yellow <b>30</b>, wrinkled green <b>10</b> (check: 90 + 30 + 30 + 10 = 160).</li>
<li>(d) Round green and wrinkled yellow are <b>new combinations</b> found in neither parent. So the genes for seed shape and seed colour separate and are <b>inherited independently</b> of each other. Each trait on its own still follows 3 : 1 (round : wrinkled = 120 : 40).</li>
</ol>
"""),
],
"mistakes": [
("Putting two copies in a germ cell", "Writing the germ cells of a TT plant as “TT”.", "A germ cell carries one copy of each gene: TT gives only T; Tt gives T and t."),
("Mixing up the two F₂ ratios", "“F₂ genotypic ratio is 3 : 1.”", "3 : 1 is the phenotypic ratio; the genotypic ratio is 1 TT : 2 Tt : 1 tt."),
("Saying the recessive trait is lost", "“In F₁ the shortness trait is destroyed.”", "It is present but not expressed (Tt); it reappears in F₂."),
("Using unrelated letters", "Writing tall as T and short as S.", "Use the same letter for one gene: capital for dominant (T), small for recessive (t)."),
("Blaming the mother for the child's sex", "“The mother decides whether the baby is a boy or a girl.”", "All eggs carry X; the sperm carries X or Y, so the father's chromosome decides."),
("Forgetting the new combinations", "Listing only round yellow and wrinkled green in the dihybrid F₂.", "F₂ also has round green and wrinkled yellow — proof of independent inheritance (9 : 3 : 3 : 1)."),
("Thinking asexual offspring never vary", "“Bacteria produced by fission are exact copies.”", "DNA copying is not perfectly accurate, so minor variations still arise and accumulate slowly."),
],
"revision": [
"Heredity = transmission of traits from parents to offspring; variation = differences among individuals.",
"Variation is greatest with sexual reproduction (DNA of two parents); asexual gives only minor copying-error variation.",
"Variants that suit the environment survive better — the basis of evolution.",
"Earlobe activity: free and attached earlobes — an inherited trait.",
"Mendel used garden pea (Pisum sativum): contrasting traits, short life cycle, self-pollinating, many seeds.",
"Each trait is controlled by two copies of a gene, one from each parent; a germ cell carries only one copy.",
"Dominant trait shows with one copy (T); recessive trait shows only in double copy (tt).",
"TT × tt → F₁ all Tt (tall). F₁ selfed → F₂ 3 tall : 1 short; genotype 1 TT : 2 Tt : 1 tt.",
"Genotype = genetic make-up (TT, Tt, tt); phenotype = visible trait (tall, short).",
"Self-pollinate a tall plant: all tall offspring → TT; some short → Tt.",
"RRYY × rryy → F₁ RrYy (round yellow) → F₂ 9 : 3 : 3 : 1 — traits inherited independently.",
"A gene is a section of DNA that codes for a protein: gene → enzyme → hormone → height.",
"Germ cells get one chromosome of each pair, so the chromosome number stays constant across generations.",
"Sex determination: temperature in some reptiles; some snails change sex; genetic in humans.",
"Humans: 23 pairs of chromosomes — 22 pairs autosomes + XX (female) or XY (male).",
"All eggs carry X; sperms carry X or Y — the father's sperm decides the child's sex (50 : 50).",
],
"practice": [
("chapters/heredity-evolution-10.html", "Heredity quiz"),
("cbse-class-10-science-mock-tests.html", "Class 10 Science mock tests"),
("formula-board/", "Formula Board revision cards"),
],
}
