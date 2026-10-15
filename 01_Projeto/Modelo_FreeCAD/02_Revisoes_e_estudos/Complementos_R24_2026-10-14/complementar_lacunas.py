from pathlib import Path
import json,time,hashlib,traceback,math
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve();started=time.monotonic();budget=180
source=(Path(__file__).resolve().parent / '../Implantacao_R24_2026-10-14/Guedala_Park_R24_Implantacao_Corrigida.FCStd').resolve()
manifest=json.loads(((Path(__file__).resolve().parent / '../Auditoria_implantacao_R23_2026-10-14/Manifesto_implantacao_R23.json').resolve()).read_text(encoding='utf-8'))
report={'file':str(source),'status':'running','budget_s':budget,'criterion_mm3':.1,'bbox_epsilon_mm':1e-6,
 'sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),'tray_segments':[],'office_drawer_sweeps':[],'upper_office_z_proof':{},'contacts':[],'inconclusive':[],'errors':[],
 'stats':{'pairs':0,'bbox_rejected':0,'booleans':0}}
out=(Path(__file__).resolve().parent / 'Complementos_R24.json').resolve()
def dump():report['elapsed_s']=time.monotonic()-started;out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
def check():
 if time.monotonic()-started>budget:raise TimeoutError('180s bounded budget exhausted')
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def bb(b):return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def union(b,c):return [min(b[i],c[i]) for i in range(3)]+[max(b[i],c[i]) for i in range(3,6)]
def ancestors(o):
 out=[]
 while o:out.append(o);o=o.getParentGeoFeatureGroup()
 return out
def test_swept_box(bounds,target,context):
 check();report['stats']['pairs']+=1;b=bb(target.BoundBox)
 if any(bounds[i+3]<=b[i]+1e-6 or b[i+3]<=bounds[i]+1e-6 for i in range(3)):
  report['stats']['bbox_rejected']+=1;return
 report['stats']['booleans']+=1
 try:
  s=Part.makeBox(*[bounds[i+3]-bounds[i] for i in range(3)],App.Vector(*bounds[:3]));c=s.common(target)
  if c.Volume>.1:
   report['inconclusive'].append(dict(context,swept_bbox_source_mm=bounds,conservative_common_mm3=c.Volume,reason='Positive swept BoundingBox is not automatically an actual shape collision; needs affected-scope review'));dump()
 except Exception:report['errors'].append(dict(context,error=traceback.format_exc()));dump()
