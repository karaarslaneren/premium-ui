# Component scope: when the user wants one kind of element

"Sadece inputları güzelleştir", "butonlar premium olsun", "tablo tasarımı",
"form alanlarını yenile": the task is one component family, everywhere it
appears. Do exactly that, at the same level a full redesign would get.

## Rules of scope

- Touch only the requested family and what it needs (its tokens, its
  wrapper, its label/hint/error parts). No new sections, no hero, no footer,
  no page reorganisation. Suggest those separately in one line at most.
- Find every place the component appears (grep the component, the library
  import, raw `<input>`/`<button>` tags) and list them before changing
  anything. Change it **centrally**: the component file, the library's
  theme, or one shared class. Editing 30 pages one by one is the wrong
  layer.
- Keep the project's existing direction: its colours, radius, fonts. If
  there is no direction, take tokens from what exists and say so. Ask only
  if the project has two conflicting styles.
- Skip the full proposal board. Instead show a **component board**
  (`assets/component-board.html`): 2–3 variants of this component side by
  side, each with its complete state matrix, in the project's tokens. Ask
  which variant, then apply it.
- Then run the usual checks on the real pages that use it (`verify.js`,
  visual critique, keyboard), at desktop and mobile, light and dark.

## The state matrix (every variant shows all of them)

default · hover · focus-visible · active/pressed · filled/selected ·
disabled · read-only · invalid + message · valid/success (when the product
confirms values) · loading/pending · with leading/trailing adornment ·
small / default / large · dark mode.

A component is premium when its *least* seen state is designed. Defaults
are where it falls apart.

## Variants differ in kind

Three colour swaps of one input are one variant. Vary on these axes:

- **Container:** outlined · filled (tinted surface) · underline only ·
  inset (sunken) · borderless in a grouped card.
- **Label:** above (default, most usable) · floating inside · inline left
  (dense settings forms) · hidden label + visible placeholder only for
  search (still `aria-label`).
- **Focus:** ring with offset · border colour + soft glow · underline that
  draws from the left · surface lightens.
- **Density:** comfortable (48 px) · default (44 px) · compact (36–40 px,
  tables and toolbars only).

## Text input recipe

- Height 44 px default (40 compact, 48 large); horizontal padding 12–16 px;
  16 px font on mobile (smaller zooms iOS).
- Label above, 13–14 px, medium weight; optional marker "(isteğe bağlı)"
  instead of red asterisks everywhere.
- Hint below in muted text, replaced by the error message on error; both
  tied with `aria-describedby`; `aria-invalid="true"` on error.
- Error: border + message + icon, never colour alone; message says how to
  fix ("E-posta adresinde @ eksik"), appears on blur or submit, not on the
  first keystroke.
- Focus: visible at 3:1 against the surface, 2 px, with offset or inner
  glow; transition 120–160 ms on border/box-shadow only.
- Placeholder is an example, not a label ("ornek@firma.com"), at 4.5:1 if it
  carries meaning, otherwise ≥ 3:1.
- Adornments: leading icon or unit (₺, %, +90), trailing clear button,
  password reveal, spinner while validating; each ≥ 24 px hit area with a
  label.
- Right `type`, `inputmode`, `autocomplete` (`email`, `tel`, `one-time-code`,
  `postal-code`, `cc-number`…). Numbers right-aligned with tabular figures
  in tables.
- Turkish formats: phone `+90 5xx xxx xx xx`, IBAN `TR` + groups of four,
  money with `,` decimals and `.` thousands, date `GG.AA.YYYY`. Mask while
  typing without moving the caret.
- Character count when there is a limit (`32/160`), turning warning at 90 %.
- Textareas grow with content up to a max height.

## Related controls

- **Select / combobox:** looks like the input; chevron rotates when open;
  menu matches the input's radius and width; keyboard (arrows, Enter, Esc,
  type-ahead); search inside when > 10 options; selected item marked with a
  check, not only colour.
- **Checkbox / radio / switch:** custom drawing, native input underneath;
  ≥ 24 px target incl. the label; check draws with stroke animation
  (≤ 200 ms); switch thumb slides with `transform`; indeterminate state.
- **Search:** leading icon, `⌘K`/`Ctrl K` hint chip when a shortcut exists,
  clear button, results count.
- **OTP / code:** separate boxes, paste fills all, auto-advance, `inputmode=numeric`.
- **Date / range:** typed input that accepts `GG.AA.YYYY` plus a calendar,
  never calendar-only.
- **Form layout:** one column; related short fields side by side (il/ilçe);
  group headings; primary action bottom-left aligned with the fields;
  inline save state ("Kaydedildi · 14:02").

## Buttons, tables, cards (same method, short)

- **Buttons:** primary / secondary / ghost / destructive / icon-only;
  height matches inputs; pressed = `scale(.98)`; loading keeps width and
  shows a spinner + verb ("Kaydediliyor"); ghost buttons use the surface's
  ink colour (pitfalls).
- **Tables:** sticky header, row hover, zebra or dividers (not both),
  numeric columns right-aligned tabular, row actions on hover *and* a menu
  for touch, empty/loading/error rows, column with the key fact first.
- **Cards:** one job per card, whole card clickable with one real link,
  hover lifts 2–4 px with shadow change, focus ring on the card.

## Report

List what was changed and where (`components/ui/input.tsx` + the theme
token), how many usages it covers, and anything left out (e.g. "3 eski
form `<input>` doğrudan stilli, ortak bileşene taşınmadı").
