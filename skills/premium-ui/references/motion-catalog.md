# Motion catalog

Each entry: what it is, when it earns its place, and minimal vanilla code.
All snippets assume these tokens:

```css
:root {
  --ease: cubic-bezier(.16, 1, .3, 1);
  --spring: cubic-bezier(.34, 1.56, .64, 1);
}
```

And one shared bootstrap that arms reveals only when JS works:

```js
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const fine = matchMedia('(pointer: fine)').matches; // mouse-only effects
if (!reduced && 'IntersectionObserver' in window) {
  document.body.classList.add('armed');
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: .1 });
  document.querySelectorAll('[data-reveal],[data-reveal-lines]').forEach((el) => io.observe(el));
}
```

---

## Scroll reveal (fade-up + blur-in)

Default entrance for blocks and cards. Stagger with `transition-delay`.

```css
.armed [data-reveal] { opacity: 0; transform: translateY(28px); filter: blur(6px); }
.armed [data-reveal].in { opacity: 1; transform: none; filter: none;
  transition: opacity .9s var(--ease), transform .9s var(--ease), filter .9s var(--ease); }
```

## Line mask reveal (headlines)

Each line slides up from behind its own mask. Use on section headings only.

```html
<h2 data-reveal-lines>
  <span class="line"><span>Bir kez bağlayın,</span></span>
  <span class="line"><span><em class="serif">her yerde</em> satın.</span></span>
</h2>
```
```css
.line { display: block; overflow: hidden; padding-bottom: .08em; margin-bottom: -.08em; }
.line > span { display: inline-block; }
.armed .line > span { transform: translateY(105%); }
.armed .in .line > span { transform: none; transition: transform 1.1s var(--ease); }
```
Set `transitionDelay = i * 120ms` per line when the heading enters.

## Count-up (number ticker)

For prices, stats, savings, results of a calculation. Count from the value
currently on screen, not from 0 and not from the last target: if the user
toggles again mid-count, the next count must start where the number is now
(track the displayed value in the step function, and cancel the previous
frame before starting).

```js
const fmt = new Intl.NumberFormat('tr-TR', { maximumFractionDigits: 0 });
function countTo(el, from, to, ms = 900) {
  if (reduced) { el.textContent = fmt.format(to); return; }
  const t0 = performance.now();
  const step = (now) => {
    const t = Math.min(1, (now - t0) / ms), k = 1 - Math.pow(1 - t, 4);
    el.textContent = fmt.format(from + (to - from) * k);
    if (t < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}
```

## SVG flow: line draw + packet along path

The strongest "explains the product" device: data/orders/messages moving
between nodes (source → engine → destination, then fan-out back).

- Draw: `stroke-dasharray = length; stroke-dashoffset = length → 0`.
- Packet: a circle moved with `path.getPointAtLength()` in rAF (easing in JS),
  or SMIL `<animateMotion><mpath href="#id"/></animateMotion>` for a
  zero-JS ambient loop (auth screens).
- Provide two SVGs with fixed viewBoxes — wide (md+) and tall (mobile) — and
  animate whichever is visible (`getBoundingClientRect().width > 0`).
- Pair it with a live log list (prepend items, keep 5) and a checklist of
  what the engine does at the hub; that turns motion into explanation.
- Run the loop only while the section is visible (IntersectionObserver).

```js
function packet(svg, path, color, reverse, ms) {
  return new Promise((done) => {
    const len = path.getTotalLength();
    const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('r', 7); dot.setAttribute('fill', color); svg.appendChild(dot);
    const t0 = performance.now();
    const step = (now) => {
      const t = Math.min(1, (now - t0) / ms);
      const k = t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      const p = path.getPointAtLength(len * (reverse ? 1 - k : k));
      dot.setAttribute('cx', p.x); dot.setAttribute('cy', p.y);
      t < 1 ? requestAnimationFrame(step) : (dot.remove(), done());
    };
    requestAnimationFrame(step);
  });
}
```

## Scroll-pinned story (scrollytelling, "kayarak ilerleyen")

Use for "how it works" with 3–6 steps. The section is tall
(`steps × 65vh + 100vh`); an inner `position: sticky; top: 0; height: 100svh`
frame stays put while scroll progress picks the step. Users prefer this to a
long column of steps that scrolls past.

```js
function progress(section) {
  const b = section.getBoundingClientRect();
  return Math.min(1, Math.max(0, -b.top / (b.height - innerHeight)));
}
// on scroll (rAF-batched): index = floor(p * n); sub = p * n - index
// track.style.transform = `translateX(${-index * 100}%)`;  // screens side by side
// active step: fade its text in (opacity + translateY), fill its bar by `sub` (scaleX)
```
- Step texts keep their space: render every step's body at full height and
  switch the active one with opacity/transform only. Don't expand bodies with
  `grid-template-rows: 0fr → 1fr`, `max-height` or `height` — those animate
  layout every frame and break the motion rule. Progress bars are
  `transform: scaleX(sub)` with `transform-origin: left`, not `width`.
