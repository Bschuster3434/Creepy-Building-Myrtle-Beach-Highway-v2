"""Preserve M5 controls before batching; export render/physics pivot data together."""
import math
import bpy


def prepare(colliders):
    definitions = []
    names = [('D01L_front_hinge', 'door', 'front doors'),
             ('D01R_front_hinge', 'door', 'front doors'),
             ('D02_left_store_hinge', 'cratesDoor', 'crate storeroom door'),
             ('D03_right_store_hinge', 'packingDoor', 'packing room door'),
             ('D04_rear_hinge', 'rearDoor', 'rear door')]
    moving_names = set()
    for name, control, label in names:
        pivot = bpy.data.objects[name]
        pivot['interaction'] = control
        moving_names.update(o.name for o in pivot.children_recursive)
        closed = pivot['closed_angle']
        swing = (pivot['open_angle'] - closed + math.pi) % (2 * math.pi) - math.pi
        definitions.append({'name': name, 'control': control, 'label': label,
                            'hinge': [pivot.location.x, -pivot.location.y],
                            'width': pivot['clear_opening_m'], 'closedAngle': closed,
                            'swingAngle': swing, 'restAngle': pivot.rotation_euler.z,
                            'halfThickness': .04 if control == 'door' else .085})
    colliders[:] = [c for c in colliders if c['name'] not in moving_names]
    for obj in bpy.data.objects:
        if obj.name.startswith('Pendant_bulb'):
            obj['interaction'] = 'bulb'
            obj['circuit'] = 'passage' if obj.location.y > 5.8 else 'light'
        elif obj.name.startswith('Light_switch'):
            obj['interaction'] = 'light'
            obj['circuit'] = 'light'
        for fixture, circuit in [('Crates', 'cratesLight'), ('Packing', 'packingLight'), ('Rear_passage', 'passage')]:
            if obj.name in ['Rear_switch_' + fixture, 'Rear_switch_toggle_' + fixture]:
                obj['interaction'] = circuit
                obj['circuit'] = circuit
            if obj.name == 'Rear_bulb_' + fixture:
                obj['interaction'] = 'bulb'
                obj['circuit'] = circuit
    return definitions
