import FreeCAD as App
from pathlib import Path
import json, hashlib

p=(Path(__file__).resolve().parent / '.').resolve();b=(Path(__file__).resolve().parent / '../..').resolve();d=App.ActiveDocument
expected=(Path(__file__).resolve().parent / '../Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve()
assert Path(d.FileName).resolve()==(Path(__file__).resolve().parent / '../Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve()
adopted={x['object'] for x in json.loads(((Path(__file__).resolve().parent / '../Revisao_solicitada_R28_2026-10-14/Medidas_atual_R28.json').resolve()).read_text(encoding='utf-8'))['items']}
r08=json.loads(((Path(__file__).resolve().parent / '../Padronizacao_R08_2026-10-14/Padronizacao_R08.json').resolve()).read_text(encoding='utf-8'))
r07=json.loads(((Path(__file__).resolve().parent / '../Montagem_R07_2026-10-14/Montagem_G2_R07.json').resolve()).read_text(encoding='utf-8'))
def parts(names):
 result=[]
 for n in names:
  assert n in adopted,n
  o=d.getObject(n)
  result.append({'object':n,'label':o.Label,'volume_m3':o.Shape.Volume/1e9})
 return result
rows=[]
for r in r08['changed_drawers']:
 rows.append({'drawer':r['drawer'],'label':r['label'],'wood':parts(r['wood_names']),'tray_wood':[]})
g2names=[x['name'] for x in r07['parts'] if x['category']=='wood']
traynames=['OrganizadorG2R06']+['OrganizadorG2R%03d'%i for i in [1,2,3,4,10,11,12,13,14]]
g2={'drawer':'G2','label':'G2 · utensílios','wood':parts(g2names),'tray_wood':parts(traynames)}
rows.append(g2)
assert len(rows)==9
assert sum(len(r['wood']) for r in rows)==54
assert len(g2['tray_wood'])==10
old=json.loads(((Path(__file__).resolve().parent / '../Padronizacao_R08_2026-10-14/Carga_R08.json').resolve()).read_text(encoding='utf-8'))
comparison=[]
for r in rows:
 r['wood_volume_m3']=sum(x['volume_m3'] for x in r['wood'])
 r['tray_volume_m3']=sum(x['volume_m3'] for x in r['tray_wood'])
 previous=next(x for x in old if x['drawer']==r['label'])
 comparison.append({'drawer':r['label'],'volume_delta_m3':r['wood_volume_m3']-previous['wood_volume_m3']})
 r['scenarios']=[]
 for density in [750,900]:
  body=r['wood_volume_m3']*density;tray=r['tray_volume_m3']*density
  r['scenarios'].append({'hypothetical_density_kg_m3':density,'box_and_front_kg':body,'tray_wood_kg':tray,'subtotal_known_geometry_kg':body+tray,'balance_before_other_accessories_and_contents_kg':40-body-tray})
result={'canonical_sha256':hashlib.sha256(expected.read_bytes()).hexdigest(),'candidate_total_kg':40,'capacity_confirmed':False,'actual_material_density_known':False,'content_masses_known':False,'method':'Read64selected wood solids only, sum native volumes. No geometry, pose, visibility, recompute or save changes. Utensil gabarits excluded from mass. Manufacturer moving-runner mass treatment must be confirmed; no inferred steel/plastic density applied.','formulas':{'contents_budget':'40 - box_and_front_mass - organizers_mass - other_chargeable_moving_accessories_mass','remaining_margin':'contents_budget - actual_contents_mass'},'rows':rows,'comparison_previous_wood':comparison}
((Path(__file__).resolve().parent / 'Cargas_gavetas_R28.json').resolve()).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
result={'drawers':len(rows),'wood_solids':64,'volume_changes':comparison,'g2_tray_m3':g2['tray_volume_m3'],'sha256':result['canonical_sha256']}
