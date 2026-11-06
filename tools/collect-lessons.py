#!/usr/bin/env python3
"""Collect the lessons users shared with `learn.py share` and say what to fold into the skill.

For the maintainer, not shipped behaviour. Reads the "[öğrenilenler]" issues on GitHub
(needs `gh`, logged in) or a folder of saved report bodies, then prints:

- lessons, grouped when several users wrote the same thing
- issue kinds by how many users hit them, flagged when pitfalls.md misses them
- faces by how many boards used them, flagged when type-library.md doesn't mark them †
- which tone / corners users picked vs passed over

Usage:
    python3 tools/collect-lessons.py [--repo owner/name] [--state open|closed|all] [--min-users 2]
    python3 tools/collect-lessons.py --from-dir reports/      # *.md files holding issue bodies

Close an issue once its content is in a release; the default only reads open ones.
"""
import argparse
import collections
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "premium-ui"
MARKER = "<!-- premium-ui-share v1 -->"


def norm(s):
    return re.sub(r"[^\w]+", " ", s.lower()).strip()


def words(s):
    return {w for w in norm(s).split() if len(w) > 2}


def parse(body):
    if MARKER not in (body or ""):
        return None
    m = re.search(r"```json\s*(\{.*?\})\s*```", body, re.S)
    try:
        return json.loads(m.group(1)) if m else None
    except ValueError:
        return None


def from_github(repo, state):
    cmd = ["gh", "issue", "list", "--repo", repo, "--state", state, "--limit", "500",
           "--search", '"[öğrenilenler]" in:title', "--json", "number,title,body,author,url"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("gh issue list failed: " + r.stderr.strip())
    return [{"ref": f"#{i['number']}", "user": (i.get("author") or {}).get("login", "?"), "body": i["body"]}
            for i in json.loads(r.stdout)]


def from_dir(folder):
    return [{"ref": p.name, "user": p.stem.split("__")[0], "body": p.read_text(encoding="utf-8")}
            for p in sorted(Path(folder).glob("*.md"))]


def main(argv):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--repo", default="karaarslaneren/premium-ui")
    p.add_argument("--state", default="open", choices=["open", "closed", "all"])
    p.add_argument("--from-dir")
    p.add_argument("--min-users", type=int, default=2, help="users needed before something counts as a pattern")
    a = p.parse_args(argv)

    raw = from_dir(a.from_dir) if a.from_dir else from_github(a.repo, a.state)
    reports = [(r, d) for r in raw if (d := parse(r["body"]))]
    if not reports:
        print("No shared reports found.")
        return
    users = {r["user"] for r, _ in reports}
    versions = collections.Counter(d.get("skill", "?") for _, d in reports)
    print(f"# Shared lessons\n\n{len(reports)} reports from {len(users)} users · "
          f"{sum(d.get('boards', 0) for _, d in reports)} boards · skill versions: "
          + ", ".join(f"{v} ({n})" for v, n in versions.most_common()) + "\n")

    # lessons: greedy clustering on word overlap
    clusters = []
    for r, d in reports:
        for lesson in d.get("lessons", []):
            w = words(lesson)
            for c in clusters:
                if w and len(w & c["words"]) / len(w | c["words"]) >= 0.4:
                    c["items"].append((r, lesson)); c["words"] |= w
                    break
            else:
                clusters.append({"words": w, "items": [(r, lesson)]})
    clusters.sort(key=lambda c: -len({r["user"] for r, _ in c["items"]}))
    pitfalls = norm((SKILL / "references" / "pitfalls.md").read_text(encoding="utf-8"))
    skill_text = norm(" ".join(p.read_text(encoding="utf-8") for p in [SKILL / "SKILL.md", *(SKILL / "references").glob("*.md")]))

    print("## Lessons\n")
    for c in clusters:
        who = {r["user"] for r, _ in c["items"]}
        refs = ", ".join(sorted({r["ref"] for r, _ in c["items"]}))
        tag = " **← candidate for the skill**" if len(who) >= a.min_users else ""
        print(f"- ({len(who)} users; {refs}){tag}")
        for _, lesson in c["items"][:3]:
            print(f"  - {lesson}")
    print()

    kinds, kind_users = collections.Counter(), collections.defaultdict(set)
    for r, d in reports:
        for k, n in d.get("issues", {}).items():
            kinds[k] += n; kind_users[k].add(r["user"])
    if kinds:
        print("## Issues found while designing\n")
        for k, n in sorted(kinds.items(), key=lambda kv: (-len(kind_users[kv[0]]), -kv[1])):
            kw = k.split("-")
            covered = sum(w in pitfalls for w in kw) >= -(-len(kw) * 2 // 3)
            tag = "" if covered else (" **← not in pitfalls.md**" if len(kind_users[k]) >= a.min_users else " (not in pitfalls.md)")
            print(f"- `{k}`: {n}x by {len(kind_users[k])} users{tag}")
        print()

    lib = (SKILL / "references" / "type-library.md").read_text(encoding="utf-8")
    marked = {m.strip() for m in re.findall(r"([A-Z][\w ]+?) †", lib)}
    fonts, font_users = collections.Counter(), collections.defaultdict(set)
    boards = sum(d.get("boards", 0) for _, d in reports) or 1
    for r, d in reports:
        for f, n in d.get("fonts", {}).items():
            fonts[f] += n; font_users[f].add(r["user"])
    if fonts:
        print("## Faces\n")
        for f, n in fonts.most_common(20):
            share = n / boards
            tag = " †" if f in marked else (" **← overused? mark † in type-library.md**"
                                             if share >= 0.25 and len(font_users[f]) >= a.min_users else "")
            print(f"- {f}: {n} boards ({share:.0%}), {len(font_users[f])} users{tag}")
        missing = sorted(f for f in fonts if norm(f) not in skill_text)
        if missing:
            print(f"\nNot in type-library.md (models picked them from memory): {', '.join(missing[:15])}")
        print()

    picked, passed = collections.Counter(), collections.Counter()
    for _, d in reports:
        picked.update(d.get("picked", {})); passed.update(d.get("passed", {}))
    if picked or passed:
        print("## Picks\n")
        for k in sorted(set(picked) | set(passed)):
            total = picked[k] + passed[k]
            print(f"- {k}: picked {picked[k]} of {total} times shown ({picked[k] / total:.0%})")
        print("\nOne direction in three gets picked by chance (33%); far above or below is a signal.")


if __name__ == "__main__":
    main(sys.argv[1:])
