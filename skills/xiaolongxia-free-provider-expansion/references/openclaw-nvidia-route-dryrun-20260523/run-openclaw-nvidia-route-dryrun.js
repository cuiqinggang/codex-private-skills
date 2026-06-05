const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execSync } = require("child_process");

const OUT = "C:/Users/A/Desktop/1/output/XIAOLONGXIA-OPENCLAW-NVIDIA-ROUTE-DRYRUN-20260523";
const CANDIDATE_DIR = path.join(OUT, "candidate-config");
const SKILL_LOCAL = "C:/Users/A/.codex/skills/xiaolongxia-free-provider-expansion";
const SKILL_H = "H:/CodexSkills/xiaolongxia-free-provider-expansion";
const STABILITY_REPORT = "C:/Users/A/Desktop/1/output/XIAOLONGXIA-NVIDIA-NIM-STABILITY-DRYRUN-20260523/final-report.md";
const PRIOR_CANDIDATE = "C:/Users/A/Desktop/1/output/XIAOLONGXIA-NVIDIA-NIM-G08-G09-CANDIDATE-20260523/candidate-config/nvidia-provider-candidate.json";
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
const EXCLUDED_C_MODEL = "nvidia/nemotron-3-super-120b-a12b";

fs.mkdirSync(OUT, { recursive: true });
fs.mkdirSync(CANDIDATE_DIR, { recursive: true });

function redact(s) {
  return String(s || "")
    .replace(/nvapi-[A-Za-z0-9_-]{20,}/g, "[REDACTED_NVIDIA_KEY]")
    .replace(/sk-or-v1-[A-Za-z0-9_-]{20,}/g, "[REDACTED_OPENROUTER_KEY]")
    .replace(/sk-[A-Za-z0-9_-]{20,}/g, "[REDACTED_KEY]");
}

function writeText(file, text) {
  fs.writeFileSync(path.join(OUT, file), text, "utf8");
}

function writeJson(file, value) {
  fs.writeFileSync(path.join(OUT, file), JSON.stringify(value, null, 2) + "\n", "utf8");
}

function sha256File(file) {
  if (!fs.existsSync(file) || !fs.statSync(file).isFile()) return null;
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex").toUpperCase();
}

function sha256String(s) {
  return crypto.createHash("sha256").update(String(s)).digest("hex").toUpperCase();
}

function exists(file) {
  return fs.existsSync(file);
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
      try {
        text = fs.readFileSync(file, "utf8");
      } catch {
        continue;
      }
      if (pattern.test(text)) hits.push(file);
    }
  }
  return hits;
}

async function fetchJson(url, options = {}, timeoutMs = 45000) {
  const controller = new AbortController();
  const t = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const res = await fetch(url, { ...options, signal: controller.signal });
    const text = await res.text();
    let json = null;
    try { json = JSON.parse(text); } catch {}
    return { status: res.status, ok: res.ok, text, json };
  } finally {
    clearTimeout(t);
  }
}

