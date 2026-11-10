from pathlib import Path
import json, hashlib, zipfile, statistics

R = Path('C:/Users/A/Documents/DSH-Workspace/pi-single-dual-r89-20261110/r95-four-core/f2')
h = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
f = json.loads((R / 'EXPERIMENT-FREEZE.json').read_text())
sf = json.loads((R / 'run/FREEZE.json').read_text())
a = json.loads((R / 'ANALYSIS.json').read_text())
assert all(h(R / p) == v for p, v in f['snapshot_after'].items())
assert len(a['rows']) == 8
receipts = zipfiles = sample_inputs = 0
cpus, peaks, times = [], [], {}
for row in a['rows']:
    case = R / 'run' / row['case']
    W = case / 'work'
    r = json.loads((case / 'RESULT.json').read_text())
    e = json.loads((W / 'EXECUTION.json').read_text())
    d = json.loads((W / 'DELIVERY.json').read_text())
    assert r['valid'] and not r['failures'] and r['cli_exit_code'] == 0
    assert d['accepted'] == d['requested'] == 128 and d['files'] == 6144
    assert len(e['results']) == 128 and {x['index'] for x in e['results']} == set(range(128))
    lm = e['lane_metrics']
    pin = row['label'] in ['B', 'C']
    assert len(lm) == 4 and all(x['count'] == 32 and x['process_exit_code'] == 0 and x['pin_requested'] == pin for x in lm)
    assert sorted(x['affinity_actual'] for x in lm) == ([[0], [1], [2], [3]] if pin else [[0, 1, 2, 3]] * 4)
    assert len({x['pid'] for x in e['results']}) == 4
    assert all(h(R / p) == v for p, v in row['receipts'].items())
    for i in range(128):
        w = W / ('lane-' + str(i % 4)) / ('job-' + str(i).zfill(2))
        expected = sf['unique_task_input_hashes'][i]
        assert Path(e['results'][i]['cwd']).resolve() == w.resolve()
        rr = json.loads((w / 'delivery.json').read_text())
        assert rr['status'] == 'CONTENT_ACCEPTED' and rr['qa']['pass'] and all(rr['qa']['checks'].values())
        assert all(h(w / n) == v for n, v in rr['sha256'].items())
        assert json.loads((w / 'manifest.json').read_text()) == expected
        with zipfile.ZipFile(w / 'delivery.zip') as z:
            assert len(z.namelist()) == 48 and z.testzip() is None
            assert {n: hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()} == expected
        receipts += 1
        zipfiles += 48
        if i < 4 or i >= 124:
            assert {p.relative_to(w / 'input').as_posix(): h(p) for p in (w / 'input').rglob('*') if p.is_file()} == expected
            sample_inputs += 48
    cpus.append(sum(x['cpu_s'] for x in e['results']) / 4)
    peaks.extend(x['peak_wset_bytes'] for x in lm)
    times.setdefault(row['label'], []).append(row['total_s'])
print(json.dumps(dict(audit='PASS', frozen_source_files=len(f['snapshot_after']), all_job_receipts=receipts, all_zip_members=zipfiles, sampled_raw_inputs=sample_inputs, cpu_work_div4_range_s=[min(cpus), max(cpus)], worker_peak_wset_mib_range=[min(peaks) / 1048576, max(peaks) / 1048576], means={k: statistics.mean(v) for k, v in times.items()}, freeze_sha256=h(R / 'EXPERIMENT-FREEZE.json'))))
