#!/usr/bin/env python3
import argparse
import csv
import itertools
import re
from pathlib import Path

import yaml


STOPWORDS = {
    "and", "the", "with", "from", "into", "must", "has", "have", "for", "are",
    "not", "that", "this", "using", "within", "without", "over", "under", "each",
    "every", "ensure", "element", "elements", "attribute", "attributes", "aria",
    "html", "page", "rule", "rules", "style", "code", "accessible", "name"
}


def load_catalog(path: Path):
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict) or "rule_sets" not in data:
        raise ValueError("catalog must contain rule_sets")
    return data


def tokenize(text: str):
    normalized = re.sub(r"[^a-z0-9]+", " ", str(text or "").lower())
    return {tok for tok in normalized.split() if len(tok) >= 3 and tok not in STOPWORDS and not tok.isdigit()}


def score_rules(left, right):
    left_tokens = tokenize(left.get("title") or left.get("id"))
    right_tokens = tokenize(right.get("title") or right.get("id"))
    if not left_tokens or not right_tokens:
        return 0.0, []

    shared = sorted(left_tokens & right_tokens)
    if len(shared) < 2:
        return 0.0, shared

    union = left_tokens | right_tokens
    score = len(shared) / len(union)
    return round(score, 4), shared


def build_rows(catalog):
    rows = []
    rule_sets = catalog.get("rule_sets", [])

    for left_set, right_set in itertools.combinations(rule_sets, 2):
        left_provider = left_set.get("provider", left_set.get("id", ""))
        right_provider = right_set.get("provider", right_set.get("id", ""))

        for left_rule in left_set.get("rules", []):
            for right_rule in right_set.get("rules", []):
                score, shared = score_rules(left_rule, right_rule)
                if score < 0.34:
                    continue

                rows.append(
                    {
                        "left_provider": left_provider,
                        "left_rule_set": left_set.get("id", ""),
                        "left_rule_id": left_rule.get("id", ""),
                        "left_rule_title": left_rule.get("title", ""),
                        "left_rule_url": left_rule.get("url", ""),
                        "right_provider": right_provider,
                        "right_rule_set": right_set.get("id", ""),
                        "right_rule_id": right_rule.get("id", ""),
                        "right_rule_title": right_rule.get("title", ""),
                        "right_rule_url": right_rule.get("url", ""),
                        "score": score,
                        "shared_tokens": "|".join(shared),
                    }
                )

    rows.sort(key=lambda item: (-float(item["score"]), item["left_rule_id"], item["right_rule_id"]))
    return rows


def write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "left_provider",
        "left_rule_set",
        "left_rule_id",
        "left_rule_title",
        "left_rule_url",
        "right_provider",
        "right_rule_set",
        "right_rule_id",
        "right_rule_title",
        "right_rule_url",
        "score",
        "shared_tokens",
    ]
    with path.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Generate cross-source accessibility rule comparison CSV")
    parser.add_argument(
        "--catalog-yaml",
        default="kitty-specs/001-wai-standards-yaml-ld-ingestion/research/accessibility-rule-catalogs.yaml",
    )
    parser.add_argument(
        "--csv-out",
        default="kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/accessibility-rule-catalogs.comparison.csv",
    )
    args = parser.parse_args()

    catalog = load_catalog(Path(args.catalog_yaml))
    rows = build_rows(catalog)
    write_csv(Path(args.csv_out), rows)

    print(f"comparisons={len(rows)}")
    print(f"out={args.csv_out}")


if __name__ == "__main__":
    main()
