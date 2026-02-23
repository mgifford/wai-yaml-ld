#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

import yaml


def load_yaml(path: Path):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML object")
    links = data.get("links", [])
    if not isinstance(links, list):
        raise ValueError(f"{path} must contain a 'links' list")
    return links


def alias(raw: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_]", "_", raw)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "node"


def s(value: str) -> str:
    return str(value).replace('"', "'")


def should_include(link: dict, mode: str) -> bool:
    rel = str(link.get("relation_type", ""))
    if mode == "all":
        return True
    if mode == "atag-wcag":
        return (
            str(link.get("source_standard_id", "")) == "atag-2.0"
            and str(link.get("target_standard_id", "")) == "wcag-2.2"
            and rel == "inferred_sc_reference_cross_standard"
        )
    if mode == "informative":
        return rel == "informative_resource_reference_standard"
    raise ValueError(f"unknown mode: {mode}")


def link_label(link: dict, mode: str) -> str:
    rel = str(link.get("relation_type", ""))
    if mode == "atag-wcag":
        code = str(link.get("target_criterion_code", ""))
        profile = str(link.get("target_profile_ref", ""))
        if profile:
            return f"{code} ({profile})"
        return code or rel
    if mode == "informative":
        return str(link.get("basis", "")) or rel
    return rel


def source_node(link: dict) -> tuple[str, str]:
    source_kind = str(link.get("source_kind", ""))
    if source_kind == "informative_resource":
        resource_id = str(link.get("source_resource_id", ""))
        title = str(link.get("source_criterion_title", ""))
        nid = f"res_{alias(resource_id)}"
        label = f"resource:{resource_id}"
        if title:
            label += f" {title}"
        return nid, label

    standard = str(link.get("source_standard_id", ""))
    code = str(link.get("source_criterion_code", ""))
    title = str(link.get("source_criterion_title", ""))
    nid = f"sc_{alias(standard)}_{alias(code)}"
    label = f"{standard} SC {code}"
    if title:
        label += f": {title}"
    return nid, label


def target_node(link: dict) -> tuple[str, str]:
    standard = str(link.get("target_standard_id", ""))
    target_sc = str(link.get("target_criterion_code", ""))
    if target_sc:
        nid = f"sc_{alias(standard)}_{alias(target_sc)}"
        label = f"{standard} SC {target_sc}"
        return nid, label
    nid = f"std_{alias(standard)}"
    label = standard
    return nid, label


def build_mermaid(links: list[dict], mode: str, max_edges: int) -> str:
    lines = ["graph LR"]
    node_defs = {}
    edge_count = 0

    for link in links:
        if not should_include(link, mode):
            continue
        if max_edges > 0 and edge_count >= max_edges:
            break

        src_id, src_label = source_node(link)
        dst_id, dst_label = target_node(link)
        node_defs[src_id] = src_label
        node_defs[dst_id] = dst_label

        label = link_label(link, mode)
        lines.append(f'    {src_id}["{s(src_label)}"] -->|{s(label)}| {dst_id}["{s(dst_label)}"]')
        edge_count += 1

    if edge_count == 0:
        lines.append('    empty["No matching links"]')

    return "\n".join(lines) + "\n"


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate Mermaid views for cross-standard references")
    parser.add_argument("--dataset-yaml", required=True)
    parser.add_argument("--full-mmd-out", required=True)
    parser.add_argument("--atag-wcag-mmd-out", required=True)
    parser.add_argument("--informative-mmd-out", required=True)
    parser.add_argument("--max-edges-full", type=int, default=600)
    parser.add_argument("--max-edges-filtered", type=int, default=500)
    args = parser.parse_args()

    links = load_yaml(Path(args.dataset_yaml))

    full_text = build_mermaid(links, mode="all", max_edges=args.max_edges_full)
    atag_wcag_text = build_mermaid(links, mode="atag-wcag", max_edges=args.max_edges_filtered)
    informative_text = build_mermaid(links, mode="informative", max_edges=args.max_edges_filtered)

    write(Path(args.full_mmd_out), full_text)
    write(Path(args.atag_wcag_mmd_out), atag_wcag_text)
    write(Path(args.informative_mmd_out), informative_text)

    print(f"dataset_links={len(links)}")
    print(f"full={args.full_mmd_out}")
    print(f"atag_wcag={args.atag_wcag_mmd_out}")
    print(f"informative={args.informative_mmd_out}")


if __name__ == "__main__":
    main()
