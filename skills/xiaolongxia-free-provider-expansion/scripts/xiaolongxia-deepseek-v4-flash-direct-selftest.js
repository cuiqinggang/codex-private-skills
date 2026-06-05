const fs = require("fs");
const path = require("path");

const projectRoot = process.env.XIAOLONGXIA_PROJECT_ROOT || "C:\\Users\\A\\xiaolongxia-free-api-local";
const secretFile = process.env.XIAOLONGXIA_DEEPSEEK_SECRET_FILE || path.join(projectRoot, "secrets", "deepseek_api_key.txt");
const outputRoot = process.env.XIAOLONGXIA_DEEPSEEK_OUTPUT_ROOT || "C:\\Users\\A\\Desktop\\1\\output\\XIAOLONGXIA-DEEPSEEK-DIRECT-WIRE-IN-20260524";
const mode = process.env.XIAOLONGXIA_DEEPSEEK_SELFTEST_MODE || "full";

const endpoint = "https://api.deepseek.com/chat/completions";
const model = "deepseek-v4-flash";
const providerId = "deepseek-official-direct";
const marker = "XIAOLONGXIA_DEEPSEEK_DIRECT_OK";

function nowIso() {
  return new Date().toISOString();
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function writeJson(file, data) {
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function writeText(file, text) {
  fs.writeFileSync(file, text, "utf8");
}

function readSecret() {
  const value = fs.readFileSync(secretFile, "utf8").trim();
  if (!value) {
    throw new Error("DeepSeek secret file is empty");
  }
  return value;
}

function redactError(text) {
  if (!text) return "";
  return String(text)
    .replace(/sk-[A-Za-z0-9_-]{8,}/g, "sk-REDACTED")
    .replace(/Bearer\s+[A-Za-z0-9._-]+/gi, "Bearer REDACTED");
}

function hasChinese(text) {
  return /[\u4e00-\u9fff]/.test(text || "");
}

function hasLeak(text) {
  const lower = String(text || "").toLowerCase();
  return [
    "deepseek",
    "api",
    "provider",
    "模型",
    "接口",
    "密钥",
    "token",
    "openai",
    "chatgpt",
    "nvidia",
    "llama",
  ].some((term) => lower.includes(term.toLowerCase()));
}

function hasFalsePromise(text) {
  return /一定(提高|提升|变好|见效)|保证|包过|百分百|100%|肯定提分/.test(text || "");
}

function hasUnconfirmedChannelClaim(text) {
  return /app下载|下载APP|微信(入口|联系|添加)|官网|网址|网站|续费|价格|收费标准|小钱|先尝后买|试用一阵子|24小时|第一周免费|永久免费/.test(text || "");
}

function evaluate(text, options = {}) {
  const answer = String(text || "").trim();
  const compactLen = answer.replace(/\s/g, "").length;
  const markerOk = options.marker ? answer.includes(options.marker) : true;
  if (options.marker) {
    return {
      marker_ok: markerOk,
      chinese_ok: true,
      short_ok: compactLen > 0 && compactLen <= (options.maxChars || 180),
      no_model_api_provider_leak: true,
      no_false_promise: true,
      no_unconfirmed_channel_claim: true,
      suitable_for_xiaolongxia: markerOk,
      score_1_to_5: markerOk ? 5 : 1,
    };
  }
  const chineseOk = options.expectChinese === false ? true : hasChinese(answer);
  const shortOk = compactLen > 0 && compactLen <= (options.maxChars || 180);
  const noLeak = !hasLeak(answer);
  const noFalsePromise = !hasFalsePromise(answer);
  const noUnconfirmedClaim = !hasUnconfirmedChannelClaim(answer);
  const ok = markerOk && chineseOk && shortOk && noLeak && noFalsePromise && noUnconfirmedClaim;
  return {
    marker_ok: markerOk,
    chinese_ok: chineseOk,
    short_ok: shortOk,
    no_model_api_provider_leak: noLeak,
    no_false_promise: noFalsePromise,
    no_unconfirmed_channel_claim: noUnconfirmedClaim,
    suitable_for_xiaolongxia: ok,
    score_1_to_5: ok ? 5 : (chineseOk && noLeak && noFalsePromise ? 4 : 2),
  };
}

async function callDeepSeek(apiKey, testCase) {
  const system = [
    "你是小龙虾的本地回复草稿生成模块。",
    "只生成本地测试草稿，不发送任何真实消息。",
    "中文、简短、温和、像真人在家长群里说话。",
    "不要怼人，不要阴阳怪气，不要说想得美、别瞎传这类刺耳表达。",
    "不要提模型、API、provider、OpenAI、ChatGPT、DeepSeek、NVIDIA、密钥、接口。",
    "不要承诺成绩一定提升，不要编造APP、网站、微信入口、价格、续费。",
    "遇到费用、是否免费、怎么体验这类未确认信息，只能说以实际安排为准，不要编造免费试用周期或收费说法。",
    "如果是 marker 测试，只返回指定 marker，不要添加任何其他文字。",
  ].join("\n");

  const body = {
    model,
    messages: [
      { role: "system", content: system },
      { role: "user", content: testCase.prompt },
    ],
    temperature: testCase.temperature ?? 0.2,
    max_tokens: testCase.max_tokens ?? 320,
    stream: false,
    thinking: { type: "disabled" },
  };

  const started = Date.now();
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json; charset=utf-8",
      },
      body: JSON.stringify(body),
    });
    const raw = await response.text();
    let json = null;
    try {
      json = JSON.parse(raw);
    } catch {
      // Keep raw preview below.
    }
    const content = json?.choices?.[0]?.message?.content || "";
    const returnedModel = json?.model || null;
    const finishReason = json?.choices?.[0]?.finish_reason || null;
    const evaluation = evaluate(content, {
      marker: testCase.marker,
      expectChinese: testCase.expectChinese,
      maxChars: testCase.maxChars,
    });
    return {
      id: testCase.id,
      category: testCase.category,
      prompt: testCase.prompt,
      provider_id: providerId,
      endpoint_base: "https://api.deepseek.com",
      requested_model: model,
      returned_model: returnedModel,
      http_status: response.status,
      latency_ms: Date.now() - started,
      success: response.ok && evaluation.suitable_for_xiaolongxia,
      response_contains_marker: testCase.marker ? content.includes(testCase.marker) : null,
      draft_reply: content,
      finish_reason: finishReason,
      evaluation,
      error_summary: response.ok ? "" : redactError(raw).slice(0, 500),
      sent_to_real_group: false,
      key_printed: false,
    };
  } catch (err) {
    return {
      id: testCase.id,
      category: testCase.category,
      prompt: testCase.prompt,
      provider_id: providerId,
      endpoint_base: "https://api.deepseek.com",
      requested_model: model,
      returned_model: null,
      http_status: null,
      latency_ms: Date.now() - started,
      success: false,
      response_contains_marker: testCase.marker ? false : null,
      draft_reply: "",
      finish_reason: null,
      evaluation: evaluate("", { marker: testCase.marker, expectChinese: testCase.expectChinese }),
      error_summary: redactError(err && err.message ? err.message : String(err)).slice(0, 500),
      sent_to_real_group: false,
      key_printed: false,
    };
  }
}

