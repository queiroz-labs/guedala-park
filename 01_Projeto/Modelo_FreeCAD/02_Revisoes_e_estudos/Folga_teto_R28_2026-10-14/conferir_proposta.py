"""Affected scope: lower the whole office cabinet20mm, preserving its internals."""
from pathlib import Path
import json,hashlib,time,traceback
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
source=(Path(__file__).resolve().parent / '../Geometria_R27_2026-10-14/Guedala_Park_R27_Geometria_Oficial.FCStd').resolve()
manifest=json.loads(((Path(__file__).resolve().parent / '../Auditoria_implantacao_R23_2026-10-14/Manifesto_implantacao_R23.json').resolve()).read_text(encoding='utf-8'))
report={'file':str(source),'sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),'proposed_drop_mm':20,'contacts':[],'errors':[],'stats':{'pairs':0,'bbox_separated':0,'booleans':0},'parts':[]}
start=time.monotonic();d=None
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def bb(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def union(a,b):return [min(a[i],b[i]) for i in range(3)]+[max(a[i],b[i]) for i in range(3,6)]
def check(bounds,t,ctx):
 assert time.monotonic()-start<120
 report['stats']['pairs']+=1;b=bb(t)
 if any(bounds[i+3]<=b[i]+1e-6 or b[i+3]<=bounds[i]+1e-6 for i in range(3)):
  report['stats']['bbox_separated']+=1;return
 report['stats']['booleans']+=1
 box=Part.makeBox(*[bounds[i+3]-bounds[i] for i in range(3)],App.Vector(*bounds[:3]))
 volume=box.common(t).Volume
 if volume>.1:report['contacts'].append(dict(ctx,conservative_common_mm3=volume,swept_bbox_source_mm=bounds))
try:
 assert not App.GuiUp
 d=App.openDocument(str(source));m=d.getObject('Modulo016')
 assert abs(m.Placement.Base.z-1920)<1e-6
 assert float(m.Altura)==550 and float(m.Comprimento)==2000 and float(m.Profundidade)==350
 selected={r['name']:r for r in manifest['items'] if r['adoption_scope']=='adopted_result'}
 for n in ['Peca127','Peca128','Peca358','Peca107']:selected.pop(n,None)
 selected.update({n:{'source_root':'CabeceiraDoisPaineisR25'} for n in ['PainelCabeceiraR25','PainelCabeceiraR001']})
 moving=[n for n,r in selected.items() if r['source_root']==m.Name]
 targets={n:shape(d.getObject(n)) for n in selected if n not in moving}
 targets.update({r['name']:shape(d.getObject(r['name'])) for r in manifest['architecture']})
 before={n:bb(shape(d.getObject(n))) for n in moving}
 report['before_module_bbox_source_mm']=bb(shape(m))
 p=m.Placement;p.Base.z-=20;m.Placement=p;d.recompute()
 report['after_module_bbox_source_mm']=bb(shape(m))
 for n in moving:
  after=bb(shape(d.getObject(n)));expected=[v-(20 if i in [2,5] else 0) for i,v in enumerate(before[n])]
  assert max(abs(a-b) for a,b in zip(after,expected))<1e-5
  envelope=union(before[n],after)
  for q,t in targets.items():check(envelope,t,{'scope':'whole_office_cabinet_lowering_20mm','moving':n,'target':q})
  report['parts'].append({'name':n,'before_bbox_source_mm':before[n],'after_bbox_source_mm':after})
 # The existing front/hinge motion acts only horizontally and preserves all Z intervals.
 # Pair clearance inside the module is unchanged by translating the entire module.
 rows=json.loads(((Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Montagem_R18.json').resolve()).read_text(encoding='utf-8'))['doors']
 fronts=[r['front'] for r in rows if r['module']==m.Name]
 metals=[n for n in moving if n.startswith('FerragemComum') or n.startswith('CalcoComum')]
 dynamic_names=fronts+metals
 report['doors_and_hardware_min_z_after_mm']=min(bb(shape(d.getObject(n)))[2] for n in dynamic_names)
 report['sofa_max_z_mm']=max(bb(shape(d.getObject(n)))[5] for n in ['Peca122','Peca123','Peca124','Peca125','Peca126'])
 report['nominal_door_hardware_sofa_gap_mm']=report['doors_and_hardware_min_z_after_mm']-report['sofa_max_z_mm']
 report['nominal_top_to_scenario_ceiling_mm']=float(d.getObject('Parametros').TetoQuarto.Value)-report['after_module_bbox_source_mm'][5]
 report['selected_moving_parts']=len(moving);report['stationary_targets']=len(targets)
 report['internal_relative_geometry_unchanged']='All parts translated together, dimensions and controls unchanged. Existing internal door-pair evidence preserved under this common translation.'
 report['status']='proposal_passed_scoped_lowering' if not report['contacts'] else 'proposal_requires_review'
except Exception:
 report['status']='failed';report['errors'].append(traceback.format_exc())
finally:
 if d is not None:App.closeDocument(d.Name)
 report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest();report['source_unchanged']=report['sha256_before']==report['sha256_after']
 report['limits']='New rigid lowering path of whole cabinet, saved closed fronts, selected current stationary solids and walls/floors. No dynamic pose repeat; internal relative motions unchanged. Ceiling is2470 hypothetical datum;20mm is a proposed installation allowance, not a guaranteed sufficient site tolerance. No real ceiling/fixation/person/window-operating trajectory assessed.'
 ((Path(__file__).resolve().parent / 'Conferencia_folga_R28.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print('GAP_PROPOSAL',report['status'],report['stats'],len(report['contacts']),len(report['errors']),report['source_unchanged'])
