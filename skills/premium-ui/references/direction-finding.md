# Finding design directions

A direction is premium when it could only belong to this product. The
failure mode is the opposite: every project gets the same three looks
(warm paper + italic serif, dark "control room", yellow-black poster) and
every site starts to resemble every other. This file is how to avoid that.
Do it before filling the proposal board.

## 1. Gather raw material (from the project, not from taste)

Write these down in a few words each:

- **The product's world.** Physical objects, places, documents, sounds and
  rituals of the domain. Shipping: labels, barcodes, routes, stamps, depots,
  pallets, tracking numbers. Accounting: ledgers, receipts, stamps, columns.
  Food: menus, tickets, chalkboards, steam, plates. Aim for 8–12 nouns,
  and split them in two: the **obvious** ones (the product's main output,
  the thing its marketing already says) and the **less obvious** ones (a
  ritual, a sound, a tool of the trade, a time of day, a place in the
  audience's own day). For a dental clinic booking app: obvious is the
  appointment calendar and the tooth; less obvious is the waiting-room
  number screen and its chime, the paper bib and its clip, the 8:00 first
  patient, the X-ray lightbox.
- **The audience and the moment of use.** Who opens this, where, and in what
  mood? A small seller checking orders on a phone between packages is not a
  finance team on a 27" monitor.
- **What already exists.** Logo colours and shapes, an existing palette,
  fonts, illustration, the product's name (sound, length, letterforms),
  screenshots. Directions should grow from these unless the user wants a
  clean break.
- **What the neighbours look like.** If you know the category's usual look
  (e.g. every competitor is blue-and-white), note it: that is what to stand
  apart from.
- **Constraints.** Panels are used for hours (calmer, denser, readable);
  landing pages get seconds (more contrast and character). Accessibility
  (AA contrast) applies to every direction.

## 2. Turn material into candidates

From the nouns, pick 5–6 metaphors that could carry a whole visual system
(e.g. "the shipping label", "the route map", "the depot at night",
"the receipt roll"). For each, place it on these axes:

| Axis | Range |
| --- | --- |
| Value | light · mid · dark |
| Colour | muted / earthy · clean neutral + one accent · saturated / multi |
| Temperature | warm · neutral · cool |
| Type character | geometric · grotesk · humanist · serif (old-style, modern, slab) · mono · display / condensed |
| Emphasis device | weight contrast · colour · case / tracking · second face · underline / highlight · size jump |
| Shape | pill / soft · small radius · sharp · cut corners · heavy borders · organic |
| Density | airy · balanced · dense |
| Material | flat · print (grain, halftone, registration) · paper / card · glass / depth · technical lines / grid |
| Motion personality | calm glide · snappy / mechanical · bouncy / playful · stamped / step-wise |

The emphasis device is a real choice: an italic serif word is one option of
six, not the default.

## 3. Choose three that are actually different

- Every pair of directions differs on **at least three axes**, and at least
  one of those is *value* or *type character*. Three palettes on the same
  layout and fonts are one direction in three colours.
- At least one direction should come straight from the product's existing
  assets (if there are any), and at least one should be a bolder reading of
  the domain.
- At least one direction comes from the **less obvious** half of the noun
  list. The obvious metaphors are the ones any designer (and any run of
  this skill) reaches for first, so a board made only of them is the same
  board every time for this product. Keep an obvious one when it is the
  right answer, but not three.
- Name each direction after its metaphor in the product's world ("Teslim
  Fişi", "Gece Vardiyası", "Rota Haritası"), not after a generic style
  ("Minimal", "Modern", "Kontrol Kulesi").

## 4. Overused defaults — allowed only with a product reason

These looks appear whenever a model designs without looking at the product.
Use one only if you can name what in *this* product calls for it, and write
that reason on the board:

- warm off-white "paper" background + italic serif emphasis word
- near-black background + teal/mint accent + mono numbers ("control room")
- near-black or navy + condensed uppercase headings (Barlow Condensed and
  kin) + amber/yellow accent ("night shift", "ops", "kitchen rail")
- yellow + black heavy-border poster / brutalism
- kraft / manila beige + slab or stamp ("parcel", "envelope", "receipt")
- monospace everywhere + uppercase + 2px black borders on near-white
  ("thermal label", "receipt", "spreadsheet") — a strong idea once, a
  default when it shows up on every board
- purple-to-blue gradient SaaS with glassy cards
- Inter or Instrument Sans for everything, pill buttons, 24–28px cards

At most one direction on a board may use an overused default. A board also
doesn't need "one light, one mid, one dark": include a dark direction only
when the moment of use calls for it, and say why.

**Faces.** Models reach for the same "characterful but safe" faces: Inter,
Instrument Sans/Serif, Space Grotesk, JetBrains Mono, IBM Plex Sans/Mono,
Barlow / Barlow Condensed, Bricolage Grotesque, Fraunces, Nunito, Rubik,
Sora, Schibsted Grotesk. Use at most one of these per board, and no face
in more than one direction on the same board. For each direction, open the
genre it needs in `type-library.md`, shortlist the faces whose notes match
the metaphor, then pick — the first face that comes to mind is usually on
the list above. Run `scripts/check-fonts.py` on the chosen faces. The list is a symptom,
not a ban list: whatever face you find yourself reaching for on every
project is the next one to add.

**Asked again.** If a board was already shown in this conversation or the
project (the user asks for "başka seçenekler"), the new board reuses none of
its metaphors, faces or background values.

## 5. Two tests before the board

- **Swap test.** Read each direction's one-line reason and imagine it on a
  different product (a bank, a recipe app). If it still fits, it is generic:
  make it more specific or replace it.
- **Squint test.** Picture the three mini heroes blurred. If two look alike
  (same value, same layout block, same accent position), change one.

## 6. Recommending one

Recommend the direction that best fits the audience and moment of use, and
say in one sentence what it costs (e.g. "dense, needs careful mobile
layout", "strong yellow wears in a panel used all day; panel uses a calmer
variant"). The recommendation is never "the safest-looking one" by default.
