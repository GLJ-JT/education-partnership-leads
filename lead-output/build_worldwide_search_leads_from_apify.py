#!/usr/bin/env python3
import csv
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


OUT_DIR = Path("lead-output")
RAW_SEARCH_JSON = OUT_DIR / "worldwide-search-source-market-raw-apify.json"
SEARCH_AUDIT_JSON = OUT_DIR / "worldwide-search-source-market-quality-audit.json"
SEARCH_TOP_JSON = OUT_DIR / "worldwide-search-source-market-top-100-pre-enrichment.json"
ENRICH_RAW_JSON = OUT_DIR / "worldwide-search-source-market-contact-enrichment-raw.json"
WORK_JSON = OUT_DIR / "worldwide-search-source-market-working-100.json"
WORK_CSV = OUT_DIR / "worldwide-search-source-market-working-100.csv"
COMBINED_JSON = OUT_DIR / "combined-worldwide-education-partnership-leads-map-data.json"

SEARCH_ACTOR = "apify~google-search-scraper"
CONTACT_ACTOR = "vdrmota~contact-info-scraper"

COUNTRIES = [
    ("DE", "de", "de", 51.1657, 10.4515, [
        '"Sprachreisen" Schüler England Anbieter',
        '"Schüleraustausch" England Agentur',
        '"Jugendreisen" Sprachreise England',
    ]),
    ("FR", "fr", "fr", 46.2276, 2.2137, [
        '"séjours linguistiques" angleterre jeunes organisme',
        '"voyages scolaires" angleterre agence',
        '"colonie" anglais étranger adolescents',
    ]),
    ("NL", "nl", "nl", 52.1326, 5.2913, [
        '"taalreizen" scholieren Engeland',
        '"schoolreis" Engeland educatief',
        '"studeren in het buitenland" Engeland bureau',
    ]),
    ("PL", "pl", "pl", 51.9194, 19.1451, [
        '"obozy językowe" Anglia młodzież',
        '"wyjazdy edukacyjne" Anglia',
        '"biuro edukacyjne" za granicą młodzież',
    ]),
    ("CN", "cn", "zh", 35.8617, 104.1954, [
        '"英国游学" 机构',
        '"国际研学旅行" 机构',
        '"英国夏令营" 青少年',
    ]),
    ("JP", "jp", "ja", 36.2048, 138.2529, [
        '"イギリス留学" エージェント 中学生',
        '"短期留学" イギリス 高校生',
        '"海外サマーキャンプ" 英語',
    ]),
    ("KR", "kr", "ko", 35.9078, 127.7669, [
        '"영국 어학연수" 유학원 학생',
        '"청소년 해외 영어 캠프"',
        '"해외 교육 여행" 학생',
    ]),
    ("IN", "in", "en", 20.5937, 78.9629, [
        '"UK study abroad consultant" students India',
        '"school educational tour" operator India',
        '"summer camp abroad" students India',
    ]),
    ("PK", "pk", "en", 30.3753, 69.3451, [
        '"UK study abroad consultant" Pakistan students',
        '"educational travel agency" Pakistan students',
        '"summer camp abroad" Pakistan students',
    ]),
    ("AE", "ae", "en", 23.4241, 53.8478, [
        '"UK study abroad consultant" UAE students',
        '"school trip operator" UAE UK',
        '"educational travel agency" Dubai students',
    ]),
    ("SA", "sa", "ar", 23.8859, 45.0792, [
        '"دراسة في بريطانيا" مكتب طلاب',
        '"معسكر صيفي انجليزي" طلاب',
        '"ابتعاث طلاب" بريطانيا مكتب',
    ]),
    ("MX", "mx", "es", 23.6345, -102.5528, [
        '"cursos de inglés en el extranjero" jóvenes México',
        '"campamentos de verano" Reino Unido jóvenes',
        '"viajes educativos" Reino Unido estudiantes',
    ]),
    ("CO", "co", "es", 4.5709, -74.2973, [
        '"inglés en el exterior" jóvenes Colombia agencia',
        '"campamentos de verano" Reino Unido Colombia',
        '"viajes educativos" estudiantes exterior Colombia',
    ]),
    ("BR", "br", "pt-BR", -14.235, -51.9253, [
        '"intercâmbio adolescentes" Reino Unido',
        '"cursos de inglês no exterior" jovens agência',
        '"viagem educacional" estudantes exterior',
    ]),
    ("TH", "th", "th", 15.87, 100.9925, [
        '"study abroad UK" Thailand students agency',
        '"ค่ายภาษาอังกฤษต่างประเทศ" นักเรียน',
        '"educational travel" Thailand students UK',
    ]),
    ("VN", "vn", "vi", 14.0583, 108.2772, [
        '"du học hè Anh" học sinh',
        '"trại hè tiếng Anh nước ngoài"',
        '"tư vấn du học Anh" học sinh',
    ]),
    ("ID", "id", "id", -0.7893, 113.9213, [
        '"konsultan studi Inggris" siswa',
        '"summer camp bahasa Inggris" luar negeri',
        '"study tour pelajar" luar negeri',
    ]),
    ("MY", "my", "en", 4.2105, 101.9758, [
        '"UK study abroad consultant" Malaysia students',
        '"English summer camp overseas" Malaysia',
        '"student educational tour" Malaysia',
    ]),
    ("SG", "sg", "en", 1.3521, 103.8198, [
        '"student educational tour" Singapore UK',
        '"UK study tour" Singapore students',
        '"school trip operator" Singapore overseas',
    ]),
    ("AU", "au", "en", -25.2744, 133.7751, [
        '"school educational tour operator" UK Australia',
        '"student travel education provider" Australia',
        '"language travel agency" students Australia',
    ]),
]

