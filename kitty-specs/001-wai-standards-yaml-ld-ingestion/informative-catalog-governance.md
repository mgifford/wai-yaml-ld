# Informative Catalog Governance and Curation

Feature: `001-wai-standards-yaml-ld-ingestion`

This document defines repeatable governance for informative resource curation across:

- `research/w3c-wai-informative-resources.yaml`
- `research/wai-aria-informative.yaml`
- visibility subset in `research/w3c-wai-standards.yaml`

## 1) Admission and Classification Rules (T008)

### Admission criteria

A new resource may be added when at least one is true:

- It is directly requested by project stakeholders.
- It supports implementation of normative standards already in scope.
- It provides ecosystem context needed for conformance interpretation (for example APG, AAM, ACT format guidance).

### Classification rules

- Use `type: informative` for guidance, supporting notes, and contextual resources.
- Use `type: standard` in informative catalogs only when the resource is a formal TR specification linked as reference context.
- Use `type: technical_spec` in `w3c-wai-standards.yaml` for technical spec visibility entries.
- Keep normative success criteria only in `*-normative.yaml` files.

## 2) Coverage Checklist for Required Resource Families (T009)

Required families:

- APG: `aria-apg-home`, `aria-apg-patterns`, `aria-apg-examples`
- AAM and related technical specs: `core-aam-1.2`, `html-aam-1.0`, `svg-aam-1.0`, `html-aria`, `accname-1.2`
- EPUB: `epub-a11y-1.1`, `epub-a11y-tech-1.1`
- Sustainability: `web-sustainability-guidelines`
- ACT: `act-rules-format-1.1`, `act-rules-format-1.0`, `act-rules-format-latest`

Verification command:

```bash
python - <<'PY'
from pathlib import Path

required = {
  'aria-apg-home','aria-apg-patterns','aria-apg-examples',
  'core-aam-1.2','html-aam-1.0','svg-aam-1.0','html-aria','accname-1.2',
  'epub-a11y-1.1','epub-a11y-tech-1.1',
  'web-sustainability-guidelines',
  'act-rules-format-1.1','act-rules-format-1.0','act-rules-format-latest'
}

base = Path('kitty-specs/001-wai-standards-yaml-ld-ingestion/research')
shared = (base / 'w3c-wai-informative-resources.yaml').read_text()
aria = (base / 'wai-aria-informative.yaml').read_text()
index = (base / 'w3c-wai-standards.yaml').read_text()

missing_shared = sorted([rid for rid in required if f"id: {rid}" not in shared])
missing_aria = sorted([rid for rid in required if f"id: {rid}" not in aria])
visibility_required = {
  'aria-apg-home','aria-apg-patterns','aria-apg-examples',
  'core-aam-1.2','html-aam-1.0','svg-aam-1.0','html-aria','accname-1.2',
  'epub-a11y-1.1','epub-a11y-tech-1.1','web-sustainability-guidelines'
}
missing_index = sorted([rid for rid in visibility_required if f"id: {rid}" not in index])

print('missing_shared', missing_shared)
print('missing_aria', missing_aria)
print('missing_index_visibility', missing_index)
print('ok', not missing_shared and not missing_aria and not missing_index)
PY
```

Expected outcome:

- `missing_shared []`
- `missing_aria []`
- `missing_index_visibility []`
- `ok True`

## 3) Stable ID Policy (T010)

### ID format

- Lowercase kebab-case.
- Prefer semantic slugs containing version when applicable (for example `core-aam-1.2`).
- For rolling specs, use explicit `-latest` suffix (for example `act-rules-format-latest`).

### Uniqueness and stability

- IDs are immutable once published in repository history.
- Do not repurpose an existing ID for a different URL or concept.
- If URL target changes materially, create a new ID and keep old entry only if needed for backward compatibility.

### Duplicate prevention

- Before adding a resource, search all feature catalogs for the candidate ID and URL.
- If the resource already exists, update `applies_to` or visibility metadata instead of creating a duplicate.

## 4) Review and Commit Checklist

- [ ] Admission criteria satisfied and documented in PR/commit rationale
- [ ] Classification (`informative`, `standard`, `technical_spec`) is appropriate for file context
- [ ] ID follows stable ID policy and is not duplicated
- [ ] Required resource-family coverage check passes
- [ ] Editor diagnostics show no file errors