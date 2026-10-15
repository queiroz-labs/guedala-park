"""Read-only R23 console audit: external hardware contacts, four changed leaves.
Never tests same-assembly metal pairs or saves a FreeCAD document.
"""
from pathlib import Path
import json, hashlib, time, traceback
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
started=time.monotonic()
report={'status':'running','scope':'External hardware contacts only; changed R18 leaves in R23 source coordinates; mirror isometry preserves intersections',
 'threshold_volume_mm3':0.1,'bbox_epsilon_mm':1e-6,'budget_s':300,
 'excluded':['front-front SAT and boolean audits','same hinge assembly metal contacts','70T3553','MOVENTO','manufacturing or load approval'],
 'cases':[],'contacts':[],'errors':[],'stats':{'pairs':0,'bbox_rejected':0,'booleans':0},'manifest':{}}
out=(Path(__file__).resolve().parent / 'Auditoria_externa_R23.json').resolve()
def dump():
 report['elapsed_s']=time.monotonic()-started
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class BudgetExceeded(Exception):pass
def check_budget():
 if time.monotonic()-started>report['budget_s']:raise BudgetExceeded('Bounded computation budget exceeded')
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def bbox(b):return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def test(s,t,context):
 check_budget();report['stats']['pairs']+=1
 x,y=s.BoundBox,t.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):
  report['stats']['bbox_rejected']+=1;return
 report['stats']['booleans']+=1
 t0=time.monotonic()
 try:
  common=s.common(t)
  volume=common.Volume
  if volume>.1:
   report['contacts'].append(dict(context,volume_mm3=volume,contact_bbox_source_mm=bbox(common.BoundBox),boolean_s=time.monotonic()-t0))
 except Exception:
  report['errors'].append(dict(context,error=traceback.format_exc()))
 dump()
