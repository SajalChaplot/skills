import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/'scripts'))
from workspace import apply_controller_result
from feedback_controller import initial_state,evaluate_event
from ingest_reviews import ingest

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/'project.json'
        self.project=json.loads((ROOT/'projects/security-alert-review.json').read_text())
        self.path.write_text(json.dumps(self.project))
    def tearDown(self):self.tmp.cleanup()

    def test_feedback_marks_only_invalidated_downstream_stale_and_logs(self):
        now=dt.datetime(2026,11,26,tzinfo=dt.timezone.utc)
        event={'decision_id':'security-alert-navigation','reason':'Asset pivot fails','trigger':'contradiction',
               'invalidates':['information_architecture'],'new_evidence_ids':['finding-1'],
               'risk_level':'low','mandatory_constraint_status':'clear'}
        policy=json.loads((ROOT/'profiles/iteration-policy.json').read_text())
        workflow=json.loads((ROOT/'workflow.json').read_text())
        result,state=evaluate_event(policy,workflow,initial_state(now),event,now+dt.timedelta(minutes=1))
        out=apply_controller_result(self.path,result,event,state)
        by_stage={a['id']:a for s in out['sections'] for a in s.get('artifacts',[])}
        self.assertFalse(by_stage['problem-context'].get('stale',False))
        self.assertTrue(by_stage['ia-map']['stale'])
        self.assertTrue(by_stage['three-concepts']['stale'])
        self.assertTrue(by_stage['recommendation']['stale'])
        self.assertTrue(by_stage['test-plan']['stale'])
        self.assertIn('feedback-event-001',by_stage)

    def test_exported_feedback_matched_to_artifact_version(self):
        report={'project_id':self.project['project_id'],'reviews':{
            'ia-candidates::ia-map':{'status':'needs_revision','artifact_version':1,'note':'Please test the resource entry point.'},
            'mandate::problem-context':{'status':'reviewed','artifact_version':7,'note':'Old review.'}}}
        result=ingest(self.project,report)
        self.assertEqual(result['needs_assessment'],1)
        self.assertEqual(result['items'][0]['origin_stage'],'information_architecture')
        self.assertEqual(result['items'][0]['action'],'assess_possible_invalidation')
        self.assertEqual(result['items'][1]['action'],'verify_on_current_version')

if __name__=='__main__':unittest.main()
