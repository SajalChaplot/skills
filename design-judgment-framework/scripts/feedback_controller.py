#!/usr/bin/env python3
"""Configurable bounded non-linear design workflow controller (stdlib only).

Examples:
 python3 scripts/feedback_controller.py --policy profiles/iteration-policy.json \
   --workflow workflow.json --state projects/alert-iteration-state.json \
   --event examples/controller-events/revisit-ia.json --out workspace-output/controller-result.json

Only controller invocations are enforceable. Agents must report tool-call counts and must
call the controller after each significant checkpoint. External actions are never authorized.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
from pathlib import Path
from typing import Any

REVISIT_TRIGGERS = {"new_evidence", "contradiction", "failed_validation", "constraint_change", "material_weakness"}
DEFAULT_POLICY_KEYS = {"revision_limits", "execution_budget", "convergence", "reentry", "exhaustion"}
VALID_OUTCOMES = {"CONTINUE", "REVISIT", "VALIDATE", "STOP", "ESCALATE"}


def utc_now():
    return dt.datetime.now(dt.timezone.utc)


def parse_time(value):
    if isinstance(value, dt.datetime):
        parsed = value
    else:
        parsed = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")
    return parsed.astimezone(dt.timezone.utc)


def merge_policy(base: dict, override: dict | None) -> dict:
    result = copy.deepcopy(base)
    if override:
        if set(override) - DEFAULT_POLICY_KEYS:
            raise ValueError("Override may edit only iteration-policy sections")
        for k, v in override.items():
            if not isinstance(v, dict) or k not in result:
                raise ValueError(f"Invalid policy override section: {k}")
            if set(v) - set(result[k]):
                raise ValueError(f"Unknown policy key(s): {set(v)-set(result[k])}")
            result[k].update(v)
    validate_policy(result)
    return result


def _integer(value, name, lower=0, upper=100000):
    if isinstance(value, bool) or not isinstance(value, int) or not lower <= value <= upper:
        raise ValueError(f"{name} must be an integer in [{lower}, {upper}]")


def validate_policy(p):
    if not all(k in p for k in DEFAULT_POLICY_KEYS):
        raise ValueError("Policy missing required sections")
    for k, v in p["revision_limits"].items():
        _integer(v, f"revision_limits.{k}", 1, 100)
    _integer(p["execution_budget"]["max_elapsed_minutes"], "max_elapsed_minutes", 1, 10080)
    _integer(p["execution_budget"]["max_reported_tool_calls"], "max_reported_tool_calls", 1, 100000)
    _integer(p["convergence"]["max_stagnant_cycles"], "max_stagnant_cycles", 1, 100)
    delta = p["convergence"]["min_meaningful_rubric_delta"]
    if isinstance(delta, bool) or not isinstance(delta, (int, float)) or not 0 <= delta <= 100:
        raise ValueError("min_meaningful_rubric_delta must be 0..100")
    if not isinstance(p["convergence"]["require_novel_evidence_or_change"], bool):
        raise ValueError("require_novel_evidence_or_change must be boolean")
    if not isinstance(p["reentry"]["allowed_triggers"], list) or not set(p["reentry"]["allowed_triggers"]) <= REVISIT_TRIGGERS:
        raise ValueError("Invalid reentry.allowed_triggers")
    for k in ("rerun_affected_downstream", "require_invalidation_targets", "allow_explicit_human_reopen"):
        if not isinstance(p["reentry"][k], bool):
            raise ValueError(f"{k} must be boolean")
    for k in ("material_risk", "unresolved_mandatory_constraints"):
        if p["exhaustion"][k] != "escalate":
            raise ValueError(f"Safety invariant: exhaustion.{k} must stay 'escalate'")
    if p["exhaustion"]["otherwise"] != "stop_provisional":
        raise ValueError("Safety invariant: exhausted decisions are provisional, never approved")


def stages(workflow):
    ids = [s["id"] for s in workflow["stages"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate stage id")
    by_id = {s["id"]: s for s in workflow["stages"]}
    for s in workflow["stages"]:
        for dep in s.get("depends_on", []):
            if dep not in by_id:
                raise ValueError(f"Unknown dependency {dep} for {s['id']}")
    return ids, by_id


def affected_path(workflow, targets, cascade=True):
    order, by_id = stages(workflow)
    bad = set(targets) - set(order)
    if bad:
        raise ValueError(f"Unknown invalidated workflow stage(s): {sorted(bad)}")
    affected = set(targets)
    if cascade:
        keep_running = True
        while keep_running:
            before = len(affected)
            affected.update(s["id"] for s in workflow["stages"] if any(d in affected for d in s.get("depends_on", [])))
            keep_running = len(affected) > before
    return [s for s in order if s in affected]


def initial_state(now=None):
    return {
        "schema_version": "1.2",
        "started_at": (now or utc_now()).isoformat(),
        "total_revisions": 0,
        "reported_tool_calls": 0,
        "decisions": {},
        "stage_reentries": {},
        "events": []
    }


def _outcome(action, reason, state, rerun_stages=None, status="in_progress", warnings=None):
    if action not in VALID_OUTCOMES:
        raise ValueError("Unknown controller action")
    return {
        "action": action,
        "status": status,
        "reason": reason,
        "rerun_stages": rerun_stages or [],
        "budgets_used": {
            "total_revisions": state["total_revisions"],
            "reported_tool_calls": state["reported_tool_calls"],
            "stage_reentries": dict(state["stage_reentries"])
        },
        "warnings": warnings or [],
        "authorization": "No production, external, irreversible, or privileged action authorized"
    }


def evaluate_event(policy, workflow, state, event, now=None):
    """Return (controller_result, updated_state) without touching files."""
    validate_policy(policy)
    now = parse_time(now or utc_now())
    state = copy.deepcopy(state)
    if not event.get("decision_id") or not event.get("reason"):
        raise ValueError("Event must contain decision_id and reason")
    decision_id = event["decision_id"]
    if event.get("risk_level", "unknown") not in {"low", "material", "high", "unknown"}:
        raise ValueError("risk_level must be low, material, high or unknown")
    if event.get("mandatory_constraint_status", "unknown") not in {"clear", "unknown", "violated"}:
        raise ValueError("mandatory_constraint_status must be clear, unknown or violated")
    trigger = event.get("trigger", "checkpoint")
    if trigger not in (REVISIT_TRIGGERS | {"checkpoint", "needs_validation", "complete", "explicit_human_reopen"}):
        raise ValueError(f"Unknown trigger: {trigger}")
    _integer(event.get("tool_calls_delta", 0), "tool_calls_delta", 0)
    state["reported_tool_calls"] += event.get("tool_calls_delta", 0)
    decision = state["decisions"].setdefault(decision_id, {"revisions": 0, "stagnant_cycles": 0, "known_evidence_ids": [], "change_fingerprints": []})
    evidence = set(event.get("new_evidence_ids", [])) - set(decision["known_evidence_ids"])
    fingerprint = event.get("material_change_fingerprint")
    new_change = bool(fingerprint) and fingerprint not in decision["change_fingerprints"]
    improvement = event.get("rubric_delta")
    if improvement is not None:
        if isinstance(improvement, bool) or not isinstance(improvement, (int, float)) or not -100 <= improvement <= 100:
            raise ValueError("rubric_delta must be a signed numeric 0..100 change")
        if not event.get("rubric_id"):
            raise ValueError("rubric_delta requires rubric_id; compare only scores on the same rubric")
    elapsed = (now - parse_time(state["started_at"])).total_seconds() / 60
    if elapsed < 0:
        raise ValueError("Event time is earlier than project start")
    event_summary = {"at": now.isoformat(), "decision_id": decision_id, "trigger": trigger, "reason": event["reason"]}
    # Block external execution and mandatory-constraint violations regardless of policy.
    if event.get("mandatory_constraint_status") == "violated":
        result = _outcome("ESCALATE", "Known mandatory constraint violation. Redesign or obtain appropriate human resolution; no autonomous release.", state, status="blocked")
    elif event.get("external_action_requested", False):
        result = _outcome("ESCALATE", "Explicit human authorization required for external/privileged execution.", state, status="approval_required")
    else:
        budget = policy["execution_budget"]
        exhausted = []
        if elapsed >= budget["max_elapsed_minutes"]:
            exhausted.append("elapsed time")
        if state["reported_tool_calls"] >= budget["max_reported_tool_calls"]:
            exhausted.append("reported tool calls")
        if decision.get("terminal_action") and trigger != "explicit_human_reopen":
            result = _outcome(decision["terminal_action"],
                              "This decision's previous terminal state remains in effect. A human-approved reopen with an updated policy/run is required to resume.",
                              state, status=decision.get("terminal_status", "provisional"))
        elif exhausted:
            risk = event.get("risk_level", "unknown")
            unknown_constraint = event.get("mandatory_constraint_status", "unknown") != "clear"
            escal = risk in ("material", "high", "unknown") or unknown_constraint
            result = _outcome("ESCALATE" if escal else "STOP", "Budget exhausted: " + ", ".join(exhausted), state,
                              status="needs_human_review" if escal else "provisional",
                              warnings=["Tool-call budget applies only to usage reported by the agent/runtime."])
        elif trigger == "checkpoint":
            result = _outcome("CONTINUE", "No relevant change to an earlier decision; continue current work.", state)
        elif trigger == "needs_validation":
            result = _outcome("VALIDATE", "More design reasoning is not a substitute for missing external evidence.", state, status="awaiting_evidence")
        elif trigger == "complete":
            risk = event.get("risk_level", "unknown")
            constraints = event.get("mandatory_constraint_status", "unknown")
            gate = event.get("approval_gate", "human_review")
            if risk in ("high", "material", "unknown") or constraints != "clear" or gate in ("human_approval_required", "human_review", "blocked"):
                result = _outcome("ESCALATE", "Design reasoning finished, but risk, constraints or authorization remain unresolved.", state, status="needs_human_review")
            else:
                result = _outcome("STOP", "Decision exploration complete within budget; implementation permissions remain separate.", state, status="provisional_or_reviewed")
        else:
            explicit = trigger == "explicit_human_reopen"
            if explicit and (not policy["reentry"]["allow_explicit_human_reopen"] or not event.get("human_approved", False)):
                result = _outcome("ESCALATE", "Human-approved reopening is required; do not infer permission.", state, status="approval_required")
            elif trigger not in policy["reentry"]["allowed_triggers"] and not explicit:
                result = _outcome("CONTINUE", f"Re-entry trigger {trigger} disabled in policy.", state)
            else:
                if explicit:
                    decision["stagnant_cycles"] = 0
                    decision.pop("terminal_action", None)
                    decision.pop("terminal_status", None)
                targets = event.get("invalidates", [])
                if policy["reentry"]["require_invalidation_targets"] and not targets:
                    raise ValueError("Re-entry requires one or more invalidated stages")
                rerun = affected_path(workflow, targets, policy["reentry"]["rerun_affected_downstream"])
                limits = policy["revision_limits"]
                exceeded = []
                if decision["revisions"] >= limits["per_decision"]:
                    exceeded.append("per-decision revisions")
                if state["total_revisions"] >= limits["total_per_project"]:
                    exceeded.append("total project revisions")
                if any(state["stage_reentries"].get(s, 0) >= limits["per_stage"] for s in rerun):
                    exceeded.append("stage re-entries")
                if exceeded:
                    escal = event.get("risk_level", "unknown") in ("material", "high", "unknown") or event.get("mandatory_constraint_status", "unknown") != "clear"
                    result = _outcome("ESCALATE" if escal else "STOP", "Revision budget exhausted: " + ", ".join(exceeded), state,
                                      status="needs_human_review" if escal else "provisional")
                else:
                    meaningful = bool(evidence) or new_change or (improvement is not None and improvement >= policy["convergence"]["min_meaningful_rubric_delta"])
                    if not meaningful:
                        decision["stagnant_cycles"] += 1
                    else:
                        decision["stagnant_cycles"] = 0
                    if decision["stagnant_cycles"] >= policy["convergence"]["max_stagnant_cycles"]:
                        risk = event.get("risk_level", "unknown")
                        escal = risk in ("material", "high", "unknown") or event.get("mandatory_constraint_status", "unknown") != "clear"
                        result = _outcome("ESCALATE" if escal else "STOP", "Convergence stop: successive revisions supplied no material improvement or new evidence.", state,
                                          status="needs_human_review" if escal else "provisional")
                    elif policy["convergence"]["require_novel_evidence_or_change"] and not meaningful and not explicit:
                        result = _outcome("VALIDATE", "No new evidence, measurable improvement, or unique material change; collect evidence before reopening.", state, status="awaiting_evidence")
                    else:
                        decision["revisions"] += 1
                        state["total_revisions"] += 1
                        for s in rerun:
                            state["stage_reentries"][s] = state["stage_reentries"].get(s, 0) + 1
                        decision["known_evidence_ids"].extend(sorted(evidence))
                        if new_change:
                            decision["change_fingerprints"].append(fingerprint)
                        result = _outcome("REVISIT", "Reopen only invalidated stage(s) and their dependent outputs; preserve unaffected evidence.", state, rerun,
                                          warnings=["Previously displayed downstream artifacts should be marked stale until rebuilt."])
    if result["action"] in ("STOP", "ESCALATE"):
        decision["terminal_action"] = result["action"]
        decision["terminal_status"] = result["status"]
    event_summary["result"] = result["action"]
    event_summary["rerun_stages"] = result["rerun_stages"]
    state["events"].append(event_summary)
    result["decision_id"] = decision_id
    result["elapsed_minutes"] = round(elapsed, 3)
    result["decision_revisions"] = decision["revisions"]
    result["stagnant_cycles"] = decision["stagnant_cycles"]
    return result, state


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--policy", required=True)
    p.add_argument("--project-policy")
    p.add_argument("--workflow", required=True)
    p.add_argument("--state", required=True)
    p.add_argument("--event")
    p.add_argument("--init-only", action="store_true", help="Initialize run-state at project/session start, before expensive exploration")
    p.add_argument("--out")
    p.add_argument("--project", help="Optional project manifest to mark affected artifacts stale and publish the controller outcome")
    p.add_argument("--workspace-out", help="Output HTML for --project integration")
    args = p.parse_args()
    policy = merge_policy(json.loads(Path(args.policy).read_text()), json.loads(Path(args.project_policy).read_text()) if args.project_policy else None)
    workflow = json.loads(Path(args.workflow).read_text())
    state_path = Path(args.state)
    if args.init_only:
        if not state_path.exists():
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(json.dumps(initial_state(), indent=2) + "\n")
            print(f"Initialized design run: {state_path}")
        else:
            print(f"Run already initialized, preserving start time and counters: {state_path}")
        return
    if not args.event:
        p.error("--event is required unless --init-only is set")
    event = json.loads(Path(args.event).read_text())
    state = json.loads(state_path.read_text()) if state_path.exists() else initial_state()
    result, next_state = evaluate_event(policy, workflow, state, event)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(next_state, indent=2) + "\n")
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(result, indent=2) + "\n")
    if args.project:
        from workspace import apply_controller_result, build
        apply_controller_result(args.project, result, event, next_state)
        if args.workspace_out:
            build(args.project, args.workspace_out, Path(__file__).resolve().parent.parent / "web/workspace-template.html", args.policy, args.state)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
