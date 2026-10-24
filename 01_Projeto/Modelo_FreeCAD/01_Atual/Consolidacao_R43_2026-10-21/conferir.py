import FreeCAD as A, Part, pathlib,json,hashlib
P=pathlib.Path(__file__).resolve().parent
d=A.getDocument('Guedala_Park_R43_Consolidado');orig=A.getDocument('Guedala_Park_R42_Consolidado')
info=json.loads((P/'Integracao.json').read_text(encoding='utf-8'));hidden=set(info['hidden_original_objects'])
def w(o):
 q=o.Shape.copy()
 if hasattr(o,'getGlobalPlacement'):q.Placement=o.getGlobalPlacement()
 return q
def visible(o):
 if not o.ViewObject.Visibility:return False
 return all(visible(x) for x in o.InList if hasattr(x,'Group') and o in x.Group)
def volume(q,t):return q.common(t).Volume if q.BoundBox.intersect(t.BoundBox) else 0
def box(x,y,z,a,b,c):return Part.makeBox(a,b,c,A.Vector(x,y,z))
context=[]
for o in d.Objects:
 if o.Name.startswith('BC43_') or o.Name in hidden or hasattr(o,'Group') or not hasattr(o,'Shape') or o.Shape.isNull():continue
 if visible(o) or o.Name in ['Peca075','Peca051','Peca399','Peca185','Peca190','Peca396']:context.append((o.Name,w(o)))
def hits(q,items):return [[n,round(volume(q,t),4)] for n,t in items if volume(q,t)>.1]
r={'context_solids':len(context),'pose_checks':[],'continuous_sweeps':[],'maintenance':[],'static_context':[],'unchanged_original_errors':[]}
fixed=[(o.Name,w(o)) for n in ['Madeira','Trilhos','Batentes'] for o in d.getObject('BC43_'+n).Group]
for a in [0,134,268]:
 for b in [0,116.5,233]:
  d.BC43_Controle.CursoEsquerda=a;d.BC43_Controle.CursoDireita=b;d.recompute()
  left=[(o.Name,w(o)) for o in d.BC43_FolhaEsquerda.Group];right=[(o.Name,w(o)) for o in d.BC43_FolhaDireita.Group]
  found=[]
  for n,q in left+right:found.extend([[n]+h for h in hits(q,context+fixed)])
  for n,q in left:found.extend([[n]+h for h in hits(q,right)])
  r['pose_checks'].append({'front':a,'rear':b,'hits':found})
d.BC43_Controle.CursoEsquerda=0;d.BC43_Controle.CursoDireita=0;d.recompute()
for x,y,width in [(2780,4822,560),(2815,4852,525)]:r['continuous_sweeps'].append(hits(box(x,y,221.5,width,27,500),context))
for args in [(2760,4800,200,600,90,543),(2760,4800,200,720,85,543),(2880,4470,200,600,415,543)]:r['maintenance'].append(hits(box(*args),context))
for n,q in fixed:r['static_context'].extend([[n]+h for h in hits(q,context)])
interior=box(2778,4890,218,564,382,509)
r['storage_intrusions']=[]
for group in ['Madeira','Fixacoes','Trilhos','Batentes','FolhaEsquerda','FolhaDireita']:
 for o in d.getObject('BC43_'+group).Group:
  v=volume(w(o),interior)
  if v>.1:r['storage_intrusions'].append([o.Name,v])
r['storage_envelope_mm']=[564,382,509]
r['invalid_new_shapes']=[o.Name for o in d.Objects if o.Name.startswith('BC43_') and hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]
(P/'Verificacao_R43_parcial.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
for o in orig.Objects:
 q=d.getObject(o.Name)
 if not q:r['unchanged_original_errors'].append([o.Name,'missing']);continue
 if not hasattr(o,'Group') and hasattr(o,'Shape') and not o.Shape.isNull():
  a=w(o);b=w(q)
  if abs(a.Volume-b.Volume)>.01 or str(a.BoundBox)!=str(b.BoundBox):r['unchanged_original_errors'].append([o.Name,'geometry'])
 if o.Name not in hidden and o.ViewObject.Visibility!=q.ViewObject.Visibility:r['unchanged_original_errors'].append([o.Name,'visibility'])
 if getattr(o,'ExpressionEngine',[])!=getattr(q,'ExpressionEngine',[]):r['unchanged_original_errors'].append([o.Name,'expression'])
r['source_sha256']=hashlib.sha256(pathlib.Path(orig.FileName).read_bytes()).hexdigest()
r['limits']=['Ferragens são envelopes, não CAD industrial.','Resistência, suspensão, tolerâncias, porta real e hidráulica não validadas para fabricação.','Fundo original mantido sem recorte; sifão e recorte hipotéticos ficam ocultos.']
(P/'Verificacao_R43.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
d.save()
