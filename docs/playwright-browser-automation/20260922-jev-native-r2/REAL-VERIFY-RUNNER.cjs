'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { performance } = require('node:perf_hooks');

const WORKSPACE = 'C:\\Users\\A\\playwright-browser-automation5-final-reality-competition-work';
const BROWSER_ROOT = 'C:\\AI\\Playwright-Native-AI-Browser';
const GOLDEN = path.join(BROWSER_ROOT, 'scripts', 'golden-harness.cjs');
const FIXTURE = path.join(BROWSER_ROOT, 'scripts', 'local-fixture-server.cjs');
const UPLOAD = path.join(BROWSER_ROOT, 'tests', 'fixtures', 'upload.txt');
const PROFILE = path.join(BROWSER_ROOT, 'profile', 'tests', 'library');
const OUT_ROOT = path.join(WORKSPACE, 'TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW', 'JEV-NATIVE-VIRTUAL-99', 'REAL-VERIFY');

const EXPECTED = Object.freeze({
  taskSha256: '31f60923bddd1fece2a1d64a574f6ad5a3bc16fd0b0ef01127c87522e7084960',
  validRuleSha256: '2d2e4ab5495fdffb921a57113e6c7ecf5e9cf6802f9a729386bf941a3fd5c7ae',
  goldenSha256: '1c67a634e0c0fc24ed057752358f4c20a6c05550be6146fd8d11b1a723f25e08',
  browserR3FingerprintSha256: '9a3b067287d64b6ec28d09a86fc92a88de710597148d37ce1ca8bc7b51713edd',
  targetMs: 820,
  matureMaxMs: 1050,
  historicalMs: 1525.09,
  warmups: 3,
  runs: 30,
});

function sha256File(file) {
  return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
}
function fail(delta, error) {
  if (error) process.stderr.write(String(error && error.stack ? error.stack : error) + '\n');
  process.stdout.write([
    'REAL_RUNS=0',
    'VALID_RUNS=0',
    'T_REAL_MIN_MS=N/A',
    'T_REAL_P50_MS=N/A',
    'T_REAL_P95_MS=N/A',
    'T_REAL_MAX_MS=N/A',
    'TARGET_820_REACHED=NOT_EVALUATED',
    'MATURE_1050_REACHED=NOT_EVALUATED',
    'BEATS_1525_09=NOT_EVALUATED',
    `NEW_T_STAR_REAL_MS=${EXPECTED.historicalMs}`,
    `REALITY_DELTA=${delta}`,
    'ACTION=STOP',
    'RETURN_TO_GPT=YES',
  ].join('\n') + '\n');
  process.exitCode = 2;
}
function percentileNearestRank(values, p) {
  const a = [...values].sort((x, y) => x - y);
  return a[Math.max(0, Math.ceil(p * a.length) - 1)];
}
function fmt(n) { return Number(n).toFixed(2); }

