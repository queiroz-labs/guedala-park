"""Only previously uncovered moving families vs unchanged whole architecture."""
from pathlib import Path
import json,time,hashlib,traceback
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve();started=time.monotonic();budget=240
source=(Path(__file__).resolve().parent / '../Implantacao_R24_2026-10-14/Guedala_Park_R24_Implantacao_Corrigida.FCStd').resolve()
manifest=json.loads(((Path(__file__).resolve().parent / '../Auditoria_implantacao_R23_2026-10-14/Manifesto_implantacao_R23.json').resolve()).read_text(encoding='utf-8'))
report={'file':str(source),'status':'running','budget_s':budget,'criterion_mm3':.1,'bbox_epsilon_mm':1e-6,
 'scope':'Only new R10 twelve hinged leaves, R04 two corner leaves and current G2 rigid moving box/locks/program against 27 whole walls and 9 floors. No zero pose, furniture/front pairs, own wood, intrahardware, guide telescoping or old family repeat.',
 'sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),'cases':[],'contacts':[],'errors':[],'manifest':{},'stats':{'pairs':0,'bbox_rejected':0,'booleans':0}}
out=(Path(__file__).resolve().parent / 'Movimentos_arquitetura_R24.json').resolve()
def dump():
 report['elapsed_s']=time.monotonic()-started;out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
def check():
 if time.monotonic()-started>budget:raise TimeoutError('240s budget exhausted')
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def bb(b):return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def ancestors(o):
 chain=[]
 while o is not None:chain.append(o.Name);o=o.getParentGeoFeatureGroup()
 return chain
def test(s,t,context):
 check();report['stats']['pairs']+=1;x,y=s.BoundBox,t.BoundBox
 if any(getattr(x,k+'Max')<=getattr(y,k+'Min')+1e-6 or getattr(y,k+'Max')<=getattr(x,k+'Min')+1e-6 for k in ['X','Y','Z']):report['stats']['bbox_rejected']+=1;return
 report['stats']['booleans']+=1
 try:
  c=s.common(t)
  if c.Volume>.1:
   b=bb(c.BoundBox);report['contacts'].append(dict(context,volume_mm3=c.Volume,contact_bbox_source_mm=b,contact_bbox_mirrored_mm=[7400-b[3],b[1],b[2],7400-b[0],b[4],b[5]]));dump()
 except Exception:report['errors'].append(dict(context,error=traceback.format_exc()));dump()
d=None
try:
 assert not App.GuiUp
 d=App.openDocument(str(source));report['gui_up']=bool(App.GuiUp)
 arch={r['name']:shape(d.getObject(r['name'])) for r in manifest['architecture']}
 report['manifest']['architecture']=[{'name':r['name'],'label':r['label'],'class':r['architectural_class']} for r in manifest['architecture']]
 r10=json.loads(((Path(__file__).resolve().parent / '../Dobradicas_R10_2026-10-14/Montagem_R10.json').resolve()).read_text(encoding='utf-8'))['doors']
 roles=[]
 for r in r10:
  metal=[b['body'] for h in r['hinges'] for b in h['bodies']]+[h['plate'] for h in r['hinges']]
  roles.append({'family':'R10','door':r['door'],'label':d.getObject(r['door']).Label,'control':r['control'],'field':'Abertura','moving':[r['front']]+metal})
 def corner_names(role):
  found=[r['name'] for r in manifest['items'] if r['name'].startswith('FerragemSimples') and ((' '+role+' - ') in r['label'] or ('porta '+role) in r['label'])]
  assert len(found)==12,(role,found)
  return found
 for role,front,panel,cell in [('A','FrenteSimplesR04','PainelSimplesR04','B2'),('B','FrenteSimplesR001','PainelSimplesR001','B3')]:
  f=d.getObject(front);assert f.Base.Name==panel,(front,f.Base.Name,panel)
  chain=ancestors(f);assert 'CantoSimplesR04' in chain,chain
  roles.append({'family':'R04','door':'CantoR04'+role,'label':f.Label,'control':'ControleSimplesR04','field':cell,'front':front,'front_base':panel,'front_ancestors':chain,'moving':[front]+corner_names(role)})
 g=d.getObject('Gaveta005');assert g is not None and 'Extensao' in g.PropertiesList
 assert any('MontagemG2R' in o.Name for o in g.Group),(g.Name,[o.Name for o in g.Group])
 movable=[r['name'] for r in manifest['items'] if r['adoption_scope']=='adopted_result' and g.Name in ancestors(d.getObject(r['name']))]
 assert movable
 roles.append({'family':'G2R07','door':g.Name,'label':g.Label,'control':g.Name,'field':'Extensao','moving':movable,
  'stationary_guide_excluded':[r['name'] for r in manifest['items'] if r['source_root']=='Modulo005' and 'GuiasG2R07' in ancestors(d.getObject(r['name']))]})
 for r in roles:r['moving_metadata']=[{'name':n,'label':d.getObject(n).Label,'ancestors':ancestors(d.getObject(n))} for n in r['moving']]
 report['manifest']['moving_roles']=roles
 for r in r10:d.getObject(r['control']).Abertura=0
 d.getObject('ControleSimplesR04').set('B2','0 deg');d.getObject('ControleSimplesR04').set('B3','0 deg');g.Extensao=0;d.recompute()
 for role in roles:
  for value in ([100,200,300,400,500] if role['family']=='G2R07' else [30,60,86]):
   check();control=d.getObject(role['control'])
   if role['family']=='R04':control.set(role['field'],str(value)+' deg')
   else:setattr(control,role['field'],value)
   d.recompute();before=len(report['contacts']);stats=dict(report['stats']);moving_boxes=[]
   for n in role['moving']:
    o=d.getObject(n);s=shape(o);moving_boxes.append({'name':n,'bbox_source_mm':bb(s.BoundBox)})
    for target in manifest['architecture']:
     test(s,arch[target['name']],{'family':role['family'],'door':role['door'],'value':value,'unit':'mm' if role['family']=='G2R07' else 'deg','moving':n,'moving_label':o.Label,'target':target['name'],'target_label':target['label'],'target_class':target['architectural_class']})
   report['cases'].append({'family':role['family'],'door':role['door'],'value':value,'new_contacts':len(report['contacts'])-before,'stats_delta':{k:report['stats'][k]-stats[k] for k in stats},'moving_bbox':moving_boxes});dump()
  if role['family']=='R04':d.getObject(role['control']).set(role['field'],'0 deg')
  else:setattr(d.getObject(role['control']),role['field'],0)
  d.recompute()
 report['status']='complete_new_sampled_architecture_scope'
except TimeoutError as e:report.update(status='partial_budget_limit',error=str(e))
except Exception:report.update(status='failed',error=traceback.format_exc())
finally:
 if d is not None:App.closeDocument(d.Name)
 report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest();report['source_unchanged']=report['sha256_before']==report['sha256_after']
 report['limits']='Discrete new architecture-only samples, not continuous motion, loads/fixation/real stops, tolerance certification or fabrication. G2 is rigid translation; fixed MOVENTO guides not translated, no physical telescoping. Tray loaded withdrawal lift/advance segments remain outside this scope. No ceiling solid to audit. No CAD save or GUI.'
 dump();print('NEW_MOVEMENT_RESULT',report['status'],len(report['cases']),report['stats'],len(report['contacts']),len(report['errors']),report['source_unchanged'])
