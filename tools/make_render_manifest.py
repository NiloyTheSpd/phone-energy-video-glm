#!/usr/bin/env python3
"""Generate the render manifest: per-chapter render plans, concat order, and the GPU script."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.join(ROOT, "repo")
PROJ = os.path.join(ROOT, "project")
TL = json.load(open(os.path.join(PROJ, "voice", "timeline.json")))
SB = json.load(open(os.path.join(PROJ, "storyboard", "chapters.json")))
RM = os.path.join(ROOT, "render_manifest")
CH_DIR = os.path.join(RM, "chapters")
os.makedirs(CH_DIR, exist_ok=True)
FPS = 24

total = TL["total"]
rows = []
for i, c in enumerate(TL["chapters"]):
    t0, t1 = c["t0"] - 0.7, 0.0            # start a beat before the first line
    t1 = TL["chapters"][i + 1]["t0"] - 0.7 if i < 11 else total
    t0 = max(0.0, t0)
    n = c["n"]
    rows.append(dict(n=n, title=c["title"], frm=t0, to=round(t1, 3),
                     frames=(round(t0 * FPS), round(t1 * FPS)), out=f"out/ch{n:02d}.mp4"))
# the end card lives inside ch12's span (t0 = total-5.8); keep ch12 to the very end.
for r in rows:
    plan = {
        "chapter": r["n"], "title": r["title"],
        "from": round(r["frm"], 3), "to": r["to"],
        "frame_range": list(r["frames"]), "frame_count": r["frames"][1] - r["frames"][0],
        "fps": FPS, "resolution": "1920x1080",
        "video_codec": "libx264 (crf 14, preset medium, yuv420p — set by core/render/video.mjs)",
        "command": f"node core/render/video.mjs project --fps 24 --workers 2 --q 'from={r['frm']}&to={r['to']}' --out project/{r['out']}",
        "audio": "project/out/mix.wav (full-film mix; mux after concat — see audio_mix_plan.md)",
        "subtitle": "burned into the page itself (drawSubs); project/script/subtitles.srt is the export",
    }
    json.dump(plan, open(os.path.join(CH_DIR, f"ch{r['n']:02d}.json"), "w"), indent=1)

with open(os.path.join(RM, "concat_order.txt"), "w") as f:
    for r in rows:
        f.write(f"file 'project/{r['out']}'\n")
    f.write("# concat with: ffmpeg -f concat -safe 0 -i concat_order.txt -c copy out/video.mp4\n")

sb = {c["n"]: c for c in SB["chapters"]}
json.dump({
    "film": "Why Your Phone Gets Heavier When You Charge It",
    "total_seconds": total, "fps": FPS, "resolution": "1920x1080",
    "chapters": [dict(r, marks=sb[r["n"]]["marks_count"], camera_keys=len(sb[r["n"]]["camera_keyframes"])) for r in rows],
}, open(os.path.join(RM, "chapters", "index.json"), "w"), indent=1)

print("render manifest chapters written:", [r["out"] for r in rows])
print("total film:", total, "s; frames:", round(total * FPS))
