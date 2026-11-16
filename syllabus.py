"""Master list of every subject and chapter the portal covers (CBSE 2026–27).

This is what the Content Tracker measures against: a chapter that is listed here but has no chapter
notes page yet shows up as "not started", so nothing can be missed.

Each subject: key, class, name, code, hubs (subject notes pages it belongs to), verified (chapter list
checked against the official 2026–27 syllabus PDF), chapters [(number, title, quiz-slug or None)].
Chapter slugs (used in URLs) are derived from the title.
"""
import re

SUBJECTS = [
{"key": "class10/science", "class": "10", "name": "Science", "code": "086", "hubs": ["resources/science-x.html"], "verified": True,
 "chapters": [
  (1, "Chemical Reactions and Equations", "chemical-reactions-10"),
  (2, "Acids, Bases and Salts", None),
  (3, "Metals and Non-metals", None),
  (4, "Carbon and its Compounds", None),
  (5, "Life Processes", "life-processes-10"),
  (6, "Control and Coordination", None),
  (7, "How do Organisms Reproduce?", None),
  (8, "Heredity", "heredity-evolution-10"),
  (9, "Light – Reflection and Refraction", "light-optics-10"),
  (10, "The Human Eye and the Colourful World", None),
  (11, "Electricity", "electricity-10"),
  (12, "Magnetic Effects of Electric Current", None),
  (13, "Our Environment", None)]},
{"key": "class10/maths", "class": "10", "name": "Mathematics (Standard & Basic)", "code": "041 / 241",
 "hubs": ["resources/maths-x.html", "resources/maths-basic-x.html"], "verified": False,
 "chapters": [
  (1, "Real Numbers", "real-numbers-10"), (2, "Polynomials", None),
  (3, "Pair of Linear Equations in Two Variables", None), (4, "Quadratic Equations", "quadratic-equations-10"),
  (5, "Arithmetic Progressions", "arithmetic-progressions-10"), (6, "Triangles", "triangles-10"),
  (7, "Coordinate Geometry", None), (8, "Introduction to Trigonometry", None),
  (9, "Some Applications of Trigonometry", None), (10, "Circles", None),
  (11, "Areas Related to Circles", None), (12, "Surface Areas and Volumes", None),
  (13, "Statistics", "statistics-probability-10"), (14, "Probability", None)]},
{"key": "class10/social-science", "class": "10", "name": "Social Science", "code": "087", "hubs": ["resources/sst-x.html"], "verified": False,
 "chapters": [
  (1, "History: The Rise of Nationalism in Europe", None), (2, "History: Nationalism in India", None),
  (3, "History: The Making of a Global World", None), (4, "History: The Age of Industrialisation", None),
  (5, "History: Print Culture and the Modern World", None),
  (6, "Geography: Resources and Development", None), (7, "Geography: Forest and Wildlife Resources", None),
  (8, "Geography: Water Resources", None), (9, "Geography: Agriculture", None),
  (10, "Geography: Minerals and Energy Resources", None), (11, "Geography: Manufacturing Industries", None),
  (12, "Geography: Lifelines of National Economy", None),
  (13, "Political Science: Power Sharing", None), (14, "Political Science: Federalism", None),
  (15, "Political Science: Gender, Religion and Caste", None), (16, "Political Science: Political Parties", None),
  (17, "Political Science: Outcomes of Democracy", None),
  (18, "Economics: Development", None), (19, "Economics: Sectors of the Indian Economy", None),
  (20, "Economics: Money and Credit", None), (21, "Economics: Globalisation and the Indian Economy", None),
  (22, "Map Work", None)]},
{"key": "class10/ai", "class": "10", "name": "Artificial Intelligence", "code": "417", "hubs": ["resources/ai-x.html"], "verified": False,
 "chapters": [
  (1, "Revisiting the AI Project Cycle and Ethical Frameworks", "ai-introduction-10"),
  (2, "Advanced Concepts of Modeling in AI", "ml-concepts-10"), (3, "Evaluating Models", None),
  (4, "Statistical Data", "data-handling-10"), (5, "Computer Vision", None),
  (6, "Natural Language Processing", None), (7, "Employability Skills (Part A)", None)]},
{"key": "class10/computer-applications", "class": "10", "name": "Computer Applications", "code": "165",
 "hubs": ["resources/comp-app-x.html"], "verified": False,
 "chapters": [(1, "Networking and the Internet", None), (2, "HTML", None), (3, "Cyber Ethics", None),
              (4, "Python Basics", "python-basics-10")]},
{"key": "class10/english-ll", "class": "10", "name": "English Language and Literature", "code": "184",
 "hubs": ["resources/english-ll-x.html"], "verified": False,
 "chapters": [
  (1, "Reading Comprehension", None), (2, "Grammar", None), (3, "Writing Skills", None),
  (4, "First Flight: A Letter to God", None), (5, "First Flight: Nelson Mandela – Long Walk to Freedom", None),
  (6, "First Flight: Two Stories about Flying", None), (7, "First Flight: From the Diary of Anne Frank", None),
  (8, "First Flight: Glimpses of India", None), (9, "First Flight: Mijbil the Otter", None),
  (10, "First Flight: Madam Rides the Bus", None), (11, "First Flight: The Sermon at Benares", None),
  (12, "First Flight: The Proposal", None), (13, "First Flight: Poems", None),
  (14, "Footprints without Feet: Supplementary Reader", None)]},
{"key": "class10/english-comm", "class": "10", "name": "English Communicative", "code": "101",
 "hubs": ["resources/english-comm-x.html"], "verified": False,
 "chapters": [(1, "Reading", None), (2, "Writing", None), (3, "Grammar", None), (4, "Literature: Prose", None),
              (5, "Literature: Poetry", None), (6, "Literature: Drama / Novel", None)]},
{"key": "class10/hindi-a", "class": "10", "name": "हिंदी कोर्स A", "code": "002", "hubs": ["resources/hindi-a-x.html"], "verified": False,
 "chapters": [(1, "अपठित गद्यांश और काव्यांश", None), (2, "व्याकरण", None), (3, "रचनात्मक लेखन", None),
              (4, "क्षितिज: काव्य खंड", None), (5, "क्षितिज: गद्य खंड", None), (6, "कृतिका", None)]},
{"key": "class12/physics", "class": "12", "name": "Physics", "code": "042", "hubs": ["resources/physics-xii-new.html"], "verified": False,
 "hub_locked": True,
 "chapters": [
  (1, "Electric Charges and Fields", "electrostatics-12"), (2, "Electrostatic Potential and Capacitance", "electrostatics-12"),
  (3, "Current Electricity", "current-electricity-12"), (4, "Moving Charges and Magnetism", None),
  (5, "Magnetism and Matter", None), (6, "Electromagnetic Induction", "em-induction-12"),
  (7, "Alternating Current", "em-induction-12"), (8, "Electromagnetic Waves", None),
  (9, "Ray Optics and Optical Instruments", "ray-optics-12"), (10, "Wave Optics", None),
  (11, "Dual Nature of Radiation and Matter", "dual-nature-12"), (12, "Atoms", "dual-nature-12"),
  (13, "Nuclei", "dual-nature-12"), (14, "Semiconductor Electronics", None)]},
{"key": "class12/chemistry", "class": "12", "name": "Chemistry", "code": "043", "hubs": ["resources/chemistry-xii.html"], "verified": True,
 "chapters": [
  (1, "Solutions", "solutions-12"), (2, "Electrochemistry", "electrochemistry-12"),
  (3, "Chemical Kinetics", "chemical-kinetics-12"), (4, "The d- and f-Block Elements", None),
  (5, "Coordination Compounds", "coordination-12"), (6, "Haloalkanes and Haloarenes", None),
  (7, "Alcohols, Phenols and Ethers", None), (8, "Aldehydes, Ketones and Carboxylic Acids", "aldehydes-ketones-12"),
  (9, "Amines", None), (10, "Biomolecules", None)]},
{"key": "class12/biology", "class": "12", "name": "Biology", "code": "044", "hubs": ["resources/biology-xii.html"], "verified": False,
 "chapters": [
  (1, "Sexual Reproduction in Flowering Plants", None), (2, "Human Reproduction", "human-reproduction-12"),
  (3, "Reproductive Health", None), (4, "Principles of Inheritance and Variation", "genetics-evolution-12"),
  (5, "Molecular Basis of Inheritance", "molecular-basis-12"), (6, "Evolution", "genetics-evolution-12"),
  (7, "Human Health and Disease", None), (8, "Microbes in Human Welfare", None),
  (9, "Biotechnology: Principles and Processes", "biotechnology-12"), (10, "Biotechnology and its Applications", "biotechnology-12"),
  (11, "Organisms and Populations", None), (12, "Ecosystem", "ecosystem-12"), (13, "Biodiversity and Conservation", None)]},
{"key": "class12/maths", "class": "12", "name": "Mathematics", "code": "041", "hubs": ["resources/maths-xii.html"], "verified": False,
 "chapters": [
  (1, "Relations and Functions", None), (2, "Inverse Trigonometric Functions", None), (3, "Matrices", "matrices-12"),
  (4, "Determinants", "matrices-12"), (5, "Continuity and Differentiability", None),
  (6, "Application of Derivatives", "application-derivatives-12"), (7, "Integrals", "integrals-12"),
  (8, "Application of Integrals", "integrals-12"), (9, "Differential Equations", "differential-equations-12"),
  (10, "Vector Algebra", None), (11, "Three Dimensional Geometry", None), (12, "Linear Programming", None),
  (13, "Probability", "probability-12")]},
{"key": "class12/computer-science", "class": "12", "name": "Computer Science", "code": "083", "hubs": ["resources/cs-xii.html"], "verified": False,
 "chapters": [
  (1, "Python Revision Tour", "python-basics-10"), (2, "Functions", "python-functions-12"), (3, "Exception Handling", None),
  (4, "File Handling: Text, Binary and CSV Files", None), (5, "Data Structures: Stack", "data-structures-12"),
  (6, "Computer Networks", "networking-12"), (7, "Database Concepts and SQL", "database-sql-12"),
  (8, "Interface of Python with MySQL", "database-sql-12")]},
{"key": "class12/economics", "class": "12", "name": "Economics", "code": "030", "hubs": ["resources/economics-xii.html"], "verified": False,
 "chapters": [
  (1, "Macro: National Income and Related Aggregates", None), (2, "Macro: Money and Banking", None),
  (3, "Macro: Determination of Income and Employment", None), (4, "Macro: Government Budget and the Economy", None),
  (5, "Macro: Balance of Payments and Foreign Exchange", None),
  (6, "IED: Indian Economy on the Eve of Independence", None), (7, "IED: Indian Economy 1950–1990", None),
  (8, "IED: Liberalisation, Privatisation and Globalisation", None), (9, "IED: Human Capital Formation", None),
  (10, "IED: Rural Development", None), (11, "IED: Employment", None),
  (12, "IED: Environment and Sustainable Development", None),
  (13, "IED: Comparative Development Experiences of India and its Neighbours", None)]},
{"key": "class12/accountancy", "class": "12", "name": "Accountancy", "code": "055", "hubs": ["resources/accountancy-xii.html"], "verified": False,
 "chapters": [
  (1, "Accounting for Partnership: Basic Concepts", None), (2, "Reconstitution: Admission of a Partner", None),
  (3, "Reconstitution: Retirement and Death of a Partner", None), (4, "Dissolution of Partnership Firm", None),
  (5, "Accounting for Share Capital", None), (6, "Issue and Redemption of Debentures", None),
  (7, "Financial Statements of a Company", None), (8, "Analysis of Financial Statements", None),
  (9, "Accounting Ratios", None), (10, "Cash Flow Statement", None)]},
{"key": "class12/business-studies", "class": "12", "name": "Business Studies", "code": "054", "hubs": ["resources/business-xii.html"], "verified": False,
 "chapters": [
  (1, "Nature and Significance of Management", None), (2, "Principles of Management", None),
  (3, "Business Environment", None), (4, "Planning", None), (5, "Organising", None), (6, "Staffing", None),
  (7, "Directing", None), (8, "Controlling", None), (9, "Financial Management", None),
  (10, "Financial Markets", None), (11, "Marketing", None), (12, "Consumer Protection", None)]},
{"key": "class12/english-core", "class": "12", "name": "English Core", "code": "301", "hubs": ["resources/english-xii.html"], "verified": False,
 "chapters": [
  (1, "Reading Comprehension", None), (2, "Creative Writing", None),
  (3, "Flamingo: The Last Lesson", None), (4, "Flamingo: Lost Spring", None), (5, "Flamingo: Deep Water", None),
  (6, "Flamingo: The Rattrap", None), (7, "Flamingo: Indigo", None), (8, "Flamingo: Poets and Pancakes", None),
  (9, "Flamingo: The Interview", None), (10, "Flamingo: Going Places", None), (11, "Flamingo: Poems", None),
  (12, "Vistas: The Third Level", None), (13, "Vistas: The Tiger King", None),
  (14, "Vistas: Journey to the End of the Earth", None), (15, "Vistas: The Enemy", None),
  (16, "Vistas: On the Face of It", None), (17, "Vistas: Memories of Childhood", None)]},
]

