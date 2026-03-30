# GitHub Copilot Agent Instructions

## Agent Rules

All AI agents working in this repository must read [`AGENTS.md`](../AGENTS.md) first. It contains the primary agent instructions for this repository. Additional project-level rules live in [`.kittify/AGENTS.md`](../.kittify/AGENTS.md). Key rules include:

- Always use absolute or project-root-relative paths when referencing files or directories.
- Use only UTF-8 compatible characters in all files (no smart quotes, em dashes, or Windows-1252 characters).
- Commit only meaningful units of work with descriptive, imperative-mood commit messages.
- Never commit agent runtime directories (`.claude/`, `.codex/`, `.gemini/`, etc.) or secrets.

## What This Repository Is

`wai-yaml-ld` turns W3C WAI accessibility standards (WCAG, ATAG, UAAG, ARIA, HTML, CSS) into structured YAML/JSON-LD/CSV artifacts that LLMs can reliably consume when generating or reviewing code.

> **EXPERIMENTAL**: Most content was AI-generated and has not been validated in production settings. Treat it as a starting point only.

## Key Files and Directories

### Primary Data Files

| File | Purpose |
|------|---------|
| `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml` | Standards catalog (primary LLM entrypoint) |
| `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml` | Cross-standard relationship graph |
| `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml` | Informative resources catalog |
| `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.2-normative.yaml` | WCAG 2.2 normative content |
| `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml` | ATAG-to-WCAG crosswalk |
| `kitty-specs/001-wai-standards-yaml-ld-ingestion/research/derived/cross-standard-references.yaml` | Derived cross-standard references |

### Schemas (for validation)

All YAML files have matching JSON schemas in `schemas/`. Always provide both a YAML file and its schema when pointing an LLM at this repository.

### Documentation

| File | Purpose |
|------|---------|
| `README.md` | Project overview, data files index, and LLM usage guide |
| `TUTORIALS.md` | Usage tutorials |
| `COGNITIVE_GUIDE.md` | Cognitive accessibility patterns and datasets |
| `docs/link-graph-playbook.md` | Query patterns and prompt templates |
| `docs/link-graph-reviewer-checklist.md` | Review/QA checklist |
| `docs/w3c-standards-alignment.md` | W3C standards alignment analysis |
| `docs/accessibility-agent-contract.md` | Accessibility contract for agents |

### Specs and Plans

Implementation specs live in `kitty-specs/`. Each feature directory contains `spec.md`, `plan.md`, `tasks.md`, and a `tasks/` subdirectory with work-package files.

### Scripts

Python utility scripts in `scripts/`:

- `generate_cross_standard_references.py` - Regenerate cross-standard reference artifacts
- `generate_standards_link_graph.py` - Regenerate standards link graph
- `validate_standards_graph.py` - Validate the graph
- `validate_cross_standard_references.py` - Validate cross-standard references
- `monitor_w3c_sources.py` - Monitor W3C source changes
- `check_resource_links.py` - Check resource link freshness

## Development Workflow

### Build

```bash
npm install
npm run build:api   # builds static GraphQL-style API artifacts into dist/
```

### Adding or Modifying Standards

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

### CI Workflows

| Workflow | Purpose |
|----------|---------|
| `.github/workflows/standards-link-graph-validate.yml` | Validate standards link graph on push/PR |
| `.github/workflows/refresh-standards-artifacts.yml` | Manual artifact refresh |
| `.github/workflows/w3c-standards-monitor.yml` | Scheduled W3C standard change monitoring |
| `.github/workflows/daily-resource-link-check.yml` | Daily resource link/freshness check |
| `.github/workflows/deploy-api.yml` | Deploy API to GitHub Pages |

## Data Model Conventions

- Standards entries use fields: `id`, `name`, `url`, `type`, `format_hint`
- When adding a standard to `w3c-wai-standards.yaml`, also add nodes to `standards-link-graph.yaml` and create relationship edges
- YAML files must pass their matching JSON Schema validation before merging

## Encoding Requirements

Use only UTF-8 characters. Avoid smart quotes, em/en dashes, Unicode arrows, and copy-pasted content from Microsoft Office (see the safe vs. unsafe character table below).

Run `spec-kitty validate-encoding --all --fix` to detect and auto-repair encoding issues.

### Safe vs. Unsafe Characters

| Avoid | Use Instead |
|-------|------------|
| Left/right double quotes (U+201C, U+201D) | Standard ASCII `"` |
| Left/right single quotes (U+2018, U+2019) | Standard ASCII `'` |
| Em dash (U+2014) or en dash (U+2013) | ASCII hyphen `-` |
| Unicode right arrow (U+2192) | ASCII `->` |
| Multiplication sign (U+00D7) | Lowercase `x` |
| Plus-minus sign (U+00B1) | `+/-` |
| Degree symbol (U+00B0) | `degrees` |
