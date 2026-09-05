"""Build a local reference board and schematic from unchanged research sources."""
from pathlib import Path
import csv
import html
import json
import math

ROOT = Path(__file__).resolve().parent
rows = list(csv.DictReader((ROOT / 'source-inventory.csv').open(encoding='utf-8-sig')))
for row in rows:
    group = row['RelativePath'].split('\\')[0]
    row['Classification'] = {'google_maps_images': 'Photographic screenshot; see dossier for acquisition date', 'exterior_generated': 'Generated exterior concept; not evidence', 'interior_generated': 'Generated interior concept; not evidence', 'Doors and Windows': 'Detail/product or unverified reference; not building evidence'}[group]
with (ROOT / 'source-inventory.csv').open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

footprints = json.loads((ROOT / 'sources/footprints.json').read_text())['data']['features']
addresses = json.loads((ROOT / 'sources/addresses.json').read_text())['data']['features']
parcels = json.loads((ROOT / 'sources/parcels.json').read_text())['data']['features']
target = next(f for f in footprints if f['attributes']['OBJECTID'] == 100281)
ring = target['geometry']['rings'][0]
cx = sum(p[0] for p in ring[:-1]) / 4
cy = sum(p[1] for p in ring[:-1]) / 4
def metric(p):
    return ((p[0]-cx)*111320*math.cos(math.radians(cy)), (p[1]-cy)*111320)
def canvas(p):
    x,y = metric(p)
    return 660+x*4.5, 460-y*4.5
def points(r):
    return ' '.join(f'{x:.2f},{y:.2f}' for x,y in map(canvas,r))
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 760" role="img" aria-label="County GIS footprint and parcel context, north up">', '<rect width="1100" height="760" fill="#f3f5ee"/>', '<defs><clipPath id="map"><rect x="15" y="80" width="1070" height="580"/></clipPath></defs>', '<g clip-path="url(#map)">']
for f in parcels:
    for r in f['geometry']['rings']:
        svg.append(f'<polygon points="{points(r)}" fill="none" stroke="#b89d75" stroke-width="1.5"/>')
for f in footprints:
    color = '#d45331' if f['attributes']['OBJECTID']==100281 else '#93a09f'
    for r in f['geometry']['rings']:
        svg.append(f'<polygon points="{points(r)}" fill="{color}" stroke="#263e42"/>')
for a in addresses:
    x,y = canvas([a['geometry']['x'], a['geometry']['y']])
    label = '4397 target (county: E; Brian: W)' if a['attributes']['ADDRESS'].startswith('4397') else a['attributes']['ADDRESS']
    svg.append(f'<circle cx="{x}" cy="{y}" r="3" fill="#152f35"/><text x="{x+8}" y="{y-8}" font-size="13" font-family="sans-serif">{html.escape(label)}</text>')
svg += ['</g>', '<text x="30" y="34" font-size="23" font-family="sans-serif" fill="#152f35">4397 Hwy 9 W — mapped site context</text>', '<text x="30" y="59" font-size="14" font-family="sans-serif">Horry County GIS • accessed 2026-09-04 • target footprint SOURCE=1998</text>', '<path d="M1030 150V105m-7 12 7-12 7 12" fill="none" stroke="#152f35" stroke-width="3"/><text x="1024" y="94" font-family="sans-serif">N</text>', '<path d="M40 695H130M40 689V701M130 689V701" stroke="#152f35" stroke-width="3"/><text x="40" y="720" font-size="14" font-family="sans-serif">20 m approximate</text>', '<text x="260" y="695" font-size="14" font-family="sans-serif">Orange: target footprint • Gray: other footprints • Tan: parcel boundaries</text>', '<text x="260" y="720" font-size="14" font-family="sans-serif">Schematic from GIS geometry; not a survey. Road surface is shown in the aerial reference.</text>', '</svg>']
(ROOT / 'site-context.svg').write_text('\n'.join(svg), encoding='utf-8')
refs = json.loads((ROOT / 'reference-annotations.json').read_text(encoding='utf-8'))
cards = []
for ident, filename, date, view, annotation in refs:
    src = 'references/google_maps_images/' + filename
    cards.append(f'<figure data-date="{"dated" if date.startswith("Nov") else "undated"}"><a href="{html.escape(src, quote=True)}"><img loading="lazy" src="{html.escape(src, quote=True)}" alt="{html.escape(view)}"></a><figcaption><h2>{ident} · {view}</h2><p class="date">{html.escape(date)}</p><p>{html.escape(annotation)}</p><small>{html.escape(filename)} · Google imagery; screenshot filename dated Jan 2, 2026</small></figcaption></figure>')
