# wai-yaml-ld

Machine-readable YAML resources for W3C WAI standards, plus governance and monitoring artifacts for maintaining them.

## Start Here

1. Read [README.md](README.md)
2. Review feature spec at [kitty-specs/001-wai-standards-yaml-ld-ingestion/spec.md](kitty-specs/001-wai-standards-yaml-ld-ingestion/spec.md)
3. Review implementation plan at [kitty-specs/001-wai-standards-yaml-ld-ingestion/plan.md](kitty-specs/001-wai-standards-yaml-ld-ingestion/plan.md)
4. Follow quickstart at [kitty-specs/001-wai-standards-yaml-ld-ingestion/quickstart.md](kitty-specs/001-wai-standards-yaml-ld-ingestion/quickstart.md)

## What To Point an LLM At

- Primary entrypoint: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml)
- Full informative catalog: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml)
- ARIA-focused informative catalog: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wai-aria-informative.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wai-aria-informative.yaml)
- Crosswalk logic and exception handling: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml)

## Comprehensive YAML Files

- Standards index: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml)
- WCAG 2.2 normative: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.2-normative.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.2-normative.yaml)
- WCAG 2.0 legacy normative: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.0-normative.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.0-normative.yaml)
- ATAG 2.0 normative: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-2.0-normative.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-2.0-normative.yaml)
- UAAG 2.0 normative: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/uaag-2.0-normative.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/uaag-2.0-normative.yaml)
- Shared informative resources: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml)
- CSS specifications index (machine-readable, includes full inventory extracted from W3C CSS overview): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/css-specifications-index.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/css-specifications-index.yaml)
- HTML Living Standard accessibility index (machine-readable, includes full section inventory extracted from WHATWG source): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/html-living-standard-accessibility.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/html-living-standard-accessibility.yaml)
- ATAG to WCAG 2.2 crosswalk: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml)

## JSON Schemas (for tooling/LLM validation)

- Standards index schema: [schemas/w3c-wai-standards.schema.json](schemas/w3c-wai-standards.schema.json)
- Shared informative catalog schema: [schemas/w3c-wai-informative-resources.schema.json](schemas/w3c-wai-informative-resources.schema.json)
- ARIA informative catalog schema: [schemas/wai-aria-informative.schema.json](schemas/wai-aria-informative.schema.json)
- CSS specifications index schema: [schemas/css-specifications-index.schema.json](schemas/css-specifications-index.schema.json)
- HTML Living Standard accessibility index schema: [schemas/html-living-standard-accessibility.schema.json](schemas/html-living-standard-accessibility.schema.json)
- Crosswalk schema: [schemas/atag-to-wcag-2.2-crosswalk.schema.json](schemas/atag-to-wcag-2.2-crosswalk.schema.json)

If you are pointing an LLM at this repository, provide both the target YAML file and its matching schema file as context.

## Why These Live Under research/

For this repository phase, these are curated specification datasets and governance outputs generated under the feature directory. Keeping them under `research/` keeps all ingestion artifacts together and tied to spec/plan/tasks.

If this repository later publishes a stable external data package, create a promoted location (for example `datasets/wai/`) and keep `research/` as the change-staging source.

## Monitoring W3C Standard Changes

Monitoring is now set up with:

- Watchlist baseline: [monitoring/w3c-tr-watchlist.json](monitoring/w3c-tr-watchlist.json)
- Monitor script: [scripts/monitor_w3c_sources.py](scripts/monitor_w3c_sources.py)
- Scheduled GitHub Action: [.github/workflows/w3c-standards-monitor.yml](.github/workflows/w3c-standards-monitor.yml)

The workflow runs weekly and on manual dispatch, checks watched TR headers (ETag/Last-Modified), uploads a report artifact, and opens an issue when changes are detected.

Run manually:

- Baseline refresh: `python scripts/monitor_w3c_sources.py --refresh --watchlist monitoring/w3c-tr-watchlist.json --report monitoring/w3c-change-report.md`
- Change check: `python scripts/monitor_w3c_sources.py --check --watchlist monitoring/w3c-tr-watchlist.json --report monitoring/w3c-change-report.md`

## Governance and Maintenance Docs

- Maintenance baseline: [kitty-specs/001-wai-standards-yaml-ld-ingestion/maintenance-baseline.md](kitty-specs/001-wai-standards-yaml-ld-ingestion/maintenance-baseline.md)
- Normative refresh procedure: [kitty-specs/001-wai-standards-yaml-ld-ingestion/normative-refresh-procedure.md](kitty-specs/001-wai-standards-yaml-ld-ingestion/normative-refresh-procedure.md)
- Informative catalog governance: [kitty-specs/001-wai-standards-yaml-ld-ingestion/informative-catalog-governance.md](kitty-specs/001-wai-standards-yaml-ld-ingestion/informative-catalog-governance.md)

## Repository Hygiene

Local machine/runtime files are ignored by [.gitignore](.gitignore), including local agent directories and local `.kittify` runtime metadata.
