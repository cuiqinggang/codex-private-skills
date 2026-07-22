#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const skillDir = path.resolve(path.dirname(__filename), "..");
const skillPath = path.join(skillDir, "SKILL.md");
const guidePath = path.join(
  skillDir,
  "references",
  "CLAUDE-STYLE-12-LAYER-DETAILED-CHINESE-GUIDE.md"
);
const openaiYamlPath = path.join(skillDir, "agents", "openai.yaml");

function readText(filePath) {
  return fs.existsSync(filePath) ? fs.readFileSync(filePath, "utf8") : "";
}

const skill = readText(skillPath);
const guide = readText(guidePath);
const openaiYaml = readText(openaiYamlPath);

const expectedLayers = [
  "Layer 1 — Control Plane / Orchestrator",
  "Layer 2 — Short Entry / Memory",
  "Layer 3 — Skills / Progressive Disclosure",
  "Layer 4 — Planning / Work Decomposition",
  "Layer 5 — Subagents / Context Isolation",
  "Layer 6 — Execution Plane",
  "Layer 7 — Hooks / Lifecycle Triggers",
  "Layer 8 — Scripts / Deterministic Checks",
  "Layer 9 — Verification Plane",
  "Layer 10 — Repair Loop",
  "Layer 11 — Compact / Handoff",
  "Layer 12 — Final Acceptance",
];

const requiredGuidePhrases = [
  "这不是普通 12 步，而是 12 个控制层",
  "前 5 层：防止乱开始",
  "Execution Plane 只能 claim，不能 self-accept",
  "Verification Plane 负责 acceptance / rejection",
  "rejected claim 必须返修",
  "没有 final-acceptance.md / json，就没有最终 PASS",
  "每一层必须按以下格式写",
  "Verification Plane 是否接受 no-op / exception",
  "把 12 Layer 改成普通 12 步",
  "CLAUDE_STYLE_12_LAYER_EFFECTIVE_CORE_LOGIC_EXPANDED",
];

const requiredTemplateFields = [
  "本层目的：",
  "本层输入：",
  "本层动作：",
  "本层产物：",
  "本层验证：",
  "失败返回：",
  "证据路径：",
  "是否允许跳过：",
  "本任务中的具体应用：",
];

const errors = [];

if (!skill.includes("name: complete-claude-style-replica-flow")) {
  errors.push("SKILL.md frontmatter name is missing or wrong.");
}
if (skill.includes("TODO")) {
  errors.push("SKILL.md still contains TODO placeholders.");
}
if (!skill.includes("references/CLAUDE-STYLE-12-LAYER-DETAILED-CHINESE-GUIDE.md")) {
  errors.push("SKILL.md does not point to the detailed guide.");
}
if (!skill.includes("不要把 12 Layer 改写成普通 12 步")) {
  errors.push("SKILL.md does not preserve the anti-rewrite rule.");
}
if (!openaiYaml.includes("完整 Claude-style 复刻流程")) {
  errors.push("agents/openai.yaml display name is missing.");
}
if (!guide) {
  errors.push("Detailed Chinese guide is missing.");
} else {
  for (const layer of expectedLayers) {
    if (!guide.includes(layer)) {
      errors.push(`Detailed guide missing exact layer heading: ${layer}`);
    }
  }
  for (const phrase of requiredGuidePhrases) {
    if (!guide.includes(phrase)) {
      errors.push(`Detailed guide missing required phrase: ${phrase}`);
    }
  }
  for (const field of requiredTemplateFields) {
    if (!guide.includes(field)) {
      errors.push(`Detailed guide missing task-package field: ${field}`);
    }
  }
  if (!guide.includes("官方支撑点") || !guide.includes("https://code.claude.com/docs/en/skills")) {
    errors.push("Detailed guide missing official-source support notes.");
  }
}

const result = {
  skillDir,
  checkedFiles: [
    path.relative(skillDir, skillPath),
    path.relative(skillDir, guidePath),
    path.relative(skillDir, openaiYamlPath),
  ],
  expectedLayerCount: expectedLayers.length,
  errors,
  pass: errors.length === 0,
};

console.log(JSON.stringify(result, null, 2));
process.exit(result.pass ? 0 : 1);
