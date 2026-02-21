# Maintenance Baseline: Governance and Validation

Feature: `001-wai-standards-yaml-ld-ingestion`

This guide defines the baseline workflow for maintaining YAML artifacts in this feature.

## 1) Canonical Source Refresh Workflow (T001)

### Source authority order

1. W3C TR canonical URLs for standards and technical specifications
2. W3C WAI pages for contextual and informative resources
3. Project-local YAML artifacts for policy and crosswalk behavior

### Refresh triggers

- A W3C TR version/status change is published
- A new user request adds or updates source coverage
- A scheduled maintenance pass is performed
- A downstream consumer reports stale or missing source metadata

### Refresh sequence

1. Update relevant source URLs and metadata in `research/w3c-wai-standards.yaml`
2. Update normative or informative files impacted by the source change
3. Re-check policy fields and crosswalk behavior notes
4. Run the validation checklist in this document

## 2) Repeatable Validation Checklist (T002)

Run these checks after each update:

- [ ] YAML diagnostics pass for every edited file
- [ ] Required top-level fields exist per `contracts/wai-yaml-contract.yaml`
- [ ] IDs are stable and unique in the edited file
- [ ] URLs are canonical (prefer `https://www.w3.org/TR/...` for standards)
- [ ] Normative and informative content remain separated by file purpose
- [ ] WCAG policy fields are still present and consistent

## 3) Standards Index Change Log Workflow (T003)

When editing `research/w3c-wai-standards.yaml`:

1. Confirm each new/changed entry has `id`, `name`, `url`, `type`, and `format_hint`
2. Verify `primary_wcag_version` and `wcag_version_policy` are reviewed and unchanged unless intentional
3. Confirm index pointers to local project artifacts remain valid:
   - `./atag-to-wcag-2.2-crosswalk.yaml`
   - `./w3c-wai-informative-resources.yaml`
4. Include a concise commit message describing why the index changed

## 4) Minimal Schema Contract Checks (T011)

Use `contracts/wai-yaml-contract.yaml` as the minimum schema contract:

- `standards_index`: verify required top-level fields and `source_required_fields`
- `informative_catalog`: verify top-level fields and per-resource required fields
- `aria_informative_catalog`: verify required top-level structure
- `crosswalk`: verify explicit 4.1.1 exception behavior and profile-target semantics remain represented

If a file structure changes, update the contract first, then update data files.

## 5) Quick Verification Command Examples (T012)

From repository root:

```bash
# Verify required resources exist in standards index
grep -E "aria-apg-home|core-aam-1.2|accname-1.2|web-sustainability-guidelines|css-specifications-overview|html-living-standard" \
  kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml

# Verify crosswalk exception behavior reference exists
grep -Ei "4\.1\.1|exception" \
  kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml
```

Use editor diagnostics (Problems panel) to validate YAML parseability for edited files.

## WP01 Exit Check

WP01 is complete when:

- This baseline is present and current
- A maintainer can follow this page and validate all feature artifacts without extra assumptions
- `tasks.md` and `tasks/WP01-*.md` status reflect completion