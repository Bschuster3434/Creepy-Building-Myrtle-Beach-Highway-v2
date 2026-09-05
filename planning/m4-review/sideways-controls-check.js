async(page)=>{
  const checks=[];
  const check=(name,pass,evidence)=>{checks.push({name,pass,evidence});if(!pass)throw Error(name+': '+JSON.stringify(evidence));};
  await page.goto('http://127.0.0.1:5173/?qa=1');await page.waitForFunction(()=>window.__M3);
  const position=()=>page.evaluate(()=>window.__M3.snapshot().position);
  const hold=async(key)=>{await page.keyboard.down(key);await page.waitForTimeout(350);await page.keyboard.up(key);return position();};
  for(const [key,sign] of [['KeyA',-1],['KeyD',1],['ArrowLeft',-1],['ArrowRight',1]]){
    await page.evaluate(()=>window.__M3.reset());const p=await hold(key);
    check(key+' moves sideways',p[0]*sign>.45&&Math.abs(p[2]-3.1)<.03,p);
  }
  await page.getByRole('button',{name:'Field notes'}).click();
  await page.getByRole('button',{name:'Return to the apron'}).click();
  check('return to apron focuses the view',await page.evaluate(()=>document.activeElement.tagName==='CANVAS'));
  check('right arrow works after return to apron',(await hold('ArrowRight'))[0]>.45);
  await page.evaluate(()=>window.__M3.reset());
  await page.getByRole('button',{name:'Return to the apron'}).focus();
  check('focused UI button does not block A',(await hold('KeyA'))[0]<-.45);
  await page.getByRole('button',{name:'Close field notes'}).click();
  await page.evaluate(()=>window.__M3.aim([0,1.72,3.1],[5,1.72,3.1]));
  const rotated=await hold('KeyD');
  check('sideways movement follows the view direction',rotated[2]>3.55&&Math.abs(rotated[0])<.03,rotated);
  await page.evaluate(()=>window.__M3.reset());await page.keyboard.down('KeyD');await page.waitForTimeout(150);
  await page.evaluate(()=>{const input=document.createElement('input');input.id='qa-input';document.body.appendChild(input);input.focus();});
  await page.keyboard.up('KeyD');const released=await position();await page.waitForTimeout(200);
  check('keyup clears movement after focus changes',Math.abs((await position())[0]-released[0])<.03);
  const typed=await hold('KeyA');check('text inputs retain their keys',Math.abs(typed[0]-released[0])<.03);
  await page.evaluate(()=>document.getElementById('qa-input').remove());
  await page.getByRole('button',{name:'Explore the store'}).click();await page.waitForTimeout(100);
  check('mouse capture still enters',await page.evaluate(()=>window.__M3.snapshot().locked));
  await page.evaluate(()=>window.__M3.reset());check('D works with mouse captured',(await hold('KeyD'))[0]>.45);
  await page.evaluate(()=>document.exitPointerLock());await page.waitForTimeout(100);
  check('sideways help remains visible',await page.locator('.movement-help').isVisible());
  return {checks};
}
