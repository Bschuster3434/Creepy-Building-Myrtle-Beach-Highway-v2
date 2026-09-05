"""Read V1 scene and export inspection artifacts into V2; never save the blend."""
import bpy
import json
import hashlib
from pathlib import Path
from mathutils import Vector

OUT = Path(__file__).resolve().parent / 'v1-inspection'
OUT.mkdir(exist_ok=True)
source = Path(bpy.data.filepath)
digest = hashlib.sha256(source.read_bytes()).hexdigest()
items = []
for obj in bpy.context.scene.objects:
    bounds = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    items.append(dict(name=obj.name, type=obj.type, location=list(obj.matrix_world.translation),
        dimensions=list(obj.dimensions), parent=obj.parent.name if obj.parent else None,
        hidden_render=obj.hide_render,
        bounds_min=[min(v[i] for v in bounds) for i in range(3)],
        bounds_max=[max(v[i] for v in bounds) for i in range(3)]))
(OUT / 'scene-inventory.json').write_text(json.dumps(dict(source=str(source), sha256=digest,
    units=bpy.context.scene.unit_settings.system, objects=items), indent=2), encoding='utf-8')
for item in items:
    if any(word in item['name'].lower() for word in ['chair', 'counter', 'interior', 'room', 'partition', 'door', 'shelf']):
        print(json.dumps(item))
print('INSPECTION_DONE', len(items), digest)

# Temporary cutaway of the loaded V1 scene, with no source save.
scene = bpy.context.scene
for obj in scene.objects:
    name = obj.name.lower()
    keep = obj.type == 'MESH' and any(name.startswith(p) for p in (
        'wall_', 'interior_', 'front_entry_', 'rear_service_', 'alcove_wall_',
        'front_left_', 'front_right_', 'door_alcove_'))
    if 'ceiling' in name:
        keep = False
    obj.hide_render = not keep
scene.render.engine = 'BLENDER_WORKBENCH'
scene.display.shading.light = 'STUDIO'
scene.display.shading.color_type = 'SINGLE'
scene.display.shading.single_color = (0.72, 0.75, 0.77)
scene.display.shading.show_shadows = True
scene.display.shading.show_cavity = True
scene.display.shading.cavity_type = 'BOTH'
scene.display.shading.background_type = 'WORLD'
scene.world.color = (0.9, 0.9, 0.9)
scene.render.resolution_x = 1000
scene.render.resolution_y = 1300
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
camera_data = bpy.data.cameras.new('V2_Inspection_Camera')
camera = bpy.data.objects.new('V2_Inspection_Camera', camera_data)
scene.collection.objects.link(camera)
scene.camera = camera
camera.location = (0, 0, 25)
camera.rotation_euler = (0, 0, 0)
camera_data.type = 'ORTHO'
camera_data.ortho_scale = 18
scene.render.filepath = str(OUT / 'v1-top-cutaway.png')
bpy.ops.render.render(write_still=True)
camera.location = (0, -6.1, 1.65)
camera.rotation_euler = (Vector((0, 1.5, 1.5)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
camera_data.type = 'PERSP'
camera_data.lens = 20
scene.render.resolution_x = 1400
scene.render.resolution_y = 900
scene.render.filepath = str(OUT / 'v1-entry-cutaway.png')
bpy.ops.render.render(write_still=True)
assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
print('V1_SOURCE_HASH_UNCHANGED')
