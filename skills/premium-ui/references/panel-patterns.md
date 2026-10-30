# Panel patterns (dashboards, admin, settings)

Panels are used for hours, so motion is quieter than on a landing page:
one page-enter transition, hover lifts, live status, count-ups on first view.
The premium feel comes from the shell, type, and honest, useful content.

## 1. Theme the component library centrally

Most panels are built from a component library (Flux, shadcn/ui, Filament,
MUI...). Do NOT restyle page by page. Instead:

1. **Override the neutral scale** the library paints with. Example (Flux /
   Tailwind v4 — Flux uses `zinc` for everything):
   ```css
   @theme {
     --font-sans: 'Instrument Sans', ui-sans-serif, system-ui, sans-serif;
     --font-serif: 'Instrument Serif', Georgia, serif;
     /* warm paper at the light end, near-black at the dark end */
     --color-zinc-50: #f7f6f2; --color-zinc-100: #f1efea; --color-zinc-200: #e6e3dc;
     --color-zinc-300: #d3cfc7; --color-zinc-400: #a3a09a; --color-zinc-500: #73726e;
     --color-zinc-600: #55565a; --color-zinc-700: #393b40; --color-zinc-800: #202328;
     --color-zinc-900: #14171c; --color-zinc-950: #0b0d10;
     --color-paper: #f4f2ec; --color-ink: #0e1013; --color-brand: #0f766e;
     --color-accent: var(--color-ink);            /* primary buttons */
     --color-accent-content: var(--color-brand);  /* links, current nav item */
     --color-accent-foreground: #fff;
   }
   @layer theme { .dark { --color-accent: #14b8a6; --color-accent-content: #5eead4; --color-accent-foreground: #0b0d10; } }
   ```
2. **Global shape overrides** via the library's data attributes (unlayered so
   they beat inline utility radii):
   ```css
   [data-flux-button]:not([data-flux-button-group] *) { border-radius: 9999px; }
   input[data-flux-control], textarea[data-flux-control], [data-flux-select-button] { border-radius: .75rem; }
   [data-flux-callout], [data-flux-card], [data-flux-modal] > dialog { border-radius: 1.25rem; }
   [data-flux-heading] { letter-spacing: -.02em; }
   [data-flux-main] [data-flux-heading].text-2xl { font-size: 2.125rem; font-weight: 600; letter-spacing: -.03em; }
   ```
3. **Page enter**: `[data-flux-main] > * { animation: page .45s var(--ease) both }`
   with `from { opacity: 0; transform: translateY(10px) }`. Replays on SPA
   navigation (wire:navigate / router). Disable under reduced motion.

Inspect a rendered element first (`outerHTML`) to find the real data
attributes and classes before writing overrides.

## 2. App shell: sheet on paper

- Body and sidebar share the background colour (paper / near-black); the
  sidebar has no border on desktop.
- The page content is a raised sheet: `lg:m-2 lg:rounded-[28px] bg-white`
  + a 1px ring + a long soft shadow. Dark mode: one step lighter than the body.
- Sidebar nav grouped by job, not by data model, e.g. Genel Bakış /
  Entegrasyon / Kontrol / Hesap. Remove starter-kit leftovers (Repository,
  Documentation links, English "Platform" headings).
- Logo: the same mark as the marketing site (e.g. ink circle).
- Admin/staff area: same shell on a visibly different background so nobody
  mistakes it for a customer account.

## 3. Overview dashboard (replace placeholder boxes)

Build it from real queries, scoped to the current tenant/user:

1. **Greeting**: local-time greeting + first name, the first name in the
   expressive face. Date in the user's locale and timezone (not app UTC).
2. **Status pill** only when true (e.g. "Sync running" only if something is
   connected). A status light that lies destroys trust.
3. **Setup checklist** (dark card) until onboarding is done: numbered steps,
   done ones struck through, progress bar, each step links to its screen.
4. **Stat tiles** (2×2 / 4 across): icon chip, big tabular number, label,
   whole tile is a link; tile turns warning-coloured when the number is bad
   (failures > 0).
5. **Two activity panels**: recent business objects (orders, tickets…) with
   coloured source dot, amount, state badge; and a dark "live log" panel with
   status dots + relative time + link to the full log.
6. Empty states that say what will appear and when ("Henüz sipariş gelmedi.
   Pazaryerinden gelen siparişler burada görünecek.").
7. A user with no tenant/org gets a single onboarding card instead of zeros.
8. `poll` every 30s if the data moves.

Test: renders for no-tenant user, shows checklist for fresh tenant, shows own
data and **never another tenant's**.

## 4. Lists, forms, settings

- Page header: big title + one-line purpose subheading + primary action on the right.
- Plan/usage context next to lists ("3 bağlantıdan 1'i kullanımda") instead
  of only failing at the limit.
- Disabled-with-reason beats hidden ("Kuyrukta · 2 dk").
- Tables: keep the library's table, rely on theme; add badges for state.
- Auth screens: split layout — left a dark rounded panel with an ambient
  product animation (SMIL packets along paths) + one quote with the serif
  accent word; right the form on paper, centred, max 380px.

## 5. Language

If the UI language is not English, make sure the framework's own strings are
translated too (starter-kit settings pages, validation messages, relative
dates). In Laravel: `lang/<locale>.json` for `__()` strings, `lang/<locale>/{auth,passwords,validation,pagination}.php`,
`APP_LOCALE`, and remember attribute-based titles like Livewire `#[Title('...')]`
are NOT passed through `__()`. Update tests that assert English copy, and
tell the user the production `.env` needs the locale change too.
