"""
formula_topics_master.py
────────────────────────
Master topic list for Formula Flash reels.
~180 topics spanning Physics, Chemistry, Biology, Maths, CS — Class 10 & 12.

Imported by generate_formula_reel_v2.py and post_formula_reel.py.
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
            {"label": "Magnetic Flux",   "formula": r"$\Phi = BA\cos\theta$",               "diagram": "flux",        "note": "Weber (Wb)"},
            {"label": "Faraday's Law",   "formula": r"$\varepsilon = -N\dfrac{d\Phi}{dt}$", "diagram": "coil_magnet", "note": "Volt (V)"},
            {"label": "Lenz's Law",      "formula": r"$\varepsilon = -\dfrac{d\Phi}{dt}$",  "diagram": "lenz",        "note": "Opposes cause"},
            {"label": "Motional EMF",    "formula": r"$\varepsilon = Blv$",                 "diagram": "motional",    "note": "B·l·v"},
            {"label": "Self-Inductance", "formula": r"$\varepsilon = -L\dfrac{dI}{dt}$",    "diagram": "inductor",    "note": "Henry (H)"},
        ],
    },

    "current_electricity": {
        "subject": "Physics", "chapter_tag": "Chapter 3 · Class XII",
        "title_line1": "Current", "title_line2": "Electricity",
        "board_note": "8-10 marks · Every Board Exam",
        "hashtags": "#Physics #Electricity #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Ohm's Law",   "formula": r"$V = IR$",                      "diagram": "ohm",    "note": "V·I·R"},
            {"label": "Resistivity", "formula": r"$R = \rho\dfrac{l}{A}$",         "diagram": "wire",   "note": "Ohm-metre"},
            {"label": "KVL",         "formula": r"$\sum V = 0$",                  "diagram": "loop",   "note": "Closed loop"},
            {"label": "Wheatstone",  "formula": r"$\dfrac{P}{Q}=\dfrac{R}{S}$",   "diagram": "bridge", "note": "Balanced bridge"},
            {"label": "Power",       "formula": r"$P = \dfrac{V^2}{R} = I^2R$",   "diagram": "power",  "note": "Watt (W)"},
        ],
    },

    "electrostatics": {
        "subject": "Physics", "chapter_tag": "Chapter 1 · Class XII",
        "title_line1": "Electrostatics", "title_line2": "Key Formulae",
        "board_note": "8-10 marks · Every Board Exam",
        "hashtags": "#Physics #Electrostatics #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Coulomb's Law",  "formula": r"$F = k\dfrac{q_1 q_2}{r^2}$",        "diagram": "flux",    "note": "Newton (N)"},
            {"label": "Electric Field", "formula": r"$E = \dfrac{F}{q} = \dfrac{kQ}{r^2}$","diagram": "wire",    "note": "N/C"},
            {"label": "Potential",      "formula": r"$V = \dfrac{kQ}{r}$",                 "diagram": "ohm",     "note": "Volt (V)"},
            {"label": "Capacitance",    "formula": r"$C = \dfrac{Q}{V} = \varepsilon_0\dfrac{A}{d}$","diagram": "motional","note": "Farad (F)"},
            {"label": "Energy stored",  "formula": r"$U = \dfrac{1}{2}CV^2$",              "diagram": "power",   "note": "Joule (J)"},
        ],
    },

    "optics": {
        "subject": "Physics", "chapter_tag": "Chapter 9-10 · Class XII",
        "title_line1": "Ray Optics", "title_line2": "& Wave Optics",
        "board_note": "10-12 marks · Every Board Exam",
        "hashtags": "#Physics #Optics #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Mirror Formula",  "formula": r"$\dfrac{1}{f} = \dfrac{1}{v}+\dfrac{1}{u}$","diagram": "loop",    "note": "Sign convention"},
            {"label": "Lens Formula",    "formula": r"$\dfrac{1}{f} = \dfrac{1}{v}-\dfrac{1}{u}$","diagram": "bridge",  "note": "Thin lens"},
            {"label": "Magnification",   "formula": r"$m = \dfrac{v}{u} = \dfrac{h_i}{h_o}$",    "diagram": "ohm",     "note": "Dimensionless"},
            {"label": "Snell's Law",     "formula": r"$n_1\sin\theta_1 = n_2\sin\theta_2$",       "diagram": "flux",    "note": "Refraction"},
            {"label": "Young's Fringes", "formula": r"$\beta = \dfrac{\lambda D}{d}$",            "diagram": "motional","note": "Fringe width"},
        ],
    },

    "semiconductor": {
        "subject": "Physics", "chapter_tag": "Chapter 14 · Class XII",
        "title_line1": "Semiconductor", "title_line2": "Devices",
        "board_note": "5-7 marks · Every Board Exam",
        "hashtags": "#Physics #Semiconductor #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Diode Current",    "formula": r"$I = I_0(e^{V/\eta V_T}-1)$",     "diagram": "power",   "note": "Shockley eq."},
            {"label": "Transistor Gain",  "formula": r"$\beta = \dfrac{I_C}{I_B}$",       "diagram": "ohm",     "note": "Current gain"},
            {"label": "Logic AND",        "formula": r"$Y = A \cdot B$",                  "diagram": "bridge",  "note": "Both HIGH"},
            {"label": "Logic OR",         "formula": r"$Y = A + B$",                      "diagram": "loop",    "note": "Either HIGH"},
            {"label": "Logic NOT",        "formula": r"$Y = \bar{A}$",                    "diagram": "wire",    "note": "Complement"},
        ],
    },

    "magnetism": {
        "subject": "Physics", "chapter_tag": "Chapter 4-5 · Class XII",
        "title_line1": "Moving Charges", "title_line2": "& Magnetism",
        "board_note": "6-8 marks · Every Board Exam",
        "hashtags": "#Physics #Magnetism #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Biot-Savart",   "formula": r"$dB = \dfrac{\mu_0}{4\pi}\dfrac{I\,dl\sin\theta}{r^2}$","diagram": "flux",    "note": "Tesla (T)"},
            {"label": "Ampere's Law",  "formula": r"$\oint B\cdot dl = \mu_0 I$",                            "diagram": "loop",    "note": "Closed loop"},
            {"label": "Force on wire", "formula": r"$F = BIl\sin\theta$",                                    "diagram": "motional","note": "Newton (N)"},
            {"label": "Lorentz Force", "formula": r"$F = q(v\times B)$",                                     "diagram": "wire",    "note": "On charge"},
            {"label": "Solenoid B",    "formula": r"$B = \mu_0 nI$",                                        "diagram": "inductor","note": "n = turns/m"},
        ],
    },

    "dual_nature": {
        "subject": "Physics", "chapter_tag": "Chapter 11 · Class XII",
        "title_line1": "Dual Nature", "title_line2": "of Matter",
        "board_note": "4-5 marks · Board Exam",
        "hashtags": "#Physics #QuantumPhysics #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Photoelectric",  "formula": r"$KE_{max} = h\nu - \phi$",         "diagram": "power",   "note": "Einstein eq."},
            {"label": "de Broglie",     "formula": r"$\lambda = \dfrac{h}{mv}$",         "diagram": "flux",    "note": "Wave of matter"},
            {"label": "Threshold Freq", "formula": r"$\nu_0 = \dfrac{\phi}{h}$",         "diagram": "ohm",     "note": "Min. frequency"},
            {"label": "Stopping Pot.",  "formula": r"$eV_0 = KE_{max}$",                 "diagram": "motional","note": "Volt (V)"},
            {"label": "Photon Energy",  "formula": r"$E = h\nu = \dfrac{hc}{\lambda}$",  "diagram": "wire",    "note": "Joule (J)"},
        ],
    },

    "atoms_nuclei": {
        "subject": "Physics", "chapter_tag": "Chapter 12-13 · Class XII",
        "title_line1": "Atoms &", "title_line2": "Nuclei",
        "board_note": "5-6 marks · Board Exam",
        "hashtags": "#Physics #AtomicPhysics #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Bohr Radius",     "formula": r"$r_n = \dfrac{n^2 h^2}{4\pi^2 m k e^2}$","diagram": "loop",    "note": "0.529 Angstrom"},
            {"label": "Energy Level",    "formula": r"$E_n = -\dfrac{13.6}{n^2}$ eV",           "diagram": "power",   "note": "Hydrogen"},
            {"label": "Mass-Energy",     "formula": r"$E = mc^2$",                              "diagram": "ohm",     "note": "Einstein"},
            {"label": "Half-Life",       "formula": r"$T_{1/2} = \dfrac{0.693}{\lambda}$",      "diagram": "inductor","note": "Decay constant"},
            {"label": "Radioactive law", "formula": r"$N = N_0 e^{-\lambda t}$",               "diagram": "flux",    "note": "Activity"},
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
            {"label": "Mirror Formula", "formula": r"$\dfrac{1}{f}=\dfrac{1}{v}+\dfrac{1}{u}$","diagram": "loop",    "note": "Sign convention"},
            {"label": "Magnification",  "formula": r"$m = -\dfrac{v}{u}$",                     "diagram": "ohm",     "note": "Mirror"},
            {"label": "Snell's Law",    "formula": r"$n = \dfrac{\sin i}{\sin r}$",            "diagram": "flux",    "note": "Refraction"},
            {"label": "Lens Formula",   "formula": r"$\dfrac{1}{f}=\dfrac{1}{v}-\dfrac{1}{u}$","diagram": "bridge",  "note": "Thin lens"},
            {"label": "Power of Lens",  "formula": r"$P = \dfrac{1}{f}$",                      "diagram": "power",   "note": "Dioptre (D)"},
        ],
    },

    "electricity_class10": {
        "subject": "Physics", "chapter_tag": "Chapter 12 · Class X",
        "title_line1": "Electricity", "title_line2": "Class 10",
        "board_note": "8-10 marks · Board Exam",
        "hashtags": "#Physics #Electricity #CBSE #BoardExam2026 #ClassX",
        "rows": [
            {"label": "Ohm's Law",        "formula": r"$V = IR$",                        "diagram": "ohm",    "note": "V = IR"},
            {"label": "Resistance",       "formula": r"$R = \rho\dfrac{l}{A}$",           "diagram": "wire",   "note": "Ohm (Omega)"},
            {"label": "Series R",         "formula": r"$R_s = R_1+R_2+R_3$",             "diagram": "loop",   "note": "Same current"},
            {"label": "Parallel R",       "formula": r"$\dfrac{1}{R_p}=\dfrac{1}{R_1}+\dfrac{1}{R_2}$","diagram": "bridge","note": "Same voltage"},
            {"label": "Power",            "formula": r"$P = VI = I^2R = \dfrac{V^2}{R}$","diagram": "power",  "note": "Watt (W)"},
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
            {"label": "Rate Law",          "formula": r"$r = k[A]^m[B]^n$",                                           "diagram": "flux",    "note": "mol/L/s"},
            {"label": "1st Order k",       "formula": r"$k = \dfrac{2.303}{t}\log\dfrac{[A]_0}{[A]}$",                "diagram": "power",   "note": "s^{-1}"},
            {"label": "Half Life (1st)",   "formula": r"$t_{1/2} = \dfrac{0.693}{k}$",                                "diagram": "inductor","note": "Independent of [A]"},
            {"label": "Arrhenius",         "formula": r"$k = A e^{-E_a/RT}$",                                         "diagram": "ohm",     "note": "Activation energy"},
            {"label": "Activation Energy", "formula": r"$\ln\dfrac{k_2}{k_1}=\dfrac{E_a}{R}\left(\dfrac{1}{T_1}-\dfrac{1}{T_2}\right)$","diagram": "bridge","note": "J/mol"},
        ],
    },

    "electrochemistry": {
        "subject": "Chemistry", "chapter_tag": "Chapter 2 · Class XII",
        "title_line1": "Electro-", "title_line2": "chemistry",
        "board_note": "5-6 marks · Every Board Exam",
        "hashtags": "#Chemistry #Electrochemistry #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Nernst Equation", "formula": r"$E = E^\circ - \dfrac{RT}{nF}\ln Q$",        "diagram": "loop",    "note": "Cell potential"},
            {"label": "Gibbs & EMF",     "formula": r"$\Delta G^\circ = -nFE^\circ$",              "diagram": "power",   "note": "J/mol"},
            {"label": "Faraday's 1st",   "formula": r"$m = \dfrac{Zit}{F}$",                       "diagram": "wire",    "note": "Mass deposited"},
            {"label": "Molar Conduct.",  "formula": r"$\Lambda_m = \dfrac{\kappa \times 1000}{M}$","diagram": "bridge",  "note": "S cm² / mol"},
            {"label": "Kohlrausch",      "formula": r"$\Lambda_m^\infty = \sum\lambda_i$",         "diagram": "ohm",     "note": "At infinite dilution"},
        ],
    },

    "solutions": {
        "subject": "Chemistry", "chapter_tag": "Chapter 1 · Class XII",
        "title_line1": "Solutions &", "title_line2": "Colligative Prop.",
        "board_note": "5-6 marks · Every Board Exam",
        "hashtags": "#Chemistry #Solutions #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Molarity",        "formula": r"$M = \dfrac{\mathrm{moles}}{\mathrm{L\ soln}}$","diagram": "ohm",     "note": "mol/L"},
            {"label": "Raoult's Law",    "formula": r"$p_A = p_A^\circ x_A$",                                          "diagram": "flux",    "note": "Vapour pressure"},
            {"label": "Boiling Pt Rise", "formula": r"$\Delta T_b = K_b \cdot m$",                                     "diagram": "power",   "note": "Ebullioscopy"},
            {"label": "Freezing Pt Dep.","formula": r"$\Delta T_f = K_f \cdot m$",                                     "diagram": "motional","note": "Cryoscopy"},
            {"label": "van't Hoff",      "formula": r"$\pi = iMRT$",                                                   "diagram": "bridge",  "note": "Osmotic pressure"},
        ],
    },

    "coordination": {
        "subject": "Chemistry", "chapter_tag": "Chapter 9 · Class XII",
        "title_line1": "Coordination", "title_line2": "Compounds",
        "board_note": "4-5 marks · Board Exam",
        "hashtags": "#Chemistry #Coordination #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Coordination No.", "formula": r"$CN = \mathrm{ligands\ bonded\ to\ metal}$",   "diagram": "loop",    "note": "Central metal"},
            {"label": "IUPAC naming",     "formula": r"$\mathrm{ligands\ (\alpha)\ +\ metal(ON)}$",   "diagram": "ohm",     "note": "Anionic complex"},
            {"label": "EAN",              "formula": r"$EAN = Z - x + 2n$",                     "diagram": "bridge",  "note": "Effective atomic no."},
            {"label": "Crystal Field",    "formula": r"$\Delta_o > P \rightarrow \text{\mathrm{low\ spin}$","diagram": "flux",   "note": "Octahedral"},
            {"label": "Stability Const.", "formula": r"$K = \dfrac{[\mathrm{complex}]}{[\mathrm{M}][\mathrm{L}]^n}$","diagram": "power","note": "Larger = more stable"},
        ],
    },

    "solid_state": {
        "subject": "Chemistry", "chapter_tag": "Chapter 1 · Class XII",
        "title_line1": "Solid", "title_line2": "State",
        "board_note": "4-5 marks · Board Exam",
        "hashtags": "#Chemistry #SolidState #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Packing Eff. SC",  "formula": r"$PE = \dfrac{\pi}{6} \approx 52.4\%$",         "diagram": "ohm",     "note": "Simple cubic"},
            {"label": "Packing Eff. BCC", "formula": r"$PE = \dfrac{\sqrt{3}\pi}{8} \approx 68\%$",   "diagram": "flux",    "note": "Body-centred"},
            {"label": "Packing Eff. FCC", "formula": r"$PE = \dfrac{\pi}{3\sqrt{2}} \approx 74\%$",   "diagram": "power",   "note": "Face-centred"},
            {"label": "Density",          "formula": r"$d = \dfrac{Z \cdot M}{N_A \cdot a^3}$",       "diagram": "bridge",  "note": "g/cm³"},
            {"label": "Radius ratio",     "formula": r"$r^+/r^- \rightarrow \mathrm{coord.\ no.}$","diagram": "motional","note": "Ionic crystals"},
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
            {"label": "Combination",    "formula": r"$A + B \rightarrow AB$",                     "diagram": "ohm",     "note": "Two reactants → one"},
            {"label": "Decomposition",  "formula": r"$AB \rightarrow A + B$",                     "diagram": "flux",    "note": "One → multiple"},
            {"label": "Displacement",   "formula": r"$A + BC \rightarrow AC + B$",                "diagram": "bridge",  "note": "More reactive displaces"},
            {"label": "Double Disp.",   "formula": r"$AB + CD \rightarrow AD + CB$",              "diagram": "loop",    "note": "Exchange of ions"},
            {"label": "Redox",          "formula": r"$\mathrm{Ox\ loses\ e}^-,\ \mathrm{Red\ gains\ e}^-$","diagram": "power",   "note": "OIL RIG"},
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
            {"label": "Monohybrid Ratio", "formula": r"$3 : 1$",                                            "diagram": "flux",    "note": "F2 phenotype ratio"},
            {"label": "Dihybrid Ratio",   "formula": r"$9 : 3 : 3 : 1$",                                   "diagram": "bridge",  "note": "F2 phenotype ratio"},
            {"label": "Hardy-Weinberg",   "formula": r"$p^2 + 2pq + q^2 = 1$",                             "diagram": "power",   "note": "Allele frequency"},
            {"label": "Chi-Square",       "formula": r"$\chi^2 = \sum\dfrac{(O-E)^2}{E}$",                 "diagram": "ohm",     "note": "Goodness of fit"},
            {"label": "Linkage",          "formula": r"$\%\ \mathrm{Recomb} = \dfrac{\mathrm{recombinants}}{\mathrm{total}}\times100$","diagram": "loop","note": "Morgan's work"},
        ],
    },

    "photosynthesis": {
        "subject": "Biology", "chapter_tag": "Chapter 13 · Class XI / Ch 11 XII",
        "title_line1": "Photosynthesis", "title_line2": "Key Equations",
        "board_note": "5-6 marks · Board Exam",
        "hashtags": "#Biology #Photosynthesis #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Overall Eq.",    "formula": r"$6CO_2 + 6H_2O \rightarrow C_6H_{12}O_6 + 6O_2$","diagram": "flux",    "note": "Chlorophyll req."},
            {"label": "Light Rxn",      "formula": r"$H_2O \rightarrow 2H^+ + 2e^- + \frac{1}{2}O_2$",        "diagram": "power",   "note": "Water splitting"},
            {"label": "ATP synthesis",  "formula": r"$ADP + P_i + \mathrm{energy} \rightarrow ATP$",             "diagram": "ohm",     "note": "Photophosphorylation"},
            {"label": "Calvin Cycle",   "formula": r"$3CO_2 + 9ATP + 6NADPH \rightarrow G3P$",                 "diagram": "loop",    "note": "Dark reaction"},
            {"label": "RQ (glucose)",   "formula": r"$RQ = \dfrac{CO_2 \text{ released}}{O_2 \text{ absorbed}} = 1$","diagram": "bridge","note": "Respiratory quotient"},
        ],
    },

    "reproduction": {
        "subject": "Biology", "chapter_tag": "Chapter 1-3 · Class XII",
        "title_line1": "Human", "title_line2": "Reproduction",
        "board_note": "5-7 marks · Every Board Exam",
        "hashtags": "#Biology #Reproduction #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Oogenesis",      "formula": r"$2n \rightarrow n \text{ (ovum)}$",          "diagram": "loop",    "note": "Diploid to haploid"},
            {"label": "Spermatogenesis","formula": r"$2n \rightarrow 4n \text{ sperms}$",         "diagram": "bridge",  "note": "One cell = 4 sperms"},
            {"label": "Gestation",      "formula": r"$\approx 280 \text{ days} = 40 \text{ weeks}$",              "diagram": "ohm",     "note": "Human pregnancy"},
            {"label": "Sex Chromosomes","formula": r"$\mathrm{XX=Female},\ \mathrm{XY=Male}$",                    "diagram": "flux",    "note": "Chromosomal sex det."},
            {"label": "Contraception",  "formula": r"$\mathrm{Efficacy} = \left(1 - \dfrac{\mathrm{fail\ rate}}{100}\right)$","diagram": "power","note": "Pearl index"},
        ],
    },

    "ecology": {
        "subject": "Biology", "chapter_tag": "Chapter 13-14 · Class XII",
        "title_line1": "Ecology &", "title_line2": "Ecosystem",
        "board_note": "4-5 marks · Board Exam",
        "hashtags": "#Biology #Ecology #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "10% Energy Law", "formula": r"$\mathrm{Energy\ at\ next\ level} = 10\%$",   "diagram": "flux",    "note": "Lindemann's law"},
            {"label": "GPP vs NPP",     "formula": r"$NPP = GPP - R$",                               "diagram": "power",   "note": "Net primary prod."},
            {"label": "Species Div.",   "formula": r"$H = -\sum p_i \ln p_i$",                        "diagram": "bridge",  "note": "Shannon index"},
            {"label": "Population",     "formula": r"$\dfrac{dN}{dt} = rN$",                          "diagram": "loop",    "note": "Exponential growth"},
            {"label": "Logistic",       "formula": r"$\dfrac{dN}{dt} = rN\dfrac{K-N}{K}$",           "diagram": "ohm",     "note": "K = carrying capacity"},
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
            {"label": "Photosynthesis", "formula": r"$6CO_2+6H_2O \rightarrow C_6H_{12}O_6+6O_2$","diagram": "flux",    "note": "Light needed"},
            {"label": "Respiration",    "formula": r"$C_6H_{12}O_6+6O_2 \rightarrow 6CO_2+6H_2O+ATP$","diagram": "power","note": "Energy release"},
            {"label": "Anaerobic",      "formula": r"$C_6H_{12}O_6 \rightarrow 2C_2H_5OH+2CO_2$","diagram": "loop",    "note": "Fermentation"},
            {"label": "Osmosis",        "formula": r"$\pi = iCRT$",                              "diagram": "bridge",  "note": "Osmotic pressure"},
            {"label": "Transpiration",  "formula": r"$\mathrm{Rate} \propto \mathrm{temp,\ wind,\ low\ RH}$","diagram": "ohm", "note": "Stomata control"},
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
            {"label": "Chain Rule",          "formula": r"$\dfrac{dy}{dx}=\dfrac{dy}{du}\cdot\dfrac{du}{dx}$","diagram": "flux",    "note": "Composite fn"},
            {"label": "Product Rule",        "formula": r"$(uv)' = u'v + uv'$",                              "diagram": "ohm",     "note": "Leibniz rule"},
            {"label": "Integration by Parts","formula": r"$\int u\,dv = uv - \int v\,du$",                   "diagram": "bridge",  "note": "ILATE order"},
            {"label": "Definite Integral",   "formula": r"$\int_a^b f(x)\,dx = F(b)-F(a)$",                 "diagram": "loop",    "note": "Newton-Leibniz"},
            {"label": "Area Under Curve",    "formula": r"$A = \int_a^b |f(x)|\,dx$",                       "diagram": "power",   "note": "sq. units"},
        ],
    },

    "vectors_3d": {
        "subject": "Mathematics", "chapter_tag": "Chapter 10-11 · Class XII",
        "title_line1": "Vectors &", "title_line2": "3D Geometry",
        "board_note": "10-12 marks · Every Board Exam",
        "hashtags": "#Maths #Vectors #3DGeometry #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Dot Product",    "formula": r"$\vec{a}\cdot\vec{b} = |\vec{a}||\vec{b}|\cos\theta$","diagram": "ohm",     "note": "Scalar result"},
            {"label": "Cross Product",  "formula": r"$|\vec{a}\times\vec{b}| = |\vec{a}||\vec{b}|\sin\theta$","diagram": "motional","note": "Vector result"},
            {"label": "Line (vector)",  "formula": r"$\vec{r} = \vec{a} + \lambda\vec{b}$",               "diagram": "wire",    "note": "Parametric form"},
            {"label": "Distance Pt-Ln","formula": r"$d = \dfrac{|\vec{AP}\times\vec{b}|}{|\vec{b}|}$",    "diagram": "bridge",  "note": "Units = same as coords"},
            {"label": "Plane equation","formula": r"$ax+by+cz = d$",                                      "diagram": "flux",    "note": "Normal form"},
        ],
    },

    "probability": {
        "subject": "Mathematics", "chapter_tag": "Chapter 13 · Class XII",
        "title_line1": "Probability", "title_line2": "Theorems",
        "board_note": "8-10 marks · Every Board Exam",
        "hashtags": "#Maths #Probability #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Addition Rule",  "formula": r"$P(A\cup B)=P(A)+P(B)-P(A\cap B)$","diagram": "loop",    "note": "Union"},
            {"label": "Conditional",    "formula": r"$P(A|B) = \dfrac{P(A\cap B)}{P(B)}$","diagram": "bridge", "note": "Given B occurred"},
            {"label": "Bayes' Theorem", "formula": r"$P(A_i|B)=\dfrac{P(A_i)P(B|A_i)}{\sum P(A_j)P(B|A_j)}$","diagram": "ohm","note": "Reverse conditional"},
            {"label": "Binomial Dist.", "formula": r"$P(X=r)=\binom{n}{r}p^r q^{n-r}$","diagram": "power",   "note": "n trials, p success"},
            {"label": "Mean (Binomial)","formula": r"$\mu = np,\quad \sigma^2 = npq$",   "diagram": "flux",    "note": "Variance = npq"},
        ],
    },

    "matrices_determinants": {
        "subject": "Mathematics", "chapter_tag": "Chapter 3-4 · Class XII",
        "title_line1": "Matrices &", "title_line2": "Determinants",
        "board_note": "10-12 marks · Every Board Exam",
        "hashtags": "#Maths #Matrices #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Matrix Product",  "formula": r"$(AB)_{ij} = \sum_k A_{ik}B_{kj}$",   "diagram": "bridge",  "note": "Order: (m×n)(n×p)"},
            {"label": "Transpose",       "formula": r"$(AB)^T = B^T A^T$",                   "diagram": "loop",    "note": "Reversal"},
            {"label": "Determinant 2x2", "formula": r"$\det A = ad - bc$",                   "diagram": "ohm",     "note": "2×2 matrix"},
            {"label": "Cramer's Rule",   "formula": r"$x_i = \dfrac{D_i}{D}$",               "diagram": "flux",    "note": "System of equations"},
            {"label": "Inverse",         "formula": r"$A^{-1} = \dfrac{\text{adj}(A)}{\det(A)}$","diagram": "power","note": "Exists iff det != 0"},
        ],
    },

    "linear_programming": {
        "subject": "Mathematics", "chapter_tag": "Chapter 12 · Class XII",
        "title_line1": "Linear", "title_line2": "Programming",
        "board_note": "5-6 marks · Board Exam",
        "hashtags": "#Maths #LinearProgramming #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "Objective Fn",   "formula": r"$Z = ax + by$",                         "diagram": "ohm",     "note": "Maximise / Minimise"},
            {"label": "Constraints",    "formula": r"$a_1 x+b_1 y \leq c_1,\ x,y \geq 0$","diagram": "bridge",  "note": "Feasible region"},
            {"label": "Corner Points",  "formula": r"$Z_{opt}\ \mathrm{at\ vertex\ of\ region}$","diagram": "flux","note": "Extreme point theorem"},
            {"label": "Unbounded",      "formula": r"$Z \rightarrow \infty\ \mathrm{(open\ region)}$","diagram": "power","note": "No finite max"},
            {"label": "Feasible Soln.", "formula": r"$\{(x,y):\ \mathrm{all\ constraints}\}$","diagram": "loop","note": "Convex polygon"},
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
            {"label": "Standard Form",  "formula": r"$ax^2 + bx + c = 0$",                "diagram": "ohm",     "note": "a != 0"},
            {"label": "Quadratic Form.","formula": r"$x = \dfrac{-b \pm \sqrt{b^2-4ac}}{2a}$","diagram": "flux", "note": "Roots"},
            {"label": "Discriminant",   "formula": r"$D = b^2 - 4ac$",                    "diagram": "power",   "note": "D>0 real, D=0 equal"},
            {"label": "Sum of Roots",   "formula": r"$\alpha+\beta = -\dfrac{b}{a}$",     "diagram": "bridge",  "note": "Vieta's formula"},
            {"label": "Product of Roots","formula": r"$\alpha\beta = \dfrac{c}{a}$",      "diagram": "loop",    "note": "Vieta's formula"},
        ],
    },

    "trigonometry_cl10": {
        "subject": "Mathematics", "chapter_tag": "Chapter 8-9 · Class X",
        "title_line1": "Trigonometry", "title_line2": "Identities",
        "board_note": "6-8 marks · Board Exam",
        "hashtags": "#Maths #Trigonometry #CBSE #BoardExam2026 #ClassX",
        "rows": [
            {"label": "Pythagorean",   "formula": r"$\sin^2\theta + \cos^2\theta = 1$",       "diagram": "ohm",     "note": "Fundamental"},
            {"label": "Identity 2",    "formula": r"$1 + \tan^2\theta = \sec^2\theta$",       "diagram": "flux",    "note": "Divide by cos²"},
            {"label": "Identity 3",    "formula": r"$1 + \cot^2\theta = \csc^2\theta$",       "diagram": "power",   "note": "Divide by sin²"},
            {"label": "SOH-CAH-TOA",   "formula": r"$\sin=\dfrac{O}{H},\ \cos=\dfrac{A}{H},\ \tan=\dfrac{O}{A}$","diagram": "bridge","note": "Right triangle"},
            {"label": "Angle of Elev.","formula": r"$\tan\theta = \dfrac{\text{height}}{\text{distance}}$","diagram": "loop","note": "Heights & distances"},
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
            {"label": "De Morgan I",    "formula": r"$\overline{A+B} = \bar{A}\cdot\bar{B}$","diagram": "flux",    "note": "NOR = AND of NOT"},
            {"label": "De Morgan II",   "formula": r"$\overline{A\cdot B} = \bar{A}+\bar{B}$","diagram": "ohm",    "note": "NAND = OR of NOT"},
            {"label": "Absorption",     "formula": r"$A + AB = A$",                          "diagram": "bridge",  "note": "Simplification"},
            {"label": "Half Adder",     "formula": r"$S=A\oplus B,\ C=A\cdot B$",            "diagram": "loop",    "note": "Sum & Carry"},
            {"label": "POS / SOP",      "formula": r"$f=\sum m_i = \prod M_i$",              "diagram": "power",   "note": "Canonical forms"},
        ],
    },

    "networking": {
        "subject": "CS", "chapter_tag": "Chapter 4 · Class XII",
        "title_line1": "Computer", "title_line2": "Networks",
        "board_note": "3-4 marks · Board Exam",
        "hashtags": "#ComputerScience #Networking #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "IP Address",    "formula": r"$\mathrm{IPv4:\ 32\ bits\ =\ 4\ octets}$",         "diagram": "bridge",  "note": "e.g. 192.168.1.1"},
            {"label": "Bandwidth",     "formula": r"$BW = \dfrac{\mathrm{Data}}{\mathrm{Time}}$",   "diagram": "wire",    "note": "bps / kbps / Mbps"},
            {"label": "OSI Layers",    "formula": r"$7\rightarrow 1:\ \mathrm{App\ to\ Physical}$",      "diagram": "loop",    "note": "7 layer model"},
            {"label": "HTTP vs HTTPS", "formula": r"$\mathrm{HTTPS = HTTP + TLS}$",           "diagram": "ohm",     "note": "Port 443 vs 80"},
            {"label": "URL structure", "formula": r"$\mathrm{protocol://domain/path}$",     "diagram": "power",   "note": "Uniform Res. Locator"},
        ],
    },

    "python_basics": {
        "subject": "CS", "chapter_tag": "Class XI-XII",
        "title_line1": "Python", "title_line2": "Quick Reference",
        "board_note": "5-6 marks · Practical + Theory",
        "hashtags": "#ComputerScience #Python #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "List slicing",  "formula": r"$\mathrm{list[start:stop:step]}$",           "diagram": "wire",    "note": "0-indexed"},
            {"label": "List comp.",    "formula": r"$[f(x) \text{ for } x \text{ in list}]$",  "diagram": "loop",    "note": "Concise loops"},
            {"label": "dict get",      "formula": r"$d.get(k,\ \mathrm{default})$",               "diagram": "bridge",  "note": "No KeyError"},
            {"label": "Lambda",        "formula": r"$\lambda x: x^2$",                         "diagram": "ohm",     "note": "Anonymous fn"},
            {"label": "File I/O",      "formula": r"$\mathrm{open(f,}'r') as fh:}$",         "diagram": "flux",    "note": "Context manager"},
        ],
    },

    "dbms": {
        "subject": "CS", "chapter_tag": "Chapter 7 · Class XII",
        "title_line1": "Database", "title_line2": "Management",
        "board_note": "4-5 marks · Board Exam",
        "hashtags": "#ComputerScience #DBMS #SQL #CBSE #BoardExam2027 #ClassXII",
        "rows": [
            {"label": "SELECT",        "formula": r"$\mathrm{SELECT\ col\ FROM\ tbl}$",   "diagram": "ohm",     "note": "Query"},
            {"label": "JOIN",          "formula": r"$\mathrm{INNER/LEFT/RIGHT\ JOIN}$",     "diagram": "bridge",  "note": "Combine tables"},
            {"label": "GROUP BY",      "formula": r"$\mathrm{SELECT\ col,AGG()\ GROUP\ BY}$",   "diagram": "loop",    "note": "Aggregate"},
            {"label": "Primary Key",   "formula": r"$\mathrm{Unique\ +\ NOT\ NULL}$",        "diagram": "power",   "note": "Entity integrity"},
            {"label": "Foreign Key",   "formula": r"$\mathrm{References\ PK\ of\ table}$",  "diagram": "flux",    "note": "Referential integrity"},
        ],
    },

}
