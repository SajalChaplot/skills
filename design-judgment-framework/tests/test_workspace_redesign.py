import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent


def luminance(hexcolor):
    rgb=[int(hexcolor[i:i+2],16)/255 for i in (1,3,5)]
    rgb=[c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4 for c in rgb]
    return .2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2]


def contrast(a,b):
    x,y=sorted([luminance(a),luminance(b)],reverse=True)
    return (x+.05)/(y+.05)


class RedesignedWorkspaceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template=(ROOT/'web/workspace-template.html').read_text()

    def test_control_text_contrast_above_aa(self):
        # Reviewer select menu uses explicit, non-inherited high-contrast colors.
        self.assertIn('color-scheme:light',self.template)
        self.assertIn('select option{background:#fff!important;color:#162a34!important}',self.template)
        self.assertGreater(contrast('#162a34','#ffffff'),4.5)
        self.assertGreater(contrast('#495963','#ffffff'),4.5)
        self.assertGreater(contrast('#165a52','#ffffff'),4.5)

    def test_zoomable_modal_and_visual_types(self):
        for clause in ('<dialog id="visualDialog"','aria-labelledby="visualTitle"',
                       'aria-describedby="visualDescription"','id="zoomIn"','id="zoomOut"',
                       'id="zoomFit"','style.zoom=String(zoom)',"type==='image'",
                       "type==='ia'","type==='wireframes'","type==='steps'",'View larger'):
            self.assertIn(clause,self.template)
        self.assertIn('e.key===\'Escape\'',self.template)

    def test_project_defined_tabs_and_inline_reviews(self):
        self.assertIn('project.sections.forEach',self.template)
        self.assertIn('function renderArtifactReview',self.template)
        self.assertIn('function renderNav',self.template)
        project=json.loads((ROOT/'projects/workspace-redesign-review.json').read_text())
        self.assertEqual([s['title'] for s in project['sections']],
                         ['Reviewer goals & constraints','Layout explorations','Visual QA & screenshots','Interaction checks'])
        blocks=[b for section in project['sections'] for a in section['artifacts'] for b in a['blocks']]
        self.assertGreaterEqual(sum(b['type']=='image' for b in blocks),2)

    def test_mobile_keeps_policy_import_export(self):
        for id in ('mobileMore','mobilePolicyBtn','mobileImportBtn','mobileProjectBtn','menuBtn'):
            self.assertIn(f'id="{id}"',self.template)
        self.assertIn('openPolicy',self.template)
        self.assertIn('review-status',self.template.replace('Review status','review-status'))

if __name__=='__main__':
    unittest.main()
