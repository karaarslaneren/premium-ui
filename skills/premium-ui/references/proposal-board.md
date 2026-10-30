# Proposal board: suggest directions before building

When the skill starts in a project and the user has not already fixed a
direction, do not build yet. Study the project, then show **2–3 distinct
directions** as live mini-designs on one page, and let the user pick.

## 1. What to gather first (10 minutes, read-only)

- What the product does and for whom (README, overview docs, routes, models).
- 3–5 product truths that motion could show (see SKILL.md step 1).
- What exists: current CSS/tokens, component library, fonts, logo, dark mode,
  the screens that exist (landing? dashboard? settings? lists?).
- Real numbers available for the designs (prices, limits, intervals, counts).
- Weak spots worth fixing (placeholder dashboard, untranslated strings,
  starter-kit leftovers, inconsistent buttons, no empty states).

## 2. What each direction must contain

Directions must differ in **idea**, not just colour. Good spread: one calm
editorial, one dark technical, one bold/expressive — adjusted to the product.

For each direction:

| Field | Example |
| --- | --- |
| Name + one-line idea | "Kâğıt & Mürekkep — sakin, editoryal; ürün bir hikâye gibi akar" |
| Palette | 5 swatches: background, surface, ink, accent, event colour |
| Type | UI face + optional expressive face for 1–3 words |
| Shape | pills + 28px cards / sharp chamfers / heavy borders |
| Signature animation | the one moving thing that shows a product truth |
| Landing ideas | 3 bullets: hero, one interactive tool, one section |
| Panel ideas | 3 bullets: shell, dashboard, one list/detail page |
| Risk / fit | who it suits, what it costs (effort, readability) |

Then a short, separate **"Bu projede önerdiklerim"** list: 4–8 concrete
improvements independent of direction (e.g. "Dashboard yer tutucu kutulardan
oluşuyor → gerçek verili genel bakış", "Ayarlar İngilizce → Türkçe",
"Plan sınırı sadece hata mesajında görünüyor → listelerin yanında göster").

## 3. Render the board

Write ONE self-contained HTML file (no build step, fonts from Google Fonts,
no other external JS). Put it in the session scratchpad (or `/tmp`) — not in
the project — unless the user asks to keep it. Then show it:

- If an Artifact / page-publish tool is available, publish it there.
- Otherwise open it in the browser tool and take a screenshot per direction
  (desktop width), and give the file path.

Each direction is a column (stacked on mobile) containing: the swatches, the
type sample, a **mini hero** (headline with the accent word, two buttons, the
signature animation running in pure CSS/SVG), and a **mini panel** (sidebar
stub + one stat tile + one list row + a primary button) — all painted with
that direction's tokens, so the user sees the landing and the panel feel
together.

Skeleton (fill tokens and content per project; keep animations CSS-only):

```html
<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tasarım önerileri</title>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;600&family=Instrument+Serif:ital@1&family=Space+Grotesk:wght@500;700&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>
  body { margin: 0; font: 15px/1.5 system-ui; background: #ecebe7; color: #111; }
  .board { display: grid; gap: 20px; padding: 24px; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); }
  .dir { background: var(--bg); color: var(--ink); border-radius: var(--r); padding: 24px; font-family: var(--ui); overflow: hidden; }
  .dir[data-dir="a"] { --bg:#f4f2ec; --surface:#fff; --ink:#0e1013; --muted:#5e6470; --accent:#0f766e; --event:#ea580c; --r:28px; --ui:'Instrument Sans'; --display:'Instrument Serif'; }
  .dir[data-dir="b"] { --bg:#0b0d10; --surface:#14171c; --ink:#e6eef0; --muted:#8a919c; --accent:#2dd4bf; --event:#f5b14a; --r:6px; --ui:'Space Grotesk'; --display:'JetBrains Mono'; }
  .dir[data-dir="c"] { /* third direction */ }
  .swatches { display: flex; gap: 6px; } .swatches i { width: 28px; height: 28px; border-radius: 50%; }
  .hero h3 { font-size: 34px; line-height: 1; letter-spacing: -.03em; margin: 16px 0 8px; }
  .hero em { font-family: var(--display); color: var(--accent); }
  .btn { display: inline-block; padding: 10px 16px; border-radius: 999px; background: var(--ink); color: var(--bg); font-weight: 600; }
  .panel { display: grid; grid-template-columns: 70px 1fr; gap: 10px; margin-top: 18px; }
  .card { background: var(--surface); border-radius: calc(var(--r) * .7); padding: 14px; }
  /* signature animation per direction: e.g. a packet moving along a path */
  @keyframes travel { from { offset-distance: 0% } to { offset-distance: 100% } }
  .packet { offset-path: path('M10 40 C 90 40, 110 10, 190 10'); animation: travel 2.4s cubic-bezier(.16,1,.3,1) infinite; }
  @media (prefers-reduced-motion: reduce) { * { animation: none !important } }
</style></head>
<body><main class="board">
  <section class="dir" data-dir="a">
    <strong>A · [Ad]</strong><p>[tek cümlelik fikir]</p>
    <div class="swatches"><i style="background:var(--bg);outline:1px solid #0002"></i><i style="background:var(--surface)"></i><i style="background:var(--ink)"></i><i style="background:var(--accent)"></i><i style="background:var(--event)"></i></div>
    <div class="hero"><h3>[Başlık] <em>[vurgu]</em></h3><a class="btn">[CTA]</a>
      <svg viewBox="0 0 200 50" width="100%"><path d="M10 40 C 90 40, 110 10, 190 10" fill="none" stroke="currentColor" stroke-opacity=".2"/><circle class="packet" r="5" fill="var(--event)"/></svg></div>
    <div class="panel"><div class="card"></div><div class="card"><small>[gerçek bir metrik]</small><b style="font-size:28px;display:block">[sayı]</b></div></div>
    <ul><li>Landing: …</li><li>Panel: …</li><li>İmza animasyonu: …</li></ul>
  </section>
  <!-- B, C -->
</main>
<section style="padding:0 24px 32px"><h2>Bu projede önerdiklerim</h2><ol><li>…</li></ol></section>
</body></html>
```

## 4. Ask, then build

Ask the user to choose (a multiple-choice question if the tool exists:
options = the direction names, first one marked as your recommendation, plus
"karıştır" — mix parts). Also ask which of the project-specific improvements
to include. Only after the answer, continue with SKILL.md step 3 onward using
the chosen direction's tokens.

If the user says "sen seç" / "you choose": pick, say why in one sentence,
and proceed.
