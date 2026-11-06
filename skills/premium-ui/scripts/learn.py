#!/usr/bin/env python3
"""The skill's memory across sessions and projects.

Usage:
    python3 learn.py recall [--project NAME] [--boards 8]
    python3 learn.py board <board.html> --project NAME
    python3 learn.py choice --project NAME --picked B [--text "user's words"]
    python3 learn.py feedback --project NAME --text "user's words"
    python3 learn.py issue --project NAME --kind ghost-button [--text "..."]
    python3 learn.py lesson "One line: what to do differently, and why"
    python3 learn.py share [--send | --never] [--all]

Everything is stored in $PREMIUM_UI_HOME (default ~/.claude/premium-ui), so it
survives plugin updates: journal.jsonl (one event per line) and lessons.md
(distilled rules, read at the start of every session). PREMIUM_UI_MEMORY=off
turns every command into a no-op. Standard library only.

`share` turns what was learned since the last share into an anonymous report
(lessons, issue counts, faces used, light/dark and corner picks; no project
names, user quotes, paths or code) for the skill's GitHub repo. Without
--send it only prints the report; send it only after the user said yes.
"""
import argparse
import collections
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

HOME = Path(os.environ.get("PREMIUM_UI_HOME") or Path.home() / ".claude" / "premium-ui")
JOURNAL = HOME / "journal.jsonl"
LESSONS = HOME / "lessons.md"
SHARED = HOME / "shared.json"
REPO = os.environ.get("PREMIUM_UI_REPO", "karaarslaneren/premium-ui")
LABEL = "öğrenilenler"
SHARE_MARKER = "<!-- premium-ui-share v1 -->"
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

    state = shared_state()
    if not state.get("never"):
        new_events, new_lessons = pending_share(state)
        new_issues = sum(1 for e in new_events if e.get("type") == "issue")
        if len(new_lessons) >= 2 or new_issues >= 5:
            print(f"\n## Sharing\n\n{len(new_lessons)} new lessons and {new_issues} issues since the last share. "
                  "At the end of this session, offer once to share them (learning.md §4).")


# ---------- share ----------

def lesson_lines():
    if not LESSONS.exists():
        return []
    return [l[2:].strip() for l in LESSONS.read_text(encoding="utf-8").splitlines() if l.startswith("- ")]


def shared_state():
    try:
        return json.loads(SHARED.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def skill_version():
    try:
        manifest = Path(__file__).resolve().parents[3] / ".claude-plugin" / "plugin.json"
        return json.loads(manifest.read_text(encoding="utf-8")).get("version", "?")
    except (OSError, ValueError, IndexError):
        return "?"


def scrub(text, projects):
    text = re.sub(r"https?://\S+", "<url>", text)
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "<email>", text)
    text = re.sub(r"(~|/Users|/home|[A-Z]:\\)[^\s`'\")]*", "<path>", text)
    for name in sorted(projects, key=len, reverse=True):
        if name and len(name) > 2:
            text = re.sub(re.escape(name), "<proje>", text, flags=re.I)
    return text


def pending_share(state=None):
    """What a share would contain now: events and lessons not shared yet."""
    state = shared_state() if state is None else state
    since = state.get("last", "")
    events = [e for e in read_journal() if e.get("ts", "") > since]
    done = set(state.get("lessons", []))
    lessons = [l for l in lesson_lines() if norm(l) not in done]
    return events, lessons


def build_report(events, lessons):
    projects = {e.get("project") for e in read_journal() if e.get("project")}
    boards = [e for e in events if e.get("type") == "board"]
    issues = collections.Counter(e["kind"] for e in events if e.get("type") == "issue")
    fonts = collections.Counter(f for b in boards for f in dict.fromkeys(b.get("fonts") or [f for d in b["dirs"] for f in d["fonts"]]))
    spread = collections.Counter(d[attr] for b in boards for d in b["dirs"] for attr in ("tone", "corners") if d.get(attr))
    picked, passed = collections.Counter(), collections.Counter()
    last_board = {}
    for e in read_journal():
        if e.get("type") == "board":
            last_board[e.get("project")] = e
        elif e.get("type") == "choice" and e in events and e.get("project") in last_board:
            keys = re.findall(r"[a-z]", e["picked"].lower()) if len(e["picked"]) <= 5 else []
            for d in last_board[e["project"]]["dirs"]:
                for attr in ("tone", "corners"):
                    if d.get(attr):
                        (picked if d["key"].lower() in keys else passed)[d[attr]] += 1
    lessons = [scrub(l, projects) for l in lessons]
    data = {
        "v": 1, "skill": skill_version(),
        "from": min((e["ts"][:10] for e in events), default=None), "to": max((e["ts"][:10] for e in events), default=None),
        "boards": len(boards), "choices": sum(1 for e in events if e.get("type") == "choice"),
        "feedback": sum(1 for e in events if e.get("type") == "feedback"),
        "lessons": lessons, "issues": dict(issues.most_common()), "fonts": dict(fonts.most_common()),
        "spread": dict(spread), "picked": dict(picked), "passed": dict(passed),
    }
    title = f"[öğrenilenler] {len(lessons)} yeni kural, {sum(issues.values())} hata, {len(boards)} pano (premium-ui {data['skill']})"
    md = [SHARE_MARKER, "",
          f"Skill {data['skill']} · {data['from'] or '-'} → {data['to'] or '-'} · {data['boards']} pano, "
          f"{data['choices']} seçim, {data['feedback']} geri bildirim", ""]
    md += ["### Öğrenilen kurallar", ""] + ([f"- {l}" for l in lessons] or ["(yok)"]) + [""]
    if issues:
        md += ["### Bulunan hatalar", ""] + [f"- `{k}`: {n}" for k, n in issues.most_common()] + [""]
    if fonts:
        md += ["### Panolarda kullanılan fontlar", "", ", ".join(f"{f} ({n})" if n > 1 else f for f, n in fonts.most_common()), ""]
    if picked or passed:
        md += ["### Seçilen yönler", "", "Seçilen: " + (", ".join(f"{k} {v}" for k, v in picked.most_common()) or "-")
               + " · seçilmeyen: " + (", ".join(f"{k} {v}" for k, v in passed.most_common()) or "-"), ""]
    md += ["<details><summary>Veri</summary>", "", "```json", json.dumps(data, ensure_ascii=False), "```", "", "</details>", "",
           "_`learn.py share` ile, kullanıcının onayıyla gönderildi. Proje adları, kullanıcının sözleri, dosya yolları ve kod içermez._"]
    return title, "\n".join(md), data


