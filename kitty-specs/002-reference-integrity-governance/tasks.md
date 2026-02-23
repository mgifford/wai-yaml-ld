# Tasks: Reference Integrity Governance

Feature: `002-reference-integrity-governance`

## Subtasks

- [x] T001 Implement cross-standard reference validator script
- [x] T002 Validate direct relation source/target criterion existence
- [x] T003 Validate inferred mapping consistency with crosswalk profiles
- [x] T004 Validate informative resource target relationships against applies_to
- [ ] T005 Add validator gate to PR validation workflow
- [ ] T006 Add validator gate to artifact refresh workflow
- [ ] T007 Add governance runbook and ownership checklist

## Work Packages

### WP01 - Accuracy validation engine

- Priority: P0
- Included subtasks: T001, T002, T003, T004
- Independent test: Validator catches malformed or inconsistent links and passes current dataset.
- Dependencies: none
- Prompt: `tasks/WP01-accuracy-validation-engine.md`

### WP02 - CI enforcement

- Priority: P0
- Included subtasks: T005, T006
- Independent test: Workflows fail on validator errors.
- Dependencies: WP01
- Prompt: `tasks/WP02-ci-enforcement.md`

### WP03 - Governance runbook

- Priority: P1
- Included subtasks: T007
- Independent test: Maintainer can follow one checklist for quarterly relationship audit.
- Dependencies: WP01
- Prompt: `tasks/WP03-governance-runbook.md`
