"""Shared final material pass for the M4 generator and incremental polish."""
import bpy
import numpy as np

def apply(root):
    rng=np.random.default_rng(94397)
    n=512;y,x=np.mgrid[0:n,0:n]/n
    folder=root/'model/full-textures';folder.mkdir(exist_ok=True)
    for name,color,strength in [('asphalt',(.145,.151,.143),.018),('gravel',(.38,.36,.30),.035),('bark',(.23,.20,.155),.023)]:
        mat=bpy.data.materials['M3_'+name];nt=mat.node_tree;bs=nt.nodes.get('Principled BSDF')
        noise=rng.normal(0,1,(n,n))*strength
        if name=='bark':noise+=np.sin(x*2*np.pi*37+np.sin(y*2*np.pi*3)*.65)*.035
        else:noise+=np.sin(x*2*np.pi*5)*np.cos(y*2*np.pi*7)*.006
        data=np.ones((n,n,4),dtype=np.float32);data[:,:,:3]=np.clip(np.array(color)[None,None,:]+noise[:,:,None],0,1)
        im=bpy.data.images.get('M4_'+name+'_base') or bpy.data.images.new('M4_'+name+'_base',width=n,height=n)
        im.pixels.foreach_set(data.ravel());im.filepath_raw=str(folder/(im.name+'.png'));im.file_format='PNG';im.save();im.pack()
        tex=nt.nodes.get('M4_surface') or nt.nodes.new('ShaderNodeTexImage');tex.name='M4_surface';tex.image=im
        nt.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
    # Broader lawn variation avoids conspicuous short-repeat ground tiling.
    for ob in bpy.data.objects:
        if ob.type=='MESH' and ob.name=='Static_M3_grass' and not ob.get('M4_ground_uv'):
            for loop in ob.data.uv_layers.active.data:loop.uv/=4
            ob['M4_ground_uv']=True
    # Smooth branch normals retain the modeled silhouette without faceted shading.
    for ob in bpy.data.objects:
        if ob.type=='MESH' and ob.data.materials and ob.data.materials[0].name=='M3_bark':
            for poly in ob.data.polygons:poly.use_smooth=True

if __name__=='__main__':
    from pathlib import Path
    import json
    root=Path(__file__).resolve().parents[1]
    bpy.ops.wm.open_mainfile(filepath=str(root/'model/myrtle-beach-v2-complete.blend'))
    apply(root)
    bpy.ops.wm.save_as_mainfile(filepath=str(root/'model/myrtle-beach-v2-complete.blend'))
    out=root/'app/public/assets/complete.glb'
    bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',export_animations=False,export_extras=True,export_cameras=False,export_lights=False,export_draco_mesh_compression_enable=True,export_draco_mesh_compression_level=6,export_draco_position_quantization=16,export_draco_normal_quantization=10,export_draco_texcoord_quantization=14)
    path=root/'planning/m4-review/asset-report.json';report=json.loads(path.read_text());report['glbBytes']=out.stat().st_size;report['textureCount']=25;report['estimatedTextureMiBWithMipmaps']=25*512*512*4*4/3/1024**2
    path.write_text(json.dumps(report,indent=2));print('M4_FINISH_COMPLETE',json.dumps(report))
