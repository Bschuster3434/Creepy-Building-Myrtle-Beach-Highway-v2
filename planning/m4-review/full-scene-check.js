async (page) => {

  const out='C:/Users/brian/Documents/Blender/Creepy-Building-Myrtle-Beach-Highway-v2/planning/m4-review';
  const errors=[],checks=[];page.on('pageerror',e=>errors.push(e.message));
  const check=(name,pass,evidence)=>{checks.push({name,pass,evidence});if(!pass)throw Error(name+': '+JSON.stringify(evidence));};
  await page.setViewportSize({width:1920,height:1080});
  const cdp=await page.context().newCDPSession(page);await cdp.send('Network.enable');
  await cdp.send('Network.setCacheDisabled',{cacheDisabled:true});
  await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:40,downloadThroughput:25e6/8,uploadThroughput:5e6/8});
  await page.goto('http://127.0.0.1:5173/?qa=1');await page.waitForFunction(()=>window.__M3);
  const cold=await page.evaluate(()=>({navigationReadyMs:performance.now(),...window.__M3.snapshot(),gpu:window.__M3.renderer(),userAgent:navigator.userAgent,resources:performance.getEntriesByType('resource').map(r=>({name:r.name,transferSize:r.transferSize,duration:r.duration})),assets:window.__M3.assets()}));
  await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:0,downloadThroughput:-1,uploadThroughput:-1});
  await page.getByRole('button',{name:'Explore the store'}).click();
  await page.evaluate(()=>window.__M3.operateTarget('door'));await page.waitForTimeout(1000);
  check('all prepared rear door pivots load',cold.assets.preparedDoors.every(d=>d.present),cold.assets);
  check('all four spaces and three rear fixtures are present',cold.assets.rooms.length===4&&cold.assets.fixtures.length===3,cold.assets);
  await page.evaluate(()=>window.__M3.resetFrames());
  const state=()=>page.evaluate(()=>window.__M3.snapshot());
  // Each segment has a precise QA start; travel inside the segment uses real keys.
  const segments=[
    ['left room entry',[0,1.83,-6.85],[-2.1,1.83,-6.85]],
    ['left room full aisle',[-2.1,1.83,-6.85],[-2.1,1.83,-12.8]],
    ['right room entry',[0,1.83,-6.85],[2.2,1.83,-6.85]],
    ['right room full aisle',[2.2,1.83,-6.85],[2.2,1.83,-13.6]],
    ['rear passage',[0,1.83,-7.8],[0,1.83,-14.4]],
    ['rear exit and steps',[0,1.83,-14.4],[0,1.83,-17.7]],
    ['rear yard',[0,1.69,-17.7],[4.8,1.69,-17.7]],
    ['right side path',[4.8,1.69,-17.7],[4.8,1.69,2.8]],
    ['return to apron',[4.8,1.69,2.8],[0,1.69,2.8]],
    ['left side path',[-4.8,1.69,2.8],[-4.8,1.69,-17.7]],
  ];
  const samples=[];
  for(const [name,p,t] of segments){
    await page.evaluate(([p,t])=>window.__M3.aim(p,t),[p,t]);await page.waitForTimeout(80);
    await page.keyboard.down('KeyW');await page.waitForTimeout(Math.hypot(p[0]-t[0],p[2]-t[2])/2.1*1000);await page.keyboard.up('KeyW');
    const s=await state();samples.push({name,...s});
    check(name,Math.hypot(s.position[0]-t[0],s.position[2]-t[2])<.30,s.position);
  }
  const performance=await state();
  const views=[['front-reference',[1.2,3,17],[0,2,0]],['front-left',[-24,3,6],[0,2,-6]],['front-right',[17,3.1,14],[0,2,-6.2]],['crates',[-2.1,1.83,-8.4],[-2.5,1.35,-13]],['packing',[1.9,1.83,-8.4],[2.7,1.3,-12]],['packing-detail',[2.0,1.83,-10.6],[2.94,1.19,-10.8]],['rear',[6,2.7,-21],[0,1.5,-13]],['side-path',[4.8,1.69,-2],[4.8,1.69,-15]],['site',[22,15,28],[0,2,-8]],['road',[-5.2,1.7,3.3],[10,1.2,14]]];
  for(const [name,p,t] of views){await page.evaluate(([p,t])=>window.__M3.inspect(p,t),[p,t]);await page.waitForTimeout(180);await page.screenshot({path:out+'/'+name+'.png'});}
  await page.evaluate(()=>window.__M3.operateTarget('light'));
  await page.evaluate(()=>window.__M3.inspect([-2.1,1.83,-8.4],[-2.5,1.35,-13]));await page.waitForTimeout(200);await page.screenshot({path:out+'/crates-lit.png'});
  check('full scene has no runtime errors',errors.length===0,errors);
  const report={conditions:{viewport:[1920,1080],network:'25 Mbps down / 5 Mbps up / 40 ms latency; cache disabled',...cold},checks,samples,performance,errors};

  await page.evaluate(()=>{document.exitPointerLock();window.__M3.reset();});
  return report;
}
