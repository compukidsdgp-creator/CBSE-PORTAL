"""Batch 03 — Class 12 Biology: one more paper's worth (plus spares). Run once."""
import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from mock_bank_add import Batch

b = Batch("biology12")
SR, HR, RH, PI, MB = "Sexual Reproduction in Flowering Plants", "Human Reproduction", "Reproductive Health", "Principles of Inheritance and Variation", "Molecular Basis of Inheritance"
EV, HD, MW, BP, BA = "Evolution", "Human Health and Disease", "Microbes in Human Welfare", "Biotechnology: Principles and Processes", "Biotechnology and its Applications"
OP, ES, BC = "Organisms and Populations", "Ecosystem", "Biodiversity and Conservation"

# ── SECTION A — MCQ ──
b.m("A", SR, "The innermost wall layer of the microsporangium, which nourishes the developing pollen grains, is the:", "endothecium", "middle layer", "epidermis", "tapetum", "D")
b.m("A", SR, "Which of the following is a post-fertilisation event in flowering plants?", "Pollination", "Embryogenesis", "Microsporogenesis", "Megasporogenesis", "B")
b.m("A", HR, "During pregnancy in human females, the hormone hCG is secreted by the:", "placenta", "anterior pituitary", "hypothalamus", "corpus albicans", "A")
b.m("A", RH, "Which of the following is a natural method of contraception?", "Vasectomy", "Copper-T", "Lactational amenorrhoea", "Oral contraceptive pills", "C")
b.m("A", PI, "In a cross between two heterozygous plants (Aa × Aa), the proportion of offspring that are homozygous is:", "1/4", "3/4", "1", "1/2", "D")
b.m("A", PI, "A disorder caused by the presence of an additional copy of chromosome number 21 is:", "Down's syndrome", "Turner's syndrome", "Klinefelter's syndrome", "phenylketonuria", "A")
b.m("A", MB, "In eukaryotes, the removal of introns from the hnRNA and the joining of exons in a defined order is called:", "capping", "tailing", "splicing", "replication", "C")
b.m("A", EV, "Which of the following pairs is an example of homologous organs?", "Wings of a butterfly and wings of a bird", "Thorn of Bougainvillea and tendril of Cucurbita", "Sweet potato and potato", "Flippers of a penguin and flippers of a dolphin", "B")
b.m("A", HD, "Which of the following diseases is caused by a helminth?", "Typhoid", "Common cold", "Ringworm", "Ascariasis", "D")
b.m("A", MW, "Milk is converted into curd by the action of:", "Lactobacillus", "Acetobacter aceti", "Clostridium butylicum", "Trichoderma polysporum", "A")
b.m("A", BP, "In the cloning vector pBR322, which of the following is commonly used as a selectable marker?", "ori", "rop", "the ampicillin resistance gene", "the BamHI recognition site", "C")
b.m("A", BA, "The first transgenic cow, Rosie, produced milk that was enriched with:", "human insulin", "human alpha-lactalbumin", "human growth hormone", "alpha-1-antitrypsin", "B")
b.m("A", ES, "The rate of formation of new organic matter by consumers in an ecosystem is called:", "gross primary productivity", "net primary productivity", "standing crop", "secondary productivity", "D")
b.m("A", BC, "Which of the following animals became extinct mainly because of over-exploitation by human beings?", "Steller's sea cow", "Bengal tiger", "Indian rhinoceros", "Asiatic lion", "A")
b.m("A", OP, "A population interaction in which both the interacting species are harmed is:", "mutualism", "commensalism", "competition", "predation", "C")

b.ar("A", EV, "The eye of an octopus and the eye of a mammal are analogous structures.", "Analogous structures are the result of convergent evolution.", "A")
b.ar("A", HR, "Spermatogenesis begins at birth in human males.", "Spermatogenesis is started at puberty by a significant increase in the secretion of GnRH.", "D")
b.ar("A", PI, "Haemophilia is a sex-linked recessive disorder.", "The gene for haemophilia is located on the Y chromosome.", "C")

# ── SECTION B — VSA ──
b.q("VSA", "B", MB, "State the function of (a) the promoter and (b) the terminator in a transcription unit.")
b.q("VSA", "B", HD, "What is metastasis? Why is it considered the most feared property of malignant tumours?")
b.q("VSA", "B", ES, "Distinguish between gross primary productivity and net primary productivity. Write the relationship between the two.")
b.q("VSA", "B", RH, "What is amniocentesis? Why has a statutory ban been imposed on its use for determining the sex of the foetus?")
b.q("VSA", "B", BA, "What is RNA interference (RNAi)? How has it been used to protect tobacco plants from the nematode Meloidogyne incognita?")
b.q("VSA", "B", OP, "Define natality and mortality. How does each of them affect the density of a population?")

