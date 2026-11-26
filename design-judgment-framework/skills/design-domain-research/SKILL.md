---
name: design-domain-research
description: Builds and maintains cited domain design knowledge for an AI design agent. Use when working in a new domain or when existing design principles, personas, precedents, risks or product patterns are missing or outdated.
---
# Research the domain, not just popular products

1. Define the domain's characteristic user jobs, failure consequences, roles, task environments and regulatory/security constraints.
2. Select products with meaningfully different audiences and trade-offs. Favor firsthand design docs, design systems, UX studies and first-person decision retrospectives. Include industry counterexamples.
3. For each product distinguish published principles, explicitly documented personas, observed interface behavior, inferred motivations, alternative choices, constraints and known results. Do not infer outcomes from visual patterns.
4. Extract **conditional** rules: `When [user/task/constraint], prefer [pattern], because [mechanism]; except when [countercondition]; validate using [metric]`.
5. Classify each claim: `published_principle`, `documented_decision`, `observed_ui`, `inference`, `hypothesis`, or `outcome_with_evidence`.
6. Track source URL, source type, consulted date, context, applicability, limitations and contradiction cases. Prefer newer original sources for products that evolve rapidly.
7. Write `library/domains/<domain>.json` and `library/precedents/<domain>.json` using the developer examples as *schema demonstrations*, not as universal content. Surface uncovered research questions.

Handoff: the domain rules and research limitations to `design-precedents`; never label heuristics as empirical facts. Revisit records when the UI/product/user context changes.


## V1.2 feedback and publish hook

After producing or materially revising this skill's output, publish a reviewable, versioned artifact with `design-artifact-workspace` (`scripts/workspace.py record`). The HTML navigation section is chosen for this project, not dictated by the skill name. Then evaluate material contradictions with `design-feedback-controller`. If an earlier assumption was invalidated, identify exact affected workflow stages, preserve evidence provenance, and follow the controller outcome. Do not automatically restart the entire workflow or exceed the configured iteration policy.
