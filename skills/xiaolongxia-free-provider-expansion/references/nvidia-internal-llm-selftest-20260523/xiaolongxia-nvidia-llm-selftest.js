const fs = require('fs');
const path = require('path');

const projectRoot = process.env.PROJECT_ROOT || path.resolve(__dirname, '..');
const outputRoot = process.env.OUTPUT_ROOT || 'C:\\Users\\A\\Desktop\\1\\output\\XIAOLONGXIA-NVIDIA-INTERNAL-LLM-SELFTEST-20260523';
const secretFile = process.env.NVIDIA_SECRET_FILE || path.join(projectRoot, 'secrets', 'nvidia_api_key.txt');
const modelMode = process.env.MODEL_MODE || 'auto';
const simulatePrimaryFailure = process.env.SIMULATE_PRIMARY_FAILURE === 'true';
const primaryModel = process.env.PRIMARY_MODEL || 'meta/llama-3.1-8b-instruct';
const fallbackModel = process.env.FALLBACK_MODEL || 'meta/llama-3.1-70b-instruct';
const timeoutSec = Number(process.env.TIMEOUT_SEC || '60');

const endpoint = 'https://integrate.api.nvidia.com/v1/chat/completions';
const routeName = 'xiaolongxia-nvidia-nim-dryrun';
const providerId = 'nvidia-nim-dryrun';

function ensureDir(p) { fs.mkdirSync(p, { recursive: true }); }
function nowIso() { return new Date().toISOString(); }
function readText(p) { return fs.readFileSync(p, 'utf8'); }
function writeText(p, s) { fs.writeFileSync(p, s, 'utf8'); }
function writeJson(p, obj) { writeText(p, JSON.stringify(obj, null, 2)); }
function mdEscape(text) { return String(text || '').replace(/\|/g, '\\|').replace(/\r?\n/g, '<br>'); }
function short(text, n = 110) {
  const s = String(text || '').replace(/\s+/g, ' ').trim();
  return s.length > n ? s.slice(0, n) + '...' : s;
}
function hasChinese(text) { return /[\u4e00-\u9fff]/.test(String(text || '')); }
function containsAny(text, words) {
  const s = String(text || '').toLowerCase();
  return words.some(w => s.includes(String(w).toLowerCase()));
}
function looksLikeSecret(text) {
  return /(sk-or-v1-[A-Za-z0-9_-]{20,}|nvapi-[A-Za-z0-9_-]{20,})/.test(String(text || ''));
}

const primaryTasks = [
  '孩子四年级作文不会写，家长应该怎么辅导？',
  '数学应用题孩子总看不懂题目，怎么办？',
  'AI 辅导和普通补课有什么区别？',
  '孩子做作业拖拉，家长怎么引导？',
  '请用小龙虾风格回答：AI 辅导到底有什么用？'
];

const fallbackTasks = [
  '请给一个小学三年级数学应用题讲解思路，不要直接只给答案。',
  '家长没有时间辅导孩子，AI 可以怎么帮忙？请简短回答。',
  '孩子会不会依赖 AI？请给家长一个稳妥回答。'
];

const autoTasks = [
  '请用 80 字以内解释：孩子写作文为什么需要先搭框架？'
];

const bannedLeakWords = [
  'nvidia', 'provider', 'openai', 'chatgpt', 'llama', 'meta/llama',
  '接口', '密钥', 'token', 'key', '大模型名称'
];
const bannedUnconfirmed = [
  'app下载', '下载app', '官网', '网站', '微信', '小程序', '公众号',
  '价格', '续费', '会员', '月费', '年费', '收费标准', '永久免费',
  '24小时', '随时在线', '保证', '一定提高', '包提高', '承诺'
];

function getTasks() {
  if (modelMode === 'primary') return primaryTasks;
  if (modelMode === 'fallback') return fallbackTasks;
  return autoTasks;
}

function outputNames() {
  if (modelMode === 'primary') return {
    json: 'G03-primary-8b-internal-selftest.json',
    md: 'G03-primary-8b-internal-selftest.md',
    statusPass: 'G03_PASS_PRIMARY_8B_INTERNAL_SELFTEST'
  };
  if (modelMode === 'fallback') return {
    json: 'G04-fallback-70b-internal-selftest.json',
    md: 'G04-fallback-70b-internal-selftest.md',
    statusPass: 'G04_PASS_FALLBACK_70B_INTERNAL_SELFTEST'
  };
  return {
    json: simulatePrimaryFailure ? 'G05-auto-switch-forced-failure-internal-selftest.json' : 'G05-auto-switch-normal-internal-selftest.json',
    md: simulatePrimaryFailure ? 'G05-auto-switch-forced-failure-internal-selftest.md' : 'G05-auto-switch-normal-internal-selftest.md',
    statusPass: simulatePrimaryFailure ? 'G05_PASS_AUTO_FORCED_FALLBACK_INTERNAL_SELFTEST' : 'G05_PASS_AUTO_NORMAL_INTERNAL_SELFTEST'
  };
}

