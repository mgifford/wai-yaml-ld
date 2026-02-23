#!/usr/bin/env python3
import argparse
import csv
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

SC_REF_RE = re.compile(r"(?:Success\s+Criterion|SC)\s*([1-4]\.\d+\.\d+)", re.IGNORECASE)
WCAG_RE = re.compile(r"\bWCAG(?:\s*2\.0|\s*2\.1|\s*2\.2)?\b", re.IGNORECASE)
ATAG_RE = re.compile(r"\bATAG(?:\s*2\.0)?\b", re.IGNORECASE)
UAAG_RE = re.compile(r"\bUAAG(?:\s*2\.0)?\b", re.IGNORECASE)
ARIA_RE = re.compile(r"\bWAI-ARIA\b|\bARIA\b", re.IGNORECASE)


def load_yaml(path: Path):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def normalize_standard_id(raw: str) -> str:
    value = str(raw).strip().lower()
    mapping = {
        "wcag-2.2": "wcag-2.2",
        "wcag-2.0": "wcag-2.0",
        "wcag-2.0-legacy": "wcag-2.0",
        "atag-2.0": "atag-2.0",
        "atag-2": "atag-2.0",
        "uaag-2.0": "uaag-2.0",
        "uaag-2": "uaag-2.0",
        "wai-aria": "wai-aria-1.2",
        "aria": "wai-aria-1.2",
        "wai-aria-1.2": "wai-aria-1.2",
    }
    return mapping.get(value, str(raw).strip())


def build_normative_index(data: dict):
    standard_id = normalize_standard_id(data.get("standard_id", ""))
    tr_url = str(data.get("tr_url", ""))
    criteria = data.get("normative_success_criteria", [])

    criterion_by_code = {}
    criterion_rows = []
    for item in criteria:
        code = str(item.get("code", "")).strip()
        if not code:
            continue
        row = {
            "standard_id": standard_id,
            "standard_url": tr_url,
            "criterion_id": str(item.get("id", "")).strip(),
            "criterion_code": code,
            "criterion_title": str(item.get("title", "")).strip(),
            "criterion_level": str(item.get("level", "")).strip(),
            "criterion_url": str(item.get("url", "")).strip(),
            "normative_text": str(item.get("normative_text", "")),
        }
        criterion_rows.append(row)
        criterion_by_code[code] = row

    return {
        "standard_id": standard_id,
        "standard_url": tr_url,
        "criteria": criterion_rows,
        "criteria_by_code": criterion_by_code,
    }


def detect_explicit_standard_mentions(text: str):
    mentions = set()
    if WCAG_RE.search(text):
        if "2.0" in text:
            mentions.add("wcag-2.0")
        elif "2.2" in text:
            mentions.add("wcag-2.2")
        else:
            mentions.add("wcag-2.0")
    if ATAG_RE.search(text):
        mentions.add("atag-2.0")
    if UAAG_RE.search(text):
        mentions.add("uaag-2.0")
    if ARIA_RE.search(text):
        mentions.add("wai-aria-1.2")
    return mentions


def excerpt(text: str, limit: int = 180):
    compact = " ".join(str(text).split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1] + "…"


def add_link(links: list[dict], link: dict):
    links.append(link)


