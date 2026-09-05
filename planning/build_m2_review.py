"""Build dimensioned SVGs and a local review page from the V2 parameter file."""
from pathlib import Path
import json
import html
import csv
import math

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'planning'/'m2-review'
P=json.loads((ROOT/'model'/'blockout-parameters.json').read_text())
W,D,T,F=[P[k] for k in ['shell_width','shell_depth','wall_thickness','floor_level']]
pw=P['passage_clear_width']/2
pt=P['partition_thickness']
sy=P['store_start']
dy=P['store_door_y']
dw=P['store_door_width']
entry=P['entry_recess']
doorhalf=P['front_door_pair_width']/2
return_y=P['entry_return_front_y']
return_length=math.hypot(P['entry_mouth_width']/2-doorhalf,entry-return_y)
recess_inside=max(entry-T,0)
width_at_inner_wall=P['front_door_pair_width']+2*recess_inside
shop_area=(W-2*T)*(sy-T)-recess_inside*(width_at_inner_wall+P['front_door_pair_width'])/2
sx,oy,scale=310,940,49

def xy(x,y): return sx+x*scale,oy-y*scale
def start(w,h,title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">',f'<rect width="{w}" height="{h}" fill="#f6f4ed"/>',
    '<style>text{font-family:system-ui,sans-serif;fill:#243c3d}.small{font-size:12px}.dim{font-size:13px}.title{font-size:23px;font-weight:650}.room{font-size:15px;font-weight:600}</style>',
    f'<text x="32" y="42" class="title">{title}</text>', '<text x="32" y="67" class="small">M2 / 4397 Hwy 9 W / provisional dimensions in metres / September 4, 2026</text>']
svg=start(840,1110,'Provisional floor plan')
def rect(x0,x1,y0,y1,fill,stroke='none'):
    x,y=xy(x0,y1)
    svg.append(f'<rect x="{x}" y="{y}" width="{(x1-x0)*scale}" height="{(y1-y0)*scale}" fill="{fill}" stroke="{stroke}"/>')
def line(a,b,color='#243c3d',width=1,dash=''):
    x,y=xy(*a); xx,yy=xy(*b)
    svg.append(f'<path d="M{x},{y}L{xx},{yy}" fill="none" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"/>')
