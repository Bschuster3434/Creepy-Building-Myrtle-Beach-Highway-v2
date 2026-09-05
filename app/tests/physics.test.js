import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {blocked,move,canSwing,floorHeight} from '../src/physics.js';
const {colliders}=JSON.parse(readFileSync(new URL('../public/assets/sample.json',import.meta.url)));
test('closed pair stops entry; open pair admits the 0.50 m player',()=>{
  const closed={x:0,z:1};move(closed,0,-4,colliders,0);assert.ok(closed.z>-.3);
  const open={x:0,z:1};move(open,0,-2.8,colliders,1);assert.ok(open.z<-1.79);
});
test('substeps stop a long-frame move at walls and furniture',()=>{
  const p={x:0,z:-4};move(p,10,0,colliders,1);assert.ok(p.x<3);
  const q={x:0,z:-1};move(q,0,-8,colliders,1);assert.ok(q.z>-2.16 && q.z<-2.05,'service counter stops the customer at its front edge');
});
test('customer area connects around the counter left end to the serving side and passage',()=>{
  const route=[[0,3],[0,-1.5],[-2.78,-1.5],[-2.78,-3.55],[0,-3.55],[1.7,-3.55],[1.7,-4.15],[0,-4.15],[.3,-5.35],[0,-6.85],[0,-14.7]];
  for(let i=1;i<route.length;i++){
    const [a,b]=[route[i-1],route[i]];const n=Math.ceil(Math.hypot(b[0]-a[0],b[1]-a[1])/.05);
    for(let j=0;j<=n;j++)assert.equal(blocked(a[0]+(b[0]-a[0])*j/n,a[1]+(b[1]-a[1])*j/n,colliders,1),false,`route ${i} sample ${j}`);
  }
});
test('door swing refuses to sweep through player',()=>{
  assert.equal(canSwing(0,1,{x:-.4,z:-.7}),false);
  assert.equal(canSwing(1,0,{x:0,z:-.305}),false);
  assert.equal(canSwing(0,1,{x:0,z:1}),true);
});
test('threshold levels and sample boundary remain bounded',()=>{
  assert.equal(floorHeight(0,1),.07);assert.equal(floorHeight(0,.6),.09);assert.equal(floorHeight(0,.2),.18);assert.equal(floorHeight(0,-2),.18);
  assert.equal(blocked(0,-9,colliders,1),false);assert.ok(blocked(0,-15.3,colliders,1));assert.ok(blocked(6,0,colliders,1));
});
test('closer storeroom entrances connect to the continuous central passage',()=>{
  const route=[[0,-5.3],[0,-6.85],[-2.2,-6.85],[-2.2,-7.7],[-2.2,-6.85],[0,-6.85],[2.2,-6.85],[2.2,-7.7],[2.2,-6.85],[0,-6.85],[0,-14.7]];
  for(let i=1;i<route.length;i++){
    const [a,b]=[route[i-1],route[i]];const n=Math.ceil(Math.hypot(b[0]-a[0],b[1]-a[1])/.04);
    for(let j=0;j<=n;j++)assert.equal(blocked(a[0]+(b[0]-a[0])*j/n,a[1]+(b[1]-a[1])*j/n,colliders,1),false,`rear route ${i} sample ${j}`);
  }
  assert.ok(!colliders.some(c=>c.name.startsWith('Sample_passage')));
});
