const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execSync } = require("child_process");

const OUT = "C:/Users/A/Desktop/1/output/XIAOLONGXIA-NVIDIA-SHADOW-TEST-LOCAL-DRAFT-20260523";
const INPUT_DIR = path.join(OUT, "shadow-input");
const CANDIDATE_DIR = path.join(OUT, "candidate-config");
const LOCAL_SKILL = "C:/Users/A/.codex/skills/xiaolongxia-free-provider-expansion";
const H_SKILL = "H:/CodexSkills/xiaolongxia-free-provider-expansion";
const PREV_ROUTE_REPORT = "C:/Users/A/Desktop/1/output/XIAOLONGXIA-OPENCLAW-NVIDIA-ROUTE-DRYRUN-20260523/final-report.md";
const PREV_ROUTE_CONFIG = "C:/Users/A/Desktop/1/output/XIAOLONGXIA-OPENCLAW-NVIDIA-ROUTE-DRYRUN-20260523/candidate-config/openclaw-nvidia-nim-dryrun.json";
const NVIDIA_KEY_FILE = "C:/Users/A/xiaolongxia-free-api-local/secrets/nvidia_api_key.txt";
const XLLX_TOKEN_FILE = "C:/Users/A/xiaolongxia-free-api-local/secrets/xiaolongxia_newapi_token.txt";
const OPENCLAW_CONFIG = "C:/Users/A/.openclaw/openclaw.json";
const XLLX_COMPOSE = "C:/Users/A/xiaolongxia-free-api-local/docker-compose.yml";
const XLLX_ENV = "C:/Users/A/xiaolongxia-free-api-local/.env";

const ROUTE_NAME = "xiaolongxia-nvidia-nim-dryrun";
const PROVIDER_ID = "nvidia-nim-dryrun";
const BASE_URL = "https://integrate.api.nvidia.com/v1";
const PRIMARY = "meta/llama-3.1-8b-instruct";
const FALLBACK = "meta/llama-3.1-70b-instruct";
const EXCLUDED = "nvidia/nemotron-3-super-120b-a12b";

fs.mkdirSync(OUT, { recursive: true });
fs.mkdirSync(INPUT_DIR, { recursive: true });
fs.mkdirSync(CANDIDATE_DIR, { recursive: true });

function redact(s) {
  return String(s || "")
    .replace(/nvapi-[A-Za-z0-9_-]{20,}/g, "[REDACTED_NVIDIA_KEY]")
    .replace(/sk-or-v1-[A-Za-z0-9_-]{20,}/g, "[REDACTED_OPENROUTER_KEY]")
    .replace(/sk-[A-Za-z0-9_-]{20,}/g, "[REDACTED_KEY]");
}

function writeText(rel, text) {
  fs.writeFileSync(path.join(OUT, rel), text, "utf8");
}

function writeJson(rel, value) {
  fs.writeFileSync(path.join(OUT, rel), JSON.stringify(value, null, 2) + "\n", "utf8");
}

function exists(p) {
  return fs.existsSync(p);
}

function sha256File(p) {
  if (!fs.existsSync(p) || !fs.statSync(p).isFile()) return null;
  return crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex").toUpperCase();
}

function sha256String(s) {
  return crypto.createHash("sha256").update(String(s)).digest("hex").toUpperCase();
}

function run(command) {
  try {
    return { ok: true, output: redact(execSync(command, { encoding: "utf8", stdio: ["ignore", "pipe", "pipe"], timeout: 30000 })) };
  } catch (e) {
    return { ok: false, output: redact((e.stdout || "") + (e.stderr || "") + e.message) };
  }
}

function walk(root, acc = []) {
  if (!fs.existsSync(root)) return acc;
  for (const ent of fs.readdirSync(root, { withFileTypes: true })) {
    const p = path.join(root, ent.name);
    if (ent.isDirectory()) walk(p, acc);
    else if (ent.isFile()) acc.push(p);
  }
  return acc;
}

