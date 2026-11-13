"""
mock_bank_add.py — helper for adding question batches to question-bank/*.json

Used by the batch scripts in question-bank/batches/. Each batch script is run
once; it appends its questions to the subject file with new, never-reused ids.

    from mock_bank_add import Batch
    b = Batch("science10")
    b.m("A", "Life Processes", "Question?", "opt A", "opt B", "opt C", "opt D", "B")
    b.ar("A", "Heredity", "assertion text", "reason text", "A")
    b.q("VSA", "A", "Life Processes", "Question text")
    b.save()
"""
import json
import re
from pathlib import Path

BANK_DIR = Path(__file__).parent / "question-bank"

BLUEPRINTS = {
    "science10": dict(file="class10_science.json", prefix="sc10", subject="Science", cls="X",
                      max_marks=80, time="3 Hours", sections=[
        ("SECTION A", "Biology", 30, [["MCQ", 7], ["A/R", 2], ["VSA", 3], ["SA", 2], ["CBQ", 1], ["LA", 1]]),
        ("SECTION B", "Chemistry", 25, [["MCQ", 6], ["A/R", 2], ["VSA", 1], ["SA", 2], ["CBQ", 1], ["LA", 1]]),
        ("SECTION C", "Physics", 25, [["MCQ", 3], ["A/R", 1], ["SA", 4], ["CBQ", 1], ["LA", 1]])]),
    "maths10": dict(file="class10_maths.json", prefix="ma10", subject="Mathematics", cls="X",
                    max_marks=80, time="3 Hours", sections=[
        ("SECTION A", "MCQ & Assertion-Reason", 20, [["MCQ", 18], ["A/R", 2]]),
        ("SECTION B", "Very Short Answer", 10, [["VSA", 5]]),
        ("SECTION C", "Short Answer", 18, [["SA", 6]]),
        ("SECTION D", "Long Answer", 20, [["LA", 4]]),
        ("SECTION E", "Case Study", 12, [["CBQ", 3]])]),
    "maths12": dict(file="class12_maths.json", prefix="ma12", subject="Mathematics", cls="XII",
                    max_marks=80, time="3 Hours", sections=[
        ("SECTION A", "MCQ & Assertion-Reason", 20, [["MCQ", 18], ["A/R", 2]]),
        ("SECTION B", "Very Short Answer", 10, [["VSA", 5]]),
        ("SECTION C", "Short Answer", 18, [["SA", 6]]),
        ("SECTION D", "Long Answer", 20, [["LA", 4]]),
        ("SECTION E", "Case Study", 12, [["CBQ", 3]])]),
}
for _k, _f, _p, _s in (("physics12", "class12_physics.json", "ph12", "Physics"),
                       ("chemistry12", "class12_chemistry.json", "ch12", "Chemistry"),
                       ("biology12", "class12_biology.json", "bi12", "Biology")):
    BLUEPRINTS[_k] = dict(file=_f, prefix=_p, subject=_s, cls="XII", max_marks=70, time="3 Hours", sections=[
        ("SECTION A", "MCQ & Assertion-Reason", 16, [["MCQ", 14], ["A/R", 2]]),
        ("SECTION B", "Very Short Answer", 10, [["VSA", 5]]),
        ("SECTION C", "Short Answer", 21, [["SA", 7]]),
        ("SECTION D", "Case Study", 8, [["CBQ", 2]]),
        ("SECTION E", "Long Answer", 15, [["LA", 3]])])


class Batch:
    def __init__(self, subject_key: str):
        bp = BLUEPRINTS[subject_key]
        self.path = BANK_DIR / bp["file"]
        self.prefix = bp["prefix"]
        if self.path.exists():
            self.bank = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self.bank = {"subject_key": subject_key, "subject": bp["subject"], "class": bp["cls"],
                         "max_marks": bp["max_marks"], "time": bp["time"],
                         "sections": [{"name": n, "title": t, "marks": m, "slots": s}
                                      for n, t, m, s in bp["sections"]],
                         "questions": []}
        nums = [int(re.search(r"(\d+)$", q["id"]).group(1)) for q in self.bank["questions"]]
        self.n = max(nums, default=0)
        self.added = 0

    def _add(self, qtype, sec, chapter, text, **extra):
        self.n += 1; self.added += 1
        q = {"id": f"{self.prefix}-{self.n:04d}", "section": f"SECTION {sec}", "type": qtype,
             "chapter": chapter, "text": text.strip()}
        q.update(extra)
        self.bank["questions"].append(q)

    def m(self, sec, chapter, text, a, b, c, d, ans):
        self._add("MCQ", sec, chapter, text,
                  options=[f"(A) {a}", f"(B) {b}", f"(C) {c}", f"(D) {d}"], answer=f"({ans})")

    def ar(self, sec, chapter, assertion, reason, ans):
        self._add("A/R", sec, chapter, f"Assertion (A): {assertion}\nReason (R): {reason}", answer=f"({ans})")

    def q(self, qtype, sec, chapter, text):
        self._add(qtype, sec, chapter, text)

    def save(self):
        BANK_DIR.mkdir(exist_ok=True)
        self.path.write_text(json.dumps(self.bank, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"{self.path.name}: +{self.added} questions, {len(self.bank['questions'])} total")
