---
name: codex-app-plugin-workflow-orchestrator
description: Use when a Codex task needs to route Product Design, Figma/design input, web app building, browser validation, GitHub, Supabase/backend planning, deployment, or agentic delivery workflow into a safe, reviewable, visually verified project flow.
---

# Codex App Plugin Workflow Orchestrator

## Purpose

This skill turns Codex App plugins, skills, MCP tools, browser validation, GitHub, Figma/design inputs, database planning, deployment checks, and visual proof into a reviewable development workflow.

It is not a plugin shopping list. It is a routing layer for deciding which capability to use, when to use it, and what needs user authorization.

## Trigger Scenarios

Consider this skill when the user asks Codex to:

1. Build a Web App, page, dashboard, control panel, or console.
2. Recreate HTML, CSS, or React from a screenshot, image, prototype, or Figma file.
3. Generate a clickable acceptance page for AI Company Knowledge OS.
4. Validate frontend UI, visual fidelity, browser behavior, or mobile responsiveness.
5. Plan product design, user paths, screen structure, or feature modules.
6. Work with GitHub issues, pull requests, code review, or bug triage.
7. Draft Supabase, Postgres, API, auth, RLS, or schema plans.
8. Prepare Vercel, Netlify, or local deployment verification.
9. Run planning, TDD, debugging, or delivery closure.

## Capability Layers

L1 Product Thinking:
- Product Design
- requirement breakdown
- user journey
- page modules
- prototype review

L2 Design-to-Code:
- Figma
- screenshots, images, and design restoration
- UI structure recognition
- HTML, CSS, React implementation

L3 App Building:
- Build Web Apps
- Build iOS Apps
- Expo, SwiftUI, React, Vite route selection

L4 Runtime Validation:
- Chrome
- Browser testing
- screenshot validation
- console log check
- mobile viewport check

L5 Data and Backend:
- Supabase
- Postgres
- API
- Auth, RLS, schema, SQL

L6 Delivery and Collaboration:
- GitHub
- PR
- issue
- code review
- Vercel deployment

L7 Agentic Workflow:
- planning
- TDD
- debugging
- delivery workflow
- final acceptance

## User Project Rules

The user's current acceptance preference is strict:

Any Codex stage result must not only provide a path, text report, or file list. Prefer a browser-openable acceptance page, screenshot evidence page, diagram page, contact sheet, or other visual proof.

Before claiming completion for UI, dashboard, document, or workflow artifacts, check the user's visual acceptance skill when relevant:

`C:\Users\A\.codex\skills\visual-proof-acceptance`

## Safety Rules

1. Do not blindly install every plugin mentioned in a video or tutorial.
2. Do not assume current Codex App plugin names, permissions, or marketplace availability match the source material.
3. Start with local files and read-only checks.
4. For GitHub, Supabase, Vercel, Figma, or any account-backed service, request explicit user authorization before write actions, deployment, database mutation, or token use.
5. Produce visual proof or a clickable acceptance page for important deliverables.

## Next-Run Reuse Instruction

When a future task resembles web app creation, design-to-code, AI Company dashboards, browser validation, GitHub workflow, backend planning, or deployment, first read:

- `PLUGIN-WORKFLOW-MATRIX.md`
- `PROJECT-ROUTING-RULES.md`
- `SAFE-INSTALL-AND-CAPABILITY-CHECK.md`
- `VISUAL-PROOF-WORKFLOW.md`
