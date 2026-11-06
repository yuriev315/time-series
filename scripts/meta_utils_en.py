"""Shared helpers: resolve title, authors and first-public date of a registry entry
from its cached metadata (arXiv / Crossref / OpenAlex), and text normalisation."""
import re
import unicodedata

WINDOW_START, WINDOW_END = "2023-10-29", "2026-10-29"
STOP = {"a", "an", "the", "of", "for", "and", "in", "on", "with", "to", "via", "by", "is", "are",
        "from", "at", "as", "its", "do", "how", "much", "can", "using", "based"}


DASHES = str.maketrans({c: "-" for c in "\u2010\u2011\u2012\u2013\u2014\u2015\u2212"})


def fold(s):
    s = re.sub(r"[{}\\]", "", (s or "").translate(DASHES))
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", fold(strip_tags(s)).lower())


def tokens(s):
    return [t for t in re.findall(r"[a-z0-9]+", fold(strip_tags(s)).lower()) if t not in STOP and len(t) > 1]


def title_similarity(a, b):
    """Jaccard similarity of title tokens; a title fully contained in the other (e.g. an
    official short title "PM2.5-GNN") counts as a match."""
    na, nb = norm(a), norm(b)
    if na and nb and (na in nb or nb in na) and min(len(na), len(nb)) >= 8:
        return 1.0
    ta, tb = set(tokens(a)), set(tokens(b))
    return len(ta & tb) / max(1, len(ta | tb))


def arxiv_ok(rec):
    ax = rec.get("arxiv") or {}
    return ax if ax.get("title") else {}


def resolve_title(rec, entry):
    cr, oa = rec.get("crossref") or {}, rec.get("openalex") or {}
    ax = arxiv_ok(rec)
    if entry.get("doi") and cr.get("title"):
        return strip_tags(cr["title"])
    return strip_tags(ax.get("title") or cr.get("title") or oa.get("title") or entry.get("title") or "")


def all_titles(rec, entry):
    """Every known title of the work (arXiv and journal versions may be titled differently)."""
    cr, oa = rec.get("crossref") or {}, rec.get("openalex") or {}
    ts = [arxiv_ok(rec).get("title"), cr.get("title"), oa.get("title"),
          (rec.get("publisher_page") or {}).get("title"), entry.get("title")]
    out = []
    for t in ts:
        t = strip_tags(t or "").strip()
        if t and norm(t) not in {norm(x) for x in out}:
            out.append(t)
    return out


def resolve_authors(rec, entry):
    cr, oa = rec.get("crossref") or {}, rec.get("openalex") or {}
    ax = arxiv_ok(rec)
    if entry.get("doi") and cr.get("authors"):
        return cr["authors"]
    # last resort: first author recorded in the seed from the publisher page (flagged in the catalogue)
    return ax.get("authors") or cr.get("authors") or oa.get("authors") or \
        (rec.get("publisher_page") or {}).get("authors") or \
        ([entry["first_author"]] if entry.get("first_author") else [])


def surname(name):
    parts = fold(name).split()
    return re.sub(r"[^A-Za-z]", "", parts[-1]) if parts else ""


def first_public(rec):
    """Return (date, precision_label, source_label). Earliest of arXiv v1 and Crossref
    online/print/posted/created dates; OpenAlex publication_date only as a fallback."""
    cands = []
    ax = arxiv_ok(rec)
    if ax.get("published"):
        cands.append((ax["published"][:10], "arXiv v1 提交日"))
    cr = rec.get("crossref") or {}
    for k in ("published-online", "published-print", "posted", "created"):
        d = (cr.get("dates") or {}).get(k)
        if d:
            cands.append((d, f"Crossref {k}"))
    for pdoi, pd in (rec.get("preprint_dates") or {}).items():
        d = pd.get("posted") or pd.get("published-online") or pd.get("created") or pd.get("issued")
        if d:
            cands.append((d, f"预印本/讨论稿 {pdoi}（Crossref has-preprint）"))
    if not cands and cr.get("year"):
        cands.append((str(cr["year"]), "Crossref 出版年"))
    pp = rec.get("publisher_page") or {}
    if pp.get("publication_date"):
        cands.append((pp["publication_date"], f"出版方页面 citation_publication_date（{pp.get('url')}）"))
    oa_date = (rec.get("openalex") or {}).get("publication_date")
    # OpenAlex only as a fallback: it pads month/year-only dates to the 1st (e.g. 2026-10-01)
    if oa_date and not cands:
        cands.append((oa_date, "OpenAlex publication_date（可能为月/年精度补齐）"))
    if not cands:
        return "", "无", "无"
    # Prefer the earliest day-precision date; a coarser date (YYYY or YYYY-MM) wins only if its
    # whole period ends before that day (otherwise "2026-10" would beat "2026-10-08").
    day = [c for c in cands if len(c[0]) == 10]
    coarse = [c for c in cands if len(c[0]) != 10]
    best = min(day) if day else None
    for c in coarse:
        end = c[0] + ("-12-31" if len(c[0]) == 4 else "-31")
        if best is None or end < best[0]:
            best = c if best is None or (c[0] + "-01-01")[:10] < (best[0] + "-01-01")[:10] else best
    date, src = best
    precision = {10: "日", 7: "月", 4: "年"}.get(len(date), "未知")
    return date, precision, src


def window_status(date, precision):
    if not date:
        return "待核实（无日期）"
    if precision == "日":
        return "近三年" if WINDOW_START <= date <= WINDOW_END else "三年前"
    lo = (date + "-01-01")[:10]
    hi = (date + "-12-31")[:10] if precision == "年" else date + "-31"
    if lo >= WINDOW_START and hi <= WINDOW_END:
        return "近三年"
    if hi < WINDOW_START:
        return "三年前"
    return "待核实（日期精度不足，跨窗口边界）"
