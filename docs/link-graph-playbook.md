# Link Graph Playbook

Practical guide for navigating and querying how WCAG, ATAG, UAAG, ARIA, HTML, and CSS are linked in this repository.

Reviewer onboarding quick-reference: [docs/link-graph-reviewer-checklist.md](link-graph-reviewer-checklist.md)

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

## 6) Example Q&A Outputs

### Example 1: “How does HTML map to WCAG outcomes?”

Question:

"Using the link graph, show how HTML connects to WCAG 2.2."

Good answer shape:

- Direct path: `html-living-standard -> supports_outcome_for -> wcag-2.2` (`e020`)
- Related supporting path: `html-aam-1.0 -> implements_mapping_for -> html-living-standard` (`e017`), then HTML contributes to WCAG outcomes via `e020`
- ARIA/host-language constraint path: `aria-in-html -> profiles -> html-living-standard` (`e016`)
- Suggested follow-up files:
   - [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/html-living-standard-accessibility.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/html-living-standard-accessibility.yaml)
   - [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml)

### Example 2: “Which specs support ARIA implementation details?”

Question:

"List mapping and computation specs that support WAI-ARIA implementation."

Good answer shape:

- `core-aam-1.2 -> implements_mapping_for -> wai-aria-1.2` (`e018`)
- `accname-1.2 -> supports_outcome_for -> wai-aria-1.2` (`e019`)
- Explain that one edge covers API mappings and the other covers name/description computation behavior
- Point to source specs:
   - [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml)

### Example 3: “What are the most central datasets?”

Question:

"What datasets should I read first to understand this repository quickly?"

Good answer shape:

- Start with graph root dataset via `catalogs` edges (`e024` to `e028`)
- Recommend in order:
   1. [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml)
   2. [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml)
   3. [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml)
   4. [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/css-specifications-index.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/css-specifications-index.yaml)
   5. [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/html-living-standard-accessibility.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/html-living-standard-accessibility.yaml)

## 7) Common Mistakes and Anti-Pattern Prompts

### Mistake: Asking for vague “all links” summaries

Anti-pattern prompt:

"Explain everything about how all standards are related."

Better prompt:

"Using `standards-link-graph.yaml`, list only edges where `to = wcag-2.2`, grouped by relation type, and cite edge IDs."

### Mistake: Ignoring edge confidence

Anti-pattern prompt:

"Treat all graph edges as equally authoritative and produce hard conclusions."

Better prompt:

"Separate `high` and `medium` confidence edges and clearly flag conclusions that rely on `medium` confidence links."

### Mistake: Mixing normative claims with informative catalogs

Anti-pattern prompt:

"Use informative catalog entries as if they are normative conformance requirements."

Better prompt:

"Distinguish normative specs from informative resources using node `kind` and relation context before drawing compliance conclusions."

### Mistake: Not constraining scope/depth

Anti-pattern prompt:

"Return every possible path in the graph."

Better prompt:

"Return paths from `html-living-standard` to `wcag-2.2` with maximum depth 2 and include edge IDs only."

### Mistake: Skipping source verification

Anti-pattern prompt:

"Answer only from memory; do not reference files."

Better prompt:

"For each edge used in your answer, include the node IDs and the source YAML file that grounds the claim."

## 8) Visualization Views and What They Show

Use these views together:

- Full topology view: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.mmd](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.mmd)
   - Best for complete node/edge inventory
- Relation-grouped view: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.by-relation.mmd](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.by-relation.mmd)
   - Best for understanding connection semantics (`maps_to`, `profiles`, `implements_mapping_for`, etc.)
- WCAG-centric neighborhood: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.wcag-centric.mmd](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.wcag-centric.mmd)
   - Best for “what influences WCAG outcomes?” analysis
- Part-level view (HTML/CSS sections/modules): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.mmd](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.mmd)
   - Best for “which parts of specs link to parent standards and WCAG?”
- Part-level table: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.edges.csv](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.edges.csv)
   - Best for filtering and spreadsheet-style review
- Interactive filter UI: [docs/standards-link-viewer.html](standards-link-viewer.html)
   - Best for fast exploratory filtering by node, relation, and confidence

Regenerate visualization views:

`python scripts/generate_standards_visualizations.py --graph-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml --html-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/html-living-standard-accessibility.yaml --css-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/css-specifications-index.yaml --by-relation-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.by-relation.mmd --wcag-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.wcag-centric.mmd --parts-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.mmd --parts-csv-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.edges.csv`
