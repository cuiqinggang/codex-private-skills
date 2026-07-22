---
name: frontend-production-router
description: Use when Codex must route a frontend task among an existing website-clone skill and ui-design-system-router, including URL clone, screenshot-to-page, new product UI, clone-and-originalize, redesign, multi-page extension, or final visual quality review. Triggers include 前端生产编排、网站克隆、截图还原、参考网站但不要照抄、DESIGN.md、多页面一致性和视觉验收。
---

# Frontend Production Router

Keep the clone layer, design-system layer, and orchestration/acceptance layer independent.

## Start workflow

1. Run `scripts/verify_skill_availability.py`.
2. Classify the request with `scripts/detect_task_type.py`.
3. Read the selected workflow in `workflows/` and `ROUTING_RULES.md`.
4. Invoke only the required existing skill(s); never copy their implementation into this skill.
5. Exchange artifacts through `INTEGRATION_CONTRACT.md`.
6. Validate the handoff with `scripts/validate_handoff.py`.
7. Require source/prototype desktop and mobile evidence for visual-fidelity claims.
8. Record success in `RECENT_USE_LOG.md` and failures in `FAILURE_REVIEW.md`.

## Stable capability owners

- `indie-site-reference-factory`: URL/reference-site analysis, compliant Next.js/React/Tailwind reconstruction, stage-gated screenshots, and similarity evidence.
- `ui-design-system-router`: original project-level `DESIGN.md`, design tokens, responsiveness, accessibility, commercial safety, and long-term consistency.
- `frontend-production-router`: task classification, sequencing, artifact transfer, cycle prevention, and final acceptance.

## Hard rules

- Do not modify, rename, delete, or embed either stable skill.
- Do not route a written new-product brief to clone-only execution.
- Do not route exact clone requests through originalization unless the user asks for a derivative design.
- Never claim 80-90% or higher similarity without matched-view screenshot evidence and scoring logic.
- Never copy logos, trademarks, proprietary fonts/assets, or source copy into an original product.
- Stop on missing skill, incompatible contract version, missing required artifact, circular call, or duplicate page generation.