function buildPrompt(input) {
  return [
    '你是小龙虾内部 LLM/provider 层的自测响应器，只返回给本地测试脚本，不发送消息。',
    '请只输出一段中文，不要标题、不要编号、不要列表。',
    '尽量控制在 80 到 120 个汉字；如果问题复杂，也不要超过 180 个汉字。',
    '像给家长解释，不要官方套话，不要夸大。',
    '不要提 NVIDIA、模型、provider、OpenAI、ChatGPT、API、接口、密钥、token。',
    '不要编造 App、网站、微信入口、价格、续费、24 小时在线、永久免费等未确认信息。',
    '不要承诺成绩一定提升。学习问题要强调讲思路、改作文、陪练、启发孩子自己想。',
    '问题：' + input
  ].join('\n');
}

async function requestJson(url, options, timeoutMs) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(new Error('timeout')), timeoutMs);
  const started = Date.now();
  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    const text = await res.text();
    let json = null;
    try { json = text ? JSON.parse(text) : null; } catch {}
    return { ok: res.ok, status: res.status, text, json, latency_ms: Date.now() - started, error_summary: '' };
  } catch (err) {
    return { ok: false, status: null, text: '', json: null, latency_ms: Date.now() - started, error_summary: err.message || String(err) };
  } finally {
    clearTimeout(timer);
  }
}

async function callModel(model, prompt, apiKey) {
  const body = {
    model,
    messages: [
      { role: 'system', content: '只做小龙虾内部 LLM 自测，不发送消息。' },
      { role: 'user', content: buildPrompt(prompt) }
    ],
    temperature: 0.2,
    max_tokens: 120,
    stream: false
  };

  const res = await requestJson(endpoint, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
      'Content-Type': 'application/json; charset=utf-8'
    },
    body: JSON.stringify(body)
  }, timeoutSec * 1000);

  let text = '';
  let returnedModel = '';
  let errorSummary = res.error_summary;
  if (res.json) {
    returnedModel = res.json.model || '';
    if (Array.isArray(res.json.choices) && res.json.choices[0] && res.json.choices[0].message) {
      text = String(res.json.choices[0].message.content || '').trim();
    }
    if (res.json.error) errorSummary = String(res.json.error.message || JSON.stringify(res.json.error));
  }
  if (!text && !errorSummary && !res.ok) errorSummary = short(res.text, 240);
  if (!text && res.ok) errorSummary = 'empty reply';

  return {
    requested_model: model,
    returned_model: returnedModel,
    http_status: res.status,
    latency_ms: res.latency_ms,
    text,
    success: Boolean(res.ok && text),
    error_summary: short(errorSummary, 240)
  };
}

function simulatedFailure(prompt) {
  return {
    requested_model: primaryModel,
    returned_model: '',
    http_status: 503,
    latency_ms: 0,
    text: '',
    success: false,
    error_summary: 'simulated primary model failure for auto fallback selftest',
    simulated_failure: true,
    prompt
  };
}

function evaluate(text) {
  const s = String(text || '').trim();
  const chineseOk = hasChinese(s);
  const noLeak = !containsAny(s, bannedLeakWords) && !looksLikeSecret(s);
  const noFalsePromise = !containsAny(s, bannedUnconfirmed);
  const noEnglishTrace = !/(thinking|reasoning|system prompt|as an ai|assistant)/i.test(s);
  const noSend = !containsAny(s, ['已发送', '我已经发', '发到群里', '我会联系']);
  const concise = s.length >= 20 && s.length <= 320;
  return {
    chinese_ok: chineseOk,
    concise_ok: concise,
    no_model_api_provider_leak: noLeak,
    no_false_promise_or_unconfirmed_claim: noFalsePromise,
    no_english_reasoning_trace: noEnglishTrace,
    sent_to_real_group: false,
    no_send_implication: noSend,
    pass: chineseOk && concise && noLeak && noFalsePromise && noEnglishTrace && noSend
  };
}

async function runOne(prompt, apiKey) {
  const attempts = [];
  let selected;
  let usedFallback = false;

  if (modelMode === 'primary') {
    selected = await callModel(primaryModel, prompt, apiKey);
    attempts.push(selected);
  } else if (modelMode === 'fallback') {
    selected = await callModel(fallbackModel, prompt, apiKey);
    attempts.push(selected);
  } else {
    const first = simulatePrimaryFailure ? simulatedFailure(prompt) : await callModel(primaryModel, prompt, apiKey);
    attempts.push(first);
    selected = first;
    if (!first.success) {
      const second = await callModel(fallbackModel, prompt, apiKey);
      attempts.push(second);
      selected = second;
      usedFallback = true;
    }
  }

  const evaluation = evaluate(selected.text);
  return {
    prompt,
    model_mode: modelMode,
    route_name: routeName,
    provider_id: providerId,
    selected_model: selected.requested_model,
    returned_model: selected.returned_model,
    used_fallback: usedFallback,
    http_status: selected.http_status,
    latency_ms: selected.latency_ms,
    text: selected.text,
    success: Boolean(selected.success && evaluation.pass),
    error_summary: selected.error_summary,
    evaluation,
    sent: false,
    sent_to_real_group: false,
    real_message_id: null,
    real_group_id: null,
    attempts
  };
}

