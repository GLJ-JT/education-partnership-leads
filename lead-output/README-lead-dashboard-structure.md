# Lead Dashboard JSON Structure

Use `lead-json-structure.json` as the field contract for future lead batches.

The dashboard expects a JSON array of lead objects. Keep the fields in this order:

1. `business_name`
2. `website`
3. `city`
4. `country`
5. `email`
6. `phone`
7. `instagram`
8. `linkedin_company_url`
9. `linkedin_person_url`
10. `linkedin_source`
11. `decision_maker_name`
12. `decision_maker_title`
13. `decision_maker_email`
14. `decision_maker_phone`
15. `decision_source_url`
16. `decision_source_type`
17. `decision_confidence`
18. `score`
19. `notes`
20. `google_maps_url`

Rules:

- Leave unknown fields blank. Do not guess decision-maker names, emails, phones, or LinkedIn profiles.
- Use semicolons for multiple emails, phones, Instagram URLs, or LinkedIn URLs.
- Put source-backed proof for decision-maker data in `decision_source_url`.
- Use `High`, `Medium`, or `Low` for `decision_confidence`.
- Keep `score` numeric where possible.

Starter file:

`lead-json-template.json`