def label(x,y,text,cls='small',anchor='middle'):
    x,y=xy(x,y)
    svg.append(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{html.escape(text)}</text>')
def dimh(a,b,y,labeltext):
    line((a,y),(b,y))
    for x in [a,b]: line((x,y-.10),(x,y+.10))
    label((a+b)/2,y+.15,labeltext,'dim')
rect(-W/2,W/2,0,D,'#fff')
rect(-W/2+T,W/2-T,T,sy,'#dce8e0')
for s in [-1,1]:
    a,b=sorted([s*W/2,s*(W/2-T)])
    rect(a,b,0,D,'#855b49')
    a,b=sorted([s*(pw+pt),s*(W/2-T)])
    rect(a,b,sy,sy+pt,'#526665')
    a,b=sorted([s*pw,s*(pw+pt)])
    for y0,y1 in [(sy,dy),(dy+dw,D-T)]: rect(a,b,y0,y1,'#526665')
for a,b in [(-W/2,-.5),(.5,W/2)]: rect(a,b,D-T,D,'#855b49')
mouth=P['entry_mouth_width']/2
for s in [-1,1]:
    for a,b in [(mouth,P['display_inner_x']),(P['display_outer_x'],W/2)]:
        a,b=sorted([s*a,s*b]);rect(a,b,0,T,'#855b49')
    line((s*P['display_inner_x'],.10),(s*P['display_outer_x'],.10),'#2e8898',5)
    line((s*mouth,return_y),(s*doorhalf,entry),'#2e8898',4)
    # Door closed/open poses and swing arcs in plan.
    hinge=(s*(pw+pt/2),dy+dw)
    line(hinge,(hinge[0]+s*dw,hinge[1]),'#b17a35',3)
    line(hinge,(hinge[0],dy),'#b17a35',1,'4 3')
    x,y=xy(hinge[0]+s*dw,hinge[1]);xx,yy=xy(hinge[0],dy)
    svg.append(f'<path d="M{x},{y}A{dw*scale},{dw*scale} 0 0 {1 if s<0 else 0} {xx},{yy}" fill="none" stroke="#b17a35" stroke-dasharray="3 3"/>')
    line((s*doorhalf,entry),(s*(doorhalf+doorhalf*math.cos(math.radians(85))),entry+doorhalf*math.sin(math.radians(85))),'#b17a35',3)
line((-.5,D-.12),(-.5,D+.88),'#b17a35',3)
rect(1.25,3.15,1.64,2.26,'#ae8555')
rect(1.97,2.43,2.65,3.11,'#ae8555')
label(2.2,1.25,'Counter 1.90 × 0.62')
label(2.2,3.55,'Empty chair')
label(0,5.8,'R01 / OPEN STORE','room')
label(0,5.3,f'6.87 m clear width / ~{shop_area:.1f} m²')
label(0,4.85,'M3 proposed furnished-room boundary')
for s,name in [(-1,'R02 / LEFT STORE'),(1,'R03 / RIGHT STORE')]:
    label(s*2.14,12.8,name,'small')
    label(s*2.14,12.35,'2.565 × 6.14 m')
    label(s*2.14,11.9,'15.75 m²')
label(0,14,'R04','room')
label(0,13.6,'Passage')
dimh(-pw,pw,13.1,'1.50 clear')
dimh(-W/2,W/2,16.1,'7.35 m shell width')
dimh(-W/2+T,-pw-pt,14.7,'2.565 clear')
dimh(pw+pt,W/2-T,14.7,'2.565 clear')
line((W/2+.55,0),(W/2+.55,D))
for y in [0,D]:line((W/2+.4,y),(W/2+.7,y))
label(W/2+.85,7.7,'15.30 m','dim','start')
line((W/2+2.45,T),(W/2+2.45,sy))
label(W/2+2.6,4.0,'8.56 m','dim','start')
line((W/2+2.45,sy+pt),(W/2+2.45,D-T))
label(W/2+2.6,11.5,'6.14 m','dim','start')
line((-W/2-.3,-P['canopy_depth']),(W/2+.3,-P['canopy_depth']),'#8c9f9c',2,'5 4')
label(0,-1.85,'CANOPY: 1.45 m beyond front wall / front faces ~200° SSW')
report=json.loads((OUT/'circulation-check.json').read_text())
for a,b in zip(report['route'],report['route'][1:]):line(a,b,'#27766b',2,'6 4')
svg.extend(['<text x="32" y="1060" class="small">Green dashed: recorded route. Ochre: open doors and swing zones. Blue: existing glazing.</text>',
'<text x="32" y="1082" class="small">Room sizes and fittings are invented. Rear exit and ceiling follow Brian’s recollection.</text>','</svg>'])
(OUT/'dimensioned-plan.svg').write_text('\n'.join(svg),encoding='utf-8')

# Longitudinal section schematic uses the same heights and depth as the scene.
svg=start(1100,540,'Longitudinal section through central passage')
def q(y,z):return 125+y*53,390-z*53
def secbox(y0,y1,z0,z1,color):
    x,y=q(y0,z1);svg.append(f'<rect x="{x}" y="{y}" width="{(y1-y0)*53}" height="{(z1-z0)*53}" fill="{color}"/>')
def secline(a,b,color,width=2,dash=''):
    x,y=q(*a);xx,yy=q(*b);svg.append(f'<path d="M{x},{y}L{xx},{yy}" stroke="{color}" stroke-width="{width}" stroke-dasharray="{dash}"/>')
secbox(0,D,0,F,'#777e74')
secbox(T,D-T,F+P['ceiling_clear_height'],F+P['ceiling_clear_height']+.12,'#bac5bc')
secline((0,P['roof_front']),(D,P['roof_rear']),'#314648',7)
for a,b,h in P['parapet_segments']:
    secline((a,h),(b,h),'#9b614c',4)
for seg,nextseg in zip(P['parapet_segments'],P['parapet_segments'][1:]):
    secline((seg[1],seg[2]),(seg[1],nextseg[2]),'#9b614c',4)
secline((-P['canopy_depth'],P['canopy_front_height']),(0,P['canopy_back_height']),'#738d89',6)
secline((-P['canopy_depth'],0),(-P['canopy_depth'],P['canopy_front_height']),'#738d89',3)
secline((entry,F),(entry,F+P['front_door_height']),'#b17a35',3)
secline((D-.12,F),(D-.12,F+P['interior_door_height']),'#b17a35',3)
secline((sy,F),(sy,F+P['ceiling_clear_height']),'#8c9f9c',1,'5 4')
for x,y,text in [(135,112,'Front parapet +4.40'),(760,166,'Rear parapet +3.60'),(300,240,'Roof +3.70 → +3.40; fall 0.30 m / 1.96%'),(330,285,'Flat ceiling +3.08; 2.90 m clear above floor'),(300,340,'Eye +1.83 (1.65 m above floor)'),(340,413,'Floor +0.18; apron +0.07; ground datum 0.00')]:
    svg.append(f'<text x="{x}" y="{y}" class="dim">{text}</text>')
secline((1,F+1.65),(D-.4,F+1.65),'#27766b',1,'6 4')
svg.extend(['<text x="32" y="468" class="small">Side parapet shown in projection. Ceiling remains level while roof and parapet descend independently.</text>',
'<text x="32" y="490" class="small">Clear roof cavity is ~0.13 m rear to ~0.43 m front; structural framing and drainage remain unresolved.</text>',
'<text x="32" y="512" class="small">Thresholds are provisional small steps. No measured levels, basement or upper floor are established.</text>','</svg>'])
(OUT/'section.svg').write_text('\n'.join(svg),encoding='utf-8')

rooms=[['R01','Open store','6.87 clear width × 8.56 maximum clear depth',f'~{shop_area:.1f}','Invented; recess deducted approximately'],['R02','Left storeroom','2.565 × 6.14','15.75','Invented'],['R03','Right storeroom','2.565 × 6.14','15.75','Invented'],['R04','Rear passage','1.50 × 6.26','9.39','Invented']]
openings=[['D01','Front paired glazed doors','1.40 total / 0.70 each','2.15',f'y={entry:.3f}','Observed arrangement; size and inward swing invented'],['D02','Left storeroom door','1.00','2.10','x=-0.81; y=9.35–10.35','Invented; opens into room'],['D03','Right storeroom door','1.00','2.10','x=+0.81; y=9.35–10.35','Invented; opens into room'],['D04','Rear door','1.00','2.10','Centered y=15.18','Recollection; size and outward swing invented'],['W01/W02','Display windows','1.90 each','1.82','Front; sill 0.66 above floor','Observed fixed display arrangement; sizes inferred'],['W03/W04','Angled entrance returns',f'{return_length:.3f} each','1.49',f'45 degrees; entry recess {entry:.3f}','Observed glazing; W04 top-hinged approach approved; build in M3'],['I01–I03','Closed right-side infill','1.55 / 1.15 / 1.05','1.10 / 2.10 / 2.05','y=5.15 / 9.25 / 12.00','Closed baseline observed; extents provisional']]
for name,headers,rows in [('room-schedule.csv',['ID','Room','Clear dimensions m','Area m2','Class'],rooms),('opening-schedule.csv',['ID','Opening','Width m','Height m','Location','Evidence and decision'],openings)]:
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f);writer.writerow(headers);writer.writerows(rows)

