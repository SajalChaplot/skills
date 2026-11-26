# Shared workflow contracts

## Sequence, required stage outputs

1. **Context** (`design-context`): `decision_context` with domain, primary job, users (role × familiarity × context), stakeholders, success metrics, constraints, ambiguity, scope, and action type.
2. **Evidence acquisition** (`design-domain-research`, only if missing, outdated or contradictory): `domain_evidence` with sourced principles and design-decision cases, evidence type, recorded date, strength and limitations. Never treat competitors as proof of outcome.
3. **Precedents** (`design-precedents`): `precedent_shortlist`, each precedent with similarity, contrast, verified source URL, and transferable *conditional* rule. Surface contradictions.
4. **Information architecture** (`design-information-architecture`): `ia_exploration` for organizational, navigational or cross-object questions; otherwise an explicit `skip_reason`. Include object model, 2–4 different information structures, task paths, alternative weaknesses and before-wireframe validation. See `references/IA_CONTRACT.md`.
5. **Options** (`design-options`): 2–4 distinct options with 0–5 fit estimates across the eight axes, reasons, candidate unknowns, sources, and known constraint violations; a preference comparison and sensitivity analysis.
6. **Governance** (`design-governance`): `assessment` with evidence_confidence and risk in [0,1], reversibility, action_requires_approval, hard_constraint_violations, unknown_constraints, justification; `gate` reason.
7. **Validation** (`design-validation`): cheapest discriminating test, target users, outcome metric, guardrail metrics, failure criteria, owner, due condition (not invented date), and resulting update to precedent/library only when verified.
8. **Orchestrator** (`design-judgment`): one decision record combining all stages, preference snapshot, recommendation and uncertainties; optionally use `scripts/evaluate.py` to make scores reproducible.

## Mandatory separation of concepts

- **Preferences**: relative importance chosen by users, documented through org/task profile and provenance. These affect score ranking.
- **Fit scores**: design team's estimates of how well an option serves each preference (0–5). Record rubric and rationale. Not proof.
- **Confidence**: strength of evidence for the recommendation (0–1), explicitly justified, not a control to move upward arbitrarily.
- **Risk**: potential negative impact and cost of reversal (0–1), explicitly justified. Risk is not an organization preference.
- **Constraints**: requirements. A disqualified option cannot win by weights. Unknown constraints must be investigated or escalated.
- **Authorization**: permission for an agent to take an external action; distinct from assessment. Never infer authorization from a high score.

## Axes (stable API keys)

`efficiency`, `learnability`, `discoverability`, `flexibility`, `transparency`, `consistency`, `recoverability`, `collaboration`.

These keys are the **original V1 screen/interaction evaluator axes**. IA exploration can use explicitly defined **case-specific axes** in a separate rubric and scorer; these are not silently converted to or synced with the eight original axes. See `references/IA_CONTRACT.md`.

Scoring formula: `score(option) = 100 × Σ(weight_i × fit_i / 5) / Σ(weight_i)`. The denominator is the **sum of nonnegative active weights**, not always 800. If all weights are 0, refuse to rank. If an option lacks any fit score for a positive-weight axis, mark it incomplete and do not rank it.

Report a gap less than **5 percentage points** as near-tie; this is a heuristic, not a statistically validated threshold. Perform sensitivity analysis by changing each positive weight ±20 points (bounded 0–100); warn if the winner changes. Don't imply this grid exhausts uncertainty.

## Gate policy (v1)

1. `hard_constraint_violations` nonempty → `blocked`; redesign.
2. `unknown_constraints` nonempty → `human_review`; establish compliance before implementation.
3. `action_requires_approval` true → `human_approval_required` regardless of score. Actions touching external systems cannot be authorized via this gate.
4. `risk ≥ 0.65` or not reversible and `risk ≥ 0.30` → `human_approval_required`.
5. `risk ≥ 0.35` and `evidence_confidence < 0.50` → `research_required` before commitment.
6. For reversible choices with risk ≤ `0.20 + 0.002 × initiative` (at most 0.40), confidence ≥ 0.70 → `low_risk_autonomous_proposal` (only authorized internal work); with lower confidence → `prototype_and_validate`.
7. Otherwise → `human_review`.

When several conditions apply, the earlier one wins. Always state gate reasoning and a next step. The tool cannot replace professional oversight in regulated or safety-critical contexts.

## Data contract

`profiles/preferences.json` contains schema_version, organization fields (`priority_weights`, `autonomy_initiative`, `hard_constraints`) and task overrides. An example decision is `examples/developer-project-setup.json`, with task_id, options and `assessment`.


## V1.2 addendum — non-linear iteration and artifact workspace

- The sequence above identifies normal dependencies, **not an irreversible step order**. `workflow.json` contains `depends_on` edges; `design-feedback-controller` permits selective re-entry on documented evidence/contradiction. See `references/ITERATION_POLICY.md` and editable `profiles/iteration-policy.json`.
- After each meaningful stage output, `design-artifact-workspace` records a versioned artifact and generates a project-specific, offline HTML review workspace. See `references/WORKSPACE_CONTRACT.md`. The left-nav sections are authored in `projects/<project-id>.json` and vary by project; do not force one tab per stage.
- Reviewer feedback is exported, triaged and may trigger invalidation; review comments do not automatically become observed research evidence.
- All `STOP` outcomes are provisional, and high-risk/constraint uncertainty escalates. A skill prompt cannot itself enforce live execution limits: explicit controller calls and runtime deadlines are necessary.
