#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path

import yaml


def load_links(path: Path):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("links"), list):
        raise ValueError(f"{path} must contain a YAML object with a 'links' list")
    return data.get("links", [])


def matches(value: str, expected: str) -> bool:
    return str(value).strip() == str(expected).strip()


def filter_links(
    links,
    source_standard: str,
    source_sc: str,
    target_standard: str,
    target_sc: str,
    relation_types: list[str],
    basis: str,
    include_intra: bool,
):
    out = []
    for item in links:
        if source_standard and not matches(item.get("source_standard_id", ""), source_standard):
            continue
        if source_sc and not matches(item.get("source_criterion_code", ""), source_sc):
            continue
        if target_standard and not matches(item.get("target_standard_id", ""), target_standard):
            continue
        if target_sc and not matches(item.get("target_criterion_code", ""), target_sc):
            continue
        if relation_types and str(item.get("relation_type", "")) not in relation_types:
            continue
        if basis and not matches(item.get("basis", ""), basis):
            continue
        if not include_intra and str(item.get("relation_type", "")) == "direct_sc_reference_intra_standard":
            continue
        out.append(item)
    return out


def print_table(links, limit: int):
    rows = links[:limit] if limit > 0 else links
    if not rows:
        print("no matches")
        return
    header = [
        "link_id",
        "relation_type",
        "basis",
        "source_standard_id",
        "source_criterion_code",
        "source_resource_id",
        "target_standard_id",
        "target_criterion_code",
        "target_profile_ref",
    ]
    print("\t".join(header))
    for item in rows:
        print(
            "\t".join(
                [
                    str(item.get("link_id", "")),
                    str(item.get("relation_type", "")),
                    str(item.get("basis", "")),
                    str(item.get("source_standard_id", "")),
                    str(item.get("source_criterion_code", "")),
                    str(item.get("source_resource_id", "")),
                    str(item.get("target_standard_id", "")),
                    str(item.get("target_criterion_code", "")),
                    str(item.get("target_profile_ref", "")),
                ]
            )
        )


def print_json(links, limit: int):
    rows = links[:limit] if limit > 0 else links
    print(json.dumps(rows, indent=2, ensure_ascii=False))


def write_csv(path: Path, links, limit: int):
    rows = links[:limit] if limit > 0 else links
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
        writer.writerows(rows)
    print(str(path))


def main():
    parser = argparse.ArgumentParser(description="Query cross-standard reference links")
    parser.add_argument("--dataset-yaml", required=True)
    parser.add_argument("--source-standard", default="")
    parser.add_argument("--source-sc", default="")
    parser.add_argument("--target-standard", default="")
    parser.add_argument("--target-sc", default="")
    parser.add_argument("--relation-type", action="append", default=[])
    parser.add_argument("--basis", default="")
    parser.add_argument("--include-intra-standard", action="store_true")
    parser.add_argument("--format", choices=["table", "json", "csv"], default="table")
    parser.add_argument("--out-csv", default="")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    links = load_links(Path(args.dataset_yaml))
    filtered = filter_links(
        links,
        source_standard=args.source_standard,
        source_sc=args.source_sc,
        target_standard=args.target_standard,
        target_sc=args.target_sc,
        relation_types=args.relation_type,
        basis=args.basis,
        include_intra=args.include_intra_standard,
    )

    print(f"matches={len(filtered)}")

    if args.format == "table":
        print_table(filtered, args.limit)
    elif args.format == "json":
        print_json(filtered, args.limit)
    else:
        out_csv = args.out_csv or "monitoring/cross-standard-reference-query.csv"
        write_csv(Path(out_csv), filtered, args.limit)


if __name__ == "__main__":
    main()
