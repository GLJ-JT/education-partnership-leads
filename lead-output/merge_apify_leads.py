#!/usr/bin/env python3
import csv
import json
import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


DATASETS = {
    "uk_google_maps": "hkE63WdOi09fLgVhj",
    "turkey_google_maps": "0n98Abqa79DAXivOQ",
}

OUTPUT_DIR = Path("lead-output")
FINAL_CSV = OUTPUT_DIR / "education-partnership-leads-50.csv"
RAW_JSON = OUTPUT_DIR / "education-partnership-leads-raw.json"


def pick_first(value):
    if isinstance(value, list):
        return value[0] if value else ""
    return value or ""


def join_values(value):
    if isinstance(value, list):
        return "; ".join(str(v) for v in value if v)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return value or ""


def domain_from_url(url):
    if not url:
        return ""
    parsed = urlparse(url if "://" in url else f"https://{url}")
    return parsed.netloc.replace("www.", "")


def lead_score(item):
    text = " ".join(
        str(item.get(k, ""))
        for k in ("title", "categoryName", "categories", "website", "city")
    ).lower()
    score = 0
    for needle in (
        "study",
        "school travel",
        "educational travel",
        "summer school",
        "language",
        "international",
        "ib",
        "boarding",
        "camp",
        "tour",
    ):
        if needle in text:
            score += 2
    if item.get("website"):
        score += 2
    if item.get("phone"):
        score += 1
    if item.get("emails") or item.get("email"):
        score += 3
    if item.get("instagrams"):
        score += 1
    if item.get("totalScore"):
        score += 1
    return score


def fetch_dataset(token, dataset_id):
    url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
    response = requests.get(url, params={"token": token, "format": "json"}, timeout=60)
    response.raise_for_status()
    return response.json()


def normalize(item, source):
    emails = item.get("emails") or item.get("email") or ""
    instagrams = item.get("instagrams") or item.get("instagram") or ""
    categories = item.get("categories") or item.get("categoryName") or ""
    city = item.get("city") or item.get("location", {}).get("city") or ""
    country = item.get("countryCode") or item.get("country") or ""
    rating = item.get("totalScore") or item.get("rating") or ""
    reviews = item.get("reviewsCount") or ""
    notes_parts = [
        f"category: {join_values(categories)}" if categories else "",
        f"rating: {rating}" if rating else "",
        f"reviews: {reviews}" if reviews else "",
        f"source: {source}",
    ]
    return {
        "business_name": item.get("title") or item.get("name") or "",
        "website": item.get("website") or "",
        "city": city,
        "country": country,
        "email": join_values(emails),
        "phone": item.get("phone") or "",
        "instagram": join_values(instagrams),
        "owner_director_manager_name": "",
        "director_or_manager_email": "",
        "google_maps_url": item.get("url") or "",
        "score": lead_score(item),
        "notes": " | ".join(part for part in notes_parts if part),
    }


def main():
    load_dotenv()
    token = os.environ["APIFY_TOKEN"]
    OUTPUT_DIR.mkdir(exist_ok=True)

    raw_items = []
    for source, dataset_id in DATASETS.items():
        for item in fetch_dataset(token, dataset_id):
            item["_source"] = source
            raw_items.append(item)

    RAW_JSON.write_text(json.dumps(raw_items, indent=2, ensure_ascii=False))

    seen = set()
    rows = []
    for item in raw_items:
        row = normalize(item, item["_source"])
        key = domain_from_url(row["website"]) or row["business_name"].lower()
        if not key or key in seen:
            continue
        seen.add(key)
        rows.append(row)

    rows.sort(key=lambda row: int(row["score"]), reverse=True)
    rows = rows[:50]

    fieldnames = [
        "business_name",
        "website",
        "city",
        "country",
        "email",
        "phone",
        "instagram",
        "owner_director_manager_name",
        "director_or_manager_email",
        "google_maps_url",
        "score",
        "notes",
    ]
    with FINAL_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"raw_items={len(raw_items)}")
    print(f"deduped_rows={len(rows)}")
    print(f"csv={FINAL_CSV}")
    print(f"json={RAW_JSON}")


if __name__ == "__main__":
    main()
