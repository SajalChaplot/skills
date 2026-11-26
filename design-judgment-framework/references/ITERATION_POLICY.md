# V1.2 selective iteration and stopping contract

## State model

The orchestrator is not a linear wizard. Each skill emits versioned artifacts. An evidence or evaluation event may invalidate an upstream stage. `scripts/feedback_controller.py` produces one of:

- `CONTINUE`: no reason to reopen previous work; continue current stage or next relevant stage.
- `REVISIT`: rerun only the explicitly invalidated stage(s) and the transitive downstream dependencies in `workflow.json`. Mark affected artifacts stale until refreshed.
- `VALIDATE`: reasoning is insufficient; obtain user, observational, analytics, technical, or compliance evidence.
- `STOP`: finish this attempt with a **provisional** design decision. No implicit authorization.
- `ESCALATE`: unresolved material risk, constraint, external action, or approval requirement blocks autonomous commitment.

The feedback service may run after ANY stage (including a reviewer challenge after the decision record). It is not a one-time final step.

## Configurable policy and safeguards

`profiles/iteration-policy.json` is the organization default. Every number is a tunable heuristic:

| Key | Default | Meaning |
|---|---:|---|
| `revision_limits.per_decision` | 3 | Maximum automatic revision cycles per decision |
| `revision_limits.total_per_project` | 8 | Sum of cycles across the project |
| `revision_limits.per_stage` | 3 | Maximum re-entries to an individual stage |
| `execution_budget.max_elapsed_minutes` | 30 | From initialized run-state to next controller call; wall-clock check |
| `execution_budget.max_reported_tool_calls` | 60 | Only tool calls **reported to controller** can be counted |
| `convergence.min_meaningful_rubric_delta` | 5 | Threshold for comparison on an identical, explained rubric; NOT empirical validation |
| `convergence.max_stagnant_cycles` | 2 | Maximum consecutive cycles without novel evidence, material change or meaningful score delta |

A project may override allowed keys in a partial file (example in `profiles/iteration-policy-project-example.json`). Hard safety invariants are checked by code: exhausted material/high/unknown risk and unresolved mandatory constraints escalate; otherwise exhausted work stops provisionally. Time or revision exhaustion never approves external or destructive actions. The separate `design-governance` gate always applies.

The HTML workspace's Policy drawer can change and download a **copy**. To make it effective, apply the exported JSON to a profile or provide it to an agent and rerun. Browser file permissions do not permit silently mutating the agent configuration.

## Controller input contract

An event is one JSON object:

```json
{
  "decision_id": "unique-decision-id",
  "trigger": "contradiction",
  "reason": "Specific claim invalidated and why",
  "invalidates": ["information_architecture"],
  "new_evidence_ids": ["research-note-001"],
  "material_change_fingerprint": "revision-002",
  "rubric_delta": 0,
  "rubric_id": "same-ia-rubric-v1",
  "risk_level": "low",
  "mandatory_constraint_status": "clear",
  "external_action_requested": false,
  "tool_calls_delta": 4
}
```

- Triggers: `checkpoint`, `new_evidence`, `contradiction`, `failed_validation`, `constraint_change`, `material_weakness`, `needs_validation`, `complete`, `explicit_human_reopen`.
- `invalidates` accepts exact stage IDs from `workflow.json`. List the **earliest proven invalidated stage**, not every stage as a shortcut.
- `new_evidence_ids` must be stable source or observation identifiers; don't invent them. A unique `material_change_fingerprint` means a genuinely different hypothesis, artifact or contradiction, not merely rephrasing.
- `rubric_delta` is optional, signed 0–100 with a required same-`rubric_id` comparison. Scores are judgment estimates unless separately validated.
- `risk_level` must be `low`, `material`, `high` or `unknown`; omitted is treated as unknown. `mandatory_constraint_status` must be `clear`, `unknown`, `violated`; omitted is treated as unknown.
- `tool_calls_delta` requires accurate runtime reporting; if unavailable, use an external native tool budget and state this limit is not measured by the helper.
- `explicit_human_reopen` additionally requires `human_approved:true`. It is still bounded unless the human edits policy.

## No-loop guarantees and known boundaries

Within **reported events** and controller invocations, the revision and time budgets bound re-entries. An agent that ignores the controller is not bounded by this JSON: ensure the runtime or orchestration wrapper invokes it at each checkpoint and refuses new automatic re-entry when the controller returns `STOP`/`ESCALATE`.

Avoid deceptive numerical convergence. When no comparable rubric or new observations exist, use contradiction resolution and external tests. Stagnation must not be hidden by renaming the same concern as new evidence. Preserve contradictions for auditors and reviewers in the workspace.

## Test cases

- New valid evidence invalidates IA → `REVISIT` IA, options, governance, validation and decision record; do not revisit context without cause.
- Unchanged assertion → `VALIDATE` on first attempt, then `STOP`/`ESCALATE` at stagnation threshold.
- Project iteration limit reached → provisional stop or escalation, never pass.
- High-risk incomplete or external action → approval required regardless of estimated score.

### Publishing controller outcomes to HTML

Add `--project projects/my-project.json --workspace-out workspace-output/my-project.html` to the feedback controller invocation. This marks artifacts from invalidated stages stale and appends a checkpoint artifact in the project-selected `workflow_history_section_id`, if provided. The same call rebuilds the HTML. Default remains non-mutating when `--project` is omitted.

### Start the clock before work begins

At project/session kickoff, call `python3 scripts/feedback_controller.py --policy profiles/iteration-policy.json --workflow workflow.json --state projects/<id>-state.json --init-only`. It creates state only if absent, preserving an existing run's counters. Without this explicit initialization, the clock begins at the first controller event, potentially excluding earlier research time. A project spanning multiple working sessions requires a deliberate new run or a larger policy budget; do not silently reset limits.
