#!/usr/bin/env python3
"""Project-defined HTML workspace: record artifacts and build self-contained review HTML.

build: python3 scripts/workspace.py build --project projects/security-alert.json --out workspace-output/security-alert.html --policy profiles/iteration-policy.json
record: python3 scripts/workspace.py record --project projects/security-alert.json --artifact examples/agent-artifact-event.json --out workspace-output/security-alert.html --policy profiles/iteration-policy.json

Artifact events are versioned, and existing artifact IDs are updated in place.
The HTML shell is fixed; the project decides sections, labels, order and content.
"""
from __future__ import annotations

import argparse
import base64
import copy
import datetime as dt
import json
import mimetypes
from pathlib import Path

MAX_IMAGE_BYTES = 8 * 1024 * 1024
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def validate_project(project):
    if not isinstance(project, dict) or not isinstance(project.get("project_id"), str) or not project.get("project_id"):
        raise ValueError("Project must have a project_id")
    if not isinstance(project.get("title"), str) or not project.get("title"):
        raise ValueError("Project must have a title")
    sections = project.get("sections")
    if not isinstance(sections, list):
        raise ValueError("Project sections must be an array, possibly empty")
    seen = set()
    for section in sections:
        if not section.get("id") or not section.get("title") or section["id"] in seen:
            raise ValueError("Section IDs and titles must be nonempty and section IDs unique")
        seen.add(section["id"])
        a_seen = set()
        for art in section.get("artifacts", []):
            if not art.get("id") or art["id"] in a_seen:
                raise ValueError(f"Artifact IDs must be unique within section {section['id']}")
            a_seen.add(art["id"])
            for block in art.get("blocks", []):
                if not isinstance(block, dict) or not isinstance(block.get("type", "text"), str):
                    raise ValueError("Artifact blocks must be structured objects")
    return project


def image_data(project, base):
    p = copy.deepcopy(project)
    base = base.resolve()
    for section in p["sections"]:
        for artifact in section.get("artifacts", []):
            for block in artifact.get("blocks", []):
                if block.get("type") != "image" or "local_path" not in block:
                    continue
                rel = block.pop("local_path")
                path = (base / rel).resolve()
                if path != base and base not in path.parents:
                    raise ValueError("Image local_path must stay inside the project folder")
                if path.suffix.lower() not in IMAGE_EXTS:
                    raise ValueError("Only PNG, JPEG, WebP and GIF images can be embedded")
                if path.stat().st_size > MAX_IMAGE_BYTES:
                    raise ValueError("Image is too large to embed")
                mime = mimetypes.guess_type(str(path))[0]
                block["src"] = f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"
    return p


