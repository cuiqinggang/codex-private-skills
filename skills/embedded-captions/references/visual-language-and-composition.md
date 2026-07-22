## The DNA registry — ten visual languages (replaces the template catalog)

Both modes draw from **[dna/](dna/README.md)** — ten art-directed visual languages that
**parameterize per scene** (accent sampled from the footage, contact shadow along the
measured light direction, depth-match blur, RMS-coupled hero amplitude):

| DNA             | Register       | Scene fit                                       | Voice                                                                                              |
| --------------- | -------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **cream**       | premium-warm   | dark/mid warm scenes                            | Inter + warm cream + screen; glowing emergence hero (successor of cinematic-cream)                 |
| **ink**         | premium        | **bright scenes (luma > 150)**                  | near-black multiply — type printed ON the wall; the bright-scene answer                            |
| **editorial**   | editorial-luxe | introspective / fashion / poetic                | Bodoni Moda, lowercase-italic hero — magazine elegance                                             |
| **keynote**     | tech-premium   | product / launch                                | opaque white Inter 800, dead-center stillness                                                      |
| **documentary** | formal         | interview / serious                             | burn-in reveals, no hero — gravitas IS the style                                                   |
| **loud**        | loud           | hype / sport / social                           | Anton + scene-sampled accent, single-unit slam + ripple; body ANNOUNCES in front (`bodyLayer: fg`) |
| **neon**        | loud-cyber     | cyberpunk / nightlife / tech-noir (dark scenes) | electric-cyan signage, ignition flicker, the hero powers ON like a sign                            |
| **glitch**      | loud-cyber     | digital / hacker / AI                           | RGB-split echoes snap together on landing; machine-percussive timing                               |
| **chrome**      | loud-luxe      | Y2K / fashion-tech / music                      | liquid-metal gradient hero + one sheen sweep during the hold                                       |
| **velocity**    | loud-sport     | sport / auto / fitness                          | every word arrives along its motion vector (streak+skew), hero passes with speed trails            |

Pick by `safe-zones.json` (`heroAnchor.bandLuma`, `palette.temperature`) × content
register — [dna/README.md](dna/README.md) has the decision rule. Authoring:
`cinematic.json` takes `"dna": "<name>"`.

The engine generates the **hero three-act** from the DNA (no authoring needed):
co-visible captions dim (setup) → per-letter entrance with amplitude ∝ spoken loudness
(impact) → breathe + glow until exit (afterglow).

(Legacy: `plan.template:"cinematic-cream"` maps to `dna:"cream"` automatically.
The retired 54-template library lives outside the skill at
`~/Downloads/embedded-captions-archive/standard-templates-54/`; `_motion.md` remains
in-skill as the motion-verb reference catalog.)

---

## Aesthetic decision — tone × shot × platform (input to the catalog shortlist, NOT a second router)

Classify the clip on 3 axes and feed the result into CATALOG.md's shortlisting — this section never picks a mode/engine by itself:

**Tone** (what feel does the content have?)

- documentary | conversational | energetic | poetic | keynote | investigative | music-video

**Shot** (what's the framing?)

- close-up (head + shoulders) | mid-shot (torso+) | wide (full body+) | cut-montage (mixed shots)

**Platform** (where will it play?)

- 9:16 portrait (TikTok/IG/Shorts) | 16:9 landscape (YouTube/web) | 1:1 square | broadcast export

Cross-reference in [references/direction-catalog.md § Classification matrix](references/direction-catalog.md) for direction language — then return to [CATALOG.md](CATALOG.md) to shortlist identities (this matrix informs the shortlist; the catalog is the only routing surface).

## Composition craft (embed track) — read before embedding

The full **embed-track** playbook lives in **[references/composition-craft.md](references/composition-craft.md)**:
transcript role-annotation, phrase grouping, planes & clean-zone anchoring, zone coherence,
climax pop & readability, edge-breathing, the occlusion 3-step judgement, and
accumulation/persistence. It governs how a _promoted_ phrase sits INTO the scene — read it
before authoring any embed (Cinematic `plan.json` or Standard `index.html`). The default **rail**
track has its own, much simpler spec → **[references/rail.md](references/rail.md)**.

---

## Shared knowledge

| Doc                                                                      | What                                                                                                                               |
| ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| [references/rail.md](references/rail.md)                                 | **The rail track** — standard lower-third subtitle spec (the default; carries most text).                                          |
| [references/composition-craft.md](references/composition-craft.md)       | **The embed-track playbook** — grouping, planes, climax pop, occlusion judgement, accumulation/persistence. Read before embedding. |
| [dna/README.md](dna/README.md)                                           | **The DNA registry** — ten scene-parameterized visual languages; how to pick.                                                      |
| [references/reference-bar.md](references/reference-bar.md)               | **The taste bar** — per-register world-class references + the 5 positive checks.                                                   |
| [references/aesthetic-principles.md](references/aesthetic-principles.md) | **The 18 rules.** Beat Veed AI on taste. Read first.                                                                               |
| [references/motion-vocabulary.md](references/motion-vocabulary.md)       | 10 named motion primitives + tone→timing lookup                                                                                    |
| [references/direction-catalog.md](references/direction-catalog.md)       | 10 ship-ready aesthetics + tone×shot×platform matrix                                                                               |
| [references/anti-patterns.md](references/anti-patterns.md)               | Bugs already locked out (CoreML, letter-spacing reflow, etc.)                                                                      |
| [references/scene-types.md](references/scene-types.md)                   | When a wall surface is usable (4 conditions)                                                                                       |
| [references/layout-heuristics.md](references/layout-heuristics.md)       | Plane positioning, clean-zone selection, crown 3 conditions, pillarbox math                                                        |
| [references/typography-presets.md](references/typography-presets.md)     | Font-size × column-width matrix (starting points)                                                                                  |
| [references/caption-grouping.md](references/caption-grouping.md)         | Word → group rules (pauses, sentence boundaries)                                                                                   |
| [references/failure-modes.md](references/failure-modes.md)               | Long tail of dev gotchas                                                                                                           |
| [references/bespoke-vs-presets.md](references/bespoke-vs-presets.md)     | Why presets fail sometimes; clone-and-tweak pattern                                                                                |

**Read the aesthetic principles and direction catalog FIRST.** Everything else is implementation detail.

---
