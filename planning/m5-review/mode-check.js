// Historical pre-review controls. Use controls-review-check.js for the current UI.
async (page) => {
  const out='C:/Users/brian/Documents/Blender/Creepy-Building-Myrtle-Beach-Highway-v2/planning/m5-review';
  async function run(p,browser){
    const checks=[],errors=[];p.on('pageerror',e=>errors.push(e.message));
    const check=(name,pass,evidence)=>{checks.push({name,pass,evidence});if(!pass)throw Error(name);};
    const state=()=>p.evaluate(()=>window.__M3.snapshot());
    const distance=(a,b)=>Math.hypot(...a.map((v,i)=>v-b[i]));
    const drag=async(dx,dy)=>{await p.mouse.move(850,480);await p.mouse.down();await p.mouse.move(850+dx,480+dy,{steps:12});await p.mouse.up();await p.waitForTimeout(100);};
    try{
      await p.setViewportSize({width:1920,height:1080});await p.goto('http://127.0.0.1:5173/?qa=1');await p.waitForFunction(()=>window.__M3);
      // Exercise a rejected initial pointer-lock request, then drag fallback.
      await p.evaluate(()=>{const c=document.querySelector('canvas');c.__request=c.requestPointerLock;c.requestPointerLock=()=>Promise.reject(Error('QA denied capture'));});
      await p.getByRole('button',{name:'Explore the store',exact:false}).click();await p.waitForTimeout(100);
      check('capture rejection leaves usable fallback',await p.getByRole('button',{name:'Enable mouse look',exact:true}).isVisible()&&!(await state()).locked);
      let before=await state();await drag(110,-65);let after=await state();
      check('drag changes yaw and pitch without moving player',Math.abs(after.yaw-before.yaw)>.15&&Math.abs(after.pitch-before.pitch)>.1&&distance(after.position,before.position)<.01);
      await p.evaluate(()=>{const c=document.querySelector('canvas');c.requestPointerLock=c.__request;});
      await p.getByRole('button',{name:'Enable mouse look',exact:true}).click();await p.waitForTimeout(120);
      check('mouse capture can recover',(await state()).locked);
      before=await state();await p.mouse.move(1100,600);await p.waitForTimeout(100);check('captured mouse turns view',Math.abs((await state()).yaw-before.yaw)>.05);
      await p.keyboard.press('Escape');await p.waitForTimeout(100);check('Escape restores drag help',!(await state()).locked&&await p.getByRole('button',{name:'Enable mouse look',exact:true}).isVisible());
      await p.getByRole('button',{name:'Field notes',exact:false}).click();await p.getByRole('button',{name:'Return to the apron',exact:true}).click();
      await p.getByRole('button',{name:'Close field notes',exact:true}).click();
      for(const key of ['KeyA','KeyD','ArrowLeft','ArrowRight']){
        before=await state();await p.keyboard.down(key);await p.waitForTimeout(220);await p.keyboard.up(key);after=await state();
        check(`${key} moves after UI focus`,Math.abs(after.position[0]-before.position[0])>.35);
      }
      await p.keyboard.down('KeyW');await p.evaluate(()=>window.dispatchEvent(new Event('blur')));before=await state();await p.waitForTimeout(200);await p.keyboard.up('KeyW');
      check('blur clears held keys',distance((await state()).position,before.position)<.03);
      await p.evaluate(()=>{const input=document.createElement('input');input.id='qa-input';document.body.appendChild(input);input.focus();});
      before=await state();await p.keyboard.press('KeyW');await p.keyboard.press('Digit2');await p.waitForTimeout(100);
      check('editable controls keep their own input',(await state()).mode==='walk'&&distance((await state()).position,before.position)<.01);
      await p.evaluate(()=>document.getElementById('qa-input').remove());
      await p.evaluate(()=>window.__M3.aim([0,1.83,-6.85],[2,1.5,-8]));
      const saved=await state();
      for(let repeat=0;repeat<3;repeat++){
        await p.keyboard.down('KeyW');await p.keyboard.press('Digit2');await p.keyboard.up('KeyW');await p.waitForTimeout(100);
        check(`orbit enters and clears walking input ${repeat}`,(await state()).mode==='orbit'&&!(await state()).locked);
        const preserved=(await state()).walkingPosition;
        before=await state();await drag(130,60);after=await state();
        check(`orbit drag rotates ${repeat}`,distance(before.position,after.position)>1&&distance(after.walkingPosition,preserved)<.01);
        before=await state();await p.mouse.wheel(0,-300);await p.waitForTimeout(100);after=await state();
        check(`orbit wheel zooms ${repeat}`,distance(before.position,after.position)>1);
        before=await state();await p.keyboard.press('ArrowLeft');await p.keyboard.press('Equal');after=await state();
        check(`orbit keyboard rotates and zooms ${repeat}`,distance(before.position,after.position)>.5);
        const interaction=await p.evaluate(()=>window.__M3.operateTarget('door'));await p.keyboard.press('KeyE');
        check(`inspection input cannot operate doors ${repeat}`,interaction===false&&(await state()).door===0);
        await p.mouse.wheel(0,-20000);await p.waitForTimeout(100);after=await state();
        check(`orbit minimum distance bounded ${repeat}`,distance(after.position,after.inspectionTarget)>=14.999);
        await p.mouse.wheel(0,30000);await p.waitForTimeout(100);after=await state();
        check(`orbit maximum distance bounded ${repeat}`,distance(after.position,after.inspectionTarget)<=65.001);
        await p.keyboard.press('Digit3');await p.waitForTimeout(80);before=await state();
        check(`top-down enters ${repeat}`,before.mode==='top'&&Math.abs(before.pitch+Math.PI/2)<.001);
        await drag(120,85);after=await state();
        check(`top-down drag pans without tilting ${repeat}`,distance(before.position,after.position)>.5&&Math.abs(after.pitch+Math.PI/2)<.001);
        before=await state();await p.keyboard.press('ArrowRight');await p.keyboard.press('ArrowUp');await p.keyboard.press('Equal');after=await state();
        check(`top-down keyboard pans and zooms ${repeat}`,distance(before.position,after.position)>.1&&after.zoom>before.zoom);
        await p.mouse.wheel(0,-20000);await p.waitForTimeout(100);check(`top-down max zoom bounded ${repeat}`,(await state()).zoom<=4);
        await p.mouse.wheel(0,30000);await p.waitForTimeout(100);check(`top-down min zoom bounded ${repeat}`,(await state()).zoom>=.65);
        await p.keyboard.press('Digit1');await p.waitForTimeout(80);after=await state();
        check(`walking pose restored ${repeat}`,after.mode==='walk'&&distance(after.position,preserved)<.01&&Math.abs(after.yaw-saved.yaw)<.001&&Math.abs(after.pitch-saved.pitch)<.001,after.position);
      }
      for(const mode of ['Orbit','Top-down','Walk']){await p.getByRole('button',{name:mode,exact:false}).click();await p.waitForTimeout(100);check(`${mode} button works`,(await state()).mode==={Orbit:'orbit','Top-down':'top',Walk:'walk'}[mode]);}
      await p.setViewportSize({width:1280,height:800});await p.keyboard.press('Digit3');await p.waitForTimeout(150);check('resized top-down view remains valid',(await state()).viewport[0]===1280);
      await p.setViewportSize({width:1920,height:1080});await p.getByRole('button',{name:'Field notes',exact:false}).click();await p.getByRole('button',{name:'Return to the apron',exact:true}).click();
      check('apron reset exits inspection coherently',(await state()).mode==='walk'&&distance((await state()).position,[0,1.72,3.1])<.01);
      await p.getByRole('button',{name:'Close field notes',exact:true}).click();
      check('no runtime errors',errors.length===0,errors);
      await p.goto('http://127.0.0.1:5173/');await p.getByRole('button',{name:'Explore by dragging',exact:true}).waitFor({state:'visible'});
      check('normal URL exposes no QA API',await p.evaluate(()=>typeof window.__M3==='undefined'));
    }catch(e){errors.push(e.message);await p.screenshot({path:`out/${browser}-mode-failure.png`.replace('out/',out+'/')});}
    return {browser,checks,errors,pass:errors.length===0};
  }
  const chrome=await run(page,'chrome');await page.goto('about:blank');if(!chrome.pass)return {chrome};
  const edgeBrowser=await page.context().browser().browserType().launch({channel:'msedge',headless:true});
  try{return {chrome,edge:await run(await edgeBrowser.newPage(),'edge')};}finally{await edgeBrowser.close();}
}