function scanKeyPatterns(roots) {
  const pattern = /(nvapi-[A-Za-z0-9_-]{20,}|sk-or-v1-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9_-]{20,})/;
  const hits = [];
  for (const root of roots) {
    for (const file of walk(root)) {
      if (file.replaceAll("\\", "/").endsWith("/nvidia_api_key.txt")) continue;
      let text = "";
      try { text = fs.readFileSync(file, "utf8"); } catch { continue; }
      if (pattern.test(text)) hits.push(file);
    }
  }
  return hits;
}

async function fetchJson(url, options = {}, timeoutMs = 60000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    const text = await res.text();
    let json = null;
    try { json = JSON.parse(text); } catch {}
    return { status: res.status, ok: res.ok, text, json };
  } finally {
    clearTimeout(timer);
  }
}

async function getProductionModels() {
  if (!fs.existsSync(XLLX_TOKEN_FILE)) return { ok: false, status: 0, modelIds: [], error: "xiaolongxia token file missing" };
  const token = fs.readFileSync(XLLX_TOKEN_FILE, "utf8").trim();
  try {
    const res = await fetchJson("http://localhost:3011/v1/models", {
      headers: { Authorization: `Bearer ${token}` }
    }, 20000);
    const modelIds = Array.isArray(res.json?.data) ? res.json.data.map(x => x.id).filter(Boolean).sort() : [];
    return { ok: res.ok, status: res.status, modelIds, error: res.ok ? "" : redact(res.text).slice(0, 300) };
  } catch (e) {
    return { ok: false, status: 0, modelIds: [], error: redact(e.message) };
  }
}

function checkRealSendRisk() {
  const ps = run("powershell -NoProfile -Command \"Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'xiaolongxia|openclaw|feishu|wechat|telegram|send|bot' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Depth 4\"");
  let rows = [];
  try {
    rows = ps.output.trim() ? JSON.parse(ps.output) : [];
    if (!Array.isArray(rows)) rows = [rows];
  } catch {
    rows = [];
  }
  const risky = rows.filter(r => {
    const c = String(r.CommandLine || "");
    const name = String(r.Name || "");
    if (!c) return false;
    if (/WeChatAppEx\.exe|WeChat\.exe|WXWork\.exe|Feishu\.exe|Lark\.exe|Telegram\.exe/i.test(name)) return false;
    if (/run-xiaolongxia-nvidia-shadow-test\.js/i.test(c)) return false;
    if (/Get-CimInstance|Win32_Process|ConvertTo-Json|run-xiaolongxia-nvidia-shadow-test\.js/i.test(c)) return false;
    if (!/(node|python|powershell|pwsh|cmd|\.ps1|\.js|\.py)/i.test(name + " " + c)) return false;
    return /(feishu|wechat|telegram|飞书|微信).*(send|bot|bridge|group|群|message)|send[_-]?message|send_group|group_send/i.test(c);
  });
  return { raw_count: rows.length, risky_count: risky.length, risky: risky.map(r => ({ ProcessId: r.ProcessId, Name: r.Name, CommandLine: redact(r.CommandLine).slice(0, 500) })) };
}

