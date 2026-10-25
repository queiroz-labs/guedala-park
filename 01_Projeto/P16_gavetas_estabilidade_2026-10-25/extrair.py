"""Leitura das gavetas fechadas; trajetorias por copias, sem mover o CAD."""
from pathlib import Path
import json,hashlib
import FreeCAD as App
HERE=Path(__file__).resolve().parent
doc=App.getDocument('Guedala_Park_R51_Sem_estudo_tubular')
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def row(o):
 s=world(o);b=s.BoundBox;v=sum(q.Volume for q in s.Solids)
 cg=sum((q.CenterOfMass*q.Volume for q in s.Solids),App.Vector())/v
 return dict(name=o.Name,label=o.Label,box_mm=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],volume_mm3=v,center_mm=[cg.x,cg.y,cg.z])
drawers=[]
for name in ('Gaveta008','Gaveta009'):
 o=doc.getObject(name);assert abs(o.Extensao.Value)<1e-8
 vector=o.getGlobalPlacement().Rotation.multVec(App.Vector(0,-o.CursoNominal.Value,0))
 p=[row(c) for c in o.Group if hasattr(c,'Shape') and not c.Shape.isNull()]
 drawers.append(dict(name=name,wood=p[:6],locks=p[6:],full_stroke_mm=o.CursoNominal.Value,
  translation_global_mm=[vector.x,vector.y,vector.z],
  properties={k:str(getattr(o,k)) for k in ['AlturaParedeSobreFundo','AlturaUtilProposta','VaoVerticalEstimado','CursoNominal']},
  physical_side_height_mm=p[0]['box_mm'][5]-p[0]['box_mm'][2],
  physical_back_above_bottom_height_mm=p[3]['box_mm'][5]-p[3]['box_mm'][2]))
data=dict(cad=doc.FileName,sha256=hashlib.sha256(Path(doc.FileName).read_bytes()).hexdigest(),
 drawers=drawers,fixed_original=[row(doc.getObject(n)) for n in ['Peca369','Peca370','Peca371','Peca110']],
 scope='Geometria nominal da R51. Guias STEP estaticas nao representam telescopio. Massas de ferragens/itens/equipamentos ainda nao pesadas.')
(HERE/'Geometria_R51.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
result=dict(drawers=[dict(name=r['name'],translation=r['translation_global_mm'],side=r['physical_side_height_mm'],back=r['physical_back_above_bottom_height_mm']) for r in drawers],source_unchanged=True)
