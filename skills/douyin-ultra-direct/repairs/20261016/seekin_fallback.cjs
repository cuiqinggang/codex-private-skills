// Reuse the installed Playwright and the existing configured browser only.
// No launch, profile switch, existing-tab navigation, login or cookie extraction.
const fs = require('fs');
const path = require('path');
const ROOT = 'C:\\AI\\Playwright-Native-AI-Browser';
const pw = require(path.join(ROOT, 'node_modules', 'playwright-core'));
const share = process.argv[2];
if (!/^https:\/\/(?:v\.|www\.)?douyin\.com\//.test(share || '')) throw Error('INVALID_SHARE_URL');
let browser, page;
const created = new Set();
const started = Date.now();
let finished = false;
async function cleanup() {
  if (finished) return;
  finished = true;
  clearTimeout(watchdog);
  for (const ownPage of created) await ownPage.close().catch(() => {});
  if (browser) await browser.close().catch(() => {});
}
const watchdog = setTimeout(async () => {
  process.stderr.write('SEEKIN_TOTAL_TIMEOUT\n');
  process.exitCode = 1;
  await cleanup();
}, 115000);
const allowedMedia = value => {
  try { const u = new URL(value); return u.protocol === 'https:' && /(?:^|\.)(?:douyinvod|douyin|bytecdn|snssdk)\.com$/.test(u.hostname); }
  catch { return false; }
};
(async () => {
  const cfg = JSON.parse(fs.readFileSync(path.join(ROOT, 'app', 'mcp-persistent.config.json'), 'utf8'));
  const endpoint = cfg.browser?.cdpEndpoint;
  if (!/^http:\/\/(?:127\.0\.0\.1|localhost):\d+$/.test(endpoint || '')) throw Error('EXISTING_LOCAL_CDP_CONFIG_REQUIRED');
  browser = await pw.chromium.connectOverCDP(endpoint, { timeout: Math.min(30000, cfg.browser.cdpTimeout || 30000) });
  const context = browser.contexts()[0];
  if (!context) throw Error('EXISTING_BROWSER_CONTEXT_REQUIRED');
  page = await context.newPage();
  created.add(page);
  page.on('popup', popup => created.add(popup));
  await page.goto('https://www.seekin.ai/douyin-downloader/', { waitUntil: 'domcontentloaded', timeout: 20000 });
  await page.getByRole('textbox').fill(share, { timeout: 5000 });
  await page.getByRole('button', { name: 'Download', exact: true }).click({ timeout: 5000 });
  await page.getByRole('button', { name: /(?:720P|1080P).*MP4/ }).first().waitFor({ state: 'visible', timeout: 30000 });
  let result = page.getByRole('button', { name: /720P.*MP4/ }).first();
  if (!await result.count()) result = page.getByRole('button', { name: /1080P.*MP4.*With audio/ }).first();
  if (!await result.count()) throw Error('COMPATIBLE_AUDIO_VIDEO_CHOICE_MISSING');
  const title = await page.locator('img[alt]').evaluateAll(images => images.map(i => i.alt).filter(s => s && !/logo/i.test(s)).join(' | '));
  const popupPromise = page.waitForEvent('popup', { timeout: 10000 });
  await result.click({ timeout: 5000 });
  const popup = await popupPromise;
  created.add(popup);
  await popup.waitForURL(url => allowedMedia(String(url)), { timeout: 10000, waitUntil: 'commit' });
  const url = popup.url();
  if (!allowedMedia(url)) throw Error('UNEXPECTED_MEDIA_HOST');
  process.stdout.write(JSON.stringify({ url, title, quality: '720P', provider: 'SEEKIN_EXISTING_BROWSER', elapsed_ms: Date.now() - started }) + '\n');
})().catch(async error => {
  if (page) process.stderr.write('RESULT_PAGE: ' + (await page.locator('body').innerText({ timeout: 2000 }).catch(() => '')).slice(0, 3500) + '\n');
  process.stderr.write(String(error.message).slice(0, 1500) + '\n');
  process.exitCode = 1;
}).finally(cleanup);
