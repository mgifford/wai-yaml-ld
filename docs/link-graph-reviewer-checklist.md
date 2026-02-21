# Link Graph Reviewer Checklist

One-page checklist for reviewing link-graph updates in this repository.

## Scope and Inputs

- [ ] Confirm the PR clearly states the intended graph change (new nodes, new edges, or confidence/evidence updates).
- [ ] Confirm reviewer has these files open:
  - [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml)
  - [schemas/standards-link-graph.schema.json](../schemas/standards-link-graph.schema.json)
  - [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.edges.csv](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.edges.csv)

## Graph Integrity

- [ ] Every edge `from` and `to` points to an existing node ID.
- [ ] Relation values are valid and semantically appropriate for the claim.
- [ ] Node IDs remain stable (avoid renames unless migration is explicit).
- [ ] New nodes include `id`, `label`, `kind`, and `url`.
- [ ] New edges include `id`, `from`, `relation`, `to`, `confidence`, and `evidence`.

## Evidence Quality

- [ ] `confidence = high` edges are grounded in explicit source artifacts.
- [ ] `confidence = medium` edges are clearly marked as interpretive/supporting.
- [ ] Evidence text is specific and testable (not generic claims).
- [ ] Normative vs informative resources are not conflated.

## Freshness and Generated Artifacts

- [ ] Extraction fields are fresh enough for current policy:
  - `full_spec_inventory_extracted_at`
  - `full_section_inventory_extracted_at`
- [ ] Regenerated outputs are committed when graph changed:
  - [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.jsonld](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.jsonld)
  - [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.edges.csv](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.edges.csv)
  - [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.mmd](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.mmd)

## Reviewer Commands

Run these locally before approval:

`python scripts/validate_standards_graph.py --graph-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml --stale-threshold-days 120 --check-file kitty-specs/001-wai-standards-yaml-ld-ingestion/research/css-specifications-index.yaml:full_spec_inventory_extracted_at --check-file kitty-specs/001-wai-standards-yaml-ld-ingestion/research/html-living-standard-accessibility.yaml:full_section_inventory_extracted_at`

`python scripts/generate_standards_link_graph.py --graph-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml --jsonld-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.jsonld --csv-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.edges.csv --mermaid-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.mmd`

## Approval Gate

- [ ] CI workflow `Standards Link Graph Validation` is passing.
- [ ] Checklist items above are satisfied or explicitly waived with rationale.
- [ ] PR description includes impact summary for downstream human/LLM consumers.