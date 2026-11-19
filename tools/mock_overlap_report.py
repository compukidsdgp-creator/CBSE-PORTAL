"""Summarise tools/mock_overlap_audit.js output: how many different questions the 15 rendered papers of each page use."""
import collections, json, re, sys
d = json.load(open(sys.argv[1]))
print(f"{'page':58} {'slots':>5} {'unique':>6} {'repeat-free':>11} {'P1∩P2':>6} {'max uses':>8}")
for f, ps in sorted(d.items()):
    if isinstance(ps, dict) or not ps:
        print(f"{f:58} n/a"); continue
    P = [[re.sub(r"\W+", " ", q.lower()).strip()[:160] for q in p] for p in ps]
    slots = sum(map(len, P)); c = collections.Counter(q for p in P for q in p)
    ov = sum(len(set(P[i]) & set(P[i + 1])) / max(1, len(set(P[i]))) for i in range(len(P) - 1)) / (len(P) - 1)
    print(f"{f:58} {slots:5} {len(c):6} {100 * len(c) / slots:10.0f}% {100 * ov:5.0f}% {max(c.values()):8}")
