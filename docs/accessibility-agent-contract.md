# Accessibility Agent Contract (Minimal)

Use this when wiring an external `AGENTS.md` and `ACCESSIBILITY.md` to this repository.

## Goal

- Reduce unsupported accessibility claims by forcing retrieval from curated standards artifacts.
- Improve advice quality by requiring standards traceability for each recommendation.

## Integration Pattern

1. `AGENTS.md` points to `ACCESSIBILITY.md` as the policy for accessibility answers.
2. `ACCESSIBILITY.md` points to this repository's machine-readable sources.
3. The agent follows decision rules: retrieve first, then answer with evidence, else return uncertainty.

## Copy-Ready `AGENTS.md` Snippet

```md
## Accessibility Policy

For accessibility guidance, follow `ACCESSIBILITY.md` in this repository.
Do not provide normative claims from memory when retrievable standards context is available.
If evidence is missing, state uncertainty and request/locate the missing source.
```

## Copy-Ready `ACCESSIBILITY.md` Snippet

```md
# Accessibility Guidance Policy

## Required Sources (retrieve before answering)

1. Standards graph:
   - https://github.com/mgifford/wai-yaml-ld/blob/main/kitty-specs/001-wai-standards-yaml-ld-ingestion/research/standards-link-graph.yaml
2. Standards index:
   - https://github.com/mgifford/wai-yaml-ld/blob/main/kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-standards.yaml
3. Informative catalog:
   - https://github.com/mgifford/wai-yaml-ld/blob/main/kitty-specs/001-wai-standards-yaml-ld-ingestion/research/w3c-wai-informative-resources.yaml
4. Matching schemas for validation:
   - https://github.com/mgifford/wai-yaml-ld/blob/main/schemas/standards-link-graph.schema.json
   - https://github.com/mgifford/wai-yaml-ld/blob/main/schemas/w3c-wai-standards.schema.json
   - https://github.com/mgifford/wai-yaml-ld/blob/main/schemas/w3c-wai-informative-resources.schema.json

## Decision Rules

1. Retrieve relevant nodes/edges/resources first.
2. For each recommendation, include traceability:
   - standard/spec IDs
   - edge or relation used
   - confidence (`high` or `medium`)
3. Separate normative vs informative references in output.
4. If no source supports a claim, do not assert it as fact.

## Output Contract

Return two blocks:

1. Proposed implementation guidance
2. Standards traceability table

Traceability table columns:
- `recommendation`
- `source_ids`
- `relation_or_edge`
- `confidence`
- `notes`
```

## Prompt Pattern for Code Reviews

```text
Review this change for accessibility.
Use project code + retrieved standards context.
For each issue or recommendation, include:
- source IDs
- relation/edge used
- confidence
If evidence is missing, mark as uncertain.
```

## Why This Reduces Hallucinations

- Narrows the answer space to curated, versioned standards data.
- Converts free-form reasoning into evidence-constrained reasoning.
- Makes unsupported claims visible because every claim must map to source IDs and relations.

## Limits (Important)

- This reduces but does not eliminate hallucinations.
- Prompt quality and retrieval quality still determine outcomes.
- Advice quality drops when relevant project code or standards artifacts are not in context.
