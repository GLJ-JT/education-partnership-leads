#!/usr/bin/env python3
import csv
import json
from pathlib import Path


INPUT = Path("lead-output/education-partnership-leads-50-clean.json")
OUT_JSON = Path("lead-output/education-partnership-leads-50-quality-audit.json")
OUT_CSV = Path("lead-output/education-partnership-leads-50-quality-audit.csv")


AUDIT = {
    "Newcastle International School": ("Keep", "B", "UK host/education provider", "UK language school/summer camp angle. Useful as host/partner, not a source-market agency."),
    "Oxford International Study Centre": ("Keep", "A", "UK host/education provider", "International school/language/sixth-form profile fits UK camp partnership."),
    "Voyager School Travel": ("Keep", "A", "UK educational travel operator", "Educational travel operator. Useful for UK camp partnerships and UK-to-China source market."),
    "Stonehenge Turizm Yurt Dışı Eğitim ve Danışmanlık": ("Keep", "A", "Turkey outbound education agency", "Yurt disi egitim means overseas education. Useful Turkey source-market referrer."),
    "Britannia English Academy": ("Keep", "A", "UK language school", "English language camp/school with high review volume. Strong UK camp ecosystem partner."),
    "Summer School of English for Foreign Children": ("Keep", "A", "UK language summer school", "Directly aligned with international children learning English in UK."),
    "Study International": ("Review", "C", "Education media/marketing", "Education media/ad agency, not clearly an operator. Potential marketing channel, weaker lead."),
    "European Study Tours": ("Keep", "B", "UK educational travel operator", "School tour operator. Good for UK/British source-market trips, but check direction of travel."),
    "International Summer Camp UK Ltd": ("Keep", "A", "UK summer camp operator", "Very aligned, though possibly competitor. Good partnership/benchmark lead."),
    "Sports Tours International": ("Review", "C", "Sports travel operator", "Travel operator but sports-focused and not clearly youth education/camp."),
    "University of Liverpool International Summer School": ("Review", "C", "UK university summer school", "International summer school, but university/adult leaning; may not match youth camp."),
    "International House Manchester": ("Keep", "A", "UK language school", "Strong language school/English camp fit."),
    "St Clare's, Oxford": ("Keep", "B", "UK international school/language provider", "International school/language provider. Useful partner, probably institutional rather than agency."),
    "Mill Hill International": ("Keep", "B", "UK international/boarding school", "Good international private school profile, useful host/network partner."),
    "ISSFT® International Summer School for Teens": ("Keep", "A", "UK teen summer school", "Direct summer school for teens; excellent benchmark/partnership lead."),
    "Bishop's Stortford College International Summer School": ("Keep", "A", "UK international summer school", "Directly aligned with youth international summer school."),
    "The English Language Centre Bristol": ("Keep", "B", "UK language school", "Strong language school. Useful partner/referral route, less camp-specific."),
    "Marine Discovery Penzance": ("Remove", "D", "Local activity/tour provider", "Local boat tour agency, not international education/source-market referrer."),
    "Tourist Information Centre Isles of Scilly": ("Remove", "D", "Tourist information", "Tourist info centre, not a student recruitment or camp operator."),
    "The School Trip": ("Keep", "B", "UK school trip platform/operator", "School trip/education consultant. Useful for UK camp partnerships."),
    "Cornwall Underground Adventures": ("Remove", "D", "Local activity provider", "Adventure activity provider, not international student/camp recruitment channel."),
    "Kernow Tours": ("Remove", "D", "Local tour operator", "Local tour operator, not youth education/source-market referrer."),
    "Which Boarding School": ("Keep", "B", "School placement consultant", "Boarding school consultant may reach international families; good referral-adjacent lead."),
    "Crowded House Tours": ("Remove", "D", "Turkey inbound tourism", "Gallipoli/inbound Turkey travel agency; not useful for sending students to UK or China."),
    "Yds Academy": ("Review", "C", "Turkey language school", "Turkey language school. Could be source-market partner if students seek overseas camps, but needs manual validation."),
    "English Express": ("Review", "C", "Turkey language school", "Turkey language school. Possible source-market referrer, but not clearly overseas travel/study agency."),
    "Study in Turkiye": ("Remove", "D", "Inbound-to-Turkey education", "Appears focused on studying in Turkey, opposite direction from your target."),
    "Yourtrainingcamp": ("Remove", "D", "Training camp/travel", "Not clearly youth education or outbound study travel."),
    "Halcyon London International School": ("Keep", "B", "UK international school", "International school with relevant audience; partner/referral possibility."),
    "Malvern College": ("Keep", "B", "UK boarding/private school", "International-facing boarding/private school; useful institutional partner."),
    "The School Travel Company": ("Keep", "A", "UK school travel operator", "School travel company. Strong for educational trips/camp partnerships."),
    "Wrekin College": ("Keep", "B", "UK boarding/private school", "Boarding school with international outlook; useful UK institutional partner."),
    "Shrewsbury School": ("Keep", "B", "UK boarding/private school", "Strong private/boarding school with international audience."),
    "St. Mary's Riding Centre Ltd": ("Remove", "D", "Local riding school", "Local riding provider, not international camp/source-market referrer."),
    "Oxbridge International Summer School": ("Keep", "A", "UK international summer school", "Directly aligned, but website missing in scrape; needs website recovery."),
    "Glenbrittle Youth Hostel": ("Remove", "D", "Hostel", "Accommodation/youth hostel, not a student recruitment or camp operator."),
    "Cnoc Soilleir Limited": ("Review", "C", "Music/cultural education", "Music/cultural education provider. Possible niche partner, but weak source-market fit."),
    "International School Aberdeen": ("Keep", "B", "UK international school", "International school; relevant for partnerships/referrals."),
    "The Learning Adventure": ("Keep", "A", "Educational travel operator", "Educational travel operator. Strong fit for UK/China study trip partnerships."),
    "Advice Yurtdışı Eğitim": ("Keep", "A", "Turkey outbound education agency", "Yurt disi egitim means overseas education. Good Turkey source-market referrer."),
    "Sümelas Camping": ("Remove", "D", "Local campground/tourism", "Campground/tourism venue in Turkey, not source-market education partner."),
    "ACS International School Egham": ("Keep", "B", "UK international school", "International school with relevant international audience."),
    "DGI Study Trips": ("Keep", "A", "Study trip operator", "Direct study trips operator. Strong fit."),
    "Select School Tours - Educational School Trips": ("Keep", "A", "Educational school trip operator", "Educational school trips operator. Strong fit."),
    "Adcote School for Girls": ("Keep", "B", "UK private/boarding school", "Private/boarding school with international potential."),
    "Basis Travel - Free Walking Tour Istanbul": ("Remove", "D", "Turkey inbound tourism", "Istanbul walking tour/inbound tourism; not useful for UK/China camp recruitment."),
    "Travel Store Turkey - Private Tours & Packages - Free Cancellation": ("Remove", "D", "Turkey inbound tourism", "Turkey private tours/packages; not youth education/outbound source-market fit."),
    "Education Destination Ltd": ("Keep", "B", "UK education destination/operator", "Education/tour operator. Potential fit, but lower evidence/low review count."),
    "Nemrut Turları Murat Polat": ("Remove", "D", "Turkey inbound tourism", "Local Turkey tour agency; not useful for sending students abroad."),
    "الدراسة في تركيا - Directly Education": ("Remove", "D", "Inbound-to-Turkey education", "Arabic 'study in Turkey' lead; opposite direction from target source-market recruitment."),
}


def main():
    rows = json.loads(INPUT.read_text(encoding="utf-8"))
    audited = []
    for row in rows:
        recommendation, grade, role, reason = AUDIT.get(
            row["business_name"],
            ("Review", "C", "Unclassified", "Needs manual review against source-market/UK-or-China-camp fit."),
        )
        audited.append(
            {
                **row,
                "quality_recommendation": recommendation,
                "quality_grade": grade,
                "market_role": role,
                "quality_reason": reason,
            }
        )

    OUT_JSON.write_text(json.dumps(audited, indent=2, ensure_ascii=False), encoding="utf-8")

    fields = list(audited[0].keys())
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(audited)

    counts = {}
    for row in audited:
        counts[row["quality_recommendation"]] = counts.get(row["quality_recommendation"], 0) + 1
    print(counts)
    print(OUT_JSON)
    print(OUT_CSV)


if __name__ == "__main__":
    main()
