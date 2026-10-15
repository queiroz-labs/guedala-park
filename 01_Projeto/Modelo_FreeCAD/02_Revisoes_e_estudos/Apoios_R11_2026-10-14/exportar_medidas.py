import FreeCAD as App
from pathlib import Path
import json
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R11_Apoios_Simples.FCStd').resolve())
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R11.json').resolve()).read_text(encoding='utf-8'))
rows=[];masses=[]
for r in data['doors']:
 m=doc.getObject(r['module']);g=doc.getObject(r['door']);front=doc.getObject(r['front']);panel=front.Base
 bb=panel.Shape.optimalBoundingBox();mp=m.getGlobalPlacement()
 rows.append({'door':g.Name,'module':m.Name,'side':'left','module_base':list(mp.Base),'module_rotation':list(mp.Rotation.Q),'module_yaw_deg':mp.Rotation.toEuler()[0],
 'hinge_inner_x_mm':r['hinge_support_inner_x_mm'],'closed_leaf_base':list(g.Placement.Base),
 'front_local_box':[bb.XMin,bb.YMin,bb.ZMin,bb.XMax,bb.YMax,bb.ZMax],'front_height':float(panel.Height)})
 masses.append({'door':g.Name,'dimensions_mm':[float(panel.Length),float(panel.Width),float(panel.Height)],'wood_volume_mm3':front.Shape.Volume,
 'scenario_MDF900kg_m3_plus_handle200g_kg':front.Shape.Volume*900/1e9+.2,'hinges_candidate':2,'real_material_weight_and_fixation_pending':True})
((Path(__file__).resolve().parent / 'Frentes_plano_R11.json').resolve()).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
report={'doors':masses,'office_clear_cells_nominal_mm':[482,482,482,464],
 'headboard_clear_cells_nominal_mm':[425.75,425.75,416.75,441.75],
 'scope':'Larguras entre faces de madeira, antes de ferragens/mãos. Último vão cabeceira existente/vizinha calculado entre1340,25 e1782. Cenário900 de referência; pesos reais/carga/fixação pendentes.'}
((Path(__file__).resolve().parent / 'Medidas_carga_R11.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps(report,ensure_ascii=False)
