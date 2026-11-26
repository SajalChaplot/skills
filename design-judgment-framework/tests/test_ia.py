import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('ia_engine',ROOT/'scripts/evaluate_ia.py')
ia=importlib.util.module_from_spec(spec);spec.loader.exec_module(ia)

class IAExplorationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case=json.loads((ROOT/'examples/security-alert-ia.json').read_text(encoding='utf-8'))

    def test_security_alert_example_priorities_match_original_decision(self):
        w=ia.resolve(self.case)
        self.assertEqual(w['efficiency'],90)
        self.assertEqual(w['information_density'],80)
        self.assertEqual(w['discoverability'],55)
        self.assertEqual(w['user_control'],95)
        self.assertEqual(w['guidance'],70)
        self.assertEqual(w['flexibility'],70)
        self.assertEqual(w['consistency'],85)
        self.assertEqual(w['simplicity'],80)

    def test_sample_has_four_structurally_distinct_alternatives(self):
        opts=self.case['alternatives']
        self.assertEqual(len(opts),4)
        self.assertEqual(len({o['organizing_principle'] for o in opts}),4)
        for option in opts:
            self.assertEqual(len(option['task_walkthroughs']),len(self.case['task_scenarios']))
            self.assertTrue(option['navigation_tree'])
            self.assertTrue(option['benefits'])
            self.assertTrue(option['failure_modes'])

    def test_sample_provisional_leader(self):
        report=ia.evaluate(self.case)
        self.assertEqual(report['preference_leader'],'alert-centered')
        self.assertTrue(report['requires_independent_ia_validation'])
        self.assertEqual(len(report['ranked_options']),4)
        self.assertEqual(report['evaluation_status'],'illustrative_ia_fit_estimates_not_user_evidence')

    def test_opposing_guidance_only_weights_can_change_leader(self):
        w={k:0 for k in self.case['rubric']['axes']}
        w['guidance']=100
        report=ia.evaluate(self.case,w)
        self.assertEqual(report['preference_leader'],'workflow-centered')

    def test_unknown_axis_rejected(self):
        with self.assertRaises(ValueError): ia.resolve(self.case, {'invented':90})

    def test_missing_fit_axis_rejected(self):
        case=json.loads(json.dumps(self.case))
        del case['alternatives'][0]['fit_scores']['simplicity']
        with self.assertRaises(ValueError):ia.evaluate(case)

    def test_known_hard_constraint_blocks_option(self):
        case=json.loads(json.dumps(self.case))
        case['alternatives'][0]['known_hard_constraint_violations']=['Unauthorized access to restricted data']
        report=ia.evaluate(case)
        self.assertNotEqual(report['preference_leader'],'alert-centered')
        self.assertEqual(report['disqualified_options'][0]['id'],'alert-centered')

    def test_zero_weights_rejected(self):
        w={k:0 for k in self.case['rubric']['axes']}
        with self.assertRaises(ValueError):ia.resolve(self.case,w)

    def test_workflow_requires_ia_before_screen_options(self):
        workflow=json.loads((ROOT/'workflow.json').read_text())
        ids=[s['id'] for s in workflow['stages']]
        self.assertTrue(ids.index('precedents') < ids.index('information_architecture') < ids.index('options'))
        self.assertEqual(len(list((ROOT/'skills').glob('*/SKILL.md'))),10)  # v1.2 adds feedback + workspace service skills

    def test_standalone_viewer_embeds_same_json(self):
        html=(ROOT/'web/ia-explorer.html').read_text()
        start=html.index('<script id="seed" type="application/json">')+len('<script id="seed" type="application/json">')
        end=html.index('</script>',start)
        viewer=json.loads(html[start:end])
        self.assertEqual(viewer['rubric']['weights'], self.case['rubric']['weights'])
        self.assertEqual({x['id'] for x in viewer['alternatives']},{x['id'] for x in self.case['alternatives']})

if __name__ == '__main__':unittest.main()
