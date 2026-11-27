"""Batch 05 — Class 10 Science: one more paper's worth (plus spares). Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("science10")
LP, CC, RP, HE, EN = "Life Processes", "Control and Coordination", "How do Organisms Reproduce?", "Heredity", "Our Environment"
CR, AB, MN, CA = "Chemical Reactions and Equations", "Acids, Bases and Salts", "Metals and Non-metals", "Carbon and its Compounds"
LI, HU, EL, MG = "Light - Reflection and Refraction", "The Human Eye and the Colourful World", "Electricity", "Magnetic Effects of Electric Current"

# ───────────────────────── SECTION A — BIOLOGY ─────────────────────────
b.m("A", HE, "Pea plants with round yellow seeds (RRYY) are crossed with plants having wrinkled green seeds (rryy). When the F₁ plants are self-pollinated, the fraction of F₂ plants with wrinkled yellow seeds is:", "9/16", "3/16", "1/16", "6/16", "B")
b.m("A", HE, "Which of the following statements about genes is correct?", "Genes are made up of proteins.", "Genes are present only in the cytoplasm of a cell.", "A gene is a section of DNA that provides the information for making a protein.", "Each body cell carries only one copy of every gene.", "C")
b.m("A", EN, "In the aquatic food chain phytoplankton → zooplankton → small fish → large fish, the highest concentration of a non-biodegradable pesticide will be found in the:", "phytoplankton", "zooplankton", "small fish", "large fish", "D")
b.m("A", EN, "The ozone layer in the upper atmosphere protects living organisms on the Earth from:", "infrared radiation", "ultraviolet radiation", "visible light", "microwaves", "B")
b.m("A", LP, "Which of the following events does NOT take place during photosynthesis?", "Absorption of light energy by chlorophyll", "Conversion of light energy into chemical energy and splitting of water molecules", "Reduction of carbon dioxide to carbohydrates", "Oxidation of glucose to carbon dioxide and water", "D")
b.m("A", CC, "The part of the human brain that controls involuntary actions such as blood pressure, salivation and vomiting is the:", "cerebrum", "cerebellum", "medulla", "hypothalamus", "C")
b.m("A", RP, "In human beings, the structure that supplies nutrition to the developing embryo from the mother's blood is the:", "placenta", "ovary", "oviduct", "cervix", "A")

b.ar("A", LP, "Guard cells control the exchange of gases through the stomata of a leaf.", "Guard cells do not contain any chloroplasts.", "C")
b.ar("A", HE, "In human beings, the sex of a child is decided by the mother.", "A woman has a perfect pair of sex chromosomes, both called X.", "D")

b.q("VSA", "A", HE, "What are sex chromosomes? How many sex chromosomes are present in (a) a body cell of a human male and (b) a human sperm cell?")
b.q("VSA", "A", EN, "What is a food web? Why is a food web more stable than a single food chain?")
b.q("VSA", "A", LP, "Name the products formed when glucose is broken down (a) in human muscle cells during vigorous exercise, when oxygen is in short supply, and (b) in the mitochondria in the presence of oxygen. Why do we sometimes get muscle cramps after running fast?")
b.q("VSA", "A", CC, "Explain how the shoot of a plant kept near a window bends towards the light. Name the plant hormone involved.")

b.q("SA", "A", HE, "In pea plants, green pod colour (G) is dominant over yellow pod colour (g). A plant that is heterozygous for pod colour is crossed with a plant having yellow pods.\n(a) Write the gametes produced by each parent.\n(b) Work out the genotypes of the offspring and state the ratio of plants with green pods to plants with yellow pods.\n(c) How can a gardener find out whether a pea plant with green pods is homozygous or heterozygous?")
b.q("SA", "A", CC, "(a) Draw a neat diagram of a neuron and label any four parts.\n(b) Describe how a nerve impulse travels from one neuron to the next.")

b.q("CBQ", "A", EN, "The eco-club of a school carried out a one-week survey of the waste thrown away in the school canteen. They found vegetable peels, leftover food, paper plates, plastic spoons, plastic water bottles, glass bottles and aluminium foil. The club then set up two separate bins and a compost pit behind the school garden.\n(a) Classify the items found into biodegradable and non-biodegradable waste.\n(b) Why is it better to use paper or leaf plates instead of plastic plates? Give one reason.\n(c) Suggest two changes in our habits that can reduce the amount of non-biodegradable waste we produce.\nOR\n(c) What happens to the biodegradable waste put into the compost pit? Which organisms bring about this change?")

b.q("LA", "A", RP, "(a) Name three different types of methods used to prevent pregnancy and explain how each of them works.\n(b) How are sexually transmitted diseases spread? Name one bacterial and one viral sexually transmitted disease.\n(c) Why is the misuse of medical tests to find out the sex of an unborn child harmful to society?")

# ───────────────────────── SECTION B — CHEMISTRY ─────────────────────────
b.m("B", CR, "Which of the following is an example of a combination reaction?", "2KClO₃ → 2KCl + 3O₂", "Zn + H₂SO₄ → ZnSO₄ + H₂", "2Mg + O₂ → 2MgO", "NaOH + HCl → NaCl + H₂O", "C")
b.m("B", CR, "In the reaction CuO + H₂ → Cu + H₂O, the substance that gets oxidised is:", "CuO", "H₂", "Cu", "H₂O", "B")
b.m("B", AB, "The chemical formula of washing soda is:", "NaHCO₃", "Na₂CO₃", "CaOCl₂", "Na₂CO₃·10H₂O", "D")
b.m("B", AB, "When zinc granules are heated with sodium hydroxide solution, the gas evolved is:", "oxygen", "hydrogen", "chlorine", "carbon dioxide", "B")
b.m("B", CA, "The hydrogenation of vegetable oils to make vegetable ghee is carried out in the presence of a catalyst such as:", "nickel", "iron", "copper", "aluminium", "A")

b.ar("B", AB, "Plaster of Paris should be stored in a moisture-proof container.", "Plaster of Paris reacts with water to form gypsum, which sets into a hard solid mass.", "A")
b.ar("B", CA, "Ethanol is used in medicines such as cough syrups and tincture of iodine.", "Ethanol burns in air with a clean blue flame.", "B")
b.ar("B", AB, "Sodium chloride is a basic salt.", "Sodium chloride is formed by the reaction of a strong acid with a strong base.", "D")

b.q("VSA", "B", CR, "What is rancidity? State two ways in which rancidity of food containing fats and oils can be prevented.")
b.q("VSA", "B", AB, "While diluting a concentrated acid, why should the acid be added slowly to water and not water to the acid? What could happen if water were added to the concentrated acid?")

b.q("SA", "B", AB, "Write balanced chemical equations for the following and describe what is observed in each case:\n(a) Dilute hydrochloric acid is added to zinc granules.\n(b) Dilute hydrochloric acid is added to sodium hydroxide solution containing a few drops of phenolphthalein.\n(c) Dilute hydrochloric acid is added to calcium carbonate, and the gas formed is passed through lime water.")
b.q("SA", "B", CR, "Balance the following chemical equations and state the type of reaction in each case:\n(a) Na + H₂O → NaOH + H₂\n(b) Zn + AgNO₃ → Zn(NO₃)₂ + Ag\n(c) CaCO₃ → CaO + CO₂ (on heating)")

b.q("CBQ", "B", AB, "Riya wanted to test some household substances without using litmus. She used turmeric powder, red cabbage juice and a few drops of phenolphthalein from the school laboratory. She also noticed that the smell of chopped onion on a cloth strip disappeared when the strip was dipped in a basic solution. She tested soap solution, lemon juice, baking soda solution and vinegar.\n(a) What colour change will be seen when turmeric is added to soap solution?\n(b) What are olfactory indicators? Name two substances that can be used as olfactory indicators.\n(c) A solution turns phenolphthalein pink. Is it acidic or basic? State whether its pH is more or less than 7.\nOR\n(c) Which two of the substances tested by Riya will turn blue litmus red? Will they change the colour of phenolphthalein?")

b.q("LA", "B", MN, "(a) Distinguish between roasting and calcination. Write one balanced chemical equation for each.\n(b) How is mercury obtained from its ore, cinnabar (HgS)? Write the chemical equations involved.\n(c) Describe the electrolytic refining of copper with the help of a labelled diagram.\nOR\n(a) Why are sulphide and carbonate ores converted into oxides before the metal is extracted from them?\n(b) Write the balanced chemical equation for the reaction of iron(III) oxide with aluminium. What is this reaction called, and where is it used?\n(c) Why are highly reactive metals such as sodium and magnesium obtained by electrolysis of their molten chlorides and not by reduction with carbon?")

# ───────────────────────── SECTION C — PHYSICS ─────────────────────────
b.m("C", LI, "When an object is placed at the centre of curvature of a concave mirror, the image formed is:", "virtual, erect and enlarged", "real, inverted and of the same size, at the centre of curvature", "real, inverted and diminished, at the focus", "virtual, erect and diminished", "B")
b.m("C", HU, "The Sun is seen about two minutes before actual sunrise and for about two minutes after actual sunset. This is due to:", "dispersion of light", "scattering of light", "atmospheric refraction", "reflection of light from clouds", "C")
b.m("C", EL, "If the potential difference across a resistor of fixed resistance is doubled, the electric power consumed by it becomes:", "two times", "half", "the same", "four times", "D")

b.ar("C", HU, "Danger signal lights are red in colour.", "Red light, having the longest wavelength in the visible spectrum, is scattered the least by fog and smoke.", "A")
b.ar("C", LI, "A concave mirror can form a virtual image of an object.", "A concave mirror always forms a magnified image.", "C")

b.q("SA", "C", LI, "An object 4 cm high is placed 15 cm in front of a concave mirror of focal length 10 cm. Using the mirror formula, find the position, nature and size of the image.")
b.q("SA", "C", LI, "(a) Define 1 dioptre of power of a lens.\n(b) A convex lens of focal length 25 cm and a concave lens of focal length 10 cm are placed in contact. Find the power and the focal length of the combination. Will the combination behave as a converging or a diverging lens?")
b.q("SA", "C", HU, "(a) What is hypermetropia? State two causes of this defect.\n(b) The near point of a hypermetropic eye is 50 cm. Find the power of the lens needed so that the person can read a book held at 25 cm. Name the type of lens.")
b.q("SA", "C", EL, "Three resistors of 5 Ω, 10 Ω and 30 Ω are connected in parallel across a 12 V battery. Calculate (a) the current through each resistor, (b) the total current drawn from the battery and (c) the equivalent resistance of the combination.")
b.q("SA", "C", MG, "(a) State the right-hand thumb rule.\n(b) Describe the pattern of the magnetic field lines due to a current-carrying circular loop.\n(c) How will the magnetic field at the centre of a circular coil change if (i) the current in it is doubled and (ii) the number of turns is made three times, the current remaining the same?")

b.q("CBQ", "C", HU, "During a school trip to the hills, students noticed that the sky was deep blue at noon, while the Sun looked reddish at sunrise. Their teacher explained that sunlight is scattered by the very small particles of air in the atmosphere, and that the amount of scattering depends on the wavelength of the light. She added that astronauts in space see the sky as dark.\n(a) Why does the clear sky appear blue?\n(b) Why does the sky appear dark to astronauts in space?\n(c) Why does the Sun appear reddish at sunrise and sunset?\nOR\n(c) What is the Tyndall effect? Give one example of it seen in daily life.")

b.q("LA", "C", LI, "(a) Draw ray diagrams to show the formation of the image by a concave mirror when the object is placed (i) between the pole and the focus and (ii) beyond the centre of curvature. State the nature of the image in each case.\n(b) An object is placed 10 cm from a convex lens of focal length 15 cm. Find the position and the magnification of the image, and state its nature.\nOR\n(a) Explain, with a ray diagram, why a pencil partly dipped in water in a glass tumbler appears bent at the surface of the water.\n(b) The refractive index of diamond is 2.42. What is the meaning of this statement?\n(c) Calculate the speed of light in a medium of refractive index 2.4. (Speed of light in vacuum = 3 × 10⁸ m/s)")

b.save()
