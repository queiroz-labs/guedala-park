import FreeCAD as A, FreeCADGui as G, Part, pathlib, shutil, hashlib, json
P=pathlib.Path(__file__).resolve().parent
source=P.parent/'Consolidacao_R42_2026-10-22/Guedala_Park_R42_Consolidado.FCStd'
target=P/'Guedala_Park_R43_Consolidado.FCStd'
expected='b30ae9ab9c82620ecdab26b2cfae589037954356d515b483b5b6849f76e4bc26'
assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
assert not target.exists(), 'R43 already exists; do not overwrite'
shutil.copy2(source,target)
d=A.openDocument(str(target));d.Label='Guedala Park R43 — gabinete de correr'
s=A.getDocument('Banheiro_Detalhamento_R02')
root=d.addObject('App::DocumentObjectGroup','BanheiroCorrerR43');root.Label='R43 — gabinete: portas de correr e frente removível'
root.addProperty('App::PropertyString','Status','Rastreabilidade');root.Status='Incorporado geometricamente; ferragens em envelope, resistência e hidráulica não liberadas para fabricação'
root.addProperty('App::PropertyString','Origem','Rastreabilidade');root.Origem='Detalhamento_R02; R42 preservada; fundo original sem recorte hidráulico'
ctrl=d.addObject('App::FeaturePython','BC43_Controle');root.addObject(ctrl)
for n,m in [('CursoEsquerda',268),('CursoDireita',233)]:
 ctrl.addProperty('App::PropertyFloatConstraint',n,'Movimento');setattr(ctrl,n,(0,0,m,1))
def copy(o,parent):
 if hasattr(o,'Group'):
  q=d.addObject('App::Part' if o.TypeId=='App::Part' else 'App::DocumentObjectGroup','BC43_'+o.Name)
  parent.addObject(q);q.Label=o.Label
  if hasattr(o,'Placement'):q.Placement=o.Placement
  for child in o.Group:
   if child.Name!='Fundo':copy(child,q)
 else:
  q=d.addObject('PartDesign::Feature','BC43_'+o.Name);parent.addObject(q);q.Label=o.Label;q.Shape=o.Shape.copy();q.Placement=o.Placement
  q.ViewObject.ShapeColor=o.ViewObject.ShapeColor;q.ViewObject.Transparency=o.ViewObject.Transparency
  if 'Natureza' in o.PropertiesList:q.addProperty('App::PropertyString','Natureza','Rastreabilidade');q.Natureza=o.Natureza
 return q
for n in ['Madeira','Fixacoes','Trilhos','Batentes','FolhaEsquerda','FolhaDireita']:copy(s.getObject(n),root)
for side,x,sign in [('Esquerda',2780,'+'),('Direita',3048,'-')]:d.getObject('BC43_Folha'+side).setExpression('Placement.Base.x',str(x)+sign+'BC43_Controle.Curso'+side)
ref=d.addObject('App::DocumentObjectGroup','BC43_Referencias');root.addObject(ref);ref.Label='HIPÓTESES OCULTAS — sifão, recorte e acesso; não executar'
for n in ['Hidraulica','Acesso','Fundo']:copy(s.getObject(n),ref)
def descendants(o):
 out=[o]
 for c in getattr(o,'Group',[]):out+=descendants(c)
 return out
for o in descendants(ref):o.ViewObject.Visibility=False
old=['Peca394','Peca395','Peca397','FolhaBanheiroR12','FolhaBanheiroR001','DobradicaComumR12','DobradicaComumR037','DobradicaComumR038','DobradicaComumR039']
hidden=[]
for n in old:
 o=d.getObject(n)
 for child in descendants(o):child.ViewObject.Visibility=False;hidden.append(child.Name)
 o.addProperty('App::PropertyString','StatusR43','Rastreabilidade');o.StatusR43='Histórico R42 oculto; substituído pelo conjunto BanheiroCorrerR43'
d.recompute();d.save()
(P/'Integracao.json').write_text(json.dumps({'source_sha256':expected,'hidden_original_objects':hidden,'objects':len(d.Objects),'new_objects':[o.Name for o in d.Objects if o.Name.startswith('BC43_')],'note':'4 dobradiças do banheiro substituídas. Quantitativos antigos R42 são históricos. Fundo original preservado sem recorte.'},ensure_ascii=False,indent=2),encoding='utf-8')
A.setActiveDocument(d.Name);G.activeDocument().activeView().viewAxonometric();G.activeDocument().activeView().fitAll();G.updateGui()
