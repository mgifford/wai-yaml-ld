# Reference Integrity Governance Runbook

Feature: `002-reference-integrity-governance`

This runbook defines repeatable governance for cross-standard reference integrity and long-term maintenance.

## Scope

Applies to:

- `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml`
- `scripts/validate_cross_standard_references.py`
- CI workflows that regenerate and validate link artifacts

## Roles and Responsibilities

- **Data Maintainer (owner)**
  - Maintains relation taxonomy and data semantics.
  - Reviews proposed relation changes and evidence quality.
  - Runs and triages integrity validation results.

- **Workflow Maintainer (backup owner)**
  - Maintains CI gate behavior in pull request and refresh workflows.
  - Confirms validator failures block merges until resolved.

- **Reviewer**
  - Verifies that direct references have adequate evidence.
  - Verifies inferred and informative links follow policy and checks.

## Relation Taxonomy Change Policy

Current supported relation types are the project contract and must remain explicit:

- `direct_sc_reference_cross_standard`
- `direct_sc_reference_intra_standard`
- `direct_standard_reference`
- `inferred_sc_reference_cross_standard`
- `informative_resource_reference_standard`

Policy for taxonomy changes:

1. Propose the change in the feature or PR description with rationale and intended impact.
2. Update generation logic and `scripts/validate_cross_standard_references.py` in the same change.
3. Add/adjust fixture or sample data so the new relation is testable.
4. Run integrity validation and ensure no existing valid links regress.
5. Require maintainer review before merge for any new relation type or basis value.

## Evidence Standard for Direct Links

Direct relations (`basis: direct`) require evidence that supports a non-inferred citation claim.

Minimum evidence expectations:

- Source criterion exists in its canonical normative dataset.
- Target criterion exists when relation is SC-to-SC.
- `evidence_excerpt` contains text indicating explicit reference context.
- `target_url` points to a canonical target location.

Direct-link review checks:

- Confirm relation type matches the citation granularity (criterion vs standard).
- Confirm no inferred basis is used for direct claims.
- Confirm no placeholder or empty evidence fields are introduced.

## Audit Cadence and Triggers

### Cadence

- **Quarterly**: full audit of direct, inferred, and informative relationships.
- **Per PR touching derived links or validator logic**: targeted audit for changed records.

### Triggered audits

Run an out-of-cycle audit when:

- relation taxonomy changes,
- crosswalk profiles change,
- informative catalog `applies_to` fields change,
- validator logic is updated.

## Audit Procedure

1. Regenerate cross-standard references from source artifacts.
2. Run `scripts/validate_cross_standard_references.py` on generated output.
3. Review all validator failures and classify as:
   - data issue,
   - rule issue,
   - expected taxonomy evolution.
4. For direct link failures, validate evidence and source/target criterion correctness.
5. For inferred link failures, verify profile membership and basis semantics.
6. For informative failures, verify resource IDs and `applies_to` alignment.
7. Resolve issues and rerun validation until clean.
8. Record audit summary in PR notes or maintenance log.

## Operational Commands

From repository root:

```bash
python scripts/generate_cross_standard_references.py \
  --wcag22-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.2-normative.yaml \
  --wcag20-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.0-normative.yaml \
  --atag-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-2.0-normative.yaml \
  --uaag-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/uaag-2.0-normative.yaml \
  --crosswalk-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml \
  --informative-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml \
  --out-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml \
  --out-csv kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.csv

python scripts/validate_cross_standard_references.py \
  --dataset-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml \
  --wcag22-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.2-normative.yaml \
  --wcag20-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.0-normative.yaml \
  --atag-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-2.0-normative.yaml \
  --uaag-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/uaag-2.0-normative.yaml \
  --crosswalk-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml \
  --informative-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml
```

## Exit Criteria

Governance is operating correctly when:

- Validator passes on current generated artifacts.
- PR and refresh workflows both execute validator as required gates.
- Every taxonomy change includes validator and review updates.
- Quarterly audit checklist is completed and archived.
