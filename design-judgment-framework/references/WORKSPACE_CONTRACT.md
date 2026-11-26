# V1.2 project-defined artifact workspace

## Fixed shell, configurable sections

Each project provides `projects/<project-id>.json` with an **ordered array of sections**. The HTML shell owns the responsive left navigation, top bar, review rail, accessible labels, exporting, printing and iteration-policy drawer. The **project manifest**, created and edited by the agent, owns the actual tabs. Do not hard-code research, IA, wireframes or problem brief as mandatory tabs.

```json
{
  "schema_version": "1.2",
  "project_id": "unique-id",
  "title": "Project title",
  "domain": "Developer tools",
  "project_status": "provisional",
  "version": 1,
  "sections": [
    {
      "id": "model-comparison",
      "title": "Model comparison",
      "group": "Explore",
      "description": "Why the alternatives matter",
      "artifacts": [
        {
          "id": "ia-v1",
          "title": "Alternative information architectures",
          "summary": "Different organizing models",
          "review_status": "pending",
          "evidence_level": "hypothesis",
          "version": 1,
          "decision_id": "my-design-decision",
          "stale": false,
          "blocks": [{"type": "text", "text": "Research is pending."}]
        }
      ]
    }
  ]
}
```

## Block catalog

Blocks render offline and do not accept arbitrary executable HTML/JS. Text is escaped by DOM rendering. Supported types:

- `text` / `markdown`: `{type, title?, text}` — the `markdown` type is intentionally plain text in the offline viewer; prefer semantic blocks for formatted content.
- `bullets`: `{type, title?, items:[string...]}`
- `table`: `{type, title?, columns:[string...], rows:[[cell,...],...]}`
- `callout`: `{type, title?, heading?, text, tone?:"warning"|"danger"|""}`
- `quote`: `{type, title?, text}`
- `sources`: `{type, title?, items:[{title,url,note}]}` (only HTTP(S) URLs are linked)
- `steps`: `{type, title?, steps:[string...]}`
- `ia`: `{type, title?, variants:[{title,summary,nodes:[{label,depth:0|1|2}]}]}`
- `wireframes`: `{type, title?, screens:[{name,app,heading,nav:[string...],selected_nav:0,controls,cards:[{title,detail}],action,rationale}]}`
- `image`: `{type, title?, local_path:"relative-file.png",alt,caption}`. Build step embeds PNG/JPEG/WebP/GIF up to 8 MB from within project folder; do not use remote/private images unless authorized.

The generic wireframe renderer is schematic, not production UI. An agent can embed a real design screenshot as an `image` block, with explicit permission and provenance, alongside its rationale. The workspace does not create/edit Figma layers or preserve editable source for arbitrary uploaded screenshots.

## Publishing events

A stage output may append or update an artifact:

```json
{
  "section_id": "model-comparison",
  "section_title": "Model comparison",
  "section_group": "Explore",
  "section_description": "Structural alternatives",
  "artifact": {
    "id": "ia-v1",
    "title": "Updated IA comparison",
    "summary": "Reopened because of an investigation task conflict",
    "evidence_level": "mixed: observation + inference",
    "blocks": [{"type":"text","text":"Finding and implications..."}]
  }
}
```

`python3 scripts/workspace.py record --project projects/my-project.json --artifact event.json --out workspace-output/my-project.html --policy profiles/iteration-policy.json`

- New section ID → new tab with requested title, group, ordering by insertion.
- Existing artifact ID → replace content and increment version. For provenance that requires an immutable history, create separate history artifacts or keep snapshots externally; overwritten artifacts are **not** automatically version-archived.
- Agent records `stale:true` for invalidated content. Do not quietly remove user-reviewed records.
- `build` injects a project policy snapshot into HTML. The generated HTML does **not** load external JS/CSS or send data anywhere.

## Reviewer feedback

Each artifact has Reviewed / Needs revision / Pending plus free-text notes. Browser localStorage is best-effort; **Export reviews** writes a JSON file, which the agent can ingest as an input. Reviewer feedback can raise a contradiction, but is not itself validated field research. Review records are local to `project_id`; use a new project ID if different projects should have isolated reviews.

The browser can import a project JSON, switch tabs dynamically, export content JSON, and export policy JSON; it cannot silently update local project, agent state or skill policy. Screen-reader/keyboard testing is recommended in the intended deployment browser.

## Required editorial quality

Label source type, date when available, observation versus inference, confidence and unknowns. Favor short descriptive headings and visual alternatives. Show the final recommendation **and** rejected alternatives; include failure/rollback criteria, relevant approval gates and latest iteration status. Sections should be determined by what a particular project requires, not by a default universal checklist.

### Feedback-controller bridge

Provide `--project projects/<id>.json --workspace-out workspace-output/<id>.html` to `scripts/feedback_controller.py`. On `REVISIT`, artifacts with `origin_stage` inside the affected downstream closure are marked `stale:true` and their default review state returns to pending. If `workflow_history_section_id` exists on the project, a controller audit artifact is appended there (and the agent may choose its project-specific title/group). This is an **opt-in bridge** so other agents can use the controller without mutating a project manifest.

A previously exported review applies to an artifact version. After a new version is recorded, the HTML review status resets to pending until that version is re-checked. Previous notes can remain visible for continuity.

### Review feedback triage utility

Run `python3 scripts/ingest_reviews.py --project projects/my-project.json --reviews exported-reviews.json --out workspace-output/review-triage.json`. It matches artifact IDs and versions, identifies current `needs_revision` records, and surfaces associated `decision_id` / `origin_stage`. It **does not** automatically send a controller revisit event: human reviewer opinions must be evaluated and assigned the appropriate evidence classification first.

## V1.2.1 workspace viewer and review behavior

The manifest and review-export schemas remain `1.2` to preserve compatibility. The HTML renderer now uses inline artifact review forms and a reusable accessible modal viewer. `image`, `ia`, `wireframes`, and multi-step `steps` blocks must expose a visible enlargement control. Image `alt` is required for meaningful content; captions and source/provenance should accompany illustrative or unvalidated visuals. Long tables receive a keyboard-focusable, labeled horizontal-scrolling region. The project controls the navigation, not the template. The native `select` and every `option` must remain high contrast in a light color scheme, and every input must have a visible, programmatically associated label. The mobile More disclosure keeps secondary operations discoverable.

The HTML can preserve review notes locally and export them but does not execute agent feedback or update the configured policy automatically. Do not claim WCAG conformance from the template alone; inspect actual generated content in target browsers and screen readers.
