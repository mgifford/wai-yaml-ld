#!/usr/bin/env python3
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import yaml


ACT_INDEX_URL = "https://www.w3.org/WAI/standards-guidelines/act/rules/"
AXE_INDEX_URL = "https://dequeuniversity.com/rules/axe/html/4.11"
ALFA_INDEX_URL = "https://alfa.siteimprove.com/rules"


def fetch_text(url: str) -> str:
    req = Request(url, headers={"User-Agent": "wai-yaml-ld-rule-refresh/1.0"})
    with urlopen(req, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def extract_act_rules(html: str):
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', html, flags=re.IGNORECASE)
    seen = {}
    for href in hrefs:
        absolute = urljoin(ACT_INDEX_URL, href)
        match = re.match(r"^https://www\.w3\.org/WAI/standards-guidelines/act/rules/([a-z0-9]{6})/(proposed/)?$", absolute)
        if not match:
            continue
        rule_id = match.group(1)
        status = "proposed" if match.group(2) else "approved"
        seen[rule_id] = {
            "id": rule_id,
            "url": absolute,
            "status": status,
        }
    return [seen[key] for key in sorted(seen.keys())]


def extract_axe_rules(html: str):
    matches = set(re.findall(r"https://dequeuniversity\.com/rules/axe/4\.11/([a-z0-9-]+)", html, flags=re.IGNORECASE))
    return [
        {
            "id": rule_id.lower(),
            "url": f"https://dequeuniversity.com/rules/axe/4.11/{rule_id.lower()}",
            "status": "published",
        }
        for rule_id in sorted(matches)
    ]


def extract_alfa_rules(html: str):
    matches = set(re.findall(r"/rules/(sia-r[0-9]+)", html, flags=re.IGNORECASE))
    return [
        {
            "id": rule_id.lower(),
            "url": f"https://alfa.siteimprove.com/rules/{rule_id.lower()}",
            "status": "published",
        }
        for rule_id in sorted(matches, key=lambda value: int(value.split("r", 1)[1]))
    ]


def build_catalog(act_rules, axe_rules, alfa_rules):
    today = datetime.now(timezone.utc).date().isoformat()
    return {
        "project": "wai-standards-yaml-ld-ingestion",
        "updated": today,
        "scope": "accessibility_rule_catalogs",
        "act_rules_extracted_at": today,
        "axe_rules_extracted_at": today,
        "alfa_rules_extracted_at": today,
        "rule_sets": [
            {
                "id": "w3c-act-rules",
                "title": "W3C ACT Rules",
                "provider": "W3C",
                "catalog_url": ACT_INDEX_URL,
                "type": "informative",
                "applies_to": ["wcag-2.2", "wai-aria-1.2", "atag-2.0", "uaag-2.0"],
                "rule_count": len(act_rules),
                "rules": act_rules,
            },
            {
                "id": "deque-axe-rules-4.11",
                "title": "Deque axe-core Rules 4.11",
                "provider": "Deque",
                "catalog_url": AXE_INDEX_URL,
                "type": "vendor_tool_rules",
                "applies_to": ["wcag-2.2", "wai-aria-1.2"],
                "rule_count": len(axe_rules),
                "rules": axe_rules,
            },
            {
                "id": "siteimprove-alfa-rules",
                "title": "Siteimprove Alfa Rules",
                "provider": "Siteimprove",
                "catalog_url": ALFA_INDEX_URL,
                "type": "vendor_tool_rules",
                "applies_to": ["wcag-2.2", "wai-aria-1.2"],
                "rule_count": len(alfa_rules),
                "rules": alfa_rules,
            },
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Refresh ACT, axe-core, and Alfa machine-readable rule catalogs")
    parser.add_argument(
        "--out-yaml",
        default="kitty-specs/001-wai-standards-yaml-ld-ingestion/research/accessibility-rule-catalogs.yaml",
        help="Path to output YAML file",
    )
    args = parser.parse_args()

    act_rules = extract_act_rules(fetch_text(ACT_INDEX_URL))
    axe_rules = extract_axe_rules(fetch_text(AXE_INDEX_URL))
    alfa_rules = extract_alfa_rules(fetch_text(ALFA_INDEX_URL))

    if not act_rules:
        raise SystemExit("No ACT rules extracted; refusing to overwrite output")
    if not axe_rules:
        raise SystemExit("No axe rules extracted; refusing to overwrite output")
    if not alfa_rules:
        raise SystemExit("No Alfa rules extracted; refusing to overwrite output")

    catalog = build_catalog(act_rules, axe_rules, alfa_rules)
    output_path = Path(args.out_yaml)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml.safe_dump(catalog, sort_keys=False, allow_unicode=True))

    print(f"act_rules={len(act_rules)} axe_rules={len(axe_rules)} alfa_rules={len(alfa_rules)}")
    print(f"out={output_path}")


if __name__ == "__main__":
    main()
