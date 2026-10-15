from pathlib import Path
import json
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R08_Gavetas_Comuns.FCStd').resolve())
data=json.loads(((Path(__file__).resolve().parent / 'Padronizacao_R08.json').resolve()).read_text(encoding='utf-8'))
drawers=[doc.getObject(r['drawer']) for r in data['changed_drawers']]
g2=next(o for o in doc.Objects if o.Label=='G2 · utensílios' and hasattr(o,'Extensao'))
drawers.append(g2)
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def vol(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return a.common(b).Volume
def moving(g):return [o for o in g.Group if hasattr(o,'CategoriaR08') and o.CategoriaR08 in ['wood','locking'] or hasattr(o,'Fonte') and o.Name.startswith('MontagemG2')]
def profiles(g):
 m=next(o for o in g.InList if o.TypeId=='App::Part')
 if g==g2:return [o for o in doc.Objects if hasattr(o,'Fonte') and o.Name.startswith('MontagemG2') and o.Label.startswith(('48346342','49027541'))]
 return [doc.getObject(n) for r in data['changed_drawers'] if r['drawer']==g.Name for n in r['profile_names']]
for g in drawers:g.Extensao=0
doc.recompute()
internal=[];hardware=[];fixedStructure=[];courses=[]
for g in drawers:
 wood=[o for o in moving(g) if hasattr(o,'CategoriaR08') and o.CategoriaR08=='wood' or hasattr(o,'Fonte') and '[3B0R-' in o.Label]
 for i,o in enumerate(wood):
  for q in wood[i+1:]:
   v=vol(shape(o),shape(q))
   if v>.1:internal.append({'drawer':g.Label,'pair':[o.Label,q.Label],'mm3':v})
 for o in profiles(g):
  for q in wood:
   v=vol(shape(o),shape(q))
   if v>.1:hardware.append({'drawer':g.Label,'hardware':o.Label,'wood':q.Label,'mm3':v})
 m=next(o for o in g.InList if o.TypeId=='App::Part')
 structure=[o for o in m.Group if o.TypeId=='Part::Box' and not hasattr(o,'Deslocamento')]
 for o in profiles(g):
  for q in structure:
   v=vol(shape(o),shape(q))
   if v>.1:fixedStructure.append({'drawer':g.Label,'hardware':o.Label,'structure':q.Label,'mm3':v})
for r in data['changed_drawers']:
 g=doc.getObject(r['drawer']);m=doc.getObject(r['module'])
 room=next(o for o in m.InList if o.Name.startswith('Ambiente_'))
 ownFixed=doc.getObject(r['fixed_part'])
 static=[o for o in m.Group if o.TypeId=='Part::Box' and not hasattr(o,'Deslocamento')]
 static += [o for q in drawers if q!=g and m in q.InList for o in moving(q)+profiles(q)]
 static += [o for o in room.Group if o.TypeId=='Part::Box' and o.Label.startswith('Bancada cozinha')]
 walls=[o for o in doc.Objects if o.TypeId=='Part::Box' and ('Parede' in o.Label or o.Label.startswith('Cama') or o.Label.startswith('Mesa'))]
 static += walls
 # Abre uma folha ideal para liberar o vão de ensaio, sem validar mecanismo de correr.
 sliding=[o for o in m.Group if hasattr(o,'Deslocamento')]
 sliderOriginal={o.Name:float(o.Deslocamento) for o in sliding}
 if sliding:
  right=g.Placement.Base.x>1000
  for o in sliding:o.Deslocamento=985 if (right and o.Label.endswith('2')) or (not right and o.Label.endswith('1')) else 0
  doc.recompute()
 obstacles=[(o,shape(o)) for o in static];hits=[];positions=range(0,int(r['NL'])+1,25)
 for pos in positions:
  g.Extensao=pos;doc.recompute()
  for o in moving(g):
   a=shape(o)
   for q,b in obstacles:
    v=vol(a,b)
    if v>.1:hits.append({'pose_mm':pos,'moving':o.Label,'obstacle':q.Label,'mm3':v})
 g.Extensao=0
 for o in sliding:o.Deslocamento=sliderOriginal[o.Name]
 doc.recompute()
 courses.append({'drawer':g.Label,'poses':len(positions),'maximum_candidate_mm':r['NL'],'hits':hits})
g1=next(g for g in drawers if g.Label=='G1 · talheres')
floor=next(o for o in moving(g2) if 'Fundo_da_gaveta' in o.Label)
floorTop=shape(floor).optimalBoundingBox().ZMax
limit=min(shape(o).BoundBox.ZMin for o in profiles(g1))
height={'floor_top_global_mm':floorTop,'upper_runner_min_global_mm':limit,'conservative_vertical_space_mm':limit-floorTop,
 'required_program_with_reserve_mm':111,'nominal_margin_mm':limit-floorTop-111,
 'scope':'Menor cota Z da montagem fechada proposta G1, sobre toda a largura. Nominal, sem flexão/tolerância/regulagem ou homologação cinemática.'}
doc.save()
report={'wood_internal_hits':internal,'hardware_wood_hits':hardware,'profile_structure_hits':fixedStructure,'courses':courses,'G2_height':height,
 'invalid':[o.Name for o in doc.Objects if hasattr(o,'CategoriaR08') and not o.Shape.isValid()],
 'scope':'Oito caixas alteradas, candidato500/400. Geometria rígida, demais caixas fechadas; perfis próprios estáticos não animados. Não repete os ensaios antigos intactos nem certifica mecanismo real/carga.'}
((Path(__file__).resolve().parent / 'Auditoria_R08.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({**report,'hardware_wood_hits_count':len(hardware),'hardware_wood_hits':hardware[:5]},ensure_ascii=False)
