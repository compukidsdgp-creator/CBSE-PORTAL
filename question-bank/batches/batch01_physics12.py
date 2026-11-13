"""Batch 01 — Class 12 Physics: one paper's worth (plus spare) of original questions. Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("physics12")
EC, EP, CE, MC, MM = "Electric Charges and Fields", "Electrostatic Potential and Capacitance", "Current Electricity", "Moving Charges and Magnetism", "Magnetism and Matter"
EM, AC, EW, RO, WO = "Electromagnetic Induction", "Alternating Current", "Electromagnetic Waves", "Ray Optics and Optical Instruments", "Wave Optics"
DN, AT, NU, SE = "Dual Nature of Radiation and Matter", "Atoms", "Nuclei", "Semiconductor Electronics"

# ── SECTION A — MCQ ──
b.m("A", EC, "The force between two point charges kept at a distance r apart is F. If the distance is doubled and one of the charges is also doubled, the force becomes:", "2F", "F/2", "F/4", "4F", "B")
b.m("A", EC, "A closed surface encloses an electric dipole. The net electric flux through the surface is:", "zero", "q/ε₀", "2q/ε₀", "−q/ε₀", "A")
b.m("A", EP, "A capacitor is charged by a battery and then disconnected. A dielectric slab of dielectric constant K is now inserted to fill the space between the plates. The energy stored in the capacitor becomes:", "K times", "K² times", "1/K times", "unchanged", "C")
b.m("A", EP, "The work done in moving a charge of 2 C between two points on an equipotential surface is:", "2 J", "4 J", "infinite", "zero", "D")
b.m("A", CE, "The potential difference across a conductor of fixed length is doubled. The drift velocity of the electrons will:", "be halved", "be doubled", "remain the same", "become four times", "B")
b.m("A", CE, "Kirchhoff's junction rule is a consequence of the conservation of:", "charge", "energy", "momentum", "mass", "A")
b.m("A", MC, "A charged particle enters a uniform magnetic field with its velocity parallel to the field. The path of the particle is:", "a circle", "a helix", "a straight line", "a parabola", "C")
b.m("A", MC, "A proton moves in a circle of radius r in a uniform magnetic field with speed v. If its speed is doubled, the radius of the path becomes:", "r/2", "2r", "4r", "r", "B")
b.m("A", MM, "The magnetic susceptibility of a diamagnetic material is:", "large and positive", "small and positive", "large and negative", "small and negative", "D")
b.m("A", EM, "Lenz's law is a consequence of the law of conservation of:", "charge", "momentum", "energy", "mass", "C")
b.m("A", AC, "In an a.c. circuit containing only an inductor, the current:", "lags behind the voltage by π/2", "leads the voltage by π/2", "is in phase with the voltage", "leads the voltage by π", "A")
b.m("A", AC, "The power factor of a series LCR circuit at resonance is:", "zero", "0.5", "0.707", "1", "D")
b.m("A", EW, "Which of the following electromagnetic waves has the highest frequency?", "Microwaves", "Gamma rays", "Ultraviolet rays", "X-rays", "B")
b.m("A", RO, "The critical angle for a medium of refractive index 2, with respect to air, is:", "30°", "45°", "60°", "90°", "A")
b.m("A", WO, "In Young's double slit experiment, the separation between the slits is halved and the distance of the screen from the slits is doubled. The fringe width becomes:", "half", "double", "unchanged", "four times", "D")
b.m("A", DN, "The energy of a photon of wavelength λ is E. The energy of a photon of wavelength λ/2 is:", "E/2", "E", "2E", "4E", "C")
b.m("A", AT, "The radius of the first orbit of the hydrogen atom is r₀. According to Bohr's model, the radius of the second orbit is:", "2r₀", "4r₀", "r₀/2", "8r₀", "B")
b.m("A", NU, "The density of nuclear matter is:", "independent of the mass number", "proportional to the mass number", "inversely proportional to the mass number", "proportional to the cube of the mass number", "A")
b.m("A", SE, "In an n-type semiconductor, the majority charge carriers and the type of dopant atoms are respectively:", "holes, trivalent", "holes, pentavalent", "electrons, pentavalent", "electrons, trivalent", "C")

b.ar("A", EP, "The electric field inside a conductor is zero under electrostatic conditions.", "The free charges of a conductor rearrange themselves until the net electric field inside it becomes zero.", "A")
b.ar("A", DN, "Photoelectric emission does not take place below the threshold frequency, however intense the incident light may be.", "The energy of a photon depends on the intensity of the incident light.", "C")
b.ar("A", NU, "Nuclear forces are charge independent.", "Nuclear forces are much stronger than the Coulomb force between protons inside a nucleus.", "B")

# ── SECTION B — VSA ──
b.q("VSA", "B", EC, "Define the electric dipole moment and state its direction and SI unit. What are the net force and the torque on an electric dipole placed parallel to a uniform electric field?")
b.q("VSA", "B", CE, "Two wires A and B of the same material have their lengths in the ratio 1 : 2 and their radii in the ratio 2 : 1. Find the ratio of their resistances.")
b.q("VSA", "B", MC, "Write the expression for the magnetic moment of a current-carrying loop. A circular coil of 100 turns and radius 10 cm carries a current of 2 A. Calculate its magnetic moment.")
b.q("VSA", "B", EW, "Name the electromagnetic waves that are used (a) in radar systems for aircraft navigation and (b) for killing germs in water purifiers. Write one more use of each.\nOR\nHow are electromagnetic waves produced? Write the relation between the amplitudes of the electric and magnetic fields in an electromagnetic wave in vacuum.")
b.q("VSA", "B", WO, "State two conditions necessary for obtaining a sustained interference pattern. Why can two independent sodium lamps not produce such a pattern?")
b.q("VSA", "B", AT, "The energy of an electron in the ground state of the hydrogen atom is −13.6 eV. Find its kinetic energy and its potential energy in the first excited state.")

# ── SECTION C — SA ──
b.q("SA", "C", EC, "Using Gauss's law, derive an expression for the electric field at a point due to an infinitely long, straight, uniformly charged wire. How does this field vary with the distance from the wire?")
b.q("SA", "C", EP, "Derive an expression for the capacitance of a parallel plate capacitor with air between its plates. How does the capacitance change if the separation between the plates is doubled and a slab of dielectric constant 4 fills the space between them?")
b.q("SA", "C", CE, "State the principle of a Wheatstone bridge. Using Kirchhoff's rules, obtain the condition for the bridge to be balanced.")
b.q("SA", "C", EM, "Define the self-inductance of a coil and write its SI unit. Derive an expression for the self-inductance of a long solenoid of length l, area of cross-section A and N turns.")
b.q("SA", "C", AC, "A series LCR circuit has L = 0.5 H, C = 8 μF and R = 25 Ω, and is connected to a variable-frequency a.c. source of 100 V (rms). Calculate:\n(a) the angular frequency at which resonance occurs,\n(b) the rms current at resonance, and\n(c) the quality factor of the circuit.")
b.q("SA", "C", RO, "A ray of light passes through a triangular glass prism of refracting angle A. Draw the ray diagram and derive the relation between the refractive index of the prism, the angle of the prism and the angle of minimum deviation.")
b.q("SA", "C", DN, "Light of wavelength 400 nm is incident on a metal surface of work function 2.0 eV. Calculate:\n(a) the energy of the incident photon in eV,\n(b) the maximum kinetic energy of the emitted photoelectrons, and\n(c) the stopping potential.\n(Take hc = 1240 eV nm)")
b.q("SA", "C", NU, "Draw the graph showing the variation of binding energy per nucleon with mass number. Using this graph, explain why energy is released in (a) nuclear fission and (b) nuclear fusion.")
b.q("SA", "C", SE, "Draw the circuit diagram of a full-wave rectifier using two p-n junction diodes. Explain its working and show the input and output waveforms.")

# ── SECTION D — CASE STUDY ──
b.q("CBQ", "D", MC, "A magnetic resonance imaging (MRI) machine in a hospital needs a strong and uniform magnetic field. This field is produced by a long solenoid, which is a wire wound closely in the form of a helix. When a current flows through it, the magnetic field inside the solenoid is nearly uniform and parallel to its axis, while the field outside is very weak. The field can be made stronger by increasing the current, by increasing the number of turns per unit length, or by using a suitable core.\n(a) Write the expression for the magnetic field inside a long solenoid carrying a current I and having n turns per unit length.\n(b) A solenoid has 2000 turns per metre and carries a current of 5 A. Calculate the magnetic field inside it. (μ₀ = 4π × 10⁻⁷ T m A⁻¹)\n(c) Why is the magnetic field outside a long solenoid nearly zero?\nOR\n(c) How does the magnetic field inside the solenoid change when a soft iron core is inserted in it? Give a reason.")
b.q("CBQ", "D", RO, "Optical fibres carry telephone and internet signals as pulses of light over long distances. A fibre has a central glass core surrounded by a cladding made of glass of a different refractive index. Light entering the core at a suitable angle strikes the core-cladding boundary again and again and is reflected back each time without any loss, so the signal travels along the fibre even when the fibre is bent.\n(a) Name the phenomenon on which the working of an optical fibre is based and state the two conditions necessary for it.\n(b) The refractive index of the core is 1.5 and that of the cladding is 1.2. Calculate the sine of the critical angle for the core-cladding boundary.\n(c) Why must the refractive index of the cladding be less than that of the core?\nOR\n(c) State two advantages of optical fibres over copper cables for communication.")

# ── SECTION E — LA ──
b.q("LA", "E", AC, "(a) State the principle of a transformer and explain its working with a labelled diagram.\n(b) Why is the core of a transformer laminated?\n(c) A step-down transformer converts 2200 V to 220 V. Its primary coil has 3000 turns. Find the number of turns in the secondary coil. If the output power is 4.4 kW and the transformer is ideal, find the current in the primary coil.\nOR\n(a) Describe the principle and working of an a.c. generator with a labelled diagram.\n(b) Obtain the expression for the emf induced in the rotating coil.\n(c) A coil of 100 turns and area 0.1 m² rotates at 50 revolutions per second in a uniform magnetic field of 0.02 T. Find the maximum emf generated.")
b.q("LA", "E", RO, "(a) Draw a labelled ray diagram of a compound microscope for the final image formed at the least distance of distinct vision. Obtain the expression for its magnifying power.\n(b) A convex lens of focal length 20 cm is placed in contact with a concave lens of focal length 30 cm. Find the power and the focal length of the combination.\nOR\n(a) Draw a labelled ray diagram of an astronomical telescope in normal adjustment and write the expression for its magnifying power.\n(b) State two advantages of a reflecting telescope over a refracting telescope.\n(c) An astronomical telescope has an objective of focal length 150 cm and an eyepiece of focal length 5 cm. Find its magnifying power and the length of the tube in normal adjustment.")
b.q("LA", "E", CE, "(a) Define the drift velocity of electrons in a conductor. Derive the relation between the current and the drift velocity.\n(b) Hence obtain an expression for the resistivity of the conductor in terms of the number density of electrons and the relaxation time.\n(c) A copper wire of area of cross-section 1.0 × 10⁻⁶ m² carries a current of 1.6 A. If the number density of free electrons is 8 × 10²⁸ m⁻³, calculate the drift velocity. (e = 1.6 × 10⁻¹⁹ C)\nOR\n(a) Derive an expression for the electric potential at a point on the axial line of an electric dipole.\n(b) What is the potential at any point on the equatorial line of the dipole?\n(c) Two charges of +2 μC and −2 μC are placed 6 cm apart. Calculate the potential at a point on the axial line at a distance of 9 cm from the centre of the dipole.")

b.save()
