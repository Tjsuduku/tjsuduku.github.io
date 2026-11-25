// Renders every design in art.html to JPG under web/public/works/.
// Usage (from the repo root):  node tools/works-art/render.js            all designs
//                              node tools/works-art/render.js bcaa ai     only these ids
// Needs Playwright once:  npm i -D playwright && npx playwright install chromium   (inside web/ is fine)
const path = require('path')
const fs = require('fs')
let chromium
try { ({ chromium } = require('playwright')) } catch { ({ chromium } = require(path.join(__dirname, '../../web/node_modules/playwright'))) }

const ART = 'file://' + path.join(__dirname, 'art.html')
// Drawn versions go to tools/works-art/out so they never overwrite the photo covers in web/public/works.
const OUT = path.join(__dirname, 'out')

;(async () => {
  const b = await chromium.launch()
  const p = await b.newPage()
  await p.goto(ART + '#cover-events')
  const all = await p.evaluate(() => window.__DESIGNS)
  const only = process.argv.slice(2)
  for (const [id, d] of Object.entries(all)) {
    if (only.length && !only.includes(id) && !only.some((o) => id.endsWith(o))) continue
    await p.setViewportSize({ width: d.w, height: d.h })
    await p.goto(ART + '#' + encodeURIComponent(id))
    await p.reload()
    await p.evaluate(() => window.__READY)
    await p.waitForTimeout(150)
    const file = path.join(OUT, d.out)
    fs.mkdirSync(path.dirname(file), { recursive: true })
    await p.screenshot({ path: file, type: 'jpeg', quality: 84 })
    console.log(id.padEnd(26), (fs.statSync(file).size / 1024).toFixed(0) + ' KB', d.out)
  }
  await b.close()
})()
