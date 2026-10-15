"""New scope only: temporary Loop parking and the affected basket maintenance encounter."""
from pathlib import Path
import json, hashlib, time, traceback
import FreeCAD as App, Part

root=(Path(__file__).resolve().parent / '.').resolve()
base=(Path(__file__).resolve().parent / '../..').resolve()
source=(Path(__file__).resolve().parent / '../Programa_R25_2026-10-14/Guedala_Park_R25_Programa_Conferido.FCStd').resolve()
manifest=json.loads(((Path(__file__).resolve().parent / '../Auditoria_implantacao_R23_2026-10-14/Manifesto_implantacao_R23.json').resolve()).read_text(encoding='utf-8'))
r15=json.loads(((Path(__file__).resolve().parent / '../Cesto_R15_2026-10-14/Montagem_R15.json').resolve()).read_text(encoding='utf-8'))
out=(Path(__file__).resolve().parent / 'Estacionamento_Loop_R26.json').resolve()
started=time.monotonic()
report={'file':str(source),'status':'running','source_sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),
 'proposed_lateral_translation_source_mm':[650,0,0], 'cases':[], 'contacts':[], 'errors':[],
 'stats':{'pairs':0,'bbox_separated':0,'booleans':0}}
def dump():
 report['elapsed_s']=time.monotonic()-started
 out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def bb(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def swept(s,v):
 b=bb(s);c=[b[i]+v[i%3] for i in range(6)]
 return [min(b[i],c[i]) for i in range(3)]+[max(b[i],c[i]) for i in range(3,6)]
def check(bounds,target,context):
 assert time.monotonic()-started<120,'Bounded audit exceeded 120 seconds'
 report['stats']['pairs']+=1;b=bb(target)
 if any(bounds[i+3]<=b[i]+1e-6 or b[i+3]<=bounds[i]+1e-6 for i in range(3)):
  report['stats']['bbox_separated']+=1;return
 report['stats']['booleans']+=1
 try:
  box=Part.makeBox(*[bounds[i+3]-bounds[i] for i in range(3)],App.Vector(*bounds[:3]))
  common=box.common(target)
  if common.Volume>.1:report['contacts'].append(dict(context,conservative_common_mm3=common.Volume,swept_bbox_source_mm=bounds))
 except Exception:report['errors'].append(dict(context,error=traceback.format_exc()))
d=None
try:
 assert not App.GuiUp
 assert report['source_sha256_before']=='eef8683b0b9a1743156ef769540381492d1b3f32b2a3e32ff9f79b7d9ff1f40a'
 d=App.openDocument(str(source))
 bin_names=['Peca147','Peca148','Peca149']
 bins={n:shape(d.getObject(n)) for n in bin_names}
 report['bin_parts']=[{'name':n,'label':d.getObject(n).Label,'before_source_mm':bb(s),'parked_source_mm':[bb(s)[i]+(650 if i in [0,3] else 0) for i in range(6)]} for n,s in bins.items()]
 names={r['name'] for r in manifest['items'] if r['adoption_scope']=='adopted_result'}
 names.update(r['name'] for r in manifest['architecture'])
 # The current R25 headboard supersedes the old manifest's single box.
 names.difference_update(['Peca127','Peca128','Peca358','Peca107']+bin_names)
 names.update(['PainelCabeceiraR25','PainelCabeceiraR001'])
 targets={n:shape(d.getObject(n)) for n in sorted(names)}
 report['targets']=[{'name':n,'label':d.getObject(n).Label,'bbox_source_mm':bb(s)} for n,s in targets.items()]
 for n,s in bins.items():
  envelope=swept(s,[650,0,0])
  for q,t in targets.items():check(envelope,t,{'phase':'bin_lateral_forward_and_reverse','moving':n,'target':q})
  report['cases'].append({'phase':'bin_lateral_forward_and_reverse','moving':n,'swept_bbox_source_mm':envelope})
 parked={}
 for n,s in bins.items():
  t=s.copy();t.translate(App.Vector(650,0,0));parked[n]=t
 floor=shape(d.getObject('Peca007'));f=bb(floor)
 report['floor_support']={'name':'Peca007','bbox_source_mm':f,'entire_bin_footprint_within_floor':all(f[0]<=bb(s)[0] and bb(s)[3]<=f[3] and f[1]<=bb(s)[1] and bb(s)[4]<=f[4] for s in parked.values()),'bin_base_on_floor_top':abs(min(bb(s)[2] for s in parked.values())-f[5])<1e-6}
 c=d.getObject(r15['control'])
 assert all(abs(float(getattr(c,k).Value))<1e-9 for k in ['Abertura','RetiradaSaco','EndireitarSaco','RetiradaPainelSuperior','RetiradaConjunto'])
 c.Abertura=55;c.RetiradaSaco=445;c.EndireitarSaco=55;c.RetiradaPainelSuperior=200;d.recompute()
 moving=[d.getObject(n) for n in r15['moving']]
 before={o.Name:shape(o) for o in moving}
 c.RetiradaConjunto=400;d.recompute()
 for o in moving:
  a=before[o.Name];b=shape(o);ba=bb(a);bc=bb(b)
  delta=[bc[i]-ba[i] for i in range(3)]
  assert max(abs(v-w) for v,w in zip(delta,[0,-400,0]))<1e-5
  envelope=swept(a,delta)
  for n,s in parked.items():check(envelope,s,{'phase':'released_frame_0_to_400','moving':o.Name,'target':n})
  report['cases'].append({'phase':'released_frame_0_to_400','moving':o.Name,'swept_bbox_source_mm':envelope})
 # The already-proven daily sack and upper-panel routes are only compared to the new parked bin.
 for n in [r15['bag'],r15['upper']]:
  s=shape(d.getObject(n))
  for q,t in parked.items():check(bb(s),t,{'phase':'removed_sack_or_upper_end_vs_parked_bin','moving':n,'target':q})
 report['minimum_lateral_gap_frame_bin_mm']=min(bb(s)[0] for s in parked.values())-max(bb(shape(o))[3] for o in moving)
 report['status']='complete_scoped_proposal' if not report['contacts'] and not report['errors'] and report['floor_support']['entire_bin_footprint_within_floor'] and report['floor_support']['bin_base_on_floor_top'] else 'unresolved'
except Exception:
 report['status']='failed';report['errors'].append({'error':traceback.format_exc()})
finally:
 if d is not None:App.closeDocument(d.Name)
 report['source_sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest()
 report['source_unchanged']=report['source_sha256_before']==report['source_sha256_after']
 report['limits']='Geometric proposal for three existing rigid bin gabarits, horizontal path on ideal floor and affected maintenance encounter only. No lifting/dragging method, hand/body space, loaded bin weight, pedal actuation, physical floor, caster, retention, hydraulic or structural approval. Neither guest arrangements nor other open doors/drawers included. Return bin before daily use; maintenance sequence, not an interlock. Original maintenance collision with bin at home remains documented.'
 dump()
 print('PARKING_RESULT',report['status'],report['stats'],len(report['contacts']),len(report['errors']),report['source_unchanged'])
