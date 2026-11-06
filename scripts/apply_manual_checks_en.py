#!/usr/bin/env python3
"""Apply documented manual verification decisions (scripts/seeds/materials_manual_checks_cn.json)
to the materials result files. Each decision keeps its note; files of rejected duplicates are
removed when "delete_file" is set.

Usage: python3 -I scripts/apply_manual_checks_en.py <project_dir>
"""
import json
import shutil
import sys
from pathlib import Path

proj = Path(sys.argv[1])
checks = json.loads((proj / "scripts/seeds/materials_manual_checks_cn.json").read_text())
for fname in ("materials_results_en.json", "materials_courses_results_en.json"):
    p = proj / "scripts" / fname
    if not p.exists():
        continue
    res = json.loads(p.read_text())
    for iid, c in checks.items():
        if iid not in res:
            continue
        r = res[iid]
        r["status"] = c["status"]
        r["manual_check"] = c["note"]
        r["reason"] = "" if c["status"] == "ok" else c["note"]
        if c.get("delete_file") and r.get("local_path"):
            lp = proj / r["local_path"]
            if lp.is_dir():
                shutil.rmtree(lp)
            elif lp.exists():
                lp.unlink()
            r["local_path"], r["sha256"] = "", ""
        print(iid, r["status"])
    p.write_text(json.dumps(res, ensure_ascii=False, indent=1))
