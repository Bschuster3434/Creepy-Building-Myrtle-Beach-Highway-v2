"""Create V2 only. Run with Blender --background --python this_file -- [--walk]."""
import bpy
import json
import math
import sys
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'model'
REVIEW = ROOT / 'planning' / 'm2-review'
REVIEW.mkdir(parents=True, exist_ok=True)
P = json.loads((OUT / 'blockout-parameters.json').read_text())
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1
scene['provenance'] = 'V2 original geometry; provisional dimensions. M1 E03-E19 and authorized imagined interior.'
scene['parameters'] = json.dumps(P)
W, D, T, F = (P[k] for k in ['shell_width', 'shell_depth', 'wall_thickness', 'floor_level'])
H = F + P['ceiling_clear_height']
FRONT_TOP=P['parapet_segments'][0][2]
REAR_TOP=P['parapet_segments'][-1][2]
assert P['roof_rear']-.07 > H+.12, 'Roof must clear ceiling assembly'
collections = {}
for name in ['Shell', 'Roof', 'Storefront', 'Glazing', 'Partitions', 'Doors', 'Furniture', 'Site', 'Cameras']:
    c = bpy.data.collections.new(name)
    scene.collection.children.link(c)
    collections[name] = c
colors = {'brick': (.40,.19,.13,1), 'infill': (.43,.25,.19,1), 'trim': (.77,.77,.68,1),
          'glass': (.12,.21,.23,1), 'floor': (.48,.46,.40,1), 'inside': (.66,.65,.57,1),
          'roof': (.20,.23,.23,1), 'wood': (.38,.28,.17,1), 'grass': (.34,.40,.25,1),
          'road': (.23,.25,.25,1), 'tree': (.21,.31,.19,1), 'trunk': (.28,.23,.17,1)}
materials = {}
for name, color in colors.items():
    m = bpy.data.materials.new(name)
    m.diffuse_color = color
    materials[name] = m
colliders, doors, glass = [], [], []

def move_collection(obj, group):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    collections[group].objects.link(obj)

def box(name, loc, size, mat='brick', group='Shell', collision=False):
    assert min(size) > 0, (name, size)
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(materials[mat])
    move_collection(o, group)
    o['evidence'] = 'Invented fit' if group in ['Partitions','Furniture','Doors'] else 'See M2 geometry decision register'
    if collision:
        colliders.append(o)
    if group == 'Glazing':
        glass.append(o)
    return o

def bounds_box(name, x0,x1,y0,y1,z0,z1, **kw):
    return box(name, ((x0+x1)/2,(y0+y1)/2,(z0+z1)/2), (x1-x0,y1-y0,z1-z0), **kw)

def segment(name, a,b,z0,z1,thick,mat='trim',group='Storefront'):
    a,b = Vector(a),Vector(b)
    o = box(name, ((a.x+b.x)/2,(a.y+b.y)/2,(z0+z1)/2), ((b-a).length,thick,z1-z0),mat,group)
    o.rotation_euler.z = math.atan2(b.y-a.y,b.x-a.x)
    return o

def panel(name,a,b,z0,z1, operable=False):
    # Frames follow the existing opening perimeter; no new exterior subdivision.
    segment(name+'_sill',a,b,z0,z0+.065,.09)
    segment(name+'_head',a,b,z1-.065,z1,.09)
    for i,p in enumerate([a,b]):
        box(name+'_jamb_'+str(i),(p[0],p[1],(z0+z1)/2),(.065,.09,z1-z0),'trim','Storefront')
    o=segment(name+'_pane',a,b,z0+.065,z1-.065,.025,'glass','Glazing')
    o['operable_proposal'] = 'Top-hinged whole return pane; inward 15 degrees, pending Brian review' if operable else 'Fixed display glazing'
    return o

def door(name, hinge, width, closed_angle, open_angle, glazed=False):
    pivot = bpy.data.objects.new(name+'_hinge',None)
    collections['Doors'].objects.link(pivot)
    pivot.location = hinge
    height = P['front_door_height'] if glazed else P['interior_door_height']
    parts=[]
    if glazed:
        parts += [box(name+'_rail_'+str(i),(width/2,0,z),(width,.07,.11),'trim','Doors') for i,z in enumerate([.055,.47,height-.055])]
        parts += [box(name+'_stile_'+str(i),(x,0,height/2),(.07,.07,height),'trim','Doors') for i,x in enumerate([.035,width-.035])]
        pane=box(name+'_glass',(width/2,0,(height+.52)/2),(width-.14,.025,height-.63),'glass','Glazing')
        parts.append(pane)
        parts.append(box(name+'_lower_panel',(width/2,0,.255),(width-.14,.05,.34),'trim','Doors'))
    else:
        parts.append(box(name+'_leaf',(width/2,0,height/2),(width,.045,height),'wood','Doors'))
    for part in parts:
        part.parent = pivot
    pivot.rotation_euler.z = closed_angle
    pivot['closed_angle'] = closed_angle
    pivot['open_angle'] = open_angle
    pivot['clear_opening_m'] = width
    doors.append(pivot)
    return pivot

