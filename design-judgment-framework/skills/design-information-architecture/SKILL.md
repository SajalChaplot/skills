---
name: design-information-architecture
description: Explore, compare, and justify information architecture alternatives before committing to navigation, layout, or wireframes. Use for design questions involving information organization, entities, grouping, navigation, hierarchy, findability, search, filtering, or cross-object workflows in any product domain.
---
# Design information architecture: structural decision making

## Purpose and entry condition

Run **after** context/domain/precedent discovery and **before** screen/UI alternatives whenever users need to find, traverse, group, compare, or act on multiple information objects. This includes dashboards, workflow tools, security alerts, admin consoles, marketplaces, knowledge systems, and developer products.

You may skip this skill for a purely local presentation or interaction change **only** when the underlying object model, grouping, labels, hierarchy, navigation paths, and task flow are established and unaffected. Record the skip rationale in the decision record. Do **not** silently assume that a screen-level concept establishes an IA.

## Required inputs

`decision_context` (primary task beneficiary, secondary users, jobs, context, success/guardrail outcomes, permissions and constraints), `domain_evidence` if available, `precedent_shortlist`, organizational/task priorities when available. Missing evidence is marked as unknown; never substitute an invented user mental model.

## Workflow

1. **Map jobs and uncertainty.** Enumerate 3–6 critical user questions and tasks (include a non-happy path and a secondary persona). Identify whether work starts from an object, a goal, a resource, an event, or a time-based queue. Distinguish observed behavior from inferred behavior.
2. **Build the information model.** List content/entity types, their identifiers, parent-child and many-to-many relationships, states, attributes, permissions and lifecycle. Distinguish data relationships from the grouping users should navigate. Note source of truth and cross-links. Do not assume a backend schema is the right navigation model.
3. **Generate structurally different IAs.** For materially new IA decisions, generate **at least three** alternatives (two if tightly constrained, explain why). Try object-centered, task/workflow-centered, resource/context-centered, activity/timeline-centered, audience-centered, or grouped-incident models **only when applicable**; these are prompts, not universal categories. Show a compact tree or adjacency list, default entry, labels, search/filter strategy, transitions and cross-object navigation for each. Keep a viable existing baseline if one exists.
4. **Trace the same representative tasks** through every architecture. Identify starting point, target object/action, transitions, context retention, failure/recovery route, permissions and visibility. Count steps only if they are defined in the model; never invent actual speed metrics.
5. **Compare with an IA rubric.** Separate structural correctness and required constraints (gating) from editable priorities (relative weights). Candidate IA dimensions could include findability, information density, navigation efficiency, user control, guidance, flexibility, clarity, consistency, scalability, and context preservation. Use only task-relevant dimensions with clear 0–5 scoring rubrics; do not automatically equate 'density' with 'simplicity' or duplicate correlated concepts. Label fit ratings as hypothetical until research validates them.
6. **Stress-test competing personas and contexts.** Show at least one task where each alternative breaks down; check novice/expert differences, different entry points, irregular tasks, high-volume data, missing data, error states, permissions and accessibility. If primary beneficiary is disputed, compare persona outcomes independently rather than averaging away the conflict.
7. **Choose conditionally.** Report leading IA, why it fits the task and preferences, what is sacrificed, plausible hybrid complements, contradicting evidence, sensitivity to changed priorities, and when a different IA would win. An optional hybrid may inherit parts of a baseline, but identify which model owns primary navigation. Weighted scoring does not prove user mental model or architecture correctness.
8. **Validate IA before screen fidelity.** Prefer tree testing for hierarchy/label findability, card sorting or mental-model interviews for grouping uncertainty, task-based low-fidelity prototype testing for cross-object workflows, and content/permission audits for structural completeness. Define disconfirming observations and a decision review gate. Do not treat card sorting alone as confirmation of task success.

## Output contract (`ia_exploration`)

- `decision_scope`, `skip_reason` (if skipped), `primary_job`, `primary_beneficiary`, `secondary_users`, `information_model` (objects, relationships, states, permissions), `task_scenarios`, `assumptions_and_evidence`.
- `alternatives[]` each with **organizing_principle, default_entry, navigation_tree, cross_links, search_and_filters, task_walkthroughs, benefits, failure_modes, fit_rationale, evidence_status, unknown_constraints**.
- `comparison` with weights and provenance, per-option fit estimates, disqualified choices, near ties, sensitivity and per-persona differences; avoid ranking when active axes lack values.
- `recommendation` with primary architecture, optional secondary overlays, context-dependent exceptions, user groups who lose, and triggers to reconsider.
- `validation` with test method, tasks, metrics (e.g. findability, wrong turns, task success, confidence, recovery), and observation that would invalidate the provisional architecture.

Pass the `ia_exploration` artifact to `design-options`, which must use it as a structural boundary for screen concepts. If IA remains unresolved, do not disguise uncertainty by producing polished screens. Present low-fidelity alternatives or request evidence/approval based on risk.

## Reference example / runnable tool

- `examples/security-alert-ia.json` demonstrates **illustrative** object-, workflow-, resource-, and incident-oriented alternatives based on a prior design discussion, not verified user research.
- `scripts/evaluate_ia.py --case examples/security-alert-ia.json` ranks documented assumptions with a **case-specific, explicitly chosen** IA rubric. It does not change the original eight-axis V1 engine or inject new domain defaults.
- `web/ia-explorer.html` is an offline interactive viewer for **that example**; its knobs are not a universal IA standard.

## Sources for method (not evidence for a specific product decision)

- NN/g, IA study guide: https://www.nngroup.com/articles/ia-study-guide/
- NN/g, card sorting versus tree testing: https://www.nngroup.com/articles/card-sorting-tree-testing-differences/
- NN/g, tree testing navigation categories: https://www.nngroup.com/articles/tree-testing/

The methods do not justify a specific product's ontology; evaluate that with domain-specific evidence.


## V1.2 feedback and publish hook

After producing or materially revising this skill's output, publish a reviewable, versioned artifact with `design-artifact-workspace` (`scripts/workspace.py record`). The HTML navigation section is chosen for this project, not dictated by the skill name. Then evaluate material contradictions with `design-feedback-controller`. If an earlier assumption was invalidated, identify exact affected workflow stages, preserve evidence provenance, and follow the controller outcome. Do not automatically restart the entire workflow or exceed the configured iteration policy.
