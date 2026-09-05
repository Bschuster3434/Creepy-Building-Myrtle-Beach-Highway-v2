"""Derive the M3 sample from the approved, read-only M2 blockout.
Blender --background --python model/build_sample.py
All generated outputs stay in V2. Materials are deterministic original procedural work.
"""
import bpy, math, json
import numpy as np
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'app/public/assets'
TEX = ROOT / 'model/sample-textures'
ASSETS.mkdir(parents=True, exist_ok=True)
TEX.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'model/myrtle-beach-v2-blockout.blend'))
scene = bpy.context.scene
scene.frame_set(1)
for o in list(bpy.data.objects):
    o.animation_data_clear()
    if o.type in {'CAMERA','LIGHT'} or o.name.startswith(('Counter_placeholder','Chair_', 'Tree_', 'Neighbor_', 'Field_', 'Utility_', 'Near_carriageway','Far_carriageway','Median','Road_edge','Rear_landing','Rear_step')):
        bpy.data.objects.remove(o, do_unlink=True)
    else:
        o.hide_render=False
for o in bpy.data.objects:
    if 'closed_angle' in o: o.rotation_euler.z=o['closed_angle']
    if o.name in {'D02_left_store_hinge','D03_right_store_hinge'}:
        o.rotation_euler.z=o['open_angle']

# Brian's M3 service-shop revision: shorten the sales room by 3 m while
# keeping the exterior envelope and continuous central passage unchanged.
STORE_FRONT=5.8
STORE_SHIFT=STORE_FRONT-8.8
for o in bpy.data.objects:
    if o.name.startswith(('Store_front_','Store_door_head_')) or o.name in {'D02_left_store_hinge','D03_right_store_hinge'}:
        o.location.y+=STORE_SHIFT
    elif o.name.startswith('Passage_wall_'):
        if o.name.endswith('_0'):
            o.location.y+=STORE_SHIFT
        else:
            o.location.y+=STORE_SHIFT/2
            o.dimensions.y-=STORE_SHIFT

rng = np.random.default_rng(4397)
N=512
y,x=np.mgrid[0:N,0:N]/N
noise=rng.normal(0,1,(N,N))
def image(name, rgb):
    a=np.ones((N,N,4),dtype=np.float32); a[:,:,:3]=np.clip(rgb,0,1)
    im=bpy.data.images.new(name,width=N,height=N)
    im.pixels.foreach_set(a.ravel()); im.filepath_raw=str(TEX/(name+'.png')); im.file_format='PNG'; im.save()
    return im

def texture(kind):
    if kind=='brick':
        row=np.floor(y*16).astype(int); col=np.floor(x*8+(row%2)*.5).astype(int)%8
        u=(x*8+(row%2)*.5)%1; v=(y*16)%1
        mortar=(u<.045)|(u>.955)|(v<.085)|(v>.915)
        variation=rng.uniform(-.07,.07,(16,8))[row,col]
        mottled=.025*np.sin(x*132+y*48)*np.sin(y*178)+noise*.014
        base=np.array([.49,.34,.265])[None,None,:]+(variation*.65+mottled)[:,:,None]
        base[mortar]=np.array([.56,.535,.455])+noise[mortar,None]*.016
        height=np.where(mortar,.1,.75)+noise*.055
    elif kind=='wood':
        grain=np.sin(x*900+np.sin(y*26)*1.3+np.sin(x*37)*3)*.005
        broad=np.sin(x*82+np.sin(y*9))*.008
        base=np.array([.44,.36,.265])[None,None,:]+(grain+broad+noise*.006)[:,:,None]
        height=.5+grain*.3+noise*.005
    else:
        colors={'floor':[.52,.49,.42], 'inside':[.72,.70,.62], 'trim':[.63,.65,.56], 'roof':[.22,.245,.22], 'grass':[.35,.375,.24]}
        cloud=np.sin(x*26+np.cos(y*12))*np.sin(y*19)*.012
        base=np.array(colors[kind])[None,None,:]+(cloud+noise*.012)[:,:,None]
        height=.5+noise*.07
    albedo=image(kind+'_base',base)
    dy,dx=np.gradient(height)
    normal=np.dstack((-dx*1.4,-dy*1.4,np.ones_like(dx)))
    normal/=np.linalg.norm(normal,axis=2)[:,:,None]
    normal=image(kind+'_normal',normal*.5+.5); normal.colorspace_settings.name='Non-Color'
    return albedo,normal

