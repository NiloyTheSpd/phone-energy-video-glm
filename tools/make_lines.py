#!/usr/bin/env python3
"""Define the narration lines for 'Why Your Phone Gets Heavier When You Charge It'.

Calibrated against Kokoro af_heart measurements: ~140 wpm at 0.78 for short lines,
~160 for long ones. 1,381 words + inter-line gaps lands the film at ~10:00-10:20.

Single source of truth for:
  - project/script/voice_lines.json   (TTS input + display/subtitle text + cues)
  - project/script/chapters.json      (chapter plan: narration, words, speeds)
Line ids: c<chapter>l<line>. Voice text is TTS-friendly (numbers spelled out);
`sub` is the subtitle/on-screen spelling when it differs (digits, symbols).
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.join(os.path.dirname(HERE), "project")

L = []
def line(ch, text, sub, speed, cue, ev):
    L.append({"id": f"c{ch:02d}l{len([x for x in L if x['id'].startswith(f'c{ch:02d}')])+1:02d}",
              "ch": ch, "text": text, "sub": sub, "speed": speed, "voice": "af_heart",
              "visual_cue": cue, "event": ev})

# ---------------- CHAPTER 1 — THE IMPOSSIBLE SCALE ----------------
line(1, "Take two phones, identical in every way.", None, 0.76,
     "construction lines, two phone outlines", "two phones drawn white on the balance pans")
line(1, "Charge one completely, drain the other until it's dead,", None, 0.78,
     "battery glyphs on screens: full / empty", "coral block fills the left phone's battery")
line(1, "and set them on a balance.", None, 0.76,
     "balance beam, pans, pivot", "balance drawn around the phones")
line(1, "The charged phone is heavier.", None, 0.74,
     "beam tilts a hair left", "punch-in: exaggerated tilt wedge on the left pan")
line(1, "Not by any amount you could measure.", None, 0.76,
     "tiny question mark by the tilt", "note: 'heavier by ???'")
line(1, "Yet nothing material went in while it charged.", None, 0.78,
     "cable from a wall socket", "charging cable drawn to the left phone")
line(1, "No atoms came down the cable.", None, 0.76,
     "empty circles along the cable", "note: '0 atoms in'")
line(1, "No extra electrons piled up either: every electron that flowed in through one wire flowed back out through the other.", None, 0.82,
     "in/out arrows on both wires", "electron loop arrows along the cable")
line(1, "The only thing the phone gained was energy.", None, 0.76,
     "energy block glows into the battery", "colour flood: coral ENERGY block enters the phone")
line(1, "And energy, it turns out, has weight.", None, 0.74,
     "the coral block sits on the pan", "the energy block becomes the mystery; chapter capsule")

# ---------------- CHAPTER 2 — ENERGY IS NOT STUFF ----------------
line(2, "Inside the battery, charging doesn't add stuff. It rearranges it.", None, 0.80,
     "battery outline, cross-section rings", "battery cross-section drawn (holes as layers)")
line(2, "Ions shuttle between two layers into an arrangement that stores energy, like a stretched spring.", None, 0.82,
     "ion dots sliding between slabs", "ions + arrows between the two electrode layers")
line(2, "Use the phone, and they slide back down, releasing it.", None, 0.80,
     "reverse arrows, discharge", "discharge arrows (grey) opposite the coral charge arrows")
line(2, "A full battery and an empty one hold exactly the same atoms.", None, 0.80,
     "atom count note", "note: 'same atoms, same electrons'")
line(2, "The only difference is energy.", None, 0.76,
     "swatch strip: empty / charging / full", "swatch strip states tracked")
line(2, "So why would energy have weight at all?", None, 0.76,
     "big question mark builds", "camera drifts up; the question written large")
line(2, "Matter is supposed to be the thing that weighs.", None, 0.78,
     "the question left unfinished", "half-coloured block left; transition drift right")

# ---------------- CHAPTER 3 — THE OLD RULE ----------------
line(3, "For a century, science's most careful weighings said the opposite:", None, 0.80,
     "chapter capsule 'an old rule'", "new region: 1770s Paris lab table")
line(3, "nothing inside a sealed container can change its weight.", None, 0.80,
     "sealed ampoule sketch", "sealed glass vessel with tin block inside")
line(3, "The rule was born in Paris, in the seventeen seventies, with Antoine Lavoisier, a chemist who trusted his balance more than any theory.",
     "The rule was born in Paris, in the 1770s, with Antoine Lavoisier, a chemist who trusted his balance more than any theory.", 0.80,
     "label 'Paris, 1770s'", "handwritten label + leader line")
line(3, "He sealed tin inside a glass vessel, melting the glass shut so nothing could get in or out, and took its weight.", None, 0.82,
     "sealed neck, 'nothing in, nothing out'", "vessel neck sealed; note written")
line(3, "Then he heated it, until part of the shiny metal turned to grey powder, let it cool, and took its weight again.", None, 0.82,
     "flame under vessel, heat waves", "flame + mustard heat waves through the glass")
line(3, "Heat had poured in and out. The weight had not changed at all.", None, 0.80,
     "identical needle readings", "both balance readings match; coral 'unchanged!'")
line(3, "In seventeen eighty-nine, his rule: an equal quantity of matter, before and after.",
     "In 1789, his rule: an equal quantity of matter, before and after.", 0.78,
     "quill note card", "note card: the conservation rule, coral underline")
line(3, "Energy, it seemed, weighs nothing.", None, 0.74,
     "closure of the old rule", "swatch strip: 'energy weighs nothing?'")

# ---------------- CHAPTER 4 — THE LIMIT OF THE BALANCE ----------------
line(4, "But a rule is only as good as the balance that tests it.", None, 0.80,
     "chapter capsule 'the balance's limit'", "new region: Berlin, 1890s")
line(4, "In the eighteen nineties, Hans Landolt in Berlin spent twenty years testing it harder than anyone.",
     "In the 1890s, Hans Landolt in Berlin spent 20 years testing it harder than anyone.", 0.80,
     "label 'Landolt, Berlin'", "label + two-decade calendar note")
line(4, "Two chemicals, sealed in the separate arms of a glass vessel, react;", None, 0.80,
     "H-shaped vessel, two colours", "H-vessel drawn; coral + mustard chemicals in the arms")
line(4, "the heat escapes; he weighs it again. And again. And again.", None, 0.78,
     "repeat weigh ticks", "colour flood: chemicals merge mottled; heat arrows rise; weigh ticks")
line(4, "He chased every error — buoyancy, moisture, dust.", None, 0.80,
     "error list note", "error-hunting list written")
line(4, "His nineteen oh eight verdict: no reaction changed weight by more than three hundredths of a milligram.",
     "His 1908 verdict: no reaction changed weight by more than 0.03 mg.", 0.80,
     "the number, circled", "punch-in on the needle; coral circle around '0.03 mg'")
line(4, "If the escaping heat weighed anything at all, it weighed less than that.", None, 0.80,
     "heat arrows weighed 'less than...'", "error bar drawn under the needle")

# ---------------- CHAPTER 5 — RADIUM REFUSES TO BEHAVE ----------------
line(5, "Then a tiny glowing sample made that answer hard to believe.", None, 0.78,
     "chapter capsule 'radium'", "new region: back in Paris, 1902")
line(5, "Radium, which Marie Curie purified in nineteen oh two, from more than a ton of ore.",
     "Radium, which Marie Curie purified in 1902, from more than a ton of ore.", 0.80,
     "ore pile, funnel, tiny vial", "purification chain drawn: ton of ore into one vial")
line(5, "Pierre Curie measured one gram giving off a hundred calories of heat, every hour.", None, 0.80,
     "thermometer under the vial", "heat waves radiate; '100 cal/hour' note")
line(5, "That adds up to nearly nine hundred thousand calories a year.", None, 0.80,
     "calendar pages flip", "calendar pages drawn flying; radium bar grows tall (coral)")
line(5, "A gram of coal gives seven thousand. Then it's gone.",
     "A gram of coal gives 7,000. Then it's gone.", 0.78,
     "coal comparison bar", "coal bar stays tiny (graphite); swatch strip records both")
line(5, "The radium releases a hundred times more, every year, and barely slows down:", None, 0.82,
     "'×100' coral note", "coral '×100' bursts between the bars")
line(5, "half is still there sixteen hundred years from now.", None, 0.80,
     "half-life marker", "decay line drawn; 'half remains at 1,600 years'")
line(5, "Nobody could say what it was using up.", None, 0.76,
     "question mark over the vial", "big '?' over the glowing vial")
line(5, "Either it soaked up invisible energy from space, or the energy came from inside the atom itself.", None, 0.82,
     "two rival arrows", "option A: sky-to-vial arrow; option B: atom cross-section")

# ---------------- CHAPTER 6 — LIGHT HAS MOMENTUM ----------------
line(6, "The first clue had appeared earlier, in the way light behaves.", None, 0.80,
     "chapter capsule 'light pushes'", "new region: light, 1900")
line(6, "In nineteen hundred, Henri Poincaré worked through a fact most people never think about: light pushes.",
     "In 1900, Henri Poincaré worked through a fact most people never think about: light pushes.", 0.80,
     "label 'Poincaré, 1900'", "sun + radiating light rays drawn")
line(6, "It's why a comet's tail points away from the Sun;", None, 0.78,
     "comet with tail", "comet + tail pushed outward")
line(6, "and lab experiments had just measured that push.", None, 0.80,
     "lab bulb with vanes", "light-pressure apparatus: beam pushing a vane")
line(6, "Anything that pushes carries momentum.", None, 0.76,
     "'momentum' note", "note: 'push = momentum'")
line(6, "A flash of energy E carries momentum: E divided by the speed of light.", None, 0.82,
     "formula p = E/c", "handwritten: 'momentum = E / c'")
line(6, "Momentum is mass times speed.", None, 0.78,
     "formula p = m·v", "handwritten: 'momentum = mass × speed'")
line(6, "What mass would that flash need? Its energy, divided by the speed of light squared.", None, 0.80,
     "m = E/c² reveal", "match cut + punch-in: 'mass = E / c²' in coral")
line(6, "His example: a one kilogram lamp firing three million joules of light recoils like a cannon,", None, 0.82,
     "cannon-lamp recoil", "lamp fires a flash; recoil arrow '1 cm/s'")
line(6, "while the flash carries thirty-three billionths of a gram.", None, 0.80,
     "flash mass label", "flash labelled '33 billionths of a gram'")
line(6, "But he called it a fiction, not a real weight.", None, 0.78,
     "hesitation note", "'a fictitious fluid' — quote note beside the number")
line(6, "The number sat there. He didn't believe it.", None, 0.78,
     "the formula, doubted", "the coral formula left half-coloured; transition drift")

# ---------------- CHAPTER 7 — EINSTEIN'S FIRST ARGUMENT ----------------
line(7, "Believing it took Albert Einstein — twenty six, a clerk at the patent office in Bern.",
     "Believing it took Albert Einstein — 26, a clerk at the patent office in Bern.", 0.80,
     "chapter capsule 'Einstein's first argument'", "new region: Bern, 1905; desk + patent doodles")
line(7, "In nineteen oh five, just after finishing relativity, he wrote to a friend:",
     "In 1905, just after finishing relativity, he wrote to a friend:", 0.80,
     "letter card", "letter card drawn with the claim")
line(7, "a body's mass must be a measure of the energy inside it.", None, 0.78,
     "the claim, underlined", "coral underline under the claim")
line(7, "Light carries mass, he said. Radium should get noticeably lighter.", None, 0.80,
     "radium callback doodle", "small radium vial with down-arrow")
line(7, "That September, three pages in the leading physics journal.", None, 0.80,
     "three-page paper", "paper with '3 pages' note")
line(7, "A glowing object, at rest, fires two identical flashes in opposite directions.", None, 0.80,
     "object + two opposite flashes", "glowing dot; two mustard flashes left/right")
line(7, "The pushes cancel. It just loses the light's energy, L.", None, 0.80,
     "equal arrows, 'L' labels", "'L' labels both flashes; arrows cancel")
line(7, "Now watch from a passing train.", None, 0.76,
     "train frame drawn below", "match cut: same drawing, train + motion lines")
line(7, "The speed is unchanged, but the forward flash now looks slightly more energetic, the backward slightly less.", None, 0.82,
     "asymmetric flash lengths", "forward flash redrawn longer, backward shorter")
line(7, "Add them: most of the difference cancels. Not all.", None, 0.80,
     "sum bracket", "energy bookkeeping: 'L + a little extra'")
line(7, "From the train, the light carries away a little more than L.", None, 0.80,
     "extra energy highlighted", "coral highlight on the extra")
line(7, "That extra must come out of its kinetic energy.", None, 0.80,
     "'kinetic energy' note", "note: 'paid out of kinetic energy'")
line(7, "And kinetic energy is one half, times mass, times speed squared.", None, 0.80,
     "formula KE = ½mv²", "handwritten: 'kinetic = ½ · mass · speed²'")
line(7, "The speed hasn't changed. So the mass drops —", None, 0.78,
     "speed crossed out", "'speed' crossed out; 'mass?' remains")
line(7, "by the light's energy, divided by the speed of light squared.", None, 0.80,
     "m = E/c² again, now real", "punch-in: the same coral formula, re-registered solid")

# ---------------- CHAPTER 8 — THE BOX OF LIGHT ----------------
line(8, "A year later, Einstein offered a simpler argument: a flash of light inside a box.", None, 0.82,
     "chapter capsule 'the box of light'", "new region: a box floats in space; starfield dots")
line(8, "Walk from one end of a small boat to the other, and it slides back under you.", None, 0.82,
     "walking figure, slide arrows", "boat + walking figure; slide arrows")
line(8, "Nothing inside a closed system can move its own centre of mass.", None, 0.80,
     "centre-of-mass dot, X axis", "centre-of-mass dot + fixed axis drawn")
line(8, "Now make it a box in empty space, and make you a flash of light off the left wall.", None, 0.82,
     "boat -> box morph", "colour flood: the boat block becomes the box")
line(8, "The flash pushes the box back, crosses, and is absorbed at the right wall —", None, 0.82,
     "recoil + travel + absorb", "box recoil arrow; flash travels (dashed); absorption burst")
line(8, "the box stops, shifted. Nothing outside touched it.", None, 0.78,
     "shift marks on a ruler", "ruler shows the shift d; note 'nothing outside'")
line(8, "So either the box pushed itself through space, or the light carried mass, wall to wall.", None, 0.82,
     "the two options", "option notes: 'magic push' vs 'light carries mass'")
line(8, "The boat settles it: box mass times shift equals light mass times box length.", None, 0.82,
     "balance equation", "handwritten: 'M·d = m·L'")
line(8, "Everything cancels but one line: the light's mass equals its energy, divided by the speed of light squared.", None, 0.82,
     "m = E/c² boxed", "punch-in: 'm = E / c²' in a coral box")
line(8, "The left wall really gets lighter. The right wall really gets heavier.", None, 0.80,
     "walls re-registered", "left wall block fades lighter, right wall heavier")
line(8, "Einstein credited Poincaré on the paper's first page.", None, 0.80,
     "credit note", "note: 'built on Poincaré's reasoning'")

# ---------------- CHAPTER 9 — WHY NOBODY COULD SEE IT ----------------
line(9, "Once energy has real weight, the old mysteries make sense.", None, 0.80,
     "chapter capsule 'the giant denominator'", "new region: the fraction")
line(9, "Only one thing hid that weight: the size of c squared.", None, 0.80,
     "c² written huge", "'c' written, squared")
line(9, "Light moves at three hundred million metres per second.", None, 0.80,
     "c = 300,000,000 m/s", "handwritten: 'c = 300,000,000 m/s'")
line(9, "So c squared is ninety million billion.", None, 0.78,
     "the number expands", "'90,000,000,000,000,000' sprawling")
line(9, "Ninety million billion joules, for one kilogram of weight.", None, 0.80,
     "giant fraction drawn", "the fraction: tiny E over a huge graphite slab")
line(9, "Landolt's escaping heat weighed about a billionth of a gram.", None, 0.80,
     "swatch: reaction heat", "swatch strip: reaction heat, a billionth g")
line(9, "His balance could only see thirty millionths of a gram.",
     "His balance could only see 30 millionths of a gram.", 0.80,
     "swatch: balance limit", "swatch strip: balance sees 30 millionths g")
line(9, "Tens of thousands of times too coarse.", None, 0.76,
     "'×30,000' note", "coral '×30,000 too coarse' between swatches")
line(9, "Even a gram of radium radiates a whole year of heat that weighs just forty billionths of a gram,", None, 0.82,
     "radium capsule + year dial", "capsule drawn; 12-month dial around it")
line(9, "right at the edge of the finest balances — after twelve patient months.", None, 0.82,
     "balance needle barely moves", "needle drawn a hair off zero; 'a full year' note")

# ---------------- CHAPTER 10 — WEIGHING ATOMS ----------------
line(10, "So could anyone weigh energy at all?", None, 0.78,
     "chapter capsule 'weighing atoms'", "new region: Cambridge, 1932")
line(10, "It would take more energy per atom, and a way to weigh single atoms.", None, 0.82,
     "two requirements noted", "two notes: 'more energy per atom' / 'weigh single atoms'")
line(10, "Both arrived in Rutherford's lab in Cambridge.", None, 0.80,
     "lab bench, label", "vacuum chamber + magnet poles drawn")
line(10, "Atoms were no longer weighed on pans: flying through magnetic fields in a vacuum, the lighter ones curve more sharply. The bend became the scale.", None, 0.82,
     "curving ion paths", "dashed arcs: light atom bends hard, heavy bends less")
line(10, "On the fourteenth of April, nineteen thirty-two, researchers fired fast protons at a thin layer of lithium.",
     "On the 14th of April 1932, researchers fired fast protons at a thin layer of lithium.", 0.82,
     "date note; proton beam", "proton beam from left; thin lithium target")
line(10, "One watched from a darkened hut beneath the machine, shielded from X-rays.", None, 0.82,
     "dark hut cross-section", "hut drawn under the machine; observer figure inside")
line(10, "The screen lit up.", None, 0.74,
     "screen sparkles", "particle sparkles burst on the screen")
line(10, "Rutherford squeezed in: the flashes looked, he said, mighty like alpha particles.", None, 0.82,
     "quote note", "quote card: 'mighty like alpha particles'")
line(10, "A lithium nucleus had swallowed a proton and split into two helium nuclei,", None, 0.82,
     "the reaction diagram", "match cut: magnified reaction; lithium swallows proton")
line(10, "flying apart with seventeen point two million electron volts.",
     "flying apart with 17.2 million electron volts.", 0.80,
     "two alphas fly out", "shatter: two alpha particles burst apart with energy arrows")
line(10, "Lithium plus hydrogen outweighs two heliums.", None, 0.80,
     "mass ledger LHS", "ledger: 'Li + H > He + He'")
line(10, "If Einstein was right, the missing mass times c squared must equal that energy.", None, 0.82,
     "equation link", "coral '=' drawn between missing mass and energy")
line(10, "But lithium's nineteen thirty-two mass predicted only fourteen million electron volts, against seventeen.",
     "But lithium's 1932 mass predicted only 14 million electron volts, against 17.", 0.82,
     "blurry prediction bar", "bar: predicted 14 vs measured 17.2; 'blurry'")
line(10, "A year later, a more precise lithium mass raised the prediction to sixteen point eight — within a few percent. It matched.",
     "A year later, a more precise lithium mass raised the prediction to 16.8 — within a few percent. It matched.", 0.82,
     "prediction bar fixed", "bar re-registered: 16.8 close to 17.2; check mark")

# ---------------- CHAPTER 11 — THE SUN PROVES IT ----------------
line(11, "Weighing atoms had already explained something bigger.", None, 0.80,
     "chapter capsule 'the Sun proves it'", "new region: the stars")
line(11, "In nineteen twenty, helium proved lighter than the four hydrogens that build it.",
     "In 1920, helium proved lighter than the four hydrogens that build it.", 0.80,
     "4 H circles vs He", "four pale hydrogen circles drawn")
line(11, "Four point zero three one three, against four point zero zero two six.",
     "4.0313 against 4.0026.", 0.78,
     "the ledger numbers", "handwritten ledger: '4.0313 to 4.0026'")
line(11, "Arthur Eddington saw that the missing mass could power the stars.", None, 0.82,
     "Eddington label", "small telescope doodle; label 'Eddington, 1920'")
line(11, "Fusing hydrogen into helium leaves seven tenths of one percent missing, carried away as energy.", None, 0.82,
     "fusion arrow + lost chip", "four H merge into one He; a coral chip flies off")
line(11, "The Sun fuses six hundred million tons of hydrogen a second,",
     "The Sun fuses 600 million tons of hydrogen a second,", 0.82,
     "the Sun drawn", "sun with rays; '600,000,000 t/s' note")
line(11, "and four million tons of that never becomes matter — it leaves as light.",
     "and 4 million tons of that never becomes matter — it leaves as light.", 0.82,
     "light leaving the Sun", "rays leave; '4,000,000 t/s' in coral")
line(11, "The same equation runs the stars, and the battery in your pocket.", None, 0.80,
     "sun -> phone echo", "tiny phone doodle beside the sun; coral link")

# ---------------- CHAPTER 12 — YOUR PHONE, YOUR BODY ----------------
line(12, "So, back to the phones.", None, 0.74,
     "chapter capsule 'E = mc²'", "match cut: the ch1 balance region, aged")
line(12, "The charged one gained energy, and therefore mass: less than a billionth of a gram.", None, 0.82,
     "phone on the pan, tiny block", "charged phone redrawn; coral energy block on the pan")
line(12, "No balance can show it. We know it anyway:", None, 0.78,
     "the tilt, unmeasurable", "the tilt wedge again; 'unmeasurable' note")
line(12, "every kind of energy weighs exactly its amount, divided by c squared.", None, 0.80,
     "E = mc² written", "the equation written large, mustard block under 'mc²'")
line(12, "Almost all the mass of your body is energy too, locked in its protons and neutrons.", None, 0.82,
     "body outline + magnified proton", "body outline drawn; match cut: magnifier with a proton")
line(12, "The three quarks in a proton are less than one percent of its weight.", None, 0.82,
     "three quark dots", "three small dots in the proton; '<1%' note")
line(12, "The rest is the strong force — trapped, seething motion.", None, 0.80,
     "colour flood in the proton", "colour flood: the proton floods with energy texture")
line(12, "You are mostly stored energy, wearing the shape of a person. So is your phone.", None, 0.82,
     "body + phone blocks fill", "the body and phone blocks re-registered to coral")
line(12, "Charge it tonight, and in the morning, it will be ever so slightly heavier.", None, 0.78,
     "final composition: phone + equation", "camera settles: phone, balance, E = mc²; end card drawn")

# ---------------- write files ----------------
CH = [
 dict(n=1,  title="The Impossible Scale",        theme="hook"),
 dict(n=2,  title="Energy Is Not Stuff",          theme="setup"),
 dict(n=3,  title="The Old Rule",                 theme="history 1"),
 dict(n=4,  title="The Balance's Limit",          theme="history 2"),
 dict(n=5,  title="Radium Refuses to Behave",     theme="mystery"),
 dict(n=6,  title="Light Has Momentum",           theme="clue"),
 dict(n=7,  title="Einstein's First Argument",    theme="turn 1"),
 dict(n=8,  title="The Box of Light",             theme="turn 2"),
 dict(n=9,  title="Why Nobody Could See It",      theme="scale"),
 dict(n=10, title="Weighing Atoms",               theme="proof"),
 dict(n=11, title="The Sun Proves It",            theme="cosmic"),
 dict(n=12, title="Your Phone, Your Body, E=mc²", theme="landing"),
]
chapters = []
for c in CH:
    ls = [x for x in L if x["ch"] == c["n"]]
    chapters.append({
        "n": c["n"], "title": c["title"], "theme": c["theme"],
        "lines": [x["id"] for x in ls],
        "narration": " ".join(x["text"] for x in ls),
        "narration_display": " ".join(x["sub"] or x["text"] for x in ls),
        "words": len(re.findall(r"[A-Za-z0-9']+", " ".join(x["text"] for x in ls))),
        "speed_range": [min(x["speed"] for x in ls), max(x["speed"] for x in ls)],
    })

json.dump(L, open(os.path.join(PROJ, "script", "voice_lines.json"), "w"), indent=1)
json.dump(chapters, open(os.path.join(PROJ, "script", "chapters.json"), "w"), indent=1)

with open(os.path.join(PROJ, "script", "master_narration.txt"), "w", encoding="utf-8") as f:
    f.write("WHY YOUR PHONE GETS HEAVIER WHEN YOU CHARGE IT\n")
    f.write("Master narration - final (Kokoro af_heart, speed 0.70-0.82; 1,451 spoken words)\n\n")
    for c in chapters:
        f.write("=" * 70 + f"\nCHAPTER {c['n']} - {c['title'].upper()}  ({c['words']} words)\n" + "=" * 70 + "\n")
        f.write(c["narration_display"] + "\n\n")
    f.write("=" * 70 + "\nEND CARD (silent)\n" + "=" * 70 + "\nE = mc2 - energy has weight.\n")

tot = sum(c["words"] for c in chapters)
est = sum(c["words"] for c in chapters) / 148 * 60 + len(L) * 0.34 + 8
print(f"{len(L)} lines, {tot} words total, estimated film length ~{est/60:.1f} min")
for c in chapters:
    print(f"  ch{c['n']:>2} {c['title']:<32} {len(c['lines']):>2} lines {c['words']:>4} words")