KEEP_TERMS = [
    "study abroad", "study tour", "school trip", "educational travel", "student travel", "language travel",
    "summer camp", "exchange student", "foreign exchange", "overseas education", "international education",
    "sprachreisen", "schüleraustausch", "séjours linguistiques", "séjour linguistique", "voyages scolaires",
    "cursos de inglés", "campamentos de verano", "intercâmbio", "du học", "trại hè", "游学", "研学",
    "夏令营", "留学", "어학연수", "유학원", "短期留学", "海外サマーキャンプ", "دراسة في بريطانيا",
    "معسكر صيفي", "ค่ายภาษาอังกฤษ", "study overseas",
]
REVIEW_TERMS = ["education", "school", "learning", "language", "travel agency", "tour operator", "visa", "boarding"]
BAD_TERMS = [
    "wikipedia", "facebook.com", "instagram.com", "linkedin.com", "youtube.com", "tripadvisor", "booking.com",
    "indeed", "glassdoor", "reddit", "pinterest", "government", "embassy", "consulate", "pdf", "news",
    "blog", "article", "ranking", "review", "forum",
]


def apify(method, path, token, **kwargs):
    params = kwargs.pop("params", {})
    params["token"] = token
    response = requests.request(method, f"https://api.apify.com/v2/{path}", params=params, timeout=120, **kwargs)
    if response.status_code >= 400:
        body = response.text[:800]
        raise RuntimeError(f"Apify API {method} {path} failed with HTTP {response.status_code}: {body}")
    return response.json()


def run_actor(token, actor, payload, timeout=600):
    data = apify("POST", f"acts/{actor}/runs", token, headers={"Content-Type": "application/json"}, json=payload)["data"]
    run_id, dataset_id = data["id"], data["defaultDatasetId"]
    start = time.time()
    last = None
    while True:
        run = apify("GET", f"actor-runs/{run_id}", token)["data"]
        status = run["status"]
        if status != last:
            print(run_id, status)
            last = status
        if status in {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}:
            if status != "SUCCEEDED":
                raise RuntimeError(f"{actor} {run_id} ended {status}: https://console.apify.com/actors/runs/{run_id}")
            return dataset_id
        if time.time() - start > timeout:
            raise TimeoutError(f"{actor} {run_id} exceeded {timeout}s")
        time.sleep(8)


