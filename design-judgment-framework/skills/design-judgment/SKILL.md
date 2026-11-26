---
name: design-judgment
description: Orchestrates evidence-grounded product design decisions under ambiguity. Use for UX choices, conflicting design principles, design alternatives, governance, or agent autonomy decisions across any domain.
---
# Design judgment: non-linear orchestration (v1.2)

Use as the entry point. Locate the framework root (the directory containing `workflow.json`, `profiles/`, `references/`, `scripts/`, `projects/`). Read `references/CONTRACTS.md`, `references/ITERATION_POLICY.md`, `references/WORKSPACE_CONTRACT.md`, `profiles/preferences.json`, and `profiles/iteration-policy.json` before execution.

**Workflow is a dependency graph, not a linear wizard.** `workflow.json` identifies normal dependencies and the bounded feedback controller allows selective backward transitions. A new IA finding can invalidate wireframes; a validation failure can invalidate earlier user assumptions. Re-run affected artifacts only and preserve contradictory history. Do not iterate just to generate more alternatives.

## Required project bootstrap

1. Frame the problem with `design-context` and create a stable project ID and decision ID(s).
2. Activate `design-artifact-workspace` to choose a **project-specific section/navigation model**. The HTML shell is fixed, but the tabs are never predefined by this skill. Create `projects/<project-id>.json`; publish the first standalone HTML with a brief and known uncertainties. Every meaningful stage output becomes an inspectable artifact.
3. Load the user-configurable `profiles/iteration-policy.json` and any project overrides. Initialize controller run-state at the start of the exploration (`--init-only`) so the time budget includes research/design time; do not wait for the first revisit event. Explain any time/revision/tool budgets that affect autonomy. The browser's policy export is not automatically active in the agent runtime.

## Normal stage dependencies (revisitable, not prescriptive)

- `design-context`: user, task, risks, business goal and outcomes.
- `design-domain-research`: when domain evidence is absent, stale or contradictory; cite sources and mark inference.
- `design-precedents`: comparable and contrasting documented decisions.
- `design-information-architecture`: required for structural questions; explore independent architectures and trace equivalent tasks. Explicitly justify skipping when local screen changes don't affect IA.
- `design-options`: compare actual interaction/wireframe alternatives under user-configured preferences and hard constraints.
- `design-governance`: separate confidence, risk, hard constraints and authorization.
- `design-validation`: formulate tests that could reverse the recommendation.
- `design-judgment`: assemble the current conditional recommendation and verified limits.

After any major stage or review feedback, activate `design-feedback-controller` with a structured event. Handle outcomes:

| Controller action | Required behavior |
|---|---|
| `CONTINUE` | Continue work without gratuitous revisits |
| `REVISIT` | Mark affected artifacts stale; re-run only returned stages and refresh HTML |
| `VALIDATE` | Stop inventing reasons; obtain new external/user evidence |
| `STOP` | Publish the strongest **provisional** conclusion and remaining open issues |
| `ESCALATE` | Publish the blocker and request explicit human resolution; do not implement |

The feedback controller maintains file-based state (`projects/<project-id>-state.json`); invoke `scripts/feedback_controller.py` rather than assuming skill metadata enforces runtime limits. If runtime cannot enforce clocks or report tool calls, say so and use its native execution limits. The governance gate is independent of the feedback controller.

## Deliverable

Deliver a generated **single-file HTML workspace** with a left navigation chosen for this project, research/provenance, reviewable artifacts, alternative IA (or a documented skip), competing wireframe concepts when relevant, selected conditional recommendation, governance/validation, and decision/revision history as applicable. Include source JSON, user-editable iteration policy, and an explanation of how exported reviewer feedback feeds future revisions.

Use `python3 scripts/workspace.py build --project projects/<project-id>.json --policy profiles/iteration-policy.json --out workspace-output/<project-id>.html` after a stage output. Use `record` for subsequent artifact updates.

## Integrity checks

- Never invent observations, persona rankings, measurements, or outcomes.
- Preference scores are not evidence; don't promote synthetic examples to validated choices.
- Every upstream revisit must identify specific invalidations; preserve unaffected work and history.
- Never let any preference or iteration policy waive mandatory privacy, security, legal, accessibility or organizational controls.
- No numerical score, reviewer click or `STOP` status authorizes external/irreversible actions.
- Skills are text instructions and CLI helpers; runtimes must explicitly invoke them. No automatic background execution is implied.
