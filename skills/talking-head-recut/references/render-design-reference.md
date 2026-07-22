# talking-head-recut detailed reference

#### Visual Design Library (<SKILL_DIR>/references/)

Beyond the composition-level `themeId`, the skill ships a richer **reference
library** at `<SKILL_DIR>/references/` covering three **orthogonal**
visual dimensions you can freely mix:

```
Style  ×  Layout  ×  VideoFrame
 (10)      (4)         (3)
```

| dimension  | keys                                                                                              | what it decides                                                          |
| ---------- | ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **style**  | `academic` `editorial` `minimal` `spotlight` `geom` `whiteboard` `audit` `terminal` `swiss` `xhs` | the card's visual language — fonts, colors, ornament, layout-within-card |
| **layout** | `split` `stack` `pip` `overlay`                                                                   | how the source video and the card share the canvas                       |
| **frame**  | `clean` `hairline` `polaroid`                                                                     | the decorative chrome around the video element                           |

Read `<SKILL_DIR>/references/DESIGN_INDEX.md`
for the full matrix and a loose decision guide (interview / product launch / data analysis /
social clip / technical tutorial / emotional story …). When you decide to use a specific
style / layout / frame, Read the corresponding file:

- `references/styles/<key>.html` — self-contained card fragment with that
  style's CSS tokens (colors, fonts, padding, ornament) and a placeholder
  takeaway. Copy the `.card[data-card-id="ref-<key>"]` style block, rename
  the data-card-id to your card's id, swap the placeholder content for the
  real takeaway, and you're done.
- `references/layouts/<key>.html` — exact `videoBounds` + `cardBounds` for
  both landscape and portrait, with a copy-paste JSON snippet for
  `storyboard.json`'s per-card `layout` field.
- `references/frames/<key>.html` — decorative HTML to add as a sibling of
  `#video-wrap`, plus placement instructions for the composition CSS.

Pick `style × layout × frame` **per card** — you can change all three
between cards as long as the transitions read smoothly. A common rhythm:
open `editorial × overlay × clean`, switch to `audit × split × hairline`
for the data card, close on `whiteboard × pip × polaroid`.

The 10 styles are skill-side design tokens, **not composition-level themes** —
they don't need to be declared in `storyboard.composition`; they live
inside each card's HTML. The `themeId` field can still pick a
composition-level palette (table above) that controls page-body background
and video border chrome.

#### Layout Compositions (Card + Video)

Two coordinated decisions per card define how it shares the canvas with
the source video:

- **`card.zone`** (declared in `storyboard.json`) — one of the 5 schema
  values; resolve it into pixel bounds (per the table in Step 6) when
  you write the card-host wrapper's inline `style` in Step 9.
- **`#video-wrap` bounds at this card's time window** (declared
  imperatively in the composition's GSAP timeline) — the agent tweens
  `#video-wrap` to a target rect for each layout transition.

Schema does NOT store per-card video bounds. `videoTrack.bounds` is
**one-time** at composition level (defaults to full canvas). Video
"moving" between cards is purely a GSAP animation authored in
`index.html`. There is no `card.layout` field — earlier versions of this
doc invented one; the real schema only has `card.zone`.

**4 composition layouts** (from `references/layouts/`) — each is a
recipe pairing a `zone` with a `#video-wrap` tween target:

| composition layout | recommended `card.zone` | GSAP target for `#video-wrap` (landscape 1920×1080)                       | GSAP target for `#video-wrap` (portrait 1080×1920)                | when to use                                     |
| ------------------ | ----------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------- |
| `split`            | `side-panel`            | `{ left: 960, top: 0, width: 960, height: 1080 }`                         | `{ left: 0, top: 960, width: 1080, height: 960 }` (bottom half)   | speaker + data side-by-side / 50:50 weight      |
| `stack`            | `lower-third`           | `{ left: 14, top: 14, width: 1892, height: 548 }` (top 52%)               | `{ left: 0, top: 0, width: 1080, height: 844 }` (top 44%)         | speaker on top + summary card below             |
| `pip`              | `fullscreen`            | `{ left: 1480, top: 760, width: 400, height: 300 }` + add `.framed` class | `{ left: 690, top: 28, width: 360, height: 203 }` + add `.framed` | content-heavy card + corner pip                 |
| `overlay`          | `video-overlay`         | `{ left: 0, top: 0, width: 1920, height: 1080 }` (full-bleed)             | `{ left: 0, top: 0, width: 1080, height: 1920 }`                  | cinematic / dramatic / glass card on full video |