d=None
try:
 assert not App.GuiUp
 d=App.openDocument(str(source));report['gui_up']=bool(App.GuiUp)
 arch={r['name']:shape(d.getObject(r['name'])) for r in manifest['architecture']}
 # Exact three loaded tray translation segments from R07, drawer open500.
 g2=d.getObject('Gaveta005');g2.Extensao=500;d.recompute()
 trays=[o for o in g2.Group if o.Label.startswith('Bandeja removivel')];assert len(trays)==2
 for tray in trays:
  original=tray.Placement.copy()
  parts=[d.getObject(r['name']) for r in manifest['items'] if r['adoption_scope']=='adopted_result' and tray.Name in [o.Name for o in ancestors(d.getObject(r['name']))]]
  for title,delta in [('elevar120',App.Vector(0,0,120)),('avancar40',App.Vector(0,-40,0)),('elevarmais100',App.Vector(0,0,100))]:
   check();start=list(tray.Placement.Base);before={o.Name:bb(shape(o).BoundBox) for o in parts}
   tray.Placement.Base=tray.Placement.Base+delta;d.recompute();case={'tray':tray.Name,'label':tray.Label,'drawer_extension_mm':500,'segment':title,'from_local_mm':start,'to_local_mm':list(tray.Placement.Base),'parts':[]}
   for o in parts:
    swept=union(before[o.Name],bb(shape(o).BoundBox));case['parts'].append({'name':o.Name,'swept_bbox_source_mm':swept})
    for target in manifest['architecture']:test_swept_box(swept,arch[target['name']],{'scope':'loaded_tray_architecture','tray':tray.Name,'segment':title,'moving':o.Name,'target':target['name']})
   report['tray_segments'].append(case);dump()
  tray.Placement=original;d.recompute()
 g2.Extensao=0;d.recompute()
 # Source daily sofa currently adopted: only five displayed physical primitives.
 sofa_names=['Peca122','Peca123','Peca124','Peca125','Peca126'];sofa={n:shape(d.getObject(n)) for n in sofa_names}
 report['sofa']=[{'name':n,'label':d.getObject(n).Label,'bbox_source_mm':bb(s.BoundBox)} for n,s in sofa.items()]
 rows=json.loads(((Path(__file__).resolve().parent / '../Padronizacao_R08_2026-10-14/Padronizacao_R08.json').resolve()).read_text(encoding='utf-8'))['changed_drawers']
 for row in [r for r in rows if r['drawer'] in ['Gaveta008','Gaveta009']]:
  check();g=d.getObject(row['drawer']);g.Extensao=0;d.recompute();pl0=g.getGlobalPlacement()
  before={n:{'bbox':bb(shape(d.getObject(n)).BoundBox),'matrix':d.getObject(n).getGlobalPlacement().Matrix.A} for n in row['moving_names']}
  expr=list(g.ExpressionEngine);assert any(path.lstrip('.')=='Placement.Base.y' and 'Extensao' in text for path,text in expr),expr
  g.Extensao=400;d.recompute();pl1=g.getGlobalPlacement();delta=pl1.Base-pl0.Base
  assert max(abs(x-y) for x,y in zip(pl0.Rotation.toMatrix().A,pl1.Rotation.toMatrix().A))<1e-9
  case={'drawer':g.Name,'label':g.Label,'interval_mm':[0,400],'source_expression_engine':expr,'parent':g.getParentGeoFeatureGroup().Name,'global_translation_mm':list(delta),'parts':[]}
  for n in row['moving_names']:
   o=d.getObject(n);after=o.getGlobalPlacement().Matrix.A;old=before[n]['matrix']
   assert all(abs(after[k]-old[k])<1e-9 for k in [0,1,2,4,5,6,8,9,10])
   assert max(abs(after[k]-old[k]-v) for k,v in zip([3,7,11],list(delta)))<1e-6
   swept=union(before[n]['bbox'],bb(shape(o).BoundBox));case['parts'].append({'name':n,'swept_bbox_source_mm':swept})
   for target,s in sofa.items():test_swept_box(swept,s,{'scope':'office_drawer_vs_new_daily_sofa','drawer':g.Name,'moving':n,'target':target})
  report['office_drawer_sweeps'].append(case);g.Extensao=0;d.recompute();dump()
 # Prove Z invariance without angle samples: each dynamic translation is horizontal
 # after parent rotation, and each dynamic rotation axis is world vertical.
 r18=json.loads(((Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Montagem_R18.json').resolve()).read_text(encoding='utf-8'))['doors']
 office=[r for r in r18 if r['module']=='Modulo016'];mov=[]
 for r in office:mov+=[r['front']]+[b['body'] for h in r['hinges'] for b in h['bodies']]+[h['plate'] for h in r['hinges']]
 assert len(set(mov))==52
 dynamic={};proof_parts=[]
 for n in mov:
  o=d.getObject(n);s=shape(o);proof_parts.append({'name':n,'z_interval_source_mm':[s.BoundBox.ZMin,s.BoundBox.ZMax]})
  for a in ancestors(o):
   expressions=[(p.lstrip('.'),t) for p,t in getattr(a,'ExpressionEngine',[]) if p.lstrip('.').startswith('Placement.')]
   if not expressions:continue
   parent=a.getParentGeoFeatureGroup();rot=parent.getGlobalPlacement().Rotation if parent else App.Rotation()
   checks=[]
   for p,t in expressions:
    if p.startswith('Placement.Base.'):
     axis=p[-1];v={'x':App.Vector(1,0,0),'y':App.Vector(0,1,0),'z':App.Vector(0,0,1)}[axis];world=rot.multVec(v);ok=abs(world.z)<1e-9
    elif p=='Placement.Rotation.Angle':world=rot.multVec(a.Placement.Rotation.Axis);ok=abs(abs(world.z)-1)<1e-9
    else:world=App.Vector();ok=False
    checks.append({'field':p,'expression':t,'world_axis':list(world),'z_invariant':ok})
   dynamic[a.Name]={'name':a.Name,'parent':parent.Name if parent else None,'checks':checks}
 invariance=all(c['z_invariant'] for v in dynamic.values() for c in v['checks'])
 zlo=min(r['z_interval_source_mm'][0] for r in proof_parts);zhi=max(r['z_interval_source_mm'][1] for r in proof_parts)
 szmax=max(s.BoundBox.ZMax for s in sofa.values());gap=zlo-szmax
 report['upper_office_z_proof']={'moving_parts':proof_parts,'dynamic_transform_checks':list(dynamic.values()),'z_invariant':invariance,'upper_office_interval_mm':[zlo,zhi],'sofa_max_z_mm':szmax,'minimum_vertical_separation_mm':gap,'proven_separate_for_all_inputs_of_current_horizontal_model':invariance and gap>0}
 if not invariance or gap<=0:report['inconclusive'].append({'scope':'upper_office_vs_sofa_z','reason':'Cannot prove invariant disjoint Z intervals'})
 report['status']='complete_scoped_complements'
except TimeoutError as e:report.update(status='partial_budget_limit',error=str(e))
except Exception:report.update(status='failed',error=traceback.format_exc())
finally:
 if d is not None:App.closeDocument(d.Name)
 report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest();report['source_unchanged']=report['sha256_before']==report['sha256_after']
 report['limits']='Continuous envelopes of specified rigid translations only; no new inside/bancada tests, old pose repeats, actual hand/people/cushions/guest conversion, intrahardware, physical guide/caster functioning or tolerance/load/fixation/fabrication release. Upper-office proof is only invariant Z separation from adopted daily sofa.'
 dump();print('COMPLEMENTS_RESULT',report['status'],report['stats'],len(report['inconclusive']),len(report['errors']),report['source_unchanged'])