def mark_shared(lessons_all):
    state = shared_state()
    state["last"] = now()
    state["lessons"] = sorted(set(state.get("lessons", [])) | {norm(l) for l in lessons_all})
    SHARED.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")


def cmd_share(a):
    HOME.mkdir(parents=True, exist_ok=True)
    if a.never:
        state = shared_state(); state["never"] = True
        SHARED.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        print("OK: sharing will not be offered again (delete shared.json to undo).")
        return
    events, lessons = pending_share({} if a.all else None)
    if not lessons and not any(e.get("type") in ("board", "issue") for e in events):
        print("Nothing new to share since the last report.")
        return
    title, body, _ = build_report(events, lessons)
    if not a.send:
        print(f"Title: {title}\n\n{body}\n")
        print(f"Preview only. Show this to the user; if they agree, run: learn.py share --send   (repo: {REPO})")
        return
    gh = shutil.which("gh")
    if gh and subprocess.run([gh, "auth", "status"], capture_output=True).returncode == 0:
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(body)
        for extra in (["--label", LABEL], []):
            r = subprocess.run([gh, "issue", "create", "--repo", REPO, "--title", title, "--body-file", f.name, *extra],
                               capture_output=True, text=True)
            if r.returncode == 0:
                break
        os.unlink(f.name)
        if r.returncode == 0:
            mark_shared(lesson_lines())
            print("Sent: " + r.stdout.strip())
            return
        print("gh could not create the issue: " + (r.stderr.strip() or r.stdout.strip()))
    url = f"https://github.com/{REPO}/issues/new?" + urllib.parse.urlencode({"title": title, "body": body, "labels": LABEL})
    if len(url) > 7500:
        path = HOME / "share-report.md"
        path.write_text(body, encoding="utf-8")
        url = f"https://github.com/{REPO}/issues/new?" + urllib.parse.urlencode({"title": title, "labels": LABEL})
        print(f"Report saved to {path}. Open the link, paste the file's contents as the body, submit:\n{url}")
    else:
        print(f"Open this link and press Submit (nothing is sent until then):\n{url}")
    mark_shared(lesson_lines())


def main(argv):
    p = argparse.ArgumentParser(description="premium-ui memory: what earlier sessions designed and learned.")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("recall"); r.add_argument("--project"); r.add_argument("--boards", type=int, default=8)
    b = sub.add_parser("board"); b.add_argument("file"); b.add_argument("--project", required=True)
    c = sub.add_parser("choice"); c.add_argument("--project", required=True); c.add_argument("--picked", required=True); c.add_argument("--text")
    f = sub.add_parser("feedback"); f.add_argument("--project", required=True); f.add_argument("--text", required=True)
    i = sub.add_parser("issue"); i.add_argument("--project", required=True); i.add_argument("--kind", required=True); i.add_argument("--text")
    l = sub.add_parser("lesson"); l.add_argument("text")
    s = sub.add_parser("share"); s.add_argument("--send", action="store_true"); s.add_argument("--never", action="store_true")
    s.add_argument("--all", action="store_true", help="include what was already shared")
    a = p.parse_args(argv)
    if os.environ.get("PREMIUM_UI_MEMORY", "").lower() in ("off", "0", "false"):
        print("premium-ui memory is off (PREMIUM_UI_MEMORY); nothing read or written.")
        return
    {"recall": cmd_recall, "board": cmd_board, "choice": cmd_choice, "feedback": cmd_feedback,
     "issue": cmd_issue, "lesson": cmd_lesson, "share": cmd_share}[a.cmd](a)


if __name__ == "__main__":
    main(sys.argv[1:])
