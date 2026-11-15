# QA report — «Why Your Phone Gets Heavier When You Charge It»

> **QA round 4 (current)** — a full extra QA pass requested after round 3 still
> looked bad. Every finding below is from this round; the round-3 report is kept at the bottom.

## What round 4 found and fixed

**A. A physics error in the narration (audio regenerated).**
Line `c09l09` said radium's year of heat weighs "forty **millionths** of a gram".
The correct value is forty **billionths** (0.116 W × 1 year / c² = 4.1 × 10⁻⁸ g —
the source transcript was right). Fixed in `voice_lines.json`, `master_narration.txt`,
the on-page note, the subtitle; the WAV was regenerated with Kokoro (6.429 s),
re-checked by Whisper (0 mismatches) and the whole timeline was rebuilt
(`tools/build_timeline.py`), so cues, `.srt`, manifests and events all moved with it.

**B. A systematic layout QA (new tool).** `tools/text_collisions.mjs` loads the live
page and compares the real bounding box of every on-page text (`window.__TEXTBOXES()`,
world coordinates from the glyph layout) against every other text. The page accumulates,
so any two texts that overlap will eventually share the screen. First run on the round-3
page: **39 colliding pairs** (the earlier QA had checked swept labels and reading times,
not pairwise box collisions). All 39 were fixed by moving notes / retiming cameras;
final state: **0 collisions, 0 texts outside the canvas** (180 texts).

**C. Camera keys that cropped content mid-element or mid-word.** Each camera key was
checked against the world boxes of the texts and drawings that must be on screen at
that moment. Fixes: ch1 opening now an extreme push-in (2.0×) on the first phone with a
faster draw (1.7 s); ch3 weigh/rule cameras keep the ch4 capsule out of frame; ch4 wide
key pulled inside the grain; ch5 bar chart re-scaled (260-unit bar, labels inside the
frame, ×100 burst moved off the bar); ch6 formula stack raised 30 units, doubt notes
re-homed; ch7 kinetic stack moved fully inside its own cell (it crossed into ch12 and
ran over the phone), reveal block re-placed, camera keys re-aimed; ch8 "left wall
lighter / right wall heavier" split into two short notes that fit between the walls,
Poincaré credit moved under the options, M·d = m·L raised clear of the ruler; ch9
swatch labels stacked instead of colliding, needle + note moved, radium notes spaced;
ch10 ledger moved off the proton arrow, prediction bars dropped 60 units, blurry/17.2/14
labels spaced, hut note moved below the hut; ch11 wide keys re-aimed so ch10's hut notes
never enter the frame mid-word; ch12 fully re-laid-out into clean quadrants (balance +
phone left, equation right, magnified proton bottom-centre with an up-right handle, body
bottom-right, closing notes clear of the subtitle chip), end card raised clear of the
big equation.

**D. QA stills re-taken at settled moments.** Five stills had been captured
mid-gesture (bar tops cut, labels half-written). `project/qa_stills.json` now samples
each beat when its camera key has settled, and ch01 opens on the phone being drawn.

## Round-4 result

| Check | Result |
|---|---|
| Text-text collisions (world boxes, all 180 texts) | **0** |
| Texts outside the canvas (grain area + margin) | **0** |
| Whisper vs script | **0 / 120 mismatches** (radium line re-verified) |
| Subtitle cues | hold ≥ speech + 0.6 s, no overlaps (rebuild verified) |
| QA stills | 62 PNGs re-rendered from the fixed page and reviewed visually |
| Known acceptable artefacts | during camera *gestures* neighbouring drawings may enter/leave the frame edge (canvas grammar); foley event count changed 1119 → 1123 with the re-timed page |

Reproduce the layout check: `node tools/text_collisions.mjs project`
(stills: `node project/tools/qa_stills.mjs project project/qa_stills.json`).

---

## Round-3 report (kept for reference)
QA was performed on **still images only**. No video, chapter or master file
was rendered, concatenated or exported — the final render is left for the GPU laptop
(`render_manifest/gpu_render_commands.sh`).

## The QA set

62 PNG stills in `qa_stills/` (1920×1080): the first, midpoint and final
frame of every chapter, plus every major visual event — each equation reveal, match cut,
colour flood, particle effect, cross-section, swatch strip and key label.

## How each still was reviewed

1. **Programmatic checks** — file exists, non-blank (ink coverage), palette clusters
   match the style (cream paper / graphite / coral / mustard), subtitle chip present at
   speech times and inside the reserved bottom-left zone, colour-block offset 5–12 units
   down-right (engine-enforced by construction: `dx 3–12, dy 3–10` per block).
2. **Vision review** — every still was described by a vision model against its expected
   content (see the fix log below); composition, readability, overlap and stylus placement
   were checked, and the stills were re-rendered after each fix round.
3. **Library checks** — `core/render/readcheck.mjs` (on-page text reading times) and
   `core/render/events.mjs` (event export) were run against the final page.