def aged_texture(kind):
    # Periodic multiscale noise: quiet broad variation and irregular local wear,
    # with no change to the previously accepted exterior materials.
    r=np.random.default_rng(9137)
    field=np.zeros_like(x)
    for cells,weight in [(3,.50),(7,.25),(15,.13),(31,.07),(63,.035)]:
        grid=r.normal(0,1,(cells,cells))
        gx=x*cells;gy=y*cells
        ix=np.floor(gx).astype(int);iy=np.floor(gy).astype(int)
        fx=gx-ix;fy=gy-iy;fx=fx*fx*(3-2*fx);fy=fy*fy*(3-2*fy)
        layer=(grid[iy%cells,ix%cells]*(1-fx)+grid[iy%cells,(ix+1)%cells]*fx)*(1-fy)+(grid[(iy+1)%cells,ix%cells]*(1-fx)+grid[(iy+1)%cells,(ix+1)%cells]*fx)*fy
        field+=weight*layer
    field=(field-field.mean())/field.std()*.16
    micro=r.normal(0,1,(N,N))
    if kind=='aged_wood':
        warp=.014*np.sin(2*np.pi*y*2)+field*.012
        grain=np.sin(2*np.pi*(x+warp)*110)*.006+np.sin(2*np.pi*(x+warp)*37)*.009
        worn=np.clip((field-.08)*.7,0,.15)
        base=np.array([.405,.355,.285])[None,None,:]+(field*.025+grain+micro*.005)[:,:,None]
        base+=worn[:,:,None]*np.array([.10,.10,.09])
        height=.5+grain*.3+micro*.004
    elif kind=='aged_paint':
        worn=field>.285
        base=np.array([.60,.605,.53])[None,None,:]+(field*.10+micro*.006)[:,:,None]
        base[worn]=np.array([.38,.36,.29])+micro[worn,None]*.008
        height=.6+micro*.007-worn*.09
    elif kind=='aged_plaster':
        base=np.array([.62,.605,.535])[None,None,:]+(field*.045+micro*.005)[:,:,None]
        height=.5+micro*.012
    else:
        base=np.array([.455,.44,.39])[None,None,:]+(field*.032+micro*.007)[:,:,None]
        height=.5+micro*.018
    albedo=image(kind+'_base',base)
    dy,dx=np.gradient(height)
    norm=np.dstack((-dx,-dy,np.ones_like(dx)))
    norm/=np.linalg.norm(norm,axis=2)[:,:,None]
    normal=image(kind+'_normal',norm*.5+.5); normal.colorspace_settings.name='Non-Color'
    return albedo,normal

mats={}
for kind in ['brick','wood','floor','inside','trim','roof','grass']:
    m=bpy.data.materials.new('M3_'+kind); m.use_nodes=True
    nt=m.node_tree; bs=nt.nodes.get('Principled BSDF'); bs.inputs['Roughness'].default_value=.83 if kind!='trim' else .66
    a,n=texture(kind)
    tex=nt.nodes.new('ShaderNodeTexImage'); tex.image=a; nt.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
    tex=nt.nodes.new('ShaderNodeTexImage'); tex.image=n
    norm=nt.nodes.new('ShaderNodeNormalMap'); norm.inputs['Strength'].default_value=.45
    nt.links.new(tex.outputs['Color'],norm.inputs['Color']); nt.links.new(norm.outputs['Normal'],bs.inputs['Normal'])
    mats[kind]=m
for kind in ['aged_wood','aged_paint','aged_plaster','aged_floor']:
    m=bpy.data.materials.new('M3_'+kind);m.use_nodes=True
    nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Roughness'].default_value=.88
    a,n=aged_texture(kind)
    tex=nt.nodes.new('ShaderNodeTexImage');tex.image=a;nt.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
    tex=nt.nodes.new('ShaderNodeTexImage');tex.image=n
    norm=nt.nodes.new('ShaderNodeNormalMap');norm.inputs['Strength'].default_value=.22
    nt.links.new(tex.outputs['Color'],norm.inputs['Color']);nt.links.new(norm.outputs['Normal'],bs.inputs['Normal'])
    mats[kind]=m
def plain(name,color,metal=0,rough=.6):
    m=bpy.data.materials.new('M3_'+name); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*color,1); bs.inputs['Metallic'].default_value=metal; bs.inputs['Roughness'].default_value=rough
    mats[name]=m; return m
plain('iron',(.095,.10,.085),.7,.47)
glass=plain('glass',(.57,.69,.66),.1,.19)
bs=glass.node_tree.nodes.get('Principled BSDF'); bs.inputs['Alpha'].default_value=.16
glass.surface_render_method='DITHERED'
plain('ceramic',(.78,.75,.64),0,.34)
plain('edge_wood',(.26,.225,.165),0,.91)
plain('plaster_patch',(.30,.28,.235),0,.95)
plain('wall_ghost',(.355,.34,.285),0,.95)
plain('hairline',(.25,.245,.215),0,.98)
plain('paper',(.60,.55,.415),0,.95)
bulb=plain('bulb',(.9,.82,.61),0,.3)
bs=bulb.node_tree.nodes.get('Principled BSDF'); bs.inputs['Emission Color'].default_value=(1,.82,.5,1); bs.inputs['Emission Strength'].default_value=2

