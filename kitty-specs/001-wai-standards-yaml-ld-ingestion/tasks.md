# Tasks: WAI Standards YAML-LD Ingestion

Feature: `001-wai-standards-yaml-ld-ingestion`

## Subtasks

- [x] T001 Define and document canonical source refresh workflow for normative files
- [x] T002 Add repeatable validation checklist for YAML syntax and required keys
- [x] T003 Add change log section to standards index update workflow
- [x] T004 Confirm WCAG 2.2 policy and 4.1.1 exception notes remain synchronized across files
- [x] T005 Verify crosswalk profile targets and mapping_count consistency after updates
- [x] T006 Create update procedure for normative criteria refresh from W3C TR sources
- [x] T007 Add criteria deduplication and SC exclusion guardrails to update procedure
- [ ] T008 Define informative resource admission criteria and classification rules
- [ ] T009 Add explicit review checklist for APG/AAM/AccName/EPUB/WSG/ACT link presence
- [ ] T010 Add policy for adding new informative resources with stable IDs
- [x] T011 Define minimal schema contract checks for index, normative, informative, and crosswalk files
- [x] T012 Add quick verification command examples for maintainers

## Work Packages

### WP01 - Governance and validation baseline

- Priority: P0
- Independent test: A maintainer can follow one documented checklist and verify all current YAML artifacts without ambiguity.
- Included subtasks: T001, T002, T003, T011, T012
- Dependencies: none
- Prompt: `tasks/WP01-governance-and-validation-baseline.md`
- Implementation artifact: `maintenance-baseline.md`
- Parallel opportunities: Can run in parallel with discovery work for WP02.
- Risks: Checklist too generic and not tied to actual files.

### WP02 - Normative refresh and crosswalk consistency

- Priority: P0
- Independent test: Updating one normative source does not break WCAG policy notes, SC exception behavior, or crosswalk consistency.
- Included subtasks: T004, T005, T006, T007
- Dependencies: WP01
- Prompt: `tasks/WP02-normative-refresh-and-crosswalk-consistency.md`
- Implementation artifact: `normative-refresh-procedure.md`
- Parallel opportunities: Internal subtasks can parallelize by file (WCAG/ATAG/UAAG vs crosswalk).
- Risks: Unintended criteria drift during extraction refresh.

### WP03 - Informative catalog governance and curation

- Priority: P1
- Independent test: Requested informative resources are consistently represented in top-level and catalog files with stable IDs and classification.
- Included subtasks: T008, T009, T010
- Dependencies: WP01
- Prompt: `tasks/WP03-informative-catalog-governance-and-curation.md`
- Parallel opportunities: Can execute concurrently with WP02 once WP01 is complete.
- Risks: Misclassification of standards vs informative resources.

## MVP Recommendation

- MVP: Complete WP01 + WP02
- Rationale: Delivers stable maintenance and normative correctness guarantees before catalog expansion.

## Dependency Summary

- WP01: no dependencies
- WP02: depends on WP01
- WP03: depends on WP01