## Overall results

| Aspect | Result |
|---|---|
| Visual correctness | all 62 stills show their expected content after 3 fix rounds |
| Style compliance | cream canvas, pencil-first, colour blocks under pencil and offset, ragged edges, construction lines left in, half-done blocks, no boiling (deterministic marks), camera grammar per STYLE.md |
| Readability | readcheck: 147 OK · 28 passed (swept labels, `pass:true`) · 3 within 0.05 s of target (0.25 s step rounding) |
| Composition | subject fills ≥ 1/3 frame height at key moments; punch-ins 1.4–2.05× |
| Camera framing | 126 shots, 6 move kinds (gesture/drift/push/cut/follow/punch), keys strictly time-ordered |
| Subtitle clearance | 83 cues from real audio; min hold 3.25 s; all ≥ speech+0.6 s; zero overlaps; chip bottom-left |
| Stylus | rides the active mark, lifts between marks, leaves frame in long pauses (engine rule) |
| Colour-block offset | 5–12 units down-right, engine-enforced per mark (seeded, never boiling) |
| Drawing-progress evidence | every chapter ends with unfinished marks: half-coloured blocks (ch6 formula), line-only objects (ch12 body fill), construction lines throughout |
| Motion potential | every chapter has 39–72 marks, 8–15 camera keys, ≥1 gesture, flood/shatter/match-cut/particles distributed (675 marks total) |
| Audio sync | marks scheduled from the Whisper-aligned line clock (`voice/timeline.json`); strokes begin with or 0.05–0.15 s before their line |
| Audio | ASR check 0/120 mismatches; mix −13.7 LUFS pre-mux (mux targets −14) |

## Issues found and fixed during QA

1. **Black phone screens** — a lost `/255` in the composite's colour-canvas alpha made every
   colour block render solid black. Fixed (buffers verified pale before/after).
2. **Canvas too small for the 4th grid column** — the 4320-wide grid exceeded the 4160-wide
   world; marks in column 4 / row 3 clipped. Domain enlarged to 4640×2760 with overscan.
3. **Out-of-order camera keys** — each chapter's trailing drift key (TE+2.0) overlapped the
   next chapter's entry key (T−0.5), breaking the camera walk at every chapter boundary.
   Re-ordered: trailing keys at TE+0.12, entry keys at T+0.55 (a 1.3 s cross-chapter gesture).
4. **ch12 collisions** — the balance was drawn over the body outline, and the end card over
   the big equation. Chapter re-laid-out into clean quadrants; end card moved to the empty
   top-right with a clear margin.
5. **Text collisions** — ch5 'one year later' over the radium bar; ch6 flash-number swept out
   of frame; ch7 'from a passing train' over the 'amusing and seductive' note; ch10 date over
   'fast protons', 'lithium' over it, hut note over 'measured'; ch11 Eddington notes stacked
   too tight; ch12 closing notes over the strong-force caption. All repositioned and re-checked.
6. **The end card strangled the closing notes** — the card camera left before the final
   on-page lines could be read. The notes are now written during the last spoken line and
   the card camera waits until the card itself starts being drawn.
7. **Two notes missing their time argument** (never drawn) — found by the storyboard dump
   validating mark times; fixed and re-rendered.
8. **Stills captured mid-draw** — several event stills fired before their marks finished;
   retimed to completed states (battery cross-section, formula reveals, sun, hut, bars).

## Known, accepted behaviours

- **Neighbouring chapters visible at frame edges** — the film is one continuous page; the
  camera necessarily shows the previous region's edge during gestures. This is the style's
  own grammar (STYLE.md: "Every frame is a region of one page").
- **The stylus overlaps drawings while writing** — it rides the mark being made, by design;
  it parks in empty paper or leaves the frame in pauses.
- **Transient chip overlap during punch-ins** — at punch-in moments the subtitle chip can
  pass over edge content for a fraction of a second; resting compositions keep the bottom
  160 px clear.
- **3 readcheck items within 0.05 s** of the target (measured at 0.25 s step resolution).

## Per-still listing

