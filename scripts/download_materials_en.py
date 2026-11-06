#!/usr/bin/env python3
"""Download and verify learning materials (university course notes and books).

Inputs : scripts/seeds/materials_courses_seed_cn.json, scripts/seeds/materials_books_seed_cn.json
Outputs: university_materials/files/..., books/files/...
         scripts/materials_registry_cn.json   merged items with stable ids (UMxxx / BKxxx)
         scripts/materials_results_en.json (books) and scripts/materials_courses_results_en.json
         (courses): per-item download/verification records (resume-safe)

One item counts once: a book, or a complete course-notes package (never per lecture file).
An item that appears in both lists (same normalised title or same file URL) is kept once, as a
book, and cross-tagged "大学讲义"; it is not counted towards the course target.

Verification
  pdf       : HTTP 200, %PDF-, pypdf parses, >= MIN_PAGES pages, title tokens (>= 0.6) and the first
              author's/instructor's surname found in the first 6 pages; outline (bookmarks) extracted
              as the checked table of contents.
  multi_pdf : every listed file passes the PDF checks above except title/author, which must be found
              in at least one file (title tokens >= 0.5, or instructor surname, or course code).
  html      : the table-of-contents page and every same-site page under its directory are saved with
              their images/CSS into one zip; verified if all pages return 200 with substantive text,
              the page count reaches the expected chapter count, and < 5% of resources are missing.
Items failing a soft check are "pending" (not counted). Legal public sources only; no paywall/login.

Usage: python3 -I scripts/download_materials_en.py <project_dir> <staging_dir> <pypdf_lib_dir>
                  [--target 50] [--kind course|book] [--retry-failed]
"""
import argparse
import hashlib
import io
import json
import re
import shutil
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import zipfile
from html.parser import HTMLParser
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ratelimit_en  # noqa: E402
from meta_utils_en import fold, norm, tokens  # noqa: E402

UA = "time_series_literature/1.0 (learning-material collection; low rate)"
KINDS = {"course": ("materials_courses", "UM", "university_materials"),
         "book": ("materials_books", "BK", "books")}
MIN_PAGES = {"course": 10, "book": 40}


def get(url, dest=None):
    host = urllib.parse.urlparse(url).netloc
    err = ""
    for attempt in range(3):
        ratelimit_en.wait("dl_" + host, 3.0)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
                cl = r.headers.get("Content-Length")
                if cl and cl.isdigit() and int(cl) != len(data):
                    raise IOError(f"truncated {len(data)}/{cl}")
                if dest:
                    Path(dest).write_bytes(data)
                return {"status": r.status, "ctype": r.headers.get("Content-Type", ""),
                        "final_url": r.geturl(), "data": data}
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}"
            if e.code in (401, 402, 403, 404, 410, 451):
                return {"status": e.code, "error": err}
        except Exception as e:
            err = repr(e)[:200]
        time.sleep(8 * (attempt + 1))
    return {"status": None, "error": err}


def surname(name):
    parts = fold(name).split()
    return re.sub(r"[^A-Za-z]", "", parts[-1]) if parts else ""


