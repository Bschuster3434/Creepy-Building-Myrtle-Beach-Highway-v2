export const RADIUS = .25;

export function circleBox(x, z, box, radius = RADIUS) {
  const dx = Math.max(box.min[0] - x, 0, x - box.max[0]);
  const dz = Math.max(box.min[2] - z, 0, z - box.max[2]);
  return dx * dx + dz * dz < radius * radius;
}

export function circleSegment(x, z, a, b, radius = RADIUS + .04) {
  const dx = b[0] - a[0], dz = b[1] - a[1];
  const t = Math.max(0, Math.min(1, ((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz || 1)));
  return Math.hypot(x-a[0]-t*dx,z-a[1]-t*dz) < radius;
}

export function doorSegments(amount) {
  if(Array.isArray(amount)) return amount.map(d=>{
    const angle=d.closedAngle+d.swingAngle*d.amount;
    return [d.hinge,[d.hinge[0]+d.width*Math.cos(angle),d.hinge[1]-d.width*Math.sin(angle)],d.halfThickness];
  });
  // Coordinates are exported Blender meters mapped to Three.js X/Z.
  const left = amount * 95 * Math.PI / 180;
  const right = Math.PI - amount * 95 * Math.PI / 180;
  return [
    [[-.7,-.305],[-.7+.7*Math.cos(left),-.305-.7*Math.sin(left)]],
    [[.7,-.305],[.7+.7*Math.cos(right),-.305-.7*Math.sin(right)]],
  ];
}

export function blocked(x,z,colliders,doorAmount,bounds={minX:-5,maxX:5,maxZ:4.5,minZ:-15.3}) {
  if (x < bounds.minX || x > bounds.maxX || z > bounds.maxZ || z < bounds.minZ) return true;
  if (colliders.some(b => b.max[1] > .26 && b.min[1] < 1.98 && circleBox(x,z,b))) return true;
  return doorSegments(doorAmount).some(([a,b,thickness=.04])=>circleSegment(x,z,a,b,RADIUS+thickness));
}

export function move(position,dx,dz,colliders,doorAmount,bounds) {
  // Substep even long frames; sliding is checked on each axis.
  const steps=Math.max(1,Math.ceil(Math.hypot(dx,dz)/.06));
  for(let i=0;i<steps;i++) {
    if(!blocked(position.x+dx/steps,position.z,colliders,doorAmount,bounds)) position.x+=dx/steps;
    if(!blocked(position.x,position.z+dz/steps,colliders,doorAmount,bounds)) position.z+=dz/steps;
  }
  return position;
}

export function floorHeight(x,z,fullSite=false) {
  if(fullSite) {
    if(Math.abs(x)<=3.675 && z<=0 && z>=-15.30)return .18;
    if(Math.abs(x)<=.9 && z< -15.3 && z>=-16.68)return .18;
    if(Math.abs(x)<=.9 && z< -16.68 && z>=-17.06)return .09;
    if(z<0 || Math.abs(x)>4.675 || z>4.7)return .04;
  }
  // Approved apron, two shallow threshold steps, and level shop floor.
  if(z<=0) return .18;
  if(Math.abs(x)<=1.1 && z<=.4) return .18;
  if(Math.abs(x)<=1.1 && z<=.8) return .09;
  return .07;
}

export function canSwing(from,to,position,definition) {
  const n=Math.max(1,Math.ceil(Math.abs(to-from)/.015));
  for(let i=1;i<=n;i++) {
    const amount=from+(to-from)*i/n;
    const segments=doorSegments(definition?[{...definition,amount}]:amount);
    if(segments.some(([a,b,thickness=.04])=>circleSegment(position.x,position.z,a,b,RADIUS+thickness+.005))) return false;
  }
  return true;
}
