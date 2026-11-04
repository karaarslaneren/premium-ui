# Stack: Laravel + Blade / Livewire / Flux (Tailwind v4)

Read this only when the project is Laravel. Generic rules live in
`SKILL.md`, `panel-patterns.md` and `pitfalls.md`.

Detect: `artisan`, `composer.json` with `laravel/framework`; Livewire if
`livewire/livewire`, Flux if `livewire/flux`; Tailwind v4 if `resources/css/app.css`
contains `@import "tailwindcss"` / `@theme`.

## 1. Theming Flux centrally

Flux paints almost everything with the `zinc` scale, so override that scale
instead of restyling pages. The values below are from one past project and
only show *where* things go — write your direction's own values:

```css
@theme {
  --font-sans: '[UI face]', ui-sans-serif, system-ui, sans-serif;
  --font-display: '[emphasis face, if the direction has one]', ui-sans-serif, sans-serif;
  /* the direction's neutral scale, light end to dark end */
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

Global shape overrides via Flux data attributes (unlayered, so they beat
inline utility radii):

```css
[data-flux-button]:not([data-flux-button-group] *) { border-radius: 9999px; }
input[data-flux-control], textarea[data-flux-control], [data-flux-select-button] { border-radius: .75rem; }
[data-flux-callout], [data-flux-card], [data-flux-modal] > dialog { border-radius: 1.25rem; }
[data-flux-heading] { letter-spacing: -.02em; }
[data-flux-main] [data-flux-heading].text-2xl { font-size: 2.125rem; font-weight: 600; letter-spacing: -.03em; }
```

Page enter: `[data-flux-main] > * { animation: page .45s var(--ease) both }`
with `from { opacity: 0; transform: translateY(10px) }`. It replays on
`wire:navigate`. Disable under reduced motion.

Inspect a rendered element (`outerHTML`) first: Flux attribute names change
between versions.

## 2. Livewire specifics

- **Calculators / plan finders**: compute the answer server-side with
  `wire:model.live` and echo slider values client-side (`x-text="$wire.field"`)
  so dragging feels instant.
- **Dashboard polling**: `wire:poll.30s` only on the parts whose data moves.
- **Scripts after `wire:navigate`**: page scripts do not re-run on SPA
  navigation. Hook reveals/animations to `document.addEventListener('livewire:navigated', init)`
  and make `init` idempotent (skip already-armed elements).
- **Method names**: never name a component method like a `Livewire\Component`
  method (`pull`, `reset`, `only`, `fill`, `validate`…): it fatals with a
  white screen. Use specific names (`pullCatalogue`).
- **Tests**: Pest/PHPUnit with `Livewire::test(...)`; assert tenant scoping
  (`actingAs($userA)` never sees `$userB`'s rows).

## 3. Language (non-English UI)

- `APP_LOCALE` (and `APP_FALLBACK_LOCALE`) in `.env` / `config/app.php`.
- `lang/<locale>.json` for `__()` strings; `lang/<locale>/{auth,passwords,validation,pagination}.php`
  (`php artisan lang:publish` if `lang/` doesn't exist).
- Attribute titles like Livewire `#[Title('...')]` are NOT passed through
  `__()` — set the title in `render()` with `->title(__('...'))` instead.
- Starter-kit settings pages (profile, password, appearance) ship English copy.
- Dates: `Carbon::setLocale()` / `->translatedFormat()`, and convert to the
  user's timezone for display (app timezone is usually UTC).
- Update tests that assert English copy; tell the user the production `.env`
  needs the locale change too.

## 4. Pitfalls seen in Laravel projects

| Symptom | Cause | Fix |
| --- | --- | --- |
| White screen after adding a Livewire action | Method name clashes with `Livewire\Component` | Rename to something specific |
| Dates / English strings in a Turkish UI | `APP_LOCALE=en`, starter-kit strings, `#[Title]` not translated | §3 above |
| Wrong greeting ("İyi geceler" at 09:00) | App timezone UTC | Convert to the user's timezone |
| Animations dead after clicking a nav link | Scripts don't re-run on `wire:navigate` | Re-init on `livewire:navigated` |
