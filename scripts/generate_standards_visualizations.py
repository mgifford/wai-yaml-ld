#!/usr/bin/env python3
import argparse
import csv
import re
from collections import defaultdict, deque
from pathlib import Path

import yaml


def load_yaml(path: Path):
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return data


def write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def safe_label(text: str):
    return str(text).replace('"', "'")


def build_mermaid_id_map(node_ids):
    mapping = {}
    used = set()
    for node_id in node_ids:
        base = "n_" + re.sub(r"[^a-zA-Z0-9_]", "_", str(node_id))
        base = re.sub(r"_+", "_", base).strip("_") or "n"
        candidate = base
        suffix = 2
        while candidate in used:
            candidate = f"{base}_{suffix}"
            suffix += 1
        mapping[node_id] = candidate
        used.add(candidate)
    return mapping


def build_relation_view(graph):
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    mermaid_ids = build_mermaid_id_map([node.get("id", "") for node in nodes])

    lines = ["graph LR"]
    for node in nodes:
        node_id = node.get("id", "")
        lines.append(f'    {mermaid_ids.get(node_id, node_id)}["{safe_label(node.get("label", node_id))}"]')

    grouped = defaultdict(list)
    for edge in edges:
        grouped[edge.get("relation", "unknown")].append(edge)

    for relation in sorted(grouped.keys()):
        lines.append(f"    %% relation: {relation}")
        for edge in grouped[relation]:
            source = mermaid_ids.get(edge["from"], edge["from"])
            target = mermaid_ids.get(edge["to"], edge["to"])
            lines.append(f'    {source} -->|{safe_label(relation)}| {target}')

    return "\n".join(lines) + "\n"


def build_wcag_view(graph, anchor="wcag-2.2", max_depth=2):
    nodes = {node["id"]: node for node in graph.get("nodes", [])}
    edges = graph.get("edges", [])
    mermaid_ids = build_mermaid_id_map(list(nodes.keys()))

    adjacency = defaultdict(list)
    reverse = defaultdict(list)
    for edge in edges:
        adjacency[edge["from"]].append(edge)
        reverse[edge["to"]].append(edge)

    visited = {anchor}
    queue = deque([(anchor, 0)])
    kept_edges = []

    while queue:
        current, depth = queue.popleft()
        if depth >= max_depth:
            continue

        for edge in adjacency.get(current, []):
            kept_edges.append(edge)
            nxt = edge["to"]
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, depth + 1))

        for edge in reverse.get(current, []):
            kept_edges.append(edge)
            nxt = edge["from"]
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, depth + 1))

    dedup = {}
    for edge in kept_edges:
        dedup[edge["id"]] = edge
    kept_edges = [dedup[key] for key in sorted(dedup.keys())]

    lines = ["graph LR"]
    for node_id in sorted(visited):
        node = nodes.get(node_id, {"label": node_id})
        lines.append(f'    {mermaid_ids.get(node_id, node_id)}["{safe_label(node.get("label", node_id))}"]')
    for edge in kept_edges:
        source = mermaid_ids.get(edge["from"], edge["from"])
        target = mermaid_ids.get(edge["to"], edge["to"])
        lines.append(f'    {source} -->|{safe_label(edge.get("relation", ""))}| {target}')

    return "\n".join(lines) + "\n"


def build_parts_view(html_data, css_data):
    lines = ["graph LR"]

    lines.append('    html_living_standard["HTML Living Standard"]')
    lines.append('    css_overview["W3C CSS Specifications Overview"]')
    lines.append('    wcag_22["WCAG 2.2"]')

    html_parent_url = html_data.get("canonical_url", "")
    css_parent_url = css_data.get("overview_url", "")
    wcag_url = ""
    for guidance in css_data.get("related_accessibility_guidance", []):
        if guidance.get("id") == "wcag-2.2":
            wcag_url = guidance.get("url", "")
            break

    edges_rows = []

    for section in html_data.get("accessibility_related_sections", []):
        section_id = f'html_{section.get("id", "section")}'.replace("-", "_")
        title = section.get("title", section.get("id", "HTML section"))
        lines.append(f'    {section_id}["{safe_label(title)}"]')
        lines.append(f"    {section_id} -->|part_of| html_living_standard")
        lines.append(f"    {section_id} -->|supports_outcome_for| wcag_22")
        edges_rows.append((
            section.get("id", ""),
            section.get("url", ""),
            "part_of",
            "html-living-standard",
            html_parent_url,
            "html-accessibility-related-section"
        ))
        edges_rows.append((
            section.get("id", ""),
            section.get("url", ""),
            "supports_outcome_for",
            "wcag-2.2",
            wcag_url,
            "html-accessibility-related-section"
        ))

    for module in css_data.get("accessibility_relevant_modules", []):
        module_id = f'css_{module.get("id", "module")}'.replace("-", "_").replace(".", "_")
        title = module.get("title", module.get("id", "CSS module"))
        lines.append(f'    {module_id}["{safe_label(title)}"]')
        lines.append(f"    {module_id} -->|part_of| css_overview")
        lines.append(f"    {module_id} -->|supports_outcome_for| wcag_22")
        edges_rows.append((
            module.get("id", ""),
            module.get("url", ""),
            "part_of",
            "w3c-css-overview",
            css_parent_url,
            "css-accessibility-relevant-module"
        ))
        edges_rows.append((
            module.get("id", ""),
            module.get("url", ""),
            "supports_outcome_for",
            "wcag-2.2",
            wcag_url,
            "css-accessibility-relevant-module"
        ))

    return "\n".join(lines) + "\n", edges_rows


def write_parts_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(["part_id", "part_url", "relation", "target", "target_url", "part_type"])
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Generate visualization views for standards graph and part-level links")
    parser.add_argument("--graph-yaml", required=True)
    parser.add_argument("--html-yaml", required=True)
    parser.add_argument("--css-yaml", required=True)
    parser.add_argument("--by-relation-out", required=True)
    parser.add_argument("--wcag-out", required=True)
    parser.add_argument("--parts-out", required=True)
    parser.add_argument("--parts-csv-out", required=True)
    args = parser.parse_args()

    graph = load_yaml(Path(args.graph_yaml))
    html_data = load_yaml(Path(args.html_yaml))
    css_data = load_yaml(Path(args.css_yaml))

    relation_view = build_relation_view(graph)
    wcag_view = build_wcag_view(graph)
    parts_view, part_rows = build_parts_view(html_data, css_data)

    write_text(Path(args.by_relation_out), relation_view)
    write_text(Path(args.wcag_out), wcag_view)
    write_text(Path(args.parts_out), parts_view)
    write_parts_csv(Path(args.parts_csv_out), part_rows)

    print(f"relation_view={args.by_relation_out}")
    print(f"wcag_view={args.wcag_out}")
    print(f"parts_view={args.parts_out}")
    print(f"parts_csv={args.parts_csv_out}")


if __name__ == "__main__":
    main()