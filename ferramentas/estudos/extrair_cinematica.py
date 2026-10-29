"""Snapshot somente leitura das formulas e referenciais; nao anima a fonte."""
from pathlib import Path
import json,re,hashlib,os,csv
import FreeCAD as App
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(os.environ['GP_CINEMATICA_OUT']).resolve()
assert not HERE.is_relative_to(ROOT), 'Saida deve ficar fora do git'
HERE.mkdir(parents=True,exist_ok=True)
release=json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
cad=ROOT/release['cadPath'];before=hashlib.sha256(cad.read_bytes()).hexdigest()
assert release['cadRevision']=='R54' and before==release['cadSHA256']
doc=App.openDocument(str(cad))
parents={o.Name:[p for p in o.InList if 'Group' in p.PropertiesList and o in p.Group] for o in doc.Objects};memo={}
def visible(o):
 if o.Name not in memo:memo[o.Name]=bool(o.Visibility) and all(visible(p) for p in parents[o.Name])
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

module_sources={}
for path in sorted((ROOT/'06_Entregas/Fichas_fabricacao').glob('P??-pecas.csv')):
 for r in csv.DictReader(path.open(encoding='utf-8-sig'),delimiter=';'):
  for n in r['IDs CAD'].split(' | '):module_sources[n]=path.stem[:3]
def ancestors(o):
 seen=set();stack=list(parents.get(o.Name,[]))
 while stack:
  p=stack.pop()
  if p.Name in seen:continue
  seen.add(p.Name);stack.extend(parents.get(p.Name,[]))
 return sorted(seen)
def box(sh):
 b=sh.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
geometry={}
for o in doc.Objects:
 if o.TypeId.startswith('App::') or not visible(o):continue
 sh=getattr(o,'Shape',None)
 if sh is None or sh.isNull() or not sh.Solids or abs(sh.Volume)<.01:continue
 if any(p.TypeId.startswith('Part::') and visible(p) for p in o.InList):continue
 anc=ancestors(o); moving=[n for n in anc if n in leaves and leaves[n]['visible_effective']]
 g=world(o)
 geometry[o.Name]=dict(label=o.Label,box_global_mm=box(g),ancestors=anc,leaf=moving[0] if len(moving)==1 else None,
  module=module_sources.get(o.Name),volume_mm3=abs(g.Volume),expressions=dict(o.ExpressionEngine))
 if len(moving)==1:
  # Only front geometry has been validated as rigid with the leaf by the existing extractor.
  # Hinges have separate articulation; do not assign the front's matrix to all hardware.
  geometry[o.Name]['rigid_front']=o.Name in [f['name'] for f in leaves[moving[0]]['fronts']]
drawers={}
for o in doc.Objects:
 if not o.Name.startswith('Gaveta') or 'CursoNominal' not in o.PropertiesList or not visible(o):continue
 ex=dict(o.ExpressionEngine)
 drawers[o.Name]=dict(label=o.Label,course_mm=float(o.CursoNominal.Value),extension_mm=float(o.Extensao.Value),
  expressions=ex,parent_matrix=o.getGlobalPlacement().multiply(o.Placement.inverse()).toMatrix().A,
  source_axis=xyz(o.Placement.Rotation.Axis),props={p:float(getattr(o,p).Value) for p in ('LocalX','LocalY','LocalZ','GiroLocal')},
  parts=[n for n,g in geometry.items() if o.Name in g['ancestors']])
data.update(revision='R54',drawers=drawers,geometry=geometry,
 geometry_scope='Caixas globais envolventes extraidas de solidos efetivamente visiveis. Nao equivalem a BREP para colisao.',
 source_unchanged=True)
(HERE/'Snapshot.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
result=dict(revision='R54',sha256_before=before,geometry=len(geometry),drawers=len(drawers),sheets=len(sheets),leaves=len(leaves),visible_leaves=sum(v['visible_effective'] for v in leaves.values()),cells=sum(len(s) for s in sheets.values()),source_unchanged=True)

(HERE/'Extracao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result),flush=True)
App.closeDocument(doc.Name)
assert hashlib.sha256(cad.read_bytes()).hexdigest()==before
import os,sys
sys.stdout.flush();sys.stderr.flush();os._exit(0)
