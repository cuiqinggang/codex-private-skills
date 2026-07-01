#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

const root = process.cwd();
const outDir = path.join(root, "reports", "creation-20260527");
fs.mkdirSync(outDir, { recursive: true });

const scripts = [
  "scripts/verify-required-files.mjs",
  "scripts/verify-context-budget-rules.mjs",
  "scripts/verify-stage-gate-rules.mjs",
];

const runs = scripts.map((script) => {
  const result = spawnSync(process.execPath, [path.join(root, script)], {
    cwd: root,
    encoding: "utf8",
  });
  return {
    script,
    exitCode: result.status,
    stdout: result.stdout,
    stderr: result.stderr,
    pass: result.status === 0,
  };
});

const rootFiles = [
  "SKILL.md",
  "README.md",
  "RUNBOOK.md",
  "SOURCE-OF-TRUTH-MAP.md",
  "CONTEXT-BUDGET-RULES.md",
  "SCRIPT-VERIFICATION-RULES.md",
  "GOVERNANCE-EVOLUTION-METHOD.md",
  "MATURE-REPLAY-METHOD.md",
  "FAILURE-PATTERN-CATALOG.md",
  "GLOSSARY-ZH.md",
  "MANIFEST.md",
];

const templateFiles = [
  "templates/SKILL-GOVERNANCE-PATCH-TEMPLATE.md",
  "templates/SKILL-LOGIC-COMPACTION-TEMPLATE.md",
  "templates/SOURCE-OF-TRUTH-MAP-TEMPLATE.md",
  "templates/CONTEXT-BUDGET-PATCH-TEMPLATE.md",
  "templates/STAGE-GATE-SCRIPT-VERIFICATION-TEMPLATE.md",
  "templates/DECLARED-REQUIREMENT-100-TEMPLATE.md",
  "templates/ARTIFACT-CHECKPOINT-CLOSURE-TEMPLATE.md",
  "templates/FINAL-REPORT-TEMPLATE.md",
  "templates/COMPLETION-LEDGER-TEMPLATE.md",
];

const checks = [
  { name: "all child scripts pass", pass: runs.every((run) => run.pass) },
  { name: "all root files exist", pass: rootFiles.every((file) => fs.existsSync(path.join(root, file))) },
  { name: "all templates exist", pass: templateFiles.every((file) => fs.existsSync(path.join(root, file))) },
  { name: "scripts directory exists", pass: fs.existsSync(path.join(root, "scripts")) },
  { name: "reports creation directory exists", pass: fs.existsSync(outDir) },
];

const result = {
  script: "verify-governance-skill",
  status: checks.every((check) => check.pass) ? "PASS" : "FAIL",
  checks,
  runs,
};

fs.writeFileSync(path.join(outDir, "verify-governance-skill.json"), JSON.stringify(result, null, 2));
console.log(JSON.stringify(result, null, 2));
process.exit(result.status === "PASS" ? 0 : 1);
