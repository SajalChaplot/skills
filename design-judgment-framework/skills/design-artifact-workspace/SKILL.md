---
name: design-artifact-workspace
description: Generate and continuously update a self-contained, reviewable HTML design workspace with an agent-defined left navigation, structured artifacts, alternative IA and wireframes, and exportable human feedback. Use throughout a design project, not only at the end.
---
# Publish a project-defined HTML design workspace

## Non-negotiable output contract

Every meaningful piece of design work (problem framing, new evidence, assumptions, persona/job definition, entity model, IA branches, wireframe explorations, choices, governance and validation) must be **inspectable by the human reviewer**, unless omitted for privacy, irrelevance, or explicit project scope. Record source/provenance, review state, version and unresolved questions. Publish an updated standalone `.html` workspace at logical checkpoints and on final delivery.

**The HTML shell is fixed; the tabs are NOT fixed.** `projects/<project-id>.json` contains an ordered `sections[]` array. The agent chooses the number, grouping, order, label and purpose of sections for the *specific project*. Don't copy the demonstration labels verbatim to every project, and don't create empty tabs just to mirror workflow stages. A project could have three sections or fourteen; use the fewest that provide natural review boundaries. Research, problem definition, IA, wireframes and concept decisions may be separate or combined when appropriate.

## Design the workspace using the framework

1. **Context:** Determine the current user job and what evidence the reviewer must inspect. Define the reviewer's own task: find important decisions, compare alternatives, detect assumptions and request a revision. Use high discoverability, consistent navigation, readable content hierarchy, and low cognitive load.
2. **IA:** Decide the top-level review sections from the actual project artifacts, not from a universal design-process checklist. Group related artifacts by intent or decision. Keep high-impact alternatives and rationale visible, and keep superseded versions traceable.
3. **Alternatives:** If IA variations exist, use the `ia` block; if wireframe concepts exist, use `wireframes`; for evidence use `sources`, `table`, `text` or `callout`. The templates are editable structured representations, not claims of tested designs. Images can be embedded as local assets when available.
4. **Choice and verification:** Every artifact has a clear title, short summary, evidence level (`documented`, `inference`, `hypothesis`, `validated`, etc.), status (`pending`, `reviewed`, `needs_revision`), version and optional `decision_id`. The browser provides artifact-level review controls and notes. Reviewer feedback is exported as JSON rather than silently changing any agent's state.
5. **Iteration:** If a previous decision is reopened, mark invalidated artifacts `stale:true`, update the relevant content after re-entry, then increase versions. Keep a project-specific feedback/revision history if it materially affects review.
6. **Access and privacy:** Use no tracking, external scripts, or network assets by default. The output is one local HTML file. Don't publish secrets/PII in a shareable workspace. Cite research URLs where available and distinguish source evidence from simulated examples.

## Data and commands

Start by creating a project JSON (see `projects/security-alert-review.json` and `projects/developer-setup-review.json` for two **different nav structures**). Read `references/WORKSPACE_CONTRACT.md` for the JSON schema and block catalog.

Generate the HTML:

```bash
python3 scripts/workspace.py build \
  --project projects/my-project.json \
  --policy profiles/iteration-policy.json \
  --out workspace-output/my-project.html
```

At each checkpoint, emit an artifact event, then record and regenerate:

```bash
python3 scripts/workspace.py record \
  --project projects/my-project.json \
  --artifact path/to/stage-artifact-event.json \
  --policy profiles/iteration-policy.json \
  --out workspace-output/my-project.html
```

Existing artifact IDs are revised with incremented versions; unknown section IDs create **new project-defined tabs**, requiring the event's section title/group. The agent decides the tabs. The browser can import a different project JSON without rebuilding, but the durable deliverable is the generated standalone HTML.

## Human review loop

The reviewer navigates via the left rail, marks artifacts Reviewed/Needs revision, adds reasons and exports review JSON. The agent can run `python3 scripts/ingest_reviews.py --project projects/my-project.json --reviews exported-reviews.json --out workspace-output/review-triage.json` to map feedback to artifact versions, decision IDs and origin stages. The agent investigates each claim, then uses `design-feedback-controller` when a real invalidation is established. Reviewer opinion is an input, not automatically verified user-research evidence. Human approval of the deliverable is not equivalent to authorization to ship changes.

If no stage artifacts are available yet, publish a short contextual brief and label the gaps. Do not fabricate content to fill sections.

## Workspace UI design standard (V1.2 workspace refresh)

Designers and product managers use the output to **inspect evidence and visual reasoning**, compare options, and approve or challenge individual *artifacts*. The workspace itself should follow the design judgment workflow:

1. **Reviewer context:** Optimize for scanning the current section, opening evidence/IA/wireframes at inspection size, and providing actionable feedback with minimal context switching.
2. **Information architecture:** Keep project-chosen navigation sections in the left rail. The shell is reusable, but section names and counts come from the project manifest. Avoid empty process-driven tabs. Put artifact-level reviews immediately beneath their respective artifact rather than in a detached rail.
3. **Visual alternatives:** Keep IA options, low-fi wireframes, step flows, and screenshots inspectable. Provide visible **View larger** controls for every visual that benefits from close inspection (including generated IA and wireframe blocks, not only image files). Never force reviewers to interpret tiny thumbnails as sufficient evidence.
4. **Image viewer:** Use a native modal dialog with an accessible title and description, explicit Close, Fit, +/− zoom, Escape behavior, scroll-to-pan, and focus return. Preserve alt text for embedded image artifacts. Make keyboard operation and 200% browser zoom viable.
5. **Input accessibility:** Use readable native controls (at least 14–16px labels/values), explicit labels, visible focus treatment, and light color-scheme for select menus. The select element **and its option list** must use high-contrast foreground and background colors. Do not communicate review status via color alone.
6. **Responsive review:** On mobile, retain navigation, review export, policy editing and project import/export via an accessible action disclosure; do not simply hide operations.
7. **Review trust:** Annotate research provenance, assumptions, versions, stale states, and decision IDs. Keep note/status controls next to the content they refer to. Clearly explain that browser edits do not automatically change the agent's files.
8. **Quality assurance:** Before delivery, test navigation, review inputs, IA and wireframe enlargement, screenshot/image enlargement, policy editing, exporting, and narrow-screen overflow in an actual browser. Use the browser's Accessibility Tree, keyboard-only checks, and contrast measurement where possible. Automated checks do not replace assistive-technology testing.

Do not claim universal WCAG conformance without full manual and assistive-technology verification. The fixed shell should be robust, but artifacts generated by an agent still need text, labels, and evidence-quality review.
