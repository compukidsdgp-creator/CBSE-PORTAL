"""Batch 02 — Class 10 Science: tops the pool up for one more paper. Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("science10")
LP, CC, RP, HE, EN = "Life Processes", "Control and Coordination", "How do Organisms Reproduce?", "Heredity", "Our Environment"
CR, AB, MN, CA = "Chemical Reactions and Equations", "Acids, Bases and Salts", "Metals and Non-metals", "Carbon and its Compounds"
LI, HU, EL, MG = "Light - Reflection and Refraction", "The Human Eye and the Colourful World", "Electricity", "Magnetic Effects of Electric Current"

# ───────────────────────── SECTION A — BIOLOGY ─────────────────────────
b.m("A", LP, "Which component of blood helps in the clotting of blood at the site of an injury?", "Red blood cells", "White blood cells", "Platelets", "Plasma", "C")
b.m("A", CC, "The part of the human brain that maintains the posture and balance of the body is the:", "cerebrum", "cerebellum", "medulla", "pons", "B")
b.m("A", RP, "Regeneration as a method of reproduction is seen in:", "Planaria", "Amoeba", "Rhizopus", "Yeast", "A")
b.m("A", HE, "The number of pairs of autosomes present in a human body cell is:", "1", "23", "46", "22", "D")
b.m("A", EN, "Organisms that break down the dead remains and waste products of other organisms are called:", "producers", "decomposers", "herbivores", "carnivores", "B")
b.m("A", LP, "The products of anaerobic respiration in yeast are:", "ethanol and carbon dioxide", "lactic acid and energy only", "carbon dioxide and water", "pyruvate and oxygen", "A")

b.ar("A", HE, "A child who inherits a Y chromosome is a boy.", "A child inherits one sex chromosome from each parent.", "B")
b.ar("A", LP, "Veins have valves along their length.", "Valves ensure that the blood in the veins flows only in one direction, towards the heart.", "A")

b.q("VSA", "A", CC, "What is a reflex arc? Name its components in the order in which the nerve impulse travels through them.")
b.q("VSA", "A", RP, "Why is the copying of DNA an essential part of reproduction? What is the importance of the small variations that arise during this copying?")
b.q("VSA", "A", EN, "How is ozone formed in the upper atmosphere? Write the reactions involved.")

b.q("SA", "A", LP, "(a) Explain how air is taken in and given out of the lungs during breathing in human beings.\n(b) State three features of the alveoli that make them suitable for the exchange of gases.")
b.q("SA", "A", HE, "In pea plants, round seeds (R) are dominant over wrinkled seeds (r) and yellow seeds (Y) are dominant over green seeds (y). A plant with round yellow seeds (RRYY) is crossed with a plant with wrinkled green seeds (rryy).\n(a) What will be the appearance of the seeds of the F₁ plants?\n(b) Write the ratio of the four kinds of plants obtained in the F₂ generation.\n(c) What does this cross tell us about the inheritance of two different traits?")

b.q("CBQ", "A", CC, "In some hilly regions, many people were found to have a swollen neck. Doctors found that the soil and water in these regions were poor in a particular mineral, so the food grown there also lacked it. A gland in the neck needs this mineral to make its hormone. The government then started a programme to supply salt enriched with this mineral, and the number of new cases fell sharply.\n(a) Name the gland and the mineral referred to in the passage.\n(b) Name the hormone produced by this gland and state its function.\n(c) Name the disease described here. Why is the timing and amount of hormone released by a gland so important? Explain with the example of insulin.\nOR\n(c) Name the hormone that is released into the blood when a person is frightened. State two changes that it brings about in the body.")

b.q("LA", "A", CC, "(a) Name the three main regions of the human brain and state one function of each.\n(b) How are the brain and the spinal cord protected in our body?\n(c) State two differences between a reflex action and a voluntary action.\nOR\n(a) What are plant hormones? Name one hormone that promotes growth and one that inhibits growth.\n(b) Explain, with the role of auxin, how a shoot bends towards light.\n(c) What is meant by geotropism? How do roots and shoots respond to gravity?")

# ───────────────────────── SECTION B — CHEMISTRY ─────────────────────────
b.m("B", CR, "Which of the following is a redox reaction?", "NaOH + HCl → NaCl + H₂O", "BaCl₂ + Na₂SO₄ → BaSO₄ + 2NaCl", "CuO + H₂ → Cu + H₂O", "CaO + H₂O → Ca(OH)₂", "C")
b.m("B", CA, "Which of the following is an unsaturated hydrocarbon?", "C₂H₆", "C₃H₆", "C₄H₁₀", "CH₄", "B")
b.m("B", MN, "Which of the following metals is the most reactive?", "Potassium", "Iron", "Copper", "Silver", "A")

b.ar("B", MN, "Sodium reacts violently with cold water.", "Sodium lies below hydrogen in the reactivity series.", "C")
b.ar("B", AB, "Bleaching powder gives a strong smell of chlorine when it is left open in air.", "Bleaching powder reacts slowly with the carbon dioxide of the air to release chlorine.", "A")

b.q("VSA", "B", CA, "Give reasons: (a) carbon compounds are generally poor conductors of electricity, and (b) most carbon compounds have low melting and boiling points.")

b.q("SA", "B", AB, "Three solutions X, Y and Z have pH values of 2, 7 and 13 respectively.\n(a) Which solution will react with zinc granules to release hydrogen gas? Write the equation, taking the acid to be dilute hydrochloric acid.\n(b) Which solution will turn phenolphthalein pink?\n(c) What happens when solutions X and Z are mixed? Name the type of reaction.")
b.q("SA", "B", CA, "An organic compound A with the molecular formula C₂H₆O is used in tincture of iodine and in cough syrups. On heating with alkaline potassium permanganate, A gives compound B, a dilute solution of which is used as vinegar.\n(a) Identify A and B.\n(b) Write the chemical equation for the conversion of A into B.\n(c) What happens when A and B are warmed together in the presence of an acid? Write the equation.")

b.q("CBQ", "B", CR, "Before whitewashing the walls of his house, a painter adds lumps of quicklime to a bucket of water. The mixture becomes so hot that the water starts to bubble. He lets it stand and then applies the solution to the walls. The walls look dull at first, but two or three days later they have a bright white, shiny finish.\n(a) Write the chemical equation for the reaction of quicklime with water and name the product.\n(b) Is this reaction exothermic or endothermic? What type of reaction is it?\n(c) Explain, with a chemical equation, why the walls become shiny two or three days after whitewashing.\nOR\n(c) Write the chemical formula of marble. Name the gas given out when marble reacts with dilute hydrochloric acid and write the equation.")

b.q("LA", "B", MN, "(a) What is observed when an iron nail is kept in copper sulphate solution for some time? Write the chemical equation and state what this tells us about the reactivity of iron and copper.\n(b) Show the formation of magnesium chloride by the transfer of electrons. (Atomic numbers: Mg = 12, Cl = 17)\n(c) Why are sodium and potassium obtained by electrolysis and not by reduction of their oxides with carbon?\nOR\n(a) Distinguish between roasting and calcination with one chemical equation each.\n(b) Describe the electrolytic refining of copper. Name the anode, the cathode and the electrolyte used.\n(c) What is anode mud?")

# ───────────────────────── SECTION C — PHYSICS ─────────────────────────
b.q("SA", "C", LI, "A convex mirror used as a rear-view mirror in a bus has a radius of curvature of 4 m. A car is 6 m behind the bus. Find the position, nature and magnification of the image of the car.")
b.q("SA", "C", EL, "(a) Define the resistivity of a material and write its SI unit.\n(b) A wire of length 2 m and area of cross-section 1.0 × 10⁻⁶ m² has a resistance of 0.034 Ω. Calculate the resistivity of its material.\n(c) What will be the resistance of the wire if its length is doubled, keeping the area the same?")
b.q("SA", "C", HU, "Give reasons for the following:\n(a) Stars appear to twinkle but planets do not.\n(b) Danger signal lights are red in colour.\n(c) The sky appears dark to astronauts in space.")

b.q("CBQ", "C", MG, "During a classroom demonstration, a teacher placed a magnetic compass near a straight copper wire connected to a battery through a switch. When the switch was closed, the compass needle moved from its position. When the terminals of the battery were interchanged, the needle moved in the opposite direction. The teacher then wound the wire into a circular loop and repeated the experiment, and the needle moved by a larger amount.\n(a) What does the movement of the compass needle show?\n(b) Why did the needle move in the opposite direction when the battery terminals were interchanged?\n(c) How does the magnetic field due to a straight current-carrying wire change when (i) the current is increased and (ii) the compass is moved farther from the wire?\nOR\n(c) Why does a circular coil of n turns produce a magnetic field n times as strong as that of a single turn carrying the same current?")

b.q("LA", "C", HU, "(a) Draw a labelled diagram of the human eye. State the function of the iris, the ciliary muscles and the retina.\n(b) What is meant by the power of accommodation of the eye?\n(c) The far point of a person with myopia is 80 cm. Find the nature and the power of the lens needed to correct this defect.\nOR\n(a) What is dispersion of white light? Draw a diagram to show the dispersion of white light by a glass prism.\n(b) Why do different colours of white light bend through different angles in a prism?\n(c) How did Newton show that white light is made up of seven colours and that these colours can be recombined?")

b.save()
