# Visual critique

Writing CSS is not seeing the page. In evals, boards that "passed" by
reading the code still shipped ghost buttons at 1.1:1 contrast and phone
mock-ups that were empty in every still frame. Look at the result before
the user does.

Run this after filling the proposal board (before showing it) and after
each built section (SKILL.md step 6).

## 1. Capture

- **Browser tool available:** screenshot at 1440×900 and at 375–390 wide
  after animations settle, and run `scripts/verify.js` at both sizes.
- **Scroll-driven pages** (pinned or scrubbed scenes), or a hidden browser
  pane: `node scripts/scenes.mjs <url> --out DIR` scrolls in real time and
  captures one 1440×900 frame per screen (`--width 390 --height 844` for
  mobile). Serve local files over http first.
- **No browser tool:** `python3 scripts/snapshot.py <page.html>`. It uses
  the Chrome / Chromium / Edge already on the machine (headless), writes
  `snapshots/desktop.png`, `desktop-top.png` and `mobile.png` next to the
  page, and prints the `verify.js` report for both widths. Then open the
  PNGs with your file-reading tool and look at them. Local files only; for
  a running dev server use a browser tool.
- **Neither works** (no browser on the machine): say so in the reply. Never
  write that the page was checked visually when it wasn't.

## 2. Look, and answer in writing

Read the screenshots as a stranger would, not as the author who knows what
each element is meant to be. One line per question, per direction or
section:

1. **Legible?** Every button, label and number. Check secondary / ghost
   buttons and text on coloured or dark surfaces first: that is the most
   repeated miss.
2. **Finished?** No empty frames, blank phone or screen mock-ups, grey
   placeholder boxes, leftover `[brackets]`. If a signature animation starts
   empty, give its first frame content so a still image still tells the
   story (screenshots, reduced motion and slow devices all see that frame).
3. **Broken?** Clipping, overlap, content running off the right edge,
   one-word lines, important text cut with "…", Turkish letters (ğ ş ı İ)
   in a different font from the rest of the word.
4. **Squint.** At a glance, do the directions differ in value and layout?
   Does each hero have one focal point, not three competing ones?
5. **Swap.** Is the product's metaphor visible in the picture itself, or
   does it only live in the description text?
6. **Mobile.** Columns stack cleanly, buttons aren't cramped, the headline
   fits, nothing scrolls sideways.
7. **Level.** For a landing page or its plan: the level check in
   `high-end.md` (8 rows, 0–2 each). Under 12 of 16 → fix the lowest rows
   first. For a component: is every state in the matrix designed, in light
   and dark (`component-craft.md`)?

## 2b. Three critics (landing pages and boards)

After the six questions, read the same screenshots three more times, each
time as one person, and write their single harshest note:

- **Art director:** Does it have a point of view? Is there one idea,
  carried by the motif, the pictures and the type, or a collection of
  tasteful parts? Which element would they cut?
- **Motion designer:** Which scene is the signature moment, and are its
  three frames (`high-end.md` §1b) strong as stills? Does anything move
  without explaining something? Do scenes hand over or hard-cut?
- **Accessibility reviewer:** Reduced motion, keyboard path through pinned
  scenes and menus, text over images, focus on custom controls.

Then the **AI tell test**: would a designer looking at this guess within
five seconds that a model made it? Common tells: centred hero + three
cards, purple/blue gradient, glassmorphism on everything, emoji icons,
generic "Geleceği…" headlines, identical section rhythm, a giant footer
wordmark, stock-like illustrations. Name each tell you find and remove it.

For a build in a real browser, also scroll once at 4× CPU slowdown and
read `verify.js` → `performance`.

## 3. Fix, re-shoot, report

Fix every problem from step 2 and every `fail` from `verify.js`, then
capture again. At most two rounds; whatever is still open goes in the reply
by name. Tell the user what the check found and fixed in one line (e.g.
"Görsel kontrol: C yönündeki ikincil buton koyu zeminde okunmuyordu,
düzeltildi").
