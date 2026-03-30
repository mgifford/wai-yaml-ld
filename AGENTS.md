# AGENTS.md

Instructions for AI coding agents working in this repository.
See also `.kittify/AGENTS.md` for full project-level agent rules (encoding, git discipline, AI disclosure, etc.).

---

## What This Repository Is

`wai-yaml-ld` turns W3C WAI accessibility standards (WCAG, ATAG, UAAG, ARIA, HTML, CSS) into structured YAML/JSON-LD/CSV artifacts that LLMs can reliably consume when generating or reviewing code.

> **EXPERIMENTAL**: Most content was AI-generated and has not been validated in production settings. Treat it as a starting point only.

---

## Build and Setup

```bash
npm install
npm run build:api   # builds static GraphQL-style API artifacts into dist/
```

Requires Node.js >= 20.

---

## Validation Scripts

```bash
python scripts/validate_standards_graph.py
python scripts/validate_cross_standard_references.py
```

---

## Key Files and Directories

| Path | Purpose |
|------|---------|
| `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml` | Standards catalog - primary LLM entrypoint |
| `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml` | Cross-standard relationship graph |
| `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml` | Informative resources catalog |
| `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.2-normative.yaml` | WCAG 2.2 normative content |
| `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml` | ATAG-to-WCAG crosswalk |
| `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml` | Derived cross-standard references |
| `schemas/` | JSON schemas for validating every YAML data file |
| `scripts/` | Python utilities to regenerate and validate artifacts |
| `docs/` | Documentation, playbooks, and reviewer checklists |
| `kitty-specs/` | Implementation specs, plans, and task work packages |

---

## Adding or Modifying Standards

1. Edit `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml`
2. Add nodes and edges to `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml`
3. Regenerate derived artifacts:
   ```bash
   python scripts/generate_cross_standard_references.py
   python scripts/generate_standards_link_graph.py
   ```
4. Validate:
   ```bash
   python scripts/validate_standards_graph.py
   python scripts/validate_cross_standard_references.py
   ```

---

## Data Model Conventions

- Standards entries use fields: `id`, `name`, `url`, `type`, `format_hint`
- When adding a standard to `w3c-wai-standards.yaml`, also add nodes to `standards-link-graph.yaml` and create relationship edges
- Every YAML file must pass its matching JSON Schema in `schemas/` before merging

---

## Encoding Requirements

Use only UTF-8 characters. Avoid smart quotes, em/en dashes, Unicode arrows, and content copy-pasted from Microsoft Office.

| Avoid | Use Instead |
|-------|------------|
| Left/right double quotes (U+201C, U+201D) | Standard ASCII `"` |
| Left/right single quotes (U+2018, U+2019) | Standard ASCII `'` |
| Em dash (U+2014) or en dash (U+2013) | ASCII hyphen `-` |
| Unicode right arrow (U+2192) | ASCII `->` |
| Multiplication sign (U+00D7) | Lowercase `x` |

---

## CI Workflows

| Workflow | Purpose |
|----------|---------|
| `.github/workflows/standards-link-graph-validate.yml` | Validate standards link graph on push/PR |
| `.github/workflows/refresh-standards-artifacts.yml` | Manual artifact refresh |
| `.github/workflows/w3c-standards-monitor.yml` | Scheduled W3C standard change monitoring |
| `.github/workflows/daily-resource-link-check.yml` | Daily resource link/freshness check |
| `.github/workflows/deploy-api.yml` | Deploy API to GitHub Pages |

---

## AI Disclosure Rule

Whenever an AI agent contributes meaningfully to this repository, it must disclose its participation in the `AI Disclosure` section of `README.md`. If that section does not exist, create it.
