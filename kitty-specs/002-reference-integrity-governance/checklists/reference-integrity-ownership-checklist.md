# Reference Integrity Ownership Checklist

Feature: `002-reference-integrity-governance`

Use this checklist for quarterly audits and any high-impact relationship change.

## Ownership

- [ ] Primary owner assigned for cross-standard reference integrity.
- [ ] Backup owner assigned for CI workflow and validator continuity.
- [ ] Reviewer assigned for direct-link evidence verification.
- [ ] Contact/rotation information is current in project planning notes.

## Relation Taxonomy Governance

- [ ] Relation types in use match approved taxonomy.
- [ ] Any new relation type includes documented rationale and approval.
- [ ] Validator rules were updated for taxonomy changes.
- [ ] Existing valid relation semantics were preserved (no accidental weakening).

## Direct Reference Evidence Quality

- [ ] Direct links include non-empty evidence context.
- [ ] Source criterion codes are valid in canonical normative datasets.
- [ ] Target criterion codes are valid when SC-to-SC relation applies.
- [ ] Direct standard references do not incorrectly carry target criterion codes.

## Inferred and Informative Relationship Quality

- [ ] Inferred links use `basis: inferred_profile_mapping`.
- [ ] Inferred links map to supported profile/channel constraints.
- [ ] Informative links use `basis: catalog_applies_to`.
- [ ] Informative link targets align with catalog `applies_to` declarations.

## Execution and Evidence

- [ ] Artifact regeneration command completed successfully.
- [ ] `validate_cross_standard_references.py` returned success.
- [ ] Any failures were triaged with owner and remediation recorded.
- [ ] Final audit result was documented in PR description or maintenance log.

## Cadence

- [ ] Quarterly full audit completed.
- [ ] Additional audit run for taxonomy or validator changes.
- [ ] Additional audit run for crosswalk or informative catalog updates.
