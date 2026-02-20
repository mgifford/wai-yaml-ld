# Research Notes: WAI Standards YAML-LD Ingestion

## Decisions

### Decision: Use direct W3C TR URLs for normative standards

- Rationale: Canonical, stable references for ingestion pipelines
- Alternatives considered: WAI landing pages, generic standards hub pages

### Decision: Maintain separate normative and informative catalogs

- Rationale: Prevent conflating conformance requirements with guidance/supporting material
- Alternatives considered: Single mixed catalog

### Decision: Make WCAG 2.2 the primary target

- Rationale: Current baseline for implementation guidance and conformance alignment
- Alternatives considered: WCAG 2.0-only baseline

### Decision: Keep WCAG 2.0 as legacy/provenance

- Rationale: Backward reference and provenance continuity for legacy consumers
- Alternatives considered: Remove WCAG 2.0 file immediately

### Decision: Explicitly model SC 4.1.1 exception in ATAG -> WCAG 2.2 crosswalk

- Rationale: WCAG 2.2 cumulative profile handling requires explicit machine-readable exception behavior
- Alternatives considered: Implicit exception by omission only

## Informative Resource Coverage Decisions

Included in shared and/or ARIA-focused catalogs:

- APG (home, patterns, examples)
- Core AAM 1.2
- HTML AAM 1.0
- AccName 1.2
- ARIA in HTML
- SVG AAM 1.0
- EPUB Accessibility 1.1
- EPUB Accessibility Techniques 1.1
- Web Sustainability Guidelines
- ARRM resources
- ACT Rules Format 1.1, 1.0, and latest stream

## Validation Approach

- Run targeted text searches for required IDs/URLs
- Run YAML diagnostics on modified files
- Keep edits scoped to `kitty-specs/001-wai-standards-yaml-ld-ingestion/`
