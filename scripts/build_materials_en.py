#!/usr/bin/env python3
"""Build catalogues and reading maps for learning materials (courses and books).

Inputs : scripts/materials_registry_cn.json, scripts/materials_results_en.json (books),
         scripts/materials_courses_results_en.json (courses),
         optional scripts/seeds/materials_<kind>_top_cn.json  [{"id": ..., "reason": ...}]
Outputs: university_materials/catalog_cn.csv, university_materials/reading_map_cn.md,
         books/catalog_cn.csv, books/reading_map_cn.md,
         scripts/materials_checksums_en.txt (sha256sum lines for every verified file),
         scripts/materials_stats_en.json

Only items whose files were completely downloaded and verified ("ok") are counted. Download
verification checks completeness and identity (title/author/pages/TOC); it is NOT a reading of
the content, and the catalogue says so.

Usage: python3 -I scripts/build_materials_en.py <project_dir>
"""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

STATUS = {"ok": "已核验（计入）", "pending": "待核验（不计入）", "failed": "下载失败（不计入）"}
KIND = {"course": ("university_materials", "大学课程教材与完整讲义", "materials_courses_results_en.json"),
        "book": ("books", "教科书、专著与参考书", "materials_results_en.json")}


def year_of(e):
    m = re.search(r"(19|20)\d\d", e.get("term") or e.get("version_year") or "")
    return int(m.group(0)) if m else None


