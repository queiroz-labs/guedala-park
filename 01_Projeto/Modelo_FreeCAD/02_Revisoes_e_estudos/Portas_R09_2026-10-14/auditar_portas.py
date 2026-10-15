from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
d=next(v for v in App.listDocuments().values() if v.FileName and Path(v.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R09_Portas_Comuns.FCStd').resolve())
prev=next(v for v in App.listDocuments().values() if v.FileName and Path(v.FileName).resolve()==(Path(__file__).resolve().parent / '../Padronizacao_R08_2026-10-14/Guedala_Park_R08_Gavetas_Comuns.FCStd').resolve())
data=json.loads(((Path(__file__).resolve().parent / 'Controles_R09.json').resolve()).read_text(encoding='utf-8'));rows=data['doors']
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def vol(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return a.common(b).Volume
closed=[];single=[]
for r in rows:
 g=d.getObject(r['door']);g.Abertura=0;d.recompute()
 a=shape(d.getObject(r['front'])).optimalBoundingBox();b=shape(prev.getObject(r['front'])).optimalBoundingBox()
 closed.append({'door':g.Label,'maximum_closed_delta_mm':max(abs(getattr(a,k)-getattr(b,k)) for k in ['XMin','YMin','ZMin','XMax','YMax','ZMax'])})
 m=next(o for o in g.InList if o.TypeId=='App::Part');structure=[o for o in m.Group if o.TypeId=='Part::Box']
 cases=[]
 for angle in [0,30,60,86,110]:
  g.Abertura=angle;d.recompute();a=shape(d.getObject(r['front']));hits=[]
  for o in structure:
   v=vol(a,shape(o))
   if v>.1:hits.append({'structure':o.Label,'mm3':v})
  cases.append({'angle':angle,'hits':hits})
 g.Abertura=0;d.recompute();single.append({'door':g.Name,'module':m.Label,'cases':cases})
simultaneous=[]
for angle in [30,60,86,90,110]:
 for r in rows:d.getObject(r['door']).Abertura=angle
 d.recompute();hits=[]
 for i,r in enumerate(rows):
  for q in rows[i+1:]:
   a,b=shape(d.getObject(r['front'])),shape(d.getObject(q['front']));v=vol(a,b)
   if v>.1:hits.append({'pair':[d.getObject(r['door']).Label,d.getObject(q['door']).Label],'objects':[r['door'],q['door']],'mm3':v})
 simultaneous.append({'angle_all':angle,'hits':hits})
for r in rows:d.getObject(r['door']).Abertura=0
d.recompute();d.save()
report={'closed_geometry':closed,'single_doors':single,'simultaneous':simultaneous,'scope':'17 controles ideais, sem deslocamento real de dobradiças. Não certifica hardware, batente, tolerância ou movimento com gavetas abertas.'}
((Path(__file__).resolve().parent / 'Auditoria_controles_R09.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({'closed_delta_max_mm':max(r['maximum_closed_delta_mm'] for r in closed),'own_structure_hits':[r for r in single if any(c['hits'] for c in r['cases'])],'simultaneous':simultaneous},ensure_ascii=False)