async function main() {
  ensureDir(outputRoot);
  const names = outputNames();
  const secretExists = fs.existsSync(secretFile);
  const apiKey = secretExists ? readText(secretFile).trim() : '';
  if (!apiKey) {
    const doc = {
      generated_at: nowIso(),
      status: 'STOP_KEY_REQUIRED',
      key_source: secretFile,
      key_printed: false
    };
    writeJson(path.join(outputRoot, names.json), doc);
    writeText(path.join(outputRoot, names.md), `# Internal LLM Selftest\n\nStatus: \`STOP_KEY_REQUIRED\`\n`);
    process.exitCode = 2;
    return;
  }

  const tasks = getTasks();
  const results = [];
  for (const task of tasks) {
    results.push(await runOne(task, apiKey));
  }

  const successCount = results.filter(r => r.success).length;
  const realSendCount = results.filter(r => r.sent || r.sent_to_real_group || r.real_message_id || r.real_group_id).length;
  const leakCount = results.filter(r => !r.evaluation.no_model_api_provider_leak).length;
  const falseClaimCount = results.filter(r => !r.evaluation.no_false_promise_or_unconfirmed_claim).length;
  const expectedModel = modelMode === 'fallback' ? fallbackModel : primaryModel;
  const selectedModelOk = modelMode === 'auto'
    ? (simulatePrimaryFailure ? results.every(r => r.selected_model === fallbackModel && r.used_fallback) : results.every(r => r.selected_model === primaryModel && !r.used_fallback))
    : results.every(r => r.selected_model === expectedModel);
  const pass = successCount === tasks.length && selectedModelOk && realSendCount === 0 && leakCount === 0 && falseClaimCount === 0 && !looksLikeSecret(JSON.stringify(results));
  const status = pass ? names.statusPass : `${names.statusPass.replace('_PASS_', '_PARTIAL_')}`;

  const doc = {
    generated_at: nowIso(),
    task_id: 'XIAOLONGXIA-NVIDIA-INTERNAL-LLM-SELFTEST-20260523',
    model_mode: modelMode,
    simulate_primary_failure: simulatePrimaryFailure,
    route_name: routeName,
    provider_id: providerId,
    endpoint_base: 'https://integrate.api.nvidia.com/v1',
    primary_model: primaryModel,
    fallback_model: fallbackModel,
    key_source: secretFile,
    key_printed: false,
    production_config_modified: false,
    real_group_connected: false,
    real_send_count: realSendCount,
    total: tasks.length,
    success_count: successCount,
    selected_model_ok: selectedModelOk,
    leak_count: leakCount,
    false_promise_or_unconfirmed_claim_count: falseClaimCount,
    status,
    results
  };
  writeJson(path.join(outputRoot, names.json), doc);

  const md = [
    `# ${modelMode.toUpperCase()} Internal LLM Selftest`,
    '',
    `Generated: ${doc.generated_at}`,
    '',
    `Status: \`${status}\``,
    '',
    `- Model mode: \`${modelMode}\``,
    `- Simulate primary failure: ${simulatePrimaryFailure}`,
    `- Route: \`${routeName}\``,
    `- Provider: \`${providerId}\``,
    `- Primary: \`${primaryModel}\``,
    `- Fallback: \`${fallbackModel}\``,
    '- UI required: false',
    '- Real send: false',
    '- Key printed: false',
    '',
    '| # | HTTP | Selected model | Fallback | Pass | Latency ms | Response |',
    '|---:|---:|---|---|---|---:|---|',
    ...results.map((r, i) => `| ${i + 1} | ${r.http_status ?? ''} | \`${r.selected_model}\` | ${r.used_fallback} | ${r.success} | ${r.latency_ms ?? ''} | ${mdEscape(short(r.text, 90))} |`),
    '',
    '## Summary',
    '',
    `- Success: ${successCount}/${tasks.length}`,
    `- Selected model OK: ${selectedModelOk}`,
    `- Real sends: ${realSendCount}`,
    `- Model/API/provider leaks: ${leakCount}`,
    `- False promises or unconfirmed claims: ${falseClaimCount}`,
    ''
  ].join('\n');
  writeText(path.join(outputRoot, names.md), md);

  console.log(`status=${status}`);
  console.log(`mode=${modelMode}`);
  console.log(`simulate_primary_failure=${simulatePrimaryFailure}`);
  console.log(`success=${successCount}/${tasks.length}`);
  console.log(`selected_model_ok=${selectedModelOk}`);
  console.log(`real_send_count=${realSendCount}`);
  console.log(`leak_count=${leakCount}`);
  console.log(`false_claim_count=${falseClaimCount}`);
  console.log(`json=${path.join(outputRoot, names.json)}`);
  console.log(`md=${path.join(outputRoot, names.md)}`);
}

main().catch(err => {
  console.error(err.stack || err.message || String(err));
  process.exit(1);
});
