import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';

const now = () => new Date().toISOString();
const sha256 = data => crypto.createHash('sha256').update(data).digest('hex');

function safeUrl(input) {
  try {
    const u = new URL(String(input));
    u.username = '';
    u.password = '';
    u.search = '';
    u.hash = '';
    return u.toString();
  } catch {
    return '<UNPARSEABLE_URL>';
  }
}

function safeHeaders(headers = {}) {
  return Object.keys(headers).sort();
}

function jsonLine(obj) {
  return JSON.stringify(obj) + '\n';
}

async function mkdirs(root) {
  await fs.mkdir(path.join(root, 'raw'), { recursive: true });
  await fs.mkdir(path.join(root, 'safe'), { recursive: true });
}

async function append(file, obj) {
  await fs.appendFile(file, jsonLine(obj), 'utf8');
}

async function writeJson(file, obj) {
  await fs.writeFile(file, JSON.stringify(obj, null, 2) + '\n', 'utf8');
}

function bufferInfo(payload) {
  const b = Buffer.isBuffer(payload) ? payload : Buffer.from(String(payload ?? ''), 'utf8');
  return { bytes: b.length, sha256: sha256(b) };
}

async function actionabilityProbe(page, selector) {
  const locator = page.locator(selector);
  const count = await locator.count();
  if (count !== 1) {
    return { selector, captured_at: now(), locator_count: count, exactly_one: false };
  }

  const visible = await locator.isVisible().catch(() => false);
  const enabled = await locator.isEnabled().catch(() => false);
  const box1 = await locator.boundingBox().catch(() => null);

  await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
  const box2 = await locator.boundingBox().catch(() => null);

  const sameBox = !!box1 && !!box2 &&
    ['x','y','width','height'].every(k => Math.abs(box1[k] - box2[k]) < 0.01);

  const dom = await locator.evaluate(el => {
    const r = el.getBoundingClientRect();
    const x = r.left + r.width / 2;
    const y = r.top + r.height / 2;
    const hit = document.elementFromPoint(x, y);
    const cs = getComputedStyle(el);
    const animations = el.getAnimations({ subtree: true }).map(a => ({
      playState: a.playState,
      pending: a.pending,
      currentTime: a.currentTime,
      effect: a.effect?.getTiming?.() ?? null
    }));
    const hitDesc = hit ? {
      tag: hit.tagName,
      id: hit.id || null,
      classes: typeof hit.className === 'string' ? hit.className : null
    } : null;
    return {
      ready_state: document.readyState,
      visibility_state: document.visibilityState,
      computed_style: {
        display: cs.display,
        visibility: cs.visibility,
        opacity: cs.opacity,
        pointer_events: cs.pointerEvents,
        z_index: cs.zIndex,
        position: cs.position,
        transform: cs.transform
      },
      center: { x, y },
      hit_target: hitDesc,
      receives_events_approx: !!hit && (hit === el || el.contains(hit)),
      active_animations: animations
    };
  }).catch(error => ({ probe_error: String(error) }));

  return {
    selector,
    captured_at: now(),
    locator_count: count,
    exactly_one: true,
    visible,
    enabled,
    bounding_box_frame_1: box1,
    bounding_box_frame_2: box2,
    stable_approx_two_animation_frames: sameBox,
    ...dom
  };
}

