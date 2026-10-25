"""Copia formas; nao modifica Extensao, expressoes ou documento da fonte."""
from pathlib import Path
import json,hashlib
import FreeCAD as App,Part
HERE=Path(__file__).resolve().parent
g=json.loads((HERE/'Geometria_R51.json').read_text(encoding='utf8'))
study=json.loads((HERE.parent/'Bancada_marcenaria_2026-10-25/Resultados.json').read_text(encoding='utf8'))
doc=App.getDocument('Guedala_Park_R51_Sem_estudo_tubular')
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def box(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def overlap(a,b):return all(min(a[i+3],b[i+3])-max(a[i],b[i])>1e-6 for i in range(3))
moving={r['name']:world(doc.getObject(r['name'])) for dr in g['drawers'] for r in dr['wood']+dr['locks']}
guide_names={o.Name for n in ['GuiasComunsR006','GuiasComunsR007'] for o in doc.getObject(n).Group}
excluded=set(moving)|guide_names|{'Peca111','Peca112','Peca367','Peca368'}
parents={o.Name:[p for p in o.InList if 'Group' in p.PropertiesList and o in p.Group] for o in doc.Objects};memo={}
def visible(o):
 if o.Name not in memo:memo[o.Name]=bool(o.ViewObject.Visibility) and all(visible(p) for p in parents[o.Name])
 return memo[o.Name]
fixed=[]
for o in doc.Objects:
 if o.Name in excluded or not o.isDerivedFrom('Part::Feature') or o.Shape.isNull() or not visible(o):continue
 s=world(o);fixed.append((o.Name,s,box(s),'R51'))
for p in study['panels']:
 s=Part.makeBox(*p['size_mm'],App.Vector(*p['origin_mm']));fixed.append((p['id'],s,box(s),'ESTUDO'))
potential=[];hits=[];checks=0
for name,s in moving.items():
 b=box(s);sweep=b.copy();sweep[4]+=400
 for n,q,bq,source in fixed:
  checks+=1
  if not overlap(sweep,bq):continue
  lo=max(0.,bq[1]-b[4]);hi=min(400.,bq[4]-b[1]);samples=[]
  if hi<lo:continue
  for i in range(21):
   t=lo+(hi-lo)*i/20;z=s.copy();z.translate(App.Vector(0,t,0));vol=z.common(q).Volume
   if vol>1e-5:samples.append(dict(extension_mm=t,volume_mm3=vol))
  potential.append(dict(moving=name,fixed=n,source=source,AABB_interval_mm=[lo,hi],sample_count=21,positive_samples=len(samples)))
  if samples:hits.append(dict(moving=name,fixed=n,source=source,samples=samples))
# Duas extensoes independentes: caixas varridas disjuntas provam separacao.
cross=[]
for a in g['drawers'][0]['wood']+g['drawers'][0]['locks']:
 for b in g['drawers'][1]['wood']+g['drawers'][1]['locks']:
  ba=a['box_mm'].copy();bb=b['box_mm'].copy();ba[4]+=400;bb[4]+=400
  if overlap(ba,bb):cross.append([a['name'],b['name']])
assert hashlib.sha256(Path(g['cad']).read_bytes()).hexdigest()==g['sha256']
data=dict(source_sha256=g['sha256'],source_unchanged=True,drawers=2,rigid_moving_shapes=16,
 stroke_mm=[0,400],translation_global_axis='+Y',fixed_shapes=len(fixed),broadphase_pairs=checks,
 potential_swept_AABB_contacts=potential,positive_sample_interferences=hits,
 independent_drawer_swept_AABB_contacts=cross,
 continuous_separation_proven_by_disjoint_swept_boxes=not potential and not cross,
 excluded_static_guide_shapes=sorted(guide_names),
 scope='Caixas varridas sao teste continuo conservador. Candidatos positivos precisam analise adicional;21 amostras BREP nao provam ausencia continua. STEP inteiro estatico da guia nao e telescopio real. Sem tolerancias, deformacao, maos ou retirada da gaveta.')
(HERE/'Conferencia_movimento.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
result={k:data[k] for k in ['fixed_shapes','broadphase_pairs','potential_swept_AABB_contacts','positive_sample_interferences','independent_drawer_swept_AABB_contacts','continuous_separation_proven_by_disjoint_swept_boxes']}
