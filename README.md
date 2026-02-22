# wai-yaml-ld

Machine-readable accessibility standards context for AI coding systems.

This repository turns key W3C WAI + related standards (WCAG, ATAG, UAAG, ARIA, HTML, CSS) into structured YAML/JSON-LD/CSV artifacts that an LLM can reliably consume when generating or reviewing code.

GitHub Pages landing page (if enabled):

- https://mgifford.github.io/wai-yaml-ld/
- Playbook web page: https://mgifford.github.io/wai-yaml-ld/link-graph-playbook.html
- Interactive viewer: https://mgifford.github.io/wai-yaml-ld/standards-link-viewer.html
- Semantic theory/reference page: https://mgifford.github.io/wai-yaml-ld/semantic-linked-data-llm.html
- W3C standards alignment: https://mgifford.github.io/wai-yaml-ld/w3c-standards-alignment.html

## What This Project Is For

- Give humans and LLMs a single, machine-readable source of truth for accessibility standards context
- Reduce hallucinated or outdated accessibility advice by grounding responses in curated standards datasets
- Make relationships between standards explicit (for example HTML/ARIA/CSS support paths toward WCAG outcomes)
- Support repeatable governance: schema validation, change monitoring, freshness checks, and CI guardrails

## W3C Standards Alignment and Open Web Philosophy

This project aligns with W3C's broader standards ecosystem and embodies open web principles:

- **W3C Maturity Model**: Supports organizational accessibility maturity progression through structured data for people, processes, and technology dimensions
- **Ethical Web Principles**: Embodies all ten principles including transparency, accessibility for all, verifiability, and environmental sustainability
- **Open Web**: Machine-readable formats, transparent governance, and freely available data strengthen the open web
- **Standards Gaps**: Addresses gaps in current W3C standards distribution including machine-readable formats, cross-standard relationships, and AI-optimized documentation

For detailed analysis, see [W3C Standards Alignment documentation](docs/w3c-standards-alignment.md) or [web version](https://mgifford.github.io/wai-yaml-ld/w3c-standards-alignment.html).

## Why Use This With an LLM

If an LLM only sees your app code, it often gives generic accessibility advice.

If an LLM sees your app code plus this repository’s structured standards context, it can:

- map implementation choices to specific standards relationships
- separate normative vs informative references
- produce more auditable, standards-aligned recommendations
- explain why a recommendation is being made (via graph edges and evidence)

## How To Use With an LLM (Recommended Flow)

1. Provide your app code context.
2. Add this standards context bundle:
	- [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml)
	- [schemas/standards-link-graph.schema.json](schemas/standards-link-graph.schema.json)
	- [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml)
	- [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml)
3. Ask the LLM to cite node IDs / edge IDs when making accessibility claims.
4. Ask for output in two parts:
	- code changes
	- standards traceability (what standards/edges justify each change)
5. Validate outcomes with your normal testing + accessibility checks.

Example prompt starter:

"Use my app code + `standards-link-graph.yaml` to propose accessible code changes. For each recommendation, include: (a) relevant standard/spec node IDs, (b) edge IDs from the graph, and (c) whether the support is high or medium confidence."

## Start Here

If you are new to this repository:

1. Start with [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml)
2. Then open [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml)
3. Use [docs/link-graph-playbook.md](docs/link-graph-playbook.md) for query patterns and prompt templates
4. Use [docs/link-graph-reviewer-checklist.md](docs/link-graph-reviewer-checklist.md) for review/QA
5. For project implementation context, see:
	- [kitty-specs/001-wai-standards-yaml-ld-ingestion/spec.md](kitty-specs/001-wai-standards-yaml-ld-ingestion/spec.md)
	- [kitty-specs/001-wai-standards-yaml-ld-ingestion/plan.md](kitty-specs/001-wai-standards-yaml-ld-ingestion/plan.md)
	- [kitty-specs/001-wai-standards-yaml-ld-ingestion/quickstart.md](kitty-specs/001-wai-standards-yaml-ld-ingestion/quickstart.md)

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
- Accessibility rule catalogs (machine-readable ACT + Deque axe + Siteimprove Alfa): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/accessibility-rule-catalogs.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/accessibility-rule-catalogs.yaml)
- CSS specifications index (machine-readable, includes full inventory extracted from W3C CSS overview): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/css-specifications-index.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/css-specifications-index.yaml)
- HTML Living Standard accessibility index (machine-readable, includes full section inventory extracted from WHATWG source): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/html-living-standard-accessibility.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/html-living-standard-accessibility.yaml)
- Standards link graph (machine-readable relationships across WCAG/ATAG/UAAG/ARIA/HTML/CSS): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml)
- ATAG to WCAG 2.2 crosswalk: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml)

## JSON Schemas (for tooling/LLM validation)

