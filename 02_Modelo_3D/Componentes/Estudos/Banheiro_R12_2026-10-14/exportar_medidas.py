import FreeCAD as App
from pathlib import Path
import json
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R12_Banheiro_Simples.FCStd').resolve())
data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R12.json').resolve()).read_text(encoding='utf-8'));rows=[];masses=[]
for r in data['doors']:
 m=doc.getObject(r['module']);g=doc.getObject(r['door']);front=doc.getObject(r['front']);panel=front.Base;bb=panel.Shape.optimalBoundingBox();mp=m.getGlobalPlacement()
 if 'mirror' in r:bb.add(doc.getObject(r['mirror']).Shape.optimalBoundingBox())
 rows.append({'door':g.Name,'module':m.Name,'side':r['side'],'module_base':list(mp.Base),'module_rotation':list(mp.Rotation.Q),'module_yaw_deg':mp.Rotation.toEuler()[0],
 'hinge_inner_x_mm':18 if r['side']=='left' else float(m.Comprimento)-18,'hinge_y_mm':r['plate_hole_row_y']-.5,'closed_leaf_base':list(g.Placement.Base),
 'front_local_box':[bb.XMin,bb.YMin,bb.ZMin,bb.XMax,bb.YMax,bb.ZMax],'front_height':float(panel.Height)})
 volume=doc.getObject(r['mirror']).Shape.Volume if 'mirror' in r else 0
 masses.append({'door':g.Name,'wood_volume_mm3':front.Shape.Volume,'glass_volume_mm3':volume,'scenario_wood900_glass2500_handle200g_kg':front.Shape.Volume*900/1e9+volume*2500/1e9+.2,'hinge_quantity_candidate':len(r['hinges'])})
((Path(__file__).resolve().parent / 'Frentes_plano_R12.json').resolve()).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
report={'fronts':masses,'lower_internal_nominal_mm':[564,382,509],'mirror_internal_nominal_mm':[564,108,714],
 'mirror_closed_assembly_depth_mm':150,'mirror_closed_front_layering_mm':{'mirror':[0,4],'wood':[4,22],'carcass_front':24,'rear':150},
 'scope':'Vãos de madeira nominais, antes de ferragem/conteúdo/tubulação. Massas são cenários, não pesos reais. Fundo inferior inteiro ainda exige detalhamento hidráulico; não é comprovação de sifão/torneira.'}
((Path(__file__).resolve().parent / 'Medidas_carga_R12.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');result=report
