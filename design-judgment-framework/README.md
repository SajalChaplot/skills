# Design Judgment Framework · v1.2.1 (iterative workflow + accessible HTML artifact workspace)

A portable, domain-extensible **decision workflow for human and AI product designers**, especially when evidence is incomplete. The framework does **not** treat a numeric score as proof that a design is right; it makes assumptions and preferences inspectable.

## What you get

- **Ten connected Agent Skills:** the original eight (orchestrator, context, domain research, precedents, IA exploration, options, governance and validation), plus **feedback controller** and **HTML artifact workspace**.
- **An offline IA Exploration Studio:** `web/ia-explorer.html` compares four security-alert information architectures with editable **task-specific** weights and navigation outlines; use it to test the reasoning process, not to claim research-backed results.
- **A local slider interface:** open `web/index.html` in a browser to tune organization- and task-level weights and the agent's initiative; import/export `preferences.json`.
- **A separate IA decision tool:** `python3 scripts/evaluate_ia.py --case examples/security-alert-ia.json --out examples/security-alert-ia-evaluation.json`. It accepts case-defined IA dimensions without changing the original eight sliders.
- **A dependency-free Python decision engine:** run with `python3 scripts/evaluate.py --config profiles/preferences.json --case examples/developer-project-setup.json --out examples/sample-evaluation.json`.
- **An example developer-domain library:** documented, linked sources are distinguished from inferred design rules and simulated option fit ratings.
- **Agent-readable contracts:** `workflow.json` encodes the connected stage graph, `references/CONTRACTS.md` documents handoffs, and `examples/decision-record-template.json` provides the final output shape.

## Install in an agent

Keep the entire framework folder in your project or another agent-accessible location. Copy or link all ten folders under `skills/` into the skill discovery folder supported by your agent (for example `.agents/skills/` when supported). Make `design-judgment` the entry skill. Tell your agent the **absolute path of this framework root**, which contains `references/`, `profiles/`, `library/`, `examples/`, and `scripts/`. The skills use paths relative to that framework root, **not** relative to the installed skill directory. Agent discovery and chaining vary by product; copying alone may not automatically run the workflow.

Use this entry prompt:

> Use the design-judgment skill to evaluate our [design question]. Domain: [domain]. Target workflow: [job]. Read the shared preferences and current domain evidence. Show alternative designs, weighted trade-offs, confidence, risk, approval gate, and a test plan. Cite precedent evidence, state what is inferred, and do not invent measurements.

## Workflow

`Context ↔ Evidence ↔ Precedents ↔ IA ↔ UI alternatives ↔ Governance ↔ Validation`

Skills have ordinary dependencies, but the agent may selectively revisit earlier decisions when evidence or review contradicts them. `design-feedback-controller` enforces configured revisit budgets at each invocation; `design-artifact-workspace` publishes each reviewable output to project-chosen HTML tabs. See the V1.2 section below.

The orchestrator is responsible for reading/activating each skill, passing the shared structured artifacts, and producing a decision record. **Skill invocation is an instruction convention, not a guaranteed runtime API**. If other skill folders cannot be dynamically activated, load their `SKILL.md` files as reference instructions.


## New in V1.1 — explicit IA exploration

**Why:** In a security-alert design exercise, an alert-centered navigation model was selected before alternatives were explicitly explored. Previous priority sliders explained some trade-offs, but they did not establish that the underlying information model matched users' jobs. V1.1 closes the *process* gap: explore entity models and competing IA concepts **before** wireframes.

- Read `skills/design-information-architecture/SKILL.md` and `references/IA_CONTRACT.md` for the repeatable method, outputs and review gates.
- The skill is **domain-agnostic**: an agent chooses task-relevant structural alternatives (object-, task-, resource-, incident-, timeline-, or audience-centered, etc.) and traces representative tasks through each. The labels are **hypotheses**, not universally correct templates.
- Read `examples/security-alert-ia-decision.md` for a human-readable worked comparison and inspect `examples/security-alert-ia.json` for a machine-readable example comparing four IAs and the prior user-specified eight priorities (Efficiency 90, Information density 80, Discoverability 55, User control 95, Guidance 70, Flexibility 70, Consistency 85, Simplicity 80). Fit ratings, tree maps and paths are **illustrative and unvalidated**.
- Open `web/ia-explorer.html` to change these IA weights and inspect comparative structure, strengths and failures. Download the JSON evaluation; the web page does not write files to disk automatically.
- Run `python3 scripts/evaluate_ia.py --case examples/security-alert-ia.json` to reproduce example ranking. The scorer dynamically validates the **case-defined** IA axes, filters known hard-constraint violations, reports near ties and weight sensitivity. It does not assert that a high score means the IA was validated.
- For a task with unaffected IA, state the explicit `skip_reason`. This avoids forcing elaborate IA work on every small visual decision.

See `references/V2_IA_INTEGRATION_NOTES.md` for the migration path into V2.

