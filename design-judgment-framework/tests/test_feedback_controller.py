import datetime as dt
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from feedback_controller import initial_state, merge_policy, evaluate_event, affected_path

POLICY = json.loads((ROOT/'profiles/iteration-policy.json').read_text())
WORKFLOW = json.loads((ROOT/'workflow.json').read_text())
START = dt.datetime(2026, 11, 26, 9, 0, tzinfo=dt.timezone.utc)


def evt(trigger='contradiction', **kwargs):
    return {'decision_id':'d1','trigger':trigger,'reason':'Specific contradictory artifact finding',
            'invalidates':['information_architecture'], 'risk_level':'low',
            'mandatory_constraint_status':'clear', **kwargs}


class FeedbackTests(unittest.TestCase):
    def setUp(self):
        self.state = initial_state(START)

    def go(self, event, minutes=1, policy=None):
        result, self.state = evaluate_event(policy or POLICY, WORKFLOW, self.state,
                                            event, START + dt.timedelta(minutes=minutes))
        return result

    def test_selective_downstream_not_context(self):
        plan = affected_path(WORKFLOW, ['information_architecture'])
        self.assertEqual(plan, ['information_architecture','options','governance','validation','decision_record'])
        self.assertNotIn('context', plan)

    def test_revisit_with_new_evidence(self):
        output = self.go(evt(new_evidence_ids=['research-1']))
        self.assertEqual(output['action'],'REVISIT')
        self.assertEqual(output['decision_revisions'],1)
        self.assertEqual(self.state['total_revisions'],1)

    def test_no_new_evidence_requires_validation_then_stops(self):
        self.assertEqual(self.go(evt(), minutes=1)['action'],'VALIDATE')
        end = self.go(evt(), minutes=2)
        self.assertEqual(end['action'],'STOP')
        self.assertEqual(end['status'],'provisional')
        self.assertEqual(self.state['total_revisions'],0)

    def test_independent_rubric_can_count_as_change_but_not_validation(self):
        first = self.go(evt(rubric_delta=6, rubric_id='ia-rubric-v1'), minutes=1)
        self.assertEqual(first['action'],'REVISIT')
        self.assertIn('No production',first['authorization'])

    def test_score_delta_without_rubric_rejected(self):
        with self.assertRaises(ValueError): self.go(evt(rubric_delta=8))

    def test_revisions_limited(self):
        for i in range(3):
            out=self.go(evt(new_evidence_ids=[f'obs-{i}']), minutes=i+1)
            self.assertEqual(out['action'],'REVISIT')
        fourth=self.go(evt(new_evidence_ids=['obs-new']), minutes=4)
        self.assertEqual(fourth['action'],'STOP')
        self.assertEqual(fourth['status'],'provisional')

    def test_high_risk_exhaustion_escalates(self):
        short=merge_policy(POLICY, {'revision_limits':{'per_decision':1}})
        self.assertEqual(self.go(evt(new_evidence_ids=['a']), policy=short)['action'],'REVISIT')
        second=self.go(evt(new_evidence_ids=['b'],risk_level='high'), minutes=2, policy=short)
        self.assertEqual(second['action'],'ESCALATE')

    def test_time_budget_is_checked(self):
        result=self.go(evt(new_evidence_ids=['research-1']),minutes=31)
        self.assertEqual(result['action'],'STOP')
        self.assertIn('elapsed time',result['reason'])

    def test_tool_budget_when_usage_reported(self):
        result=self.go(evt(new_evidence_ids=['research-1'],tool_calls_delta=60))
        self.assertEqual(result['action'],'STOP')

    def test_mandatory_violation_and_external_privileged_action(self):
        self.assertEqual(self.go(evt(mandatory_constraint_status='violated'))['action'],'ESCALATE')
        self.assertEqual(self.go(evt(external_action_requested=True),minutes=2)['action'],'ESCALATE')

    def test_manual_reopen_requires_approval(self):
        self.assertEqual(self.go(evt(trigger='explicit_human_reopen'))['action'],'ESCALATE')
        self.assertEqual(self.go(evt(trigger='explicit_human_reopen',human_approved=True),minutes=2)['action'],'REVISIT')

    def test_invalid_stage(self):
        with self.assertRaises(ValueError): self.go(evt(invalidates=['unknown-stage'],new_evidence_ids=['a']))

    def test_safe_policy_override(self):
        changed=merge_policy(POLICY,{'revision_limits':{'per_decision':5}})
        self.assertEqual(changed['revision_limits']['per_decision'],5)
        with self.assertRaises(ValueError): merge_policy(POLICY,{'exhaustion':{'material_risk':'stop_provisional'}})
        with self.assertRaises(ValueError): merge_policy(POLICY,{'arbitrary':{'key':1}})

    def test_complete_remains_non_authorizing(self):
        low=self.go(evt(trigger='complete',approval_gate='low_risk_autonomous_proposal'))
        self.assertEqual(low['action'],'STOP')
        self.assertNotEqual(low['status'],'approved')

    def test_terminal_state_prevents_new_automatic_revisits(self):
        short=merge_policy(POLICY, {'revision_limits':{'per_decision':1}})
        self.assertEqual(self.go(evt(new_evidence_ids=['a']), policy=short)['action'],'REVISIT')
        self.assertEqual(self.go(evt(new_evidence_ids=['b']), minutes=2, policy=short)['action'],'STOP')
        blocked=self.go(evt(new_evidence_ids=['c']), minutes=3, policy=short)
        self.assertEqual(blocked['action'],'STOP')
        self.assertIn('terminal state',blocked['reason'])

    def test_unknown_constraints_escalate_when_finished(self):
        result=self.go(evt(trigger='complete',mandatory_constraint_status='unknown',approval_gate='human_review'))
        self.assertEqual(result['action'],'ESCALATE')

if __name__=='__main__': unittest.main()
