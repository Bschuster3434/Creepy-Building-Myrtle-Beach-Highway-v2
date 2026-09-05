async (page) => {
  const out = 'C:/Users/brian/Documents/Blender/Creepy-Building-Myrtle-Beach-Highway-v2/planning/m3-review';
  const checks = [];
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  const check = (name, pass, evidence) => {checks.push({name,pass,evidence});if(!pass)throw new Error(name+': '+JSON.stringify(evidence));};
  await page.setViewportSize({width:1920,height:1080});
  const cdp=await page.context().newCDPSession(page);
  await cdp.send('Network.enable');
  await cdp.send('Network.setCacheDisabled',{cacheDisabled:true});
  await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:40,downloadThroughput:25e6/8,uploadThroughput:5e6/8});
  const t=Date.now();
  await page.goto('http://127.0.0.1:5173/?qa=1');
  await page.waitForFunction(()=>!!window.__M3);
  const cold=await page.evaluate(()=>({readyMs:window.__M3.snapshot().readyMs,resources:performance.getEntriesByType('resource').map(r=>({name:r.name,transferSize:r.transferSize,duration:r.duration})),navigationReadyMs:performance.now(),gpu:window.__M3.renderer(),userAgent:navigator.userAgent}));
  cold.wallReadyMs=Date.now()-t;
  await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:0,downloadThroughput:-1,uploadThroughput:-1});
  await page.screenshot({path:out+'/front.png'});
  await page.getByRole('button',{name:'Explore the store'}).click();
  await page.waitForTimeout(150);
  check('pointer capture enters',await page.evaluate(()=>window.__M3.snapshot().locked));
  const aim=async(p,t)=>{await page.evaluate(([p,t])=>window.__M3.aim(p,t),[p,t]);await page.waitForTimeout(120);};
  const state=()=>page.evaluate(()=>window.__M3.snapshot());
  const use=async()=>{await page.keyboard.press('KeyE');await page.waitForTimeout(900);};
  await aim([0,1.72,1.3],[0,1.72,-4]);
  await page.keyboard.down('KeyW');await page.waitForTimeout(1200);await page.keyboard.up('KeyW');
  check('closed front door stops real keyboard movement',(await state()).position[2]>-.3,await state());
  await aim([0,1.72,1.3],[0,1.2,-.305]);
  for(let i=0;i<4;i++){
    await aim([0,1.72,1.3],i%2===0?[0,1.2,-.305]:[-.73,1.2,-.66]);
    await use();check('door repeated toggle '+i,Math.abs((await state()).door-(i%2===0?1:0))<.01);
  }
  await aim([0,1.83,-2.2],[0,1.5,0]);
  await page.screenshot({path:out+'/interior-glazing.png'});
  await aim([0,1.72,1.3],[0,1.2,-.305]);
  await use();
  await aim([0,1.72,1.3],[0,1.72,-6]);
  await page.keyboard.down('KeyW');await page.waitForTimeout(2650);await page.keyboard.up('KeyW');
  check('open door admits walking to the service counter',(await state()).position[2]<-2.0 && (await state()).position[2]>-2.2,await state());
  await aim([-2.78,1.83,-1.5],[-2.78,1.83,-4]);
  await page.keyboard.down('KeyW');await page.waitForTimeout(960);await page.keyboard.up('KeyW');
  check('left counter access admits real walking',(await state()).position[2]<-3.45,await state());
  await aim((await state()).position,[0,1.83,(await state()).position[2]]);
  await page.keyboard.down('KeyW');await page.waitForTimeout(1320);await page.keyboard.up('KeyW');
  check('serving aisle connects behind the counter',Math.abs((await state()).position[0])<.3,await state());
  await aim([0,1.83,-4.7],[4,1.83,-4.7]);
  await page.keyboard.down('KeyW');await page.waitForTimeout(2200);await page.keyboard.up('KeyW');
  check('shelving blocks the player',(await state()).position[0]<2.7,await state());
  await aim([.75,1.83,-1.45],[1.088,1.39,-.29]);
  check('light switch is reachable by aim',(await page.locator('.interaction').textContent()).includes('lights'));
  for(let i=0;i<4;i++){await use();check('actual light toggles '+i,(await state()).lightsOn===(i%2===0));}
  await use();
  await aim([1.5,1.72,1],[.84,1.55,-.16]);
  check('approved pane is reachable by aim',(await page.locator('.interaction').textContent()).includes('window'));
  for(let i=0;i<4;i++){
    await aim([1.5,1.83,-1],i%2===0?[.84,1.55,-.16]:[.963,1.61,-.292]);
    await use();check('window repeated tilt '+i,Math.abs((await state()).windowAmount-(i%2===0?1:0))<.01);
  }
  await aim([1.5,1.72,1],[.84,1.55,-.16]);
  await use();
  await aim([1.5,1.83,-1],[.963,1.61,-.292]);
  await page.screenshot({path:out+'/window-open.png'});
  await aim([0,1.83,-4.1],[2.2,1.03,-3.5]);
  await page.screenshot({path:out+'/chair-counter.png'});
  await aim([-.35,1.83,-.9],[.1,1.45,-4.8]);
  await page.screenshot({path:out+'/room.png'});
  await page.evaluate(()=>window.__M3.operateTarget('light'));
  await page.waitForTimeout(200);
  await page.screenshot({path:out+'/room-daylight.png'});
  await aim([.05,1.83,-1.95],[.95,1.45,-2.79]);
  await page.screenshot({path:out+'/produce-counter.png'});
  await page.evaluate(()=>window.__M3.operateTarget('light'));
  await aim([.35,1.83,-5.35],[0,1.65,.3]);
  await page.screenshot({path:out+'/toward-storefront.png'});
  await aim([0,1.83,-7.8],[0,1.83,-14.7]);
  await page.keyboard.down('KeyW');await page.waitForTimeout(2700);await page.keyboard.up('KeyW');
  check('continuous central passage reaches the rear door',(await state()).position[2]<-13.2,await state());
  for(const side of [-1,1]){
    await aim([0,1.83,-6.85],[side*2.2,1.83,-6.85]);
    await page.keyboard.down('KeyW');await page.waitForTimeout(900);await page.keyboard.up('KeyW');
    check('storeroom entrance '+side+' is reachable',side*(await state()).position[0]>1.7,await state());
  }
  await aim([0,1.83,-5.35],[0,1.65,-14.8]);
  await page.screenshot({path:out+'/passage.png'});
  await page.evaluate(()=>window.__M3.resetFrames());
  const route=[[[0,1.72,3.1],[0,1.72,-2],1800],[[-2.78,1.83,-1.5],[-2.78,1.83,-4],960],[[-2.78,1.83,-3.55],[0,1.83,-3.55],1320],[[0,1.83,-3.55],[.4,1.83,-6.8],1600],[[0,1.83,-6.85],[0,1.83,-14.7],3000]];
  const routeSamples=[];
  for(const [p,t,duration] of route){await aim(p,t);await page.keyboard.down('KeyW');await page.waitForTimeout(duration);await page.keyboard.up('KeyW');routeSamples.push(await state());}
  const performanceReport=await state();
  await page.keyboard.down('KeyW');
  await page.evaluate(()=>window.dispatchEvent(new Event('blur')));
  const before=(await state()).position;
  await page.waitForTimeout(250);await page.keyboard.up('KeyW');
  check('focus loss clears held movement',Math.hypot(...(await state()).position.map((v,i)=>v-before[i]))<.02);
  await page.evaluate(()=>document.exitPointerLock());await page.waitForTimeout(100);
  check('pointer release restores entry controls',await page.getByRole('button',{name:'Explore the store'}).isVisible());
  await page.getByRole('button',{name:'Explore the store'}).click();await page.waitForTimeout(100);
  check('pointer capture resumes',await page.evaluate(()=>window.__M3.snapshot().locked));
  check('no browser runtime errors',errors.length===0,errors);
  const report={conditions:{viewport:[1920,1080],coldNetwork:'25 Mbps down / 5 Mbps up / 40 ms latency / cache disabled',...cold},checks,routeSamples,performance:performanceReport,errors};
  await page.evaluate(()=>{document.exitPointerLock();window.__M3.reset();});
  return report;
}