**Intentional V1.1 boundary:** The existing eight generic organization/task sliders and the new case-specific IA rubric are **separate**, not automatically synchronized. The V2 plan still owns evidence-grounded domain/persona prioritization and dynamic mapping across the layers. Do not represent the security-alert example's weights as universal recommendations.

**Evidence methods:** Organizational models, labels, navigation, and search should be tested independently of visual screens. See NN/g's [IA study guide](https://www.nngroup.com/articles/ia-study-guide/), [card sorting vs tree testing](https://www.nngroup.com/articles/card-sorting-tree-testing-differences/) and [tree-testing overview](https://www.nngroup.com/articles/tree-testing/). These support the *research approach*, not the security-alert architecture choice.

## Slider hierarchy

1. `organization.priority_weights` sets defaults (0–100 per axis, relative importance, **not** percentages).
2. `tasks[].priority_weight_overrides` replaces only named weights for the matching task.
3. `organization.autonomy_initiative` (and optional task override) adjusts the narrow low-risk autonomous threshold. It **cannot** waive high-risk approval or required safeguards.
4. Evidence confidence and decision risk come from `case.assessment` with rationale and sources; they are **not** user taste settings.
5. Legal, security, accessibility, and privacy obligations are separate, mandatory guardrails. Regulatory details must be determined for each jurisdiction and product; the bundle does not certify compliance.

Open the slider interface, configure a task, and click **Export JSON**. Replace `profiles/preferences.json` with the exported file for agent/CLI use. The page itself does not silently edit the local file system.

## Decision engine limitations

- Each candidate's eight `fit_scores` (0–5) are **estimates**, not observed user outcomes. Agents must provide reasons and sources in their decision record.
- Weighted scores make value trade-offs visible. They are not probabilities or evidence confidence.
- A narrow score gap is **inconclusive**; sensitivity checks can expose fragile rankings.
- Known hard-constraint violations disqualify options; unknown compliance and safety status requires review.
- The policy returns recommendation gates, **not authorization to execute external actions**. Publishing, purchases, account or permission changes, or production deployment still require explicit authorization.

## Extending to a new domain

Use `design-domain-research` to create `library/domains/<domain>.json` and `library/precedents/<domain>.json` with citations, scope, limitations and confidence. Do not copy developer-domain heuristics into finance or security as universal laws. Adjust organization defaults and task overrides through the slider. Domain research is an ongoing activity; evidence can expire.

## Reproducible verification

`python3 -m unittest discover -s tests -v`

`python3 scripts/evaluate_ia.py --case examples/security-alert-ia.json`

Sources and provenance: `references/SOURCES.md`. This is an independently authored framework; it is not an official design methodology of any vendor.

---

# New in V1.2 — bounded iteration + project-defined HTML workspaces

V1.2 preserves V1.1's slider UI, IA Explorer, original decision evaluators and seven domain/UX-stage skills, while adding **two service skills** (`design-feedback-controller`, `design-artifact-workspace`). There are now **ten connected skills**.

### 1. Non-linear workflow with configurable loop safeguards

Design is not a linear process. If a wireframe conflicts with an IA assumption or validation overturns a prior decision, the agent may revisit only affected stages and their dependent outputs. `workflow.json` declares stage dependencies. `scripts/feedback_controller.py` processes structured events and returns `CONTINUE`, `REVISIT`, `VALIDATE`, `STOP` or `ESCALATE`.

Users can edit `profiles/iteration-policy.json` or supply a partial override (sample: `profiles/iteration-policy-project-example.json`). By default the controller limits exploration to 3 revisions per decision, 8 per project, 3 entries per stage, 30 elapsed minutes, 60 **reported** tool calls, and 2 stagnant cycles. These values are product heuristics, not measured optimal limits. Safety boundaries are never waived.

Try a selective IA revisit **without mutating the example project**:

```bash
python3 scripts/feedback_controller.py \
  --policy profiles/iteration-policy.json --workflow workflow.json \
  --state workspace-output/sample-controller-state.json \
  --event examples/controller-events/revisit-ia.json \
  --out workspace-output/sample-controller-result.json
```

The controller **does not run automatically** when a SKILL.md is read. The agent/orchestrator must call it at checkpoints, report tool calls where available, and obey `STOP`/`ESCALATE`. For strict wall-clock budgets, also configure the agent runtime's native deadline. The controller checks actual elapsed time only when invoked.

### 2. Reviewable HTML workspace with agent-chosen tabs

The project manifest (not a hard-coded checklist) defines ordered navigation sections, groups and artifacts. Every project can have different tabs; the shell retains consistent left navigation, artifact rendering, evidence labels, reviewer notes, status, import/export and a policy editor drawer.

Open these **standalone**, offline review files:

- `workspace-output/security-alert-review.html` — eight tabs covering a security-alert design exercise, illustrative IA alternatives and low-fidelity visual wireframes.
- `workspace-output/developer-setup-review.html` — three different project-defined tabs; proves the layout is not locked to any checklist.

