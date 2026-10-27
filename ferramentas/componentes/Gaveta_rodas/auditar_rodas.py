from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R13_Gaveta_Rodas.FCStd').resolve())
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R13.json').resolve()).read_text(encoding='utf-8'));g=doc.getObject(data['drawer']);m=doc.getObject(data['module']);g.Extensao=0;doc.recompute()
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def vol(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return a.common(b).Volume
wood=[doc.getObject(n) for n in data['wood_names']];program=[doc.getObject(n) for n in data['program_names']]
moving=[doc.getObject(n) for n in data['moving_names']];fixed=[doc.getObject(n) for n in data['fixed_names']]
internal=[]
for i,o in enumerate(wood+program):
 for q in (wood+program)[i+1:]:
  v=vol(shape(o),shape(q))
  if v>.1:internal.append({'pair':[o.Name,q.Name],'mm3':v})
wheelWood=[]
for o in [doc.getObject(n) for r in data['wheels'] for n in r['parts']]:
 for q in wood:
  v=vol(shape(o),shape(q))
  if v>.1:wheelWood.append({'pair':[o.Name,q.Name],'mm3':v})
room=next(o for o in m.InList if o.Name.startswith('Ambiente_'))
obstacles=fixed+[o for o in room.Group if o.TypeId=='Part::Box']+list(doc.getObject('ParedesInteiras').Group)
for moduleName in ['Modulo004','Modulo005','Modulo006']:
 obstacles.extend(o for o in doc.getObject(moduleName).Group if o.TypeId=='Part::Box')
cached=[(o,shape(o)) for o in obstacles];courses=[]
for pos in list(range(0,401,25))+[425,450,460,500,520,530]:
 g.Extensao=pos;doc.recompute();hits=[]
 for o in moving:
  a=shape(o)
  for q,b in cached:
   v=vol(a,b)
   if v>.1:hits.append({'moving':o.Name,'target':q.Name,'label':q.Label,'mm3':v})
 courses.append({'extension_mm':pos,'hits':hits})
# Once fully outside the reference upper carcass, an illustrative lift40 is examined separately.
g.Extensao=530;g.Placement.Base.z=79;doc.recompute();lift=[]
for o in moving:
 for q,b in cached:
  v=vol(shape(o),b)
  if v>.1:lift.append({'moving':o.Name,'target':q.Name,'mm3':v})
g.Placement.Base.z=39;g.Extensao=0;doc.recompute();doc.save()
mass=sum(o.Shape.Volume for o in wood)
report={'internal_wood_program_hits':internal,'wheel_wood_hits':wheelWood,'courses':courses,'lift40_at_extension530_hits':lift,
 'wood_volume_mm3':mass,'wood_mass_scenario750_kg':mass*750/1e9,'wood_mass_scenario900_kg':mass*900/1e9,
 'program_margins_mm':{'handle_end_each':31,'broom_top_to_rim':23},'nominal_guide_gap_each_mm':2,
 'closed_vertical_reserve_mm':35,'full_withdrawal_rear_to_upper_carcass_front_mm':10,
 'target_count':len(obstacles),'invalid':[o.Name for o in moving+fixed if not o.Shape.isValid()],
 'scope':'Somente caixa nova/rodas-gabarito/conteúdo nominal R13. Translação ideal e levantamento ilustrativo, não rolagem/piso/pessoa/carga/tolerâncias. Apoios são reservas, sem resistência calculada. Não repete nove gavetasR08.'}
((Path(__file__).resolve().parent / 'Auditoria_R13.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({'internal_hits':internal,'wheel_wood_hits':wheelWood,'course_positions':len(courses),'courses_with_hits':[r for r in courses if r['hits']],'lift_hits':lift,'wood_mass_scenario750_kg':report['wood_mass_scenario750_kg'],'wood_mass_scenario900_kg':report['wood_mass_scenario900_kg'],'targets':len(obstacles),'invalid':report['invalid']},ensure_ascii=False)