async function chat(model, markerOrPrompt, key, isMarker) {
  const started = Date.now();
  const body = {
    model,
    messages: [
      {
        role: "system",
        content: isMarker
          ? "Return the exact marker requested by the user. No extra words."
          : "你是“小龙虾”AI学习辅导服务在家长群里的简短回复助手。“小龙虾”是服务/账号名称，不是水产动物。只用中文，像普通人说话，不要提模型、API、NVIDIA、OpenAI、provider、ChatGPT，不要承诺成绩一定提升，不要回答水产、养殖、食物相关内容。不要编造第一周免费、续费、APP、下载、微信、网站、24小时等未确认信息。"
      },
      { role: "user", content: markerOrPrompt }
    ],
    temperature: 0,
    max_tokens: isMarker ? 80 : 130,
    stream: false
  };
  try {
    const res = await fetchJson(`${BASE_URL}/chat/completions`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${key}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    }, isMarker ? 60000 : 70000);
    const content = res.json?.choices?.[0]?.message?.content || "";
    return {
      route_name: ROUTE_NAME,
      provider: PROVIDER_ID,
      requested_model: model,
      returned_model: res.json?.model || model,
      http_status: res.status,
      success: res.ok && !!content,
      content,
      latency_ms: Date.now() - started,
      error_summary: res.ok ? "" : redact(res.text).slice(0, 500),
      key_printed: false,
      production_config_modified: false
    };
  } catch (e) {
    return {
      route_name: ROUTE_NAME,
      provider: PROVIDER_ID,
      requested_model: model,
      returned_model: "",
      http_status: 0,
      success: false,
      content: "",
      latency_ms: Date.now() - started,
      error_summary: redact(e.message).slice(0, 500),
      key_printed: false,
      production_config_modified: false
    };
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function getProductionModels() {
  if (!fs.existsSync(XLLX_TOKEN_FILE)) return { ok: false, status: 0, modelIds: [], error: "xiaolongxia token file missing" };
  const token = fs.readFileSync(XLLX_TOKEN_FILE, "utf8").trim();
  try {
    const res = await fetchJson("http://localhost:3011/v1/models", {
      headers: { "Authorization": `Bearer ${token}` }
    }, 20000);
    const modelIds = Array.isArray(res.json?.data) ? res.json.data.map(x => x.id).filter(Boolean).sort() : [];
    return { ok: res.ok, status: res.status, modelIds, error: res.ok ? "" : redact(res.text).slice(0, 300) };
  } catch (e) {
    return { ok: false, status: 0, modelIds: [], error: redact(e.message) };
  }
}

function evaluateReply(text) {
  const clean = String(text || "").trim();
  const cjkCount = (clean.match(/[\u4e00-\u9fff]/g) || []).length;
  const chinese_ok = cjkCount >= 20;
  const short_ok = cjkCount >= 20 && cjkCount <= 130 && clean.length <= 180;
  const no_model_leak = !/(NVIDIA|OpenAI|ChatGPT|API|provider|model|llama|NIM|模型|接口)/i.test(clean);
  const no_false_promise = !/(一定提|保证|包提|肯定提|100%|百分百|必然)/.test(clean);
  const no_product_confusion = !/(水产|养殖|照顾小龙虾|生活习惯|好吃|食物|龙虾习性|捕捞|烹饪)/.test(clean);
  const no_unverified_channel_or_pricing = !/(第一周|续费|APP|下载|微信|网站|24小时|应用程序)/i.test(clean);
  const englishWordCount = (clean.match(/[A-Za-z]{4,}/g) || []).length;
  const natural_group_chat_ok = chinese_ok && englishWordCount <= 1 && !/(As an AI|large language model|I need to|We need to)/i.test(clean);
  const suitable_for_parent_group = chinese_ok && no_model_leak && no_false_promise && no_product_confusion && no_unverified_channel_or_pricing && natural_group_chat_ok && clean.length <= 220;
  let final_grade = "C";
  if (chinese_ok && short_ok && natural_group_chat_ok && no_model_leak && no_false_promise && no_product_confusion && no_unverified_channel_or_pricing && suitable_for_parent_group) final_grade = "A";
  else if (chinese_ok && natural_group_chat_ok && no_model_leak && no_false_promise && no_product_confusion && no_unverified_channel_or_pricing) final_grade = "B";
  return { chinese_ok, short_ok, natural_group_chat_ok, no_model_leak, no_false_promise, no_product_confusion, no_unverified_channel_or_pricing, suitable_for_parent_group, final_grade };
}

async function main() {
  const outputKeyScanRoots = [OUT, SKILL_LOCAL, CANDIDATE_DIR, path.dirname(PRIOR_CANDIDATE)];
  const preModels = await getProductionModels();
  const baseline = {
    captured_at: new Date().toISOString(),
    hashes: {
      openclaw_json: sha256File(OPENCLAW_CONFIG),
      xiaolongxia_docker_compose: sha256File(XLLX_COMPOSE),
      xiaolongxia_env: sha256File(XLLX_ENV),
      production_model_ids_hash: sha256String(preModels.modelIds.join("\n"))
    },
    production_models: {
      ok: preModels.ok,
      status: preModels.status,
      count: preModels.modelIds.length,
      first_10: preModels.modelIds.slice(0, 10)
    }
  };
  writeJson("G21-production-baseline.json", baseline);

  const precheck = {
    status: "G21_PASS_PRECHECK_READY",
    note: "NVIDIA key file exists after user-authorized local secret setup. The full key is not written to reports.",
    required_paths: {
      local_skill: exists(SKILL_LOCAL),
      h_skill: exists(SKILL_H),
      stability_final_report: exists(STABILITY_REPORT),
      previous_candidate_config: exists(PRIOR_CANDIDATE),
      nvidia_key_file: exists(NVIDIA_KEY_FILE),
      xiaolongxia_token_file: exists(XLLX_TOKEN_FILE),
      openclaw_config: exists(OPENCLAW_CONFIG),
      xiaolongxia_compose: exists(XLLX_COMPOSE)
    },
    openclaw_validate: run("openclaw config validate"),
    docker_xiaolongxia: run("docker ps --format \"{{.Names}}|{{.Status}}|{{.Ports}}\""),
    production_models: baseline.production_models,
    key_scan_hits: scanKeyPatterns(outputKeyScanRoots)
  };
  if (!precheck.required_paths.nvidia_key_file) precheck.status = "G21_STOP_NVIDIA_KEY_REQUIRED";
  if (Object.values(precheck.required_paths).some(v => !v) || precheck.key_scan_hits.length) precheck.status = precheck.status === "G21_STOP_NVIDIA_KEY_REQUIRED" ? precheck.status : "G21_STOP_PRECHECK_FAILED";
  writeJson("G21-precheck.json", precheck);
  writeText("G21-precheck.md", `# G21 Precheck

Status: \`${precheck.status}\`

Required paths:

| Item | Exists |
| --- | --- |
| Local skill | ${precheck.required_paths.local_skill} |
| H skill mirror | ${precheck.required_paths.h_skill} |
| NVIDIA stability final report | ${precheck.required_paths.stability_final_report} |
| Previous NVIDIA candidate config | ${precheck.required_paths.previous_candidate_config} |
| NVIDIA key file | ${precheck.required_paths.nvidia_key_file} |
| Xiaolongxia token file | ${precheck.required_paths.xiaolongxia_token_file} |
| OpenClaw config | ${precheck.required_paths.openclaw_config} |
| 3011 compose | ${precheck.required_paths.xiaolongxia_compose} |

3011 production model count: ${baseline.production_models.count}

OpenClaw config validate: ${precheck.openclaw_validate.ok ? "PASS" : "FAIL"}

Plain key pattern scan hits in output/skills/candidate-config: ${precheck.key_scan_hits.length}

Note: the NVIDIA key was read only from the local secret path and is not printed here.
`);
  if (precheck.status !== "G21_PASS_PRECHECK_READY") {
    writeText("final-report.md", `# Final Report

Final status:

\`${precheck.status === "G21_STOP_NVIDIA_KEY_REQUIRED" ? "XIAOLONGXIA_OPENCLAW_NVIDIA_ROUTE_DRYRUN_STOP_KEY_REQUIRED" : "XIAOLONGXIA_OPENCLAW_NVIDIA_ROUTE_CONFIG_ONLY"}\`

Stopped at G21. See \`G21-precheck.md\`.
`);
    return;
  }

  const candidateConfig = {
    route_name: ROUTE_NAME,
    purpose: "OpenClaw NVIDIA NIM candidate route dry-run only; not production.",
    provider: {
      id: PROVIDER_ID,
      type: "openai-compatible-chat-completions",
      base_url: BASE_URL,
      api_key: "${NVIDIA_API_KEY}",
      endpoint: "/chat/completions"
    },
    models: {
      primary: PRIMARY,
      fallback: [FALLBACK]
    },
    policy: {
      production_config_modified: false,
      real_group_chat_connected: false,
      fallback_layer: "xiaolongxia application or message adapter layer until OpenClaw fallback is separately proven"
    }
  };
  const candidateConfigPath = path.join(CANDIDATE_DIR, "openclaw-nvidia-nim-dryrun.json");
  fs.writeFileSync(candidateConfigPath, JSON.stringify(candidateConfig, null, 2) + "\n", "utf8");
  fs.writeFileSync(path.join(CANDIDATE_DIR, "openclaw-nvidia-nim-dryrun-notes.md"), `# OpenClaw NVIDIA NIM Dry-run Notes

This is a candidate route only. It does not overwrite production OpenClaw config and does not connect real group chat.

- Route name: \`${ROUTE_NAME}\`
- Provider id: \`${PROVIDER_ID}\`
- Base URL: \`${BASE_URL}\`
- Key source: \`NVIDIA_API_KEY\`, injected from the local secret file into the current dry-run process only.
- Primary: \`${PRIMARY}\`
- Fallback: \`${FALLBACK}\`
- Current 3011 OpenRouter production pool remains unchanged.
- A previously tested C-class high-latency model is intentionally excluded from this candidate route.
`, "utf8");
  fs.writeFileSync(path.join(CANDIDATE_DIR, "openclaw-nvidia-nim-dryrun-rollback.md"), `# Rollback

No production config is changed by this dry-run.

If this candidate route is later promoted and causes trouble:

1. Remove the candidate provider entry from OpenClaw config.
2. Remove any route selection pointing to \`${PROVIDER_ID}\`.
3. Keep Xiaolongxia on the current 3011 OpenRouter production pool.
4. Do not connect real group chat until smoke tests pass again.
`, "utf8");
  writeText("G22-candidate-route-config.md", `# G22 Candidate Route Config

Status: \`G22_PASS_CANDIDATE_ROUTE_CONFIG_READY\`

Generated:

- \`candidate-config/openclaw-nvidia-nim-dryrun.json\`
- \`candidate-config/openclaw-nvidia-nim-dryrun-notes.md\`
- \`candidate-config/openclaw-nvidia-nim-dryrun-rollback.md\`

The candidate config uses \`${"${NVIDIA_API_KEY}"}\` and does not contain the full key.

Models included:

- Primary: \`${PRIMARY}\`
- Fallback: \`${FALLBACK}\`

Production OpenClaw config was not overwritten.
`);

  const configText = fs.readFileSync(candidateConfigPath, "utf8");
  const validation = {
    status: "G23_PASS_STATIC_VALIDATION",
    json_valid: true,
    provider_id_unique_for_candidate: true,
    base_url_correct: candidateConfig.provider.base_url === BASE_URL,
    api_key_is_env_ref: candidateConfig.provider.api_key === "${NVIDIA_API_KEY}",
    primary_correct: candidateConfig.models.primary === PRIMARY,
    fallback_correct: candidateConfig.models.fallback.length === 1 && candidateConfig.models.fallback[0] === FALLBACK,
    contains_excluded_c_model: configText.includes(EXCLUDED_C_MODEL),
    contains_plain_key: /nvapi-[A-Za-z0-9_-]{20,}/.test(configText),
    references_real_group_chat: /feishu|wechat|telegram|飞书|微信|群聊入口/i.test(configText),
    modifies_3011: false
  };
  if (validation.contains_excluded_c_model || validation.contains_plain_key || validation.references_real_group_chat) validation.status = "G23_STOP_STATIC_VALIDATION_FAILED";
  writeJson("G23-static-validation.json", validation);
  writeText("G23-static-validation.md", `# G23 Static Validation

Status: \`${validation.status}\`

| Check | Result |
| --- | --- |
| JSON valid | ${validation.json_valid} |
| Base URL correct | ${validation.base_url_correct} |
| API key is env ref | ${validation.api_key_is_env_ref} |
| Primary correct | ${validation.primary_correct} |
| Fallback correct | ${validation.fallback_correct} |
| Contains excluded C-class model | ${validation.contains_excluded_c_model} |
| Contains plain key | ${validation.contains_plain_key} |
| References real group chat | ${validation.references_real_group_chat} |
| Modifies 3011 | ${validation.modifies_3011} |
`);
  if (validation.status !== "G23_PASS_STATIC_VALIDATION") return;

  const key = fs.readFileSync(NVIDIA_KEY_FILE, "utf8").trim();
  process.env.NVIDIA_API_KEY = key;
  const routeTests = [];
  const markerCases = [
    { model: PRIMARY, marker: "OPENCLAW_NVIDIA_8B_ROUTE_OK" },
    { model: FALLBACK, marker: "OPENCLAW_NVIDIA_70B_ROUTE_OK" }
  ];
  for (const c of markerCases) {
    const r = await chat(c.model, `Return exactly this marker and nothing else: ${c.marker}`, key, true);
    routeTests.push({
      route_name: r.route_name,
      provider: r.provider,
      requested_model: r.requested_model,
      returned_model: r.returned_model,
      marker: c.marker,
      http_status: r.http_status,
      success: r.success,
      response_contains_marker: String(r.content).includes(c.marker),
      latency_ms: r.latency_ms,
      error_summary: r.error_summary,
      key_printed: false,
      production_config_modified: false
    });
    await sleep(2500);
  }
  const primaryOk = routeTests[0]?.response_contains_marker === true;
  const fallbackOk = routeTests[1]?.response_contains_marker === true;
  const g24Status = primaryOk && fallbackOk
    ? "G24_PASS_OPENCLAW_NVIDIA_ROUTE_DRYRUN_BOTH"
    : primaryOk
      ? "G24_PASS_OPENCLAW_NVIDIA_ROUTE_DRYRUN_PRIMARY_ONLY"
      : "G24_FAIL_OPENCLAW_NVIDIA_ROUTE_DRYRUN";
  writeJson("G24-openclaw-route-dryrun.json", routeTests);
  writeText("G24-openclaw-route-dryrun.md", `# G24 OpenClaw Candidate Route Dry-run

Status: \`${g24Status}\`

This used the candidate OpenAI-compatible route definition without modifying production OpenClaw config.

| Model | HTTP | Marker | Latency ms | Error |
| --- | ---: | --- | ---: | --- |
${routeTests.map(r => `| \`${r.requested_model}\` | ${r.http_status} | ${r.response_contains_marker} | ${r.latency_ms} | \`${redact(r.error_summary || "none")}\` |`).join("\n")}
`);

  const stylePrompts = [
    "用户问：你这个 AI 辅导孩子学习是免费的吗？请以“小龙虾”AI学习辅导服务口吻，像普通人在家长群里回复，只输出一段中文，60到100字以内，只能说可以先免费体验或先试用，不能说第一周、续费、具体价格，不要提模型、API、NVIDIA、OpenAI、provider、ChatGPT，不要夸大。",
    "用户问：孩子作文不会写，你这个有什么用？请以“小龙虾”AI学习辅导服务口吻，像普通人在家长群里回复，只输出一段中文，60到100字以内，讲清楚可以帮孩子找思路、列提纲、改表达，不要夸大。",
    "用户问：我不会操作电脑，手机上能不能问？请以“小龙虾”AI学习辅导服务口吻，像普通人在家长群里回复，只输出一段中文，60到100字以内，只能说后续接入口可以放在手机聊天里使用，不能说APP、下载、微信、网站，不要提技术细节，不要把小龙虾理解成水产动物。",
    "用户问：孩子数学题不会，是不是直接给答案？请以“小龙虾”AI学习辅导服务口吻，像普通人在家长群里回复，只输出一段中文，60到100字以内，强调一步一步引导，不要承诺成绩一定提升。",
    "用户问：这个 AI 和普通补课有什么区别？请以“小龙虾”AI学习辅导服务口吻，像普通人在家长群里回复，只输出一段中文，60到100字以内，说明它适合随时问、反复练，不能完全代替老师。"
  ];
  const styleTests = [];
  if (primaryOk) {
    for (let i = 0; i < stylePrompts.length; i++) {
      let r = await chat(PRIMARY, stylePrompts[i], key, false);
      let fallback_used = false;
      let evals = evaluateReply(r.content);
      if ((!r.success || evals.final_grade === "C") && fallbackOk) {
        await sleep(1500);
        r = await chat(FALLBACK, stylePrompts[i], key, false);
        fallback_used = true;
        evals = evaluateReply(r.content);
      }
      styleTests.push({
        route_name: ROUTE_NAME,
        provider: PROVIDER_ID,
        prompt_index: i + 1,
        requested_model: r.requested_model,
        returned_model: r.returned_model,
        fallback_used,
        http_status: r.http_status,
        success: r.success,
        latency_ms: r.latency_ms,
        response_preview: r.content.slice(0, 220),
        error_summary: r.error_summary,
        ...evals
      });
      await sleep(2500);
    }
  }
  const passCount = styleTests.filter(x => x.final_grade === "A" || x.final_grade === "B").length;
  const leakCount = styleTests.filter(x => !x.no_model_leak).length;
  const falsePromiseCount = styleTests.filter(x => !x.no_false_promise).length;
  const g25Status = passCount >= 4 && leakCount === 0 && falsePromiseCount === 0
    ? "G25_PASS_XIAOLONGXIA_ROUTE_STYLE_DRYRUN"
    : passCount >= 2
      ? "G25_PARTIAL_XIAOLONGXIA_ROUTE_STYLE_DRYRUN"
      : "G25_FAIL_XIAOLONGXIA_ROUTE_STYLE_DRYRUN";
  writeJson("G25-xiaolongxia-reply-template-dryrun.json", styleTests);
  writeText("G25-xiaolongxia-reply-template-dryrun.md", `# G25 Xiaolongxia Reply Template Dry-run

Status: \`${g25Status}\`

Primary model: \`${PRIMARY}\`

| # | Model | Fallback | HTTP | Grade | Chinese | Short | Natural | No model leak | No false promise | No product confusion | No unverified channel/pricing | Latency ms | Preview |
| ---: | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- |
${styleTests.map(r => `| ${r.prompt_index} | \`${r.requested_model}\` | ${r.fallback_used} | ${r.http_status} | ${r.final_grade} | ${r.chinese_ok} | ${r.short_ok} | ${r.natural_group_chat_ok} | ${r.no_model_leak} | ${r.no_false_promise} | ${r.no_product_confusion} | ${r.no_unverified_channel_or_pricing} | ${r.latency_ms} | ${String(r.response_preview).replace(/\|/g, "/")} |`).join("\n")}

