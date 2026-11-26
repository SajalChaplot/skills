# Workspace redesign decision record · V1.2.1

## Problem and reviewer jobs

**Observed user feedback:** The first V1.2 workspace has accessibility/usability issues, including dropdown menu option contrast; images and visual artifacts cannot be enlarged. The target users are **product designers and PMs** who inspect research, choices, IA explorations and wireframes.

Reviewer's core jobs:

1. Find the right decision and its evidence, regardless of which project-defined step produced it.
2. Inspect an image/diagram/wireframe at a useful size to judge hierarchy and details.
3. Mark a specific artifact reviewed or needs revision and leave a concrete reason.
4. Configure iteration policy and export it without believing browser changes silently altered agent files.

## Competing IA concepts

| Concept | Benefits | Weakness | Choice |
|---|---|---|---|
| **A. Left tabs + detached right review rail** (V1.2) | Review always in view | Reviewer must cross-reference distant controls with artifacts; competes for visual width | Rejected |
| **B. Left tabs + artifact-first single column, inline review** | More visual width; status and notes anchored to artifact; works on mobile | Scrolling required for multiple long artifacts | **Selected** |
| **C. Full-screen document reader with slide-like pagination** | Focused per artifact | Harder to scan relationships and compare neighboring artifacts | Rejected for default; may be appropriate later |

The left navigation is **structural**, not a hard-coded process. `sections[]` remains fully project defined, matching the existing output contract.

## Key decisions and their trade-offs

- **Visual inspection:** Dedicated `dialog` viewer supports all visual blocks (images, IA diagrams, generated wireframes and longer step flows), with visible View larger actions; in-modal scroll, Fit, keyboard `+/-/0`, Escape, and focus restoration. Structured diagrams are recreated from manifest data, not treated as bitmap screenshots.
- **Review locality:** Status and notes are placed below each artifact. The native `select` is retained but is explicitly `color-scheme: light` with white background and dark `option` text, even in dark OS/browser environments. Label and visible status tag are both textual.
- **Editorial shell:** Restrained ink + dark teal, white surfaces, higher text sizes, fewer competing accents, sticky toolbar, high-contrast navigation and explicit progress count. Approximate scores remain labeled as hypotheses, not validation.
- **Mobile:** Drawer-style project navigation; all important actions remain available through a high-contrast More disclosure, including policy and project import/export.
- **Local-first trust:** Standalone HTML, no external scripts/fonts, no telemetry. Feedback is stored locally best-effort and must be exported to the agent.

## Validation checklist / known boundaries

- Existing 44 Python regressions for workflow, feedback controller, project-defined tabs and safe payload embedding remain passing.
- Browser smoke checks: section navigation, IA enlargement, wireframe enlargement, zoom and Escape, review status and notes, policy range editing, mobile drawer and overflow. Native select computed background is white and text is dark.
- Further verification needed in deployment browsers: Windows native option popup appearance, VoiceOver/NVDA on actual hardware, 200/400% browser zoom and large real image sets.
- Browser **does not** apply exported policy automatically or sync feedback to an agent. No additional claim of WCAG certification is made.