d=None
try:
 assert not App.GuiUp
 a=json.loads(((Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Montagem_R18.json').resolve()).read_text(encoding='utf-8'))
 plan=json.loads(((Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Dados_plano_R18.json').resolve()).read_text(encoding='utf-8'))
 source=Path(json.loads(((Path(__file__).resolve().parent / '../Rotulos_R23_2026-10-14/Rotulos_R23.json').resolve()).read_text(encoding='utf-8'))['file'])
 report.update(file=str(source),source_sha256_before=sha(source),runtime_version=list(App.Version()),gui_up=bool(App.GuiUp))
 d=App.openDocument(str(source));rows=a['doors'];changed=[r for r in rows if r['door'] in a['changed_doors']]
 # Existing explicit scope, including one conservative retired reserve
 # DivisorApoioVizinhaR03. No visibility-based omission. Separate it in reports.
 names=list(dict.fromkeys(t['name'] for t in plan['targets']))
 # FaixaFixaEstudo is an adopted proposed reserve, confirmed by owner in R23.
 names+=['PlacaL','PlacaL001','Peca255','Peca256','LateralApoioPrincipal']
 names=list(dict.fromkeys(names))
 statics={n:shape(d.getObject(n)) for n in names}
 hardware=lambda r:[d.getObject(b['body']) for h in r['hinges'] for b in h['bodies']]+[d.getObject(h['plate']) for h in r['hinges']]
 # Only the own front and actual support plane are classified as mounting interfaces.
 supports={}
 for r in changed:
  m=d.getObject(r['module']);inv=m.getGlobalPlacement().inverse();x=r['hinge_support_inner_x_mm'];ss=[]
  for o in m.Group:
   if o.TypeId!='Part::Box':continue
   s=o.Shape.copy();s.Placement=inv.multiply(o.getGlobalPlacement());bb=s.BoundBox
   if abs(bb.XMin-x)<1e-5:ss.append(o.Name)
  supports[r['door']]=ss
 report['manifest']={'changed':[dict(door=r['door'],label=d.getObject(r['door']).Label,control=r['control'],front=r['front'],mount_supports=supports[r['door']],hardware=[o.Name for o in hardware(r)]) for r in changed],
  'stationary_targets':[dict(name=n,label=d.getObject(n).Label,scope='historical_additional_conservative' if n=='DivisorApoioVizinhaR03' else 'adopted_participant') for n in names],
  'neighbor_fronts':[r['front'] for r in rows]+['FrenteSimplesR04','FrenteSimplesR001'],
  'explicit_active_reserve':'FaixaFixaEstudo, 7x18x272 as saved, not replaced by documentary 25mm'}
 def reset(angle=0):
  for r in rows:d.getObject(r['control']).Abertura=angle
  d.getObject('ControleSimplesR04').set('B2',str(angle)+' deg');d.getObject('ControleSimplesR04').set('B3',str(angle)+' deg');d.recompute()
 def external_case(r,angle,mode):
  targets=dict(statics)
  targets.update({q['front']:shape(d.getObject(q['front'])) for q in rows})
  targets.update({n:shape(d.getObject(n)) for n in ['FrenteSimplesR04','FrenteSimplesR001']})
  before=len(report['contacts']);stats=dict(report['stats'])
  for o in hardware(r):
   s=shape(o)
   for n,t in targets.items():
    category='mounting_interface' if n==r['front'] or n in supports[r['door']] else 'obstacle_or_neighbor'
    test(s,t,dict(mode=mode,door=r['door'],angle_deg=angle,hardware=o.Name,hardware_label=o.Label,target=n,target_label=d.getObject(n).Label,category=category))
  report['cases'].append(dict(mode=mode,door=r['door'],angle_deg=angle,new_contacts=len(report['contacts'])-before,stats_delta={k:report['stats'][k]-stats[k] for k in stats}))
  dump()
 reset()
 for r in changed:
  for angle in [0,30,60,86]:
   check_budget();d.getObject(r['control']).Abertura=angle;d.recompute();external_case(r,angle,'individual_others_closed')
  d.getObject(r['control']).Abertura=0;d.recompute()
 for angle in [30,60,86]:
  check_budget();reset(angle)
  for r in changed:external_case(r,angle,'simultaneous')
  # Different-leaf hardware only, at least one changed leaf. Includes current R04 corner.
  groups=[(r['door'],r['module'],hardware(r)) for r in rows]
  groups += [('CantoR04A','Modulo003',[o for o in d.Objects if o.Name=='FerragemSimplesR04' or (o.Name.startswith('FerragemSimplesR') and o.Name[len('FerragemSimplesR'):].isdigit() and 1<=int(o.Name[len('FerragemSimplesR'):])<=11)]),
             ('CantoR04B','Modulo003',[o for o in d.Objects if o.Name.startswith('FerragemSimplesR') and o.Name[len('FerragemSimplesR'):].isdigit() and 12<=int(o.Name[len('FerragemSimplesR'):])<=23])]
  ch={r['door'] for r in changed};before=len(report['contacts']);count=0
  for i,(one,mn,hs) in enumerate(groups):
   for two,mt,ht in groups[i+1:]:
    if mn!=mt or not ({one,two}&ch):continue
    for o in hs:
     s=shape(o)
     for q in ht:
      count+=1;test(s,shape(q),dict(mode='different_leaf_hardware',angle_deg=angle,doors=[one,two],hardware=o.Name,hardware_label=o.Label,target=q.Name,target_label=q.Label,category='obstacle_or_neighbor'))
  report['cases'].append(dict(mode='different_leaf_hardware',angle_deg=angle,pairs=count,new_contacts=len(report['contacts'])-before));dump()
 report['status']='complete_sampled_scope'
except BudgetExceeded as exc:
 report.update(status='partial_budget_limit',error=str(exc))
except Exception:
 report.update(status='failed',error=traceback.format_exc())
finally:
 if d is not None:App.closeDocument(d.Name)
 if 'file' in report:report['source_sha256_after']=sha(Path(report['file']));report['source_unchanged']=report['source_sha256_before']==report['source_sha256_after']
 report['limits']='Amostras discretas; volumes >0,1 mm3 são triagem CAD, não tolerância certificada. Nenhuma prova contínua, carga/fixação/usinagem, batente, fabricação ou homologação interna da ferragem. Corpos fonte avaliados no referencial preservado; reflexão comum conserva contatos. CAD não salvo.'
 dump()
 print('AUDIT_RESULT',json.dumps({k:report[k] for k in ['status','elapsed_s','stats','source_unchanged'] if k in report}),len(report['contacts']))
