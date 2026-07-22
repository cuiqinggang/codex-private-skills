# GPT-Codex Loop

## Codex-First Rule

Formal complex tasks start in Codex. Codex gathers:

- user goal and true intent,
- relevant local files,
- existing skills,
- prior handoff or replay evidence,
- public mature references,
- available tools,
- risks and stop conditions,
- proposed task level,
- proposed gates and verification points.

GPT receives a prepared intelligence brief. GPT should not plan from thin air when Codex can collect the missing evidence.

## Gate Review Protocol

Each gate moves through:

```text
Codex evidence + claim
  -> GPT accepted / rejected / needs_more_info
  -> Codex proceeds / repairs / collects more evidence
```

## Codex Must Submit

- gate id,
- task id,
- current level,
- what was done,
- evidence paths,
- verification results,
- open issues,
- risk changes,
- exact Codex claim,
- requested GPT decision.

## GPT Must Decide

GPT returns one of:

- `accepted`
- `rejected`
- `needs_more_info`
- `stop_and_ask_user`

For rejection, GPT must provide a repair command package with allowed scope, forbidden scope, required evidence, verification command/checklist, and stop conditions.

## No Self-Acceptance

Codex may self-check. Codex may not final-accept L4-L5 tasks without independent review and final acceptance artifacts.
