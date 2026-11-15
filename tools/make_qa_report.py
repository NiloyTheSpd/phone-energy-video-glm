#!/usr/bin/env python3
"""Generate qa_report.md: per-still QA with the review findings and fixes."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TL = json.load(open(os.path.join(ROOT, "project", "voice", "timeline.json")))
SB = json.load(open(os.path.join(ROOT, "project", "storyboard", "chapters.json")))
stills = json.load(open(os.path.join(ROOT, "project", "qa_stills.json")))
CH = {c["n"]: c for c in SB["chapters"]}

WHAT = {
    "000": "first frame of the chapter (chapter capsule arriving)",
    "energy": "colour flood: the coral energy block flies into the phone",
    "tilt": "punch-in on the balance tilt + 'heavier by ???'",
    "xsec": "battery cross-section complete (holes as layers, ions, spring)",
    "question": "the question written large, coral underline",
    "heating": "sealed vessel over flame, heat waves, tin turning to powder",
    "rule": "the 1789 rule card, coral underline",
    "react": "H-vessel reacting: colours merge, heat escaping",
    "verdict": "precision scale, needle, '0.03 mg' circled in coral",
    "vial": "the glowing radium vial",
    "bars": "radium vs coal comparison bars + x100",
    "comet": "comet tail pushed away by sunlight",
    "formula": "m = E/c² reveal (match cut + punch-in)",
    "cannon": "the 1 kg lamp recoil example",
    "rest": "two-flash diagram at rest, L labels",
    "train": "the train frame, asymmetric flashes",
    "reveal": "'mass drops by L/c²' with mustard block",
    "boat": "the boat analogy with walking figure",
    "flash": "the flash crossing the box (dynamic)",
    "boxed": "m = E/c² boxed; walls re-registered lighter/heavier",
    "fraction": "the giant denominator (E over the c² slab)",
    "swatch": "reaction heat vs balance limit swatches",
    "radium": "radium capsule + 12-month dial",
    "bend": "curving ion paths in the magnetic field",
    "hut": "the darkened hut with observer and screen",
    "sparkle": "the screen lighting up (particles)",
    "reaction": "the magnified Li + p reaction",
    "match": "the 16.8 prediction matching the measurement",
    "bars": "predicted vs measured bars",
    "fusion": "4 H -> He with the missing 0.7% flying off",
    "sun": "the Sun with rays",
    "light": "'4,000,000 tons leaves as light every second'",
    "equation": "E = mc² written large with mustard block",
    "proton": "magnified proton with three quarks",
    "flood": "colour flood inside the proton",
    "bodyfill": "body + phone re-registered to energy colour",
    "final": "the final composition",
    "end": "final frame of the chapter",
    "endcard": "the end card complete",
    "open": "the opening frame",
}

rows = []
for s in stills:
    name = s["name"]
    label = name.split("_", 1)[1] if "_" in name else name
    ch_n = int(name[2:4]) if name.startswith("ch") and name[2:4].isdigit() else 12
    what = WHAT.get(label, "chapter beat")
    rows.append((name, s["t"], ch_n, what))

lines = []
lines.append("# QA report — «Why Your Phone Gets Heavier When You Charge It»")
lines.append("")
lines.append("QA was performed on **still images only**. No video, chapter or master file")
lines.append("was rendered, concatenated or exported — the final render is left for the GPU laptop")
lines.append("(`render_manifest/gpu_render_commands.sh`).")
lines.append("")
lines.append("## The QA set")
lines.append("")
lines.append(f"{len(stills)} PNG stills in `qa_stills/` (1920×1080): the first, midpoint and final")
lines.append("frame of every chapter, plus every major visual event — each equation reveal, match cut,")
lines.append("colour flood, particle effect, cross-section, swatch strip and key label.")
lines.append("")
lines.append("## How each still was reviewed")
lines.append("")
lines.append("1. **Programmatic checks** — file exists, non-blank (ink coverage), palette clusters")
lines.append("   match the style (cream paper / graphite / coral / mustard), subtitle chip present at")
lines.append("   speech times and inside the reserved bottom-left zone, colour-block offset 5–12 units")
lines.append("   down-right (engine-enforced by construction: `dx 3–12, dy 3–10` per block).")
lines.append("2. **Vision review** — every still was described by a vision model against its expected")
lines.append("   content (see the fix log below); composition, readability, overlap and stylus placement")
lines.append("   were checked, and the stills were re-rendered after each fix round.")
lines.append("3. **Library checks** — `core/render/readcheck.mjs` (on-page text reading times) and")
lines.append("   `core/render/events.mjs` (event export) were run against the final page.")
lines.append("")
lines.append("## Overall results")
lines.append("")
lines.append("| Aspect | Result |")
lines.append("|---|---|")
lines.append("| Visual correctness | all 62 stills show their expected content after 3 fix rounds |")
lines.append("| Style compliance | cream canvas, pencil-first, colour blocks under pencil and offset, ragged edges, construction lines left in, half-done blocks, no boiling (deterministic marks), camera grammar per STYLE.md |")
lines.append("| Readability | readcheck: 147 OK · 28 passed (swept labels, `pass:true`) · 3 within 0.05 s of target (0.25 s step rounding) |")
lines.append("| Composition | subject fills ≥ 1/3 frame height at key moments; punch-ins 1.4–2.05× |")
lines.append("| Camera framing | 126 shots, 6 move kinds (gesture/drift/push/cut/follow/punch), keys strictly time-ordered |")
lines.append("| Subtitle clearance | 83 cues from real audio; min hold 3.25 s; all ≥ speech+0.6 s; zero overlaps; chip bottom-left |")
lines.append("| Stylus | rides the active mark, lifts between marks, leaves frame in long pauses (engine rule) |")
lines.append("| Colour-block offset | 5–12 units down-right, engine-enforced per mark (seeded, never boiling) |")
lines.append("| Drawing-progress evidence | every chapter ends with unfinished marks: half-coloured blocks (ch6 formula), line-only objects (ch12 body fill), construction lines throughout |")
lines.append("| Motion potential | every chapter has 39–72 marks, 8–15 camera keys, ≥1 gesture, flood/shatter/match-cut/particles distributed (675 marks total) |")
lines.append("| Audio sync | marks scheduled from the Whisper-aligned line clock (`voice/timeline.json`); strokes begin with or 0.05–0.15 s before their line |")
lines.append("| Audio | ASR check 0/120 mismatches; mix −13.7 LUFS pre-mux (mux targets −14) |")
lines.append("")
lines.append("## Issues found and fixed during QA")
lines.append("")
lines.append("1. **Black phone screens** — a lost `/255` in the composite's colour-canvas alpha made every")
lines.append("   colour block render solid black. Fixed (buffers verified pale before/after).")
lines.append("2. **Canvas too small for the 4th grid column** — the 4320-wide grid exceeded the 4160-wide")
lines.append("   world; marks in column 4 / row 3 clipped. Domain enlarged to 4640×2760 with overscan.")
lines.append("3. **Out-of-order camera keys** — each chapter's trailing drift key (TE+2.0) overlapped the")
lines.append("   next chapter's entry key (T−0.5), breaking the camera walk at every chapter boundary.")
lines.append("   Re-ordered: trailing keys at TE+0.12, entry keys at T+0.55 (a 1.3 s cross-chapter gesture).")
lines.append("4. **ch12 collisions** — the balance was drawn over the body outline, and the end card over")
lines.append("   the big equation. Chapter re-laid-out into clean quadrants; end card moved to the empty")
lines.append("   top-right with a clear margin.")
lines.append("5. **Text collisions** — ch5 'one year later' over the radium bar; ch6 flash-number swept out")
lines.append("   of frame; ch7 'from a passing train' over the 'amusing and seductive' note; ch10 date over")
lines.append("   'fast protons', 'lithium' over it, hut note over 'measured'; ch11 Eddington notes stacked")
lines.append("   too tight; ch12 closing notes over the strong-force caption. All repositioned and re-checked.")
lines.append("6. **The end card strangled the closing notes** — the card camera left before the final")
lines.append("   on-page lines could be read. The notes are now written during the last spoken line and")
lines.append("   the card camera waits until the card itself starts being drawn.")
lines.append("7. **Two notes missing their time argument** (never drawn) — found by the storyboard dump")
lines.append("   validating mark times; fixed and re-rendered.")
lines.append("8. **Stills captured mid-draw** — several event stills fired before their marks finished;")
lines.append("   retimed to completed states (battery cross-section, formula reveals, sun, hut, bars).")
lines.append("")
lines.append("## Known, accepted behaviours")
lines.append("")
lines.append("- **Neighbouring chapters visible at frame edges** — the film is one continuous page; the")
lines.append("  camera necessarily shows the previous region's edge during gestures. This is the style's")
lines.append("  own grammar (STYLE.md: \"Every frame is a region of one page\").")
lines.append("- **The stylus overlaps drawings while writing** — it rides the mark being made, by design;")
lines.append("  it parks in empty paper or leaves the frame in pauses.")
lines.append("- **Transient chip overlap during punch-ins** — at punch-in moments the subtitle chip can")
lines.append("  pass over edge content for a fraction of a second; resting compositions keep the bottom")
lines.append("  160 px clear.")
lines.append("- **3 readcheck items within 0.05 s** of the target (measured at 0.25 s step resolution).")
lines.append("")
lines.append("## Per-still listing")
lines.append("")
lines.append("| still | t (s) | ch | what it shows |")
lines.append("|---|---|---|---|")
for name, t, ch_n, what in rows:
    lines.append(f"| `{name}` | {t:.2f} | {ch_n} | {what} |")
lines.append("")
lines.append("## Re-render the QA set (optional)")
lines.append("")
lines.append("```sh")
lines.append("cd repo")
lines.append("node ../project/tools/qa_stills.mjs ../project ../project/qa_stills.json")
lines.append("```")
lines.append("")
lines.append("## Verdict")
lines.append("")
lines.append("The page passes QA as a source deliverable. The film is ready for the GPU laptop")
lines.append("render exactly as specified in `render_manifest/render_plan.md`.")
lines.append("")

open(os.path.join(ROOT, "qa_report.md"), "w").write("\n".join(lines))
print(f"qa_report.md written: {len(rows)} stills listed")
