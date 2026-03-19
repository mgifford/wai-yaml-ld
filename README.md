# wai-yaml-ld

> ⚠️ **EXPERIMENTAL — Validation Required**
>
> **This project is still experimental. Most of this site was generated with AI and has not yet been validated in real-world settings.** All content must be treated as a starting point only — not as authoritative or production-ready guidance.
>
> **Impacts may vary** based on where and how it is implemented. Do not rely on this data without independent verification against the original W3C standards.
>
> **People with experience conducting studies on the accessibility impact and cost of AI cycles should be involved** before any significant implementation decisions are made.
>
> **We need your feedback.** If you have positive or negative results from trying this project, please [open an issue](https://github.com/mgifford/wai-yaml-ld/issues). Provide links and references so claims can be discussed and validated by the community.

Machine-readable accessibility standards context for AI coding systems.

This repository turns key W3C WAI + related standards (WCAG, ATAG, UAAG, ARIA, HTML, CSS) into structured YAML/JSON-LD/CSV artifacts that an LLM can reliably consume when generating or reviewing code.

GitHub Pages landing page:

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
- Cross-standard references (direct + inferred SC links and informative resource links): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml)
- Cross-standard references table: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.csv](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.csv)

## Cognitive Resources

- Cognitive patterns crosswalk: [cognitive_patterns.yaml](cognitive_patterns.yaml)
- Cognitive implementation guide: [COGNITIVE_GUIDE.md](COGNITIVE_GUIDE.md)
- Canonical supplemental cognitive mapping: [supplemental_guidance.yaml](supplemental_guidance.yaml)
- Related personas for cognitive context: [personas.yaml](personas.yaml)

Primary W3C references used by these resources:

- Supplemental Guidance to WCAG 2: https://www.w3.org/WAI/WCAG2/supplemental/
- Supplemental cognitive patterns: https://www.w3.org/WAI/WCAG2/supplemental/#patterns
- WCAG 2.2 Recommendation: https://www.w3.org/TR/WCAG22/
- Understanding WCAG 2.2: https://www.w3.org/WAI/WCAG22/Understanding/

## JSON Schemas (for tooling/LLM validation)

- Standards index schema: [schemas/w3c-wai-standards.schema.json](schemas/w3c-wai-standards.schema.json)
- Shared informative catalog schema: [schemas/w3c-wai-informative-resources.schema.json](schemas/w3c-wai-informative-resources.schema.json)
- ARIA informative catalog schema: [schemas/wai-aria-informative.schema.json](schemas/wai-aria-informative.schema.json)
- CSS specifications index schema: [schemas/css-specifications-index.schema.json](schemas/css-specifications-index.schema.json)
- HTML Living Standard accessibility index schema: [schemas/html-living-standard-accessibility.schema.json](schemas/html-living-standard-accessibility.schema.json)
- Accessibility rule catalogs schema: [schemas/accessibility-rule-catalogs.schema.json](schemas/accessibility-rule-catalogs.schema.json)
- Standards link graph schema: [schemas/standards-link-graph.schema.json](schemas/standards-link-graph.schema.json)
- Crosswalk schema: [schemas/atag-to-wcag-2.2-crosswalk.schema.json](schemas/atag-to-wcag-2.2-crosswalk.schema.json)
- Cross-standard references schema: [schemas/cross-standard-references.schema.json](schemas/cross-standard-references.schema.json)

If you are pointing an LLM at this repository, provide both the target YAML file and its matching schema file as context.

## Why These Live Under research/

For this repository phase, these are curated specification datasets and governance outputs generated under the feature directory. Keeping them under `research/` keeps all ingestion artifacts together and tied to spec/plan/tasks.

If this repository later publishes a stable external data package, create a promoted location (for example `datasets/wai/`) and keep `research/` as the change-staging source.

## Monitoring W3C Standard Changes

Monitoring is now set up with:

- Watchlist baseline: [monitoring/w3c-tr-watchlist.json](monitoring/w3c-tr-watchlist.json)
- Monitor script: [scripts/monitor_w3c_sources.py](scripts/monitor_w3c_sources.py)
- Scheduled GitHub Action: [.github/workflows/w3c-standards-monitor.yml](.github/workflows/w3c-standards-monitor.yml)
- Weekly resource link/freshness checker: [.github/workflows/weekly-resource-link-check.yml](.github/workflows/weekly-resource-link-check.yml)
- Manual artifact refresh workflow: [.github/workflows/refresh-standards-artifacts.yml](.github/workflows/refresh-standards-artifacts.yml)

Current schedule behavior:

- `W3C Standards Monitor` runs weekly (Mondays at 08:00 UTC) and on manual dispatch.
- `Weekly Resource Link Check` runs weekly (Mondays at 08:30 UTC) and on manual dispatch.
- `Refresh Standards Artifacts` runs quarterly (1st day of Jan/Apr/Jul/Oct at 08:15 UTC) and on manual dispatch.