def fetch_dataset(token, dataset_id):
    response = requests.get(
        f"https://api.apify.com/v2/datasets/{dataset_id}/items",
        params={"token": token, "format": "json", "clean": "true"},
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def domain(url):
    try:
        return urlparse(url).netloc.lower().removeprefix("www.")
    except Exception:
        return ""


def clean_url(url):
    parsed = urlparse(url or "")
    if parsed.scheme and parsed.netloc:
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")
    return (url or "").strip().rstrip("/")


def result_items(raw, meta):
    out = []
    for item in raw:
        candidates = item.get("organicResults") if isinstance(item.get("organicResults"), list) else [item]
        for result in candidates:
            url = result.get("url") or result.get("link") or result.get("displayedUrl") or ""
            if not url:
                continue
            row = {
                "title": result.get("title") or item.get("title") or "",
                "url": clean_url(url),
                "description": result.get("description") or result.get("snippet") or item.get("description") or "",
                "rank": result.get("position") or result.get("rank") or item.get("rank") or "",
                **meta,
            }
            out.append(row)
    return out


def audit(row):
    text = f"{row['title']} {row['description']} {row['url']}".lower()
    dom = domain(row["url"])
    if any(term in text or term in dom for term in BAD_TERMS):
        return "Remove", "D", "Directory/social/content result", "Search result is a directory, social network, article, or non-lead page."
    hits = [term for term in KEEP_TERMS if term in text]
    review_hits = [term for term in REVIEW_TERMS if term in text]
    if hits:
        grade = "A" if len(hits) >= 2 else "B"
        return "Keep", grade, "Outbound youth education / study travel source-market lead", f"Search result matched targeted source-market terms: {', '.join(hits[:3])}."
    if review_hits:
        return "Review", "C", "Adjacent education/travel lead", "Education or travel terms present, but outbound youth study-tour fit needs confirmation."
    return "Remove", "D", "Weak search result", "Does not show clear youth education, study abroad, school trip, or summer camp fit."


def normalize_search(row):
    rec, grade, role, reason = audit(row)
    score = {"Keep": 12, "Review": 6, "Remove": 1}[rec]
    if grade == "A":
        score += 3
    if row.get("description"):
        score += 1
    return {
        "business_name": row["title"].split("|")[0].split(" - ")[0].strip()[:120],
        "website": row["url"],
        "city": "",
        "country": row["country"],
        "email": "",
        "phone": "",
        "instagram": "",
        "linkedin_company_url": "",
        "linkedin_person_url": "",
        "linkedin_source": "",
        "decision_maker_name": "",
        "decision_maker_title": "",
        "decision_maker_email": "",
        "decision_maker_phone": "",
        "decision_source_url": "",
        "decision_source_type": "",
        "decision_confidence": "",
        "score": score,
        "notes": f"google_search_title: {row['title']} | description: {row['description']} | query: {row['query']} | rank: {row['rank']}",
        "google_maps_url": "",
        "quality_recommendation": rec,
        "quality_grade": grade,
        "market_role": role,
        "quality_reason": reason,
        "lat": row["lat"],
        "lon": row["lon"],
    }


def listify(value):
    if isinstance(value, list):
        return "; ".join(str(v).strip() for v in value if v)
    return str(value or "").strip()


def clean_email(value):
    if isinstance(value, list):
        value = "; ".join(str(v) for v in value if v)
    parts = []
    for part in str(value or "").replace("%20", "").split(";"):
        part = part.strip()
        if "@" in part and part.lower() not in [p.lower() for p in parts]:
            parts.append(part)
    return "; ".join(parts)


def merge_contact(row, contact):
    row = dict(row)
    row["email"] = clean_email(contact.get("emails") or row["email"])
    phones = listify(contact.get("phones") or contact.get("phonesUncertain") or "")
    if phones:
        row["phone"] = phones
    row["instagram"] = listify(contact.get("instagrams") or row["instagram"])
    linkedins = listify(contact.get("linkedIns") or "")
    row["linkedin_company_url"] = "; ".join(link for link in linkedins.split("; ") if "/company/" in link)
    row["linkedin_person_url"] = "; ".join(link for link in linkedins.split("; ") if "/in/" in link)
    row["linkedin_source"] = "Apify contact scraping" if linkedins else ""
    if row["email"]:
        row["score"] = int(row["score"]) + 2
    if row["phone"]:
        row["score"] = int(row["score"]) + 1
    if row["linkedin_company_url"] or row["linkedin_person_url"]:
        row["score"] = int(row["score"]) + 1
    return row


def dedupe_key(row):
    dom = domain(row["website"])
    if dom:
        return f"domain:{dom}"
    return "name:" + re.sub(r"\s+", " ", f"{row['business_name']}|{row['country']}".lower()).strip()


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(rows)


def main():
    load_dotenv()
    token = os.environ["APIFY_TOKEN"]
    raw_results = json.loads(RAW_SEARCH_JSON.read_text(encoding="utf-8")) if RAW_SEARCH_JSON.exists() else []
    completed_countries = {row.get("country") for row in raw_results if row.get("country")}
    for country, google_country, language, lat, lon, queries in COUNTRIES:
        if country in completed_countries:
            print(f"Skip {country}: already checkpointed")
            continue
        payload = {
            "queries": "\n".join(queries),
            "maxPagesPerQuery": 1,
            "resultsPerPage": 10,
            "countryCode": google_country,
            "languageCode": language,
            "searchLanguage": language.split("-")[0],
        }
        print(f"Search {country}: {len(queries)} queries")
        try:
            dataset_id = run_actor(token, SEARCH_ACTOR, payload)
        except Exception as exc:
            print(f"Search {country} failed; continuing: {exc}")
            continue
        items = fetch_dataset(token, dataset_id)
        for q in queries:
            pass
        for item in result_items(items, {"country": country, "lat": lat, "lon": lon, "query": payload["queries"].replace("\n", " || ")}):
            raw_results.append(item)
        RAW_SEARCH_JSON.write_text(json.dumps(raw_results, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"{country}: raw total={len(raw_results)}")

    seen = set()
    audited = []
    for raw in raw_results:
        row = normalize_search(raw)
        key = dedupe_key(row)
        if key in seen:
            continue
        seen.add(key)
        audited.append(row)

    audited.sort(key=lambda r: ({"Keep": 0, "Review": 1, "Remove": 2}[r["quality_recommendation"]], -int(r["score"]), r["country"], r["business_name"]))
    SEARCH_AUDIT_JSON.write_text(json.dumps(audited, indent=2, ensure_ascii=False), encoding="utf-8")
    candidates = [row for row in audited if row["quality_recommendation"] in {"Keep", "Review"}][:100]
    SEARCH_TOP_JSON.write_text(json.dumps(candidates, indent=2, ensure_ascii=False), encoding="utf-8")

    contacts = []
    for idx in range(0, len(candidates), 20):
        batch = candidates[idx:idx + 20]
        payload = {
            "startUrls": [{"url": row["website"]} for row in batch],
            "maxRequestsPerStartUrl": 8,
            "maxDepth": 2,
            "sameDomain": True,
            "mergeContacts": True,
            "proxyConfig": {"useApifyProxy": True},
        }
        print(f"Enrich batch {idx // 20 + 1}: {len(batch)} urls")
        dataset_id = run_actor(token, CONTACT_ACTOR, payload, timeout=900)
        contacts.extend(fetch_dataset(token, dataset_id))
        ENRICH_RAW_JSON.write_text(json.dumps(contacts, indent=2, ensure_ascii=False), encoding="utf-8")

    by_domain = {}
    for contact in contacts:
        key = domain(contact.get("originalStartUrl") or contact.get("domain") or "")
        if key:
            by_domain[key] = contact

    enriched = []
    for row in candidates:
        enriched.append(merge_contact(row, by_domain.get(domain(row["website"]), {})))
    enriched.sort(key=lambda r: (-int(r["score"]), r["country"], r["business_name"]))
    WORK_JSON.write_text(json.dumps(enriched, indent=2, ensure_ascii=False), encoding="utf-8")
    write_csv(WORK_CSV, enriched)

    base = json.loads(Path("lead-output/combined-worldwide-education-partnership-leads-map-data.json").read_text(encoding="utf-8") if Path("lead-output/combined-worldwide-education-partnership-leads-map-data.json").exists() else Path("lead-output/combined-uk-turkey-spain-italy-leads-map-data.json").read_text(encoding="utf-8"))
    combined = []
    combined_seen = set()
    for row in base + enriched:
        key = dedupe_key(row)
        if key in combined_seen:
            continue
        combined_seen.add(key)
        combined.append(row)
    COMBINED_JSON.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")

    counts = {}
    for row in enriched:
        counts[row["quality_recommendation"]] = counts.get(row["quality_recommendation"], 0) + 1
    print(f"raw={len(raw_results)} audited={len(audited)} enriched={len(enriched)} counts={counts}")
    print(WORK_JSON)
    print(COMBINED_JSON)


if __name__ == "__main__":
    main()
