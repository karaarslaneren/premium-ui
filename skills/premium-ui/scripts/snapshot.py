#!/usr/bin/env python3
"""Screenshot a page and run verify.js on it with headless Chrome.

For when no browser tool is available. Uses the Chrome / Chromium / Edge
already installed on the machine; nothing is downloaded.

Usage:
    python3 snapshot.py <page.html> [--out DIR] [--wait MS]

Writes to DIR (default: next to the page, in `snapshots/`):
    desktop.png       1440 wide, full page height (capped at 6000px)
    desktop-top.png   1440×900, what the first screen shows
    mobile.png        390 wide, full page height
And prints the verify.js report for desktop and mobile: summary plus every
fail/warn item. Exit code 1 if any check fails.

Read the PNGs (they are images you can look at) and do the visual critique.
Animations are captured at one moment (--wait, default 4000ms of virtual
time); judge motion in a real browser when one is available.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANDIDATES = [
    os.environ.get("CHROME", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
    "microsoft-edge", "chrome", "msedge",
]
MARK = "__PREMIUM_UI_VERIFY__"
MIN_WINDOW = 500  # headless Chrome ignores narrower --window-size


def find_chrome():
    for c in CANDIDATES:
        if not c:
            continue
        p = c if os.path.isabs(c) else shutil.which(c)
        if p and os.path.exists(p):
            return p
    sys.exit("No Chrome/Chromium/Edge found. Set CHROME=/path/to/browser.")


def run(chrome, profile, args, timeout=90):
    cmd = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
           "--no-first-run", "--no-default-browser-check",
           f"--user-data-dir={profile}", *args]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def frame_page(target, width, height):
    """Chrome's headless window can't go below ~500px wide, so narrow viewports
    are rendered in an iframe of the exact width inside a wider window."""
    return (
        '<!doctype html><body style="margin:0;background:#777">'
        f'<iframe src="{target}" style="border:0;display:block;width:{width}px;height:{height}px"></iframe>'
        "<script>addEventListener('message',e=>{const p=document.createElement('pre');"
        f"p.id='{MARK}';p.textContent=e.data;document.body.append(p)}})</script>"
    )


def render(chrome, profile, page, width, height, wait, args):
    """Load `page` (a local file) at width×height, through a frame when narrow."""
    if width >= MIN_WINDOW:
        return run(chrome, profile, [f"--window-size={width},{height}", *args, Path(page).as_uri()])
    wrapper = Path(page).with_name(f".snapshot-frame-{Path(page).name}")
    wrapper.write_text(frame_page(Path(page).name, width, height))
    try:
        return run(chrome, profile, [f"--window-size={MIN_WINDOW},{height}", *args, wrapper.as_uri()])
    finally:
        wrapper.unlink(missing_ok=True)


def audit(chrome, profile, page, width, height, wait):
    """Load a copy of the page with verify.js appended; read the report from the DOM."""
    src = (HERE / "verify.js").read_text()
    hook = (
        "<script>addEventListener('load',()=>setTimeout(()=>{let r;"
        f"try{{r=eval({json.dumps(src)})}}catch(e){{r={{error:String(e)}}}}"
        "r.pageHeight=document.documentElement.scrollHeight;const j=JSON.stringify(r);"
        "if(parent!==window){parent.postMessage(j,'*');return}"
        f"const p=document.createElement('pre');p.id='{MARK}';"
        "p.hidden=true;p.textContent=j;document.body.append(p)"
        f"}},{max(wait - 1500, 500)}))</script>"
    )
    path = Path(page).resolve()
    copy = path.with_name(f".snapshot-{path.name}")
    copy.write_text(path.read_text() + hook)
    try:
        res = render(chrome, profile, copy, width, height, wait,
                     [f"--virtual-time-budget={wait + 1000}", "--dump-dom"])
    finally:
        copy.unlink(missing_ok=True)
    m = re.search(rf'<pre id="{MARK}"[^>]*>(.*?)</pre>', res.stdout, re.S)
    if not m:
        return {"error": "verify.js report not found in the page (script error?)"}, None
    report = json.loads(html.unescape(m.group(1)))
    return report, report.get("pageHeight")


def shot(chrome, profile, page, out, width, height, wait):
    out.unlink(missing_ok=True)
    render(chrome, profile, Path(page).resolve(), width, height, wait,
           [f"--virtual-time-budget={wait}", f"--screenshot={out}"])
    if out.exists() and width < MIN_WINDOW:
        crop(out, width)
    return out.exists()


def crop(png, width):
    """Trim the grey margin right of a framed narrow screenshot, if a tool is around."""
    try:
        from PIL import Image
        with Image.open(png) as im:
            im.crop((0, 0, width, im.height)).save(png)
        return
    except Exception:
        pass
    if shutil.which("sips"):
        h = subprocess.run(["sips", "-g", "pixelHeight", str(png)], capture_output=True, text=True).stdout
        m = re.search(r"pixelHeight: (\d+)", h)
        if m:
            subprocess.run(["sips", "-c", m.group(1), str(width), "--cropOffset", "0", "0", str(png)],
                           capture_output=True)


def brief(report):
    if "error" in report:
        return {"error": report["error"]}
    issues = {k: v["items"] for k, v in report["checks"].items() if v["status"] in ("fail", "warn")}
    return {"summary": report["summary"], "issues": issues}


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 2
    page = argv[0]
    if page.startswith(("http://", "https://")):
        print("Local files only. For a running site, use a browser tool and scripts/verify.js.")
        return 2
    wait = int(argv[argv.index("--wait") + 1]) if "--wait" in argv else 4000
    if "--out" in argv:
        out_dir = Path(argv[argv.index("--out") + 1])
    else:
        out_dir = Path(page).resolve().parent / "snapshots"
    out_dir.mkdir(parents=True, exist_ok=True)

    chrome = find_chrome()
    profile = tempfile.mkdtemp(prefix="premium-ui-chrome-")
    result, failed = {}, False
    try:
        for name, w, h in (("desktop", 1440, 900), ("mobile", 390, 844)):
            report, page_h = audit(chrome, profile, page, w, h, wait)
            full_h = min(max(page_h or h, h), 6000)
            files = []
            if shot(chrome, profile, page, out_dir / f"{name}.png", w, full_h, wait):
                files.append(str(out_dir / f"{name}.png"))
            if name == "desktop" and shot(chrome, profile, page, out_dir / "desktop-top.png", w, h, wait):
                files.append(str(out_dir / "desktop-top.png"))
            result[name] = {"screenshots": files, "verify": brief(report)}
            failed |= bool(report.get("summary", {}).get("fail"))
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
