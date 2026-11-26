"""Public Douyin share-page workflow; see references/recovery-20261102.md."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
from urllib.parse import urlparse

UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) "
      "AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 "
      "Version/17.0 Mobile/15E148 Safari/604.1")


def command(args, timeout=100):
    result = subprocess.run(args, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8', 'replace')[-1500:])
    return result.stdout


def item_from(data):
    for node in data.get('loaderData', {}).values():
        if isinstance(node, dict):
            items = (node.get('videoInfoRes') or {}).get('item_list', [])
            if items:
                return items[0]
    raise RuntimeError('No public video item; do not bypass login or verification')


def validate(path, expected_duration=0):
    meta = json.loads(command([
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration,size:stream=codec_type,codec_name,width,height',
        '-of', 'json', str(path)]))
    streams = meta.get('streams', [])
    video = next((s for s in streams if s['codec_type'] == 'video'), None)
    duration = float(meta.get('format', {}).get('duration', 0))
    if not video or not video.get('width') or not video.get('height') or duration <= 0:
        raise RuntimeError('Invalid or empty video')
    if expected_duration and abs(duration - expected_duration) > 2:
        raise RuntimeError('Duration does not match source')
    command(['ffmpeg', '-v', 'error', '-xerror', '-i', str(path),
             '-map', '0:v:0', '-map', '0:a?', '-f', 'null', '-'], timeout=180)
    return meta


def main():
    start = time.monotonic()
    parser = argparse.ArgumentParser()
    parser.add_argument('share_text')
    parser.add_argument('--out-dir', required=True)
    args = parser.parse_args()
    for tool in ('curl', 'ffprobe', 'ffmpeg'):
        if not shutil.which(tool):
            raise RuntimeError('Missing existing dependency: ' + tool)
    found = re.search(r'https://[^\s<>]+', args.share_text)
    if not found:
        raise RuntimeError('No HTTPS share URL')
    url = found.group().rstrip('.,;，。；')
    host = urlparse(url).hostname
    if host not in ('v.douyin.com', 'www.douyin.com', 'douyin.com', 'www.iesdouyin.com'):
        raise RuntimeError('Unsupported input host')
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='douyin-public-') as tmp:
        cookie = str(Path(tmp) / 'anonymous-cookies.txt')
        base = ['curl', '-fsSL', '--proto', '=https', '--proto-redir', '=https',
                '--max-time', '25', '-A', UA, '-H', 'Accept-Language: zh-CN,zh;q=0.9',
                '-e', 'https://www.douyin.com/', '-b', cookie, '-c', cookie]
        command(base + ['https://www.iesdouyin.com/'])
        if host == 'v.douyin.com':
            resolved = command(base + ['-o', os.devnull, '-w', '%{url_effective}', url]).decode()
        else:
            resolved = url
        match = re.search(r'/(?:video|note)/(\d{15,25})', resolved)
        if not match:
            raise RuntimeError('Short URL did not resolve to a supported video page')
        vid = match.group(1)
        share_url = 'https://www.iesdouyin.com/share/video/' + vid + '/'
        data = None
        for _ in range(2):
            html = command(base + [share_url]).decode('utf-8')
            match = re.search(r'window\._ROUTER_DATA\s*=\s*(.*?)</script>', html, re.S)
            if match:
                data = json.loads(match.group(1).strip().rstrip(';'))
                break
        if data is None:
            raise RuntimeError('Share page unavailable; stop this route without bypassing challenges')
        item = item_from(data)
        if str(item.get('aweme_id')) != vid or item.get('images'):
            raise RuntimeError('Item mismatch or unsupported image album')
        duration = item.get('video', {}).get('duration', 0) / 1000
        if duration <= 0:
            raise RuntimeError('Missing source duration; cannot certify a complete download')
        target = out / ('douyin_' + vid + '.mp4')
        if target.exists():
            raise RuntimeError('Output exists; preserve it and choose a fresh verification directory')
        urls = item.get('video', {}).get('play_addr', {}).get('url_list', [])
        if not urls:
            raise RuntimeError('No published playback URL')
        media_url = urls[0].replace('/playwm/', '/play/')
        if urlparse(media_url).hostname not in ('aweme.snssdk.com', 'www.iesdouyin.com', 'www.douyin.com'):
            raise RuntimeError('Unexpected playback host')
        partial = target.with_suffix('.part.mp4')
        try:
            command(base[:base.index('--max-time')] + ['--max-time', '90'] +
                    base[base.index('--max-time')+2:] + [media_url, '-o', str(partial)])
            meta = validate(partial, duration)
            if item.get('music', {}).get('duration', 0) and not any(
                    s.get('codec_type') == 'audio' for s in meta.get('streams', [])):
                raise RuntimeError('Source has audio but downloaded file has no audio track')
            partial.rename(target)
        except Exception:
            partial.unlink(missing_ok=True)
            raise
        receipt = {'status': 'PASS', 'source_url': url, 'video_id': vid,
                   'title': item.get('desc'), 'path': str(target),
                   'metadata': meta, 'full_decode': 'PASS',
                   'elapsed_seconds': round(time.monotonic() - start, 3)}
        target.with_suffix('.receipt.json').write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(receipt, ensure_ascii=True))


if __name__ == '__main__':
    main()
