"""Read-only projection data for dimensioned compatibility sheets, not fabrication."""
import FreeCAD as App
from pathlib import Path
import json,hashlib
p=(Path(__file__).resolve().parent / '.').resolve();b=(Path(__file__).resolve().parent / '../..').resolve();d=App.ActiveDocument
current=(Path(__file__).resolve().parent / '../Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve()
assert Path(d.FileName).resolve()==(Path(__file__).resolve().parent / '../Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd').resolve()
baseline=json.loads(((Path(__file__).resolve().parent / '../Revisao_solicitada_R28_2026-10-14/Medidas_atual_R28.json').resolve()).read_text(encoding='utf-8'))
assert hashlib.sha256(current.read_bytes()).hexdigest()==baseline['sha256']
def read(f):return json.loads((b/'02_Revisoes_e_estudos'/f).read_text(encoding='utf-8'))
doorfiles=['Dobradicas_R10_2026-10-14/Montagem_R10.json','Portas_opostas_R18_2026-10-14/Montagem_R18.json','Banheiro_R12_2026-10-14/Montagem_R12.json']
doors=[];metal=set();frames=set()
for f in doorfiles:
 for r in read(f)['doors']:
  r=dict(r);r['source']=f;r['current_label']=d.getObject(r['control']).Label
  frames.add(r['front']);doors.append(r)
  for h in r['hinges']:
   metal.add(h['plate']);metal.update(a['body'] for a in h['bodies'])
assert len(doors)==24 and sum(len(r['hinges']) for r in doors)==50
drawer=read('Padronizacao_R08_2026-10-14/Padronizacao_R08.json')['changed_drawers']
wood=set()
for r in drawer:
 wood.update(r['wood_names']);metal.update(set(r['moving_names'])-set(r['wood_names']));metal.update(r['profile_names'])
for r in read('Montagem_R07_2026-10-14/Montagem_G2_R07.json')['parts']:
 (wood if r['category']=='wood' else metal).add(r['name'])
for r in baseline['items']:
 if r['object'].startswith(('Ferragem','Calco')):metal.add(r['object'])
modules=[]
for m in baseline['modules']:
 o=d.getObject(m['object']);inv=o.getGlobalPlacement().inverse();pieces=[]
 for r in baseline['items']:
  if r['root']!=o.Name:continue
  item=d.getObject(r['object']);shape=item.Shape.copy();shape.Placement=inv.multiply(item.getGlobalPlacement());bb=shape.BoundBox
  name=item.Name
  kind='metal' if name in metal else 'reserve' if name.startswith(('ReferenciaCorrer','Roda','Conteudo','OrganizadorG2')) and 'bandeja' not in item.Label.lower() else 'panel'
  linework=[]
  if kind=='panel' and len(shape.Edges)<150:
   for edge in shape.Edges:
    try:
     if edge.Curve.__class__.__name__ in ('Line','LineSegment'):pts=[v.Point for v in edge.Vertexes]
     else:pts=edge.discretize(Number=16)
     if len(pts)>1:linework.append([[v.x,v.y,v.z] for v in pts])
    except Exception:pass
  pieces.append({'object':name,'label':item.Label,'kind':kind,'local_bbox':[bb.XMin,bb.YMin,bb.ZMin,bb.XMax,bb.YMax,bb.ZMax],'lines':linework})
 hinges=[]
 for r in doors:
  if r['module']!=o.Name:continue
  for h in r['hinges']:
   plate=next(q for q in pieces if q['object']==h['plate']);bb=plate['local_bbox']
   hinges.append({'door':r['current_label'],'plate':h['plate'],'plate_center_local_mm':[(bb[i]+bb[i+3])/2 for i in range(3)],'level_mm':h['level'],'source':r['source']})
 for piece in pieces:
  if o.Name=='Modulo001' and '173H7100' in piece['label']:
   bb=piece['local_bbox'];hinges.append({'door':piece['label'],'plate':piece['object'],'plate_center_local_mm':[(bb[i]+bb[i+3])/2 for i in range(3)],'level_mm':None,'source':'Canto_2026-10-13/Canto_simples_R04/README.md'})
 modules.append({**m,'pieces':pieces,'hinge_references':hinges})
result={'document':d.Name,'sha256':baseline['sha256'],'modules':modules,'doors':doors,'drawer_rows':drawer,'hinge_assemblies':54,'hinge_plates':54,'original_touched':d.isTouched(),'method':'Native edge polylines for simple panels; bounding rectangles for hardware/reservations. Coordinates transformed into source-module local frame without mutating original. Mirror front uses Xdisplay=bodyWidth-Xlocal. Hinge symbols denote plate envelope centers, not drilling coordinates.'}
((Path(__file__).resolve().parent / 'Base_pranchas_R28.json').resolve()).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
result={'modules':len(modules),'selected_module_pieces':sum(len(m['pieces']) for m in modules),'hinge_refs':sum(len(m['hinge_references']) for m in modules),'sha256':baseline['sha256'],'touched':d.isTouched()}
