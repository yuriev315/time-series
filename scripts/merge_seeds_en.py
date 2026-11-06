#!/usr/bin/env python3
"""Merge per-category seed lists into one registry with stable, unique IDs.

Inputs : scripts/seeds/<slug>_seed_cn.json  (one per category, ranked)
         scripts/seeds/01_general_methods_fields_cn.json (optional extra fields for TS001..)
         scripts/annotations_cn.json (summaries for the general-methods entries)
Output : scripts/registry_cn.json      merged entries (one per paper)
         scripts/id_registry_en.json   key -> id map (keys: arxiv:, doi:, title:) so IDs stay
                                       stable across re-runs (resume-safe)

De-duplication: the same arXiv id, DOI or normalised title found in several category lists
becomes one entry. Its primary category is the first category (in SLUGS order) that listed it;
the other categories are added to "cross" (each listing category also records its rank).

Usage: python3 -I scripts/merge_seeds_en.py <project_dir>
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

SLUGS = [("01_general_methods", "通用方法"), ("02_finance", "金融"), ("03_air_quality", "空气质量"),
         ("04_water_quality", "水质"), ("05_weather_climate", "气象与气候"), ("06_energy_power", "能源与电力"),
         ("07_hydrology", "水文与水资源"), ("08_transport", "交通与出行"), ("09_industrial", "工业与设备"),
         ("10_health", "医疗与公共卫生")]
NAME = dict(SLUGS)
FIELDS = ["sub", "task_type", "target", "dataset", "frequency", "horizon", "method_class", "exogenous",
          "spatial", "split", "code", "field_basis", "summary", "summary_basis", "reason", "priority",
          "era", "old_reason", "title", "first_author", "first_public_date", "date_source", "venue",
          "landing", "title_note", "doi_note"]


def norm_title(t):
    t = unicodedata.normalize("NFKD", re.sub(r"<[^>]+>", " ", t or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", t.lower())


def clean_doi(d):
    d = (d or "").strip()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d, flags=re.I)
    return d.lower()


def clean_arxiv(a):
    a = (a or "").strip()
    a = re.sub(r"^(arxiv:|https?://arxiv\.org/(abs|pdf)/)", "", a, flags=re.I)
    return re.sub(r"v\d+$", "", a).replace(".pdf", "")


def main():
    proj = Path(sys.argv[1])
    sd = proj / "scripts/seeds"
    idreg_path = proj / "scripts/id_registry_en.json"
    idreg = json.loads(idreg_path.read_text()) if idreg_path.exists() else {}
    next_n = max([int(v[2:]) for v in idreg.values()] + [58]) + 1

    general_fields = {}
    gf = sd / "01_general_methods_fields_cn.json"
    if gf.exists():
        general_fields = json.loads(gf.read_text())
    ann = json.loads((proj / "scripts/annotations_cn.json").read_text())

    reg = {}  # id -> entry
    for slug, cname in SLUGS:
        path = sd / f"{slug}_seed_cn.json"
        if not path.exists():
            continue
        seeds = json.loads(path.read_text())
        for i, s in enumerate(seeds):
            rank = s.get("rank") or (i + 1)
            ax, doi = clean_arxiv(s.get("arxiv")), clean_doi(s.get("doi"))
            nt = norm_title(s.get("title", ""))
            keys = [k for k in (ax and f"arxiv:{ax}", doi and f"doi:{doi}",
                                len(nt) > 20 and f"title:{nt}") if k]
            if slug == "01_general_methods":
                sid = s["id"]
            else:
                sid = next((idreg[k] for k in keys if k in idreg), None)
                if sid is None:
                    sid = f"TS{next_n:03d}"
                    next_n += 1
            for k in keys:
                idreg.setdefault(k, sid)

            if sid not in reg:
                e = {"id": sid, "primary_slug": slug, "primary": cname, "cross": [], "cross_basis": [],
                     "ranks": {}, "arxiv": ax, "doi": doi, "pdf_candidates": []}
                if slug == "01_general_methods":
                    f = general_fields.get(sid, {})
                    e.update({k: v for k, v in f.items() if k not in ("cross", "cross_basis")})
                    e.update(sub=s.get("sub", ""), reason=s["reason"], priority=s["priority"],
                             era=s.get("era", "recent"), old_reason=s.get("old_reason", ""),
                             summary=ann.get(sid, ""),
                             summary_basis=s.get("summary_basis", "摘要（arXiv API / Crossref 返回的摘要）"),
                             topic=s.get("topic", ""))
                    cross_in = f.get("cross", [])
                    cross_basis_in = f.get("cross_basis", "")
                else:
                    e.update({k: s.get(k, "") for k in FIELDS})
                    cross_in = s.get("cross", [])
                    cross_basis_in = s.get("cross_basis", "")
                reg[sid] = e
            else:
                e = reg[sid]
                e["arxiv"] = e["arxiv"] or ax
                e["doi"] = e["doi"] or doi
                cross_in = s.get("cross", [])
                cross_basis_in = s.get("cross_basis", "")
                if cname != e["primary"] and cname not in e["cross"]:
                    e["cross"].append(cname)
                    e["cross_basis"].append(f"{cname}：该类检索也独立选入（排名 {rank}）")
            e["ranks"][slug] = rank
            for c in cross_in or []:
                if c in NAME.values() and c != e["primary"] and c not in e["cross"]:
                    e["cross"].append(c)
                    if cross_basis_in:
                        e["cross_basis"].append(f"{c}：{cross_basis_in}")
            for u in s.get("pdf_candidates", []) or []:
                if u and u not in e["pdf_candidates"]:
                    e["pdf_candidates"].append(u)

    idreg_path.write_text(json.dumps(idreg, ensure_ascii=False, indent=0))
    out = sorted(reg.values(), key=lambda e: e["id"])
    (proj / "scripts/registry_cn.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    per = {slug: sum(1 for e in out if slug in e["ranks"]) for slug, _ in SLUGS}
    print(json.dumps({"entries": len(out), "listed_per_category": per,
                      "multi_listed": sum(len(e["ranks"]) > 1 for e in out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
