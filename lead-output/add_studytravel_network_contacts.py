#!/usr/bin/env python3
import json
from collections import OrderedDict
from pathlib import Path


DATA = Path("lead-output/combined-worldwide-education-partnership-leads-map-data.json")
SOURCE = "StudyTravel Network member portal / My Network screenshot supplied by account member"

FIELDS = [
    "business_name",
    "website",
    "city",
    "country",
    "email",
    "phone",
    "instagram",
    "linkedin_company_url",
    "linkedin_person_url",
    "linkedin_source",
    "decision_maker_name",
    "decision_maker_title",
    "decision_maker_email",
    "decision_maker_phone",
    "decision_source_url",
    "decision_source_type",
    "decision_confidence",
    "score",
    "notes",
    "google_maps_url",
    "quality_recommendation",
    "quality_grade",
    "market_role",
    "quality_reason",
    "lat",
    "lon",
]


def lead(company, person, title, city, country, lat, lon, role, notes, grade="A", score=17):
    record = {
        "business_name": company,
        "website": "",
        "city": city,
        "country": country,
        "email": "",
        "phone": "",
        "instagram": "",
        "linkedin_company_url": "",
        "linkedin_person_url": "",
        "linkedin_source": "",
        "decision_maker_name": person,
        "decision_maker_title": title,
        "decision_maker_email": "",
        "decision_maker_phone": "",
        "decision_source_url": "",
        "decision_source_type": "StudyTravel Network member portal",
        "decision_confidence": "High",
        "score": score,
        "notes": f"source: {SOURCE} | {notes}",
        "google_maps_url": "",
        "quality_recommendation": "Keep",
        "quality_grade": grade,
        "market_role": role,
        "quality_reason": "Visible StudyTravel Network connection with named education/travel decision-maker or senior commercial contact.",
        "lat": lat,
        "lon": lon,
    }
    return OrderedDict((field, record.get(field, "")) for field in FIELDS)


STUDYTRAVEL_CONTACTS = [
    lead("Bridge Mills Galway Language Centre - International House Galway", "Patrick Creed", "School Director", "Galway", "IE", 53.2707, -9.0568, "Ireland English language school / educator", "Network tags: connected; Educator. Locations: Ireland."),
    lead("Interway Educational Consultancy", "Gustavo Viale", "CEO", "Buenos Aires", "AR", -34.6037, -58.3816, "Argentina outbound education consultancy", "Network tags: connected; Agent. Locations: International, Argentina, Canada, United Kingdom."),
    lead("ARSAA - Argentine Study Abroad Association (ICABA)", "Gustavo Viale", "CEO", "Buenos Aires", "AR", -34.6037, -58.3816, "Argentina study abroad association", "Network tags: connected; Association. Locations: Argentina."),
    lead("MLI International Schools - Dublin", "Brendan Kelly", "Group Marketing Director", "Dublin", "IE", 53.3498, -6.2603, "Ireland international schools / junior programmes", "Network tags: connected; Educator. Locations: International, Ireland, United Kingdom."),
    lead("Osvita Tour Agency", "Elena Pshegorskaya", "Director", "Surrey", "CA", 49.1913, -122.849, "Canada / Ukraine education travel agent", "Network tags: connected; Agent. Locations: International, Canada, Ukraine."),
    lead("Ally - Your Education Hub", "Ricardo Lemos", "COO", "Brazil", "BR", -14.235, -51.9253, "Brazil education hub / service provider", "Network tags: connected; Service Provider. Locations: Brazil."),
    lead("LAL Cape Town", "Shaun Fitzhenry", "Regional Sales Manager Europe", "Cape Town", "ZA", -33.9249, 18.4241, "South Africa language school / educator", "Network tags: connected; Educator. Locations: South Africa."),
    lead("No Fluff", "Nicola Lutz", "Owner", "United Kingdom", "GB", 51.5072, -0.1276, "UK study travel service provider", "Network tags: connected; Service Provider. Locations: United Kingdom.", grade="B", score=14),
    lead("Frances King School of English - London", "Roberto Russo", "Partner Relations", "London", "GB", 51.5072, -0.1276, "UK English language school partner relations", "Network tags: connected; Educator. Locations: International, United Kingdom."),
    lead("St Clare's Oxford", "Francisco Bustos", "Student Recruitment Manager", "Oxford", "GB", 51.752, -1.2577, "UK international education / student recruitment", "Network tags: connected; Educator. Locations: United Kingdom."),
    lead("VEF Global (ISTANBUL)", "Basak Aras", "", "Istanbul", "TR", 41.0082, 28.9784, "Turkey education service provider", "Network tags: connected; Service Provider. Locations: Turkiye.", grade="B", score=15),
    lead("The National Mathematics & Science College", "Jake Wilson", "Director of Business Development", "Coventry", "GB", 52.4068, -1.5197, "UK STEM / international school business development", "Network tags: connected; Educator. Locations: United Kingdom."),
    lead("Morgan Oxford Education (formerly Y2GO Limited)", "Richard Morgan", "Chairman", "Nigeria", "NG", 9.082, 8.6753, "International education agency / agent", "Network tags: connected; Agent. Locations: International, Canada, Egypt, Ghana, Hungary, Nigeria, United Kingdom, United States."),
    lead("Univag School", "Fabricio Vargas", "CEO", "Brazil", "BR", -14.235, -51.9253, "Brazil education provider / educator", "Network tags: connected; Educator. Locations: Brazil."),
    lead("Ireland4Europe", "Kamran Khan", "CEO / Owner", "Ireland", "IE", 53.3498, -6.2603, "Ireland outbound/inbound education travel agent", "Network tags: connected; Agent. Locations: International, Argentina, Czech Republic, France, Germany, Hungary, Ireland, Italy, Poland, Portugal, Russia."),
    lead("EduSolv Consultancy & Solutions", "Giuliana Bonvini", "AI Architect & Founder", "Crawley", "GB", 51.1091, -0.1872, "UK education consultancy / service provider", "Network tags: connected; Service Provider. Locations: United Kingdom.", grade="B", score=14),
    lead("ES Global", "Aamir Ghafoor", "", "United Arab Emirates", "AE", 25.2048, 55.2708, "UAE education agent", "Network tags: connected; Agent. Locations: International, Kenya, Pakistan, Portugal, United Arab Emirates, United Kingdom.", grade="B", score=15),
    lead("Olymp Group LTD", "Romeo Fazal", "Global Recruitment Manager", "International", "INT", 42.5, 12.5, "International student recruitment agent", "Network tags: connected; Agent. Locations: International, Australia, Canada, Germany, Malta, Romania, Spain, United Kingdom, United States.", grade="B", score=15),
]


def main():
    leads = json.loads(DATA.read_text(encoding="utf-8"))
    existing = {
        (item.get("business_name", "").strip().lower(), item.get("decision_maker_name", "").strip().lower())
        for item in leads
    }
    added = 0
    for item in STUDYTRAVEL_CONTACTS:
        key = (item["business_name"].strip().lower(), item["decision_maker_name"].strip().lower())
        if key not in existing:
            leads.append(item)
            added += 1
    DATA.write_text(json.dumps(leads, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"added={added} total={len(leads)}")


if __name__ == "__main__":
    main()
