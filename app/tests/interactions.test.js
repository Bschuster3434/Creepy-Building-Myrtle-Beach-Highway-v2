import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {blocked,move,canSwing,doorSegments} from '../src/physics.js';
const m=JSON.parse(readFileSync(new URL('../public/assets/complete.json',import.meta.url)));
const pose=(control,amount)=>m.doors.map(d=>({...d,amount:d.control===control?amount:1}));
const crossings={door:[[0,1],[0,-1.5]],cratesDoor:[[0,-6.85],[-2.1,-6.85]],packingDoor:[[0,-6.85],[2.1,-6.85]],rearDoor:[[0,-14.4],[0,-17.5]]};

for(const [control,[a,b]] of Object.entries(crossings)){
  test(`${control}: closed collision stops both directions and open allows both directions`,()=>{
    for(const [start,end] of [[a,b],[b,a]]){
      for(const amount of [0,1]){
        const p={x:start[0],z:start[1]};
        move(p,end[0]-p.x,end[1]-p.z,m.colliders,pose(control,amount),m.bounds);
        const error=Math.hypot(p.x-end[0],p.z-end[1]);
        assert.ok(amount?error<.01:error>.3,`${control} amount ${amount}: ${JSON.stringify(p)}`);
      }
    }
  });
}

test('each leaf has matching collision at 101 poses and rejects opening/closing through the body',()=>{
  for(const d of m.doors){
    for(let i=0;i<=100;i++){
      const [[a,b]]=doorSegments([{...d,amount:i/100}]);
      const p={x:(a[0]+b[0])/2,z:(a[1]+b[1])/2};
      assert.ok(blocked(p.x,p.z,[],[{...d,amount:i/100}],m.bounds));
      assert.equal(canSwing(0,1,p,d),false);
      assert.equal(canSwing(1,0,p,d),false);
    }
    assert.ok(canSwing(0,1,{x:8,z:4},d));
  }
});

test('stale open-leaf colliders are absent and each opening has its own control',()=>{
  assert.equal(m.doors.length,5);
  assert.equal(new Set(m.doors.map(d=>d.control)).size,4);
  assert.equal(m.circuits.length,4);
  assert.ok(!m.colliders.some(c=>/^D0[234]_.*leaf$|^Door_cross_rail|^Door_lever/.test(c.name)));
});

test('long diagonal movement cannot tunnel through an animating door',()=>{
  for(const d of m.doors){
    for(const amount of [.2,.5,.8]){
      const [[a,b]]=doorSegments([{...d,amount}]);
      const mx=(a[0]+b[0])/2,mz=(a[1]+b[1])/2;
      const dx=(b[1]-a[1])/d.width,dz=-(b[0]-a[0])/d.width;
      const p={x:mx+dx,z:mz+dz};
      move(p,-2*dx,-2*dz,[],[{...d,amount}],m.bounds);
      assert.ok((p.x-mx)*dx+(p.z-mz)*dz>0);
    }
  }
});
