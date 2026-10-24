import FreeCAD as A, Part, pathlib, json, itertools, hashlib
ROOT=pathlib.Path(__file__).resolve().parent
d=next(x for x in A.listDocuments().values() if x.FileName.endswith('Escritorio_montagem_vertical_R02_ESTUDO.FCStd'))
src=A.getDocument('Guedala_Park_R42_Consolidado')
def s(o):
 q=o.Shape.copy();q.Placement=o.getGlobalPlacement();return q
def b(q):
 a=q.BoundBox;return [a.XMin,a.YMin,a.ZMin,a.XMax,a.YMax,a.ZMax]
def overlap(a,c):
 x=b(a);y=b(c);return all(min(x[i+3],y[i+3])-max(x[i],y[i])>1e-7 for i in range(3))
def sweep(q,v):
 pieces=[q];direction=A.Vector(v);direction.normalize()
 for f in q.Faces:
  if f.normalAt(0,0).dot(direction)>0.999:pieces.append(f.extrude(v))
 return pieces[0].multiFuse(pieces[1:]).removeSplitter() if len(pieces)>1 else q
for n in ['Caixa_Gaveta008','Caixa_Gaveta009']:d.getObject(n).Extensao=0
d.recompute()
car={o.Name:s(o) for o in d.getObject('Carcaca_470x248').Group}
draw=[{o.Name:s(o) for o in d.getObject('Caixa_'+n).Group} for n in ['Gaveta008','Gaveta009']]
envelopes=[];cargo=[]
for i,n in enumerate(['Gaveta008','Gaveta009']):
 out={}
 for name,q in draw[i].items():
  if name.endswith('_Frente'):
   v=b(q);q=Part.makeBox(v[3]-v[0],v[4]-v[1],v[5]-v[2],A.Vector(*v[:3]))
  if not name.endswith('_Frente'):q=sweep(q,A.Vector(0,0,3))
  out[name]=sweep(q,A.Vector(0,378,0))
 envelopes.append(out)
 cargo.append(sweep(sweep(s(d.getObject('Util_'+n)),A.Vector(0,0,3)),A.Vector(0,378,0)))
hits=[];checks=0
def test(kind,na,a,nb,c):
 global checks
 checks+=1
 if overlap(a,c):
  v=a.common(c).Volume
  if v>0.001:hits.append(dict(kind=kind,a=na,b=nb,volume_mm3=v))
for i in range(2):
 for name,q in envelopes[i].items():
  for n,c in car.items():test('madeira_0a378_e_0a3',name,q,n,c)
  for n,c in envelopes[1-i].items():test('gavetas_independentes_0a378_e_0a3',name,q,n,c)
 for n,c in car.items():test('carga_0a378_e_0a3',str(i),cargo[i],n,c)
 for n,c in envelopes[1-i].items():test('carga_vs_outra_gaveta_0a378_e_0a3',str(i),cargo[i],n,c)
# Verify geometrical source reference rather than trusting copied dimensions alone.
dimensions=[]
for n in ['Peca367','Peca368','Peca369','Peca370','Peca371']:
 original=s(src.getObject(n));ref=s(d.getObject('Antes_'+n));new=s(d.getObject('Novo_'+n))
 dimensions.append({'name':n,'source_bbox':b(original),'new_bbox':b(new),
 'source_reference_symmetric_difference_mm3':original.cut(ref).Volume+ref.cut(original).Volume,
 'valid':new.isValid(),'solid_count':len(new.Solids)})
fronts=[]
for n,old in [('Gaveta008','GavetaComumR077'),('Gaveta009','GavetaComumR089')]:
 oldshape=s(src.getObject(old));new=s(d.getObject(n+'_Frente'))
 fronts.append({'name':n,'symmetric_difference_mm3':oldshape.cut(new).Volume+new.cut(oldshape).Volume})
# Maximum regulation leaves positive clearance, including stored objects.
lowerfloor=b(s(d.getObject('Gaveta008_Fundo')))[5]
upperfloor=b(s(d.getObject('Gaveta009_Fundo')))[5]
frontbottom=b(s(d.getObject('Gaveta009_Frente')))[2]
ceiling=b(s(d.getObject('Novo_Peca371')))[2]
margin_lower=frontbottom-(lowerfloor+60.4+3)
margin_upper=ceiling-(upperfloor+54+3)
assert not hits and margin_lower>=1 and margin_upper>=1
assert all(x['source_reference_symmetric_difference_mm3']<0.001 for x in dimensions)
assert all(x['symmetric_difference_mm3']<0.001 for x in fronts)
# Exclude all original office components; inspect all other finite solid references.
exclude=set()
def visit(o):
 if o.Name in exclude:return
 exclude.add(o.Name)
 for c in getattr(o,'Group',[]):visit(c)
visit(src.getObject('Modulo015'))
outer=Part.makeCompound([q for p in envelopes for q in p.values()]+cargo+list(car.values()))
external_candidates=[];external_hits=[]
for o in src.Objects:
 if o.Name in exclude or hasattr(o,'Group') or not hasattr(o,'Shape') or o.Shape.isNull() or not o.Shape.Solids:continue
 q=s(o)
 if overlap(outer,q):
  external_candidates.append({'name':o.Name,'label':o.Label})
  v=outer.common(q).Volume
  if v>0.001:external_hits.append({'name':o.Name,'label':o.Label,'volume_mm3':v})
result={'status':'GEOMETRIA_CONFERIDA_MONTAGEM_MECANICA_PENDENTE',
 'method':'Union of orthogonal face extrusions along Y0..378 and Z0..3; conservative bounding solids for fronts held at final aligned height. Independent positions of the two drawers. Exact original fronts retained in CAD. No rail/clip geometry included.',
 'checks':checks,'collisions':hits,'external_candidates':external_candidates,'external_hits':external_hits,
 'carcass_reference_checks':dimensions,'front_checks':fronts,
 'payload_min_clearance_with_3mm_adjustment_mm':{'lower_under_upper_front':margin_lower,'upper_under_top':margin_upper},
 'assembly_blockers':['Exact conventional runner and clip profile absent','Front mounting must allow final independent alignment; not designed','Rear notches/holes/screw pattern and tolerances pending','Wood joints, bottom strength and total load not validated'],
 'source_sha256':hashlib.sha256(pathlib.Path(src.FileName).read_bytes()).hexdigest()}
(ROOT/'Auditoria_intervalos.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
if 'ResultadoAuditoria' not in d.getObject('Limites_do_estudo').PropertiesList:d.getObject('Limites_do_estudo').addProperty('App::PropertyString','ResultadoAuditoria')
d.getObject('Limites_do_estudo').ResultadoAuditoria='GEOMETRIA CONFERIDA; MONTAGEM PENDENTE. Carga conservada no percurso0..378mm e regulagem0..3mm com frentes realinhadas. Margens minimas1,6/1mm. Perfil/engates/fixacao das frentes/recortes/carga por validar.'
d.recompute();d.save()
