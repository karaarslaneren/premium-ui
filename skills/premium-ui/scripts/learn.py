#!/usr/bin/env python3
"""The skill's memory across sessions and projects.

Usage:
    python3 learn.py recall [--project NAME] [--boards 8]
    python3 learn.py board <board.html> --project NAME
    python3 learn.py choice --project NAME --picked B [--text "user's words"]
    python3 learn.py feedback --project NAME --text "user's words"
    python3 learn.py issue --project NAME --kind ghost-button [--text "..."]
    python3 learn.py lesson "One line: what to do differently, and why"

Everything is stored in $PREMIUM_UI_HOME (default ~/.claude/premium-ui), so it
survives plugin updates: journal.jsonl (one event per line) and lessons.md
(distilled rules, read at the start of every session). PREMIUM_UI_MEMORY=off
turns every command into a no-op. Standard library only.
"""
import argparse
import collections
import datetime
import html
import json
import os
import re
import sys
from pathlib import Path

HOME = Path(os.environ.get("PREMIUM_UI_HOME") or Path.home() / ".claude" / "premium-ui")
JOURNAL = HOME / "journal.jsonl"
LESSONS = HOME / "lessons.md"
LESSONS_HEADER = "# premium-ui lessons\n\nOne line each. Newest last. Merge duplicates, delete what stopped being true.\n\n"
GENERIC = {"serif", "sans-serif", "monospace", "system-ui", "ui-sans-serif", "ui-serif", "ui-monospace",
           "cursive", "fantasy", "inherit", "initial", "-apple-system", "blinkmacsystemfont", "segoe ui",
           "helvetica", "helvetica neue", "arial", "georgia", "times new roman", "menlo", "consolas"}


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def read_journal():
    if not JOURNAL.exists():
        return []
    events = []
    for line in JOURNAL.read_text(encoding="utf-8").splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            pass
    return events


def append(event):
    HOME.mkdir(parents=True, exist_ok=True)
    event = {"ts": now(), **event}
    with JOURNAL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


# ---------- board parsing ----------

def lightness(value):
    """Relative lightness 0..1 of a #hex or rgb() colour, None if unknown."""
    if not value:
        return None
    value = value.strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{3,8})", value)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    else:
        m = re.match(r"rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)", value)
        if not m:
            return None
        r, g, b = (int(x) for x in m.groups())
    return round((max(r, g, b) + min(r, g, b)) / 2 / 255, 2)


def font_names(decl):
    names = []
    for part in decl.split(","):
        name = part.strip().strip("'\"").strip()
        if (name and not name.startswith("var(") and name.lower() not in GENERIC
                and not re.fullmatch(r"[\d.]+[a-z%]*|normal|bold|bolder|lighter|italic", name.lower())):
            names.append(name)
    return names


def parse_board(text):
    link_fonts = []
    for href in re.findall(r"""href=["']([^"']*fonts\.googleapis\.com/css2?[^"']*)""", text):
        for fam in re.findall(r"family=([^&:;]+)", html.unescape(href)):
            link_fonts.append(fam.replace("+", " ").strip())

    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", text, re.S))
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    dirs = collections.OrderedDict()

    for key, start in [(m.group(1), m.end()) for m in re.finditer(r"""<section[^>]*data-dir=["'](\w+)["']""", text)]:
        h2 = re.search(r"<h2[^>]*>(.*?)</h2>", text[start:start + 3000], re.S)
        name = re.sub(r"<[^>]+>", "", h2.group(1)).strip() if h2 else ""
        dirs[key] = {"key": key, "name": html.unescape(re.sub(r"\s+", " ", name)), "fonts": [], "vars": {}}

    for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        for key in re.findall(r"""data-dir=["']?(\w+)""", selector):
            d = dirs.setdefault(key, {"key": key, "name": "", "fonts": [], "vars": {}})
            for prop, val in re.findall(r"(--[\w-]+|font-family)\s*:\s*([^;]+)", body):
                val = val.strip()
                if prop == "font-family" or (re.search(r"font|ui|display|head|body|mono|serif|sans", prop)
                                             and not re.search(r"(-w|weight|size|lh|leading|track|spacing|style|case)$", prop)):
                    for n in font_names(val):
                        if n not in d["fonts"]:
                            d["fonts"].append(n)
                elif prop in ("--bg", "--accent", "--ink", "--surface", "--r", "--radius", "--btn-r"):
                    d["vars"].setdefault(prop, val)

    out = []
    for d in dirs.values():
        v = d.pop("vars")
        light = lightness(v.get("--bg"))
        radius = re.match(r"([\d.]+)", v.get("--r") or v.get("--radius") or v.get("--btn-r") or "")
        d.update({
            "bg": v.get("--bg"), "accent": v.get("--accent"),
            "tone": None if light is None else ("dark" if light < 0.35 else "light"),
            "corners": None if not radius else ("sharp" if float(radius.group(1)) <= 4 else "soft" if float(radius.group(1)) >= 14 else "medium"),
        })
        out.append(d)
    return {"fonts": list(dict.fromkeys(link_fonts)), "dirs": out}


