# SOP: Claude Code Cursor Predeploy

## Phase 1: Existing Stack Information Collection

Task ID:

`CLAUDE_CODE_CURSOR_EXISTING_STACK_INFO_COLLECTION_V1`

Collect:

- Cursor status and work directory.
- Terminal type and Git Bash/WSL availability.
- Whether `claude`, `ccr`, `node`, `npm`, and `git` are available.
- Claude Code version, path, and basic text response.
- Provider environment variable presence and model names without secrets.
- Legacy proxy remnants and port `15721`.
- Output folder and file-input helper status.
- `.claude` and `.claude-code-router` structure.
- Codex/Hermes/GPT collaboration touchpoints.

Output:

${REDACTED_SECRET}

## Phase 2: Blocker Analysis

Task ID:

`CLAUDE_CODE_CURSOR_SUPER_TOOL_BLOCKER_ANALYSIS_V1`

Classify blockers as:

- Environment
- Protocol/tool-use
- Model
- Ecosystem
- User experience
- External collaboration

Each blocker must include:

- Severity
- Whether it blocks long deployment
- Whether it can be removed before deployment
- Suggested fix
- User input required
- Automation possibility
- Timeout/recovery strategy

Output:

${REDACTED_SECRET}

## Phase 3: Predeploy Blocker Elimination

Task ID:

`CLAUDE_CODE_CURSOR_PRE_DEPLOY_BLOCKER_ELIMINATION_V1`

Handle only blockers that are safe and scoped. Before writes:

- Back up `.claude`.
- Back up `.claude-code-router`.
- Back up PowerShell profile.
- Capture environment variable summary without secrets.
- Back up existing `ClaudeCode_Outputs`.

Output:

${REDACTED_SECRET}

## Phase 4: Formal Long Deployment

Task ID:

`CLAUDE_CODE_CURSOR_SUPER_TOOL_ONE_PASS_LONG_DEPLOYMENT_V1`

Enter this phase only after Phase 1-3 are complete or explicitly waived with a documented reason.

Target shape:

`Cursor + Git Bash + Claude Code + CCR + multi-model routing + skills + hooks + subagents + reports + evidence + rollback`
