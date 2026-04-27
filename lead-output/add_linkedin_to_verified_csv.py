#!/usr/bin/env python3
import csv
import json
from pathlib import Path


INPUT = Path("lead-output/education-partnership-leads-50-verified-decision-makers.csv")
RAW = Path("lead-output/education-partnership-leads-raw.json")
OUTPUT = Path("lead-output/education-partnership-leads-50-verified-with-linkedin.csv")


def domain_key(url):
    if not url:
        return ""
    url = url.lower().split("?")[0].rstrip("/")
    for prefix in ("https://www.", "http://www.", "https://", "http://"):
        if url.startswith(prefix):
            url = url[len(prefix):]
            break
    return url


def as_list(value):
    if not value:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v]
    return [str(value)]


raw_items = json.loads(RAW.read_text())
linkedin_by_site = {}
linkedin_by_name = {}

for item in raw_items:
    links = as_list(item.get("linkedIns") or item.get("linkedins") or item.get("linkedin"))
    if not links:
        continue
    website = domain_key(item.get("website", ""))
    name = (item.get("title") or item.get("name") or "").strip().lower()
    if website:
        linkedin_by_site[website] = links
    if name:
        linkedin_by_name[name] = links


with INPUT.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
    fields = list(rows[0].keys())

new_fields = [
    "linkedin_company_url",
    "linkedin_person_url",
    "linkedin_source",
]

for row in rows:
    links = linkedin_by_site.get(domain_key(row["website"])) or linkedin_by_name.get(row["business_name"].strip().lower()) or []
    company_links = [link for link in links if "/company/" in link]
    person_links = [link for link in links if "/in/" in link]
    row["linkedin_company_url"] = "; ".join(dict.fromkeys(company_links))
    row["linkedin_person_url"] = "; ".join(dict.fromkeys(person_links))
    row["linkedin_source"] = "Apify contact scraping" if links else ""

with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fields + new_fields)
    writer.writeheader()
    writer.writerows(rows)

print(f"wrote={OUTPUT}")
print(f"rows_with_linkedin={sum(1 for row in rows if row['linkedin_company_url'] or row['linkedin_person_url'])}")