for o in bpy.data.objects:
    if o.type!='MESH': continue
    old=o.data.materials[0].name if o.data.materials else 'inside'
    kind={'infill':'brick','trunk':'wood','road':'floor','tree':'grass','inside':'aged_plaster'}.get(old,old)
    if o.name.startswith(('D02_','D03_','D04_')):kind='aged_wood'
    o.data.materials.clear(); o.data.materials.append(mats.get(kind,mats['inside']))
    if o.name=='Ground': o.dimensions=(24,32,.22); o.location=(0,8,-.15)

colliders=[]
def collider(o):
    bpy.context.view_layer.update()
    verts=[o.matrix_world@Vector(v) for v in o.bound_box]
    lo=[min(v[i] for v in verts) for i in range(3)]; hi=[max(v[i] for v in verts) for i in range(3)]
    colliders.append({'name':o.name,'min':[lo[0],lo[2],-hi[1]],'max':[hi[0],hi[2],-lo[1]]})
for o in bpy.data.objects:
    if o.type=='MESH' and o.name.startswith(('Side_wall','Front_pier','Display_spandrel','Store_front','Passage_wall','Rear_wall','Canopy_post','Return_base','D02_','D03_','D04_')): collider(o)

def box(name,loc,size,mat='aged_wood',collision=False,parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=size
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mats[mat])
    if parent: o.parent=parent
    if collision: collider(o)
    return o
def rod(name,a,b,r=.015,mat='iron'):
    a,b=Vector(a),Vector(b)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=(b-a).length,location=(a+b)/2)
    o=bpy.context.object; o.name=name; o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); o.data.materials.append(mats[mat]); return o

# Full front room, invented restrained store furnishings.
F=.18
box('Interior_floor_finish',(0,7.65,F+.0015),(6.865,15.06,.003),'aged_floor')
COUNTER_Y=2.80
box('Counter_carcass',(.50,COUNTER_Y,F+.445),(5.20,.66,.89),collision=True)
box('Counter_top',(.50,COUNTER_Y,F+.945),(5.30,.80,.065),collision=True)
box('Counter_plinth',(.50,COUNTER_Y,F+.045),(5.12,.60,.09))
for xx in [-2.07,-1.03,.01,1.05,2.09,3.07]:
    box('Counter_front_stile',(xx,2.452,F+.47),(.055,.04,.80),'aged_paint')
for zz in [.13,.81]:box('Counter_front_rail',(.50,2.452,F+zz),(5.16,.04,.055),'aged_paint')
for xx in [-1.55,-.51,.53,1.57,2.58]:box('Counter_recess_panel',(xx,2.47,F+.47),(.94,.024,.62),'aged_paint')
box('Counter_right_return',(2.86,3.58,F+.445),(.48,.91,.89),collision=True)
box('Counter_return_top',(2.86,3.61,F+.945),(.58,1.02,.065),collision=True)
box('Chair_seat',(2.2,2.88,F+.455),(.46,.45,.045),collision=True)
for xx in [1.995,2.405]:
    for yy in [2.69,3.07]:
        rod('Chair_turned_leg',(xx,yy,F+.025),(xx,yy,F+.46),.022,'wood')
    rod('Chair_back_post',(xx,3.075,F+.38),(xx,3.10,F+.99),.021,'wood')
    rod('Chair_side_stretcher',(xx,2.69,F+.18),(xx,3.07,F+.18),.012,'wood')
for xx in [2.07,2.2,2.33]: box('Chair_back_slat',(xx,3.095,F+.76),(.035,.026,.39))
box('Chair_crest',(2.2,3.1,F+.99),(.47,.05,.08),collision=True)
rod('Chair_cross_stretcher',(1.995,2.9,F+.18),(2.405,2.9,F+.18),.012,'wood')
# Keep the requested empty chair on the serving side of the counter.
for o in bpy.data.objects:
    if o.name.startswith('Chair_'):o.location.y+=.88
for c in colliders:
    if c['name'].startswith('Chair_'):
        c['min'][2]-=.88;c['max'][2]-=.88
for side in [-1,1]:
    for yy in [4.85,7.05]:
        xx=side*3.12
        box('Shelf_back',(xx+side*.235,yy,F+1.02),(.035,1.84,2.04),collision=True)
        for end in [-.92,.92]: box('Shelf_upright',(xx,yy+end,F+1.02),(.46,.055,2.04),collision=True)
        for zz in [.12,.60,1.08,1.56,2.03]: box('Empty_shelf',(xx,yy,F+zz),(.48,1.84,.043),collision=True)
        for zz in [.61,1.09,1.57]: box('Shelf_label_edge',(xx-side*.245,yy,F+zz),(.012,1.81,.035),'trim')
