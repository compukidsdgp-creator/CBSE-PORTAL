"""Batch 03 — Class 10 Science: one more paper's worth (plus spares). Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("science10")
LP, CC, RP, HE, EN = "Life Processes", "Control and Coordination", "How do Organisms Reproduce?", "Heredity", "Our Environment"
CR, AB, MN, CA = "Chemical Reactions and Equations", "Acids, Bases and Salts", "Metals and Non-metals", "Carbon and its Compounds"
LI, HU, EL, MG = "Light - Reflection and Refraction", "The Human Eye and the Colourful World", "Electricity", "Magnetic Effects of Electric Current"

# ───────────────────────── SECTION A — BIOLOGY ─────────────────────────
b.m("A", HE, "A pea plant that is heterozygous for tallness (Tt) is crossed with a dwarf pea plant (tt). The ratio of tall to dwarf plants among the offspring will be:", "3 : 1", "1 : 1", "1 : 2 : 1", "all tall", "B")
b.m("A", HE, "Which of the following characters of the pea plant was NOT among those studied by Mendel?", "Shape of the seed", "Colour of the flower", "Shape of the leaf", "Height of the stem", "C")
b.m("A", EN, "In the food chain grass → grasshopper → frog → snake → eagle, the frog is a:", "producer", "primary consumer", "tertiary consumer", "secondary consumer", "D")
b.m("A", EN, "Which of the following groups contains only biodegradable materials?", "Grass clippings, paper and cotton cloth", "Plastic bottle, glass and paper", "Polythene bag, fruit peels and wood", "Aluminium foil, cotton and DDT", "A")
b.m("A", RP, "After fertilisation in a flower, the fruit develops from the:", "ovary", "ovule", "style", "petal", "A")
b.m("A", RP, "Which of the following organisms reproduces by forming spores in sporangia?", "Hydra", "Planaria", "Leishmania", "Rhizopus", "D")
b.m("A", CC, "Growth hormone in the human body is secreted by the:", "thyroid gland", "adrenal gland", "pituitary gland", "pancreas", "C")
b.m("A", LP, "Which of the following organisms breaks down food material outside its body and then absorbs it?", "Amoeba", "Bread mould", "Cuscuta", "Grasshopper", "B")

b.ar("A", RP, "In human males, the testes are located outside the abdominal cavity in the scrotum.", "The formation of sperms requires a temperature lower than the normal body temperature.", "A")
b.ar("A", EN, "The flow of energy in an ecosystem is unidirectional.", "Only about 1% of the energy available at one trophic level is passed on to the next trophic level.", "C")
b.ar("A", LP, "The kidneys are the main excretory organs in human beings.", "Urine is stored in the urinary bladder until it is passed out.", "B")

b.q("VSA", "A", HE, "What is a gene? Explain, taking the example of plant height, how a gene controls a characteristic.")
b.q("VSA", "A", EN, "What is a trophic level? Why do food chains usually have only three or four trophic levels?")
b.q("VSA", "A", RP, "Name the male and the female reproductive parts of a bisexual flower. How is cross-pollination different from self-pollination?")
b.q("VSA", "A", CC, "What are tropic movements? Give one example each of positive phototropism and negative geotropism.")

b.q("SA", "A", LP, "(a) What is translocation in plants? Which tissue carries it out?\n(b) Explain how water and minerals reach the top of a tall tree. What is the role of transpiration in this process?")
b.q("SA", "A", RP, "(a) Describe the process of budding in Hydra.\n(b) Why can complex multicellular organisms not reproduce by simple cell division, as unicellular organisms do?\n(c) Name one organism that reproduces by fragmentation.")
b.q("SA", "A", HE, "(a) Explain, with the help of a flow chart, how the sex of a child is determined in human beings.\n(b) Why is it wrong to say that the mother is responsible for the sex of her child?")

b.q("CBQ", "A", HE, "Ravi crossed a pure-breeding pea plant with violet flowers with a pure-breeding pea plant with white flowers. All the plants of the F₁ generation had violet flowers. He then allowed the F₁ plants to self-pollinate and raised 400 plants in the F₂ generation. Of these, 300 plants had violet flowers and 100 had white flowers.\n(a) Which flower colour is dominant? Give a reason.\n(b) Using V for the dominant allele and v for the recessive allele, write the genotype of the F₁ plants.\n(c) How many of the 300 violet-flowered F₂ plants are expected to be pure-breeding? Explain.\nOR\n(c) Write the genotypic ratio of the F₂ generation and name the genotypes.")

b.q("LA", "A", LP, "(a) What is respiration? Write two differences between aerobic and anaerobic respiration.\n(b) Show, with the help of a flow chart, the breakdown of glucose by different pathways in (i) yeast, (ii) our muscle cells during vigorous exercise and (iii) the mitochondria.\n(c) Why do we sometimes get muscle cramps after running fast?\nOR\n(a) Write the balanced chemical equation for photosynthesis and list the three events that occur during this process.\n(b) How do desert plants carry out gas exchange without losing too much water?\n(c) Describe an experiment to show that chlorophyll is necessary for photosynthesis.")

# ───────────────────────── SECTION B — CHEMISTRY ─────────────────────────
b.m("B", CR, "Which of the following is a double displacement reaction?", "2Mg + O₂ → 2MgO", "CaCO₃ → CaO + CO₂", "AgNO₃ + NaCl → AgCl + NaNO₃", "Zn + CuSO₄ → ZnSO₄ + Cu", "C")
b.m("B", CR, "In the balanced equation a Fe + b H₂O → c Fe₃O₄ + d H₂, the values of a, b, c and d are respectively:", "3, 4, 1, 4", "2, 3, 1, 3", "3, 4, 1, 3", "1, 4, 1, 4", "A")
b.m("B", AB, "When dilute hydrochloric acid is added to sodium carbonate, a gas is given off that turns lime water milky. The gas is:", "hydrogen", "carbon dioxide", "chlorine", "oxygen", "B")
b.m("B", AB, "An aqueous solution of which of the following salts is basic?", "NaCl", "NH₄Cl", "K₂SO₄", "Na₂CO₃", "D")
b.m("B", MN, "Which of the following non-metals is a good conductor of electricity?", "Sulphur", "Graphite", "Phosphorus", "Iodine", "B")
b.m("B", MN, "An element X forms an oxide X₂O. A solution of this oxide in water turns red litmus blue. The element X is most likely:", "sulphur", "carbon", "phosphorus", "sodium", "D")
b.m("B", CA, "The IUPAC name of the compound CH₃CH₂CHO is:", "propanol", "propanone", "propanal", "propanoic acid", "C")
b.m("B", CA, "Which of the following pairs of compounds belongs to the same homologous series?", "CH₄ and C₂H₆", "C₃H₆ and C₃H₈", "C₂H₄ and C₃H₈", "C₂H₆ and C₂H₄", "A")

b.ar("B", CR, "Iron gates and grills are painted to protect them from rusting.", "A coat of paint prevents moist air from coming in contact with the surface of iron.", "A")
b.ar("B", CA, "Ethanoic acid is a strong acid.", "Ethanoic acid turns blue litmus red.", "D")
b.ar("B", AB, "Baking powder is used to make cakes soft and spongy.", "Sodium hydrogencarbonate is also used in soda-acid fire extinguishers.", "B")

b.q("VSA", "B", CR, "Why should a magnesium ribbon be cleaned with sandpaper before burning it in air? Write the balanced chemical equation for the burning of magnesium.")
b.q("VSA", "B", MN, "What is an alloy? Why is pure gold not used for making jewellery? What is meant by 22-carat gold?")

b.q("SA", "B", MN, "Metals differ in how they react with water.\n(a) Name one metal that reacts with cold water and write the balanced equation for the reaction.\n(b) Name one metal that does not react with cold or hot water but reacts with steam. Write the equation.\n(c) Why does calcium start floating when it reacts with water?")
b.q("SA", "B", AB, "(a) How is washing soda obtained from baking soda? Write the chemical equations involved.\n(b) What is meant by water of crystallisation? Write the formula of washing soda and of gypsum.\n(c) State one use of washing soda.")
b.q("SA", "B", CR, "What is a decomposition reaction? Write one balanced chemical equation each for a decomposition reaction brought about by (a) heat, (b) electricity and (c) light.")

b.q("CBQ", "B", AB, "While playing in the garden, Nisha was stung by a red ant and felt a sharp burning pain. Her mother quickly rubbed a paste of baking soda on the spot and the pain soon reduced. The same evening, her grandfather complained of a burning feeling in his chest after a heavy meal and took a spoonful of an antacid. Her mother explained that both remedies work on the same principle.\n(a) Name the acid present in the sting of the ant.\n(b) Why did the baking soda paste give relief? Name the type of reaction involved.\n(c) Why does a person get a burning feeling in the stomach after overeating? Name one substance commonly used as an antacid.\nOR\n(c) Why are we advised to brush our teeth after eating sweets? How does toothpaste help to prevent tooth decay?")

b.q("LA", "B", CR, "(a) Why should a chemical equation always be balanced?\n(b) Write the balanced chemical equations for the following and state the type of each reaction:\n(i) Aluminium reacts with copper chloride to give aluminium chloride and copper.\n(ii) Zinc carbonate on heating gives zinc oxide and carbon dioxide.\n(iii) Hydrogen combines with chlorine to form hydrogen chloride.\n(c) In the reaction ZnO + C → Zn + CO, identify the substance that is oxidised and the substance that is reduced.\nOR\n(a) What is rancidity? State two methods used to prevent it.\n(b) What is corrosion? Name the conditions required for the rusting of iron and describe an activity to show that both are needed.\n(c) What is the black coating formed on silver articles left in air? Name the substance responsible for it.")

# ───────────────────────── SECTION C — PHYSICS ─────────────────────────
b.m("C", LI, "An object is placed 15 cm in front of a convex lens of focal length 10 cm. The image is formed at a distance of:", "6 cm", "15 cm", "25 cm", "30 cm", "D")
b.m("C", LI, "Light travels from air into glass of refractive index 1.5. If the speed of light in air is 3 × 10⁸ m/s, its speed in glass is:", "3 × 10⁸ m/s", "2 × 10⁸ m/s", "4.5 × 10⁸ m/s", "1.5 × 10⁸ m/s", "B")
b.m("C", EL, "The heat produced in a 20 Ω resistor when a current of 2 A flows through it for 5 s is:", "200 J", "100 J", "400 J", "800 J", "C")
b.m("C", HU, "The focal length of the human eye lens is adjusted to see near and distant objects by the:", "ciliary muscles", "pupil", "retina", "iris", "A")
b.m("C", MG, "In domestic electric circuits in India, the potential difference between the live wire and the neutral wire is:", "110 V", "50 V", "440 V", "220 V", "D")

b.ar("C", LI, "The focal length of a concave lens is taken as positive.", "A concave lens spreads out a parallel beam of light passing through it.", "D")
b.ar("C", EL, "Tungsten is used for making the filaments of electric bulbs.", "Tungsten has a very high melting point.", "A")

b.q("SA", "C", LI, "A concave lens of focal length 20 cm forms an image at a distance of 10 cm from the lens on the same side as the object. Find the distance of the object from the lens and the magnification. State the nature of the image.")
b.q("SA", "C", LI, "(a) Define the principal focus of a concave mirror.\n(b) An object is placed 10 cm in front of a concave mirror of focal length 15 cm. Find the position, nature and magnification of the image.")
b.q("SA", "C", EL, "Two resistors of 4 Ω and 12 Ω are connected in parallel, and this combination is connected in series with a 2 Ω resistor and a 6 V battery. Find (a) the equivalent resistance of the circuit, (b) the current drawn from the battery and (c) the current through the 4 Ω resistor.")
b.q("SA", "C", EL, "In a house, an electric heater of 1000 W is used for 2 hours a day and a 100 W bulb is used for 10 hours a day. Calculate (a) the electrical energy consumed in 30 days in kWh and (b) the cost of this energy at ₹6 per kWh.")
b.q("SA", "C", MG, "(a) What is meant by earthing? Why is it necessary for electrical appliances with metallic bodies?\n(b) Distinguish between overloading and short-circuiting in a domestic circuit.\n(c) What is the function of an electric fuse?")
b.q("SA", "C", HU, "A student cannot see objects clearly when they are more than 2 m away.\n(a) Name the defect of vision she is suffering from.\n(b) State two possible causes of this defect.\n(c) Find the nature and power of the lens she needs to see distant objects clearly.")

b.q("CBQ", "C", LI, "Rohan's grandmother uses a convex lens of focal length 10 cm as a magnifying glass to read the small print on medicine labels. She holds the lens 6 cm above the label and sees a large, clear image of the letters.\n(a) What is the power of the lens?\n(b) Find the position of the image formed by the lens and state its nature.\n(c) Find the magnification produced.\nOR\n(c) If she holds the lens 20 cm above the label, where will the image be formed and what will be its size compared with the letters?")

b.q("LA", "C", MG, "(a) Describe an activity to show that a current-carrying straight conductor experiences a force when it is placed in a magnetic field.\n(b) State Fleming's left-hand rule.\n(c) A proton moving horizontally from west to east enters a magnetic field that is directed vertically downwards. In which direction will the proton be deflected?\nOR\n(a) Draw the pattern of magnetic field lines due to a current-carrying circular loop.\n(b) How does the magnetic field at the centre of the loop change if (i) the current is increased and (ii) the number of turns is increased?\n(c) What is an electromagnet? State two ways in which its strength can be increased.")

b.save()
