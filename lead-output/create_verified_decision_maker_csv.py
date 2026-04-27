#!/usr/bin/env python3
import csv
from pathlib import Path


INPUT = Path("lead-output/education-partnership-leads-50.csv")
OUTPUT = Path("lead-output/education-partnership-leads-50-verified-decision-makers.csv")


VERIFIED = {
    "Oxford International Study Centre": {
        "decision_maker_name": "Benjamin Llewelyn",
        "decision_maker_title": "Principal / Proprietor",
        "decision_maker_phone": "+44 1865 201009",
        "decision_maker_email": "",
        "decision_source_url": "https://www.oxintstudycentre.com/about-us",
        "decision_source_type": "Official website",
        "decision_confidence": "High",
    },
    "Voyager School Travel": {
        "decision_maker_name": "Tricia Bryant",
        "decision_maker_title": "Sales & Operations Director",
        "decision_maker_phone": "+44 1273 827327",
        "decision_maker_email": "schools@voyagerschooltravel.com",
        "decision_source_url": "https://www.voyagerschooltravel.com/about-us/meet-the-team/",
        "decision_source_type": "Official website",
        "decision_confidence": "High",
    },
    "Britannia English Academy": {
        "decision_maker_name": "David Madrid Lluesma; Sergio Valls Orenga",
        "decision_maker_title": "Directors",
        "decision_maker_phone": "+44 7704 042005",
        "decision_maker_email": "",
        "decision_source_url": "https://find-and-update.company-information.service.gov.uk/company/08146137/officers",
        "decision_source_type": "Companies House",
        "decision_confidence": "High",
    },
    "European Study Tours": {
        "decision_maker_name": "Andrew James Mark Lewis Bracey; Peter John Churchus; Andrew James Clark; Aiden Charles Barwick Clegg; Neil Allen Currie; Nicole Sarah Graff; Anthony Gerald Jones; Anthony Graham Sadler",
        "decision_maker_title": "Current company directors",
        "decision_maker_phone": "",
        "decision_maker_email": "",
        "decision_source_url": "https://www.companiesintheuk.co.uk/ltd/european-study-tours",
        "decision_source_type": "Company registry mirror",
        "decision_confidence": "Medium",
    },
    "International Summer Camp UK Ltd": {
        "decision_maker_name": "Hiran Silva; Donna Silva",
        "decision_maker_title": "Directors",
        "decision_maker_phone": "+44 330 043 4634",
        "decision_maker_email": "",
        "decision_source_url": "https://find-and-update.company-information.service.gov.uk/company/SC401612",
        "decision_source_type": "Companies House",
        "decision_confidence": "High",
    },
    "International House Manchester": {
        "decision_maker_name": "John O'Leary; Peter Hayes; Katie Hayes",
        "decision_maker_title": "Director, School Principal; Director, Marketing; Director, School Registrar",
        "decision_maker_phone": "+44 7483 365723",
        "decision_maker_email": "",
        "decision_source_url": "https://ihmanchester.com/about-us/",
        "decision_source_type": "Official website",
        "decision_confidence": "High",
    },
    "St Clare's, Oxford": {
        "decision_maker_name": "Duncan Reith",
        "decision_maker_title": "Headteacher / Principal",
        "decision_maker_phone": "01865 552031",
        "decision_maker_email": "",
        "decision_source_url": "https://www.get-information-schools.service.gov.uk/Establishments/Establishment/Details/133430",
        "decision_source_type": "GOV.UK Get Information about Schools",
        "decision_confidence": "High",
    },
    "Halcyon London International School": {
        "decision_maker_name": "Jeff Lippman",
        "decision_maker_title": "Director / Headteacher-Principal",
        "decision_maker_phone": "+44 20 7258 1169",
        "decision_maker_email": "",
        "decision_source_url": "https://www.halcyonschool.com/about-us/directors-welcome",
        "decision_source_type": "Official website",
        "decision_confidence": "High",
    },
    "Malvern College": {
        "decision_maker_name": "Keith Metcalfe",
        "decision_maker_title": "Headmaster",
        "decision_maker_phone": "+44 1684 581502",
        "decision_maker_email": "",
        "decision_source_url": "https://www.malverncollege.org.uk/about-us/contact-us/",
        "decision_source_type": "Official website",
        "decision_confidence": "High",
    },
    "Wrekin College": {
        "decision_maker_name": "Toby Spence",
        "decision_maker_title": "Headmaster / CEO Wrekin Old Hall Trust",
        "decision_maker_phone": "+44 1952 265645",
        "decision_maker_email": "admissions@wrekincollege.com",
        "decision_source_url": "https://wrekinoldhall.com/wrekin-college-welcome/contact/",
        "decision_source_type": "Official website",
        "decision_confidence": "High",
    },
    "Shrewsbury School": {
        "decision_maker_name": "Martin Cropper; Leo Winkley",
        "decision_maker_title": "Director of Admissions; Headmaster",
        "decision_maker_phone": "01743 280552; 01743 280526",
        "decision_maker_email": "",
        "decision_source_url": "https://www.shrewsbury.org.uk/page/directions-shrewsbury-school",
        "decision_source_type": "Official website",
        "decision_confidence": "High",
    },
    "International School Aberdeen": {
        "decision_maker_name": "Nick Little",
        "decision_maker_title": "Head of School",
        "decision_maker_phone": "+44 1224 730300",
        "decision_maker_email": "",
        "decision_source_url": "https://www.tes.com/magazine/leadership/strategy/my-week-head-international-school-aberdeen",
        "decision_source_type": "Education press",
        "decision_confidence": "Medium",
    },
    "ACS International School Egham": {
        "decision_maker_name": "Mark Wilson; Suzanne Ingham",
        "decision_maker_title": "Head of School; Dean of Admissions",
        "decision_maker_phone": "+44 1784 430611",
        "decision_maker_email": "",
        "decision_source_url": "https://www.acs-schools.com/egham/about/leadership-team/",
        "decision_source_type": "Official website",
        "decision_confidence": "High",
    },
    "DGI Study Trips": {
        "decision_maker_name": "Kate Erskine; Shannon Gibson",
        "decision_maker_title": "Head of DGI Study Trips; Sales Manager",
        "decision_maker_phone": "+44 161 884 5361",
        "decision_maker_email": "",
        "decision_source_url": "https://www.dgistudytrips.com/about-us/",
        "decision_source_type": "Official website",
        "decision_confidence": "High",
    },
    "Select School Tours - Educational School Trips": {
        "decision_maker_name": "",
        "decision_maker_title": "Management / Sales team listed, no named decision maker visible",
        "decision_maker_phone": "+44 1444 870100",
        "decision_maker_email": "",
        "decision_source_url": "https://selectschooltours.com/about-us/",
        "decision_source_type": "Official website",
        "decision_confidence": "Low",
    },
    "The School Travel Company": {
        "decision_maker_name": "Andrew Gardiner",
        "decision_maker_title": "Owner / Director",
        "decision_maker_phone": "+44 1384 398893",
        "decision_maker_email": "",
        "decision_source_url": "https://www.theschooltravelcompany.com/about-us/",
        "decision_source_type": "Official website",
        "decision_confidence": "High",
    },
    "The Learning Adventure": {
        "decision_maker_name": "Alex Seigel",
        "decision_maker_title": "CEO",
        "decision_maker_phone": "+44 20 7157 9964",
        "decision_maker_email": "info@thelearningadventure.com",
        "decision_source_url": "https://the-learning-adventure.10web.cloud/en-us/about/meet-our-team/",
        "decision_source_type": "Official website",
        "decision_confidence": "High",
    },
    "The English Language Centre Bristol": {
        "decision_maker_name": "John Duncan; Margaret Duncan; Andrew Edwards",
        "decision_maker_title": "Directors / Welfare Officers; Principal / Homestay Manager",
        "decision_maker_phone": "+44 117 970 7060",
        "decision_maker_email": "info@elcbristol.co.uk",
        "decision_source_url": "https://elcbristol.co.uk/english-language-school-bristol/the-admin-team/",
        "decision_source_type": "Official website",
        "decision_confidence": "High",
    },
}


NEW_FIELDS = [
    "decision_maker_name",
    "decision_maker_title",
    "decision_maker_phone",
    "decision_maker_email",
    "decision_source_url",
    "decision_source_type",
    "decision_confidence",
]


with INPUT.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
    original_fields = list(rows[0].keys())

for row in rows:
    verified = VERIFIED.get(row["business_name"], {})
    for field in NEW_FIELDS:
        row[field] = verified.get(field, "")
    if verified:
        row["owner_director_manager_name"] = verified["decision_maker_name"]
        row["director_or_manager_email"] = verified["decision_maker_email"]

with OUTPUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=original_fields + NEW_FIELDS)
    writer.writeheader()
    writer.writerows(rows)

print(f"wrote={OUTPUT}")
print(f"verified_rows={sum(1 for row in rows if row['decision_source_url'])}")