for xx,yy in [(-2.5,8.2),(-1.9,8.25),(2.9,8.35)]:
    box('Crate_base',(xx,yy,F+.035),(.50,.38,.055),collision=True)
    for zz in [.095,.195,.295]:
        for sy in [-1,1]: box('Crate_slat',(xx,yy+sy*.18,F+zz),(.50,.025,.075))
        for sx in [-1,1]: box('Crate_end',(xx+sx*.235,yy,F+zz),(.025,.34,.075))
    # Occupancy envelope: the hollow slats must still stop the walking body.
    colliders.append({'name':'crate','min':[xx-.25,F,-yy-.19],'max':[xx+.25,F+.34,-yy+.19]})
for side in [-1,1]:
    box('Interior_plaster',(side*3.427,4.51,1.67),(.012,8.54,2.98),'aged_plaster')
    box('Skirting',(side*3.407,4.5,F+.07),(.032,8.50,.14),'aged_paint')
    box('Ceiling_cornice',(side*3.395,4.5,3.015),(.06,8.5,.10),'aged_paint')
for yy in [1.85,4.45,7.8]:
    rod('Pendant_cord',(0,yy,3.07),(0,yy,2.70),.008)
    bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=.23,radius2=.075,depth=.15,location=(0,yy,2.66))
    bpy.context.object.name='Pendant_shade'; bpy.context.object.data.materials.append(mats['trim'])
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.066,location=(0,yy,2.58))
    bpy.context.object.name='Pendant_bulb'; bpy.context.object.data.materials.append(mats['bulb'])

# Fine storefront profiles, door muntins and actual moving hardware.
for n in ['D01L_front_hinge','D01R_front_hinge']:
    p=bpy.data.objects[n]
    room_face=1 if n.startswith('D01L') else -1
    # G01: two columns of five tall panes, continuously joined to the stiles.
    # The first pass incorrectly used a short, floating four-light cross.
    for part in list(p.children):
        if part.name.endswith('_rail_1') or part.name.endswith('_lower_panel'):
            bpy.data.objects.remove(part,do_unlink=True)
    pane=bpy.data.objects[n.removesuffix('_hinge')+'_glass']
    pane.location.z=1.10;pane.dimensions=(.56,.025,1.81)
    box('Door_bottom_rail',(.35,0,.14),(.70,.07,.17),'trim',parent=p)
    box('Door_muntin',(.35,0,1.10),(.023,.065,1.81),'trim',parent=p)
    for row in range(1,5):
        zz=.195+row*1.81/5
        box('Door_cross_muntin',(.35,0,zz),(.56,.065,.024),'trim',parent=p)
    # Continuous room-facing glazing stops, aligned with the same pane grid.
    for xx in [.083,.35,.617]:
        box('Door_inner_glazing_stop',(xx,room_face*.039,1.10),(.014,.015,1.81),'aged_paint',parent=p)
    for row in range(6):
        zz=.195+row*1.81/5
        box('Door_inner_cross_stop',(.35,room_face*.039,zz),(.548,.015,.014),'aged_paint',parent=p)
    for face in [-1,1]:box('Door_handle',(.59,face*.070,1.03),(.026,.055,.19),'iron',parent=p)
    for zz in [.22,1.85]: box('Door_hinge',(.015,0,zz),(.035,.10,.095),'iron',parent=p)
for sx in [-1,1]:
    box('Display_sill_nose',(sx*2.17,-.067,.823),(2.02,.22,.075),'trim')
    box('Display_inner_sill',(sx*2.17,.145,.824),(1.98,.36,.065),'aged_paint')
    # Join interior casing to the opening rather than leaving a floating ledge.
    for xx in [sx*1.22,sx*3.12]:
        box('Display_inner_jamb',(xx,.125,1.75),(.075,.28,1.82),'aged_paint')
        box('Display_inner_casing',(xx,.278,1.75),(.11,.035,1.94),'aged_paint')
    box('Display_inner_head',(sx*2.17,.125,2.625),(1.90,.28,.07),'aged_paint')
    box('Display_inner_head_casing',(sx*2.17,.278,2.66),(2.02,.035,.105),'aged_paint')
    box('Display_inner_apron',(sx*2.17,.263,.758),(1.92,.035,.085),'aged_paint')
for xx in np.arange(-3.8,3.9,.19):
    o=box('Canopy_seam',(float(xx),-.73,3.178),(.018,1.45,.014),'trim'); o.rotation_euler.x=.089

