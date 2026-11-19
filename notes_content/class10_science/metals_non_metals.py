"""Class 10 Science — Chapter 3: Metals and Non-metals (NCERT, rationalised 2026–27 syllabus)."""

CHAPTER = {
"slug": "metals-and-non-metals",
"class": "10", "subject": "Science", "subject_slug": "science", "number": 3,
"title": "Metals and Non-metals",
"status": "draft",                     # draft = hidden preview; live = published after approval
"updated": "2026-11-19",
"unit": "Unit I · Chemical Substances – Nature and Behaviour",
"description": "CBSE Class 10 Science Chapter 3 notes: physical and chemical properties of metals and non-metals, the reactivity series, ionic compounds, extraction and refining of metals, corrosion and its prevention, and alloys — with labelled diagrams, worked examples and common mistakes.",
"glance": """
<p>Metals are usually hard, shiny, malleable, ductile and good conductors; non-metals are mostly the opposite. Chemically, metals <b>lose electrons</b> to form positive ions and basic oxides, while non-metals <b>gain electrons</b> and form acidic oxides. Arranging metals by how readily they react gives the <b>reactivity series</b>, which explains displacement reactions and decides how each metal is extracted from its ore. The chapter ends with corrosion and the ways we prevent it.</p>
<ul>
  <li>Write equations for metals reacting with oxygen, water/steam, dilute acids and salt solutions; explain amphoteric oxides.</li>
  <li>Use the reactivity series to predict displacement reactions.</li>
  <li>Show the formation of NaCl and MgCl₂ by electron-dot structures and list properties of ionic compounds.</li>
  <li>Explain roasting, calcination, reduction (carbon, thermit), electrolytic reduction and electrolytic refining of copper.</li>
  <li>Describe the experiment on conditions for rusting and methods to prevent corrosion; name common alloys.</li>
</ul>
""",
"concepts": [
("Physical properties of metals", """
<p>Pure metals have a shining surface — <b>metallic lustre</b> (seen when iron, copper or magnesium is rubbed with sandpaper) — and are generally <b>hard</b>, though hardness varies.</p>
<ul>
  <li><b>Malleability:</b> metals can be beaten into thin sheets. Gold and silver are the most malleable.</li>
  <li><b>Ductility:</b> metals can be drawn into thin wires. Gold is the most ductile — one gram of gold can be drawn into a wire about 2 km long.</li>
  <li><b>Conduction of heat:</b> wax on one end of a copper or aluminium wire melts when the other end is heated. Silver and copper are the best conductors.</li>
  <li><b>Conduction of electricity:</b> a bulb in a circuit glows when a metal is placed in the gap; this is why wires are coated with PVC or rubber.</li>
  <li><b>Sonority:</b> metals produce a ringing sound when struck — that is why school bells are made of metal.</li>
</ul>
<p><b>Exceptions:</b> mercury is liquid at room temperature; gallium and caesium melt on the palm; sodium and potassium are soft enough to cut with a knife and have low densities and melting points; lead and mercury conduct heat poorly.</p>
"""),
("Physical properties of non-metals", """
<p>Non-metals are solids (carbon, sulphur, iodine) or gases (oxygen, nitrogen, hydrogen); <b>bromine</b> is the only liquid non-metal. Sulphur and coal (carbon) crumble into powder when hammered — non-metals are <b>brittle</b>, neither malleable nor ductile, generally dull and poor conductors of heat and electricity.</p>
<p><b>Exceptions:</b> iodine is lustrous; carbon as <b>diamond</b> is the hardest natural substance with a very high melting and boiling point, and as <b>graphite</b> is a conductor of electricity. Elements showing properties of both are <b>metalloids</b>. Physical properties alone cannot classify elements, so chemical properties are used.</p>
"""),
("Metals and non-metals with oxygen", """
<p>Burnt magnesium ribbon gives white MgO, whose solution turns red litmus <b>blue</b>; burnt sulphur gives SO₂, whose solution turns blue litmus <b>red</b>. So metal oxides are <b>basic</b> and non-metal oxides are generally <b>acidic</b>.</p>
<p class="eq">Metal + Oxygen → Metal oxide &nbsp;&nbsp;|&nbsp;&nbsp; 2Cu + O₂ → 2CuO (black) &nbsp;&nbsp;|&nbsp;&nbsp; 4Al + 3O₂ → 2Al₂O₃</p>
<p>Some metal oxides, such as Al₂O₃ and ZnO, react with both acids and bases to give salt and water. They are <b>amphoteric oxides</b>:</p>
<p class="eq">Al₂O₃ + 6HCl → 2AlCl₃ + 3H₂O &nbsp;&nbsp;|&nbsp;&nbsp; Al₂O₃ + 2NaOH → 2NaAlO₂ (sodium aluminate) + H₂O</p>
<p>Most metal oxides are insoluble in water; the soluble ones form <b>alkalis</b>: Na₂O + H₂O → 2NaOH and K₂O + H₂O → 2KOH.</p>
<p><b>Sodium and potassium</b> catch fire in open air, so they are stored under <b>kerosene</b>. Mg, Al, Zn and Pb form a protective oxide layer. Magnesium burns with a dazzling white flame; iron filings burn when sprinkled in a flame; copper only gets coated with black CuO; silver and gold do not react even at high temperature. Thickening aluminium's oxide layer by electrolysis is <b>anodising</b>.</p>
"""),
("Metals with water", """
<p class="eq">Metal + Water → Metal oxide + Hydrogen; metal oxide + water → metal hydroxide</p>
<ul>
  <li><b>Potassium and sodium</b> react violently with <b>cold</b> water; the heat ignites the hydrogen: 2K + 2H₂O → 2KOH + H₂ + heat (similarly for Na).</li>
  <li><b>Calcium</b> reacts less violently and starts <b>floating</b> as hydrogen bubbles stick to it: Ca + 2H₂O → Ca(OH)₂ + H₂.</li>
  <li><b>Magnesium</b> reacts with <b>hot</b> water and also floats.</li>
  <li><b>Aluminium, iron and zinc</b> react only with <b>steam</b>, giving the oxide and hydrogen: 2Al + 3H₂O → Al₂O₃ + 3H₂ and 3Fe + 4H₂O → Fe₃O₄ + 4H₂.</li>
  <li><b>Lead, copper, silver and gold</b> do not react with water at all.</li>
</ul>
"""),
("Metals with dilute acids", """
<p class="eq">Metal + Dilute acid → Salt + Hydrogen</p>
<p>With dilute HCl, magnesium reacts most vigorously (the tube gets warmest), then aluminium, zinc and iron (Fe + 2HCl → FeCl₂ + H₂); copper does not react. Hydrogen is <b>not</b> evolved when metals react with <b>nitric acid</b>, because HNO₃ is a strong oxidising agent: it oxidises the H₂ to water and is itself reduced to an oxide of nitrogen. Only magnesium and manganese give H₂ with <b>very dilute</b> HNO₃.</p>
<p><b>Aqua regia</b> (“royal water”) is a freshly prepared mixture of concentrated hydrochloric acid and concentrated nitric acid in the ratio <b>3 : 1</b>. It dissolves gold and platinum, which neither acid can dissolve alone.</p>
"""),
("Metals with solutions of other metal salts: the reactivity series", """
<p>An iron nail in blue copper sulphate solution gets a brown copper coating and the solution turns pale green; copper in iron sulphate solution shows no change. A more reactive metal <b>displaces</b> a less reactive metal from its salt solution:</p>
<p class="eq">Fe + CuSO₄ → FeSO₄ + Cu &nbsp;&nbsp;|&nbsp;&nbsp; Metal A + Salt of B → Salt of A + Metal B (if A is more reactive)</p>
<p>Metals listed in decreasing order of reactivity form the <b>reactivity series</b>:</p>
<p class="eq">K &gt; Na &gt; Ca &gt; Mg &gt; Al &gt; Zn &gt; Fe &gt; Pb &gt; [H] &gt; Cu &gt; Hg &gt; Ag &gt; Au</p>
<p>Metals above hydrogen displace hydrogen from dilute acids; copper, mercury, silver and gold, below hydrogen, cannot.</p>
"""),
("How metals and non-metals react: ionic compounds", """
<p>Noble gases have a filled valence shell (octet; helium a duplet) and are unreactive; other elements react to attain this stable configuration. Sodium (2, 8, 1) <b>loses</b> one electron to become Na⁺ (2, 8); chlorine (2, 8, 7) <b>gains</b> that electron to become Cl⁻ (2, 8, 8). The oppositely charged ions are held by strong electrostatic attraction:</p>
<p class="eq">Na → Na⁺ + e⁻ &nbsp;&nbsp;|&nbsp;&nbsp; Cl + e⁻ → Cl⁻ &nbsp;&nbsp;|&nbsp;&nbsp; Na⁺ + Cl⁻ → NaCl</p>
<p>Magnesium (2, 8, 2) similarly gives one electron to each of two chlorine atoms (Mg²⁺, 2Cl⁻ → MgCl₂). Compounds formed by electron transfer from a metal to a non-metal are <b>ionic</b> or <b>electrovalent compounds</b>. Their properties:</p>
<ul>
  <li><b>Physical nature:</b> solid, hard and <b>brittle</b> because of strong forces between ions.</li>
  <li><b>High melting and boiling points:</b> much energy is needed to overcome the strong inter-ionic attraction (NaCl melts at 1074 K).</li>
  <li><b>Solubility:</b> generally soluble in water and insoluble in kerosene and petrol.</li>
  <li><b>Conduction:</b> no conduction as solids, where ions cannot move; they conduct when <b>molten</b> or <b>dissolved in water</b>, as the ions become free to move.</li>
</ul>
"""),
("Occurrence and extraction of metals", """
<p>The earth's crust is the main source of metals (sea water also has some). Naturally occurring compounds are <b>minerals</b>; a mineral from which a metal can be profitably extracted is an <b>ore</b>. Least reactive metals (Au, Ag, Pt, Cu) occur <b>free</b>; the most reactive (K, Na, Ca, Mg, Al) never do; middle ones (Zn, Fe, Pb) occur as oxides, sulphides or carbonates.</p>
<p><b>Enrichment:</b> ores contain unwanted soil and sand called <b>gangue</b>, removed first. The extraction method then depends on reactivity.</p>
<p><b>Low in the series</b> — oxides are reduced by heating alone. Cinnabar (HgS) is heated in air: 2HgS + 3O₂ → 2HgO + 2SO₂, then 2HgO → 2Hg + O₂. Copper from Cu₂S: 2Cu₂S + 3O₂ → 2Cu₂O + 2SO₂, then 2Cu₂O + Cu₂S → 6Cu + SO₂.</p>
<p><b>Middle of the series</b> — metals are easier to obtain from oxides, so sulphide and carbonate ores are first converted to oxides. <b>Roasting</b> is heating a sulphide ore strongly in excess air: 2ZnS + 3O₂ → 2ZnO + 2SO₂. <b>Calcination</b> is heating a carbonate ore strongly in limited air: ZnCO₃ → ZnO + CO₂. The oxide is then <b>reduced</b> with carbon: ZnO + C → Zn + CO. Reactive metals like aluminium can also reduce oxides; with iron(III) oxide the reaction is so exothermic that molten iron forms — the <b>thermit reaction</b>, used to join railway tracks and cracked machine parts:</p>
<p class="eq">Fe₂O₃ + 2Al → 2Fe + Al₂O₃ + heat &nbsp;&nbsp;|&nbsp;&nbsp; 3MnO₂ + 4Al → 3Mn + 2Al₂O₃ + heat</p>
<p><b>Top of the series</b> — carbon cannot reduce their oxides, as these metals have more affinity for oxygen. They are obtained by <b>electrolytic reduction</b> of their molten chlorides; the metal deposits at the cathode and chlorine is liberated at the anode: Na⁺ + e⁻ → Na (cathode); 2Cl⁻ → Cl₂ + 2e⁻ (anode). Aluminium is obtained by electrolytic reduction of aluminium oxide.</p>
<p><b>Refining:</b> the metal obtained is impure. In <b>electrolytic refining</b> of copper, a thick block of <b>impure copper is the anode</b>, a thin strip of <b>pure copper is the cathode</b>, and acidified copper sulphate solution is the electrolyte. On passing current, copper dissolves from the anode and an equal amount of pure copper deposits on the cathode. Soluble impurities enter the solution; insoluble ones settle below the anode as <b>anode mud</b>.</p>
"""),
("Corrosion and its prevention", """
<p>Silver turns black (silver sulphide), copper gains a green coat (basic copper carbonate, from moist CO₂) and iron gets brown flaky <b>rust</b>. This slow eating away of metals is <b>corrosion</b>.</p>
<p><b>Conditions for rusting:</b> take clean iron nails in three test tubes. In <b>A</b> the nail is in ordinary water, open to air. In <b>B</b> it is in <b>boiled distilled water</b> (no dissolved air) with a layer of oil on top to stop air dissolving. In <b>C</b> it sits above <b>anhydrous calcium chloride</b>, which absorbs moisture, in a corked tube (dry air). After a few days only the nail in A has rusted. So iron rusts only when <b>both air (oxygen) and water</b> are present.</p>
<p><b>Prevention:</b> painting, oiling, greasing, <b>galvanising</b> (coating iron or steel with a thin layer of zinc — the article stays protected even if the zinc layer is broken, because zinc is more reactive and corrodes first), chrome plating, anodising and making alloys.</p>
<p><b>Alloys:</b> a homogeneous mixture of two or more metals, or a metal and a non-metal, made by melting them together. Pure iron is soft; with a little carbon (about 0.05%) it becomes hard, strong steel. <b>Stainless steel</b> (iron with nickel and chromium) is hard and does not rust. An alloy of mercury is an <b>amalgam</b>. <b>Brass</b> = copper + zinc; <b>bronze</b> = copper + tin; <b>solder</b> = lead + tin, with a low melting point, used to weld electrical wires. Alloys have lower conductivity and melting points than the pure metals. Pure (24-carat) gold is too soft for jewellery, so <b>22-carat gold</b> — 22 parts gold with 2 parts silver or copper — is used.</p>
"""),
],
"diagrams": [
("steam", "Action of steam on a metal: the metal heated in steam from the wet glass wool forms its oxide, and hydrogen is collected over water.", """
<svg viewBox="0 0 660 340" role="img" aria-labelledby="t-st" xmlns="http://www.w3.org/2000/svg">
<title id="t-st">Action of steam on a metal with hydrogen gas collected by downward displacement of water</title>
<defs><radialGradient id="mn-flame" cx=".5" cy=".7" r=".6"><stop offset="0" stop-color="#bfdbfe"/><stop offset=".5" stop-color="#60a5fa"/><stop offset="1" stop-color="#f59e0b"/></radialGradient></defs>
<!-- clamp stand -->
<rect x="62" y="306" width="120" height="10" rx="2" fill="#6b7280"/>
<rect x="86" y="126" width="6" height="182" fill="#9ca3af" stroke="#4b5563" stroke-width="1"/>
<rect x="92" y="147" width="56" height="6" fill="#9ca3af" stroke="#4b5563" stroke-width="1"/>
<!-- boiling tube (horizontal) -->
<path d="M330 132 H140 Q120 132 120 150 Q120 168 140 168 H330" fill="#f8fafc" stroke="#3a4a63" stroke-width="2.4"/>
<rect x="140" y="128" width="14" height="44" rx="3" fill="#78716c" stroke="#44403c" stroke-width="1.2"/>
<g fill="#e0f2fe" stroke="#7dd3fc" stroke-width="1"><path d="M160 136 q8 6 0 12 q8 6 0 12 q8 4 4 6 h28 q-6 -4 0 -8 q-8 -6 0 -12 q-8 -6 0 -10z"/></g>
<g fill="#9ca3af" stroke="#4b5563" stroke-width="1"><path d="M220 167 l6 -9 l9 2 l2 7z"/><path d="M236 167 l5 -8 l10 1 l3 7z"/><path d="M252 167 l6 -7 l8 3 l1 4z"/></g>
<rect x="330" y="134" width="20" height="32" rx="3" fill="#a16207" stroke="#713f12" stroke-width="1.5"/>
<!-- burner -->
<ellipse cx="243" cy="198" rx="10" ry="26" fill="url(#mn-flame)"/>
<rect x="235" y="222" width="16" height="78" fill="#9ca3af" stroke="#4b5563" stroke-width="1.2"/>
<rect x="215" y="298" width="56" height="10" rx="2" fill="#6b7280"/>
<!-- trough -->
<path d="M430 220 V306 Q430 312 436 312 H614 Q620 312 620 306 V220" fill="none" stroke="#3a4a63" stroke-width="2.6"/>
<rect x="432" y="240" width="186" height="70" fill="#dbeafe"/>
<line x1="432" y1="240" x2="618" y2="240" stroke="#60a5fa" stroke-width="1.5"/>
<!-- inverted gas jar / test tube -->
<path d="M520 284 V170 Q520 152 537 152 Q554 152 554 170 V284" fill="#ffffff" stroke="#3a4a63" stroke-width="2.4"/>
<path d="M522 214 H552 V284 H522Z" fill="#dbeafe"/>
<!-- delivery tube -->
<path d="M350 150 H470 V292 H530 V270" fill="none" stroke="#3a4a63" stroke-width="6" stroke-linejoin="round"/>
<path d="M350 150 H470 V292 H530 V270" fill="none" stroke="#f8fafc" stroke-width="2.5" stroke-linejoin="round"/>
<g fill="#fff" stroke="#3b82f6" stroke-width="1"><circle cx="534" cy="256" r="2.5"/><circle cx="538" cy="238" r="2"/><circle cx="533" cy="222" r="2.5"/></g>
<g font-family="Inter,Segoe UI,sans-serif" font-size="13" fill="#1f2937">
<line x1="124" y1="96" x2="178" y2="142" stroke="#6b7280"/><text x="16" y="82">Glass wool</text><text x="16" y="98">soaked in water</text>
<line x1="246" y1="104" x2="240" y2="160" stroke="#6b7280"/><text x="246" y="96" text-anchor="middle">Metal sample</text>
<line x1="356" y1="104" x2="320" y2="133" stroke="#6b7280"/><text x="360" y="96" text-anchor="middle">Boiling tube</text>
<text x="420" y="140" text-anchor="middle">Delivery tube</text>
<line x1="560" y1="182" x2="545" y2="190" stroke="#6b7280"/><text x="564" y="172" font-weight="700">Hydrogen</text><text x="564" y="188" font-weight="700">gas</text>
<line x1="172" y1="262" x2="235" y2="262" stroke="#6b7280"/><text x="118" y="266">Burner</text>
<line x1="74" y1="232" x2="86" y2="232" stroke="#6b7280"/><text x="16" y="236">Stand</text>
<text x="590" y="300" text-anchor="middle">Water</text>
<text x="525" y="332" text-anchor="middle">Trough</text>
</g>
</svg>
"""),
("electron-dot", "Formation of sodium chloride and magnesium chloride by transfer of electrons (crosses = electrons of the metal, dots = electrons of chlorine).", """
<svg viewBox="0 0 640 300" role="img" aria-labelledby="t-ed" xmlns="http://www.w3.org/2000/svg">
<title id="t-ed">Electron-dot structures showing transfer of electrons in the formation of sodium chloride and magnesium chloride</title>
<defs><marker id="mn-ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#b91c1c"/></marker></defs>
<g font-family="Inter,Segoe UI,sans-serif" fill="#1f2937">
<text x="60" y="79" text-anchor="middle" font-size="20" font-weight="700">Na</text><path d="M80 69 L86 75 M86 69 L80 75" stroke="#b91c1c" stroke-width="1.8"/>
<path d="M84 64 Q119.0 30 154 64" fill="none" stroke="#b91c1c" stroke-width="1.5" marker-end="url(#mn-ah)"/>
<text x="118" y="79" text-anchor="middle" font-size="20">+</text>
<text x="180" y="79" text-anchor="middle" font-size="20" font-weight="700">Cl</text><circle cx="175" cy="51" r="2.6" fill="#1d4ed8"/><circle cx="185" cy="51" r="2.6" fill="#1d4ed8"/><circle cx="175" cy="93" r="2.6" fill="#1d4ed8"/><circle cx="185" cy="93" r="2.6" fill="#1d4ed8"/><circle cx="203" cy="67" r="2.6" fill="#1d4ed8"/><circle cx="203" cy="77" r="2.6" fill="#1d4ed8"/><circle cx="157" cy="72" r="2.6" fill="#1d4ed8"/>
<text x="250" y="79" text-anchor="middle" font-size="22">→</text>
<path d="M300 42 H294 V102 H300 M340 42 H346 V102 H340" fill="none" stroke="#1f2937" stroke-width="1.6"/><text x="349" y="50" font-size="14" font-weight="700">+</text>
<text x="320" y="79" text-anchor="middle" font-size="20" font-weight="700">Na</text>
<path d="M392 42 H386 V102 H392 M448 42 H454 V102 H448" fill="none" stroke="#1f2937" stroke-width="1.6"/><text x="457" y="50" font-size="14" font-weight="700">−</text>
<text x="420" y="79" text-anchor="middle" font-size="20" font-weight="700">Cl</text><circle cx="415" cy="51" r="2.6" fill="#1d4ed8"/><circle cx="425" cy="51" r="2.6" fill="#1d4ed8"/><circle cx="415" cy="93" r="2.6" fill="#1d4ed8"/><circle cx="425" cy="93" r="2.6" fill="#1d4ed8"/><circle cx="443" cy="67" r="2.6" fill="#1d4ed8"/><circle cx="443" cy="77" r="2.6" fill="#1d4ed8"/><path d="M394 69 L400 75 M400 69 L394 75" stroke="#b91c1c" stroke-width="1.8"/>
<text x="60" y="120" text-anchor="middle" font-size="12" fill="#4b5563">Na (2, 8, 1)</text>
<text x="180" y="120" text-anchor="middle" font-size="12" fill="#4b5563">Cl (2, 8, 7)</text>
<text x="320" y="120" text-anchor="middle" font-size="12" fill="#4b5563">Na⁺ (2, 8)</text>
<text x="420" y="120" text-anchor="middle" font-size="12" fill="#4b5563">Cl⁻ (2, 8, 8)</text>
<text x="370" y="144" text-anchor="middle" font-size="13" font-weight="700">Sodium chloride, NaCl</text>
<text x="60" y="219" text-anchor="middle" font-size="20" font-weight="700">Cl</text><circle cx="55" cy="191" r="2.6" fill="#1d4ed8"/><circle cx="65" cy="191" r="2.6" fill="#1d4ed8"/><circle cx="55" cy="233" r="2.6" fill="#1d4ed8"/><circle cx="65" cy="233" r="2.6" fill="#1d4ed8"/><circle cx="37" cy="207" r="2.6" fill="#1d4ed8"/><circle cx="37" cy="217" r="2.6" fill="#1d4ed8"/><circle cx="83" cy="212" r="2.6" fill="#1d4ed8"/>
<text x="106" y="219" text-anchor="middle" font-size="20">+</text>
<text x="150" y="219" text-anchor="middle" font-size="20" font-weight="700">Mg</text><path d="M124 209 L130 215 M130 209 L124 215" stroke="#b91c1c" stroke-width="1.8"/><path d="M170 209 L176 215 M176 209 L170 215" stroke="#b91c1c" stroke-width="1.8"/>
<path d="M126 204 Q106.0 170 86 204" fill="none" stroke="#b91c1c" stroke-width="1.5" marker-end="url(#mn-ah)"/>
<path d="M174 204 Q194.0 170 214 204" fill="none" stroke="#b91c1c" stroke-width="1.5" marker-end="url(#mn-ah)"/>
<text x="196" y="219" text-anchor="middle" font-size="20">+</text>
<text x="240" y="219" text-anchor="middle" font-size="20" font-weight="700">Cl</text><circle cx="235" cy="191" r="2.6" fill="#1d4ed8"/><circle cx="245" cy="191" r="2.6" fill="#1d4ed8"/><circle cx="235" cy="233" r="2.6" fill="#1d4ed8"/><circle cx="245" cy="233" r="2.6" fill="#1d4ed8"/><circle cx="263" cy="207" r="2.6" fill="#1d4ed8"/><circle cx="263" cy="217" r="2.6" fill="#1d4ed8"/><circle cx="217" cy="212" r="2.6" fill="#1d4ed8"/>
<text x="300" y="219" text-anchor="middle" font-size="22">→</text>
<path d="M342 182 H336 V242 H342 M398 182 H404 V242 H398" fill="none" stroke="#1f2937" stroke-width="1.6"/><text x="407" y="190" font-size="14" font-weight="700">−</text>
<text x="370" y="219" text-anchor="middle" font-size="20" font-weight="700">Cl</text><circle cx="365" cy="191" r="2.6" fill="#1d4ed8"/><circle cx="375" cy="191" r="2.6" fill="#1d4ed8"/><circle cx="365" cy="233" r="2.6" fill="#1d4ed8"/><circle cx="375" cy="233" r="2.6" fill="#1d4ed8"/><circle cx="347" cy="207" r="2.6" fill="#1d4ed8"/><circle cx="347" cy="217" r="2.6" fill="#1d4ed8"/><path d="M390 209 L396 215 M396 209 L390 215" stroke="#b91c1c" stroke-width="1.8"/>
<path d="M438 182 H432 V242 H438 M482 182 H488 V242 H482" fill="none" stroke="#1f2937" stroke-width="1.6"/><text x="491" y="190" font-size="14" font-weight="700">2+</text>
<text x="460" y="219" text-anchor="middle" font-size="20" font-weight="700">Mg</text>
<path d="M528 182 H522 V242 H528 M584 182 H590 V242 H584" fill="none" stroke="#1f2937" stroke-width="1.6"/><text x="593" y="190" font-size="14" font-weight="700">−</text>
<text x="556" y="219" text-anchor="middle" font-size="20" font-weight="700">Cl</text><circle cx="551" cy="191" r="2.6" fill="#1d4ed8"/><circle cx="561" cy="191" r="2.6" fill="#1d4ed8"/><circle cx="551" cy="233" r="2.6" fill="#1d4ed8"/><circle cx="561" cy="233" r="2.6" fill="#1d4ed8"/><circle cx="579" cy="207" r="2.6" fill="#1d4ed8"/><circle cx="579" cy="217" r="2.6" fill="#1d4ed8"/><path d="M530 209 L536 215 M536 209 L530 215" stroke="#b91c1c" stroke-width="1.8"/>
<text x="60" y="260" text-anchor="middle" font-size="12" fill="#4b5563">Cl (2, 8, 7)</text>
<text x="150" y="260" text-anchor="middle" font-size="12" fill="#4b5563">Mg (2, 8, 2)</text>
<text x="240" y="260" text-anchor="middle" font-size="12" fill="#4b5563">Cl (2, 8, 7)</text>
<text x="370" y="260" text-anchor="middle" font-size="12" fill="#4b5563">Cl⁻ (2, 8, 8)</text>
<text x="460" y="260" text-anchor="middle" font-size="12" fill="#4b5563">Mg²⁺ (2, 8)</text>
<text x="556" y="260" text-anchor="middle" font-size="12" fill="#4b5563">Cl⁻ (2, 8, 8)</text>
<text x="463" y="284" text-anchor="middle" font-size="13" font-weight="700">Magnesium chloride, MgCl₂</text>
<path d="M497 17 L503 23 M503 17 L497 23" stroke="#b91c1c" stroke-width="1.8"/><text x="510" y="24" font-size="12">metal electron</text><circle cx="500" cy="38" r="2.6" fill="#1d4ed8"/><text x="510" y="42" font-size="12">non-metal electron</text>
</g></svg>
"""),
("refining", "Electrolytic refining of copper: impure copper anode, pure copper cathode, acidified copper sulphate electrolyte and anode mud.", """
<svg viewBox="0 0 620 340" role="img" aria-labelledby="t-rf" xmlns="http://www.w3.org/2000/svg">
<title id="t-rf">Electrolytic refining of copper</title>
<defs><marker id="mn-ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#1d4ed8"/></marker></defs>
<!-- wires and battery -->
<g fill="none" stroke="#b91c1c" stroke-width="2.2" stroke-linejoin="round"><path d="M232 112 V50 H292"/><path d="M328 50 H398 V112"/></g>
<line x1="296" y1="34" x2="296" y2="66" stroke="#1f2937" stroke-width="2.5"/>
<line x1="308" y1="42" x2="308" y2="58" stroke="#1f2937" stroke-width="5"/>
<line x1="292" y1="50" x2="296" y2="50" stroke="#b91c1c" stroke-width="2.2"/><line x1="308" y1="50" x2="328" y2="50" stroke="#b91c1c" stroke-width="2.2"/>
<!-- tank -->
<path d="M150 120 V296 Q150 304 158 304 H462 Q470 304 470 296 V120" fill="none" stroke="#3a4a63" stroke-width="2.8"/>
<rect x="152" y="150" width="316" height="152" fill="#bfdbfe"/>
<line x1="152" y1="150" x2="468" y2="150" stroke="#2563eb" stroke-width="1.5"/>
<!-- anode: thick impure block -->
<rect x="212" y="112" width="40" height="150" rx="2" fill="#b45309" stroke="#78350f" stroke-width="1.5"/>
<g fill="#78350f" opacity=".55"><circle cx="222" cy="170" r="2.5"/><circle cx="238" cy="196" r="2"/><circle cx="226" cy="228" r="2.5"/><circle cx="242" cy="244" r="2"/></g>
<!-- anode mud -->
<path d="M196 302 Q210 284 232 286 Q256 284 270 302Z" fill="#57534e"/>
<!-- cathode: thin pure strip -->
<rect x="394" y="112" width="9" height="150" fill="#ea8a4f" stroke="#9a3412" stroke-width="1.2"/>
<!-- ion movement -->
<g font-family="Inter,Segoe UI,sans-serif" font-size="12" fill="#1d4ed8" font-weight="700">
<line x1="264" y1="190" x2="382" y2="190" stroke="#1d4ed8" stroke-width="1.6" marker-end="url(#mn-ar)"/><text x="323" y="182" text-anchor="middle">Cu²⁺</text>
<line x1="264" y1="230" x2="382" y2="230" stroke="#1d4ed8" stroke-width="1.6" marker-end="url(#mn-ar)"/><text x="323" y="222" text-anchor="middle">Cu²⁺</text>
</g>
<g font-family="Inter,Segoe UI,sans-serif" font-size="13" fill="#1f2937">
<text x="302" y="24" text-anchor="middle">Battery</text>
<text x="222" y="44" font-weight="700" font-size="16">+</text><text x="404" y="44" font-weight="700" font-size="16">−</text>
<line x1="132" y1="132" x2="212" y2="140" stroke="#6b7280"/><text x="16" y="120" font-weight="700">Anode</text><text x="16" y="136">(impure copper)</text>
<line x1="490" y1="132" x2="403" y2="140" stroke="#6b7280"/><text x="494" y="120" font-weight="700">Cathode</text><text x="494" y="136">(pure copper)</text>
<line x1="490" y1="212" x2="460" y2="212" stroke="#6b7280"/><text x="494" y="208">Acidified copper</text><text x="494" y="224">sulphate solution</text>
<line x1="104" y1="290" x2="214" y2="296" stroke="#6b7280"/><text x="16" y="286">Anode mud</text><text x="16" y="302">(impurities)</text>
<text x="310" y="326" text-anchor="middle">Electrolytic tank</text>
</g>
</svg>
"""),
("rusting", "Investigating the conditions for rusting: only the nail exposed to both air and water (tube A) rusts.", """
<svg viewBox="0 0 620 360" role="img" aria-labelledby="t-ru" xmlns="http://www.w3.org/2000/svg">
<title id="t-ru">Three test tubes showing that iron rusts only in the presence of both air and water</title>
<!-- tube A -->
<path d="M110 80 V280 Q110 302 130 302 Q150 302 150 280 V80" fill="#f8fafc" stroke="#3a4a63" stroke-width="2.4"/>
<path d="M112 200 V280 Q112 300 130 300 Q148 300 148 280 V200Z" fill="#dbeafe"/>
<line x1="112" y1="200" x2="148" y2="200" stroke="#60a5fa" stroke-width="1.5"/>
<rect x="127" y="150" width="6" height="140" fill="#9a3412"/><rect x="122" y="146" width="16" height="5" rx="1" fill="#9a3412"/>
<g fill="#c2410c"><circle cx="126" cy="210" r="2"/><circle cx="134" cy="232" r="2.2"/><circle cx="126" cy="258" r="2"/><circle cx="134" cy="276" r="2"/></g>
<!-- tube B -->
<path d="M290 80 V280 Q290 302 310 302 Q330 302 330 280 V80" fill="#f8fafc" stroke="#3a4a63" stroke-width="2.4"/>
<path d="M292 186 V280 Q292 300 310 300 Q328 300 328 280 V186Z" fill="#dbeafe"/>
<rect x="292" y="172" width="36" height="14" fill="#fde68a"/>
<rect x="307" y="150" width="6" height="140" fill="#6b7280"/><rect x="302" y="146" width="16" height="5" rx="1" fill="#6b7280"/>
<rect x="286" y="66" width="48" height="22" rx="3" fill="#a16207" stroke="#713f12" stroke-width="1.5"/>
<!-- tube C -->
<path d="M470 80 V280 Q470 302 490 302 Q510 302 510 280 V80" fill="#f8fafc" stroke="#3a4a63" stroke-width="2.4"/>
<path d="M472 250 V280 Q472 300 490 300 Q508 300 508 280 V250Z" fill="#f3f4f6" stroke="#9ca3af"/>
<g fill="#d1d5db" stroke="#9ca3af" stroke-width=".8"><circle cx="480" cy="262" r="4"/><circle cx="492" cy="258" r="4"/><circle cx="502" cy="266" r="4"/><circle cx="486" cy="276" r="4"/><circle cx="498" cy="282" r="4"/><circle cx="490" cy="292" r="3.5"/></g>
<rect x="487" y="110" width="6" height="128" fill="#6b7280"/><rect x="482" y="106" width="16" height="5" rx="1" fill="#6b7280"/>
<rect x="466" y="66" width="48" height="22" rx="3" fill="#a16207" stroke="#713f12" stroke-width="1.5"/>
<g font-family="Inter,Segoe UI,sans-serif" font-size="13" fill="#1f2937">
<text x="130" y="60" text-anchor="middle">Air</text>
<line x1="72" y1="150" x2="126" y2="176" stroke="#6b7280"/><text x="16" y="134">Rusted</text><text x="16" y="150">iron nail</text>
<line x1="72" y1="238" x2="113" y2="238" stroke="#6b7280"/><text x="16" y="234">Water</text>
<line x1="346" y1="78" x2="334" y2="78" stroke="#6b7280"/><text x="350" y="82">Cork</text>
<line x1="346" y1="180" x2="328" y2="180" stroke="#6b7280"/><text x="350" y="176">Layer of</text><text x="350" y="192">oil</text>
<line x1="346" y1="240" x2="328" y2="240" stroke="#6b7280"/><text x="350" y="236">Boiled distilled</text><text x="350" y="252">water</text>
<line x1="526" y1="78" x2="514" y2="78" stroke="#6b7280"/><text x="530" y="82">Cork</text>
<line x1="526" y1="160" x2="493" y2="160" stroke="#6b7280"/><text x="530" y="156">Iron nail</text><text x="530" y="172">in dry air</text>
<line x1="526" y1="270" x2="508" y2="270" stroke="#6b7280"/><text x="530" y="250">Anhydrous</text><text x="530" y="266">calcium</text><text x="530" y="282">chloride</text>
<text x="130" y="326" text-anchor="middle" font-weight="700">A: air + water</text>
<text x="130" y="344" text-anchor="middle" fill="#b91c1c">Rusts</text>
<text x="310" y="326" text-anchor="middle" font-weight="700">B: water, no air</text>
<text x="310" y="344" text-anchor="middle" fill="#15803d">No rust</text>
<text x="490" y="326" text-anchor="middle" font-weight="700">C: air, no water</text>
<text x="490" y="344" text-anchor="middle" fill="#15803d">No rust</text>
</g>
</svg>
"""),
("extraction-steps", "Steps in the extraction of metals from their ores according to their position in the reactivity series.", """
<svg viewBox="0 0 660 430" role="img" aria-labelledby="t-ex" xmlns="http://www.w3.org/2000/svg">
<title id="t-ex">Flow chart of steps involved in the extraction of metals of high, medium and low reactivity</title>
<defs><marker id="mn-fa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#475569"/></marker></defs>
<g fill="none" stroke="#475569" stroke-width="1.6" marker-end="url(#mn-fa)">
<path d="M330 48 V66"/>
<path d="M330 100 V114 H110 V128"/><path d="M330 114 V128"/><path d="M330 114 H550 V128"/>
<path d="M110 172 V246"/>
<path d="M330 172 V186 H270 V198"/><path d="M330 186 H410 V198"/>
<path d="M550 172 V198"/>
<path d="M270 232 V246 H330 V258"/>
<path d="M330 290 V304"/>
<path d="M550 232 V304"/>
<path d="M110 280 V384 H232"/>
<path d="M330 336 V362"/><path d="M550 336 V384 H428"/>
</g>
<path d="M410 232 V246 H330" fill="none" stroke="#475569" stroke-width="1.6"/>
<g stroke-width="1.4">
<rect x="250" y="16" width="160" height="32" rx="6" fill="#f1f5f9" stroke="#475569"/>
<rect x="210" y="68" width="240" height="32" rx="6" fill="#f1f5f9" stroke="#475569"/>
<rect x="30" y="130" width="160" height="42" rx="6" fill="#fee2e2" stroke="#b91c1c"/>
<rect x="250" y="130" width="160" height="42" rx="6" fill="#fef3c7" stroke="#b45309"/>
<rect x="470" y="130" width="160" height="42" rx="6" fill="#dcfce7" stroke="#15803d"/>
<rect x="206" y="200" width="128" height="32" rx="6" fill="#fff" stroke="#475569"/>
<rect x="346" y="200" width="128" height="32" rx="6" fill="#fff" stroke="#475569"/>
<rect x="490" y="200" width="120" height="32" rx="6" fill="#fff" stroke="#475569"/>
<rect x="30" y="248" width="160" height="32" rx="6" fill="#fff" stroke="#475569"/>
<rect x="214" y="260" width="232" height="30" rx="6" fill="#fff" stroke="#475569"/>
<rect x="250" y="306" width="160" height="30" rx="6" fill="#fff" stroke="#475569"/>
<rect x="490" y="306" width="120" height="30" rx="6" fill="#fff" stroke="#475569"/>
<rect x="234" y="364" width="192" height="40" rx="6" fill="#e0e7ff" stroke="#4338ca"/>
</g>
<g font-family="Inter,Segoe UI,sans-serif" font-size="13" fill="#1f2937" text-anchor="middle">
<text x="330" y="37" font-weight="700">Ore</text>
<text x="330" y="89">Concentration of ore</text>
<text x="110" y="148" font-weight="700">High reactivity</text><text x="110" y="164" font-size="12">K, Na, Ca, Mg, Al</text>
<text x="330" y="148" font-weight="700">Medium reactivity</text><text x="330" y="164" font-size="12">Zn, Fe, Pb, etc.</text>
<text x="550" y="148" font-weight="700">Low reactivity</text><text x="550" y="164" font-size="12">Cu, Hg, etc.</text>
<text x="270" y="221">Carbonate ore</text><text x="410" y="221">Sulphide ore</text>
<text x="550" y="221">Sulphide ore</text>
<text x="110" y="264" font-size="12">Electrolysis of</text><text x="110" y="277" font-size="12">molten ore</text>
<text x="330" y="280" font-size="12">Calcination / Roasting → oxide</text>
<text x="330" y="326" font-size="12">Reduction to metal</text>
<text x="550" y="326" font-size="12">Roasting → metal</text>
<text x="330" y="380" font-weight="700">Purification (refining)</text><text x="330" y="396" font-size="12">→ pure metal</text>
</g>
</svg>
"""),
],
"formulas": [
("Metal + oxygen", "Metal + O₂ → Metal oxide (basic)", "2Cu + O₂ → 2CuO; 4Al + 3O₂ → 2Al₂O₃"),
("Amphoteric oxide", "Reacts with both acid and base → salt + water", "Al₂O₃ + 6HCl → 2AlCl₃ + 3H₂O; Al₂O₃ + 2NaOH → 2NaAlO₂ + H₂O"),
("Soluble metal oxide + water", "Metal oxide + H₂O → Alkali", "Na₂O + H₂O → 2NaOH; K₂O + H₂O → 2KOH"),
("Metal + cold water", "Metal + H₂O → Metal hydroxide + H₂", "2Na + 2H₂O → 2NaOH + H₂; Ca + 2H₂O → Ca(OH)₂ + H₂"),
("Metal + steam", "Metal + H₂O(g) → Metal oxide + H₂", "2Al + 3H₂O → Al₂O₃ + 3H₂; 3Fe + 4H₂O → Fe₃O₄ + 4H₂"),
("Metal + dilute acid", "Metal + Acid → Salt + H₂ (metals above H)", "Fe + 2HCl → FeCl₂ + H₂"),
("Displacement", "More reactive metal displaces less reactive one", "Fe + CuSO₄ → FeSO₄ + Cu"),
("Reactivity series", "Decreasing reactivity", "K > Na > Ca > Mg > Al > Zn > Fe > Pb > H > Cu > Hg > Ag > Au"),
("Ionic bond", "Metal loses e⁻, non-metal gains e⁻", "Na → Na⁺ + e⁻; Cl + e⁻ → Cl⁻; Mg → Mg²⁺ + 2e⁻"),
("Aqua regia", "Conc. HCl : conc. HNO₃ = 3 : 1", "Dissolves gold and platinum"),
("Roasting", "Sulphide ore heated in excess air", "2ZnS + 3O₂ → 2ZnO + 2SO₂"),
("Calcination", "Carbonate ore heated in limited air", "ZnCO₃ → ZnO + CO₂"),
("Reduction by carbon", "Metal oxide + C → Metal + CO", "ZnO + C → Zn + CO"),
("Thermit reaction", "Metal oxide + Al → Metal + Al₂O₃ + heat", "Fe₂O₃ + 2Al → 2Fe + Al₂O₃ + heat"),
("Self-reduction (low reactivity)", "Heating sulphide ore in air", "2HgS + 3O₂ → 2HgO + 2SO₂; 2HgO → 2Hg + O₂; 2Cu₂O + Cu₂S → 6Cu + SO₂"),
("Electrolytic reduction", "Molten chloride electrolysed", "Cathode: Na⁺ + e⁻ → Na; Anode: 2Cl⁻ → Cl₂ + 2e⁻"),
("Carat of gold", "Purity = carat ÷ 24 × 100%", "22 carat = 22/24 × 100 ≈ 91.7% gold"),
],
"worked": [
("An element X forms an oxide X₂O₃ that reacts with both dilute HCl and NaOH solution to give salt and water. (a) What type of oxide is it? (b) Identify X. (c) Write balanced equations for both reactions. (3 marks)", """
<ol>
<li>An oxide that reacts with both acids and bases to give salt and water is an <b>amphoteric oxide</b>.</li>
<li>A metal with oxide formula X₂O₃ that is amphoteric is <b>aluminium</b> (Al₂O₃).</li>
<li>With acid: <b>Al₂O₃ + 6HCl → 2AlCl₃ + 3H₂O</b> — check: Al 2 = 2, O 3 = 3, H 6 = 6, Cl 6 = 6.</li>
<li>With base: <b>Al₂O₃ + 2NaOH → 2NaAlO₂ + H₂O</b> — check: Al 2 = 2, Na 2 = 2, O 5 = 5 (3 + 2 on the left, 4 + 1 on the right), H 2 = 2.</li>
</ol>
"""),
("Why is sodium kept immersed in kerosene oil? Why does calcium float when it reacts with water? (2 marks)", """
<p class="ans">Sodium is so reactive that it catches fire when kept in open air, reacting vigorously with oxygen and moisture; kerosene keeps air and water away from it. Calcium floats because bubbles of hydrogen gas formed in the reaction (Ca + 2H₂O → Ca(OH)₂ + H₂) stick to its surface and make it buoyant.</p>
"""),
("Four metals W, X, Y and Z were tested with salt solutions. W displaces copper from CuSO₄ solution but does not react with FeSO₄. X displaces iron from FeSO₄ but does not react with ZnSO₄. Y displaces silver from AgNO₃ but does not react with CuSO₄. Z does not react with any of these solutions, including AgNO₃. (a) Arrange W, X, Y, Z in decreasing order of reactivity. (b) What would you observe if X is added to copper sulphate solution? (3 marks)", """
<ol>
<li>A metal displaces only metals that are <b>below</b> it in the reactivity series.</li>
<li>X displaces Fe but not Zn → X lies <b>between Zn and Fe</b>. W displaces Cu but not Fe → W lies <b>between Fe and Cu</b>.</li>
<li>Y displaces Ag but not Cu → Y lies <b>between Cu and Ag</b>. Z cannot even displace silver → Z is <b>below Ag</b>.</li>
<li>(b) X is more reactive than iron, and hence than copper, so it displaces copper: the <b>blue colour of the solution fades</b> and a <b>reddish-brown deposit of copper</b> forms on X.</li>
</ol>
<p class="ans">(a) Decreasing reactivity: <b>X &gt; W &gt; Y &gt; Z</b>.</p>
"""),
("Show the formation of Na₂O and MgO by the transfer of electrons. Name the ions present. (Atomic numbers: Na 11, O 8, Mg 12) (3 marks)", """
<ol>
<li>Electronic configurations: Na 2, 8, 1; O 2, 6; Mg 2, 8, 2.</li>
<li><b>Na₂O:</b> each of two sodium atoms loses one electron and oxygen gains both: 2Na → 2Na⁺ + 2e⁻; O + 2e⁻ → O²⁻. Two Na⁺ (2, 8) and one O²⁻ (2, 8) attract each other → Na₂O.</li>
<li><b>MgO:</b> magnesium loses two electrons to one oxygen atom: Mg → Mg²⁺ + 2e⁻; O + 2e⁻ → O²⁻ → Mg²⁺O²⁻.</li>
<li>Ions: sodium ion Na⁺, oxide ion O²⁻, magnesium ion Mg²⁺. In electron-dot form, draw the metal electrons as crosses moving to the oxygen atom, which ends with an octet.</li>
</ol>
"""),
("Why do ionic compounds have high melting points? Why do they conduct electricity in the molten state but not in the solid state? (2 marks)", """
<p class="ans">There is a strong electrostatic force of attraction between the oppositely charged ions, so a large amount of energy is needed to break it — hence high melting points. In the solid state the ions are held in fixed positions and cannot move; in the molten state (or in solution) the ions become free to move towards the electrodes and carry current.</p>
"""),
("A metal M is found in nature as its sulphide ore MS. It is in the middle of the reactivity series. Describe the steps to extract M with equations. Why is the sulphide converted to an oxide? Name the method used to purify the metal and draw its labelled diagram for copper. (5 marks)", """
<ol>
<li>A middle-series metal with a sulphide ore, e.g. <b>zinc (ZnS, zinc blende)</b>. First the ore is concentrated to remove gangue.</li>
<li><b>Roasting</b> — heat strongly in excess air: <b>2ZnS + 3O₂ → 2ZnO + 2SO₂</b>.</li>
<li><b>Reduction</b> — heat the oxide with carbon (coke): <b>ZnO + C → Zn + CO</b>.</li>
<li>The sulphide is converted to the oxide because it is <b>easier to obtain a metal from its oxide</b> than from its sulphide or carbonate.</li>
<li><b>Electrolytic refining:</b> impure metal as the anode, a thin strip of pure metal as the cathode, and a solution of a soluble salt of the metal as electrolyte. For copper: anode = impure copper, cathode = pure copper, electrolyte = acidified CuSO₄. Pure copper deposits on the cathode; insoluble impurities collect below the anode as anode mud (see the diagram above).</li>
</ol>
"""),
("Three test tubes A, B and C contain iron nails: A in tap water open to air, B in boiled distilled water covered with oil, C with anhydrous calcium chloride and corked. In which tube does the nail rust? Give reasons for each, and state two methods of preventing rusting. (3 marks)", """
<ol>
<li><b>A</b> — the nail rusts, because both air (oxygen) and water are present.</li>
<li><b>B</b> — no rust: boiling removes dissolved air and the oil layer stops air from dissolving again, so only water is present.</li>
<li><b>C</b> — no rust: anhydrous CaCl₂ absorbs moisture, so only dry air is present.</li>
<li>Prevention: painting/oiling/greasing, and <b>galvanising</b> (coating with zinc). Others: chrome plating, alloying.</li>
</ol>
"""),
("A goldsmith says the bangle is made of 22-carat gold. (a) What percentage of the bangle is gold? (b) Why is 24-carat gold not used for jewellery? (c) Name the other metals usually alloyed with it. (2 marks)", """
<ol>
<li>(a) Pure gold is 24 carat, so 22-carat gold = 22/24 × 100 = <b>91.67% gold</b> (about 91.7%).</li>
<li>(b) 24-carat (pure) gold is very <b>soft</b>, so ornaments would bend and lose shape easily.</li>
<li>(c) The remaining 2 parts are <b>silver or copper</b>, which make the alloy harder.</li>
</ol>
"""),
],
"mistakes": [
("Wrong product with steam", "“3Fe + 4H₂O → 3Fe(OH)₂ + H₂” or “Fe + H₂O → FeO + H₂”.", "With steam, metals give the oxide: 3Fe + 4H₂O → Fe₃O₄ + 4H₂; 2Al + 3H₂O → Al₂O₃ + 3H₂."),
("Hydrogen from nitric acid", "“Zn + 2HNO₃ → Zn(NO₃)₂ + H₂.”", "HNO₃ is an oxidising agent and oxidises H₂ to water; only Mg and Mn give H₂ with very dilute HNO₃."),
("Roasting vs calcination", "“Calcination is heating a sulphide ore in air.”", "Roasting: sulphide ore, excess air. Calcination: carbonate ore, limited air."),
("Electrodes in refining", "“Pure copper is the anode and impure copper the cathode.”", "Impure copper = anode (thick block); pure copper = cathode (thin strip)."),
("Ionic compounds conduct as solids", "“NaCl conducts electricity because it has ions.”", "Ions in solid NaCl cannot move; it conducts only when molten or dissolved in water."),
("Displacement direction", "“Cu + FeSO₄ → CuSO₄ + Fe.”", "Copper is less reactive than iron, so no reaction. Only Fe + CuSO₄ → FeSO₄ + Cu occurs."),
("Rusting needs only water", "“Iron rusts in water.”", "Rusting needs both air (oxygen) and water/moisture together."),
],
"revision": [
"Metals: lustrous, hard, malleable, ductile, sonorous, good conductors. Gold most malleable/ductile; Ag and Cu best conductors.",
"Exceptions: Hg liquid; Na, K soft, low density; Ga, Cs melt on palm; Pb, Hg poor heat conductors.",
"Non-metals: brittle, dull, poor conductors; bromine is liquid; iodine is lustrous; graphite conducts; diamond hardest.",
"Metal oxides are basic, non-metal oxides acidic; Al₂O₃ and ZnO are amphoteric.",
"Na and K stored in kerosene; Mg, Al, Zn, Pb have protective oxide layers; anodising thickens the Al₂O₃ layer.",
"Cold water: K, Na (violent, H₂ catches fire), Ca (floats); hot water: Mg; steam: Al, Zn, Fe (give oxides); no reaction: Pb, Cu, Ag, Au.",
"Metal + dilute acid → salt + H₂ (Mg > Al > Zn > Fe; Cu none). HNO₃ gives no H₂ except with Mg, Mn (very dilute).",
"Aqua regia = conc. HCl : conc. HNO₃ = 3 : 1; dissolves gold and platinum.",
"Reactivity: K Na Ca Mg Al Zn Fe Pb [H] Cu Hg Ag Au. Fe + CuSO₄ → FeSO₄ + Cu.",
"Ionic compounds: metal loses e⁻, non-metal gains e⁻; hard, brittle, high m.p., water-soluble, conduct only when molten/dissolved.",
"Ore = mineral from which metal is extracted profitably; gangue = impurities removed first.",
"Low reactivity: heat alone (HgS → HgO → Hg; Cu₂S → Cu). Medium: roast (sulphide) or calcine (carbonate) → oxide → reduce with C.",
"Thermit: Fe₂O₃ + 2Al → 2Fe + Al₂O₃ + heat — joins railway tracks.",
"High reactivity (K–Al): electrolysis of molten chloride/oxide; metal at cathode.",
"Electrolytic refining of Cu: impure anode, pure cathode, acidified CuSO₄, anode mud below anode.",
"Rusting needs air + water. Prevent: paint, oil, grease, galvanise (Zn), chrome-plate, anodise, alloy. Brass Cu+Zn, bronze Cu+Sn, solder Pb+Sn, 22-carat gold.",
],
"practice": [
("cbse-class-10-science-mock-tests.html", "Class 10 Science mock tests"),
("virtual-labs/chemistry/04-metals-with-acids.html", "Metals with acids virtual lab"),
("virtual-labs/chemistry/05-metals-with-water.html", "Metals with water virtual lab"),
("virtual-labs/chemistry/06-displacement-reactions.html", "Displacement reactions lab"),
("virtual-labs/chemistry/29-ionic-bond-formation.html", "Ionic bond formation explorer"),
("formula-board/", "Formula Board revision cards"),
],
}
