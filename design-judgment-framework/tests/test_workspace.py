import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'scripts'))
from workspace import validate_project,build,record


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.security=json.loads((ROOT/'projects/security-alert-review.json').read_text())
        self.dev=json.loads((ROOT/'projects/developer-setup-review.json').read_text())
    def tearDown(self):self.tmp.cleanup()

    def project(self,content):
        path=self.root/'project.json'
        path.write_text(json.dumps(content))
        return path

    def test_dynamic_sections_not_fixed(self):
        self.assertEqual(len(self.security['sections']),8)
        self.assertEqual(len(self.dev['sections']),3)
        security=build(self.project(self.security),self.root/'out.html',ROOT/'web/workspace-template.html')
        html=security.read_text()
        self.assertIn('Navigation explorations',html)
        self.assertIn('Feedback & iteration',html)
        self.assertNotIn('__PROJECT_DATA__',html)
        dev_html=build(self.project(self.dev),self.root/'out2.html',ROOT/'web/workspace-template.html').read_text()
        self.assertIn('Setup friction',dev_html)
        self.assertNotIn('Navigation explorations',dev_html)

    def test_new_section_and_artifact(self):
        src=self.project(self.dev)
        event={'section_id':'unplanned-research','section_title':'Unplanned research','section_group':'Discover',
               'artifact':{'id':'task-study','title':'Task study','blocks':[{'type':'text','text':'Findings TBD'}]}}
        event_path=self.root/'event.json';event_path.write_text(json.dumps(event))
        first=record(src,event_path)
        self.assertEqual(first['sections'][-1]['title'],'Unplanned research')
        second=record(src,event_path)
        self.assertEqual(second['sections'][-1]['artifacts'][0]['version'],2)
        self.assertEqual(second['version'],3)
        self.assertEqual(len(second['sections']),4)

    def test_duplicate_section_rejected(self):
        bad=copy.deepcopy(self.dev);bad['sections'].append(copy.deepcopy(bad['sections'][0]))
        with self.assertRaises(ValueError):validate_project(bad)

    def test_html_payload_does_not_break_script(self):
        obj=copy.deepcopy(self.dev)
        obj['sections'][0]['artifacts'][0]['blocks'][0]['text']='</script><script>alert(123)</script>'
        html=build(self.project(obj),self.root/'out.html',ROOT/'web/workspace-template.html').read_text()
        self.assertNotIn('</script><script>alert(123)',html)
        self.assertIn('\\u003c/script>',html)

    def test_image_path_cannot_escape_project_dir(self):
        obj=copy.deepcopy(self.dev)
        obj['sections'][0]['artifacts'][0]['blocks'].append({'type':'image','local_path':'../secrets.png'})
        with self.assertRaises(ValueError):build(self.project(obj),self.root/'out.html',ROOT/'web/workspace-template.html')

    def test_image_embedding(self):
        from base64 import b64decode
        # Single pixel PNG used solely for file-embedding verification.
        (self.root/'pixel.png').write_bytes(b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+WlSwAAAAASUVORK5CYII='))
        obj=copy.deepcopy(self.dev)
        obj['sections'][0]['artifacts'][0]['blocks'].append({'type':'image','local_path':'pixel.png','alt':'test'})
        html=build(self.project(obj),self.root/'out.html',ROOT/'web/workspace-template.html').read_text()
        self.assertIn('data:image/png;base64,',html)

if __name__=='__main__':unittest.main()
