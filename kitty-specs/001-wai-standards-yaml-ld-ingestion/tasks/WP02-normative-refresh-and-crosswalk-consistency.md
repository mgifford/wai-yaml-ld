---
work_package_id: "WP02"
title: "Normative refresh and crosswalk consistency"
lane: "planned"
dependencies:
  - "WP01"
subtasks:
  - "T004"
  - "T005"
  - "T006"
  - "T007"
phase: "Phase 2 - Normative maintenance"
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

# Work Package Prompt: WP02 - Normative refresh and crosswalk consistency

## Implementation Command

- `spec-kitty implement WP02 --base WP01`

## Objective

Ensure normative file refreshes preserve WCAG policy semantics and ATAG -> WCAG crosswalk consistency.

## Context

Relevant files:

- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.2-normative.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.0-normative.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-2.0-normative.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/uaag-2.0-normative.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml`

## Subtask Guidance

### T004 - Keep WCAG policy notes synchronized

- Verify policy statements in index and normative files remain aligned.
- Ensure explicit SC 4.1.1 exception handling remains documented where required.

### T005 - Verify crosswalk mapping consistency

- Validate profile target behavior and mapping counts after any criteria updates.
- Confirm no orphaned mappings or stale references.

### T006 - Create normative refresh procedure

- Document repeatable steps for refreshing criteria from canonical TR sources.
- Include file-by-file update order and verification points.

### T007 - Add dedupe and SC exclusion guardrails

- Define safeguards against duplicate criteria entries.
- Preserve explicit exclusion behavior for 4.1.1 in WCAG 2.2 cumulative assumptions.

## Definition of Done

- Normative refresh process is documented and reproducible.
- Crosswalk behavior remains correct after refresh.

## Risks and Reviewer Notes

- Risk: Parser assumptions can drift with TR markup changes.
- Reviewer should spot-check at least one criterion mapping path end-to-end.