# W04: local X follows the 45-degree return; local +Y points outward.
pane=bpy.data.objects['W04_return_pane']
# Inset moving glass from the stationary jambs; M2's full-span placeholder
# intersected the door's hinge stile. The approved outer perimeter is unchanged.
pane.dimensions=(pane.dimensions.x-.13,.016,pane.dimensions.z)
bpy.context.view_layer.objects.active=pane
bpy.ops.object.select_all(action='DESELECT'); pane.select_set(True)
bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
pivot=bpy.data.objects.new('W04_top_hinge',None); scene.collection.objects.link(pivot)
pivot.location=(.8375,.1675,2.265); pivot.rotation_euler.z=math.radians(135)
bpy.context.view_layer.update(); world=pane.matrix_world.copy(); pane.parent=pivot; pane.matrix_world=world
pivot['interaction']='window'; pivot['open_radians']=math.radians(-15)
pane['operable_proposal']='Approved concealed top hinge, 15 degree inward tilt'
box('Window_latch',(0,0,-1.29),(.09,.045,.035),'iron',parent=pivot)
# Slender room-facing stops move with the existing single return pane.
for xx in [-.122,.122]:box('W04_inner_sash_stile',(xx,-.017,-.68),(.018,.022,1.33),'aged_paint',parent=pivot)
for zz in [-.014,-1.346]:box('W04_inner_sash_rail',(0,-.017,zz),(.26,.022,.022),'aged_paint',parent=pivot)
for side in [-1,1]:
    # Continuous angled interior frame, exactly following M2's return plane.
    angle=math.radians(45 if side<0 else 135)
    center=Vector((side*.8375,.1675,0));axis=Vector((math.cos(angle),math.sin(angle),0))
    inward=Vector((side/math.sqrt(2),1/math.sqrt(2),0))
    for along in [-.185,.185]:
        point=center+axis*along+inward*.054
        o=box('Return_inner_casing',(*point[:2],1.585),(.048,.030,1.48),'aged_paint');o.rotation_euler.z=angle
    for zz in [.874,2.295]:
        point=center+inward*.054
        o=box('Return_inner_frame_rail',(*point[:2],zz),(.405,.030,.052),'aged_paint');o.rotation_euler.z=angle
switch=box('Light_switch_plate',(1.088,.268,1.39),(.115,.035,.18),'ceramic')
switch['interaction']='light'
box('Light_switch_toggle',(1.088,.294,1.39),(.026,.028,.06),'iron')['interaction']='light'
# M2's open central passage remains open all the way to the centered rear door.
# Rear storeroom leaves are held in M2's reviewed open pose, with real colliders.
for side in [-1,1]:
    for yy in [9.35,10.35]:box('Storeroom_jamb',(side*.73,yy,1.25),(.052,.062,2.14),'aged_paint')
    box('Storeroom_head',(side*.73,9.85,2.32),(.052,1.08,.072),'aged_paint')
    box('Passage_skirting',(side*.729,12.75,.25),(.03,4.55,.14),'aged_paint')

# Small retained details: construction, fittings and signs of long disuse.
def ribbon(name, points, width, material, surface='wall'):
    verts=[]
    for p in points:
        delta=Vector((0,0,width/2)) if surface=='wall' else Vector((width/2,0,0))
        verts.extend([Vector(p)-delta,Vector(p)+delta])
    faces=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(points)-1)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update()
    o=bpy.data.objects.new(name,mesh);scene.collection.objects.link(o);o.data.materials.append(mats[material]);return o
wear=np.random.default_rng(1229)
for side in [-1,1]:
    for yy,zz in [(1.5,2.78),(3.1,1.85),(6.2,2.82),(8.1,.70)]:
        points=[(side*3.419,yy+i*.065+float(wear.uniform(-.016,.016)),zz-i*.07) for i in range(9)]
        ribbon('Plaster_hairline',points,.0018,'hairline')
    # Former wall-mounted notice left a subtle rectangular finish difference.
    box('Old_notice_ghost',(side*3.418,3.10,1.95),(.001,.47,.58),'wall_ghost')
    for yy,zz,extent in [(1.2,.49,.15),(2.6,2.87,.09),(7.9,2.8,.14)]:
        verts=[]
        for i in range(20):
            angle=i*2*math.pi/20;radius=extent*float(wear.uniform(.50,1))
            verts.append((side*3.418,yy+math.cos(angle)*radius,zz+math.sin(angle)*radius*.7))
        face=tuple(range(20)) if side<0 else tuple(reversed(range(20)))
        mesh=bpy.data.meshes.new('Plaster_paint_loss');mesh.from_pydata(verts,[],[face]);mesh.update()
        patch=bpy.data.objects.new('Plaster_paint_loss',mesh);scene.collection.objects.link(patch);patch.data.materials.append(mats['plaster_patch'])
    for yy in [2.1,6.5]:
        box('Old_outlet_plate',(side*3.397,yy,.49),(.035,.10,.14),'ceramic')
        for zz in [.47,.51]:box('Outlet_slot',(side*3.376,yy,zz),(.008,.032,.008),'iron')
    # Varied chips on interior skirting, showing undercoat rather than debris.
    for _ in range(22):
        yy=float(wear.uniform(.6,8.5));length=float(wear.uniform(.025,.15))
        box('Skirting_paint_loss',(side*3.388,yy,float(wear.uniform(.20,.30))),(.003,length,.006),'edge_wood')
