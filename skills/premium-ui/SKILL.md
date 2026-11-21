---
name: premium-ui
description: Designs premium, product-specific interfaces with purposeful motion — landing pages AND app panels/dashboards/admin screens — inside an existing project. First studies the codebase (product, real prices/limits, stack) and proposes 2–3 design directions as live mini-designs plus concrete improvement suggestions, then builds the chosen one and audits it in a browser. Also handles one component family across the project ("sadece inputlar", "butonları premium yap", "tablo tasarımı") with variants and full state coverage. Use whenever the user wants a whole page, section set, panel or component family to look and move better — "premium", "profesyonel", "animasyonlu", "şık", "modern", "yeniden tasarla", a landing/tanıtım sayfası, a dashboard or panel redesign — or points at a reference site and says "bu tarzda" / "like this", even if they don't say "design". Do NOT use it for a one-value tweak (one colour, one spacing fix, a typo), pure backend work, generating images/logos/brand kits, slide decks, or charts on their own — handle those directly or with the matching skill.
---

# Premium UI

Premium is not "more effects". It is: one clear visual idea, type and spacing
that feel deliberate, and motion that **explains the product**. A reader should
understand what the product does by watching the page move.

Reference files (read the one the task needs, not all):

- `references/direction-finding.md` — how to derive directions from the product's world so every project doesn't get the same look. Read before any proposal or "you choose".
- `references/type-library.md` — faces grouped by genre with character notes, all checked for Turkish glyphs. Pick faces from here, not from memory.
- `references/high-end.md` — the bar: scenes instead of stacked sections, the brand shape as a system, real pictures, explorable real data, chrome, choreographed motion, and the level check. Read before planning or reviewing a landing page.
- `references/component-craft.md` — when the request is one component family (inputs, buttons, tables…): scope rules, state matrix, variants, recipes.
- `references/proposal-board.md` — how to propose 2–3 directions with live mini-designs before building.
- `references/motion-catalog.md` — single animation techniques, with when to use them and drop-in code.
- `references/motion-engine.md` — scroll-linked, choreographed motion: choosing GSAP/ScrollTrigger, CSS scroll timelines or View Transitions, choreography tokens, master timelines, page transitions, motion budget.
- `references/art-direction.md` — image inventory and one treatment for all photos, shot lists when there are none, visuals drawn from real data, type as image.
- `references/copy.md` — headlines and scene text that carry the design; patterns, banned phrases.
- `references/webgl.md` — the optional 3D tier: when it earns its place, stack, device tiers, fallback.
- `references/panel-patterns.md` — app shell, dashboard, tables, forms, empty states, theming a component library.
- `references/craft-baseline.md` — type/spacing scales, accessibility, performance budget, copy, loading/empty/error states.
- `references/visual-critique.md` — how to look at the board and each built section (screenshots, six questions, fix and re-shoot) before the user sees it.
- `references/learning.md` — the skill's memory across sessions: recall what earlier boards used and what went wrong, log choices and feedback, distil lessons. Read at the start of every session.
- `references/pitfalls.md` — stack-agnostic mistakes that already happened once; check before shipping.
- `references/stacks/<stack>.md` — framework-specific recipes and pitfalls. Read **only** the one matching the project:
  `laravel-livewire.md` (Blade, Livewire, Flux), `react-next.md` (React, Next.js, shadcn/ui), `vue-nuxt.md` (Vue, Nuxt, Inertia + Vue).
  For anything else (Svelte, Astro, plain HTML…) apply the generic rules.
- `references/prompt-template.md` — the brief to ask the user for when they give too little.

Bundled files:

- `assets/proposal-board.html` — the proposal board template (step 0).
- `assets/component-board.html` — the component board template: variants × states, light and dark (component scope).
- `scripts/verify.js` — the page audit run in step 6 (now with lab performance: LCP, CLS, weight, long frames).
- `scripts/scenes.mjs` — Node + headless Chrome: real-time scrolled screenshots, one viewport per stop, for pinned/scrubbed pages (snapshot.py's full-page shot can't show them).
- `scripts/study.js` — measures a reference site (scenes, type scale, palette, motion stack, chrome) in the browser; step 2.
- `scripts/snapshot.py` — when there is no browser tool: headless Chrome screenshots (desktop, mobile) of a local HTML file plus the `verify.js` report.
- `scripts/learn.py` — the memory: `recall` at the start, `board` / `choice` / `feedback` / `issue` as they happen, `lesson` at the end, `share` (opt-in) to send anonymous lessons to the skill's repo. Stored in `~/.claude/premium-ui/`, outside the plugin.
- `scripts/check-fonts.py` — checks that Google Fonts families exist and contain the needed glyphs (default ğĞşŞıİçÇöÖüÜ). Run it on every face before it goes on a board.