# Continuous level floor, thin ceiling, separately falling concealed roof.
bounds_box('Floor',-W/2,W/2,0,D,0,F,mat='floor')
for s in [-1,1]:
    x=s*(W/2-T/2)
    box('Side_wall_'+str(s),(x,D/2,(F+3.25)/2),(T,D,3.25-F),collision=True)
    for i,(y0,y1,z) in enumerate(P['parapet_segments']):
        box('Parapet_'+str(s)+'_'+str(i),(x,(y0+y1)/2,(3.25+z)/2),(T,y1-y0,z-3.25))
        box('Parapet_coping_'+str(s)+'_'+str(i),(x,(y0+y1)/2,z+.025),(T+.035,y1-y0,.05))
box('Flat_ceiling',(0,D/2,H+.06),(W-2*T,D-2*T,.12),'inside','Roof')
roof=box('Low_slope_roof',(0,D/2,(P['roof_front']+P['roof_rear'])/2),(W-T,D,.14),'roof','Roof')
roof.rotation_euler.x=math.atan2(P['roof_rear']-P['roof_front'],D)
rw=P['rear_door_width']
for a,b in [(-W/2,-rw/2),(rw/2,W/2)]:
    bounds_box('Rear_wall',a,b,D-T,D,F,REAR_TOP,collision=True)
bounds_box('Rear_lintel',-rw/2,rw/2,D-T,D,F+2.1,REAR_TOP,collision=True)
door('D04_rear',(-rw/2,D-T/2,F+.01),rw,0,math.pi/2)
box('Rear_landing',(0,D+.75,.09),(1.8,1.5,.18),'floor','Site')
box('Rear_step',(0,D+1.7,.045),(1.8,.4,.09),'floor','Site')

# Front facade openings, angled glazed recess and paired doors.
mouth=P['entry_mouth_width']/2
return_y=P['entry_return_front_y']
return_run=P['entry_recess']-return_y
return_inset=mouth-P['front_door_pair_width']/2
return_angle=math.degrees(math.atan2(return_run,return_inset))
assert math.isclose(return_angle,P['entry_return_angle_degrees'],abs_tol=1e-6)
wi,wo=P['display_inner_x'],P['display_outer_x']
zs,zh=F+P['display_sill'],F+P['display_head']
for sign in [-1,1]:
    for i,(a,b) in enumerate([(mouth,wi),(wo,W/2)]):
        x0,x1=sorted([sign*a,sign*b])
        bounds_box('Front_pier_'+str(sign)+'_'+str(i),x0,x1,0,T,F,3.3,collision=True)
    x0,x1=sorted([sign*wi,sign*wo])
    bounds_box('Display_spandrel_'+str(sign),x0,x1,0,T,F,zs,collision=True)
    bounds_box('Display_lintel_'+str(sign),x0,x1,0,T,zh,3.3)
    panel('W0'+str(1 if sign<0 else 2)+'_display',(x0,-.025),(x1,-.025),zs,zh)
    a=(sign*mouth,return_y)
    b=(sign*P['front_door_pair_width']/2,P['entry_recess'])
    segment('Return_base_'+str(sign),a,b,F,zs,.10,'trim')
    pane=panel('W0'+str(3 if sign<0 else 4)+'_return',a,b,zs,F+P['front_door_height'],operable=sign>0)
    pane['angle_to_front_degrees']=return_angle
    pane['meets_door_jamb_directly']=True
    segment('Return_lintel_'+str(sign),a,b,F+P['front_door_height'],3.3,.12,'brick','Shell')
