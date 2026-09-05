async (page) => {
  const out='C:/Users/brian/Documents/Blender/Creepy-Building-Myrtle-Beach-Highway-v2/planning/m5-review';
  async function run(p,browser){
    const checks=[],errors=[],samples=[];let cold,performance;
    p.on('pageerror',e=>errors.push(e.message));
    const check=(name,pass,evidence)=>{checks.push({name,pass,evidence});if(!pass)throw Error(name);};
    const state=()=>p.evaluate(()=>window.__M3.snapshot());
    try{
      await p.setViewportSize({width:1920,height:1080});
      const cdp=await p.context().newCDPSession(p);await cdp.send('Network.enable');await cdp.send('Network.setCacheDisabled',{cacheDisabled:true});
      await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:40,downloadThroughput:25e6/8,uploadThroughput:5e6/8});
      await p.goto('http://127.0.0.1:5173/?qa=1');await p.waitForFunction(()=>window.__M3);
      cold=await p.evaluate(()=>({navigationReadyMs:performance.now(),readyMs:window.__M3.snapshot().readyMs,userAgent:navigator.userAgent,gpu:window.__M3.renderer(),resources:performance.getEntriesByType('resource').map(r=>({name:r.name,transferSize:r.transferSize,duration:r.duration}))}));
      cold.transferBytes=cold.resources.reduce((n,r)=>n+r.transferSize,0);
      await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:0,downloadThroughput:-1,uploadThroughput:-1});
      await p.getByRole('button',{name:'Explore the store',exact:false}).click();
      await p.evaluate(()=>['door','cratesDoor','packingDoor','rearDoor','light','cratesLight','packingLight','passage'].forEach(id=>window.__M3.operateTarget(id)));
      await p.waitForTimeout(1000);
      const returnAccess=[['door',[0,1.83,-1.8],[-.73,1.2,-.66],[0,1.2,-.305]],['cratesDoor',[-2.35,1.83,-6.85],[-1.35,1.2,-7.35],[-.81,1.2,-6.85]],['packingDoor',[2.35,1.83,-6.85],[1.35,1.2,-7.35],[.81,1.2,-6.85]],['rearDoor',[0,1.74,-16.85],[-.5,1.2,-15.65],[0,1.2,-15.18]]];
      for(const [id,pos,open,closed] of returnAccess){
        for(const [target,amount] of [[open,0],[closed,1]]){
          await p.evaluate(([pos,target])=>window.__M3.aim(pos,target),[pos,target]);await p.waitForTimeout(100);
          check(`${id} reachable from reverse side before ${amount?'opening':'closing'}`,(await state()).target===id,(await state()).target);
          await p.keyboard.press('KeyE');await p.waitForTimeout(870);
          check(`${id} ${amount?'reopens':'closes'} from reverse side`,(await state()).doors.filter(d=>d.control===id).every(d=>d.amount===amount));
        }
      }
      await p.evaluate(()=>{window.__M3.reset();window.__M3.resetFrames();});
      // One continuous route: aim updates retain the actual current position.
      const points=[['entrance',[0,-1.5]],['customer aisle',[-2.78,-1.5]],['around counter',[-2.78,-3.55]],['serving aisle',[0,-3.55]],['front passage',[.3,-5.35]],['storeroom junction',[0,-6.85]],['crate room entry',[-2.25,-6.85]],['crate room full aisle',[-2.25,-12.8]],['crate room return',[-2.25,-6.85]],['passage return',[0,-6.85]],['packing room entry',[2.25,-6.85]],['packing room full aisle',[2.25,-13.6]],['packing room return',[2.25,-6.85]],['passage again',[0,-6.85]],['rear passage',[0,-14.4]],['rear exit and steps',[0,-17.7]],['rear yard',[4.8,-17.7]],['right side path',[4.8,2.8]],['front apron',[0,2.8]],['left apron',[-4.8,2.8]],['left side path',[-4.8,-17.7]],['yard return',[0,-17.7]],['reenter rear',[0,-14.4]],['return through passage',[0,-6.85]]];
      for(const [name,[x,z]] of points){
        for(let attempt=0;attempt<3;attempt++){
          const s=await state(),distance=Math.hypot(s.position[0]-x,s.position[2]-z);
          if(distance<.08)break;
          await p.evaluate(([x,z])=>{const pos=window.__M3.snapshot().position;window.__M3.aim(pos,[x,pos[1],z]);},[x,z]);
          await p.keyboard.down('KeyW');await p.waitForTimeout(Math.max(25,(distance-.035)/2.1*1000));await p.keyboard.up('KeyW');
        }
        const s=await state();samples.push({name,position:s.position,p95Ms:s.p95Ms,drawCalls:s.drawCalls,triangles:s.triangles});
        check(name,Math.hypot(s.position[0]-x,s.position[2]-z)<.18,s.position);
        check(`${name} body is clear`,await p.evaluate(()=>{const p=window.__M3.snapshot().position;return !window.__M3.blocked(p[0],p[2]);}));
      }
      performance=await state();
      check('walkthrough p95 meets accepted 20 ms',performance.p95Ms<=20,performance.p95Ms);
      check('initial transfer meets 15 MB',cold.transferBytes<=15e6,cold.transferBytes);
      check('sampled draw calls within 350',Math.max(...samples.map(s=>s.drawCalls))<=350,Math.max(...samples.map(s=>s.drawCalls)));
      check('rendered triangles including shadow pass within 750k',Math.max(...samples.map(s=>s.triangles))<=750000,Math.max(...samples.map(s=>s.triangles)));
      const views=[['crates',[-2.25,1.83,-8.4],[-2.5,1.4,-12]],['packing',[1.9,1.83,-8.4],[2.7,1.3,-12]],['rear-door',[0,1.83,-14.1],[-.4,1.3,-15.9]],['sales',[-2.6,1.83,-3.6],[1.4,1.3,-2.8]]];
      for(const [name,pos,target] of views){await p.evaluate(([a,b])=>window.__M3.aim(a,b),[pos,target]);await p.waitForTimeout(150);await p.screenshot({path:`${out}/${browser}-${name}.png`});}
      for(const [id,name] of [['orbit','orbit'],['top','top-down']]){
        await p.evaluate(id=>window.__M3.setMode(id),id);await p.waitForTimeout(180);await p.screenshot({path:`${out}/${browser}-${name}.png`});
      }
      check('no runtime errors',errors.length===0,errors);
    }catch(e){errors.push(e.message);await p.screenshot({path:`${out}/${browser}-route-failure.png`});}
    return {browser,conditions:{viewport:[1920,1080],network:'25 Mbps down / 5 Mbps up / 40 ms latency; cache disabled; one scene rendering; all four light circuits on during walking'},cold,performance,samples,checks,errors,pass:errors.length===0};
  }
  const chrome=await run(page,'chrome');await page.goto('about:blank');if(!chrome.pass)return {chrome};
  const edgeBrowser=await page.context().browser().browserType().launch({channel:'msedge',headless:true});
  try{return {chrome,edge:await run(await edgeBrowser.newPage(),'edge')};}finally{await edgeBrowser.close();}
}