For 4:5 (1080×1350), scale portrait y/h values by `1350/1920 ≈ 0.703`
(see Step 7.0 Channel A / Channel B `recommendedRatio` resolution
table).

**Other zone values for one-off variants** (still uses `card.zone`; no
fake "layout" field):

| `zone`            | resolved bounds                                        | common use                            |
| ----------------- | ------------------------------------------------------ | ------------------------------------- |
| `fullscreen`      | covers whole canvas                                    | hero card, video tweens to hidden/pip |
| `whiteboard-area` | inset 40px margin (landscape) or bottom 45% (portrait) | dense data card, free margins         |
| `lower-third`     | bottom 30% band                                        | talking-head annotation               |
| `side-panel`      | right 42% (landscape) or bottom 40% (portrait)         | sidebar / "split" recipe              |
| `video-overlay`   | full canvas; expect transparent card root              | glass overlay on full-bleed video     |

You can mix recipes per card — choose `card.zone` based on what suits
the moment, then write the GSAP tween for `#video-wrap` between cards.

#### Storyboard Render Contract

`storyboard.json` is an agent-internal planning artifact — no CLI
command parses it. It exists to keep your timing and content decisions
explicit before you write each card's HTML. Stick to the v3-style
shape below so the same outline drives the composition you assemble in
Step 9.

Required structure (see Step 6 for the full example):

- `schemaVersion: 3`
- `composition: { fps, width, height, durationSeconds, layout, themeId, seed }` — note `durationSeconds`/`fps`/`themeId`/`layout` live **inside** `composition`, NOT at top level
- `videoTrack: { sourcePath, startSec, endSec, bounds? }` — video bounds default to full canvas
- `subtitles: { enabled, ... }`
- `cards[]` — each card has the 6 required fields: `id`, `intent`, `startSec`, `endSec`, `accentIndex`, `zone`, `contentHints`

Rules:

- Card times stay inside `composition.durationSeconds` and should not overlap unless intentional (use `data-track-index` to control z-order when they do).
- Visual details live in card HTML fragments (Step 8), NOT in `contentHints`. `contentHints` is your own structured prompt for designing the card; the rendered look is the HTML.
- Keep the storyboard shape stable — even though nothing parses it, you read it back while authoring Step 8/9, and consistency keeps card IDs and timing in sync.
- Agent-side decisions like "I picked overlay × geom × clean" do NOT belong in `storyboard.json` — keep them in working memory and use them when authoring card HTML + GSAP tweens.

**Transparent card backgrounds for cards that share canvas with video.**
When the GSAP tween leaves video visible behind/beside the card (overlay
recipe, pip recipe, or any `card.zone = 'lower-third' | 'video-overlay'`
moment), the card's `.root` MUST NOT paint a full opaque background —
otherwise it occludes the video. Two patterns:

```css
/* Pattern A: transparent root, page body provides the cream backdrop */
html,
body {
  background: var(--bg);
}
.card[data-card-id="card-X"] .root {
  background: transparent;
}

/* Pattern B: explicit per-card background ONLY for fullscreen cards */
.card[data-card-id="card-hero"] .root {
  background: var(--bg);
}
.card[data-card-id="card-overlay"] .root {
  background: transparent;
}
```

For `side-panel`-zone cards (split recipe), the card-host is already
only half the canvas, so an opaque card bg is fine — it only covers its
half.

### 8. Write Each Card's HTML

Create `$WORK_DIR/public/cards/{card-id}.html` for each card. Each file
contains a single rooted HTML fragment that follows this contract:

#### Card HTML Contract

