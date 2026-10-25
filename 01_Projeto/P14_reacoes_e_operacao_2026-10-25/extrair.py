"""Somente leitura da R51: centros e volumes BREP, sem mover controladores."""
from pathlib import Path
import json,hashlib
import FreeCAD as App
HERE=Path(__file__).resolve().parent
doc=App.getDocument('Guedala_Park_R51_Sem_estudo_tubular')
control=doc.getObject('ControleCestoR15')
assert abs(control.Abertura.Value)<1e-8 and abs(control.RetiradaConjunto.Value)<1e-8
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def record(name):
 o=doc.getObject(name);s=world(o);b=s.BoundBox;ss=s.Solids
 v=sum(a.Volume for a in ss);cg=sum((a.CenterOfMass*a.Volume for a in ss),App.Vector())/v
 return dict(name=name,label=o.Label,volume_mm3=v,center_mm=[cg.x,cg.y,cg.z],
  visible_local=o.ViewObject.Visibility,parents=[p.Name for p in o.InList],
  included_in_moving_wood_baseline=name in [f'PecaCestoR{i:03d}' for i in range(3,17)],
  box_mm=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax])
names=[f'PecaCestoR{i:03d}' for i in range(3,22)]
names+=['Peca352','Peca353','Peca354','PecaCestoR15','ApoioCestoC01R31','ApoioCestoC02R31','ApoioCestoC03R31']
data=dict(cad=doc.FileName,sha256=hashlib.sha256(Path(doc.FileName).read_bytes()).hexdigest(),
 source_pose_deg=control.Abertura.Value,source_translation_mm=control.RetiradaConjunto.Value,
 parts=[record(n) for n in names],scope='Frente e13 pecas da armacao sao geometria-gabarito. Pinos/apoios nao sao componentes comerciais dimensionados. Massas reais pendentes.')
(HERE/'Geometria_R51.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
result=dict(parts=len(names),frame_volume_mm3=sum(r['volume_mm3'] for r in data['parts'] if r['name'] in [f'PecaCestoR{i:03d}' for i in range(4,17)]),source_unchanged=True)
