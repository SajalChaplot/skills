# Start a project in Design Judgment Framework v1.2

## Install skills

Keep this directory intact. Let the agent runtime discover the **ten `skills/*/SKILL.md`** entries (or load them as reference documents if it does not support automatic discovery). Select `design-judgment` as your entry skill and provide the absolute path to this package root. Skill files alone do **not** execute shell scripts: grant the agent permitted local file/command capabilities in its runtime or run the provided Python helpers explicitly.

## One prompt to give the agent

> Use Design Judgment Framework v1.2 for this project. Start by identifying the decision question, who the primary job benefits, applicable evidence, constraints and uncertainties. Build a project-defined HTML workspace: choose an appropriate left-nav section structure from the artifacts this project actually needs, rather than copying a standard tab checklist. Preserve research references and clearly label hypotheses. Explore IA only where relevant, generate and compare meaningful wireframe alternatives, assess risk and evidence independently, and show a conditional recommendation and validation plan. After each significant step, record a workspace artifact. When new findings contradict earlier work, invoke design-feedback-controller with a causal invalidation event; obey its iteration policy and stop/escalate statuses. Let me review the resulting HTML and export revision notes.

## Make a project

1. Copy `examples/project-starter.json` to `projects/my-project.json` and replace its ID/name. Leave `sections: []` until the agent chooses the right project-specific tabs.
2. Edit `profiles/iteration-policy.json` (or provide a partial project override) if the default revision/time limits don't fit the project. Do not change evidence confidence via preferences.
3. Initialize the iteration timer before doing substantial research: `python3 scripts/feedback_controller.py --policy profiles/iteration-policy.json --workflow workflow.json --state projects/my-project-state.json --init-only`. This begins the configured exploration budget. For a multi-day project, explicitly start a new authorized exploration run or adjust the policy; do not silently reset a spent budget.
4. Ask the agent to create structured artifact events and use `scripts/workspace.py record` after each meaningful stage.
5. Generate or regenerate `workspace-output/my-project.html` with `scripts/workspace.py build --project projects/my-project.json --policy profiles/iteration-policy.json --out workspace-output/my-project.html`.
6. Review the HTML locally. Mark artifacts for revision and download Review JSON. Route it through `scripts/ingest_reviews.py` for a triage list; an agent must decide if a controller re-entry is justified.

## Re-entry example

`python3 scripts/feedback_controller.py --policy profiles/iteration-policy.json --workflow workflow.json --state projects/my-project-state.json --event examples/controller-events/revisit-ia.json --project projects/my-project.json --workspace-out workspace-output/my-project.html`

The example event refers to security-alert navigation, so replace its decision ID, reason, evidence IDs and invalidated stages for a real project. A controller event is not verified user research. If the design's assumptions cannot be tested within the configured budget, the agent must publish a provisional result or escalate; it must not loop indefinitely.

## Try the samples

- Open `workspace-output/security-alert-review.html` to see eight agent-selected tabs, structural IA variations and interactive review notes.
- Open `workspace-output/developer-setup-review.html` to see **three different tabs** using the same HTML shell.
- Open `workspace-output/security-alert-iteration-demo.html` to see a real controller call mark affected artifacts stale and append a reviewable feedback record.

## Verify

`python3 -m unittest discover -s tests -v`

Evidence and caveats are documented in `references/` and the README. The HTML is fully offline; updates require re-running local scripts. Tool-call/time limits apply only when the agent invokes the controller and accurately reports usage.

## Revised workspace UI (V1.2.1)

For visual inspection, click **View larger** on an image, an IA variant, a generated wireframe, or a longer step flow. Zoom in/out with the controls or `+`/`-`, choose **Fit** or press `0` to see the whole visual (which can be small on phones), and press **Escape** to close. Scroll inside the viewer to pan a zoomed visual.

To review, locate the artifact in the project-specific left navigation, set **Review status** and enter a **Review notes** reason directly beneath it. Export review JSON to pass the changes to the agent. A changed artifact version requires a fresh review.

To adjust the bounded iteration policy, select **Iteration policy** on desktop or **More → Iteration policy** on mobile, change the sliders, and **Export policy JSON**. Apply that exported policy to your actual agent run; the HTML file does not make changes to skill source files on its own.

For the redesign rationale and a self-review example with zoomable embedded screenshots, open `references/WORKSPACE_REDESIGN_DECISIONS.md` and `workspace-output/workspace-redesign-review.html`.
