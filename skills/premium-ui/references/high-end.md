# High-end: what separates a top-tier site from a tidy one

A tidy page has good tokens, clean cards and a few reveals. A top-tier page
(the level of a studio-built site for a real place or product) feels
**directed**: every screen is a composed scene, the brand's own shape runs
through everything, and the product's real facts are shown as bespoke
visuals you can play with. This file is the bar. Read it before planning a
landing page or reviewing one.

Reference studied: a technology-park site built this way. It uses one
typeface (Montserrat), so the level does not come from fonts. Its level
comes from the eight things below. Don't copy that site's look; copy *how*
it is made.

## Studying a reference

When the user gives a site ("bu seviyede", "bu tarzda"), measure it before
describing it. Open it at 1440×900, scroll to the bottom once (pinned and
lazy parts mount), back to the top, then run `scripts/study.js` in the page
(read the file, pass it to the browser tool's JS runner). It returns the
scene list with heights, pins and surfaces, the type scale (display px,
scale jump, eyebrow labels), palette by area, motion stack (GSAP /
ScrollTrigger / Lenis / CSS scroll timelines / view transitions), hover and
focus rule counts, and chrome. Screenshot each scene too.

Write down what it teaches, row by row of the level check below ("8 sahne,
3'ü sabitlenmiş; ölçek sıçraması 5×; Lenis + ScrollTrigger; 155 hover
kuralı"), and what you will *not* take (palette, fonts, layout, its
metaphors). Without a browser tool, fetch the HTML and its CSS and read
them for the same facts; say the study was partial.

## 1. Scenes, not sections

Plan the page as 5–8 **scenes**. A scene fills the viewport and says one
thing. Write the plan before any code, one line per scene:

`scene | the visitor's question it answers | composition | what moves | real data used`

- Every scene answers a question a visitor really has, in the order they
  have it (What is this? Is it for me? Where / how does it work? What does
  it cost? How do I start?). A scene with no question is cut.
- **No two adjacent scenes share a composition.** Compositions to choose
  from: full-bleed image with type over it · centred statement on a plain
  field · split (sticky text / moving visual) · index list + large preview ·
  bespoke diagram or map · card grid · single big number · stacked cards ·
  timeline. A page that is "heading + 3 cards" five times is the tidy level.
- Long stories become **pinned sequences**: the scene stays, its content
  steps through 3–6 states driven by scroll (steps on a map, floors of a
  building, stages of an order, items in a gallery). Show progress (01/05,
  a filling bar, an active list item).
- Surfaces follow a planned rhythm: light → brand colour → light → dark → …
  Write the rhythm into the plan. Full-bleed colour changes are what make a
  page feel edited instead of stacked.
- There is **no standard section list**. Pricing, FAQ, logos, CTA, footer
  appear only when this product needs them, in the form this product needs.

## 1b. One signature moment

Award juries reward one unforgettable moment over many effects. Pick the
scene where the product's main truth is shown and make it *the* moment;
everything else stays quieter so it can land.

Storyboard it before code, in three frames, each strong as a still image
(screenshots, slow devices and reduced motion all see a still):

- **Frame 0** (scene enters): what is already on screen, never empty.
- **Frame 1** (middle of the scroll / interaction): the change that
  explains something (the order splits into three carriers, the floor lifts
  off the plan, the map draws the route).
- **Frame 2** (settled): the conclusion the visitor should remember, with
  the real number or fact.

Then say what drives it (scroll scrub, pointer, time) and how it reads on
a phone. Build it with `motion-engine.md`. If a frame looks weak as a
still, the moment is weak; fix the frame, not the easing.

## 2. The brand mark as a graphic system

Take one shape from the product's own identity (the logo's geometry, the
product's object: a chevron, a wave, a grid cell, a ticket edge, a plate
outline) and make it the system:

- image mask in the hero, background pattern on cards, divider, loader,
  active-state indicator, bullet, cursor or scroll cue;
- drawn with SVG so it scales and animates (stroke draw, morph, slide).

One motif used ten times reads as a brand. Ten unrelated effects read as a
template. If the logo gives nothing, take the shape from the product's
metaphor (`direction-finding.md`).

## 3. Art direction: real pictures of the real thing

- Photographs of the actual place, product, people or work, cropped with
  intent (subject off-centre, room for type, consistent colour grade).
  Look for them in the project (`public/`, `storage/`, `assets/`, the
  current site) and use them.
- No photos? Then bespoke visuals built from the product: the real UI in a
  frame, an isometric or flat SVG diagram of the real thing, a map with the
  real locations. Never stock-photo filler or emoji icons.
