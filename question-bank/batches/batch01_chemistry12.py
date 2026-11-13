"""Batch 01 — Class 12 Chemistry: one paper's worth (plus spare) of original questions. Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("chemistry12")
SO, EL, KI, DF, CO = "Solutions", "Electrochemistry", "Chemical Kinetics", "The d- and f-Block Elements", "Coordination Compounds"
HA, AL, AK, AM, BI = "Haloalkanes and Haloarenes", "Alcohols, Phenols and Ethers", "Aldehydes, Ketones and Carboxylic Acids", "Amines", "Biomolecules"

# ── SECTION A — MCQ ──
b.m("A", SO, "Which colligative property is most suitable for determining the molar mass of proteins and polymers?", "Relative lowering of vapour pressure", "Elevation of boiling point", "Osmotic pressure", "Depression of freezing point", "C")
b.m("A", SO, "The van't Hoff factor for K₂SO₄, assuming complete dissociation in water, is:", "2", "3", "4", "1", "B")
b.m("A", SO, "A mixture of nitric acid and water forms a maximum boiling azeotrope. This solution shows:", "negative deviation from Raoult's law", "positive deviation from Raoult's law", "ideal behaviour", "no change in boiling point", "A")
b.m("A", EL, "The unit of molar conductivity is:", "S cm⁻¹", "S cm mol⁻¹", "S⁻¹ cm² mol⁻¹", "S cm² mol⁻¹", "D")
b.m("A", EL, "The quantity of charge required to reduce 1 mol of Al³⁺ ions to Al is:", "1 F", "2 F", "3 F", "6 F", "C")
b.m("A", EL, "The electrolyte used in a lead storage battery is:", "38% solution of sulphuric acid", "concentrated nitric acid", "potassium hydroxide solution", "ammonium chloride paste", "A")
b.m("A", KI, "The unit of the rate constant for a first order reaction is:", "mol L⁻¹ s⁻¹", "s⁻¹", "L mol⁻¹ s⁻¹", "mol² L⁻² s⁻¹", "B")
b.m("A", KI, "For a zero order reaction, the half-life period is:", "directly proportional to the initial concentration", "independent of the initial concentration", "inversely proportional to the initial concentration", "proportional to the square of the initial concentration", "A")
b.m("A", KI, "A catalyst increases the rate of a reaction by:", "increasing the activation energy", "increasing the enthalpy of reaction", "shifting the equilibrium towards products", "providing a path of lower activation energy", "D")
b.m("A", DF, "Most transition metal ions are coloured in aqueous solution because of:", "charge transfer from water", "their small size", "d-d transitions of electrons", "their high ionisation enthalpy", "C")
b.m("A", DF, "Lanthanoid contraction is caused by:", "the high nuclear charge alone", "the poor shielding of nuclear charge by 4f electrons", "the strong shielding by 5d electrons", "the presence of unpaired electrons", "B")
b.m("A", CO, "The oxidation state of iron in K₄[Fe(CN)₆] is:", "+2", "+3", "+4", "0", "A")
b.m("A", CO, "The IUPAC name of [Co(NH₃)₆]Cl₃ is:", "hexaamminecobalt(II) chloride", "hexaaminecobaltate(III) chloride", "cobalt(III) hexaammine chloride", "hexaamminecobalt(III) chloride", "D")
b.m("A", HA, "Which of the following alkyl halides reacts fastest by the SN1 mechanism?", "CH₃Br", "CH₃CH₂Br", "(CH₃)₃CBr", "(CH₃)₂CHBr", "C")
b.m("A", AL, "Phenol reacts with bromine water to give a white precipitate of:", "o-bromophenol", "2,4,6-tribromophenol", "p-bromophenol", "bromobenzene", "B")
b.m("A", AK, "Which of the following compounds gives a silver mirror with Tollens' reagent?", "Propanone", "Ethanal", "Ethanol", "Ethanoic acid", "B")
b.m("A", AM, "Which of the following is the strongest base in aqueous solution?", "NH₃", "CH₃NH₂", "(CH₃)₂NH", "C₆H₅NH₂", "C")
b.m("A", BI, "The linkage that joins two amino acid units in a protein is called:", "a peptide linkage", "a glycosidic linkage", "a phosphodiester linkage", "an ester linkage", "A")
b.m("A", BI, "The deficiency of which vitamin causes scurvy?", "Vitamin A", "Vitamin B₁₂", "Vitamin D", "Vitamin C", "D")

b.ar("A", SO, "The molarity of a solution changes with temperature.", "The volume of a solution changes with temperature.", "A")
b.ar("A", CO, "[Ni(CO)₄] is a diamagnetic complex.", "Nickel is in the +2 oxidation state in [Ni(CO)₄].", "C")
b.ar("A", AL, "Phenol is a stronger acid than ethanol.", "The phenoxide ion is stabilised by resonance, whereas the ethoxide ion is not.", "A")

# ── SECTION B — VSA ──
b.q("VSA", "B", SO, "State Henry's law. Why are bottles of soft drinks sealed under high pressure?")
b.q("VSA", "B", EL, "Calculate the standard emf and the standard Gibbs energy change of the cell Zn | Zn²⁺(1 M) || Cu²⁺(1 M) | Cu.\n(Given: E°(Zn²⁺/Zn) = −0.76 V, E°(Cu²⁺/Cu) = +0.34 V, F = 96500 C mol⁻¹)")
b.q("VSA", "B", KI, "The rate constant of a first order reaction is 6.93 × 10⁻³ s⁻¹. Calculate its half-life and the time required for 75% of the reaction to be completed.")
b.q("VSA", "B", DF, "Give reasons:\n(a) Zinc, cadmium and mercury are not regarded as transition elements.\n(b) Transition metals and many of their compounds act as good catalysts.")
b.q("VSA", "B", HA, "Give two reasons why haloarenes are less reactive than haloalkanes towards nucleophilic substitution reactions.")
b.q("VSA", "B", AM, "Describe a chemical test to distinguish between methylamine and dimethylamine. Write the chemical equation involved.\nOR\nWrite the chemical equations for the conversion of aniline into (a) benzenediazonium chloride and (b) 2,4,6-tribromoaniline.")

# ── SECTION C — SA ──
b.q("SA", "C", SO, "(a) Define the molal elevation constant (ebullioscopic constant).\n(b) 18 g of glucose (molar mass 180 g mol⁻¹) is dissolved in 1 kg of water. Calculate the boiling point of the solution. (K_b for water = 0.52 K kg mol⁻¹, boiling point of pure water = 373.15 K)")
b.q("SA", "C", EL, "(a) State Kohlrausch's law of independent migration of ions.\n(b) The limiting molar conductivities of HCl, NaCl and CH₃COONa are 426, 126 and 91 S cm² mol⁻¹ respectively. Calculate the limiting molar conductivity of acetic acid.\n(c) If the molar conductivity of an acetic acid solution is 39.1 S cm² mol⁻¹, find its degree of dissociation.")
b.q("SA", "C", KI, "The rate constant of a reaction doubles when the temperature is raised from 300 K to 310 K. Calculate the activation energy of the reaction. (R = 8.314 J K⁻¹ mol⁻¹, log 2 = 0.3010)")
b.q("SA", "C", DF, "Account for the following:\n(a) Cr²⁺ is a reducing agent while Mn³⁺ is an oxidising agent, although both have the d⁴ configuration.\n(b) Actinoids show a wider range of oxidation states than lanthanoids.\n(c) Cu⁺ ion is not stable in aqueous solution.")
b.q("SA", "C", CO, "Using valence bond theory, compare [Fe(CN)₆]³⁻ and [FeF₆]³⁻ with respect to (a) the type of hybridisation, (b) the magnetic behaviour and (c) whether each is an inner or outer orbital complex. (Atomic number of Fe = 26)")
b.q("SA", "C", HA, "Differentiate between SN1 and SN2 reactions on the basis of (a) the number of steps in the mechanism, (b) the order of the reaction and (c) the stereochemistry of the product. Give one example of an alkyl halide that reacts mainly by each mechanism.")
b.q("SA", "C", AL, "How will you carry out the following conversions? Write the chemical equations.\n(a) Phenol to salicylaldehyde\n(b) Propene to propan-2-ol\n(c) Ethanol to ethoxyethane")
b.q("SA", "C", AK, "Explain the following reactions with one chemical equation each:\n(a) Aldol condensation\n(b) Cannizzaro reaction\n(c) Clemmensen reduction")
b.q("SA", "C", AM, "Account for the following:\n(a) Aniline does not undergo the Friedel-Crafts reaction.\n(b) The pK_b of aniline is higher than that of methylamine.\n(c) Aromatic diazonium salts are more stable than aliphatic diazonium salts.")

# ── SECTION D — CASE STUDY ──
b.q("CBQ", "D", BI, "Carbohydrates are the main source of energy in our food. Glucose, a monosaccharide, exists mostly in a cyclic form. Two monosaccharide units join through an oxygen atom to form a disaccharide such as sucrose, maltose or lactose. Sugars that reduce Tollens' reagent and Fehling's solution are called reducing sugars. Starch, the storage polysaccharide of plants, is a mixture of two components, amylose and amylopectin, while cellulose forms the cell walls of plants.\n(a) What name is given to the linkage that joins two monosaccharide units?\n(b) Why is sucrose a non-reducing sugar while maltose is a reducing sugar?\n(c) Write two structural differences between amylose and amylopectin.\nOR\n(c) Name the products obtained on the hydrolysis of (i) sucrose and (ii) lactose. Why is sucrose called invert sugar?")
b.q("CBQ", "D", EL, "A fuel cell is a galvanic cell that converts the energy of combustion of a fuel directly into electrical energy. In the hydrogen-oxygen fuel cell, hydrogen and oxygen gases are bubbled through porous carbon electrodes into a concentrated aqueous solution of sodium hydroxide. The cell runs as long as the gases are supplied, and the only product is water. Such cells were used to provide electrical power in the Apollo space programme, and the water produced was used by the astronauts for drinking.\n(a) Write the reactions taking place at the anode and at the cathode of this cell.\n(b) Write the overall cell reaction.\n(c) State two advantages of a fuel cell over a thermal power plant.\nOR\n(c) How is a fuel cell different from a primary cell such as a dry cell? Give two points.")

# ── SECTION E — LA ──
b.q("LA", "E", AK, "(a) An organic compound A (C₃H₆O) does not reduce Tollens' reagent but gives a yellow precipitate with iodine and sodium hydroxide. On reduction, A gives compound B (C₃H₈O), which on heating with concentrated sulphuric acid gives compound C (C₃H₆). Identify A, B and C and write the equations for the reactions involved.\n(b) Give one chemical test each to distinguish between (i) benzaldehyde and acetophenone and (ii) ethanal and propanal.\nOR\n(a) Arrange the following in increasing order of acid strength and give a reason: CH₃COOH, ClCH₂COOH, FCH₂COOH, Cl₂CHCOOH.\n(b) Why are carboxylic acids higher boiling than alcohols of comparable molecular mass?\n(c) Write the equations for (i) the Hell-Volhard-Zelinsky reaction and (ii) the decarboxylation of sodium ethanoate.")
b.q("LA", "E", CO, "(a) Write the IUPAC names of [Pt(NH₃)₂Cl₂] and K₃[Cr(C₂O₄)₃].\n(b) Draw the crystal field splitting diagram for an octahedral complex. Write the electronic configuration of a d⁴ ion when (i) Δ₀ > P and (ii) Δ₀ < P.\n(c) What type of isomerism is shown by [Co(NH₃)₅Br]SO₄ and [Co(NH₃)₅SO₄]Br? Give a chemical test to distinguish between them.\nOR\n(a) What is meant by the chelate effect? Give one example of a chelating ligand.\n(b) Draw the geometrical isomers of [Co(en)₂Cl₂]⁺. Which of them is optically active?\n(c) Explain why [Ti(H₂O)₆]³⁺ is coloured while [Sc(H₂O)₆]³⁺ is colourless.")
b.q("LA", "E", KI, "(a) State two differences between the order and the molecularity of a reaction.\n(b) A first order reaction is 20% complete in 10 minutes. Calculate the rate constant and the time taken for 75% completion of the reaction. (log 1.25 = 0.0969, log 4 = 0.6021)\n(c) What is a pseudo first order reaction? Give one example.\nOR\n(a) Derive the integrated rate equation for a zero order reaction.\n(b) Show that the half-life of a first order reaction is independent of the initial concentration.\n(c) The half-life of a first order reaction is 30 minutes. What fraction of the reactant remains after 2 hours?")

b.save()
