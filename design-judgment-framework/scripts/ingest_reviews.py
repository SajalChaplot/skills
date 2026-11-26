#!/usr/bin/env python3
"""Triage exported HTML workspace review feedback for a design agent (stdlib only).

Does not treat reviewer comments as validated user research or auto-trigger redesign.
Usage: python3 scripts/ingest_reviews.py --project projects/security-alert-review.json --reviews path/to/reviews.json --out workspace-output/review-triage.json
"""
import argparse
import json
from pathlib import Path


def ingest(project, export):
    if export.get('project_id') != project.get('project_id'):
        raise ValueError('Review project_id does not match project manifest')
    artifact_map={f"{s['id']}::{a['id']}":(s,a) for s in project['sections'] for a in s.get('artifacts',[])}
    triage=[]
    for key, record in export.get('reviews', {}).items():
        if key not in artifact_map:
            triage.append({'artifact_key':key,'state':'unknown_artifact','action':'investigate'})
            continue
        section,art=artifact_map[key]
        review_version=record.get('artifact_version')
        version_match=review_version==art.get('version',1)
        triage.append({
            'artifact_key':key,
            'artifact_title':art['title'],
            'decision_id':art.get('decision_id'),
            'origin_stage':art.get('origin_stage'),
            'reviewed_version':review_version,
            'current_version':art.get('version',1),
            'review_status':record.get('status','pending'),
            'review_note':record.get('note',''),
            'state':'current' if version_match else 'older_artifact_version',
            'action':('assess_possible_invalidation' if version_match and record.get('status')=='needs_revision' else
                      'verify_on_current_version' if not version_match else 'no_reopen_required'),
            'evidence_classification':'human_review_feedback_not_verified_user_research'
        })
    return {'schema_version':'1.2','project_id':project['project_id'],
            'needs_assessment':sum(x['action']=='assess_possible_invalidation' for x in triage),
            'items':triage,
            'next_step':'Agent must assess each possible invalidation, establish provenance and scope, then submit appropriate event to feedback controller. This export does not auto-authorize a redesign.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project',required=True);p.add_argument('--reviews',required=True);p.add_argument('--out')
    a=p.parse_args()
    result=ingest(json.loads(Path(a.project).read_text()),json.loads(Path(a.reviews).read_text()))
    payload=json.dumps(result,indent=2)+'\n'
    if a.out: Path(a.out).write_text(payload)
    print(payload)

if __name__=='__main__':main()
