#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const outDir = path.join(root, "reports", "creation-20260527");
fs.mkdirSync(outDir, { recursive: true });

const required = [
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

const checks = required.map((file) => ({
  file,
  exists: fs.existsSync(path.join(root, file)),
}));

const result = {
  script: "verify-required-files",
  status: checks.every((check) => check.exists) ? "PASS" : "FAIL",
  checks,
};

fs.writeFileSync(path.join(outDir, "verify-required-files.json"), JSON.stringify(result, null, 2));
console.log(JSON.stringify(result, null, 2));
process.exit(result.status === "PASS" ? 0 : 1);
