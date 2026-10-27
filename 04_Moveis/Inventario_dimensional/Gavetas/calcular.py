from pathlib import Path
import json, zipfile, hashlib, csv
p=Path(__file__).resolve().parents[2]
out=Path(__file__).resolve().parent
r28=p/'Modelo_FreeCAD/02_Revisoes_e_estudos/Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd'
r44=p/'Modelo_FreeCAD/01_FGVTN/Guedala_Park_R44_Consolidado.FCStd'
old=json.loads((Path(__file__).resolve().parents[3]/'02_Modelo_3D/Componentes/Gavetas/Cargas_gavetas_R28.json').read_text(encoding='utf-8-sig'))
checks=[]
with zipfile.ZipFile(r28) as a,zipfile.ZipFile(r44) as b:
 for row in old['rows']:
  for x in row['wood']+row['tray_wood']:
   n=x['object']+'.Shape.brp'
   checks.append({'object':x['object'],'same_brep_R28_R44':a.read(n)==b.read(n)})
rows=[]
current=json.loads((out/'Massas_R44_recalculadas.json').read_text(encoding='utf-8'))
for x in current['rows']:
 v=x['volume_total_m3']
 rows.append({'drawer':x['drawer'],'label':x['label'],'wood_volume_m3':v,'wood_mass_750':v*750,'wood_mass_900':v*900,'balance_35kg_750':35-v*750,'balance_35kg_900':35-v*900})
data={'source_sha256':hashlib.sha256(r44.read_bytes()).hexdigest(),'capacity_kg':35,'method':'Actual volumes independently reread from R44 using the R28 list of wood objects. BREP comparison failed, so no R28 volumes were transferred. Includes wood fronts and G2 trays, excludes moving hardware and actual contents. Densities hypothetical. Capacity is total budget, not content rating.','all_shapes_equal':all(c['same_brep_R28_R44'] for c in checks),'shape_checks':checks,'rows':rows}
(out/'Calculos_cargas_35kg.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
with (out/'Orcamento_carga.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps({'all_shapes_equal':data['all_shapes_equal'],'rows':len(rows),'source_sha256':data['source_sha256']},ensure_ascii=False))
