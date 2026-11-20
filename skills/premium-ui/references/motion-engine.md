# Motion engine: scroll-linked, choreographed, continuous

`motion-catalog.md` covers single effects (a reveal, a counter, a packet on
a path). Top-tier sites go further: motion is **driven by scroll progress**,
several elements move on **one timeline**, and sections hand over to each
other like camera moves instead of hard cuts. This file is how.

## 1. Pick the engine

| Situation | Engine |
| --- | --- |
| Project already ships GSAP, or the page has 2+ pinned/scrubbed scenes | **GSAP + ScrollTrigger** (free for all use since 2025, plugins included) |
| No new dependency allowed, effects are simple (parallax, progress bar, fade with scroll) | **CSS scroll-driven animations** (`animation-timeline`), wrapped in `@supports` |
| Moving between pages or states (list → detail, tab → tab, filter) | **View Transitions API**, feature-detected |
| Smooth "weighted" scrolling | **Lenis**, optional, only with GSAP or for long editorial pages |
| A handful of one-shot reveals | the IntersectionObserver bootstrap in `motion-catalog.md`; no library |

Ask before adding a dependency to the user's project; say what it adds
(GSAP core + ScrollTrigger ≈ 45 kB gz, Lenis ≈ 4 kB gz). Install from npm
in the project; use a pinned CDN URL only on boards and static pages.

## 2. Choreography tokens

Write these next to the colour tokens. Every animation picks from them, so
the page moves with one personality.

```css
:root {
  --dur-micro: 160ms;   /* hover, press, focus */
  --dur-ui: 320ms;      /* menus, tabs, toasts */
  --dur-reveal: 900ms;  /* entrances */
  --dur-scene: 1400ms;  /* scene changes, hero intro */
  --stagger: 90ms;      /* between siblings: title → visual → details */
  --ease-out: cubic-bezier(.16, 1, .3, 1);     /* arrive */
  --ease-inout: cubic-bezier(.65, 0, .35, 1);  /* travel, camera moves */
  --ease-spring: cubic-bezier(.34, 1.56, .64, 1); /* land, snap */
}
```

The direction sets the personality: calm (longer, no spring), mechanical
(shorter, `steps()` or linear segments), playful (springs, overshoot).
Write the personality in one word in the plan.

**Sequence inside a scene:** eyebrow → headline (by line) → visual → body
→ actions, each `--stagger` apart, overlapping, never waiting for the
previous one to finish. Exits are faster than entrances (≈ 60 %).

## 3. GSAP + ScrollTrigger recipes

Setup once, respecting reduced motion and cleaning up on SPA navigation:

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

