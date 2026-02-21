#!/usr/bin/env python3
import argparse
import csv
import json
from pathlib import Path

import yaml


def load_graph(path: Path):
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ValueError("graph must be a YAML object")
    if "nodes" not in data or "edges" not in data:
        raise ValueError("graph must contain 'nodes' and 'edges'")
    return data


def validate_references(graph):
    node_ids = {node.get("id") for node in graph.get("nodes", [])}
    missing = []
    for edge in graph.get("edges", []):
        if edge.get("from") not in node_ids:
            missing.append((edge.get("id"), "from", edge.get("from")))
        if edge.get("to") not in node_ids:
            missing.append((edge.get("id"), "to", edge.get("to")))
    if missing:
        details = ", ".join(f"{eid}:{side}={node}" for eid, side, node in missing)
        raise ValueError(f"edge references unknown node(s): {details}")


def build_jsonld(graph):
    jsonld = {
        "@context": {
            "id": "@id",
            "type": "@type",
            "label": "http://www.w3.org/2000/01/rdf-schema#label",
            "url": {"@id": "http://schema.org/url", "@type": "@id"},
            "kind": "http://schema.org/additionalType",
            "relation": "http://schema.org/relationship",
            "from": {"@id": "http://schema.org/fromLocation", "@type": "@id"},
            "to": {"@id": "http://schema.org/toLocation", "@type": "@id"},
            "confidence": "http://schema.org/confidence",
            "evidence": "http://schema.org/description"
        },
        "id": f"urn:graph:{graph.get('graph_id', 'wai-standards-link-graph')}",
        "type": "Dataset",
        "label": graph.get("name"),
        "graph_id": graph.get("graph_id"),
        "updated": graph.get("updated"),
        "@graph": []
    }

    for node in graph.get("nodes", []):
        jsonld["@graph"].append(
            {
                "id": f"urn:node:{node.get('id')}",
                "type": "Thing",
                "label": node.get("label"),
                "kind": node.get("kind"),
                "url": node.get("url")
            }
        )

    for edge in graph.get("edges", []):
        jsonld["@graph"].append(
            {
                "id": f"urn:edge:{edge.get('id')}",
                "type": "Relationship",
                "from": f"urn:node:{edge.get('from')}",
                "to": f"urn:node:{edge.get('to')}",
                "relation": edge.get("relation"),
                "confidence": edge.get("confidence"),
                "evidence": edge.get("evidence")
            }
        )

    return jsonld


def write_csv(path: Path, edges):
    fields = ["edge_id", "from", "relation", "to", "confidence", "evidence"]
    with path.open("w", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=fields)
        writer.writeheader()
        for edge in edges:
            writer.writerow(
                {
                    "edge_id": edge.get("id", ""),
                    "from": edge.get("from", ""),
                    "relation": edge.get("relation", ""),
                    "to": edge.get("to", ""),
                    "confidence": edge.get("confidence", ""),
                    "evidence": edge.get("evidence", "")
                }
            )


def main():
    parser = argparse.ArgumentParser(description="Generate JSON-LD and CSV artifacts from standards link graph YAML")
    parser.add_argument("--graph-yaml", required=True, help="Path to standards-link-graph.yaml")
    parser.add_argument("--jsonld-out", required=True, help="Path to output JSON-LD file")
    parser.add_argument("--csv-out", required=True, help="Path to output CSV edge file")
    args = parser.parse_args()

    graph_path = Path(args.graph_yaml)
    jsonld_path = Path(args.jsonld_out)
    csv_path = Path(args.csv_out)

    graph = load_graph(graph_path)
    validate_references(graph)

    jsonld_path.parent.mkdir(parents=True, exist_ok=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    jsonld = build_jsonld(graph)
    jsonld_path.write_text(json.dumps(jsonld, indent=2) + "\n")
    write_csv(csv_path, graph.get("edges", []))

    print(f"nodes={len(graph.get('nodes', []))} edges={len(graph.get('edges', []))}")
    print(f"jsonld={jsonld_path}")
    print(f"csv={csv_path}")


if __name__ == "__main__":
    main()