#!/usr/bin/env python3
"""Download and verify full-text PDFs, category by category, until each category has
TARGET verified papers (ranked main list first, reserves only when needed).

A download counts as VERIFIED only if all of these hold:
  - HTTP 200 and the file starts with %PDF- and is fully saved;
  - pypdf parses it;
  - full text, not an abstract/preview page or supplement: >= 4 pages, >= 12,000 characters of
    extractable text, a references section is present, and it does not start as a supplement;
  - the target title is found on the first pages (token match >= 0.8);
  - the first author's surname is found on the first pages;
  - source URL, version label, local path and SHA256 are recorded.
Files that are real PDFs of the right paper but fail a soft check (e.g. title match 0.5-0.8,
author not found, no references heading) are kept in pending_pdfs/ as "pending" (not counted).

Before downloading, the seed title is compared with the title returned by arXiv/Crossref/OpenAlex;
a mismatch (wrong identifier) is recorded as a failure without downloading.

Candidate order: arXiv-listed papers -> arXiv latest version first; DOI-listed papers -> legal OA
copies (seed URLs, OpenAlex OA locations), then arXiv. Paywalled/login/captcha routes are never
attempted; 401/402/403/404/451 stop retries for that URL. Each URL is tried at most 3 times.
Rate limits are shared across processes (scripts/ratelimit_en.py).

Resume-safe: results in scripts/download_results_en.json; verified/pending/failed entries are
not re-attempted unless --retry-failed is given. Existing verified files from earlier rounds are
re-checked against the full-text and author rules (no re-download).

Usage:
  python3 -I scripts/download_papers_en.py <project_dir> <staging_dir> <pypdf_lib_dir>
         [--target 50] [--only <slug>] [--retry-failed]
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ratelimit_en  # noqa: E402
from meta_utils_en import (all_titles, fold, first_public, norm, resolve_authors,  # noqa: E402
                           resolve_title, surname, title_similarity, tokens)

UA = "time_series_literature/1.0 (literature collection; low rate)"
SLUGS = ["01_general_methods", "02_finance", "03_air_quality", "04_water_quality",
         "05_weather_climate", "06_energy_power", "07_hydrology", "08_transport",
         "09_industrial", "10_health"]
NAME2SLUG = {"通用方法": "01_general_methods", "金融": "02_finance", "空气质量": "03_air_quality",
             "水质": "04_water_quality", "气象与气候": "05_weather_climate",
             "能源与电力": "06_energy_power", "水文与水资源": "07_hydrology",
             "交通与出行": "08_transport", "工业与设备": "09_industrial", "医疗与公共卫生": "10_health"}
REF_RE = re.compile(r"\b(references|bibliography|literature cited|works cited|reference list)\b|参考文献",
                    re.I)


def raw_surname(authors):
    """Last name token without ASCII folding, so that transliteration variants can be tried."""
    parts = re.sub(r"[{}\\]", "", authors[0]).split() if authors else []
    return parts[-1] if parts else ""


def members(e):
    return {e["primary_slug"]} | {NAME2SLUG[c] for c in e.get("cross", []) if c in NAME2SLUG}


def short_title(title):
    title = fold(re.sub(r"<[^>]+>", "", title))
    head = title.split(":")[0].strip()
    if ":" in title and len(head.split()) <= 3:
        words = head.split()
    else:
        words = [w for w in re.findall(r"[A-Za-z0-9]+", title)
                 if w.lower() not in {"a", "an", "the", "of", "for", "and", "in", "on", "with", "to",
                                      "via", "by", "is", "are", "from", "at", "as", "using", "based"}][:4]
    out = "".join(w[:1].upper() + w[1:] for w in re.findall(r"[A-Za-z0-9]+", " ".join(words)))
    return out[:40] or "Untitled"


def fetch(url, dest):
    host = urllib.parse.urlparse(url).netloc
    key = "arxiv.org" if host.endswith("arxiv.org") else host
    interval = 4.0 if key == "arxiv.org" else 3.0
    err = ""
    for attempt in range(3):
        ratelimit_en.wait("dl_" + key, interval)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*"})
            with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
                shutil.copyfileobj(r, f)
                cl = r.headers.get("Content-Length")
                size = dest.stat().st_size
                if cl and cl.isdigit() and int(cl) != size:
                    err = f"truncated ({size}/{cl} bytes)"
                    raise IOError(err)
                return {"http_status": r.status, "content_type": r.headers.get("Content-Type", ""),
                        "final_url": r.geturl(), "attempts": attempt + 1, "bytes": size}
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}"
            if e.code in (401, 402, 403, 404, 410, 451):
                return {"http_status": e.code, "error": err, "attempts": attempt + 1}
        except Exception as e:
            err = err or repr(e)[:200]
        time.sleep(8 * (attempt + 1))
    return {"http_status": None, "error": err, "attempts": 3}


def inspect_pdf(path, titles, author_surname):
    if isinstance(titles, str):
        titles = [titles]
    best = None
    for t in titles or [""]:
        info = _inspect_pdf(path, t, author_surname)
        if best is None or info.get("title_match", 0) > best.get("title_match", 0):
            best = info
            best["matched_title"] = t
    return best


def _inspect_pdf(path, title, author_surname):
    import pypdf
    info = {}
    with open(path, "rb") as f:
        head = f.read(1024)
    info["magic_ok"] = head.lstrip().startswith(b"%PDF-")
    if not info["magic_ok"]:
        info["error"] = "not a PDF: " + head[:80].decode("latin-1", "replace").replace("\n", " ")
        return info
    try:
        reader = pypdf.PdfReader(str(path))
        n = len(reader.pages)
        info["pages"] = n
        texts = []
        for i in range(min(n, 80)):
            try:
                texts.append(reader.pages[i].extract_text() or "")
            except Exception:
                texts.append("")
        first = "\n".join(texts[:2])
        whole = "\n".join(texts)
        info["text_chars"] = len(whole)
        info["first_text_head"] = " ".join(first.split())[:300]
        tt = tokens(title)
        blob = re.sub(r"[^a-z0-9]", "", fold(first).lower())
        if tt and blob and sum(t in blob for t in tt) / len(tt) < 0.8:   # cover page? try page 3
            blob3 = re.sub(r"[^a-z0-9]", "", fold("\n".join(texts[:3])).lower())
            blob = blob3 if blob3 else blob
        info["title_match"] = round(sum(t in blob for t in tt) / max(1, len(tt)), 3)
        # accept plain ASCII folding and German-style transliteration (Schlüter -> Schlueter)
        translit = author_surname.translate(str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
                                                           "Ä": "Ae", "Ö": "Oe", "Ü": "Ue"}))
        variants = {re.sub(r"[^a-z]", "", fold(v).lower()) for v in (author_surname, translit)} - {""}
        info["author_found"] = any(v in blob for v in variants)
        info["references_found"] = bool(REF_RE.search(whole))
        info["supplement_only"] = bool(re.match(r"\s*(supplementary|supporting information|appendix)",
                                                first, re.I))
        letters = [ch for ch in whole[:20000] if ch.isalpha()]
        cjk = sum("一" <= ch <= "鿿" for ch in letters)
        info["lang"] = "cn" if letters and cjk / len(letters) > 0.3 else "en"
        info["parse_ok"] = True
    except Exception as e:
        info["parse_ok"] = False
        info["error"] = "pypdf failed: " + repr(e)[:200]
    return info


def classify(info):
    """-> ('ok'|'pending'|'reject', reason)"""
    if not info.get("magic_ok") or not info.get("parse_ok"):
        return "reject", info.get("error", "not parseable")
    if info.get("title_match", 0) < 0.5:
        return "reject", f"wrong document (title match {info.get('title_match')})"
    problems = []
    if info.get("pages", 0) < 4 or info.get("text_chars", 0) < 12000:
        problems.append(f"not full text? pages={info.get('pages')} chars={info.get('text_chars')}")
    if info.get("supplement_only"):
        problems.append("looks like supplementary material")
    if info.get("title_match", 0) < 0.8:
        problems.append(f"title match {info.get('title_match')}")
    if not info.get("author_found"):
        problems.append("first-author surname not found on first pages")
    if not info.get("references_found"):
        problems.append("no references section detected")
    return ("ok", "") if not problems else ("pending", "; ".join(problems))


def candidates(e, rec):
    ax = (rec.get("arxiv") or {}).get("latest_version")
    arx = [("arXiv " + ax + "（预印本/作者版）", "https://arxiv.org/pdf/" + ax)] if ax else []
    oa_locs = {}
    for loc in (rec.get("openalex") or {}).get("locations", []):
        if loc.get("is_oa") and loc.get("pdf_url") and "arxiv.org" not in loc["pdf_url"]:
            oa_locs[loc["pdf_url"]] = f"OpenAlex OA: {loc.get('version') or '版本未标注'} @ {loc.get('source') or loc.get('host_org') or '未知来源'}"
    seeds = [(oa_locs.get(u, "种子列表提供的 OA 链接（版本未标注）"), u) for u in e.get("pdf_candidates", [])
             if "arxiv.org" not in u]
    others = [(lab, u) for u, lab in oa_locs.items() if u not in e.get("pdf_candidates", [])]
    order = arx + seeds + others if e.get("arxiv") else seeds + others + arx
    seen, out = set(), []
    for lab, u in order:
        if u not in seen:
            seen.add(u)
            out.append((lab, u))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("proj")
    ap.add_argument("staging")
    ap.add_argument("pylib")
    ap.add_argument("--target", type=int, default=50)
    ap.add_argument("--only")
    ap.add_argument("--retry-failed", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, a.pylib)
    proj, staging_root = Path(a.proj), Path(a.staging)
    reg = {e["id"]: e for e in json.loads((proj / "scripts/registry_cn.json").read_text())}
    meta = json.loads((proj / "scripts/metadata_cache_en.json").read_text())
    res_path = proj / "scripts/download_results_en.json"
    results = json.loads(res_path.read_text()) if res_path.exists() else {}
    pdf_dir, pend_dir = proj / "pdfs", proj / "pending_pdfs"
    pdf_dir.mkdir(exist_ok=True)
    staging_root.mkdir(parents=True, exist_ok=True)

    def save():
        res_path.write_text(json.dumps(results, ensure_ascii=False, indent=1))

    def place(sid, src, lang, rec_out, status, year, authors, title):
        fname = f"{year}_{surname(authors[0]) if authors else 'Anon'}_{short_title(title)}_{lang}.pdf"
        target_dir = pdf_dir if status == "ok" else pend_dir
        target_dir.mkdir(exist_ok=True)
        target = target_dir / fname
        sha = hashlib.sha256(Path(src).read_bytes()).hexdigest()
        clash = next((k for k, r in results.items() if r.get("sha256") == sha and k != sid
                      and r.get("status") in ("ok", "pending")), None)
        if clash:
            return f"duplicate of {clash} (same SHA256)"
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() != sha:
            target = target_dir / fname.replace(f"_{lang}.pdf", f"_{sid}_{lang}.pdf")
        shutil.move(str(src), target)
        rec_out.update(status=status, local_path=str(target.relative_to(proj)), sha256=sha,
                       size=target.stat().st_size)
        return ""

    # Re-check files verified under the earlier (title-only) rules, and re-inspect pending
    # files (a pending file is promoted to verified only if it now passes every check).
    for sid, r in results.items():
        if r.get("status") == "pending" and sid in reg and (proj / r["local_path"]).exists():
            rec = meta.get(sid, {})
            title, authors = resolve_title(rec, reg[sid]), resolve_authors(rec, reg[sid])
            info = inspect_pdf(proj / r["local_path"], all_titles(rec, reg[sid]), raw_surname(authors))
            if classify(info)[0] == "ok":
                newp = pdf_dir / Path(r["local_path"]).name
                shutil.move(str(proj / r["local_path"]), newp)
                r.update(status="ok", local_path=str(newp.relative_to(proj)), reason="", checks_v2={
                    k: info.get(k) for k in ("pages", "text_chars", "title_match", "author_found",
                                             "references_found", "supplement_only", "lang")})
        if r.get("status") == "ok" and not r.get("checks_v2") and sid in reg:
            rec = meta.get(sid, {})
            title, authors = resolve_title(rec, reg[sid]), resolve_authors(rec, reg[sid])
            info = inspect_pdf(proj / r["local_path"], all_titles(rec, reg[sid]), raw_surname(authors))
            verdict, why = classify(info)
            r["checks_v2"] = {k: info.get(k) for k in ("pages", "text_chars", "title_match", "author_found",
                                                       "references_found", "supplement_only", "lang")}
            r["pages"], r["title_match"] = info.get("pages"), info.get("title_match")
            if verdict != "ok":
                pend_dir.mkdir(exist_ok=True)
                newp = pend_dir / Path(r["local_path"]).name
                shutil.move(str(proj / r["local_path"]), newp)
                r.update(status="pending", local_path=str(newp.relative_to(proj)), reason="recheck: " + why)
    save()

    count = {s: 0 for s in SLUGS}
    for sid, r in results.items():
        if r.get("status") == "ok" and sid in reg:
            for s in members(reg[sid]):
                count[s] += 1

    for slug in SLUGS:
        if a.only and slug != a.only:
            continue
        listed = sorted((e for e in reg.values() if slug in e.get("ranks", {})),
                        key=lambda e: e["ranks"][slug])
        for e in listed:
            if count[slug] >= a.target:
                break
            sid = e["id"]
            prev = results.get(sid, {})
            if prev.get("status") in ("ok", "pending") or (prev.get("status") == "failed" and not a.retry_failed):
                continue
            rec = meta.get(sid, {})
            title, authors = resolve_title(rec, e), resolve_authors(rec, e)
            out = {"title": title, "tries": [], "category_attempt": slug}
            if not title or not authors:
                # metadata not fetched yet (e.g. API rate limit): skip without recording, retry next run
                print(f"  skip {sid}: metadata missing, will retry on next run", file=sys.stderr)
                continue
            if e.get("title") and max(title_similarity(e["title"], t)
                                      for t in all_titles(rec, {})) < 0.6 if all_titles(rec, {}) else False:
                out.update(status="failed",
                           reason=f"identifier/title mismatch: seed '{e['title'][:80]}' vs source '{title[:80]}'")
                results[sid] = out
                save()
                continue
            fp = first_public(rec)[0]
            year = fp[:4] if fp else "0000"
            cands = candidates(e, rec)
            if not cands:
                out.update(status="failed", reason="no legal public PDF route found (link only)")
                results[sid] = out
                save()
                continue
            for label, url in cands:
                stage = Path(tempfile.mkdtemp(prefix=sid + "_", dir=staging_root))
                dest = stage / "download.bin"
                print(f"[{slug} {count[slug]}/{a.target}] {sid} GET {url}", file=sys.stderr)
                t = {"label": label, "url": url, **fetch(url, dest)}
                if t.get("http_status") == 200 and dest.exists():
                    info = inspect_pdf(dest, all_titles(rec, e), raw_surname(authors))
                    t.update({k: info.get(k) for k in ("magic_ok", "parse_ok", "pages", "text_chars",
                                                       "title_match", "author_found", "references_found",
                                                       "supplement_only", "lang", "error",
                                                       "first_text_head")})
                    verdict, why = classify(info)
                    t["verdict"], t["why"] = verdict, why
                    if verdict in ("ok", "pending"):
                        dup = place(sid, dest, info["lang"], out, verdict, year, authors, title)
                        if dup:
                            t["verdict"], t["why"] = "reject", dup
                        else:
                            out.update(pdf_url=url, version_label=label, pages=info.get("pages"),
                                       title_match=info.get("title_match"), checks_v2={
                                           k: info.get(k) for k in ("pages", "text_chars", "title_match",
                                                                    "author_found", "references_found",
                                                                    "supplement_only", "lang")})
                            if verdict == "pending":
                                out["reason"] = why
                out["tries"].append(t)
                shutil.rmtree(stage, ignore_errors=True)
                if out.get("status") == "ok":
                    break
                if out.get("status") == "pending":
                    # keep looking for a cleaner copy among the remaining routes
                    continue
            if out.get("status") not in ("ok", "pending"):
                out["status"] = "failed"
                out["reason"] = "; ".join(f"{t['label']}: {t.get('why') or t.get('error') or t.get('http_status')}"
                                          for t in out["tries"])
            results[sid] = out
            if out["status"] == "ok":
                for s in members(e):
                    count[s] += 1
            save()
        print(f"== {slug}: verified {count[slug]} / target {a.target}", file=sys.stderr)
    save()
    print(json.dumps(count, ensure_ascii=False))


if __name__ == "__main__":
    main()
