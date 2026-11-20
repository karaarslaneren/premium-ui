# 3D and WebGL: a tier, not a default

Many award-winning sites use WebGL, but the good ones use it for atmosphere
and framing, not spectacle. It costs weight, battery and accessibility, so
it is an opt-in tier with a fallback.

## 1. When it earns its place

Use it only when one of these is true, and say which in the plan:

- The product is a **physical thing or place** whose shape matters
  (a building, a device, furniture, a vehicle, a campus): a model the
  visitor can turn or fly through explains it better than photos.
- The signature moment needs **depth or particles** that SVG/CSS can't
  carry (thousands of points becoming a map, a material changing).
- The user asked for it, and the audience is on desktop or recent phones.

Otherwise: SVG, CSS 3D transforms (`perspective`, `rotateX/Y`) and
scroll-scrubbed images give 80 % of the effect at 5 % of the cost.

## 2. Stack

- **three.js** (most common), or **React Three Fiber** + drei in React
  projects; **OGL** when you need tiny shaders without a scene graph.
- Models: glTF/GLB, Draco- or Meshopt-compressed, textures as KTX2;
  bake lighting and shadows into textures instead of computing them live.
- Drive the camera with the same scroll timeline as the DOM (GSAP
  timeline → camera position/target keys), so 3D and text move as one.

## 3. Budget and tiers

| Tier | Detect | What runs |
| --- | --- | --- |
| High | desktop, `navigator.hardwareConcurrency >= 8`, no `saveData` | full model, post-processing, particles |
| Mid | recent phone / laptop | reduced DPR (`Math.min(devicePixelRatio, 1.5)`), no post-processing, fewer particles |
| Low / fallback | no WebGL2, `prefers-reduced-motion`, `saveData`, low memory, failed context | a still render (pre-rendered image/video poster) and the normal HTML content |

- Per-frame work under ~4 ms; pause the render loop when the canvas is off
  screen (IntersectionObserver) or the tab is hidden.
- Load the 3D chunk lazily after first paint; the LCP element is never the
  canvas. Total 3D payload under ~2 MB.
- Measure with DevTools at 4× CPU slowdown; if it drops below ~50 fps,
  move down a tier.

## 4. Accessibility and content

- The canvas is decoration or illustration: `aria-hidden="true"` with the
  information also in HTML (labels, list of floors, the numbers).
- Pointer-driven rotation needs keyboard controls or is purely ambient.
- Reduced motion: still render, no camera flights.
- Text never lives only inside the canvas.

## 5. Log it

`learn.py build … --moves webgl-scene` so later projects see it was used
and don't reach for it by habit.
