import sys,os,json,time,pathlib,ctypes,datetime
from fast_resolver import resolve_a,extract_url,aweme_id,ResolutionError
from browser_fallback import resolve_b
from downloader import download
def now():return datetime.datetime.now().astimezone().isoformat()
def clipboard():
 u=ctypes.WinDLL('user32',use_last_error=True);k=ctypes.WinDLL('kernel32',use_last_error=True)
 u.GetClipboardData.restype=ctypes.c_void_p;k.GlobalLock.argtypes=[ctypes.c_void_p];k.GlobalLock.restype=ctypes.c_void_p;k.GlobalUnlock.argtypes=[ctypes.c_void_p]
 if not u.OpenClipboard(None):raise RuntimeError('CLIPBOARD_OPEN_FAILED')
 try:
  handle=u.GetClipboardData(13)
  if not handle:raise RuntimeError('CLIPBOARD_UNICODE_TEXT_MISSING')
  ptr=k.GlobalLock(handle)
  if not ptr:raise RuntimeError('CLIPBOARD_LOCK_FAILED')
  try:return ctypes.wstring_at(ptr)
  finally:k.GlobalUnlock(handle)
 finally:u.CloseClipboard()
def desktop():
 buf=ctypes.create_unicode_buffer(32768)
 if ctypes.windll.shell32.SHGetFolderPathW(None,0x10,None,0,buf)!=0:raise RuntimeError('DESKTOP_PATH_FAILED')
 return pathlib.Path(buf.value)
def resolve(text,log,expected=None,bridge=None):
 tick=time.perf_counter_ns();ident=expected or aweme_id(extract_url(text))
 def observe(e):
  nonlocal ident
  if e.get('event')=='share_redirect':ident=ident or aweme_id(e['final_url'])
  log(e)
 try:result=resolve_a(text,observe,expected)
 except Exception as exc:
  log({'event':'A_FAILED','error_type':type(exc).__name__,'error':str(exc)})
  if os.environ.get('DOUYIN_NO_BROWSER_FALLBACK')=='1':raise ResolutionError('SSR_UNAVAILABLE_BROWSER_LAUNCH_DISABLED') from exc
  if not ident:raise ResolutionError('FALLBACK_B_AWEME_ID_UNAVAILABLE') from exc
  log({'event':'AUTO_FALLBACK','route':'B_PLAYWRIGHT_BROWSER_MEDIA','aweme_id':ident})
  result=resolve_b(ident,log,bridge)
 result['T_RESOLVE_MS']=(time.perf_counter_ns()-tick)/1e6
 return result
def main():
 tick=time.perf_counter_ns()
 evidence=pathlib.Path(os.environ.get('DOUYIN_RUN_DIR',str(pathlib.Path(__file__).resolve().parents[1]/'evidence'/datetime.datetime.now().strftime('run-%Y%m%d-%H%M%S-%f'))))
 evidence.mkdir(parents=True,exist_ok=False)
 stream=(evidence/'events.jsonl').open('x',encoding='utf-8')
 def log(e):
  e={'at':now(),'tick_ns':time.perf_counter_ns(),**e}
  stream.write(json.dumps(e,ensure_ascii=False)+'\n');stream.flush()
 try:
  log({'event':'PRODUCT_START','argv':sys.argv,'product_ui':'NONE'})
  text=os.environ.get('DOUYIN_SHARE_URL') or clipboard();log({'event':'clipboard_read','CLIPBOARD_READ':'PASS'})
  url=extract_url(text);log({'event':'url_extract','URL_EXTRACT':'PASS','url':url})
  print('正在解析并下载到桌面...',flush=True)
  media=resolve(url,log)
  target=desktop()/('douyin_'+media['aweme_id']+'.mp4')
  result=download(media,target,log)
  # The final_verifier event timestamp is the product validity endpoint.
  result.update(ROUTE_USED=media['route'],T_RESOLVE_MS=media['T_RESOLVE_MS'],T_FULL_DOWNLOAD_MS=(time.perf_counter_ns()-tick)/1e6,DESKTOP_OUTPUT='YES')
  log({'event':'PRODUCT_RESULT',**result})
  print('下载完成：'+str(target),flush=True);return 0
 except Exception as exc:
  log({'event':'PRODUCT_RESULT','DOWNLOAD_PASS':'NO','REALITY_DELTA':str(exc)})
  print('下载失败：'+str(exc),flush=True);return 1
 finally:stream.close()
if __name__=='__main__':sys.exit(main())
