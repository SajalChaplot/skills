---
name: design-validation
description: Creates falsifiable tests and feedback loops for ambiguous UX decisions and updates evidence records only after verification. Use after a provisional design recommendation or experiment.
---
# Validate and learn

1. Identify the assumption that most threatens the preferred option. Choose the **cheapest test capable of changing the decision**: past research review, instrumentation, expert review, user task study, prototype comparison or staged rollout.
2. Define the primary success metric, guardrails, target role and task, collection plan, failure/stop criteria, and limitations. Use measurable behaviors rather than aesthetic approval alone.
3. Match method to consequence: riskier and harder-to-reverse decisions need stronger evidence and approval; do not use an informal preference vote as proof for high-risk changes.
4. Precommit to what observations would support, reject or alter the choice. Do not fabricate a result, sample size or launch date.
5. On genuine observed results: record design version, context, measured outcome, source and date; update a precedent as `outcome_with_evidence`. On negative or ambiguous results, preserve the contradiction.
6. Schedule reevaluation triggers by event (new user segment, policy change, degraded KPI, product migration) rather than inventing calendar commitments.

Deliver a validation plan and a post-test decision-record template. Do not claim learning occurred until the evidence exists.


## IA-specific validation

If the decision includes `ia_exploration`, select a validation method suitable for the remaining structural uncertainty *before* screen fidelity: tree tests for findability/navigation, card sorting for uncertain grouping and labels, and low-fidelity task walkthroughs for non-linear object pivots. Test the same tasks across alternatives and record what finding would reverse the IA selection.


## V1.2 feedback and publish hook

After producing or materially revising this skill's output, publish a reviewable, versioned artifact with `design-artifact-workspace` (`scripts/workspace.py record`). The HTML navigation section is chosen for this project, not dictated by the skill name. Then evaluate material contradictions with `design-feedback-controller`. If an earlier assumption was invalidated, identify exact affected workflow stages, preserve evidence provenance, and follow the controller outcome. Do not automatically restart the entire workflow or exceed the configured iteration policy.
