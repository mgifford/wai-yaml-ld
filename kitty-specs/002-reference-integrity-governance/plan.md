# Implementation Plan: Reference Integrity Governance

Feature: `002-reference-integrity-governance`

## Objectives

1. Add a deterministic validator for cross-standard reference integrity.
2. Enforce validation in both refresh and PR workflows.
3. Document governance cadence and review responsibilities.

## Work Packages

### WP01 - Accuracy validation engine

- Deliver `scripts/validate_cross_standard_references.py`
- Validate source/target criterion existence and basis/relation consistency
- Validate informative-resource relationships against catalog applies_to data

### WP02 - CI enforcement and maintenance loop

- Add validator step to `standards-link-graph-validate.yml`
- Add validator step to `refresh-standards-artifacts.yml`
- Ensure failures are explicit and actionable

### WP03 - Spec-Kitty governance and operating guide

- Create governance tasks docs with review cadence
- Define policy for relation taxonomy evolution
- Document minimum evidence requirements for direct links

## Sequencing

- WP01 -> WP02 -> WP03

## Success Signals

- Validator exits `0` on current artifact set.
- CI workflows run validator as a required gate.
- Governance docs identify owner responsibilities and periodic checks.
