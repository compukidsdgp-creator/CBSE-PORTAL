"""Batch 02 — Class 12 Chemistry: tops the pool up for one more paper. Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("chemistry12")
SO, EL, KI, DF, CO = "Solutions", "Electrochemistry", "Chemical Kinetics", "The d- and f-Block Elements", "Coordination Compounds"
HA, AL, AK, AM, BI = "Haloalkanes and Haloarenes", "Alcohols, Phenols and Ethers", "Aldehydes, Ketones and Carboxylic Acids", "Amines", "Biomolecules"

# ── SECTION A — MCQ ──
b.m("A", SO, "The unit of molality is:", "mol L⁻¹", "mol kg⁻¹", "g L⁻¹", "mol dm⁻³", "B")
b.m("A", EL, "The standard electrode potential of the standard hydrogen electrode is taken as:", "0.00 V", "1.00 V", "−1.00 V", "0.76 V", "A")
b.m("A", KI, "The molecularity of an elementary reaction can never be:", "1", "2", "3", "zero", "D")
b.m("A", DF, "The highest oxidation state shown by manganese in its compounds is:", "+4", "+6", "+7", "+2", "C")
b.m("A", CO, "The coordination number of cobalt in [Co(en)₃]³⁺ is:", "3", "6", "4", "2", "B")
b.m("A", HA, "Chlorobenzene reacts with methyl chloride and sodium in dry ether to give toluene. This reaction is called the:", "Wurtz-Fittig reaction", "Fittig reaction", "Wurtz reaction", "Friedel-Crafts reaction", "A")
b.m("A", AL, "Lucas reagent is a mixture of:", "anhydrous AlCl₃ and concentrated HCl", "concentrated HNO₃ and concentrated H₂SO₄", "anhydrous ZnCl₂ and dilute HCl", "anhydrous ZnCl₂ and concentrated HCl", "D")
b.m("A", AK, "Formalin is a 40% aqueous solution of:", "ethanal", "methanol", "methanal", "methanoic acid", "C")
b.m("A", AM, "The Gabriel phthalimide synthesis is used for the preparation of:", "primary aliphatic amines", "secondary amines", "tertiary amines", "primary aromatic amines", "A")
b.m("A", BI, "The sugar present in DNA is:", "ribose", "2-deoxyribose", "glucose", "fructose", "B")

b.ar("A", KI, "The rate of a reaction generally increases when the temperature is raised.", "At a higher temperature, a larger fraction of the molecules has energy equal to or greater than the activation energy.", "A")
b.ar("A", HA, "Tertiary alkyl halides react fastest by the SN2 mechanism.", "The rate of an SN2 reaction decreases as the crowding around the carbon bearing the halogen increases.", "D")

# ── SECTION B — VSA ──
b.q("VSA", "B", SO, "What is an ideal solution? State two of its characteristics and give one example.")
b.q("VSA", "B", EL, "Why does the conductivity of a solution decrease on dilution, whereas its molar conductivity increases?")
b.q("VSA", "B", CO, "Write the IUPAC names of the following coordination compounds and state the oxidation number of the central metal in each:\n(a) [Cr(NH₃)₃Cl₃]\n(b) K₂[Zn(OH)₄]")
b.q("VSA", "B", AL, "Give reasons:\n(a) The boiling point of ethanol is higher than that of methoxymethane.\n(b) o-Nitrophenol is more steam volatile than p-nitrophenol.")
b.q("VSA", "B", BI, "What are essential and non-essential amino acids? Give one example of each. What is a zwitterion?")

# ── SECTION C — SA ──
b.q("SA", "C", SO, "(a) Define osmotic pressure.\n(b) A solution is prepared by dissolving 1.0 g of a polymer in water to make 100 mL of solution. Its osmotic pressure at 300 K is 2.5 × 10⁻³ atm. Calculate the molar mass of the polymer. (R = 0.0821 L atm K⁻¹ mol⁻¹)")
b.q("SA", "C", EL, "Write the Nernst equation for the cell Zn | Zn²⁺(0.1 M) || Cu²⁺(0.01 M) | Cu and calculate its emf at 298 K. (E°cell = 1.10 V)")
b.q("SA", "C", DF, "Write balanced ionic equations for the following reactions:\n(a) Acidified potassium permanganate with iron(II) ions\n(b) Acidified potassium permanganate with oxalate ions\n(c) Acidified potassium dichromate with iodide ions")
b.q("SA", "C", HA, "Write the structure of the major product in each of the following reactions and give a reason for your answer in each case:\n(a) 2-Bromobutane is heated with alcoholic potassium hydroxide.\n(b) Chlorobenzene is treated with a mixture of concentrated nitric acid and concentrated sulphuric acid.\n(c) Bromoethane is treated with silver cyanide.")
b.q("SA", "C", AM, "Identify the compounds A, B and C in the following sequence of reactions and write the equations:\nBenzoic acid is heated with ammonia to give A. A is treated with bromine and aqueous sodium hydroxide to give B. B is treated with sodium nitrite and hydrochloric acid at 273-278 K to give C.\nName the reaction by which A is converted into B.")
b.q("SA", "C", BI, "(a) Write two structural differences between DNA and RNA.\n(b) What type of bonding stabilises the α-helix structure of a protein?\n(c) What happens when a protein is denatured? Give one example.")

# ── SECTION D — CASE STUDY ──
b.q("CBQ", "D", KI, "Hydrogen peroxide solution decomposes very slowly at room temperature. When a small amount of potassium iodide solution is added, the decomposition becomes rapid and bubbles of oxygen are seen at once. If the mixture is warmed, the reaction becomes faster still. Chemists explain these observations by saying that molecules must collide with a certain minimum energy before they can react, and that only a fraction of the collisions are effective.\n(a) Define the activation energy of a reaction.\n(b) How does potassium iodide increase the rate of this reaction? Does it change the enthalpy change of the reaction?\n(c) Write the Arrhenius equation and state what each term in it represents.\nOR\n(c) The decomposition follows first order kinetics with a half-life of 20 minutes under certain conditions. How long will it take for the concentration of hydrogen peroxide to fall to one-eighth of its initial value?")
b.q("CBQ", "D", AL, "Ethanol is produced on a large scale by the fermentation of the sugar present in molasses, sugarcane or fruits. The process is carried out by yeast in the absence of air. The ethanol sold for industrial use is made unfit for drinking by adding substances such as copper sulphate and pyridine. Methanol, which is sometimes present in illicit liquor, is highly poisonous and can cause blindness and death even in small amounts.\n(a) Name the two enzymes, present in yeast, that take part in the conversion of sugar into ethanol.\n(b) What is ethanol called after copper sulphate and pyridine have been added to it? Why are they added?\n(c) What product is obtained when ethanol is oxidised with (i) pyridinium chlorochromate (PCC) and (ii) acidified potassium dichromate in excess?\nOR\n(c) Describe a chemical test to distinguish between methanol and ethanol and write the equation involved.")

# ── SECTION E — LA ──
b.q("LA", "E", EL, "(a) State Faraday's first law of electrolysis.\n(b) A current of 2 A is passed through a solution of silver nitrate for 30 minutes. Calculate the mass of silver deposited at the cathode. (Atomic mass of Ag = 108 u, F = 96500 C mol⁻¹)\n(c) Name the products formed at the cathode and at the anode when (i) an aqueous solution of sodium chloride and (ii) dilute sulphuric acid are electrolysed using platinum electrodes.\nOR\n(a) Write the reactions taking place at the anode and at the cathode of a lead storage battery when it is in use.\n(b) What happens when the battery is recharged?\n(c) The resistance of a conductivity cell filled with a KCl solution of conductivity 1.29 × 10⁻² S cm⁻¹ is 100 Ω. Calculate the cell constant.")
b.q("LA", "E", AL, "(a) Write the mechanism of the acid-catalysed hydration of ethene to ethanol.\n(b) Explain Williamson's synthesis of ethers with one example. Why can tert-butyl ethyl ether not be prepared from tert-butyl bromide and sodium ethoxide?\n(c) Write the equation for Kolbe's reaction.\nOR\n(a) How will you convert (i) phenol to benzene, (ii) ethanol to ethanal and (iii) anisole to phenol?\n(b) Arrange the following in increasing order of acid strength and give a reason: phenol, p-nitrophenol, p-cresol.\n(c) Give one chemical test to distinguish between phenol and ethanol.")
b.q("LA", "E", SO, "(a) State Raoult's law for a solution of two volatile liquids. What is meant by positive deviation from Raoult's law? Give one example and explain the cause of the deviation.\n(b) The vapour pressures of pure liquids A and B at a certain temperature are 400 mm Hg and 600 mm Hg respectively. If the total vapour pressure of their solution is 520 mm Hg, find the mole fraction of each liquid in the solution and the mole fraction of A in the vapour phase.\nOR\n(a) What is the van't Hoff factor? What is its value for a solute that associates in solution?\n(b) 2.0 g of a non-electrolyte solute dissolved in 100 g of benzene lowers the freezing point of benzene by 0.64 K. Calculate the molar mass of the solute. (K_f for benzene = 5.12 K kg mol⁻¹)\n(c) Why is a 1 M solution of NaCl expected to show a greater depression in freezing point than a 1 M solution of glucose?")

b.save()
