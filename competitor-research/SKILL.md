---
name: competitor-reasoning
description: Investigate competitors through customer jobs, workflows, defaults and product boundaries, then turn evidence into separate product and design recommendations. Use for strategic competitive analysis, UX teardowns, differentiation and screenshot-backed research presentations; not a basic vendor price lookup.
---

# Competitor reasoning

Produce decisions, not a feature inventory alone. Connect the user's problem to competitor evidence, an interpretation, a product implication, a design implication and a concrete validation or action.

## Frame the decision and cohort

Identify the product being designed, target users, job, trigger, stakes and decision this research should inform. Use connected context before asking for missing information. If the product is unspecified, proceed with a clearly labeled assumption about the problem; do not claim a confirmed direct-competitor relationship.

Prefer a small cohort of roughly 3–4 complementary references: a close functional competitor, an established market leader to study expectations, and an adjacent or indirect analogue. Explain each selection. Market scale is not proof of usability. Honor an explicit request for broader coverage: retain a broad inventory and curate a deeper cohort within it rather than silently reducing scope.

Use the same job across the cohort. Compare the complete journey from trigger to resolution, including handoffs and recovery, instead of equating a feature checkbox with successful completion.

## Build an evidence trail

Use current first-party documentation, release notes and actual product interfaces where accessible. Add customer reviews, community posts and interviews when they can answer an important question. Distinguish anecdotes from a sampled theme. Keep source URLs, date checked, plan/role/version, units and scope near the relevant claim.

For consequential findings, record:

- **Evidence:** documented behavior, observed screen, or reported experience.
- **Interpretation:** what the evidence may mean for the customer's job.
- **Confidence and limitation:** what was and was not established.
- **Product implication:** capability, policy, economics, ownership, priority or positioning decision.
- **Design implication:** entry point, information, interaction, state, flow or recovery decision.
- **Action and check:** what to do next and what evidence would justify advancing.

A screenshot proves only what it shows. Documentation is not a usability test. Do not infer behavior from a static image, prevalence from a complaint, or commercial impact from a plausible story. Label inferred costs, illustrative scenarios and unmeasured outcomes.

## Apply the analytical lenses

Use the lenses that inform the decision; report material gaps rather than fabricating a completed study.

**Jobs-to-be-Done:** map trigger → desired outcome → competing solution → remaining friction. Connect the outcome to commercial value as a hypothesis unless supported by customer or business evidence.

**Heuristics and usability:** examine state visibility, user language, control, consistency, error prevention and recovery through the entire job. Separate visible structural issues from interaction hypotheses that require task testing. Name the scenario and completion criterion; avoid unsupported usability scores.

**Win-loss and review mining:** seek the triggering incident, prior workaround, unacceptable failure and deciding tradeoff. Preserve sample scope, dates and source quality. If interviews or systematic review mining did not occur, say so and propose the specific research needed. Do not call a missing feature a lost-deal reason without evidence.

**Changelog and delta tracking:** compare dated versions of the same journey, default or rule. Distinguish a release announcement from observed behavior. Do not infer R&D velocity, a strategic pivot or architecture from a single release. Do not create recurring monitoring unless requested.

**The invisible feature:** distinguish (1) an explicit unsupported boundary, (2) absence in reviewed documentation, and (3) a genuinely observed omission. Explore explanations such as product scope, simplicity, economics or separate systems as hypotheses. Absence does not establish deliberate rejection, failed testing or inability to scale. Include counter-evidence that would invalidate the inference.

**Defaults:** ask what happens if the admin or user changes nothing. Inspect scope, permissions, inherited rules, opt-ins, notifications, stopping behavior, resets and exceptions. Trace what a default change does to existing overrides. Defaults reveal actual behavior; intent and technical constraints require separate evidence.

**Avoid fast-follow:** identify the underlying structural problem before recommending a copied capability. Decide what to match as a useful baseline and where to differentiate around the user's job. Keep a proposed solution separate from the competitor's current behavior.

## Show the evidence

Pair recommendations with actual screens when available. Annotate the entry point, useful pattern, friction hypothesis and proposed response. Link each annotation to its evidence. Show a documented journey as such; reserve “tested walkthrough” for interactions actually performed.

Prefer complete published app views and full-page captures where legitimately available. Label sections, dialogs, historical community images and conceptual visuals honestly. Do not fabricate surrounding UI, stitch unrelated states into an alleged screenshot, or present a documentation page as the product interface. Explain meaningful access gaps and continue with supported evidence.

For each product gallery, add a **Pattern to borrow** callout that connects the observed pattern to the user's specific problem, with controls opening its supporting screenshots.

## End with insight to action

State a counter-strategy: what to match, what structural problem to solve differently, why that matters and which assumptions remain open. Supply a prioritized table:

**Insight + evidence → action → product responsibility → design responsibility → acceptance/validation check → priority and dependency.**

Suggest responsibility types, not assignments to real people. Include tradeoffs and a decision gate. Success metrics must reflect the desired outcome and its guardrails, not merely feature adoption. Label suggested metrics and set numerical targets only when a baseline or user instruction supports them. Identify what to defer and what evidence would change the recommendation.

## Resources and presentation

- For a finished presentation or research artifact, read [presentation-layout.md](references/presentation-layout.md). It includes the tabbed HTML layout and a deck storyboard. Adapt to the requested format; do not force every answer into HTML or slides.
- For a concrete application, read [worked-example.md](references/worked-example.md). It contains a historical AI-spend example and links to evidence assets. Reverify vendor behavior before reusing facts.
- [Worked HTML example](assets/ai-spend-example.html) preserves the actual layout and interactions from the original project. Treat its content as dated example material, not a universal template or current source. Inspect relevant style/interaction portions rather than loading the entire embedded-image file into context.
