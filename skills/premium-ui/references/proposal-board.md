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

Start from the template **`assets/proposal-board.html`**: copy it to the
session scratchpad (not into the project, unless the user asks to keep it)
and fill it. It is one self-contained file (Google Fonts only, CSS-only
animations, reduced-motion handled) and passes `scripts/verify.js` at
desktop and mobile widths as shipped. Keep it passing after you fill it.

Each direction is a column (stacked on mobile) containing: the swatches, the
type sample, a **mini hero** (headline with the accent word, two buttons, the
signature animation running in pure CSS/SVG), a **mini panel** (sidebar stub
+ one stat tile + one list row), the landing/panel/animation ideas and the
fit line — all painted with that direction's tokens, so the user sees the
landing and the panel feel together.

When filling it:

- Replace every `[bracketed]` placeholder; delete the hint text.
- Change each `.dir[data-dir]` token block (colours, radius, fonts) and the
  Google Fonts URL to the fonts you actually use.
- Replace the generic packet-on-a-path with each direction's real signature
  animation (it must show a product truth, see SKILL.md step 1).
- Use real numbers from the project in the stat tile and list row.

Then show it:

- If the Artifact tool is available, publish the file with it (private by
  default) and give the user the link.
- Otherwise open it in the browser tool, take one screenshot per direction at
  desktop width, and give the file path.

## 4. Ask, then build

Ask the user to choose (a multiple-choice question if the tool exists:
options = the direction names, first one marked as your recommendation, plus
"karıştır" — mix parts). Also ask which of the project-specific improvements
to include. Only after the answer, continue with SKILL.md step 3 onward using
the chosen direction's tokens.

If the user says "sen seç" / "you choose": pick, say why in one sentence,
and proceed.
