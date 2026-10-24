import sys,json,itertools,collections
from pathlib import Path
sys.path.append('C:/Users/Elias/AppData/Local/Programs/FreeCAD-1.1.4/lib')
import FreeCAD as App,Part
root=Path('C:/Users/Elias/Documents/PROJETOS/Guedala park')
d=App.openDocument(str(root/'guedala-park/01_Projeto/Modelo_FreeCAD/01_Atual/Auditoria_R32_2026-10-20/Guedala_Park_R32_Auditoria.FCStd'))
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
shapes={}
for o in native:
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();shapes[o.Name]=s
def bounds(s):
 b=s.BoundBox;return [round(v,4) for v in [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]]
modules={o.Name:[x.Name for x in native if x in o.OutListRecursive] for o in d.Objects if o.Name.startswith('Modulo') and o.TypeId=='App::Part'}
report={'native_count':len(native),'types':dict(collections.Counter(o.TypeId for o in native)),'invalid':[o.Name for o in native if not o.Shape.isValid()],'modules':{},'intermodule_hits':[]}
for n,parts in modules.items():
 c=Part.makeCompound([shapes[x] for x in parts]);report['modules'][n]={'label':d.getObject(n).Label,'parts':parts,'bounds':bounds(c)}
bank=Part.makeCompound([shapes[n] for n in modules['Modulo019']]+[shapes['Peca421']])
report['bank_with_backrest_bounds']=bounds(bank)
count=0
def overlaps(a,b):
 return all(min(getattr(a,k+'Max'),getattr(b,k+'Max'))-max(getattr(a,k+'Min'),getattr(b,k+'Min'))>0.00001 for k in 'XYZ')
for ma,mb in itertools.combinations(modules,2):
 for a in modules[ma]:
  ba=shapes[a].BoundBox
  for b in modules[mb]:
   count+=1
   if not overlaps(ba,shapes[b].BoundBox):continue
   v=shapes[a].common(shapes[b]).Volume
   if v>.1:report['intermodule_hits'].append({'modules':[ma,mb],'a':a,'b':b,'labels':[d.getObject(a).Label,d.getObject(b).Label],'volume_mm3':round(v,4),'bounds_a':bounds(shapes[a]),'bounds_b':bounds(shapes[b])})
report['intermodule_pairs']=count
(root/'tmp/auditoria_completa_r33.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='modules'},ensure_ascii=False))
