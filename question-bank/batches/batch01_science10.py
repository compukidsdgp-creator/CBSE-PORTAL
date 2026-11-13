"""Batch 01 — Class 10 Science: two papers' worth of original questions. Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("science10")
LP, CC, RP, HE, EN = "Life Processes", "Control and Coordination", "How do Organisms Reproduce?", "Heredity", "Our Environment"
CR, AB, MN, CA = "Chemical Reactions and Equations", "Acids, Bases and Salts", "Metals and Non-metals", "Carbon and its Compounds"
LI, HU, EL, MG = "Light - Reflection and Refraction", "The Human Eye and the Colourful World", "Electricity", "Magnetic Effects of Electric Current"

# ───────────────────────── SECTION A — BIOLOGY ─────────────────────────
b.m("A", LP, "The enzyme pepsin digests proteins most effectively in:",
    "the alkaline medium of the small intestine", "the acidic medium of the stomach",
    "the neutral medium of the mouth", "the alkaline medium of the large intestine", "B")
b.m("A", LP, "Oxygen-rich blood returning from the lungs first enters which chamber of the human heart?",
    "Right atrium", "Right ventricle", "Left atrium", "Left ventricle", "C")
b.m("A", LP, "The opening and closing of a stomatal pore is brought about by the change in shape of:",
    "epidermal cells", "mesophyll cells", "root hair cells", "guard cells", "D")
b.m("A", LP, "Which of the following shows the correct path of air during inhalation in humans?",
    "Nostrils → pharynx → larynx → trachea → bronchi → alveoli",
    "Nostrils → larynx → pharynx → bronchi → trachea → alveoli",
    "Nostrils → trachea → pharynx → larynx → alveoli → bronchi",
    "Nostrils → pharynx → trachea → larynx → bronchi → alveoli", "A")
b.m("A", LP, "The structural and functional unit of the human kidney, where urine is formed, is the:",
    "ureter", "nephron", "urethra", "urinary bladder", "B")
b.m("A", CC, "The tiny gap across which a nerve impulse passes from one neuron to the next is called a:",
    "dendrite", "axon", "synapse", "cell body", "C")
b.m("A", CC, "Which plant hormone mainly promotes cell division and is present in high concentration in fruits and seeds?",
    "Auxin", "Gibberellin", "Abscisic acid", "Cytokinin", "D")
b.m("A", CC, "Iodised salt is recommended in our diet because iodine is needed for the synthesis of:",
    "thyroxine", "insulin", "adrenaline", "growth hormone", "A")
b.m("A", CC, "When you accidentally touch a hot vessel, your hand is pulled back at once. The reflex arc for this action is formed in the:",
    "cerebrum", "spinal cord", "cerebellum", "medulla", "B")
b.m("A", RP, "In which of the following organisms does binary fission take place in a definite orientation in relation to its cell structures?",
    "Amoeba", "Plasmodium", "Leishmania", "Hydra", "C")
b.m("A", RP, "After fertilisation in a flowering plant, the seed develops from the:",
    "ovary", "stigma", "anther", "ovule", "D")
b.m("A", RP, "Which of the following sexually transmitted diseases is caused by bacteria?",
    "Gonorrhoea", "AIDS", "Genital warts", "Hepatitis-B", "A")
b.m("A", HE, "A pure tall pea plant (TT) is crossed with a pure dwarf pea plant (tt) and the F₁ plants are self-pollinated. The ratio of the genotypes TT : Tt : tt in the F₂ generation is:",
    "3 : 1 : 0", "1 : 2 : 1", "1 : 1 : 2", "2 : 1 : 1", "B")
b.m("A", HE, "In human beings, whether a child will be a boy or a girl is decided by:",
    "the sex chromosome present in the mother's egg", "the diet of the mother during pregnancy",
    "the sex chromosome present in the father's sperm", "the age of the parents", "C")
b.m("A", EN, "Which of the following is a correct food chain?",
    "Grasshopper → Grass → Frog → Snake", "Grass → Frog → Grasshopper → Snake",
    "Snake → Frog → Grasshopper → Grass", "Grass → Grasshopper → Frog → Snake", "D")
b.m("A", EN, "If 10,000 J of energy is available at the producer level of a food chain, the energy available to the secondary consumers will be about:",
    "100 J", "1000 J", "10 J", "5000 J", "A")

b.ar("A", LP, "Arteries have thick and elastic walls.",
     "Blood flows through the arteries under high pressure as it is pumped out of the heart.", "A")
b.ar("A", CC, "Insulin helps in regulating the level of sugar in the blood.",
     "Insulin is secreted by the thyroid gland.", "C")
b.ar("A", RP, "Plants raised by vegetative propagation are genetically similar to the parent plant.",
     "Vegetative propagation involves the fusion of male and female gametes.", "C")
b.ar("A", EN, "The use of chlorofluorocarbons (CFCs) is being reduced all over the world.",
     "A molecule of ozone is made up of three atoms of oxygen.", "B")

b.q("VSA", "A", LP, "Why is the rate of breathing in aquatic organisms much faster than that in terrestrial organisms? Give one reason.")
b.q("VSA", "A", LP, "State two differences between the transport of materials in xylem and in phloem.")
b.q("VSA", "A", CC, "Name the plant hormone responsible for (a) the elongation of the stem and (b) the wilting of leaves. State one more function of each.")
b.q("VSA", "A", RP, "What is the role of the seminal vesicles and the prostate gland in the human male reproductive system?")
b.q("VSA", "A", HE, "How did Mendel's experiments with pea plants show that a trait may be dominant or recessive? Explain with one example.")
b.q("VSA", "A", EN, "Why are substances like polythene bags called non-biodegradable? State two ways in which they harm the environment.")

b.q("SA", "A", LP, "Describe the digestion of food in the small intestine of human beings. In your answer, state the role of (a) bile juice, (b) pancreatic juice and (c) villi.")
b.q("SA", "A", CC, "How is the movement of the leaves of the 'touch-me-not' plant different from the bending of a shoot towards light? Give three points of difference.")
b.q("SA", "A", RP, "Describe the events that take place in a flower from the time a pollen grain lands on a suitable stigma until the formation of the zygote. What do the ovary and the ovule develop into after fertilisation?")
b.q("SA", "A", HE, "A plant with blue flowers (BB) is crossed with a plant with white flowers (bb).\n(a) What will be the colour of the flowers in the F₁ generation? Give a reason.\n(b) If the F₁ plants are self-pollinated, what percentage of the F₂ plants will have white flowers?\n(c) State the ratio of BB : Bb plants in the F₂ generation.")

b.q("CBQ", "A", EN, "Farmers around a village pond used a pesticide on their crops for several years. Rain water carried a part of this pesticide into the pond. A study of the pond showed that the concentration of the pesticide was 0.02 ppm in water, 5 ppm in small fish and 25 ppm in the fish-eating birds living near the pond. The pesticide could not be broken down by the organisms and so it kept collecting in their bodies.\n(a) Name the phenomenon shown by the rising concentration of the pesticide.\n(b) Why do the birds have the highest concentration of the pesticide?\n(c) Suggest two practices that farmers can adopt to reduce this problem.\nOR\n(c) Write a food chain of four trophic levels operating in this pond and name the organisms that form the third trophic level.")
b.q("CBQ", "A", LP, "The kidneys remove nitrogenous wastes such as urea from the blood. If both kidneys of a person stop working, the wastes build up in the blood and can be fatal. Such a person is treated with an artificial kidney, a process called haemodialysis. The patient's blood is passed through long tubes with a selectively permeable lining, which are dipped in a tank of dialysing fluid. The wastes pass from the blood into this fluid and the purified blood is returned to the patient.\n(a) Name the main nitrogenous waste removed by the kidneys in humans.\n(b) Why should the dialysing fluid have the same concentration of salts and glucose as normal blood?\n(c) State two differences between the working of a natural kidney and that of an artificial kidney.\nOR\n(c) Explain how the amount of water reabsorbed in the nephron changes on a hot day when a person has drunk very little water.")

b.q("LA", "A", RP, "(a) Name the parts of the human female reproductive system where (i) eggs are produced, (ii) fertilisation takes place and (iii) the embryo is implanted.\n(b) How does the embryo get its nourishment inside the mother's body?\n(c) What happens when the egg is not fertilised?\nOR\n(a) What is contraception? List three different methods of contraception and state how each one works.\n(b) Why is the use of a condom also considered important for health reasons?")
b.q("LA", "A", LP, "(a) What is meant by double circulation of blood? Why is it necessary in human beings?\n(b) Why is the wall of the left ventricle thicker than that of the right ventricle?\n(c) State two differences between arteries and veins.\nOR\n(a) List the three events that occur during photosynthesis.\n(b) How do desert plants take up carbon dioxide and still prevent the loss of water?\n(c) Describe an activity to show that sunlight is necessary for photosynthesis.")

# ───────────────────────── SECTION B — CHEMISTRY ─────────────────────────
b.m("B", CR, "The reaction Fe + CuSO₄ → FeSO₄ + Cu is an example of a:",
    "combination reaction", "displacement reaction", "decomposition reaction", "double displacement reaction", "B")
b.m("B", CR, "Which of the following is an endothermic process?",
    "Burning of natural gas", "Respiration", "Decomposition of calcium carbonate on heating", "Reaction of quicklime with water", "C")
b.m("B", CR, "When lead nitrate is heated strongly, brown fumes are seen. These fumes are of:",
    "nitrogen dioxide", "nitrogen", "oxygen", "lead oxide", "A")
b.m("B", CR, "Packets of potato chips are flushed with nitrogen gas in order to:",
    "make the chips crisp", "increase the weight of the packet", "add flavour to the chips", "prevent the oil in the chips from getting oxidised", "D")
b.m("B", AB, "A solution turns red litmus blue. Its pH is most likely to be:",
    "1", "4", "7", "10", "D")
b.m("B", AB, "The chemical formula of Plaster of Paris is:",
    "CaSO₄·2H₂O", "CaSO₄·½H₂O", "CaCO₃", "Ca(OH)₂", "B")
b.m("B", AB, "Milk of magnesia, used as an antacid, is chemically:",
    "sodium hydrogencarbonate", "calcium hydroxide", "magnesium hydroxide", "magnesium carbonate", "C")
b.m("B", AB, "Tooth enamel starts getting corroded when the pH in the mouth falls below:",
    "7.0", "5.5", "8.5", "6.5", "B")
b.m("B", MN, "Which of the following metals is kept under kerosene oil?",
    "Sodium", "Magnesium", "Aluminium", "Zinc", "A")
b.m("B", MN, "Which of the following oxides is amphoteric in nature?",
    "Na₂O", "CO₂", "Al₂O₃", "MgO", "C")
b.m("B", MN, "Ionic compounds generally have high melting points because:",
    "they are soluble in water", "strong electrostatic forces of attraction hold their ions together",
    "they conduct electricity in the solid state", "they are made up of molecules", "B")
b.m("B", MN, "Brass is an alloy of:",
    "copper and zinc", "copper and tin", "lead and tin", "iron and carbon", "A")
b.m("B", CA, "The functional group present in propanone is:",
    "aldehyde", "alcohol", "ketone", "carboxylic acid", "C")
b.m("B", CA, "The next higher homologue of C₃H₇OH is:",
    "C₂H₅OH", "C₄H₉OH", "C₃H₇CHO", "C₄H₈", "B")
b.m("B", CA, "The total number of covalent bonds present in a molecule of ethane (C₂H₆) is:",
    "5", "6", "7", "8", "C")
b.m("B", CA, "When ethanol reacts with sodium metal, the products formed are:",
    "sodium hydroxide and ethene", "sodium ethanoate and water",
    "sodium carbonate and hydrogen", "sodium ethoxide and hydrogen", "D")

b.ar("B", CR, "White silver chloride turns grey when it is kept in sunlight.",
     "Silver chloride decomposes into silver and chlorine in the presence of sunlight.", "A")
b.ar("B", AB, "Dry hydrogen chloride gas does not change the colour of dry blue litmus paper.",
     "Hydrogen chloride produces hydrogen ions only in the presence of water.", "A")
b.ar("B", MN, "Gold and platinum occur in the free state in nature.",
     "Gold and platinum are highly reactive metals.", "C")
b.ar("B", CA, "Soaps do not form lather easily with hard water.",
     "Hard water contains calcium and magnesium salts, which react with soap to form an insoluble scum.", "A")

b.q("VSA", "B", AB, "A milkman adds a very small amount of baking soda to fresh milk.\n(a) Why does he shift the pH of the fresh milk from 6 to slightly alkaline?\n(b) Why does this milk take a longer time to set as curd?")
b.q("VSA", "B", MN, "Give reasons for the following:\n(a) Ionic compounds conduct electricity in the molten state but not in the solid state.\n(b) Metals are used for making school bells.")

b.q("SA", "B", CR, "Write balanced chemical equations for the following reactions and name the type of each reaction:\n(a) Barium chloride solution is mixed with sodium sulphate solution.\n(b) Zinc granules are added to dilute sulphuric acid.\n(c) Ferrous sulphate crystals are heated strongly.")
b.q("SA", "B", AB, "(a) What is the chlor-alkali process? Write the chemical equation of the reaction involved.\n(b) Name the gas produced at the anode and the gas produced at the cathode in this process.\n(c) State one use of each of these two gases.")
b.q("SA", "B", MN, "A metal M occurs in nature as its carbonate ore, MCO₃. The metal lies in the middle of the reactivity series.\n(a) Name the two main steps used to obtain the metal from this ore.\n(b) Write the chemical equations for these steps, taking zinc as the metal.\n(c) Name the process used to refine the impure metal so obtained.")
b.q("SA", "B", CA, "(a) Distinguish between saturated and unsaturated hydrocarbons on the basis of the flame they produce on burning.\n(b) What is hydrogenation? Write a chemical equation to show it.\n(c) State one industrial application of hydrogenation.")

b.q("CBQ", "B", MN, "Three clean iron nails were kept in three test tubes for a week. Test tube P had tap water, so the nail was in contact with both air and water. Test tube Q had boiled distilled water covered with a layer of oil. Test tube R had dry air with some anhydrous calcium chloride. After a week, only the nail in test tube P had rusted. Rusting damages bridges, ships and car bodies, and a lot of money is spent every year to prevent it.\n(a) What does this experiment tell us about the conditions necessary for rusting?\n(b) Why was a layer of oil added in test tube Q?\n(c) What is galvanisation? Why does a galvanised iron article not rust even when the zinc coating is scratched?\nOR\n(c) What is an alloy? Name the metals mixed with iron to make stainless steel and state how this helps.")
b.q("CBQ", "B", CA, "Most dirt is oily in nature and oil does not dissolve in water. A soap molecule has two ends: a long hydrocarbon chain and an ionic end. When soap is added to water containing oily dirt, the soap molecules arrange themselves in clusters around the oil droplets. Rinsing then removes the dirt. In hard water, however, soap forms a sticky white solid and a lot of soap is wasted. Detergents were developed to overcome this problem.\n(a) What name is given to the cluster of soap molecules formed around an oil droplet?\n(b) Which end of the soap molecule attaches to the oil droplet and which end faces the water?\n(c) Why does soap form a sticky solid (scum) with hard water? Why do detergents not form it?\nOR\n(c) Would a micelle be formed if soap were dissolved in ethanol instead of water? Give a reason for your answer.")

b.q("LA", "B", CA, "(a) Write the chemical equation for the reaction of ethanoic acid with ethanol in the presence of an acid catalyst. Name the reaction and the product.\n(b) What is observed when ethanoic acid is added to sodium hydrogencarbonate? Write the equation.\n(c) Why is pure ethanoic acid called glacial acetic acid?\n(d) State one chemical test to distinguish ethanol from ethanoic acid.\nOR\n(a) What is a homologous series? State three characteristics of a homologous series.\n(b) Draw the structures of the two isomers of butane (C₄H₁₀).\n(c) Why does carbon form compounds mainly by covalent bonding?")
b.q("LA", "B", AB, "(a) Explain the importance of pH in (i) the digestion of food in the stomach and (ii) the growth of plants in soil.\n(b) What is baking powder? Write the equation for the change that takes place when it is heated or mixed with water, and explain how it makes a cake soft and spongy.\n(c) What is meant by water of crystallisation? Give one example of a salt that has it.\nOR\n(a) How is washing soda prepared from sodium chloride? Write the chemical equations of the steps involved.\n(b) State two uses of washing soda.\n(c) A solution of sodium carbonate is basic. Explain why.")

# ───────────────────────── SECTION C — PHYSICS ─────────────────────────
b.m("C", LI, "An object is placed 20 cm in front of a concave mirror of focal length 10 cm. The image formed is:",
    "virtual, erect and magnified", "real, inverted and of the same size as the object",
    "real, inverted and diminished", "real, inverted and magnified", "B")
b.m("C", LI, "The refractive index of water is 4/3 and that of glass is 3/2. The refractive index of glass with respect to water is:",
    "9/8", "8/9", "2", "1/2", "A")
b.m("C", LI, "A lens has a focal length of −50 cm. Its power and nature are:",
    "+2 D, convex", "+0.5 D, convex", "−2 D, concave", "−0.5 D, concave", "C")
b.m("C", HU, "The sky appears blue to an observer on the Earth because of the:",
    "reflection of sunlight by clouds", "dispersion of sunlight by water droplets",
    "refraction of sunlight by the atmosphere", "scattering of sunlight by fine particles in the atmosphere", "D")
b.m("C", HU, "A student sitting on the last bench cannot read the blackboard clearly but can read a book easily. The defect of vision and the lens needed to correct it are:",
    "myopia, concave lens", "myopia, convex lens", "hypermetropia, convex lens", "hypermetropia, concave lens", "A")
b.m("C", EL, "A wire of resistance R is stretched to double its length without any change in its volume. Its new resistance is:",
    "R/2", "R", "2R", "4R", "D")
b.m("C", EL, "Three resistors of 2 Ω, 3 Ω and 6 Ω are connected in parallel. Their equivalent resistance is:",
    "1 Ω", "11 Ω", "6 Ω", "1/11 Ω", "A")
b.m("C", EL, "One kilowatt-hour of electrical energy is equal to:",
    "3.6 × 10³ J", "3.6 × 10⁵ J", "3.6 × 10⁶ J", "3.6 × 10⁸ J", "C")
b.m("C", MG, "The magnetic field inside a long straight current-carrying solenoid is:",
    "zero", "the same at all points", "greater at the ends than at the centre", "changing from point to point", "B")
b.m("C", MG, "The direction of the magnetic field around a straight current-carrying conductor is given by:",
    "the right-hand thumb rule", "Fleming's left-hand rule", "Ohm's law", "Joule's law", "A")

b.ar("C", LI, "A convex mirror is used as a rear-view mirror in vehicles.",
     "A convex mirror always forms a virtual, erect and diminished image and gives a wider field of view.", "A")
b.ar("C", EL, "A fuse wire is made of a material that has a high melting point.",
     "A fuse wire melts and breaks the circuit when the current becomes larger than the safe limit.", "D")
b.ar("C", MG, "Two magnetic field lines never cross each other.",
     "Magnetic field lines are closed curves.", "B")

b.q("SA", "C", LI, "An object 5 cm high is placed at a distance of 30 cm from a convex lens of focal length 20 cm. Find the position, nature and size of the image formed.")
b.q("SA", "C", LI, "(a) State the two laws of refraction of light.\n(b) The refractive index of glass is 1.5. Calculate the speed of light in glass. (Speed of light in vacuum = 3 × 10⁸ m/s)")
b.q("SA", "C", LI, "A concave mirror of focal length 15 cm forms a real image that is three times the size of the object. Calculate the distance of the object from the mirror.")
b.q("SA", "C", HU, "Explain the formation of a rainbow in the sky with the help of a labelled diagram. Why is a rainbow always seen in the direction opposite to that of the Sun?")
b.q("SA", "C", HU, "(a) What is presbyopia? State its cause and how it is corrected.\n(b) Why can we see the Sun about two minutes before the actual sunrise?")
b.q("SA", "C", EL, "(a) Derive an expression for the equivalent resistance of three resistors R₁, R₂ and R₃ connected in series.\n(b) Why is an ammeter always connected in series in a circuit?")
b.q("SA", "C", EL, "An electric iron is rated 1100 W, 220 V. Calculate:\n(a) the current drawn by the iron,\n(b) the resistance of its heating element, and\n(c) the energy consumed in kWh if it is used for 2 hours.")
b.q("SA", "C", MG, "(a) Draw the pattern of magnetic field lines around a bar magnet.\n(b) State two properties of magnetic field lines.\n(c) How does a current-carrying solenoid behave like a bar magnet?")
b.q("SA", "C", MG, "(a) State Fleming's left-hand rule.\n(b) On what factors does the force on a current-carrying conductor placed in a magnetic field depend?\n(c) When is this force the largest?")

b.q("CBQ", "C", EL, "In a house, all the appliances are connected in parallel across the live and neutral wires, and each appliance has its own switch. The supply reaches the house at 220 V. The wiring has two separate circuits, one of 5 A rating for bulbs and fans and another of 15 A rating for appliances such as geysers and air coolers. A third wire, the earth wire, is connected to the metal body of appliances such as the electric iron and the refrigerator.\n(a) Why are household appliances connected in parallel and not in series? Give one reason.\n(b) What is the function of the earth wire?\n(c) What is overloading? State two ways in which it can be caused.\nOR\n(c) A geyser of 2 kW and an electric kettle of 1.5 kW are switched on together in the 15 A circuit at 220 V. Find the total current drawn and state whether the fuse will blow.")
b.q("CBQ", "C", LI, "An eye specialist tests the eyesight of two patients. For the first patient, Asha, the prescription for the lens is +2.0 D. For the second patient, Imran, the prescription is −0.5 D. The power of a lens tells us how strongly it converges or diverges light, and opticians often place lenses in contact to get the required power.\n(a) What type of lens is prescribed for Asha?\n(b) Calculate the focal length of the lens prescribed for Imran.\n(c) Define one dioptre. If lenses of power +2.0 D and −0.5 D are placed in contact, find the power and the focal length of the combination.\nOR\n(c) Draw a ray diagram to show how a convex lens corrects the defect of vision in which nearby objects cannot be seen clearly.")

b.q("LA", "C", EL, "(a) State Ohm's law. Describe the shape of the V-I graph for a metallic conductor.\n(b) List the factors on which the resistance of a conductor depends.\n(c) A 4 Ω resistor is connected in series with a parallel combination of a 6 Ω resistor and a 3 Ω resistor. The arrangement is connected to a 6 V battery. Find (i) the total resistance of the circuit, (ii) the current drawn from the battery and (iii) the current through the 6 Ω resistor.\nOR\n(a) What is the heating effect of electric current? Write the expression for the heat produced in a resistor.\n(b) Why is tungsten used for the filament of an electric bulb?\n(c) A 100 W bulb and a 60 W bulb are connected in parallel to a 220 V supply. Find the total current drawn from the supply.")
b.q("LA", "C", LI, "(a) Draw a ray diagram to show the image formed by a convex lens when the object is placed between F₁ and 2F₁. State the nature of the image.\n(b) Write the lens formula and state the sign convention used for the object distance.\n(c) An object is placed 30 cm from a concave lens of focal length 15 cm. Find the position and the magnification of the image.\nOR\n(a) Draw a ray diagram to show the image formed by a concave mirror when the object is placed between the pole and the principal focus. State the nature of the image.\n(b) Define the radius of curvature of a spherical mirror and write its relation with the focal length.\n(c) An object is placed 10 cm in front of a convex mirror of focal length 15 cm. Find the position and nature of the image.")

b.save()
