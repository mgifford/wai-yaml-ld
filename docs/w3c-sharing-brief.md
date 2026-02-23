# W3C Sharing Brief: wai-yaml-ld

## Purpose

`wai-yaml-ld` provides machine-readable accessibility standards context for humans and AI systems, with explicit governance for source freshness, relationship integrity, and reproducible derived artifacts.

## What This Repository Contributes

- Curated canonical YAML datasets for core accessibility standards and related informative resources.
- Explicit graph relationships between standards, criteria, and implementation-support resources.
- Reproducible derived artifacts (JSON-LD, CSV, Mermaid) for analysis and traceability.
- Integrity controls that distinguish direct references from inferred mappings.
- Scheduled source monitoring and governance workflows.

## Recommended Materials to Share

### 1) Orientation

- Repository overview: [`README.md`](../README.md)
- Standards alignment write-up: [`docs/w3c-standards-alignment.md`](w3c-standards-alignment.md)
- Link-graph playbook: [`docs/link-graph-playbook.md`](link-graph-playbook.md)

### 2) Canonical Data and Contracts

- Standards index: [`kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml`](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml)
- Standards graph: [`kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml`](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml)
- Cross-standard references: [`kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml`](../kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml)
- Graph schema: [`schemas/standards-link-graph.schema.json`](../schemas/standards-link-graph.schema.json)
- Cross-standard schema: [`schemas/cross-standard-references.schema.json`](../schemas/cross-standard-references.schema.json)

### 3) Governance and Integrity Evidence

- Integrity validator: [`scripts/validate_cross_standard_references.py`](../scripts/validate_cross_standard_references.py)
- CI validation workflow: [`.github/workflows/standards-link-graph-validate.yml`](../.github/workflows/standards-link-graph-validate.yml)
- Source monitoring workflow: [`.github/workflows/w3c-standards-monitor.yml`](../.github/workflows/w3c-standards-monitor.yml)
- Refresh workflow: [`.github/workflows/refresh-standards-artifacts.yml`](../.github/workflows/refresh-standards-artifacts.yml)
- Governance runbook: [`kitty-specs/002-reference-integrity-governance/governance-runbook.md`](../kitty-specs/002-reference-integrity-governance/governance-runbook.md)
- Ownership checklist: [`kitty-specs/002-reference-integrity-governance/checklists/reference-integrity-ownership-checklist.md`](../kitty-specs/002-reference-integrity-governance/checklists/reference-integrity-ownership-checklist.md)

## Suggested Message to W3C Contacts

We are sharing `wai-yaml-ld` as an open, machine-readable companion dataset for accessibility standards context. The project preserves canonical source authority while improving traceability, cross-standard linkage, and practical reuse by humans and AI tools. We welcome review on data model fit, governance expectations, and opportunities to align with existing W3C publication/maintenance pathways.

## Suggested Outreach Sequence

1. Open a public issue/discussion in this repository with a short "request for W3C review" summary and links to this brief.
2. Share the summary in relevant W3C community channels (for example APA and AGWG-adjacent community touchpoints) with clear scope and non-normative intent.
3. Offer a short demo of:
   - graph navigation,
   - cross-standard integrity checks,
   - monitoring and refresh lifecycle.
4. Capture feedback as tracked issues labeled `w3c-feedback`.