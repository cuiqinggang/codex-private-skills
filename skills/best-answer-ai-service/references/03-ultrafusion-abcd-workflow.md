# UltraFusion A/B/C/D Workflow

## Core Definition

UltraFusion is a workflow, not just a model ensemble.

All A/B/C/D layers are extreme layers. There is no ordinary draft layer.

```text
A = independent extreme drafts
B = cross-absorption extreme drafts
C = dense fusion extreme draft
D = final stress-tested extreme answer
```

V15 is the hard quality standard. In formal testing, V15 must be included in each invocation according to the current V15 rule.

## A Layer: Independent Extreme Drafts

Purpose:

- make each model independently produce its strongest answer;
- maximize useful diversity;
- avoid early convergence.

Inputs:

- user question;
- full V15 prompt;
- A-layer instructions;
- no other model outputs.

Outputs:

- A_GPT;
- A_DeepSeek;
- A_GLM or other selected model;
- A_Kimi/MiniMax/Gemini/Grok/etc. depending on availability.

Rule:

```text
No model should see another A draft during A.
```

## B Layer: Cross-Absorption Extreme Drafts

Purpose:

- each model reads all A drafts;
- each model absorbs strengths, finds omissions, rejects weak points, and writes a stronger version;
- preserve diversity while becoming more complete.

Inputs:

- user question;
- full V15 prompt;
- all A drafts;
- B-layer instructions.

Outputs:

- B1/B2/B3/B4 extreme drafts.

Rule:

```text
B is not a summary layer. It is a second extreme generation after collision.
```

## Optional B1/B2 Split

When extra control is needed, split B:

```text
B1 = cross-absorption and critique
B2 = second-round extreme rewrite
```

This keeps the process more auditable.

## C Layer: Dense Fusion Extreme Draft

Purpose:

- fuse all B drafts;
- remove duplication;
- keep strongest reasoning;
- mark assumptions and evidence types;
- build a more structured, denser answer.

Inputs:

- user question;
- full V15 prompt;
- all B drafts.

Output:

```text
C_Fusion
```

Rule:

```text
C should not blindly average models. It should select, reject, compress, and strengthen.
```

## D Layer: Final Stress-Tested Answer

Purpose:

- treat C_Fusion as an unknown candidate;
- extract atomic claims;
- check facts, assumptions, and logic;
- build strongest counterexamples;
- close reasoning gaps;
- produce final answer.

Output:

```text
Ultra_Answer_Final
```

D must be conservative, stable, and evidence-aware.

## Product Mapping

Hide process complexity from normal users.

User-facing modes:

| User mode | Internal workflow |
|---|---|
| Quick Answer | D-Lite / single lightweight enhanced path |
| Deep Answer | partial multi-step route |
| Best Answer | Full A/B/C/D UltraFusion |

## Key Product Insight

The user buys the final answer, not the visible process.

Show enough process evidence to build trust, but keep the main interface simple.
