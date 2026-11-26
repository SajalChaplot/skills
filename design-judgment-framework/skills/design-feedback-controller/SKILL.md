---
name: design-feedback-controller
description: Controls non-linear design iteration, selective revisits, versioning, convergence and configurable stopping policies. Use whenever new evidence or review feedback challenges an earlier design decision and at major stage checkpoints.
---
# Bounded, non-linear design feedback controller

## Responsibility

Use the feedback controller as a **service skill**, not a mandatory step that runs only after validation. Design work may go from wireframes back to IA, from validation back to persona assumptions, or from a policy contradiction back to research. Re-enter *only stages whose outputs were invalidated* and their dependent outputs. Preserve unaffected evidence and keep a visible revision log.

This controller returns one of `CONTINUE`, `REVISIT`, `VALIDATE`, `STOP`, `ESCALATE`. **STOP does not mean implementation approval.** This skill never authorizes external actions or changes mandatory safeguards.

## User-configurable policy

1. Read `profiles/iteration-policy.json` from the framework root before beginning a project. Initialize the time budget **before the first research or design step** using `python3 scripts/feedback_controller.py --policy profiles/iteration-policy.json --workflow workflow.json --state projects/<project-id>-state.json --init-only`. The user may edit this JSON, choose to use the default, or supply a **partial project override** (see `profiles/iteration-policy-project-example.json`). Call `scripts/feedback_controller.py --project-policy path` to apply allowed overrides.
2. Explain key options at project kickoff only when they matter: per-decision revision cycles (default 3), total project revisions (8), per-stage re-entries (3), duration budget (30 minutes), reported tool calls (60), meaningful improvement delta (5 rubric points), and maximum stagnant cycles (2). Defaults are **heuristics**, not validated thresholds. Users may configure them.
3. Do not let project overrides waive safety invariants: exhausted high/material/unknown risk and unresolved mandatory constraints escalate; exhaustion otherwise produces a **provisional stop**. Mandatory violations immediately escalate. Real-world release/privileged actions require separate human authorization.
4. The generated HTML workspace has a Policy drawer for adjusting/exporting a JSON copy. **Exported changes are not active until a user or agent applies them to the source file or passes that policy to the controller.** Never claim browser-side sliders silently reconfigured an autonomous agent.

## At every material skill checkpoint

1. Identify the `decision_id`, current stage, new information, its provenance, and whether it invalidates an earlier output. Distinguish observation from hypothesis and preference from evidence.
2. If nothing relevant changed, send a `checkpoint` event → `CONTINUE`.
3. If user evidence or an actual contradiction challenges a design decision, send a specific trigger (`new_evidence`, `contradiction`, `failed_validation`, `constraint_change`, or `material_weakness`). Include **explicit `invalidates` stage IDs**, unique `new_evidence_ids` or a changed rationale fingerprint, risk and mandatory-constraint status.
4. The controller returns the ordered `rerun_stages` closure from `workflow.json`. Rerun **only** these outputs. Mark superseded downstream artifacts stale in the HTML project workspace until refreshed. Never erase rejected alternatives or contradictory evidence.
5. If no new evidence or unique material change is available, the controller recommends `VALIDATE` instead of endless AI reasoning. If the configured stagnation threshold or budget is reached, it returns `STOP` (provisional) or `ESCALATE` (human review).
6. Record the event and outcome in the project artifact workspace, with links to affected decisions and the current policy snapshot.

## Example event

```json
{
  "decision_id": "security-alert-navigation",
  "trigger": "contradiction",
  "reason": "An analyst task fails when pivoting from alert to resource context.",
  "invalidates": ["information_architecture"],
  "new_evidence_ids": ["analyst-walkthrough-001"],
  "material_change_fingerprint": "asset-pivot-v2",
  "risk_level": "low",
  "mandatory_constraint_status": "clear",
  "tool_calls_delta": 4
}
```

Use `python3 scripts/feedback_controller.py --policy profiles/iteration-policy.json --workflow workflow.json --state projects/my-project-state.json --event path/to/event.json --out workspace-output/last-controller-result.json`.

**Runtime qualification:** File-based counters and deadlines are enforceable only when the orchestrating agent calls the script and reports its tool usage. Skills/JSON alone cannot enforce an agent's wall-clock runtime. The script compares timestamps at each invocation, counts reported tools, and prevents further declared revisits at the next checkpoint. If the agent runtime has native deadlines/tool budgets, configure those too.

## Stop conditions and output

- **Converged:** Evidence is adequate, no material unresolved conflict; propose conclusion, then use separate governance/approval gate.
- **No new evidence:** Return `VALIDATE`; repeated stale cycles reach convergence stop.
- **Budget exhausted:** `STOP` with provisional strongest option and unknowns; `ESCALATE` for material/high/unknown risk or unresolved mandatory constraints.
- **Constraint violation:** `ESCALATE` with blocked implementation.
- **Explicit human reopen:** Supported with `human_approved=true` where policy permits, but still subject to configured budgets; human can edit limits deliberately and re-run.

Return `controller_result`, `updated_run_state`, `affected_artifacts`, `next_step`, and an audit entry for the HTML workspace. Read `references/ITERATION_POLICY.md` for full contract.
