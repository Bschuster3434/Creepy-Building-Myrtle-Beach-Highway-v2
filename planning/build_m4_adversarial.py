"""Build the local before/after review and verify its linked evidence."""
from pathlib import Path
from html import escape
import json, hashlib, re
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'planning/m4-adversarial'
review=ROOT/'planning/m4-review'
views=[('passage-floor','Passage wall and floor joints'),('switch','Rear switch moved beside the door'),('right-wall','Nearly flush masonry infill'),('trees','Fuller canopies and connected utility wires'),('room-trim','Storeroom baseboard contact'),('exterior','Overall exterior and neighboring siding')]
cards=[]
for name,title in views:
    pair=''.join(f'<figure><a href="{phase}-{name}.png"><img src="{phase}-{name}.png" alt="{escape(title)}: {phase}" loading="lazy"></a><figcaption>{phase.title()}</figcaption></figure>' for phase in ['before','after'])
    cards.append(f'<section><h2>{title}</h2><div class="pair">{pair}</div></section>')
asset=json.loads((review/'asset-report.json').read_text())
chrome=json.loads((review/'full-scene-report.json').read_text())
edge=json.loads((review/'edge-report.json').read_text())
contact=json.loads((OUT/'construction-audit.json').read_text())
mesh=json.loads((OUT/'mesh-audit.json').read_text())
assert not contact['failed'] and not mesh['misses'] and not mesh['portalObstructions']
assert all(c['pass'] for r in [chrome,edge] for c in r['checks'])
metrics=f"{asset['triangles']:,} triangles · {asset['glbBytes']/1e6:.2f} MB GLB · {len(contact['checks'])} contact checks · {mesh['wallFloorAndBackingRays']:,} saved-mesh probes"
OUT.joinpath('index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Old store / Adversarial review</title><style>
*{box-sizing:border-box}body{margin:0;background:#efede3;color:#303a30;font:16px/1.6 system-ui}main{max-width:1500px;margin:auto;padding:36px}h1{font:52px Georgia}h2{margin-top:40px}a{color:#465f39}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;background:white}img{display:block;width:100%}figcaption{padding:12px}.metrics{background:#dae0d0;padding:18px}@media(max-width:750px){.pair{grid-template-columns:1fr}h1{font-size:36px}}
</style><main><h1>Adversarial review · September 5</h1><p>Corrections to wall joints, mounted details and canopy density. The approved layout and atmosphere remain the basis.</p><p><a href="http://127.0.0.1:5173/">Open the updated walkthrough</a> · <a href="../m4-review.md">Verification and provenance</a> · <a href="../m4-review/index.html">Full scene review</a></p><p class="metrics">'''+metrics+'''</p><p>The pass also corrected crate stacking, hand-truck floor contact and collision bounds, wall-mounted vents and tally board, pipe straps, pendant conduit contact, utility-wire supports and neighboring siding. Right-wall rectangles remain subtle seams for inferred filled openings.</p>'''+''.join(cards)+f'''<h2>Validation</h2><p>Production build, nine Node tests, 27 interaction checks and 13 full-scene checks in each browser pass. Entrance geometry passes 320 sampled poses and 108 glazing-grid checks. Geometry probes and selected views cannot prove that every surface is defect-free.</p><p>At 1080p with an isolated rendering scene, Chrome/Edge p95 frame intervals are {chrome['performance']['p95Ms']:.1f}/{edge['performance']['p95Ms']:.1f} ms. Cache-disabled loading at 25 Mbps is {chrome['conditions']['navigationReadyMs']/1000:.2f}/{edge['conditions']['navigationReadyMs']/1000:.2f} seconds. The five-second cold-load target remains provisional; see the detailed review for the measured tradeoff.</p><p><a href="construction-audit.json">Construction contacts</a> · <a href="mesh-audit.json">Saved geometry audit</a> · <a href="../m4-review/full-scene-report.json">Chrome route</a> · <a href="../m4-review/edge-report.json">Edge route</a></p></main></html>''',encoding='utf-8')
missing=[]
for gallery in [OUT/'index.html',review/'index.html']:
    for src in re.findall(r'<img[^>]+src="([^"]+)"',gallery.read_text(encoding='utf-8')):
        if not (gallery.parent/unquote(src)).exists():missing.append(src)
assert not missing,missing
files=['model/myrtle-beach-v2-complete.blend','app/public/assets/complete.glb','app/public/assets/complete.json','model/build_full.py','model/full_scene_finish.py','model/audit_full.py']
summary={'milestone':'M4','revision':'adversarial review, September 5','nodeTestsPassed':9,'browserChecks':{name:len(json.loads((review/(name+'.json')).read_text())['checks']) for name in ['browser-report','full-scene-report','edge-report']},'constructionContactChecks':len(contact['checks']),'savedMeshProbes':mesh['wallFloorAndBackingRays'],'missingImages':missing,'hashes':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}}
(review/'verification-summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
