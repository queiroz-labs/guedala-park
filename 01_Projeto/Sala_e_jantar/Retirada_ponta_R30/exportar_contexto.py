import FreeCAD as App, Part
from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
base=p.parents[1]/'Modelo_FreeCAD/02_Revisoes_e_estudos'
d=App.getDocument('Guedala_Park_R30_Juntas_Rotulos')
bank=json.loads((base/'Banco_R16_2026-10-14/Montagem_R16.json').read_text(encoding='utf-8'))
old=json.loads((base/'Revisao_solicitada_R28_2026-10-14/Medidas_atual_R28.json').read_text(encoding='utf-8'))
names=set(r['object'] for r in old['items'])
names.update(o.Name for o in d.getObject('ParedesInteiras').Group)
names.update(['CadeiraLinaR30_1','CadeiraLinaR30_2','CadeiraLinaR30_3','FundoTanqueR29'])
names.discard('Peca354')
inv=d.getObject('Modulo019').getGlobalPlacement().inverse()
rows=[];shapes={}
for n in sorted(names):
 o=d.getObject(n)
 if not o or not hasattr(o,'Shape') or o.Shape.isNull():continue
 if 'cadeira' in o.Label.lower() and n.startswith('Peca'):continue
 s=o.Shape.copy();s.Placement=inv.multiply(o.getGlobalPlacement());b=s.BoundBox
 if b.XMin>2000 or b.XMax< -1800 or b.YMin>650 or b.YMax< -2200 or b.ZMin>2500:continue
 bb=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
 rows.append(dict(name=n,label=o.Label,bbox=[round(v,4) for v in bb]));shapes[n]=s
leaf=bank['leaf']
assert leaf in shapes,leaf
b=shapes[leaf].BoundBox
# Exact swept prism for translation along bank local -X toward kitchen.
endgap=20
stroke=b.XMax+endgap
sweep=Part.makeBox(b.XLength+stroke,b.YLength,b.ZLength,App.Vector(b.XMin-stroke,b.YMin,b.ZMin))
hits=[]
for n,s in shapes.items():
 if n==leaf:continue
 a=sweep.BoundBox;t=s.BoundBox
 if all(min(getattr(a,k+'Max'),getattr(t,k+'Max'))-max(getattr(a,k+'Min'),getattr(t,k+'Min'))>1e-6 for k in 'XYZ'):
  vol=sweep.common(s).Volume
  if vol>.1:hits.append(dict(name=n,label=d.getObject(n).Label,volume=vol))
result=dict(source=d.FileName,sha256=hashlib.sha256(Path(d.FileName).read_bytes()).hexdigest(),coordinates='Bank local: X0 kitchen end, X1800 sofa end, Y0 front, Y450 rear, floor Z0. Unmirrored source coordinate frame; distances invariant under apartment reflection.',leaf=leaf,bank_names=list(set(bank['structure']+bank['new'])),context=rows,stroke_mm=stroke,end_gap_mm=endgap,sweep_hits=hits,limits='Selected adopted R28 objects refreshed in R30, current Lina substituted, full-height walls. Fixed closed pose; bounding context with exact common volumes for sweep candidates. No model mutation.')
(p/'Contexto_R30.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
result={'leaf':leaf,'bbox':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],'stroke':stroke,'hits':hits,'count':len(rows)}

def swept_box(lo,dim,delta):
 return Part.makeBox(*[dim[i]+abs(delta[i]) for i in range(3)],App.Vector(*[lo[i]+min(0,delta[i]) for i in range(3)]))
def collisions(s,opening=None):
 found=[]
 for n,t in shapes.items():
  if n==leaf:continue
  if n=='Peca406' and opening is not None:t=t.cut(opening)
  a=s.BoundBox;bb=t.BoundBox
  if all(min(getattr(a,k+'Max'),getattr(bb,k+'Max'))-max(getattr(a,k+'Min'),getattr(bb,k+'Min'))>1e-6 for k in 'XYZ'):
   v=s.common(t).Volume
   if v>.1:found.append({'name':n,'volume':v})
 return found
# Comparative nominal actual panel, not a measured product: 750x300x30.
# Lowering within existing reservation preserves 10 above shelf z320.
panel_start=[43,65,330];panel_size=[750,300,30];panel_stroke=813
opening=Part.makeBox(20,320,40,App.Vector(-1,55,325))
panel_sweep=swept_box(panel_start,panel_size,[-panel_stroke,0,0])
lift=swept_box([-770,65,330],panel_size,[0,0,640])
operators={
 'frontal_600':dict(box=[-1420,-85,0,-820,515,1800],note='600x600 footprint ahead of conservative envelope, not a body standard; 10 mm from closed door; secondary lateral gap to fridge315.'),
 'lateral_600':dict(box=[-600,-600,0,0,0,1800],note='600x600 footprint on room side; only2.5 mm to fridge front plane. Does not prove reach or movement.'),
}
for row in operators.values():
 bb=row['box'];s=Part.makeBox(*[bb[i+3]-bb[i] for i in range(3)],App.Vector(*bb[:3]));row['hits']=collisions(s)
check=dict(nominal_panel_mm=panel_size,start_mm=panel_start,stroke_mm=panel_stroke,opening_hypothesis_mm=[320,40],opening_yz_mm=[55,325,375,365],remaining_top_strip_mm=35,clearances_mm={'side_each':10,'vertical_each':5,'above_shelf':10},panel_sweep_original=collisions(panel_sweep),panel_sweep_virtual_opening=collisions(panel_sweep,opening),panel_lift_hits=collisions(lift,opening),envelope_tip_to_closed_door_mm=610,panel_tip_to_closed_door_mm=660,envelope_side_to_fridge_mm=440,panel_side_to_fridge_mm=465,operators=operators,limits='Operator boxes are sensitivity examples, not ergonomic, accessible or regulatory clearance. Door closed and fridge closed; no door swing, hand, load or full leaf-to-table cycle validation. Opening has no engineered reinforcement. Nominal panel dimensions are design hypotheses.')
assert not check['panel_sweep_virtual_opening']
assert not check['panel_lift_hits']
(p/'Verificacao_retirada.json').write_text(json.dumps(check,ensure_ascii=False,indent=2),encoding='utf-8')
assert hashlib.sha256(Path(d.FileName).read_bytes()).hexdigest()==json.loads((p/'Contexto_R30.json').read_text(encoding='utf-8'))['sha256']
result=check