for yy in [2.1,5.8,7.8,11.4]:
    pts=[(-1.8+i*.13+float(wear.uniform(-.025,.025)),yy+float(wear.uniform(-.06,.06)),F+.004) for i in range(13)]
    ribbon('Floor_shrinkage_hairline',pts,.002,'hairline','floor')
for xx in [-1.55,-.51,.53,1.57,2.58]:
    box('Counter_drawer_face',(xx,3.144,.81),(.94,.026,.21),'aged_wood')
    rod('Counter_drawer_pull',(xx-.065,3.18,.82),(xx+.065,3.18,.82),.010,'iron')
    for dx in [-.065,.065]:box('Drawer_pull_mount',(xx+dx,3.164,.82),(.027,.028,.03),'iron')
    box('Counter_lower_cupboard',(xx,3.144,.45),(.94,.026,.40),'aged_wood')
    box('Cupboard_pull',(xx+.32,3.173,.53),(.022,.025,.065),'iron')
for _ in range(30):
    xx=float(wear.uniform(-2.12,3.14));yy=float(wear.choice([2.402,3.198]))
    box('Counter_edge_wear',(xx,yy,1.156),(float(wear.uniform(.015,.065)),.006,.005),'edge_wood')
for side in [-1,1]:
    for yy in [4.85,7.05]:
        for zz in [.80,1.28,1.76]:
            for dy in [-.63,.12,.63]:
                box('Empty_label_holder',(side*2.871,yy+dy,zz),(.006,.13,.036),'iron')
                box('Faded_shelf_label',(side*2.865,yy+dy,zz),(.004,.10,.021),'paper')
        for dy in [-.92,.92]:
            for zz in [.39,2.02]:
                rod('Shelf_fastener',(side*2.878,yy+dy,zz),(side*2.868,yy+dy,zz),.007,'iron')
        for _ in range(10):
            box('Shelf_lip_wear',(side*2.873,yy+float(wear.uniform(-.85,.85)),float(wear.choice([.78,1.26,1.74,2.21]))),(.004,float(wear.uniform(.02,.12)),.006),'edge_wood')
# A stopped wall clock, blank old notices and surface-run electrical conduit.
def disk(name,loc,radius,depth,material):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=radius,depth=depth,location=loc,rotation=(math.pi/2,0,0))
    o=bpy.context.object;o.name=name;o.data.materials.append(mats[material]);return o
disk('Clock_rim',(-1.55,8.757,2.42),.19,.055,'iron')
disk('Clock_face',(-1.55,8.724,2.42),.172,.008,'paper')
for i in range(12):
    a=i*math.pi/6
    rod('Clock_tick',(-1.55+math.sin(a)*.142,8.716,2.42+math.cos(a)*.142),(-1.55+math.sin(a)*.158,8.716,2.42+math.cos(a)*.158),.003,'iron')
rod('Stopped_clock_hour',(-1.55,8.710,2.42),(-1.475,8.710,2.37),.005,'iron')
rod('Stopped_clock_minute',(-1.55,8.706,2.42),(-1.425,8.706,2.397),.003,'iron')
box('Notice_board',(-2.55,8.755,1.70),(.60,.045,.70),'aged_wood')
for xx,zz in [(-2.68,1.79),(-2.42,1.59)]:
    box('Faded_notice',(xx,8.729,zz),(.20,.003,.28),'paper')
    rod('Notice_pin',(xx,8.72,zz+.12),(xx,8.71,zz+.12),.005,'iron')
rod('Switch_conduit',(1.088,.286,1.50),(1.088,.286,2.95),.007,'iron')
for zz in [1.8,2.45,2.9]:box('Conduit_clip',(1.088,.287,zz),(.036,.027,.012),'iron')

# Relocate fittings with the revised partitions; extend the passage skirting
# to the same rear endpoint instead of leaving a gap at the new doorway.
for o in bpy.data.objects:
    if o.name.startswith(('Storeroom_jamb','Storeroom_head','Clock_','Stopped_clock_','Notice_board','Faded_notice','Notice_pin')):
        o.location.y+=STORE_SHIFT
    elif o.name.startswith('Passage_skirting'):
        o.location.y+=STORE_SHIFT/2;o.dimensions.y-=STORE_SHIFT

# Sparse, recognizable traces of a produce shop where customers were served.
# These fittings and prices are invented set dressing, not historical evidence.
plain('scale_enamel',(.265,.315,.275),.15,.67)
plain('dull_tin',(.40,.415,.38),.65,.55)
plain('chalkboard',(.105,.125,.105),0,.97)
plain('faded_chalk',(.49,.495,.415),0,.99)

def lettering(name,body,loc,size,material='faded_chalk'):
    curve=bpy.data.curves.new(name,'FONT');curve.body=body;curve.size=size
    curve.align_x='CENTER';curve.space_character=1.1;curve.resolution_u=3
    o=bpy.data.objects.new(name,curve);scene.collection.objects.link(o)
    o.location=loc;o.rotation_euler.x=math.pi/2;o.data.materials.append(mats[material])
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
    bpy.ops.object.convert(target='MESH');return bpy.context.object

