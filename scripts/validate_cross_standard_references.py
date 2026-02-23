#!/usr/bin/env python3
import argparse
from pathlib import Path

import yaml


def load_yaml(path: Path):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def norm_standard(raw: str) -> str:
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


def criterion_index(normative_data: dict):
    out = set()
    for item in normative_data.get("normative_success_criteria", []):
        code = str(item.get("code", "")).strip()
        if code:
            out.add(code)
    return out


def informative_applies_to_index(informative_data: dict):
    out = {}
    for item in informative_data.get("resources", []):
        resource_id = str(item.get("id", "")).strip()
        targets = set()
        for target in item.get("applies_to", []):
            targets.add(norm_standard(str(target)))
        if resource_id:
            out[resource_id] = targets
    return out


def validate_links(links_data: dict, crit_index: dict, profile_membership: dict, informative_targets: dict):
    failures = []
    links = links_data.get("links", [])
    if not isinstance(links, list):
        return ["links must be a list"]

    for link in links:
        link_id = str(link.get("link_id", "<missing>"))
        relation = str(link.get("relation_type", ""))
        basis = str(link.get("basis", ""))

        source_standard = norm_standard(str(link.get("source_standard_id", "")))
        target_standard = norm_standard(str(link.get("target_standard_id", "")))
        source_sc = str(link.get("source_criterion_code", "")).strip()
        target_sc = str(link.get("target_criterion_code", "")).strip()
        profile_ref = str(link.get("target_profile_ref", "")).strip()

        if relation == "direct_sc_reference_cross_standard":
            if basis != "direct":
                failures.append(f"{link_id}: direct_sc_reference_cross_standard must have basis=direct")
            if source_standard == target_standard:
                failures.append(f"{link_id}: direct_sc_reference_cross_standard must be cross-standard")
            if not source_sc or source_sc not in crit_index.get(source_standard, set()):
                failures.append(f"{link_id}: missing/unknown source criterion code '{source_sc}' for {source_standard}")
            if not target_sc or target_sc not in crit_index.get(target_standard, set()):
                failures.append(f"{link_id}: missing/unknown target criterion code '{target_sc}' for {target_standard}")

        elif relation == "direct_sc_reference_intra_standard":
            if basis != "direct":
                failures.append(f"{link_id}: direct_sc_reference_intra_standard must have basis=direct")
            if source_standard != target_standard:
                failures.append(f"{link_id}: intra-standard relation must have same source/target standard")
            if not source_sc or source_sc not in crit_index.get(source_standard, set()):
                failures.append(f"{link_id}: unknown source criterion code '{source_sc}' for {source_standard}")
            if not target_sc or target_sc not in crit_index.get(target_standard, set()):
                failures.append(f"{link_id}: unknown target criterion code '{target_sc}' for {target_standard}")

        elif relation == "direct_standard_reference":
            if basis != "direct":
                failures.append(f"{link_id}: direct_standard_reference must have basis=direct")
            if target_sc:
                failures.append(f"{link_id}: direct_standard_reference must not carry target_criterion_code")

        elif relation == "inferred_sc_reference_cross_standard":
            if basis != "inferred_profile_mapping":
                failures.append(f"{link_id}: inferred relation must have basis=inferred_profile_mapping")
            if source_standard != "atag-2.0" or target_standard != "wcag-2.2":
                failures.append(f"{link_id}: inferred mapping currently only supports atag-2.0 -> wcag-2.2")
            if not profile_ref:
                failures.append(f"{link_id}: inferred relation requires target_profile_ref")
                continue
            expected = profile_membership.get(profile_ref)
            if expected is None:
                failures.append(f"{link_id}: unknown profile ref '{profile_ref}'")
                continue
            if target_sc not in expected:
                failures.append(f"{link_id}: target SC '{target_sc}' not in profile '{profile_ref}'")

        elif relation == "informative_resource_reference_standard":
            if basis != "catalog_applies_to":
                failures.append(f"{link_id}: informative relation must have basis=catalog_applies_to")
            resource_id = str(link.get("source_resource_id", "")).strip()
            if not resource_id:
                failures.append(f"{link_id}: informative relation missing source_resource_id")
                continue
            allowed = informative_targets.get(resource_id)
            if allowed is None:
                failures.append(f"{link_id}: source_resource_id '{resource_id}' not found in informative catalog")
                continue
            if target_standard not in allowed:
                failures.append(f"{link_id}: target_standard_id '{target_standard}' not declared in applies_to for '{resource_id}'")

        else:
            failures.append(f"{link_id}: unsupported relation_type '{relation}'")

    return failures


def main():
    parser = argparse.ArgumentParser(description="Validate cross-standard references dataset integrity")
    parser.add_argument("--dataset-yaml", required=True)
    parser.add_argument("--wcag22-yaml", required=True)
    parser.add_argument("--wcag20-yaml", required=True)
    parser.add_argument("--atag-yaml", required=True)
    parser.add_argument("--uaag-yaml", required=True)
    parser.add_argument("--crosswalk-yaml", required=True)
    parser.add_argument("--informative-yaml", required=True)
    args = parser.parse_args()

    dataset = load_yaml(Path(args.dataset_yaml))
    wcag22 = load_yaml(Path(args.wcag22_yaml))
    wcag20 = load_yaml(Path(args.wcag20_yaml))
    atag = load_yaml(Path(args.atag_yaml))
    uaag = load_yaml(Path(args.uaag_yaml))
    crosswalk = load_yaml(Path(args.crosswalk_yaml))
    informative = load_yaml(Path(args.informative_yaml))

    crit_index = {
        "wcag-2.2": criterion_index(wcag22),
        "wcag-2.0": criterion_index(wcag20),
        "atag-2.0": criterion_index(atag),
        "uaag-2.0": criterion_index(uaag),
    }

    profiles = crosswalk.get("target_profiles", {})
    profile_membership = {
        str(profile_id): {str(code) for code in profile_data.get("criterion_codes", [])}
        for profile_id, profile_data in profiles.items()
    }

    informative_targets = informative_applies_to_index(informative)

    failures = validate_links(dataset, crit_index, profile_membership, informative_targets)

    if failures:
        for item in failures:
            print(f"FAIL: {item}")
        raise SystemExit(2)

    print("ok: cross-standard references integrity checks passed")


if __name__ == "__main__":
    main()