function buildCases() {
  const cases = [
    {
      id: "DS-MARKER-001",
      category: "marker",
      marker,
      expectChinese: false,
      maxChars: 80,
      temperature: 0,
      max_tokens: 120,
      prompt: `请只回复：${marker}`,
    },
    {
      id: "DS-STYLE-001",
      category: "xiaolongxia_style",
      prompt: "你这个 AI 辅导孩子学习是免费的吗？请用小龙虾风格回答，80字以内。",
    },
    {
      id: "DS-STYLE-002",
      category: "xiaolongxia_style",
      prompt: "孩子作文不会写，有什么办法？请用家长群里能直接看的口吻回答，100字以内。",
    },
    {
      id: "DS-STYLE-003",
      category: "xiaolongxia_style",
      prompt: "数学应用题不会做，AI 能怎么帮？不要直接承诺提分，100字以内。",
    },
    {
      id: "DS-STYLE-004",
      category: "xiaolongxia_style",
      prompt: "我不会用电脑，怎么先体验？不要编造app下载、网站、微信入口，100字以内。",
    },
    {
      id: "DS-STYLE-005",
      category: "xiaolongxia_style",
      prompt: "孩子会不会依赖 AI？请给家长一个稳妥回答，100字以内。",
    },
  ];
  return mode === "quick" ? cases.slice(0, 2) : cases;
}

