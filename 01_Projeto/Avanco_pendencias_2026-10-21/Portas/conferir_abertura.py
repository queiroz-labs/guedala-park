"""Ensaios de referência Blum da R42; não validam a candidata FGVTN."""
import FreeCAD as A, pathlib, json, hashlib, traceback
ROOT=pathlib.Path(__file__).resolve().parent
d=A.getDocument('Guedala_Park_R42_Consolidado')
sha=hashlib.sha256(pathlib.Path(d.FileName).read_bytes()).hexdigest()
def visible(o):
 seen=set()
 while o and o.Name not in seen:
  seen.add(o.Name)
  if not o.Visibility:return False
  o=o.getParentGeoFeatureGroup() if hasattr(o,'getParentGeoFeatureGroup') else None
 return True
def world(o):
 q=o.Shape.copy();q.Placement=o.getGlobalPlacement();return q
def bb(q):
 b=q.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def overlap(q,r):
 a=bb(q);b=bb(r);return all(min(a[k+3],b[k+3])-max(a[k],b[k])>1e-6 for k in range(3))
def children(o):
 out=[]
 for c in getattr(o,'Group',[]):out.append(c);out+=children(c)
 return out
controls=[o for o in d.Objects if o.Name.startswith('ControlePorta') and 'CursoEstudo' in o.PropertiesList]
saved={o.Name:(o.Abertura.Value,o.CursoEstudo.Value) for o in controls}
native=[o for o in d.Objects if not hasattr(o,'Group') and hasattr(o,'Shape') and hasattr(o,'getGlobalPlacement') and not o.Shape.isNull() and o.Shape.Solids and visible(o) and o.Shape.Volume>300000]
baseline={o.Name:world(o) for o in native};poses={o.Name:str(o.getGlobalPlacement()) for o in native}
result={'scope':'Reference Blum kinematics only; temporary extension of study controls to110. Does not model FGVTN110 hinge trajectory.',
 'angles_deg':[0,30,60,86,100,110],'source_sha256':sha,'obstacle_filter':'Visible leaf solids >300000mm3, geometric ancestor visibility respected; small hardware excluded. One door moves; other doors remain in saved positions.',
 'controls':[],'hits':[],'error':None,'restored':False}
d.openTransaction('Ensaio temporário portas R42 — não salvar')
try:
 for c in controls:
  rows=[]
  leaves=[o for o in d.Objects if o.TypeId=='App::Part' and any(path=='Abertura' and expr==c.Name+'.Abertura' for path,expr in o.ExpressionEngine)]
  moving={o.Name for leaf in leaves for o in children(leaf)}
  panels=[o for o in native if o.Name in moving]
  if not panels:result['controls'].append({'control':c.Name,'label':c.Label,'status':'No visible large panel mapped'});continue
  c.CursoEstudo=110
  for angle in result['angles_deg']:
   c.Abertura=angle;d.recompute()
   rows.append({'angle':angle,'panels':[{'name':o.Name,'bbox':bb(world(o)),'valid':o.Shape.isValid()} for o in panels]})
   for o in panels:
    q=world(o)
    for other in native:
     if other.Name in moving:continue
     r=baseline[other.Name]
     if overlap(q,r):
      v=q.common(r).Volume
      if v>.1:result['hits'].append({'control':c.Name,'label':c.Label,'angle':angle,'panel':o.Name,'obstacle':other.Name,'obstacle_label':other.Label,'volume_mm3':v})
  c.Abertura=saved[c.Name][0];c.CursoEstudo=saved[c.Name][1];d.recompute()
  result['controls'].append({'control':c.Name,'label':c.Label,'saved_limit_deg':saved[c.Name][1],'panels':[o.Name for o in panels],'poses':rows})
  (ROOT/'Progresso.json').write_text(json.dumps({'completed':len(result['controls']),'total':len(controls),'hits':len(result['hits'])}),encoding='utf-8')
except Exception:result['error']=traceback.format_exc()
finally:
 for n,(a,c) in saved.items():d.getObject(n).Abertura=a;d.getObject(n).CursoEstudo=c
 d.recompute();d.abortTransaction();d.recompute()
 result['restored']=all(str(o.getGlobalPlacement())==poses[o.Name] for o in native)
 result['source_unchanged']=hashlib.sha256(pathlib.Path(d.FileName).read_bytes()).hexdigest()==sha
 (ROOT/'Auditoria_abertura_R42.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
assert result['restored'] and result['source_unchanged'] and result['error'] is None
