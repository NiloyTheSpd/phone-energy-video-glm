// Page-layout QA: node text_collisions.mjs <project> [--out coll.json]
// Camera-free page-layout check: every pair of on-page texts whose WORLD boxes
// overlap (the page accumulates, so any two texts eventually share the screen).
// Also flags texts outside the canvas content area.
import fs from 'fs'; import path from 'path';
import { openDemo, closeServer } from '../repo/core/render/page.mjs';
const dir = process.argv[2];
const outArg = process.argv.includes('--out') ? process.argv[process.argv.indexOf('--out') + 1] : '/tmp/collisions.json';
const { browser, page } = await openDemo(dir, { q: 'clean=1', warnings: false });
const DUR = await page.evaluate(() => window.DUR);
const boxes = await page.evaluate(() => window.__TEXTBOXES());
await browser.close(); await closeServer();
const ov = (a, b) => Math.min(a[2], b[2]) - Math.max(a[0], b[0]) > 6 && Math.min(a[3], b[3]) - Math.max(a[1], b[1]) > 5;
const issues = [];
for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++) {
  const a = boxes[i], b = boxes[j];
  if (ov(a.box, b.box))
    issues.push({ a: a.text, b: b.text, abox: a.box, bbox: b.box, ta: +a.t0.toFixed(1), tb: +b.t0.toFixed(1) });
}
for (const t of boxes) {
  if (t.box[2] > 4340 || t.box[0] < -30 || t.box[3] > 2660 || t.box[1] < -30)
    issues.push({ type: 'outside-canvas', a: t.text, abox: t.box });
}
fs.writeFileSync(outArg, JSON.stringify({ DUR, n: boxes.length, issues }, null, 1));
console.log(`texts: ${boxes.length}  collisions: ${issues.length - issues.filter(i => i.type).length}  outside: ${issues.filter(i => i.type).length}`);
for (const i of issues.slice(0, 80)) {
  if (i.type) { console.log(`OUTSIDE: "${i.a}" box=${i.abox.map(v => v | 0)}`); continue; }
  console.log(`ov "${i.a}" @${i.ta} ${i.abox.map(v => v | 0)}  ||  "${i.b}" @${i.tb} ${i.bbox.map(v => v | 0)}`);
}
