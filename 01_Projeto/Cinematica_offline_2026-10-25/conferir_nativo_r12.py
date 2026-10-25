"""Referencia complementar R12, somente20 celulas necessarias e2 folhas.
Documento temporario proprio; a R51 nao e animada nem salva.
"""
from pathlib import Path
import json,re,hashlib
import FreeCAD as App
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/'Snapshot_R51.json').read_text(encoding='utf8'))
src=App.getDocument('Guedala_Park_R51_Sem_estudo_tubular');active=App.ActiveDocument.Name
assert hashlib.sha256(Path(src.FileName).read_bytes()).hexdigest()==d['sha256']
names=['FolhaBanheiroR002','FolhaBanheiroR003'];sheet='CinematicaComumR12';cells=d['sheets'][sheet]
aliases={r['alias']:a for a,r in cells.items() if r['alias']}
needed=set();queue=[]
for n in names:
 for expr in d['leaves'][n]['expressions'].values():queue.extend(aliases[a] for a in re.findall(sheet+r'\.(\w+)',expr))
while queue:
 a=queue.pop()
 if a in needed:continue
 needed.add(a);queue.extend(r for r in re.findall(r'\b[A-Z]+[1-9]\d*\b',cells[a]['content']) if r in cells)
refs={}
for a in needed:
 for name,prop in re.findall(r'(Controle\w*)\.(\w+)',cells[a]['content']):refs.setdefault(name,set()).add(prop)
tmpname='Temporario_Validacao_Offline_R12';assert tmpname not in App.listDocuments()
tmp=App.newDocument(tmpname)
try:
 for n,props in refs.items():
  o=tmp.addObject('App::FeaturePython',n)
  for p in props:o.addProperty('App::PropertyAngle',p);setattr(o,p,d['controls'][n][p])
 o=tmp.addObject('Spreadsheet::Sheet',sheet)
 for a in sorted(needed):
  o.set(a,cells[a]['content'])
  if cells[a]['alias']:o.setAlias(a,cells[a]['alias'])
 for n in names:
  old=src.getObject(n);o=tmp.addObject('App::Part',n)
  for p in ['LocalX','LocalY','LocalZ']:
   o.addProperty('App::PropertyLength',p);setattr(o,p,getattr(old,p))
  for p in ['GiroLocal','Abertura','CursoEstudo']:
   o.addProperty('App::PropertyAngle',p);setattr(o,p,getattr(old,p))
  o.Placement=old.Placement
  for prop,expr in old.ExpressionEngine:o.setExpression(prop,expr)
 rows=[]
 for angle in (0.,45.,86.):
  for n,props in refs.items():
   if 'Abertura' in props:tmp.getObject(n).Abertura=angle
  tmp.recompute()
  for n in names:
   parent=src.getObject(n).getGlobalPlacement().multiply(src.getObject(n).Placement.inverse())
   for f in d['leaves'][n]['fronts']:
    c=parent.multVec(tmp.getObject(n).Placement.multVec(App.Vector(*f['leaf_local_center_mm'])))
    rows.append(dict(leaf=n,front=f['name'],angle_deg=angle,center_world_mm=[c.x,c.y,c.z]))
 assert all(abs(src.getObject(n).Abertura.Value)<1e-8 for n in names)
 out=dict(source_sha256=d['sha256'],native_cells=len(needed),poses=rows,source_unchanged=True)
 (HERE/'Referencia_nativa_R12.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf8')
 result=dict(native_cells=len(needed),poses=len(rows),source_unchanged=True)
finally:
 App.closeDocument(tmpname)
 if active in App.listDocuments():App.setActiveDocument(active)
