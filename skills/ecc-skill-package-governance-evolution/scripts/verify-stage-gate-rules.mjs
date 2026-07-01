#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const outDir = path.join(root, "reports", "creation-20260527");
fs.mkdirSync(outDir, { recursive: true });

function read(file) {
  const full = path.join(root, file);
  return fs.existsSync(full) ? fs.readFileSync(full, "utf8") : "";
}

const text = [
  read("SCRIPT-VERIFICATION-RULES.md"),
  read("SKILL.md"),
  read("templates/STAGE-GATE-SCRIPT-VERIFICATION-TEMPLATE.md"),
].join("\n");

const checks = [
  { name: "hard rule secondary verification exists", pass: text.includes("Every hard rule must have secondary verification") || text.includes("Hard rule must be verified") },
  { name: "gate PASS verification exists", pass: text.includes("Every gate PASS requires script or deterministic checklist evidence") || text.includes("Gate PASS requires verification") },
  { name: "deterministic checklist fallback exists", pass: text.includes("deterministic checklist") || text.includes("确定性清单") },
  { name: "stage verification summary exists", pass: text.includes("Stage verification summary required") || text.includes("stage-verification-summary") },
];

const result = {
  script: "verify-stage-gate-rules",
  status: checks.every((check) => check.pass) ? "PASS" : "FAIL",
  checks,
};

fs.writeFileSync(path.join(outDir, "verify-stage-gate-rules.json"), JSON.stringify(result, null, 2));
console.log(JSON.stringify(result, null, 2));
process.exit(result.status === "PASS" ? 0 : 1);
