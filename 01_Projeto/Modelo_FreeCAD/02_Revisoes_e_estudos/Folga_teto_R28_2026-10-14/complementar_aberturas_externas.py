"""Only four office leaves after the new20mm drop, versus unchanged outside obstacles."""
from pathlib import Path
import json,time,hashlib,traceback
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
source=(Path(__file__).resolve().parent / 'Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve()
manifest=json.loads(((Path(__file__).resolve().parent / '../Auditoria_implantacao_R23_2026-10-14/Manifesto_implantacao_R23.json').resolve()).read_text(encoding='utf-8'))
doors=[r for r in json.loads(((Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Montagem_R18.json').resolve()).read_text(encoding='utf-8'))['doors'] if r['module']=='Modulo016']
report={'file':str(source),'sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),'situations':[],'contacts':[],'errors':[],
 'stats':{'pairs':0,'bbox_separated':0,'booleans':0},'scope':'Affected outside encounters of4office leaves/fronts+hinges/plates at30/60/86, after R28 lowering. Excludes inside-module pairs preserved by common translation; not a repeat of old173pose grids or global apartment tests.'}
start=time.monotonic();d=None
def shape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def bb(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def check(s,t,ctx):
 assert time.monotonic()-start<120
 report['stats']['pairs']+=1;a=bb(s);b=bb(t)
 if any(a[i+3]<=b[i]+1e-6 or b[i+3]<=a[i]+1e-6 for i in range(3)):
  report['stats']['bbox_separated']+=1;return
 report['stats']['booleans']+=1
 v=s.common(t).Volume
 if v>.1:report['contacts'].append(dict(ctx,common_mm3=v))
try:
 assert not App.GuiUp and len(doors)==4
 d=App.openDocument(str(source));assert abs(d.getObject('Modulo016').Placement.Base.z-1900)<1e-8
 selected={r['name']:r for r in manifest['items'] if r['adoption_scope']=='adopted_result'}
 for n in ['Peca127','Peca128','Peca358','Peca107']:selected.pop(n,None)
 selected.update({n:{'source_root':'CabeceiraDoisPaineisR25'} for n in ['PainelCabeceiraR25','PainelCabeceiraR001']})
 targets={n:shape(d.getObject(n)) for n,r in selected.items() if r['source_root']!='Modulo016'}
 targets.update({r['name']:shape(d.getObject(r['name'])) for r in manifest['architecture']})
 report['stationary_targets']=len(targets)
 for row in doors:
  c=d.getObject(row['control']);assert float(c.Abertura.Value)==0
  names=[row['front']]+[b['body'] for h in row['hinges'] for b in h['bodies']]+[h['plate'] for h in row['hinges']]
  for angle in [30,60,86]:
   c.Abertura=angle;d.recompute();case={'control':c.Name,'front':row['front'],'angle_deg':angle,'parts':len(names)}
   for n in names:
    s=shape(d.getObject(n))
    for q,t in targets.items():check(s,t,{'control':c.Name,'angle_deg':angle,'moving':n,'target':q})
   report['situations'].append(case)
  c.Abertura=0;d.recompute()
 report['final_four_controls_deg']={r['control']:float(d.getObject(r['control']).Abertura.Value) for r in doors}
 report['invalid']=[o.Name for o in d.Objects if 'Invalid' in o.State]
 report['status']='affected_external_poses_complete' if not report['contacts'] and not report['invalid'] else 'requires_review'
except Exception:
 report['status']='failed';report['errors'].append(traceback.format_exc())
finally:
 if d is not None:App.closeDocument(d.Name)
 report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest();report['source_unchanged']=report['sha256_before']==report['sha256_after']
 report['elapsed_s']=time.monotonic()-start
 report['limits']='Twelve discrete individual poses only. No continuous certificate, arbitrary simultaneous combinations, actual ceiling, fixation, load/tolerance or inside STEP contacts. No original document save, scene visibility, programme or controls modified.'
 ((Path(__file__).resolve().parent / 'Complemento_aberturas_R28.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print('R28_OUTSIDE_POSES',report['status'],len(report['situations']),report['stats'],len(report['contacts']),len(report['errors']),report['source_unchanged'])
