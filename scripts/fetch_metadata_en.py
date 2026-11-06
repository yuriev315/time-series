#!/usr/bin/env python3
"""Fetch bibliographic metadata for every registry entry.

Sources (public APIs, no login):
  - arXiv API (export.arxiv.org): title, authors, v1 date, latest version + date, comment,
    journal_ref, DOI, abstract (batched id_list requests)
  - Crossref REST API: authoritative DOI metadata incl. online/print/posted dates
  - OpenAlex API: publication_date, open-access locations (pdf_url, version, host) and any
    arXiv copy of a DOI-only paper (so the arXiv v1 date can decide the first public date)

Output: scripts/metadata_cache_en.json keyed by entry id (resume-safe: cached parts are skipped).
Rate limits are shared across processes via scripts/ratelimit_en.py; each request is tried at
most 3 times.

Usage: python3 -I scripts/fetch_metadata_en.py <project_dir>
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ratelimit_en  # noqa: E402

UA = "time_series_literature/1.0 (literature metadata collection; low rate)"
INTERVAL = {"export.arxiv.org": 3.5, "api.crossref.org": 1.0, "api.openalex.org": 0.5}
ATOM = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def get(url, accept="application/json"):
    host = urllib.parse.urlparse(url).netloc
    err = ""
    for attempt in range(3):
        ratelimit_en.wait(host, INTERVAL.get(host, 2.0))
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return 404, b""
            err = f"HTTP {e.code}"
            if e.code == 429:  # back off hard on rate limiting
                time.sleep(30)
        except Exception as e:  # network errors
            err = repr(e)
        print(f"  retry {attempt + 1}/3 {url}: {err}", file=sys.stderr)
        time.sleep(5 * (attempt + 1))
    return None, err.encode()


def arxiv_batch(ids):
    out = {}
    for i in range(0, len(ids), 100):
        chunk = ids[i:i + 100]
        url = ("https://export.arxiv.org/api/query?max_results=200&id_list=" + ",".join(chunk))
        status, body = get(url, accept="application/atom+xml")
        if status != 200:
            print("arXiv API failed", status, file=sys.stderr)
            continue
        for e in ET.fromstring(body).findall("a:entry", ATOM):
            abs_url = e.findtext("a:id", "", ATOM)
            if "/abs/" not in abs_url:
                continue
            vid = abs_url.rsplit("/abs/", 1)[-1]
            base = re.sub(r"v\d+$", "", vid)
            pc = e.find("arxiv:primary_category", ATOM)
            out[base] = {
                "abs_url": abs_url, "latest_version": vid,
                "title": " ".join(e.findtext("a:title", "", ATOM).split()),
                "authors": [a.findtext("a:name", "", ATOM) for a in e.findall("a:author", ATOM)],
                "published": e.findtext("a:published", "", ATOM),
                "updated": e.findtext("a:updated", "", ATOM),
                "abstract": " ".join(e.findtext("a:summary", "", ATOM).split()),
                "comment": e.findtext("arxiv:comment", "", ATOM),
                "journal_ref": e.findtext("arxiv:journal_ref", "", ATOM),
                "doi": e.findtext("arxiv:doi", "", ATOM),
                "primary_category": pc.get("term") if pc is not None else "",
            }
    return out


def date_str(parts):
    p = (parts or {}).get("date-parts", [[None]])[0]
    return "-".join(f"{x:02d}" if i else str(x) for i, x in enumerate(p) if x) if p and p[0] else ""


def crossref(doi):
    status, body = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    if status != 200:
        return {"error": f"status {status}"}
    m = json.loads(body)["message"]
    dates = {k: date_str(m.get(k)) for k in ("published-online", "published-print", "posted",
                                              "issued", "created")}
    year = None
    for k in ("published-print", "published-online", "issued"):
        if dates.get(k):
            year = int(dates[k][:4])
            break
    return {
        "title": " ".join((m.get("title") or [""])[0].split()),
        "authors": [" ".join(filter(None, [a.get("given"), a.get("family")])) or a.get("name", "")
                    for a in m.get("author", [])],
        "year": year, "dates": dates,
        "container": (m.get("container-title") or [""])[0],
        "volume": m.get("volume", ""), "issue": m.get("issue", ""), "page": m.get("page", ""),
        "type": m.get("type", ""), "url": m.get("URL", ""), "publisher": m.get("publisher", ""),
        "abstract": m.get("abstract", ""),
        # e.g. Copernicus discussion papers / posted preprints of the same work
        "preprints": [r.get("id", "") for r in (m.get("relation") or {}).get("has-preprint", [])
                      if r.get("id-type") == "doi"],
    }


def openalex(doi):
    status, body = get("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi))
    if status != 200:
        return {"error": f"status {status}"}
    w = json.loads(body)
    locs, arxiv_ids = [], []
    for loc in w.get("locations", []):
        src = loc.get("source") or {}
        locs.append({"pdf_url": loc.get("pdf_url"), "landing": loc.get("landing_page_url"),
                     "is_oa": loc.get("is_oa"), "version": loc.get("version"),
                     "license": loc.get("license"), "source": src.get("display_name"),
                     "source_type": src.get("type"), "host_org": src.get("host_organization_name")})
        for u in (loc.get("landing_page_url") or "", loc.get("pdf_url") or ""):
            m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", u)
            if m and m.group(1) not in arxiv_ids:
                arxiv_ids.append(m.group(1))
    inv = w.get("abstract_inverted_index") or {}
    abstract = " ".join(word for _, word in sorted((p, word) for word, ps in inv.items() for p in ps))
    return {"id": w.get("id"), "title": w.get("title"), "year": w.get("publication_year"),
            "publication_date": w.get("publication_date"),
            "authors": [a["author"]["display_name"] for a in w.get("authorships", [])],
            "oa_status": (w.get("open_access") or {}).get("oa_status"),
            "locations": locs, "arxiv_ids": arxiv_ids, "abstract": abstract}


def publisher_page(url):
    """Standard citation_* <meta> tags (Highwire/Google Scholar) of an official landing page."""
    status, body = get(url, accept="text/html")
    if status != 200:
        return {"error": f"status {status}", "url": url}
    html = body.decode("utf-8", "replace")
    tags = re.findall(r'<meta\s+name="(citation_[a-z_]+)"\s+content="([^"]*)"', html)
    pick = lambda k: [v for n, v in tags if n == k]
    date = (pick("citation_publication_date") or pick("citation_date") or [""])[0].replace("/", "-")
    return {"url": url, "title": (pick("citation_title") or [""])[0], "authors": pick("citation_author"),
            "publication_date": date, "pdf_url": (pick("citation_pdf_url") or [""])[0],
            "venue": (pick("citation_conference_title") or pick("citation_journal_title") or [""])[0]}


def main():
    proj = Path(sys.argv[1])
    reg = json.loads((proj / "scripts/registry_cn.json").read_text())
    cache_path = proj / "scripts/metadata_cache_en.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}

    def save():
        cache_path.write_text(json.dumps(cache, ensure_ascii=False, indent=1))

    # 1) DOI metadata (Crossref + OpenAlex); OpenAlex may reveal an arXiv copy
    for e in reg:
        rec = cache.setdefault(e["id"], {})
        doi = e.get("doi")
        if doi and "crossref" not in rec:
            print("crossref", e["id"], doi, file=sys.stderr)
            rec["crossref"] = crossref(doi)
        if doi and "openalex" not in rec:
            rec["openalex"] = openalex(doi)
            save()
    # 2) arXiv metadata, batched; includes arXiv copies found via OpenAlex
    want = {}
    for e in reg:
        rec = cache[e["id"]]
        ax = e.get("arxiv") or next(iter((rec.get("openalex") or {}).get("arxiv_ids") or []), "")
        if ax and not (rec.get("arxiv") or {}).get("title"):   # missing or earlier failure (e.g. 429)
            want[ax] = e["id"]
            if not e.get("arxiv"):
                rec["arxiv_via_openalex"] = ax
    if want:
        got = arxiv_batch(sorted(want))
        for ax, sid in want.items():
            cache[sid]["arxiv"] = got.get(ax, {"error": "not returned by arXiv API"})
        save()
    # 3) DOI announced by arXiv for arXiv-only entries -> Crossref/OpenAlex too
    for e in reg:
        rec = cache[e["id"]]
        doi = (rec.get("arxiv") or {}).get("doi") or ""
        if doi and not e.get("doi"):
            if "crossref" not in rec:
                rec["crossref"] = crossref(doi.lower())
            if "openalex" not in rec:
                rec["openalex"] = openalex(doi.lower())
            save()
    # 5) entries with neither DOI nor arXiv id: read the official landing page's citation tags
    for e in reg:
        rec = cache[e["id"]]
        if not e.get("doi") and not e.get("arxiv") and e.get("landing") and "publisher_page" not in rec:
            rec["publisher_page"] = publisher_page(e["landing"])
            save()
    # 4) dates of registered preprints (Crossref relation has-preprint), which may make a
    #    journal paper older than its own publication date suggests
    for e in reg:
        rec = cache[e["id"]]
        cr = rec.get("crossref") or {}
        if cr.get("title") and "preprints" not in cr:      # cached before this field existed
            doi = e.get("doi") or ((rec.get("arxiv") or {}).get("doi") or "").lower()
            if doi:
                rec["crossref"] = crossref(doi)
                cr = rec["crossref"]
                save()
        for pdoi in cr.get("preprints", []) or []:
            rec.setdefault("preprint_dates", {})
            if pdoi.lower() not in rec["preprint_dates"]:
                pr = crossref(pdoi.lower())
                rec["preprint_dates"][pdoi.lower()] = (pr.get("dates") or {}) if pr.get("title") else {}
                save()
    save()
    print(f"done: {len(cache)} records -> {cache_path}")


if __name__ == "__main__":
    main()
