import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {blocked,move,floorHeight} from '../src/physics.js';
const m=JSON.parse(readFileSync(new URL('../public/assets/complete.json',import.meta.url)));
const doors=m.doors.map(d=>({...d,amount:1}));
function route(points){
  for(let i=1;i<points.length;i++){
    const [a,b]=[points[i-1],points[i]],n=Math.ceil(Math.hypot(b[0]-a[0],b[1]-a[1])/.04);
    for(let j=0;j<=n;j++){
      const x=a[0]+(b[0]-a[0])*j/n,z=a[1]+(b[1]-a[1])*j/n;
      assert.equal(blocked(x,z,m.colliders,doors,m.bounds),false,`segment ${i}: ${x.toFixed(2)}, ${z.toFixed(2)}`);
    }
    const p={x:a[0],z:a[1]};move(p,b[0]-a[0],b[1]-a[1],m.colliders,doors,m.bounds);
    assert.ok(Math.hypot(p.x-b[0],p.z-b[1])<.01);
  }
}
test('complete route enters both furnished rooms and exits at rear',()=>{
  route([[0,3],[0,-1.5],[-2.78,-1.5],[-2.78,-3.55],[0,-3.55],[.3,-5.35],[0,-6.85],[-2.25,-6.85],[-2.25,-12.8],[-2.25,-6.85],[0,-6.85],[2.2,-6.85],[2.2,-13.6],[2.2,-6.85],[0,-6.85],[0,-14.5],[0,-17.7],[4.8,-17.7],[4.8,2.8],[0,2.8]]);
});
test('rear and side furnishings stop movement while site boundary is constrained',()=>{
  assert.ok(blocked(-3.08,-10.2,m.colliders,1,m.bounds));
  assert.ok(blocked(2.92,-10.6,m.colliders,1,m.bounds));
  assert.ok(blocked(0,6,m.colliders,1,m.bounds));
  assert.ok(blocked(0,-23,m.colliders,1,m.bounds));
});
test('rear steps descend to site and side paths stay at ground level',()=>{
  assert.equal(floorHeight(0,-14,true),.18);
  assert.equal(floorHeight(0,-16,true),.18);
  assert.equal(floorHeight(0,-16.85,true),.09);
  assert.equal(floorHeight(0,-17.4,true),.04);
  assert.equal(floorHeight(4.8,-8,true),.04);
});