const messages = [
  {
    message_id: "SIM-001",
    simulated_sender: "家长A",
    input_text: "你这个 AI 辅导孩子学习是免费的吗？我想先了解一下。",
    category: "免费体验问题",
    expected_reply_style: "说明可以先体验，别承诺具体收费政策。",
    should_reply: true,
    risk_note: "不要编造第一周免费、价格、续费。"
  },
  {
    message_id: "SIM-002",
    simulated_sender: "家长B",
    input_text: "孩子作文一直不会写，半天憋不出几句话，你这个有什么用？",
    category: "孩子作文不会写",
    expected_reply_style: "强调找思路、列提纲、改表达。",
    should_reply: true,
    risk_note: "不要承诺作文成绩一定提升。"
  },
  {
    message_id: "SIM-003",
    simulated_sender: "家长C",
    input_text: "数学应用题不会做，AI 是直接给答案吗？",
    category: "数学题不会做",
    expected_reply_style: "强调分步骤引导和理解题意。",
    should_reply: true,
    risk_note: "不要鼓励直接抄答案。"
  },
  {
    message_id: "SIM-004",
    simulated_sender: "家长D",
    input_text: "我不太会操作电脑，这个用起来会不会很复杂？",
    category: "家长不会操作电脑",
    expected_reply_style: "降低门槛，说明后续可做成简单入口。",
    should_reply: true,
    risk_note: "不要编造 APP、网站、微信入口已经上线。"
  },
  {
    message_id: "SIM-005",
    simulated_sender: "家长E",
    input_text: "这个 AI 和普通补课有什么区别？",
    category: "AI 和补课区别",
    expected_reply_style: "随时问、反复练，不能替代老师。",
    should_reply: true,
    risk_note: "不要贬低老师或机构。"
  },
  {
    message_id: "SIM-006",
    simulated_sender: "家长F",
    input_text: "我担心孩子用了 AI 以后就不动脑子了，会不会依赖？",
    category: "担心孩子依赖 AI",
    expected_reply_style: "承认风险，强调引导式使用。",
    should_reply: true,
    risk_note: "不要否认风险。"
  },
  {
    message_id: "SIM-007",
    simulated_sender: "家长G",
    input_text: "手机上能不能用？家里老人带孩子，电脑不太会。",
    category: "手机能不能用",
    expected_reply_style: "说明可以设计成手机聊天式体验，但不编造已上线入口。",
    should_reply: true,
    risk_note: "不要说已上线 APP 或微信号。"
  },
  {
    message_id: "SIM-008",
    simulated_sender: "家长H",
    input_text: "四年级语文作文总是写流水账，有办法练吗？",
    category: "四年级语文作文",
    expected_reply_style: "给一个可执行练习办法。",
    should_reply: true,
    risk_note: "不要长篇教学。"
  },
  {
    message_id: "SIM-009",
    simulated_sender: "家长I",
    input_text: "三年级数学应用题，孩子读不懂题，这种能辅导吗？",
    category: "三年级数学应用题",
    expected_reply_style: "强调读题、圈关键词、画图或拆步骤。",
    should_reply: true,
    risk_note: "不要直接承诺提分。"
  },
  {
    message_id: "SIM-010",
    simulated_sender: "家长J",
    input_text: "孩子写作业拖拉，坐半小时一个字不写，这个能帮上忙吗？",
    category: "作业拖拉",
    expected_reply_style: "给轻量方法，必要时家长陪伴和规则。",
    should_reply: true,
    risk_note: "不做心理/医疗诊断。"
  },
  {
    message_id: "SIM-011",
    simulated_sender: "家长K",
    input_text: "我下班晚，没时间每天辅导孩子作业，这个能不能帮我分担一点？",
    category: "家长没时间辅导",
    expected_reply_style: "说明能辅助讲题、检查思路、陪练，但家长仍要关注。",
    should_reply: true,
    risk_note: "不要替代家长或老师。"
  },
  {
    message_id: "SIM-012",
    simulated_sender: "家长L",
    input_text: "我想先试试看，不知道孩子愿不愿意配合。",
    category: "想先试试看",
    expected_reply_style: "建议从一个小问题开始体验。",
    should_reply: true,
    risk_note: "不要催单，不要夸大。"
  }
];

function safeTextForMarkdown(s) {
  return String(s || "").replace(/\|/g, "/").replace(/\r?\n/g, " ");
}