function buildMarkdown(doc) {
  const lines = [
    "# Xiaolongxia DeepSeek V4 Flash Direct Selftest",
    "",
    `- Generated: ${doc.generated_at}`,
    `- Provider: \`${doc.provider_id}\``,
    `- Endpoint base: \`${doc.endpoint_base}\``,
    `- Model: \`${doc.model}\``,
    `- Mode: \`${doc.mode}\``,
    `- Direct path: Xiaolongxia internal LLM wrapper -> DeepSeek official API`,
    `- 3011/New API used: ${doc.newapi_3011_used}`,
    `- OpenRouter used: ${doc.openrouter_used}`,
    `- OpenClaw 18789 /v1 proxy used: ${doc.openclaw_18789_proxy_used}`,
    `- Real sends: ${doc.real_send_count}`,
    `- Key printed: ${doc.key_printed}`,
    `- Overall success: ${doc.success}`,
    "",
    "## Summary",
    "",
    `- Total tests: ${doc.summary.total}`,
    `- Passed: ${doc.summary.passed}`,
    `- Failed: ${doc.summary.failed}`,
    `- Average latency ms: ${doc.summary.average_latency_ms}`,
    "",
    "## Results",
    "",
    "| ID | HTTP | Success | Latency ms | Score | Preview |",
    "| --- | ---: | --- | ---: | ---: | --- |",
  ];
  for (const r of doc.results) {
    const preview = String(r.draft_reply || r.error_summary || "")
      .replace(/\s+/g, " ")
      .replace(/\|/g, "/")
      .slice(0, 120);
    lines.push(`| ${r.id} | ${r.http_status ?? ""} | ${r.success} | ${r.latency_ms} | ${r.evaluation.score_1_to_5} | ${preview} |`);
  }
  return `${lines.join("\n")}\n`;
}

async function main() {
  ensureDir(outputRoot);
  const apiKey = readSecret();
  const results = [];
  for (const testCase of buildCases()) {
    results.push(await callDeepSeek(apiKey, testCase));
    await new Promise((resolve) => setTimeout(resolve, 500));
  }

  const passed = results.filter((r) => r.success).length;
  const latencies = results.filter((r) => Number.isFinite(r.latency_ms)).map((r) => r.latency_ms);
  const avg = latencies.length ? Math.round(latencies.reduce((a, b) => a + b, 0) / latencies.length) : null;
  const doc = {
    generated_at: nowIso(),
    task_id: "XIAOLONGXIA-DEEPSEEK-DIRECT-WIRE-IN-20260524",
    provider_id: providerId,
    endpoint_base: "https://api.deepseek.com",
    endpoint,
    model,
    mode,
    secret_file: secretFile,
    key_printed: false,
    newapi_3011_used: false,
    openrouter_used: false,
    openclaw_18789_proxy_used: false,
    real_send_count: 0,
    success: passed === results.length,
    summary: {
      total: results.length,
      passed,
      failed: results.length - passed,
      average_latency_ms: avg,
    },
    results,
  };

  writeJson(path.join(outputRoot, "G01-deepseek-direct-selftest.json"), doc);
  writeText(path.join(outputRoot, "G01-deepseek-direct-selftest.md"), buildMarkdown(doc));
  console.log(JSON.stringify({
    success: doc.success,
    total: doc.summary.total,
    passed: doc.summary.passed,
    failed: doc.summary.failed,
    average_latency_ms: doc.summary.average_latency_ms,
    key_printed: false,
  }, null, 2));
  process.exit(doc.success ? 0 : 2);
}

main().catch((err) => {
  ensureDir(outputRoot);
  const failure = {
    generated_at: nowIso(),
    task_id: "XIAOLONGXIA-DEEPSEEK-DIRECT-WIRE-IN-20260524",
    success: false,
    error_summary: redactError(err && err.message ? err.message : String(err)),
    key_printed: false,
  };
  writeJson(path.join(outputRoot, "G01-deepseek-direct-selftest.json"), failure);
  console.error(JSON.stringify(failure, null, 2));
  process.exit(1);
});