(async () => {
  try {
    for (const p of [WORKSPACE, BROWSER_ROOT, GOLDEN, FIXTURE, UPLOAD, PROFILE]) {
      if (!fs.existsSync(p)) return fail(`REQUIRED_PATH_MISSING:${p}`);
    }
    const goldenHash = sha256File(GOLDEN);
    if (goldenHash !== EXPECTED.goldenSha256) {
      return fail(`CANONICAL_GOLDEN_SHA_MISMATCH:${goldenHash}`);
    }

    const twinProfile = path.join(WORKSPACE, 'TWIN-PLAYWRIGHT-GOLDEN-REALITY-SHADOW', 'PLAYWRIGHT_GOLDEN_REALITY_PROFILE.json');
    if (!fs.existsSync(twinProfile)) return fail('TWIN_PROFILE_MISSING');
    const profile = JSON.parse(fs.readFileSync(twinProfile, 'utf8'));
    if (profile.task_sha256 !== EXPECTED.taskSha256) return fail('TASK_SHA_MISMATCH');
    if (profile.valid_rule_sha256 !== EXPECTED.validRuleSha256) return fail('VALID_RULE_SHA_MISMATCH');
    if (profile.browser_r3_fingerprint_sha256 !== EXPECTED.browserR3FingerprintSha256) return fail('BROWSER_R3_FINGERPRINT_MISMATCH');
    if (profile.canonical_golden_sha256 !== EXPECTED.goldenSha256) return fail('TWIN_GOLDEN_SHA_MISMATCH');

    const { chromium } = require(GOLDEN);
    const { createFixtureServer } = require(FIXTURE);
    fs.mkdirSync(OUT_ROOT, { recursive: true });

    const fixture = await createFixtureServer(0);
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ acceptDownloads: true });
    context.setDefaultTimeout(5000);
    const page = await context.newPage();

    // Fixed Golden is deterministic. Per the frozen JEV policy, CODE owns
    // uniquely determined action selection, so JEV calls are intentionally 0.
    await page.route('**/api', route => route.fulfill({ json: { source: 'intercepted' } }));

    async function resetReady() {
      for (const p of context.pages()) {
        if (p !== page) await p.close().catch(() => {});
      }
      await page.goto(fixture.baseURL, { waitUntil: 'commit' });
      await page.getByTestId('title').waitFor();
    }

    async function one(round, measured) {
      await resetReady();
      const t0 = performance.now();
      try {
        if (await page.getByTestId('title').textContent() !== 'Native AI Fixture Ready') throw new Error('state mismatch');

        await page.click('#second-link');
        await page.goBack({ waitUntil: 'commit' });
        await page.getByTestId('title').waitFor();

        if (await page.getByRole('button').count() < 4) throw new Error('locator mismatch');

        await page.getByLabel('Name').fill('round-' + round);
        await page.selectOption('#color', 'blue');
        await page.check('#agree');
        await page.click('#submit');
        if (await page.locator('#form-result').textContent() !== `round-${round}:blue:true`) throw new Error('extract mismatch');

        await page.getByLabel('Keyboard target').pressSequentially('ABC');
        await page.dragAndDrop('#drag', '#drop');
        if (await page.locator('#drop').textContent() !== 'native-drag') throw new Error('drag mismatch');

        await page.setInputFiles('#upload', UPLOAD);
        const [download] = await Promise.all([page.waitForEvent('download'), page.click('#download')]);
        if (measured) {
          const dl = path.join(OUT_ROOT, `run-${String(round).padStart(2, '0')}-download.txt`);
          await download.saveAs(dl);
        }

        const dialog = page.waitForEvent('dialog').then(async d => {
          if (d.message() !== 'native-dialog') throw new Error('dialog mismatch');
          await d.accept();
        });
        await Promise.all([dialog, page.click('#dialog')]);

        const [popup] = await Promise.all([page.waitForEvent('popup'), page.click('#popup')]);
        await popup.locator('#popup-ready').waitFor();
        await popup.close();

        const frame = page.frameLocator('#frame');
        await frame.locator('#frame-button').click();
        if (await frame.locator('#frame-result').textContent() !== 'frame-clicked') throw new Error('frame mismatch');

        await page.click('#api');
        await page.locator('#api-result').filter({ hasText: 'intercepted' }).waitFor();
        if (await page.locator('#api-result').textContent() !== 'intercepted') throw new Error('route mismatch');

        const isolated = await browser.newContext();
        try {
          const ip = await isolated.newPage();
          await ip.goto(fixture.baseURL, { waitUntil: 'commit' });
          if (await ip.evaluate(() => localStorage.getItem('native')) !== null) throw new Error('isolation mismatch');
        } finally {
          await isolated.close();
        }

        const t1 = performance.now();
        return { pass: true, tValidMs: t1 - t0 };
      } catch (error) {
        return { pass: false, tValidMs: performance.now() - t0, error: String(error && error.stack ? error.stack : error) };
      }
    }

    try {
      await resetReady();
      for (let i = 1; i <= EXPECTED.warmups; i++) {
        const r = await one(i, false);
        if (!r.pass) return fail(`WARMUP_FAIL:${i}`, r.error);
      }

      const results = [];
      for (let i = 1; i <= EXPECTED.runs; i++) {
        const r = await one(i, true);
        results.push(r);
        if (!r.pass) {
          fs.writeFileSync(path.join(OUT_ROOT, 'FAILED-RUN.json'), JSON.stringify({ run: i, ...r }, null, 2));
          process.stdout.write([
            `REAL_RUNS=${results.length}`,
            `VALID_RUNS=${results.filter(x => x.pass).length}`,
            'T_REAL_MIN_MS=N/A',
            'T_REAL_P50_MS=N/A',
            'T_REAL_P95_MS=N/A',
            'T_REAL_MAX_MS=N/A',
            'TARGET_820_REACHED=NOT_EVALUATED',
            'MATURE_1050_REACHED=NOT_EVALUATED',
            'BEATS_1525_09=NOT_EVALUATED',
            `NEW_T_STAR_REAL_MS=${EXPECTED.historicalMs}`,
            `REALITY_DELTA=MEASURED_RUN_FAIL:${i}`,
            'ACTION=STOP',
            'RETURN_TO_GPT=YES',
          ].join('\n') + '\n');
          process.exitCode = 3;
          return;
        }
      }

      const vals = results.map(r => r.tValidMs).sort((a, b) => a - b);
      const min = vals[0];
      const p50 = percentileNearestRank(vals, 0.50);
      const p95 = percentileNearestRank(vals, 0.95);
      const max = vals[vals.length - 1];
      const newStar = Math.min(EXPECTED.historicalMs, min);

      fs.writeFileSync(path.join(OUT_ROOT, 'REAL-VERIFY-RESULT.json'), JSON.stringify({
        freeze_id: 'JEV-NATIVE-PLAYWRIGHT-EXTREME-V1-R2-EXECUTABLE',
        task_sha256: EXPECTED.taskSha256,
        valid_rule_sha256: EXPECTED.validRuleSha256,
        canonical_golden_sha256: EXPECTED.goldenSha256,
        warmups: EXPECTED.warmups,
        measured_runs: EXPECTED.runs,
        valid_runs: results.length,
        jev_calls: 0,
        jev_reason: 'Fixed Golden action selection is uniquely determined by state + frozen contract; CODE path required by JEV Virtual-99 policy.',
        min_ms: min,
        p50_ms: p50,
        p95_ms: p95,
        max_ms: max,
        target_820_reached: min <= EXPECTED.targetMs,
        mature_1050_reached: min <= EXPECTED.matureMaxMs,
        beats_1525_09: min < EXPECTED.historicalMs,
        new_t_star_real_ms: newStar,
        results: results.map((r, i) => ({ run: i + 1, t_valid_ms: r.tValidMs, valid: true })),
      }, null, 2));

      process.stdout.write([
        `REAL_RUNS=${EXPECTED.runs}`,
        `VALID_RUNS=${EXPECTED.runs}`,
        `T_REAL_MIN_MS=${fmt(min)}`,
        `T_REAL_P50_MS=${fmt(p50)}`,
        `T_REAL_P95_MS=${fmt(p95)}`,
        `T_REAL_MAX_MS=${fmt(max)}`,
        `TARGET_820_REACHED=${min <= EXPECTED.targetMs ? 'YES' : 'NO'}`,
        `MATURE_1050_REACHED=${min <= EXPECTED.matureMaxMs ? 'YES' : 'NO'}`,
        `BEATS_1525_09=${min < EXPECTED.historicalMs ? 'YES' : 'NO'}`,
        `NEW_T_STAR_REAL_MS=${fmt(newStar)}`,
        'REALITY_DELTA=NONE',
        'ACTION=STOP',
        'RETURN_TO_GPT=NO',
      ].join('\n') + '\n');
    } finally {
      await context.close().catch(() => {});
      await browser.close().catch(() => {});
      await fixture.close().catch(() => {});
    }
  } catch (error) {
    fail('RUNNER_EXCEPTION', error);
  }
})();
