import FreeCAD as A, Part, pathlib, json, itertools, hashlib, traceback
ROOT=pathlib.Path(__file__).resolve().parent
def bb(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def overlap(a,b):
 p=bb(a);q=bb(b);return all(min(p[i+3],q[i+3])-max(p[i],q[i])>1e-7 for i in range(3))
def sweep(s,dist):
 # Exact linear sweep for these orthogonal parts: original plus every +Y face prism.
 pieces=[s]
 for f in s.Faces:
  if f.normalAt(0,0).y>0.999:pieces.append(f.extrude(A.Vector(0,dist,0)))
 return pieces[0].multiFuse(pieces[1:]).removeSplitter() if len(pieces)>1 else s
def main():
 d=next(x for x in A.listDocuments().values() if x.FileName.endswith('Escritorio_montagem_vertical_R02_ESTUDO.FCStd'))
 src=next(x for x in A.listDocuments().values() if x.Name=='Guedala_Park_R42_Consolidado')
 old={n:d.getObject(n).Extensao.Value for n in ['Caixa_Gaveta008','Caixa_Gaveta009']}
 for n in old:d.getObject(n).Extensao=0
 d.recompute()
 carc={o.Name:shape(o) for o in d.getObject('Carcaca_470x248').Group}
 drawers=[{o.Name:shape(o) for o in d.getObject('Caixa_'+n).Group if hasattr(o,'Shape')} for n in ['Gaveta008','Gaveta009']]
 cargo=[shape(d.getObject('Util_'+n)) for n in ['Gaveta008','Gaveta009']]
 sweeps=[{n:sweep(s,378) for n,s in p.items()} for p in drawers]
 cargo_sweeps=[sweep(s,378) for s in cargo]
 findings=[];checks=0
 def test(kind,na,sa,nb,sb,extra=None):
  nonlocal checks
  checks+=1
  if not overlap(sa,sb):return
  v=sa.common(sb).Volume
  if v>0.001:findings.append(dict(kind=kind,a=na,b=nb,volume_mm3=v,**(extra or {})))
 for i in range(2):
  for n,s in sweeps[i].items():
   for k,q in carc.items():test('madeira_percurso_continuo',n,s,k,q)
   for k,q in sweeps[1-i].items():test('duas_gavetas_posicoes_independentes',n,s,k,q)
  for k,q in carc.items():test('carga_percurso_continuo',str(i),cargo_sweeps[i],k,q)
  for k,q in sweeps[1-i].items():test('carga_vs_outra_gaveta',str(i),cargo_sweeps[i],k,q)
 # Source baseline height validation: includes original rails and front of other drawer.
 baseline=[]
 for i,n in enumerate(['Gaveta008','Gaveta009']):
  g=src.getObject(n);floor=src.getObject('GavetaComumR074' if i==0 else 'GavetaComumR086')
  f=bb(shape(floor));h=float(g.AlturaUtilProposta.Value)
  p=Part.makeBox(322,359,h,A.Vector(4339,307,f[5]));sw=sweep(p,400)
  other=src.getObject('Gaveta009' if i==0 else 'Gaveta008')
  for o in other.Group:
   if hasattr(o,'Shape') and not o.Shape.isNull():test('referencia_R42_altura_util_em_movimento',n,sw,o.Name,shape(o))
  baseline.append({'drawer':n,'declared_height':h,'floor_top':f[5],'prism':bb(p)})
 # Regulation extremes, whole assembly versus fronts realigned in place.
 regulation=[]
 for a,b in itertools.product([0,3],repeat=2):
  shifted=[]
  for i,dz in enumerate([a,b]):
   pp={}
   for n,s in drawers[i].items():
    q=s.copy();q.translate(A.Vector(0,0,dz));pp[n]=q
   shifted.append(pp)
  for n,s in shifted[0].items():
   for k,q in shifted[1].items():test('regulagem_frentes_acompanham',n,s,k,q,{'inferior_dz':a,'superior_dz':b})
  for i,dz in enumerate([a,b]):
   cp=cargo_sweeps[i].copy();cp.translate(A.Vector(0,0,dz))
   for k,q in carc.items():test('regulagem_carga_vs_carcaca',str(i),cp,k,q,{'inferior_dz':a,'superior_dz':b})
   for k,s in sweeps[1-i].items():
    q=s.copy()
    if not k.endswith('_Frente'):q.translate(A.Vector(0,0,[a,b][1-i]))
    test('regulagem_carga_frentes_realinhadas',str(i),cp,k,q,{'inferior_dz':a,'superior_dz':b})
 # Sweep against apartment's source leaf solids, excluding every office component.
 exclude=set()
 def descend(o):
  if o.Name in exclude:return
  exclude.add(o.Name)
  for c in getattr(o,'Group',[]):descend(c)
 descend(src.getObject('Modulo015'))
 ext_candidates=[]
 full=Part.makeCompound([s for p in sweeps for s in p.values()]+cargo_sweeps)
 for o in src.Objects:
  if o.Name in exclude or hasattr(o,'Group') or not hasattr(o,'Shape') or o.Shape.isNull() or not o.Shape.Solids:continue
  q=shape(o)
  if not overlap(full,q):continue
  ext_candidates.append({'name':o.Name,'label':o.Label,'visible_local':o.ViewObject.Visibility,'bbox':bb(q)})
  for i in range(2):
   for n,s in sweeps[i].items():test('percurso_vs_apartamento_todas_referencias',n,s,o.Name,q,{'other_label':o.Label,'visible_local':o.ViewObject.Visibility})
   test('carga_vs_apartamento_todas_referencias',str(i),cargo_sweeps[i],o.Name,q,{'other_label':o.Label,'visible_local':o.ViewObject.Visibility})
 result={'status':'PENDENTE','tests':checks,'findings':findings,'baseline':baseline,'external_candidates':ext_candidates,'source_sha256':hashlib.sha256(pathlib.Path(src.FileName).read_bytes()).hexdigest(),
 'method':'Exact translational swept solids for orthogonal wood and cargo prisms; independent drawer positions; vertical regulation endpoint comparisons. All source leaf references included, local visibility not equivalent to effective visibility.'}
 (ROOT/'Auditoria_completa.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
 for n,v in old.items():d.getObject(n).Extensao=v
 d.recompute()
try:main()
except Exception:
 (ROOT/'Auditoria_erro.txt').write_text(traceback.format_exc(),encoding='utf-8');raise