def build(project_path, output_path, template_path, policy_path=None, run_state_path=None):
    project_path, output_path, template_path = map(Path, (project_path, output_path, template_path))
    project = json.loads(project_path.read_text(encoding="utf-8"))
    validate_project(project)
    if policy_path:
        project["iteration_policy"] = json.loads(Path(policy_path).read_text(encoding="utf-8"))
    if run_state_path and Path(run_state_path).exists():
        project["iteration_state"] = json.loads(Path(run_state_path).read_text(encoding="utf-8"))
    safe_project = image_data(project, project_path.parent)
    payload = json.dumps(safe_project, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    template = template_path.read_text(encoding="utf-8")
    if template.count("__PROJECT_DATA__") != 1:
        raise ValueError("HTML template must contain one project data insertion point")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(template.replace("__PROJECT_DATA__", payload), encoding="utf-8")
    return output_path


def record(project_path, event_path):
    project_path, event_path = Path(project_path), Path(event_path)
    project = json.loads(project_path.read_text(encoding="utf-8"))
    evt = json.loads(event_path.read_text(encoding="utf-8"))
    section_id = evt.get("section_id")
    artifact = evt.get("artifact")
    if not section_id or not isinstance(artifact, dict) or not artifact.get("id") or not artifact.get("title"):
        raise ValueError("Event requires section_id and artifact with id and title")
    match = next((s for s in project["sections"] if s["id"] == section_id), None)
    if match is None:
        if not evt.get("section_title"):
            raise ValueError("New section needs section_title")
        match = {"id": section_id, "title": evt["section_title"], "description": evt.get("section_description", ""),
                 "group": evt.get("section_group", "Project"), "artifacts": []}
        project["sections"].append(match)
    existing = next((a for a in match.get("artifacts", []) if a["id"] == artifact["id"]), None)
    artifact = copy.deepcopy(artifact)
    artifact["updated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    if existing:
        artifact["version"] = existing.get("version", 1) + 1
        artifact["review_status"] = "pending"  # Every changed artifact requires renewed verification.
        match["artifacts"][match["artifacts"].index(existing)] = artifact
    else:
        artifact.setdefault("version", 1)
        match.setdefault("artifacts", []).append(artifact)
    project["version"] = project.get("version", 1) + 1
    validate_project(project)
    project_path.write_text(json.dumps(project, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return project


def apply_controller_result(project_path, result, event, run_state):
    """Connect feedback events with reviewable project artifacts and stale downstream outputs."""
    project_path = Path(project_path)
    project = json.loads(project_path.read_text(encoding="utf-8"))
    validate_project(project)
    if result["action"] == "REVISIT":
        targets = set(result.get("rerun_stages", []))
        for section in project["sections"]:
            for art in section.get("artifacts", []):
                if art.get("origin_stage") in targets:
                    art["stale"] = True
                    art["review_status"] = "pending"
    history_id = project.get("workflow_history_section_id")
    if history_id:
        section = next((s for s in project["sections"] if s["id"] == history_id), None)
        if section is None:
            section={"id":history_id,"title":project.get("workflow_history_section_title","Iteration history"),
                     "group":project.get("workflow_history_section_group","Review"),"description":"Reviewable decision-controller events and re-entry decisions.","artifacts":[]}
            project["sections"].append(section)
        evt_index = len(run_state.get("events", []))
        artifact = {
            "id": f"feedback-event-{evt_index:03d}",
            "title": f"Feedback checkpoint {evt_index}: {result['action']}",
            "summary": result["reason"],
            "version": 1,
            "review_status": "pending",
            "evidence_level": "controller_output_not_user_research",
            "decision_id": event["decision_id"],
            "origin_stage": "feedback_controller",
            "blocks": [
                {"type":"table","title":"Checkpoint","columns":["Field","Recorded value"],"rows":[
                    ["Trigger",event.get("trigger","checkpoint")],
                    ["Controller outcome",result["action"]],
                    ["Invalidated stages",", ".join(event.get("invalidates", [])) or "None"],
                    ["Rerun stages", " → ".join(result.get("rerun_stages", [])) or "None"],
                    ["Decision revisions",str(result.get("decision_revisions",0))],
                    ["Elapsed minutes",str(result.get("elapsed_minutes",0))],
                ]},
                {"type":"callout","heading":"Reason and next step","text": event.get("reason","") + " | " + result["reason"],
                 "tone":"warning" if result["action"] in ("VALIDATE","STOP","ESCALATE") else ""}
            ]
        }
        section["artifacts"].append(artifact)
    project["project_status"] = {"STOP":"provisional","ESCALATE":"blocked","VALIDATE":"in_review","REVISIT":"in_review"}.get(result["action"],project.get("project_status","in_review"))
    project["version"] = project.get("version", 1) + 1
    validate_project(project)
    project_path.write_text(json.dumps(project, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return project


def main():
    root = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("build", "record"):
        a = sub.add_parser(name)
        a.add_argument("--project", required=True)
        a.add_argument("--out", required=True)
        a.add_argument("--policy")
        a.add_argument("--run-state")
        a.add_argument("--template", default=str(root / "web" / "workspace-template.html"))
        if name == "record":
            a.add_argument("--artifact", required=True)
    args = p.parse_args()
    if args.command == "record":
        record(args.project, args.artifact)
    result = build(args.project, args.out, args.template, args.policy, args.run_state)
    print(f"Built {result} ({result.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