# ---------- commands ----------

def cmd_board(a):
    text = Path(a.file).read_text(encoding="utf-8")
    parsed = parse_board(text)
    if not parsed["dirs"] and not parsed["fonts"]:
        sys.exit("learn.py: no directions or Google Fonts found in " + a.file)
    e = append({"type": "board", "project": a.project, "file": str(Path(a.file).resolve()), **parsed})
    for d in e["dirs"]:
        print(f"{d['key'].upper()}  {d['name'] or '?'}  | {', '.join(d['fonts']) or '?'} | {d['tone'] or '?'}, {d['corners'] or '?'} corners")
    print(f"logged board for {a.project} ({len(e['dirs'])} directions, fonts: {', '.join(e['fonts'])})")


def cmd_choice(a):
    append({"type": "choice", "project": a.project, "picked": a.picked, "text": a.text})
    print(f"logged choice {a.picked} for {a.project}")


def cmd_feedback(a):
    append({"type": "feedback", "project": a.project, "text": a.text})
    print(f"logged feedback for {a.project}")


def cmd_issue(a):
    kind = re.sub(r"[^a-z0-9]+", "-", a.kind.lower()).strip("-")
    append({"type": "issue", "project": a.project, "kind": kind, "text": a.text})
    total = sum(1 for e in read_journal() if e.get("type") == "issue" and e.get("kind") == kind)
    print(f"logged issue '{kind}' ({total}x so far)")


def norm(s):
    return re.sub(r"[^\w]+", " ", s.lower()).strip()


def cmd_lesson(a):
    HOME.mkdir(parents=True, exist_ok=True)
    current = LESSONS.read_text(encoding="utf-8") if LESSONS.exists() else LESSONS_HEADER
    line = a.text.strip().lstrip("- ").strip()
    if norm(line) in {norm(l) for l in current.splitlines()}:
        print("already in lessons.md")
        return
    LESSONS.write_text(current + ("" if current.endswith("\n") else "\n") + f"- {line}\n", encoding="utf-8")
    print(f"added to {LESSONS}")


