#!/usr/bin/env python3
"""Verify conference venues against official proceedings index pages.

arXiv "comments" only carry the authors' own claim of acceptance. This script
fetches each official proceedings index page once and looks for the exact
(normalised) title of every seed entry, so a venue can be marked as verified
from the original publisher listing.

Output: scripts/venue_check_en.json  {seed_id: [{"venue":..., "index":..., "match":...}]}

Usage: python3 -I scripts/verify_venues_en.py <project_dir>
"""
import json
import re
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path

UA = "time_series_literature/1.0 (literature collection; low rate)"
INDEXES = {
    "ICML 2024 (PMLR v235)": "https://proceedings.mlr.press/v235/",
    "ICML 2025 (PMLR v267)": "https://proceedings.mlr.press/v267/",
    "AISTATS 2025 (PMLR v258)": "https://proceedings.mlr.press/v258/",
    "NeurIPS 2024": "https://papers.nips.cc/paper_files/paper/2024",
    "NeurIPS 2025": "https://papers.nips.cc/paper_files/paper/2025",
    "ICLR 2024": "https://proceedings.iclr.cc/paper_files/paper/2024",
    "ICLR 2025": "https://proceedings.iclr.cc/paper_files/paper/2025",
    "PVLDB vol 17 (2024)": "https://www.vldb.org/pvldb/volumes/17/",
}


def norm(s):
    s = unicodedata.normalize("NFKD", re.sub(r"<[^>]+>", " ", s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", s.lower())


def fetch(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except Exception as e:
            err = repr(e)
            print(f"  retry {attempt + 1}/3 {url}: {err}", file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    return None, err


def main():
    proj = Path(sys.argv[1])
    meta = json.loads((proj / "scripts/metadata_cache_en.json").read_text())
    titles = {}
    for sid, m in meta.items():
        t = (m.get("arxiv") or {}).get("title") or (m.get("crossref") or {}).get("title") or ""
        if t:
            titles[sid] = t
    out = {sid: [] for sid in titles}
    status = {}
    for venue, url in INDEXES.items():
        code, page = fetch(url)
        status[venue] = {"url": url, "http_status": code, "chars": len(page) if code == 200 else 0}
        print(f"{venue}: HTTP {code}, {status[venue]['chars']} chars", file=sys.stderr)
        if code != 200:
            continue
        blob = norm(page)
        for sid, t in titles.items():
            full = norm(t)
            # Titles sometimes change between arXiv and proceedings (e.g. a "Position:" prefix
            # or a subtitle), so also try the part before the colon when it is long enough.
            head = norm(t.split(":")[0]) if ":" in t else ""
            if full and full in blob:
                out[sid].append({"venue": venue, "index": url, "match": "full_title"})
            elif len(head) >= 25 and head in blob:
                out[sid].append({"venue": venue, "index": url, "match": "title_before_colon"})
        time.sleep(3)
    (proj / "scripts/venue_check_en.json").write_text(
        json.dumps({"indexes": status, "matches": out}, ensure_ascii=False, indent=1))
    print("matched:", {k: [x["venue"] for x in v] for k, v in out.items() if v})


if __name__ == "__main__":
    main()