`Weekly Resource Link Check` includes an auto-normalization pass that attempts safe replacements for dated W3C TR snapshot URLs and opens a PR when changes are available.

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
- Cross-standard reference dataset (direct citation + inferred mapping + informative applies_to): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml)
- Cross-standard reference CSV: [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.csv](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.csv)
- Cross-standard reference Mermaid (full): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.mmd](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.mmd)
- Cross-standard Mermaid (ATAG → WCAG SC): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.atag-wcag.mmd](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.atag-wcag.mmd)
- Cross-standard Mermaid (informative → standard): [kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.informative.mmd](kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.informative.mmd)
- Interactive static viewer (filters by node/relation/confidence): [docs/standards-link-viewer.html](docs/standards-link-viewer.html)

Generate or refresh derived graph artifacts:

- `python scripts/generate_standards_link_graph.py --graph-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml --jsonld-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.jsonld --csv-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.edges.csv --mermaid-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.mmd`
- `python scripts/generate_standards_visualizations.py --graph-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml --html-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/html-living-standard-accessibility.yaml --css-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/css-specifications-index.yaml --by-relation-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.by-relation.mmd --wcag-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-graph.wcag-centric.mmd --parts-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.mmd --parts-csv-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/standards-link-parts.edges.csv`
- `python scripts/generate_wcag_sc_crosswalk_map.py --crosswalk-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml --wcag-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.2-normative.yaml --mmd-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/wcag-2.2-sc-crosswalk.mmd --csv-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/wcag-2.2-sc-crosswalk.csv`
- `python scripts/generate_cross_standard_references.py --wcag22-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.2-normative.yaml --wcag20-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.0-normative.yaml --atag-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-2.0-normative.yaml --uaag-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/uaag-2.0-normative.yaml --crosswalk-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml --informative-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml --out-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml --out-csv kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.csv`
- `python scripts/generate_cross_standard_reference_views.py --dataset-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml --full-mmd-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.mmd --atag-wcag-mmd-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.atag-wcag.mmd --informative-mmd-out kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.informative.mmd`
- `python scripts/refresh_accessibility_rule_catalogs.py --out-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/accessibility-rule-catalogs.yaml`

Query examples for cross-standard references:

- Inferred ATAG → WCAG SC links: `python scripts/query_cross_standard_references.py --dataset-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml --source-standard atag-2.0 --target-standard wcag-2.2 --relation-type inferred_sc_reference_cross_standard --format table --limit 25`
- Informative resources that reference WCAG: `python scripts/query_cross_standard_references.py --dataset-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml --relation-type informative_resource_reference_standard --target-standard wcag-2.2 --format table --limit 25`

Open the interactive viewer locally:

- `python -m http.server 8000`
- Visit `http://localhost:8000/docs/standards-link-viewer.html`

## Governance and Maintenance Docs

 - Reference integrity governance spec: [kitty-specs/002-reference-integrity-governance/spec.md](kitty-specs/002-reference-integrity-governance/spec.md)
 - Reference integrity implementation plan: [kitty-specs/002-reference-integrity-governance/plan.md](kitty-specs/002-reference-integrity-governance/plan.md)

 Cross-standard integrity validation command:

 - `python scripts/validate_cross_standard_references.py --dataset-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml --wcag22-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.2-normative.yaml --wcag20-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.0-normative.yaml --atag-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-2.0-normative.yaml --uaag-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/uaag-2.0-normative.yaml --crosswalk-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml --informative-yaml kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml`

## Repository Hygiene

Local machine/runtime files are ignored by [.gitignore](.gitignore), including local agent directories and local `.kittify` runtime metadata.

## Similar efforts to provide machine-focused direction
- https://www.last-child.com/build-ai-brain-a11y.html
- https://github.com/mikemai2awesome/agent-skills/tree/main
- https://github.com/mikemai2awesome/a11y-rules

## Static GraphQL-style API (GitHub Pages)

This repository now includes a static API build pipeline that converts the YAML/YAML-LD datasets into small JSON endpoints designed for AI agents.

> Experimental: GraphQL support is currently GraphQL-style/static (schema + introspection + resolver-like JSON endpoints). Different LLMs and toolchains may or may not use this library directly.

### Build locally

- Install dependencies: `npm install`
- Generate static API: `npm run build:api`

Generated output:

- `dist/api/v1/sc/all.json`
- `dist/api/v1/sc/{ref-id}.json` (example: `dist/api/v1/sc/1-1-1.json`)
- `dist/api/v1/guidelines/all.json`
- `dist/api/v1/schema.graphql`
- `dist/api/v1/introspection.json`

Published URL pattern (after deploy):

- `https://mgifford.github.io/wai-yaml-ld/api/index.json`
- `https://mgifford.github.io/wai-yaml-ld/api/v1/sc/all.json`
- `https://mgifford.github.io/wai-yaml-ld/api/v1/sc/1-1-1.json`
- `https://mgifford.github.io/wai-yaml-ld/api/v1/introspection.json`

