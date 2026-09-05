"""Construction contact checks and an independent ray audit of saved geometry."""
import bpy,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

def bounds(o):
    verts=[o.matrix_world@Vector(v) for v in o.bound_box]
    return ([min(v[i] for v in verts) for i in range(3)],[max(v[i] for v in verts) for i in range(3)])

def audit_construction(root):
    bpy.context.view_layer.update()
    support_prefixes=('Interior_plaster','Side_wall','Rear_wall','Store_front','Passage_wall','Store_door_head')
    supports=[(o,bounds(o)) for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(support_prefixes)]
    prefixes=('Skirting','Ceiling_cornice','Passage_skirting','Passage_short_skirting','Partition_room_','Partition_short_skirting','Rear_room_','Store_rear_baseboard','Room_nameplate','Rear_switch_','Old_outlet_plate','Crate_tally_board','Packing_wall_rail','Rear_wall_ghost','Old_fixing','Vent_louvre','High_vent_louvre','Downpipe_strap')
    checks=[]
    for o in bpy.data.objects:
        if o.type!='MESH' or not o.name.startswith(prefixes) or 'toggle' in o.name:continue
        lo,hi=bounds(o)
        contacts=[]
        for other,(a,b) in supports:
            if other==o:continue
            overlap=[min(hi[i],b[i])-max(lo[i],a[i]) for i in range(3)]
            if min(overlap)>.0002:contacts.append({'name':other.name,'overlap':overlap})
        checks.append({'name':o.name,'passes':bool(contacts),'bounds':[lo,hi],'wallContacts':contacts})
        if 'cornice' in o.name:
            checks.append({'name':o.name+' ceiling joint','passes':hi[2]>=3.085,'top':hi[2]})
    for o in bpy.data.objects:
        if o.type=='MESH' and o.name.startswith(('Closed_right_infill','Infill_perimeter')):
            lo,hi=bounds(o)
            checks.append({'name':o.name+' masonry face','passes':lo[0]<3.675 and hi[0]<=3.677,'projectionMeters':hi[0]-3.675})
    assert not any(o.name.startswith('Skirting_paint_loss') for o in bpy.data.objects)
    report={'checks':checks,'failed':[c for c in checks if not c['passes']], 'scope':'Unbeveled construction bounds must penetrate supporting wall surfaces; trim must meet ceiling; right infill projects at most 2 mm. Saved-mesh ray audit is separate.'}
    out=root/'planning/m4-adversarial';out.mkdir(exist_ok=True)
    (out/'construction-audit.json').write_text(json.dumps(report,indent=2))
    assert not report['failed'],str(report['failed'])
    print('CONSTRUCTION_AUDIT_PASS',len(checks),flush=True)

def audit_saved(root):
    bpy.ops.wm.open_mainfile(filepath=str(root/'model/myrtle-beach-v2-complete.blend'))
    bpy.context.view_layer.update()
    wall_names={'M3_aged_plaster','M3_brick'}
    walls=[]
    all_mesh=[]
    for o in bpy.data.objects:
        if o.type!='MESH':continue
        tree=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])
        all_mesh.append(tree)
        if o.data.materials and o.data.materials[0].name in wall_names:walls.append(tree)
    failed=[];count=0
    def probe(label,point,axis,distance,trees=walls):
        nonlocal count
        count+=1
        if not any(t.ray_cast(Vector(point),Vector(axis),distance)[0] is not None for t in trees):failed.append({'label':label,'point':point,'direction':axis})
    for k in range(85):
        y=5.84+k*.109
        for z in [.185,.205,.30,1.40,2.40,3.065]:
            if 6.29<y<7.41 and z<2.30:continue
            for s in [-1,1]:probe('passage wall',(0,y,z),(s,0,0),.89)
    for k in range(135):
        y=.28+k*.109
        for z in [.185,.26,1.4,2.85,3.065]:
            for s in [-1,1]:probe('outer wall interior',(s*3.1,y,z),(s,0,0),.6)
    # Check actual wall backing immediately behind the saved fixture faces.
    for point,axis in [((.710,14.30,1.4),(1,0,0)),((-2.12,5.958,1.4),(0,-1,0)),((2.12,5.958,1.4),(0,-1,0)),((-2.2,15.038,1.75),(0,1,0))]:
        probe('switch backing',point,axis,.055)
    for x in [-2.1,0,2.1]:
        for k in range(50):probe('continuous floor',(x,.4+k*.285,.3),(0,0,-1),.15,all_mesh)
    # Doorway must have no opaque switch suspended in the clear portal.
    portal_blocked=[]
    for x in [-.3,0,.3]:
        for z in [1.25,1.4,1.55]:
            origin=Vector((x,14.8,z));direction=Vector((0,1,0))
            if any(t.ray_cast(origin,direction,.6)[0] is not None for t in all_mesh):portal_blocked.append([x,z])
    report={'wallFloorAndBackingRays':count,'misses':failed,'portalObstructions':portal_blocked,'scope':'Actual saved mesh rays along floor/wall seams, all opaque passage runs (excluding deliberate door openings), side-wall interiors, switch supports and the clear rear portal. Sampling cannot prove every triangle is defect-free.'}
    (root/'planning/m4-adversarial/mesh-audit.json').write_text(json.dumps(report,indent=2))
    assert not failed and not portal_blocked,str(report)
    print('SAVED_MESH_AUDIT_PASS',count,flush=True)

if __name__=='__main__':audit_saved(Path(__file__).resolve().parents[1])
