// QA stills only (never video): node qa_stills.mjs <project> <stills.json> [--out dir]
// <project> = the folder holding index.html; stills.json = [{"name": "ch01_000", "t": 0.9}, ...]
// Saves PNG stills (the library's still.mjs saves JPEG; QA here wants PNG per the master prompt).
import fs from 'fs'; import path from 'path';
import { openDemo, closeServer } from '../../repo/core/render/page.mjs';
const args = process.argv.slice(2);
const dir = args[0], spec = args[1], outArg = args.find(a => a.startsWith('--out'));
const outDir = outArg ? outArg.slice(6) : path.resolve(path.dirname(path.dirname(dir)), 'qa_stills');
fs.mkdirSync(outDir, { recursive: true });
const stills = JSON.parse(fs.readFileSync(spec, 'utf8'));
const { browser, page } = await openDemo(dir, { warnings: true });
for (const s of stills) {
  const t0 = Date.now();
  await page.evaluate(t => window.render(t), s.t);
  const f = path.join(outDir, `${s.name}.png`);
  await page.screenshot({ path: f, type: 'png' });
  console.log(`${s.name}  t=${s.t}  ${Date.now() - t0}ms`);
}
await browser.close(); closeServer();