- Without JS the section must still read as a normal list: put the sticky
  frame, the dimmed inactive screens and the hidden step bodies under
  `.armed` (added by JS), so the no-JS page shows every step stacked.
- Screens: a flex track of `flex: 0 0 100%` panels; inactive ones `opacity:.2; scale(.9); blur(3px)`.
- Give the grid column with the track `min-width: 0`, or the track's width
  blows out the grid.
- No ancestor of the sticky element may have `overflow: hidden`.
- Steps are buttons that scroll to the middle of their slice.
- Inside each screen, stagger children with `--i` and `transition-delay: calc(var(--i) * 110ms)` when the screen becomes active.

## Magnetic buttons

```js
if (fine && !reduced) document.querySelectorAll('[data-magnetic]').forEach((el) => {
  el.addEventListener('pointermove', (e) => {
    const b = el.getBoundingClientRect();
    el.style.transform = `translate(${(e.clientX - b.left - b.width / 2) * .18}px, ${(e.clientY - b.top - b.height / 2) * .3}px)`;
  });
  el.addEventListener('pointerleave', () => { el.style.transform = ''; });
});
```

## Cursor-follow glow (cards)

Border glow + soft fill that tracks the pointer. Set `--gx/--gy` on pointermove.

```css
.glow { position: relative; isolation: isolate; }
.glow::before { content: ''; position: absolute; inset: 0; border-radius: inherit; padding: 1px;
  background: radial-gradient(380px circle at var(--gx,-200px) var(--gy,-200px), rgb(20 184 166 / .55), transparent 45%);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none; }
```

## 3D tilt card + sheen

For one hero object (badge, card, device). `perspective` on the stage,
`rotateX/rotateY` from pointer position, a sheen gradient whose
`background-position` follows x, plus a slow `translate` sway loop.

## Sliding highlight / shared ring

A single absolutely positioned ring that glides (spring) to the selected item:
plan finder → matching pricing column, segmented control → pressed option.
Position from `offsetLeft/offsetTop/offsetWidth/offsetHeight` of the target;
recompute on resize and after `document.fonts.ready`.

## Segmented control

Pill group with a dark thumb that slides under `aria-pressed="true"`:
`transform: translateX(btn.offsetLeft - pad)`. If options differ in width,
size the thumb with `scaleX` from a fixed base width (and counter-scale its
content), or make the options equal width — transitioning `width` is a layout
animation.

## Interactive calculator / plan finder

The best "premium" moment is a tool that answers the buyer's question with
real rules: price after commission, which plan fits, savings per year.

- Mirror the product's real formula/limits (read config); write tests for it.
- Show the reason, not just the answer: "Profesyonel en fazla 6 pazaryeri
  hesabı içeriyor; Kurumsal 10 mağaza ve 20 hesaba kadar yetiyor." Numbers
  in the explanation must visibly add up with the numbers the user picked.
- With a server-driven framework it's fine to compute the answer on the
  server, as long as the slider value itself is echoed on the client so
  dragging feels instant (Livewire recipe in `stacks/laravel-livewire.md`).
- Range input: input height = thumb height, line drawn on the track
  pseudo-element (see pitfalls).

## Savings tag on period switch

When switching monthly → yearly: strike through the 12-month price, raise a
"X ₺ tasarruf" tag with spring, count it up from 0.

## Horizontal scroll-snap carousel (FAQ, testimonials, cases)

Track bleeds off the right edge, starts on the container's left edge:

```css
.track { --edge: max(1.25rem, calc((100vw - 80rem) / 2 + 2rem));
  padding-inline: var(--edge); scroll-padding-inline: var(--edge);
  display: flex; gap: 1rem; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; }
.track > * { scroll-snap-align: start; flex: 0 0 min(82vw, 400px); }
```
Arrows `scrollBy(cardStep)`, counter + progress bar from `scrollLeft`,
mouse drag via pointer capture (turn off snapping while dragging, re-snap on
release). Mark the nearest card `is-current` and lift it slightly.

## Giant wordmark footer

Brand name at ~22vw, `leading-[.78]`, cropped by `overflow:hidden`. Letters
rise in with stagger when the footer enters; text fill is a radial gradient
clipped to text whose centre follows the pointer.

## Ambient extras (use sparingly)

Slow blurred blobs (18s drift), film grain overlay (SVG turbulence, 5% opacity,
multiply), marquee for logos (40s linear), pinging status dot. Never more than
one ambient loop per viewport.
