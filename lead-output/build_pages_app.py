#!/usr/bin/env python3
from pathlib import Path


SOURCE = Path("lead-output/combined-uk-turkey-spain-italy-leads-map.html")
OUTPUT = Path("docs/index.html")


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(SOURCE.read_text(encoding="utf-8"), encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
