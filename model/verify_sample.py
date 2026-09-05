"""Check the exported source's moving window against the paired door mesh sweep."""
import bpy, json, math
from pathlib import Path
from mathutils.bvhtree import BVHTree
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'model/myrtle-beach-v2-sample.blend'))
pane=bpy.data.objects['W04_return_pane']; window=bpy.data.objects['W04_top_hinge']
doors=[bpy.data.objects[n] for n in ['D01L_front_hinge','D01R_front_hinge']]
def tree(o):
    return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])
collisions=[]
for w in range(16):
    window.rotation_euler.x=math.radians(-w)
    for d in range(20):
        doors[0].rotation_euler.z=math.radians(d*5)
        doors[1].rotation_euler.z=math.radians(180-d*5)
        bpy.context.view_layer.update()
        for moving in window.children:
            if moving.type!='MESH':continue
            pt=tree(moving)
            for door in doors:
                for part in door.children:
                    if part.type=='MESH' and pt.overlap(tree(part)):
                        collisions.append({'windowDegrees':w,'doorDegrees':d*5,'windowPart':moving.name,'object':part.name})
# Ray-check the actual opaque trim: every pane center is clear and each divider
# meets the vertical grid, from both exterior and interior faces.
grid_checks=[]
for i,door in enumerate(doors):
    door.rotation_euler.z=0 if i==0 else math.pi
    bpy.context.view_layer.update()
    opaque=[tree(o) for o in door.children if o.type=='MESH' and o.data.materials[0].name!='M3_glass']
    for direction in [-1,1]:
        def hit(px,pz):
            start=door.matrix_world@Vector((px,-direction*.30,pz));axis=door.matrix_world.to_3x3()@Vector((0,direction,0))
            return any(t.ray_cast(start,axis,.6)[0] is not None for t in opaque)
        for row in range(5):
            z=.195+(row+.5)*1.81/5
            for px in [.21,.49]:grid_checks.append(not hit(px,z))
            grid_checks.append(hit(.35,z))
        for row in range(1,5):
            for px in [.21,.35,.49]:grid_checks.append(hit(px,.195+row*1.81/5))
report={'windowDoorSweepSamples':320,'meshIntersections':collisions,'windowInwardTiltDegrees':15,'glazingGridRayChecks':len(grid_checks),'glazingGridRayFailures':grid_checks.count(False),'scope':'Moving pane, sash stops and latch versus both detailed door leaves at 1 degree window / 5 degree door intervals; actual opaque grid checked from both faces. Discrete mesh checks, not a continuous engineering clearance guarantee.'}
(ROOT/'planning/m3-review/window-clearance.json').write_text(json.dumps(report,indent=2))
print(json.dumps({**report,'meshIntersections':collisions[:8],'intersectionCount':len(collisions)}))
assert not collisions
assert all(grid_checks)
