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
  read("CONTEXT-BUDGET-RULES.md"),
  read("README.md"),
  read("RUNBOOK.md"),
  read("SKILL.md"),
].join("\n");

const checks = [
  { name: "no default reports full-read rule exists", pass: text.includes("Do not default-read `reports/**`") || text.includes("Do not full-read reports by default") },
  { name: "progressive disclosure rule exists", pass: text.includes("Progressive Disclosure") || text.includes("渐进加载") },
  { name: "reports archive rule exists", pass: text.includes("Reports Archive") || text.includes("报告归档") },
  { name: "short entry rule exists", pass: text.includes("Short Entry File") || text.includes("短入口") },
];

const result = {
  script: "verify-context-budget-rules",
  status: checks.every((check) => check.pass) ? "PASS" : "FAIL",
  checks,
};

fs.writeFileSync(path.join(outDir, "verify-context-budget-rules.json"), JSON.stringify(result, null, 2));
console.log(JSON.stringify(result, null, 2));
process.exit(result.status === "PASS" ? 0 : 1);