bounds_box('Front_parapet',-W/2,W/2,0,T,3.3,FRONT_TOP)
bounds_box('Recess_front_lintel',-mouth,mouth,0,T,F+P['front_door_height'],3.3)
box('Front_coping',(0,T/2,FRONT_TOP+.025),(W+.035,T+.035,.05))
doorw=P['front_door_pair_width']/2
door('D01L_front',(-doorw,P['entry_recess'],F+.01),doorw,0,math.radians(95),True)
door('D01R_front',(doorw,P['entry_recess'],F+.01),doorw,math.pi,math.radians(85),True)
bounds_box('Entry_head',-doorw,doorw,P['entry_recess']-.06,P['entry_recess']+.06,F+P['front_door_height'],3.3)
cd=P['canopy_depth']
canopy=box('Canopy_sheet',(0,-cd/2, (P['canopy_front_height']+P['canopy_back_height'])/2),(W+.55,cd,.12),'trim','Storefront')
canopy.rotation_euler.x=math.atan2(P['canopy_back_height']-P['canopy_front_height'],cd)
box('Canopy_front_fascia',(0,-cd,P['canopy_front_height']-.035),(W+.55,.12,.16),'trim','Storefront')
for i,x in enumerate([-W/2-.13,-.43,W/2+.13]):
    box('Canopy_post_'+str(i),(x,-cd,P['canopy_front_height']/2),(.065,.065,P['canopy_front_height']),'trim','Storefront',True)
box('Chimney',(W/2-.34,10.6,3.85),(.52,.65,1.05))
box('Chimney_cap',(W/2-.34,10.6,4.4),(.65,.77,.10),'roof')
for i,(y,z,w,h) in enumerate([(5.15,1.88,1.55,1.10),(9.25,1.52,1.15,2.1),(12,1.55,1.05,2.05)]):
    box('Closed_right_infill_'+str(i),(W/2+.008,y,z),(.02,w,h),'infill')
for s in [-1,1]:
    for i,y in enumerate([3.0,7.4,12.9]):
        box('Low_vent_'+str(s)+'_'+str(i),(s*(W/2+.013),y,.32),(.025,.30,.16),'roof')
box('High_front_side_vent',(W/2+.016,.6,2.85),(.03,.23,.22),'roof')
box('High_front_left_vent',(-W/2-.016,.6,2.85),(.03,.23,.22),'roof')

# Authorized imagined layout, adjusted to V2 envelope.
pw=P['passage_clear_width']/2
pt=P['partition_thickness']
sy=P['store_start']
dy=P['store_door_y']
dw=P['store_door_width']
for s in [-1,1]:
    a,b=sorted([s*(pw+pt),s*(W/2-T)])
    bounds_box('Store_front_'+str(s),a,b,sy,sy+pt,F,H,mat='inside',group='Partitions',collision=True)
    a,b=sorted([s*pw,s*(pw+pt)])
    for i,(y0,y1) in enumerate([(sy,dy),(dy+dw,D-T)]):
        bounds_box('Passage_wall_'+str(s)+'_'+str(i),a,b,y0,y1,F,H,mat='inside',group='Partitions',collision=True)
    bounds_box('Store_door_head_'+str(s),a,b,dy,dy+dw,F+2.1,H,mat='inside',group='Partitions',collision=True)
    door('D02_left_store' if s<0 else 'D03_right_store',(s*(pw+pt/2),dy+dw,F+.01),dw,-math.pi/2,math.pi if s<0 else 0)
box('Counter_placeholder',(2.2,1.95,F+.47),(1.9,.62,.94),'wood','Furniture',True)
box('Chair_seat',(2.2,2.88,F+.46),(.46,.46,.09),'wood','Furniture',True)
box('Chair_back',(2.2,3.08,F+.77),(.46,.07,.60),'wood','Furniture',True)
for x in [1.99,2.41]:
    for y in [2.68,3.08]:
        box('Chair_leg',(x,y,F+.22),(.045,.045,.44),'wood','Furniture')

# Immediate setting; positions are contextual estimates, not surveyed boundaries.
box('Ground',(0,5,-.15),(95,95,.22),'grass','Site')
box('Front_apron',(0,-2.35,.035),(W+2,4.7,.07),'floor','Site')
box('Threshold_landing',(0,-.20,.125),(2.2,.40,.11),'floor','Site')
box('Threshold_lower_step',(0,-.60,.08),(2.2,.40,.02),'floor','Site')
box('Near_carriageway',(0,-9,-.01),(95,7,.10),'road','Site')
box('Median',(0,-16,-.005),(95,7,.10),'grass','Site')
box('Far_carriageway',(0,-23,-.01),(95,7,.10),'road','Site')
for y in [-5.6,-12.4,-19.6,-26.4]:
    box('Road_edge',(0,y,.045),(95,.10,.008),'trim','Site')
