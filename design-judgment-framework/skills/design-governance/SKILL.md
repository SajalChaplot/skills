---
name: design-governance
description: Determines UX decision confidence, risk, reversibility, guardrail violations and required human approval. Use before autonomous design changes or execution, especially for uncertain or high-impact decisions.
---
# Independent confidence, risk, and authorization gate

1. Assess `evidence_confidence` 0–1 **from evidence**, identifying supporting user research, analytics, prototype results, unknowns and conflicting findings. A user preference does not justify increasing confidence.
2. Assess `risk` 0–1 from severity × reach × recovery difficulty × uncertainty; document rationale. Do not treat this as a user preference slider.
3. Inspect hard constraints: security, privacy, accessibility, legal/regulatory needs and business policy. **Unknown** status is not “passing.” Distinguish a concrete violation from unresolved compliance.
4. Determine reversibility, blast radius, production data impact, external effects and whether the action itself requires explicit approval.
5. Apply the exact gate priority from `references/CONTRACTS.md` in the framework root or the reference script. `autonomy_initiative` controls only low-risk discretionary choices; it cannot allow high-risk or irreversible autonomous actions.
6. Return one of `blocked`, `human_approval_required`, `human_review`, `research_required`, `prototype_and_validate`, or `low_risk_autonomous_proposal`, with reasons.
7. Even a low-risk gate grants **no extra tool permissions**. Ask for explicit authorization to post, spend, change permissions, modify production, or act outside previously permitted work.

Pass the gate and critical questions to `design-validation`. If confidence or risk cannot be justified, err toward research/review rather than a numeric guess.


## V1.2 feedback and publish hook

After producing or materially revising this skill's output, publish a reviewable, versioned artifact with `design-artifact-workspace` (`scripts/workspace.py record`). The HTML navigation section is chosen for this project, not dictated by the skill name. Then evaluate material contradictions with `design-feedback-controller`. If an earlier assumption was invalidated, identify exact affected workflow stages, preserve evidence provenance, and follow the controller outcome. Do not automatically restart the entire workflow or exceed the configured iteration policy.
