"""Batch 05 — Class 12 Chemistry: one more paper's worth (plus spares). Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("chemistry12")
SO, EL, KI, DF, CO = "Solutions", "Electrochemistry", "Chemical Kinetics", "The d- and f-Block Elements", "Coordination Compounds"
HA, AL, AK, AM, BI = "Haloalkanes and Haloarenes", "Alcohols, Phenols and Ethers", "Aldehydes, Ketones and Carboxylic Acids", "Amines", "Biomolecules"

# ── SECTION A — MCQ ──
b.m("A", SO, "Which of the following 0.1 molal aqueous solutions will have the highest freezing point?", "NaCl", "CaCl₂", "Urea", "Al₂(SO₄)₃", "C")
b.m("A", SO, "Which of the following mixtures shows a negative deviation from Raoult's law?", "Ethanol and acetone", "Chloroform and acetone", "Benzene and toluene", "Ethanol and water", "B")
b.m("A", EL, "The cell constant (G*) of a conductivity cell whose electrodes have area A and are separated by a distance l is:", "A/l", "R/κ", "κ/R", "l/A", "D")
b.m("A", EL, "If the standard emf (E°cell) of a galvanic cell is positive, then the standard Gibbs energy change (ΔG°) of the cell reaction is:", "negative", "positive", "zero", "impossible to predict", "A")
b.m("A", KI, "For the reaction 2N₂O₅ → 4NO₂ + O₂, the rate of formation of NO₂ is related to the rate of disappearance of N₂O₅ by:", "d[NO₂]/dt = −d[N₂O₅]/dt", "d[NO₂]/dt = −2 d[N₂O₅]/dt", "d[NO₂]/dt = −½ d[N₂O₅]/dt", "d[NO₂]/dt = −4 d[N₂O₅]/dt", "B")
b.m("A", KI, "The half-life of a first order reaction is 10 minutes. The time required for 75% of the reaction to be completed is:", "30 minutes", "40 minutes", "20 minutes", "15 minutes", "C")
b.m("A", DF, "On the basis of its electronic configuration, which of the following ions is expected to be colourless?", "Ti³⁺", "V³⁺", "Fe³⁺", "Cu⁺", "D")
b.m("A", DF, "The oxidation state of chromium in potassium dichromate, K₂Cr₂O₇, is:", "+6", "+3", "+7", "+4", "A")
b.m("A", DF, "The most common oxidation state shown by the lanthanoids is:", "+3", "+2", "+4", "+5", "A")
b.m("A", CO, "The number of ions produced when one formula unit of [Co(NH₃)₅Cl]Cl₂ dissolves in water is:", "2", "3", "4", "6", "B")
b.m("A", CO, "Which of the following is an ambidentate ligand?", "NO₂⁻", "NH₃", "ethane-1,2-diamine (en)", "C₂O₄²⁻", "A")
b.m("A", HA, "An alcohol is best converted into an alkyl chloride, with both the by-products escaping as gases, by using:", "PCl₅", "PCl₃", "HCl with anhydrous ZnCl₂", "SOCl₂", "D")
b.m("A", HA, "The preparation of an alkyl iodide by heating an alkyl chloride with sodium iodide in dry acetone is called the:", "Swarts reaction", "Wurtz reaction", "Finkelstein reaction", "Sandmeyer reaction", "C")
b.m("A", AL, "Which of the following compounds is the most acidic?", "Phenol", "p-Cresol", "Ethanol", "p-Nitrophenol", "D")
b.m("A", AK, "Which of the following compounds does NOT undergo aldol condensation?", "Ethanal", "Methanal", "Propanal", "Propanone", "B")
b.m("A", AK, "A carboxylic acid can be reduced directly to a primary alcohol by:", "LiAlH₄", "NaBH₄", "H₂ / Pd–BaSO₄", "Zn–Hg / concentrated HCl", "A")
b.m("A", AM, "In the Hoffmann bromamide degradation, an amide is converted into a primary amine that contains:", "the same number of carbon atoms", "one carbon atom more", "one carbon atom less", "two carbon atoms less", "C")
b.m("A", BI, "Which of the following is a non-reducing sugar?", "Glucose", "Maltose", "Lactose", "Sucrose", "D")

b.ar("A", AM, "Aniline is a weaker base than methylamine.", "In aniline, the lone pair of electrons on the nitrogen atom is delocalised over the benzene ring and is less available for protonation.", "A")
b.ar("A", DF, "Transition metals form a large number of interstitial compounds.", "Transition metals have very low melting points.", "C")
b.ar("A", AL, "Phenol undergoes electrophilic substitution reactions more readily than benzene.", "Phenol is slightly soluble in water.", "B")

# ── SECTION B — VSA ──
b.q("VSA", "B", AK, "Write the chemical equations for the following reactions:\n(a) Clemmensen reduction of propanone\n(b) Etard reaction")
b.q("VSA", "B", CO, "On the basis of crystal field theory, write the electronic configuration of a d⁴ metal ion in an octahedral field when (a) Δ₀ > P and (b) Δ₀ < P. Which of the two complexes will be high spin?")
b.q("VSA", "B", HA, "Explain why an alkyl halide reacts with KCN to form mainly an alkyl cyanide, but with AgCN it forms mainly an alkyl isocyanide.")
b.q("VSA", "B", DF, "State any two differences between the lanthanoids and the actinoids.")
b.q("VSA", "B", BI, "What is meant by the denaturation of a protein? Give one example. Which level of structure of the protein remains unaffected during denaturation?")

# ── SECTION C — SA ──
b.q("SA", "C", SO, "(a) Define the van't Hoff factor.\n(b) 5.85 g of sodium chloride is dissolved in 500 g of water. Assuming complete dissociation, calculate the freezing point of the solution. (Kf for water = 1.86 K kg mol⁻¹, molar mass of NaCl = 58.5 g mol⁻¹, freezing point of water = 273.15 K)")
b.q("SA", "C", KI, "The rate constant of a first order reaction is 1.155 × 10⁻³ s⁻¹. Calculate:\n(a) the half-life of the reaction,\n(b) the time taken for the concentration of the reactant to fall from 0.8 M to 0.1 M,\n(c) the fraction of the reactant left unreacted after 20 minutes.")
b.q("SA", "C", CO, "Using valence bond theory, predict (a) the hybridisation, (b) the geometry and (c) the magnetic behaviour of [Ni(CN)₄]²⁻ and [NiCl₄]²⁻. (Atomic number of Ni = 28)")
b.q("SA", "C", HA, "How will you bring about the following conversions? Write the chemical equations.\n(a) Ethanol to iodoethane\n(b) Benzene to chlorobenzene\n(c) Propene to 1-bromopropane")
b.q("SA", "C", AK, "Arrange the following as directed and give a reason in each case:\n(a) CH₃COOH, ClCH₂COOH, FCH₂COOH — increasing order of acid strength\n(b) Ethanal, propanone, methanal — increasing order of reactivity towards nucleophilic addition\n(c) Butane, propanal, propan-1-ol — increasing order of boiling point")
b.q("SA", "C", AM, "Write the chemical equations for the following reactions:\n(a) Carbylamine reaction of aniline\n(b) Coupling reaction of benzenediazonium chloride with phenol\n(c) Acetylation of aniline")

# ── SECTION D — CASE STUDY ──
b.q("CBQ", "D", DF, "In a school laboratory, a teacher shows the class aqueous solutions of copper(II) sulphate (blue), zinc sulphate (colourless), iron(II) sulphate (pale green) and potassium permanganate (purple). She explains that many transition metal ions are coloured and paramagnetic, and that iron and its compounds are used as catalysts in industry, for example in the Haber process for making ammonia.\n(a) Why is zinc sulphate solution colourless while copper(II) sulphate solution is blue?\n(b) Give two reasons why transition metals and their compounds act as good catalysts.\n(c) Calculate the spin-only magnetic moment of the Fe²⁺ ion. (Atomic number of Fe = 26)\nOR\n(c) Mn²⁺ is much more resistant than Fe²⁺ to oxidation to the +3 state. Explain on the basis of electronic configuration. (Atomic numbers: Mn = 25, Fe = 26)")
b.q("CBQ", "D", HA, "A student took a sample of optically active 2-bromobutane and heated it with aqueous potassium hydroxide. The product, butan-2-ol, was found to be optically inactive. Her teacher explained that the reaction went mainly through a planar carbocation, which the hydroxide ion can attack from either side. In a second experiment, 1-bromobutane reacted in a single step with complete inversion of configuration.\n(a) What is a racemic mixture? Why is it optically inactive?\n(b) Why does the SN1 reaction of an optically active alkyl halide give a racemic product?\n(c) Which of the two, 1-bromobutane or 2-bromobutane, reacts faster by the SN2 mechanism? Give a reason.\nOR\n(c) Which of the two, C₆H₅CH₂Cl or C₆H₅CHClC₆H₅, is hydrolysed more easily by aqueous KOH through the SN1 mechanism? Give a reason.")

# ── SECTION E — LA ──
b.q("LA", "E", DF, "(a) Write the electronic configurations of chromium (Z = 24) and copper (Z = 29). Why are these different from the expected configurations?\n(b) Explain why (i) transition metals show variable oxidation states and (ii) the E° value for the Mn³⁺/Mn²⁺ couple is much more positive than that for the Fe³⁺/Fe²⁺ couple.\n(c) Write the balanced chemical equations for the preparation of potassium permanganate from pyrolusite ore (MnO₂).\nOR\n(a) What are actinoids? Why do actinoids show a wider range of oxidation states than lanthanoids?\n(b) Compare the lanthanoids and the actinoids with respect to (i) atomic and ionic sizes and (ii) chemical reactivity.\n(c) Name a lanthanoid that shows the +4 oxidation state and state why it acts as an oxidising agent in this state.")
b.q("LA", "E", AM, "(a) An aromatic compound A (C₇H₇NO) on heating with bromine and sodium hydroxide gives compound B (C₆H₇N). B reacts with sodium nitrite and hydrochloric acid at 273–278 K to give C, which on warming with water gives D, a compound that gives a violet colour with neutral FeCl₃ solution. Identify A, B, C and D and write the chemical equations involved.\n(b) Arrange the following in increasing order of basic strength in aqueous solution: C₂H₅NH₂, (C₂H₅)₂NH, (C₂H₅)₃N, NH₃.\nOR\n(a) Describe the Hinsberg test for distinguishing primary, secondary and tertiary amines.\n(b) Why is aniline acetylated before its nitration?\n(c) Why are aliphatic amines stronger bases than ammonia?")
b.q("LA", "E", EL, "(a) Define molar conductivity. How does it change with dilution for (i) a strong electrolyte and (ii) a weak electrolyte?\n(b) The conductivity of a 0.002 M solution of acetic acid is 7.81 × 10⁻⁵ S cm⁻¹. Calculate its molar conductivity and degree of dissociation, given that the limiting molar conductivity of acetic acid is 390.5 S cm² mol⁻¹.\nOR\n(a) Write the Nernst equation and calculate the emf of the following cell at 298 K:\nMg(s) | Mg²⁺(0.01 M) || Ag⁺(0.001 M) | Ag(s)\n(E°Mg²⁺/Mg = −2.37 V, E°Ag⁺/Ag = +0.80 V)\n(b) How many coulombs of electricity are required to reduce 0.5 mol of Cu²⁺ ions to copper metal? (F = 96500 C mol⁻¹)")

b.save()
