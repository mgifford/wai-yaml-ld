# Feature Spec: Reference Integrity Governance

## Feature ID

- `002-reference-integrity-governance`

## Summary

Establish Spec-Kitty-governed accuracy controls so `wai-yaml-ld` remains a reliable, self-maintained reference for W3C accessibility standards relationships, with explicit prevention of false-positive links.

## Problem Statement

As the repository expands cross-standard links (normative and informative), confidence and long-term maintenance require explicit governance beyond data generation scripts. Without hard validation gates, inferred links can be mistaken for direct citations and relationship accuracy can drift.

## Goals

- Enforce relation-type integrity (`direct` vs `inferred`) for cross-standard links.
- Block false positives in CI before merge.
- Make governance auditable and maintainable through Spec-Kitty work packages.
- Keep this repository usable as a single, dependable accessibility standards reference.

## Non-Goals

- Claiming legal or normative authority over W3C standards.
- Replacing source-of-truth TR/NOTE documents.
- Guaranteeing zero conceptual ambiguity in standards interpretation.

## Scope

### In Scope

- Accuracy validation for `derived/cross-standard-references.yaml`.
- CI enforcement in validation and refresh workflows.
- Governance documentation under Spec-Kitty for periodic review and maintenance ownership.

### Out of Scope

- Rewriting all historical datasets.
- Building a separate hosted API service.

## Functional Requirements

1. The project MUST validate that every direct SC reference maps to an existing source and target criterion code in canonical normative datasets.
2. The project MUST validate that inferred links are clearly marked `basis: inferred_profile_mapping` and remain constrained to supported mapping channels.
3. The project MUST validate informative resource links against catalog membership and declared `applies_to` targets.
4. CI MUST fail when cross-standard reference integrity checks fail.
5. Governance artifacts MUST document change-control and audit expectations.

## Data Contract Extensions

- `cross-standard-references.yaml` relation integrity checks:
  - `direct_sc_reference_cross_standard`
  - `direct_sc_reference_intra_standard`
  - `direct_standard_reference`
  - `inferred_sc_reference_cross_standard`
  - `informative_resource_reference_standard`

## Acceptance Criteria

- A maintainer can run one command to validate cross-standard reference integrity and receive actionable failures.
- PR validation blocks merges when relationship integrity fails.
- Refresh workflow enforces the same integrity checks on regenerated artifacts.
- Governance tasks and ownership expectations are documented in Spec-Kitty.

## Risks and Mitigations

- Risk: Overly rigid checks may block legitimate future relation-types.
  - Mitigation: Keep relation taxonomy explicit and versioned; update validator with spec changes.
- Risk: Source model drift (new IDs/types) creates maintenance burden.
  - Mitigation: Spec-Kitty review cadence and workflow-based early detection.

## Operational Notes

- Relationship generation remains data-driven; governance adds verification and change controls.
- CI failure is intentional for uncertain or malformed links.

## Open Questions

- Should a formal reviewer-approval requirement be added for any new `relation_type` value?
- Should we add signed-off evidence snapshots for direct cross-standard SC citations when they appear?
