# Quickstart: WAI Standards YAML-LD Ingestion

## 1) Open the feature directory

- `cd /workspaces/codespaces-blank/wai-yaml-ld`

## 2) Review key artifacts

- Spec: `kitty-specs/001-wai-standards-yaml-ld-ingestion/spec.md`
- Plan: `kitty-specs/001-wai-standards-yaml-ld-ingestion/plan.md`
- Maintenance baseline: `kitty-specs/001-wai-standards-yaml-ld-ingestion/maintenance-baseline.md`
- Standards index: `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml`
- Shared informative catalog: `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml`
- Crosswalk: `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml`

## 3) Make updates safely

- Keep normative criteria in `*-normative.yaml` files only
- Keep informative links in informative catalog files only
- Preserve stable IDs and existing policy fields

## 4) Verify changes

- Run targeted search checks for new IDs/URLs
- Run diagnostics on edited YAML files

## 5) Commit and push

- Stage only files under `kitty-specs/001-wai-standards-yaml-ld-ingestion/`
- Commit with clear message
- Push with full-scope credentials; if needed:
  - `env -u GITHUB_TOKEN -u GH_TOKEN git push`
