from pathlib import Path
import json,math
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(v for v in App.listDocuments().values() if v.FileName and Path(v.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R11_Apoios_Simples.FCStd').resolve())
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R11.json').resolve()).read_text(encoding='utf-8'));axes=json.loads(((Path(__file__).resolve().parent / 'Eixos_71B3550.json').resolve()).read_text(encoding='utf-8'))
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def common(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):return 0
 return a.common(b).Volume
def point(o,p):return o.getGlobalPlacement().multiply(o.Placement.inverse()).multVec(App.Vector(p[0],0,p[1]))
cases=[];joints=[];closed=[]
for r in data['doors']:
 g=doc.getObject(r['door']);control=doc.getObject(r['control']);module=doc.getObject(r['module']);front=doc.getObject(r['front'])
 wood=[o for o in module.Group if o.TypeId=='Part::Box']+([doc.getObject('DivisorApoioVizinhaR03')] if module.Name=='Modulo003' else [])+[front]
 adjacent=[doc.getObject(x['front']) for x in data['doors'] if x['door']!=r['door'] and x['module']==r['module']]+([doc.getObject('VizinhaComCanecosR03')] if module.Name=='Modulo003' else [])
 hardware=[doc.getObject(b['body']) for h in r['hinges'] for b in h['bodies']]+[doc.getObject(h['plate']) for h in r['hinges']]
 for angle in [0,30,60,86]:
  control.Abertura=angle;doc.recompute();hits=[]
  for o in hardware:
   a=shape(o)
   for q in wood+adjacent:
    v=common(a,shape(q))
    if v>.1:hits.append({'hardware':o.Label,'wood':q.Label,'mm3':v})
  fa=shape(front)
  for q in wood[:-1]+adjacent:
   v=common(fa,shape(q))
   if v>.1:hits.append({'front':front.Label,'wood':q.Label,'mm3':v})
  cases.append({'door':g.Name,'module':module.Label,'angle':angle,'hits':hits})
  for h in r['hinges']:
   bs={b['index']:doc.getObject(b['body']) for b in h['bodies']}
   residuals=[]
   for i,j,key in [(1,2,'a'),(1,3,'b'),(2,4,'c'),(3,4,'d')]:residuals.append((point(bs[i],axes[key])-point(bs[j],axes[key])).Length)
   hole=front.Tool.Shapes[0 if h['level']==r['hinges'][0]['level'] else 1]
   hp=g.getGlobalPlacement().multVec(hole.Placement.Base)
   cp=point(bs[4],[-6.5,38.5])
   joints.append({'door':g.Name,'level':h['level'],'angle':angle,'joint_residual_mm':max(residuals),'cup_axis_reference_residual_mm':(hp-cp).Length})
  if angle==0:
   b=fa.optimalBoundingBox();closed.append({'door':g.Name,'bbox':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]})
 control.Abertura=0;doc.recompute()
simultaneous=[]
for angle in [30,60,86]:
 for r in data['doors']:doc.getObject(r['control']).Abertura=angle
 doc.recompute();hits=[]
 for i,r in enumerate(data['doors']):
  for q in data['doors'][i+1:]:
   a,b=shape(doc.getObject(r['front'])),shape(doc.getObject(q['front']));v=common(a,b)
   if v>.1:hits.append({'pair':[r['door'],q['door']],'mm3':v})
 simultaneous.append({'angle_all':angle,'hits':hits})
for r in data['doors']:doc.getObject(r['control']).Abertura=0
doc.recompute();doc.save()

# Changed third leaf against existing neighbor in its proposed study opening.
neighbour=[]
s=doc.getObject('ControleCanto');s.set('B4','86 deg');doc.recompute()
r=next(x for x in data['doors'] if x['door']=='Folha002');control=doc.getObject(r['control']);nf=doc.getObject('VizinhaComCanecosR03')
for angle in [0,30,60,86]:
 control.Abertura=angle;doc.recompute();neighbour.append({'new_door_angle':angle,'neighbor_input_deg':86,'front_intersection_mm3':common(shape(doc.getObject(r['front'])),shape(nf))})
control.Abertura=0;s.set('B4','0 deg');doc.recompute();doc.save()
report={'neighbor_changed_leaf':neighbour,'cases':cases,'joints':joints,'closed':closed,'simultaneous':simultaneous,
 'max_joint_residual_mm':max(r['joint_residual_mm'] for r in joints),'max_cup_reference_residual_mm':max(r['cup_axis_reference_residual_mm'] for r in joints),
 'scope':'Geometria rigidamente articulada pelos eixos STEP,28 posições individuais e3 iguais simultâneas. Não testa batente70T3553, carga, tolerâncias ou todas as combinações com gavetas.'}
((Path(__file__).resolve().parent / 'Auditoria_R11.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({'cases_with_hits':[r for r in cases if r['hits']],'max_joint_residual_mm':report['max_joint_residual_mm'],'max_cup_reference_residual_mm':report['max_cup_reference_residual_mm'],'simultaneous':simultaneous,'neighbor':neighbour},ensure_ascii=False)
