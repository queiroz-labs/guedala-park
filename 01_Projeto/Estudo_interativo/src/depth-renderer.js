// Offline WebGL rasterizer. Occlusion is resolved per pixel, not by average face depth.
class DepthRenderer {
  constructor(){
    this.canvas=document.createElement('canvas');
    this.gl=this.canvas.getContext('webgl',{alpha:true,antialias:true,preserveDrawingBuffer:true});
    if(!this.gl)throw new Error('WebGL indisponível');
    const gl=this.gl;
    const shader=(type,source)=>{const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(s));return s;};
    const program=gl.createProgram();
    gl.attachShader(program,shader(gl.VERTEX_SHADER,'attribute vec3 position; attribute vec4 color; varying vec4 tint; void main(){gl_Position=vec4(position,1.0);tint=color;}'));
    gl.attachShader(program,shader(gl.FRAGMENT_SHADER,'precision mediump float; varying vec4 tint; void main(){gl_FragColor=tint;}'));
    gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw new Error(gl.getProgramInfoLog(program));
    gl.useProgram(program);this.buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,this.buffer);
    for(const [name,size,offset] of [['position',3,0],['color',4,12]]){const p=gl.getAttribLocation(program,name);gl.enableVertexAttribArray(p);gl.vertexAttribPointer(p,size,gl.FLOAT,false,28,offset);}
    gl.enable(gl.DEPTH_TEST);gl.depthFunc(gl.LEQUAL);gl.disable(gl.CULL_FACE);
  }
  draw(ctx,faces,w,h,ratio,selected){
    const gl=this.gl;this.canvas.width=Math.round(w*ratio);this.canvas.height=Math.round(h*ratio);gl.viewport(0,0,this.canvas.width,this.canvas.height);
    gl.clearColor(0,0,0,0);gl.depthMask(true);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
    const opaque=[],transparent=[],edges=[];
    const vertex=(arr,p,c,a)=>arr.push(p[0]/w*2-1,1-p[1]/h*2,-p[2]/4096,...c,a);
    for(const f of faces){
      const light=f.normal[1]?1.04:.80+.11*f.normal[0]-.07*f.normal[2];
      const c=rgb(shade(f.c,light)).map(v=>v/255), a=f.alpha??1;
      const arr=a<.995?[]:opaque;
      for(let i=1;i<f.points.length-1;i++)for(const p of [f.points[0],f.points[i],f.points[i+1]])vertex(arr,p,c,a);
      if(a<.995)transparent.push({vertices:arr,depth:f.depth});
      if(a>.995){const stroke=rgb(selected&&f.id===selected?'#c17b37':shade(f.c,.74)).map(v=>v/255);for(let i=0;i<f.points.length;i++)for(const p of [f.points[i],f.points[(i+1)%f.points.length]])vertex(edges,[p[0],p[1],p[2]+.06],stroke,1);}
    }
    const upload=(v,mode)=>{if(!v.length)return;gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(v),gl.DYNAMIC_DRAW);gl.drawArrays(mode,0,v.length/7);};
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
