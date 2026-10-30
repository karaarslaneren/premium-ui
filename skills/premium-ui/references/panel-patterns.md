# Panel patterns (dashboards, admin, settings)

Panels are used for hours, so motion is quieter than on a landing page:
one page-enter transition, hover lifts, live status, count-ups on first view.
The premium feel comes from the shell, type, and honest, useful content.

## 1. Theme the component library centrally

Most panels are built from a component library (Flux, shadcn/ui, Filament,
MUI...). Do NOT restyle page by page. Instead:

1. **Override the tokens the library paints with**: its neutral scale or
   CSS variables (surfaces, text, border, primary, radius), light and dark.
2. **Global shape overrides** where tokens can't reach: target the
   library's stable data attributes or a component variant, not page markup.
3. **Page enter**: one short animation on the main content
   (`from { opacity: 0; transform: translateY(10px) }`, .45s `--ease`) that
   replays on SPA navigation. Disable under reduced motion.

Inspect a rendered element first (`outerHTML`) to find the real data
attributes and classes before writing overrides.

Library-specific recipes (Flux, shadcn/ui, Nuxt UI, PrimeVue, Vuetify) are in
`stacks/<your-stack>.md`.

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
8. Poll / revalidate every ~30s only the parts whose data moves.

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
dates, page titles). Format numbers and dates with the user's locale and
timezone. Update tests that assert English copy, and tell the user if the
production environment needs a locale setting changed too. Where each
framework keeps these strings: `stacks/<your-stack>.md`.
