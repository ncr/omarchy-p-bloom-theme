// Portable, silent 24-second loop. Original image geometry and text never move.
// The animated light is clipped to the actual bright ink in the supplied image.
export const LOOP_SECONDS = 24;
export function createAmbient(host) {
  const canvas=document.createElement('canvas');canvas.className='ambient-ink';canvas.setAttribute('aria-hidden','true');
  Object.assign(canvas.style,{position:'absolute',inset:'0',width:'100%',height:'100%',pointerEvents:'none',mixBlendMode:'screen'});host.append(canvas);
  const ctx=canvas.getContext('2d'),mask=document.createElement('canvas'),ink=mask.getContext('2d');
  let generation=0,ready=false,spec=null,raf=0,previous=0,enabled=true;
  let audioLevels={active:false,bass:0,mids:0,highs:0};
  async function load(source,profile){
    const own=++generation;ready=false;ctx.clearRect(0,0,canvas.width,canvas.height);spec=profile;
    const image=new Image();image.src=source;
    try{await image.decode();}catch{return;}
    if(own!==generation)return;
    const w=1280,h=Math.round(w*image.naturalHeight/image.naturalWidth);
    canvas.width=mask.width=w;canvas.height=mask.height=h;
    ink.drawImage(image,0,0,w,h);const pixels=ink.getImageData(0,0,w,h);
    ink.filter='blur(5px)';ink.drawImage(image,0,0,w,h);ink.filter='none';const smooth=ink.getImageData(0,0,w,h);
    for(let i=0;i<pixels.data.length;i+=4){
      const a=pixels.data,b=smooth.data,delta=(a[i]+a[i+1]+a[i+2]-b[i]-b[i+1]-b[i+2])/3;
      a[i+3]=Math.min(160,Math.max(0,(delta-3)*6));
      a[i]=Math.min(255,a[i]*2.2);a[i+1]=Math.min(255,a[i+1]*2.2);a[i+2]=Math.min(255,a[i+2]*2.2);
    }
    ink.putImageData(pixels,0,0);ready=true;
  }
  function render(seconds){
    if(!ready||!enabled)return;
    const w=canvas.width,h=canvas.height,t=((seconds%LOOP_SECONDS)+LOOP_SECONDS)%LOOP_SECONDS;
    ctx.clearRect(0,0,w,h);ctx.globalCompositeOperation='source-over';
    for(const [i,s]of spec.spots.entries()){
      const phase=2*Math.PI*(t*s.cycles/LOOP_SECONDS+s.phase);
      const band=[audioLevels.bass,audioLevels.mids,audioLevels.highs][i%3]||0;
      const pulse=audioLevels.active?.05+.65*Math.pow(band,1.5):.14+.09*Math.sin(phase);
      const angle=2*Math.PI*t/LOOP_SECONDS+s.phase*2*Math.PI;
      const x=(s.x+(s.orbitX||0)*Math.cos(angle))*w,y=(s.y+(s.orbitY||0)*Math.sin(angle))*h;
      const radius=s.radius*w,g=ctx.createRadialGradient(x,y,0,x,y,radius);
      g.addColorStop(0,'rgba(255,255,255,'+pulse+')');g.addColorStop(.4,'rgba(255,255,255,'+(pulse*.55)+')');g.addColorStop(1,'rgba(255,255,255,0)');
      ctx.fillStyle=g;ctx.fillRect(x-radius,y-radius,radius*2,radius*2);
    }
    ctx.globalCompositeOperation='source-in';ctx.drawImage(mask,0,0);ctx.globalCompositeOperation='source-over';
  }
  function tick(now){if(now-previous>=1000/24){render(now/1000);previous=now;}raf=requestAnimationFrame(tick);}
  function start(){if(!raf)raf=requestAnimationFrame(tick);}
  function stop(){cancelAnimationFrame(raf);raf=0;}
  function setEnabled(value){enabled=value;canvas.hidden=!value;if(!value)stop();else start();}
  return {load,render,start,stop,setEnabled,setAudioLevels(value){audioLevels=value;},canvas,destroy(){stop();generation++;canvas.remove();}};
}
