import io
import json
import unittest
import urllib.error
from unittest.mock import patch
import run

SHARE = 'https://v.douyin.com/x2jZ6T5FqOQ/'
MEDIA = 'https://v6-kefu.douyinvod.com/example.mp4'

class Response:
    url = 'https://www.iesdouyin.com/share/video/7669298890101094769/'
    def __enter__(self): return self
    def __exit__(self, *args): pass

class RepairTests(unittest.TestCase):
    def test_share_text_is_extracted(self):
        self.assertEqual(run.extract_url('4.61 分享视频 ' + SHARE + ' 复制链接'), SHARE)

    def test_healthy_api_never_starts_browser(self):
        with patch.object(run, 'parse_share_api', return_value={'ok': True}), patch.object(run.subprocess, 'run') as child:
            self.assertEqual(run.parse_share(SHARE, {}), {'ok': True})
            child.assert_not_called()

    def test_502_uses_explicit_link_and_resolved_id(self):
        result = type('Result', (), {'returncode': 0, 'stdout': json.dumps({'url': MEDIA, 'title': 'test', 'elapsed_ms': 2})})()
        state = {}
        with patch.object(run, 'parse_share_api', side_effect=urllib.error.HTTPError(SHARE,502,'Bad Gateway',{},None)), patch.object(run.subprocess, 'run', return_value=result) as child, patch.object(run.urllib.request,'urlopen',return_value=Response()):
            value = run.parse_share(SHARE, state)
            self.assertEqual(value['content_id'], '7669298890101094769')
            self.assertEqual(child.call_args.args[0][-1], SHARE)
            self.assertEqual(state['route'], 'SEEKIN_EXISTING_BROWSER')

    def test_failed_alternative_cannot_report_success(self):
        result = type('Result', (), {'returncode': 1, 'stderr': 'CDP unavailable'})()
        with patch.object(run, 'parse_share_api',side_effect=RuntimeError('503')), patch.object(run.subprocess,'run',return_value=result):
            with self.assertRaisesRegex(RuntimeError,'API_AND_SEEKIN_FAILED'):
                run.parse_share(SHARE,{})

    def test_unknown_content_id_rejected(self):
        result = type('Result', (), {'returncode':0,'stdout':json.dumps({'url':MEDIA})})()
        response = Response(); response.url = 'https://www.douyin.com/'
        with patch.object(run,'parse_share_api',side_effect=RuntimeError('503')), patch.object(run.subprocess,'run',return_value=result), patch.object(run.urllib.request,'urlopen',return_value=response):
            with self.assertRaisesRegex(RuntimeError,'CONTENT_ID_UNRESOLVED'):
                run.parse_share(SHARE,{})

if __name__ == '__main__': unittest.main()
