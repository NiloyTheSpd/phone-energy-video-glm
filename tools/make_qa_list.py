#!/usr/bin/env python3
"""Define the QA still list (first/mid/end of each chapter + every major visual event)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TL = json.load(open(os.path.join(ROOT, "project", "voice", "timeline.json")))
L = {x["id"]: x for x in TL["lines"]}
CH = {c["n"]: c for c in TL["chapters"]}
T = lambda i: L[i]["t0"]
TE = lambda i: L[i]["t1"]

stills = []
def add(name, t):
    stills.append({"name": name, "t": round(max(0.05, min(TL["total"] - 0.05, t)), 2)})

def ch_range(n):
    c = CH[n]
    t1 = CH[n + 1]["t0"] - 0.35 if n < 12 else TL["end_card"]["t0"] + TL["end_card"]["draw"] + TL["end_card"]["hold"] - 0.25
    return c["t0"], t1

# per chapter: first, mid, end + events
plan = {
 1: [("energy", T("c01l10") + 1.3), ("tilt", T("c01l04") + 1.2)],
 2: [("xsec", T("c02l03") + 0.4), ("question", T("c02l06") + 1.6)],
 3: [("heating", T("c03l05") + 2.8), ("rule", T("c03l07") + 1.8)],
 4: [("react", T("c04l04") + 1.1), ("verdict", T("c04l06") + 1.6)],
 5: [("vial", T("c05l04") + 0.2), ("bars", T("c05l06") + 2.6)],
 6: [("comet", T("c06l03") + 1.0), ("formula", T("c06l09") + 0.4), ("cannon", T("c06l09") + 2.0)],
 7: [("rest", T("c07l07") + 1.6), ("train", T("c07l09") + 2.2), ("reveal", T("c07l14") + 1.2)],
 8: [("boat", T("c08l03") + 1.6), ("flash", T("c08l06") + 0.9), ("boxed", T("c08l11") + 1.2)],
 9: [("fraction", T("c09l05") + 1.0), ("swatch", T("c09l08") + 0.8), ("radium", T("c09l09") + 2.0)],
 10: [("bend", T("c10l04") + 1.8), ("hut", T("c10l07") + 0.5), ("sparkle", T("c10l07") + 0.35),
      ("reaction", T("c10l10") + 0.9), ("bars", T("c10l13") + 0.3), ("match", T("c10l13") + 1.5)],
 11: [("fusion", T("c11l05") + 0.9), ("sun", T("c11l07") + 0.6), ("light", T("c11l07") + 1.0)],
 12: [("equation", T("c12l05") + 0.5), ("proton", T("c12l07") + 0.5), ("flood", T("c12l08") + 0.4),
      ("bodyfill", T("c12l09") + 0.4), ("final", TE("c12l09") - 0.8)],
}
for n in range(1, 13):
    t0, t1 = ch_range(n)
    add(f"ch{n:02d}_000", t0 + 0.3)
    for label, t in plan.get(n, []):
        add(f"ch{n:02d}_{label}", t)
    add(f"ch{n:02d}_end", t1 - 0.6)
# the end card, complete
add("endcard", TL["total"] - 0.4)
# opening frame
add("ch01_open", 0.85)

json.dump(stills, open(os.path.join(ROOT, "project", "qa_stills.json"), "w"), indent=1)
print(len(stills), "stills:", ", ".join(s["name"] for s in stills))
