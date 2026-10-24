import FreeCAD as A, FreeCADGui as G, Part, pathlib, json, math, hashlib
out=pathlib.Path(__file__).parent
s=A.getDocument('Guedala_Park_R44_Consolidado')
def world(n):
 o=s.getObject(n);q=o.Shape.copy();q.Placement=o.getGlobalPlacement();return q
back=world('Peca421')
lids=[world(n) for n in ['BancoR43_Painel1','BancoR43_Painel2']]
d=A.newDocument('Rockler_Fixacao_R46_TESTE')
d.Label='Rockler R46 — teste de eixos, NÃO é CAD da ferragem'
def add(n,q,c,t=0):
 o=d.addObject('PartDesign::Feature',n);o.Shape=q;o.ViewObject.ShapeColor=c;o.ViewObject.Transparency=t;return o
for n in ['Peca421','Peca408','PecaBancoR007AtualR31']:
 add(n,world(n),(.65,.6,.5),60)
for i,q in enumerate(lids):add('Tampa_Fechada_'+str(i+1),q,(.3,.65,.8),65)
cases=[]
for idx,lid in enumerate(lids):
 for ax in [100,118,140,160,180,200,201]:
  az=400
  theta=math.degrees(math.atan2(20,ax-102)) if ax>102 else 45
  angles=sorted(set(list(range(91))+[min(90,max(0,theta))]))
  hits=[]
  for ang in angles:
   q=lid.copy();q.rotate(A.Vector(ax,0,az),A.Vector(0,-1,0),ang)
   vol=q.common(back).Volume if q.BoundBox.intersect(back.BoundBox) else 0
   if vol>1e-5:hits.append({'angulo':ang,'volume_mm3':vol})
  cases.append({'tampa':idx+1,'eixo_x':ax,'eixo_z':az,'poses':len(angles),'colisoes':len(hits),'primeira':hits[0] if hits else None,'x_min_analitico':ax-math.hypot(ax-102,20) if ax>102 else None})
  if ax==160:
   q=lid.copy();q.rotate(A.Vector(ax,0,az),A.Vector(0,-1,0),theta)
   add('Tampa_'+str(idx+1)+'_Hipotese_X160',q,(.9,.25,.15),30)
   hit=q.common(back)
   if hit.Volume>0:add('Colisao_'+str(idx+1),hit,(1,0,0))
meta=d.addObject('App::FeaturePython','LeiaMe')
for key,val in {'Limite':'Eixos hipotéticos favoráveis em Z400; não representam a geometria exata Rockler. Teste suficiente para rejeitar fixação local junto à traseira.', 'Criterio':'Eixo sob tampa: Z<=400. Para não entrar em X<100 durante 0-90°, X>=201 em Z400. Tangência sem folga em X201.', 'Fonte':s.FileName,'Preservacao':'Tampas e original R44 não alterados; só cópias no estudo.'}.items():
 meta.addProperty('App::PropertyString',key);setattr(meta,key,val)
d.recompute();G.activeDocument().activeView().viewAxonometric();G.activeDocument().activeView().fitAll()
d.saveAs(str(out/'Rockler_Fixacao_TESTE.FCStd'))
data={'fonte_sha256':hashlib.sha256(pathlib.Path(s.FileName).read_bytes()).hexdigest(),'eixos_hipoteticos_nao_CAD_ferragem':True,'casos':cases,'limite_x_z400_mm':201,'formula':'X >= 101 + (420-Z)^2/4, para Z<=400 e X>102; contato com X100, sem margem','dimensoes_tampas_preservadas':True}
(out/'Teste_fixacao.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
result=data