const mm = gsap.matchMedia();
mm.add({ full: '(prefers-reduced-motion: no-preference)', reduce: '(prefers-reduced-motion: reduce)' }, (ctx) => {
  if (ctx.conditions.reduce) return; // content is already visible; nothing animates
  heroIntro(); pinnedScene(); imageConverge();
  return () => {}; // matchMedia reverts every tween/trigger made here
});
```

**Master timeline per scene (scrub):** one timeline, many tracks, scroll
position 0→1 drives it. This is what makes scroll feel directed.

```js
function pinnedScene() {
  const tl = gsap.timeline({
    defaults: { ease: 'none' },
    scrollTrigger: { trigger: '#plan', start: 'top top', end: '+=300%', pin: true, scrub: 0.6,
                     snap: { snapTo: 'labels', duration: 0.4, ease: 'power2.inOut' } },
  });
  tl.addLabel('floor-0')
    .to('.plan-floor[data-f="0"]', { yPercent: -8, opacity: .35 })
    .from('.plan-floor[data-f="1"]', { yPercent: 12, opacity: 0 }, '<')
    .to('.legend [data-f="1"]', { '--on': 1 }, '<')       // legend follows the same clock
    .addLabel('floor-1')
    .to('.plan-progress', { scaleX: 1 }, 0);              // progress bar spans the whole timeline
}
```

- `scrub: 0.6` smooths the link to the scrollbar; `snap: 'labels'` settles
  on a meaningful state instead of between two.
- Pin with `pin: true` and let ScrollTrigger add the spacer; never pin an
  element whose ancestor has `overflow: hidden` or a transform.
- Mobile: `mm.add('(max-width: 767px)', …)` with a shorter `end`, or no pin
  at all (stacked steps).

**Image converge / scatter** (photos fly in from the edges and settle
around a statement, as in a gallery wall):

```js
gsap.utils.toArray('.converge img').forEach((img, i) => {
  gsap.from(img, { x: () => gsap.utils.random(-40, 40) + 'vw', y: () => gsap.utils.random(-30, 30) + 'vh',
    rotate: gsap.utils.random(-12, 12), scale: .6, ease: 'none',
    scrollTrigger: { trigger: '.converge', start: 'top bottom', end: 'center center', scrub: 1 } });
});
```

**Headline by lines/words:** GSAP SplitText (free) with `mask: 'lines'`,
or split by hand into `<span>` lines; animate `yPercent: 110 → 0` with
`--stagger`. Keep the real text in the DOM once (`aria-label` on the
heading if you duplicate it).

**Velocity-aware motion:** fast flicks shouldn't trigger long
choreography. Read `self.getVelocity()` in `onUpdate`; above ~2500 px/s,
jump to the end state (`tl.progress(1)`) instead of playing the entrance.

## 4. Lenis (optional smooth scroll)

```js
import Lenis from 'lenis';
const lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((t) => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0);
```

Only with `(prefers-reduced-motion: no-preference)`. Check that anchor
links (`lenis.scrollTo(hash)`), keyboard scrolling (Space, PgDn) and
scrollable children (`data-lenis-prevent`) still work. Never on panels.

## 5. CSS scroll-driven animations (no library)

For progress bars, parallax and "reveal while crossing the viewport":

```css
@supports (animation-timeline: view()) {
  @media (prefers-reduced-motion: no-preference) {
    .reveal { animation: rise linear both; animation-timeline: view(); animation-range: entry 0% cover 30%; }
    .parallax { animation: drift linear both; animation-timeline: view(); }
    .read-progress { transform-origin: left; animation: grow linear both; animation-timeline: scroll(root); }
  }
}
@keyframes rise { from { opacity: 0; transform: translateY(40px); } }
@keyframes drift { from { transform: translateY(-8%); } to { transform: translateY(8%); } }
@keyframes grow { from { transform: scaleX(0); } }
```

Browsers without support show the end state (no `@supports` match), which
is the correct fallback. Named timelines (`scroll-timeline-name`,
`view-timeline-name` + `timeline-scope`) let one element's scroll drive
another's animation, enough for a simple pinned scene with `position:
sticky`.

## 6. Page and state transitions (View Transitions)

Between states on one page (filter, tab, list → detail in an SPA):

```js
function go(update) {
  if (!document.startViewTransition || matchMedia('(prefers-reduced-motion: reduce)').matches) return update();
  document.startViewTransition(update);
}
```
```css
.card-photo { view-transition-name: var(--vt, none); } /* set --vt per item: photo-12 */
::view-transition-old(root), ::view-transition-new(root) { animation-duration: var(--dur-ui); }
```

Between pages of a multi-page site (Laravel, plain HTML): `@view-transition
{ navigation: auto; }` in both pages' CSS; shared elements get the same
`view-transition-name`. Unsupported browsers just navigate. Livewire
`wire:navigate`, Next.js and Nuxt have their own hooks; see the stack file.

Give each transition a meaning: the clicked card's image *becomes* the
detail hero; a tab's content slides in the direction of the tab. No
cross-fade-everything.

## 7. Budget and checks

- Animate only transform, opacity, filter, clip-path, and CSS variables
  that feed them. `scrub` tweens of `width/height/top/left` are the most
  common cause of jank on scroll.
- One scrubbed scene active at a time; kill or pause triggers off-screen
  (`toggleActions`, `ScrollTrigger.batch`).
- After building, scroll the whole page at 4× CPU slowdown (DevTools) and
  run `verify.js` (its `performance` block). Long tasks over 50 ms during
  scroll → simplify that scene.
- Log the moves you used with `learn.py build` (`scroll-scrub`,
  `pinned-steps`, `view-transition`, `smooth-scroll`, `split-lines`,
  `image-converge`…).