async function chat(model, inputText, key) {
  const started = Date.now();
  const system = [
    "你是“小龙虾”AI学习辅导服务在家长群里的草稿回复助手。",
    "这是本地 shadow test，只生成草稿，不发送消息。",
    "“小龙虾”是服务/账号名称，不是水产动物。",
    "只用中文，像普通家长群里的人说话。",
    "回复 60 到 120 个中文字左右。",
    "不要提模型、API、NVIDIA、OpenAI、provider、ChatGPT。",
    "不要承诺成绩一定提升，不要夸大，不要做医疗、金融、法律承诺。",
    "不要编造 APP、下载、微信、网站、手机版本、24小时、第一周免费、付费、订阅、续费、具体价格、个性化辅导计划、服务质量等未确认信息。",
    "遇到低置信度问题，只给“建议人工回复”的温和草稿。"
  ].join("\n");
  const body = {
    model,
    messages: [
      { role: "system", content: system },
      { role: "user", content: `请根据这条模拟家长群消息生成一条可供人工审核的回复草稿：\n${inputText}` }
    ],
    temperature: 0,
    max_tokens: 170,
    stream: false
  };
  try {
    const res = await fetchJson(`${BASE_URL}/chat/completions`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${key}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    }, 70000);
    const content = res.json?.choices?.[0]?.message?.content || "";
    return {
      selected_model: model,
      draft_reply: content.trim(),
      latency_ms: Date.now() - started,
      http_status: res.status,
      success: res.ok && !!content.trim(),
      error_summary: res.ok ? "" : redact(res.text).slice(0, 500)
    };
  } catch (e) {
    return {
      selected_model: model,
      draft_reply: "",
      latency_ms: Date.now() - started,
      http_status: 0,
      success: false,
      error_summary: redact(e.message).slice(0, 500)
    };
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function evaluateDraft(reply) {
  const text = String(reply || "").trim();
  const cjk = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const chinese_ok = cjk >= 25;
  const short_ok = cjk >= 25 && cjk <= 150 && text.length <= 240;
  const no_model_leak = !/(NVIDIA|OpenAI|ChatGPT|API|provider|model|llama|NIM|模型|接口)/i.test(text);
  const no_false_promise = !/(一定提|保证|包提|肯定提|100%|百分百|必然|一定能|必定)/.test(text);
  const no_unverified_claim = !/(第一周|续费|APP|下载|微信|网站|24小时|价格|收费标准|付费|订阅|手机版本|手机端版本|专门的手机|个性化辅导计划|服务质量|提高学习效率|提高.*效果)/i.test(text);
  const no_english_reasoning = !/(As an AI|I need to|We need to|large language model|Let's craft|Need to answer)/i.test(text);
  const no_garbled_text = !/�/.test(text);
  const no_product_confusion = !/(水产|养殖|照顾小龙虾|龙虾习性|捕捞|烹饪|好吃)/.test(text);
  const natural_group_chat_ok = chinese_ok && no_english_reasoning && (text.match(/[A-Za-z]{4,}/g) || []).length <= 2;
  const useful_ok = /(作文|提纲|表达|数学|步骤|题意|练|试|体验|手机|家长|老师|辅导|引导|作业|思路|孩子|学习)/.test(text);
  const parent_friendly = chinese_ok && no_false_promise && no_unverified_claim && no_product_confusion;
  const suitable_to_send_after_human_review = chinese_ok && natural_group_chat_ok && short_ok && useful_ok && no_model_leak && no_false_promise && no_unverified_claim && no_english_reasoning && no_garbled_text && no_product_confusion;
  let score = 1;
  if (suitable_to_send_after_human_review) score = 5;
  else if (chinese_ok && natural_group_chat_ok && no_model_leak && no_false_promise && no_unverified_claim && no_product_confusion) score = 4;
  else if (chinese_ok && no_model_leak && no_false_promise && no_english_reasoning) score = 3;
  else if (text) score = 2;
  const reject = [];
  if (!chinese_ok) reject.push("中文不足");
  if (!short_ok) reject.push("长度不合适");
  if (!natural_group_chat_ok) reject.push("不像群聊口吻或含英文推理");
  if (!useful_ok) reject.push("帮助性不足");
  if (!no_model_leak) reject.push("泄露模型/API/provider");
  if (!no_false_promise) reject.push("存在虚假承诺");
  if (!no_unverified_claim) reject.push("包含未确认渠道/价格声明");
  if (!no_garbled_text) reject.push("疑似乱码");
  if (!no_product_confusion) reject.push("小龙虾产品语境混淆");
  return {
    chinese_ok,
    natural_group_chat_ok,
    short_ok,
    useful_ok,
    no_model_leak,
    no_false_promise,
    parent_friendly,
    suitable_to_send_after_human_review,
    no_english_reasoning,
    no_garbled_text,
    no_unverified_claim,
    no_product_confusion,
    score_1_to_5: score,
    reject_reason: reject.length ? reject.join("; ") : ""
  };
}

async function main() {
  const preModels = await getProductionModels();
  const baseline = {
    captured_at: new Date().toISOString(),
    hashes: {
      openclaw_config: sha256File(OPENCLAW_CONFIG),
      xiaolongxia_compose: sha256File(XLLX_COMPOSE),
      xiaolongxia_env: sha256File(XLLX_ENV),
      production_model_ids: sha256String(preModels.modelIds.join("\n"))
    },
    production_models: {
      ok: preModels.ok,
      status: preModels.status,
      count: preModels.modelIds.length,
      first_10: preModels.modelIds.slice(0, 10)
    }
  };
  writeJson("G29-production-baseline.json", baseline);

  const realSendRisk = checkRealSendRisk();
  const g29 = {
    status: "G29_PASS_PRECHECK_READY",
    required_paths: {
      previous_final_report: exists(PREV_ROUTE_REPORT),
      local_skill: exists(LOCAL_SKILL),
      h_skill: exists(H_SKILL),
      candidate_config: exists(PREV_ROUTE_CONFIG),
      nvidia_key_file: exists(NVIDIA_KEY_FILE),
      openclaw_config: exists(OPENCLAW_CONFIG),
      xiaolongxia_compose: exists(XLLX_COMPOSE)
    },
    production_models: baseline.production_models,
    openclaw_validate: run("openclaw config validate"),
    real_send_risk: realSendRisk,
    key_scan_hits: scanKeyPatterns([OUT, LOCAL_SKILL, H_SKILL])
  };
  if (!g29.required_paths.nvidia_key_file) g29.status = "G29_STOP_NVIDIA_KEY_REQUIRED";
  if (Object.values(g29.required_paths).some(v => !v) || !g29.openclaw_validate.ok || g29.real_send_risk.risky_count > 0 || g29.key_scan_hits.length > 0) {
    g29.status = g29.status === "G29_STOP_NVIDIA_KEY_REQUIRED" ? g29.status : "G29_STOP_PRECHECK_FAILED";
  }
  writeJson("G29-precheck.json", g29);
  writeText("G29-precheck.md", `# G29 Precheck

Status: \`${g29.status}\`

| Check | Result |
| --- | --- |
| Previous final report exists | ${g29.required_paths.previous_final_report} |
| Local skill exists | ${g29.required_paths.local_skill} |
| H skill mirror exists | ${g29.required_paths.h_skill} |
| Candidate config exists | ${g29.required_paths.candidate_config} |
| NVIDIA key file exists | ${g29.required_paths.nvidia_key_file} |
| OpenClaw config exists | ${g29.required_paths.openclaw_config} |
| 3011 compose exists | ${g29.required_paths.xiaolongxia_compose} |
| 3011 model count | ${baseline.production_models.count} |
| OpenClaw validate | ${g29.openclaw_validate.ok ? "PASS" : "FAIL"} |
| Real send risky process count | ${g29.real_send_risk.risky_count} |
| Output/skill key scan hits | ${g29.key_scan_hits.length} |

No real group send interface is used by this shadow test.
`);
  if (g29.status !== "G29_PASS_PRECHECK_READY") {
    const finalStatus = g29.status === "G29_STOP_NVIDIA_KEY_REQUIRED"
      ? "XIAOLONGXIA_NVIDIA_SHADOW_TEST_STOP_KEY_REQUIRED"
      : "XIAOLONGXIA_NVIDIA_SHADOW_TEST_STOP_REAL_SEND_RISK";
    writeText("final-report.md", `# Final Report

Final status:

\`${finalStatus}\`

Stopped at G29. See \`G29-precheck.md\`.
`);
    return;
  }

  fs.writeFileSync(path.join(INPUT_DIR, "simulated-parent-group-messages.json"), JSON.stringify(messages, null, 2) + "\n", "utf8");
  writeText("G30-shadow-input-dataset.md", `# G30 Shadow Input Dataset

Status: \`G30_PASS_SHADOW_INPUT_READY\`

Created:

\`shadow-input/simulated-parent-group-messages.json\`

Message count: ${messages.length}

| ID | Category | Should reply | Risk note |
| --- | --- | --- | --- |
${messages.map(m => `| ${m.message_id} | ${m.category} | ${m.should_reply} | ${m.risk_note} |`).join("\n")}

All messages are local simulations. They do not contain real contacts, real group names, or phone numbers.
`);

  const key = fs.readFileSync(NVIDIA_KEY_FILE, "utf8").trim();
  process.env.NVIDIA_API_KEY = key;
  const drafts = [];
  for (const m of messages) {
    let result = await chat(PRIMARY, m.input_text, key);
    let used_fallback = false;
    let evalFirst = evaluateDraft(result.draft_reply);
    if ((!result.success || evalFirst.score_1_to_5 < 4) && m.should_reply) {
      await sleep(1200);
      const fb = await chat(FALLBACK, m.input_text, key);
      const evalFb = evaluateDraft(fb.draft_reply);
      if (fb.success && evalFb.score_1_to_5 >= evalFirst.score_1_to_5) {
        result = fb;
        used_fallback = true;
      }
    }
    drafts.push({
      message_id: m.message_id,
      input_text: m.input_text,
      selected_model: result.selected_model,
      used_fallback,
      draft_reply: result.draft_reply,
      latency_ms: result.latency_ms,
      http_status: result.http_status,
      error_summary: result.error_summary,
      generated_at: new Date().toISOString(),
      sent_to_real_group: false
    });
    await sleep(1500);
  }
  delete process.env.NVIDIA_API_KEY;

  const successfulDrafts = drafts.filter(d => d.http_status === 200 && d.draft_reply).length;
  const g31Status = successfulDrafts === messages.length
    ? "G31_PASS_SHADOW_DRAFTS_GENERATED"
    : successfulDrafts > 0
      ? "G31_PARTIAL_SHADOW_DRAFTS_GENERATED"
      : "G31_FAIL_SHADOW_DRAFT_GENERATION";
  writeJson("G31-shadow-generated-drafts.json", drafts);
  writeText("G31-shadow-generated-drafts.md", `# G31 Shadow Generated Drafts

Status: \`${g31Status}\`

Generated drafts: ${successfulDrafts}/${messages.length}

| ID | Model | Fallback | HTTP | Sent real group | Latency ms | Draft preview |
| --- | --- | --- | ---: | --- | ---: | --- |
${drafts.map(d => `| ${d.message_id} | \`${d.selected_model}\` | ${d.used_fallback} | ${d.http_status} | ${d.sent_to_real_group} | ${d.latency_ms} | ${safeTextForMarkdown(d.draft_reply).slice(0, 180)} |`).join("\n")}
`);

  const reviews = drafts.map(d => ({
    message_id: d.message_id,
    input_text: d.input_text,
    selected_model: d.selected_model,
    used_fallback: d.used_fallback,
    sent_to_real_group: d.sent_to_real_group,
    draft_reply: d.draft_reply,
    ...evaluateDraft(d.draft_reply)
  }));
  const score4 = reviews.filter(r => r.score_1_to_5 >= 4).length;
  const leakCount = reviews.filter(r => !r.no_model_leak).length;
  const falsePromiseCount = reviews.filter(r => !r.no_false_promise).length;
  const englishReasoningCount = reviews.filter(r => !r.no_english_reasoning).length;
  const garbledCount = reviews.filter(r => !r.no_garbled_text).length;
  const sentCount = reviews.filter(r => r.sent_to_real_group).length;
  const g32Status = score4 >= 10 && leakCount === 0 && falsePromiseCount === 0 && englishReasoningCount === 0 && garbledCount === 0 && sentCount === 0
    ? "G32_PASS_SHADOW_QUALITY_REVIEW"
    : score4 >= 7
      ? "G32_PARTIAL_SHADOW_QUALITY_REVIEW"
      : "G32_FAIL_SHADOW_QUALITY_REVIEW";
  writeJson("G32-shadow-draft-quality-review.json", reviews);
  writeText("G32-shadow-draft-quality-review.md", `# G32 Shadow Draft Quality Review

Status: \`${g32Status}\`

| Metric | Value |
| --- | ---: |
| Score >= 4 | ${score4}/${reviews.length} |
| Model/API/provider leaks | ${leakCount} |
| False promises | ${falsePromiseCount} |
| English reasoning | ${englishReasoningCount} |
| Garbled text | ${garbledCount} |
| Real sends | ${sentCount} |

| ID | Score | Suitable after review | Model | Reject reason |
| --- | ---: | --- | --- | --- |
${reviews.map(r => `| ${r.message_id} | ${r.score_1_to_5} | ${r.suitable_to_send_after_human_review} | \`${r.selected_model}\` | ${r.reject_reason || "none"} |`).join("\n")}
`);

  const failures = reviews.filter(r => r.score_1_to_5 < 4);
  if (failures.length === 0) {
    writeText("G33-shadow-failure-fix-suggestions.md", `# G33 Failure Fix Suggestions

