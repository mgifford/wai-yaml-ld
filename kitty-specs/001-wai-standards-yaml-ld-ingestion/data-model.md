# Data Model: WAI Standards YAML-LD Ingestion

## Entity: Standards Index

Primary file:
- `research/w3c-wai-standards.yaml`

Fields:
- `project` (string)
- `owner` (string)
- `updated` (date string)
- `sources` (array of SourceRef)
- `primary_wcag_version` (string)
- `wcag_version_policy` (string)

SourceRef fields:
- `id` (string, stable)
- `name` (string)
- `url` (string; absolute URL or relative project path)
- `type` (enum-like string: `standard`, `technical_spec`, `informative`, `hub`, `crosswalk`, `informative_catalog`)
- `format_hint` (string: `w3c-tr`, `html`, `yaml`)

## Entity: Normative Criteria Set

Primary files:
- `research/wcag-2.2-normative.yaml`
- `research/wcag-2.0-normative.yaml`
- `research/atag-2.0-normative.yaml`
- `research/uaag-2.0-normative.yaml`

Common fields:
- standard metadata (`standard_id`, `name`, `updated`, canonical source refs)
- criteria collection (array)

Criterion fields (typical):
- `id` or code (string)
- `title` (string)
- `level` (string)
- `text` (string)
- `url` (TR anchor URL)

## Entity: Informative Resource Catalog

Primary files:
- `research/w3c-wai-informative-resources.yaml`
- `research/wai-aria-informative.yaml`

Shared catalog item fields:
- `id` (string, stable)
- `title` (string)
- `url` (string)
- `type` (`informative` or related classification)
- `applies_to` (array of standard IDs; shared catalog)

## Entity: Crosswalk Profile

Primary file:
- `research/atag-to-wcag-2.2-crosswalk.yaml`

Fields:
- source and target metadata
- profile definitions (A/AA/AAA cumulative logic)
- explicit exclusion list including WCAG SC 4.1.1
- mapping records from ATAG criteria to WCAG criteria/profile targets

## Constraints

- IDs should be unique within each file
- URLs should be canonical and resolvable
- Normative and informative records must not be merged in one structure
- WCAG version policy must remain explicit in index and linkage metadata
