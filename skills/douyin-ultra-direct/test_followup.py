import io,json,pathlib,tempfile,unittest,urllib.error,os,sys,types,importlib.util
from unittest.mock import patch
import run

def error(status,code=None):
    return urllib.error.HTTPError('https://demo.douyin.wtf/api/v1/parse',status,'test',{},io.BytesIO(json.dumps({'error':{'code':code,'retry_after':159}}).encode()))

class FollowupTests(unittest.TestCase):
    def test_healthy_route_has_no_wait(self):
        with patch.object(run,'json_request',return_value=(200,{})) as req,patch.object(run.time,'sleep') as sleep:
            self.assertEqual(run.parse_request(None,{},{}),(200,{}))
            req.assert_called_once();sleep.assert_not_called()

    def test_502_retries_once_and_recovers(self):
        state={}
        with patch.object(run,'json_request',side_effect=[error(502),(200,{})]) as req,patch.object(run.time,'sleep') as sleep:
            self.assertEqual(run.parse_request(None,{},state),(200,{}))
            self.assertEqual(req.call_count,2);sleep.assert_called_once_with(1)
            self.assertEqual(state['parse_retry_count'],1)

    def test_repeated_502_stops(self):
        with patch.object(run,'json_request',side_effect=[error(502),error(502)]) as req,patch.object(run.time,'sleep'):
            with self.assertRaises(urllib.error.HTTPError):run.parse_request(None,{},{})
            self.assertEqual(req.call_count,2)

    def test_circuit_open_is_not_hammered(self):
        state={}
        with patch.object(run,'json_request',side_effect=error(503,'ENDPOINT_CIRCUIT_OPEN')) as req,patch.object(run.time,'sleep') as sleep:
            with self.assertRaises(urllib.error.HTTPError):run.parse_request(None,{},state)
            req.assert_called_once();sleep.assert_not_called()
            self.assertEqual(state['api_failure']['retry_after'],159)

    def test_each_run_is_retained(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d)
            with patch.object(run,'ROOT',root),patch.object(run,'LAST',root/'last_run.json'):
                run.save_report({'status':'FAIL'});run.save_report({'status':'PASS'})
                self.assertEqual(len(list((root/'history').glob('*.json'))),2)
                self.assertEqual(json.loads((root/'last_run.json').read_text())['status'],'PASS')

    def test_fallback_keeps_explicit_input_and_verifies_file(self):
        with tempfile.TemporaryDirectory() as d:
            file=pathlib.Path(d)/'video.mp4';file.write_bytes(b'x')
            result=types.SimpleNamespace(returncode=0,stdout='下载完成：'+str(file))
            state={'share_url':'https://v.douyin.com/example/'}
            with patch.object(run,'FALLBACK',file),patch.object(run.subprocess,'run',return_value=result) as child,patch.object(run,'ffprobe',return_value={'video':'h264'}):
                run.fallback_existing(state)
                self.assertEqual(child.call_args.kwargs['env']['DOUYIN_SHARE_URL'],state['share_url'])
                self.assertEqual(child.call_args.kwargs['env']['DOUYIN_NO_BROWSER_FALLBACK'],'1')
                self.assertEqual(state['output'],str(file))

    def test_legacy_fallback_does_not_launch_browser(self):
        from unittest.mock import Mock
        fast=types.ModuleType('fast_resolver')
        fast.resolve_a=Mock(side_effect=RuntimeError('SSR unavailable'))
        fast.extract_url=lambda value:value;fast.aweme_id=lambda value:'7669298890101094769';fast.ResolutionError=RuntimeError
        browser=types.ModuleType('browser_fallback');browser.resolve_b=Mock()
        downloader=types.ModuleType('downloader');downloader.download=Mock()
        with patch.dict(sys.modules,{'fast_resolver':fast,'browser_fallback':browser,'downloader':downloader}),patch.dict(os.environ,{'DOUYIN_NO_BROWSER_FALLBACK':'1'}):
            spec=importlib.util.spec_from_file_location('legacy_test',pathlib.Path(__file__).with_name('legacy_direct_save.py'))
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            with self.assertRaisesRegex(RuntimeError,'BROWSER_LAUNCH_DISABLED'):module.resolve('https://v.douyin.com/test/',lambda e:None)
            browser.resolve_b.assert_not_called()

if __name__=='__main__':unittest.main()
