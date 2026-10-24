import FreeCAD as A, FreeCADGui as G, pathlib, json, hashlib
ROOT=pathlib.Path('C:/Users/Elias/Documents/PROJETOS/Guedala park')
OUT=ROOT/'guedala-park/01_Projeto/Estudo_dimensional_R45_2026-10-23'
p=OUT/'Gavetas_Banco_R45_ESTUDO.FCStd'
d=next(d for d in A.listDocuments().values() if d.FileName==str(p))
# Organize the standalone document for clear browsing, preserving hidden diagnostic groups.
if d.getObject('SetorBanco') is None:
 bank=d.addObject('App::DocumentObjectGroup','SetorBanco');bank.Label='01 — BANCO: tampas, espaço e referências'
 office=d.addObject('App::DocumentObjectGroup','SetorGavetas');office.Label='02 — GAVETAS: variante R04 e hipótese rejeitada'
 for o in list(d.Objects):
  if o.Name.startswith('Banco_'):bank.addObject(o)
  if o.Name in ['Escritorio_Carcaca','R45_Gaveta008','R45_Gaveta009'] or o.Name.startswith('Hipotese_'):office.addObject(o)
 office.Visibility=False
for gn in ['Banco_Pose90','Banco_Referencias_SlowMulti','SetorGavetas']:
 def hide(o):
  for c in getattr(o,'Group',[]):hide(c)
  o.Visibility=False
 hide(d.getObject(gn))
for o in d.getObject('Banco_Contexto').Group:o.ViewObject.Transparency=0
d.recompute();d.save()
before={o.Name:{'volume':o.Shape.Volume,'bbox':str(o.Shape.BoundBox)} for o in d.Objects if hasattr(o,'Shape') and not hasattr(o,'Group') and not o.Shape.isNull()}
A.closeDocument(d.Name);d=A.openDocument(str(p));d.recompute()
errors=[]
for n,v in before.items():
 o=d.getObject(n)
 if o is None or not o.Shape.isValid() or abs(o.Shape.Volume-v['volume'])>.01:errors.append(n)
data=json.loads((OUT/'Calculos_e_ensaios.json').read_text(encoding='utf8'))
source=pathlib.Path(data['source']);source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
assert source_hash==data['source_sha256_before']
assert not errors
data['study_objects']=len(d.Objects)
(OUT/'Calculos_e_ensaios.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
v={'source_unchanged':True,'source_sha256':source_hash,'study_reopened':True,'shape_objects_checked':len(before),'invalid_or_changed_shapes':errors,'study_objects':len(d.Objects),'study_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'tests':{'bank_poses':182,'bank_hits':len(data['bank_motion_hits']),'rail_sensitivity_cases':24,'rail_collision_free_cases':sum(not x['hits'] for x in data['office_R04']['rail_cases']),'cargo_envelope_hits':sum(len(x['hits']) for x in data['office_R04']['cargo'])}}
(OUT/'Verificacao.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
G.activeDocument().activeView().viewAxonometric();G.activeDocument().activeView().fitAll();G.updateGui()
result=v
