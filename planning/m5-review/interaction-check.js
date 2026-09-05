async (page) => {
  const out='C:/Users/brian/Documents/Blender/Creepy-Building-Myrtle-Beach-Highway-v2/planning/m5-review';
  async function run(p,browser){
    const checks=[],errors=[];
    p.on('pageerror',e=>errors.push(e.message));
    const check=(name,pass,evidence)=>{checks.push({name,pass,evidence});if(!pass)throw Error(name);};
    const state=()=>p.evaluate(()=>window.__M3.snapshot());
    const aim=async(pos,target)=>{await p.evaluate(([a,b])=>window.__M3.aim(a,b),[pos,target]);await p.waitForTimeout(100);};
    const use=async(click=false)=>{if(click)await p.mouse.click(960,540);else await p.keyboard.press('KeyE');await p.waitForTimeout(870);};
    try{
      await p.setViewportSize({width:1920,height:1080});
      await p.goto('http://127.0.0.1:5173/?qa=1');await p.waitForFunction(()=>window.__M3);
      await p.getByRole('button',{name:'Explore the store',exact:false}).click();
      const doors=[
        ['door',[0,1.83,1.3],[0,1.2,-.305],[-.73,1.2,-.66]],
        ['cratesDoor',[0,1.83,-6.85],[-.81,1.2,-6.85],[-1.35,1.2,-7.35]],
        ['packingDoor',[0,1.83,-6.85],[.81,1.2,-6.85],[1.35,1.2,-7.35]],
        ['rearDoor',[0,1.83,-14.3],[0,1.2,-15.18],[-.5,1.2,-15.65]],
      ];
      for(const [id,pos,closed,open] of doors){
        for(let i=0;i<4;i++){
          await aim(pos,i%2?open:closed);
          check(`${id} aim ${i}`,(await state()).target===id,(await state()).target);
          const before=(await state()).doors;
          await use(i%2===0);
          const after=(await state()).doors;
          check(`${id} ${i%2?'E closes':'click opens'} ${i}`,after.filter(d=>d.control===id).every(d=>Math.abs(d.amount-(i%2?0:1))<.001),after.map(d=>[d.control,d.amount]));
          check(`${id} leaves other doors unchanged ${i}`,after.every((d,j)=>d.control===id||d.amount===before[j].amount));
        }
        // Compare rendered endpoints with collision endpoints during real animation.
        await aim(pos,closed);await p.keyboard.press('KeyE');
        const parity=[];
        for(let i=0;i<8;i++){
          await p.waitForTimeout(85);
          parity.push(await p.evaluate(()=>{const s=window.__M3.snapshot(),g=window.__M3.doorGeometry();return Math.max(...s.doors.map((d,j)=>{const a=d.closedAngle+d.swingAngle*d.amount;return Math.hypot(g[j].end[0]-d.hinge[0]-d.width*Math.cos(a),g[j].end[2]-d.hinge[1]+d.width*Math.sin(a));}));}));
        }
        await p.waitForTimeout(200);
        check(`${id} render and collision match throughout animation`,Math.max(...parity)<.0001,parity);
      }
      const lights=[['light',[.75,1.83,-1.45],[1.088,1.39,-.29]],['cratesLight',[-2.12,1.83,-6.8],[-2.12,1.4,-5.96]],['packingLight',[2.12,1.83,-6.8],[2.12,1.4,-5.96]],['passage',[0,1.83,-14.3],[.71,1.4,-14.3]]];
      for(const [id,pos,target] of lights){
        await aim(pos,target);check(`${id} switch reachable`,(await state()).target===id,(await state()).target);
        for(let i=0;i<4;i++){
          const before=(await state()).circuits;
          await use(i%2===0);const after=(await state()).circuits;
          check(`${id} independently toggles light and bulb ${i}`,after[id].on===(i%2===0)&&after[id].intensities.every(v=>i%2?v===0:v>0)&&after[id].bulbs.every(v=>i%2?v===0:v>0)&&Object.keys(after).every(k=>k===id||JSON.stringify(after[k])===JSON.stringify(before[k])),after);
        }
        await use();await p.screenshot({path:`${out}/${browser}-${id}.png`});
      }
      for(let i=0;i<4;i++){
        await aim([1.5,1.83,-1],i%2?[.963,1.61,-.292]:[.84,1.55,-.16]);
        check(`window aimed ${i}`,(await state()).target==='window');await use(i%2===0);
        check(`window repeated operation ${i}`,Math.abs((await state()).windowAmount-(i%2?0:1))<.01);
      }
      const clearance=await p.evaluate(()=>window.__M3.windowClearance());
      const wx=(clearance.min[0]+clearance.max[0])/2;
      await aim([wx,1.83,clearance.min[2]-1],[wx,1.83,clearance.max[2]+1]);
      await p.keyboard.down('KeyW');await p.waitForTimeout(900);await p.keyboard.up('KeyW');
      check('walking body stops before the window opening envelope',(await state()).position[2]<=clearance.min[2]-.245,(await state()).position);
      check('window clearance remains physically blocked',await p.evaluate(([x,z])=>window.__M3.blocked(x,z),[wx,(clearance.min[2]+clearance.max[2])/2]));
      // Every door must reject closure around a body already in its opening.
      for(const [id,pos,closed] of doors){
        const body=id==='door'?[0,1.83,-.305]:closed.map((v,i)=>i===1?1.83:v);
        await aim(body,[body[0],1.5,body[2]-1]);
        const accepted=await p.evaluate(id=>window.__M3.operateTarget(id),id);
        check(`${id} rejects unsafe closure`,accepted===false);
      }
      await aim([0,1.83,-14.3],[-.5,1.2,-15.65]);await p.keyboard.press('KeyE');
      await p.waitForTimeout(110);await aim([0,1.83,-15.18],[0,1.5,-16]);await p.waitForTimeout(850);
      check('door pauses safely if player enters during closing',(await state()).doors.find(d=>d.control==='rearDoor').amount>.15&&await p.evaluate(()=>!window.__M3.blocked(0,-15.18)),(await state()).doors);
      await aim([0,1.83,-14.3],[0,1.2,-15.18]);await p.waitForTimeout(900);
      check('paused door finishes once player clears',(await state()).doors.find(d=>d.control==='rearDoor').amount===0);
      await aim([2.12,1.83,-5.4],[2.12,1.4,-5.96]);check('switch cannot be used through room wall',(await state()).target===null,(await state()).target);
      check('no runtime errors',errors.length===0,errors);
    }catch(e){errors.push(e.message);await p.screenshot({path:`${out}/${browser}-interaction-failure.png`});}
    return {browser,checks,errors,pass:errors.length===0,userAgent:await p.evaluate(()=>navigator.userAgent)};
  }
  const chrome=await run(page,'chrome');await page.goto('about:blank');
  if(!chrome.pass)return {chrome};
  const edgeBrowser=await page.context().browser().browserType().launch({channel:'msedge',headless:true});
  try{const p=await edgeBrowser.newPage();return {chrome,edge:await run(p,'edge')};}finally{await edgeBrowser.close();}
}