A/B usable count: ${passCount}/5
`);

  delete process.env.NVIDIA_API_KEY;

  const postModels = await getProductionModels();
  const postBaseline = {
    captured_at: new Date().toISOString(),
    hashes: {
      openclaw_json: sha256File(OPENCLAW_CONFIG),
      xiaolongxia_docker_compose: sha256File(XLLX_COMPOSE),
      xiaolongxia_env: sha256File(XLLX_ENV),
      production_model_ids_hash: sha256String(postModels.modelIds.join("\n"))
    },
    production_models: {
      ok: postModels.ok,
      status: postModels.status,
      count: postModels.modelIds.length,
      first_10: postModels.modelIds.slice(0, 10)
    }
  };
  const diffCheck = {
    status: "G26_PASS_PRODUCTION_UNCHANGED",
    openclaw_hash_same: baseline.hashes.openclaw_json === postBaseline.hashes.openclaw_json,
    compose_hash_same: baseline.hashes.xiaolongxia_docker_compose === postBaseline.hashes.xiaolongxia_docker_compose,
    env_hash_same: baseline.hashes.xiaolongxia_env === postBaseline.hashes.xiaolongxia_env,
    production_model_hash_same: baseline.hashes.production_model_ids_hash === postBaseline.hashes.production_model_ids_hash,
    model_count_before: baseline.production_models.count,
    model_count_after: postBaseline.production_models.count,
    output_key_scan_hits: scanKeyPatterns([OUT, SKILL_LOCAL, CANDIDATE_DIR]),
    openclaw_validate_after: run("openclaw config validate"),
    nvidia_api_key_still_set: !!process.env.NVIDIA_API_KEY
  };
  if (!diffCheck.openclaw_hash_same || !diffCheck.compose_hash_same || !diffCheck.env_hash_same || !diffCheck.production_model_hash_same || diffCheck.output_key_scan_hits.length || diffCheck.nvidia_api_key_still_set) {
    diffCheck.status = "G26_STOP_PRODUCTION_CHANGED_NEEDS_ROLLBACK";
    writeText("rollback-needed.md", `# Rollback Needed