- Standards index schema: [schemas/w3c-wai-standards.schema.json](schemas/w3c-wai-standards.schema.json)
- Shared informative catalog schema: [schemas/w3c-wai-informative-resources.schema.json](schemas/w3c-wai-informative-resources.schema.json)
- ARIA informative catalog schema: [schemas/wai-aria-informative.schema.json](schemas/wai-aria-informative.schema.json)
- CSS specifications index schema: [schemas/css-specifications-index.schema.json](schemas/css-specifications-index.schema.json)
- HTML Living Standard accessibility index schema: [schemas/html-living-standard-accessibility.schema.json](schemas/html-living-standard-accessibility.schema.json)
- Accessibility rule catalogs schema: [schemas/accessibility-rule-catalogs.schema.json](schemas/accessibility-rule-catalogs.schema.json)
- Standards link graph schema: [schemas/standards-link-graph.schema.json](schemas/standards-link-graph.schema.json)
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
- Manual artifact refresh workflow: [.github/workflows/refresh-standards-artifacts.yml](.github/workflows/refresh-standards-artifacts.yml)

Current schedule behavior:

- `W3C Standards Monitor` runs weekly (Mondays at 08:00 UTC) and on manual dispatch.
- `Refresh Standards Artifacts` runs quarterly (1st day of Jan/Apr/Jul/Oct at 08:15 UTC) and on manual dispatch.

The monitor checks watched TR headers (ETag/Last-Modified), uploads a report artifact, and opens an issue when changes are detected.

Watchlist coverage includes W3C standards pages and rule catalogs for ACT, Deque axe, and Siteimprove Alfa.

Run manually:

- Baseline refresh: `python scripts/monitor_w3c_sources.py --refresh --watchlist monitoring/w3c-tr-watchlist.json --report monitoring/w3c-change-report.md`
- Change check: `python scripts/monitor_w3c_sources.py --check --watchlist monitoring/w3c-tr-watchlist.json --report monitoring/w3c-change-report.md`

To refresh generated standards visualization artifacts without running locally, use GitHub Actions workflow dispatch for `Refresh Standards Artifacts`. It regenerates artifacts, uploads them as workflow artifacts, and opens a PR if files changed.

## Link Graph and Relationship Navigation

To understand how standards and datasets are linked:

- Canonical graph: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml)
- Derived edge CSV: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.edges.csv](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.edges.csv)
- Derived JSON-LD: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.jsonld](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.jsonld)
- Derived Mermaid graph: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.mmd](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.mmd)
- Relation-grouped Mermaid view: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.by-relation.mmd](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.by-relation.mmd)
- WCAG-centric Mermaid view (nearby graph neighborhood): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.wcag-centric.mmd](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.wcag-centric.mmd)
- Part-level Mermaid view (HTML/CSS parts to parent specs and WCAG): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.mmd](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.mmd)
- Part-level edge CSV: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.edges.csv](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.edges.csv)
- Granular WCAG SC crosswalk map (ATAG profile-based mentions): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/wcag-2.2-sc-crosswalk.mmd](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/wcag-2.2-sc-crosswalk.mmd)
- Granular WCAG SC crosswalk table: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/wcag-2.2-sc-crosswalk.csv](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/wcag-2.2-sc-crosswalk.csv)
- Interactive static viewer (filters by node/relation/confidence): [docs/standards-link-viewer.html](docs/standards-link-viewer.html)

Generate or refresh derived graph artifacts:

- `python scripts/generate_standards_link_graph.py --graph-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml --jsonld-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.jsonld --csv-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.edges.csv --mermaid-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.mmd`
- `python scripts/generate_standards_visualizations.py --graph-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml --html-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/html-living-standard-accessibility.yaml --css-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/css-specifications-index.yaml --by-relation-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.by-relation.mmd --wcag-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.wcag-centric.mmd --parts-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.mmd --parts-csv-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.edges.csv`
- `python scripts/generate_wcag_sc_crosswalk_map.py --crosswalk-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml --wcag-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.2-normative.yaml --mmd-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/wcag-2.2-sc-crosswalk.mmd --csv-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/wcag-2.2-sc-crosswalk.csv`
- `python scripts/refresh_accessibility_rule_catalogs.py --out-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/accessibility-rule-catalogs.yaml`

Open the interactive viewer locally:

- `python -m http.server 8000`
- Visit `http://localhost:8000/docs/standards-link-viewer.html`

## Governance and Maintenance Docs

- Maintenance baseline: [kitty-specs/001-wai-standards-yaml-ld-ingestion/maintenance-baseline.md](kitty-specs/001-wai-standards-yaml-ld-ingestion/maintenance-baseline.md)
- Normative refresh procedure: [kitty-specs/001-wai-standards-yaml-ld-ingestion/normative-refresh-procedure.md](kitty-specs/001-wai-standards-yaml-ld-ingestion/normative-refresh-procedure.md)
- Informative catalog governance: [kitty-specs/001-wai-standards-yaml-ld-ingestion/informative-catalog-governance.md](kitty-specs/001-wai-standards-yaml-ld-ingestion/informative-catalog-governance.md)
- Link graph playbook (human + LLM navigation): [docs/link-graph-playbook.md](docs/link-graph-playbook.md)
- Link graph reviewer checklist (one-page quick-reference): [docs/link-graph-reviewer-checklist.md](docs/link-graph-reviewer-checklist.md)
- Accessibility agent contract (AGENTS.md + ACCESSIBILITY.md integration): [docs/accessibility-agent-contract.md](docs/accessibility-agent-contract.md)

## Repository Hygiene

Local machine/runtime files are ignored by [.gitignore](.gitignore), including local agent directories and local `.kittify` runtime metadata.
