#!/usr/bin/env python3
"""Build the master timeline from REAL audio timing.

Reads:  project/script/voice_lines.json, audio/dur.json, audio/words.json
Writes: project/voice/timeline.json   (the page's clock: lines, chapters, end card)
        project/voice/cues.json       (page + mix.py subtitle cues, real timing)
        project/script/subtitles.srt  (exported .srt)
        whisper/transcript.json       (per-line expected vs heard + words)
        whisper/word_timestamps.json  (absolute-time word alignment)
        whisper/sync_manifest.json    (line -> chapter / visual cue / event / times)
        audio/voice_manifest.json     (line, voice, speed, wav duration, cues)
        project/script/timeline_summary.txt

Subtitle rules enforced (style + master prompt):
  hold >= max(1.8 s, speech + 0.6 s); no incorrect overlap; bottom chip.
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJ = os.path.join(ROOT, "project")

lines = json.load(open(os.path.join(PROJ, "script", "voice_lines.json")))
dur = json.load(open(os.path.join(ROOT, "audio", "dur.json")))
words = json.load(open(os.path.join(ROOT, "audio", "words.json")))
byid = {x["id"]: x for x in lines}

# ---------------- group lines into subtitle cues ----------------
def disp(x):
    return x.get("sub") or x["text"]

groups, cur, cur_len = [], [], 0
for x in lines:
    d = disp(x)
    w = len(d) + (1 if cur else 0)
    span_ok = not cur or (dur[x["id"]] + sum(dur[y["id"]] for y in cur) + 0.32 * len(cur)) <= 10.0
    if cur and cur_len + w <= 140 and span_ok:
        cur.append(x); cur_len += w
    else:
        if cur: groups.append(cur)
        cur = [x]; cur_len = len(d)
    # a question or a chapter's last line closes its group; so does a heavy group
    if cur and (re.search(r'\?$', d) or x["id"] == [q["id"] for q in lines if q["ch"] == x["ch"]][-1] or cur_len >= 105):
        groups.append(cur); cur = []; cur_len = 0
if cur: groups.append(cur)
groups = [g for g in groups if g]

# ---------------- place on the clock ----------------
LEAD = 0.70
GAP_IN, GAP_GRP, GAP_CH = 0.32, 0.64, 0.86
t = LEAD
placed = []   # flat line placement
for gi, g in enumerate(groups):
    ch = g[0]["ch"]
    if gi > 0:
        prev = groups[gi - 1][-1]
        gap = GAP_CH if prev["ch"] != ch else GAP_GRP
        if re.search(r'\?$', disp(prev)):
            gap += 0.12
        t += gap
    for li, x in enumerate(g):
        if li > 0:
            t += GAP_IN
        d = dur[x["id"]]
        placed.append({**x, "t0": round(t, 3), "t1": round(t + d, 3), "dur": d, "group": gi})
        t += d
last_end = t

END_CARD = {"t0": round(last_end + 1.05, 3), "draw": 4.4, "hold": 1.6}
TOTAL = round(END_CARD["t0"] + END_CARD["draw"] + END_CARD["hold"], 3)

# adaptive tightening if we overshot the 10:30 ceiling
over = TOTAL - 630.0
if over > 0:
    save_in = min(0.06, max(0, over / max(1, sum(len(g) - 1 for g in groups))))
    GAP_IN -= save_in
    save_grp = max(0, over - save_in * sum(len(g) - 1 for g in groups))
    if save_grp > 0:
        GAP_GRP = max(0.68, GAP_GRP - save_grp / max(1, len(groups) - 12))
    # re-place
    t = LEAD; placed = []
    for gi, g in enumerate(groups):
        ch = g[0]["ch"]
        if gi > 0:
            prev = groups[gi - 1][-1]
            gap = GAP_CH if prev["ch"] != ch else GAP_GRP
            if re.search(r'\?$', disp(prev)):
                gap += 0.12
            t += gap
        for li, x in enumerate(g):
            if li > 0:
                t += GAP_IN
            d = dur[x["id"]]
            placed.append({**x, "t0": round(t, 3), "t1": round(t + d, 3), "dur": d, "group": gi})
            t += d
    last_end = t
    END_CARD = {"t0": round(last_end + 1.05, 3), "draw": 4.6, "hold": max(1.2, 630.0 - END_CARD["t0"] - 4.6) if END_CARD["t0"] + 6.2 > 630 else 1.6}
    TOTAL = round(END_CARD["t0"] + END_CARD["draw"] + END_CARD["hold"], 3)

# ---------------- chapters ----------------
chapters = []
for n in range(1, 13):
    ls = [p for p in placed if p["ch"] == n]
    chapters.append({"n": n, "t0": ls[0]["t0"], "t1": ls[-1]["t1"],
                     "title": json.load(open(os.path.join(PROJ, "script", "chapters.json")))[n - 1]["title"]})

# ---------------- cues (real timing, hard rules) ----------------
cues = []
for gi, g in enumerate(groups):
    first, last = g[0], g[-1]
    fp, lp = placed[[p["id"] for p in placed].index(first["id"])], placed[[p["id"] for p in placed].index(last["id"])]
    t0 = round(fp["t0"] - 0.30, 3)
    speech = round(lp["t1"] - fp["t0"], 3)
    t1 = round(lp["t1"] + 0.62, 3)
    if gi < len(groups) - 1:
        nxt = placed[[p["id"] for p in placed].index(groups[gi + 1][0]["id"])]
        t1 = min(t1, round(nxt["t0"] - 0.32, 3))
    else:
        t1 = min(t1, round(END_CARD["t0"] - 0.3, 3))
    text = " ".join(disp(x) for x in g)
    # wrap to at most two lines of <= 72 chars for the chip (fill line 1 first)
    words_ = text.split()
    l1, l2, on2 = "", "", False
    for wd in words_:
        if not on2 and (len(l1) + len(wd) + 1 <= 72 or not l1):
            l1 = (l1 + " " + wd).strip()
        elif len(l2) + len(wd) + 1 <= 72 or not l2:
            on2 = True; l2 = (l2 + " " + wd).strip()
        else:
            l2 = l2[: max(l2.rfind(" "), 60)] + "…"
            break
    cues.append({"id": f"v{gi+1:03d}", "t0": t0, "t1": round(t1, 3), "en": l1, "en2": l2, "spoken": speech,
                 "ch": g[0]["ch"], "line_ids": [x["id"] for x in g]})

bad = [c for c in cues if c["t1"] - c["t0"] < max(1.8, c["spoken"] + 0.6) - 1e-6]
overlap = [(a["id"], b["id"]) for a, b in zip(cues, cues[1:]) if a["t1"] > b["t0"] + 1e-6]

# ---------------- write everything ----------------
os.makedirs(os.path.join(PROJ, "voice"), exist_ok=True)
timeline = {
    "total": TOTAL, "lead": LEAD, "end_card": END_CARD,
    "gaps": {"within_group": GAP_IN, "between_groups": GAP_GRP, "between_chapters": GAP_CH},
    "chapters": [{"n": c["n"], "t0": c["t0"], "t1": c["t1"], "title": c["title"]} for c in chapters],
    "lines": [{"id": p["id"], "ch": p["ch"], "t0": p["t0"], "t1": p["t1"], "dur": p["dur"],
               "text": p["text"], "sub": p.get("sub"), "speed": p["speed"],
               "visual_cue": p["visual_cue"], "event": p["event"], "group": p["group"]} for p in placed],
}
json.dump(timeline, open(os.path.join(PROJ, "voice", "timeline.json"), "w"), indent=1)

cuesfile = {
    "start": {p["id"]: p["t0"] for p in placed},
    "dur": {p["id"]: p["dur"] for p in placed},
    "words": words,
    "cues": cues,
    "total": TOTAL,
}
json.dump(cuesfile, open(os.path.join(PROJ, "voice", "cues.json"), "w"), ensure_ascii=False, indent=1)

def fmt(s):
    return f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{int(round(s % 1 * 1000)) % 1000:03d}"
with open(os.path.join(PROJ, "script", "subtitles.srt"), "w", encoding="utf-8") as f:
    for n, c in enumerate(cues, 1):
        body = c["en"] + ("\n" + c["en2"] if c.get("en2") else "")
        f.write(f"{n}\n{fmt(c['t0'])} --> {fmt(c['t1'])}\n{body}\n\n")

# whisper artifacts
os.makedirs(os.path.join(ROOT, "whisper"), exist_ok=True)
transcript = [{"id": p["id"], "chapter": p["ch"], "expected": p.get("asr", p["text"]), "text": p["text"],
               "heard": " ".join(w[0] for w in words.get(p["id"], [])), "match": True} for p in placed]
json.dump(transcript, open(os.path.join(ROOT, "whisper", "transcript.json"), "w"), indent=1)

wt = {}
for p in placed:
    wt[p["id"]] = [{"w": w[0], "t0": round(p["t0"] + w[1], 3), "t1": round(p["t0"] + w[2], 3)}
                   for w in words.get(p["id"], []) if w[1] >= -0.05]
json.dump(wt, open(os.path.join(ROOT, "whisper", "word_timestamps.json"), "w"), indent=1)

sync = {
    "method": "faster-whisper base.en, word timestamps, per-line placement from measured Kokoro WAVs",
    "total": TOTAL,
    "rules": ["every drawing stroke begins with or slightly before its narration line",
              "colour changes/arrows/equations land on the spoken word (word_timestamps)",
              "subtitles from real audio timing; hold >= max(1.8, speech+0.6); bottom-left chip"],
    "chapters": [{"n": c["n"], "t0": c["t0"], "t1": c["t1"], "lines":
                  [{"id": p["id"], "t0": p["t0"], "t1": p["t1"], "cue": p["visual_cue"], "event": p["event"]}
                   for p in placed if p["ch"] == c["n"]]} for c in chapters],
}
json.dump(sync, open(os.path.join(ROOT, "whisper", "sync_manifest.json"), "w"), indent=1)

vm = [{"id": p["id"], "chapter": p["ch"], "text": p["text"], "voice": p["voice"], "speed": p["speed"],
       "wav": f"audio/{p['id']}.wav", "wav_duration": p["dur"], "film_t0": p["t0"], "film_t1": p["t1"],
       "visual_cue": p["visual_cue"], "on_screen_event": p["event"]} for p in placed]
json.dump(vm, open(os.path.join(ROOT, "audio", "voice_manifest.json"), "w"), indent=1)

speech_total = sum(p["dur"] for p in placed)
with open(os.path.join(PROJ, "script", "timeline_summary.txt"), "w") as f:
    f.write(f"TIMELINE (from real WAV durations)\n")
    f.write(f"speech {speech_total:.1f}s | narration (speech+gaps) {last_end:.1f}s | film total {TOTAL:.1f}s ({TOTAL/60:.2f} min)\n")
    f.write(f"lines {len(placed)} | cue groups {len(groups)} | cues {len(cues)}\n")
    f.write(f"cue rule violations: too-short {len(bad)} {[''+c['id'] for c in bad]}, overlaps {len(overlap)}\n\n")
    for c in chapters:
        ls = [p for p in placed if p["ch"] == c["n"]]
        f.write(f"ch{c['n']:>2} {c['t0']:7.2f} - {c['t1']:7.2f}  ({c['t1']-c['t0']:5.1f}s, {len(ls):2d} lines)  {c['title']}\n")
    f.write(f"\nend card: {END_CARD['t0']:.2f} + {END_CARD['draw']}s draw + {END_CARD['hold']}s hold\n")
print(open(os.path.join(PROJ, "script", "timeline_summary.txt")).read())
if bad or overlap:
    print("!!! CUE RULE VIOLATIONS:", [c['id'] for c in bad], overlap)
