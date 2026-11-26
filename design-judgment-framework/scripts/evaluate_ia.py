#!/usr/bin/env python3
"""Score an IA exploration with case-defined axes; ratings are hypothetical, not evidence.

Usage: python3 scripts/evaluate_ia.py --case examples/security-alert-ia.json [--out path]
Optional: --weights overrides.json (JSON mapping of axis keys -> new 0-100 importance values).
"""
import argparse
import json
from pathlib import Path


def bounded(v, lo, hi, label):
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not lo <= v <= hi:
        raise ValueError(f"{label} must be numeric between {lo} and {hi}")
    return float(v)


def resolve(case, overrides=None):
    axes = case["rubric"]["axes"]
    if not isinstance(axes, dict) or len(axes) < 2:
        raise ValueError("IA case must define at least two meaningful axes")
    weights = dict(case["rubric"]["weights"])
    if set(weights) != set(axes):
        raise ValueError("Weights must match exactly the axes defined by the rubric")
    for key, value in (overrides or {}).items():
        if key not in weights:
            raise ValueError(f"Unrecognized IA weight: {key}")
        weights[key] = value
    weights = {k: bounded(v, 0, 100, f"weight {k}") for k, v in weights.items()}
    if not sum(weights.values()):
        raise ValueError("Cannot rank with zero total weight")
    return weights


def fit_score(option, weights):
    fit = option["fit_scores"]
    # Require every axis, even inactive ones, to keep comparison and later edits honest.
    if set(fit) != set(weights):
        raise ValueError(f"{option['id']}: expected fit for every rubric axis, got {sorted(fit)}")
    for k, v in fit.items():
        bounded(v, 0, 5, f"{option['id']}.{k}")
    return round(100 * sum(weights[k] * fit[k] / 5 for k in weights) / sum(weights.values()), 2)


def rank(case, weights):
    eligible, blocked = [], []
    ids = set()
    for option in case["alternatives"]:
        if option["id"] in ids:
            raise ValueError(f"Duplicate IA alternative id: {option['id']}")
        ids.add(option["id"])
        reasons = option.get("known_hard_constraint_violations", [])
        if reasons:
            blocked.append({"id": option["id"], "reasons": reasons})
            continue
        eligible.append({"id":option["id"], "name":option["name"],
                         "score":fit_score(option,weights),
                         "unknown_constraints":option.get("unknown_constraints",[])})
    eligible.sort(key=lambda x: (-x["score"], x["id"]))
    return eligible, blocked


def sensitivity(case, weights, preferred_id, amount=20):
    shifts=[]
    for key in weights:
        for delta in (-amount, amount):
            w = dict(weights); w[key] = min(100, max(0, weights[key] + delta))
            if w[key] == weights[key] or sum(w.values()) == 0:
                continue
            ranking, _ = rank(case, w)
            if ranking and ranking[0]["id"] != preferred_id:
                shifts.append({"axis":key,"from":weights[key],"to":w[key],"new_winner":ranking[0]["id"]})
    return shifts


def evaluate(case, overrides=None):
    weights = resolve(case, overrides)
    ranked, blocked = rank(case, weights)
    top=ranked[0] if ranked else None
    gap=round(top["score"] - ranked[1]["score"], 2) if len(ranked)>1 else None
    shifts=sensitivity(case,weights,top["id"]) if top else []
    uncertainty=bool(case.get("known_evidence_gaps", [])) or any(o["unknown_constraints"] for o in ranked)
    return {
        "case_id":case["case_id"],
        "evaluation_status":"illustrative_ia_fit_estimates_not_user_evidence",
        "profile_origin":case["rubric"].get("weight_origin","unspecified; requires review"),
        "weights_used":weights,
        "ranked_options":ranked,
        "disqualified_options":blocked,
        "preference_leader":top["id"] if top else None,
        "top_two_gap_points":gap,
        "near_tie":gap is not None and gap < 5,
        "winner_sensitive_to_weight_changes":bool(shifts),
        "sensitivity_winner_changes":shifts,
        "evidence_gaps":case.get("known_evidence_gaps", []),
        "requires_independent_ia_validation":uncertainty,
        "decision_policy":"IA ranking is provisional; governance and user research remain separate. No external implementation authorized."
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--case', required=True)
    p.add_argument('--weights')
    p.add_argument('--out')
    args=p.parse_args()
    case=json.loads(Path(args.case).read_text(encoding='utf-8'))
    overrides=json.loads(Path(args.weights).read_text(encoding='utf-8')) if args.weights else None
    result=evaluate(case,overrides)
    if args.out: Path(args.out).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f"IA exploration: {case['title']}")
    for item in result['ranked_options']:
        print(f"  {item['score']:5.2f}  {item['name']}")
    print(f"Provisional preference leader: {result['preference_leader']}; validation required: {result['requires_independent_ia_validation']}")
    print("Scores are hypothetical fit judgments, not measured task performance or approval to implement.")


if __name__ == '__main__':
    main()