def build_direct_normative_links(normative_indexes: dict[str, dict]):
    links = []
    seen = set()

    for source_standard_id, idx in normative_indexes.items():
        for row in idx["criteria"]:
            text = row["normative_text"]
            sc_refs = set(SC_REF_RE.findall(text))
            mentioned_standards = detect_explicit_standard_mentions(text)

            for mentioned in sorted(mentioned_standards):
                if mentioned == source_standard_id:
                    continue
                key = (
                    "direct_standard_reference",
                    source_standard_id,
                    row["criterion_code"],
                    mentioned,
                )
                if key in seen:
                    continue
                seen.add(key)
                add_link(
                    links,
                    {
                        "relation_type": "direct_standard_reference",
                        "basis": "direct",
                        "confidence": "high",
                        "source_kind": "normative_success_criterion",
                        "source_standard_id": source_standard_id,
                        "source_criterion_id": row["criterion_id"],
                        "source_criterion_code": row["criterion_code"],
                        "source_criterion_title": row["criterion_title"],
                        "source_url": row["criterion_url"],
                        "target_standard_id": mentioned,
                        "target_criterion_code": "",
                        "target_profile_ref": "",
                        "target_url": normative_indexes.get(mentioned, {}).get("standard_url", ""),
                        "evidence_excerpt": excerpt(text),
                        "source_dataset": "normative_text_pattern_match",
                    },
                )

            for ref_code in sorted(sc_refs):
                candidate_targets = [source_standard_id]
                if "wcag-2.0" in mentioned_standards:
                    candidate_targets = ["wcag-2.0"]
                elif "wcag-2.2" in mentioned_standards:
                    candidate_targets = ["wcag-2.2"]
                elif "atag-2.0" in mentioned_standards:
                    candidate_targets = ["atag-2.0"]
                elif "uaag-2.0" in mentioned_standards:
                    candidate_targets = ["uaag-2.0"]

                for target_standard in candidate_targets:
                    target_index = normative_indexes.get(target_standard, {}).get("criteria_by_code", {})
                    target_row = target_index.get(ref_code)
                    if not target_row:
                        continue
                    relation_type = "direct_sc_reference_cross_standard" if target_standard != source_standard_id else "direct_sc_reference_intra_standard"
                    key = (
                        relation_type,
                        source_standard_id,
                        row["criterion_code"],
                        target_standard,
                        ref_code,
                    )
                    if key in seen:
                        continue
                    seen.add(key)
                    add_link(
                        links,
                        {
                            "relation_type": relation_type,
                            "basis": "direct",
                            "confidence": "high",
                            "source_kind": "normative_success_criterion",
                            "source_standard_id": source_standard_id,
                            "source_criterion_id": row["criterion_id"],
                            "source_criterion_code": row["criterion_code"],
                            "source_criterion_title": row["criterion_title"],
                            "source_url": row["criterion_url"],
                            "target_standard_id": target_standard,
                            "target_criterion_code": ref_code,
                            "target_profile_ref": "",
                            "target_url": target_row.get("criterion_url", ""),
                            "evidence_excerpt": excerpt(text),
                            "source_dataset": "normative_text_pattern_match",
                        },
                    )

    return links


def build_inferred_crosswalk_links(crosswalk: dict, wcag_index: dict):
    links = []
    profiles = crosswalk.get("target_profiles", {})
    mappings = crosswalk.get("mappings", [])

    for mapping in mappings:
        source_code = str(mapping.get("atag_criterion_code", "")).strip()
        source_id = str(mapping.get("atag_criterion_id", "")).strip()
        source_title = str(mapping.get("atag_title", "")).strip()
        source_url = str(mapping.get("atag_url", "")).strip()

        for profile_ref in mapping.get("target_profile_refs", []):
            profile = profiles.get(profile_ref, {})
            for wcag_code in profile.get("criterion_codes", []):
                wcag_code = str(wcag_code).strip()
                target_row = wcag_index.get("criteria_by_code", {}).get(wcag_code, {})
                links.append(
                    {
                        "relation_type": "inferred_sc_reference_cross_standard",
                        "basis": "inferred_profile_mapping",
                        "confidence": "medium",
                        "source_kind": "normative_success_criterion",
                        "source_standard_id": "atag-2.0",
                        "source_criterion_id": source_id,
                        "source_criterion_code": source_code,
                        "source_criterion_title": source_title,
                        "source_url": source_url,
                        "target_standard_id": "wcag-2.2",
                        "target_criterion_code": wcag_code,
                        "target_profile_ref": str(profile_ref),
                        "target_url": str(target_row.get("criterion_url", "")),
                        "evidence_excerpt": f"ATAG crosswalk mapping via {profile_ref}",
                        "source_dataset": "atag-to-wcag-2.2-crosswalk.yaml",
                    }
                )

    return links


def build_informative_links(informative_data: dict, standard_url_map: dict):
    links = []
    for item in informative_data.get("resources", []):
        source_id = str(item.get("id", "")).strip()
        source_url = str(item.get("url", "")).strip()
        source_title = str(item.get("title", "")).strip()
        applies_to = item.get("applies_to", [])
        if not source_id or not isinstance(applies_to, list):
            continue

        for raw_target in applies_to:
            target_standard = normalize_standard_id(str(raw_target))
            links.append(
                {
                    "relation_type": "informative_resource_reference_standard",
                    "basis": "catalog_applies_to",
                    "confidence": "high",
                    "source_kind": "informative_resource",
                    "source_standard_id": "",
                    "source_criterion_id": "",
                    "source_criterion_code": "",
                    "source_criterion_title": source_title,
                    "source_resource_id": source_id,
                    "source_url": source_url,
                    "target_standard_id": target_standard,
                    "target_criterion_code": "",
                    "target_profile_ref": "",
                    "target_url": standard_url_map.get(target_standard, ""),
                    "evidence_excerpt": f"informative resource applies_to includes {raw_target}",
                    "source_dataset": "w3c-wai-informative-resources.yaml",
                }
            )

    return links


