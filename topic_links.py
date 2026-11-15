"""Where should a reel / formula card send people? -> the exact pages for its topic.

    from topic_links import why_links, formula_links
    why_links("07_why_parallel_resistors.mp4")
    formula_links("Physics", "Alternating Current", "12")

Each returns {"learn": (title, url) | None, "chapters": [(title, url), ...], "portal": (title, url) | None}
with absolute URLs. Used by the reel / card gallery pages, the social posting scripts and /go/.
"""
import importlib
import re
from datetime import datetime, timedelta, timezone

SITE = "https://cbsemock.org.in"
TODAY = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()

CHAPTERS = {
    "ai-introduction-10": "Introduction to AI", "aldehydes-ketones-12": "Aldehydes & Ketones",
    "application-derivatives-12": "Application of Derivatives", "arithmetic-progressions-10": "Arithmetic Progressions",
    "biotechnology-12": "Biotechnology", "chemical-kinetics-12": "Chemical Kinetics",
    "chemical-reactions-10": "Chemical Reactions & Equations", "coordination-12": "Coordination Compounds",
    "current-electricity-12": "Current Electricity", "data-handling-10": "Data Handling & Visualisation",
    "data-structures-12": "Data Structures (Stack)", "database-sql-12": "Database & SQL",
    "differential-equations-12": "Differential Equations", "dual-nature-12": "Dual Nature & Atoms",
    "ecosystem-12": "Ecosystem", "electricity-10": "Electricity", "electrochemistry-12": "Electrochemistry",
    "electrostatics-12": "Electrostatics", "em-induction-12": "Electromagnetic Induction",
    "genetics-evolution-12": "Genetics & Evolution", "heredity-evolution-10": "Heredity & Evolution",
    "human-reproduction-12": "Human Reproduction", "integrals-12": "Integrals", "life-processes-10": "Life Processes",
    "light-optics-10": "Light – Reflection & Refraction", "matrices-12": "Matrices & Determinants",
    "ml-concepts-10": "Machine Learning Concepts", "molecular-basis-12": "Molecular Basis of Inheritance",
    "networking-12": "Networking", "neural-networks-10": "Neural Networks & AI Ethics",
    "oop-python-12": "OOP with Python", "probability-12": "Probability", "python-basics-10": "Python Basics",
    "python-functions-12": "Python Functions & Modules", "quadratic-equations-10": "Quadratic Equations",
    "ray-optics-12": "Ray Optics", "real-numbers-10": "Real Numbers", "solutions-12": "Solutions",
    "statistics-probability-10": "Statistics & Probability", "triangles-10": "Triangles",
}

# (pattern on the normalised topic text, chapter slug). First matches win; class filters apply after.
RULES = [
    (r"electrostat|gauss|capacitor|coulomb|electric field|electric charge", "electrostatics-12"),
    (r"current electricity|current flow|resist|ohm|kirchhoff|power forms|electric power|wire force", "current-electricity-12"),
    (r"current electricity|current flow|resist|ohm|power forms|electricity", "electricity-10"),
    (r"induction|faraday|lenz|alternating current|\bac\b", "em-induction-12"),
    (r"lens|mirror|refract|reflect|optic|\btir\b|prism|rainbow|light", "ray-optics-12"),
    (r"lens|mirror|refract|reflect|optic|\btir\b|light|rainbow|blue sky|concave", "light-optics-10"),
    (r"dual nature|photoelectric|atom|nucle|de broglie", "dual-nature-12"),
    (r"kinetic|collision|rate of reaction|activation energy", "chemical-kinetics-12"),
    (r"electrochem|cell potential|nernst|ionic conduct", "electrochemistry-12"),
    (r"solution|colligative|raoult|solid state", "solutions-12"),
    (r"coordination|ligand", "coordination-12"),
    (r"aldehyde|ketone|name reaction", "aldehydes-ketones-12"),
    (r"chemical reaction|balance eq|iron copper|displacement|redox", "chemical-reactions-10"),
    (r"genetic|mendel|inherit|evolution|chromosome|blood o", "genetics-evolution-12"),
    (r"\bdna\b|molecular|replication|transcription", "molecular-basis-12"),
    (r"heredity|chromosome|genetic|evolution|blood o|\bdna\b", "heredity-evolution-10"),
    (r"reproduct|mitosis|meiosis", "human-reproduction-12"),
    (r"biotech", "biotechnology-12"),
    (r"ecolog|ecosystem", "ecosystem-12"),
    (r"life process|nutrition|respiration|photosynth|stomach|intestine|xylem|phloem|blood|arter|vein|circ|heart|\batp\b|stomata|transport|excret", "life-processes-10"),
    (r"matri|determinant", "matrices-12"),
    (r"application derivative|maxim|minim|slope zero|derivative|calculus|differentiat", "application-derivatives-12"),
    (r"integra", "integrals-12"),
    (r"differential equation", "differential-equations-12"),
    (r"probab", "probability-12"),
    (r"real number|polynomial|hcf|lcm", "real-numbers-10"),
    (r"quadratic", "quadratic-equations-10"),
    (r"\bap\b|arithmetic progression|ap sum", "arithmetic-progressions-10"),
    (r"triangle|trig|pythag|sin|cos", "triangles-10"),
    (r"statistic|probab|mean|median|mode", "statistics-probability-10"),
    (r"stack|data structure|queue|lifo", "data-structures-12"),
    (r"sql|dbms|database|join", "database-sql-12"),
    (r"network|packet|protocol", "networking-12"),
    (r"\boop\b|class object|object oriented", "oop-python-12"),
    (r"function|recursion|module", "python-functions-12"),
    (r"python|list|tuple|dict|loop|indentation|if elif|data type|debugging|float|binary search|time complexity", "python-basics-10"),
    (r"neural|neuron|nn layers|activation|computer vision|chatbot|bias|ethic|gradient", "neural-networks-10"),
    (r"machine learning|train test|accuracy|confusion|precision|recall|decision tree|ai data|gradient", "ml-concepts-10"),
    (r"data handling|visuali|ai data", "data-handling-10"),
    (r"artificial intelligence|\bai\b", "ai-introduction-10"),
]

