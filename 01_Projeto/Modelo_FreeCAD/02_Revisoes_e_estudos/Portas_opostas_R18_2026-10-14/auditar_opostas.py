from pathlib import Path
import json,math
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();a=json.loads(((Path(__file__).resolve().parent / 'Montagem_R18.json').resolve()).read_text(encoding='utf-8'));p=Path(a['file'])
d=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==p);rows=a['doors'];changed=set(a['changed_doors'])
axes=json.loads(((Path(__file__).resolve().parent / '../Apoios_R11_2026-10-14/Eixos_71B3550.json').resolve()).read_text(encoding='utf-8'))
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def intersect(s,t):
 x=s.optimalBoundingBox();y=t.optimalBoundingBox()
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return s.common(t).Volume
def axispoint(o,p):return o.getGlobalPlacement().multiply(o.Placement.inverse()).multVec(App.Vector(p[0],0,p[1]))
corner=[]
for o in d.Objects:
 if o.Name in ['PlacaL','PlacaL001','Peca255','Peca256','LateralApoioPrincipal','DivisorApoioVizinhaR03','FaixaFixaEstudo'] or o.Name.startswith(('FrenteSimples','FerragemSimples','ApoioPortaB','FaixaQuina')):corner.append(o)
wood_by_module={}
for mn in ['Modulo016','Modulo003']:
 wood_by_module[mn]=[o for o in d.getObject(mn).Group if o.TypeId=='Part::Box']+([o for o in corner if not o.Name.startswith('Ferragem')] if mn=='Modulo003' else [])
statics=[]
for o in d.Objects:
 if o.Name.startswith('Peca') and o.Name[4:].isdigit() and int(o.Name[4:])<235 and getattr(o,'TipoPeca','')!='Parede em corte':statics.append(o)
cases=[];joints=[];valid=[]
def reset():
 for r in rows:d.getObject(r['control']).Abertura=0
 d.getObject('ControleSimplesR04').set('B2','0 deg');d.getObject('ControleSimplesR04').set('B3','0 deg');d.recompute()
reset()
# Check added ordinary panels against current structure; contacts are not strength proof.
support_hits=[]
for r in a['new_supports']:
 o=d.getObject(r['name'])
 for q in wood_by_module[r['module']]:
  if q.Name!=o.Name:
   v=intersect(shape(o),shape(q))
   if v>.1:support_hits.append({'support':o.Name,'target':q.Name,'mm3':v})
for r in [x for x in rows if x['door'] in changed]:
 g=d.getObject(r['door']);control=d.getObject(r['control']);front=d.getObject(r['front']);m=d.getObject(r['module'])
 hardware=[d.getObject(b['body']) for h in r['hinges'] for b in h['bodies']]+[d.getObject(h['plate']) for h in r['hinges']]
 adjacent=[d.getObject(q['front']) for q in rows if q['module']==r['module'] and q['door']!=r['door']]
 for angle in [0,30,60,86]:
  control.Abertura=angle;d.recompute();hits=[]
  wood=wood_by_module[r['module']]
  for o in hardware:
   for q in wood+adjacent+[front]:
    v=intersect(shape(o),shape(q))
    if v>.1:hits.append({'hardware':o.Name,'target':q.Name,'mm3':v})
  for q in wood+adjacent+statics:
   v=intersect(shape(front),shape(q))
   if v>.1:hits.append({'front':front.Name,'target':q.Name,'mm3':v})
  # In module coordinates, positive input must move the free edge outwards (negativeY).
  inv=m.getGlobalPlacement().inverse();s=front.Shape.copy();s.Placement=inv.multiply(front.getGlobalPlacement());bb=s.optimalBoundingBox()
  cases.append({'door':r['door'],'angle':angle,'side':r['side'],'hits':hits,'local_bbox':[bb.XMin,bb.YMin,bb.ZMin,bb.XLength,bb.YLength,bb.ZLength]})
  if angle>0:assert bb.YMin < -1, 'Abertura para dentro: '+str(r)
  valid.append({'door':r['door'],'angle':angle,'front_valid':front.Shape.isValid(),'hardware_valid':all(o.Shape.isValid() for o in hardware)})
  for h in r['hinges']:
   bs={b['index']:d.getObject(b['body']) for b in h['bodies']};errs=[]
   for i,j,k in [(1,2,'a'),(1,3,'b'),(2,4,'c'),(3,4,'d')]:errs.append((axispoint(bs[i],axes[k])-axispoint(bs[j],axes[k])).Length)
   hole=front.Tool.Shapes[0 if h['level']==r['hinges'][0]['level'] else 1];hp=g.getGlobalPlacement().multVec(hole.Placement.Base);cp=axispoint(bs[4],[-6.5,38.5])
   joints.append({'door':r['door'],'angle':angle,'level':h['level'],'axis_residual_mm':max(errs),'cup_axis_residual_mm':(hp-cp).Length})
 control.Abertura=0;d.recompute()
