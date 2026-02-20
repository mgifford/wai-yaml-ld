# Normative Refresh Procedure: WCAG, ATAG, UAAG, and Crosswalk

Feature: `001-wai-standards-yaml-ld-ingestion`

This procedure defines how to refresh normative criteria files while preserving WCAG policy semantics and ATAG -> WCAG 2.2 crosswalk consistency.

## Scope

- `research/wcag-2.2-normative.yaml`
- `research/wcag-2.0-normative.yaml` (legacy)
- `research/atag-2.0-normative.yaml`
- `research/uaag-2.0-normative.yaml`
- `research/atag-to-wcag-2.2-crosswalk.yaml`
- `research/w3c-wai-standards.yaml`

## Policy Guardrails (T004, T007)

Keep these statements synchronized after any refresh:

- `w3c-wai-standards.yaml` remains WCAG 2.2 primary (`primary_wcag_version: '2.2'`)
- WCAG 2.0 remains legacy/provenance
- Explicit SC 4.1.1 exclusion behavior remains documented for WCAG 2.2 cumulative handling
- ATAG normative wording is preserved; only linkage metadata translates WCAG version semantics

## Refresh Order (T006)

1. Update `w3c-wai-standards.yaml` source metadata when TR references change.
2. Refresh normative criteria files (WCAG 2.2 first, then WCAG 2.0 legacy, ATAG, UAAG).
3. Reconcile and refresh `atag-to-wcag-2.2-crosswalk.yaml` target profile references and mapping metadata.
4. Re-run all consistency checks before commit.

## Dedupe and Exclusion Rules (T007)

### WCAG 2.2 criteria safeguards

- `code` values in `wcag-2.2-normative.yaml` must be unique.
- `4.1.1` must not appear in WCAG 2.2 normative criteria.
- Duplicated success criteria entries are not allowed.

### Crosswalk safeguards

- `policy.explicit_exception_rule.excluded_wcag_codes` must include `4.1.1`.
- `target_profiles.*.criterion_codes` must not contain `4.1.1`.
- `mapping_count` must equal the number of mapping entries.

## Consistency Verification (T005)

Run from repo root:

```bash
# Crosswalk mapping_count consistency
python - <<'PY'
from pathlib import Path
import re
s = Path('kitty-specs/001-wai-standards-yaml-ld-ingestion/research/atag-to-wcag-2.2-crosswalk.yaml').read_text()
entries = len(re.findall(r'^- atag_criterion_code:', s, flags=re.M))
declared = re.search(r'^mapping_count:\s*(\d+)', s, flags=re.M)
print('mapping_entries', entries)
print('mapping_count', declared.group(1) if declared else 'missing')
PY

# WCAG 2.2 dedupe and 4.1.1 exclusion check
python - <<'PY'
from pathlib import Path
import re
from collections import Counter
s = Path('kitty-specs/001-wai-standards-yaml-ld-ingestion/research/wcag-2.2-normative.yaml').read_text()
codes = re.findall(r'^\s*code:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$', s, flags=re.M)
c = Counter(codes)
dups = [k for k,v in c.items() if v > 1]
print('code_count', len(codes))
print('unique_count', len(c))
print('contains_4_1_1', '4.1.1' in c)
print('duplicates', dups)
PY
```

Expected outcomes:

- `mapping_entries == mapping_count`
- `contains_4_1_1` is `False`
- `duplicates` is empty

## Commit Checklist

- [ ] Policy notes synchronized across index/normative/crosswalk files
- [ ] No duplicated WCAG 2.2 criteria codes
- [ ] 4.1.1 exclusion behavior preserved and explicit
- [ ] Crosswalk `mapping_count` verified against mappings
- [ ] Editor diagnostics report no errors for edited files