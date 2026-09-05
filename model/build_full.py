"""Complete scene with M5 interaction data. Reuse the approved M3 recipe.
Run with Blender --background --python-exit-code 1 --python model/build_full.py.
M2/M3 blend files, exports and their generator remain unchanged.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
recipe = (ROOT/'model/build_sample.py').read_text()
prefix, finish = recipe.split('# World-scaled box UVs:', 1)
prefix = prefix.replace("'model/sample-textures'", "'model/full-textures'")
exec(compile(prefix, str(ROOT/'model/build_sample.py'), 'exec'))
print('M4: approved sample constructed',flush=True)
REVIEW=ROOT/'planning/m5-review'
REVIEW.mkdir(parents=True,exist_ok=True)
original_names=set(o.name for o in bpy.data.objects)
# Replace the three M3 rear-context crates with the furnished room arrangement.
for o in list(bpy.data.objects):
    if o.name.startswith(('Crate_base','Crate_slat','Crate_end')):bpy.data.objects.remove(o,do_unlink=True)
colliders[:]=[c for c in colliders if c['name']!='crate' and not c['name'].startswith('Crate_base')]
plain('asphalt',(.145,.151,.143),0,.96)
plain('road_white',(.64,.63,.53),0,.96)
plain('road_yellow',(.59,.43,.12),0,.96)
plain('bark',(.235,.205,.155),0,.96)
plain('gravel',(.38,.36,.30),0,.96)
for i,c in enumerate([(.18,.245,.105),(.25,.30,.13),(.31,.335,.155),(.36,.345,.18)]):
    plain('leaf'+str(i),c,0,.9)
    mats['leaf'+str(i)].use_backface_culling=False

# Architectural finish beds into its supporting wall and overlaps the ceiling.
# Do not stretch the similarly named paint-loss decals into full-length strips.
for o in list(bpy.data.objects):
    if o.name.startswith('Skirting_paint_loss'):
        bpy.data.objects.remove(o,do_unlink=True);continue
    side=1 if o.location.x>0 else -1
    if o.name.startswith('Interior_plaster'):
        o.location.x=side*3.430;o.location.y=7.65;o.dimensions=(.020,14.832,2.98)
    elif o.name=='Skirting' or o.name.startswith('Skirting.'):
        o.location=(side*3.406,7.65,.25);o.dimensions=(.036,14.832,.150)
        o.data.materials[0]=mats['trim']
    elif o.name.startswith('Ceiling_cornice'):
        o.location=(side*3.397,7.65,3.04);o.dimensions=(.055,14.832,.10)
        o.data.materials[0]=mats['trim']
    elif o.name.startswith('Passage_skirting'):
        o.location=(side*.738,11.2215,.25);o.dimensions=(.034,7.689,.15)
        o.data.materials[0]=mats['trim']
    elif o.name.startswith('Old_outlet_plate'):
        o.location.x=side*3.408
    elif o.name.startswith('Outlet_slot'):
        o.location.x=side*3.3885
    elif o.name.startswith('Closed_right_infill'):
        # These are filled masonry openings, not raised panels or fixtures.
        o.location.x=3.672;o.dimensions.x=.008
for side in [-1,1]:
    box('Rear_room_cornice',(side*2.146,15.043,3.04),(2.556,.044,.10),'trim')
    box('Rear_room_baseboard',(side*2.146,15.044,.25),(2.556,.044,.15),'trim')
    box('Partition_room_skirting',(side*.882,11.2215,.25),(.034,7.689,.15),'trim')
    box('Partition_short_skirting',(side*.882,6.1185,.25),(.034,.409,.15),'trim')
    box('Passage_short_skirting',(side*.738,6.0585,.25),(.034,.529,.15),'trim')
    box('Partition_room_cornice',(side*.887,10.49,3.04),(.044,9.152,.10),'trim')
    box('Store_rear_baseboard',(side*2.146,5.932,.25),(2.556,.035,.15),'trim')
    # Nameplates face the passage; room functions are imagined.
    plate=box('Room_nameplate',(side*.738,6.85,2.56),(.030,.56,.19),'aged_wood')
    text=lettering('Room_label','CRATES' if side<0 else 'PACKING',(side*.721,6.85,2.52),.082)
    text.rotation_euler.z=math.pi/2 if side<0 else -math.pi/2
    for yy in [9.9,13.7]:
        # Quiet plaster ghosts and fixing holes, not rubble or damp damage.
        box('Rear_wall_ghost',(side*3.4195,yy,1.60),(.003,.62,.38),'wall_ghost')
        for dz in [-.17,.17]:box('Old_fixing',(side*3.419,yy-.25,1.6+dz),(.008,.009,.009),'iron')

def crate(name,x,y,z,scale=1):
    w,d,h=.64*scale,.46*scale,.39*scale
    for k in range(5):box(name+'_bottom',(x-w*.4+k*w*.2,y,z+.02),(w*.17,d,.035),'aged_wood')
    for zz in [.09,.21,.33]:
        for sy in [-1,1]:box(name+'_long_slat',(x,y+sy*d/2,z+zz*scale),(w,.024,.083*scale),'aged_wood')
        for sx in [-1,1]:box(name+'_end',(x+sx*w/2,y,z+zz*scale),(.026,d,.083*scale),'aged_wood')
    for sx in [-1,1]:
        for sy in [-1,1]:box(name+'_corner',(x+sx*(w/2-.022),y+sy*(d/2-.022),z+h/2),(.032,.032,h),'aged_wood')
    colliders.append({'name':name,'min':[x-w/2,F,-y-d/2],'max':[x+w/2,z+h,-y+d/2]})

def rack(name,x,y,length=2.1):
    for dy in [-length/2,length/2]:
        for dx in [-.24,.24]:box(name+'_post',(x+dx,y+dy,1.28),(.055,.055,2.2),'aged_wood')
    for z in [.33,.96,1.59,2.28]:
        for dx in [-.19,-.06,.07,.20]:box(name+'_shelf',(x+dx,y,z),(.115,length,.036),'aged_wood')
        box(name+'_lip',(x+.265,y,z+.018),(.035,length,.07),'aged_paint')
    rod(name+'_brace',(x-.25,y-length/2,.30),(x-.25,y+length/2,2.32),.017,'iron')
    colliders.append({'name':name,'min':[x-.29,F,-y-length/2-.04],'max':[x+.29,2.4,-y+length/2+.04]})

# Left: retained crate shelving and nested empty boxes, open central aisle.
for yy in [10.2,12.75]:rack('Crate_rack',-3.08,yy)
for xx,yy,zz in [(-3.07,9.65,.978),(-3.07,10.4,.348),(-3.07,12.2,.348),(-3.07,13.15,1.608),(-1.48,14.34,.183),(-1.48,14.34,.573),(-2.28,14.34,.183)]:
    crate('Retained_crate',xx,yy,zz,.8 if xx<-2.9 else 1)
box('Crate_tally_board',(-2.2,15.052,1.75),(.68,.025,.5),'chalkboard')
lettering('Crate_tally','EMPTIES',(-2.2,15.038,1.84),.084)
lettering('Crate_marks','||||  ||||',(-2.2,15.038,1.66),.067)

# Right: long packing bench, paper roll, twine, empty sorting trays, hand truck.
for yy in [9.65,11.55]:
    for xx in [2.61,3.22]:box('Packing_bench_leg',(xx,yy,.63),(.075,.075,.90),'aged_wood')
box('Packing_bench_top',(2.92,10.6,1.12),(.78,2.18,.075),'aged_wood',True)
box('Packing_lower_shelf',(2.92,10.6,.43),(.66,2.10,.045),'aged_wood')
rod('Bench_back_rail',(3.25,9.55,.51),(3.25,11.65,.51),.025,'aged_wood')
rod('Paper_roll_axle',(2.63,11.25,1.37),(3.20,11.25,1.37),.027,'iron')
rod('Paper_roll',(2.69,11.25,1.37),(3.14,11.25,1.37),.13,'paper')
for xx in [2.63,3.20]:rod('Roll_stand',(xx,11.25,1.16),(xx,11.25,1.39),.019)
box('Unrolled_paper',(2.92,10.93,1.16),(.44,.40,.003),'paper')
rod('Twine_spool',(2.91,10.14,1.16),(2.91,10.14,1.35),.065,'paper')
for zz in [1.16,1.35]:
    bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.09,depth=.013,location=(2.91,10.14,zz))
    bpy.context.object.data.materials.append(mats['aged_wood']);bpy.context.object.name='Spool_end'
for i in range(3):crate('Packing_tray',2.96,12.65,.183+i*(.39*.72),.72)
box('Packing_wall_rail',(3.405,10.6,1.94),(.035,2.15,.12),'aged_wood')
for yy in [9.85,10.22,10.59]:rod('Retained_hook',(3.38,yy,1.95),(3.29,yy,1.90),.012)
for xx in [1.48,1.93]:
    rod('Handtruck_frame',(xx,14.5,.43),(xx,14.7,1.56),.024)
    rod('Handtruck_handle',(xx,14.7,1.56),(xx,14.59,1.68),.024)
    rod('Handtruck_wheel',(xx-.045,14.47,.37),(xx+.045,14.47,.37),.15,'iron')
for zz in [.60,.98,1.35]:rod('Handtruck_crossbar',(1.48,14.53+(zz-.6)*.18,zz),(1.93,14.53+(zz-.6)*.18,zz),.018)
box('Handtruck_toe',(1.705,14.29,.25),(.54,.39,.05),'dull_tin',True)
for o in bpy.data.objects:
    if o.name.startswith('Handtruck_'):o.location.z-=.037
bpy.data.objects['Handtruck_toe'].location.z-=.005
colliders[:]=[c for c in colliders if not c['name'].startswith('Handtruck_')]
colliders.append({'name':'Handtruck_occupancy','min':[1.40,F,-14.78],'max':[2.01,1.67,-14.09]})

# Rear openings: complete hardware with named pivots ready for M5.
for name in ['D02_left_store_hinge','D03_right_store_hinge','D04_rear_hinge']:
    p=bpy.data.objects[name];p['interaction_ready']='door';w=p['clear_opening_m']
    for side in [-1,1]:
        for z in [.20,1.04,1.92]:box('Door_cross_rail',(w/2,side*.026,z),(w-.08,.02,.09),'aged_wood',parent=p)
        for xx in [.06,w-.06]:box('Door_edge_stile',(xx,side*.027,1.05),(.07,.021,2.02),'aged_wood',parent=p)
        box('Door_lock_plate',(w-.14,side*.046,1.04),(.065,.026,.17),'iron',parent=p)
        box('Door_lever',(w-.19,side*.067,1.06),(.16,.035,.028),'dull_tin',parent=p)
    for z in [.25,1.77]:box('Door_hinge_barrel',(0,0,z),(.05,.075,.12),'iron',parent=p)
# Hold rear door open for M4 room/site inspection, as the storeroom doors are.
rear=bpy.data.objects['D04_rear_hinge'];rear.rotation_euler.z=rear['open_angle']
colliders[:]=[c for c in colliders if not c['name'].startswith('D04_')]
bpy.context.view_layer.update()
for o in rear.children:
    if o.type=='MESH':collider(o)
for xx in [-.56,.56]:box('Rear_door_jamb',(xx,15.16,1.26),(.085,.27,2.18),'aged_paint')
box('Rear_door_header',(0,15.16,2.36),(1.20,.27,.085),'aged_paint')
box('Rear_threshold',(0,15.22,.19),(1.10,.33,.035),'dull_tin')
box('Rear_landing',(0,15.98,.09),(1.8,1.40,.18),'floor')
box('Rear_step',(0,16.87,.045),(1.8,.38,.09),'floor')

fixtures=[]
for name,xx,yy in [('Crates',-2.12,10.6),('Packing',2.12,10.6),('Rear_passage',0,12.4)]:
    rod('Rear_conduit',(xx,yy,3.09),(xx,yy,2.81),.011,'iron')
    box('Rear_fixture_'+name,(xx,yy,2.78),(.38,.19,.09),'ceramic')['fixture_id']=name
    box('Rear_bulb_'+name,(xx,yy,2.721),(.27,.12,.028),'bulb')['fixture_id']=name
    fixtures.append({'id':name,'position':[xx,2.68,-yy],'intensity':11,'distance':7})
    switch_pos=(xx,5.932,1.4) if xx else (.738,14.30,1.4)
    switch_size=(.11,.035,.18) if xx else (.035,.11,.18)
    sw=box('Rear_switch_'+name,switch_pos,switch_size,'ceramic')
    sw['interaction_ready']='light';sw['fixture_id']=name
    box('Rear_switch_toggle_'+name,(xx,5.958,1.4) if xx else (.710,14.30,1.4),(.025,.025,.055),'iron')

# Exterior: construction details follow existing openings and silhouette.
for side in [-1,1]:
    for yy in [3,7.4,12.9]:
        for zz in [.265,.30,.335,.37]:box('Vent_louvre',(side*3.684,yy,zz),(.028,.28,.015),'iron')
    for yy in [.6]:
        for zz in [2.78,2.83,2.88,2.93]:box('High_vent_louvre',(side*3.684,yy,zz),(.026,.21,.014),'iron')
    box('Rear_fascia',(side*1.82,15.325,3.57),(3.61,.05,.14),'trim')
    rod('Rear_downpipe',(side*3.48,15.36,.30),(side*3.48,15.36,3.61),.039,'dull_tin')
    for zz in [.65,2.7]:box('Downpipe_strap',(side*3.48,15.36,zz),(.12,.14,.025),'iron')
rod('Rear_gutter',(-3.62,15.37,3.65),(3.62,15.37,3.65),.07,'dull_tin')
box('Chimney_flue',(3.335,10.6,4.458),(.31,.43,.016),'iron')
for yy,zz,ww,hh in [(5.15,1.88,1.55,1.10),(9.25,1.52,1.15,2.1),(12,1.55,1.05,2.05)]:
    for dy in [-ww/2,ww/2]:box('Infill_perimeter',(3.674,yy+dy,zz),(.005,.009,hh),'wall_ghost')
    for z in [zz-hh/2,zz+hh/2]:box('Infill_perimeter',(3.674,yy,z),(.005,ww,.009),'wall_ghost')
for xx in [-3.79,-.43,3.79]:
    box('Canopy_base_plate',(xx,-1.45,.08),(.16,.16,.019),'iron')
    for dx in [-.054,.054]:box('Post_anchor',(xx+dx,-1.45,.10),(.019,.027,.024),'dull_tin')

# The immediate site retains the M2 contextual positions (not survey claims).
ground=bpy.data.objects['Ground'];ground.dimensions=(130,130,.22);ground.location=(0,6,-.11)
box('Side_service_strip',(-4.68,8,.024),(1.75,16,.048),'gravel')
box('Right_verge_path',(4.63,7.65,.024),(1.70,15.30,.048),'gravel')
box('Rear_service_yard',(0,18.2,.025),(11,5.6,.05),'gravel')
box('Road_apron_connection',(0,-5.18,.018),(9.35,1.02,.036),'gravel')
for yy in [-9,-23]:
    box('Highway_carriageway',(0,yy,.004),(120,7,.028),'asphalt')
    for edge in [-3.40,3.40]:box('Highway_edge',(0,yy+edge,.020),(120,.10,.006),'road_white' if edge>0 else 'road_yellow')
    for xx in range(-57,58,9):box('Highway_lane_dash',(xx,yy,.021),(3,.10,.006),'road_white')
# Sparse apron seams: maintained hardstanding with slight age.
for xx in [-2.8,0,2.8]:box('Apron_joint',(xx,-2.65,.072),(.009,3.9,.003),'wall_ghost')
box('Apron_cross_joint',(0,-2.5,.072),(9.32,.009,.003),'wall_ghost')

# Neighboring agricultural outbuilding: siding, pitched roof, corners and door.
box('Neighbor_siding',(-20,16,2.25),(12,14,4.5),'trim',True)
for side in [-1,1]:
    slope=box('Neighbor_roof',(-20+side*3.15,16,5.15),(6.5,14.65,.09),'roof')
    slope.rotation_euler.y=side*math.radians(12)
    for yy in np.arange(8.8,23.3,.45):
        seam=box('Neighbor_roof_seam',(-20+side*3.15,float(yy),5.21),(6.5,.023,.025),'dull_tin');seam.rotation_euler.y=side*math.radians(12)
    for yy in [9.0,23.0]:box('Neighbor_corner',(-20+side*6.025,yy,2.25),(.09,.13,4.5),'trim')
    for yy in np.arange(9.15,23,.40):box('Neighbor_side_batten',(-20+side*6.010,float(yy),2.25),(.035,.040,4.4),'trim')
for xx in np.arange(-25.8,-14,.25):box('Neighbor_front_batten',(float(xx),8.976,2.25),(.036,.035,4.4),'trim')
for yy in [9,23]:
    me=bpy.data.meshes.new('Neighbor_gable');me.from_pydata([(-26,yy,4.5),(-14,yy,4.5),(-20,yy,5.80)],[],[(0,1,2) if yy==9 else (2,1,0)]);me.update()
    ob=bpy.data.objects.new('Neighbor_gable',me);scene.collection.objects.link(ob);ob.data.materials.append(mats['trim'])
box('Neighbor_sliding_door',(-20,8.91,1.70),(3.1,.09,3.4),'aged_wood')
box('Neighbor_door_track',(-20,8.80,3.54),(6.35,.065,.07),'iron')
for xx in [-21.52,-18.48]:box('Neighbor_door_stile',(xx,8.845,1.70),(.08,.065,3.4),'trim')

# Branching broadleaf trees with individually shaped, clustered leaves.
# No opaque low-poly crown placeholders; all foliage is original geometry.
leafverts=[[] for _ in range(4)];leaffaces=[[] for _ in range(4)]
forest=np.random.default_rng(4404)
tree_positions=[(-7,4,8,3.1),(-7.5,13,10,3.6),(7,13,9,3.0),(2,21,11,3.5),(-3,26,12,4.1),(11,23,10,3.5),(-12,28,11,3.8),(18,31,11,4.1)]
for ti,(tx,ty,h,r) in enumerate(tree_positions):
    trunk=rod('Tree_trunk', (tx,ty,0),(tx+.15,ty-.12,h*.67),.19 if h<10 else .24,'bark');collider(trunk)
    for branch in range(14):
        a=branch*2.399+ti;reach=r*float(forest.uniform(.48,1))
        end=Vector((tx+math.cos(a)*reach,ty+math.sin(a)*reach,h*float(forest.uniform(.64,.98))))
        base=Vector((tx+.10,ty-.08,h*float(forest.uniform(.40,.64))))
        rod('Tree_branch',base,end,.047,'bark')
        for k in range(450):
            v=forest.normal(0,1,3);v/=np.linalg.norm(v)
            center=end+Vector(v*float(forest.random()**(1/3))*np.array([r*.45,r*.45,h*.145]))
            angle=float(forest.uniform(0,math.tau));length=float(forest.uniform(.15,.27));width=length*.47
            axis=Vector((math.cos(angle),math.sin(angle),float(forest.uniform(-.7,.7)))).normalized()*length
            across=axis.cross(Vector((.1,.2,1))).normalized()*width
            mi=int(forest.choice(4,p=[.30,.36,.28,.06]));vs=leafverts[mi];fs=leaffaces[mi];i=len(vs)
            vs.extend([center-axis,center-across,center+Vector((0,0,.025)),center+across,center+axis])
            fs.extend([(i,i+1,i+2),(i,i+2,i+3),(i+1,i+4,i+2),(i+2,i+4,i+3)])
for i in range(4):
    me=bpy.data.meshes.new('Leaf_geometry');me.from_pydata(leafverts[i],[],leaffaces[i]);me.update()
    ob=bpy.data.objects.new('Foliage_'+str(i),me);scene.collection.objects.link(ob);ob.data.materials.append(mats['leaf'+str(i)])

# Low cut grass clumps at verge and field edges; keep paths and building clear.
verts=[];faces=[]
for k in range(7500):
    xx=float(forest.uniform(-38,38));yy=float(forest.uniform(-28,43))
    if (-27<yy<-19.4) or (-12.6<yy<-5.5) or (abs(xx)<5.7 and -5.7<yy<21.1) or (-26.5<xx<-13.5 and 8.5<yy<23.5):continue
    height=float(forest.uniform(.035,.15));angle=float(forest.uniform(0,math.tau))
    for a in [angle,angle+1.6]:
        dx,dy=math.cos(a)*.02,math.sin(a)*.02;i=len(verts)
        verts.extend([(xx-dx,yy-dy,.005),(xx+dx,yy+dy,.005),(xx+dx*.4,yy+dy*.4,height)])
        faces.append((i,i+1,i+2))
me=bpy.data.meshes.new('Cut_grass');me.from_pydata(verts,[],faces);me.update()
ob=bpy.data.objects.new('Verge_grass',me);scene.collection.objects.link(ob);ob.data.materials.append(mats['leaf2'])

# Utility detail remains in M2's contextual location, clear of the path.
rod('Utility_pole',(6.3,4,0),(6.3,4,9.8),.12,'bark')
box('Utility_crossarm',(6.3,4,8.9),(.13,1.8,.13),'aged_wood')
for dx in [-.7,0,.7]:
    rod('Pole_insulator',(6.3,4+dx,8.96),(6.3,4+dx,9.22),.055,'ceramic')
    for a,b in [(-32,6.3),(6.3,40)]:
        for j in range(12):
            u=j/12;v=(j+1)/12
            rod('Overhead_wire',(a+(b-a)*u,4+dx,9.22-.8*4*u*(1-u)),(a+(b-a)*v,4+dx,9.22-.8*4*v*(1-v)),.009,'iron')
for xx in [-32,40]:
    rod('Context_pole',(xx,4,0),(xx,4,9.8),.12,'bark')
    box('Context_crossarm',(xx,4,8.9),(.13,1.8,.13),'aged_wood')
    for dx in [-.7,0,.7]:rod('Context_insulator',(xx,4+dx,8.96),(xx,4+dx,9.22),.055,'ceramic')
colliders.append({'name':'Utility_pole','min':[6.16,0,-4.14],'max':[6.44,9.8,-3.86]})

# Save semantic construction inventory before render batching.
import sys
sys.path.insert(0,str(ROOT/'model'))
from audit_full import audit_construction
audit_construction(ROOT)
inventory=[{'name':o.name,'material':o.data.materials[0].name,'parent':o.parent.name if o.parent else None} for o in bpy.data.objects if o.type=='MESH']
(REVIEW/'construction-inventory.json').write_text(json.dumps(inventory,indent=2))
print('M4: full construction ready; applying finish and batching',len(inventory),flush=True)
from walkthrough_data import prepare as prepare_walkthrough
interactive_doors=prepare_walkthrough(colliders)
# Reuse the accepted UV and batching pipeline; skip edge bevels on foliage.
finish=finish.split("scene.render.engine='CYCLES'",1)[0]
finish=finish.replace("if not o.name.startswith(('Ground'", "if not o.name.startswith(('Foliage','Verge_grass','Overhead_wire','Ground'")
exec(compile('# World-scaled box UVs:'+finish, str(ROOT/'model/build_sample.py'), 'exec'))
import sys
sys.path.insert(0,str(ROOT/'model'))
from full_scene_finish import apply as apply_material_finish
apply_material_finish(ROOT)
scene['milestone']='M5: complete interactive walkthrough'
scene['provenance']='M1/M2 researched shell and site relationships; approved M3 service shop; inferred exterior fittings and invented rear furnishings, neighboring finish and vegetation.'
scene.render.engine='CYCLES';scene.cycles.samples=32
scene.world.use_nodes=True
scene.world.node_tree.nodes.get('Background').inputs[0].default_value=(.65,.73,.80,1)
scene.world.node_tree.nodes.get('Background').inputs[1].default_value=.55
ld=bpy.data.lights.new('M4_afternoon_sun','SUN');ld.energy=2.4;ld.angle=math.radians(5)
lo=bpy.data.objects.new('M4_afternoon_sun',ld);scene.collection.objects.link(lo)
lo.rotation_euler=(math.radians(28),math.radians(-25),math.radians(-25))
for title,loc,target in [('Front',(9,-12,3.2),(0,5,1.7)),('Crates',(-2.1,8.4,1.83),(-2.4,13,1.3)),('Packing',(1.9,8.4,1.83),(2.7,12,1.3)),('Rear',(6,21,2.7),(0,13,1.5))]:
    cd=bpy.data.cameras.new('Review_'+title);co=bpy.data.objects.new('Review_'+title,cd);scene.collection.objects.link(co)
    co.location=loc;co.rotation_euler=(Vector(target)-co.location).to_track_quat('-Z','Y').to_euler();cd.lens=25
    if title=='Front':scene.camera=co
scene.render.resolution_x=1600;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
for im in bpy.data.images:
    if im.source=='FILE':im.pack()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/myrtle-beach-v2-complete.blend'))
bpy.ops.export_scene.gltf(filepath=str(ASSETS/'complete.glb'),export_format='GLB',export_animations=False,export_extras=True,export_cameras=False,export_lights=False,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=10,export_draco_texcoord_quantization=14)
manifest={'schema':2,'milestone':'M4','coordinates':'glTF: X right, Y up, -Z toward rear; meters','colliders':colliders,'spawn':[0,1.72,3.1],'walkerRadius':.25,'eyeHeight':1.65,'windowOpenRadians':-math.pi/12,'pendantDepths':[1.85,4.45,7.8],'fixtures':fixtures,'layout':{'storeFront':STORE_FRONT,'storeDoorCenter':6.85,'counterCustomerEdge':2.40,'counterAccessCenterX':-2.78},'source':'model/myrtle-beach-v2-complete.blend','bounds':{'minX':-11,'maxX':11,'minZ':-22,'maxZ':5.35},'rooms':['sales','crate storage','packing','rear passage'],'provenance':scene['provenance'],'preparedDoors':['D02_left_store_hinge','D03_right_store_hinge','D04_rear_hinge']}
manifest.update({'schema':3,'milestone':'M5','doors':interactive_doors,
                 'circuits':['light','cratesLight','packingLight','passage']})
(ASSETS/'complete.json').write_text(json.dumps(manifest,indent=2))
triangles=sum(len(p.vertices)-2 for o in bpy.data.objects if o.type=='MESH' for p in o.data.polygons)
textures={n.image.name:n.image for m in mats.values() for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image}
report={'milestone':'M5','triangles':triangles,'meshObjects':sum(o.type=='MESH' for o in bpy.data.objects),'materials':len(mats),'textureCount':len(textures),'estimatedTextureMiBWithMipmaps':sum(im.size[0]*im.size[1]*4*4/3 for im in textures.values())/1024**2,'glbBytes':(ASSETS/'complete.glb').stat().st_size,'colliders':len(colliders),'constructionObjects':len(inventory),'trees':len(tree_positions),'rooms':manifest['rooms']}
(REVIEW/'asset-report.json').write_text(json.dumps(report,indent=2))
print('M5_EXPORT_COMPLETE',json.dumps(report))
