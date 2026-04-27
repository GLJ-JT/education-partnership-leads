#!/usr/bin/env python3
import csv
import json
from pathlib import Path
from urllib.parse import urlparse

from build_worldwide_search_leads_from_apify import dedupe_key, domain, merge_contact


AUDIT = Path("lead-output/worldwide-search-source-market-quality-audit.json")
CONTACTS = Path("lead-output/worldwide-search-source-market-contact-enrichment-raw.json")
WORK_JSON = Path("lead-output/worldwide-search-source-market-working-100.json")
WORK_CSV = Path("lead-output/worldwide-search-source-market-working-100.csv")
COMBINED_JSON = Path("lead-output/combined-worldwide-education-partnership-leads-map-data.json")
BASE_JSON = Path("lead-output/combined-uk-turkey-spain-italy-leads-map-data.json")

BAD_DOMAINS = [
    "tiktok.com", "facebook.com", "instagram.com", "linkedin.com", "youtube.com", "note.com",
    "alc.co.jp", "kuraveil.jp", "languageinternational.", "teenlife.com", "glolea.com", "tanoniha.com",
    "wikipedia.org", "tripadvisor.", "booking.com", "reddit.com", "pinterest.",
]
BAD_TITLE_TERMS = [
    "おすすめ", "最新版", "quanto custa", "preços", "features", "費用", "viral", "ranking",
    "best ", "top ", "review", "reviews", "blog", "article", "news", "컬럼", "비용", "추천", "tips",
]
BAD_PATH_TERMS = ["/blog", "/article", "/news", "/video", "/watch", "/tag/", "/magazine/"]


def is_operator_like(row):
    text = f"{row.get('business_name','')} {row.get('notes','')} {row.get('website','')}".lower()
    parsed = urlparse(row.get("website") or "")
    dom = parsed.netloc.lower()
    path = parsed.path.lower()
    if any(bad in dom for bad in BAD_DOMAINS):
        return False
    if any(bad in path for bad in BAD_PATH_TERMS):
        return False
    if any(bad in text for bad in BAD_TITLE_TERMS):
        return False
    return row.get("quality_recommendation") == "Keep"


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)


def main():
    audited = json.loads(AUDIT.read_text(encoding="utf-8"))
    contacts = json.loads(CONTACTS.read_text(encoding="utf-8")) if CONTACTS.exists() else []
    contact_by_domain = {}
    for contact in contacts:
        key = domain(contact.get("originalStartUrl") or contact.get("domain") or "")
        if key:
            contact_by_domain[key] = contact

    picked = []
    seen = set()
    for row in audited:
        if not is_operator_like(row):
            continue
        key = dedupe_key(row)
        if key in seen:
            continue
        seen.add(key)
        picked.append(merge_contact(row, contact_by_domain.get(domain(row["website"]), {})))
        if len(picked) == 100:
            break

    picked.sort(key=lambda r: (-int(r["score"]), r["country"], r["business_name"]))
    WORK_JSON.write_text(json.dumps(picked, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(WORK_CSV, picked)

    base = json.loads(BASE_JSON.read_text(encoding="utf-8"))
    combined = []
    combined_seen = set()
    for row in base + picked:
        key = dedupe_key(row)
        if key in combined_seen:
            continue
        combined_seen.add(key)
        combined.append(row)
    COMBINED_JSON.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")

    countries = {}
    for row in picked:
        countries[row["country"]] = countries.get(row["country"], 0) + 1
    print(f"picked={len(picked)} countries={sorted(countries.items())}")


if __name__ == "__main__":
    main()
