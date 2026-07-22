# Worked example: 3-slide deck with fragments and a branch

Use this example after the contract, schema, fragment, and branching rules in `SKILL.md` are understood. It is illustrative evidence only; it does not replace lint, runtime validation, or browser checks.

## Scene HTML (skeleton)

```html
<body style="margin: 0">
  <script type="application/hyperframes-slideshow+json">
    {
      "slides": [
        {
          "sceneId": "hook",
          "notes": "Open with the stat. Pause on the $40B number."
        },
        {
          "sceneId": "problem",
          "notes": "Walk through each pain point one at a time.",
          "fragments": [11.0, 15.0],
          "hotspots": [
            {
              "id": "h1",
              "label": "Where does the $40B figure come from?",
              "target": "market-detail",
              "region": { "x": 55, "y": 60, "w": 40, "h": 20 }
            }
          ]
        },
        {
          "sceneId": "solution",
          "notes": "One sentence: what we do and who it is for."
        }
      ],
      "slideSequences": [
        {
          "id": "market-detail",
          "label": "Market sizing methodology",
          "slides": [{ "sceneId": "mkt-math", "notes": "Bottom-up: 2.3M SMBs × $17k ACV." }]
        }
      ]
    }
  </script>

  <!-- Slide 1 — hook -->
  <div
    data-composition-id="hook"
    data-start="0"
    data-duration="6"
    data-label="The hook"
    data-width="1920"
    data-height="1080"
    style="position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #0a0a0a"
  >
    <section
      class="clip"
      data-start="0"
      data-duration="6"
      data-track-index="1"
      style="position: absolute; inset: 0; display: grid; place-items: center"
    >
      <h1 id="hook-headline" style="font-size: 80px; color: #fff; font-family: sans-serif">
        SMBs lose $40B/year to manual scheduling
      </h1>
    </section>
  </div>

  <!-- Slide 2 — problem (3 fragments) -->
  <div
    data-composition-id="problem"
    data-start="6"
    data-duration="15"
    data-label="The problem"
    data-width="1920"
    data-height="1080"
    style="position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #0a0a0a"
  >
    <section
      class="clip"
      data-start="6"
      data-duration="15"
      data-track-index="1"
      style="position: absolute; inset: 0; padding: 120px 160px; box-sizing: border-box"
    >
      <h2 id="pain-headline" style="font-size: 64px; color: #fff; font-family: sans-serif">
        Three gaps operators can not close
      </h2>
      <p id="pain-1" style="font-size: 48px; color: #ccc; opacity: 0; font-family: sans-serif">
        No-shows cost 23% of booked revenue
      </p>
      <p id="pain-2" style="font-size: 48px; color: #ccc; opacity: 0; font-family: sans-serif">
        Manual reminders take 4h/week per staff
      </p>
      <p id="pain-3" style="font-size: 48px; color: #ccc; opacity: 0; font-family: sans-serif">
        Rescheduling friction drives 40% churn
      </p>
    </section>
  </div>

  <!-- Slide 3 — solution -->
  <div
    data-composition-id="solution"
    data-start="21"
    data-duration="8"
    data-label="The solution"
    data-width="1920"
    data-height="1080"
    style="position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #0a0a0a"
  >
    <section
      class="clip"
      data-start="21"
      data-duration="8"
      data-track-index="1"
      style="position: absolute; inset: 0; display: grid; place-items: center"
    >
      <h2 id="solution-headline" style="font-size: 72px; color: #fff; font-family: sans-serif">
        Acme automates scheduling for service SMBs — no-shows down 80% in 90 days
      </h2>
    </section>
  </div>

  <!-- Branch slide — excluded from main line -->
  <div
    data-composition-id="mkt-math"
    data-start="29"
    data-duration="7"
    data-label="Market math"
    data-width="1920"
    data-height="1080"
    style="position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #111"
  >
    <section
      class="clip"
      data-start="29"
      data-duration="7"
      data-track-index="1"
      style="position: absolute; inset: 0; display: grid; place-items: center"
    >
      <p id="mkt-formula" style="font-size: 56px; color: #fff; font-family: sans-serif">
        2.3M SMBs × $17k ACV = $39B serviceable market
      </p>
    </section>
  </div>

  <script>
    window.__timelines = window.__timelines || {};

    // Slide 2 fragment entrance animations
    gsap.registerPlugin(); // load any plugins before use

    const tl = gsap.timeline({ paused: true });
    window.__timelines["problem"] = tl;

    // Insert positions are absolute composition-timeline times (same as data-start / fragment values).
    tl.from("#pain-1", { opacity: 0, y: 20, duration: 0.4 }, 11.0);
    tl.from("#pain-2", { opacity: 0, y: 20, duration: 0.4 }, 15.0);
    // pain-3 lands at end of slide
    tl.from("#pain-3", { opacity: 0, y: 20, duration: 0.4 }, 13.0);
  </script>
</body>
```

## Key points in the example

- The island `sceneId` values (`"hook"`, `"problem"`, `"solution"`, `"mkt-math"`) exactly match `data-composition-id` values on scene divs.
- `mkt-math` appears only in `slideSequences` — it is never in the top-level `slides` array.
- Fragment times (`11.0`, `15.0`) are within the `problem` scene's `[6, 21]` range (times are absolute composition-timeline positions).
- The hotspot `region` (`x: 55, y: 60, w: 40, h: 20`) positions the clickable area in the lower-right quadrant of the problem slide.
- GSAP timelines are registered on `window.__timelines` and are paused — the HyperFrames engine drives playback; do not call `.play()` at construction time.