Build or re-build from any project manifest:

```bash
python3 scripts/workspace.py build \
  --project projects/security-alert-review.json \
  --policy profiles/iteration-policy.json \
  --out workspace-output/security-alert-review.html
```

Create a new artifact in any existing or new project-defined tab:

```bash
python3 scripts/workspace.py record \
  --project projects/my-project.json \
  --artifact path/to/agent-artifact-event.json \
  --policy profiles/iteration-policy.json \
  --out workspace-output/my-project.html
```

Sample event shape: `examples/agent-artifact-event.json`. Full contract: `references/WORKSPACE_CONTRACT.md`.

### 3. Human reviewer workflow

The human reads the project-specific left navigation, checks IA/wireframe alternatives, marks individual artifacts as **Reviewed / Needs revision / Pending**, adds a note and exports review JSON. The agent ingests that feedback, verifies claims and invokes the controller if an earlier artifact is invalidated. The browser stores notes locally where permitted; downloaded review JSON is the portable record. UI policy adjustments must be exported and applied by the agent to become operative.

### Design quality and evidence cautions

- The security-alert project is a **demonstration** using hypothetical user behavior, IA rankings and wireframes, not a conducted user study.
- The HTML shell is standalone with no network dependencies. It is a review document, not a complete collaborative backend or an automatic Figma design generator.
- A generated HTML workspace cannot silently modify the source skill files, project JSON or invoke an agent. Updates require the agent's local CLI or another authorized runtime.
- Existing `web/index.html` and `web/ia-explorer.html` remain separate tools; V2 still owns research-grounded mapping between domain/persona contexts and automatic preference weights.

### Full regression tests

```bash
python3 -m unittest discover -s tests -v
```

### Review feedback intake

When a reviewer exports JSON, use:

```bash
python3 scripts/ingest_reviews.py --project projects/security-alert-review.json \
  --reviews path/to/exported-reviews.json --out workspace-output/review-triage.json
```

The resulting triage list identifies stage, decision and artifact version, and distinguishes possible invalidation from outdated or already-reviewed feedback. The agent decides whether a controller revisit is warranted.

---

## V1.2.1 — Workspace usability and accessibility redesign

This update is **backward-compatible with the V1.2 project manifest, controller, preference model, review JSON, and all ten skill directories**. It rebuilds `web/workspace-template.html` from scratch for product designers and PMs. `skills/design-artifact-workspace/SKILL.md` now contains the UI review standard used to create the new shell; the decision record is `references/WORKSPACE_REDESIGN_DECISIONS.md`.

- **Dynamic, project-defined left navigation:** Sections continue to be generated from each project's `sections[]`, not a prescribed list of process tabs. Search matches section and artifact titles.
- **Artifact-first review:** Clear artifact metadata and evidence status; status dropdown and review notes sit immediately below the artifact they concern, rather than in an unrelated right rail.
- **Enlarged inspection:** Images, IA variant diagrams, generated wireframes and longer step flows have visible **View larger** buttons. Native modal viewer supports real zoom using `+`, `-`, `0` (Fit), explicit Close, Escape, horizontal and vertical scrolling, and focus restoration. Fit may shrink complex visuals substantially on narrow screens; default opens at 100% for readable inspection and scrolling.
- **Dropdown contrast fix:** Native select menus and `<option>` items explicitly request a light color scheme, dark text and white background. Labels and status are never represented by color alone.
- **More usable mobile workspace:** Navigation drawer, a More actions disclosure for policy/import/export, reduced visual clutter, and no forced global horizontal scrolling at the tested 390px viewport.
- **Trust boundaries unchanged:** Best-effort local note storage and JSON export; no automatic sync, production implementation, or compliance certification.

### Start with the self-review project

Open `workspace-output/workspace-redesign-review.html`. It has **project-specific** sections: reviewer goals, layout explorations, visual QA (desktop and mobile images that can be enlarged), and interaction checks. The artifacts are a transparent *design exercise* and smoke-test evidence, not an end-user usability study.

The previously included security and developer sample HTMLs are also rebuilt using the updated shell:

```bash
python3 scripts/workspace.py build --project projects/security-alert-review.json --policy profiles/iteration-policy.json --out workspace-output/security-alert-review.html
python3 scripts/workspace.py build --project projects/developer-setup-review.json --policy profiles/iteration-policy.json --out workspace-output/developer-setup-review.html
python3 scripts/workspace.py build --project projects/workspace-redesign-review.json --policy profiles/iteration-policy.json --out workspace-output/workspace-redesign-review.html
```

The standard `python3 -m unittest discover -s tests -v` checks the data contracts and workflow logic. Optional `tests/browser_check.py` exercises the UI in headless Chromium via Playwright; it uses `set_content` because some execution environments block local `file://` or `localhost` navigation. **A complete WCAG evaluation still requires manual keyboard, zoom, screen reader, browser/OS native select popup, and real-content testing.**