def main():
    proj = Path(sys.argv[1])
    items = json.loads((proj / "scripts/materials_registry_cn.json").read_text())
    sums, stats = [], {}
    for kind, (outdir, cname, resfile) in KIND.items():
        rp = proj / "scripts" / resfile
        res = json.loads(rp.read_text()) if rp.exists() else {}
        rows = []
        for e in sorted((x for x in items if x["kind"] == kind), key=lambda x: x["rank"]):
            r = res.get(e["id"])
            if not r:
                continue                       # reserve never attempted
            st = r.get("status")
            if st == "ok":
                if r.get("files"):
                    sums += [f"{f['sha256']}  {f['path']}" for f in r["files"]]
                elif r.get("local_path"):
                    sums.append(f"{r['sha256']}  {r['local_path']}")
            if r.get("html"):
                h = r["html"]
                integ = (f"HTML 离线包：保存页面 {h['pages_saved']}（目录预期章节 {h['expected_chapters']}），"
                         f"缺失页面 {h['pages_missing']}，资源成功 {h['resources_ok']}、缺失 {h['resources_missing']}")
            elif r.get("files"):
                integ = f"多文件讲义包：{len(r['files'])} 个文件全部下载并可解析，共 {r.get('pages')} 页"
            elif r.get("pages"):
                integ = f"单一 PDF：{r.get('pages')} 页，可解析"
            else:
                integ = ""
            if r.get("manual_check"):
                integ = (integ + "；" if integ else "") + r["manual_check"]
            vy = year_of(e)
            rows.append({
                "编号": e["id"], "类型": "大学讲义" if kind == "course" else "书籍", "排名": e["rank"],
                "标题": e["title"], "作者或教师": "; ".join(e.get("authors") or []),
                "学校或出版社": e.get("institution") or e.get("publisher", ""),
                "课程名称": e.get("course_name", ""), "课程代码": e.get("course_code", ""),
                "学期": e.get("term", ""), "先修要求": e.get("prerequisites", ""),
                "出版社": e.get("publisher", ""), "版本": e.get("edition", ""),
                "原著年份": e.get("original_year", ""), "版本年份": e.get("version_year", ""),
                "年份类别": ("近三年版本/学期" if vy and vy >= 2023 else ("经典/较早版本" if vy else "年份待核实")),
                "经典保留理由": e.get("classic_reason", ""),
                "原始来源": e.get("homepage", ""),
                "下载文件 URL": " | ".join(f["url"] for f in e.get("files", [])) or e.get("html_toc", ""),
                "本地路径": r.get("local_path", ""), "格式": {"pdf": "PDF", "multi_pdf": "多文件 PDF 讲义包",
                                                       "html": "官方 HTML 离线包（zip）"}.get(e.get("format"), e.get("format", "")),
                "语言": r.get("lang") or e.get("language", ""),
                "下载状态": STATUS.get(st, st), "完整性核验": integ,
                "未通过原因": r.get("reason", "") if st != "ok" else "",
                "完整性依据（种子）": e.get("completeness_evidence", ""), "合法依据": e.get("legal_basis", ""),
                "SHA256": r.get("sha256", "") if st == "ok" else "",
                "目录（PDF 书签，已检查）": " / ".join((r.get("toc") or [])[:40]),
                "主题覆盖": "; ".join(e.get("topics") or []), "难度": e.get("level", ""),
                "推荐阅读顺序": e.get("order_hint", ""),
                "交叉标注": "; ".join(e.get("cross") or []) or e.get("cross_kind", ""),
                "简介": e.get("summary", ""),
                "简介依据": (e.get("summary_basis") or "官方页面描述与目录") + "；仅检查目录与正文完整性，未精读",
                "选入理由": e.get("reason", ""),
                "阅读优先级": {1: "高", 2: "中", 3: "低"}.get(e.get("priority"), ""),
                "_status": st, "_year": vy, "_level": e.get("level", ""), "_topics": e.get("topics") or [],
            })
        d = proj / outdir
        d.mkdir(exist_ok=True)
        pub = [k for k in (rows[0] if rows else {}) if not k.startswith("_")]
        if rows:
            with open(d / "catalog_cn.csv", "w", newline="", encoding="utf-8-sig") as f:
                w = csv.DictWriter(f, fieldnames=pub, extrasaction="ignore")
                w.writeheader()
                w.writerows(rows)
        ok = [r for r in rows if r["_status"] == "ok"]
        yd = Counter("年份待核实" if not r["_year"] else ("2023 及以后" if r["_year"] >= 2023 else
                     "2018–2022" if r["_year"] >= 2018 else "2010–2017" if r["_year"] >= 2010 else "2009 及以前")
                     for r in ok)
        st = {"name": cname, "verified": len(ok), "pending": sum(r["_status"] == "pending" for r in rows),
              "failed": sum(r["_status"] == "failed" for r in rows), "year_distribution": dict(yd),
              "formats": dict(Counter(r["格式"] for r in ok)),
              "topics": dict(Counter(t for r in ok for t in r["_topics"]).most_common())}
        st["progress"] = f"已核验 {st['verified']} / 目标约 50；待核验 {st['pending']}；下载失败 {st['failed']}。"
        stats[kind] = st
        write_map(proj, d, kind, cname, ok, st)
    (proj / "scripts/materials_checksums_en.txt").write_text("\n".join(sorted(sums, key=lambda x: x.split()[1])) + "\n")
    (proj / "scripts/materials_stats_en.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1))
    for k, s in stats.items():
        print(s["name"], s["progress"], s["year_distribution"], s["formats"])


def write_map(proj, d, kind, cname, ok, st):
    top_p = proj / f"scripts/seeds/materials_{'courses' if kind == 'course' else 'books'}_top_cn.json"
    top = json.loads(top_p.read_text()) if top_p.exists() else []
    by = {r["编号"]: r for r in ok}
    L = [f"# {cname}：阅读路线图", "", f"进度：{st['progress']}",
         "说明：“已核验”指已检查文件完整性、目录（书签）与标题/作者一致，不代表已精读。", "",
         "## 优先阅读", "", "| 顺序 | 编号 | 资料 | 用途 |", "|---|---|---|---|"]
    n = 0
    for t in top:
        r = by.get(t["id"])
        if r:
            n += 1
            L.append(f"| {n} | {r['编号']} | [{r['标题']}](../{r['本地路径']}) | {t['reason']} |")
    if not n:
        L.append("| - | - | （待整理） | - |")
    for lvl in ("入门", "进阶", "高级"):
        rs = [r for r in ok if r["_level"] == lvl]
        if not rs:
            continue
        L += ["", f"## {lvl}", ""]
        for r in sorted(rs, key=lambda r: r["排名"]):
            who = r["学校或出版社"] + (f" {r['课程代码']}" if r["课程代码"] else "")
            L.append(f"- {r['编号']} [{r['标题']}](../{r['本地路径']}) — {r['作者或教师']}；{who}；"
                     f"{r['学期'] or r['版本年份']}；主题：{r['主题覆盖']}；建议：{r['推荐阅读顺序']}")
    rest = [r for r in ok if r["_level"] not in ("入门", "进阶", "高级")]
    if rest:
        L += ["", "## 其他", ""] + [f"- {r['编号']} [{r['标题']}](../{r['本地路径']})" for r in rest]
    (d / "reading_map_cn.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
