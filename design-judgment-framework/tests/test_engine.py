import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('design_engine',ROOT/'scripts/evaluate.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config=json.loads((ROOT/'profiles/preferences.json').read_text())
        cls.case=json.loads((ROOT/'examples/developer-project-setup.json').read_text())

    def test_task_override(self):
        weights,initiative,task=module.resolve_preferences(self.config, 'project-setup')
        self.assertEqual(weights['efficiency'],90)
        self.assertEqual(weights['recoverability'],85)
        self.assertEqual(initiative,30)
        self.assertIsNotNone(task)

    def test_default_rank_and_gate(self):
        report=module.evaluate(self.config,self.case)
        self.assertEqual(report['preferred_option'],'progressive')
        self.assertEqual(report['gate'],'prototype_and_validate')
        self.assertEqual(len(report['ranked_options']),3)

    def test_known_violation_blocks_even_with_confidence(self):
        a={**self.case['assessment'],'hard_constraint_violations':['privacy'] , 'evidence_confidence':1,'risk':0}
        self.assertEqual(module.autonomy_gate(a,100)[0],'blocked')

    def test_unknown_constraint_human_review(self):
        a={**self.case['assessment'],'unknown_constraints':['accessibility status unknown']}
        self.assertEqual(module.autonomy_gate(a,100)[0],'human_review')

    def test_requires_external_action_approval(self):
        a={**self.case['assessment'],'action_requires_approval':True,'evidence_confidence':1,'risk':0}
        self.assertEqual(module.autonomy_gate(a,100)[0],'human_approval_required')

    def test_high_risk_always_requires_approval(self):
        a={**self.case['assessment'],'risk':.85,'evidence_confidence':1}
        self.assertEqual(module.autonomy_gate(a,100)[0],'human_approval_required')

    def test_low_confidence_risk_requires_research(self):
        a={**self.case['assessment'],'risk':.48,'evidence_confidence':.20}
        self.assertEqual(module.autonomy_gate(a,0)[0],'research_required')

    def test_winner_can_change_with_preferences(self):
        w={k:0 for k in module.AXES};w['transparency']=100;w['flexibility']=100;w['discoverability']=100
        ranking,_=module.ordered_options(self.case,w)
        self.assertEqual(ranking[0]['id'],'all-upfront')

    def test_zero_weights_rejected(self):
        c=json.loads(json.dumps(self.config))
        c['organization']['priority_weights']={k:0 for k in module.AXES}
        c['tasks']=[]
        with self.assertRaises(ValueError):module.resolve_preferences(c,'missing')

    def test_missing_fit_rejected(self):
        option={'id':'test','fit_scores':{'efficiency':3}}
        with self.assertRaises(ValueError):module.option_score(option,{k:1 for k in module.AXES})

if __name__=='__main__': unittest.main()