page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>M2 blockout review / 4397 Hwy 9 W</title><style>
*{box-sizing:border-box}body{margin:0;background:#f1f2ec;color:#223d3c;font:16px/1.6 system-ui}header,main{max-width:1300px;margin:auto;padding:28px}h1{font-size:42px;line-height:1.1}h2{margin-top:36px}a{color:#186c71}img,video{width:100%;display:block}figure{margin:0;background:white;border-radius:8px;overflow:hidden}figcaption{padding:15px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}.notice{padding:18px;background:#e5dfc9;border-left:4px solid #a17c32}.tag{font-size:13px;letter-spacing:.08em}.plan{max-height:1000px;object-fit:contain;background:#f6f4ed}table{width:100%;border-collapse:collapse}td,th{padding:10px;border-bottom:1px solid #cdd5cc;text-align:left}nav{display:flex;gap:20px;flex-wrap:wrap}small{color:#5f7270}@media(max-width:760px){.grid{grid-template-columns:1fr}h1{font-size:30px}header,main{padding:20px}}
</style><header><div class="tag">M2 · APPROVED AND COMPLETE</div><h1>4397 Hwy 9 W</h1><p>Whole-building layout with an open store, two rear storerooms, central passage and empty chair behind the front-right counter.</p><p class="notice">Provisional reconstruction. Photographs support the visible architecture; exact dimensions, interior and unseen rear details are assumptions. These are simple blockout materials. Brian approved the corrected blockout with single 45-degree entrance returns meeting the doors directly. Approval is recorded in Notion. Brian also explicitly approved the concealed top-hinged right pane with a 15-degree inward tilt. M2 is Done in Notion; detailed implementation belongs to M3.</p><nav><a href="https://app.notion.com/p/3d1488886d5781c18428fc814fe8cba4">M2 in Notion</a><a href="../../model/myrtle-beach-v2-blockout.blend">Blender source</a><a href="../m2-review.md">Decisions and review notes</a><a href="#layout">Plan and section</a><a href="#walk">Walkthrough</a></nav></header><main><h2>Exterior comparisons</h2><p>Approximate corresponding viewpoints, not solved camera matches. Original screenshots remain unchanged with their Google attribution. Compare openings, canopy and parapet silhouette; tree shapes and surfaces are placeholders.</p>'''
page+='<h2 id="entrance">Corrected entrance</h2><figure><img src="entrance-correction.png" alt="Closed entrance doors with one 45-degree glazed return on each side"><figcaption>One angled pane on each side meets the door frame directly. No intermediate window bay. The return angle is 45 degrees; the provisional recess is 0.305 m.</figcaption></figure>'
for name,photo,caption in [('front','152551','G04 / undated crop consistent with Nov 2025 set'),('front-left','152518','G02 / November 2025 shown in UI'),('front-right','152613','G05 / November 2025 shown in UI')]:
    page+=f'<h3>{name.replace("-"," ").title()}</h3><div class="grid"><figure><img src="../../research/references/google_maps_images/Screenshot%202026-01-02%20{photo}.png" alt="Original {name} photograph"><figcaption>{caption} · unchanged photographic evidence</figcaption></figure><figure><img src="{name}.png" alt="V2 {name} blockout"><figcaption>V2 first-pass {name} · provisional dimensions</figcaption></figure></div>'
page+='''<h2 id="layout">Dimensioned layout</h2><div class="grid"><figure><img class="plan" src="dimensioned-plan.svg" alt="Dimensioned floor plan"><figcaption><a href="dimensioned-plan.svg">Open full plan</a> · shell 7.35 × 15.30 m</figcaption></figure><figure><img class="plan" src="plan.png" alt="Blender top cutaway"><figcaption>Blender cutaway: roof, ceiling and canopy hidden; doors open.</figcaption></figure></div><figure><img src="section.svg" alt="Longitudinal section"><figcaption><a href="section.svg">Open section</a> · floor, ceiling, roof and parapet levels are separate assumptions.</figcaption></figure><h2>Room and opening schedules</h2><p><a href="room-schedule.csv">Rooms CSV</a> · <a href="opening-schedule.csv">Openings CSV</a></p>'''
page+='<table><tr><th>Room</th><th>Clear dimensions</th><th>Area</th></tr>'+''.join(f'<tr><td>{r[0]} · {r[1]}</td><td>{r[2]}</td><td>{r[3]} m²</td></tr>' for r in rooms)+'</table>'
page+='<h2>Walking-height interior</h2><div class="grid">'
for name,caption in [('entry-interior','Entry to central passage and centered rear exit'),('chair-counter','Empty front-right chair on the staff side of the counter'),('left-store','Left storeroom looking toward its passage door'),('right-store','Right storeroom looking toward its passage door')]:
    page+=f'<figure><img src="{name}.png" alt="{caption}"><figcaption>{caption}</figcaption></figure>'
page+='</div><h2 id="walk">Recorded circulation</h2><video controls preload="metadata" src="walkthrough.mp4" poster="entry-interior.png"></video>'
page+=f'<p>{report["duration_seconds"]:.1f} seconds · eye 1.65 m above floor · all rooms visited · {report["route_samples"]} route samples checked with a 0.50 m diameter body and no wall, furniture or open-door overlap. <a href="circulation-check.json">Check details</a>.</p><p>The paired front doors open during the approach, showing that the moving glazed panels are door leaves. Each fixed entrance return is a single 45-degree pane ending at its door jamb. Workbench glass hides after frame 40 for interior visibility. This recording checks layout; browser collision and functional interactions belong to M3.</p>'
page+='''<h2>Approved operable-window approach</h2><p>Use W04, the existing right-hand angled glazed entrance return. Keep its full visible pane and opening perimeter, with a concealed top hinge allowing a limited 15° inward tilt. A 1.49 m pane would move about 0.39 m inward at its bottom. Brian explicitly approved this invented mechanism. Detailed construction and operation remain M3 work. Retain closed right-side masonry infill. M3 must check hinge/frame clearances, door separation and safe reach.</p><h2>M3 proposed boundary</h2><p>The entire R01 front store up to the partitions at y=8.8 m, including floor and flat ceiling, chair/counter, paired entrance doors, display windows and returns. Exterior: complete front facade and canopy, apron to y=-4.7 m, and side returns to y=3.5 m. Rear rooms and the rest of the site remain blockout context. Use this boundary when refining the M3 checklist and performance budgets at kickoff.</p><h2>Immediate setting</h2><figure><img src="site.png" alt="Simple immediate site masses"><figcaption>Local +Y points rearward (~020°), +X toward the right side (~110°). Neighbor at local left/rear (NW), field at right (E), divided highway in front (SSW). Distances and tree masses are provisional.</figcaption></figure></main></html>'''
(OUT/'index.html').write_text(page,encoding='utf-8')
print('Built M2 plan, section, schedules and review page.')
