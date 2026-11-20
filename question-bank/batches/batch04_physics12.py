"""Batch 04 — Class 12 Physics: tops the pool up for one more paper (plus spares). Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("physics12")
EC, EP, CE, MC, MM = "Electric Charges and Fields", "Electrostatic Potential and Capacitance", "Current Electricity", "Moving Charges and Magnetism", "Magnetism and Matter"
EM, AC, EW, RO, WO = "Electromagnetic Induction", "Alternating Current", "Electromagnetic Waves", "Ray Optics and Optical Instruments", "Wave Optics"
DN, AT, NU, SE = "Dual Nature of Radiation and Matter", "Atoms", "Nuclei", "Semiconductor Electronics"

# ── SECTION A — MCQ ──
b.m("A", EC, "A point charge Q is placed at the centre of a cube. The electric flux through any one face of the cube is:", "Q/ε₀", "Q/(6ε₀)", "6Q/ε₀", "Q/(4ε₀)", "B")
b.m("A", EC, "The magnitude of the electric field near an infinite plane sheet of charge with uniform surface charge density σ is:", "σ/(2ε₀)", "σ/ε₀", "2σ/ε₀", "σ/(4ε₀)", "A")
b.m("A", EP, "A capacitor of capacitance 4 μF is charged to a potential difference of 50 V. The energy stored in it is:", "1 × 10⁻² J", "2.5 × 10⁻³ J", "2 × 10⁻⁴ J", "5 × 10⁻³ J", "D")
b.m("A", EP, "The electric potential at a distance of 0.3 m from a point charge of 2 nC in air is: (1/4πε₀ = 9 × 10⁹ N m² C⁻²)", "6 V", "60 V", "600 V", "18 V", "B")
b.m("A", CE, "A cell of emf 2 V and internal resistance 0.5 Ω is connected across a 3.5 Ω resistor. The potential difference across the terminals of the cell is:", "2 V", "0.25 V", "1.75 V", "1.5 V", "C")
b.m("A", CE, "The SI unit of the mobility of charge carriers is:", "m² V⁻¹ s⁻¹", "m s⁻¹", "V m⁻¹ s", "m V⁻¹ s⁻²", "A")
b.m("A", MC, "The work done by the magnetic force on a charged particle moving in a uniform magnetic field is:", "qvB", "qvBr", "maximum when the velocity is perpendicular to the field", "always zero", "D")
b.m("A", MC, "The magnitude of the magnetic field at the centre of a circular loop of radius R carrying a current I is:", "μ₀I/(2πR)", "μ₀I/(2R)", "μ₀I/(4R)", "μ₀IR/2", "B")
b.m("A", MM, "Which of the following materials is ferromagnetic?", "Copper", "Aluminium", "Nickel", "Bismuth", "C")
b.m("A", EM, "A metal rod of length 0.5 m moves with a speed of 4 m/s perpendicular to a uniform magnetic field of 0.2 T. The emf induced across its ends is:", "0.4 V", "4 V", "0.1 V", "1.6 V", "A")
b.m("A", AC, "The peak value of the household a.c. voltage is about 311 V. Its rms value is about:", "311 V", "440 V", "220 V", "155 V", "C")
b.m("A", EW, "The electromagnetic waves used in the remote controls of television sets are:", "microwaves", "X-rays", "ultraviolet rays", "infrared rays", "D")
b.m("A", RO, "When light travels from glass into air, total internal reflection takes place if the angle of incidence in glass is:", "less than the critical angle", "zero", "greater than the critical angle", "of any value", "C")
b.m("A", WO, "According to Huygens' principle, every point on a wavefront acts as:", "a sink of energy", "a source of secondary wavelets", "a reflecting surface", "a point of zero disturbance", "B")
b.m("A", DN, "The de Broglie wavelength of a particle having momentum p is: (h is Planck's constant)", "h/p", "hp", "p/h", "h/(2p)", "A")
b.m("A", NU, "The radius of the nucleus of ²⁷Al is R. The radius of the nucleus of ⁶⁴Cu is approximately:", "2R", "3R/4", "64R/27", "4R/3", "D")
b.m("A", SE, "At absolute zero temperature, a crystal of pure silicon behaves as:", "an insulator", "a good conductor", "an n-type semiconductor", "a p-type semiconductor", "A")
b.m("A", AT, "According to Bohr's model, the ratio of the radius of the third orbit to that of the first orbit of the hydrogen atom is:", "3 : 1", "1 : 3", "9 : 1", "1 : 9", "C")

b.ar("A", MC, "A charged particle moving parallel to a uniform magnetic field experiences no magnetic force.", "The magnetic force on a moving charge is always perpendicular to its velocity.", "B")
b.ar("A", DN, "The maximum kinetic energy of the emitted photoelectrons increases when the intensity of the incident light is increased.", "The number of photoelectrons emitted per second is proportional to the intensity of the incident light.", "D")
b.ar("A", WO, "In Young's double slit experiment, the fringe width increases when blue light is replaced by red light.", "The wavelength of red light is shorter than that of blue light.", "C")

# ── SECTION B — VSA ──
b.q("VSA", "B", CE, "State Kirchhoff's loop rule. A battery of emf 12 V and internal resistance 1 Ω is connected to two resistors of 3 Ω and 2 Ω joined in series. Find the current in the circuit and the potential difference across the 3 Ω resistor.")
b.q("VSA", "B", MM, "Distinguish between diamagnetic and paramagnetic materials on the basis of (a) the sign and magnitude of their magnetic susceptibility and (b) their behaviour in a non-uniform magnetic field. Give one example of each.")
b.q("VSA", "B", AC, "Define inductive reactance. A pure inductor of inductance (1/π) H is connected to a 220 V (rms), 50 Hz a.c. supply. Find its reactance and the rms current in the circuit.")
b.q("VSA", "B", NU, "Distinguish between nuclear fission and nuclear fusion. Why is an extremely high temperature needed for nuclear fusion to take place?")

# ── SECTION C — SA ──
b.q("SA", "C", EP, "Three capacitors of capacitances 2 μF, 3 μF and 6 μF are connected in series across a 12 V battery. Calculate:\n(a) the equivalent capacitance of the combination,\n(b) the charge on each capacitor,\n(c) the potential difference across the 6 μF capacitor and the total energy stored.")
b.q("SA", "C", CE, "Two cells of emf E₁ and E₂ and internal resistances r₁ and r₂ are connected in parallel, with their positive terminals joined together. Derive expressions for the equivalent emf and the equivalent internal resistance of the combination.")
b.q("SA", "C", MC, "(a) Derive an expression for the torque acting on a rectangular current-carrying loop placed in a uniform magnetic field.\n(b) A coil of 50 turns, each of area 4 × 10⁻³ m², carries a current of 2 A. It is placed in a uniform magnetic field of 0.5 T with its normal making an angle of 30° with the field. Calculate the torque on the coil.")
b.q("SA", "C", EW, "(a) What is displacement current? Why was it necessary for Maxwell to introduce it?\n(b) Write the Ampere-Maxwell law.\n(c) State two characteristics of electromagnetic waves.")
b.q("SA", "C", RO, "A thin convex lens of focal length 20 cm is placed in contact with a thin concave lens of focal length 30 cm.\n(a) Find the focal length and the power of the combination.\n(b) An object is placed 90 cm in front of the combination. Find the position of the image and the magnification produced.")
b.q("SA", "C", AT, "Using Bohr's postulates, derive an expression for the total energy of the electron in the nth orbit of the hydrogen atom. What is the significance of the negative sign in this expression?")
b.q("SA", "C", SE, "(a) Explain how the depletion region and the potential barrier are formed in a p-n junction.\n(b) Draw the V-I characteristics of a p-n junction diode in forward bias and in reverse bias, and explain the shape of each.")

# ── SECTION D — CASE STUDY ──
b.q("CBQ", "D", EP, "A defibrillator is a medical device that gives a short, strong electric shock to the heart of a patient whose heart has stopped beating normally. Inside the device, a capacitor is charged to a high voltage and then discharged through the patient's chest within a few milliseconds. In one such device, a 50 μF capacitor is charged to 2000 V.\n(a) Calculate the energy stored in the capacitor.\n(b) If the capacitor is charged to only 1000 V, what will be the energy stored?\n(c) Calculate the charge stored on the capacitor when it is charged to 2000 V.\nOR\n(c) How would the capacitance change if the space between the plates were filled with a dielectric of dielectric constant 4? Give a reason.")
b.q("CBQ", "D", RO, "A school observatory has a refracting astronomical telescope. Its objective lens has a focal length of 100 cm and its eyepiece has a focal length of 5 cm. The students use it to look at the Moon and at Jupiter, with the final image formed at infinity (normal adjustment).\n(a) Calculate the magnifying power of the telescope in normal adjustment.\n(b) What is the distance between the objective and the eyepiece in this adjustment?\n(c) Why is the objective of a telescope made with a large aperture?\nOR\n(c) State two advantages of a reflecting telescope over a refracting telescope.")

# ── SECTION E — LA ──
b.q("LA", "E", EP, "(a) Derive an expression for the electric potential at a point at a distance r from the centre of a short electric dipole, along a line making an angle θ with the dipole axis.\n(b) Use it to show that the potential at any point on the equatorial line of the dipole is zero.\n(c) Two point charges of +3 nC and −2 nC are placed 10 cm apart in air. Find the point between them on the line joining them where the electric potential is zero.\nOR\n(a) Derive an expression for the energy stored in a charged capacitor.\n(b) Show that the energy density of the electric field between the plates of a parallel plate capacitor is ½ε₀E².\n(c) A 10 μF capacitor is charged to 100 V and disconnected from the battery. It is then connected across an uncharged 10 μF capacitor. Find the common potential and the loss of energy.")
b.q("LA", "E", EM, "(a) A straight conductor of length l slides with a constant velocity v on a pair of parallel rails placed in a uniform magnetic field B perpendicular to the plane of the rails. Derive an expression for the emf induced across the conductor.\n(b) If the total resistance of the circuit is R, obtain expressions for the force needed to keep the conductor moving and the power dissipated.\n(c) Calculate the induced emf, the current and the force needed if l = 0.2 m, B = 0.5 T, v = 10 m/s and R = 2 Ω.\nOR\n(a) Derive an expression for the energy stored in an inductor of self-inductance L carrying a current I.\n(b) Explain how Lenz's law is consistent with the law of conservation of energy.\n(c) The current in a coil of self-inductance 0.4 H falls steadily from 5 A to zero in 0.1 s. Find the emf induced in the coil and the energy that was stored in it at the start.")
b.q("LA", "E", WO, "(a) Using Huygens' principle, verify the laws of refraction for a plane wave travelling from a rarer medium into a denser medium.\n(b) What happens to the frequency, the wavelength and the speed of light when it passes from air into glass?\n(c) Light of wavelength 600 nm in air enters glass of refractive index 1.5. Find its wavelength and speed in the glass.\nOR\n(a) Derive the mirror formula for a concave mirror forming a real image.\n(b) An object is placed 15 cm in front of a concave mirror of focal length 10 cm. Find the position and the magnification of the image.\n(c) Why are concave mirrors used in torches and by dentists?")

b.save()
