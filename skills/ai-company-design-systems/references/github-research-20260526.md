# GitHub Research 2026-05-26

Source evidence from this run:

${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}

## Verified Candidate Repositories

All listed repositories returned GitHub API metadata and passed `git ls-remote HEAD` on 2026-05-26.

| Repository | Role | License From API |
| --- | --- | --- |
| `shadcn-ui/ui` | Editable component baseline | MIT |
| `vercel/ai-elements` | AI-native UI patterns | NOASSERTION |
| `ant-design/ant-design` | Enterprise UI design language | MIT |
| `carbon-design-system/carbon` | Token and governance reference | Apache-2.0 |
| `tremorlabs/tremor-npm` | Dashboard component patterns | Apache-2.0 |
| `xyflow/xyflow` | Node-based skills/workflow graph | MIT |
| `recharts/recharts` | Metrics and trend charts | MIT |
| `langfuse/langfuse` | AI observability concepts | NOASSERTION |

## Practical Mapping

- Use shadcn-style components when the target is a local React/Tailwind app that should stay editable.
- Use Ant Design and Carbon as references for density, enterprise status semantics, accessibility, tables, forms, and governance.
- Use xyflow-style node graphs for skills, workflows, agents, approvals, and replay dependencies.
- Use Recharts or Tremor-style patterns for small decision metrics.
- Use Langfuse only as an AI observability concept reference: traces, prompts, evals, datasets, metrics, and audit trails.

## Constraints

- Refresh GitHub metadata when current repository status, license, or activity matters.
- Do not copy private products or account-gated UI.
- Do not treat a repository with API `NOASSERTION` license as a source to copy from. Use concepts only unless license is checked manually.
