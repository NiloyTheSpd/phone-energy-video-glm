// Probe window.TEXTS boxes at given times for texts containing a substring
import { openDemo, closeServer } from '../../repo/core/render/page.mjs';
const dir = process.argv[2];
const times = process.argv[3].split(',').map(Number);
const needle = process.argv[4] || '';
const { browser, page } = await openDemo(dir, { warnings: false });
for (const t of times) {
  const boxes = await page.evaluate(([t, needle]) => {
    window.render(t);
    return (window.TEXTS(t) || []).filter(b => b.text.toLowerCase().includes(needle.toLowerCase()))
      .map(b => ({ text: b.text.slice(0, 30), x0: Math.round(b.x0), y0: Math.round(b.y0), x1: Math.round(b.x1), y1: Math.round(b.y1) }));
  }, [t, needle]);
  const c = await page.evaluate(t => { const c = window.CAMAT(t); return { x: Math.round(c.x), y: Math.round(c.y), z: +c.z.toFixed(3), r: +(c.r * 180 / Math.PI).toFixed(2) }; }, t);
  console.log(`t=${t} cam=${JSON.stringify(c)}`, JSON.stringify(boxes));
}
await browser.close(); closeServer();
