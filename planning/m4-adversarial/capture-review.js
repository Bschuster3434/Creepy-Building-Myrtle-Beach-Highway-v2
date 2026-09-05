async(page)=>{
  await page.setViewportSize({width:1920,height:1080});
  await page.goto('http://127.0.0.1:5173/?qa=1');
  await page.waitForFunction(()=>window.__M3);
  await page.getByRole('button',{name:'Explore by dragging'}).click();
  const views=[
    ['passage-floor',[0,1.83,-11],[0,.3,-13.5]],
    ['switch',[0,1.83,-13],[0,1.4,-15]],
    ['right-wall',[6,1.8,-7.2],[3.68,1.5,-9]],
    ['trees',[11,2.5,9],[0,4,-12]],
    ['room-trim',[1.5,1.3,-11],[.9,.3,-12]],
    ['exterior',[17,3.1,14],[0,2,-6.2]],
    ['tally-mount',[-1.32,1.9,-14.85],[-2.2,1.75,-15.06]],
    ['ceiling-joint',[1.5,2.7,-13],[.9,3.08,-15.05]],
    ['side-vents',[3.9,.5,-11],[3.67,.32,-12.9]],
    ['room-switch',[-2,1.6,-6.4],[-2.12,1.4,-5.93]],
  ];
  for(const [name,p,t] of views){
    await page.evaluate(([p,t])=>window.__M3.inspect(p,t),[p,t]);
    await page.waitForTimeout(200);
    await page.screenshot({path:'C:/Users/brian/Documents/Blender/Creepy-Building-Myrtle-Beach-Highway-v2/planning/m4-adversarial/after-'+name+'.png'});
  }
  return {views:views.length,snapshot:await page.evaluate(()=>window.__M3.snapshot())};
}