Status: \`G33_PASS_NO_MAJOR_FAILURES\`

No score-below-4 samples were found in this shadow test.

Keep the current prompt rules:

- Xiaolongxia is an AI learning service name, not a seafood topic.
- Do not mention model/API/provider.
- Do not make unverified channel or pricing claims.
- Do not promise grade improvement.
- Draft only; human review required before real group use.
`);
  } else {
    writeText("G33-shadow-failure-fix-suggestions.md", `# G33 Failure Fix Suggestions

Status: \`G33_FIX_SUGGESTIONS_READY\`

| Message | Category | Reason |
| --- | --- | --- |
${failures.map(f => {
  const m = messages.find(x => x.message_id === f.message_id);
  return `| ${f.message_id} | ${m?.category || ""} | ${f.reject_reason} |`;
}).join("\n")}

Suggested system prompt additions:

- If unsure about price, channel, app, website, or availability, say "可以先人工确认后再回复".
- Keep replies closer to 60-100 Chinese characters.
- If the question asks for medical, legal, financial, account, payment, or privacy advice, generate "建议人工回复" instead of an answer.

Model routing suggestion:

- Keep 8B as primary.
- Use 70B fallback only when 8B fails or gets score below 4 in local review.
- Do not auto-send low-score replies.
`);
  }

  const rules = {
    version: "2026-05-24",
    status: "G34_PASS_SHADOW_RULES_READY",
    route: ROUTE_NAME,
    primary: PRIMARY,
    fallback: FALLBACK,
    excluded: [EXCLUDED],
    rules: [
      "回复字数 60 到 120 个中文字左右",
      "只用中文",
      "真人家长群口吻",
      "不提模型/API/provider/NVIDIA/OpenAI/ChatGPT",
      "不夸大",
      "不承诺成绩一定提升",
      "不自动发送",
      "真实群聊阶段必须人工确认",
      "低置信度时生成建议人工回复",
      "遇到医疗、法律、金融、账号、密码、隐私、支付等敏感问题不自动回答",
      "免费体验问题只简短说明可以先体验，不编造价格、续费、第一周等细节",
      "学习问题以讲题、改作文、陪练、启发为核心"
    ],
    send_policy: {
      auto_send: false,
      human_review_required: true,
      real_group_enabled: false
    }
  };
  fs.writeFileSync(path.join(CANDIDATE_DIR, "xiaolongxia-shadow-reply-rules.json"), JSON.stringify(rules, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(CANDIDATE_DIR, "xiaolongxia-shadow-reply-rules.md"), `# Xiaolongxia Shadow Reply Rules

Status: \`G34_PASS_SHADOW_RULES_READY\`

These rules are candidates only and are not production configuration.

1. 回复字数 60 到 120 个中文字左右。
2. 中文。
3. 真人群聊口吻。
4. 不提模型/API/provider/NVIDIA/OpenAI/ChatGPT。
5. 不夸大。
6. 不承诺成绩一定提升。
7. 不自动发送。
8. 真实群聊阶段必须人工确认。
9. 低置信度时生成“建议人工回复”。
10. 遇到敏感问题不自动回答。
11. 免费体验问题可以简短说明可以先体验，但不编造价格、续费、第一周。
12. 学习问题以“讲题、改作文、陪练、启发”为核心。
`, "utf8");

  const postModels = await getProductionModels();
  const post = {
    captured_at: new Date().toISOString(),
    hashes: {
      openclaw_config: sha256File(OPENCLAW_CONFIG),
      xiaolongxia_compose: sha256File(XLLX_COMPOSE),
      xiaolongxia_env: sha256File(XLLX_ENV),
      production_model_ids: sha256String(postModels.modelIds.join("\n"))
    },
    production_models: {
      ok: postModels.ok,
      status: postModels.status,
      count: postModels.modelIds.length
    }
  };
  const g35 = {
    status: "G35_PASS_PRODUCTION_UNCHANGED",
    openclaw_config_hash_same: baseline.hashes.openclaw_config === post.hashes.openclaw_config,
    xiaolongxia_compose_hash_same: baseline.hashes.xiaolongxia_compose === post.hashes.xiaolongxia_compose,
    xiaolongxia_env_hash_same: baseline.hashes.xiaolongxia_env === post.hashes.xiaolongxia_env,
    production_model_list_hash_same: baseline.hashes.production_model_ids === post.hashes.production_model_ids,
    model_count_before: baseline.production_models.count,
    model_count_after: post.production_models.count,
    no_real_send: sentCount === 0 && checkRealSendRisk().risky_count === 0,
    nvidia_env_still_set: !!process.env.NVIDIA_API_KEY,
    key_scan_hits: scanKeyPatterns([OUT, LOCAL_SKILL, H_SKILL]),
    openclaw_validate_after: run("openclaw config validate")
  };
  if (!g35.openclaw_config_hash_same || !g35.xiaolongxia_compose_hash_same || !g35.xiaolongxia_env_hash_same || !g35.production_model_list_hash_same || !g35.no_real_send || g35.nvidia_env_still_set || g35.key_scan_hits.length || !g35.openclaw_validate_after.ok) {
    g35.status = "G35_STOP_PRODUCTION_CHANGED_NEEDS_ROLLBACK";
    writeText("rollback-needed.md", `# Rollback Needed

G35 detected a production difference or send risk. Stop before skill update.

See \`G35-production-diff-check.md\`.
`);
  }
  writeJson("G35-production-diff-check.json", g35);
  writeText("G35-production-diff-check.md", `# G35 Production Diff Check

Status: \`${g35.status}\`

| Check | Result |
| --- | --- |
| OpenClaw config hash same | ${g35.openclaw_config_hash_same} |
| 3011 compose hash same | ${g35.xiaolongxia_compose_hash_same} |
| 3011 env hash same | ${g35.xiaolongxia_env_hash_same} |
| 3011 model list hash same | ${g35.production_model_list_hash_same} |
| 3011 model count before/after | ${g35.model_count_before}/${g35.model_count_after} |
| No real send | ${g35.no_real_send} |
| NVIDIA_API_KEY still set | ${g35.nvidia_env_still_set} |
| Key scan hits | ${g35.key_scan_hits.length} |
| OpenClaw validate after | ${g35.openclaw_validate_after.ok ? "PASS" : "FAIL"} |
`);

  const finalStatus = g35.status !== "G35_PASS_PRODUCTION_UNCHANGED"
    ? "XIAOLONGXIA_NVIDIA_SHADOW_TEST_STOP_PRODUCTION_CHANGED"
    : g32Status === "G32_PASS_SHADOW_QUALITY_REVIEW" && g31Status === "G31_PASS_SHADOW_DRAFTS_GENERATED"
      ? "XIAOLONGXIA_NVIDIA_SHADOW_TEST_LOCAL_DRAFT_PASS"
      : "XIAOLONGXIA_NVIDIA_SHADOW_TEST_LOCAL_DRAFT_PARTIAL";
  writeText("G37-final-report-draft.md", `# Final Report Draft

Final status:

\`${finalStatus}\`

This draft is generated before G36 skill sync. Final report will be written after sync verification.
`);
}

main().catch(err => {
  delete process.env.NVIDIA_API_KEY;
  writeText("run-error.md", `# Run Error

\`${redact(err.stack || err.message)}\`
`);
  process.exitCode = 1;
});
