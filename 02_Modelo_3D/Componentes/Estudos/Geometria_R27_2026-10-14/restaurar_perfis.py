"""Restore two source-valid official shapes without the invalid spline conversion."""
from pathlib import Path
import json,hashlib,shutil
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
oldfile=(Path(__file__).resolve().parent / '../Manutencao_R26_2026-10-14/Guedala_Park_R26_Manutencao_Simples.FCStd').resolve()
sourcefile=(Path(__file__).resolve().parent / '../Montagem_R07_2026-10-14/Fonte_G2_BlUM.FCStd').resolve()
target=(Path(__file__).resolve().parent / 'Guedala_Park_R27_Geometria_Oficial.FCStd').resolve()
evidence=json.loads(((Path(__file__).resolve().parent / '../Pendencias_autonomas_2026-10-14/Equivalencia_perfis_G2.json').resolve()).read_text(encoding='utf-8'))
assert not evidence['errors'] and len(evidence['rows'])==2
assert all(r['native_new_valid'] and max(r['max_edge_sample_distance_mm'],r['max_face_sample_distance_mm'])<1e-8 for r in evidence['rows'])
assert not target.exists()
oldhash=hashlib.sha256(oldfile.read_bytes()).hexdigest()
assert oldhash=='94b8e59708276190908f7e66f5b5cb701b1a7d003c05b03d685c25bee1a7bb5f'
shutil.copy2(oldfile,target)
src=App.openDocument(str(sourcefile));d=App.openDocument(str(target))
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def snapshot(o):
 return {'placement':list(o.Placement.toMatrix().A) if 'Placement' in o.PropertiesList else None,
         'expressions':list(o.ExpressionEngine) if 'ExpressionEngine' in o.PropertiesList else None,
         'parents':sorted(q.Name for q in o.InList if q.TypeId in ['App::Part','App::DocumentObjectGroup']),
         'visibility':o.ViewObject.Visibility,
         'linked':o.LinkedObject.Name if o.TypeId=='App::Link' else None}
before={o.Name:snapshot(o) for o in d.Objects}
mapping=App.Placement(App.Vector(600,18,3.5),App.Rotation(App.Vector(1,0,0),90))
report={'base':str(oldfile),'file':str(target),'official_source':str(sourcefile),'base_sha256_before':oldhash,'restored':[]}
names=['MontagemG2R007','MontagemG2R014']
for name in names:
 o=d.getObject(name);q=src.getObject(o.Fonte.split(' / ')[-1])
 assert not o.Shape.isValid() and q.Shape.isValid() and not o.ExpressionEngine
 old_world=shape(o);old_placement=list(o.Placement.toMatrix().A);old_status=o.Status
 new=q.Shape.copy();new.Placement=mapping.multiply(q.getGlobalPlacement())
 assert new.isValid()
 old_volume=o.Shape.Volume
 o.Shape=new
 o.Status='Representação oficial restaurada R27: evita conversão geométrica B-spline inválida da R07. Superfícies/envelope/posição física mantidos; perfil estático, não telescópio. Contatos internos/fundo, carga/fixação/tolerâncias permanecem pendentes; sem corte/furação/compra.'
 d.recompute()
 new_world=shape(o)
 assert len(old_world.Vertexes)==len(new_world.Vertexes)
 delta=max((a.Point-b.Point).Length for a,b in zip(old_world.Vertexes,new_world.Vertexes))
 assert delta<1e-8,(name,delta)
 a=old_world.optimalBoundingBox();b=new_world.optimalBoundingBox()
 bd=max(abs(getattr(a,k)-getattr(b,k)) for k in ['XMin','YMin','ZMin','XMax','YMax','ZMax'])
 assert bd<1e-5,(name,bd)
 assert o.Shape.isValid()
 report['restored'].append({'name':name,'source':q.Name,'native_valid_before':False,'native_valid_after':True,
  'old_local_matrix':old_placement,'new_local_matrix':list(o.Placement.toMatrix().A),
  'max_world_vertex_difference_mm':delta,'max_optimal_world_bbox_difference_mm':bd,
  'old_reported_volume_mm3':old_volume,'official_reported_volume_mm3':o.Shape.Volume,
  'reported_volume_difference_mm3':o.Shape.Volume-old_volume,'old_status':old_status,
  'note':'Local Placement now retains the official rigid transform instead of baking it into spline surfaces; geometry in apartment remains at the same coordinates. Volume integration differs from old invalid representation; no material was deliberately added or removed.'})
changes=[]
for name,previous in before.items():
 keys=[k for k,v in snapshot(d.getObject(name)).items() if v!=previous[k]]
 if keys:
  assert name in names and keys==['placement'],(name,keys)
  changes.append({'name':name,'fields':keys})
assert len(changes)==2 and len(d.Objects)==len(before)
assert not [o.Name for o in d.Objects if 'Invalid' in o.State]
assert float(d.getObject('ControleLoopManutencaoR26').Afastamento)==0
d.Label='Guedala Park — R27 — representação oficial dos perfis'
d.save()
assert hashlib.sha256(oldfile.read_bytes()).hexdigest()==oldhash
report.update(objects=len(d.Objects),all_other_placements_expressions_parents_visibility_links_preserved=True,changes=changes,
 sha256=hashlib.sha256(target.read_bytes()).hexdigest(),base_sha256_after=oldhash,invalid=[],
 limits='Two fixed profile representations only. No new hardware, shifted physical geometry, cutout, shape healing/tolerance modification, capacity, telescope or resolution of previously unknown STEP overlaps.')
((Path(__file__).resolve().parent / 'Restauracao_R27.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
App.closeDocument(src.Name);App.setActiveDocument(d.Name)
result={'file':str(target),'restored':report['restored'],'objects':len(d.Objects),'invalid':[]}
