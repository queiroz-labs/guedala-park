"""Execute no FreeCAD. Leitura da R51, sem alterar nem salvar a fonte."""
from pathlib import Path
import FreeCAD as App,json,hashlib
HERE=Path(__file__).resolve().parent
doc=App.getDocument('Guedala_Park_R51_Sem_estudo_tubular')
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def row(o):
 s=world(o);b=s.BoundBox
 return dict(name=o.Name,label=o.Label,box=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],volume_mm3=s.Volume)
body=[o for o in doc.getObject('Modulo019').Group if hasattr(o,'Shape') and not o.Shape.isNull() and o.ViewObject.Visibility]
lids=[doc.getObject(n) for n in ('BancoR43_Painel1','BancoR43_Painel2')]
contacts=[]
for lid in lids:
 a=world(lid);b=a.BoundBox
 for o in body:
  s=world(o);c=s.BoundBox
  if abs(c.ZMax-b.ZMin)>1e-6:continue
  dx=min(b.XMax,c.XMax)-max(b.XMin,c.XMin);dy=min(b.YMax,c.YMax)-max(b.YMin,c.YMin)
  if min(dx,dy)<=1e-6:continue
  moved=a.copy();moved.translate(App.Vector(0,0,-.001));area=moved.common(s).Volume/.001
  if area>1e-4:
   contacts.append(dict(lid=lid.Name,support=o.Name,area_mm2=area,
    rectangle_global_mm=[max(b.XMin,c.XMin),max(b.YMin,c.YMin),min(b.XMax,c.XMax),min(b.YMax,c.YMax)],
    method='Penetracao virtual0,001mm em copia; nao alterou a fonte.'))
structural_names=['Peca407','Peca408','PecaBancoR16','Peca406AtualR31',
 'PecaBancoR001','PecaBancoR002','PecaBancoR003','PecaBancoR004','PecaBancoR005']
structural_names += [o.Name for o in body if o.Name.startswith(('Ref_Apoio_B','Ref_Sarrafo'))]
wood=[doc.getObject(n) for n in structural_names]
internal=[];floor=[]
for i,o in enumerate(wood):
 a=world(o);b=a.BoundBox
 if abs(b.ZMin)<1e-7:floor.append(dict(name=o.Name,nominal_area_mm2=(b.XMax-b.XMin)*(b.YMax-b.YMin)))
 for p in wood[i+1:]:
  s=world(p);c=s.BoundBox
  overlaps=[min(b.XMax,c.XMax)-max(b.XMin,c.XMin),min(b.YMax,c.YMax)-max(b.YMin,c.YMin),min(b.ZMax,c.ZMax)-max(b.ZMin,c.ZMin)]
  if min(overlaps)<-1e-7:continue
  common=a.common(s)
  def bounds(q):
   v=q.BoundBox;return [v.XMin,v.YMin,v.ZMin,v.XMax,v.YMax,v.ZMax]
  ba,bc=bounds(a),bounds(s);face_area=0.
  for axis in range(3):
   if abs(overlaps[axis])>1e-6 or not all(overlaps[j]>1e-6 for j in range(3) if j!=axis):continue
   plane=max(ba[axis],bc[axis])
   fa=[f for f in a.Faces if abs(bounds(f)[axis+3]-bounds(f)[axis])<1e-6 and abs(bounds(f)[axis]-plane)<1e-6]
   fb=[f for f in s.Faces if abs(bounds(f)[axis+3]-bounds(f)[axis])<1e-6 and abs(bounds(f)[axis]-plane)<1e-6]
   face_area+=sum(x.common(y).Area for x in fa for y in fb)
  internal.append(dict(a=o.Name,b=p.Name,overlap_mm=overlaps,common_face_area_mm2=face_area,common_volume_mm3=common.Volume,
   state='face' if face_area>1e-6 else ('volume' if common.Volume>1e-6 else 'aresta/ponto')))
data=dict(cad=doc.FileName,sha256=hashlib.sha256(Path(doc.FileName).read_bytes()).hexdigest(),lids=[row(o) for o in lids],body=[row(o) for o in body],contacts=contacts,
 structural_names=structural_names,internal_interfaces=internal,floor_contacts=floor,
 nominal_floor_area_mm2=sum(r['nominal_area_mm2'] for r in floor))
(HERE/'Geometria_R51.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
result=dict(contacts=len(contacts),main_without_cleats=sum(not r['support'].startswith('Ref_Sarrafo') for r in contacts),source_unchanged=True)
