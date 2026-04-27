#!/usr/bin/env python3
import json
import re
from pathlib import Path


INPUT = Path("lead-output/euro-spain-italy-quality-audit.json")
TEMPLATE = Path("lead-output/build_lead_earth_map.py")
OUTPUT_SCRIPT = Path("lead-output/build_euro_flat_map_generated.py")
OUTPUT_HTML = Path("lead-output/euro-spain-italy-map.html")


COORDS = {
    ("Alcobendas", "ES"): (40.5373, -3.6372),
    ("Almería", "ES"): (36.8340, -2.4637),
    ("Almuñécar", "ES"): (36.7339, -3.6907),
    ("Balestrate", "IT"): (38.0516, 13.0071),
    ("Barcelona", "ES"): (41.3874, 2.1686),
    ("Bilbao", "ES"): (43.2630, -2.9350),
    ("Casamassima", "IT"): (40.9568, 16.9206),
    ("Castillo Caleta de Fuste", "ES"): (28.3987, -13.8570),
    ("Cómpeta", "ES"): (36.8330, -3.9740),
    ("El Salobre", "ES"): (27.7830, -15.6330),
    ("Florence", "IT"): (43.7696, 11.2558),
    ("Granada", "ES"): (37.1773, -3.5986),
    ("Ingenio", "ES"): (27.9186, -15.4340),
    ("Jandia", "ES"): (28.0660, -14.3430),
    ("La Pared", "ES"): (28.2137, -14.2184),
    ("La Zubia", "ES"): (37.1197, -3.5840),
    ("Las Palmas de Gran Canaria", "ES"): (28.1235, -15.4363),
    ("Madrid", "ES"): (40.4168, -3.7038),
    ("Málaga", "ES"): (36.7213, -4.4214),
    ("Maspalomas", "ES"): (27.7606, -15.5860),
    ("Milan", "IT"): (45.4642, 9.1900),
    ("Misterbianco", "IT"): (37.5187, 15.0066),
    ("Motril", "ES"): (36.7484, -3.5169),
    ("Padua", "IT"): (45.4064, 11.8768),
    ("Palermo", "IT"): (38.1157, 13.3615),
    ("Pescara", "IT"): (42.4618, 14.2161),
    ("Playa del Inglés", "ES"): (27.7570, -15.5787),
    ("Rome", "IT"): (41.9028, 12.4964),
    ("Seville", "ES"): (37.3891, -5.9845),
    ("Soriano nel Cimino", "IT"): (42.4189, 12.2341),
    ("Torrelles de Llobregat", "ES"): (41.3552, 1.9819),
    ("València", "ES"): (39.4699, -0.3763),
    ("Vanzaghello", "IT"): (45.5793, 8.7810),
}


def main():
    leads = json.loads(INPUT.read_text(encoding="utf-8"))
    for lead in leads:
        lat, lon = COORDS.get((lead.get("city", ""), lead.get("country", "")), (None, None))
        lead["lat"] = lat
        lead["lon"] = lon

    text = TEMPLATE.read_text(encoding="utf-8")
    text = text.replace('INPUT = Path("lead-output/education-partnership-leads-50-quality-audit.json")', 'INPUT = Path("lead-output/euro-spain-italy-quality-audit.json")')
    text = text.replace('OUTPUT = Path("lead-output/education-partnership-leads-earth-map.html")', 'OUTPUT = Path("lead-output/euro-spain-italy-map.html")')
    text = text.replace("Lead Map Command Center", "Euro Lead Map Command Center")
    text = text.replace("Flat map navigation · drag pan · use zoom buttons · click a lead point", "Spain/Italy source-market leads · drag pan · button zoom · click a point")
    text = text.replace('<option value="GB">United Kingdom</option>\n              <option value="TR">Turkey</option>', '<option value="ES">Spain</option>\n              <option value="IT">Italy</option>')
    text = text.replace("centerLat: 49.6", "centerLat: 40.5")
    text = text.replace("centerLon: 14.4", "centerLon: 5.5")
    text = text.replace("zoom: 5.4", "zoom: 5.1")

    OUTPUT_SCRIPT.write_text(text, encoding="utf-8")
    namespace = {"__name__": "__main__"}
    exec(compile(text, str(OUTPUT_SCRIPT), "exec"), namespace)
    html = OUTPUT_HTML.read_text(encoding="utf-8")
    html = re.sub(
        r"const LEADS = .*?;\n    const tileCache",
        "const LEADS = " + json.dumps(leads, ensure_ascii=False) + ";\n    const tileCache",
        html,
        flags=re.S,
    )
    OUTPUT_HTML.write_text(html, encoding="utf-8")
    print(OUTPUT_HTML)
    print(len(leads))


if __name__ == "__main__":
    main()