export async function startBrowserRealityR3({
  context,
  page,
  outputDir,
  targetSelector = '#dialog',
  declaredConfig = {},
  taskId = 'GOLDEN_TASK',
  enableTrace = true
}) {
  if (!context || !page || !outputDir) throw new Error('context, page and outputDir are required');

  await mkdirs(outputDir);
  const safeEvents = path.join(outputDir, 'safe', 'events.jsonl');
  const rawCdp = path.join(outputDir, 'raw', 'cdp.jsonl');
  const safeCdp = path.join(outputDir, 'safe', 'cdp.jsonl');
  const actionability = [];

  const record = async (type, data = {}) => {
    await append(safeEvents, { ts: now(), type, ...data });
  };

  const reqSafe = request => ({
    url: safeUrl(request.url()),
    method: request.method(),
    resource_type: request.resourceType(),
    header_names: safeHeaders(request.headers()),
    is_navigation_request: request.isNavigationRequest()
  });

  context.on('request', request => { void record('request', reqSafe(request)); });
  context.on('requestfinished', request => { void record('requestfinished', reqSafe(request)); });
  context.on('requestfailed', request => {
    void record('requestfailed', { ...reqSafe(request), failure: request.failure()?.errorText ?? null });
  });
  context.on('response', response => {
    void record('response', {
      url: safeUrl(response.url()),
      status: response.status(),
      status_text: response.statusText(),
      header_names: safeHeaders(response.headers()),
      from_service_worker: response.fromServiceWorker?.() ?? null
    });
  });
  context.on('page', p => { void record('context_page', { url: safeUrl(p.url()) }); });
  context.on('serviceworker', w => { void record('service_worker', { url: safeUrl(w.url()) }); });

  page.on('console', msg => {
    void record('console', { level: msg.type(), text_sha256: sha256(msg.text()), location: msg.location() });
  });
  page.on('pageerror', error => {
    void record('pageerror', { name: error.name, message_sha256: sha256(error.message), stack_sha256: sha256(error.stack ?? '') });
  });
  page.on('crash', () => { void record('page_crash'); });
  page.on('worker', w => { void record('worker', { url: safeUrl(w.url()) }); });
  page.on('websocket', ws => {
    void record('websocket_open', { url: safeUrl(ws.url()) });
    ws.on('framesent', data => { void record('websocket_frame_sent', bufferInfo(data.payload)); });
    ws.on('framereceived', data => { void record('websocket_frame_received', bufferInfo(data.payload)); });
    ws.on('socketerror', error => { void record('websocket_error', { error_sha256: sha256(String(error)) }); });
    ws.on('close', () => { void record('websocket_close', { url: safeUrl(ws.url()) }); });
  });

  if (enableTrace) {
    try {
      await context.tracing.start({ screenshots: true, snapshots: true, sources: true });
      await record('trace_start', { status: 'STARTED' });
    } catch (error) {
      await record('trace_start', { status: 'NOT_STARTED', error_sha256: sha256(String(error)) });
    }
  }

  const cdp = await context.newCDPSession(page).catch(() => null);
  if (cdp) {
    const selected = [
      'Network.requestWillBeSent','Network.responseReceived','Network.loadingFailed','Network.loadingFinished',
      'Network.requestServedFromCache','Network.webSocketCreated','Network.webSocketWillSendHandshakeRequest',
      'Network.webSocketHandshakeResponseReceived','Network.webSocketFrameSent','Network.webSocketFrameReceived',
      'Network.webSocketFrameError','Network.webSocketClosed',
      'Page.domContentEventFired','Page.loadEventFired','Page.frameAttached','Page.frameDetached','Page.frameNavigated',
      'Page.frameStartedLoading','Page.frameStoppedLoading','Page.lifecycleEvent',
      'Page.javascriptDialogOpening','Page.javascriptDialogClosed',
      'Runtime.consoleAPICalled','Runtime.exceptionThrown'
    ];
    const sanitizeCdp = (method, params) => {
      const clone = JSON.parse(JSON.stringify(params ?? {}));
      const scrub = value => {
        if (!value || typeof value !== 'object') return;
        for (const [k,v] of Object.entries(value)) {
          if (typeof v === 'string' && /url$/i.test(k)) value[k] = safeUrl(v);
          else if (/headers|cookies|postData|requestHeaders|responseHeaders|authorization|cookie/i.test(k)) value[k] = '<REDACTED>';
          else if (v && typeof v === 'object') scrub(v);
        }
      };
      scrub(clone);
      return { ts: now(), method, params: clone };
    };
    for (const method of selected) {
      cdp.on(method, params => {
        void append(rawCdp, { ts: now(), method, params });
        void append(safeCdp, sanitizeCdp(method, params));
      });
    }
    await cdp.send('Network.enable').catch(() => {});
    await cdp.send('Page.enable').catch(() => {});
    await cdp.send('Page.setLifecycleEventsEnabled', { enabled: true }).catch(() => {});
    await cdp.send('Runtime.enable').catch(() => {});
    await cdp.send('Performance.enable').catch(() => {});
  }

  const browser = context.browser?.() ?? null;
  let browserVersion = null;
  let systemInfo = null;
  let browserCommandLine = null;
  if (browser?.newBrowserCDPSession) {
    const bcdp = await browser.newBrowserCDPSession().catch(() => null);
    if (bcdp) {
      browserVersion = await bcdp.send('Browser.getVersion').catch(() => null);
      systemInfo = await bcdp.send('SystemInfo.getInfo').catch(() => null);
      browserCommandLine = await bcdp.send('Browser.getBrowserCommandLine').catch(() => null);
      await bcdp.detach().catch(() => {});
    }
  }

  const runtimeEnv = await page.evaluate(() => ({
    href: location.href,
    title: document.title,
    readyState: document.readyState,
    visibilityState: document.visibilityState,
    userAgent: navigator.userAgent,
    platform: navigator.platform,
    language: navigator.language,
    languages: navigator.languages,
    hardwareConcurrency: navigator.hardwareConcurrency,
    deviceMemory: navigator.deviceMemory ?? null,
    webdriver: navigator.webdriver,
    cookieEnabled: navigator.cookieEnabled,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    dpr: devicePixelRatio,
    screen: {
      width: screen.width, height: screen.height,
      availWidth: screen.availWidth, availHeight: screen.availHeight,
      colorDepth: screen.colorDepth, pixelDepth: screen.pixelDepth
    }
  }));

  const storageState = await context.storageState();
  await writeJson(path.join(outputDir, 'raw', 'storage-state.json'), storageState);
  const storageSafe = {
    cookies: storageState.cookies.map(c => ({
      name: c.name,
      domain: c.domain,
      path: c.path,
      expires: c.expires,
      httpOnly: c.httpOnly,
      secure: c.secure,
      sameSite: c.sameSite,
      value_sha256: sha256(c.value)
    })),
    origins: (storageState.origins ?? []).map(o => ({
      origin: safeUrl(o.origin),
      localStorage: (o.localStorage ?? []).map(x => ({ name: x.name, value_sha256: sha256(x.value) }))
    }))
  };

  const sessionStorageSafe = await page.evaluate(() =>
    Object.keys(sessionStorage).sort().map(k => [k, sessionStorage.getItem(k)])
  ).then(entries => entries.map(([name,value]) => ({ name, value_sha256: sha256(String(value)) })))
   .catch(() => []);

  const envSafe = {
    task_id: taskId,
    captured_at: now(),
    target_selector: targetSelector,
    declared_config: declaredConfig,
    browser_version: browserVersion,
    browser_command_line: browserCommandLine,
    system_info: systemInfo,
    runtime: { ...runtimeEnv, href: safeUrl(runtimeEnv.href), title_sha256: sha256(runtimeEnv.title) },
    viewport: page.viewportSize(),
    context_pages: context.pages().map(p => safeUrl(p.url())),
    service_workers: context.serviceWorkers().map(w => safeUrl(w.url())),
    storage_state_safe: storageSafe,
    session_storage_safe: sessionStorageSafe
  };
  delete envSafe.runtime.title;
  await writeJson(path.join(outputDir, 'safe', 'environment.json'), envSafe);

  if (cdp) {
    const domSnapshot = await cdp.send('DOMSnapshot.captureSnapshot', {
      computedStyles: ['display','visibility','opacity','pointer-events','z-index','position','transform'],
      includePaintOrder: true,
      includeDOMRects: true
    }).catch(() => null);
    if (domSnapshot) await writeJson(path.join(outputDir, 'raw', 'dom-snapshot.json'), domSnapshot);

    const performance = await cdp.send('Performance.getMetrics').catch(() => null);
    if (performance) await writeJson(path.join(outputDir, 'safe', 'performance-metrics.json'), performance);
  }

  const recorder = {
    async checkpoint(label, selector = targetSelector) {
      const probe = await actionabilityProbe(page, selector);
      const entry = { label, ...probe };
      actionability.push(entry);
      await writeJson(path.join(outputDir, 'safe', 'actionability.json'), actionability);
      return entry;
    },
    async stop(result = {}) {
      await recorder.checkpoint('FINAL', targetSelector).catch(() => {});
      if (enableTrace) {
        try {
          await context.tracing.stop({ path: path.join(outputDir, 'raw', 'trace.zip') });
          await record('trace_stop', { status: 'SAVED' });
        } catch (error) {
          await record('trace_stop', { status: 'NOT_SAVED', error_sha256: sha256(String(error)) });
        }
      }
      if (cdp) await cdp.detach().catch(() => {});

      const artifacts = {};
      for (const rel of [
        'raw/trace.zip','raw/cdp.jsonl','raw/storage-state.json','raw/dom-snapshot.json',
        'safe/events.jsonl','safe/cdp.jsonl','safe/environment.json','safe/actionability.json'
      ]) {
        const abs = path.join(outputDir, rel);
        try {
          const data = await fs.readFile(abs);
          artifacts[rel] = { bytes: data.length, sha256: sha256(data) };
        } catch {}
      }

      const finalResult = {
        task_id: taskId,
        stopped_at: now(),
        target_selector: targetSelector,
        result,
        artifacts
      };
      await writeJson(path.join(outputDir, 'safe', 'golden-task-result.json'), finalResult);
      return finalResult;
    }
  };

  await recorder.checkpoint('START', targetSelector).catch(() => {});
  return recorder;
}