```html
<div class="card" data-card-id="{cardId}">
  <style>
    /* MUST: every rule starts with .card[data-card-id="{cardId}"] */
    .card[data-card-id="card-01"] .root {
      width: 100%; height: 100%;
      display: flex; ...;
      font-family: 'Caveat', 'LXGW WenKai TC', serif;
      color: var(--text);
      background: var(--bg);
    }
    .card[data-card-id="card-01"] .title { font-size: 84px; ... }
  </style>

  <div class="root">
    <h1
      id="card-01-title"
      data-anim="kinetic-chars"
      data-anim-at="0.3"
      data-anim-duration="0.5"
      data-anim-stagger="0.04"
      data-anim-pattern="pop"
    >
      <span class="char">S</span>
      <span class="char">u</span>
    </h1>
    <div
      id="card-01-line"
      data-anim="grow-x"
      data-anim-at="0.65"
      data-anim-duration="0.5"
      data-anim-target-w="420"
      style="width:0;height:8px;background:var(--accent-0);border-radius:4px;"
    ></div>
  </div>
</div>
```

**Hard rules** (`hyperframes` lint will reject violations):

- Single root `<div class="card" data-card-id="{cardId}">`
- Inline `<style>` rules MUST be prefixed with the scope selector above
- **No `<script>` tags**
- **No external URLs** in `src=` / `href=` (no CDN, no remote fonts)
- **No inline event handlers** (`onclick=` etc.)
- All assets via relative paths into the same `public/` directory
- Colors via `var(--accent-N)` etc. for portability across themes

**Animations are declared, not coded.** Use `data-anim-*` attributes
only; never write `<script>` to animate. You compile every `data-anim-*`
declaration into the single master GSAP timeline in Step 9.

#### Card Sizing — Mobile-First in Portrait

The 10 `references/styles/*.html` are sized for a **1920×1080 landscape**
preview. When `storyboard.layout = "portrait"` (1080×1920, the dominant
case for social / mobile), **scale every visual size up** — phones hold
the screen close, and the same pixel count reads smaller than on a
landscape TV-style canvas.