# Mechanical countertop scale with a dial, needle, feet and shallow metal pan.
sx,sy=.95,2.79
for dx in [-.17,.17]:
    for dy in [-.12,.12]:box('Scale_foot',(sx+dx,sy+dy,1.177),(.055,.055,.033),'iron')
box('Scale_base',(sx,sy,1.221),(.46,.36,.07),'scale_enamel')
box('Scale_column',(sx,sy+.035,1.40),(.19,.18,.31),'scale_enamel')
disk('Scale_dial_housing',(sx,sy-.07,1.465),.185,.20,'scale_enamel')
disk('Scale_dial_bezel',(sx,sy-.177,1.465),.174,.023,'dull_tin')
disk('Scale_dial_face',(sx,sy-.192,1.465),.158,.008,'paper')
for i in range(41):
    a=math.radians(-135+i*270/40)
    inner=.124 if i%5==0 else .135
    rod('Scale_dial_tick',(sx+math.sin(a)*inner,sy-.20,1.465+math.cos(a)*inner),(sx+math.sin(a)*.146,sy-.20,1.465+math.cos(a)*.146),.0017,'iron')
for i in range(5):
    a=math.radians(-135+i*67.5)
    lettering('Scale_numeral',str(i*5),(sx+math.sin(a)*.106,sy-.203,1.452+math.cos(a)*.106),.025,'iron')
lettering('Scale_units','LB',(sx,sy-.203,1.414),.022,'iron')
rod('Scale_needle',(sx+.012,sy-.21,1.45),(sx-.073,sy-.21,1.373),.0025,'iron')
rod('Scale_pan_stem',(sx,sy+.035,1.50),(sx,sy+.035,1.70),.027,'dull_tin')
box('Scale_pan',(sx,sy+.025,1.706),(.53,.39,.018),'dull_tin')
for dx in [-.26,.26]:box('Scale_pan_rim',(sx+dx,sy+.025,1.74),(.015,.39,.065),'dull_tin')
for dy in [-.165,.215]:box('Scale_pan_rim',(sx,sy+dy,1.74),(.53,.015,.065),'dull_tin')

# Three empty slatted produce compartments on a low bench behind the counter.
for xx in [-2.30,-1.55,-.80]:
    for dx in [-.29,.29]:
        for yy in [4.58,5.10]:box('Produce_bench_leg',(xx+dx,yy,.53),(.045,.045,.70),'aged_wood')
    box('Produce_bin_occupancy',(xx,4.84,.77),(.73,.65,.14),'aged_wood',collision=True)
    for j in range(6):box('Produce_bin_floor_slat',(xx-.30+j*.12,4.84,.852),(.106,.64,.024),'aged_wood')
    for zz in [.91,1.015,1.12]:
        box('Produce_bin_back_slat',(xx,5.16,zz),(.73,.023,.079),'aged_wood')
        for dx in [-.365,.365]:box('Produce_bin_end_slat',(xx+dx,4.84,zz),(.025,.65,.079),'aged_wood')
    box('Produce_bin_front',(xx,4.51,.93),(.73,.026,.14),'aged_wood')
    for dx in [-.30,.30]:
        rod('Produce_bin_nail',(xx+dx,4.493,.93),(xx+dx,4.484,.93),.006,'iron')
    box('Produce_bin_label',(xx,4.489,.94),(.29,.005,.082),'chalkboard')
for xx,label in [(-2.30,'BEANS'),(-1.55,'PEACHES'),(-.80,'TOMATOES')]:
    lettering('Bin_name',label,(xx,4.484,.922),.039)
box('Produce_price_board',(1.83,5.727,2.15),(1.72,.035,.91),'chalkboard')
for xx in [.94,2.72]:box('Price_board_frame',(xx,5.714,2.15),(.055,.052,1.01),'aged_wood')
for zz in [1.67,2.63]:box('Price_board_frame',(1.83,5.714,zz),(1.83,.052,.055),'aged_wood')
lettering('Produce_board_title','LOCAL PRODUCE',(1.83,5.705,2.44),.12)
for zz,label in [(2.23,'BEANS        35c / lb'),(2.04,'PEACHES      50c / lb'),(1.85,'TOMATOES     40c / lb')]:
    lettering('Old_chalk_price',label,(1.83,5.705,zz),.080)

# A few flattened paper bags and a resting pencil; otherwise the counter is bare.
for i in range(7):
    box('Folded_paper_bag',(-.60+i*.003,2.87,1.164+i*.003),(.29,.40,.002),'paper')
box('Bag_fold',(-.60,3.025,1.186),(.28,.024,.005),'paper')
rod('Counter_pencil',(-.24,2.89,1.170),(-.12,2.94,1.170),.003,'edge_wood')

