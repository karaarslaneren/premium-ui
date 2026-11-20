// premium-ui reference study. Run inside a reference site's page (browser tool's JS runner)
// after it has loaded, at 1440×900, scrolled to the top. Returns JSON describing HOW the site
// is made — scenes, type scale, palette, motion stack, chrome — so it can be learned from
// without copying its look. See references/high-end.md ("Studying a reference").
(() => {
  const vh = innerHeight;
  const ctx = Object.assign(document.createElement('canvas'), { width: 1, height: 1 }).getContext('2d', { willReadFrequently: true });
  const rgb = (s) => { ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = '#000'; ctx.fillStyle = s; ctx.fillRect(0, 0, 1, 1); const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data; return { r, g, b, a: a / 255 }; };
  const hex = ({ r, g, b }) => '#' + [r, g, b].map((v) => v.toString(16).padStart(2, '0')).join('');
  const lum = ({ r, g, b }) => (Math.max(r, g, b) + Math.min(r, g, b)) / 510;
  const visible = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const all = [...document.querySelectorAll('body *')].filter(visible);

  // --- type ---
  const fam = {}, sizes = [];
  for (const el of all) {
    if (![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) continue;
    const cs = getComputedStyle(el);
    const f = cs.fontFamily.split(',')[0].replace(/["']/g, '').trim();
    const px = parseFloat(cs.fontSize);
    fam[f] = (fam[f] || 0) + 1;
    sizes.push({ px, w: cs.fontWeight, lh: +(parseFloat(cs.lineHeight) / px || 0).toFixed(2), ls: cs.letterSpacing, tt: cs.textTransform, f });
  }
  sizes.sort((a, b) => b.px - a.px);
  const body = sizes.map((s) => s.px).sort((a, b) => a - b)[Math.floor(sizes.length / 2)] || 16;
  const display = sizes[0] || {};
  const eyebrows = sizes.filter((s) => s.tt === 'uppercase' && s.px <= 14 && parseFloat(s.ls) > 0.5).length;

  // --- palette (by painted area) ---
  const area = {};
  for (const el of all) {
    const c = rgb(getComputedStyle(el).backgroundColor);
    if (c.a < 0.5) continue;
    const r = el.getBoundingClientRect(); const k = hex(c);
    area[k] = (area[k] || 0) + r.width * Math.min(r.height, vh * 3);
  }
  const palette = Object.entries(area).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([k]) => k);

  // --- motion stack ---
  const html = document.documentElement;
  const libs = {
    gsap: !!window.gsap, scrollTrigger: !!window.ScrollTrigger || !!document.querySelector('.pin-spacer'),
    lenis: !!window.lenis || !!window.Lenis || html.classList.contains('lenis'),
    locomotive: !!document.querySelector('[data-scroll-container]'),
    three: !!window.THREE, // getContext() would create a context, so large canvases are only counted
    largeCanvases: [...document.querySelectorAll('canvas')].filter((c) => c.getBoundingClientRect().width > innerWidth * 0.3).length,
    swiper: !!document.querySelector('.swiper'), barba: !!document.querySelector('[data-barba]'),
    lottie: !!document.querySelector('lottie-player, dotlottie-player, [data-animation-path]'),
    video: document.querySelectorAll('video').length,
  };
  let hover = 0, focus = 0, keyframes = 0, viewTimeline = 0, viewTransitions = 0, unreadable = 0, cursorNone = false;
  for (const sheet of document.styleSheets) {
    let rules; try { rules = sheet.cssRules; } catch { unreadable++; continue; }
    const walk = (list) => { for (const r of list) {
      if (r.cssRules) walk(r.cssRules);
      if (r.type === 7) keyframes++;
      const t = r.cssText || '';
      if (r.selectorText?.includes(':hover')) hover++;
      if (r.selectorText?.includes(':focus')) focus++;
      if (/animation-timeline|view-timeline|scroll-timeline/.test(t)) viewTimeline++;
      if (/view-transition/.test(t)) viewTransitions++;
      if (/cursor:\s*none/.test(t)) cursorNone = true;
    } };
    walk(rules);
  }

  // --- scenes ---
  const main = document.querySelector('main') || document.body;
  let blocks = [...main.children].filter(visible);
  if (blocks.length < 3) blocks = [...document.querySelectorAll('section')].filter(visible);
  const scenes = blocks.slice(0, 30).map((el) => {
    const r = el.getBoundingClientRect();
    const target = el.classList.contains('pin-spacer') ? el.firstElementChild || el : el;
    let c = { r: 255, g: 255, b: 255, a: 1 };
    for (let p = target; p; p = p.parentElement) { const x = rgb(getComputedStyle(p).backgroundColor); if (x.a > 0.5) { c = x; break; } }
    const imgs = target.querySelectorAll('img, picture, video, canvas, svg').length;
    const big = [...target.querySelectorAll('img, video, canvas')].some((m) => m.getBoundingClientRect().width > innerWidth * 0.6);
    const grid = target.querySelector('[class*=grid], ul, ol');
    const cols = grid ? new Set([...grid.children].slice(0, 12).map((ch) => Math.round(ch.getBoundingClientRect().left))).size : 0;
    const sticky = !!target.querySelector('*') && [...target.querySelectorAll('*')].slice(0, 400).some((d) => getComputedStyle(d).position === 'sticky');
    const heading = target.querySelector('h1, h2, h3');
    return {
      id: target.id || (target.className + '').split(' ')[0] || target.tagName.toLowerCase(),
      heightVh: +(r.height / vh).toFixed(1),
      pinned: el.classList.contains('pin-spacer') || sticky,
      surface: lum(c) < 0.3 ? 'dark' : (Math.max(c.r, c.g, c.b) - Math.min(c.r, c.g, c.b) > 40 ? 'colour' : 'light'),
      bg: hex(c), media: imgs, fullBleedMedia: big, columns: cols,
      heading: heading ? heading.innerText.replace(/\s+/g, ' ').slice(0, 60) : '',
    };
  });

  // --- chrome ---
  const fixed = all.filter((el) => ['fixed', 'sticky'].includes(getComputedStyle(el).position) && el.getBoundingClientRect().height < vh * 0.5);
  const nav = document.querySelector('header, nav');
  const radii = {};
  for (const el of all.slice(0, 2500)) { const v = getComputedStyle(el).borderTopLeftRadius; if (v !== '0px') radii[v] = (radii[v] || 0) + 1; }

  return {
    url: location.href, title: document.title,
    pageHeightVh: +(document.documentElement.scrollHeight / vh).toFixed(1),
    type: {
      families: Object.entries(fam).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([f, n]) => `${f} (${n})`),
      display: { px: display.px, weight: display.w, lineHeight: display.lh, letterSpacing: display.ls, family: display.f },
      bodyPx: body, scaleJump: +(display.px / body).toFixed(1), eyebrowLabels: eyebrows,
    },
    palette, radii: Object.entries(radii).sort((a, b) => b[1] - a[1]).slice(0, 4).map(([k]) => k),
    motion: { ...libs, keyframes, cssScrollTimelines: viewTimeline, viewTransitions, hoverRules: hover, focusRules: focus, unreadableSheets: unreadable },
    chrome: { fixedElements: fixed.length, navPosition: nav ? getComputedStyle(nav).position : null, customCursor: cursorNone, svgCount: document.querySelectorAll('svg').length },
    scenes,
    notes: [
      'Scroll through the page once and re-run: pinned sections and lazy content only measure after they mount.',
      'Read this as method, not costume: copy the scene rhythm, scale jump and choreography, never the palette, fonts or layout.',
    ],
  };
})();
