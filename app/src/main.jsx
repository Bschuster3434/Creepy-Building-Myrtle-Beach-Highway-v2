import React, {useEffect,useRef,useState} from 'react';
import {createRoot} from 'react-dom/client';
import {createWorld} from './world.js';
import './style.css';

function App(){
  const host=useRef(null),world=useRef(null);
  const [ready,setReady]=useState(false),[error,setError]=useState(''),[locked,setLocked]=useState(false);
  const [exploring,setExploring]=useState(false),[mode,setMode]=useState('walk'),[dragFallback,setDragFallback]=useState(false);
  const [target,setTarget]=useState(null),[stats,setStats]=useState(null),[message,setMessage]=useState('');
  const [states,setStates]=useState({door:false,window:false,light:false}),[details,setDetails]=useState(false);
  useEffect(()=>{let cancelled=false;createWorld(host.current,{start:()=>setExploring(true),mode:setMode,fallback:setDragFallback,lock:setLocked,target:setTarget,stats:setStats,state:setStates,message:setMessage}).then(api=>{if(cancelled){api.dispose();return;}world.current=api;setReady(true);}).catch(e=>{if(!cancelled)setError(e.message);});return()=>{cancelled=true;world.current?.dispose();};},[]);
  useEffect(()=>{if(!message)return;const id=setTimeout(()=>setMessage(''),4000);return()=>clearTimeout(id);},[message]);
  const doorLabels={door:'front doors',cratesDoor:'crate storeroom door',packingDoor:'packing room door',rearDoor:'rear door'};
  const lightLabels={light:'sales room',cratesLight:'crate storeroom',packingLight:'packing room',passage:'rear passage'};
  const label=doorLabels[target]?`${states[target]?'Close':'Open'} the ${doorLabels[target]}`:target==='window'?`${states.window?'Close':'Tilt open'} the window`:lightLabels[target]?`Turn the ${lightLabels[target]} lights ${states[target]?'off':'on'}`:'';
  return <main>
    <div className="world" ref={host} aria-label="Interactive three-dimensional store walkthrough"/>
    <header><div className="wordmark">4397 <span>HIGHWAY 9</span></div><div className="sample-tag">THE OLD STORE <i/> BUILDING & GROUNDS</div><button className="quiet" onClick={()=>setDetails(!details)} aria-expanded={details}>Field notes <span>↗</span></button></header>
    {!exploring&&<section className="intro"><p className="eyebrow">LORIS, SOUTH CAROLINA</p><h1>A little time,<br/>left standing.</h1><p className="description">An empty chair. The afternoon light.<br/>Step inside a quiet roadside store.</p><button className="enter" disabled={!ready||!!error} onClick={()=>{world.current?.enter();}}>{error?'Unable to open the scene':ready?'Explore the store  →':'Preparing the store…'}</button>{error&&<p role="alert">{error} Refresh to retry.</p>}<p className="controls">Move the mouse to look · W / A / S / D to walk<br/>Click or E to use · Esc for the cursor · 1 / 2 / 3 change view</p></section>}
    {exploring&&<nav className="view-modes" aria-label="Viewing mode">{[['walk','Walk','1'],['orbit','Orbit','2'],['top','Top-down','3']].map(([id,name,key])=><button key={id} aria-pressed={mode===id} onClick={()=>world.current?.setMode(id)}><kbd>{key}</kbd>{name}</button>)}</nav>}
    {exploring&&!locked&&<div className="look-controls"><span>{mode==='walk'?(dragFallback?'Mouse capture unavailable · Hold left mouse + drag to look':'Click the view to resume · Move the mouse to look · W / A / S / D to walk'):mode==='orbit'?'Scroll sideways or A / D / ← / → to orbit · Scroll vertically or W / S / ↑ / ↓ to zoom · Left or right drag also works':'Drag or arrow keys to pan · Scroll or + / − to zoom'}</span></div>}
    {mode==='walk'&&<div className={`crosshair ${target?'active':''}`} aria-hidden="true"/>}
    {label&&<button className="interaction" onClick={()=>world.current?.operate()}><kbd>E</kbd>{label}</button>}
    {message&&<p role="status" className="toast">{message}</p>}
    {details&&<aside><button className="close" onClick={()=>setDetails(false)} aria-label="Close field notes">×</button><p className="eyebrow">FIELD NOTES / 01</p><h2>A store, remembered.</h2><p>The exterior follows the approved reconstruction of 4397 Highway 9. The sparse interior is imagined, including the empty chair behind the front-right counter.</p><p>Walk around the left end of the counter to find the crate storeroom, packing room and rear passage. Open each door with a click or E. Step beyond the end of an open leaf to continue into a room. The back door opens onto a quiet service yard; the paths lead around both sides of the store.</p><p>Try the small angled window on the right of the entrance. The sales room switch sits just inside on the right. Each storeroom has a switch on its front wall; the passage switch is on the right near the rear exit. Each controls its own lights.</p><p>Press 1 to walk, 2 to orbit or 3 for the top-down site view. Returning to Walk restores your position and direction. Use the mouse wheel or + / − to zoom in either inspection view.</p><button className="secondary" onClick={()=>{setDetails(false);world.current?.reset();}}>Return to the apron</button><details><summary>Scene performance</summary><p>{stats?`${stats.triangles.toLocaleString()} rendered triangles · ${stats.drawCalls} draw calls · p95 ${stats.p95Ms.toFixed(1)} ms · ready ${(stats.readyMs/1000).toFixed(2)} s`:'Waiting for the scene'}</p><small>Measurements from this browser session.</small></details></aside>}
    <footer><span>34.007932° N &nbsp; 78.764340° W</span><span className="movement-help">{mode==='walk'?'W / S forward & back · A / D or ← / → sideways':'1 Walk · 2 Orbit · 3 Top-down'}</span><span className="footer-right">SEPTEMBER LIGHT <i/> THE OLD STORE</span></footer>
  </main>;
}
createRoot(document.getElementById('root')).render(<App/>);
