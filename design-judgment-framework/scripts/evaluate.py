#!/usr/bin/env python3
"""Dependency-free, inspectable preference scoring + conservative autonomy gating.
Not a prediction of user outcomes or a license to perform actions.
"""
import argparse
import json
from pathlib import Path

AXES = ("efficiency", "learnability", "discoverability", "flexibility",
        "transparency", "consistency", "recoverability", "collaboration")


def bounded(value, low, high, field):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not low <= value <= high:
        raise ValueError(f"{field} must be a number between {low} and {high}")
    return float(value)


def resolve_preferences(config, task_id):
    org = config["organization"]
    weights = dict(org["priority_weights"])
    if set(weights) != set(AXES):
        raise ValueError("Organization must configure exactly the 8 supported axes")
    initiative = org["autonomy_initiative"]
    task = next((t for t in config.get("tasks", []) if t["id"] == task_id), None)
    if task:
        for key, value in task.get("priority_weight_overrides", {}).items():
            if key not in AXES:
                raise ValueError(f"Unknown task override axis: {key}")
            weights[key] = value
        initiative = task.get("autonomy_initiative_override", initiative)
    weights = {k: bounded(v, 0, 100, f"weight {k}") for k, v in weights.items()}
    initiative = bounded(initiative, 0, 100, "autonomy initiative")
    if sum(weights.values()) <= 0:
        raise ValueError("All weights are zero; cannot rank choices")
    return weights, initiative, task


def option_score(option, weights):
    fit = option["fit_scores"]
    for axis, weight in weights.items():
        if weight and axis not in fit:
            raise ValueError(f"Option {option['id']} lacks score for active axis {axis}")
    for axis, value in fit.items():
        if axis not in AXES:
            raise ValueError(f"Unknown fit axis {axis}")
        bounded(value, 0, 5, f"fit {option['id']}.{axis}")
    return round(100 * sum(weights[a] * fit.get(a, 0) / 5 for a in AXES) / sum(weights.values()), 2)


def autonomy_gate(assessment, initiative):
    conf = bounded(assessment["evidence_confidence"], 0, 1, "evidence confidence")
    risk = bounded(assessment["risk"], 0, 1, "risk")
    if assessment.get("hard_constraint_violations"):
        return "blocked", "Documented mandatory-constraint violations cannot be traded against preference weights."
    if assessment.get("unknown_constraints"):
        return "human_review", "Mandatory-constraint status is unknown; establish requirements before implementation."
    if assessment.get("action_requires_approval", False):
        return "human_approval_required", "The requested external/privileged action requires explicit approval."
    if risk >= .65 or (not assessment.get("reversible", False) and risk >= .30):
        return "human_approval_required", "Impact is high or meaningful harm cannot be readily reversed."
    if risk >= .35 and conf < .50:
        return "research_required", "Risk is material but evidence is insufficient."
    allowed = .20 + .002 * initiative  # never above .40
    if assessment.get("reversible", False) and risk <= allowed:
        if conf >= .70:
            return "low_risk_autonomous_proposal", "Low-risk, reversible and well-supported; internal authorized work only."
        return "prototype_and_validate", "Low-risk reversible hypothesis, but further evidence is needed before commitment."
    return "human_review", "Risk/confidence do not meet the limited low-risk autonomy criteria."


def ordered_options(case, weights):
    ranked = []
    rejected = []
    for option in case["options"]:
        violations = option.get("violates_constraints", [])
        if violations:
            rejected.append({"id": option["id"], "reason": "Constraint violations: " + "; ".join(violations)})
            continue
        ranked.append({"id": option["id"], "name": option["name"], "score": option_score(option, weights)})
    ranked.sort(key=lambda o: (-o["score"], o["id"]))
    return ranked, rejected


def sensitivity(case, weights, leading_id):
    changes=[]
    for axis in AXES:
        for delta in (-20, 20):
            altered=dict(weights)
            altered[axis]=max(0, min(100, weights[axis]+delta))
            if altered[axis] == weights[axis] or sum(altered.values()) == 0:
                continue
            ranked, _ = ordered_options(case, altered)
            if ranked and ranked[0]["id"] != leading_id:
                changes.append({"axis":axis, "weight_from":weights[axis], "weight_to":altered[axis], "winner":ranked[0]["id"]})
    return changes


def evaluate(config, case):
    weights, initiative, task = resolve_preferences(config, case["task_id"])
    ranked, rejected = ordered_options(case, weights)
    gate, reason = autonomy_gate(case["assessment"], initiative)
    if not ranked:
        gate, reason = "blocked", "No candidate is eligible due to known mandatory constraint violations."
    top = ranked[0] if ranked else None
    second = ranked[1] if len(ranked) > 1 else None
    gap = round(top["score"]-second["score"], 2) if top and second else None
    shifts = sensitivity(case, weights, top["id"]) if top else []
    return {
      "case_id":case["case_id"],"task_id":case["task_id"],
      "evaluation_status":"illustrative_estimates_not_outcome_evidence",
      "weights_used":weights,"autonomy_initiative_used":initiative,
      "task_override_active":task is not None,
      "ranked_options":ranked,"disqualified_options":rejected,
      "preferred_option":top["id"] if top else None,"top_two_gap_points":gap,
      "near_tie": gap is not None and gap < 5,
      "sensitivity_winner_changes":shifts,"ranking_sensitive":bool(shifts),
      "assessment":case["assessment"],"gate":gate,"gate_reason":reason,
      "disclaimer":"Preference scores are estimated fit ratings, not measured outcomes, evidence confidence, or authorization to act."
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', required=True)
    parser.add_argument('--case', required=True)
    parser.add_argument('--out')
    args=parser.parse_args()
    with open(args.config,encoding='utf-8') as f: config=json.load(f)
    with open(args.case,encoding='utf-8') as f: case=json.load(f)
    result=evaluate(config, case)
    out=json.dumps(result,indent=2)
    if args.out:
        Path(args.out).write_text(out+'\n',encoding='utf-8')
    print(f"Decision: {case['title']}")
    for item in result['ranked_options']:
        print(f"  {item['score']:5.2f}  {item['name']}")
    print(f"Gate: {result['gate']} — {result['gate_reason']}")
    if result['near_tie']: print('Caution: top choices are within 5 points (near tie).')
    if result['ranking_sensitive']: print('Caution: ranking changes with a ±20 weight sensitivity probe.')
    print('Scores are illustrative estimates; no autonomous external action is authorized.')


if __name__=='__main__':
    main()