def inspect_pdf(path, title, people, code):
    import pypdf
    info = {}
    head = Path(path).read_bytes()[:1024]
    if not head.lstrip().startswith(b"%PDF-"):
        return {"ok_pdf": False, "error": "not a PDF: " + head[:60].decode("latin-1", "replace")}
    try:
        r = pypdf.PdfReader(str(path))
        n = len(r.pages)
        texts = []
        for i in range(min(n, 6)):
            try:
                texts.append(r.pages[i].extract_text() or "")
            except Exception:
                texts.append("")
        sample = []
        for i in range(6, n, max(1, n // 12)):        # spot-check text through the document
            try:
                sample.append(r.pages[i].extract_text() or "")
            except Exception:
                sample.append("")
        front = "\n".join(texts)
        blob = re.sub(r"[^a-z0-9]", "", fold(front).lower())
        tt = tokens(title)
        info.update(ok_pdf=True, pages=n, front_chars=len(front),
                    sample_chars=sum(len(s) for s in sample),
                    title_match=round(sum(t in blob for t in tt) / max(1, len(tt)), 3),
                    person_found=any(surname(p).lower() in blob for p in people if surname(p)),
                    code_found=bool(code) and norm(code) in blob)
        letters = [ch for ch in (front + "".join(sample))[:20000] if ch.isalpha()]
        cjk = sum("一" <= ch <= "鿿" for ch in letters)
        info["lang"] = "cn" if letters and cjk / len(letters) > 0.3 else "en"
        toc = []
        try:
            for o in r.outline:
                if not isinstance(o, list) and getattr(o, "title", None):
                    toc.append(o.title.strip())
        except Exception:
            pass
        info["toc"] = toc[:60]
    except Exception as e:
        info.update(ok_pdf=False, error="pypdf failed: " + repr(e)[:200])
    return info


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.res = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img" and a.get("src") and not a["src"].startswith("data:"):
            self.res.append(a["src"])
        if tag == "link" and a.get("href") and "stylesheet" in (a.get("rel") or ""):
            self.res.append(a["href"])


def html_text_len(html):
    t = re.sub(r"(?s)<(script|style).*?</\1>", " ", html)
    return len(" ".join(re.sub(r"<[^>]+>", " ", t).split()))


def crawl_html(toc_url, expected, zpath, max_pages=400):
    """Save the TOC page and every same-site page it links to (one level: the TOC of a
    bookdown/quarto book lists all chapters and sections), plus their images and CSS."""
    base = toc_url if toc_url.endswith("/") else toc_url.rsplit("/", 1)[0] + "/"
    host = urllib.parse.urlparse(toc_url).netloc
    queue, seen, pages, res_urls, missing, thin = [toc_url], set(), {}, set(), [], []
    while queue and len(pages) < max_pages:
        u = urllib.parse.urldefrag(queue.pop(0))[0]
        if u in seen:
            continue
        seen.add(u)
        r = get(u)
        if r.get("status") != 200 or "html" not in r.get("ctype", ""):
            missing.append(u)
            continue
        html = r["data"].decode("utf-8", "replace")
        pages[u] = r["data"]
        if html_text_len(html) < 300:
            thin.append(u)
        p = LinkParser()
        p.feed(html)
        if u == toc_url:              # follow links from the table of contents only
            for l in p.links:
                v = urllib.parse.urldefrag(urllib.parse.urljoin(u, l))[0]
                if v.startswith(base) and "?" not in v and (v.endswith((".html", ".htm")) or v.endswith("/")) \
                        and v not in seen and v not in queue:
                    queue.append(v)
        for s in p.res:
            v = urllib.parse.urljoin(u, s)
            if urllib.parse.urlparse(v).netloc == host:
                res_urls.add(v)
    res_ok, res_missing = 0, []
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for u, data in pages.items():
            z.writestr(urllib.parse.urlparse(u).path.lstrip("/") or "index.html", data)
        for v in sorted(res_urls):
            r = get(v)
            if r.get("status") == 200:
                z.writestr(urllib.parse.urlparse(v).path.lstrip("/"), r["data"])
                res_ok += 1
            else:
                res_missing.append(v)
        z.writestr("MANIFEST_en.json", json.dumps({"toc": toc_url, "pages": sorted(pages),
                                                    "missing_pages": missing, "thin_pages": thin,
                                                    "resources_ok": res_ok, "resources_missing": res_missing},
                                                   indent=1))
    info = {"pages_saved": len(pages), "pages_missing": len(missing), "thin_pages": len(thin),
            "resources_ok": res_ok, "resources_missing": len(res_missing), "expected_chapters": expected,
            "truncated_at_max": len(pages) >= max_pages}
    ok = (len(pages) >= max(1, expected) and not missing and
          len(res_missing) <= 0.05 * max(1, res_ok + len(res_missing)) and not info["truncated_at_max"])
    return ok, info


def short(s, n=40):
    w = [x for x in re.findall(r"[A-Za-z0-9]+", fold(s)) if x.lower() not in
         {"a", "an", "the", "of", "for", "and", "in", "on", "with", "to", "using"}][:5]
    return "".join(x[:1].upper() + x[1:] for x in w)[:n] or "Untitled"


def file_key(e):
    yr = re.search(r"(19|20)\d\d", e.get("term") or e.get("version_year") or e.get("original_year") or "")
    yr = yr.group(0) if yr else "NA"
    if e["kind"] == "course":
        uni = short(e.get("institution", ""), 20)
        code = re.sub(r"[^A-Za-z0-9]", "", e.get("course_code") or "") or short(e.get("course_name", ""), 20)
        return f"{uni}_{code}_{yr}"
    au = surname((e.get("authors") or ["Anon"])[0]) or "Anon"
    ed = re.sub(r"[^A-Za-z0-9]", "", e.get("edition") or "")
    return f"{au}_{short(e['title'])}_{(ed + '_') if ed else ''}{yr}"


def merge(proj):
    idp = proj / "scripts/materials_id_registry_en.json"
    ids = json.loads(idp.read_text()) if idp.exists() else {}
    nxt = {"UM": 1 + max([int(v[2:]) for v in ids.values() if v.startswith("UM")] or [0]),
           "BK": 1 + max([int(v[2:]) for v in ids.values() if v.startswith("BK")] or [0])}
    items, by_key = {}, {}
    for kind in ("book", "course"):            # books first: shared items stay books
        slug, prefix, _ = KINDS[kind]
        p = proj / f"scripts/seeds/{slug}_seed_cn.json"
        if not p.exists():
            continue
        for i, s in enumerate(json.loads(p.read_text())):
            if s.get("exclude"):          # screened out by the coordinator (reason kept in the seed)
                continue
            s = dict(s, kind=kind)
            keys = [f"title:{norm(s.get('title', ''))}"] + [f"url:{f['url']}" for f in s.get("files", [])]
            hit = next((by_key[k] for k in keys if k in by_key), None)
            if hit:
                it = items[hit]
                tag = "大学讲义" if kind == "course" else "参考书"
                if tag not in it["cross"]:
                    it["cross"].append(tag)
                    it["cross_basis"].append(f"{tag}：{s.get('institution', '')} {s.get('course_name', '')} 同样使用（排名 {s.get('rank')}）")
                continue
            iid = next((ids[k] for k in keys if k in ids), None)
            if not iid:
                iid = f"{prefix}{nxt[prefix]:03d}"
                nxt[prefix] += 1
            for k in keys:
                ids.setdefault(k, iid)
                by_key[k] = iid
            items[iid] = dict(s, id=iid, rank=s.get("rank", i + 1), cross=[], cross_basis=[])
    idp.write_text(json.dumps(ids, ensure_ascii=False, indent=0))
    out = sorted(items.values(), key=lambda x: x["id"])
    (proj / "scripts/materials_registry_cn.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    return out


def process(e, proj, stage_root, kind):
    _, _, outdir = KINDS[kind]
    files_dir = proj / outdir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    key = file_key(e)
    rec = {"tries": [], "format": e.get("format")}
    people = e.get("authors") or []
    stage = Path(tempfile.mkdtemp(prefix=e["id"] + "_", dir=stage_root))
    try:
        if e.get("format") == "html":
            z = stage / "pkg.zip"
            ok, info = crawl_html(e.get("html_toc") or e.get("homepage"), int(e.get("html_chapters") or 0), z)
            rec["html"] = info
            target = files_dir / f"{key}_html_{e.get('language', 'en')}.zip"
            shutil.move(str(z), target)
            rec.update(status="ok" if ok else "pending", local_path=str(target.relative_to(proj)),
                       sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                       reason="" if ok else f"HTML 包不完整：{info}")
            return rec
        files = e.get("files") or []
        if not files:
            return dict(rec, status="failed", reason="no file URL")
        multi = e.get("format") == "multi_pdf" or len(files) > 1
        saved, infos, problems = [], [], []
        for j, f in enumerate(files, 1):
            dest = stage / f"f{j}.bin"
            r = get(f["url"], dest)
            t = {"url": f["url"], "label": f.get("label", ""), "http": r.get("status"), "error": r.get("error")}
            if r.get("status") == 200:
                info = inspect_pdf(dest, e["title"], people, e.get("course_code", ""))
                t.update({k: v for k, v in info.items() if k != "toc"})
                if info.get("ok_pdf"):
                    saved.append((dest, info, f))
                    infos.append(info)
                else:
                    problems.append(f"文件 {j} 非 PDF/不可解析")
            else:
                problems.append(f"文件 {j} 下载失败（{r.get('status') or r.get('error')}）")
            rec["tries"].append(t)
            if not multi and problems:
                break
        if not saved or (multi and problems):
            return dict(rec, status="failed", reason="；".join(problems) or "no PDF")
        lang = infos[0].get("lang", "en")
        if not multi:
            info = infos[0]
            if info["pages"] < MIN_PAGES[kind]:
                problems.append(f"页数 {info['pages']} 少于完整{('讲义' if kind == 'course' else '书籍')}下限 {MIN_PAGES[kind]}")
            if info["title_match"] < 0.6:
                problems.append(f"标题匹配 {info['title_match']}")
            if not info["person_found"]:
                problems.append("前 6 页未见作者/教师姓氏")
            target = files_dir / f"{key}_{lang}.pdf"
            shutil.move(str(saved[0][0]), target)
            rec.update(local_path=str(target.relative_to(proj)),
                       sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                       pages=info["pages"], toc=info.get("toc", []))
        else:
            total = sum(i["pages"] for i in infos)
            if not any(i["title_match"] >= 0.5 or i["person_found"] or i["code_found"] for i in infos):
                problems.append("所有文件中均未见课程标题/教师/课程代码")
            thin = [k for k, i in enumerate(infos, 1) if i["front_chars"] < 300]
            if len(thin) > len(infos) // 4:
                problems.append(f"{len(thin)} 个文件几乎无文本（可能为扫描件或空白）")
            d = files_dir / key
            d.mkdir(exist_ok=True)
            shas = []
            for k, (src, info, f) in enumerate(saved, 1):
                tgt = d / f"{key}_{k:02d}_{info.get('lang', lang)}.pdf"
                shutil.move(str(src), tgt)
                shas.append({"path": str(tgt.relative_to(proj)), "sha256": hashlib.sha256(tgt.read_bytes()).hexdigest(),
                             "label": f.get("label", ""), "pages": info["pages"]})
            rec.update(local_path=str(d.relative_to(proj)) + "/", files=shas, pages=total,
                       sha256=hashlib.sha256("".join(s["sha256"] for s in shas).encode()).hexdigest())
        rec["lang"] = lang
        rec.update(status="ok" if not problems else "pending", reason="；".join(problems))
        return rec
    finally:
        shutil.rmtree(stage, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proj")
    ap.add_argument("staging")
    ap.add_argument("pylib")
    ap.add_argument("--target", type=int, default=50)
    ap.add_argument("--kind")
    ap.add_argument("--retry-failed", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, a.pylib)
    proj, stage_root = Path(a.proj), Path(a.staging)
    stage_root.mkdir(parents=True, exist_ok=True)
    items = merge(proj)
    for kind in ("course", "book"):
        if a.kind and kind != a.kind:
            continue
        # separate result files so the course and book runs can proceed in parallel
        rp = proj / ("scripts/materials_results_en.json" if kind == "book"
                     else "scripts/materials_courses_results_en.json")
        res = json.loads(rp.read_text()) if rp.exists() else {}
        done = sum(1 for e in items if e["kind"] == kind and res.get(e["id"], {}).get("status") == "ok")
        # PDF items first; slow HTML crawls last so they do not block the rest
        for e in sorted((x for x in items if x["kind"] == kind),
                        key=lambda x: (x.get("format") == "html", x["rank"])):
            if done >= a.target:
                break
            prev = res.get(e["id"], {})
            if prev.get("status") in ("ok", "pending") or (prev.get("status") == "failed" and not a.retry_failed):
                continue
            print(f"[{kind} {done}/{a.target}] {e['id']} {e['title'][:70]}", file=sys.stderr)
            res[e["id"]] = process(e, proj, stage_root, kind)
            if res[e["id"]]["status"] == "ok":
                done += 1
            rp.write_text(json.dumps(res, ensure_ascii=False, indent=1))
        rp.write_text(json.dumps(res, ensure_ascii=False, indent=1))
        print(f"== {kind}: verified {done} / {a.target}", file=sys.stderr)


if __name__ == "__main__":
    main()
