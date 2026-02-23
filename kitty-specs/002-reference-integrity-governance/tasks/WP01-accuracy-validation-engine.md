---
work_package_id: "WP01"
title: "Accuracy validation engine"
lane: "doing"
subtasks:
  - "T001"
  - "T002"
  - "T003"
  - "T004"
phase: "Phase 1 - Integrity Controls"
assignee: "copilot"
agent: "copilot"
shell_pid: ""
review_status: ""
reviewed_by: ""
history:
  - timestamp: "2026-02-23T00:00:00Z"
    lane: "planned"
    agent: "system"
    action: "Prompt generated"
---

# Work Package Prompt: WP01 – Accuracy validation engine

Implement a deterministic validator for `cross-standard-references.yaml` that enforces relation-type integrity and catches false positives.

Checks to include:
- source/target criterion existence for direct SC links
- inferred mapping consistency against crosswalk profile memberships
- informative resource links consistent with informative catalog `applies_to`

## Activity Log

- 2026-02-23T17:28:33Z – copilot – lane=doing – Started WP01 implementation and integrity hardening
