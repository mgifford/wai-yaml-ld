# Link Graph Playbook

Practical guide for navigating and querying how WCAG, ATAG, UAAG, ARIA, HTML, and CSS are linked in this repository.

## 1) Best Starting Points

### For humans

1. Canonical map: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml)
2. Tabular edge view: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.edges.csv](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.edges.csv)
3. Source indexes:
   - [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml)
   - [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml)

### For LLMs

Provide these first:

1. Graph + schema
   - [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml)
   - [schemas/standards-link-graph.schema.json](../schemas/standards-link-graph.schema.json)
2. Supporting indexes
   - [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml)
   - [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml)

## 2) How to Read the Link Graph

- `nodes`: entities (standards, specs, datasets, catalogs)
- `edges`: typed relationships between nodes (`from`, `relation`, `to`)
- `relation_types`: canonical semantics for edge types
- `starting_points`: suggested launch nodes for humans vs LLMs
- `confidence` + `evidence`: how strong each link is and why it exists

## 3) Common Human Workflows

### A) Find what supports WCAG outcomes

Open the edge CSV and filter rows where `to = wcag-2.2` and `relation = supports_outcome_for`.

### B) Find mapping specs for HTML/ARIA

Filter where `relation = implements_mapping_for` and inspect `to` values for `html-living-standard` or `wai-aria-1.2`.

### C) See “what should I read first?”

Start from graph node `standards-link-graph`, then follow `catalogs` edges to indexes and crosswalk datasets.

## 4) LLM Prompt Templates

### Template: Explain standards linkage

"Using `standards-link-graph.yaml`, explain how WCAG 2.2 links to ATAG, UAAG, ARIA, HTML, and CSS. Use edge IDs and relation names, then list the most relevant source files to read next."

### Template: Build focused reading path

"Given `standards-link-graph.yaml`, produce a reading path for a developer implementing accessible forms. Prioritize nodes and edges involving HTML, ARIA in HTML, HTML AAM, AccName, and WCAG 2.2."

### Template: Detect weakly-supported links

"From `standards-link-graph.yaml`, list all edges with `confidence = medium`, explain why they are medium, and suggest what additional artifact would raise each to high confidence."

### Template: Extract machine-ready subgraph

"Create a subgraph containing nodes and edges reachable from `wcag-2.2` within depth 2. Return YAML preserving node IDs and edge IDs."

## 5) Keep Artifacts Fresh

Regenerate outputs after graph edits:

`python scripts/generate_standards_link_graph.py --graph-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml --jsonld-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.jsonld --csv-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.edges.csv --mermaid-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.mmd`

Run validation checks:

`python scripts/validate_standards_graph.py --graph-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml --stale-threshold-days 120 --check-file kitty-specs/001-wai-standards-yaml-ld-ingestion/research/css-specifications-index.yaml:full_spec_inventory_extracted_at --check-file kitty-specs/001-wai-standards-yaml-ld-ingestion/research/html-living-standard-accessibility.yaml:full_section_inventory_extracted_at`