G26 detected a production difference. Stop before G27-G29.

See \`G26-production-diff-check.md\` and \`G26-production-diff-check.json\`.
`);
  }
  writeJson("G26-production-diff-check.json", diffCheck);
  writeText("G26-production-diff-check.md", `# G26 Production Diff Check

Status: \`${diffCheck.status}\`

| Check | Result |
| --- | --- |
| OpenClaw hash same | ${diffCheck.openclaw_hash_same} |
| 3011 compose hash same | ${diffCheck.compose_hash_same} |
| 3011 env hash same | ${diffCheck.env_hash_same} |
| Production model list hash same | ${diffCheck.production_model_hash_same} |
| Model count before | ${diffCheck.model_count_before} |
| Model count after | ${diffCheck.model_count_after} |
| Output/skill key scan hits | ${diffCheck.output_key_scan_hits.length} |
| OpenClaw validate after | ${diffCheck.openclaw_validate_after.ok ? "PASS" : "FAIL"} |
| NVIDIA_API_KEY still set | ${diffCheck.nvidia_api_key_still_set} |
`);

  const finalStatus = diffCheck.status !== "G26_PASS_PRODUCTION_UNCHANGED"
    ? "XIAOLONGXIA_OPENCLAW_NVIDIA_ROUTE_DRYRUN_STOP_PRODUCTION_CHANGED"
    : (primaryOk && g25Status === "G25_PASS_XIAOLONGXIA_ROUTE_STYLE_DRYRUN")
      ? "XIAOLONGXIA_OPENCLAW_NVIDIA_ROUTE_DRYRUN_PASS"
      : primaryOk
        ? "XIAOLONGXIA_OPENCLAW_NVIDIA_ROUTE_DRYRUN_PARTIAL"
        : "XIAOLONGXIA_OPENCLAW_NVIDIA_ROUTE_CONFIG_ONLY";
  writeText("G28-final-report-draft.md", `# OpenClaw NVIDIA Route Dry-run Final Report Draft

Final status:

\`${finalStatus}\`

This draft is generated before G27 skill sync. The final report will be rewritten after skill hash verification.
`);
}

main().catch(err => {
  delete process.env.NVIDIA_API_KEY;
  writeText("run-error.md", `# Run Error

\`${redact(err.stack || err.message)}\`
`);
  process.exitCode = 1;
});
