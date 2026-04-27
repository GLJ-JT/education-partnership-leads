#!/usr/bin/env python3
import json
import re
from pathlib import Path


MAPS = [
    Path("lead-output/education-partnership-leads-earth-map.html"),
    Path("lead-output/euro-spain-italy-map.html"),
]
OUTPUT_JSON = Path("lead-output/combined-uk-turkey-spain-italy-leads-map-data.json")
OUTPUT_HTML = Path("lead-output/combined-uk-turkey-spain-italy-leads-map.html")


def load_leads(path):
    text = path.read_text(encoding="utf-8")
    match = re.search(r"const LEADS = (.*?);\n    const tileCache", text, re.S)
    if not match:
        raise ValueError(f"No embedded lead data found in {path}")
    return json.loads(match.group(1))


def dedupe_key(lead):
    website = (lead.get("website") or "").lower().strip().rstrip("/")
    if website:
        return f"site:{website}"
    return f"name:{(lead.get('business_name') or '').lower().strip()}|{lead.get('city') or ''}|{lead.get('country') or ''}"


def main():
    combined = []
    seen = set()
    for path in MAPS:
        for lead in load_leads(path):
            key = dedupe_key(lead)
            if key in seen:
                continue
            seen.add(key)
            combined.append(lead)

    order = {"Keep": 0, "Review": 1, "Remove": 2}
    combined.sort(
        key=lambda lead: (
            order.get(lead.get("quality_recommendation"), 9),
            lead.get("country") or "ZZ",
            lead.get("city") or "ZZ",
            lead.get("business_name") or "",
        )
    )
    OUTPUT_JSON.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")

    template = MAPS[0].read_text(encoding="utf-8")
    template = re.sub(
        r"const LEADS = .*?;\n    const tileCache",
        "const LEADS = " + json.dumps(combined, ensure_ascii=False) + ";\n    const tileCache",
        template,
        flags=re.S,
    )
    template = template.replace("Lead Map Command Center", "Combined Lead Map Command Center")
    template = template.replace(
        "Flat map navigation · drag pan · use zoom buttons · click a lead point",
        "UK, Turkey, Spain, and Italy leads · drag pan · button zoom · click a point",
    )
    template = template.replace(
        '<option value="GB">United Kingdom</option>\n              <option value="TR">Turkey</option>',
        '<option value="GB">United Kingdom</option>\n              <option value="TR">Turkey</option>\n              <option value="ES">Spain</option>\n              <option value="IT">Italy</option>',
    )
    template = template.replace("centerLat: 49.6", "centerLat: 43.8")
    template = template.replace("centerLon: 14.4", "centerLon: 8.5")
    template = template.replace("zoom: 5.4", "zoom: 4.7")
    OUTPUT_HTML.write_text(template, encoding="utf-8")

    counts = {}
    for lead in combined:
        rec = lead.get("quality_recommendation") or "Unknown"
        counts[rec] = counts.get(rec, 0) + 1
    print(f"combined={len(combined)} geocoded={sum(1 for lead in combined if lead.get('lat') is not None)} counts={counts}")
    print(OUTPUT_JSON)
    print(OUTPUT_HTML)


if __name__ == "__main__":
    main()
