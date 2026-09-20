// Offline WebGL rasterizer. Occlusion is resolved per pixel, not by average face depth.
class DepthRenderer {
  constructor(){
    this.canvas=document.createElement('canvas');
    this.gl=this.canvas.getContext('webgl',{alpha:true,antialias:true,preserveDrawingBuffer:true});
    if(!this.gl)throw new Error('WebGL indisponível');
    const gl=this.gl;
    const shader=(type,source)=>{const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(s));return s;};
    const program=gl.createProgram();
    gl.attachShader(program,shader(gl.VERTEX_SHADER,`attribute vec3 position; attribute vec4 color; attribute vec3 surface;
      varying vec4 tint; varying vec3 flooring;
      void main(){gl_Position=vec4(position,1.0);tint=color;flooring=surface;}`));
    const derivatives=gl.getExtension('OES_standard_derivatives');
    gl.attachShader(program,shader(gl.FRAGMENT_SHADER,`${derivatives?'#extension GL_OES_standard_derivatives : enable\n':''}
      precision highp float;
      varying vec4 tint; varying vec3 flooring;
      float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
      float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.0-2.0*f);
        return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);}
      void main(){
        vec3 c=tint.rgb;vec2 p=flooring.xy;
        if(flooring.z>0.5){
          vec2 aa=${derivatives?'max(fwidth(p),vec2(0.04))':'vec2(0.25)'};
          if(flooring.z<1.5){
            // World centimetres: continuous 20.845 x 123.03 cm planks, staggered by thirds.
            float row=floor(p.x/20.845),offset=mod(row,3.0)*41.01;
            vec2 cell=vec2(row,floor((p.y+offset)/123.03));
            vec2 q=vec2(mod(p.x,20.845),mod(p.y+offset,123.03));
            float seed=hash(cell),broad=noise(vec2(q.x*.38,q.y*.027)+seed*71.0);
            float bend=noise(vec2(q.x*.13,q.y*.021)+seed*39.0);
            float grain=noise(vec2(q.x*3.2+bend*3.0,q.y*.075)+seed*113.0);
            float fineFade=1.0-smoothstep(.15,1.1,aa.x);
            c*=.975+(seed-.5)*.065+(broad-.5)*.085+(grain-.5)*.055*fineFade;
            vec2 edge=min(q,vec2(20.845,123.03)-q);
            vec2 joint=1.0-smoothstep(vec2(0.0),aa*.8+vec2(.07),edge);
            c*=1.0-max(joint.x,joint.y)*.13;
          }else{
            // Both specified porcelain finishes use 90 x 90 cm modules.
            vec2 cell=floor(p/90.0),q=mod(p,90.0),edge=min(q,90.0-q);
            float seed=hash(cell),cloud=noise(p*.055+seed*21.0);
            float stone=noise(p*.22+seed*53.0);
            float veins=noise(vec2(p.x*.04,p.y*.18)+cloud*2.0);
            c*=.99+(seed-.5)*.025+(cloud-.5)*.045+(stone-.5)*.02;
            if(flooring.z<2.5)c*=1.0+(veins-.5)*.06;
            vec2 joint=1.0-smoothstep(vec2(.06),aa*.7+vec2(.12),edge);
            c=mix(c,tint.rgb*.85,max(joint.x,joint.y));
          }
        }
        gl_FragColor=vec4(c,tint.a);
      }`));
    gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw new Error(gl.getProgramInfoLog(program));
    gl.useProgram(program);this.buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,this.buffer);
    for(const [name,size,offset] of [['position',3,0],['color',4,12],['surface',3,28]]){const p=gl.getAttribLocation(program,name);gl.enableVertexAttribArray(p);gl.vertexAttribPointer(p,size,gl.FLOAT,false,40,offset);}
    gl.enable(gl.DEPTH_TEST);gl.depthFunc(gl.LEQUAL);gl.disable(gl.CULL_FACE);
  }
  draw(ctx,faces,w,h,ratio,selected){
    const gl=this.gl;this.canvas.width=Math.round(w*ratio);this.canvas.height=Math.round(h*ratio);gl.viewport(0,0,this.canvas.width,this.canvas.height);
    gl.clearColor(0,0,0,0);gl.depthMask(true);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
    const opaque=[],transparent=[],edges=[];
    const vertex=(arr,p,c,a,world=[0,0,0],surface=0)=>arr.push(p[0]/w*2-1,1-p[1]/h*2,-p[2]/4096,...c,a,world[0],world[2],surface);
    for(const f of faces){
      const light=f.normal[1]?1.04:.80+.11*f.normal[0]-.07*f.normal[2];
      const c=rgb(shade(f.c,light)).map(v=>v/255), a=f.alpha??1;
      const surface=floorStyle(f);
      const arr=a<.995?[]:opaque;
      for(let i=1;i<f.points.length-1;i++)for(const j of [0,i,i+1])vertex(arr,f.points[j],c,a,f.p?.[j],surface);
      if(a<.995)transparent.push({vertices:arr,depth:f.depth});
      if(a>.995&&!surface){const stroke=rgb(selected&&f.id===selected?'#c17b37':shade(f.c,.74)).map(v=>v/255);for(let i=0;i<f.points.length;i++)for(const p of [f.points[i],f.points[(i+1)%f.points.length]])vertex(edges,[p[0],p[1],p[2]+.06],stroke,1);}
    }
    const upload=(v,mode)=>{if(!v.length)return;gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(v),gl.DYNAMIC_DRAW);gl.drawArrays(mode,0,v.length/10);};
    gl.disable(gl.BLEND);gl.enable(gl.POLYGON_OFFSET_FILL);gl.polygonOffset(1,1);upload(opaque,gl.TRIANGLES);gl.disable(gl.POLYGON_OFFSET_FILL);
    upload(edges,gl.LINES);
    gl.enable(gl.BLEND);gl.blendFuncSeparate(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA,gl.ONE,gl.ONE_MINUS_SRC_ALPHA);gl.depthMask(false);
    transparent.sort((a,b)=>a.depth-b.depth);upload(transparent.flatMap(f=>f.vertices),gl.TRIANGLES);gl.depthMask(true);
    ctx.drawImage(this.canvas,0,0,w,h);
  }
}
let depthRenderer;
function renderDepth(ctx,faces,w,h,ratio,selected){
  if(depthRenderer===false)return false;
  try{depthRenderer??=new DepthRenderer();depthRenderer.draw(ctx,faces,w,h,ratio,selected);return true;}
  catch(e){depthRenderer=false;console.warn('Renderização simplificada disponível:',e.message);return false;}
}