| token                     | landscape baseline | **portrait target** | scale         |
| ------------------------- | ------------------ | ------------------- | ------------- |
| title (h1/h2 hero)        | 64–96px            | **88–132px**        | ×1.35         |
| detail / body             | 24–30px            | **30–40px**         | ×1.30         |
| kicker / chip label       | 14–16px            | **18–22px**         | ×1.30         |
| timecode / meta           | 12–14px            | **16–18px**         | ×1.30         |
| data block primary number | 48–60px            | **64–88px**         | ×1.40         |
| line-height multiplier    | 1.05–1.5           | same                | (don't scale) |

**Rule of thumb:** `portraitPx = round(landscapePx × 1.3)`, then floor
to a nearby 4px multiple for visual rhythm. Hero headlines may go up to
×1.4; small meta text stays at ×1.2 to avoid crowding.

Padding **shrinks slightly** in portrait — the card is narrower so big
landscape padding (40–64px) eats too much width. Use 24–36px horizontal
padding in portrait.

If you're producing a single card that must work in **both** layouts,
prefer a `@container` query on the card root over hard-coding sizes:

```css
.card[data-card-id="X"] .root {
  container-type: inline-size;
}
.card[data-card-id="X"] .title {
  font-size: clamp(64px, 8.5cqi, 132px);
}
.card[data-card-id="X"] .detail {
  font-size: clamp(24px, 3.2cqi, 40px);
}
```

But for most cards, a single layout choice is fine — just pick the size
table column that matches the storyboard's `layout` field.

#### Available `data-anim` Kinds

| kind            | use for             | key params                                                                                      |
| --------------- | ------------------- | ----------------------------------------------------------------------------------------------- |
| `fade-in`       | enter               | `at`, `duration`, `ease?`                                                                       |
| `fade-out`      | exit                | `at`, `duration`, `ease?`                                                                       |
| `slide-in`      | slide enter         | `at`, `duration`, `from=left\|right\|top\|bottom`, `distance`                                   |
| `kinetic-chars` | per-char pop        | `at`, `duration`, `stagger`, `pattern=pop\|fade` — element needs `<span class="char">` children |
| `typewriter`    | per-char fade       | same as kinetic-chars but slower default stagger                                                |
| `count-up`      | animate number      | `at`, `duration`, `from`, `to`, `format=.0f\|.1f\|.2f\|,d`                                      |
| `draw-path`     | SVG path reveal     | `at`, `duration` — element should be a `<path>`                                                 |
| `grow-y`        | bar height          | `at`, `duration`, `target-h` (px) — element starts `height:0`                                   |
| `grow-x`        | bar width           | `at`, `duration`, `target-w` (px) — element starts `width:0`                                    |
| `scale-pop`     | pop entrance        | `at`, `duration`                                                                                |
| `blur-in`       | unfocused → focused | `at`, `duration`                                                                                |
| `mask-reveal`   | clip reveal         | `at`, `duration`, `direction=left\|right\|top\|bottom`                                          |
| `morph-to`      | tween any CSS       | `at`, `duration`, `props='{...JSON...}'`                                                        |

`data-anim-at` is **seconds relative to the card's startSec** — when you
compile each declaration into the GSAP timeline in Step 9, add the
card's `startSec` to get the absolute time and quantize to 1/fps.

### 9. Assemble the Composition HTML

Stage the assets and write `$WORK_DIR/public/index.html`:

```bash
# SKILL_DIR is injected by the host ("Base directory for this skill: …")
SKILL_DIR="<SKILL_DIR>"

mkdir -p "$WORK_DIR/public/fonts" "$WORK_DIR/public/vendor" "$WORK_DIR/public/cards"
cp -n "$SKILL_DIR/assets/fonts/"*            "$WORK_DIR/public/fonts/"
cp -n "$SKILL_DIR/assets/vendor/gsap.min.js" "$WORK_DIR/public/vendor/"
# stage the input video — RE-ENCODE with dense keyframes. Sources with a sparse GOP
# (keyframe interval > ~1s) freeze on seek in the renderer (a frozen frame under the
# overlays); -g / -keyint_min set to your composition fps make every frame seekable.
# (Set both to your fps — 30 shown; use 24/25/60 to match.)
ffmpeg -y -i "$VIDEO_PATH" -c:v libx264 -crf 18 -g 30 -keyint_min 30 \
  -pix_fmt yuv420p -movflags +faststart -c:a aac "$WORK_DIR/public/input-video.mp4"
```

#### Composition Template

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <style>
      @font-face {
        font-family: "Caveat";
        src: url("fonts/Caveat-400-latin.woff2") format("woff2");
        font-weight: 400;
        font-display: block;
      }
      @font-face {
        font-family: "Caveat";
        src: url("fonts/Caveat-700-latin.woff2") format("woff2");
        font-weight: 700;
        font-display: block;
      }
      @font-face {
        font-family: "LXGW WenKai TC";
        src: url("fonts/LXGWWenKaiTC-400-latin.woff2") format("woff2");
        font-weight: 400;
        font-display: block;
      }
      @font-face {
        font-family: "Inter";
        src: url("fonts/Inter-400-latin.woff2") format("woff2");
        font-weight: 400;
        font-display: block;
      }
      @font-face {
        font-family: "Inter";
        src: url("fonts/Inter-700-latin.woff2") format("woff2");
        font-weight: 700;
        font-display: block;
      }
      @font-face {
        font-family: "Virgil";
        src: url("fonts/Virgil.woff2") format("woff2");
        font-display: block;
      }

      :root {
        /* Pick from the themeId palette table in Step 7 — example: classic */
        --bg: #fff9e3;
        --text: #1e1e1e;
        --accent-0: #1971c2;
        --accent-1: #e03131;
        --accent-2: #2f9e44;
        --accent-3: #e8590c;
        --accent-4: #9c36b5;
        --font-family: "Caveat", "LXGW WenKai TC", serif;
      }
      * {
        box-sizing: border-box;
      }
      /* Body font-family MUST list concrete font names (not just var(--font-family)) —
   the HyperFrames renderer's static analyzer doesn't expand CSS variables when
   resolving fonts, so a var-only chain triggers `font_family_without_font_face`
   lint and falls back to a generic. Use the concrete chain here; cards that
   want the theme font can still reference var(--font-family) internally. */
      html,
      body {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: #000;
        font-family: "Inter", "Caveat", "LXGW WenKai TC", ui-sans-serif, system-ui, sans-serif;
      }
      #stage {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
      }

      /* video-wrapper holds the source video. Its position / size are animated
   over time by the master timeline (one tween per layout transition). */
      .video-wrapper {
        position: absolute;
        left: 0;
        top: 0;
        width: 1920px;
        height: 1080px;
        overflow: hidden;
        border-radius: 0;
        box-shadow: none;
      }
      .video-wrapper video {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }

      .card-host {
        position: absolute;
        pointer-events: none;
        overflow: hidden;
      }
      .card-host .card {
        position: relative;
        width: 100%;
        height: 100%;
        overflow: hidden;
      }
      .card-host .char {
        display: inline-block;
        visibility: visible;
      }

      /* Subtle drop shadow + rounded corners for non-fullscreen video framings */
      .video-wrapper.framed {
        border-radius: 16px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
      }
    </style>
  </head>
  <body>
    <div
      id="stage"
      data-composition-id="talking-head-recut"
      data-start="0"
      data-duration="121.2"
      data-fps="30"
      data-width="1920"
      data-height="1080"
    >
      <!-- Layer 1: source video — initial position matches card-01's layout -->
      <div class="video-wrapper" id="video-wrap">
        <video
          id="bg-video"
          src="input-video.mp4"
          muted
          playsinline
          data-start="0"
          data-duration="121.2"
          data-track-index="1"
        ></video>
      </div>

      <!-- Layer 2: each card-host sits at the bounds dictated by its layout. -->
      <!-- IMPORTANT: every card-host MUST carry BOTH "card-host" and "clip" classes. -->
      <!--   - "card-host"  → our positioning + pointer-events styles                 -->
      <!--   - "clip"       → HyperFrames runtime uses this to enforce visibility     -->
      <!--                    only during data-start … data-start+data-duration.      -->
      <!--                    Without "clip" the host stays visible the whole video   -->
      <!--                    (lint: timed_element_missing_clip_class).               -->
      <!-- Example: card-01 with zone="fullscreen" → card-host covers (0,0,1920,1080) -->
      <div
        class="card-host clip"
        data-card-id="card-01"
        data-start="1.0000"
        data-duration="6.5000"
        data-track-index="2"
        style="left:0;top:0;width:1920px;height:1080px;visibility:hidden;opacity:0;"
      >
        <!-- paste the contents of public/cards/card-01.html here -->
      </div>

      <!-- Example: card-02 with zone="side-panel" (split composition layout) → card on left half -->
      <div
        class="card-host clip"
        data-card-id="card-02"
        data-start="8.0000"
        data-duration="12.0000"
        data-track-index="2"
        style="left:0;top:0;width:960px;height:1080px;visibility:hidden;opacity:0;"
      >
        <!-- card-02 HTML -->
      </div>

      <!-- ...one "card-host clip" per card with inline bounds matching resolveZoneBounds(card.zone)... -->

      <script src="vendor/gsap.min.js"></script>
      <script>
        (function () {
          // count-up formatter helper
          window.__fmt = function (v, fmt) {
            if (typeof fmt === "string" && /^\.[0-9]+f$/.test(fmt)) {
              return Number(v).toFixed(Number(fmt.slice(1, -1)));
            }
            if (fmt === ",d") return Math.round(v).toLocaleString();
            return String(Math.round(v));
          };

          const tl = window.gsap.timeline({ paused: true });

          // ── Card lifecycle (one block per card) ──
          // Example for card-01 [1.0, 7.5] with kinetic-chars at +0.3, grow-x at +0.65:

          // Enter (fade in over 0.4s)
          tl.set('.card-host[data-card-id="card-01"]', { visibility: "visible" }, 1.0);
          tl.fromTo(
            '.card-host[data-card-id="card-01"]',
            { opacity: 0 },
            { opacity: 1, duration: 0.4, ease: "power2.out" },
            1.0,
          );

          // Card-internal anims (compile each data-anim-* declaration here)
          tl.from(
            '.card[data-card-id="card-01"] #card-01-title .char',
            { opacity: 0, y: 8, scale: 0.8, duration: 0.5, ease: "power2.out", stagger: 0.04 },
            1.3,
          );
          tl.fromTo(
            '.card[data-card-id="card-01"] #card-01-line',
            { width: 0 },
            { width: 420, duration: 0.5, ease: "power2.out" },
            1.65,
          );

          // Exit (fade out over 0.35s, ending at endSec)
          tl.to(
            '.card-host[data-card-id="card-01"]',
            { opacity: 0, duration: 0.35, ease: "power2.in" },
            7.15,
          );
          tl.set('.card-host[data-card-id="card-01"]', { visibility: "hidden" }, 7.5);

          // ── Video framing transitions ──
          // When the next card uses a different composition layout, animate the
          // video-wrapper to its new bounds. Example: card-01 = fullscreen
          // (video hidden behind), card-02 = split composition (zone="side-panel"
          // → video on right, card on left).

          // Card-02 enters at 8.0s with the split composition. Animate video to
          // the right half during the card-01 → card-02 gap (between 7.5 and 8.0s).
          tl.set("#video-wrap", { className: "video-wrapper framed" }, 7.5);
          tl.to(
            "#video-wrap",
            { left: 960, top: 0, width: 960, height: 1080, duration: 0.6, ease: "power2.inOut" },
            7.5,
          );

          // Card-02 enter — same pattern as card-01
          tl.set('.card-host[data-card-id="card-02"]', { visibility: "visible" }, 8.0);
          tl.fromTo(
            '.card-host[data-card-id="card-02"]',
            { opacity: 0 },
            { opacity: 1, duration: 0.4, ease: "power2.out" },
            8.0,
          );
          // ...card-02 internal anims...

          // ── repeat for each card; if the NEXT card's layout differs,
          //    insert another tl.to('#video-wrap', ...) tween before its enter ──

          window.__timelines = window.__timelines || {};
          window.__timelines["talking-head-recut"] = tl;
        })();
      </script>
    </div>
  </body>
