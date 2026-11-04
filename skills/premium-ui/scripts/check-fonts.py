#!/usr/bin/env python3
"""Check that Google Fonts families exist and cover the glyphs a UI needs.

Usage:
    python3 check-fonts.py "Family One" "Family Two" [--chars "ğĞşŞıİçÇöÖüÜ"]

Downloads the family's CSS from fonts.googleapis.com, reads every font file's
character map (needs `fonttools` and `brotli`), and prints one line per family:
OK, MISSING <chars>, or NOT FOUND. Without fonttools it falls back to checking
that a latin-ext subset exists, which is weaker: some fonts ship latin-ext but
still lack İ.
"""
import io
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36"
DEFAULT_CHARS = "ğĞşŞıİçÇöÖüÜ"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=20).read()


def main(argv):
    chars = DEFAULT_CHARS
    if "--chars" in argv:
        i = argv.index("--chars")
        chars = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    if not argv:
        print(__doc__.strip())
        return 2
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        TTFont = None
        print("fonttools not installed: falling back to the latin-ext subset check")

    bad = 0
    for family in argv:
        url = "https://fonts.googleapis.com/css2?family=" + urllib.parse.quote_plus(family)
        try:
            css = get(url).decode()
        except urllib.error.HTTPError:
            print(f"{family}: NOT FOUND")
            bad += 1
            continue
        if TTFont is None:
            ok = "latin-ext" in css
            print(f"{family}: {'latin-ext present' if ok else 'NO latin-ext'}")
            bad += not ok
            continue
        cps = set()
        for font_url in set(re.findall(r"url\((https://[^)]+)\)", css)):
            cps |= set(TTFont(io.BytesIO(get(font_url))).getBestCmap())
        missing = "".join(c for c in chars if ord(c) not in cps)
        print(f"{family}: {'OK' if not missing else 'MISSING ' + missing}")
        bad += bool(missing)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
