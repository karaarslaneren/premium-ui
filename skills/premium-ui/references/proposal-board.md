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

Find the three directions with `direction-finding.md` first: they come from
the product's world and differ on at least three axes. There is no standard
spread (no fixed "one editorial, one dark, one bold") — a fixed spread is
exactly what makes every board look the same.

For each direction:

| Field | Example |
| --- | --- |
| Name + one-line idea | Named after its metaphor in the product's world, plus why it fits *this* product (must fail the swap test in `direction-finding.md` §5) |
| Palette | 5 swatches: background, surface, ink, accent, event colour |
| Type | UI face + the emphasis device (weight, colour, case, second face…) |
| Shape | the shape language and its radius / border values |
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
type sample, a **mini hero** (headline using the direction's emphasis device,
two buttons, the signature animation running in pure CSS/SVG), a **mini
panel** (sidebar stub + one stat tile + one list row), the
landing/panel/animation ideas and the fit line — all painted with that
direction's tokens, so the user sees the landing and the panel feel together.

The template ships in deliberate grey with system fonts: it is a skeleton,
not a style. Nothing in it is a suggestion. When filling it:

- Replace every `[bracketed]` placeholder; delete the hint text.
- Write each `.dir[data-dir]` token block from scratch for its direction —
  colours, radius, border, fonts, emphasis style — and add a Google Fonts
  `<link>` for the faces you actually use. Pick them from `type-library.md`
  and confirm with `python3 scripts/check-fonts.py "Face A" "Face B"`
  (Turkish ğ ş ı İ; some fonts have latin-ext but no İ).
- Change structure where the direction needs it: a dense direction can show
  a table row instead of a card, a print-like one can drop the rounded hero
  frame. Three columns with identical layouts read as one direction.
- Replace the generic packet-on-a-path with each direction's real signature
  animation (it must show a product truth, see SKILL.md step 1). The three
  signature animations should differ in kind, not only in colour.
- Use real numbers from the project in the stat tile and list row.

Then look at it before the user does: run `visual-critique.md` on the
board (with a browser tool, or `python3 scripts/snapshot.py <board.html>`
without one), fix what it finds, log the board (`python3 scripts/learn.py board
<board.html> --project <name>`, and an `issue` for each problem the critique
found), and only then show it:

- If the Artifact tool is available, publish the file with it (private by
  default) and give the user the link.
- Otherwise give the file path and the desktop screenshot(s).

## 4. Ask, then build

Ask the user to choose (a multiple-choice question if the tool exists:
options = the direction names, first one marked as your recommendation, plus
"karıştır" — mix parts). Also ask which of the project-specific improvements
to include. Only after the answer, continue with SKILL.md step 3 onward using
the chosen direction's tokens.

If the user says "sen seç" / "you choose": pick, say why in one sentence,
and proceed. Log the answer either way (`learn.py choice`, plus `feedback`
with the user's words if they said more than a letter).