sim=[]
for angle in [30,60,86]:
 for r in rows:d.getObject(r['control']).Abertura=angle
 d.getObject('ControleSimplesR04').set('B2',str(angle)+' deg');d.getObject('ControleSimplesR04').set('B3',str(angle)+' deg');d.recompute();hits=[]
 for i,r in enumerate(rows):
  for q in rows[i+1:]:
   if r['module']!=q['module']:continue
   v=intersect(shape(d.getObject(r['front'])),shape(d.getObject(q['front'])))
   if v>.1:hits.append({'fronts':[r['door'],q['door']],'mm3':v})
  if r['module']=='Modulo003':
   for o in corner:
    if not o.Name.startswith(('FrenteSimples','FerragemSimples')):continue
    v=intersect(shape(d.getObject(r['front'])),shape(o))
    if v>.1:hits.append({'head_front':r['door'],'corner':o.Name,'mm3':v})
 # Only different hinge assemblies on adjacent leaves, not unexplained internal source contacts.
 for mn in ['Modulo016','Modulo003']:
  rr=[r for r in rows if r['module']==mn]
  for i,r in enumerate(rr[:-1]):
   q=rr[i+1]
   if not ({r['door'],q['door']} & changed):continue
   one=[d.getObject(b['body']) for h in r['hinges'] for b in h['bodies']]+[d.getObject(h['plate']) for h in r['hinges']]
   two=[d.getObject(b['body']) for h in q['hinges'] for b in h['bodies']]+[d.getObject(h['plate']) for h in q['hinges']]
   for o in one:
    for t in two:
     v=intersect(shape(o),shape(t))
     if v>.1:hits.append({'hardware_pair':[o.Name,t.Name],'mm3':v})
 sim.append({'angle_all':angle,'hits':hits})
reset();d.save()
report={'file':str(p),'individual_cases':cases,'simultaneous':sim,'new_support_intersections':support_hits,'joint_residuals':joints,'validity':valid,'walls_room_targets':len(statics),'corner_explicit_targets':len(corner),'limits':'Quatro folhas alteradas testadas0/30/60/86; vizinhas atuais e canto simultâneo três posições. Poses amostradas, não continuidade/tolerâncias, carga/fixação ou batente mecânico. Sem contato entre corpos do mesmo STEP como critério de homologação.'}
((Path(__file__).resolve().parent / 'Auditoria_R18.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result={'individual_hits':sum(len(x['hits']) for x in cases),'simultaneous_hits':sum(len(x['hits']) for x in sim),'support_hits':support_hits,'max_axis_residual_mm':max(x['axis_residual_mm'] for x in joints),'max_cup_residual_mm':max(x['cup_axis_residual_mm'] for x in joints),'all_valid':all(x['front_valid'] and x['hardware_valid'] for x in valid)}