## Workflow

Before anything else, run `python3 scripts/learn.py recall --project <name>`
and apply what it returns (`references/learning.md` §1): lessons, faces and
metaphors to avoid, this project's earlier boards and the user's words.

### Scope first

Decide what was asked, and do only that:

| Request | Scope | Path |
| --- | --- | --- |
| "landing", "tanıtım sayfası", "siteyi yeniden tasarla" | whole page(s) | steps 0–7 |
| "panel", "dashboard" | app screens | steps 0–7, `panel-patterns.md` |
| "şu bölüm", "hero'yu" | one section | skip the board unless no direction exists; build that section only |
| "inputlar", "butonlar", "form alanları", "tablolar" | one component family | `component-craft.md` + component board; no sections, no footer, no layout changes |

Never add sections, a footer treatment or page chrome the scope didn't ask
for. Mention extra ideas in one line at the end instead.

### 0. Propose before you build

Unless the user has already fixed a direction (or says "just build it"),
start with proposals: study the project read-only, then show a **proposal
board** — 2–3 distinct directions as live mini-designs (palette, type, a mini
hero and a mini panel with the signature animation running) plus a list of
concrete, project-specific improvements ("Bu projede önerdiklerim"). Ask the
user to pick a direction and which improvements to include, then continue.
Find the directions with `references/direction-finding.md`, then follow
`references/proposal-board.md`.

### 1. Understand the product before designing anything

Detect the stack first (`package.json`, `composer.json`, framework config,
component library) and read the matching `references/stacks/*.md` file — and
only that one.