- If images are needed and missing, say which ones (subject, crop, ratio)
  in the reply and leave a clearly marked, well-proportioned placeholder.
  Don't generate fake people or fake places.

## 4. Real facts as bespoke, interactive visuals

The strongest scenes turn the product's real numbers into something you can
explore, instead of a stat card:

- a floor plan with a legend of room types and counts, tabs per floor;
- a map with routes drawn to real destinations and distance chips;
- an order travelling through the real stages with real durations;
- a price that recalculates from the visitor's own numbers.

One or two of these per page. Each must use real data from the project and
work with keyboard and touch.

## 5. Interface chrome that shows care

Small persistent details carry the "expensive" feel:

- a nav that changes state on scroll (compact, glass, active section marked);
- a section index or progress (01/07, rail of icons, thin bar);
- eyebrow labels above headings (short, tracked caps, sometimes a number);
- units set properly: `m²`, `₺`, `%` smaller and raised, tabular figures;
- every card has a hover answer (arrow slides, surface shifts, image zooms
  1.03), every link a visible focus;
- a scroll cue on the first screen, a "back to top" that works.

Chrome must stay quiet: one accent colour, small type, never competing with
the scene.

Interaction details that separate the levels:

- **Cursor** (fine pointers only, `(hover: hover) and (pointer: fine)`):
  a small follower that grows over links and shows a verb ("Aç", "Sürükle")
  over draggable or media items. Never hide the system cursor without a
  follower; never on forms or panels.
- **Menu**: the mobile/overlay menu is a scene of its own: items rise in
  sequence, the current page is marked, focus is trapped and `Esc` closes.
- **Touch**: hover effects get a deliberate touch answer (a visible
  arrow, a tap state, an always-on caption), not a shrunken hover.
- **Section handover**: the outgoing scene leaves while the next arrives
  (overlap, shared element, colour wipe) instead of a hard edge; see
  `motion-engine.md` §3 and §6.
- **Magnetic / tilt / glow** effects: one family per site, on the elements
  that deserve attention, never on everything.

## 6. Typographic restraint and contrast

- One family is enough when weight, size and colour do the work. Two-line
  headings where the second line changes weight or colour are a device,
  not a default; pick the device per direction.
- Big jumps: display 64–120 px against 16–18 px body. Timid 36 px headings
  are the tidy level.
- Tight leading on display (0.95–1.05), generous on body (1.5–1.65), a
  measure of 55–70 characters.

## 7. Choreographed motion

- Motion is tied to scroll progress (scrubbed), not only fired once:
  images converge, lines draw, cards stack, numbers settle as you scroll.
- Within a scene, elements move in sequence with overlapping timing (title,
  then visual, then details; 80–150 ms apart), on one easing family.
- Smooth scrolling (Lenis or similar) is optional; if used, it must respect
  reduced motion and not break anchor links or keyboard scrolling.
- An intro/preloader only when the first screen loads heavy media, and
  under 1.5 s. Never on every visit (store a flag).

## 8. Finish

- No layout shift: images have sizes, fonts use `swap` with matched
  fallbacks.
- Images: modern formats, lazy below the fold, a blur-up or colour
  placeholder.
- Mobile is composed, not collapsed: pinned sequences become stacked steps
  or swipeable cards, maps get a list view, nothing needs hover.

## The footer is not a signature

The footer's job is navigation, contact, legal and a way back to the top.
A giant brand wordmark is one possible device, and it has been overused by
this skill. Use it only when the brand name itself is the direction's idea,
the user hasn't seen one in this project or recently (`learn.py recall`),
and you can say why in one sentence. Otherwise: a well-organised, quiet
footer.

## Level check (score before showing)

Score the board's page plan, or a built page, 0–2 on each:

| # | Question | 0 | 2 |
| --- | --- | --- | --- |
| 1 | Scenes | stacked sections, repeated layout | 5–8 scenes, no two adjacent alike |
| 2 | Motif | unrelated effects | one product shape used across the page |
| 3 | Pictures | stock, emoji, empty boxes | real photos or bespoke visuals of the real thing |
| 4 | Facts | stat cards | at least one explorable visual from real data |
| 5 | Chrome | default nav and links | stateful nav, index/progress, units, hovers |
| 6 | Type | timid scale | clear display/body jump, one emphasis device |
| 7 | Motion | one-shot fades only | scrubbed, sequenced, explains something; one signature moment storyboarded in 3 strong frames |
| 8 | Fresh | reuses this skill's recent moves | nothing from `recall`'s recent moves without a reason |

Under 12 of 16: improve the lowest rows before showing. Report the score in
one line ("Seviye kontrolü: 13/16, en zayıf: görseller, proje fotoğrafı
yok").
