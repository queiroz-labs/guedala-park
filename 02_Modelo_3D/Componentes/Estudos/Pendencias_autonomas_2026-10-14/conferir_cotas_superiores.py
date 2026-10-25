"""New conditional ceiling-height coverage only; no ceiling construction or document save."""
from pathlib import Path
import json,hashlib,time,traceback
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
source=(Path(__file__).resolve().parent / '../Manutencao_R26_2026-10-14/Guedala_Park_R26_Manutencao_Simples.FCStd').resolve()
manifest=json.loads(((Path(__file__).resolve().parent / '../Auditoria_implantacao_R23_2026-10-14/Manifesto_implantacao_R23.json').resolve()).read_text(encoding='utf-8'))
start=time.monotonic()
report={'file':str(source),'sha256_before':hashlib.sha256(source.read_bytes()).hexdigest(),'rows':[],'modules':[],'above_scenario':[],'boundary_only':[],'shape_validity_issues':[],'errors':[]}
previous=(Path(__file__).resolve().parent / 'Cotas_superiores_R26.json').resolve()
if previous.exists():
 old=json.loads(previous.read_text(encoding='utf-8'))
 assert old['status']=='failed' and old['source_unchanged']
 assert old['sha256_before']==report['sha256_before']
 ((Path(__file__).resolve().parent / 'Cotas_superiores_primeira_sondagem.json').resolve()).write_text(json.dumps(old,ensure_ascii=False,indent=2),encoding='utf-8')
 report['rows']=old['rows']
 report['reused_completed_rows']=len(old['rows'])
d=None
try:
 assert not App.GuiUp
 d=App.openDocument(str(source));parameters=d.getObject('Parametros')
 heights={'TetoQuarto':float(parameters.TetoQuarto.Value),'TetoCozinha':float(parameters.TetoCozinha.Value)}
 assert heights=={'TetoQuarto':2470,'TetoCozinha':2570}
 report['parameters_mm']=heights
 rows={r['name']:r for r in manifest['items'] if r['adoption_scope']=='adopted_result'}
 for n in ['Peca127','Peca128','Peca358','Peca107']:rows.pop(n,None)
 for n in ['PainelCabeceiraR25','PainelCabeceiraR001']:
  rows[n]={'name':n,'source_root':'CabeceiraDoisPaineisR25','source_group':'Ambiente_quarto','link':'EspelhoPecaR010'}
 completed={r['name'] for r in report['rows']}
 for n,row in rows.items():
  if n in completed:continue
  assert time.monotonic()-start<120
  o=d.getObject(n);assert o is not None
  s=o.Shape.copy();s.Placement=o.getGlobalPlacement()
  assert not s.isNull(),n
  valid=s.isValid()
  if not valid:report['shape_validity_issues'].append({'name':n,'label':o.Label,'native_valid':o.Shape.isValid(),'world_copy_valid':valid,'source_root':row['source_root']})
  b=s.BoundBox
  category='TetoCozinha' if row['source_group'] in ['Ambiente_cozinha','Ambiente_lavanderia'] else 'TetoQuarto'
  ceiling=heights[category];zmax=b.ZMax
  mode='conservative_bbox'
  if zmax>=ceiling-1e-6:
   zmax=s.optimalBoundingBox().ZMax;mode='optimal_bbox_for_boundary_candidate'
  gap=ceiling-zmax
  item={'name':n,'label':o.Label,'source_root':row['source_root'],'source_group':row['source_group'],'scenario_parameter':category,'scenario_height_mm':ceiling,'upper_z_source_and_current_mm':zmax,'nominal_gap_mm':gap,'criterion':mode}
  report['rows'].append(item)
  if gap<-1e-5:report['above_scenario'].append(item)
  elif abs(gap)<=1e-5:report['boundary_only'].append(item)
 roots={}
 for item in report['rows']:roots.setdefault(item['source_root'],[]).append(item)
 for m in manifest['modules']:
  selected=roots.get(m['name'],[])
  assert selected,m['name']
  highest=min(selected,key=lambda r:r['nominal_gap_mm'])
  report['modules'].append({'module':m['name'],'label':d.getObject(m['name']).Label,'pieces':len(selected),'highest_piece':highest,'minimum_nominal_gap_mm':highest['nominal_gap_mm']})
 report['objects']=len(d.Objects);report['selected_current_solids']=len(report['rows'])
 report['invalid']=[o.Name for o in d.Objects if 'Invalid' in o.State]
 assert not report['invalid']
 report['status']='conditional_height_comparison_complete'
except Exception:
 report['status']='failed';report['errors'].append(traceback.format_exc())
finally:
 if d is not None:App.closeDocument(d.Name)
 report['sha256_after']=hashlib.sha256(source.read_bytes()).hexdigest();report['source_unchanged']=report['sha256_before']==report['sha256_after']
 report['elapsed_s']=time.monotonic()-start
 report['limits']='Closed/current saved state only, compared to existing hypothetical horizontal heights by source-room ownership. 2470 is the generator scenario outside kitchen/laundry; 2570 is the recorded kitchen/laundry hypothesis. No actual ceiling solid, as-built height, slopes, plaster, beam, fastening, assembly tolerance or all dynamic poses checked. A nominal zero gap is a boundary condition, not penetration or installation clearance. Reflection preserves Z. No new dimensions, ceiling solids, changes or fabrication release.'
 ((Path(__file__).resolve().parent / 'Cotas_superiores_R26.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print('HEIGHT_RESULT',report['status'],report.get('selected_current_solids'),len(report['above_scenario']),len(report['boundary_only']),len(report['errors']),report['source_unchanged'])
