"""
formula_topics_master.py
────────────────────────
Master topic list for Formula Flash reels.
~180 topics spanning Physics, Chemistry, Biology, Maths, CS — Class 10 & 12.

Imported by generate_formula_reel_v2.py and post_formula_reel.py.

Diagram keys reference diagram_library.DIAGRAMS — each topic uses
subject-relevant, non-duplicate diagrams.
"""

# Each topic:
# {
#   "subject": str,
#   "chapter_tag": str,
#   "title_line1": str,
#   "title_line2": str,
#   "board_note": str,       # text only — no emoji (font missing in matplotlib)
#   "hashtags": str,
#   "rows": [
#     {"label": str, "formula": str (LaTeX), "diagram": str, "note": str}
#   ]
# }

TOPICS = {

    # ══════════════════════════════════════════════════════
    #  PHYSICS — CLASS 12
    # ══════════════════════════════════════════════════════

    "em_induction": {
        "subject": "Physics", "chapter_tag": "Chapter 6 · Class XII",
        "title_line1": "Electromagnetic", "title_line2": "Induction",
        "board_note": "5-6 marks · Every Board Exam",
        "hashtags": "#Physics #EMI #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Magnetic Flux",   "formula": r"$\Phi = BA\cos\theta$",               "diagram": "field_lines",  "note": "Weber (Wb)"},
            {"label": "Faraday's Law",   "formula": r"$\varepsilon = -N\dfrac{d\Phi}{dt}$", "diagram": "coil_magnet_emi", "note": "Volt (V)"},
            {"label": "Lenz's Law",      "formula": r"$\varepsilon = -\dfrac{d\Phi}{dt}$",  "diagram": "lenz_ring",  "note": "Opposes cause"},
            {"label": "Motional EMF",    "formula": r"$\varepsilon = Blv$",                 "diagram": "motional_rod","note": "B·l·v"},
            {"label": "Self-Inductance", "formula": r"$\varepsilon = -L\dfrac{dI}{dt}$",    "diagram": "inductor_coil", "note": "Henry (H)"},
        ],
    },

    "current_electricity": {
        "subject": "Physics", "chapter_tag": "Chapter 3 · Class XII",
        "title_line1": "Current", "title_line2": "Electricity",
        "board_note": "8-10 marks · Every Board Exam",
        "hashtags": "#Physics #Electricity #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Ohm's Law",   "formula": r"$V = IR$",                      "diagram": "circuit_loop",  "note": "V·I·R"},
            {"label": "Resistivity", "formula": r"$R = \rho\dfrac{l}{A}$",         "diagram": "wire_resistivity","note": "Ohm-metre"},
            {"label": "KVL",         "formula": r"$\sum V = 0$",                  "diagram": "circuit_loop",  "note": "Closed loop"},
            {"label": "Wheatstone",  "formula": r"$\dfrac{P}{Q}=\dfrac{R}{S}$",   "diagram": "wheatstone",    "note": "Balanced bridge"},
            {"label": "Power",       "formula": r"$P = \dfrac{V^2}{R} = I^2R$",   "diagram": "power_triangle","note": "Watt (W)"},
        ],
    },

    "electrostatics": {
        "subject": "Physics", "chapter_tag": "Chapter 1 · Class XII",
        "title_line1": "Electrostatics", "title_line2": "Key Formulae",
        "board_note": "8-10 marks · Every Board Exam",
        "hashtags": "#Physics #Electrostatics #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Coulomb's Law",  "formula": r"$F = k\dfrac{q_1 q_2}{r^2}$",        "diagram": "two_charges",   "note": "Newton (N)"},
            {"label": "Electric Field", "formula": r"$E = \dfrac{F}{q} = \dfrac{kQ}{r^2}$","diagram": "field_lines",   "note": "N/C"},
            {"label": "Potential",      "formula": r"$V = \dfrac{kQ}{r}$",                 "diagram": "equipotential","note": "Volt (V)"},
            {"label": "Capacitance",    "formula": r"$C = \dfrac{Q}{V} = \varepsilon_0\dfrac{A}{d}$","diagram": "parallel_plates","note": "Farad (F)"},
            {"label": "Energy stored",  "formula": r"$U = \dfrac{1}{2}CV^2$",              "diagram": "parallel_plates","note": "Joule (J)"},
        ],
    },

    "optics": {
        "subject": "Physics", "chapter_tag": "Chapter 9-10 · Class XII",
        "title_line1": "Ray Optics", "title_line2": "& Wave Optics",
        "board_note": "10-12 marks · Every Board Exam",
        "hashtags": "#Physics #Optics #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Mirror Formula",  "formula": r"$\dfrac{1}{f} = \dfrac{1}{v}+\dfrac{1}{u}$","diagram": "mirror_optics","note": "Sign convention"},
            {"label": "Lens Formula",    "formula": r"$\dfrac{1}{f} = \dfrac{1}{v}-\dfrac{1}{u}$","diagram": "convex_lens","note": "Thin lens"},
            {"label": "Magnification",   "formula": r"$m = \dfrac{v}{u} = \dfrac{h_i}{h_o}$",    "diagram": "mirror_optics","note": "Dimensionless"},
            {"label": "Snell's Law",     "formula": r"$n_1\sin\theta_1 = n_2\sin\theta_2$",       "diagram": "snell",        "note": "Refraction"},
            {"label": "Young's Fringes", "formula": r"$\beta = \dfrac{\lambda D}{d}$",            "diagram": "young_fringes","note": "Fringe width"},
        ],
    },

    "semiconductor": {
        "subject": "Physics", "chapter_tag": "Chapter 14 · Class XII",
        "title_line1": "Semiconductor", "title_line2": "Devices",
        "board_note": "5-7 marks · Every Board Exam",
        "hashtags": "#Physics #Semiconductor #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Diode Current",    "formula": r"$I = I_0(e^{V/\eta V_T}-1)$",     "diagram": "pn_junction",  "note": "Shockley eq."},
            {"label": "Transistor Gain",  "formula": r"$\beta = \dfrac{I_C}{I_B}$",       "diagram": "transistor",   "note": "Current gain"},
            {"label": "Logic AND",        "formula": r"$Y = A \cdot B$",                  "diagram": "logic_gate_and",  "note": "Both HIGH"},
            {"label": "Logic OR",         "formula": r"$Y = A + B$",                      "diagram": "logic_gate_or",   "note": "Either HIGH"},
            {"label": "Logic NOT",        "formula": r"$Y = \bar{A}$",                    "diagram": "logic_gate_not",  "note": "Complement"},
        ],
    },

    "magnetism": {
        "subject": "Physics", "chapter_tag": "Chapter 4-5 · Class XII",
        "title_line1": "Moving Charges", "title_line2": "& Magnetism",
        "board_note": "6-8 marks · Every Board Exam",
        "hashtags": "#Physics #Magnetism #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Biot-Savart",   "formula": r"$dB = \dfrac{\mu_0}{4\pi}\dfrac{I\,dl\sin\theta}{r^2}$","diagram": "current_element",  "note": "Tesla (T)"},
            {"label": "Ampere's Law",  "formula": r"$\oint B\cdot dl = \mu_0 I$",                            "diagram": "wire_field", "note": "Closed loop"},
            {"label": "Force on wire", "formula": r"$F = BIl\sin\theta$",                                    "diagram": "force_on_wire","note": "Newton (N)"},
            {"label": "Lorentz Force", "formula": r"$F = q(v\times B)$",                                     "diagram": "field_lines",  "note": "On charge"},
            {"label": "Solenoid B",    "formula": r"$B = \mu_0 nI$",                                        "diagram": "solenoid", "note": "n = turns/m"},
        ],
    },

    "dual_nature": {
        "subject": "Physics", "chapter_tag": "Chapter 11 · Class XII",
        "title_line1": "Dual Nature", "title_line2": "of Matter",
        "board_note": "4-5 marks · Board Exam",
        "hashtags": "#Physics #QuantumPhysics #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Photoelectric",  "formula": r"$KE_{max} = h\nu - \phi$",         "diagram": "photoelectric",  "note": "Einstein eq."},
            {"label": "de Broglie",     "formula": r"$\lambda = \dfrac{h}{mv}$",         "diagram": "de_broglie",     "note": "Wave of matter"},
            {"label": "Threshold Freq", "formula": r"$\nu_0 = \dfrac{\phi}{h}$",         "diagram": "photoelectric",  "note": "Min. frequency"},
            {"label": "Stopping Pot.",  "formula": r"$eV_0 = KE_{max}$",                 "diagram": "photoelectric",  "note": "Volt (V)"},
            {"label": "Photon Energy",  "formula": r"$E = h\nu = \dfrac{hc}{\lambda}$",  "diagram": "de_broglie",     "note": "Joule (J)"},
        ],
    },

    "atoms_nuclei": {
        "subject": "Physics", "chapter_tag": "Chapter 12-13 · Class XII",
        "title_line1": "Atoms &", "title_line2": "Nuclei",
        "board_note": "5-6 marks · Board Exam",
        "hashtags": "#Physics #AtomicPhysics #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Bohr Radius",     "formula": r"$r_n = \dfrac{n^2 h^2}{4\pi^2 m k e^2}$","diagram": "bohr_atom",       "note": "0.529 Angstrom"},
            {"label": "Energy Level",    "formula": r"$E_n = -\dfrac{13.6}{n^2}$ eV",           "diagram": "bohr_atom",       "note": "Hydrogen"},
            {"label": "Mass-Energy",     "formula": r"$E = mc^2$",                              "diagram": "mass_energy","note": "Einstein"},
            {"label": "Half-Life",       "formula": r"$T_{1/2} = \dfrac{0.693}{\lambda}$",      "diagram": "radioactive_decay","note": "Decay constant"},
            {"label": "Radioactive law", "formula": r"$N = N_0 e^{-\lambda t}$",               "diagram": "radioactive_decay","note": "Activity"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  PHYSICS — CLASS 10
    # ══════════════════════════════════════════════════════

    "light_class10": {
        "subject": "Physics", "chapter_tag": "Chapter 10 · Class X",
        "title_line1": "Light —", "title_line2": "Reflection & Refraction",
        "board_note": "8-10 marks · Board Exam",
        "hashtags": "#Physics #Light #CBSE #BoardExam2026 #ClassX",
        "rows": [
            {"label": "Mirror Formula", "formula": r"$\dfrac{1}{f}=\dfrac{1}{v}+\dfrac{1}{u}$","diagram": "mirror_optics","note": "Sign convention"},
            {"label": "Magnification",  "formula": r"$m = -\dfrac{v}{u}$",                     "diagram": "mirror_optics","note": "Mirror"},
            {"label": "Snell's Law",    "formula": r"$n = \dfrac{\sin i}{\sin r}$",            "diagram": "snell",        "note": "Refraction"},
            {"label": "Lens Formula",   "formula": r"$\dfrac{1}{f}=\dfrac{1}{v}-\dfrac{1}{u}$","diagram": "convex_lens","note": "Thin lens"},
            {"label": "Power of Lens",  "formula": r"$P = \dfrac{1}{f}$",                      "diagram": "lens_focus","note": "Dioptre (D)"},
        ],
    },

    "electricity_class10": {
        "subject": "Physics", "chapter_tag": "Chapter 12 · Class X",
        "title_line1": "Electricity", "title_line2": "Class 10",
        "board_note": "8-10 marks · Board Exam",
        "hashtags": "#Physics #Electricity #CBSE #BoardExam2026 #ClassX",
        "rows": [
            {"label": "Ohm's Law",        "formula": r"$V = IR$",                        "diagram": "circuit_loop",  "note": "V = IR"},
            {"label": "Resistance",       "formula": r"$R = \rho\dfrac{l}{A}$",           "diagram": "wire_resistivity","note": "Ohm (Omega)"},
            {"label": "Series R",         "formula": r"$R_s = R_1+R_2+R_3$",             "diagram": "resistors_series",  "note": "Same current"},
            {"label": "Parallel R",       "formula": r"$\dfrac{1}{R_p}=\dfrac{1}{R_1}+\dfrac{1}{R_2}$","diagram": "resistors_parallel","note": "Same voltage"},
            {"label": "Power",            "formula": r"$P = VI = I^2R = \dfrac{V^2}{R}$","diagram": "power_triangle","note": "Watt (W)"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  CHEMISTRY — CLASS 12
    # ══════════════════════════════════════════════════════

    "chemical_kinetics": {
        "subject": "Chemistry", "chapter_tag": "Chapter 3 · Class XII",
        "title_line1": "Chemical", "title_line2": "Kinetics",
        "board_note": "5-6 marks · Every Board Exam",
        "hashtags": "#Chemistry #Kinetics #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Rate Law",          "formula": r"$r = k[A]^m[B]^n$",                                           "diagram": "rate_conc","note": "mol/L/s"},
            {"label": "1st Order k",       "formula": r"$k = \dfrac{2.303}{t}\log\dfrac{[A]_0}{[A]}$",                "diagram": "first_order_decay",  "note": "s^{-1}"},
            {"label": "Half Life (1st)",   "formula": r"$t_{1/2} = \dfrac{0.693}{k}$",                                "diagram": "half_life_chem",     "note": "Independent of [A]"},
            {"label": "Arrhenius",         "formula": r"$k = A e^{-E_a/RT}$",                                         "diagram": "arrhenius",          "note": "Activation energy"},
            {"label": "Activation Energy", "formula": r"$\ln\dfrac{k_2}{k_1}=\dfrac{E_a}{R}\left(\dfrac{1}{T_1}-\dfrac{1}{T_2}\right)$","diagram": "reaction_coordinate","note": "J/mol"},
        ],
    },

    "electrochemistry": {
        "subject": "Chemistry", "chapter_tag": "Chapter 2 · Class XII",
        "title_line1": "Electro-", "title_line2": "chemistry",
        "board_note": "5-6 marks · Every Board Exam",
        "hashtags": "#Chemistry #Electrochemistry #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Nernst Equation", "formula": r"$E = E^\circ - \dfrac{RT}{nF}\ln Q$",        "diagram": "galvanic_cell", "note": "Cell potential"},
            {"label": "Gibbs & EMF",     "formula": r"$\Delta G^\circ = -nFE^\circ$",              "diagram": "galvanic_cell", "note": "J/mol"},
            {"label": "Faraday's 1st",   "formula": r"$m = \dfrac{Zit}{F}$",                       "diagram": "electrolytic_cell", "note": "Mass deposited"},
            {"label": "Molar Conduct.",  "formula": r"$\Lambda_m = \dfrac{\kappa \times 1000}{M}$","diagram": "conductance_plot",  "note": "S cm² / mol"},
            {"label": "Kohlrausch",      "formula": r"$\Lambda_m^\infty = \sum\lambda_i$",         "diagram": "conductance_plot",  "note": "At infinite dilution"},
        ],
    },

    "solutions": {
        "subject": "Chemistry", "chapter_tag": "Chapter 1 · Class XII",
        "title_line1": "Solutions &", "title_line2": "Colligative Prop.",
        "board_note": "5-6 marks · Every Board Exam",
        "hashtags": "#Chemistry #Solutions #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Molarity",        "formula": r"$M = \dfrac{\mathrm{moles}}{\mathrm{L\ soln}}$","diagram": "beaker_solution",          "note": "mol/L"},
            {"label": "Raoult's Law",    "formula": r"$p_A = p_A^\circ x_A$",                        "diagram": "vapour_pressure",   "note": "Vapour pressure"},
            {"label": "Boiling Pt Rise", "formula": r"$\Delta T_b = K_b \cdot m$",                   "diagram": "boiling_point",     "note": "Ebullioscopy"},
            {"label": "Freezing Pt Dep.","formula": r"$\Delta T_f = K_f \cdot m$",                   "diagram": "boiling_point",     "note": "Cryoscopy"},
            {"label": "van't Hoff",      "formula": r"$\pi = iMRT$",                                 "diagram": "osmosis",           "note": "Osmotic pressure"},
        ],
    },

    "coordination": {
        "subject": "Chemistry", "chapter_tag": "Chapter 9 · Class XII",
        "title_line1": "Coordination", "title_line2": "Compounds",
        "board_note": "4-5 marks · Board Exam",
        "hashtags": "#Chemistry #Coordination #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Coordination No.", "formula": r"$CN = \mathrm{ligands\ bonded\ to\ metal}$",   "diagram": "coordination_sphere","note": "Central metal"},
            {"label": "IUPAC naming",     "formula": r"$\mathrm{ligands\ (\alpha)\ +\ metal(ON)}$",   "diagram": "coordination_sphere","note": "Anionic complex"},
            {"label": "EAN",              "formula": r"$EAN = Z - x + 2n$",                     "diagram": "coordination_sphere","note": "Effective atomic no."},
            {"label": "Crystal Field",    "formula": r"$\Delta_o > P \rightarrow \mathrm{low\ spin}$","diagram": "cfse_splitting",   "note": "Octahedral"},
            {"label": "Stability Const.", "formula": r"$K = \dfrac{[\mathrm{complex}]}{[\mathrm{M}][\mathrm{L}]^n}$","diagram": "coordination_sphere","note": "Larger = more stable"},
        ],
    },

    "solid_state": {
        "subject": "Chemistry", "chapter_tag": "Chapter 1 · Class XII",
        "title_line1": "Solid", "title_line2": "State",
        "board_note": "4-5 marks · Board Exam",
        "hashtags": "#Chemistry #SolidState #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Packing Eff. SC",  "formula": r"$PE = \dfrac{\pi}{6} \approx 52.4\%$",         "diagram": "crystal_lattice","note": "Simple cubic"},
            {"label": "Packing Eff. BCC", "formula": r"$PE = \dfrac{\sqrt{3}\pi}{8} \approx 68\%$",   "diagram": "crystal_lattice","note": "Body-centred"},
            {"label": "Packing Eff. FCC", "formula": r"$PE = \dfrac{\pi}{3\sqrt{2}} \approx 74\%$",   "diagram": "crystal_lattice","note": "Face-centred"},
            {"label": "Density",          "formula": r"$d = \dfrac{Z \cdot M}{N_A \cdot a^3}$",       "diagram": "crystal_lattice","note": "g/cm³"},
            {"label": "Radius ratio",     "formula": r"$r^+/r^- \rightarrow \mathrm{coord.\ no.}$","diagram": "crystal_lattice","note": "Ionic crystals"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  CHEMISTRY — CLASS 10
    # ══════════════════════════════════════════════════════

    "chemical_reactions_cl10": {
        "subject": "Chemistry", "chapter_tag": "Chapter 1 · Class X",
        "title_line1": "Chemical", "title_line2": "Reactions & Equations",
        "board_note": "5-6 marks · Board Exam",
        "hashtags": "#Chemistry #ChemicalReactions #CBSE #BoardExam2026 #ClassX",
        "rows": [
            {"label": "Combination",    "formula": r"$A + B \rightarrow AB$",                     "diagram": "rxn_combination","note": "Two reactants → one"},
            {"label": "Decomposition",  "formula": r"$AB \rightarrow A + B$",                     "diagram": "rxn_decomposition","note": "One → multiple"},
            {"label": "Displacement",   "formula": r"$A + BC \rightarrow AC + B$",                "diagram": "rxn_displacement","note": "More reactive displaces"},
            {"label": "Double Disp.",   "formula": r"$AB + CD \rightarrow AD + CB$",              "diagram": "rxn_double",  "note": "Exchange of ions"},
            {"label": "Redox",          "formula": r"$\mathrm{Ox\ loses\ e}^-,\ \mathrm{Red\ gains\ e}^-$","diagram": "electron_transfer","note": "OIL RIG"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  BIOLOGY — CLASS 12
    # ══════════════════════════════════════════════════════

    "genetics": {
        "subject": "Biology", "chapter_tag": "Chapter 5-6 · Class XII",
        "title_line1": "Principles of", "title_line2": "Inheritance",
        "board_note": "5-6 marks · Every Board Exam",
        "hashtags": "#Biology #Genetics #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Monohybrid Ratio", "formula": r"$3 : 1$",                                            "diagram": "punnett_square",  "note": "F2 phenotype ratio"},
            {"label": "Dihybrid Ratio",   "formula": r"$9 : 3 : 3 : 1$",                                   "diagram": "punnett_square",  "note": "F2 phenotype ratio"},
            {"label": "Hardy-Weinberg",   "formula": r"$p^2 + 2pq + q^2 = 1$",                             "diagram": "allele_bars","note": "Allele frequency"},
            {"label": "Chi-Square",       "formula": r"$\chi^2 = \sum\dfrac{(O-E)^2}{E}$",                 "diagram": "obs_exp_bars",  "note": "Goodness of fit"},
            {"label": "Linkage",          "formula": r"$\%\ \mathrm{Recomb} = \dfrac{\mathrm{recombinants}}{\mathrm{total}}\times100$","diagram": "crossing_over","note": "Morgan's work"},
        ],
    },

    "photosynthesis": {
        "subject": "Biology", "chapter_tag": "Chapter 13 · Class XI / Ch 11 XII",
        "title_line1": "Photosynthesis", "title_line2": "Key Equations",
        "board_note": "5-6 marks · Board Exam",
        "hashtags": "#Biology #Photosynthesis #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Overall Eq.",    "formula": r"$6CO_2 + 6H_2O \rightarrow C_6H_{12}O_6 + 6O_2$","diagram": "leaf_cross_section","note": "Chlorophyll req."},
            {"label": "Light Rxn",      "formula": r"$H_2O \rightarrow 2H^+ + 2e^- + \frac{1}{2}O_2$","diagram": "chloroplast","note": "Water splitting"},
            {"label": "ATP synthesis",  "formula": r"$ADP + P_i + \mathrm{energy} \rightarrow ATP$",  "diagram": "chloroplast","note": "Photophosphorylation"},
            {"label": "Calvin Cycle",   "formula": r"$3CO_2 + 9ATP + 6NADPH \rightarrow G3P$",        "diagram": "calvin_cycle","note": "Dark reaction"},
            {"label": "RQ (glucose)",   "formula": r"$RQ = \dfrac{CO_2 \text{ released}}{O_2 \text{ absorbed}} = 1$","diagram": "mitochondrion","note": "Respiratory quotient"},
        ],
    },

    "reproduction": {
        "subject": "Biology", "chapter_tag": "Chapter 1-3 · Class XII",
        "title_line1": "Human", "title_line2": "Reproduction",
        "board_note": "5-7 marks · Every Board Exam",
        "hashtags": "#Biology #Reproduction #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Oogenesis",      "formula": r"$2n \rightarrow n \text{ (ovum)}$",          "diagram": "cell_division",    "note": "Diploid to haploid"},
            {"label": "Spermatogenesis","formula": r"$2n \rightarrow 4n \text{ sperms}$",         "diagram": "cell_division",    "note": "One cell = 4 sperms"},
            {"label": "Gestation",      "formula": r"$\approx 280 \text{ days} = 40 \text{ weeks}$","diagram": "pregnancy_timeline","note": "Human pregnancy"},
            {"label": "Sex Chromosomes","formula": r"$\mathrm{XX=Female},\ \mathrm{XY=Male}$",    "diagram": "xy_chromosomes",        "note": "Chromosomal sex det."},
            {"label": "Contraception",  "formula": r"$\mathrm{Efficacy} = \left(1 - \dfrac{\mathrm{fail\ rate}}{100}\right)$","diagram": "hormone_feedback","note": "Pearl index"},
        ],
    },

    "ecology": {
        "subject": "Biology", "chapter_tag": "Chapter 13-14 · Class XII",
        "title_line1": "Ecology &", "title_line2": "Ecosystem",
        "board_note": "4-5 marks · Board Exam",
        "hashtags": "#Biology #Ecology #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "10% Energy Law", "formula": r"$\mathrm{Energy\ at\ next\ level} = 10\%$",   "diagram": "food_chain",       "note": "Lindemann's law"},
            {"label": "GPP vs NPP",     "formula": r"$NPP = GPP - R$",                             "diagram": "food_chain",       "note": "Net primary prod."},
            {"label": "Species Div.",   "formula": r"$H = -\sum p_i \ln p_i$",                     "diagram": "species_bars","note": "Shannon index"},
            {"label": "Population",     "formula": r"$\dfrac{dN}{dt} = rN$",                       "diagram": "population_growth","note": "Exponential growth"},
            {"label": "Logistic",       "formula": r"$\dfrac{dN}{dt} = rN\dfrac{K-N}{K}$",        "diagram": "population_growth","note": "K = carrying capacity"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  BIOLOGY — CLASS 10
    # ══════════════════════════════════════════════════════

    "life_processes_cl10": {
        "subject": "Biology", "chapter_tag": "Chapter 6 · Class X",
        "title_line1": "Life", "title_line2": "Processes",
        "board_note": "5-6 marks · Board Exam",
        "hashtags": "#Biology #LifeProcesses #CBSE #BoardExam2026 #ClassX",
        "rows": [
            {"label": "Photosynthesis", "formula": r"$6CO_2+6H_2O \rightarrow C_6H_{12}O_6+6O_2$","diagram": "leaf_cross_section","note": "Light needed"},
            {"label": "Respiration",    "formula": r"$C_6H_{12}O_6+6O_2 \rightarrow 6CO_2+6H_2O+ATP$","diagram": "mitochondrion",    "note": "Energy release"},
            {"label": "Anaerobic",      "formula": r"$C_6H_{12}O_6 \rightarrow 2C_2H_5OH+2CO_2$","diagram": "flask_bubbles","note": "Fermentation"},
            {"label": "Osmosis",        "formula": r"$\pi = iCRT$",                                "diagram": "osmosis",    "note": "Osmotic pressure"},
            {"label": "Transpiration",  "formula": r"$\mathrm{Rate} \propto \mathrm{temp,\ wind,\ low\ RH}$","diagram": "leaf_cross_section","note": "Stomata control"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  MATHEMATICS — CLASS 12
    # ══════════════════════════════════════════════════════

    "calculus": {
        "subject": "Mathematics", "chapter_tag": "Chapter 5-7 · Class XII",
        "title_line1": "Calculus", "title_line2": "Quick Reference",
        "board_note": "12-15 marks · Every Board Exam",
        "hashtags": "#Maths #Calculus #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Chain Rule",          "formula": r"$\dfrac{dy}{dx}=\dfrac{dy}{du}\cdot\dfrac{du}{dx}$","diagram": "tangent_line",    "note": "Composite fn"},
            {"label": "Product Rule",        "formula": r"$(uv)' = u'v + uv'$",                              "diagram": "tangent_line",    "note": "Leibniz rule"},
            {"label": "Integration by Parts","formula": r"$\int u\,dv = uv - \int v\,du$",                   "diagram": "integration_area","note": "ILATE order"},
            {"label": "Definite Integral",   "formula": r"$\int_a^b f(x)\,dx = F(b)-F(a)$",                 "diagram": "integration_area","note": "Newton-Leibniz"},
            {"label": "Area Under Curve",    "formula": r"$A = \int_a^b |f(x)|\,dx$",                       "diagram": "integration_area","note": "sq. units"},
        ],
    },

    "vectors_3d": {
        "subject": "Mathematics", "chapter_tag": "Chapter 10-11 · Class XII",
        "title_line1": "Vectors &", "title_line2": "3D Geometry",
        "board_note": "10-12 marks · Every Board Exam",
        "hashtags": "#Maths #Vectors #3DGeometry #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Dot Product",    "formula": r"$\vec{a}\cdot\vec{b} = |\vec{a}||\vec{b}|\cos\theta$","diagram": "vector_diagram",  "note": "Scalar result"},
            {"label": "Cross Product",  "formula": r"$|\vec{a}\times\vec{b}| = |\vec{a}||\vec{b}|\sin\theta$","diagram": "cross_product",  "note": "Vector result"},
            {"label": "Line (vector)",  "formula": r"$\vec{r} = \vec{a} + \lambda\vec{b}$",               "diagram": "vector_diagram",  "note": "Parametric form"},
            {"label": "Distance Pt-Ln","formula": r"$d = \dfrac{|\vec{AP}\times\vec{b}|}{|\vec{b}|}$",    "diagram": "cross_product",   "note": "Units = same as coords"},
            {"label": "Plane equation","formula": r"$ax+by+cz = d$",                                      "diagram": "plane_normal",  "note": "Normal form"},
        ],
    },

    "probability": {
        "subject": "Mathematics", "chapter_tag": "Chapter 13 · Class XII",
        "title_line1": "Probability", "title_line2": "Theorems",
        "board_note": "8-10 marks · Every Board Exam",
        "hashtags": "#Maths #Probability #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Addition Rule",  "formula": r"$P(A\cup B)=P(A)+P(B)-P(A\cap B)$","diagram": "venn","note": "Union"},
            {"label": "Conditional",    "formula": r"$P(A|B) = \dfrac{P(A\cap B)}{P(B)}$","diagram": "venn","note": "Given B occurred"},
            {"label": "Bayes' Theorem", "formula": r"$P(A_i|B)=\dfrac{P(A_i)P(B|A_i)}{\sum P(A_j)P(B|A_j)}$","diagram": "probability_tree","note": "Reverse conditional"},
            {"label": "Binomial Dist.", "formula": r"$P(X=r)=\binom{n}{r}p^r q^{n-r}$","diagram": "binomial_bars","note": "n trials, p success"},
            {"label": "Mean (Binomial)","formula": r"$\mu = np,\quad \sigma^2 = npq$",   "diagram": "binomial_bars","note": "Variance = npq"},
        ],
    },

    "matrices_determinants": {
        "subject": "Mathematics", "chapter_tag": "Chapter 3-4 · Class XII",
        "title_line1": "Matrices &", "title_line2": "Determinants",
        "board_note": "10-12 marks · Every Board Exam",
        "hashtags": "#Maths #Matrices #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Matrix Product",  "formula": r"$(AB)_{ij} = \sum_k A_{ik}B_{kj}$",   "diagram": "matrix_grid",  "note": "Order: (m×n)(n×p)"},
            {"label": "Transpose",       "formula": r"$(AB)^T = B^T A^T$",                   "diagram": "matrix_grid",  "note": "Reversal"},
            {"label": "Determinant 2x2", "formula": r"$\det A = ad - bc$",                   "diagram": "matrix_grid",  "note": "2×2 matrix"},
            {"label": "Cramer's Rule",   "formula": r"$x_i = \dfrac{D_i}{D}$",               "diagram": "matrix_grid",  "note": "System of equations"},
            {"label": "Inverse",         "formula": r"$A^{-1} = \dfrac{\text{adj}(A)}{\det(A)}$","diagram": "matrix_grid","note": "Exists iff det != 0"},
        ],
    },

    "linear_programming": {
        "subject": "Mathematics", "chapter_tag": "Chapter 12 · Class XII",
        "title_line1": "Linear", "title_line2": "Programming",
        "board_note": "5-6 marks · Board Exam",
        "hashtags": "#Maths #LinearProgramming #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Objective Fn",   "formula": r"$Z = ax + by$",                          "diagram": "lp_feasible",   "note": "Maximise / Minimise"},
            {"label": "Constraints",    "formula": r"$a_1 x+b_1 y \leq c_1,\ x,y \geq 0$",   "diagram": "lp_feasible",   "note": "Feasible region"},
            {"label": "Corner Points",  "formula": r"$Z_{opt}\ \mathrm{at\ vertex\ of\ region}$","diagram": "lp_feasible","note": "Extreme point theorem"},
            {"label": "Unbounded",      "formula": r"$Z \rightarrow \infty\ \mathrm{(open\ region)}$","diagram": "lp_unbounded","note": "No finite max"},
            {"label": "Feasible Soln.", "formula": r"$\{(x,y):\ \mathrm{all\ constraints}\}$","diagram": "lp_feasible",   "note": "Convex polygon"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  MATHEMATICS — CLASS 10
    # ══════════════════════════════════════════════════════

    "quadratic_cl10": {
        "subject": "Mathematics", "chapter_tag": "Chapter 4 · Class X",
        "title_line1": "Quadratic", "title_line2": "Equations",
        "board_note": "5-6 marks · Board Exam",
        "hashtags": "#Maths #Quadratic #CBSE #BoardExam2026 #ClassX",
        "rows": [
            {"label": "Standard Form",  "formula": r"$ax^2 + bx + c = 0$",                   "diagram": "quadratic_parabola","note": "a != 0"},
            {"label": "Quadratic Form.","formula": r"$x = \dfrac{-b \pm \sqrt{b^2-4ac}}{2a}$","diagram": "quadratic_parabola","note": "Roots"},
            {"label": "Discriminant",   "formula": r"$D = b^2 - 4ac$",                        "diagram": "quadratic_parabola","note": "D>0 real, D=0 equal"},
            {"label": "Sum of Roots",   "formula": r"$\alpha+\beta = -\dfrac{b}{a}$",         "diagram": "quadratic_parabola","note": "Vieta's formula"},
            {"label": "Product of Roots","formula": r"$\alpha\beta = \dfrac{c}{a}$",          "diagram": "quadratic_parabola","note": "Vieta's formula"},
        ],
    },

    "trigonometry_cl10": {
        "subject": "Mathematics", "chapter_tag": "Chapter 8-9 · Class X",
        "title_line1": "Trigonometry", "title_line2": "Identities",
        "board_note": "6-8 marks · Board Exam",
        "hashtags": "#Maths #Trigonometry #CBSE #BoardExam2026 #ClassX",
        "rows": [
            {"label": "Pythagorean",   "formula": r"$\sin^2\theta + \cos^2\theta = 1$",       "diagram": "trig_circle",  "note": "Fundamental"},
            {"label": "Identity 2",    "formula": r"$1 + \tan^2\theta = \sec^2\theta$",       "diagram": "trig_circle",  "note": "Divide by cos²"},
            {"label": "Identity 3",    "formula": r"$1 + \cot^2\theta = \csc^2\theta$",       "diagram": "trig_circle",  "note": "Divide by sin²"},
            {"label": "SOH-CAH-TOA",   "formula": r"$\sin=\dfrac{O}{H},\ \cos=\dfrac{A}{H},\ \tan=\dfrac{O}{A}$","diagram": "right_triangle","note": "Right triangle"},
            {"label": "Angle of Elev.","formula": r"$\tan\theta = \dfrac{\text{height}}{\text{distance}}$","diagram": "elevation","note": "Heights & distances"},
        ],
    },

    # ══════════════════════════════════════════════════════
    #  COMPUTER SCIENCE — CLASS 12
    # ══════════════════════════════════════════════════════

    "boolean_algebra": {
        "subject": "CS", "chapter_tag": "Chapter 3 · Class XII",
        "title_line1": "Boolean Algebra", "title_line2": "& Logic Gates",
        "board_note": "4-5 marks · Board Exam",
        "hashtags": "#ComputerScience #BooleanAlgebra #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "De Morgan I",    "formula": r"$\overline{A+B} = \bar{A}\cdot\bar{B}$","diagram": "logic_gate_and", "note": "NOR = AND of NOT"},
            {"label": "De Morgan II",   "formula": r"$\overline{A\cdot B} = \bar{A}+\bar{B}$","diagram": "logic_gate_or", "note": "NAND = OR of NOT"},
            {"label": "Absorption",     "formula": r"$A + AB = A$",                          "diagram": "truth_table",    "note": "Simplification"},
            {"label": "Half Adder",     "formula": r"$S=A\oplus B,\ C=A\cdot B$",            "diagram": "truth_table",    "note": "Sum & Carry"},
            {"label": "POS / SOP",      "formula": r"$f=\sum m_i = \prod M_i$",              "diagram": "truth_table",    "note": "Canonical forms"},
        ],
    },

    "networking": {
        "subject": "CS", "chapter_tag": "Chapter 4 · Class XII",
        "title_line1": "Computer", "title_line2": "Networks",
        "board_note": "3-4 marks · Board Exam",
        "hashtags": "#ComputerScience #Networking #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "IP Address",    "formula": r"$\mathrm{IPv4:\ 32\ bits\ =\ 4\ octets}$",         "diagram": "ip_address",       "note": "e.g. 192.168.1.1"},
            {"label": "Bandwidth",     "formula": r"$BW = \dfrac{\mathrm{Data}}{\mathrm{Time}}$",      "diagram": "network_topology", "note": "bps / kbps / Mbps"},
            {"label": "OSI Layers",    "formula": r"$7\rightarrow 1:\ \mathrm{App\ to\ Physical}$",    "diagram": "osi_stack", "note": "7 layer model"},
            {"label": "HTTP vs HTTPS", "formula": r"$\mathrm{HTTPS = HTTP + TLS}$",                   "diagram": "ip_address",       "note": "Port 443 vs 80"},
            {"label": "URL structure", "formula": r"$\mathrm{protocol://domain/path}$",               "diagram": "network_topology", "note": "Uniform Res. Locator"},
        ],
    },

    "python_basics": {
        "subject": "CS", "chapter_tag": "Class XI-XII",
        "title_line1": "Python", "title_line2": "Quick Reference",
        "board_note": "5-6 marks · Practical + Theory",
        "hashtags": "#ComputerScience #Python #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "List slicing",  "formula": r"$\mathrm{list[start:stop:step]}$",        "diagram": "code_block",   "note": "0-indexed"},
            {"label": "List comp.",    "formula": r"$[f(x) \text{ for } x \text{ in list}]$", "diagram": "code_block",   "note": "Concise loops"},
            {"label": "dict get",      "formula": r"$d.get(k,\ \mathrm{default})$",           "diagram": "code_block",   "note": "No KeyError"},
            {"label": "Lambda",        "formula": r"$\lambda x: x^2$",                        "diagram": "code_block",   "note": "Anonymous fn"},
            {"label": "File I/O",      "formula": r"$\mathrm{open(f,\ 'r')\ as\ fh}$",        "diagram": "code_block",   "note": "Context manager"},
        ],
    },

    "dbms": {
        "subject": "CS", "chapter_tag": "Chapter 7 · Class XII",
        "title_line1": "Database", "title_line2": "Management",
        "board_note": "4-5 marks · Board Exam",
        "hashtags": "#ComputerScience #DBMS #SQL #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "SELECT",        "formula": r"$\mathrm{SELECT\ col\ FROM\ tbl}$",       "diagram": "sql_table",    "note": "Query"},
            {"label": "JOIN",          "formula": r"$\mathrm{INNER/LEFT/RIGHT\ JOIN}$",        "diagram": "sql_table",    "note": "Combine tables"},
            {"label": "GROUP BY",      "formula": r"$\mathrm{SELECT\ col,AGG()\ GROUP\ BY}$", "diagram": "sql_table",    "note": "Aggregate"},
            {"label": "Primary Key",   "formula": r"$\mathrm{Unique\ +\ NOT\ NULL}$",          "diagram": "sql_table",    "note": "Entity integrity"},
            {"label": "Foreign Key",   "formula": r"$\mathrm{References\ PK\ of\ table}$",    "diagram": "sql_table",    "note": "Referential integrity"},
        ],
    },

}
