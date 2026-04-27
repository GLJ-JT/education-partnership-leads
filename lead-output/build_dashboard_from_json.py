#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--template", default="lead-output/education-partnership-leads-dashboard.html")
    parser.add_argument("--output", required=True)
    parser.add_argument("--title", default="Education Partnership Leads")
    parser.add_argument("--subtitle", default="Leads with verified contacts where available")
    args = parser.parse_args()

    leads = json.loads(Path(args.input).read_text(encoding="utf-8"))
    text = Path(args.template).read_text(encoding="utf-8")
    text = re.sub(r"<h1>.*?</h1>", f"<h1>{args.title}</h1>", text, count=1)
    text = re.sub(r'<div class="sub">.*?</div>', f'<div class="sub">{args.subtitle}</div>', text, count=1)
    text = re.sub(
        r"const LEADS = .*?;\n    const CHECKS =",
        "const LEADS = " + json.dumps(leads, ensure_ascii=False) + ";\n    const CHECKS =",
        text,
        flags=re.S,
    )
    Path(args.output).write_text(text, encoding="utf-8")
    print(args.output)
    print(len(leads))


if __name__ == "__main__":
    main()