# Order the nightly drafting works through (roadmap phases 1 → 3).
QUEUE_ORDER = ["class10/science", "class10/maths", "class12/physics", "class12/chemistry",
               "class12/biology", "class12/maths", "class12/economics", "class12/english-core",
               "class10/social-science", "class10/computer-applications", "class10/ai", "class12/computer-science",
               "class12/accountancy", "class12/business-studies", "class10/english-ll", "class10/english-comm",
               "class10/hindi-a"]


def slugify(title):
    t = title.split(": ", 1)[-1] if re.match(r"^(History|Geography|Political Science|Economics|Macro|IED|First Flight|Flamingo|Vistas): ", title) else title
    s = re.sub(r"[^a-z0-9]+", "-", t.lower().replace("–", "-")).strip("-")
    return s or re.sub(r"\W+", "-", title).strip("-").lower() or "chapter"


def chapters():
    """Flat list of every chapter with its subject info and URL slug."""
    out = []
    for s in SUBJECTS:
        for num, title, quiz in s["chapters"]:
            slug = slugify(title)
            if not re.match(r"^[a-z0-9-]+$", slug):         # Hindi titles: number-based slug
                slug = f"chapter-{num}"
            out.append({"subject": s["key"], "subject_name": s["name"], "class": s["class"], "number": num,
                        "title": title, "slug": slug, "quiz": quiz, "hubs": s["hubs"],
                        "id": f"{s['key']}/{slug}"})
    return out


if __name__ == "__main__":
    cs = chapters()
    ids = [c["id"] for c in cs]
    assert len(ids) == len(set(ids)), "duplicate chapter ids"
    print(len(SUBJECTS), "subjects,", len(cs), "chapters")
