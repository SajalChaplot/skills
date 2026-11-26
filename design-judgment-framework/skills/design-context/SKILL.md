---
name: design-context
description: Frames a product or UX design problem as a decision context. Use before design evaluation to identify the primary job, roles, experience levels, workflow, constraints, uncertainty and measurable success.
---
# Frame the decision

1. Write a falsifiable question: “For [user in situation], should we use [A/B], given [constraint], to improve [job metric]?”
2. Segment target users along **role, job, familiarity with this workflow, frequency, permissions, environment and error consequences**. Do not claim a company's primary persona from speculative public evidence.
3. Identify task state and critical path. Capture adjacent stakeholders and excluded users.
4. Clarify why the organization cares, which business outcome is affected, what cannot change, and measurable user success and guardrails.
5. List what is documented, observed, inferred, or unknown, with links/dates where available. For contested inputs, record both sides.
6. Identify decision reversibility and whether external execution is in scope; ask only essential missing questions, otherwise state provisional assumptions.

Output `decision_context` following `references/CONTRACTS.md` in the framework root. Hand off to `design-domain-research` (only when needed) and `design-precedents`.


## IA-sensitive task framing

When there are multiple objects or tasks, explicitly capture entities, entry points, known user vocabulary, canonical objects, cross-object pivots, workflow states, and existing navigation assumptions. State whether a structural IA decision is likely. Do not treat a persona label as proof of a preferred navigation model.


## V1.2 feedback and publish hook

After producing or materially revising this skill's output, publish a reviewable, versioned artifact with `design-artifact-workspace` (`scripts/workspace.py record`). The HTML navigation section is chosen for this project, not dictated by the skill name. Then evaluate material contradictions with `design-feedback-controller`. If an earlier assumption was invalidated, identify exact affected workflow stages, preserve evidence provenance, and follow the controller outcome. Do not automatically restart the entire workflow or exceed the configured iteration policy.