Read the project: README / overview docs, routes, models, config (prices,
limits, intervals). Write down 3–5 **product truths** — concrete things the
product does ("an order comes from the marketplace, goes through the engine,
lands in the store, stock goes back out"). Every major animation must show one
of these truths. If you cannot name the truth an animation shows, cut it.

Also find the real numbers: prices, plan limits, schedule intervals, supported
integrations and their status. **Never invent figures, testimonials, customer
counts or "live" claims** — and that includes offers hidden in button copy:
"Ücretsiz başla", "14 gün ücretsiz dene", "kredi kartı gerekmez", "%20
indirim" only if the config or the user says so. Read them from config/DB, or leave them out.

### 2. Handle the reference correctly

When the user gives a reference site: measure it with `scripts/study.js`
and screenshots (`high-end.md`, "Studying a reference"), then study its
*quality* (scene rhythm, scale jump, motion timing, restraint), not its
*costume*. Do not copy its palette,
fonts, shapes or layout. Users reliably reject a re-skin of the reference
("yine çok benzer oldu"). Write one sentence describing what you take from it
and one describing how this product's look will differ, before coding.

### 3. Pick one direction and set tokens first

Choose a single direction and commit. When the user lets you choose ("sen
seç", "just build it"), still derive it with `direction-finding.md` §1–2 —
quickly, in your head — instead of reaching for a familiar look; say in one
sentence which part of the product's world it comes from. Then define tokens
before any component:

- Colours: background, raised surface, ink, muted text, line, one brand accent,
  one secondary "event" colour (e.g. orders = orange). Light and dark values.
- Type: one face for UI (from `type-library.md`), and one emphasis device chosen with the direction
  (weight contrast, colour, case/tracking, a second face, highlight…) used
  sparingly in headings. Tracking and line-height follow the face — tight
  for large grotesks, looser for condensed or mono.
- Shape: one shape language from the direction (soft, small radius, sharp,
  cut corners, heavy borders…). Apply it everywhere, including buttons and
  inputs.
- Motion: the choreography tokens from `motion-engine.md` §2 (durations,
  stagger, three easings) and one word for the personality (calm,
  mechanical, playful). `--ease` / `--spring` in the catalog are aliases.
- Scales: type, spacing and elevation from `craft-baseline.md` §1 — set them
  as tokens too, so no component invents its own sizes.

Check the colour pairs against WCAG AA before building (muted text on both
background and surface, light and dark); fixing a palette later touches
every screen.

In an existing app with a component library (Flux, shadcn, etc.), theme the
library centrally (tokens + a few global overrides) instead of editing every
page — see `panel-patterns.md`.

### 4. Build section by section

Landing page: there is no standard section order. Write the **scene
plan** from `high-end.md` §1 first (5–8 scenes, the visitor's question each
answers, composition, what moves, real data), with no two adjacent scenes
alike and nothing from `recall`'s recently used moves without a reason.
Pricing, FAQ, logos, a carousel, a calculator or a big footer wordmark are
options for a specific need, never defaults. The footer is navigation,
contact and legal; see `high-end.md` "The footer is not a signature".
Log the plan with `learn.py build` once it's agreed (`learning.md` §2).

Panel: shell (sidebar on background, page as a raised sheet) → overview
dashboard with real data → list/detail pages inherit from the theme.

For every component, design its loading, empty, error and limit states and
write real microcopy for them (`craft-baseline.md` §4–5) — defaults are where
premium falls apart.

Show the user each meaningful step; ask for feedback on a section rather than
delivering everything at once. Feedback like "burası daha profesyonel olabilir"
is about that section only — redo it, keep what they liked.

### 5. Motion rules

Pick the engine with `motion-engine.md` §1 (IntersectionObserver for a few
reveals; GSAP + ScrollTrigger or CSS scroll timelines for scrubbed, pinned
scenes; View Transitions between states and pages). Ask before adding a
dependency. Build the signature moment from its three-frame storyboard.

- Animate only `transform`, `opacity`, `filter`, stroke-dash. Never layout
  properties — that includes the easy-to-miss ones: `grid-template-rows`
  (0fr → 1fr accordions), `max-height`, `width` on progress bars and slider
  thumbs. Before you tell the user "only transform/opacity", grep your CSS
  transitions/keyframes and JS style writes for them; `verify.js` also lists
  them under `layoutAnimations`.
- Reveal content only after JS confirms it can reveal it again (add an
  `armed` class from JS; hidden state lives under that class). A failed
  script must never leave a blank page. This covers *every* JS-driven hiding,
  not just scroll reveals: inactive carousel slides, collapsed story steps,
  dimmed screens — without JS they all show.
- Honour `prefers-reduced-motion`: disable loops and reveals, keep content.
  Loops that wait with `setTimeout` must still use a real delay under
  reduced motion, or they spin.
- Pause/avoid work off-screen (IntersectionObserver), batch scroll work in
  `requestAnimationFrame`.
- Stagger lists 60–120ms. Durations: micro 200–400ms, reveals 700–1100ms.
- Every interactive control needs a ≥ 22px hit area (see pitfalls).

### 6. Verify in a real browser — always

After each section: load it in the browser at desktop (1440×900) and mobile
(375×812). Check:

- Run `scripts/verify.js` in the page (read the file and pass its contents
  to the browser tool's JavaScript runner; the result is a JSON report) after
  animations settle, at both sizes, and in light and dark. It checks
  horizontal overflow, hit areas, text contrast, focus styles, infinite
  animations / missing reduced-motion support, animated layout properties,
  image alt/size, lazy hero images, font-display and document basics.
  Fix every `fail`; fix or justify every `warn`; `unverified` means a
  cross-origin stylesheet hid the rules from the script, so check that item by
  hand. The tab must be in front (a hidden tab returns an `error`). If the
  browser can emulate `prefers-reduced-motion`, run it once more with it on —
  infinite loops must be 0.
- Press Tab through the new section once: focus is visible and in order.
- Screenshots after animations settle (reveals are mid-transition right after
  scroll — wait or force the revealed class before judging), then the
  visual critique in `visual-critique.md`: look at them and answer its six
  questions. Without a browser tool, `scripts/snapshot.py` takes the
  screenshots and runs `verify.js` for local HTML.
- Interactive pieces with **real pointer drags/clicks**, not only by setting
  values in JS (a JS `.value =` can pass while a real drag fails).
- Light and dark mode for panels.
- Run the project's tests; add tests for any new logic (calculators, plan
  matching, dashboard queries scoped to the tenant/user).

Report what you checked and what you could not (e.g. "no local user to log in").

### 7. Learn from the session

Distil the session into at most three lessons with `learn.py lesson`
(`references/learning.md` §3) and tell the user in one line what was
remembered. If `recall` showed a "Sharing" section, offer once to
send the lessons to the skill's author (`learning.md` §4); send only on a
clear yes. Then the shared list:

`pitfalls.md` is made of mistakes that really happened. When this session
fixed a bug that the user had to point out, or one that cost more than one
attempt, and it isn't in `pitfalls.md` or the stack file yet, end your report
with a proposed row (Symptom | Cause | Fix) and the file it belongs in. Add it
only if the user agrees and the skill files are writable (they usually are
when the skill lives in the user's own repo; a plugin cache is overwritten on
update).
