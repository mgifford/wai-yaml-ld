# Feature Spec: WAI Standards YAML-LD Ingestion

## Feature ID

- `001-wai-standards-yaml-ld-ingestion`

## Summary

Create and maintain machine-readable YAML resources for key W3C WAI standards and related guidance, with explicit separation between normative and informative content, WCAG 2.2-first policy, and crosswalk metadata for ATAG to WCAG linkage.

## Problem Statement

Accessibility standard content is distributed across multiple W3C pages and formats. Projects that need consistent ingestion into internal systems require:

- Canonical TR links
- Structured success criteria data
- Clear versioning policy
- Reliable cross-standard relationship metadata

## Goals

- Provide one normative YAML per core standard set in scope.
- Use direct W3C TR URLs for standards sources.
- Prioritize WCAG 2.2 while preserving WCAG 2.0 as legacy/provenance.
- Include informative resource catalogs for implementation context.
- Provide machine-readable ATAG to WCAG 2.2 crosswalk with explicit 4.1.1 exception.

## Non-Goals

- Building a runtime ingestion service or API.
- Replacing authoritative W3C source documents.

## Scope

### In Scope

- Normative YAML files for WCAG, ATAG, and UAAG in this feature directory.
- Shared and ARIA-focused informative resource catalogs.
- Top-level standards index listing canonical sources and local YAML artifacts.
- Crosswalk file describing ATAG to WCAG 2.2 mappings and profile behavior.
- Derived artifact generation (JSON-LD, CSV, Mermaid) from canonical YAML sources.
- CI-based regeneration and validation checks for graph and cross-standard artifacts.
- Scheduled source monitoring and refresh workflows.

### Out of Scope

- Editing source standards text.
- Defining new conformance rules beyond published standards and explicit project policy notes.

## Inputs and Source Authority

- W3C Technical Reports (TR) pages are authoritative for standards links.
- W3C WAI pages are authoritative for role/planning and practical guidance links.
- Project-defined linkage policy metadata is authoritative for crosswalk behavior.

## Functional Requirements

1. The system MUST maintain `research/w3c-wai-standards.yaml` as the top-level index.
2. The index MUST include direct TR links for normative standards.
3. The index MUST include a pointer to `research/w3c-wai-informative-resources.yaml`.
4. The project MUST provide normative YAML files:
	 - `research/wcag-2.2-normative.yaml`
	 - `research/wcag-2.0-normative.yaml` (legacy reference)
	 - `research/atag-2.0-normative.yaml`
	 - `research/uaag-2.0-normative.yaml`
5. WCAG policy MUST declare 2.2 as primary and 2.0 as legacy.
6. WCAG 2.2 criterion handling MUST exclude 4.1.1 from cumulative profile assumptions.
7. ATAG/WCAG linkage metadata MUST include explicit 4.1.1 exception treatment.
8. The project MUST provide `research/atag-to-wcag-2.2-crosswalk.yaml`.
9. Informative resources MUST be separated from normative criteria data.
10. The shared informative catalog MUST include requested resources for APG, AAM, AccName, ARIA in HTML, SVG AAM, EPUB accessibility docs, Web Sustainability Guidelines, ARRM, digital publishing roles context, and ACT Rules Format references.
11. The project MUST generate and version derived artifacts for standards graph, crosswalk, and cross-standard references.
12. CI MUST fail when regenerated artifacts differ from committed outputs.
13. CI MUST validate cross-standard reference integrity before merge.
14. The project MUST monitor upstream W3C and related sources on a scheduled cadence and emit a change report artifact.

## Data and File Contract

### Required Files

- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wai-aria-informative.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.2-normative.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.0-normative.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-2.0-normative.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/uaag-2.0-normative.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml`

### Conventions

- YAML must remain parseable and UTF-8 clean.
- IDs should be stable and machine-readable.
- `type` and `format_hint` should be present where applicable in index files.

## Acceptance Criteria

- Top-level standards index lists normative standards, requested informative references, crosswalk file, and informative-catalog pointer.
- Normative files exist and contain structured criteria suitable for ingestion.
- Crosswalk file exists with explicit 4.1.1 exception rule.
- Informative resources are present in both shared and ARIA-focused catalogs where applicable.
- Derived outputs can be regenerated from source YAML with no uncommitted diffs.
- PR validation workflow runs graph and cross-standard validation gates.
- Monitoring and refresh workflows are configured and runnable via GitHub Actions.

## Risks and Mitigations

- Risk: W3C pages evolve and links/version status change.
	- Mitigation: keep `updated` fields current and prefer canonical TR URLs.
- Risk: Ambiguity between informative and normative classifications.
	- Mitigation: maintain explicit `type` metadata and separate files.
- Risk: Downstream consumers misread WCAG cumulative behavior around 4.1.1.
	- Mitigation: preserve explicit policy note and crosswalk exception metadata.

## Operational Notes

- Keep changes focused to feature files under `kitty-specs/001-wai-standards-yaml-ld-ingestion/`.
- Avoid committing agent runtime directories.
- Treat unrelated repository churn outside this feature as out of scope for this spec.
- Primary workflow coverage lives in:
	- `.github/workflows/standards-link-graph-validate.yml`
	- `.github/workflows/w3c-standards-monitor.yml`
	- `.github/workflows/refresh-standards-artifacts.yml`
	- `.github/workflows/weekly-resource-link-check.yml`

## Open Questions

- Should WCAG 2.0 legacy YAML remain permanently, or be archived after downstream migration to 2.2?
- Should additional schema-level contract validation be added as a required gate for every PR?
