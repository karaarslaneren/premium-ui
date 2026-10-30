# Stack: React / Next.js (shadcn/ui, Tailwind)

Read this only when the project is React. Generic rules live in `SKILL.md`,
`panel-patterns.md` and `pitfalls.md`.

Detect: `package.json` with `react` / `next`; shadcn/ui if `components.json`
exists; Tailwind v4 if the global CSS has `@import "tailwindcss"`, v3 if there
is a `tailwind.config.*`.

## 1. Theming shadcn/ui centrally

shadcn components read CSS variables from the global stylesheet
(`app/globals.css` or `src/index.css`). Change the variables, not the
components:

- Neutrals: `--background`, `--foreground`, `--card`, `--muted`,
  `--muted-foreground`, `--border`, `--input`, `--ring`.
- Brand: `--primary` / `--primary-foreground` (primary button),
  `--accent` (hover surfaces — not your brand accent), `--destructive`.
- Shape: `--radius` drives every `rounded-*` the components use.
- Dark mode: the same variables under `.dark`.

Check the existing format before writing (newer setups use `oklch(...)`
values with `@theme inline`; older ones use bare HSL triplets like
`222 47% 11%`). Keep that format.

Components are copied into the repo (`components/ui/*`). Edit them only for
things variables can't express (e.g. a pill-shaped `Button` variant), and add
a variant rather than changing the default.

## 2. Fonts

Next.js: `next/font/google` (self-hosted, no layout shift), exposed as CSS
variables and mapped in the Tailwind theme. Vite/CRA: Google Fonts `<link>`
with `display=swap` + `preconnect`.

## 3. Motion in React

- **Dependencies**: if `motion` / `framer-motion` is already installed, use it
  (`whileInView`, `layout`, `AnimatePresence`, `useReducedMotion`). Otherwise
  write the vanilla techniques from `motion-catalog.md` inside a hook — don't
  add a dependency without asking.
- **Armed reveals**: add the `armed` class in a `useEffect` on the client, so
  server-rendered HTML is fully visible without JS. Never render content with
  `opacity: 0` inline from the server.
- **Server Components**: anything with `IntersectionObserver`, pointer events
  or `requestAnimationFrame` must live in a `'use client'` component. Keep it
  small (a `<Reveal>` wrapper, a `<CountUp>`) so pages stay server components.
- **Hydration**: count-ups and greetings must render the same text on server
  and client first (final value / neutral greeting), then animate or adjust in
  an effect. Time-dependent text rendered on the server causes hydration
  mismatches.
- **Refs, not queries**: use refs instead of `document.querySelectorAll` so
  re-renders and route changes don't leave dangling observers; disconnect in
  the effect cleanup.
- **Page enter**: App Router `template.tsx` re-mounts on navigation — put the
  page-enter animation there (a `layout.tsx` does not re-mount).
- **Sliding highlight / shared ring**: `motion`'s `layoutId` does it in one
  line; without it, measure in `useLayoutEffect` and on `ResizeObserver`.

## 4. Data and i18n

- Dashboards: fetch in server components / route handlers scoped to the
  session's tenant; never trust a tenant id from the client.
- i18n: whatever the project already uses (`next-intl`, `react-i18next`);
  format numbers and dates with `Intl` and the user's locale/timezone.
- Tests: the project's runner (Vitest/Jest + Testing Library, Playwright);
  unit-test calculator/plan logic as pure functions.

## 5. Pitfalls seen in React projects

| Symptom | Cause | Fix |
| --- | --- | --- |
| Content flashes then hides, or stays hidden | Hidden state rendered on the server | Hide only under `.armed`, added in `useEffect` |
| "Text content does not match server-rendered HTML" | Time/locale-dependent text on first render | Stable first render, adjust in an effect |
| Reveals stop after client navigation | Observer created once at module scope | Create/disconnect per component in an effect |
| Theme change ignored | Edited a component class while it reads `var(--primary)` | Change the variable |
