"""Only different-angle hardware-hardware combinations of the 14 existing pairs."""
from pathlib import Path
import json,time,hashlib,traceback
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();started=time.monotonic();budget=120
old=json.loads(((Path(__file__).resolve().parent / 'Auditoria_externa_R23.json').resolve()).read_text(encoding='utf-8'))
source=Path(old['file']);report={'file':str(source),'status':'running','budget_s':budget,'angles_deg':[0,30,60,86],
 'criterion_mm3':0.1,'bbox_epsilon_mm':1e-6,'excluded':'Equal-angle diagonals, wood/front targets, same-leaf/same-hinge pairs, SAT, shape validations',
 'sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),'stats':{'pairs':0,'bbox_rejected':0,'booleans':0},'cases':[],'contacts':[],'errors':[]}
out=(Path(__file__).resolve().parent / 'Complemento_angulos_independentes_R23.json').resolve()
def dump():
 report['elapsed_s']=time.monotonic()-started;out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
def check():
 if time.monotonic()-started>budget:raise TimeoutError('120s budget exhausted')
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def bbox(b):return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def test(s,t,context):
 check();report['stats']['pairs']+=1;x,y=s.BoundBox,t.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):
  report['stats']['bbox_rejected']+=1;return
 report['stats']['booleans']+=1
 try:
  common=s.common(t)
  if common.Volume>.1:report['contacts'].append(dict(context,volume_mm3=common.Volume,contact_bbox_source_mm=bbox(common.BoundBox)));dump()
 except Exception:report['errors'].append(dict(context,error=traceback.format_exc()));dump()
d=None
try:
 assert not App.GuiUp
 d=App.openDocument(str(source));a=json.loads(((Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Montagem_R18.json').resolve()).read_text(encoding='utf-8'));rows=a['doors'];changed=set(a['changed_doors'])
 def hardware(r):return [b['body'] for h in r['hinges'] for b in h['bodies']]+[h['plate'] for h in r['hinges']]
 groups=[{'door':r['door'],'module':r['module'],'control':r['control'],'hardware':hardware(r)} for r in rows]
 groups += [{'door':'CantoR04A','module':'Modulo003','control':'ControleSimplesR04.B2','hardware':[o.Name for o in d.Objects if o.Name=='FerragemSimplesR04' or (o.Name.startswith('FerragemSimplesR') and o.Name[len('FerragemSimplesR'):].isdigit() and 1<=int(o.Name[len('FerragemSimplesR'):])<=11)]},
            {'door':'CantoR04B','module':'Modulo003','control':'ControleSimplesR04.B3','hardware':[o.Name for o in d.Objects if o.Name.startswith('FerragemSimplesR') and o.Name[len('FerragemSimplesR'):].isdigit() and 12<=int(o.Name[len('FerragemSimplesR'):])<=23]}]
 pairs=[(g,h) for i,g in enumerate(groups) for h in groups[i+1:] if g['module']==h['module'] and ({g['door'],h['door']}&changed)]
 assert len(pairs)==14
 report['manifest']={'groups':groups,'pairs':[[g['door'],h['door']] for g,h in pairs],'method':'Cache each independent leaf hardware pose once at each angle; evaluate off-diagonal combinations only, no live recompute per pair. Source coordinate reflection isometry retained.'}
 cache={}
 for angle in report['angles_deg']:
  check()
  for r in rows:d.getObject(r['control']).Abertura=angle
  d.getObject('ControleSimplesR04').set('B2',str(angle)+' deg');d.getObject('ControleSimplesR04').set('B3',str(angle)+' deg');d.recompute()
  for g in groups:cache[(g['door'],angle)]=[(n,shape(d.getObject(n))) for n in g['hardware']]
  dump()
 for g,h in pairs:
  for one in report['angles_deg']:
   for two in report['angles_deg']:
    if one==two:continue
    before=len(report['contacts']);stats=dict(report['stats'])
    for n,s in cache[(g['door'],one)]:
     for m,t in cache[(h['door'],two)]:
      test(s,t,dict(doors=[g['door'],h['door']],angles_deg=[one,two],hardware=n,hardware_label=d.getObject(n).Label,target=m,target_label=d.getObject(m).Label))
    report['cases'].append({'doors':[g['door'],h['door']],'angles_deg':[one,two],'new_contacts':len(report['contacts'])-before,'stats_delta':{k:report['stats'][k]-stats[k] for k in stats}});dump()
 report['status']='complete_sampled_off_diagonal_scope'
except TimeoutError as e:report.update(status='partial_budget_limit',error=str(e))
except Exception:report.update(status='failed',error=traceback.format_exc())
finally:
 if d is not None:App.closeDocument(d.Name)
 report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest();report['source_unchanged']=report['sha256_before']==report['sha256_after']
 report['limits']='Off-diagonal discrete angles only; no continuous sweep, certified tolerance/load/fixation/stop or manufacturing release. No CAD save or GUI.'
 dump();print('INDEPENDENT_RESULT',report['status'],len(report['cases']),report['stats'],len(report['contacts']),len(report['errors']),report['source_unchanged'])
