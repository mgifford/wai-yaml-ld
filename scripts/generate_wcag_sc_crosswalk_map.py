#!/usr/bin/env python3
import argparse
import csv
import re
from pathlib import Path

import yaml


def load_yaml(path: Path):
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def safe_label(text: str):
    return str(text).replace('"', "'")


def mermaid_alias(raw: str):
    alias = "n_" + re.sub(r"[^a-zA-Z0-9_]", "_", raw)
    alias = re.sub(r"_+", "_", alias).strip("_")
    return alias or "n"


def build_sc_index(wcag_data):
    out = {}
    for item in wcag_data.get("normative_success_criteria", []):
        code = str(item.get("code", "")).strip()
        if not code:
            continue
        out[code] = {
            "title": item.get("title", ""),
            "level": item.get("level", ""),
            "url": item.get("url", "")
        }
    return out


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fp:
        writer = csv.DictWriter(
            fp,
            fieldnames=[
                "atag_criterion_code",
                "atag_criterion_id",
                "target_profile",
                "wcag_sc_code",
                "wcag_sc_title",
                "wcag_sc_level",
                "mapping_basis"
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Generate WCAG SC granular map from ATAG crosswalk profiles")
    parser.add_argument("--crosswalk-yaml", required=True)
    parser.add_argument("--wcag-yaml", required=True)
    parser.add_argument("--mmd-out", required=True)
    parser.add_argument("--csv-out", required=True)
    args = parser.parse_args()

    crosswalk = load_yaml(Path(args.crosswalk_yaml))
    wcag = load_yaml(Path(args.wcag_yaml))
    sc_index = build_sc_index(wcag)

    profiles = crosswalk.get("target_profiles", {})
    mappings = crosswalk.get("mappings", [])

    rows = []
    lines = ["graph LR"]

    root = mermaid_alias("wcag-2.2-root")
    lines.append(f'    {root}["WCAG 2.2 Success Criteria"]')

    profile_alias = {}
    for profile_id, profile_data in profiles.items():
        alias = mermaid_alias(f"profile-{profile_id}")
        profile_alias[profile_id] = alias
        description = profile_data.get("description", profile_id)
        lines.append(f'    {alias}["{safe_label(description)}"]')
        lines.append(f"    {alias} -->|targets| {root}")

    sc_alias = {}
    seen_sc = set()
    for profile_id, profile_data in profiles.items():
        p_alias = profile_alias[profile_id]
        for sc_code in profile_data.get("criterion_codes", []):
            sc_code = str(sc_code)
            if sc_code not in sc_alias:
                alias = mermaid_alias(f"sc-{sc_code}")
                meta = sc_index.get(sc_code, {})
                title = meta.get("title", "")
                level = meta.get("level", "")
                label = f"SC {sc_code}"
                if title:
                    label += f": {title}"
                if level:
                    label += f" ({level})"
                sc_alias[sc_code] = alias
                lines.append(f'    {alias}["{safe_label(label)}"]')
            edge_key = (profile_id, sc_code)
            if edge_key not in seen_sc:
                lines.append(f"    {p_alias} -->|includes_sc| {sc_alias[sc_code]}")
                seen_sc.add(edge_key)

    seen_criterion_profile = set()
    for item in mappings:
        crit_code = str(item.get("atag_criterion_code", "")).strip()
        crit_id = str(item.get("atag_criterion_id", "")).strip()
        crit_title = str(item.get("atag_title", "")).strip()
        if not crit_code:
            continue
        crit_node = mermaid_alias(f"atag-{crit_code}")
        lines.append(f'    {crit_node}["{safe_label(f"ATAG {crit_code}: {crit_title}")}"]')
        for profile_id in item.get("target_profile_refs", []):
            if profile_id not in profile_alias:
                continue
            rel_key = (crit_code, profile_id)
            if rel_key in seen_criterion_profile:
                continue
            seen_criterion_profile.add(rel_key)
            lines.append(f"    {crit_node} -->|maps_to_profile| {profile_alias[profile_id]}")

            profile_codes = profiles.get(profile_id, {}).get("criterion_codes", [])
            for sc_code in profile_codes:
                meta = sc_index.get(str(sc_code), {})
                rows.append(
                    {
                        "atag_criterion_code": crit_code,
                        "atag_criterion_id": crit_id,
                        "target_profile": profile_id,
                        "wcag_sc_code": str(sc_code),
                        "wcag_sc_title": meta.get("title", ""),
                        "wcag_sc_level": meta.get("level", ""),
                        "mapping_basis": "atag_crosswalk_profile_membership"
                    }
                )

    mmd_path = Path(args.mmd_out)
    mmd_path.parent.mkdir(parents=True, exist_ok=True)
    mmd_path.write_text("\n".join(lines) + "\n")

    write_csv(Path(args.csv_out), rows)

    print(f"profiles={len(profiles)} criteria={len(mappings)} sc_nodes={len(sc_alias)}")
    print(f"mmd={args.mmd_out}")
    print(f"csv={args.csv_out}")


if __name__ == "__main__":
    main()