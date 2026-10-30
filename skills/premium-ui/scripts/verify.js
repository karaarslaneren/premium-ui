// premium-ui page audit. Paste the whole file into the browser tool's
// JavaScript runner (or DevTools console) on the page under test; the last
// expression is the JSON report. Run it after animations have settled, once
// at 1440×900 and once at 375×812, light and dark.
//
// Deterministic checks: horizontal overflow, small hit areas, text contrast
// (WCAG AA), infinite animations under reduced motion, non-composited
// animated properties, images without alt / size, fonts without swap,
// document basics. Heuristic: focus styles (confirm with the Tab key).
(() => {
  const MAX = 12; // items listed per check
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

  // 2. Hit areas ≥ 22px (inline links inside running text are exempt)
  const focusables = [...document.querySelectorAll('a[href], button, input:not([type=hidden]), select, textarea, summary, [role=button], [role=tab], [role=switch], [tabindex]:not([tabindex="-1"])')]
    .filter((el) => visible(el) && !el.disabled);
  {
    const items = [];
    for (const el of focusables) {
      const r = el.getBoundingClientRect();
      if (Math.min(r.width, r.height) >= 22) continue;
      if (el.tagName === 'A' && getComputedStyle(el).display === 'inline' && (el.parentElement?.innerText || '').length > (el.innerText || '').length + 10) continue;
      if (el.type === 'checkbox' || el.type === 'radio') { const label = el.closest('label') || (el.id && document.querySelector(`label[for="${el.id}"]`)); if (label && Math.min(label.getBoundingClientRect().height, 99) >= 22) continue; }
      items.push(`${sel(el)} ${Math.round(r.width)}×${Math.round(r.height)}`);
    }
    add('hitAreas', items.length ? 'fail' : 'pass', items, 'interactive targets need ≥ 22×22px');
  }

  // 3. Text contrast (WCAG AA: 4.5, large text 3)
  {
    const items = []; let checked = 0, skipped = 0;
    const effectiveOpacity = (el) => { let o = 1; for (let p = el; p && p.nodeType === 1; p = p.parentElement) o *= +getComputedStyle(p).opacity; return o; };
    const background = (el) => {
      let color = { r: 0, g: 0, b: 0, a: 0 };
      const layers = [];
      for (let p = el; p && p.nodeType === 1; p = p.parentElement) {
        const cs = getComputedStyle(p);
        if (cs.backgroundImage !== 'none') return null; // gradient / image: cannot judge
        const c = rgba(cs.backgroundColor);
        if (c.a > 0) { layers.push(c); if (c.a >= 1) break; }
      }
      layers.push({ r: 255, g: 255, b: 255, a: 1 }); // canvas default
      for (let i = layers.length - 1; i >= 0; i--) color = i === layers.length - 1 ? layers[i] : over(layers[i], color);
      return color;
    };
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, { acceptNode: (n) => n.textContent.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT });
    const els = new Set();
    while (walker.nextNode()) els.add(walker.currentNode.parentElement);
    for (const el of els) {
      if (!visible(el) || el.closest('[aria-hidden="true"], script, style, noscript, svg')) continue;
      if (effectiveOpacity(el) < 0.99) { skipped++; continue; } // mid-reveal or decorative
      const bg = background(el);
      if (!bg) { skipped++; continue; }
      const cs = getComputedStyle(el);
      const fg = over(rgba(cs.color), bg);
      const size = parseFloat(cs.fontSize), bold = +cs.fontWeight >= 700;
      const need = size >= 24 || (bold && size >= 18.66) ? 3 : 4.5;
      const r = ratio(fg, bg); checked++;
      if (r < need) items.push(`${sel(el)} ${r.toFixed(2)}:1 (need ${need}) ${cs.color} on rgb(${Math.round(bg.r)} ${Math.round(bg.g)} ${Math.round(bg.b)})`);
    }
    add('contrast', items.length ? 'fail' : 'pass', items, `${checked} text elements checked, ${skipped} skipped (gradient/image background or opacity < 1 — check those by eye)`);
  }

  // 4. Focus styles (heuristic: programmatic focus may not trigger :focus-visible everywhere)
  {
    const items = []; const prev = document.activeElement;
    const snap = (el) => { const cs = getComputedStyle(el); return [cs.outlineStyle, cs.outlineWidth, cs.outlineColor, cs.boxShadow, cs.borderColor, cs.backgroundColor, cs.textDecorationLine].join('|'); };
    // Selectors of authored :focus / :focus-visible rules, with the pseudo-class stripped,
    // so an element that has such a rule counts even if programmatic focus doesn't apply it.
    const focusSelectors = [];
    const collect = (list) => { for (const r of list) { if (r.selectorText?.includes(':focus')) r.selectorText.split(',').filter((s) => s.includes(':focus')).forEach((s) => focusSelectors.push(s.replace(/:focus(-visible|-within)?/g, '').trim() || '*')); if (r.cssRules) collect(r.cssRules); } };
    for (const s of document.styleSheets) { try { collect(s.cssRules); } catch { /* cross-origin */ } }
    const hasRule = (el) => focusSelectors.some((s) => { try { return el.matches(s); } catch { return false; } });
    for (const el of focusables.slice(0, 40)) {
      const before = snap(el);
      el.focus({ preventScroll: true, focusVisible: true });
      if (document.activeElement === el && snap(el) === before && !hasRule(el)) items.push(sel(el));
    }
    prev?.focus?.({ preventScroll: true });
    if (prev === document.body) document.activeElement?.blur?.();
    add('focusStyles', items.length ? 'warn' : 'pass', items, 'no visible change on focus — confirm by pressing Tab in a real browser');
  }

  // 5. Motion: infinite loops, reduced-motion support, animated layout properties
  {
    const rules = { reduced: false, unreadable: 0 };
    const walk = (list) => { for (const r of list) { if (r.media && /prefers-reduced-motion/.test(r.media.mediaText)) rules.reduced = true; if (r.cssRules) walk(r.cssRules); } };
    for (const s of document.styleSheets) { try { walk(s.cssRules); } catch { rules.unreadable++; } }
    const anims = document.getAnimations().filter((a) => a.playState === 'running');
    const loops = anims.filter((a) => a.effect?.getTiming().iterations === Infinity);
    const ok = new Set(['offset', 'composite', 'easing', 'computedOffset', 'transform', 'opacity', 'filter', 'translate', 'scale', 'rotate', 'offsetDistance', 'offsetRotate', 'strokeDashoffset', 'strokeDasharray', 'clipPath', 'color', 'backgroundColor', 'borderColor', 'fill', 'stroke', 'boxShadow', 'visibility', 'backgroundPosition']);
    const layout = [];
    for (const a of anims) {
      const keys = new Set((a.effect?.getKeyframes?.() || []).flatMap(Object.keys));
      if (a.transitionProperty) keys.add(a.transitionProperty.replace(/-([a-z])/g, (_, c) => c.toUpperCase()));
      const bad = [...keys].filter((k) => !ok.has(k));
      if (bad.length) layout.push(`${sel(a.effect?.target)} animates ${bad.join(', ')}`);
    }
    add('reducedMotion', report.reducedMotion && loops.length ? 'fail' : (!rules.reduced && anims.length ? 'warn' : 'pass'),
      loops.map((a) => `${sel(a.effect?.target)} ${a.animationName || a.transitionProperty || 'WAAPI'} (infinite)`),
      `${rules.reduced ? 'has' : 'NO'} prefers-reduced-motion rule${rules.unreadable ? ` (${rules.unreadable} cross-origin sheets unreadable)` : ''}; ${anims.length} running animations, ${loops.length} infinite. Re-run with reduced motion emulated: infinite loops must be 0.`);
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
  report.summary = { fail: statuses.filter((s) => s === 'fail').length, warn: statuses.filter((s) => s === 'warn').length, pass: statuses.filter((s) => s === 'pass').length };
  return report;
})();
