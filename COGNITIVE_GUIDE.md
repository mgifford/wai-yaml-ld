# Cognitive Accessibility Guide

This guide summarizes cognitive-focused supplemental accessibility patterns and links them to the project’s machine-readable datasets.

## Primary Sources

- W3C Supplemental Guidance to WCAG 2: https://www.w3.org/WAI/WCAG2/supplemental/
- W3C Cognitive Patterns index: https://www.w3.org/WAI/WCAG2/supplemental/#patterns
- WCAG 2.2 Recommendation: https://www.w3.org/TR/WCAG22/
- Understanding WCAG 2.2: https://www.w3.org/WAI/WCAG22/Understanding/

## Project Data Links

- Canonical cognitive dataset: [supplemental_guidance.yaml](supplemental_guidance.yaml)
- Cognitive crosswalk index: [cognitive_patterns.yaml](cognitive_patterns.yaml)
- Related personas: [personas.yaml](personas.yaml)
- Related workflows: [workflows.yaml](workflows.yaml)
- Related tutorial guidance: [TUTORIALS.md](TUTORIALS.md)

## Objective O1 — Help users understand what things are and how to use them

### Why it matters
Users with cognitive and learning disabilities benefit from predictable structures and clearly labeled actions.

### Patterns
- Make the purpose of each page clear.
- Use a familiar hierarchy and design.
- Clearly identify controls and their use.

### Typical WCAG linkages
- 1.3.1, 2.4.6, 3.2.4, 3.3.2

## Objective O3 — Use clear and understandable content

### Why it matters
Complex or ambiguous language increases cognitive load and lowers comprehension.

### Patterns
- Use clear words and literal language.
- Keep text succinct.
- Provide summaries for long content.

### Typical WCAG linkages
- 3.1.5, 3.3.2, 3.3.5

## Objective O4 — Help users avoid mistakes and recover from them

### Why it matters
Error prevention and recovery significantly improve completion rates for forms and multi-step processes.

### Patterns
- Design forms to prevent mistakes.
- Allow users to go back and undo.
- Avoid unexpected movement of controls.

### Typical WCAG linkages
- 3.3.1, 3.3.3, 3.3.4, 3.3.7

## Objective O6 — Ensure processes do not rely on memory

### Why it matters
Memory-intensive interactions (including login and multi-step confirmation) create avoidable barriers.

### Patterns
- Provide login approaches that reduce memory burden.
- Allow simple, single-step alternatives.
- Do not rely on user calculations or memorized intermediates.

### Typical WCAG linkages
- 2.2.1, 3.3.7, 3.3.8

## Usage Notes

- Treat this guide as interpretive and implementation-oriented, not normative text.
- Use [supplemental_guidance.yaml](supplemental_guidance.yaml) for structured ingestion and [cognitive_patterns.yaml](cognitive_patterns.yaml) for objective/pattern crosswalking.