"""Batch 02 — Class 12 Biology: one paper's worth (plus spare) of questions. Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("biology12")
SR, HR, RH, PI, MB = "Sexual Reproduction in Flowering Plants", "Human Reproduction", "Reproductive Health", "Principles of Inheritance and Variation", "Molecular Basis of Inheritance"
EV, HD, MW, BP, BA = "Evolution", "Human Health and Disease", "Microbes in Human Welfare", "Biotechnology: Principles and Processes", "Biotechnology and its Applications"
OP, ES, BC = "Organisms and Populations", "Ecosystem", "Biodiversity and Conservation"

# ── SECTION A — MCQ ──
b.m("A", SR, "How many meiotic divisions are required to produce 100 pollen grains?", "100", "25", "50", "400", "B")
b.m("A", SR, "In angiosperms, triple fusion results in the formation of the:", "zygote", "embryo sac", "primary endosperm nucleus", "seed coat", "C")
b.m("A", HR, "Ovulation in the human female is triggered by a surge in the level of:", "luteinising hormone", "progesterone", "prolactin", "oxytocin", "A")
b.m("A", HR, "Fertilisation in human beings normally takes place in the:", "uterus", "cervix", "ovary", "ampullary region of the fallopian tube", "D")
b.m("A", RH, "The copper ions released by a Copper-T mainly act by:", "preventing ovulation", "suppressing the motility and fertilising capacity of sperms", "blocking the fallopian tubes", "increasing the secretion of oestrogen", "B")
b.m("A", PI, "A heterozygous tall pea plant is crossed with a dwarf pea plant. The ratio of tall to dwarf plants in the progeny will be:", "3 : 1", "1 : 2", "1 : 1", "All tall", "C")
b.m("A", PI, "The AB blood group in human beings is an example of:", "codominance", "incomplete dominance", "polygenic inheritance", "pleiotropy", "A")
b.m("A", MB, "If a double-stranded DNA molecule has 20% adenine, the percentage of cytosine in it will be:", "20%", "40%", "60%", "30%", "D")
b.m("A", MB, "The enzyme that joins the Okazaki fragments during DNA replication is:", "DNA polymerase", "DNA ligase", "helicase", "primase", "B")
b.m("A", MB, "Which of the following codons acts as the start codon and also codes for methionine?", "UAA", "UGA", "AUG", "UAG", "C")
b.m("A", EV, "The variety of beaks seen in Darwin's finches of the Galapagos Islands is an example of:", "adaptive radiation", "convergent evolution", "genetic drift", "saltation", "A")
b.m("A", HD, "The most serious form of malaria, called malignant malaria, is caused by:", "Plasmodium vivax", "Plasmodium malariae", "Plasmodium ovale", "Plasmodium falciparum", "D")
b.m("A", HD, "The antibody present in abundance in colostrum, which protects the newborn, is:", "IgG", "IgA", "IgM", "IgE", "B")
b.m("A", MW, "Which microorganism is used for the commercial production of citric acid?", "Acetobacter aceti", "Lactobacillus", "Aspergillus niger", "Saccharomyces cerevisiae", "C")
b.m("A", BP, "The restriction enzyme EcoRI recognises and cuts the DNA sequence:", "GAATTC", "GGATCC", "AAGCTT", "CTGCAG", "A")
b.m("A", BA, "The cry genes used to make Bt cotton resistant to bollworms were obtained from:", "Agrobacterium tumefaciens", "Bacillus thuringiensis", "Escherichia coli", "Bacillus subtilis", "B")
b.m("A", OP, "The interaction between two species in which one is benefited and the other is neither benefited nor harmed is called:", "mutualism", "parasitism", "amensalism", "commensalism", "D")
b.m("A", ES, "Which of the following ecological pyramids is always upright?", "Pyramid of numbers", "Pyramid of biomass", "Pyramid of energy", "Both pyramid of numbers and pyramid of biomass", "C")
b.m("A", BC, "Which of the following is an example of in situ conservation?", "National park", "Botanical garden", "Seed bank", "Zoological park", "A")

b.ar("A", MB, "The replication of DNA is semi-conservative.", "Each new DNA molecule has one parental strand and one newly synthesised strand.", "A")
b.ar("A", HD, "Vaccination provides passive immunity to the body.", "A vaccine contains antigens that stimulate the body to produce antibodies and memory cells.", "D")
b.ar("A", BC, "Tropical regions have a greater diversity of species than temperate regions.", "Tropical regions have remained relatively undisturbed for millions of years and so had a long time for species to evolve.", "A")

# ── SECTION B — VSA ──
b.q("VSA", "B", SR, "Differentiate between geitonogamy and xenogamy. Why is geitonogamy genetically similar to autogamy?")
b.q("VSA", "B", HR, "State the role of (a) Leydig cells and (b) Sertoli cells in the human testis.")
b.q("VSA", "B", PI, "A colour-blind man marries a woman with normal vision whose father was colour-blind. With the help of a cross, find the probability of their son being colour-blind.")
b.q("VSA", "B", MW, "What are biofertilisers? Give two examples and state how each enriches the soil.\nOR\nWhat are methanogens? State their role in the production of biogas.")
b.q("VSA", "B", BC, "What is meant by 'the Evil Quartet' in relation to the loss of biodiversity? Name its four components.")

# ── SECTION C — SA ──
b.q("SA", "C", SR, "Describe the development of the female gametophyte (embryo sac) in an angiosperm, starting from the megaspore mother cell. Why is the mature embryo sac described as 7-celled and 8-nucleate?")
b.q("SA", "C", RH, "What are assisted reproductive technologies? Briefly explain any three such techniques that help infertile couples to have children.")
b.q("SA", "C", MB, "Describe the experiment of Hershey and Chase. What conclusion was drawn from it?")
b.q("SA", "C", MB, "Explain how the lac operon of E. coli is regulated (a) in the absence of lactose and (b) in the presence of lactose.")
b.q("SA", "C", EV, "(a) State the Hardy-Weinberg principle.\n(b) List any four factors that affect the Hardy-Weinberg equilibrium.\n(c) In a population in equilibrium, 16% of the individuals show the recessive trait (aa). Find the frequency of the dominant allele and the percentage of heterozygous individuals.")
b.q("SA", "C", HD, "Describe the stages of the life cycle of Plasmodium that take place in the human body. What causes the chill and high fever that recur every three to four days in malaria?")
b.q("SA", "C", BP, "Explain the three steps of each cycle of the polymerase chain reaction (PCR). Why is Taq polymerase used in this technique?")
b.q("SA", "C", ES, "(a) What is an ecological pyramid?\n(b) Why is the pyramid of biomass in a sea generally inverted?\n(c) State two limitations of ecological pyramids.")

# ── SECTION D — CASE STUDY ──
b.q("CBQ", "D", BA, "People with diabetes need regular doses of insulin. Earlier, insulin was extracted from the pancreas of slaughtered cattle and pigs. Human insulin is made of two short polypeptide chains, chain A and chain B, linked by disulphide bridges. In the body it is first made as a pro-hormone that contains an extra stretch called the C peptide, which is removed during maturation. In 1983, an American company prepared two DNA sequences corresponding to the A and B chains of human insulin and introduced them into plasmids of E. coli. The two chains were produced separately, extracted and combined to form human insulin.\n(a) State one problem caused by the use of insulin obtained from animal sources.\n(b) What is the C peptide? Is it present in mature insulin?\n(c) Why was it an advantage to produce chains A and B separately in E. coli?\nOR\n(c) What is gene therapy? Name the genetic disorder for which it was first used, and the enzyme that is deficient in this disorder.")
b.q("CBQ", "D", OP, "A small herd of deer was introduced on an island that had plenty of grass and no predators. For the first few years the number of deer increased slowly, then it rose very rapidly. As the herd grew larger, grass became scarce, and the growth slowed down. Finally the population became almost steady at about 1000 deer, the largest number that the island could support. When ecologists plotted the number of deer against time, they obtained an S-shaped curve.\n(a) What name is given to the maximum population size that a habitat can support?\n(b) Write the equation that describes this type of population growth and name the type of growth.\n(c) Why can a population not keep growing exponentially for a long time in nature?\nOR\n(c) At a time when the island had 200 deer, the intrinsic rate of natural increase was 0.1 per year. Using K = 1000, calculate the rate of growth of the population (dN/dt) at that time.")

# ── SECTION E — LA ──
b.q("LA", "E", HR, "(a) Describe the process of spermatogenesis in human beings with the help of a schematic diagram.\n(b) Explain the role of the hormones that regulate this process.\n(c) Draw a labelled diagram of a human sperm.\nOR\n(a) Describe the events of the menstrual cycle in the ovary and in the uterus.\n(b) Explain the role of the pituitary and ovarian hormones in regulating the cycle.\n(c) What is the fate of the corpus luteum if fertilisation does not occur?")
b.q("LA", "E", PI, "(a) State Mendel's law of independent assortment. Explain it with the help of a dihybrid cross between pea plants having round yellow seeds (RRYY) and wrinkled green seeds (rryy), up to the F₂ generation.\n(b) How did Morgan explain the deviation from this law in his experiments on Drosophila? Define linkage and recombination.\nOR\n(a) Explain the mechanism of sex determination in (i) human beings and (ii) honey bees.\n(b) Haemophilia is a sex-linked recessive disorder. Explain why it is much more common in males than in females.\n(c) What is aneuploidy? Give one example of a disorder caused by it.")
b.q("LA", "E", BP, "(a) List the main steps involved in recombinant DNA technology, from the isolation of DNA to the production of the desired product.\n(b) Explain how recombinant colonies can be distinguished from non-recombinant colonies by insertional inactivation of an enzyme.\n(c) What is a bioreactor? State two conditions that it provides for the growth of the cells.\nOR\n(a) Distinguish between innate immunity and acquired immunity.\n(b) Draw a labelled diagram of an antibody molecule.\n(c) Describe how the human immunodeficiency virus (HIV) multiplies inside the body after infection and why the patient becomes prone to other infections.")

b.save()
