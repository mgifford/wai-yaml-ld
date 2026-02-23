# Accessibility Tutorials (Interpretive)

Source base: WAI Tutorials content captured in `compiled w3c documents.pdf` (notably pages around 323–325, 501–502, 534–535).

## Images

### Why is this important?
Images communicate meaning, status, and actions. Without text alternatives, users of screen readers, text-only views, or constrained contexts miss critical information and functionality.

### User Experience
- Informative images include short alternatives that preserve the key takeaway.
- Decorative images use null alternatives so assistive tech can skip noise.
- Functional images describe destination or action, not just appearance.
- Complex images pair concise alternatives with nearby longer descriptions.

## Tables

### Why is this important?
Tables are accessible only when relationships between headers and data cells are programmatically explicit. Assistive technologies rely on structural markup to announce context while navigating cells.

### User Experience
- Users can move cell-by-cell and still hear relevant row/column headers.
- Responsive or restyled table views remain understandable because structure is preserved.
- Complex tables are less error-prone when associations are explicit.

## Carousels

### Why is this important?
Carousels are often high-visibility content areas, but moving/rotating content can hide information and create orientation issues. Accessible controls reduce both accessibility and usability failures.

### User Experience
- Keyboard and voice users can move between items predictably.
- Screen reader users are informed about current item and navigation controls.
- Users distracted by movement can pause or stop animation.
- Users who need more reading time can control timing.

## Menus

### Why is this important?
Navigation menus are core interaction surfaces. If menus are not keyboard operable, clearly labeled, and focus-managed, users cannot reliably discover or activate site functionality.

### User Experience
- Keyboard users can open, move within, and close menus without pointer input.
- Screen reader users receive clear names, roles, and state changes.
- Users with cognitive disabilities benefit from consistent structure and predictable behavior.
- Voice users can activate controls that have concise, stable labels.

## Evolving Sources
- WAI ARRM all tasks CSV: https://raw.githubusercontent.com/w3c/wai-arrm/draft/_data/arrm/arrm-all-tasks.csv
- WAI ARRM WCAG mapping CSV: https://raw.githubusercontent.com/w3c/wai-arrm/draft/_data/arrm/arrm-wcag-sc.csv