# World-scaled box UVs: one brick tile is 1.84 x 1.20 m (230 x 75 mm courses).
bpy.context.view_layer.update()
for o in bpy.data.objects:
    if o.type!='MESH': continue
    mesh=o.data; uv=mesh.uv_layers.active or mesh.uv_layers.new(name='UVMap')
    kind=o.data.materials[0].name.removeprefix('M3_')
    offset=(float(wear.uniform(0,1)),float(wear.uniform(0,1))) if kind in {'aged_wood','aged_paint'} else (0,0)
    su,sv=(1.84,1.20) if kind=='brick' else ((.65,2.5) if kind in {'wood','aged_wood'} else ((3.5,3.0) if kind=='aged_plaster' else (2,2)))
    for poly in mesh.polygons:
        normal=o.matrix_world.to_3x3()@poly.normal
        axis=max(range(3),key=lambda i:abs(normal[i]))
        axes=(1,2) if axis==0 else ((0,2) if axis==1 else (0,1))
        for li in poly.loop_indices:
            v=o.matrix_world@mesh.vertices[mesh.loops[li].vertex_index].co
            uv.data[li].uv=(v[axes[0]]/su+offset[0],v[axes[1]]/sv+offset[1])
    # Small rounded edges survive export; limited to detailed pieces.
    if not o.name.startswith(('Ground','Floor','Side_wall','Flat_ceiling','Low_slope','Parapet','Front_','Display_spandrel','Display_lintel','Rear_wall','Store_front','Passage_wall')):
        mod=o.modifiers.new('Soft worn edges','BEVEL'); mod.width=.004; mod.segments=1
        bpy.context.view_layer.objects.active=o
        bpy.ops.object.modifier_apply(modifier=mod.name)

# Preserve moving hierarchies while batching the new glazing stops by material.
for parent in [o for o in bpy.data.objects if o.type=='EMPTY' and o.name.startswith('D01')]:
    batches={}
    for child in parent.children:
        if child.type=='MESH':batches.setdefault(child.data.materials[0].name,[]).append(child)
    for material,children in batches.items():
        if len(children)<2:continue
        bpy.ops.object.select_all(action='DESELECT')
        for child in children:child.select_set(True)
        bpy.context.view_layer.objects.active=children[0];bpy.ops.object.join()
        children[0].name=parent.name+'_parts_'+material
# Preserve pivot trees and switch objects, combine static pieces by material.
groups={}
for o in list(bpy.data.objects):
    if o.type=='MESH' and not o.parent and 'interaction' not in o:
        groups.setdefault(o.data.materials[0].name,[]).append(o)
for name,objs in groups.items():
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs:o.select_set(True)
    bpy.context.view_layer.objects.active=objs[0]; bpy.ops.object.join(); objs[0].name='Static_'+name
scene.render.engine='CYCLES'; scene.cycles.samples=32
scene['milestone']='M3 revision 3: shallow customer area, produce service counter, closer storerooms; rear detail remains context.'
scene['provenance']='Original deterministic procedural PBR textures and invented furniture; approved M2 shell and pane mechanism.'
for im in bpy.data.images:
    if im.source=='FILE': im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/myrtle-beach-v2-sample.blend'))
bpy.ops.export_scene.gltf(filepath=str(ASSETS/'sample.glb'),export_format='GLB',export_animations=False,export_extras=True,export_cameras=False,export_lights=False)
manifest={'schema':1,'coordinates':'glTF: X right, Y up, -Z toward rear; meters','colliders':colliders,'spawn':[0,1.72,3.1], 'walkerRadius':.25,'eyeHeight':1.65,'windowOpenRadians':-math.pi/12,'pendantDepths':[1.85,4.45,7.8],'layout':{'storeFront':STORE_FRONT,'storeDoorCenter':6.85,'counterCustomerEdge':2.40,'counterAccessCenterX':-2.78},'source':'model/myrtle-beach-v2-sample.blend','provenance':'M2 exterior shell; M3 revised service-shop layout, original procedural materials and invented produce-shop fittings.'}
(ASSETS/'sample.json').write_text(json.dumps(manifest,indent=2))
triangles=sum(len(p.vertices)-2 for o in bpy.data.objects if o.type=='MESH' for p in o.data.polygons)
texture_count=sum(1 for m in mats.values() for n in m.node_tree.nodes if n.type=='TEX_IMAGE')
report={'revision':3,'triangles':triangles,'meshObjects':sum(o.type=='MESH' for o in bpy.data.objects),'materials':len(mats),'textureCount':texture_count,'textureDimensions':[N,N],'estimatedTextureMiBWithMipmaps':texture_count*N*N*4*4/3/1024**2,'glbBytes':(ASSETS/'sample.glb').stat().st_size,'colliders':len(colliders)}
(ROOT/'planning/m3-review/asset-report.json').write_text(json.dumps(report,indent=2))
print('M3_EXPORT_COMPLETE',json.dumps(report))
