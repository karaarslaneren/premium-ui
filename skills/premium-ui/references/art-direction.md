# Art direction: pictures and type that carry the page

Motion lands only when the pictures are already strong. This file covers
what to do with the images a project has, what to ask for when it has
none, how to draw product visuals from real data, and how to make type
itself the image.

## 1. Inventory first

Before designing, list every usable visual in the project: `public/`,
`storage/app/public`, `assets/`, `static/`, CMS uploads, the live site, the
logo files (prefer SVG). For each: subject, size, ratio, quality (sharp?
noisy? watermark?). Note what's missing for the scene plan.

## 2. One treatment for every image

Photos from different sources look like a scrapbook. Give them one
treatment, chosen with the direction, applied in CSS so originals stay
untouched:

| Treatment | How | Suits |
| --- | --- | --- |
| Colour grade | `filter: saturate(.85) contrast(1.05) sepia(.08)` + a tinted overlay with `mix-blend-mode: soft-light` | warm, editorial, places |
| Duotone | grayscale image + two-colour gradient overlay with `mix-blend-mode: color` (or an SVG `feColorMatrix`) | bold, brand-heavy |
| Monochrome + accent | grayscale photos, one accent element in colour | serious, technical |
| Grain | SVG `feTurbulence` noise at 4–8 % opacity on top | film, craft, food |
| Brand-shape mask | `mask-image` / `clip-path: path()` with the motif from `high-end.md` §2 | everywhere the motif lives |

Crops follow intent: subject off-centre on the thirds, clear space where
type will sit, the same horizon height across a series. Set `object-fit:
cover` with an explicit `object-position` per image; never let the browser
centre a face out of frame.

Loading: modern formats (AVIF/WebP via the framework's image component),
explicit `width`/`height`, lazy below the fold, a blurred or dominant-colour
placeholder that matches the grade.

## 3. No photos? Write a shot list, then draw

Never fill gaps with stock or generated people. Two things instead:

**A shot list in the reply**, so the user can get real photos:

```
Çekim listesi (Kargonet)
1. Hero — depoda raf arası, paketleyen eller, yatay 16:9, sağ üçte biri boş (başlık için), gün ışığı.
2. Kurye teslim anı — kapı eşiği, yüz yok, dikey 4:5.
3. Ekip — 3–5 kişi masada ekran başında, doğal, 3:2.
```

**Bespoke visuals from the product**, until photos arrive (and often
better than photos):

- **The real UI**, framed: screenshot the product's own screens (or
  rebuild the key widget in HTML with real data) inside a device or window
  frame that uses the direction's shape.
- **Diagrams from real data**, in SVG: a floor plan from room data, a map
  from coordinates, a flow from the actual pipeline steps, a timeline from
  real durations. Isometric works for buildings, warehouses and stacks
  (`transform: rotateX(55deg) rotateZ(-45deg)` on a flat SVG, or draw in
  isometric coordinates).
- **Objects of the product's world** drawn simply in the brand shape: a
  ticket, a parcel label, a plate, a receipt; one illustration style
  (stroke weight, corner radius, fill rule) for all of them.

Placeholders that must remain are honest and well-proportioned: the right
ratio, the grade colour, a small label ("Fotoğraf: depo, 16:9").

## 4. Type as image

When there are no pictures, or as the signature moment, type carries the
page:

- **Kinetic headline:** lines rise from a mask, a word swaps through the
  product's real values ("Trendyol → Hepsiburada → n11"), a number counts
  to the real figure. One per page.
- **Variable fonts:** animate `font-variation-settings` / `font-weight`
  with scroll or hover (weight 300 → 800 as a word comes into focus).
  Choose a variable face in `type-library.md` and load the axis range
  you use.
- **Scale as composition:** a single word at 18–30vw cropped by the
  viewport, or a number set huge with its unit small. Make it a scene's
  idea, not the footer's decoration (`high-end.md`, footer note).
- **Outline / fill play:** outline text that fills as you scroll (a
  `background-clip: text` gradient whose stop moves with scroll progress).

Keep real text real: selectable, translated, in the accessibility tree once.

## 5. Check

Look at the screenshots of the image-heavy scenes next to each other: do
they read as one series (same grade, same crop logic, same motif)? If one
image breaks the series, re-treat or replace it before showing.
