// premium-ui page audit. Paste the whole file into the browser tool's
// JavaScript runner (or DevTools console) on the page under test; the last
// expression is the JSON report. Run it after animations have settled, once
// at 1440×900 and once at 375×812, light and dark.
//
// Deterministic checks: horizontal overflow, small hit areas, text contrast
// (WCAG AA), infinite animations under reduced motion, non-composited
// animated properties, images without alt / size, fonts without swap,
// document basics, performance (LCP, CLS, weight, long frames; lab numbers, warn only).
// Heuristic: focus styles (confirm with the Tab key).
(() => {
  const MAX = 12; // items listed per check
  if (!innerWidth || !innerHeight || document.visibilityState === 'hidden') {
    return { error: `page is not visible (viewport ${innerWidth}×${innerHeight}, ${document.visibilityState}): bring the tab to the front and run again` };
  }
  const vw = document.documentElement.clientWidth;
  const report = { url: location.href, viewport: `${innerWidth}×${innerHeight}`, reducedMotion: matchMedia('(prefers-reduced-motion: reduce)').matches, checks: {} };

  const sel = (el) => {
    if (!el || el === document) return 'document';
    let s = el.tagName.toLowerCase();
    if (el.id) return `${s}#${el.id}`;
    const cls = [...el.classList].filter((c) => !/[:[\]/]/.test(c)).slice(0, 3);
    if (cls.length) s += '.' + cls.join('.');
    const text = (el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 40);
    return text ? `${s} "${text}"` : s;
  };
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return false;
    const cs = getComputedStyle(el);
    return cs.visibility !== 'hidden' && cs.display !== 'none';
  };
  const add = (name, status, items = [], note) => {
    report.checks[name] = { status, count: items.length, items: items.slice(0, MAX), ...(note ? { note } : {}) };
  };

  // Colour parsing through canvas handles rgb(), oklch(), color(), named colours.
  const ctx = Object.assign(document.createElement('canvas'), { width: 1, height: 1 }).getContext('2d', { willReadFrequently: true });
  const cache = new Map();
  const rgba = (str) => {
    if (cache.has(str)) return cache.get(str);
    ctx.clearRect(0, 0, 1, 1);
    ctx.fillStyle = '#000'; ctx.fillStyle = str;
    ctx.fillRect(0, 0, 1, 1);
    const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data;
    const out = { r, g, b, a: a / 255 };
    cache.set(str, out);
    return out;
  };
  const over = (top, bottom) => ({
    r: top.r * top.a + bottom.r * (1 - top.a),
    g: top.g * top.a + bottom.g * (1 - top.a),
    b: top.b * top.a + bottom.b * (1 - top.a), a: 1,
  });
  const lum = ({ r, g, b }) => {
    const f = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };

  // 1. Horizontal overflow
  {
    const items = [];
    const clipped = (el) => {
      for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
        if (/(hidden|auto|scroll|clip)/.test(getComputedStyle(p).overflowX)) return true;
      }
      return false;
    };
    if (document.documentElement.scrollWidth > vw) {
      const seen = new Set();
      for (const el of document.body.querySelectorAll('*')) {
        if (items.length >= MAX) break;
        if ([...seen].some((s) => s.contains(el))) continue;
        const r = el.getBoundingClientRect();
        if (r.width && r.right > vw + 1 && !clipped(el)) { seen.add(el); items.push(`${sel(el)} right=${Math.round(r.right)} > ${vw}`); }
      }
    }
    add('horizontalOverflow', document.documentElement.scrollWidth > vw ? 'fail' : 'pass', items,
      `scrollWidth ${document.documentElement.scrollWidth} vs viewport ${vw}`);
  }

  // 2. Hit areas ≥ 22px. Exempt (as in WCAG 2.5.8): inline links inside running
  // text, and small targets with enough free space — a 22×22 box centred on
  // the target touches no other target.
  const focusables = [...document.querySelectorAll('a[href], button, input:not([type=hidden]), select, textarea, summary, [role=button], [role=tab], [role=switch], [tabindex]:not([tabindex="-1"])')]
    .filter((el) => visible(el) && !el.disabled);
  {
    const items = [], roomy = [];
    const rects = focusables.map((el) => [el, el.getBoundingClientRect()]);
    const spaced = (el, r) => {
      const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
      const box = { left: Math.min(r.left, cx - 11), right: Math.max(r.right, cx + 11), top: Math.min(r.top, cy - 11), bottom: Math.max(r.bottom, cy + 11) };
      return !rects.some(([o, q]) => o !== el && !o.contains(el) && !el.contains(o) && q.left < box.right && q.right > box.left && q.top < box.bottom && q.bottom > box.top);
    };
    for (const [el, r] of rects) {
      if (Math.min(r.width, r.height) >= 22) continue;
      if (el.tagName === 'A' && getComputedStyle(el).display === 'inline' && (el.parentElement?.innerText || '').length > (el.innerText || '').length + 10) continue;
      if (el.type === 'checkbox' || el.type === 'radio') { const label = el.closest('label') || (el.id && document.querySelector(`label[for="${el.id}"]`)); if (label && Math.min(label.getBoundingClientRect().height, 99) >= 22) continue; }
      (spaced(el, r) ? roomy : items).push(`${sel(el)} ${Math.round(r.width)}×${Math.round(r.height)}`);
    }
    add('hitAreas', items.length ? 'fail' : 'pass', items, 'targets under 22×22px that crowd other targets');
    add('smallTargets', roomy.length ? 'warn' : 'pass', roomy, 'under 22×22px but with free space around (allowed by WCAG 2.5.8); enlarge controls you own, e.g. with padding');
  }

  // Stylesheets we cannot read (cross-origin) make the CSS-based checks below uncertain.
  const sheets = [...document.styleSheets].map((s) => { try { return s.cssRules; } catch { return null; } });
  const unreadable = sheets.filter((s) => !s).length;
  const walkRules = (fn) => { const walk = (list) => { for (const r of list) { fn(r); if (r.cssRules) walk(r.cssRules); } }; sheets.forEach((s) => s && walk(s)); };

  // 3. Text contrast (WCAG AA: 4.5, large text 3)
  {
    const items = []; let checked = 0, skipped = 0;
    const effectiveOpacity = (el) => { let o = 1; for (let p = el; p && p.nodeType === 1; p = p.parentElement) o *= +getComputedStyle(p).opacity; return o; };
    const MEDIA = new Set(['CANVAS', 'VIDEO', 'IMG', 'IFRAME', 'svg', 'PICTURE']);
    // Layers painted behind the text: what is really under its centre when it is
    // on screen (catches absolutely positioned backgrounds that aren't ancestors),
    // otherwise its ancestors. null = can't judge (image, gradient, media, unknown).
    const background = (el) => {
      const r = el.getBoundingClientRect();
      const cx = r.left + Math.min(r.width / 2, 12), cy = r.top + r.height / 2;
      const onScreen = cx >= 0 && cy >= 0 && cx < innerWidth && cy < innerHeight;
      let stack = [];
      if (onScreen) {
        const all = document.elementsFromPoint(cx, cy); const i = all.indexOf(el);
        // Covered by another layer with its own text or an opaque fill (e.g. a duplicate
        // heading used for an effect): what the reader sees isn't this element.
        const hasText = (p) => [...p.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
        if (all.slice(0, Math.max(i, 0)).some((p) => !el.contains(p) && (hasText(p) || rgba(getComputedStyle(p).backgroundColor).a >= 1))) return null;
        stack = i >= 0 ? all.slice(i) : [];
      }
      if (!stack.length) for (let p = el; p && p.nodeType === 1; p = p.parentElement) stack.push(p);
      const layers = []; let opaque = false;
      for (const p of stack) {
        if (p !== el && MEDIA.has(p.tagName)) return null;
        const cs = getComputedStyle(p);
        if (cs.backgroundImage !== 'none') return null;
        const c = rgba(cs.backgroundColor);
        if (c.a > 0) { layers.push(c); if (c.a >= 1) { opaque = true; break; } }
      }
      if (!opaque) {
        if (!onScreen) return null; // off-screen with no opaque ancestor: something else may paint it
        layers.push({ r: 255, g: 255, b: 255, a: 1 }); // canvas default
      }
      let color = layers[layers.length - 1];
      for (let i = layers.length - 2; i >= 0; i--) color = over(layers[i], color);
      return color;
    };
    // Text whose colour isn't what gets painted: gradient text, blend modes.
    const unmeasurable = (el) => {
      for (let p = el; p && p.nodeType === 1; p = p.parentElement) {
        const cs = getComputedStyle(p);
        if (cs.backgroundClip === 'text' || cs.webkitBackgroundClip === 'text' || cs.mixBlendMode !== 'normal') return true;
      }
      return rgba(getComputedStyle(el).webkitTextFillColor || 'black').a === 0;
    };
    const measure = (el) => {
      const bg = background(el);
      if (!bg) return null;
      const cs = getComputedStyle(el);
      const fg = over(rgba(cs.color), bg);
      const size = parseFloat(cs.fontSize), bold = +cs.fontWeight >= 700;
      const need = size >= 24 || (bold && size >= 18.66) ? 3 : 4.5;
      return { r: ratio(fg, bg), need, text: `${cs.color} on rgb(${Math.round(bg.r)} ${Math.round(bg.g)} ${Math.round(bg.b)})` };
    };
    const offScreen = (el) => { const r = el.getBoundingClientRect(); return r.bottom < 0 || r.top > innerHeight; };
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: (n) => n.textContent.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT });
    const els = new Set();
    while (walker.nextNode()) els.add(walker.currentNode.parentElement);
    const sx = scrollX, sy = scrollY;
    for (const el of els) {
      if (!visible(el) || el.closest('[aria-hidden="true"], script, style, noscript, svg')) continue;
      if (effectiveOpacity(el) < 0.99 || unmeasurable(el)) { skipped++; continue; } // mid-reveal, decorative, gradient/blended text
      let m = measure(el);
      // An off-screen failure may only look like one because whatever paints its
      // background isn't an ancestor: scroll it into view and measure what's really behind it.
      if (m && m.r < m.need && offScreen(el)) { el.scrollIntoView({ block: 'center', behavior: 'instant' }); m = measure(el); }
      if (!m) { skipped++; continue; }
      checked++;
      if (m.r < m.need) items.push(`${sel(el)} ${m.r.toFixed(2)}:1 (need ${m.need}) ${m.text}`);
    }
    scrollTo({ left: sx, top: sy, behavior: 'instant' });
    add('contrast', items.length ? 'fail' : 'pass', items, `${checked} text elements checked, ${skipped} skipped (image/gradient/media behind, gradient text, opacity < 1, or off-screen with an unknown background — scroll and re-run, and check those by eye)`);
  }

  // 4. Focus styles (heuristic: programmatic focus may not trigger :focus-visible everywhere)
  {
    const items = []; const prev = document.activeElement;
    const snap = (el) => { const cs = getComputedStyle(el); return [cs.outlineStyle, cs.outlineWidth, cs.outlineColor, cs.boxShadow, cs.borderColor, cs.backgroundColor, cs.textDecorationLine].join('|'); };
    // Selectors of authored :focus / :focus-visible rules, with the pseudo-class stripped,
    // so an element that has such a rule counts even if programmatic focus doesn't apply it.
    // A :focus-within rule on a wrapper (input inside a styled field) also counts for its descendants.
    const focusSelectors = [];
    const withinSelectors = [];
    walkRules((r) => { if (r.selectorText?.includes(':focus')) r.selectorText.split(',').filter((s) => s.includes(':focus')).forEach((s) => {
      const bare = s.replace(/:focus(-visible|-within)?/g, '').trim() || '*';
      (/:focus-within\s*$/.test(s.trim()) ? withinSelectors : focusSelectors).push(bare);
    }); });
    const hasRule = (el) => focusSelectors.some((s) => { try { return el.matches(s); } catch { return false; } })
      || withinSelectors.some((s) => { try { return !!el.closest(s); } catch { return false; } });
    for (const el of focusables.slice(0, 40)) {
      const before = snap(el);
      el.focus({ preventScroll: true, focusVisible: true });
      if (document.activeElement === el && snap(el) === before && !hasRule(el)) items.push(sel(el));
    }
    prev?.focus?.({ preventScroll: true });
    if (prev === document.body) document.activeElement?.blur?.();
    add('focusStyles', items.length ? (unreadable ? 'unverified' : 'warn') : 'pass', items,
      `no visible change on programmatic focus${unreadable ? ` (${unreadable} cross-origin stylesheets unreadable, so their :focus-visible rules could not be seen)` : ''} — confirm by pressing Tab in a real browser`);
  }

  // 5. Motion: infinite loops, reduced-motion support, animated layout properties
  {
    let reducedRule = false;
    walkRules((r) => { if (r.media && /prefers-reduced-motion/.test(r.media.mediaText)) reducedRule = true; });
    const anims = document.getAnimations().filter((a) => a.playState === 'running');
    const loops = anims.filter((a) => a.effect?.getTiming().iterations === Infinity);
    // Composited or paint-only properties; anything else (width, height, top, margin, max-height…) causes layout.
    const ok = new Set(['offset', 'composite', 'easing', 'computedOffset', 'transform', 'opacity', 'filter', 'backdropFilter', 'translate', 'scale', 'rotate', 'offsetDistance', 'offsetRotate', 'strokeDashoffset', 'strokeDasharray', 'clipPath', 'fill', 'stroke', 'boxShadow', 'textShadow', 'visibility', 'backgroundPosition', 'backgroundImage', 'maskPosition']);
    const paintOnly = (k) => ok.has(k) || /Color$/.test(k) || k === 'color' || k === 'all';
    const layout = [];
    for (const a of anims) {
      const keys = new Set((a.effect?.getKeyframes?.() || []).flatMap(Object.keys));
      if (a.transitionProperty) keys.add(a.transitionProperty.replace(/-([a-z])/g, (_, c) => c.toUpperCase()));
      const bad = [...keys].filter((k) => !paintOnly(k));
      if (bad.length) layout.push(`${sel(a.effect?.target)} animates ${bad.join(', ')}`);
    }
    const noRule = !reducedRule && anims.length;
    add('reducedMotion', report.reducedMotion && loops.length ? 'fail' : (noRule ? (unreadable ? 'unverified' : 'warn') : 'pass'),
      loops.map((a) => `${sel(a.effect?.target)} ${a.animationName || a.transitionProperty || 'WAAPI'} (infinite)`),
      `${reducedRule ? 'has' : 'no readable'} prefers-reduced-motion rule${unreadable ? ` (${unreadable} cross-origin stylesheets unreadable)` : ''}; ${anims.length} running animations, ${loops.length} infinite. Re-run with reduced motion emulated: infinite loops must be 0.`);
    add('layoutAnimations', layout.length ? 'warn' : 'pass', layout, 'animate transform/opacity/filter/stroke-dash only');
  }

  // 6. Images and fonts (CLS / LCP hygiene)
  {
    const imgs = [...document.images];
    add('imageAlt', imgs.some((i) => !i.hasAttribute('alt')) ? 'fail' : 'pass', imgs.filter((i) => !i.hasAttribute('alt')).map((i) => i.currentSrc || i.src), 'decorative images need alt=""');
    const unsized = imgs.filter((i) => !(i.getAttribute('width') && i.getAttribute('height')) && !getComputedStyle(i).aspectRatio.match(/\d/) && visible(i));
    add('imageSize', unsized.length ? 'warn' : 'pass', unsized.map((i) => i.currentSrc || i.src), 'set width/height or aspect-ratio to avoid layout shift');
    const lazyAbove = imgs.filter((i) => i.loading === 'lazy' && i.getBoundingClientRect().top < innerHeight && visible(i));
    add('lazyAboveFold', lazyAbove.length ? 'warn' : 'pass', lazyAbove.map((i) => i.currentSrc || i.src), 'above-the-fold (likely LCP) images should not be loading="lazy"');
    const fonts = [...document.fonts].filter((f) => f.status === 'loaded' && !['swap', 'optional', 'fallback'].includes(f.display));
    add('fontDisplay', fonts.length ? 'warn' : 'pass', fonts.map((f) => `${f.family} ${f.weight} display=${f.display}`), 'use font-display: swap (Google Fonts: &display=swap)');
  }

  // 6b. Performance (lab numbers from this load; warn only — confirm at 4× CPU slowdown in DevTools)
  {
    const take = (type) => { try { const o = new PerformanceObserver(() => {}); o.observe({ type, buffered: true }); const r = o.takeRecords(); o.disconnect(); return r; } catch { return []; } };
    const lcpE = take('largest-contentful-paint').at(-1);
    const cls = take('layout-shift').filter((e) => !e.hadRecentInput).reduce((s, e) => s + e.value, 0);
    const res = performance.getEntriesByType('resource');
    const kb = (f) => Math.round(res.filter(f).reduce((s, e) => s + (e.transferSize || e.encodedBodySize || 0), 0) / 1024);
    const nav = performance.getEntriesByType('navigation')[0];
    // long frames after load only: parsing and first render are covered by LCP
    const loaf = take('long-animation-frame').filter((e) => e.duration > 50 && e.startTime > (nav?.loadEventEnd || 0));
    const total = kb(() => true) + Math.round((nav?.transferSize || 0) / 1024);
    const js = kb((e) => e.initiatorType === 'script' || /\.m?js(\?|$)/.test(e.name));
    const img = kb((e) => e.initiatorType === 'img' || /\.(avif|webp|jpe?g|png|gif|svg)(\?|$)/.test(e.name));
    const font = kb((e) => /\.(woff2?|ttf|otf)(\?|$)/.test(e.name));
    const items = [];
    if (lcpE && lcpE.startTime > 2500) items.push(`LCP ${Math.round(lcpE.startTime)} ms (${sel(lcpE.element)}) > 2500`);
    if (cls > 0.05) items.push(`CLS ${cls.toFixed(3)} > 0.05`);
    if (total > 3072) items.push(`page weight ${total} kB > 3 MB`);
    if (js > 500) items.push(`JS ${js} kB > 500 kB`);
    if (loaf.length) items.push(`${loaf.length} long animation frames > 50 ms (longest ${Math.round(Math.max(...loaf.map((e) => e.duration)))} ms)`);
    if (document.querySelectorAll('*').length > 3000) items.push(`${document.querySelectorAll('*').length} DOM nodes > 3000`);
    add('performance', items.length ? 'warn' : 'pass', items,
      `lab: LCP ${lcpE ? Math.round(lcpE.startTime) + ' ms' : 'n/a'}, CLS ${cls.toFixed(3)}, weight ${total} kB (JS ${js}, img ${img}, fonts ${font}); cross-origin sizes may read 0. Scroll the page at 4× CPU slowdown before trusting it.`);
  }

  // 7. Document basics
  {
    const items = [];
    if (!document.documentElement.lang) items.push('<html> has no lang');
    if (!document.querySelector('meta[name=viewport]')) items.push('no viewport meta');
    if (!document.title.trim()) items.push('empty <title>');
    if (document.querySelectorAll('h1').length !== 1) items.push(`${document.querySelectorAll('h1').length} <h1> elements`);
    add('document', items.length ? 'warn' : 'pass', items);
  }

  const statuses = Object.values(report.checks).map((c) => c.status);
  report.summary = Object.fromEntries(['fail', 'warn', 'unverified', 'pass'].map((k) => [k, statuses.filter((s) => s === k).length]));
  return report;
})();
