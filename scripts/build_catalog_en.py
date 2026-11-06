#!/usr/bin/env python3
"""Build all deliverable tables from registry + metadata + download results.

Outputs
  catalog_cn.csv                        whole library (every attempted entry, one row per paper)
  download_failures_cn.csv              failed / link-only / pending (not counted) entries
  checksums_en.sha256                   sha256sum list of verified PDFs (run from project root)
  domains/<slug>/catalog_cn.csv         rows of papers belonging to that category (primary or cross)
  domains/<slug>/reading_map_cn.md      generated reading map (unless curated, see CURATED)
  scripts/stats_en.json                 per-category and library-wide counts
  README_cn.md                          progress table between <!-- PROGRESS:START/END --> markers

Counting rules (user acceptance rules): only VERIFIED full-text PDFs count; recent share and all
quotas use verified papers as denominator; a paper counts once per category; cross-category
membership requires a recorded basis.

Usage: python3 -I scripts/build_catalog_en.py <project_dir>
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from meta_utils_en import (all_titles, first_public, norm, resolve_authors, resolve_title,  # noqa: E402
                           window_status)

SLUGS = [("01_general_methods", "通用方法"), ("02_finance", "金融"), ("03_air_quality", "空气质量"),
         ("04_water_quality", "水质"), ("05_weather_climate", "气象与气候"), ("06_energy_power", "能源与电力"),
         ("07_hydrology", "水文与水资源"), ("08_transport", "交通与出行"), ("09_industrial", "工业与设备"),
         ("10_health", "医疗与公共卫生")]
NAME2SLUG = {n: s for s, n in SLUGS}
CURATED = {"01_general_methods"}       # reading maps written by hand
TARGET = 50

# Hand-checked venue evidence and version notes for the general-methods round.
MANUAL_VENUE = {
    "TS038": ("NeurIPS 2025", "https://papers.neurips.cc/paper_files/paper/2025/hash/"
              "5356603f9c47399adfd372f77a677057-Abstract-Conference.html"),
}
VERSION_NOTES = {
    "TS003": "重大修订：v1（2025-02）标题为 “Beyond the Time Domain: Recent Advances on Frequency Transforms in Time Series Analysis”，后续版本改为现标题；下载为最新版。",
    "TS021": "重大修订：v4 增加带协变量预测评测、消融与局限讨论（据 arXiv comments）。",
    "TS037": "同一模型更早的技术报告为 arXiv:2407.07874（2024-07），属不同 arXiv 条目，未单独收录；本条为 2025 年论文（新增 BOOM 基准）。",
    "TS048": "重大修订：v1（2025-02）标题以 “Position:” 开头，v2（2026-01）改为现标题并注明 TMLR 接收。",
    "TS050": "v3 为技术报告修订（增加作者、更正参考文献，据 arXiv comments）。",
}
OLD_VERSION = {
    "TS054": ("出版社正式版（Journal of Statistical Software，开放获取）", "2008-07（PDF 首页；精度：月）"),
    "TS055": ("作者主页预印本（robjhyndman.com），非出版社排版版", "2005-11-02（PDF 首页注明日期）"),
    "TS056": ("出版社排版版（JASA 2007 Vol.102 No.477，PDF 首页含 © 2007 ASA），由作者主页（华盛顿大学 Raftery）自存档托管；出版社是否授权该自存档未核实", "2007-03（PDF 首页；精度：月）"),
    "TS057": ("作者主页工作论文/投稿版（robjhyndman.com/papers/cv-wp.pdf，首页注 Preprint submitted），非出版社排版版", "2017-07-23（PDF 元数据创建日期）"),
}
STATUS_CN = {"ok": "已核验全文", "pending": "待核验（不计入）", "failed": "下载失败（不计入）"}


def basis_text(b):
    return b if "未读全文" in b or "待全文核实" in b else b + "；未读全文，未核实全文结论"


def members(e):
    return [e["primary_slug"]] + [NAME2SLUG[c] for c in e.get("cross", []) if c in NAME2SLUG]


def version_label(sid, e, rec, d):
    ax = rec.get("arxiv") or {}
    lab = d.get("version_label", "")
    if sid in OLD_VERSION:
        return OLD_VERSION[sid]
    if lab.startswith("arXiv"):
        v = f"arXiv {ax.get('latest_version', '')}（预印本/作者版"
        v += "；正式发表版见 DOI，非出版社排版版）" if (e.get("doi") or ax.get("doi")) else "）"
        return v, (ax.get("updated") or "")[:10]
    if "publishedVersion" in lab:
        cr = (rec.get("crossref") or {}).get("dates") or {}
        return f"出版社正式版（{lab}）", cr.get("published-online") or cr.get("published-print") or "未核实"
    if "acceptedVersion" in lab:
        return f"作者接受稿，非出版社排版版（{lab}）", "未核实"
    if "submittedVersion" in lab:
        return f"投稿版/预印本，非出版社排版版（{lab}）", "未核实"
    if lab:
        host = re.sub(r"^https?://([^/]+).*", r"\1", d.get("pdf_url", ""))
        return f"版本未经元数据标注（{lab}；下载域名 {host}）", "未核实"
    return "", ""


def venue_info(sid, e, rec, vc):
    cr = rec.get("crossref") or {}
    ax = rec.get("arxiv") or {}
    if cr.get("container"):
        v = cr["container"] + (f", vol. {cr['volume']}" if cr.get("volume") else "") + \
            (f", pp. {cr['page']}" if cr.get("page") else "")
        dates = cr.get("dates") or {}
        formal = dates.get("published-online") or dates.get("published-print") or str(cr.get("year") or "")
        prec = {10: "日", 7: "月", 4: "年"}.get(len(formal), "")
        return v, "Crossref（DOI 元数据）", f"{formal}（精度：{prec}，Crossref）" if formal else "未核实"
    pp = rec.get("publisher_page") or {}
    if pp.get("venue"):
        return pp["venue"], f"出版方官方页面 citation 元数据：{pp['url']}", \
            f"{pp.get('publication_date')}（出版方页面）"
    if vc.get(sid):
        m = vc[sid][0]
        yr = re.search(r"20[0-9]{2}", m["venue"]).group(0)
        return m["venue"], f"官方论文集索引页标题匹配：{m['index']}", f"{yr}（会议年份，精度：年）"
    if sid in MANUAL_VENUE:
        v, url = MANUAL_VENUE[sid]
        return v, f"官方论文页：{url}", "2025（会议年份，精度：年）"
    claim = re.search(r"(NeurIPS|ICLR|ICML|AAAI|AISTATS|TMLR|KDD|VLDB|IJCAI|CIKM|WWW)[^.;,]*",
                      (ax.get("comment") or "") + " " + (ax.get("journal_ref") or ""))
    if claim:
        return (f"arXiv 预印本（作者在 arXiv comments/journal_ref 中声明：{claim.group(0).strip()}）",
                "仅 arXiv 自述，未在官方页面核实", "未核实")
    if ax.get("journal_ref"):
        return (f"arXiv 预印本（journal_ref：{ax['journal_ref'][:120]}）", "仅 arXiv journal_ref 自述，未核实", "未核实")
    if ax:
        return "arXiv 预印本", "未发现正式发表信息（未核实是否已发表）", "未核实/未发现"
    oa = rec.get("openalex") or {}
    src = next((l.get("source") for l in oa.get("locations", []) if l.get("source")), "")
    return (src or e.get("venue", "")), ("OpenAlex 来源字段" if src else "种子列表（未核实）"), \
        (oa.get("publication_date") or "未核实")


def main():
    proj = Path(sys.argv[1])
    reg = json.loads((proj / "scripts/registry_cn.json").read_text())
    meta = json.loads((proj / "scripts/metadata_cache_en.json").read_text())
    dl = json.loads((proj / "scripts/download_results_en.json").read_text())
    vcp = proj / "scripts/venue_check_en.json"
    vc = json.loads(vcp.read_text())["matches"] if vcp.exists() else {}

    rows, fails, sums = [], [], []
    for e in reg:
        sid = e["id"]
        d = dl.get(sid)
        if not d:          # reserve never attempted -> not part of the catalogue
            continue
        rec = meta.get(sid, {})
        ax = rec.get("arxiv") or {}
        title = resolve_title(rec, e)
        authors = resolve_authors(rec, e)
        fp, prec, fsrc = first_public(rec)
        window = window_status(fp, prec)
        claimed = e.get("era", "")
        flag = ""
        if claimed == "recent" and window != "近三年":
            flag = f"种子标为近三年，但核实为“{window}”"
        venue, vbasis, formal = venue_info(sid, e, rec, vc)
        version, vdate = version_label(sid, e, rec, d)
        doi = e.get("doi") or (ax.get("doi") or "").lower()
        landing = (ax.get("abs_url") or "").replace("http://", "https://") or \
            (f"https://doi.org/{doi}" if doi else e.get("landing", ""))
        st = d.get("status", "")
        c = d.get("checks_v2") or {}
        if st == "ok":
            check = (f"通过：HTTP 200；%PDF 头；pypdf 可解析 {c.get('pages')} 页、{c.get('text_chars')} 字符；"
                     f"标题匹配 {c.get('title_match')}；第一作者姓氏已见；参考文献节已见")
            sums.append(f"{d['sha256']}  {d['local_path']}")
        else:
            check = "未通过：" + (d.get("reason") or "")
        mem = members(e)
        row = {
            "文献编号": sid, "主分类": e["primary"],
            "交叉分类": "; ".join(e.get("cross", [])), "交叉分类依据": " | ".join(e.get("cross_basis", [])),
            "子方向": e.get("sub", "") or e.get("topic", ""),
            "时间窗口": "三年前（补充/基础）" if window == "三年前" else window, "时间核验备注": flag,
            "标题": title,
            "其他题名（版本间差异）": " | ".join(t for t in all_titles(rec, {}) if norm(t) != norm(title)),
            "作者": "; ".join(authors),
            "首次公开日期": fp, "日期精度": prec, "首次公开依据": fsrc, "正式发表日期": formal,
            "渠道": venue, "渠道核验依据": vbasis, "DOI": doi, "arXiv ID": e.get("arxiv") or rec.get("arxiv_via_openalex", ""),
            "原始页面": landing, "PDF URL": d.get("pdf_url", ""), "本地相对路径": d.get("local_path", ""),
            "版本": version, "下载版本日期": vdate, "版本说明": "；".join(x for x in (VERSION_NOTES.get(sid, ""), e.get("title_note", ""),
                                             e.get("doi_note", "")) if x),
            "下载状态": STATUS_CN.get(st, st), "核验状态": check, "SHA256": d.get("sha256", ""),
            "任务类型": e.get("task_type", ""), "预测目标": e.get("target", ""), "数据集": e.get("dataset", ""),
            "数据频率": e.get("frequency", ""), "预测跨度": e.get("horizon", ""),
            "方法类别": e.get("method_class", ""), "是否使用外生变量": e.get("exogenous", ""),
            "是否使用空间信息": e.get("spatial", ""), "评测切分方式": e.get("split", ""),
            "代码链接": e.get("code", ""), "字段依据": e.get("field_basis", ""),
            "选入理由": e.get("reason", ""), "三年前保留理由": e.get("old_reason", ""),
            "内容简介": e.get("summary", ""),
            "简介依据": basis_text(e.get("summary_basis") or "摘要"),
            "阅读优先级": {1: "高", 2: "中", 3: "低"}.get(e.get("priority"), ""),
            "_members": mem, "_status": st, "_window": window,
            "_ranks": e.get("ranks", {}),
        }
        rows.append(row)
        if st != "ok":
            fails.append({"文献编号": sid, "主分类": e["primary"], "状态": STATUS_CN.get(st, st),
                          "标题": title, "原始页面": landing,
                          "尝试的PDF URL": " | ".join(t.get("url", "") for t in d.get("tries", [])),
                          "原因": d.get("reason", ""), "本地暂存路径": d.get("local_path", ""),
                          "处理": "不计入完成数量；已按排名用备选论文补位" if st == "failed"
                          else "不计入完成数量；需人工核验后才可计入"})

    pub = [k for k in rows[0] if not k.startswith("_")]

    def write_csv(path, rs, fields):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
            w.writeheader()
            w.writerows(rs)

    write_csv(proj / "catalog_cn.csv", rows, pub)
    write_csv(proj / "download_failures_cn.csv", fails,
              ["文献编号", "主分类", "状态", "标题", "原始页面", "尝试的PDF URL", "原因", "本地暂存路径", "处理"])
    (proj / "checksums_en.sha256").write_text("\n".join(sorted(sums, key=lambda x: x.split()[1])) + "\n")

    stats = {"categories": {}}
    for slug, cname in SLUGS:
        rs = [r for r in rows if slug in r["_members"]]
        ok = [r for r in rs if r["_status"] == "ok"]
        rec_ok = [r for r in ok if r["_window"] == "近三年"]
        st = {
            "name": cname, "verified": len(ok),
            "verified_primary": sum(r["主分类"] == cname for r in ok),
            "verified_unique": sum(len(r["_members"]) == 1 for r in ok),
            "verified_cross_listed": sum(len(r["_members"]) > 1 for r in ok),
            "recent": len(rec_ok), "recent_share": round(len(rec_ok) / len(ok), 3) if ok else None,
            "old": sum(r["_window"] == "三年前" for r in ok),
            "date_pending": sum(r["_window"].startswith("待核实") for r in ok),
            "pending": sum(r["_status"] == "pending" for r in rs),
            "failed": sum(r["_status"] == "failed" for r in rs),
            "status": "达标" if len(ok) >= 45 else ("进行中" if len(ok) else "未开始"),
        }
        st["progress"] = f"已核验全文 {st['verified']} / 目标约 {TARGET}；待核验 {st['pending']}；下载失败 {st['failed']}。"
        stats["categories"][slug] = st
        dom = proj / "domains" / slug
        dom.mkdir(parents=True, exist_ok=True)
        drows = [{**r, "本类排名": r["_ranks"].get(slug, "交叉标注")}
                 for r in sorted(rs, key=lambda r: (r["_status"] != "ok", r["_ranks"].get(slug, 999), r["文献编号"]))]
        write_csv(dom / "catalog_cn.csv", drows, ["本类排名"] + pub)
        if slug not in CURATED and ok:
            write_reading_map(proj, dom, slug, cname, ok, st)
    files = list((proj / "pdfs").glob("*.pdf"))
    stats["library"] = {"unique_papers_in_catalog": len(rows),
                        "unique_verified_papers": sum(r["_status"] == "ok" for r in rows),
                        "pdf_files_verified": len(files),
                        "pending": sum(r["_status"] == "pending" for r in rows),
                        "failed": sum(r["_status"] == "failed" for r in rows)}
    (proj / "scripts/stats_en.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1))
    update_readme(proj, stats)
    print(json.dumps(stats["library"], ensure_ascii=False))
    for slug, st in stats["categories"].items():
        print(f"{st['name']}: {st['progress']} 近三年 {st['recent']}（{st['recent_share']}）旧 {st['old']}")


def write_reading_map(proj, dom, slug, cname, ok, st):
    top_path = proj / "scripts/seeds" / f"{slug}_top10_cn.json"
    top = json.loads(top_path.read_text()) if top_path.exists() else []
    byid = {r["文献编号"]: r for r in ok}
    lines = [f"# {cname}：阅读路线图", "",
             f"进度：{st['progress']} 近三年（已核验文献中）{st['recent']} 篇，占 {st['recent_share']}。",
             "编号对应 [catalog_cn.csv](catalog_cn.csv)；简介与字段均依据摘要，未读全文。", "",
             "## 优先阅读 10 篇", "", "| 顺序 | 编号 | 标题 | 理由 |", "|---|---|---|---|"]
    n = 0
    for t in top:
        r = byid.get(t["id"])
        if not r:
            continue
        n += 1
        lines.append(f"| {n} | {r['文献编号']} | [{r['标题']}](../../{r['本地相对路径']}) | {t['reason']} |")
        if n == 10:
            break
    if not top:
        lines.append("| - | - | （待整理） | - |")
    lines += ["", "## 按子方向", ""]
    groups = {}
    for r in sorted(ok, key=lambda r: (r["_ranks"].get(slug, 999), r["文献编号"])):
        groups.setdefault(r["子方向"] or "其他", []).append(r)
    for g, rs in groups.items():
        lines.append(f"### {g}")
        for r in rs:
            tag = "" if r["_window"] == "近三年" else f"【{r['_window']}】"
            lines.append(f"- {r['文献编号']}{tag}（{r['阅读优先级']}）[{r['标题']}](../../{r['本地相对路径']}) — "
                         f"{r['任务类型']}；目标：{r['预测目标']}；方法：{r['方法类别']}")
        lines.append("")
    (dom / "reading_map_cn.md").write_text("\n".join(lines) + "\n")


def update_readme(proj, stats):
    p = proj / "README_cn.md"
    if not p.exists():
        return
    lines = ["| 分类 | 进度 | 主分类 | 独有 | 跨类 | 近三年占比 | 三年前 | 状态 |", "|---|---|---|---|---|---|---|---|"]
    for slug, st in stats["categories"].items():
        share = f"{st['recent']}/{st['verified']}（{st['recent_share']:.1%}）" if st["verified"] else "-"
        lines.append(f"| [{st['name']}](domains/{slug}/) | {st['progress']} | {st['verified_primary']} | "
                     f"{st['verified_unique']} | {st['verified_cross_listed']} | {share} | {st['old']} | {st['status']} |")
        lib = stats["library"]
    lines.append("")
    lines.append(f"全库去重：已核验论文 {lib['unique_verified_papers']} 篇，已核验 PDF 文件 {lib['pdf_files_verified']} 个；"
                 f"待核验 {lib['pending']}；下载失败 {lib['failed']}（均不计入）。")
    text = p.read_text()
    block = "<!-- PROGRESS:START -->\n" + "\n".join(lines) + "\n<!-- PROGRESS:END -->"
    if "<!-- PROGRESS:START -->" in text:
        text = re.sub(r"<!-- PROGRESS:START -->.*?<!-- PROGRESS:END -->", block, text, flags=re.S)
    else:
        text += "\n## 总进度（脚本自动生成）\n\n" + block + "\n"
    p.write_text(text)


if __name__ == "__main__":
    main()