box('Neighbor_NW_mass',(-20,16,2.4),(12,14,4.8),'inside','Site')
box('Field_E_mass',(28,20,-.025),(30,45,.05),'wood','Site')
for i,(x,y,r,h) in enumerate([(-6,4,3.9,8),(-7,13,4,10),(7,13,3.5,9),(2,19,4,12),(-2,24,5,12),(11,22,4,10)]):
    box('Tree_trunk_'+str(i),(x,y,h*.3),(.38,.38,h*.6),'trunk','Site')
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=(x,y,h*.72))
    o=bpy.context.object
    o.name='Tree_crown_'+str(i)
    o.scale=(r,r,h*.38)
    o.data.materials.append(materials['tree'])
    move_collection(o,'Site')
box('Utility_pole',(6.3,4,5),(.22,.22,10),'trunk','Site')

# Review cameras and a saved walking-height animation.
scene.render.engine='BLENDER_WORKBENCH'
sh=scene.display.shading
sh.light='STUDIO'
sh.color_type='MATERIAL'
sh.show_shadows=True
sh.show_cavity=True
sh.cavity_type='BOTH'
sh.show_specular_highlight=False
sh.background_type='WORLD'
scene.world.color=(.68,.73,.76)
scene.render.resolution_x=1400
scene.render.resolution_y=950
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.fps=8
scene.view_settings.view_transform='Standard'

def camera(name,loc,target,lens=38,ortho=None):
    data=bpy.data.cameras.new(name)
    o=bpy.data.objects.new(name,data)
    collections['Cameras'].objects.link(o)
    o.location=loc
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    data.lens=lens
    data.clip_start=.03
    data.clip_end=200
    if ortho:
        data.type='ORTHO'; data.ortho_scale=ortho
    return o

cameras={
 'front':camera('Front_reference',(1.2,-17,3.0),(0,0,2.0),43),
 'entrance-correction':camera('Entrance_detail',(1.7,-3.9,2.5),(0,.25,1.3),32),
 'front-left':camera('Front_left_reference',(-24,-6,3.0),(0,6,2),40),
 'front-right':camera('Front_right_reference',(17,-14,3.1),(0,6.2,2),43),
 'plan':camera('Plan',(0,D/2,27),(0,D/2,0),ortho=19),
 'entry-interior':camera('Entry_eye',(0,1.5,F+1.65),(0,11,F+1.5),22),
 'chair-counter':camera('Chair_eye',(-1.0,4.5,F+1.65),(2.2,2.2,F+.65),28),
 'left-store':camera('Left_store_eye',(-2.3,12,F+1.65),(-.8,9.8,F+1.3),25),
 'right-store':camera('Right_store_eye',(2.3,12,F+1.65),(.8,9.8,F+1.3),25),
 'site':camera('Site_overview',(38,-40,37),(0,6,0),40)
}
# Route includes each room and exits at the rear. Door leaves use their open pose.
route=[(0,-3),(0,-.6),(0,.9),(0,3),(0,7.8),(0,9.85),(-2.2,9.85),(-2.2,11.8),(-2.2,9.85),(0,9.85),(2.2,9.85),(2.2,11.8),(2.2,9.85),(0,9.85),(0,12.7),(0,15.9)]
walk=camera('Walkthrough',(0,-3,F+1.65),(0,2,F+1.65),24)
samples=[]
frame=1
for i,(a,b) in enumerate(zip(route,route[1:])):
    dist=math.dist(a,b)
    count=max(10,round(dist/.085))
    angle=math.atan2(b[1]-a[1],b[0]-a[0])
    for j in range(count):
        u=j/count
        xy=(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u)
        z=F+P['eye_height']
        walk.location=(*xy,z)
        target=Vector((xy[0]+math.cos(angle),xy[1]+math.sin(angle),z-.06))
        walk.rotation_euler=(target-walk.location).to_track_quat('-Z','Y').to_euler()
        walk.keyframe_insert(data_path='location',frame=frame)
        walk.keyframe_insert(data_path='rotation_euler',frame=frame)
        samples.append({'frame':frame,'x':xy[0],'y':xy[1]})
        frame+=1
    # Pause at each waypoint and turn smoothly before the next leg.
    if i < len(route)-2:
        next_point=route[i+2]
        start_q=walk.rotation_euler.to_quaternion()
        next_target=Vector((next_point[0]-b[0],next_point[1]-b[1],-.06))
        end_q=next_target.to_track_quat('-Z','Y')
        for turn in range(12):
            walk.location=(b[0],b[1],F+P['eye_height'])
            walk.rotation_euler=start_q.slerp(end_q,(turn+1)/12).to_euler()
            walk.keyframe_insert(data_path='location',frame=frame)
            walk.keyframe_insert(data_path='rotation_euler',frame=frame)
            samples.append({'frame':frame,'x':b[0],'y':b[1]})
            frame+=1
