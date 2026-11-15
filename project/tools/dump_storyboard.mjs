// Dump the storyboard JSONs from the live page data: chapters, shots, camera, marks, audio_sync.
// Run from the library root: node <project>/tools/dump_storyboard.mjs <project>
import fs from 'fs'; import path from 'path';
import { openDemo, closeServer } from '../../repo/core/render/page.mjs';
const dir = process.argv[2];
const outDir = path.join(dir, 'storyboard');
fs.mkdirSync(outDir, { recursive: true });
const { browser, page } = await openDemo(dir, { warnings: false });
const data = await page.evaluate(() => {
  const TLb = window.TL_DUMP || null;
  const sb = window.STORYBOARD || {};
  const cam = window.__camdump ? window.__camdump() : [];
  // marks: every EL with its timing, kind and world anchor
  const marks = (window.EL_DUMP || []).map((e, i) => ({
    i, t0: +e.t0.toFixed(3), d: +e.d.toFixed(3), kind: e.kind,
    anchor: e.wx ? [+e.wx[0].toFixed(1), +e.wx[1].toFixed(1)] : null,
    text: e.T ? e.T.s : undefined
  }));
  return { sb, cam, marks, dur: window.DUR };
});
// timeline data comes from the JSON the page already loaded
const TL = JSON.parse(fs.readFileSync(path.join(dir, 'voice', 'timeline.json'), 'utf8'));
const cues = JSON.parse(fs.readFileSync(path.join(dir, 'voice', 'cues.json'), 'utf8'));
const chaptersMeta = JSON.parse(fs.readFileSync(path.join(dir, 'script', 'chapters.json'), 'utf8'));

const chOf = t => { let n = 1; for (const c of TL.chapters) if (t >= c.t0 - 0.45) n = c.n; return n; };
const kindName = { g: 'gesture (two fingers settle)', d: 'drift', i: 'push in (accelerating)', c: 'cut (match cut)', f: 'follow the stylus', p: 'punch in' };

// ---- chapters.json ----
const chapters = TL.chapters.map(c => {
  const m = chaptersMeta.find(x => x.n === c.n);
  const lines = TL.lines.filter(l => l.ch === c.n);
  const camKeys = data.cam.filter(k => k.t >= c.t0 - 0.6 && k.t < (TL.chapters[c.n] ? TL.chapters[c.n].t0 - 0.6 : 1e9));
  return {
    n: c.n, title: m.title, theme: m.theme,
    target_duration: +(c.t1 - c.t0).toFixed(2),
    narration: m.narration_display,
    visual_objective: (data.sb[c.n] || {}).idea || '',
    page_region_cell: (data.sb[c.n] || {}).cell || null,
    initial_camera: camKeys[0] || null,
    camera_keyframes: camKeys,
    marks_count: data.marks.filter(k => k.t0 >= c.t0 - 0.5 && k.t0 < c.t1 + 0.2).length,
    notes: lines.filter(l => l.visual_cue).map(l => l.visual_cue),
    lines: lines.map(l => ({ id: l.id, t0: l.t0, t1: l.t1, cue: l.visual_cue, event: l.event })),
    transition_into_next: c.n < 12 ? `camera gesture to chapter ${c.n + 1} during the ${TL.gaps.between_chapters}s gap` : 'settle on the end card (no whole-page pull-back)'
  };
});
fs.writeFileSync(path.join(outDir, 'chapters.json'), JSON.stringify({ total: TL.total, chapters }, null, 1));

// ---- shots.json (one shot per camera key) ----
const shots = [];
data.cam.forEach((k, i) => {
  const next = data.cam[i + 1];
  const lines = TL.lines.filter(l => l.t0 >= k.t - 0.05 && (!next || l.t0 < next.t));
  shots.push({
    n: i + 1, t0: +k.t.toFixed(2), t1: next ? +next.t.toFixed(2) : TL.total,
    move: kindName[k.k] || k.k, framing: { x: k.x, y: k.y, zoom: k.z, rot_deg: k.r },
    chapter: chOf(k.t + 0.05),
    lines_here: lines.map(l => l.id),
    draws: data.marks.filter(m => m.t0 >= k.t - 0.02 && (!next || m.t0 < next.t)).length
  });
});
fs.writeFileSync(path.join(outDir, 'shots.json'), JSON.stringify({ shots }, null, 1));

// ---- camera.json ----
fs.writeFileSync(path.join(outDir, 'camera.json'), JSON.stringify({
  grammar: "k: d drift · g gesture (quick start, settles) · i push in · c cut (match cut) · f follow the stylus · p punch-in. Zoom is relative to the 1920x1080 frame over the 4640x2760 canvas.",
  keys: data.cam
}, null, 1));

// ---- marks.json ----
fs.writeFileSync(path.join(outDir, 'marks.json'), JSON.stringify({
  note: 'every PEN/BLOB/TXT/OCC mark in draw order; t0 is its narration-aligned start',
  count: data.marks.length,
  marks: data.marks.map(m => ({ ...m, chapter: chOf(m.t0) }))
}, null, 1));

// ---- audio_sync.json ----
fs.writeFileSync(path.join(outDir, 'audio_sync.json'), JSON.stringify({
  method: 'Kokoro af_heart per line; faster-whisper base.en word timestamps; placement from measured WAV durations',
  total: TL.total,
  gaps: TL.gaps,
  lines: TL.lines.map(l => ({
    id: l.id, chapter: l.ch, t0: l.t0, t1: l.t1, dur: l.dur, speed: l.speed,
    text: l.sub || l.text, cue: l.visual_cue, event: l.event,
    subtitle_cue: (cues.cues.find(c => c.line_ids.includes(l.id)) || {}).id
  })),
  subtitle_cues: cues.cues.map(c => ({ id: c.id, t0: c.t0, t1: c.t1, text: c.en + (c.en2 ? ' ' + c.en2 : ''), hold: +(c.t1 - c.t0).toFixed(2), spoken: c.spoken }))
}, null, 1));

console.log('storyboard JSONs written to', outDir);
console.log(`chapters ${chapters.length}, shots ${shots.length}, marks ${data.marks.length}, lines ${TL.lines.length}, cues ${cues.cues.length}`);
await browser.close(); closeServer();
