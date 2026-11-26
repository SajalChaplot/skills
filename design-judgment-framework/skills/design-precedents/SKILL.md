---
name: design-precedents
description: Retrieves and critically compares real design precedents from relevant products. Use to understand competing UX decisions and derive conditional rules for the present decision without copying competitors blindly.
---
# Retrieve relevant precedents

1. Read decision context and domain library. Retrieve 3–5 closest cases by **user job and stakes**, not just industry or recognizable brand. If fewer than two solid cases exist, say so.
2. For each, report source URL, evidence class, actual choice, documented alternative, observed or unknown outcome, and how this differs from the current case.
3. Search specifically for a counterexample where an apparently relevant rule produced a different design due to a different constraint.
4. Extract “When / Prefer / Because / Unless / Verify” transfer statements; mark each as verified quotation, inference, or hypothesis.
5. Rank source applicability and strength **qualitatively**. Public marketing pages or competitor screenshots are weak evidence of user outcomes.
6. Explicitly state transfer limits (different user maturity, risk, volume, platform or organization).

Output `precedent_shortlist`; pass conditional rules to `design-options` and uncertainty to `design-governance`. If no relevant evidence exists, advise a cheap discriminating test, not fabricated precedent.


## V1.2 feedback and publish hook

After producing or materially revising this skill's output, publish a reviewable, versioned artifact with `design-artifact-workspace` (`scripts/workspace.py record`). The HTML navigation section is chosen for this project, not dictated by the skill name. Then evaluate material contradictions with `design-feedback-controller`. If an earlier assumption was invalidated, identify exact affected workflow stages, preserve evidence provenance, and follow the controller outcome. Do not automatically restart the entire workflow or exceed the configured iteration policy.