PORTALS = {
    ("Physics", "10"): ("Class 10 Science mock tests", "cbse-class-10-science-mock-tests.html"),
    ("Chemistry", "10"): ("Class 10 Science mock tests", "cbse-class-10-science-mock-tests.html"),
    ("Biology", "10"): ("Class 10 Science mock tests", "cbse-class-10-science-mock-tests.html"),
    ("Science", "10"): ("Class 10 Science mock tests", "cbse-class-10-science-mock-tests.html"),
    ("Maths", "10"): ("Class 10 Maths mock tests", "cbse-class-10-maths-standard-mock-tests.html"),
    ("AI", "10"): ("Class 10 AI mock papers", "cbse-class-10-ai-mock-papers.html"),
    ("AI", "12"): ("Class 10 AI mock papers", "cbse-class-10-ai-mock-papers.html"),
    ("CS", "10"): ("Class 10 Computer Applications mock tests", "cbse-class-10-computer-applications-mock-tests.html"),
    ("Physics", "12"): ("Class 12 Physics mock papers", "cbse-class-12-physics-mock-papers.html"),
    ("Chemistry", "12"): ("Class 12 Chemistry mock papers", "cbse-class-12-chemistry-mock-papers.html"),
    ("Biology", "12"): ("Class 12 Biology mock papers", "cbse-class-12-biology-mock-papers.html"),
    ("Maths", "12"): ("Class 12 Maths mock papers", "cbse-class-12-maths-mock-papers.html"),
    ("CS", "12"): ("Class 12 Computer Science mock papers", "cbse-class-12-computer-science-mock-papers.html"),
}
SUBJECT_ALIASES = {"Mathematics": "Maths", "Math": "Maths", "Computer Science": "CS", "Artificial Intelligence": "AI"}
# which chapters a subject may link to (keeps a Physics card away from an AI quiz that shares a word)
SUBJECT_CHAPTERS = {
    "Physics": {"electrostatics-12", "current-electricity-12", "electricity-10", "em-induction-12", "ray-optics-12",
                "light-optics-10", "dual-nature-12"},
    "Chemistry": {"chemical-kinetics-12", "electrochemistry-12", "solutions-12", "coordination-12",
                  "aldehydes-ketones-12", "chemical-reactions-10"},
    "Biology": {"genetics-evolution-12", "molecular-basis-12", "heredity-evolution-10", "human-reproduction-12",
                "biotechnology-12", "ecosystem-12", "life-processes-10"},
    "Maths": {"matrices-12", "application-derivatives-12", "integrals-12", "differential-equations-12",
              "probability-12", "real-numbers-10", "quadratic-equations-10", "arithmetic-progressions-10",
              "triangles-10", "statistics-probability-10"},
    "CS": {"data-structures-12", "database-sql-12", "networking-12", "oop-python-12", "python-functions-12",
           "python-basics-10"},
    "AI": {"neural-networks-10", "ml-concepts-10", "data-handling-10", "ai-introduction-10", "python-basics-10"},
}
SUBJECT_CHAPTERS["Science"] = SUBJECT_CHAPTERS["Physics"] | SUBJECT_CHAPTERS["Chemistry"] | SUBJECT_CHAPTERS["Biology"]