</html>
```

#### GSAP Statement Cheat Sheet

Compile each `data-anim` attribute into a GSAP statement. Times are
**absolute seconds** = card.startSec + data-anim-at, quantized to 1/fps.
Selector is `.card[data-card-id="X"] #elementId`.

| data-anim                       | GSAP statement template                                                                                                                                                                                            |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `fade-in`                       | `tl.fromTo(SEL, { opacity: 0 }, { opacity: 1, duration: D, ease: 'power2.out' }, T);`                                                                                                                              |
| `fade-out`                      | `tl.to(SEL, { opacity: 0, duration: D, ease: 'power2.in' }, T);`                                                                                                                                                   |
| `slide-in` (from=left, dist=80) | `tl.fromTo(SEL, { opacity: 0, x: -80 }, { opacity: 1, x: 0, duration: D, ease: 'power2.out' }, T);`                                                                                                                |
| `kinetic-chars` (pop)           | `tl.from(SEL + ' .char', { opacity: 0, y: 8, scale: 0.8, duration: D, ease: 'power2.out', stagger: S }, T);`                                                                                                       |
| `count-up`                      | `(function(){const o={v:FROM};tl.to(o,{v:TO,duration:D,ease:'power2.out',onUpdate:function(){const el=document.querySelector(SEL);if(el)el.textContent=__fmt(o.v,'FMT');}},T);})();`                               |
| `draw-path`                     | `(function(){const el=document.querySelector(SEL);if(el){const L=el.getTotalLength();tl.set(SEL,{strokeDasharray:L,strokeDashoffset:L},T);tl.to(SEL,{strokeDashoffset:0,duration:D,ease:'power2.inOut'},T);}})();` |
| `grow-x` (target-w=W)           | `tl.fromTo(SEL, { width: 0 }, { width: W, duration: D, ease: 'power2.out' }, T);`                                                                                                                                  |
| `grow-y` (target-h=H)           | `tl.fromTo(SEL, { height: 0 }, { height: H, duration: D, ease: 'power2.out' }, T);`                                                                                                                                |
| `scale-pop`                     | `tl.fromTo(SEL, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: D, ease: 'back.out(1.6)' }, T);`                                                                                                     |
| `mask-reveal` (direction=left)  | `tl.fromTo(SEL, { clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0 0 0)', duration: D, ease: 'power2.inOut' }, T);`                                                                                         |

