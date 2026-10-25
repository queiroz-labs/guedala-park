"""Amostragem das frentes contra outros módulos e objetos correntes; não salva a fonte."""
import sys,json,hashlib
from pathlib import Path
sys.path.append('C:/Users/Elias/AppData/Local/Programs/FreeCAD-1.1.4/lib')
import FreeCAD as App,Part
root=Path('C:/Users/Elias/Documents/PROJETOS/Guedala park')
folder=root/'guedala-park/02_Modelo_3D/Componentes/Atual/Conferencia_R33_2026-10-20'
path=folder/'Guedala_Park_R33_Conferencia.FCStd'
sha=hashlib.sha256(path.read_bytes()).hexdigest()
d=App.openDocument(str(path))
roots={o.LinkedObject.Name for o in d.getObject('ApartamentoEspelhadoR20').OutListRecursive if o.TypeId=='App::Link' and o.LinkedObject and o.Visibility}
def active(o):
 seen=set()
 while o and o.Name not in seen:
  if o.Name in roots:return True
  seen.add(o.Name)
  if not o.Visibility:return False
  o=o.getParentGeoFeatureGroup() if hasattr(o,'getParentGeoFeatureGroup') else None
 return False
native=[o for o in d.Objects if o.isDerivedFrom('Part::Feature') and not o.Shape.isNull() and active(o)]
modules={o.Name:set(x.Name for x in native if x in o.OutListRecursive) for o in d.Objects if o.Name.startswith('Modulo') and o.TypeId=='App::Part'}
owner={n:m for m,names in modules.items() for n in names}
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
baseline={o.Name:world(o) for o in native}
poses={o.Name:str(o.getGlobalPlacement()) for o in native}
panels=[o for o in native if o.Shape.Volume>300000]
controls=[o for o in d.Objects if o.TypeId=='App::FeaturePython' and hasattr(o,'Abertura') and hasattr(o,'CursoEstudo') and abs(float(o.CursoEstudo)-86)<.001]
report={'source_sha256':sha,'samples_deg':[0,21.5,43,64.5,86],'controls':[],'hits':[], 'limits':'Amostragem de frentes, uma porta de cada vez, demais controles na pose salva. Contra outros módulos e objetos correntes. Exclui próprio módulo, ferragens internas, uso simultâneo, pessoas, movimento contínuo, modelos reais e medidas de campo.'}
for c in controls:
 initial=float(c.Abertura);row={'control':c.Name,'label':c.Label,'panels':[],'samples':[]}
 try:
  for angle in report['samples_deg'][1:]:
   c.Abertura=angle;d.recompute()
   moved=[o for o in panels if str(o.getGlobalPlacement())!=poses[o.Name]]
   if not row['panels']:row['panels']=[o.Name for o in moved]
   row['samples'].append(angle)
   for o in moved:
    s=world(o);b=s.BoundBox
    for other in native:
     if owner.get(other.Name)==owner.get(o.Name):continue
     a=baseline[other.Name];bb=a.BoundBox
     if not all(min(getattr(b,k+'Max'),getattr(bb,k+'Max'))-max(getattr(b,k+'Min'),getattr(bb,k+'Min'))>1e-5 for k in 'XYZ'):continue
     v=s.common(a).Volume
     if v>.1:report['hits'].append({'control':c.Name,'angle':angle,'panel':o.Name,'obstacle':other.Name,'obstacle_label':other.Label,'overlap_mm3':round(v,4)})
 finally:
  c.Abertura=initial;d.recompute()
 report['controls'].append(row)
 (root/'tmp/progresso_portas_r33.json').write_text(json.dumps({'completed':len(report['controls']),'total':len(controls),'hits':len(report['hits'])}),encoding='utf-8')
assert all(str(o.getGlobalPlacement())==poses[o.Name] for o in native)
App.closeDocument(d.Name)
assert hashlib.sha256(path.read_bytes()).hexdigest()==sha
report['source_unchanged']=True;report['poses_restored']=True
(folder/'Portas_amostragem_R33.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'controls':len(controls),'unmapped':[r['control'] for r in report['controls'] if not r['panels']],'hits':report['hits']}))

