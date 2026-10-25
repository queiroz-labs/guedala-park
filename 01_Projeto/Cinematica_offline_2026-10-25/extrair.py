"""Snapshot somente leitura das formulas e referenciais; nao anima a fonte."""
from pathlib import Path
import json,re,hashlib
import FreeCAD as App
HERE=Path(__file__).resolve().parent
doc=App.getDocument('Guedala_Park_R51_Sem_estudo_tubular')
parents={o.Name:[p for p in o.InList if 'Group' in p.PropertiesList and o in p.Group] for o in doc.Objects};memo={}
def visible(o):
 if o.Name not in memo:memo[o.Name]=bool(o.ViewObject.Visibility) and all(visible(p) for p in parents[o.Name])
 return memo[o.Name]
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement);return s
def cg(s):
 v=sum(q.Volume for q in s.Solids);return sum((q.CenterOfMass*q.Volume for q in s.Solids),App.Vector())/v,v
def xyz(v):return [v.x,v.y,v.z]
leaves={};sheet_names=set()
for o in doc.Objects:
 if 'Group' not in o.PropertiesList or 'GiroLocal' not in o.PropertiesList:continue
 expressions=dict(o.ExpressionEngine)
 names=set(re.findall(r'(CinematicaComum\w*)\.',str(expressions)))
 fronts=[c for c in o.Group if c.Name.startswith('Frente') and hasattr(c,'Shape') and not c.Shape.isNull()]
 if not names or not fronts:continue
 assert abs(o.Abertura.Value)<1e-8,'Fechar a folha na fonte antes de extrair: '+o.Name
 expected={'.Placement.Base.x':'-LocalX','.Placement.Base.y':'LocalY','.Placement.Base.z':'LocalZ','.Placement.Rotation.Angle':'GiroLocal'}
 assert all(expressions.get(p)==e for p,e in expected.items()),'Mapeamento de placement novo exige adaptar/validar o motor: '+o.Name
 sheet_names|=names
 parent=o.getGlobalPlacement().multiply(o.Placement.inverse())
 records=[]
 for c in fronts:
  sh=world(c);cworld,vol=cg(sh);local=o.getGlobalPlacement().inverse().multVec(cworld)
  records.append(dict(name=c.Name,label=c.Label,volume_mm3=vol,leaf_local_center_mm=xyz(local),
   source_global_center_mm=xyz(cworld),visible_effective=visible(c)))
 leaves[o.Name]=dict(label=o.Label,visible_effective=visible(o),parent_matrix=parent.toMatrix().A,
  props={p:float(getattr(o,p).Value) for p in ('LocalX','LocalY','LocalZ','GiroLocal','Abertura')},
  expressions={p:e for p,e in expressions.items() if p in ['LocalX','LocalY','LocalZ','GiroLocal','Abertura','CursoEstudo']},
  source_axis=xyz(o.Placement.Rotation.Axis),fronts=records)
sheets={};control_refs={}
for n in sorted(sheet_names):
 o=doc.getObject(n);rows={}
 for addr in o.getNonEmptyCells():
  content=o.getContents(addr);alias=o.getAlias(addr)
  rows[addr]=dict(content=content,alias=alias)
  for name,prop in re.findall(r'([A-Za-z_]\w*)\.([A-Za-z_]\w*)',content):
   if name.startswith('Controle'):control_refs.setdefault(name,set()).add(prop)
 sheets[n]=rows
controls={n:{p:float(getattr(doc.getObject(n),p).Value) for p in props} for n,props in control_refs.items()}
data=dict(cad=doc.FileName,sha256=hashlib.sha256(Path(doc.FileName).read_bytes()).hexdigest(),
 source_objects=len(doc.Objects),sheets=sheets,controls=controls,leaves=leaves,
 scope='Formulas e CG geometricos. Folhas ocultas/historicas identificadas; nao reativar mecanismos cancelados. Sem massas reais ou capacidade de ferragem. Nenhum controlador/documento fonte alterado.')
(HERE/'Snapshot_R51.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
result=dict(sheets=len(sheets),leaves=len(leaves),visible_leaves=sum(v['visible_effective'] for v in leaves.values()),cells=sum(len(s) for s in sheets.values()),source_unchanged=True)
