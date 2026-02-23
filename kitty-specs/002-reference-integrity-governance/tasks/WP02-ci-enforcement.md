---
work_package_id: "WP02"
title: "CI enforcement"
lane: "done"
subtasks:
  - "T005"
  - "T006"
phase: "Phase 2 - Pipeline Gates"
assignee: "copilot"
agent: "copilot"
shell_pid: ""
review_status: "approved"
reviewed_by: "Mike Gifford"
history:
  - timestamp: "2026-02-23T00:00:00Z"
    lane: "planned"
    agent: "system"
    action: "Prompt generated"
---

# Work Package Prompt: WP02 – CI enforcement

Add validator execution to:
- PR validation workflow
- refresh artifacts workflow

Fail workflow on integrity violations.

## Activity Log

- 2026-02-23T17:29:44Z – copilot – lane=doing – Verified validator gate exists in PR validation and refresh workflows
- 2026-02-23T17:29:48Z – copilot – lane=done – Confirmed cross-standard integrity validator hard-fails in both workflows
