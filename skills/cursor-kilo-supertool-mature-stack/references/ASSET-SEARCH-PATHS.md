# Asset Search Paths — Complete Maturity Architecture

**Created:** 2026-07-03
**Purpose:** Prevent AI assistant search-scope misjudgments when assessing Cursor+Kilo+OpenRouter SuperTool maturity. This file documents all canonical asset locations so any AI session can perform a complete maturity scan without missing critical layers.

## Architecture Overview: 4-Layer Asset Model

```
Layer 1: Kilo Runtime Config    →  ~/.config/kilo/          +  ~/.kilocode/
Layer 2: Agent Skills Runtime    →  ~/.agents/skills/        +  ~/.codex/skills/
Layer 3: Knowledge Brain Index   →  ~/.codex/knowledge-brain/
Layer 4: Ecosystem Station       →  ~/Desktop/AI_Coding_SuperTool_Ecosystem_Station/
```

**Critical Rule:** A maturity assessment MUST scan ALL FOUR layers. Missing any layer will cause severe underestimation (e.g., 30% instead of 88%).

---

## Layer 1: Kilo Runtime Configuration

### Canonical Paths

| Path | Content | Must Search | Notes |
|---|---|---|---|
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}

### Known Pitfall
`model.json` is the **real** effective state for Code mode, not `kilo.jsonc` or Cursor `globalStorage`. Previous sessions spent hours debugging this.

---

## Layer 2: Agent Skills Runtime

### 2a. `.agents/skills/` — Universal Agent Skills

| Path | Content | Must Search |
|---|---|---|
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}

**Total:** 31 Firecrawl skills + 1 Playwright skill = 32 agent skills, all with valid SKILL.md files.

### 2b. `.codex/skills/` — Codex Skill Runtime

| Path | Content | Must Search |
|---|---|---|
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}

### 2c. `.kilocode/skills/` — KiloCode Skill Registry

| Path | Content | Must Search |
|---|---|---|
${REDACTED_SECRET}
${REDACTED_SECRET}

${REDACTED_SECRET}

---

## Layer 3: Knowledge Brain Index

| Path | Content | Must Search |
|---|---|---|
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}

---

## Layer 4: Ecosystem Station (Desktop)

| Path | Content | Must Search |
|---|---|---|
${REDACTED_SECRET}
| `...\models\model_matrix.json` | Model matrix definition | YES |
| `...\models\model_routing_policy.json` | Model routing policy | YES |
| `...\agents\` | Agent definitions | YES |
| `...\config\` | Configuration files | YES |
| `...\docs\` | Documentation | YES |
| `...\governance\` | Governance rules | YES |
| `...\heavy_library_refs\` | Heavy reference library | YES |
| `...\indexes\` | Index files | YES |
| `...\runtime\` | Runtime files | YES |
| `...\samples\` | Sample files | YES |
| `...\validation\` | Validation rules | YES |
| `...\assets\` | Asset files | YES |
${REDACTED_SECRET}
| `...\continuous_system_verification\final_verdict.txt` | Final deployment verdict | YES |
| `...\continuous_system_verification\system_verification_report.json` | System verification report | YES |
| `...\evidence\openrouter_live_model_smoke_verification.json` | Live smoke evidence | YES |
| `...\reports\OpenRouter_Live_Model_Smoke_Verification_Report.md` | Live smoke report | YES |

---

## Desktop Delivery Packages

| Pattern | Purpose |
|---|---|
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}

**Known packages:** 002.zip (2026-07-03 maturity assessment), 123.zip, 456.zip, 391.zip, 101.zip

---

## Maturity Scan Protocol

When any AI session needs to assess or recover the SuperTool maturity state, it MUST:

1. **Read this file first** to know all paths.
2. **Scan Layer 1** — Check `kilo.jsonc` + `model.json` + `state.vscdb`.
3. **Scan Layer 2** — Check `.agents/skills/` (32 skills) + `.codex/skills/` (85+ skills). Do NOT stop at `.kilocode/skills/` empty dirs.
4. **Scan Layer 3** — Read `skills-index.md` for registered skills.
5. **Scan Layer 4** — Check `Ecosystem_Station/` + `Full_Deploy_Run/` for station state.
6. **Only then** produce a maturity percentage or status.

**Without scanning all 4 layers, any maturity assessment is invalid.**

---

## C-Drive vs K-Drive Rule

From `skills-index.md` (2026-07-01 entry):
${REDACTED_SECRET}
- **K drive** (`K:\AI\skills\`): Backup, history, reports, workspaces, knowledge indexes, restore/reference material
- **H drive**: Does not exist / historical context only

When searching for skills or maturity assets, C drive takes priority. K drive is for backup reference only.

---

## Updated: 2026-07-03

- Created after 2026-07-03 Kilo maturity assessment review
- Root cause: AI session only scanned Layer 1 (`.config/kilo/` + `.kilocode/`) and current workspace, producing 30% maturity score vs actual 88%
- Fix: This file now documents all 4 layers so future sessions cannot make the same scope error