page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>4397 Hwy 9 W — M1 reference board</title><style>
*{box-sizing:border-box}body{margin:0;background:#edf0eb;color:#183437;font:16px/1.6 system-ui,sans-serif}header,main{max-width:1320px;margin:auto;padding:30px}header{padding-top:50px}h1{font-size:42px;line-height:1.1;margin:10px 0}h2{font-size:20px;margin:0}p{max-width:950px}.eyebrow,.date{color:#546766;font-size:13px;font-weight:600}a{color:#075d67}nav{display:flex;gap:12px;flex-wrap:wrap}button{padding:10px 18px;border:1px solid #809a96;border-radius:6px;background:white;cursor:pointer}button[aria-pressed=true]{background:#183437;color:white}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}figure{margin:0;background:white;border-radius:10px;overflow:hidden;box-shadow:0 2px 5px #18343715}img{display:block;width:100%;height:auto}figcaption{padding:22px}small{color:#627574;overflow-wrap:anywhere}.wide{grid-column:1/-1}.wide img{max-height:760px;object-fit:contain}.notice{border-left:4px solid #d45331;padding:8px 18px;background:white}.hidden{display:none}@media(max-width:750px){.grid{grid-template-columns:1fr}h1{font-size:30px}main,header{padding:20px}}@media print{nav{display:none}figure{break-inside:avoid}.grid{display:block}figure{margin-bottom:20px}}</style>
<header><div class="eyebrow">M1 / RESEARCH DOSSIER / SEPTEMBER 4, 2026</div><h1>4397 Hwy 9 W</h1><p>Loris area, South Carolina · 34.007932, -78.764340<br>Location and project address confirmed by Brian. County GIS labels the address “4397 HWY 9 E.”</p><p><a href="https://app.notion.com/p/3d1488886d5781839b10f5576dfe98e5">Open the authoritative Notion dossier</a> · <a href="source-inventory.csv">Source inventory and hashes</a></p><p class="notice">Evidence supports the exterior and site. The rear, interior, exact wall dimensions and roof assembly remain uncertain. Generated concepts and V1 geometry are excluded as evidence.</p><nav aria-label="Filter ground references"><button data-filter="all" aria-pressed="true">All references</button><button data-filter="dated" aria-pressed="false">Dated ground views</button><button data-filter="undated" aria-pressed="false">Undated ground / overhead</button></nav></header><main><div class="grid">'''
page += ''.join(cards)
page += '''<figure class="wide"><img src="references/site-aerial-2026-09-04.png" alt="North-up aerial of the target beside the highway"><figcaption><h2>S04 · Site aerial</h2><p>Esri World Imagery / Vantor Vivid. Point metadata reports October 30, 2025 acquisition, 0.34 m source resolution and 8.47 m accuracy field. Accessed September 4, 2026. Target at center-right; larger neighboring residence to northwest; divided highway south and open field east. Screenshot uses browser-fitted image display.</p><a href="sources/imagery-metadata.json">Saved acquisition metadata</a></figcaption></figure><figure class="wide"><img src="site-context.svg" alt="County GIS site schematic"><figcaption><h2>GIS relationship check</h2><p>The target rectangle is east/southeast of 4381. Its older mapped envelope is about 7.35 × 15.3 m. This is not a verified shell measurement; canopy inclusion is unresolved. Parcel lines are mapping context, not surveyed boundaries.</p></figcaption></figure></div></main><script>document.querySelectorAll('button[data-filter]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('button[data-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));document.querySelectorAll('figure[data-date]').forEach(f=>f.classList.toggle('hidden',b.dataset.filter!=='all'&&f.dataset.date!==b.dataset.filter));}));</script></html>'''
(ROOT / 'reference-board.html').write_text(page, encoding='utf-8')
print(f'Built reference board, site SVG and classified {len(rows)} inventory records.')
