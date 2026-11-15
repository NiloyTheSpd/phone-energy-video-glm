// Diagnose which buffer is black in a screen region
import { openDemo, closeServer } from '../../repo/core/render/page.mjs';
const dir = process.argv[2], t = parseFloat(process.argv[3]);
// region in world coords
const rx0 = parseFloat(process.argv[4]), ry0 = parseFloat(process.argv[5]), rx1 = parseFloat(process.argv[6]), ry1 = parseFloat(process.argv[7]);
const { browser, page } = await openDemo(dir, { warnings: false });
const out = await page.evaluate(([t, rx0, ry0, rx1, ry1]) => {
  window.render(t);
  const X0 = -160, Y0 = -120, S = 1.75, BW = Math.round(4640 * S);
  const px0 = Math.max(0, Math.floor((rx0 - X0) * S)), py0 = Math.max(0, Math.floor((ry0 - Y0) * S));
  const px1 = Math.min(BW - 1, Math.ceil((rx1 - X0) * S)), py1 = Math.ceil((ry1 - Y0) * S);
  // reach into the page's internals via a debug hook
  const res = window.__diag(px0, py0, px1, py1);
  return res;
}, [t, rx0, ry0, rx1, ry1]);
console.log(JSON.stringify(out, null, 1));
await browser.close(); closeServer();
