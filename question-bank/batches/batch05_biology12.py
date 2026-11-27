"""Batch 05 — Class 12 Biology: one more paper's worth (plus spares). Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("biology12")
SR, HR, RH, PI, MB = "Sexual Reproduction in Flowering Plants", "Human Reproduction", "Reproductive Health", "Principles of Inheritance and Variation", "Molecular Basis of Inheritance"
EV, HD, MW, BP, BA = "Evolution", "Human Health and Disease", "Microbes in Human Welfare", "Biotechnology: Principles and Processes", "Biotechnology and its Applications"
OP, ES, BC = "Organisms and Populations", "Ecosystem", "Biodiversity and Conservation"

# ── SECTION A — MCQ ──
b.m("A", RH, "Which of the following is a surgical method of contraception in human males?", "Tubectomy", "Vasectomy", "Intra-uterine device", "Diaphragm", "B")
b.m("A", EV, "The theory of spontaneous generation of life was finally disproved by the experiments of:", "Oparin", "Charles Darwin", "Louis Pasteur", "Haldane", "C")
b.m("A", EV, "In a population in Hardy-Weinberg equilibrium, the frequency of allele A is 0.7. The frequency of heterozygous (Aa) individuals is:", "0.49", "0.21", "0.09", "0.42", "D")
b.m("A", MW, "Which of the following is used as a 'clot buster' to remove clots from the blood vessels of patients who have had a heart attack?", "Streptokinase", "Cyclosporin A", "Statins", "Lipase", "A")
b.m("A", MW, "The large holes in 'Swiss cheese' are due to the production of a large amount of carbon dioxide by the bacterium:", "Lactobacillus", "Saccharomyces cerevisiae", "Propionibacterium sharmanii", "Aspergillus niger", "C")
b.m("A", BP, "To release DNA from a fungal cell during the isolation of genetic material, the cell wall is broken down using the enzyme:", "lysozyme", "cellulase", "ribonuclease", "chitinase", "D")
b.m("A", BP, "During agarose gel electrophoresis, DNA fragments move through the gel towards the:", "cathode", "anode", "cathode or anode, depending on their size", "top of the gel, where they were loaded", "B")
b.m("A", BA, "The technique of ELISA, used for the early diagnosis of infections, is based on the principle of:", "antigen–antibody interaction", "DNA replication", "amplification of DNA by PCR", "separation of DNA by electrophoresis", "A")
b.m("A", OP, "An organism that can tolerate and thrive in a wide range of temperatures is described as:", "stenothermal", "eurythermal", "euryhaline", "stenohaline", "B")
b.m("A", ES, "The breakdown of detritus into smaller particles by detritivores such as earthworms is called:", "leaching", "catabolism", "humification", "fragmentation", "D")
b.m("A", BC, "In the species–area relationship, the value of the slope of the regression line (Z) on a logarithmic scale for most groups of organisms, regardless of the region, lies in the range:", "0.1 to 0.2", "0.6 to 1.2", "1.5 to 2.0", "2.5 to 3.0", "A")

# ── SECTION B — VSA ──
b.q("VSA", "B", RH, "Name any two sexually transmitted infections that can be completely cured if they are detected early and treated properly. State two simple measures that help in preventing sexually transmitted infections.")
b.q("VSA", "B", BA, "Bacillus thuringiensis produces a protein that kills certain insects. Why does this protein not kill the bacterium itself, and how does it become toxic inside the insect?")
b.q("VSA", "B", ES, "What is decomposition? Name two environmental factors that affect the rate of decomposition and state how each affects it.")
b.q("VSA", "B", EV, "What is adaptive radiation? Give one example of adaptive radiation other than Darwin's finches.")

# ── SECTION C — SA ──
b.q("SA", "C", BP, "(a) What is insertional inactivation?\n(b) Explain how insertional inactivation of the gene for the enzyme β-galactosidase helps in identifying recombinant bacterial colonies.\n(c) Why is this method preferred to selection based on the inactivation of an antibiotic resistance gene?")
b.q("SA", "C", MW, "(a) What is biogas? Name its main components.\n(b) Name the group of bacteria that produce biogas and mention one place where they are found naturally.\n(c) Briefly describe how cattle dung is used in a biogas plant.")
b.q("SA", "C", OP, "Write the equations for the exponential and the logistic growth of a population and explain the terms used. Sketch the growth curve in each case and state which model is more realistic, giving a reason.")
b.q("SA", "C", BC, "(a) What is meant by the invasion of alien species? Explain with two examples how it can cause the loss of native biodiversity.\n(b) What is co-extinction? Give one example.")
b.q("SA", "C", RH, "Explain how each of the following methods of contraception prevents pregnancy:\n(a) Oral contraceptive pills\n(b) Hormone-releasing intra-uterine devices\n(c) Barrier methods such as condoms and diaphragms")
b.q("SA", "C", BA, "(a) What is gene therapy?\n(b) Describe how gene therapy was used to treat a child suffering from adenosine deaminase (ADA) deficiency.\n(c) Why does this treatment not give a permanent cure, and what could make it permanent?")

# ── SECTION D — CASE STUDY ──
b.q("CBQ", "D", ES, "A group of students studied a grassland ecosystem near their school. They estimated that the grass plants fixed about 20,000 J of energy in a given area in one season. The grass is eaten by grasshoppers, the grasshoppers by frogs, the frogs by snakes, and the snakes by hawks. The students also noted that a single large banyan tree in the school garden supported thousands of insects, which in turn were eaten by a few birds.\n(a) Assuming the 10 per cent law, how much energy will be available to the snakes in the grassland food chain?\n(b) Why is the pyramid of energy always upright?\n(c) What is meant by the standing crop of a trophic level? How is it usually measured?\nOR\n(c) Why is the pyramid of numbers in the banyan tree ecosystem inverted?")
b.q("CBQ", "D", HD, "During a health camp, children were given the hepatitis B vaccine, which is produced in yeast using recombinant DNA technology. On the same day, a farmer who had been bitten by a snake was brought to the camp and was immediately given an injection of antivenom containing ready-made antibodies against the snake venom.\n(a) Name the type of acquired immunity developed in (i) the children and (ii) the farmer.\n(b) Why is the hepatitis B vaccine called a recombinant vaccine?\n(c) Which cells produce antibodies in the human body? Name the type of immune response they bring about.\nOR\n(c) Name the four types of barriers of innate immunity and give one example of each.")

# ── SECTION E — LA ──
b.q("LA", "E", EV, "(a) Describe the experiment performed by S. L. Miller in 1953. What did it show about the origin of life?\n(b) What are homologous and analogous organs? Explain how each of them provides evidence for divergent or convergent evolution, giving one example of each.\nOR\n(a) Explain stabilising, directional and disruptive natural selection, describing how the distribution of a trait in a population changes in each case.\n(b) What is genetic drift? What is meant by the founder effect?")
b.q("LA", "E", BA, "(a) What are transgenic animals? Explain any four ways in which transgenic animals are useful to human beings.\n(b) What is biopiracy? Why have some countries, including India, made laws to prevent it?\nOR\n(a) Explain how PCR and ELISA help in the early diagnosis of diseases.\n(b) What is the role of the Genetic Engineering Appraisal Committee (GEAC) in India?")
b.q("LA", "E", HD, "(a) Describe how HIV multiplies inside the human body after infection and how this leads to AIDS.\n(b) State three ways in which HIV is transmitted and three measures to prevent its spread.\nOR\n(a) What is cancer? Distinguish between benign and malignant tumours.\n(b) Name three types of agents that can cause cancer and describe two methods used for the detection of cancer.")

b.save()