Quantize: `T = Math.round(absSec * fps) / fps`. At 30fps the smallest
step is `1/30 ≈ 0.0333s`; rounding to 4 decimals (`.toFixed(4)`) is fine
inside the JS literal.

#### Video Framing Reference (per `layout` value)

The selector for the video container is `#video-wrap`. Animate its
bounds between cards using `tl.to('#video-wrap', { ...bounds }, T)`.
Initial bounds should be set inline on the element to match card-01's
layout. Pick a transition duration of 0.5–0.7s with `ease: 'power2.inOut'`.

**Decorative frames** (`clean` / `hairline` / `polaroid`) sit as a
**sibling** of `#video-wrap` and follow it through layout transitions.
See
[`references/frames/`](references/frames/) for each frame's placement
HTML, suggested CSS, and which layouts it pairs with. Quick rule:
`overlay` layout suppresses decorative frames (the full-bleed video
clashes with chrome); PiP layouts already have their own pill treatment
(border-radius + white ring + shadow), so add a decorative frame only on
top of `split` / `stack`.

**GSAP target lookup table** for `#video-wrap` per composition layout
(landscape 1920×1080 — for portrait & 4:5 see `references/layouts/*.html`
which list all three ratios):

| composition layout                   | typical card.zone | `#video-wrap` GSAP target                                                 | extra css class                            |
| ------------------------------------ | ----------------- | ------------------------------------------------------------------------- | ------------------------------------------ |
| `split`                              | `side-panel`      | `{ left: 960, top: 0, width: 960, height: 1080 }`                         | —                                          |
| `stack`                              | `lower-third`     | `{ left: 14, top: 14, width: 1892, height: 548 }` (top 52%)               | —                                          |
| `pip` (bottom-right)                 | `fullscreen`      | `{ left: 1480, top: 760, width: 400, height: 300 }`                       | `pip-pill` (border-radius + ring + shadow) |
| `pip` (top-left)                     | `fullscreen`      | `{ left: 40, top: 40, width: 400, height: 300 }`                          | `pip-pill`                                 |
| `overlay` (video full-bleed)         | `video-overlay`   | `{ left: 0, top: 0, width: 1920, height: 1080 }` (no change from default) | —                                          |
| **hide video** (pure-graphic moment) | `fullscreen`      | `{ opacity: 0 }` (or move off-canvas)                                     | —                                          |

