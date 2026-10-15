from pathlib import Path
import json,shutil
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve();p=(Path(__file__).resolve().parent / 'Guedala_Park_R17_Equipamentos.FCStd').resolve()
d=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==p)
old_report=(Path(__file__).resolve().parent / 'Conferencia_R17.json').resolve();backup=(Path(__file__).resolve().parent / 'Conferencia_pre_rodabanca.json').resolve()
assert not backup.exists(), 'Correção já aplicada'
shutil.copy2(old_report,backup);a=json.loads(old_report.read_text(encoding='utf-8'))
o=d.getObject('Peca140');assert abs(o.Placement.Base.y-6480)<1e-6
pl=o.Placement;pl.Base.y=6460;o.Placement=pl
o.StatusR17='Proposta: avançar70 desde R16; rearY6880 deixa100 até frente da rodabancaY6980 e120 até paredeY7000. FrenteY6460 fica540 da parede e90 antes da pedra630. X/altura/modelo preservados. Água/tomada/pega/calor/exemplar reais pendentes; sem corte/furação/compra.'
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def bb(s):
 b=s.optimalBoundingBox();return [b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength,b.ZLength]
targets=[(d.getObject(n),shape(d.getObject(n))) for n in dict.fromkeys(a['targets'])]
def hits(s):
 b=s.optimalBoundingBox();out=[]
 for t,q in targets:
  if b.intersect(q.optimalBoundingBox()):
   v=s.common(q).Volume
   if v>1e-3:out.append({'name':t.Name,'label':t.Label,'volume_mm3':v})
 return out
changed=[]
for r in a['zones']:
 if r['label'].startswith('PE12G'):
  z=d.getObject(r['name']);pl=z.Placement;pl.Base.y-=20;z.Placement=pl
  z.StatusR17='Reserva documental livre no subconjunto estacionário após proposta70; traseira mede até rodabanca, não apenas parede. Fixação/conexões/fluxo/pega/instalação não homologados.'
  changed.append(z)
d.recompute()
for z in changed:
 r=next(r for r in a['zones'] if r['name']==z.Name)
 r['bbox']=bb(shape(z));r['hits']=hits(shape(z));r['valid']=z.Shape.isValid()
 assert not r['hits'], str(r)
new_path=Part.makeBox(160,490,350,App.Vector(5520,6460,920))
a['corrections']['purifier_swept_envelope_hits']=hits(new_path)
a['corrections']['purifier_body_hits']=hits(shape(o));assert not a['corrections']['purifier_swept_envelope_hits'] and not a['corrections']['purifier_body_hits']
a['current_bboxes']['Peca140']=bb(shape(o))
a['rodabanca_correction']={'initial_R16_y':6530,'first_proposal_y':6480,'final_y':6460,'total_advance':70,'rodabanca_y':6980,'rear_y':6880,'rear_clearance':100,'front_to_stone':90,'first_result':'Reserva100 até parede colidia com rodabanca Peca141. Primeira auditoria preservada em Conferencia_pre_rodabanca.json.'}
old_report.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf-8')
d.recompute();d.save();assert d.isSaved() and o.Shape.isValid()
result={'file':str(p),'correction':a['rodabanca_correction'],'new_zones':len(changed),'hits':a['corrections']}
