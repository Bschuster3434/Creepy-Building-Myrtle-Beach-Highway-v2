import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { move, floorHeight, canSwing, blocked } from './physics.js';

export async function createWorld(host, callbacks) {
  const start=performance.now();
  const scene=new THREE.Scene();
  scene.background=new THREE.Color('#c8cfc8');
  scene.fog=new THREE.Fog('#c8cfc8',35,95);
  const walkCamera=new THREE.PerspectiveCamera(66,1,.045,130);
  let camera=walkCamera,mode='walk';
  camera.rotation.order='YXZ';
  const renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'high-performance'});
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));
  renderer.shadowMap.enabled=true; renderer.shadowMap.type=THREE.PCFSoftShadowMap;
  renderer.info.autoReset=false;
  renderer.toneMapping=THREE.ACESFilmicToneMapping; renderer.toneMappingExposure=1.05;
  host.appendChild(renderer.domElement);
  renderer.domElement.tabIndex=0;
  renderer.domElement.setAttribute('aria-label','Store view. W and S move forward and back; A and D or left and right arrows step sideways.');
  const draco=new DRACOLoader().setDecoderPath('/draco/').setWorkerLimit(2);
  const [gltf,manifest]=await Promise.all([
    new GLTFLoader().setDRACOLoader(draco).loadAsync('/assets/complete.glb'),
    fetch('/assets/complete.json').then(r=>{if(!r.ok)throw new Error('Scene manifest could not load.');return r.json();}),
  ]).finally(()=>draco.dispose());
  let disposed=false,locked=false,windowAmount=0,windowTarget=0,dragFallback=false,capturePending=false;
  let currentTarget=null,dragging=false,lastX=0,lastY=0,inspection=false,dragPointer=null;
  const keys=new Set(),ray=new THREE.Raycaster(),center=new THREE.Vector2();
  const circuits=Object.fromEntries(manifest.circuits.map(id=>[id,{on:false,lights:[],bulbs:[],switches:[]}]));
  const selectable=[];
  gltf.scene.traverse(o=>{
    if(!o.isMesh)return;
    o.castShadow=true;o.receiveShadow=true;
    const materials=Array.isArray(o.material)?o.material:[o.material];
    materials.forEach(m=>{
      if(m.map)m.map.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
      if(m.name==='M3_glass') {m.transparent=true;m.opacity=.17;m.depthWrite=false;o.castShadow=false;}
      if(m.name.startsWith('M3_leaf'))m.side=THREE.DoubleSide;
    });
    if(o.userData.interaction==='bulb'){
      o.material=o.material.clone();o.material.emissiveIntensity=0;
      circuits[o.userData.circuit].bulbs.push(o.material);
    }
    if(circuits[o.userData.interaction]){
      o.material=o.material.clone();
      circuits[o.userData.interaction].switches.push(o.material);
    }
    selectable.push(o);
  });
  scene.add(gltf.scene);
  const left=gltf.scene.getObjectByName('D01L_front_hinge'),right=gltf.scene.getObjectByName('D01R_front_hinge');
  const windowPivot=gltf.scene.getObjectByName('W04_top_hinge');
  if(!left||!right||!windowPivot)throw new Error('Interactive pivots missing from sample asset.');
  const windowQ=windowPivot.quaternion.clone();
  const doors=manifest.doors.map(d=>{
    const pivot=gltf.scene.getObjectByName(d.name);
    if(!pivot)throw new Error(`Door pivot missing: ${d.name}`);
    return {...d,pivot,rest:pivot.quaternion.clone(),amount:0,target:0};
  });
  const doorState=()=>doors.map(({pivot,rest,...d})=>d);
  const state=()=>({door:!!doors[0].target,window:!!windowTarget,light:circuits.light.on,
    ...Object.fromEntries(doors.map(d=>[d.control,!!d.target])),
    ...Object.fromEntries(Object.entries(circuits).map(([id,c])=>[id,c.on]))});
  const axisY=new THREE.Vector3(0,1,0),axisX=new THREE.Vector3(1,0,0),rotation=new THREE.Quaternion();
  function poseDoors(){for(const d of doors)d.pivot.quaternion.copy(d.rest).multiply(rotation.setFromAxisAngle(axisY,d.closedAngle+d.swingAngle*d.amount-d.restAngle));}
  poseDoors();
  // Reserve the pane's full opening envelope so it never tilts through the body.
  // The low sill alone does not cover the inward projection near the latch.
  const windowEnvelope=new THREE.Box3();
  for(let step=0;step<=15;step++){
    windowPivot.quaternion.copy(windowQ).multiply(rotation.setFromAxisAngle(axisX,-step*Math.PI/180));
    scene.updateMatrixWorld(true);windowEnvelope.union(new THREE.Box3().setFromObject(windowPivot));
  }
  windowPivot.quaternion.copy(windowQ);scene.updateMatrixWorld(true);
  windowEnvelope.expandByScalar(.005);
  const windowClearance={name:'W04_operating_clearance',min:windowEnvelope.min.toArray(),max:windowEnvelope.max.toArray()};
  manifest.colliders.push(windowClearance);
  scene.add(new THREE.HemisphereLight('#d9e5f0','#80725b',1.65));
  const sun=new THREE.DirectionalLight('#fff0d3',3.2);
  sun.position.set(-3,8,6);sun.target.position.set(1,0,-5);sun.castShadow=true;
  sun.shadow.mapSize.set(2048,2048);sun.shadow.camera.left=-12;sun.shadow.camera.right=12;
  sun.shadow.camera.top=12;sun.shadow.camera.bottom=-12;sun.shadow.camera.near=.1;sun.shadow.camera.far=32;
  sun.shadow.bias=-.00015;sun.shadow.normalBias=.025;
  scene.add(sun,sun.target);
  // Low-cost daylight bounce approximation; only the sun casts shadows.
  const bounce=new THREE.PointLight('#d8e5ec',5,10,2);bounce.position.set(0,2.25,-.9);scene.add(bounce);
  for(const depth of manifest.pendantDepths) {
    const z=-depth;
    const light=new THREE.PointLight('#ffd8a0',0,5.5,2);light.position.set(0,2.50,z);scene.add(light);
    circuits[depth>5.8?'passage':'light'].lights.push({light,intensity:14});
  }
  for(const fixture of manifest.fixtures??[]) {
    const light=new THREE.PointLight('#ffd8a0',0,fixture.distance,2);
    light.position.fromArray(fixture.position);scene.add(light);
    circuits[{Crates:'cratesLight',Packing:'packingLight',Rear_passage:'passage'}[fixture.id]].lights.push({light,intensity:fixture.intensity});
  }
  const orbitCamera=new THREE.PerspectiveCamera(50,1,.1,180);
  orbitCamera.position.set(22,18,25);
  const topCamera=new THREE.OrthographicCamera(-25,25,25,-25,.1,180);
  topCamera.up.set(0,0,-1);topCamera.position.set(0,55,-8);
  const orbit=new OrbitControls(orbitCamera,renderer.domElement),top=new OrbitControls(topCamera,renderer.domElement);
  orbit.target.set(0,1,-7.65);orbit.minDistance=15;orbit.maxDistance=65;
  orbit.minPolarAngle=.12;orbit.maxPolarAngle=Math.PI/2-.07;orbit.enablePan=false;
  orbit.enableDamping=true;orbit.dampingFactor=.12;orbit.rotateSpeed=-.7;
  orbit.mouseButtons.RIGHT=THREE.MOUSE.ROTATE;
  let wheelTurn=0,wheelZoom=0;
  top.target.set(0,0,-8);top.cursor.copy(top.target);top.maxTargetRadius=20;
  top.enableRotate=false;top.screenSpacePanning=true;top.minZoom=.65;top.maxZoom=4;
  top.mouseButtons.LEFT=THREE.MOUSE.PAN;
  orbit.update();top.update();orbit.enabled=false;top.enabled=false;
  function stopOrbitMotion(){
    wheelTurn=0;wheelZoom=0;
    const position=orbitCamera.position.clone(),quaternion=orbitCamera.quaternion.clone();
    orbit.enableDamping=false;orbit.update();
    orbitCamera.position.copy(position);orbitCamera.quaternion.copy(quaternion);orbit.update();
    orbit.enableDamping=true;
  }
  function requestMouseLook(){
    if(mode!=='walk'||locked||capturePending)return;
    capturePending=true;dragFallback=false;callbacks.fallback?.(false);
    // Request synchronously inside the activating click/key; awaiting first loses activation.
    try{Promise.resolve(renderer.domElement.requestPointerLock()).catch(captureFailed).finally(()=>{capturePending=false;});}
    catch{capturePending=false;captureFailed();}
  }
  function setMode(next,{capture=false}={}){
    if(!['walk','orbit','top'].includes(next))return;
    clear();inspection=false;
    if(next!=='walk'&&document.pointerLockElement===renderer.domElement)document.exitPointerLock();
    mode=next;camera=mode==='walk'?walkCamera:mode==='orbit'?orbitCamera:topCamera;
    orbit.enabled=mode==='orbit';top.enabled=mode==='top';
    callbacks.start();callbacks.mode?.(mode);currentTarget=null;callbacks.target(null);
    renderer.domElement.focus({preventScroll:true});
    if(next==='walk'&&capture)requestMouseLook();
  }
  const reset=()=>{setMode('walk',{capture:true});walkCamera.position.fromArray(manifest.spawn);walkCamera.rotation.set(-.02,0,0);};
  walkCamera.position.fromArray(manifest.spawn);walkCamera.rotation.set(-.02,0,0);
  const resize=()=>{const w=host.clientWidth,h=host.clientHeight;renderer.setSize(w,h);
    for(const c of [walkCamera,orbitCamera]){c.aspect=w/h;c.updateProjectionMatrix();}
    topCamera.left=-25*w/h;topCamera.right=25*w/h;topCamera.updateProjectionMatrix();};
  const observer=new ResizeObserver(resize);observer.observe(host);resize();
  function targetAtAim() {
    if(mode!=='walk'||inspection)return null;
    ray.setFromCamera(center,camera);ray.far=2.4;
    for(const hit of ray.intersectObjects(selectable,false)) {
      let o=hit.object;
      while(o){
        if(o===windowPivot)return 'window';
        if(doors.some(d=>d.control===o.userData.interaction)||circuits[o.userData.interaction])return o.userData.interaction;
        o=o.parent;
      }
      // Glass remains a physical visual occluder for use; no operating through walls.
      return null;
    }
    return null;
  }
  function operate(target=currentTarget) {
    if(mode!=='walk')return false;
    const group=doors.filter(d=>d.control===target);
    if(group.length) {
      const next=group[0].target?0:1;
      if(group.some(d=>!canSwing(d.amount,next,walkCamera.position,d))){callbacks.message('Step clear of the door swing.');return false;}
      group.forEach(d=>d.target=next);
    } else if(target==='window') windowTarget=windowTarget?0:1;
    else if(circuits[target]) {
      const c=circuits[target];c.on=!c.on;
      c.lights.forEach(({light,intensity})=>light.intensity=c.on?intensity:0);
      c.bulbs.forEach(m=>m.emissiveIntensity=c.on?3:0);
      c.switches.forEach(m=>{m.emissive.set('#f3cb78');m.emissiveIntensity=c.on?.28:0;});
    }
    else return false;
    callbacks.state(state());return true;
  }
  const onKey=e=>{
    // Release held keys even when focus changes between keydown and keyup.
    if(e.type==='keyup'){keys.delete(e.code);return;}
    if(e.code==='Escape'){clear();if(document.pointerLockElement===renderer.domElement)document.exitPointerLock();return;}
    if(e.target instanceof HTMLElement && (e.target.isContentEditable || ['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)))return;
    if(['Digit1','Digit2','Digit3'].includes(e.code)&&!e.repeat){e.preventDefault();setMode({Digit1:'walk',Digit2:'orbit',Digit3:'top'}[e.code],{capture:true});return;}
    if(mode!=='walk')return;
    if(!['KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight','KeyE'].includes(e.code))return;
    // Ordinary UI buttons must not swallow walking controls after a click.
    e.preventDefault();keys.add(e.code);
    if(e.code==='KeyE'&&!e.repeat)operate();
  };
  const look=(dx,dy)=>{
    camera.rotation.y-=dx*.002;camera.rotation.x=THREE.MathUtils.clamp(camera.rotation.x-dy*.002,-1.4,1.4);
  };
  const onMouse=e=>{if(locked&&mode==='walk')look(e.movementX,e.movementY);};
  let dragDistance=0;
  const up=(e)=>{
    const click=e?.type==='pointerup'&&dragging&&dragDistance<5&&mode==='walk';
    dragging=false;renderer.domElement.classList.remove('dragging');
    if(dragPointer!==null&&renderer.domElement.hasPointerCapture(dragPointer))renderer.domElement.releasePointerCapture(dragPointer);
    dragPointer=null;
    if(click){currentTarget=targetAtAim();operate();}
  };
  const clear=()=>{keys.clear();up();if(mode==='orbit')stopOrbitMotion();};
  const onLock=()=>{
    locked=document.pointerLockElement===renderer.domElement;
    // Ignore a late successful request if the user already switched to inspection.
    if(locked&&mode!=='walk'){document.exitPointerLock();return;}
    if(locked){dragFallback=false;callbacks.fallback?.(false);}
    clear();callbacks.lock(locked);
  };
  const captureFailed=()=>{if(mode!=='walk')return;dragFallback=true;callbacks.fallback?.(true);callbacks.message('Mouse capture is unavailable here. Hold the left mouse button and drag to look; W / A / S / D still walk.');};
  const down=e=>{
    if(e.button!==0||mode!=='walk')return;
    renderer.domElement.focus({preventScroll:true});
    if(locked){operate();return;}
    if(!dragFallback){callbacks.start();requestMouseLook();e.preventDefault();return;}
    callbacks.start();dragging=true;dragDistance=0;lastX=e.clientX;lastY=e.clientY;dragPointer=e.pointerId;
    renderer.domElement.setPointerCapture(e.pointerId);renderer.domElement.classList.add('dragging');e.preventDefault();
  };
  const drag=e=>{
    if(locked||!dragging||e.pointerId!==dragPointer)return;
    dragDistance+=Math.hypot(e.clientX-lastX,e.clientY-lastY);
    look(e.clientX-lastX,e.clientY-lastY);lastX=e.clientX;lastY=e.clientY;
  };
  window.addEventListener('keydown',onKey);window.addEventListener('keyup',onKey);
  window.addEventListener('mousemove',onMouse);window.addEventListener('blur',clear);
  document.addEventListener('visibilitychange',clear);document.addEventListener('pointerlockchange',onLock);
  document.addEventListener('pointerlockerror',captureFailed);
  renderer.domElement.addEventListener('pointerdown',down);renderer.domElement.addEventListener('pointermove',drag);
  renderer.domElement.addEventListener('pointerup',up);renderer.domElement.addEventListener('pointercancel',up);renderer.domElement.addEventListener('lostpointercapture',up);
  const inspectKey=e=>{
    if(mode==='walk'||e.type!=='keydown'||e.target?.isContentEditable||['INPUT','TEXTAREA','SELECT'].includes(e.target?.tagName))return;
    if(['Equal','NumpadAdd','Minus','NumpadSubtract','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.code)||(mode==='orbit'&&['KeyA','KeyD','KeyW','KeyS'].includes(e.code))){
      e.preventDefault();keys.add(e.code);
    }
  };
  const orbitWheel=e=>{
    if(mode!=='orbit')return;
    // Capture before OrbitControls: its wheel handler only understands deltaY.
    // Handle both axes once, without requiring pointer capture or a button press.
    e.preventDefault();e.stopImmediatePropagation();
    const unit=e.deltaMode===1?16:e.deltaMode===2?host.clientHeight:1;
    const dx=e.shiftKey&&e.deltaX===0?e.deltaY:e.deltaX;
    const dy=e.shiftKey&&e.deltaX===0?0:e.deltaY;
    wheelTurn+=dx*unit*.003;
    wheelZoom=THREE.MathUtils.clamp(wheelZoom-dy*unit*.002,-2,2);
  };
  renderer.domElement.addEventListener('wheel',orbitWheel,{capture:true,passive:false});
  function updateInspection(dt){
    const horizontal=(keys.has('ArrowLeft')?1:0)-(keys.has('ArrowRight')?1:0);
    const vertical=(keys.has('ArrowUp')?1:0)-(keys.has('ArrowDown')?1:0);
    const zoom=(keys.has('Equal')||keys.has('NumpadAdd')?1:0)-(keys.has('Minus')||keys.has('NumpadSubtract')?1:0);
    if(mode==='orbit'){
      const turn=(keys.has('KeyD')||keys.has('ArrowRight')?1:0)-(keys.has('KeyA')||keys.has('ArrowLeft')?1:0);
      const dolly=zoom+(keys.has('KeyW')||keys.has('ArrowUp')?1:0)-(keys.has('KeyS')||keys.has('ArrowDown')?1:0);
      const easing=1-Math.exp(-20*dt),scrollTurn=wheelTurn*easing,scrollZoom=wheelZoom*easing;
      wheelTurn-=scrollTurn;wheelZoom-=scrollZoom;
      if(Math.abs(wheelTurn)<.00001)wheelTurn=0;
      if(Math.abs(wheelZoom)<.00001)wheelZoom=0;
      if(turn||dolly||scrollTurn||scrollZoom){
        const spherical=new THREE.Spherical().setFromVector3(orbitCamera.position.clone().sub(orbit.target));
        spherical.theta+=turn*dt+scrollTurn;
        spherical.radius=THREE.MathUtils.clamp(spherical.radius*Math.exp(-dolly*dt-scrollZoom),orbit.minDistance,orbit.maxDistance);
        orbitCamera.position.copy(orbit.target).add(new THREE.Vector3().setFromSpherical(spherical));
      }
      orbit.update(dt);
    }else if(mode==='top'&&(horizontal||vertical||zoom)){
      const delta=new THREE.Vector3(-horizontal,0,-vertical).multiplyScalar(8*dt/topCamera.zoom);
      top.target.add(delta);topCamera.position.add(delta);
      topCamera.zoom=THREE.MathUtils.clamp(topCamera.zoom*Math.exp(zoom*dt),top.minZoom,top.maxZoom);
      topCamera.updateProjectionMatrix();top.update(dt);
    }
  }
  window.addEventListener('keydown',inspectKey);
  const frames=[];let previous=performance.now(),lastStats=0,raf;
  await renderer.compileAsync(scene,camera);
  renderer.info.reset();renderer.render(scene,camera);
  const initialReadyMs=performance.now()-start;
  function snapshot(){
    const sorted=frames.slice().sort((a,b)=>a-b);
    return {readyMs:initialReadyMs,frameSamples:frames.length,p50Ms:sorted[Math.floor(sorted.length*.5)]??0,p95Ms:sorted[Math.floor(sorted.length*.95)]??0,drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles,textures:renderer.info.memory.textures,geometries:renderer.info.memory.geometries,pixelRatio:renderer.getPixelRatio(),viewport:[host.clientWidth,host.clientHeight],position:camera.position.toArray(),yaw:camera.rotation.y,pitch:camera.rotation.x,door:doors[0].amount,windowAmount,lightsOn:circuits.light.on,locked,mode,target:currentTarget,doors:doorState(),circuits:Object.fromEntries(Object.entries(circuits).map(([id,c])=>[id,{on:c.on,intensities:c.lights.map(({light})=>light.intensity),bulbs:c.bulbs.map(m=>m.emissiveIntensity)}])),walkingPosition:walkCamera.position.toArray(),zoom:camera.zoom,inspectionTarget:(mode==='top'?top:orbit).target.toArray()};
  }
  function tick(now) {
    if(disposed)return;
    const elapsed=now-previous,dt=Math.min(elapsed/1000,.05);previous=now;
    if(mode!=='walk'&&!inspection)updateInspection(dt);
    if(document.visibilityState==='visible'&&elapsed<250){frames.push(elapsed);if(frames.length>3600)frames.shift();}
    const f=(keys.has('KeyW')||keys.has('ArrowUp')?1:0)-(keys.has('KeyS')||keys.has('ArrowDown')?1:0);
    const s=(keys.has('KeyD')||keys.has('ArrowRight')?1:0)-(keys.has('KeyA')||keys.has('ArrowLeft')?1:0);
    const norm=Math.hypot(f,s)||1,speed=2.1*dt;
    if(!inspection&&mode==='walk') {
      move(camera.position,(-Math.sin(camera.rotation.y)*f+Math.cos(camera.rotation.y)*s)*speed/norm,(-Math.cos(camera.rotation.y)*f-Math.sin(camera.rotation.y)*s)*speed/norm,manifest.colliders,doors,manifest.bounds);
      camera.position.y=THREE.MathUtils.damp(camera.position.y,floorHeight(camera.position.x,camera.position.z,true)+1.65,16,dt);
    }
    for(const d of doors){
      const next=d.amount+Math.sign(d.target-d.amount)*Math.min(Math.abs(d.target-d.amount),dt*1.3);
      if(canSwing(d.amount,next,walkCamera.position,d))d.amount=next;
    }
    poseDoors();
    windowAmount=THREE.MathUtils.damp(windowAmount,windowTarget,7,dt);
    windowPivot.quaternion.copy(windowQ).multiply(rotation.setFromAxisAngle(axisX,-windowAmount*Math.PI/12));
    scene.updateMatrixWorld(true);currentTarget=targetAtAim();
    callbacks.target(currentTarget);
    renderer.info.reset();renderer.render(scene,camera);
    if(now-lastStats>600){lastStats=now;callbacks.stats(snapshot());}
    raf=requestAnimationFrame(tick);
  }
  raf=requestAnimationFrame(tick);
  const api={
    enter:()=>setMode('walk',{capture:true}),
    dragLook:()=>{setMode('walk');dragFallback=true;callbacks.fallback?.(true);if(document.pointerLockElement===renderer.domElement)document.exitPointerLock();},
    reset:()=>{reset();renderer.domElement.focus({preventScroll:true});},setMode:next=>setMode(next,{capture:true}),operate:()=>operate(),snapshot,
    dispose(){disposed=true;cancelAnimationFrame(raf);observer.disconnect();clear();if(locked)document.exitPointerLock();
      orbit.dispose();top.dispose();window.removeEventListener('keydown',inspectKey);
      renderer.domElement.removeEventListener('wheel',orbitWheel,true);
      window.removeEventListener('keydown',onKey);window.removeEventListener('keyup',onKey);window.removeEventListener('mousemove',onMouse);window.removeEventListener('blur',clear);
      document.removeEventListener('visibilitychange',clear);document.removeEventListener('pointerlockchange',onLock);document.removeEventListener('pointerlockerror',captureFailed);
      renderer.domElement.removeEventListener('pointerdown',down);renderer.domElement.removeEventListener('pointermove',drag);renderer.domElement.removeEventListener('pointerup',up);renderer.domElement.removeEventListener('pointercancel',up);renderer.domElement.removeEventListener('lostpointercapture',up);
      const materials=new Set(),textures=new Set();scene.traverse(o=>{o.geometry?.dispose();if(o.material)(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>materials.add(m));});
      materials.forEach(m=>{Object.values(m).forEach(v=>{if(v?.isTexture)textures.add(v);});m.dispose();});textures.forEach(t=>t.dispose());renderer.dispose();renderer.domElement.remove();delete window.__M3;
    }
  };
  if(new URLSearchParams(location.search).has('qa')) api.windowBounds=()=>{
    scene.updateMatrixWorld(true);const b=new THREE.Box3().setFromObject(gltf.scene.getObjectByName('W04_return_pane'));
    return {min:b.min.toArray(),max:b.max.toArray(),center:b.getCenter(new THREE.Vector3()).toArray(),quaternion:windowPivot.quaternion.toArray()};
  };
  if(new URLSearchParams(location.search).has('qa')) api.doorGeometry=()=>doors.map(d=>({name:d.name,hinge:d.pivot.localToWorld(new THREE.Vector3()).toArray(),end:d.pivot.localToWorld(new THREE.Vector3(d.width,0,0)).toArray(),amount:d.amount}));
  if(new URLSearchParams(location.search).has('qa')) api.windowClearance=()=>windowClearance;
  // Explicit local QA mode: absent from ordinary user sessions.
  if(new URLSearchParams(location.search).has('qa'))window.__M3={...api,aim:(position,target)=>{if(mode!=='walk')setMode('walk');inspection=false;camera.position.fromArray(position);camera.lookAt(new THREE.Vector3(...target));},inspect:(position,target)=>{inspection=true;keys.clear();camera.position.fromArray(position);camera.lookAt(new THREE.Vector3(...target));},assets:()=>({rooms:manifest.rooms,preparedDoors:manifest.preparedDoors.map(name=>({name,present:!!gltf.scene.getObjectByName(name)})),fixtures:manifest.fixtures}),operateTarget:operate,blocked:(x,z)=>blocked(x,z,manifest.colliders,doors,manifest.bounds),resetFrames:()=>frames.splice(0),renderer:()=>{const gl=renderer.getContext();const ext=gl.getExtension('WEBGL_debug_renderer_info');return ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER);}};
  return api;
}