To toggle the pip-pill chrome (border-radius + white ring + drop shadow)
when entering or leaving a pip moment:

```js
// Enter pip — add chrome
tl.set("#video-wrap", { className: "video-wrapper pip-pill" }, T);
tl.to(
  "#video-wrap",
  { left: 1480, top: 760, width: 400, height: 300, duration: 0.6, ease: "power2.inOut" },
  T,
);

// Leave pip — back to clean full-bleed
tl.set("#video-wrap", { className: "video-wrapper" }, T_NEXT);
tl.to(
  "#video-wrap",
  { left: 0, top: 0, width: 1920, height: 1080, duration: 0.6, ease: "power2.inOut" },
  T_NEXT,
);
```

**Card-host bounds match the zone**. Resolve the card's `zone` into
pixel bounds using the table at the top of Step 6, then write those
into the card-host's inline `style="left:Xpx;top:Ypx;width:Wpx;
height:Hpx;..."`. For `video-overlay` zone (overlay recipe), the
card-host fills the full canvas — your CSS inside `.card .root`
decides where the actual visible card sits.

#### HyperFrames Layout / Animation QA Rules

- Build each card's static hero frame first: the moment where the card is fully visible and readable.
- Confirm video, cards, subtitles/captions, and diagrams do not unintentionally overlap.
- Confirm hidden video areas are clipped by the frame and not visible outside intended bounds.
- Register one paused master timeline as `window.__timelines["talking-head-recut"]`.
- Build timelines synchronously at page load; no `async`, `setTimeout`, Promises, or media `play()` calls.
- Do not use `Math.random()` or `Date.now()` in render paths.
- Do not use `repeat: -1`; calculate finite repeats from the video duration.
- Prefer GSAP transforms and opacity (`x`, `y`, `scale`, `rotation`, `opacity`) over layout properties (`top`, `left`, `width`, `height`) for motion.
- Animate wrappers such as `#video-wrap`, not the video element dimensions directly.
- Avoid animating the same property on the same element from multiple timelines at the same time.
- Use `data-track-index`, not `data-layer`; use `data-duration`, not `data-end`.
- Every timed element (`card-host`, sub-composition, etc.) MUST include `class="clip"` alongside its own classes — e.g. `class="card-host clip"`. The HyperFrames runtime uses `.clip` to gate visibility to the `data-start … data-start+data-duration` window. Without it the element is visible for the whole video (lint: `timed_element_missing_clip_class`).
- For body / global `font-family`, list **concrete font names** (`'Inter', 'Caveat', …`) — not a CSS variable like `var(--font-family)`. The HyperFrames font resolver doesn't expand CSS vars during static analysis (lint: `font_family_without_font_face`). Cards may still use `var(--font-family)` internally since their `@font-face` declarations are loaded.
