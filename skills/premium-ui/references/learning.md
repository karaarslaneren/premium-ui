# Learning across sessions

Each session starts from the same files, so without memory the skill repeats
itself: the same faces on the next project's board, the same ghost-button
miss, a direction the user already turned down. `scripts/learn.py` keeps a
small journal outside the plugin (`~/.claude/premium-ui/`, or
`$PREMIUM_UI_HOME`), so it survives plugin updates and is shared by every
project.

Memory is for **not repeating**: faces, metaphors, mistakes, rejected looks.
It is never a reason to reuse what won last time; a board built from past
winners is the homogenisation `direction-finding.md` exists to prevent.

## 1. Recall at the start

Before step 0 (or step 3 when the direction is already fixed):

```bash
python3 scripts/learn.py recall --project <name>
```

`<name>` is a stable project name: the `name` in `package.json` /
`composer.json`, else the git repo's folder name. Use the same one all
session. Then:

- **Lessons** are rules. Follow them like `pitfalls.md`.
- **This project** lists boards already shown here, the pick and the user's
  words. A new board here must not reuse those metaphors or faces (the
  "asked again" rule in `direction-finding.md`), and must answer the
  feedback ("kâğıt hissi istemiyorum" → no paper direction).
- **Recently used** faces and directions, all projects: at most one listed
  face on the new board; don't reuse a listed metaphor without a reason that
  is specific to this product.
- **What the user picked:** a taste pattern counts only after 3+ choices
  (e.g. light picked 4 of 4 times). Even then let it shape *one* direction
  and keep the others outside it.
- **Recurring issues:** check the top ones before showing anything.

No memory yet is normal: say nothing and continue.

## 2. Log as you go

One command each, right when it happens, not reconstructed at the end:

| When | Command |
| --- | --- |
| Board passed the visual critique and is about to be shown | `learn.py board <board.html> --project <name>` (reads directions, faces, tone and corners from the file) |
| User picks a direction | `learn.py choice --project <name> --picked B --text "their words, if any"` |
| User reacts to a design (rejects, "yine çok benzer", "daha profesyonel olsun", praises a part) | `learn.py feedback --project <name> --text "their words, short"` |
| Visual critique, `verify.js` or the user finds a problem you made | `learn.py issue --project <name> --kind <slug> --text "one line"` |

Issue slugs, so counts add up across sessions (add a new one only when none
fits): `ghost-button`, `low-contrast`, `empty-first-frame`, `label-wrap`,
`overflow`, `clipped-text`, `glyph-fallback`, `layout-animation`,
`js-hidden-content`, `reduced-motion`, `hit-area`, `invented-claim`,
`reference-copy`, `same-look`.

Log the user's words as they said them; don't log secrets, customer data or
anything from `.env`.

## 3. Distil at the end

When the session's work is done (with step 7 of SKILL.md), turn what
happened into at most three lessons:

- Something cost a retry, the user corrected you, or `recall` flagged an
  issue kind as seen twice → write a lesson:
  `learn.py lesson "Do X, because Y"`. Actionable and general: it has to
  help on a project you haven't seen. "Kargonet liked green" is journal,
  not a lesson.
- An issue kind at 3x, or a bug the user had to point out → also propose a
  `pitfalls.md` row (SKILL.md step 7). Lessons are this user's memory;
  pitfalls are the skill's.
- Keep `lessons.md` under ~30 lines: merge near-duplicates, delete a lesson
  that a later session showed to be wrong. Edit the file directly for that.

Tell the user in one line what was remembered ("Hafızaya eklendi: koyu
zeminde ghost buton kontrastı her yönde kontrol edilecek"). If they say not
to remember ("bunu hatırlama", "hafıza kullanma"), don't log; for good,
`PREMIUM_UI_MEMORY=off` turns the script off.
