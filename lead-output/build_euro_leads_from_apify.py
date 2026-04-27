#!/usr/bin/env python3
import csv
import json
import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


DATASETS = {
    "italy_apify_aborted": "QUOBqLXrhawiRJr60",
    "spain_apify_aborted": "S9JoKV4UNaxii6R5r",
}

OUT_DIR = Path("lead-output")
RAW_JSON = OUT_DIR / "euro-spain-italy-raw-apify.json"
AUDIT_JSON = OUT_DIR / "euro-spain-italy-quality-audit.json"
AUDIT_CSV = OUT_DIR / "euro-spain-italy-quality-audit.csv"
WORK_JSON = OUT_DIR / "euro-spain-italy-working-keep-review.json"
WORK_CSV = OUT_DIR / "euro-spain-italy-working-keep-review.csv"


KEEP_NAMES = {
    "Trinity ViaggiStudio": ("A", "Italy outbound study travel operator", "Viaggi studio / study travel operator. Strong convertible Italy source-market lead for UK or China programs."),
    "Master Studio": ("B", "Italy outbound study/travel agency", "Travel/study brand likely relevant to Italian student mobility. Needs source confirmation, but fit is plausible."),
    "VIVA International": ("A", "Italy summer camp / study travel operator", "Summer-camp/study-travel positioning. Strong youth education source-market fit."),
    "Study Tours": ("A", "Italy study tour operator", "Name and category directly match study tours. Strong fit for UK/China study tour partnerships."),
    "ESL – Soggiorni linguistici": ("A", "Italy language travel agency", "Soggiorni linguistici means language stays. Strong outbound language-study agency fit."),
    "inter - studioviaggi": ("A", "Italy study travel operator", "Studio viaggi / study travel operator. Strong source-market lead."),
    "Astudy": ("A", "Italy education travel consultant", "Travel agency plus educational consultant. Strong outbound student travel fit."),
    "Language Educational Travels": ("A", "Italy language educational travel provider", "Direct language/educational travel fit."),
    "MB Scambi Culturali srl": ("A", "Italy cultural exchange / study travel operator", "Scambi culturali means cultural exchanges. Strong source-market lead."),
    "Active Global Inglés House": ("A", "Spain outbound language travel agency", "Cursos en el extranjero domain and English-study travel angle. Strong Spain source-market lead."),
    "TravelEnglish": ("A", "Spain language travel agency", "English travel/study brand. Strong source-market lead."),
    "Top School": ("A", "Spain study abroad / language camp agency", "Explicit cursos extranjero, English camp, exchange students, travel agency categories. Strong fit."),
    "International EXPERIENCE. Expertos en educación internacional": ("A", "Spain international education / exchange agency", "Foreign exchange and international education. Strong source-market fit."),
    "Se Viaja Education Tour.23 SL": ("A", "Spain educational travel agency", "Education Tour name and travel agency category. Strong fit."),
}

REVIEW_NAMES = {
    "Go Study Australia": ("C", "Italy outbound study agency", "Outbound study agency but destination is Australia, not UK/China. Could cross-sell if they handle broader destinations."),
    "CHINA LONG VISA SERVICE": ("C", "Italy China visa/travel service", "China-related travel/visa lead. Could help China inbound but may not target youth education."),
    "Agenzia Visti per la Cina": ("C", "Italy China visa service", "China visa agency; relevant to China travel logistics but not clearly youth study-tour sales."),
    "China Long Travel Service Srl": ("C", "Italy China travel/visa agency", "China travel/visa agency. Review for education/youth capability."),
    "Youth Education Support": ("C", "Italy youth education organization", "Youth education name, but unclear commercial source-market role."),
    "EDUITALIA: International Education": ("C", "Italy international education network", "International education network, but may be Italy-inbound rather than outbound to UK/China."),
    "SAIIE - Spanish American Institute of International Education": ("C", "Spain international education provider", "International education, but likely Spain/US inbound-academic rather than outbound youth camps."),
    "China Internacional Travel": ("C", "Spain China travel agency", "China-related travel agency. Review for China study-tour/youth education relevance."),
    "三和旅行社 Viajes Sanhe": ("C", "Spain Chinese travel/youth org adjacent", "Chinese travel agency with youth organization category. Potential China connection, but unclear education fit."),
    "Learnlife Barcelona - Urban Hub": ("C", "Spain international school", "International school. Possible partner/referrer, but not a source-market agency."),
    "AnDa Sports Camps": ("C", "Spain sports camp operator", "Children's camp/sport tour agency. Could be youth partnership, but not UK/China outbound study-tour focus."),
    "Au Pair in Spain. Culture and Friends": ("C", "Spain cultural exchange / au pair agency", "Cultural exchange/after-school angle. Review for youth/family mobility relevance."),
}


REMOVE_KEYWORDS = [
    "supermarket",
    "discount store",
    "department store",
    "diving center",
    "scuba",
    "horseback",
    "surf school",
    "tourist attraction",
    "sightseeing",
    "cooking",
    "translation",
    "preschool",
    "local tour",
]