def cmd_recall(a):
    events = read_journal()
    lessons = LESSONS.read_text(encoding="utf-8").strip() if LESSONS.exists() else ""
    if not events and not lessons:
        print(f"No memory yet ({HOME}). Nothing to avoid; log this session's board and choices as you go.")
        return

    if lessons:
        print("## Lessons\n")
        print(re.sub(r"^# .*\n+(One line.*\n+)?", "", lessons).strip() or "(none)")
        print()

    boards = [e for e in events if e.get("type") == "board"]
    choices = []
    last_board = {}
    for i, e in enumerate(events):
        if e.get("type") == "board":
            last_board[e.get("project")] = e
        elif e.get("type") == "choice" and e.get("project") in last_board:
            choices.append((e, last_board[e["project"]]))

    if a.project:
        mine = [e for e in events if e.get("project") == a.project]
        if mine:
            print(f"## This project: {a.project}\n")
            for e in mine:
                if e["type"] == "board":
                    names = "; ".join(f"{d['key'].upper()} {d['name']} ({', '.join(d['fonts'][:2])})" for d in e["dirs"])
                    print(f"- {e['ts'][:10]} board: {names}")
                elif e["type"] == "choice":
                    print(f"- {e['ts'][:10]} picked {e['picked']}" + (f": \"{e['text']}\"" if e.get("text") else ""))
                elif e["type"] == "feedback":
                    print(f"- {e['ts'][:10]} feedback: \"{e['text']}\"")
                elif e["type"] == "issue":
                    print(f"- {e['ts'][:10]} issue {e['kind']}" + (f": {e['text']}" if e.get("text") else ""))
            if any(e["type"] == "board" for e in mine):
                print("\nA board was already shown here: a new one must not reuse its metaphors or faces.")
            print()

    recent = boards[-a.boards:]
    if recent:
        fonts = collections.Counter(f for b in recent for f in dict.fromkeys(b.get("fonts") or [f for d in b["dirs"] for f in d["fonts"]]))
        print(f"## Recently used ({len(recent)} boards, all projects)\n")
        print("Faces: " + ", ".join(f"{f} ({n})" if n > 1 else f for f, n in fonts.most_common()))
        print("Directions: " + "; ".join(f"{d['name']} [{b.get('project')}]" for b in recent for d in b["dirs"] if d["name"]))
        tones = collections.Counter(d["tone"] for b in recent for d in b["dirs"] if d.get("tone"))
        corners = collections.Counter(d["corners"] for b in recent for d in b["dirs"] if d.get("corners"))
        print("Spread: " + ", ".join(f"{k} {v}" for k, v in (tones + corners).most_common()))
        print("Prefer faces and metaphors not listed here; at most one listed face per new board.\n")

    if choices:
        picked = collections.Counter()
        passed = collections.Counter()
        lines = []
        for c, b in choices:
            keys = re.findall(r"[a-z]", c["picked"].lower()) if len(c["picked"]) <= 5 else []
            for d in b["dirs"]:
                bucket = picked if d["key"].lower() in keys else passed
                for attr in ("tone", "corners"):
                    if d.get(attr):
                        bucket[f"{d[attr]}"] += 1
            chosen = [d["name"] for d in b["dirs"] if d["key"].lower() in keys]
            lines.append(f"- {c.get('project')}: {', '.join(chosen) or c['picked']}" + (f" — \"{c['text']}\"" if c.get("text") else ""))
        print("## What the user picked\n")
        print("\n".join(lines[-6:]))
        print("Picked: " + (", ".join(f"{k} {v}" for k, v in picked.most_common()) or "-")
              + " | passed over: " + (", ".join(f"{k} {v}" for k, v in passed.most_common()) or "-"))
        print("A taste pattern needs 3+ choices before it counts; even then keep one direction outside it.\n")

    feedback = [e for e in events if e.get("type") == "feedback"][-6:]
    if feedback:
        print("## Recent feedback\n")
        for e in feedback:
            print(f"- {e['ts'][:10]} [{e.get('project')}] \"{e['text']}\"")
        print()

    issues = collections.Counter(e["kind"] for e in events if e.get("type") == "issue")
    if issues:
        print("## Recurring issues\n")
        low = norm(lessons)
        for kind, n in issues.most_common():
            hint = ""
            if n >= 3:
                hint = "  → recurring: propose a pitfalls.md row" + ("" if norm(kind) in low else " and add a lesson")
            elif n == 2 and norm(kind) not in low:
                hint = "  → seen twice: add a lesson"
            print(f"- {kind}: {n}x{hint}")
        print("Check the top ones before showing anything.")


def main(argv):
    p = argparse.ArgumentParser(description="premium-ui memory: what earlier sessions designed and learned.")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("recall"); r.add_argument("--project"); r.add_argument("--boards", type=int, default=8)
    b = sub.add_parser("board"); b.add_argument("file"); b.add_argument("--project", required=True)
    c = sub.add_parser("choice"); c.add_argument("--project", required=True); c.add_argument("--picked", required=True); c.add_argument("--text")
    f = sub.add_parser("feedback"); f.add_argument("--project", required=True); f.add_argument("--text", required=True)
    i = sub.add_parser("issue"); i.add_argument("--project", required=True); i.add_argument("--kind", required=True); i.add_argument("--text")
    l = sub.add_parser("lesson"); l.add_argument("text")
    a = p.parse_args(argv)
    if os.environ.get("PREMIUM_UI_MEMORY", "").lower() in ("off", "0", "false"):
        print("premium-ui memory is off (PREMIUM_UI_MEMORY); nothing read or written.")
        return
    {"recall": cmd_recall, "board": cmd_board, "choice": cmd_choice, "feedback": cmd_feedback,
     "issue": cmd_issue, "lesson": cmd_lesson}[a.cmd](a)


if __name__ == "__main__":
    main(sys.argv[1:])