# ── SECTION C — SA ──
b.q("SA", "C", HR, "Describe the events that take place in the human female from fertilisation up to the implantation of the blastocyst in the uterus.")
b.q("SA", "C", PI, "Explain incomplete dominance with the help of a cross between red-flowered and white-flowered snapdragon plants, up to the F₂ generation. Why are the phenotypic and genotypic ratios of the F₂ generation the same in this case?")
b.q("SA", "C", MB, "What is meant by the genetic code? Describe any five salient features of the genetic code.")
b.q("SA", "C", EV, "Explain Darwin's theory of natural selection. How does the example of industrial melanism in the peppered moth in England support this theory?")
b.q("SA", "C", HD, "(a) What is an allergy? Name the antibody and the chemicals released by mast cells that are responsible for allergic reactions.\n(b) Name one class of drugs used to reduce the symptoms of allergy.\n(c) Why are more children in metro cities suffering from allergies?")
b.q("SA", "C", MW, "Describe the primary and secondary treatment of sewage in a sewage treatment plant. What is BOD and what does a high BOD of a water sample indicate?")
b.q("SA", "C", BC, "Distinguish between in situ and ex situ conservation of biodiversity, giving two examples of each. What is cryopreservation and how does it help in conservation?")

# ── SECTION D — CASE STUDY ──
b.q("CBQ", "D", MB, "In a court case about the identity of the father of a child, the court ordered a DNA test. Blood samples were taken from the child, the mother and the man concerned. DNA was isolated from each sample, cut with restriction enzymes and the fragments were separated. The separated DNA was then transferred to a membrane and treated with a labelled probe that binds to repeated DNA sequences, called VNTRs. The bands obtained from the child were compared with those of the mother and the man.\n(a) What are VNTRs?\n(b) Name the technique used to separate the DNA fragments according to their size.\n(c) Why can DNA isolated from blood, hair roots or skin cells of a person all be used to obtain the same DNA fingerprint?\nOR\n(c) Name the scientist who developed the technique of DNA fingerprinting. Why does every person, except identical twins, have a unique DNA fingerprint?")
b.q("CBQ", "D", SR, "A farmer grows maize and papaya on his farm. In maize, the male and female flowers are borne on the same plant, while in papaya, the male and female flowers are borne on different plants. To produce a new hybrid variety of maize, a plant breeder visited his farm and carried out artificial hybridisation by covering the female inflorescences with paper bags and dusting them with pollen collected from the selected male parent.\n(a) Which of the two plants, maize or papaya, prevents both autogamy and geitonogamy? Give a reason.\n(b) What is bagging? Why is it necessary in artificial hybridisation?\n(c) Why is emasculation not needed in maize during artificial hybridisation?\nOR\n(c) Why is the endosperm of a maize grain triploid? Explain how it is formed.")

# ── SECTION E — LA ──
b.q("LA", "E", MB, "(a) Describe the process of transcription in bacteria, explaining the steps of initiation, elongation and termination.\n(b) How is the primary transcript (hnRNA) processed in eukaryotes to form a functional mRNA?\nOR\n(a) Describe the experiment of Meselson and Stahl that proved that DNA replicates semi-conservatively.\n(b) Why is DNA replication continuous on one strand and discontinuous on the other strand of the replication fork?")
b.q("LA", "E", SR, "(a) Describe the process of double fertilisation in angiosperms and name the products formed.\n(b) Describe the structure of a typical dicotyledonous embryo.\n(c) What is polyembryony? Give one example.\nOR\n(a) What are outbreeding devices? Describe any three such devices found in flowering plants.\n(b) What is pollen-pistil interaction? Why is it important?")
b.q("LA", "E", OP, "(a) Explain, with one example each, the population interactions of predation, parasitism and mutualism.\n(b) State Gause's competitive exclusion principle.\n(c) What is brood parasitism? Describe one adaptation shown in it.\nOR\n(a) Describe the steps of decomposition of detritus in an ecosystem: fragmentation, leaching, catabolism, humification and mineralisation.\n(b) How do temperature, moisture and the chemical composition of detritus affect the rate of decomposition?")

b.save()
