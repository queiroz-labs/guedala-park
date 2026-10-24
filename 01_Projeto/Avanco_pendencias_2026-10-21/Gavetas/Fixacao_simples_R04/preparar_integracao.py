import FreeCAD as A, FreeCADGui as G, pathlib, shutil, hashlib, json
ROOT=pathlib.Path(__file__).resolve().parent
src=A.getDocument('Guedala_Park_R42_Consolidado')
study=next(d for d in A.listDocuments().values() if d.FileName.endswith('Escritorio_fixacao_simples_R04_ESTUDO.FCStd'))
for n in ['Gaveta008','Gaveta009']:study.getObject('Caixa_'+n).Extensao=0
study.recompute()
target=ROOT/'Guedala_Park_R42_PREVIA_R04_NAO_APROVADA.FCStd'
shutil.copyfile(src.FileName,target)
d=A.openDocument(str(target));d.Label='PRÉVIA R42 + R04 — NÃO APROVADA; principal preservado'
hidden=[]
def hide(o):
 if o.Name in hidden:return
 hidden.append(o.Name)
 for c in getattr(o,'Group',[]):hide(c)
 o.Visibility=False
hide(d.getObject('Modulo015'))
root=d.addObject('App::Part','Previa_R04_Gavetas');root.Label='PRÉVIA — escritório R04, engates FGVTN pendentes'
def copy(old,group):
 o=d.addObject('PartDesign::Feature','R04_'+old.Name);q=old.Shape.copy();q.Placement=old.getGlobalPlacement();o.Shape=q;o.Label=old.Label;group.addObject(o)
 o.ViewObject.ShapeColor=old.ViewObject.ShapeColor;o.ViewObject.Transparency=old.ViewObject.Transparency
 return o
car=d.addObject('App::DocumentObjectGroup','R04_Carcaca');root.addObject(car)
for o in study.getObject('Carcaca_470x248').Group:copy(o,car)
for n in ['Gaveta008','Gaveta009']:
 g=d.addObject('App::Part','R04_Caixa_'+n);root.addObject(g);g.addProperty('App::PropertyLength','Extensao');g.Extensao=0;g.setExpression('Placement.Base.y','Extensao')
 for o in study.getObject('Caixa_'+n).Group:copy(o,g)
root.addProperty('App::PropertyString','Status');root.Status='PRÉVIA NÃO APROVADA: montagem sem engates FGVTN dimensionados. Não fabricar. R42 principal intacta.'
root.addProperty('App::PropertyString','FonteAuditoria');root.FonteAuditoria=str(ROOT/'Auditoria_R04.json')
d.recompute()
changes=[];verified=0
for old in src.Objects:
 new=d.getObject(old.Name)
 assert new is not None
 if not hasattr(old,'Group') and hasattr(old,'Shape') and not old.Shape.isNull() and old.Shape.Solids:
  verified+=1
  if abs(old.Shape.Volume-new.Shape.Volume)>.001 or len(old.Shape.Faces)!=len(new.Shape.Faces) or str(old.getGlobalPlacement())!=str(new.getGlobalPlacement()):changes.append(old.Name)
assert not changes
d.save()
r={'status':'PREVIA_COMPLETA_NAO_APROVADA','main_modified':False,'main_sha256':hashlib.sha256(pathlib.Path(src.FileName).read_bytes()).hexdigest(),
 'preview_file':str(target),'preview_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'original_solid_objects_compared':verified,
 'original_geometry_changes':changes,'original_office_objects_hidden':hidden,'new_root':root.Name,'reason_not_incorporated':'Exact FGVTN clip/rail interface still not validated. User conditioned main incorporation on all checks being correct.'}
assert r['main_sha256']=='b30ae9ab9c82620ecdab26b2cfae589037954356d515b483b5b6849f76e4bc26'
(ROOT/'Integracao_preparada.json').write_text(json.dumps(r,indent=2,ensure_ascii=False),encoding='utf-8')
G.activeDocument().activeView().viewAxonometric();G.activeDocument().activeView().fitAll();G.updateGui()
