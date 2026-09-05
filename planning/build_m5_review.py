"""Assemble M5 local review from completed browser reports and geometry audits."""
from pathlib import Path
from datetime import datetime, timezone
from html import escape
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'planning/m5-review'

def read(name):
    return json.loads((OUT / name).read_text(encoding='utf-8'))

reports = {name: read(name + '-report.json') for name in ['interaction', 'mode', 'route']}
control_review = read('controls-review-report.json')
assert set(control_review) == {'chrome', 'edge'} and all(r['pass'] for r in control_review.values())
assert all(r.get('pass') for suite in reports.values() for r in suite.values())
assert all(set(suite) == {'chrome', 'edge'} for suite in reports.values())
assets = read('asset-report.json')
for source, target in [('planning/m4-review/window-clearance.json', 'window-clearance.json'),
                       ('planning/m4-adversarial/mesh-audit.json', 'mesh-audit.json'),
                       ('planning/m4-adversarial/construction-audit.json', 'construction-audit.json')]:
    path = ROOT / source
    if path.exists():
        (OUT / target).write_bytes(path.read_bytes())

paths = ['model/myrtle-beach-v2-complete.blend', 'model/build_full.py', 'model/walkthrough_data.py',
         'model/build_sample.py', 'model/full_scene_finish.py', 'model/myrtle-beach-v2-blockout.blend',
         'app/public/assets/complete.glb', 'app/public/assets/complete.json',
         'app/src/world.js', 'app/src/physics.js', 'app/src/main.jsx', 'app/src/style.css',
         'app/package.json', 'app/package-lock.json', 'app/README.md',
         'app/tests/physics.test.js', 'app/tests/full-scene.test.js', 'app/tests/interactions.test.js',
         'README.md', 'planning/m5-review.md', 'planning/build_m5_review.py']
paths += [str(p.relative_to(ROOT)).replace('\\', '/') for p in OUT.glob('*-check.js')]
paths += [str(p.relative_to(ROOT)).replace('\\', '/') for p in OUT.glob('*-report.json')]
paths += [str(p.relative_to(ROOT)).replace('\\', '/') for p in (ROOT / 'app/dist/assets').glob('*.js')]
hashes = {p: {'bytes': (ROOT / p).stat().st_size, 'sha256': hashlib.sha256((ROOT / p).read_bytes()).hexdigest()} for p in paths}
summary = {'generatedAt': datetime.now(timezone.utc).isoformat(), 'milestone': 'M5',
           'status': 'Done', 'reviewPending': False, 'acceptedBy': 'Brian', 'acceptedDate': '2026-09-05',
           'controlReviewChecks': {browser: len(r['checks']) for browser, r in control_review.items()},
           'baselineEvidence': 'The three original suites describe the initial implementation before Brian requested control refinements.',
           'nodeTests': 16, 'browserChecks': {browser: {suite: len(data[browser]['checks']) for suite, data in reports.items()} for browser in ['chrome', 'edge']},
           'assets': assets, 'artifacts': hashes,
           'scope': 'Local production verification. M6 owns repository release, separate Vercel project and deployed checks.'}
(OUT / 'verification-summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')

rows = []
for browser in ['chrome', 'edge']:
    r = reports['route'][browser]
    rows.append(f'<tr><th>{browser.title()}</th><td>{r["cold"]["navigationReadyMs"]/1000:.2f} s</td><td>{r["cold"]["transferBytes"]/1e6:.2f} MB</td><td>{r["performance"]["p95Ms"]:.1f} ms</td><td>{sum(len(s[browser]["checks"]) for s in reports.values())} passed</td></tr>')
gallery = []
for name, label in [('orbit', 'Orbit inspection'), ('top-down', 'Top-down site view'),
                    ('crates', 'Crate storeroom'), ('packing', 'Packing room'),
                    ('rear-door', 'Operating rear door'), ('sales', 'Sales room'),
                    ('light', 'Sales room switch'), ('cratesLight', 'Crate room switch'),
                    ('packingLight', 'Packing room switch'), ('passage', 'Passage switch')]:
    file = f'chrome-{name}.png'
    assert (OUT / file).exists(), file
    gallery.append(f'<figure><a href="{file}"><img loading="lazy" src="{file}" alt="{escape(label)}"></a><figcaption>{escape(label)}</figcaption></figure>')

html = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>M5 — The old store</title><style>
body{font:16px/1.6 system-ui,sans-serif;background:#202820;color:#e9e6d8;margin:0;padding:40px;max-width:1400px;margin:auto}h1{font:48px Georgia,serif}a{color:#eeddaa}p{max-width:950px}table{border-collapse:collapse;width:100%;margin:28px 0}th,td{text-align:left;padding:12px;border-bottom:1px solid #65705e}.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:20px}figure{margin:0}img{width:100%;display:block}figcaption{padding:10px 0}code{background:#364131;padding:2px 5px}nav{display:flex;gap:18px;flex-wrap:wrap}
</style><h1>The old store — M5 accepted</h1>
<p><strong>Done: Brian accepted M5 on September 5, 2026.</strong> The revised controls activate orbit immediately with 2 (no-click horizontal trackpad orbit, vertical scroll zoom, A/D or Left/Right orbit, W/S or Up/Down zoom; reversed horizontal direction) and first-person mouse-look immediately with 1. <a href="controls-review-report.json">82 current control revision checks</a> pass in each of Chrome and Edge. The measurements and scene captures below are retained initial-implementation evidence. Public deployment remains M6.</p>
<p>Independent doors and four light circuits, the approved tilting window, and walking, orbit and top-down views. Desktop mouse and keyboard controls preserve the walking position across inspection modes.</p>
<nav><a href="http://127.0.0.1:5173/">Open local walkthrough</a><a href="../m5-review.md">Review and handoff</a><a href="../../app/README.md">Setup and controls</a><a href="verification-summary.json">Artifact hashes</a></nav>
<table><thead><tr><th>Browser</th><th>Cold ready</th><th>Transfer</th><th>Walking p95</th><th>Browser checks</th></tr></thead><tbody>''' + ''.join(rows) + '''</tbody></table>
<p>Production preview, 1920 × 1080 at DPR 1, 25 Mbps down / 5 Mbps up / 40 ms latency, cache disabled. Each browser runs alone; all four light circuits are on during the continuous walking route. Accepted p95 ≤20 ms, transfer ≤15 MB and approximately 5.5 s readiness.</p>
<p>16 Node tests pass. Geometry retains 320 clear window/door poses, 108 glazing-grid checks and 2,444 saved-mesh probes. Source geometry: 298,883 triangles; conservative texture memory: 33.33 MiB. Sampling verifies the recorded scenarios, not every possible user path or device.</p>
<nav><a href="interaction-report.json">Interactions</a><a href="mode-report.json">Camera and input</a><a href="route-report.json">Continuous route and performance</a><a href="asset-report.json">Assets</a><a href="window-clearance.json">Window geometry</a><a href="mesh-audit.json">Saved mesh audit</a></nav>
<p>M6 remains the public release milestone: audit and commit the release state, create the separate V2 Vercel project, then verify the deployed URL. These results describe the local build.</p>
<div class="gallery">''' + ''.join(gallery) + '</div></html>'
(OUT / 'index.html').write_text(html, encoding='utf-8')
print(json.dumps({'review': str(OUT / 'index.html'), 'browserChecks': summary['browserChecks'], 'hashedArtifacts': len(hashes)}))
