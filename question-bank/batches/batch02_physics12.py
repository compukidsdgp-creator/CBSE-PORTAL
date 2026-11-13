"""Batch 02 — Class 12 Physics: tops the pool up for one more paper. Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("physics12")
EC, EP, CE, MC, MM = "Electric Charges and Fields", "Electrostatic Potential and Capacitance", "Current Electricity", "Moving Charges and Magnetism", "Magnetism and Matter"
EM, AC, EW, RO, WO = "Electromagnetic Induction", "Alternating Current", "Electromagnetic Waves", "Ray Optics and Optical Instruments", "Wave Optics"
DN, AT, NU, SE = "Dual Nature of Radiation and Matter", "Atoms", "Nuclei", "Semiconductor Electronics"

# ── SECTION A — MCQ ──
b.m("A", EC, "The SI unit of electric flux is:", "N C⁻¹", "N m² C⁻¹", "C m⁻²", "V m⁻¹", "B")
b.m("A", EP, "Two capacitors, each of capacitance 6 μF, are connected in series. Their equivalent capacitance is:", "3 μF", "12 μF", "6 μF", "36 μF", "A")
b.m("A", CE, "When the temperature of a metallic conductor is increased, its resistivity:", "decreases", "remains the same", "increases", "first decreases and then increases", "C")
b.m("A", MC, "Two long, straight, parallel wires carry currents in the same direction. The wires will:", "repel each other", "not exert any force on each other", "rotate about each other", "attract each other", "D")
b.m("A", EM, "The SI unit of magnetic flux is the:", "weber", "tesla", "henry", "gauss", "A")
b.m("A", EW, "The speed of electromagnetic waves in vacuum is given by:", "√(μ₀ε₀)", "1/√(μ₀ε₀)", "μ₀ε₀", "1/(μ₀ε₀)", "B")
b.m("A", RO, "The focal length of a convex lens of power +4 D is:", "4 cm", "40 cm", "25 cm", "0.25 cm", "C")
b.m("A", WO, "For constructive interference between two coherent waves of wavelength λ, the path difference must be: (n = 0, 1, 2, ...)", "nλ", "(2n + 1)λ/2", "(2n + 1)λ/4", "nλ/2", "A")
b.m("A", AT, "In Rutherford's α-particle scattering experiment, most of the α-particles passed through the gold foil undeflected. This shows that:", "the nucleus is positively charged", "electrons revolve around the nucleus", "the atom is electrically neutral", "most of the space inside an atom is empty", "D")
b.m("A", SE, "When a p-n junction is forward biased, the width of its depletion region:", "increases", "decreases", "remains the same", "becomes infinite", "B")

b.ar("A", AC, "A capacitor blocks direct current but allows alternating current to pass.", "The capacitive reactance is 1/(ωC), which becomes infinite when the angular frequency ω is zero.", "A")
b.ar("A", MM, "A paramagnetic material is weakly attracted by a magnet.", "Magnetic field lines always form closed loops.", "B")

# ── SECTION B — VSA ──
b.q("VSA", "B", EP, "What is an equipotential surface? Why is no work done in moving a charge from one point to another on such a surface? Draw the equipotential surfaces for a single point charge.")
b.q("VSA", "B", EM, "State Faraday's law of electromagnetic induction. A coil of 200 turns is placed in a magnetic field such that the flux through each turn changes from 0.02 Wb to 0.01 Wb in 0.1 s. Calculate the emf induced in the coil.")
b.q("VSA", "B", RO, "A convex lens made of glass of refractive index 1.5 has a focal length of 10 cm in air. Calculate its focal length when it is immersed in water of refractive index 4/3.")
b.q("VSA", "B", SE, "Draw the energy band diagrams of a conductor, a semiconductor and an insulator. How do they differ in the size of the energy gap?")
b.q("VSA", "B", DN, "Write the expression for the de Broglie wavelength of an electron accelerated from rest through a potential difference V. Calculate this wavelength for V = 100 V.")

# ── SECTION C — SA ──
b.q("SA", "C", EC, "Two point charges of +4 μC and +1 μC are placed 30 cm apart in air.\n(a) Find the point on the line joining them where the net electric field is zero.\n(b) If the +1 μC charge is replaced by a charge of −1 μC, where on the line through the charges will the electric field be zero?")
b.q("SA", "C", MC, "Derive an expression for the force per unit length between two long, straight, parallel conductors carrying currents I₁ and I₂ and separated by a distance d. Hence define one ampere.")
b.q("SA", "C", MC, "State the Biot-Savart law. Use it to derive an expression for the magnetic field at a point on the axis of a circular loop of radius R carrying a current I.")
b.q("SA", "C", WO, "(a) Write the condition for the minima in the diffraction pattern due to a single slit.\n(b) Light of wavelength 600 nm falls normally on a slit of width 0.2 mm and the diffraction pattern is seen on a screen 1 m away. Find the width of the central maximum.\n(c) How does the width of the central maximum change if the slit is made narrower?")
b.q("SA", "C", AT, "An electron in a hydrogen atom makes a transition from the n = 3 level to the n = 2 level.\n(a) Calculate the wavelength of the radiation emitted. (R = 1.097 × 10⁷ m⁻¹)\n(b) Name the spectral series to which this line belongs.\n(c) In which region of the electromagnetic spectrum does it lie?")
b.q("SA", "C", NU, "Define the mass defect and the binding energy of a nucleus. Calculate the binding energy per nucleon of a helium nucleus (⁴He).\n(Mass of hydrogen atom = 1.007825 u, mass of neutron = 1.008665 u, mass of helium atom = 4.002603 u, 1 u = 931.5 MeV/c²)")

# ── SECTION D — CASE STUDY ──
b.q("CBQ", "D", EM, "An induction cooktop has a coil of copper wire below its glass-ceramic surface. When a high-frequency alternating current is passed through the coil, a rapidly changing magnetic field is produced. If a steel or iron vessel is placed on the surface, this changing field induces circulating currents in the base of the vessel. These currents heat the vessel directly, while the cooktop surface itself stays fairly cool. A vessel made of glass does not get heated on such a cooktop.\n(a) What name is given to the circulating currents induced in the base of the vessel?\n(b) Why does a glass vessel not get heated on an induction cooktop?\n(c) State two other useful applications of these currents.\nOR\n(c) These currents are undesirable in the core of a transformer. Why? How are they reduced?")
b.q("CBQ", "D", DN, "Automatic doors in shopping malls and burglar alarms often use a photocell. In a photocell, light falls on a metal surface called the emitter and electrons are ejected from it. These electrons are collected by another electrode, so a current flows in the circuit. When a person blocks the beam of light, the current stops and a switch is operated. The emission starts only if the frequency of the light is above a certain minimum value for that metal, and it begins almost instantly.\n(a) Define the work function of a metal.\n(b) How does the photoelectric current change when the intensity of the incident light is increased, keeping its frequency the same? What happens to the stopping potential?\n(c) The graph of stopping potential against the frequency of the incident light is a straight line. What does its slope represent?\nOR\n(c) The work function of a metal is 2.48 eV. Calculate its threshold wavelength. (Take hc = 1240 eV nm)")

# ── SECTION E — LA ──
b.q("LA", "E", EC, "(a) State Gauss's law in electrostatics.\n(b) Use it to derive expressions for the electric field due to a uniformly charged thin spherical shell at a point (i) outside the shell and (ii) inside the shell.\n(c) A thin spherical shell of radius 10 cm carries a charge of 20 μC. Calculate the electric field at a point 20 cm from its centre. (1/4πε₀ = 9 × 10⁹ N m² C⁻²)\nOR\n(a) Derive an expression for the torque acting on an electric dipole placed in a uniform electric field.\n(b) Derive an expression for the potential energy of the dipole in this field.\n(c) An electric dipole of dipole moment 4 × 10⁻⁹ C m is placed at an angle of 30° with a uniform electric field of 5 × 10⁴ N/C. Calculate the torque acting on it.")
b.q("LA", "E", AC, "(a) A resistor R, an inductor L and a capacitor C are connected in series to an a.c. source. Using a phasor diagram, derive an expression for the impedance of the circuit.\n(b) State the condition for resonance in this circuit.\n(c) In a series LCR circuit, R = 40 Ω, the inductive reactance is 70 Ω and the capacitive reactance is 40 Ω. It is connected to a 200 V (rms) a.c. source. Find the impedance, the rms current and the average power consumed.\nOR\n(a) Define the mutual inductance of a pair of coils and write its SI unit.\n(b) Derive an expression for the mutual inductance of two long coaxial solenoids of the same length wound one over the other.\n(c) The current in one coil changes from 0 to 20 A in 0.5 s. If the mutual inductance of the pair is 1.5 H, find the emf induced in the other coil.")
b.q("LA", "E", RO, "(a) Derive the relation between the object distance, the image distance and the radius of curvature for refraction at a convex spherical surface, when light travels from a rarer medium of refractive index n₁ to a denser medium of refractive index n₂.\n(b) Use this relation to obtain the lens maker's formula.\n(c) A double convex lens is made of glass of refractive index 1.5. Both its faces have a radius of curvature of 20 cm. Find its focal length.\nOR\n(a) In Young's double slit experiment, derive the expression for the fringe width.\n(b) State two conditions for the interference pattern to be clearly visible.\n(c) What happens to the fringe width if the whole apparatus is immersed in water? Give a reason.")

b.save()
