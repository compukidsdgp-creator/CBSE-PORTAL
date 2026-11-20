"""Batch 04 — Class 10 Science: one more paper's worth (plus spares). Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("science10")
LP, CC, RP, HE, EN = "Life Processes", "Control and Coordination", "How do Organisms Reproduce?", "Heredity", "Our Environment"
CR, AB, MN, CA = "Chemical Reactions and Equations", "Acids, Bases and Salts", "Metals and Non-metals", "Carbon and its Compounds"
LI, HU, EL, MG = "Light - Reflection and Refraction", "The Human Eye and the Colourful World", "Electricity", "Magnetic Effects of Electric Current"

# ───────────────────────── SECTION A — BIOLOGY ─────────────────────────
b.m("A", LP, "In the human body, bile juice is produced by the:", "liver", "pancreas", "gall bladder", "stomach", "A")
b.m("A", LP, "In the human lungs, the exchange of oxygen and carbon dioxide between air and blood takes place in the:", "bronchi", "trachea", "bronchioles", "alveoli", "D")
b.m("A", CC, "Which hormone is released into the blood by the adrenal glands when a person faces a sudden danger?", "Thyroxine", "Insulin", "Adrenaline", "Oestrogen", "C")
b.m("A", CC, "Which of the following plant hormones inhibits growth and causes the wilting of leaves?", "Auxin", "Gibberellin", "Cytokinin", "Abscisic acid", "D")
b.m("A", RP, "In human females, the fusion of the sperm with the egg normally takes place in the:", "uterus", "oviduct (fallopian tube)", "ovary", "vagina", "B")
b.m("A", HE, "In a sexually reproducing organism, the traits of an offspring are controlled by:", "DNA from the father only", "DNA from the mother only", "DNA from both the father and the mother", "DNA from neither parent", "C")
b.m("A", EN, "Which of the following is a human-made (artificial) ecosystem?", "A crop field", "A forest", "A lake", "An ocean", "A")

b.ar("A", LP, "Amoeba takes in food particles by forming finger-like extensions of its cell surface called pseudopodia.", "Amoeba is a multicellular organism with a well-developed digestive system.", "C")
b.ar("A", CC, "Plants can show movement in response to touch even though they have no nervous tissue.", "Plant cells can change their shape by changing the amount of water in them.", "A")

b.q("VSA", "A", LP, "State the functions of (a) hydrochloric acid and (b) mucus secreted by the gastric glands in the human stomach.")
b.q("VSA", "A", EN, "What would happen if all the decomposers were removed from an ecosystem? Give two reasons for your answer.")

b.q("SA", "A", RP, "(a) List two changes that take place in both boys and girls at the time of puberty, and one change seen only in boys.\n(b) How does a copper-T help to prevent pregnancy?\n(c) Apart from preventing pregnancy, what other benefit does the use of a condom provide?")

b.q("CBQ", "A", RP, "Meena's grandfather is a gardener. He grows new rose plants by planting pieces of stem cut from an old plant, and new sugarcane plants from stem pieces that have nodes. He grows potatoes by planting pieces of potato that have 'eyes', and his banana plants have not produced seeds for many years, so he grows new ones from their underground parts. In a nearby laboratory, scientists grow hundreds of orchid plants from a few cells taken from the tip of a single plant.\n(a) Name the method of reproduction used by the gardener for roses, sugarcane and potatoes.\n(b) State two advantages of this method of raising plants.\n(c) Why is this method the only practical way of growing plants such as banana?\nOR\n(c) Name the technique used by the scientists to grow orchid plants and state one advantage of it.")

b.q("LA", "A", EN, "(a) What is an ecosystem? Name its two main components and give two examples of each.\n(b) In a food chain, the plants fix 40,000 J of solar energy. How much of this energy will be available to the secondary consumers? State the law that you used.\n(c) Why do organisms at the highest trophic level have the largest concentration of harmful chemicals such as pesticides in their bodies?\nOR\n(a) Distinguish between biodegradable and non-biodegradable substances, giving two examples of each.\n(b) Suggest three ways in which the amount of waste produced in a school can be reduced.\n(c) What was observed about the amount of ozone in the atmosphere in the 1980s? What step was taken by UNEP in 1987 to deal with this problem?")

# ───────────────────────── SECTION B — CHEMISTRY ─────────────────────────
b.m("B", CR, "When an aqueous solution of barium chloride is mixed with an aqueous solution of sodium sulphate, the white precipitate formed is of:", "sodium chloride", "barium sulphate", "sodium sulphate", "barium chloride", "B")
b.m("B", AB, "Which of the following substances is used for disinfecting drinking water?", "Bleaching powder", "Baking soda", "Washing soda", "Plaster of Paris", "A")
b.m("B", MN, "Which of the following metals does NOT give hydrogen gas when it is added to dilute hydrochloric acid?", "Zinc", "Magnesium", "Iron", "Copper", "D")
b.m("B", CA, "Which of the following will burn in air with a yellow, sooty flame?", "Methane", "Ethane", "Ethyne", "Hydrogen", "C")
b.m("B", CA, "The molecular formula of the alkyne that contains three carbon atoms is:", "C₃H₈", "C₃H₆", "C₃H₂", "C₃H₄", "D")

b.ar("B", AB, "An aqueous solution of glucose does not conduct electricity.", "Glucose is a compound of carbon.", "B")

b.q("SA", "B", CA, "(a) Draw the electron dot structures of (i) ethene (C₂H₄) and (ii) a nitrogen molecule (N₂).\n(b) Why does carbon form covalent bonds instead of forming C⁴⁺ or C⁴⁻ ions?")

b.q("CBQ", "B", CR, "In the school laboratory, Arjun took about 2 g of light green crystals of ferrous sulphate in a dry boiling tube and heated it over a flame. He first noticed tiny droplets of water on the cooler upper part of the tube. On further heating, the crystals changed into a reddish-brown solid and a gas with the smell of burning sulphur was given off.\n(a) Where did the water droplets come from?\n(b) Write the balanced chemical equation for the change that takes place on strong heating and name the type of reaction.\n(c) Name the reddish-brown solid left in the boiling tube.\nOR\n(c) Give one example of a similar reaction that is used on a large scale in industry, with its balanced equation and one use of a product.")

b.q("LA", "B", MN, "(a) Show the formation of (i) Na₂O and (ii) MgO by the transfer of electrons. (Atomic numbers: Na = 11, O = 8, Mg = 12)\n(b) What are the ions present in these compounds?\n(c) State three general properties of ionic compounds.\nOR\n(a) A student placed strips of zinc, iron, copper and aluminium in four separate test tubes containing ferrous sulphate solution. In which test tubes will a change be seen? Arrange the four metals in decreasing order of reactivity.\n(b) What are amphoteric oxides? Write balanced equations to show the amphoteric nature of aluminium oxide.\n(c) Why is hydrogen gas usually not evolved when a metal reacts with nitric acid? Name two metals that do give hydrogen with very dilute nitric acid.")

# ───────────────────────── SECTION C — PHYSICS ─────────────────────────
b.m("C", EL, "A wire of length l and area of cross-section A has a resistance R. Another wire of the same material, of length 2l and area of cross-section 2A, will have a resistance of:", "R/2", "R", "2R", "4R", "B")
b.m("C", MG, "The strength of the magnetic field at the centre of a circular coil carrying a current can be increased by:", "decreasing the number of turns", "increasing the radius of the coil", "decreasing the current", "increasing the number of turns", "D")

b.q("SA", "C", HU, "(a) What is meant by the dispersion of white light? Why does a glass prism split white light into its colours?\n(b) Which colour of light bends the most and which bends the least on passing through a prism?\n(c) Why does the Sun appear reddish at sunrise and at sunset?")
b.q("SA", "C", EL, "Two bulbs rated 66 W, 220 V and 44 W, 220 V are connected in parallel across a 220 V supply. Calculate (a) the total current drawn from the supply, (b) the resistance of the 44 W bulb and (c) the electrical energy consumed in kWh if both bulbs are used for 10 hours.")

b.q("CBQ", "C", MG, "In a scrap yard, a crane lifts heavy pieces of iron using a large electromagnet. The electromagnet is a long coil of insulated copper wire wound around a soft iron core. When the operator switches on the current, the iron pieces stick to it; when he switches the current off, they drop.\n(a) What is a solenoid? Describe the magnetic field inside a long current-carrying solenoid.\n(b) State two differences between an electromagnet and a permanent magnet.\n(c) State two ways in which the strength of the electromagnet can be increased.\nOR\n(c) Why is soft iron, and not steel, used as the core of the electromagnet in the crane?")

b.q("LA", "C", EL, "(a) State Joule's law of heating and derive the expression H = I²Rt.\n(b) Give two practical applications of the heating effect of electric current.\n(c) An electric kettle draws a current of 5 A from a 220 V supply. Calculate the heat produced in 2 minutes.\nOR\n(a) Draw the schematic diagram of a circuit consisting of a battery of three cells of 2 V each, resistors of 5 Ω, 8 Ω and 12 Ω connected in series, an ammeter, a plug key and a voltmeter connected across the 12 Ω resistor.\n(b) Calculate the current in the circuit and the reading of the voltmeter.\n(c) Why are household appliances not connected in series?")

b.save()
