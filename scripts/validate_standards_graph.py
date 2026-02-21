#!/usr/bin/env python3
import argparse
from datetime import date, datetime, timezone
from pathlib import Path

import yaml


def parse_iso_date(value: str):
    try:
        return date.fromisoformat(value)
    except Exception as exc:
        raise ValueError(f"invalid ISO date '{value}'") from exc


def load_yaml(path: Path):
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def validate_edge_references(graph):
    node_ids = {node.get("id") for node in graph.get("nodes", [])}
    failures = []

    for edge in graph.get("edges", []):
        edge_id = edge.get("id", "<missing>")
        src = edge.get("from")
        dst = edge.get("to")
        if src not in node_ids:
            failures.append(f"edge '{edge_id}' has unknown from node '{src}'")
        if dst not in node_ids:
            failures.append(f"edge '{edge_id}' has unknown to node '{dst}'")

    return failures


def validate_staleness(path: Path, field: str, max_age_days: int):
    data = load_yaml(path)
    if field not in data:
        return [f"{path}: missing required staleness field '{field}'"]

    extracted = parse_iso_date(str(data[field]))
    age_days = (datetime.now(timezone.utc).date() - extracted).days
    if age_days > max_age_days:
        return [f"{path}: field '{field}' is stale ({age_days} days > {max_age_days} days)"]
    return []


def main():
    parser = argparse.ArgumentParser(description="Validate standards link graph integrity and extraction-date freshness")
    parser.add_argument("--graph-yaml", required=True, help="Path to standards-link-graph.yaml")
    parser.add_argument(
        "--stale-threshold-days",
        type=int,
        default=90,
        help="Maximum allowed age in days for extraction date fields"
    )
    parser.add_argument(
        "--check-file",
        action="append",
        default=[],
        help="File/field pair for staleness check in format <path>:<field>"
    )
    args = parser.parse_args()

    failures = []

    graph = load_yaml(Path(args.graph_yaml))
    failures.extend(validate_edge_references(graph))

    for spec in args.check_file:
        if ":" not in spec:
            failures.append(f"invalid --check-file value '{spec}', expected <path>:<field>")
            continue
        path_str, field = spec.split(":", 1)
        failures.extend(validate_staleness(Path(path_str), field, args.stale_threshold_days))

    if failures:
        for item in failures:
            print(f"FAIL: {item}")
        raise SystemExit(2)

    print("ok: graph references valid and extraction dates within threshold")


if __name__ == "__main__":
    main()