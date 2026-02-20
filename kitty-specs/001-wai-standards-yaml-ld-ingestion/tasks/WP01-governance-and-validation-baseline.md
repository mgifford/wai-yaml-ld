---
work_package_id: "WP01"
title: "Governance and validation baseline"
lane: "done"
dependencies: []
subtasks:
  - "T001"
  - "T002"
  - "T003"
  - "T011"
  - "T012"
phase: "Phase 1 - Foundation"
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
  - timestamp: "2026-02-20T00:00:00Z"
    lane: "done"
    agent: "copilot"
    action: "Implemented WP01 baseline in maintenance-baseline.md"
---

# Work Package Prompt: WP01 - Governance and validation baseline

## Implementation Command

- `spec-kitty implement WP01`

## Objective

Establish a reliable maintenance baseline for this feature so maintainers can update YAML artifacts safely and consistently.

## Context

Relevant files:

- `kitty-specs/001-wai-standards-yaml-ld-ingestion/spec.md`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/plan.md`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml`
- `kitty-specs/001-wai-standards-yaml-ld-ingestion/contracts/wai-yaml-contract.yaml`

## Subtask Guidance

### T001 - Define canonical source refresh workflow for normative files

- Document source authority order (W3C TR first, WAI pages for context only).
- Define refresh trigger conditions (new recommendation updates, user request, periodic review).

### T002 - Add repeatable validation checklist

- Create a checklist that verifies YAML parses and required fields are present.
- Include checks for stable IDs and canonical URL shape.

### T003 - Add standards-index change log workflow

- Define expected edit sequence when `w3c-wai-standards.yaml` changes.
- Ensure policy fields (`primary_wcag_version`, `wcag_version_policy`) are reviewed during each update.

### T011 - Define minimal schema contract checks

- Ensure `contracts/wai-yaml-contract.yaml` remains aligned with current file structures.
- Add explicit guidance for validating required top-level fields and nested item fields.

### T012 - Add quick verification command examples

- Provide concise examples for search and diagnostics commands maintainers should run after edits.

## Definition of Done

- A maintainer can execute a single baseline checklist and validate all feature artifacts.
- Contract and index governance rules are explicit and unambiguous.

## Risks and Reviewer Notes

- Risk: Overly abstract guidance that is not actionable.
- Reviewer should confirm each checklist item maps to a concrete file and command.
