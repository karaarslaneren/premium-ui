# Craft baseline: scales, accessibility, performance, copy, states

The quiet half of "premium". Nobody praises these, but every one of them is
noticed when missing. `scripts/verify.js` checks the measurable parts.

## 1. Scales (pick once, use everywhere)

**Type scale** (px, ~1.25 ratio; adjust the top end to the direction):

| Token | Size / line-height | Use |
| --- | --- | --- |
| `xs` | 12 / 16 | labels, meta, table captions |
| `sm` | 14 / 20 | secondary UI text, table cells |
| `base` | 16 / 24 | body, inputs (never < 16 on mobile inputs: iOS zooms) |
| `lg` | 20 / 28 | card titles, lead paragraphs |
| `xl` | 28 / 32 | page titles in panels |
| `2xl` | 40 / 44 | section headings |
| `3xl` | 64 / 64 | hero (use `clamp(40px, 7vw, 88px)`) |

- Display sizes: tracking −0.03em, line-height 1.0–1.1. Body: tracking 0, 1.5.
- Max line length 60–75ch for prose. `text-wrap: balance` on headings,
  `text-wrap: pretty` on paragraphs.
- Numbers that change or align (prices, stats, tables):
  `font-variant-numeric: tabular-nums`.
- Two weights per face is usually enough (400 + 600).

**Spacing scale** (4px base): 4, 8, 12, 16, 24, 32, 48, 64, 96, 128.
Inside a component use the small steps, between sections the large ones.
Section padding on landing pages: 96–128 desktop, 64 mobile.

**Radius**: one family. If cards are 24px, inner elements are
`card radius − padding` (nested radii look right only when they shrink).

**Elevation**: at most three levels (flat, raised, overlay). Shadows are
long, soft and low-opacity (`0 1px 2px #0000000d, 0 12px 32px -12px #0000001f`);
in dark mode use a lighter surface instead of a shadow.

## 2. Accessibility (non-negotiable)

- **Contrast** WCAG AA: 4.5:1 body text, 3:1 large text (≥ 24px, or ≥ 18.66px
  bold) and UI boundaries/icons. Check muted text on both background *and*
  raised surface, in light *and* dark.
- **Focus**: every interactive element has a visible `:focus-visible` style
  (2px outline in the accent, `outline-offset: 2px`). Never `outline: none`
  without a replacement. Tab through the page once per section.
- **Keyboard**: custom controls (segmented control, carousel, plan finder,
  menus) work with Tab / arrows / Enter / Escape. Use real `<button>` and
  `<a href>`; `aria-pressed` / `aria-selected` / `aria-expanded` reflect state.
- **Motion content**: count-ups render the final value for screen readers
  (`aria-label` with the final number, or animate a decorative copy with
  `aria-hidden`). Status that updates live: `aria-live="polite"`. Decorative
  SVG flows: `aria-hidden="true"`.
- **Visually hidden ≠ hidden**: states hidden with `opacity: 0` (inactive
  status pills, non-active story screens, a pending SMS card) are still read
  aloud. Give them `aria-hidden="true"` — or `inert` if they contain
  controls — and remove it when they become the visible state.
- **Carousels**: arrows are buttons with labels ("Önceki", "Sonraki"); slides
  are reachable by keyboard; nothing auto-advances without a pause control.
- **Images**: meaningful ones have alt text describing the content;
  decorative ones `alt=""`.
- **Language**: `<html lang>` matches the content; one `<h1>` per page,
  headings in order.
- **Hit areas**: ≥ 22×22px (aim for 44 on mobile primary actions).

## 3. Performance budget

| Metric | Target | Usual culprit |
| --- | --- | --- |
| LCP | < 2.5s | hero image lazy-loaded or huge; web fonts blocking |
| CLS | < 0.1 | images without size, fonts swapping metrics, late banners |
| INP | < 200ms | scroll/pointer handlers doing layout work |

- **Fonts**: ≤ 2 families, ≤ 4 files. `font-display: swap`; preconnect to the
  font host; prefer the framework's self-hosting (e.g. `next/font`). Subset to
  the needed scripts (`latin-ext` covers Turkish).
- **Images**: width/height or `aspect-ratio` on every image; modern formats
  (AVIF/WebP); the hero (LCP) image is *not* `loading="lazy"` and may get
  `fetchpriority="high"`; everything below the fold is lazy.
- **Motion cost**: animate transform/opacity/filter only; `will-change` only on
  elements that are animating right now; IntersectionObserver to start/stop
  loops; no scroll listeners without rAF batching.
- **Scroll-pinned sections on mobile**: shorten them (fewer vh per step) or
  replace with a simple stacked layout under ~640px — long pinned sections
  feel broken on touch.
- **Blur is expensive**: large `backdrop-filter` / `filter: blur` areas on
  scrolling content cost frames on mid-range phones; keep them small or static.
- **No new dependency** for something the motion catalog does in 20 lines.

## 4. Copy (microcopy is part of the design)

- Headlines say what the product does for the buyer, in their words, not a
  slogan. One emphasis word, not three.
- CTAs are verbs with an object: "Mağazanı bağla", not "Başla" / "Gönder".
  One primary CTA per view.
- Numbers beat adjectives: "5 dakikada stok eşitlenir" > "hızlı senkronizasyon"
  — and only if the 5 comes from config.
- Error messages say what happened and what to do: "Bağlantı reddedildi.
  API anahtarını kontrol edip tekrar dene."
- Same term for the same thing everywhere (don't mix "mağaza", "store",
  "hesap" for one concept).
- Match the product's language fully; no leftover English in a Turkish UI.

## 5. States (design them, don't leave them to defaults)

Every list, card and dashboard tile has five states — check each one:

| State | Rule |
| --- | --- |
| Loading | Skeleton with the real layout's shape (no layout jump when data arrives); spinner only for actions < 1s area |
| Empty | Says what will appear here and how to get it; one action ("İlk mağazanı bağla") |
| Partial | A few items should still look intentional (don't stretch 2 cards across a 4-column grid) |
| Error | Human message + retry; keeps the rest of the page usable |
| No permission / limit | Disabled with reason, or the upgrade path; never a silent hidden button |

Also: long names (truncate with tooltip), huge numbers (compact format
`1,2 B`), zero values, and right-to-left only if the product supports it.
