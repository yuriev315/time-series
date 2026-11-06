#!/usr/bin/env python3
"""Turn the "优先阅读 10 篇" section of each category's search notes into
scripts/seeds/<slug>_top10_cn.json ([{"id", "rank", "reason"}]), mapping the category rank
to the unified paper id via scripts/registry_cn.json.

Usage: python3 -I scripts/make_top10_en.py <project_dir>
"""
import json
import re
import sys
from pathlib import Path

proj = Path(sys.argv[1])
reg = json.loads((proj / "scripts/registry_cn.json").read_text())
for notes in sorted((proj / "scripts/seeds").glob("*_notes_cn.md")):
    slug = notes.name.replace("_notes_cn.md", "")
    if not re.match(r"\d\d_", slug):
        continue
    text = notes.read_text()
    m = re.search(r"优先阅读[^\n]*\n(.*?)(\n## |\Z)", text, re.S)
    if not m:
        continue
    by_rank = {e["ranks"][slug]: e["id"] for e in reg if slug in e["ranks"]}
    out = []
    for line in m.group(1).splitlines():
        r = re.search(r"(?:rank\s*|第\s*)(\d+)", line, re.I)
        if not r or not re.match(r"\s*(\d+[.、)]|[-*|])", line):
            continue
        rk = int(r.group(1))
        rest = line[r.end():]
        # notes use "*Title*：reason", "Title——reason" or "Title — reason"; titles may contain ":"
        for sep in ("：", "——", " — ", "—", ": "):
            if sep in rest:
                rest = rest.split(sep, 1)[1]
                break
        reason = rest.strip(" *|—–-")
        if rk in by_rank:
            out.append({"id": by_rank[rk], "rank": rk, "reason": reason})
    (proj / f"scripts/seeds/{slug}_top10_cn.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(slug, len(out))
