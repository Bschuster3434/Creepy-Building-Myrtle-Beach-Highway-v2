async (page) => {
  async function run(p,browser){
    const checks=[],errors=[];p.on('pageerror',e=>errors.push(e.message));
    const check=(name,pass,evidence)=>{checks.push({name,pass,evidence});if(!pass)throw Error(name);};
    const state=()=>p.evaluate(()=>window.__M3.snapshot());
    const dist=(a,b)=>Math.hypot(...a.map((v,i)=>v-b[i]));
    const angle=s=>Math.atan2(s.position[0]-s.inspectionTarget[0],s.position[2]-s.inspectionTarget[2]);
    const turn=(a,b)=>Math.atan2(Math.sin(angle(b)-angle(a)),Math.cos(angle(b)-angle(a)));
    const radius=s=>dist(s.position,s.inspectionTarget);
    const elevation=s=>(s.position[1]-s.inspectionTarget[1])/radius(s);
    const drag=async(button,dx,dy=0)=>{await p.mouse.move(800,500);await p.mouse.down({button});await p.mouse.move(800+dx,500+dy,{steps:8});await p.mouse.up({button});};
    try{
      await p.setViewportSize({width:1920,height:1080});await p.goto('http://127.0.0.1:5173/?qa=1');await p.waitForFunction(()=>window.__M3);
      await p.getByRole('button',{name:'Explore the store',exact:false}).click();await p.waitForTimeout(150);
      check('single entry click enables first-person mouse look',(await state()).locked);
      check('no secondary mouse activation or drag entry button',await p.getByRole('button',{name:/Enable mouse look|Explore by dragging/}).count()===0);
      await p.mouse.move(700,300);await p.waitForTimeout(80);
      let before=await state();await p.mouse.move(1000,450);await p.waitForTimeout(100);let after=await state();
      check('unheld mouse motion turns walking view',Math.abs(after.yaw-before.yaw)>.05&&Math.abs(after.pitch-before.pitch)>.05,{before:[before.yaw,before.pitch],after:[after.yaw,after.pitch]});
      before=await state();await p.keyboard.down('KeyW');await p.waitForTimeout(250);await p.keyboard.up('KeyW');
      check('walking works immediately with captured mouse',dist((await state()).position,before.position)>.35);
      await p.evaluate(()=>window.__M3.aim([0,1.83,1.3],[0,1.2,-.305]));await p.waitForTimeout(80);await p.keyboard.press('KeyE');await p.waitForTimeout(850);
      check('E door operation preserved',(await state()).door===1);
      for(let repeat=0;repeat<3;repeat++){
        await p.evaluate(()=>window.__M3.aim([0,1.83,-6.85],[2,1.6,-8]));const saved=await state();
        await p.keyboard.press('Digit2');await p.waitForTimeout(150);
        check(`2 enters active orbit and frees cursor ${repeat}`,(await state()).mode==='orbit'&&!(await state()).locked);
        // Real horizontal wheel input BEFORE any click or drag in orbit mode.
        await p.mouse.move(800,500);before=await state();await p.mouse.wheel(-180,0);await p.waitForTimeout(400);after=await state();
        check(`no-click left trackpad scroll orbits in reversed direction ${repeat}`,turn(before,after)<-.4,{delta:turn(before,after)});
        check(`horizontal trackpad scroll does not zoom or tilt ${repeat}`,Math.abs(radius(after)-radius(before))<.01&&Math.abs(elevation(after)-elevation(before))<.001);
        before=await state();await p.mouse.wheel(180,0);await p.waitForTimeout(400);after=await state();
        check(`no-click right trackpad scroll reverses left ${repeat}`,turn(before,after)>.4);
        before=await state();await drag('left',180,45);await p.waitForTimeout(180);after=await state();
        check(`left-button orbit works in reversed direction ${repeat}`,turn(before,after)>.3);
        before=await state();await drag('right',180);await p.waitForTimeout(180);after=await state();
        check(`right-button drag orbits in same reversed direction ${repeat}`,turn(before,after)>.3);
        // Restore zoom headroom: W now legitimately zooms in during each loop.
        await p.mouse.wheel(0,250);await p.waitForTimeout(400);
        before=await state();await p.mouse.wheel(0,-250);await p.waitForTimeout(150);after=await state();
        check(`scroll zooms toward building ${repeat}`,dist(after.position,after.inspectionTarget)<dist(before.position,before.inspectionTarget)-.5);
        await p.keyboard.down('ArrowRight');await p.waitForTimeout(100);before=await state();await p.waitForTimeout(140);after=await state();await p.keyboard.up('ArrowRight');
        check(`held arrow rotates continuously before repeat delay ${repeat}`,dist(after.position,before.position)>1);
        await p.keyboard.press('KeyE');await p.keyboard.down('KeyW');await p.waitForTimeout(100);await p.keyboard.up('KeyW');
        check(`orbit input preserves body and interactions ${repeat}`,dist((await state()).walkingPosition,saved.position)<.001&&(await state()).door===1);
        await p.keyboard.press('Digit1');await p.waitForTimeout(150);after=await state();
        check(`1 returns directly to mouse-look ${repeat}`,after.mode==='walk'&&after.locked);
        check(`walking pose preserved ${repeat}`,dist(after.position,saved.position)<.001&&Math.abs(after.yaw-saved.yaw)<.001&&Math.abs(after.pitch-saved.pitch)<.001);
      }
      await p.keyboard.press('Digit2');await p.waitForTimeout(150);
      for(const [key,sign] of [['KeyA',-1],['ArrowLeft',-1],['KeyD',1],['ArrowRight',1]]){
        before=await state();await p.keyboard.down(key);await p.waitForTimeout(220);await p.keyboard.up(key);after=await state();
        check(`${key} continuously orbits in requested direction`,turn(before,after)*sign>.1);
        check(`${key} keeps distance and elevation`,Math.abs(radius(after)-radius(before))<.01&&Math.abs(elevation(after)-elevation(before))<.001);
      }
      for(const [key,sign] of [['KeyS',1],['ArrowDown',1],['KeyW',-1],['ArrowUp',-1]]){
        before=await state();await p.keyboard.down(key);await p.waitForTimeout(180);await p.keyboard.up(key);after=await state();
        check(`${key} zooms ${sign<0?'in':'out'}`,(radius(after)-radius(before))*sign>1);
        check(`${key} zoom does not tilt or orbit`,Math.abs(turn(before,after))<.001&&Math.abs(elevation(after)-elevation(before))<.001);
      }
      before=await state();await p.mouse.wheel(140,120);await p.waitForTimeout(400);after=await state();
      check('diagonal trackpad gesture rotates and zooms without clicking',turn(before,after)>.3&&radius(after)>radius(before)+1);
      before=await state();await p.mouse.wheel(0,-120);await p.waitForTimeout(400);after=await state();
      check('vertical trackpad gesture only zooms',radius(after)<radius(before)-1&&Math.abs(turn(before,after))<.001);
      await p.mouse.wheel(140,0);await p.evaluate(()=>window.dispatchEvent(new Event('blur')));before=await state();await p.waitForTimeout(200);after=await state();
      check('focus loss clears pending trackpad easing',dist(after.position,before.position)<.01);
      // More than one full turn, with no horizontal stop or reversal at the seam.
      let total=0;
      for(let i=0;i<8;i++){
        before=await state();await drag('left',300);await p.waitForTimeout(300);after=await state();
        const delta=Math.atan2(Math.sin(angle(after)-angle(before)),Math.cos(angle(after)-angle(before)));total+=delta;
        check(`horizontal orbit continues in same reversed direction ${i}`,delta>.5,delta);
      }
      check('orbit passes a complete 360-degree turn',Math.abs(total)>2*Math.PI,total);
      await drag('left',250);before=await state();await p.waitForTimeout(50);after=await state();
      check('orbit eases after drag release',dist(after.position,before.position)>.001);
      await p.waitForTimeout(800);before=await state();await p.waitForTimeout(200);after=await state();
      check('orbit easing settles without endless drift',dist(after.position,before.position)<.01);
      await p.mouse.wheel(0,-20000);await p.waitForTimeout(200);after=await state();
      check('orbit minimum distance remains bounded',dist(after.position,after.inspectionTarget)>=14.999);
      await p.mouse.wheel(0,30000);await p.waitForTimeout(200);after=await state();
      check('orbit maximum distance remains bounded',dist(after.position,after.inspectionTarget)<=65.001);
      await p.keyboard.press('Digit3');await p.waitForTimeout(100);before=await state();await drag('left',130,65);after=await state();
      check('top-down pan remains functional',after.mode==='top'&&dist(after.position,before.position)>.5&&Math.abs(after.pitch+Math.PI/2)<.001);
      before=await state();await p.keyboard.down('ArrowRight');await p.waitForTimeout(200);await p.keyboard.up('ArrowRight');await p.keyboard.down('Equal');await p.waitForTimeout(200);await p.keyboard.up('Equal');after=await state();
      check('top-down held keys pan and zoom',dist(after.position,before.position)>.5&&after.zoom>before.zoom);
      await p.keyboard.press('Digit1');await p.waitForTimeout(150);check('top-down returns directly to first person',(await state()).locked&&(await state()).mode==='walk');
      await p.keyboard.press('Escape');await p.waitForTimeout(100);check('Escape releases cursor',!(await state()).locked);
      await p.mouse.click(960,540);await p.waitForTimeout(150);check('single canvas click resumes mouse look',(await state()).locked);
      await p.keyboard.down('KeyW');await p.evaluate(()=>window.dispatchEvent(new Event('blur')));before=await state();await p.waitForTimeout(200);await p.keyboard.up('KeyW');
      check('focus loss still clears walking input',dist((await state()).position,before.position)<.03);
      await p.keyboard.press('Escape');await p.waitForTimeout(100);
      await p.evaluate(()=>{const c=document.querySelector('canvas');c.__request=c.requestPointerLock;c.requestPointerLock=()=>Promise.reject(Error('QA capture denial'));});
      await p.keyboard.press('Digit1');await p.waitForTimeout(100);
      check('capture rejection exposes automatic fallback',!(await state()).locked&&await p.getByText('Mouse capture unavailable · Hold left mouse + drag to look',{exact:true}).isVisible());
      before=await state();await drag('left',120,70);after=await state();
      check('automatic fallback can still look',Math.abs(after.yaw-before.yaw)>.1&&Math.abs(after.pitch-before.pitch)>.1);
      await p.evaluate(()=>{const c=document.querySelector('canvas');c.requestPointerLock=c.__request;});await p.keyboard.press('Digit1');await p.waitForTimeout(150);
      check('1 retries default mouse look after rejection',(await state()).locked);
      await p.keyboard.press('Digit2');await p.waitForTimeout(100);
      await p.getByRole('button',{name:'Walk',exact:false}).click();await p.waitForTimeout(150);
      check('Walk button also enables mouse look directly',(await state()).locked);
      await p.keyboard.press('Escape');await p.waitForTimeout(100);
      await p.getByRole('button',{name:'Field notes',exact:false}).click();
      await p.getByRole('button',{name:'Return to the apron',exact:true}).click();await p.waitForTimeout(150);
      check('apron reset closes notes and resumes first-person view',(await state()).locked&&dist((await state()).position,[0,1.72,3.1])<.01&&await p.locator('aside').count()===0);
      check('no runtime errors',errors.length===0,errors);
    }catch(e){errors.push(e.message);}
    return {browser,checks,errors,pass:errors.length===0};
  }
  const chrome=await run(page,'chrome');await page.goto('about:blank');if(!chrome.pass)return {chrome};
  const edgeBrowser=await page.context().browser().browserType().launch({channel:'msedge',headless:true});
  try{return {chrome,edge:await run(await edgeBrowser.newPage(),'edge')};}finally{await edgeBrowser.close();}
}