def dedupe_links(links: list[dict]):
    out = []
    seen = set()
    for link in links:
        key = (
            link.get("relation_type", ""),
            link.get("source_kind", ""),
            link.get("source_standard_id", ""),
            link.get("source_criterion_code", ""),
            link.get("source_resource_id", ""),
            link.get("target_standard_id", ""),
            link.get("target_criterion_code", ""),
            link.get("target_profile_ref", ""),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(link)
    return out


def write_csv(path: Path, links: list[dict]):
    fieldnames = [
        "link_id",
        "relation_type",
        "basis",
        "confidence",
        "source_kind",
        "source_standard_id",
        "source_criterion_id",
        "source_criterion_code",
        "source_criterion_title",
        "source_resource_id",
        "source_url",
        "target_standard_id",
        "target_criterion_code",
        "target_profile_ref",
        "target_url",
        "evidence_excerpt",
        "source_dataset",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(links)


def write_yaml(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate cross-standard references dataset (direct + inferred)")
    parser.add_argument("--wcag22-yaml", required=True)
    parser.add_argument("--wcag20-yaml", required=True)
    parser.add_argument("--atag-yaml", required=True)
    parser.add_argument("--uaag-yaml", required=True)
    parser.add_argument("--crosswalk-yaml", required=True)
    parser.add_argument("--informative-yaml", required=True)
    parser.add_argument("--out-yaml", required=True)
    parser.add_argument("--out-csv", required=True)
    args = parser.parse_args()

    wcag22 = build_normative_index(load_yaml(Path(args.wcag22_yaml)))
    wcag20 = build_normative_index(load_yaml(Path(args.wcag20_yaml)))
    atag = build_normative_index(load_yaml(Path(args.atag_yaml)))
    uaag = build_normative_index(load_yaml(Path(args.uaag_yaml)))
    crosswalk = load_yaml(Path(args.crosswalk_yaml))
    informative = load_yaml(Path(args.informative_yaml))

    normative_indexes = {
        wcag22["standard_id"]: wcag22,
        wcag20["standard_id"]: wcag20,
        atag["standard_id"]: atag,
        uaag["standard_id"]: uaag,
    }

    standard_url_map = {
        "wcag-2.2": wcag22["standard_url"],
        "wcag-2.0": wcag20["standard_url"],
        "atag-2.0": atag["standard_url"],
        "uaag-2.0": uaag["standard_url"],
        "wai-aria-1.2": "https://www.w3.org/TR/wai-aria-1.2/",
    }

    links = []
    links.extend(build_direct_normative_links(normative_indexes))
    links.extend(build_inferred_crosswalk_links(crosswalk, wcag22))
    links.extend(build_informative_links(informative, standard_url_map))

    links = dedupe_links(links)

    for idx, item in enumerate(links, start=1):
        item["link_id"] = f"xref-{idx:05d}"
        if "source_resource_id" not in item:
            item["source_resource_id"] = ""

    payload = {
        "dataset_id": "cross-standard-references",
        "updated": datetime.now(timezone.utc).date().isoformat(),
        "description": "Direct and inferred references between standards criteria and informative resources.",
        "relation_types": [
            {
                "id": "direct_sc_reference_cross_standard",
                "description": "A normative success criterion explicitly references a success criterion in another standard.",
            },
            {
                "id": "direct_sc_reference_intra_standard",
                "description": "A normative success criterion explicitly references another criterion in the same standard.",
            },
            {
                "id": "direct_standard_reference",
                "description": "A normative success criterion explicitly references another standard without a specific criterion code.",
            },
            {
                "id": "inferred_sc_reference_cross_standard",
                "description": "A cross-standard SC reference inferred through profile mapping (not an explicit inline citation).",
            },
            {
                "id": "informative_resource_reference_standard",
                "description": "An informative resource links to or applies to another standard.",
            },
        ],
        "source_inputs": {
            "wcag_22_normative": args.wcag22_yaml,
            "wcag_20_normative": args.wcag20_yaml,
            "atag_20_normative": args.atag_yaml,
            "uaag_20_normative": args.uaag_yaml,
            "atag_wcag_crosswalk": args.crosswalk_yaml,
            "informative_catalog": args.informative_yaml,
        },
        "links": links,
    }

    write_yaml(Path(args.out_yaml), payload)
    write_csv(Path(args.out_csv), links)

    print(f"links={len(links)}")
    by_type = {}
    for item in links:
        by_type[item["relation_type"]] = by_type.get(item["relation_type"], 0) + 1
    for key in sorted(by_type):
        print(f"{key}={by_type[key]}")
    print(f"yaml={args.out_yaml}")
    print(f"csv={args.out_csv}")


if __name__ == "__main__":
    main()
