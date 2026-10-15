"""Static current results against actual whole walls/floors only; no poses/save."""
from pathlib import Path
import json,hashlib,time,traceback
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();started=time.monotonic();budget=240
manifest=json.loads(((Path(__file__).resolve().parent / 'Manifesto_implantacao_R23.json').resolve()).read_text(encoding='utf-8'));source=Path(manifest['file'])
report={'file':str(source),'status':'running','budget_s':budget,'criterion_volume_mm3':.1,'bbox_epsilon_mm':1e-6,
 'scope':'Saved static adopted objects vs 27 whole walls and 9 floors in base source coordinates; no ceiling geometry exists in selected composition',
 'sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(), 'manifest_file':'Manifesto_implantacao_R23.json',
 'stats':{'pairs':0,'bbox_separated':0,'bbox_boundary':0,'boolean_candidates':0,'booleans':0},
 'contacts':[],'boundary_candidates':[],'candidates':[],'errors':[],'completed_items':[]}
out=(Path(__file__).resolve().parent / 'Auditoria_arquitetura_R23.json').resolve()
def dump():
 report['elapsed_s']=time.monotonic()-started;out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
def bb(b):return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def mirror_box(b):return [7400-b[3],b[1],b[2],7400-b[0],b[4],b[5]]
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def check():
 if time.monotonic()-started>budget:raise TimeoutError('240s bounded budget exhausted')
d=None
try:
 assert not App.GuiUp
 assert report['sha256_before']==manifest['sha256']
 d=App.openDocument(str(source));report['gui_up']=bool(App.GuiUp)
 arch={r['name']:shape(d.getObject(r['name'])) for r in manifest['architecture']}
 for item in manifest['items']:
  check();o=d.getObject(item['name']);s=None
  x=item['bbox_source_mm']
  for target in manifest['architecture']:
   check();report['stats']['pairs']+=1;y=target['bbox_source_mm']
   lengths=[min(x[i+3],y[i+3])-max(x[i],y[i]) for i in range(3)]
   if min(lengths)<-1e-6:report['stats']['bbox_separated']+=1;continue
   context={'item':item['name'],'item_label':item['label'],'source_root':item['source_root'],'source_group':item['source_group'],
    'target':target['name'],'target_label':target['label'],'target_class':target['architectural_class'],'overlap_bbox_lengths_mm':lengths}
   if min(lengths)<=1e-6:
    report['stats']['bbox_boundary']+=1
    context.update(category='bbox_boundary_only_no_volume_test',interpretation='Possible placement/support contact; not volumetric penetration nor proof of actual contact/fixation')
    report['boundary_candidates'].append(context);continue
   report['stats']['boolean_candidates']+=1
   report['candidates'].append(context)
   if s is None:s=shape(o)
   report['stats']['booleans']+=1;t0=time.monotonic()
   try:
    c=s.common(arch[target['name']]);volume=c.Volume
    if volume>1e-9:
     box=bb(c.BoundBox)
     hit=dict(context,volume_mm3=volume,contact_bbox_source_mm=box,contact_bbox_mirrored_mm=mirror_box(box),boolean_s=time.monotonic()-t0,
       classification='volumetric_interpenetration_requires_review' if volume>.1 else 'positive_volume_below_triage_threshold_not_certified_tolerance')
     report['contacts'].append(hit)
   except Exception:report['errors'].append(dict(context,error=traceback.format_exc()))
   dump()
  report['completed_items'].append(item['name']);dump()
 report['status']='complete_saved_static_scope'
except TimeoutError as e:report.update(status='partial_budget_limit',error=str(e))
except Exception:report.update(status='failed',error=traceback.format_exc())
finally:
 if d is not None:App.closeDocument(d.Name)
 report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest();report['source_unchanged']=report['sha256_before']==report['sha256_after']
 report['limits']='Static saved geometry only; no moving-position coverage, actual measurements/tolerances, certified structure/load/fixation, ventilation or people. Gabarits remain gabarits. No ceiling solid in model; no ceiling collision claim. BoundaryBBox is only possible contact, not a volumetric hit. No CAD save or geometry changes.'
 dump();print('ARCH_RESULT',report['status'],report['stats'],len(report['contacts']),len(report['errors']),report['source_unchanged'])