### Why this is useful for AI accessibility review

- Map code to specific Success Criteria (example: “This button lacks an `aria-label`, violating SC 4.1.2”).
- Explain the “why” by tracing relationships from a WCAG failure node back to related ATAG requirements.
- Provide auditable evidence: recommendations can cite linked standards records instead of vague best-practice language.
- Shift accessibility guidance from article-style prose to structured, standards-aligned technical data.

### How to test the GraphQL support

Because this is a static API, test it in a discovery-first flow:

1. Inspect schema shape:
	- Open `https://mgifford.github.io/wai-yaml-ld/api/v1/schema.graphql`
2. Inspect introspection:
	- Open `https://mgifford.github.io/wai-yaml-ld/api/v1/introspection.json`
3. Resolve equivalent query targets via GET:
	- All SCs: `https://mgifford.github.io/wai-yaml-ld/api/v1/sc/all.json`
	- Specific SC: `https://mgifford.github.io/wai-yaml-ld/api/v1/sc/4-1-2.json`
4. Validate traceability fields in payloads:
	- `parentGuideline`, `sufficientTechniques`, `advisoryTechniques`, `failures`

CLI smoke test example:

```bash
curl -s https://mgifford.github.io/wai-yaml-ld/api/v1/introspection.json | head -n 20
curl -s https://mgifford.github.io/wai-yaml-ld/api/v1/sc/4-1-2.json | jq '.ref_id, .title, .failures | length'
```

### What the builder does

- Parses all `.yaml`/`.yml` files in the repository
- Preserves linked-data style identifiers (`@id`/`@type`) when present and builds a linked-data index
- Generates static resolver-like JSON files for common query patterns
- Joins WCAG success criteria with related rule-based techniques/failures and guideline references
- Emits GraphQL schema and standard introspection JSON for tool discovery

### CI/CD deploy

Workflow file: `.github/workflows/deploy-api.yml`

- Triggers on push to `main`
- Runs `npm install` and `npm run build:api`
- Deploys `dist/` to `gh-pages`

## MCP integration

For Model Context Protocol clients, use `mcp-config.json` and `mcp-bridge.js`.

### One-click Codespaces setup

- Automatic in Codespaces via [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json): first launch runs `npm run setup` and each startup runs `npm run codespace:hint` to print key API URLs
- Run: `npm run setup`
- Start bridge: `npm run mcp:bridge`

`mcp-config.json` points your MCP client to `mcp-bridge.js`, which fetches:

- Criterion endpoint: `/api/v1/sc/{id}.json`
- Schema discovery: `/api/v1/introspection.json`

This lets AI tools discover schema shape first, then fetch only the specific criterion/technique payloads they need.

## AI Disclosure

This section documents which AI tools were used in building, maintaining, and running this project.

### Building the Project

**GitHub Copilot (SWE Agent)**
Used to generate the initial project plan and scaffold the repository content, including YAML data files, JSON schemas, Python scripts, and documentation. The `copilot-swe-agent[bot]` account created the first commit. Subsequent AI-assisted contributions by this agent are also reflected in the commit history.

**GitHub Copilot (Coding Agent)**
Used to implement features and tasks throughout the project lifecycle, including adding new standards data, regenerating derived artifacts, and updating documentation. The Coding Agent operates under the same `copilot-swe-agent[bot]` account as the SWE Agent; commits by that account in the git history reflect contributions from both.

### Running the Project

**LLMs as data consumers (user-supplied)**
This project is designed to be consumed by any LLM the user chooses. When following the recommended flow (see [How To Use With an LLM](#how-to-use-with-an-llm-recommended-flow)), users supply their own LLM. No specific LLM is bundled or required to run the project. The YAML/JSON-LD/CSV artifacts are LLM-agnostic.

**MCP-compatible AI tools (optional, user-configured)**
The MCP bridge (`mcp-bridge.js`, `mcp-config.json`) enables MCP-compatible AI coding tools - such as GitHub Copilot, Claude, or others - to discover and query the static API endpoints at runtime. This is opt-in and requires the user to configure their own MCP client. No browser-based AI is required or automatically enabled.

### Browser-based AI

No browser-based AI is automatically enabled or required to use this project. The interactive viewer (`docs/standards-link-viewer.html`) and other static pages are plain HTML/JavaScript with no embedded AI. Users may choose to run browser extensions or browser-native AI features on their own.

### What Has Not Been Used

No AI model training or fine-tuning has been performed on this project's data. No OpenAI, Anthropic, or Google Cloud AI APIs are called by any script, workflow, or build step in this repository. No AI-generated content is served to end users without being reviewed and committed to the repository first.

> If you use an AI tool to contribute to this project, please add your tool to this section following the format above. See [`.kittify/AGENTS.md`](.kittify/AGENTS.md) for the full AI Disclosure rule.
