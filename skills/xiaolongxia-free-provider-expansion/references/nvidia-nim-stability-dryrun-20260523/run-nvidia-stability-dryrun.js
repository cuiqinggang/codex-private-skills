const fs = require("fs");
const path = require("path");

const out = "C:/Users/A/Desktop/1/output/XIAOLONGXIA-NVIDIA-NIM-STABILITY-DRYRUN-20260523";
fs.mkdirSync(out, { recursive: true });

const key = process.env.NVIDIA_API_KEY;
if (!key) {
  throw new Error("NVIDIA_API_KEY is required in the current process.");
}

const endpoint = "https://integrate.api.nvidia.com/v1/chat/completions";
const models = [
  { id: "meta/llama-3.1-8b-instruct", label: "llama31_8b" },
  { id: "nvidia/nemotron-3-super-120b-a12b", label: "nemotron_super" },
  { id: "meta/llama-3.1-70b-instruct", label: "llama31_70b" },
];

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function redact(value) {
  return String(value || "")
    .replace(/nvapi-[A-Za-z0-9_-]+/g, "nvapi-***")
    .replace(/sk-[A-Za-z0-9_-]{8,}/g, "sk-***");
}

async function callModel(model, messages, maxTokens = 120) {
  const body = {
    model,
    messages,
    temperature: 0,
    max_tokens: maxTokens,
    stream: false,
  };
  const timestamp = new Date().toISOString();
  const start = Date.now();
  let httpStatus = null;
  let success = false;
  let text = "";
  let returnedModel = "";
  let errorType = "none";
  let errorSummary = "";

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${key}`,
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(body),
      signal: AbortSignal.timeout(120000),
    });
    httpStatus = response.status;
    const raw = await response.text();
    if (!response.ok) {
      errorType = `http_${response.status}`;
      errorSummary = redact(raw).slice(0, 360);
    } else {
      const json = JSON.parse(raw);
      returnedModel = json.model || model;
      text = json.choices?.[0]?.message?.content || "";
      success = true;
    }
  } catch (error) {
    errorType = error.name || "request_error";
    errorSummary = redact(error.message || String(error)).slice(0, 360);
  }

  return {
    requested_model: model,
    returned_model: returnedModel,
    http_status: httpStatus,
    success,
    latency_ms: Date.now() - start,
    error_type: errorType,
    error_summary: errorSummary,
    timestamp,
    text,
  };
}

function hasChinese(value) {
  return /[\u4e00-\u9fff]/.test(String(value || ""));
}

function noGarbled(value) {
  const text = String(value || "");
  return !(text.includes("\uFFFD") || /\?{4,}/.test(text) || text.includes("乱码"));
}

function compactLength(value) {
  return Array.from(String(value || "").replace(/\s+/g, "")).length;
}

function noLongEnglish(value) {
  return !/[A-Za-z]{4,}/.test(String(value || ""));
}

function noModelLeak(value) {
  return !/(API|provider|model|ChatGPT|OpenAI|NVIDIA|NIM|llama|nemotron)/i.test(String(value || ""));
}

function noFalsePromise(value) {
  const text = String(value || "");
  return !["一定", "保证", "肯定", "包提高", "立刻提高", "100%"].some((word) => text.includes(word));
}

function containsAny(value, words) {
  const text = String(value || "");
  return words.some((word) => text.includes(word));
}

function grade(score) {
  if (score >= 5) return "A";
  if (score >= 3) return "B";
  return "C";
}

function average(rows, prop) {
  const values = rows.map((row) => row[prop]).filter((value) => typeof value === "number");
  return values.length ? Math.round(values.reduce((sum, value) => sum + value, 0) / values.length) : null;
}

async function main() {
  fs.writeFileSync(
    path.join(out, "G14-precheck.md"),
    [
      "# G14 Precheck",
      "",
      "Status: `G14_PASS_PRECHECK_READY_USER_ALLOWED_TEMP_KEY`",
      "",
      "The previous key was exposed in chat, but the user explicitly instructed to continue using it for this dry-run and not rotate now.",
      "The key is used only in process memory and is not written to files.",
      "",
      "Production OpenClaw/OpenRouter config remains unchanged.",
      "",
    ].join("\n"),
    "utf8",
  );

  const g15 = [];
  const rounds = [
    ["ROUND1", "NVIDIA_STABILITY_R1_OK"],
    ["ROUND2", "NVIDIA_STABILITY_R2_OK"],
    ["ROUND3", "NVIDIA_STABILITY_R3_OK"],
  ];

  for (const model of models) {
    for (const [round, marker] of rounds) {
      const result = await callModel(
        model.id,
        [{ role: "user", content: `Return exactly this marker and nothing else: ${marker}` }],
        100,
      );
      const markerPass = (result.text || "").includes(marker);
      g15.push({
        ...result,
        provider: "nvidia",
        round,
        marker,
        response_contains_marker: markerPass,
        no_key_leak: !/nvapi-[A-Za-z0-9_-]{20,}/.test(JSON.stringify(result)),
      });
      await sleep(3000);
    }
  }

  fs.writeFileSync(path.join(out, "G15-stability-marker-tests.json"), JSON.stringify(g15, null, 2), "utf8");
  const g15Lines = [
    "# G15 Stability Marker Tests",
    "",
    "| Model | Round | HTTP | Success | Marker | Latency ms | Error |",
    "| --- | --- | ---: | --- | --- | ---: | --- |",
  ];
  for (const row of g15) {
    g15Lines.push(`| \`${row.requested_model}\` | ${row.round} | ${row.http_status ?? ""} | ${row.success} | ${row.response_contains_marker} | ${row.latency_ms} | \`${row.error_type}\` |`);
  }
  const g15ByModel = Object.fromEntries(models.map((model) => [model.id, g15.filter((row) => row.requested_model === model.id)]));
  const g15PassModels = Object.entries(g15ByModel)
    .filter(([, rows]) => rows.filter((row) => row.response_contains_marker).length >= 2
      && !rows.some((row) => [401, 403, 404].includes(row.http_status))
      && !rows.some((row, index) => row.http_status === 429 && rows[index - 1]?.http_status === 429))
    .map(([id]) => id);
  const g15Status = g15PassModels.length === 3
    ? "G15_PASS_STABILITY_TESTS"
    : g15PassModels.length > 0
      ? "G15_PARTIAL_STABILITY_TESTS"
      : "G15_FAIL_STABILITY_TESTS";
  g15Lines.push("", `Status: \`${g15Status}\``);
  fs.writeFileSync(path.join(out, "G15-stability-marker-tests.md"), `${g15Lines.join("\n")}\n`, "utf8");

  const qaPrompts = [
    "小学四年级孩子不会写作文，家长很着急，你用三句话给家长一个简单办法。要求：中文回复，不超过120字，口语化，不要长篇解释，不要自称大型语言模型，不要输出英文，不要乱码，不要空泛营销。",
    "有人在群里问：你这个 AI 辅导孩子学习到底有什么用？请用普通人能听懂的话回答，不要超过 80 字。要求：中文回复，口语化，不要自称大型语言模型，不要输出英文。",
    "孩子数学应用题不会做，AI 应该直接给答案，还是一步一步引导？请简短回答。要求：中文回复，不超过120字，口语化，不要输出英文。",
  ];
  const g16 = [];
  for (const model of models) {
    for (let index = 0; index < qaPrompts.length; index += 1) {
      const result = await callModel(model.id, [{ role: "user", content: qaPrompts[index] }], 160);
      const text = result.text || "";
      const fields = {
        chinese_ok: hasChinese(text) && noLongEnglish(text),
        concise_ok: compactLength(text) <= 120,
        useful_ok: containsAny(text, ["办法", "先", "每天", "引导", "讲", "练", "作文", "答案", "步骤", "思路", "改", "问"]),
        no_garbled_text: noGarbled(text),
        no_overlong_answer: compactLength(text) <= 120,
        suitable_for_group_chat: hasChinese(text) && compactLength(text) <= 120 && noGarbled(text) && !text.includes("作为一个") && !text.includes("大型语言模型"),
      };
      const score = Object.values(fields).filter(Boolean).length;
      g16.push({
        ...result,
        provider: "nvidia",
        question_index: index + 1,
        prompt: qaPrompts[index],
        ...fields,
        final_grade: grade(score),
        response_preview: text.slice(0, 220),
      });
      await sleep(3000);
    }
  }
  fs.writeFileSync(path.join(out, "G16-chinese-qa-dryrun.json"), JSON.stringify(g16, null, 2), "utf8");
  const g16Lines = [
    "# G16 Chinese QA Dry-run",
    "",
    "| Model | Q | HTTP | Chinese | Concise | Useful | No garbled | Group suitable | Latency ms | Grade | Preview |",
    "| --- | ---: | ---: | --- | --- | --- | --- | --- | ---: | --- | --- |",
  ];
  for (const row of g16) {
    const preview = String(row.response_preview).replace(/\|/g, "/").replace(/\s+/g, " ");
    g16Lines.push(`| \`${row.requested_model}\` | ${row.question_index} | ${row.http_status ?? ""} | ${row.chinese_ok} | ${row.concise_ok} | ${row.useful_ok} | ${row.no_garbled_text} | ${row.suitable_for_group_chat} | ${row.latency_ms} | ${row.final_grade} | ${preview} |`);
  }
  const g16ByModel = Object.fromEntries(models.map((model) => [model.id, g16.filter((row) => row.requested_model === model.id)]));
  const g16PassModels = Object.entries(g16ByModel)
    .filter(([, rows]) => rows.filter((row) => ["A", "B"].includes(row.final_grade)).length >= 2)
    .map(([id]) => id);
  const g16Status = g16PassModels.length === 3
    ? "G16_PASS_CHINESE_QA"
    : g16PassModels.length > 0
      ? "G16_PARTIAL_CHINESE_QA"
      : "G16_FAIL_CHINESE_QA";
  g16Lines.push("", `Status: \`${g16Status}\``);
  fs.writeFileSync(path.join(out, "G16-chinese-qa-dryrun.md"), `${g16Lines.join("\n")}\n`, "utf8");

  const stylePrompts = [
    "用户问：“你这个 AI 辅导是免费的吗？”请像真人在家长群里简短回答，60到100字以内，突出可以先免费体验。不要太官方，不要提 API、模型、provider，不要自称 ChatGPT。",
    "用户问：“孩子成绩差，AI 真有用吗？”请像真人在家长群里简短回答，60到100字以内，不夸大，不承诺成绩一定提升，强调讲题、改作文、陪练。不要提 API、模型、provider。",
    "用户问：“我不会用电脑，能不能用手机问？”请像真人在家长群里简短回答，60到100字以内，说明可以用手机，降低门槛。不要提 API、模型、provider。",
  ];
  const g17 = [];
  for (const model of models) {
    for (let index = 0; index < stylePrompts.length; index += 1) {
      const result = await callModel(model.id, [{ role: "user", content: stylePrompts[index] }], 160);
      const text = result.text || "";
      const len = compactLength(text);
      const fields = {
        natural_chat_style: hasChinese(text) && containsAny(text, ["可以", "先", "不用", "别", "家长", "孩子", "手机", "试", "问", "讲", "练"]) && !containsAny(text, ["尊敬", "用户", "您好，感谢"]),
        short_reply_ok: len >= 40 && len <= 120,
        no_false_promise: noFalsePromise(text),
        no_model_leak: noModelLeak(text),
        suitable_for_parent_group: hasChinese(text) && noGarbled(text) && noFalsePromise(text) && noModelLeak(text) && len <= 120,
      };
      const score = Object.values(fields).filter(Boolean).length;
      g17.push({
        ...result,
        provider: "nvidia",
        scenario_index: index + 1,
        prompt: stylePrompts[index],
        ...fields,
        final_grade: grade(score),
        response_preview: text.slice(0, 220),
      });
      await sleep(3000);
    }
  }
  fs.writeFileSync(path.join(out, "G17-xiaolongxia-style-dryrun.json"), JSON.stringify(g17, null, 2), "utf8");
  const g17Lines = [
    "# G17 Xiaolongxia-style Short Reply Dry-run",
    "",
    "| Model | S | HTTP | Natural | Short | No false promise | No model leak | Parent group | Latency ms | Grade | Preview |",
    "| --- | ---: | ---: | --- | --- | --- | --- | --- | ---: | --- | --- |",
  ];
  for (const row of g17) {
    const preview = String(row.response_preview).replace(/\|/g, "/").replace(/\s+/g, " ");
    g17Lines.push(`| \`${row.requested_model}\` | ${row.scenario_index} | ${row.http_status ?? ""} | ${row.natural_chat_style} | ${row.short_reply_ok} | ${row.no_false_promise} | ${row.no_model_leak} | ${row.suitable_for_parent_group} | ${row.latency_ms} | ${row.final_grade} | ${preview} |`);
  }
  const g17ByModel = Object.fromEntries(models.map((model) => [model.id, g17.filter((row) => row.requested_model === model.id)]));
  const g17PassModels = Object.entries(g17ByModel)
    .filter(([, rows]) => rows.filter((row) => ["A", "B"].includes(row.final_grade)).length >= 2)
    .map(([id]) => id);
  const g17Status = g17PassModels.length === 3
    ? "G17_PASS_XIAOLONGXIA_STYLE"
    : g17PassModels.length > 0
      ? "G17_PARTIAL_XIAOLONGXIA_STYLE"
      : "G17_FAIL_XIAOLONGXIA_STYLE";
  g17Lines.push("", `Status: \`${g17Status}\``);
  fs.writeFileSync(path.join(out, "G17-xiaolongxia-style-dryrun.md"), `${g17Lines.join("\n")}\n`, "utf8");

  const summary = [];
  for (const model of models) {
    const markerRows = g15ByModel[model.id];
    const qaRows = g16ByModel[model.id];
    const styleRows = g17ByModel[model.id];
    const markerPass = markerRows.filter((row) => row.response_contains_marker).length;
    const qaAB = qaRows.filter((row) => ["A", "B"].includes(row.final_grade)).length;
    const styleAB = styleRows.filter((row) => ["A", "B"].includes(row.final_grade)).length;
    const avgLatency = average([...markerRows, ...qaRows, ...styleRows], "latency_ms");
    let tier = "C";
    if (markerPass >= 2 && qaAB >= 2 && styleAB >= 2 && avgLatency < 15000) tier = "A+";
    else if (markerPass >= 2 && qaAB >= 2 && styleAB >= 2) tier = "A";
    else if (markerPass >= 2 && (qaAB >= 1 || styleAB >= 1)) tier = "B";
    summary.push({
      model: model.id,
      marker_pass: `${markerPass}/3`,
      chinese_ab: `${qaAB}/3`,
      style_ab: `${styleAB}/3`,
      avg_latency_ms: avgLatency,
      tier,
    });
  }
  fs.writeFileSync(path.join(out, "G18-nvidia-final-dryrun-ranking.json"), JSON.stringify(summary, null, 2), "utf8");
  const primary = summary.find((row) => row.tier === "A+") || summary.find((row) => row.tier === "A") || summary.find((row) => row.tier === "B");
  const backups = summary.filter((row) => row.model !== primary?.model && ["A+", "A", "B"].includes(row.tier));
  const g18Lines = [
    "# G18 NVIDIA Final Dry-run Ranking",
    "",
    "| Model | Marker | Chinese A/B | Style A/B | Avg latency ms | Tier |",
    "| --- | --- | --- | --- | ---: | --- |",
  ];
  for (const row of summary) {
    g18Lines.push(`| \`${row.model}\` | ${row.marker_pass} | ${row.chinese_ab} | ${row.style_ab} | ${row.avg_latency_ms} | ${row.tier} |`);
  }
  g18Lines.push("");
  g18Lines.push(`Recommended next OpenClaw dry-run primary: \`${primary?.model || "none"}\`.`);
  g18Lines.push(`Recommended backups: ${backups.length ? backups.map((row) => `\`${row.model}\``).join(", ") : "none"}.`);
  g18Lines.push(`Not recommended: ${summary.filter((row) => row.tier === "C").map((row) => `\`${row.model}\``).join(", ") || "none"}.`);
  g18Lines.push("");
  g18Lines.push("Can enter OpenClaw candidate route dry-run: YES, if still not connected to real group chat.");
  g18Lines.push("Still not allowed: direct real group chat production use.");
  fs.writeFileSync(path.join(out, "G18-nvidia-final-dryrun-ranking.md"), `${g18Lines.join("\n")}\n`, "utf8");

  console.log(JSON.stringify({
    g15Status,
    g16Status,
    g17Status,
    summary,
    primary: primary?.model,
    backups: backups.map((row) => row.model),
  }, null, 2));
}

main().catch((error) => {
  console.error(red(error.stack || error.message || String(error)));
  process.exit(1);
});
