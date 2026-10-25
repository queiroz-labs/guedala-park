import FreeCAD as App, FreeCADGui as Gui, Part
from pathlib import Path
import json,hashlib
p=Path(__file__).resolve().parent
ctx=json.loads((p/'Contexto_R30.json').read_text(encoding='utf-8'))
d=App.getDocument('Guedala_Park_R30_Juntas_Rotulos');sha=hashlib.sha256(Path(d.FileName).read_bytes()).hexdigest()
assert sha==ctx['sha256']
inv=d.getObject('Modulo019').getGlobalPlacement().inverse();fixed={}
for r in ctx['context']:
 o=d.getObject(r['name']);s=o.Shape.copy();s.Placement=inv.multiply(o.getGlobalPlacement());fixed[o.Name]=s
def box(pos,size):return Part.makeBox(*size,App.Vector(*pos))
def moved(s,delta):t=s.copy();t.translate(App.Vector(*delta));return t
def common(a,b):
 x,y=a.BoundBox,b.BoundBox
 if any(min(getattr(x,k+'Max'),getattr(y,k+'Max'))-max(getattr(x,k+'Min'),getattr(y,k+'Min'))<=1e-6 for k in 'XYZ'):return 0
 return a.common(b).Volume
def sweep(s,delta):
 b=s.BoundBox;pos=[b.XMin,b.YMin,b.ZMin];sz=[b.XLength,b.YLength,b.ZLength]
 return box([pos[i]+min(0,delta[i]) for i in range(3)],[sz[i]+abs(delta[i]) for i in range(3)])
# Keep originals untouched. Modify copies only.
fixed.pop(ctx['leaf'])
fixed['Peca406']=fixed['Peca406'].cut(box([-1,25,308],[20,380,62])).cut(box([-1,-1,370],[20,452,31]))
fixed['PecaBancoR007']=moved(fixed['PecaBancoR007'],[0,0,-10])
fixed['PecaBancoR006']=fixed['PecaBancoR006'].cut(box([408,19,292],[20,392,11]))
new={
 'Portico_frente':box([-30,0,0],[30,25,370]),
 'Portico_tras':box([-30,405,0],[30,45,370]),
 'Cabecalho_assento':box([-30,0,370],[48,450,30]),
 'Uniao_inferior':box([-30,25,0],[30,380,30]),
 'Suporte_guia_frente':box([28,20,310],[750,10,60]),
 'Suporte_guia_tras':box([28,400,310],[750,10,60]),
 'Ligacao_guia_posterior':box([28,410,365],[750,22,30]),
}
# Bounds for fit only; not STEP hardware, section schedule, or claimed strength.
fixed.update(new)
rails={'Guia_frente':box([28,30,311],[750,19.1,53.1]),'Guia_tras':box([28,380.9,311],[750,19.1,53.1])}
tray={'Plataforma':box([28,50,312],[750,330,10]),'Aba_frente':box([28,50,322],[750,15,40]),'Aba_tras':box([28,365,322],[750,15,40])}
leaf=box([43,65,322],[750,300,30])
fixed_checks=[]
for n,s in new.items():
 for other,t in fixed.items():
  if other==n:continue
  v=common(s,t)
  if v>.1:fixed_checks.append([n,other,v])
assert not fixed_checks,fixed_checks
checks=[]
for n,s in tray.items():
 sw=sweep(s,[-750,0,0])
 for other,t in fixed.items():
  v=common(sw,t)
  if v>.1:checks.append([n,other,v])
for other,t in fixed.items():
 v=common(sweep(leaf,[-843,0,0]),t)
 if v>.1:checks.append(['Folha',other,v])
lift=sweep(moved(leaf,[-843,0,0]),[0,0,648])
for other,t in fixed.items():
 v=common(lift,t)
 if v>.1:checks.append(['Elevar_folha',other,v])
for n,s in tray.items():
 v=common(lift,moved(s,[-750,0,0]))
 if v>.1:checks.append(['Elevar_folha',n,v])
assert not checks,checks
for n,s in rails.items():
 for other,t in fixed.items():
  assert common(s,t)<.1,(n,other)
# Support at stage2: tray[-722,28], leaf[-800,-50].
result={'status':'Geometric proposal; no source changes or fabrication release','design_requirement':{'occupants':3,'kg_each':80,'total_kg':240,'capacity_verified':False},'portal_external_projection_mm':30,'opening_mm':[380,62],'opening_yz_mm':[25,308,405,370],'shelf_new_z_mm':[292,310],'lower_divider_new_top_mm':292,'tray_mm':[750,330,10],'tray_assembled_max_height_mm':50,'rail_fit_only_mm':[750,19.1,53.1],'rail_required_travel_mm':750,'panel_mm':[750,300,30],'panel_start_mm':[43,65,322],'tray_travel_mm':750,'panel_additional_slide_mm':93,'panel_total_travel_mm':843,'panel_final_x_mm':[-800,-50],'tray_final_x_mm':[-722,28],'supported_panel_length_final_mm':672,'leading_overhang_mm':78,'panel_cg_final_x_mm':-425,'panel_cg_inside_support_interval':True,'tip_to_closed_door_mm':630,'frame_to_panel_tail_mm':20,'static_collisions':fixed_checks,'sweep_collisions':checks,'lower_content_top_mm':274,'new_clearance_content_to_shelf_mm':18,'source_sha256':sha,'limits':'All member shapes are spatial envelopes, not tube wall or structural sizing. Rail inner members and lock not modeled. Static CG check only, not forces, flexure, tilt or durability. Floor support, welds, fixings, tray composition, stops and occupant concentrated loads pending. Portal30 occupies passage permanently; mounted whole bench end becomes1830 nominal.'}
(p/'Bandeja_reforcos_verificacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
name='Estudo_Bandeja_Ponta_R30'
assert name not in App.listDocuments()
target=p/(name+'.FCStd');assert not target.exists()
study=App.newDocument(name)
bankset=set(ctx['bank_names'])
for n,s in fixed.items():
 if n not in bankset and n not in new and n not in ['Peca091','Peca092']:continue
 o=study.addObject('PartDesign::Feature','Ref_'+n);o.Shape=s;o.Label=n+' · cópia / envelope'
 o.ViewObject.ShapeColor=(.25,.42,.48) if n in new else (.76,.77,.71)
 o.ViewObject.Transparency=0 if n in new else 75
for n,s in rails.items():
 o=study.addObject('PartDesign::Feature',n);o.Shape=s;o.Label=n+' · reserva sem produto selecionado';o.ViewObject.ShapeColor=(.5,.5,.55)
for n,s in tray.items():
 o=study.addObject('PartDesign::Feature',n);o.Shape=moved(s,[-750,0,0]);o.ViewObject.ShapeColor=(.79,.49,.2)
o=study.addObject('PartDesign::Feature','Folha_nominal');o.Shape=moved(leaf,[-843,0,0]);o.ViewObject.ShapeColor=(.85,.72,.5);o.ViewObject.Transparency=35
study.recompute();Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();study.saveAs(str(target))
assert hashlib.sha256(Path(d.FileName).read_bytes()).hexdigest()==sha
result={'saved':str(target),'collisions':checks,'remaining_to_door_mm':630,'design_load_kg':240,'capacity_verified':False}
