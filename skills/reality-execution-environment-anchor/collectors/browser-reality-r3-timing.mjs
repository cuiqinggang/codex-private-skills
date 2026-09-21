import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';

const now = () => new Date().toISOString();
const sha256 = data => crypto.createHash('sha256').update(data).digest('hex');
const canonicalJson = value => {
  if (Array.isArray(value)) return '[' + value.map(canonicalJson).join(',') + ']';
  if (value && typeof value === 'object') {
    return '{' + Object.keys(value).sort().map(k => JSON.stringify(k) + ':' + canonicalJson(value[k])).join(',') + '}';
  }
  return JSON.stringify(value);
};

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

async function writeJson(file, value) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, JSON.stringify(value, null, 2) + '\n', 'utf8');
}

/**
 * 极轻量 Golden Timing recorder.
 * 不挂 request/response listener，不启 Trace，不启 CDP，不做 DOMSnapshot。
 * 只冻结任务身份、最小浏览器身份摘要和 monotonic wall-clock duration。
 */
export async function startBrowserRealityTiming({
  context,
  page,
  outputDir,
  taskId,
  targetSelector = '#dialog',
  runId
}) {
  if (!context || !page || !outputDir || !taskId || !runId) {
    throw new Error('context, page, outputDir, taskId, runId are required');
  }

  const startNs = process.hrtime.bigint();
  const startedAt = now();

  // 仅一次轻量读取，用于证明三次运行仍是同一真实页面/Context 家族。
  const identity = await page.evaluate(() => ({
    href: location.href,
    userAgent: navigator.userAgent,
    platform: navigator.platform,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    dpr: devicePixelRatio
  }));

  const contextPageCount = context.pages().length;
  const identitySafe = {
    url: safeUrl(identity.href),
    user_agent_sha256: sha256(identity.userAgent),
    platform: identity.platform,
    timezone: identity.timezone,
    dpr: identity.dpr,
    context_page_count: contextPageCount
  };
  const identityFingerprint = sha256(canonicalJson(identitySafe));

  return {
    async stop(result = {}) {
      const endNs = process.hrtime.bigint();
      const stoppedAt = now();
      const durationMs = Number(endNs - startNs) / 1_000_000;
      const outcome = result.outcome ?? result.status ?? result.result ?? 'UNKNOWN';

      const payload = {
        schema_version: '1.0',
        mode: 'GOLDEN_TIMING_RUN',
        task_id: taskId,
        run_id: runId,
        target_selector: targetSelector,
        started_at: startedAt,
        stopped_at: stoppedAt,
        duration_ms: durationMs,
        outcome: String(outcome),
        identity_safe: identitySafe,
        identity_fingerprint: identityFingerprint,
        heavy_observability: false,
        trace: false,
        cdp: false,
        dom_snapshot: false,
        network_listeners_added: false,
        result_safe: {
          outcome: String(outcome),
          error_code: result.error_code ?? null,
          error_class: result.error_class ?? null
        }
      };

      await writeJson(path.join(outputDir, 'safe', 'timing-run.json'), payload);
      return payload;
    }
  };
}