def _norm(text):
    return " " + re.sub(r"[^a-z0-9]+", " ", text.lower()).strip() + " "


def chapters_for(text, subject, classes, limit=2):
    subject = SUBJECT_ALIASES.get(subject, subject)
    allowed = SUBJECT_CHAPTERS.get(subject)
    t, out = _norm(text), []
    for pat, slug in RULES:
        if slug in out or slug[-2:] not in classes or (allowed and slug not in allowed):
            continue
        if slug == "ai-introduction-10" and out:          # generic AI quiz only when nothing specific fits
            continue
        if re.search(pat, t):
            out.append(slug)
        if len(out) >= limit:
            break
    return [(CHAPTERS[s] + " quiz", f"{SITE}/chapters/{s}.html") for s in out]


def portal_for(subject, classes):
    subject = SUBJECT_ALIASES.get(subject, subject)
    if subject == "CS":                                     # Class 12 CS portal is the main CS page
        classes = sorted(classes, reverse=True)
    for c in classes:
        if (subject, c) in PORTALS:
            label, href = PORTALS[(subject, c)]
            return label, f"{SITE}/{href}"
    return None


def learn_for(reel_module):
    try:
        from learn_articles import ARTICLES
    except Exception:
        return None
    for a in ARTICLES:
        if a["reel"] == reel_module and datetime.strptime(a["published"], "%Y-%m-%d").date() <= TODAY:
            return a["h1"], f"{SITE}/learn/{a['slug']}.html"
    return None


def _why_module(slug):
    parts = slug.split("_")
    for k in range(len(parts), 0, -1):
        name = "_".join(parts[:k])
        try:
            return name, importlib.import_module("why_reels." + name)
        except ModuleNotFoundError:
            continue
    return slug, None


def why_links(filename):
    """filename like '07_why_parallel_resistors.mp4' (or just the slug)."""
    m = re.match(r"(?:\d+_why_)?(.+?)(?:\.mp4|\.txt)?$", filename.rsplit("/", 1)[-1])
    slug = m.group(1)
    name, mod = _why_module(slug)
    tags = getattr(mod, "TAGS", "") if mod else ""
    title = ""
    if mod is not None:
        first = mod.CAPTION.strip().splitlines()[0]
        title = first.split("WHY? —", 1)[-1]
    classes = [c for c in ("10", "12") if f"Class {c}" in tags or f"& {c}" in tags] or ["10", "12"]
    subject = next((s for k, s in (("AI", "AI"), ("Computer Science", "CS"), ("Maths", "Maths"), ("Physics", "Physics"),
                                   ("Chemistry", "Chemistry"), ("Biology", "Biology"), ("Science", "Science"))
                    if k in tags), "Science")
    text = f"{slug} {title} {tags}"
    return {"learn": learn_for(name), "chapters": chapters_for(text, subject, classes),
            "portal": portal_for(subject, classes)}


def formula_links(subject, topic, cls):
    """subject e.g. 'Physics'/'Mathematics'/'CS', topic text, cls '10' / '12' / 'X' / 'XII'."""
    c = {"X": "10", "XII": "12", "XI-XII": "12"}.get(str(cls), str(cls))
    classes = [c] if c in ("10", "12") else ["10", "12"]      # unclassed cards are the Class 10 basics
    ch = []
    for c_try in classes:                            # in class-preference order
        ch = chapters_for(f"{topic} {subject}", subject, [c_try], limit=1)
        if ch:
            break
    if ch and len(classes) > 1:                      # class unknown: follow the chapter's class
        classes = [ch[0][1].rsplit("-", 1)[-1].split(".")[0]]
    return {"learn": None, "chapters": ch, "portal": portal_for(subject, classes)}


def best_link(links):
    """The single most useful link (for captions): Learn article > chapter quiz > subject portal > home."""
    if links.get("learn"):
        return links["learn"]
    if links.get("chapters"):
        return links["chapters"][0]
    return links.get("portal") or ("Free notes & mock papers", SITE)


if __name__ == "__main__":
    import glob, os
    for f in sorted(glob.glob("formula-posts/why/*/*.mp4")):
        L = why_links(os.path.basename(f))
        print(os.path.basename(f)[:34].ljust(34), "|", (L["learn"] or ("-",))[0][:30].ljust(30), "|",
              ", ".join(c[0].replace(" quiz", "") for c in L["chapters"]) or "-", "|", (L["portal"] or ("-",))[0])