scene.frame_start=1
scene.frame_end=frame-1
for d in doors:
    d.rotation_euler.z=d['open_angle']
bpy.context.view_layer.update()
# Check a swept 0.5 m diameter body against actual wall/furniture/open-leaf bounds.
checks=[]
obstacles=colliders+[o for o in collections['Doors'].objects if o.type=='MESH']
for sample in samples:
    x,y=sample['x'],sample['y']
    for o in obstacles:
        vs=[o.matrix_world@Vector(v) for v in o.bound_box]
        lo=[min(v[k] for v in vs) for k in range(3)]
        hi=[max(v[k] for v in vs) for k in range(3)]
        if hi[2]<F+.05 or lo[2]>F+1.8: continue
        dx=max(lo[0]-x,0,x-hi[0]); dy0=max(lo[1]-y,0,y-hi[1])
        if dx*dx+dy0*dy0<P['walker_radius']**2:
            checks.append({'frame':sample['frame'],'object':o.name})
report={'route_samples':len(samples),'walker_diameter_m':2*P['walker_radius'],
 'collisions':checks,'door_pose':'all open','eye_height_m':P['eye_height'],
 'limitations':'Horizontal swept-circle check; conservative leaf AABBs. Threshold steps and real browser physics require M3 verification.',
 'route':route, 'duration_seconds':(frame-1)/scene.render.fps,
 'entrance_return_angle_degrees':return_angle,
 'entrance_return_panes':len([o for o in glass if '_return_pane' in o.name]),
 'entrance_return_recess_m':P['entry_recess'],
 'front_door_opening_frames':[28,40]}
(REVIEW/'circulation-check.json').write_text(json.dumps(report,indent=2))
assert not checks, str(checks[:10])
for d in doors:
    d.rotation_euler.z=d['closed_angle']
    d.keyframe_insert(data_path='rotation_euler',frame=1)
    if d.name.startswith('D01'):
        d.keyframe_insert(data_path='rotation_euler',frame=28)
    d.rotation_euler.z=d['open_angle']
    d.keyframe_insert(data_path='rotation_euler',frame=40 if d.name.startswith('D01') else 2)
for o in glass:
    o.hide_render=False
    o.keyframe_insert(data_path='hide_render',frame=1)
    o.keyframe_insert(data_path='hide_render',frame=40)
    o.hide_render=True
    o.keyframe_insert(data_path='hide_render',frame=41)
scene.camera=cameras['front-right']
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'myrtle-beach-v2-blockout.blend'))

def render(name,cam):
    scene.camera=cam
    scene.render.filepath=str(REVIEW/(name+'.png'))
    bpy.ops.render.render(write_still=True)

for name in ['front','front-left','front-right','site','entrance-correction']:
    render(name,cameras[name])
scene.frame_set(41)
for d in doors: d.rotation_euler.z=d['open_angle']
for o in glass: o.hide_render=True
for name in ['entry-interior','chair-counter','left-store','right-store']:
    render(name,cameras[name])
hidden=[]
for group in ['Roof','Site']:
    for o in collections[group].objects:
        if not o.hide_render: hidden.append(o)
        o.hide_render=True
for o in collections['Shell'].objects:
    if o.name.startswith(('Front_parapet','Front_coping','Entry_head','Recess_front_lintel')):
        o.hide_render=True; hidden.append(o)
for o in collections['Storefront'].objects:
    if o.name.startswith('Canopy'):
        o.hide_render=True; hidden.append(o)
scene.render.resolution_x=1000
scene.render.resolution_y=1450
render('plan',cameras['plan'])
for o in hidden: o.hide_render=False
if '--walk' in sys.argv:
    scene.camera=walk
    scene.render.resolution_x=960
    scene.render.resolution_y=640
    frames=REVIEW/'walk-frames'
    frames.mkdir(exist_ok=True)
    scene.render.filepath=str(frames/'frame-')
    bpy.ops.render.render(animation=True)
print('M2_BUILD_COMPLETE',json.dumps(report))
