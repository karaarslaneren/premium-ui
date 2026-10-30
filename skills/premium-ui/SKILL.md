---
name: premium-ui
description: Designs premium, product-specific interfaces with purposeful motion — landing pages AND app panels/dashboards/admin screens. First studies the project and proposes 2–3 design directions as live mini-designs plus concrete improvement suggestions, then builds the chosen one. Use when the user asks for a "premium", "profesyonel", "animasyonlu", "şık", "modern" design, a landing/tanıtım sayfası, a dashboard or panel redesign, or points at a reference site and says "bu tarzda" / "like this". Covers concept, theme tokens, motion catalog (scroll reveal, line mask, count-up, SVG flow, scroll-pinned story, magnetic, glow, plan finder, carousels), panel shell patterns, and a browser verification loop.
---

# Premium UI

Premium is not "more effects". It is: one clear visual idea, type and spacing
that feel deliberate, and motion that **explains the product**. A reader should
understand what the product does by watching the page move.

Reference files (read the one the task needs, not all):

- `references/proposal-board.md` — how to propose 2–3 directions with live mini-designs before building.
- `references/motion-catalog.md` — every animation technique, with when to use it and drop-in code.
- `references/panel-patterns.md` — app shell, dashboard, tables, forms, empty states, theming a component library.
- `references/craft-baseline.md` — type/spacing scales, accessibility, performance budget, copy, loading/empty/error states.
- `references/pitfalls.md` — stack-agnostic mistakes that already happened once; check before shipping.
- `references/stacks/<stack>.md` — framework-specific recipes and pitfalls. Read **only** the one matching the project:
  `laravel-livewire.md` (Blade, Livewire, Flux), `react-next.md` (React, Next.js, shadcn/ui), `vue-nuxt.md` (Vue, Nuxt, Inertia + Vue).
  For anything else (Svelte, Astro, plain HTML…) apply the generic rules.
- `references/prompt-template.md` — the brief to ask the user for when they give too little.

Bundled files:

- `assets/proposal-board.html` — the proposal board template (step 0).
- `scripts/verify.js` — the page audit run in step 6.

## Workflow

### 0. Propose before you build

Unless the user has already fixed a direction (or says "just build it"),
start with proposals: study the project read-only, then show a **proposal
board** — 2–3 distinct directions as live mini-designs (palette, type, a mini
hero and a mini panel with the signature animation running) plus a list of
concrete, project-specific improvements ("Bu projede önerdiklerim"). Ask the
user to pick a direction and which improvements to include, then continue.
Follow `references/proposal-board.md`.

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
counts or "live" claims.** Read them from config/DB, or leave them out.

### 2. Handle the reference correctly

When the user gives a reference site: study its *quality* (motion timing,
restraint, typographic confidence), not its *costume*. Do not copy its palette,
fonts, shapes or layout. Users reliably reject a re-skin of the reference
("yine çok benzer oldu"). Write one sentence describing what you take from it
and one describing how this product's look will differ, before coding.

### 3. Pick one direction and set tokens first

Choose a single direction and commit (examples: light editorial on warm paper;
dark technical; bold brutalist). Then define tokens before any component:

- Colours: background, raised surface, ink, muted text, line, one brand accent,
  one secondary "event" colour (e.g. orders = orange). Light and dark values.
- Type: one sans for UI, optionally one expressive face used *only* for 1–3
  emphasis words per heading (e.g. italic serif). Tight tracking on display
  sizes (−0.03em), relaxed body.
- Shape: one radius language (pills + 20–32px cards, or sharp). Apply it
  everywhere, including buttons and inputs.
- Easing: `--ease: cubic-bezier(.16,1,.3,1)` for reveals,
  `--spring: cubic-bezier(.34,1.56,.64,1)` for things that land/snap.
- Scales: type, spacing and elevation from `craft-baseline.md` §1 — set them
  as tokens too, so no component invents its own sizes.

Check the colour pairs against WCAG AA before building (muted text on both
background and surface, light and dark); fixing a palette later touches
every screen.

In an existing app with a component library (Flux, shadcn, etc.), theme the
library centrally (tokens + a few global overrides) instead of editing every
page — see `panel-patterns.md`.

### 4. Build section by section

Landing page, typical order (adapt to the product):
hero (product truth animated) → integrations/logos with status → flow
explainer → how it works (scroll-pinned) → features bento with
micro-interactions → interactive tool (calculator / plan finder) → pricing →
FAQ carousel → CTA → footer wordmark.

Panel: shell (sidebar on background, page as a raised sheet) → overview
dashboard with real data → list/detail pages inherit from the theme.

For every component, design its loading, empty, error and limit states and
write real microcopy for them (`craft-baseline.md` §4–5) — defaults are where
premium falls apart.

Show the user each meaningful step; ask for feedback on a section rather than
delivering everything at once. Feedback like "burası daha profesyonel olabilir"
is about that section only — redo it, keep what they liked.

### 5. Motion rules

- Animate only `transform`, `opacity`, `filter`, stroke-dash. Never layout properties.
- Reveal content only after JS confirms it can reveal it again (add an
  `armed` class from JS; hidden state lives under that class). A failed
  script must never leave a blank page.
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
  Fix every `fail`; fix or justify every `warn`. If the browser can emulate
  `prefers-reduced-motion`, run it once more with it on — infinite loops must be 0.
- Press Tab through the new section once: focus is visible and in order.
- Screenshots after animations settle (reveals are mid-transition right after
  scroll — wait or force the revealed class before judging).
- Interactive pieces with **real pointer drags/clicks**, not only by setting
  values in JS (a JS `.value =` can pass while a real drag fails).
- Light and dark mode for panels.
- Run the project's tests; add tests for any new logic (calculators, plan
  matching, dashboard queries scoped to the tenant/user).

Report what you checked and what you could not (e.g. "no local user to log in").