| still | t (s) | ch | what it shows |
|---|---|---|---|
| `ch01_000` | 1.00 | 1 | first frame of the chapter (chapter capsule arriving) |
| `ch01_energy` | 39.11 | 1 | colour flood: the coral energy block flies into the phone |
| `ch01_tilt` | 12.58 | 1 | punch-in on the balance tilt + 'heavier by ???' |
| `ch01_end` | 40.57 | 1 | final frame of the chapter |
| `ch02_000` | 41.82 | 2 | first frame of the chapter (chapter capsule arriving) |
| `ch02_xsec` | 54.44 | 2 | battery cross-section complete (holes as layers, ions, spring) |
| `ch02_question` | 67.57 | 2 | the question written large, coral underline |
| `ch02_end` | 72.14 | 2 | final frame of the chapter |
| `ch03_000` | 73.39 | 3 | first frame of the chapter (chapter capsule arriving) |
| `ch03_heating` | 103.36 | 3 | sealed vessel over flame, heat waves, tin turning to powder |
| `ch03_rule` | 114.48 | 3 | the 1789 rule card, coral underline |
| `ch03_end` | 122.12 | 3 | final frame of the chapter |
| `ch04_000` | 123.37 | 4 | first frame of the chapter (chapter capsule arriving) |
| `ch04_react` | 141.16 | 4 | H-vessel reacting: colours merge, heat escaping |
| `ch04_verdict` | 150.78 | 4 | precision scale, needle, '0.03 mg' circled in coral |
| `ch04_end` | 161.71 | 4 | final frame of the chapter |
| `ch05_000` | 162.96 | 5 | first frame of the chapter (chapter capsule arriving) |
| `ch05_vial` | 181.32 | 5 | the glowing radium vial |
| `ch05_bars` | 192.78 | 5 | predicted vs measured bars |
| `ch05_end` | 209.08 | 5 | final frame of the chapter |
| `ch06_000` | 210.33 | 6 | first frame of the chapter (chapter capsule arriving) |
| `ch06_comet` | 223.61 | 6 | comet tail pushed away by sunlight |
| `ch06_formula` | 249.58 | 6 | m = E/c² reveal (match cut + punch-in) |
| `ch06_cannon` | 251.18 | 6 | the 1 kg lamp recoil example |
| `ch06_end` | 266.61 | 6 | final frame of the chapter |
| `ch07_000` | 267.86 | 7 | first frame of the chapter (chapter capsule arriving) |
| `ch07_rest` | 303.33 | 7 | two-flash diagram at rest, L labels |
| `ch07_train` | 311.39 | 7 | the train frame, asymmetric flashes |
| `ch07_reveal` | 334.40 | 7 | 'mass drops by L/c²' with mustard block |
| `ch07_end` | 341.03 | 7 | final frame of the chapter |
| `ch08_000` | 342.28 | 8 | first frame of the chapter (chapter capsule arriving) |
| `ch08_boat` | 355.51 | 8 | the boat analogy with walking figure |
| `ch08_flash` | 371.70 | 8 | the flash crossing the box (dynamic) |
| `ch08_boxed` | 402.32 | 8 | m = E/c² boxed; walls re-registered lighter/heavier |
| `ch08_end` | 404.96 | 8 | final frame of the chapter |
| `ch09_000` | 406.21 | 9 | first frame of the chapter (chapter capsule arriving) |
| `ch09_fraction` | 423.55 | 9 | the giant denominator (E over the c² slab) |
| `ch09_swatch` | 436.01 | 9 | reaction heat vs balance limit swatches |
| `ch09_radium` | 440.63 | 9 | radium capsule + 12-month dial |
| `ch09_end` | 450.13 | 9 | final frame of the chapter |
| `ch10_000` | 451.38 | 10 | first frame of the chapter (chapter capsule arriving) |
| `ch10_bend` | 464.97 | 10 | curving ion paths in the magnetic field |
| `ch10_hut` | 487.94 | 10 | the darkened hut with observer and screen |
| `ch10_sparkle` | 487.79 | 10 | the screen lighting up (particles) |
| `ch10_reaction` | 502.88 | 10 | the magnified Li + p reaction |
| `ch10_bars` | 517.34 | 10 | predicted vs measured bars |
| `ch10_match` | 518.54 | 10 | the 16.8 prediction matching the measurement |
| `ch10_end` | 533.54 | 10 | final frame of the chapter |
| `ch11_000` | 534.79 | 11 | first frame of the chapter (chapter capsule arriving) |
| `ch11_fusion` | 556.88 | 11 | 4 H -> He with the missing 0.7% flying off |
| `ch11_sun` | 568.95 | 11 | the Sun with rays |
| `ch11_light` | 569.35 | 11 | '4,000,000 tons leaves as light every second' |
| `ch11_end` | 578.03 | 11 | final frame of the chapter |
| `ch12_000` | 579.28 | 12 | first frame of the chapter (chapter capsule arriving) |
| `ch12_equation` | 597.31 | 12 | E = mc² written large with mustard block |
| `ch12_proton` | 608.25 | 12 | magnified proton with three quarks |
| `ch12_flood` | 612.61 | 12 | colour flood inside the proton |
| `ch12_bodyfill` | 618.39 | 12 | body + phone re-registered to energy colour |
| `ch12_final` | 622.15 | 12 | the final composition |
| `ch12_end` | 628.95 | 12 | final frame of the chapter |
| `endcard` | 629.40 | 12 | the end card complete |
| `ch01_open` | 0.85 | 1 | the opening frame |

## Re-render the QA set (optional)

```sh
cd repo
node ../project/tools/qa_stills.mjs ../project ../project/qa_stills.json
```

## Verdict

The page passes QA as a source deliverable. The film is ready for the GPU laptop
render exactly as specified in `render_manifest/render_plan.md`.