def fetch_dataset(token, dataset_id):
    url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
    response = requests.get(url, params={"token": token, "format": "json"}, timeout=90)
    response.raise_for_status()
    return response.json()


def clean_url(url):
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.scheme and parsed.netloc:
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    return url


def clean_email(value):
    if isinstance(value, list):
        value = "; ".join(str(v) for v in value if v)
    parts = []
    for part in (value or "").replace("%20", "").split(";"):
        part = part.strip()
        if part and part.lower() not in [existing.lower() for existing in parts]:
            parts.append(part)
    return "; ".join(parts)


def links(value):
    if isinstance(value, list):
        return "; ".join(str(v) for v in value if v)
    return value or ""


def score(row, recommendation):
    base = {"Keep": 12, "Review": 7, "Remove": 2}[recommendation]
    if row["email"]:
        base += 2
    if row["phone"]:
        base += 1
    if row["linkedin_company_url"]:
        base += 1
    return base


def audit(item):
    name = item.get("title") or item.get("name") or ""
    if name in KEEP_NAMES:
        grade, role, reason = KEEP_NAMES[name]
        return "Keep", grade, role, reason
    if name in REVIEW_NAMES:
        grade, role, reason = REVIEW_NAMES[name]
        return "Review", grade, role, reason

    text = " ".join(
        str(item.get(k, ""))
        for k in ("title", "categoryName", "categories", "website")
    ).lower()
    if any(word in text for word in REMOVE_KEYWORDS):
        return "Remove", "D", "Non-convertible local/retail/tourism lead", "Does not appear to sell outbound youth study tours/camps to UK or China."
    if "tour agency" in text or "tour operator" in text or "travel agency" in text:
        return "Remove", "D", "Generic tourism/travel lead", "Generic tourism or local tour operator, not clearly outbound youth education."
    return "Review", "C", "Unclear education lead", "Needs manual source check for UK/China outbound youth-study-tour relevance."


def normalize(item, source):
    recommendation, grade, role, reason = audit(item)
    emails = item.get("emails") or item.get("email") or ""
    linkedin = links(item.get("linkedIns") or item.get("linkedins") or item.get("linkedin") or "")
    row = {
        "business_name": item.get("title") or item.get("name") or "",
        "website": clean_url(item.get("website") or ""),
        "city": item.get("city") or "",
        "country": item.get("countryCode") or "",
        "email": clean_email(emails),
        "phone": item.get("phone") or "",
        "instagram": links(item.get("instagrams") or item.get("instagram") or ""),
        "linkedin_company_url": "; ".join(link for link in linkedin.split("; ") if "/company/" in link),
        "linkedin_person_url": "; ".join(link for link in linkedin.split("; ") if "/in/" in link),
        "linkedin_source": "Apify contact scraping" if linkedin else "",
        "decision_maker_name": "",
        "decision_maker_title": "",
        "decision_maker_email": "",
        "decision_maker_phone": "",
        "decision_source_url": "",
        "decision_source_type": "",
        "decision_confidence": "",
        "score": "",
        "notes": f"category: {links(item.get('categories') or item.get('categoryName') or '')} | rating: {item.get('totalScore') or ''} | reviews: {item.get('reviewsCount') or ''} | source: {source}",
        "google_maps_url": item.get("url") or "",
        "quality_recommendation": recommendation,
        "quality_grade": grade,
        "market_role": role,
        "quality_reason": reason,
    }
    row["score"] = score(row, recommendation)
    return row


def write_csv(path, rows):
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    load_dotenv()
    token = os.environ["APIFY_TOKEN"]
    raw = []
    for source, dataset_id in DATASETS.items():
        for item in fetch_dataset(token, dataset_id):
            item["_source"] = source
            raw.append(item)

    RAW_JSON.write_text(json.dumps(raw, indent=2, ensure_ascii=False), encoding="utf-8")

    seen = set()
    rows = []
    for item in raw:
        row = normalize(item, item["_source"])
        key = (row["website"] or row["business_name"]).lower()
        if not key or key in seen:
            continue
        seen.add(key)
        rows.append(row)

    order = {"Keep": 0, "Review": 1, "Remove": 2}
    rows.sort(key=lambda r: (order[r["quality_recommendation"]], -int(r["score"]), r["business_name"]))
    working = [row for row in rows if row["quality_recommendation"] in {"Keep", "Review"}]

    AUDIT_JSON.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    WORK_JSON.write_text(json.dumps(working, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(AUDIT_CSV, rows)
    write_csv(WORK_CSV, working)

    counts = {}
    for row in rows:
        counts[row["quality_recommendation"]] = counts.get(row["quality_recommendation"], 0) + 1
    print(f"raw={len(raw)} deduped={len(rows)} working={len(working)} counts={counts}")
    print(AUDIT_JSON)
    print(WORK_JSON)


if __name__ == "__main__":
    main()
