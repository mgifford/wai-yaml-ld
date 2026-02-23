#!/usr/bin/env python3
import argparse
import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

import yaml


ACT_INDEX_URL = "https://www.w3.org/WAI/standards-guidelines/act/rules/"
AXE_INDEX_URL = "https://dequeuniversity.com/rules/axe/html/4.11"
ALFA_INDEX_URL = "https://alfa.siteimprove.com/rules"
IBM_CHECKER_RULESETS_URL = "https://www.ibm.com/able/requirements/checker-rule-sets/"
QUALWEB_REPO_URL = "https://github.com/qualweb/act-rules"
QUALWEB_RULES_API_URL = "https://api.github.com/repos/qualweb/act-rules/contents/src/rules?ref=master"


def fetch_text(url: str) -> str:
    req = Request(url, headers={"User-Agent": "wai-yaml-ld-rule-refresh/1.0"})
    with urlopen(req, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def fetch_json(url: str):
    req = Request(url, headers={"User-Agent": "wai-yaml-ld-rule-refresh/1.0"})
    with urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def clean_text(value: str) -> str:
    stripped = re.sub(r"<[^>]+>", " ", value)
    unescaped = html.unescape(stripped)
    return re.sub(r"\s+", " ", unescaped).strip()


def extract_act_rules(html: str):
    anchors = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, flags=re.IGNORECASE | re.DOTALL)
    seen = {}
    for href, label in anchors:
        absolute = urljoin(ACT_INDEX_URL, href)
        match = re.match(r"^https://www\.w3\.org/WAI/standards-guidelines/act/rules/([a-z0-9]{6})/(proposed/)?$", absolute)
        if not match:
            continue
        rule_id = match.group(1)
        status = "proposed" if match.group(2) else "approved"
        title = clean_text(label)

        existing = seen.get(rule_id)
        if existing and existing.get("status") == "approved" and status == "proposed":
            continue

        payload = {
            "id": rule_id,
            "url": absolute,
            "status": status,
        }
        if title:
            payload["title"] = title
        seen[rule_id] = payload
    return [seen[key] for key in sorted(seen.keys())]


def extract_axe_rules(html: str):
    anchors = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, flags=re.IGNORECASE | re.DOTALL)
    seen = {}
    for href, label in anchors:
        absolute = urljoin(AXE_INDEX_URL, href)
        match = re.match(r"^https://dequeuniversity\.com/rules/axe/4\.11/([a-z0-9-]+)$", absolute, flags=re.IGNORECASE)
        if not match:
            continue

        rule_id = match.group(1).lower()
        title = clean_text(label)
        if title.lower().startswith(rule_id):
            title = title[len(rule_id):].strip(" :-")

        payload = {
            "id": rule_id,
            "url": f"https://dequeuniversity.com/rules/axe/4.11/{rule_id}",
            "status": "published",
        }
        if title:
            payload["title"] = title
        seen[rule_id] = payload

    return [seen[key] for key in sorted(seen.keys())]


def extract_alfa_rules(html: str):
    anchors = re.findall(r'<a[^>]+href=["\'](/rules/sia-r[0-9]+)["\'][^>]*>(.*?)</a>', html, flags=re.IGNORECASE | re.DOTALL)
    seen = {}
    for href, label in anchors:
        rule_id = href.rsplit("/", 1)[-1].lower()
        title = clean_text(label)
        title = re.sub(r"^SIA-R[0-9]+\s*", "", title, flags=re.IGNORECASE).strip(" :-")

        payload = {
            "id": rule_id,
            "url": f"https://alfa.siteimprove.com/rules/{rule_id}",
            "status": "published",
        }
        if title:
            payload["title"] = title
        seen[rule_id] = payload

    return [seen[key] for key in sorted(seen.keys(), key=lambda value: int(value.split("r", 1)[1]))]


def extract_qualweb_rules():
    items = fetch_json(QUALWEB_RULES_API_URL)
    rules = []

    for item in items:
        name = item.get("name", "")
        match = re.match(r"^QW-ACT-R([0-9]+)\.ts$", name)
        if not match:
            continue

        rule_num = int(match.group(1))
        rule_id = f"QW-ACT-R{rule_num}"
        rules.append(
            {
                "id": rule_id,
                "url": item.get("html_url") or f"{QUALWEB_REPO_URL}/blob/master/src/rules/{name}",
                "status": "published",
            }
        )

    return sorted(rules, key=lambda rule: int(rule["id"].split("R", 1)[1]))


def build_catalog(act_rules, axe_rules, alfa_rules, qualweb_rules):
    today = datetime.now(timezone.utc).date().isoformat()
    return {
        "project": "wai-standards-yaml-ld-ingestion",
        "updated": today,
        "scope": "accessibility_rule_catalogs",
        "act_rules_extracted_at": today,
        "axe_rules_extracted_at": today,
        "alfa_rules_extracted_at": today,
        "qualweb_rules_extracted_at": today,
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
            {
                "id": "qualweb-act-rules",
                "title": "QualWeb ACT Rules",
                "provider": "QualWeb",
                "catalog_url": QUALWEB_REPO_URL,
                "type": "act_implementation_rules",
                "applies_to": ["wcag-2.2", "wai-aria-1.2"],
                "rule_count": len(qualweb_rules),
                "rules": qualweb_rules,
            },
            {
                "id": "ibm-equal-access-checker-rule-sets",
                "title": "IBM Equal Access Accessibility Checker Rule Sets",
                "provider": "IBM",
                "catalog_url": IBM_CHECKER_RULESETS_URL,
                "type": "act_implementation_rules",
                "applies_to": ["wcag-2.2", "wai-aria-1.2", "atag-2.0", "uaag-2.0"],
                "rule_count": None,
                "rules": [],
                "extraction_note": "The IBM checker rule-sets page is dynamically rendered; include as published ACT-aligned source metadata.",
            },
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Refresh ACT, axe-core, Alfa, and partner ACT implementation rule catalogs")
    parser.add_argument(
        "--out-yaml",
        default="kitty-specs/001-wai-standards-yaml-ld-ingestion/research/accessibility-rule-catalogs.yaml",
        help="Path to output YAML file",
    )
    args = parser.parse_args()

    act_rules = extract_act_rules(fetch_text(ACT_INDEX_URL))
    axe_rules = extract_axe_rules(fetch_text(AXE_INDEX_URL))
    alfa_rules = extract_alfa_rules(fetch_text(ALFA_INDEX_URL))
    qualweb_rules = extract_qualweb_rules()

    if not act_rules:
        raise SystemExit("No ACT rules extracted; refusing to overwrite output")
    if not axe_rules:
        raise SystemExit("No axe rules extracted; refusing to overwrite output")
    if not alfa_rules:
        raise SystemExit("No Alfa rules extracted; refusing to overwrite output")
    if not qualweb_rules:
        raise SystemExit("No QualWeb rules extracted; refusing to overwrite output")

    catalog = build_catalog(act_rules, axe_rules, alfa_rules, qualweb_rules)
    output_path = Path(args.out_yaml)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml.safe_dump(catalog, sort_keys=False, allow_unicode=True))

    print(
        f"act_rules={len(act_rules)} axe_rules={len(axe_rules)} "
        f"alfa_rules={len(alfa_rules)} qualweb_rules={len(qualweb_rules)}"
    )
    print(f"out={output_path}")


if __name__ == "__main__":
    main()
