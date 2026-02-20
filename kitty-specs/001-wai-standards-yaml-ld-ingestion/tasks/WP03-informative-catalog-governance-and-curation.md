---
work_package_id: "WP03"
title: "Informative catalog governance and curation"
lane: "planned"
dependencies:
  - "WP01"
subtasks:
  - "T008"
  - "T009"
  - "T010"
phase: "Phase 2 - Informative curation"
assignee: ""
agent: ""
shell_pid: ""
review_status: ""
reviewed_by: ""
history:
  - timestamp: "2026-02-20T00:00:00Z"
    lane: "planned"
    agent: "system"
    action: "Prompt generated via /spec-kitty.tasks"
---

# Work Package Prompt: WP03 - Informative catalog governance and curation

## Implementation Command

- `spec-kitty implement WP03 --base WP01`

## Objective

Maintain a high-quality informative resource catalog with stable IDs, consistent classifications, and complete required coverage.

## Context

Relevant files:

- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wai-aria-informative.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml`

## Subtask Guidance

### T008 - Define informative admission and classification rules

- Document criteria for adding new informative entries.
- Clarify when entries should be labeled `informative` vs `technical_spec` references in index contexts.

### T009 - Add explicit coverage checklist for requested resources

- Include checks for APG, AAM, AccName, ARIA in HTML, SVG AAM, EPUB docs, Web Sustainability Guidelines, and ACT entries.
- Ensure expected entries appear in the intended catalogs.

### T010 - Define stable ID policy for new resources

- Provide naming and versioning conventions for IDs.
- Prevent duplicate IDs and ambiguous title variants.

## Definition of Done

- Informative catalogs follow explicit and repeatable governance rules.
- Coverage checklist verifies all requested resource families.

## Risks and Reviewer Notes

- Risk: Resource classification drift between files.
- Reviewer should compare top-level index visibility with full informative catalog coverage.
