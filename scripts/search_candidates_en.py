#!/usr/bin/env python3
"""Candidate discovery helper (arXiv API + OpenAlex), date-filtered by default
to the collection window 2023-10-29 .. 2026-10-29 (first public date).

Commands
  arxiv  "<arXiv search_query>" [-n 25] [--abs 400] [--all-dates]
         e.g. arxiv 'ti:"air quality" AND abs:forecast*'
  openalex "<free-text search>" [-n 25] [--abs 400] [--all-dates] [--oa] [--title]
         --title  : search titles only (title.search) instead of full text
         --oa     : only works with an open-access copy
  abs <arXiv id | DOI>   full metadata + abstract for one work

Rate limits are shared across processes (scripts/ratelimit_en.py):
arXiv >= 3.5 s between requests, OpenAlex >= 0.5 s.

Usage: python3 -I scripts/search_candidates_en.py <command> ...
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.dont_write_bytecode = True  # keep scripts/ free of __pycache__
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ratelimit_en  # noqa: E402

UA = "time_series_literature/1.0 (literature discovery; low rate)"
WIN_FROM, WIN_TO = "2023-10-29", "2026-10-29"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def get(url, host, interval):
    err = ""
    for attempt in range(3):
        ratelimit_en.wait(host, interval)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            err = repr(e)
            print(f"  retry {attempt + 1}/3: {err}", file=sys.stderr)
            ratelimit_en.wait(host + "_backoff", 0)
            import time
            time.sleep(10 * (attempt + 1))
    raise SystemExit(f"request failed: {url}: {err}")


def clip(s, n):
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[:n] + "..."


def arxiv_entries(body):
    out = []
    for e in ET.fromstring(body).findall("a:entry", NS):
        vid = e.findtext("a:id", "", NS).rsplit("/abs/", 1)[-1]
        if "api/errors" in vid:
            continue
        pc = e.find("arxiv:primary_category", NS)
        out.append({
            "id": vid, "v1_date": e.findtext("a:published", "", NS)[:10],
            "updated": e.findtext("a:updated", "", NS)[:10],
            "cat": pc.get("term") if pc is not None else "",
            "title": " ".join(e.findtext("a:title", "", NS).split()),
            "authors": [a.findtext("a:name", "", NS) for a in e.findall("a:author", NS)],
            "comment": e.findtext("arxiv:comment", "", NS) or "",
            "journal_ref": e.findtext("arxiv:journal_ref", "", NS) or "",
            "doi": e.findtext("arxiv:doi", "", NS) or "",
            "abstract": " ".join(e.findtext("a:summary", "", NS).split()),
        })
    return out


def cmd_arxiv(a):
    q = a.query
    if not a.all_dates:
        q = f"({q}) AND submittedDate:[{WIN_FROM.replace('-', '')}0000 TO {WIN_TO.replace('-', '')}2359]"
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": q, "max_results": a.n, "sortBy": "relevance"})
    for e in arxiv_entries(get(url, "export.arxiv.org", 3.5)):
        au = e["authors"][0] + (" et al." if len(e["authors"]) > 1 else "") if e["authors"] else ""
        print(f"[arXiv {e['id']}] v1={e['v1_date']} {e['cat']} | {e['title']} | {au}")
        extra = " ".join(x for x in (e["journal_ref"] and "JR: " + e["journal_ref"],
                                    e["doi"] and "DOI: " + e["doi"],
                                    e["comment"] and "C: " + clip(e["comment"], 120)) if x)
        if extra:
            print("    " + extra)
        if a.abs:
            print("    " + clip(e["abstract"], a.abs))


def oa_abstract(w):
    inv = w.get("abstract_inverted_index") or {}
    return " ".join(word for _, word in sorted((p, word) for word, ps in inv.items() for p in ps))


def oa_line(w, nabs):
    src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
    best = w.get("best_oa_location") or {}
    arx = [l.get("landing_page_url") for l in w.get("locations", [])
           if "arxiv.org" in (l.get("landing_page_url") or "")]
    au = [x["author"]["display_name"] for x in w.get("authorships", [])][:1]
    print(f"[{w['id'].rsplit('/', 1)[-1]}] {w.get('publication_date')} {w.get('type')} | {w.get('title')} | "
          f"{au[0] + ' et al.' if au else ''} | {src}")
    print(f"    DOI: {w.get('doi') or '-'} | OA: {w.get('open_access', {}).get('oa_status')} "
          f"pdf={best.get('pdf_url') or '-'} ({best.get('version') or '-'}, "
          f"{(best.get('source') or {}).get('display_name') or '-'}) | arXiv: {arx[0] if arx else '-'}")
    if nabs:
        print("    " + (clip(oa_abstract(w), nabs) or "(no abstract in OpenAlex)"))


def cmd_openalex(a):
    flt = ["type:article|preprint|review"]
    if not a.all_dates:
        flt.append(f"from_publication_date:{WIN_FROM},to_publication_date:{WIN_TO}")
    if a.oa:
        flt.append("is_oa:true")
    params = {"per_page": a.n, "filter": ",".join(flt)}
    if a.title:
        params["filter"] += f",title.search:{a.query}"
    else:
        params["search"] = a.query
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    for w in json.loads(get(url, "api.openalex.org", 0.5)).get("results", []):
        oa_line(w, a.abs)


def cmd_abs(a):
    ident = a.ident.strip()
    if ident.startswith("10.") or ident.startswith("https://doi.org/"):
        doi = ident.replace("https://doi.org/", "")
        w = json.loads(get("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi),
                           "api.openalex.org", 0.5))
        oa_line(w, 0)
        print("AUTHORS:", "; ".join(x["author"]["display_name"] for x in w.get("authorships", [])))
        for l in w.get("locations", []):
            print("  LOC:", l.get("is_oa"), l.get("version"), (l.get("source") or {}).get("display_name"),
                  l.get("pdf_url") or "-", l.get("landing_page_url") or "-")
        print("ABSTRACT:", oa_abstract(w) or "(none in OpenAlex)")
    else:
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"id_list": ident})
        for e in arxiv_entries(get(url, "export.arxiv.org", 3.5)):
            print(json.dumps({k: v for k, v in e.items() if k != "abstract"}, ensure_ascii=False))
            print("ABSTRACT:", e["abstract"])


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    x = sub.add_parser("arxiv")
    x.add_argument("query")
    o = sub.add_parser("openalex")
    o.add_argument("query")
    o.add_argument("--oa", action="store_true")
    o.add_argument("--title", action="store_true")
    for s in (x, o):
        s.add_argument("-n", type=int, default=25)
        s.add_argument("--abs", type=int, default=0)
        s.add_argument("--all-dates", action="store_true")
    b = sub.add_parser("abs")
    b.add_argument("ident")
    a = p.parse_args()
    {"arxiv": cmd_arxiv, "openalex": cmd_openalex, "abs": cmd_abs}[a.cmd](a)


if __name__ == "__main__":
    main()
