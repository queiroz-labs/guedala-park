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

fixed.pop(ctx['leaf'])
fixed['Peca406']=fixed['Peca406'].cut(box([-1,30,308],[20,390,62])).cut(box([-1,-1,370],[20,452,31]))
fixed['PecaBancoR007']=moved(fixed['PecaBancoR007'],[0,0,-10])
fixed['PecaBancoR006']=fixed['PecaBancoR006'].cut(box([408,19,292],[20,392,11]))
# Preserve contents; small relocations needed for new continuous front support.
fixed['PecaBancoR025']=moved(fixed['PecaBancoR025'],[0,12,0])
fixed['PecaBancoR024']=moved(fixed['PecaBancoR024'],[0,3,0])
def post(y):return box([-30,y,0],[30,30,370]).cut(box([-27,y+3,-1],[24,24,372]))
new={'Montante_frente':post(0),'Montante_tras':post(420),'Cabecalho_macico':box([-22,0,370],[40,450,30]),
'Apoio_B01':box([1402,20,0],[18,390,80]),'Apoio_B02':box([1034,20,0],[18,390,82]),'Apoio_B03':box([818,20,0],[18,390,82]),'Apoio_B04':box([18,432,0],[1764,18,18])}
for i,(x,end) in enumerate([(18,818),(836,1034),(1052,1402),(1420,1782)]):
 for label,y in [('frente',20),('tras',414)]:new['Sarrafo_'+label+str(i)]=box([x,y,310],[end-x,18,90])
fixed.update(new)
rails={'Guia_frente':box([28,38,311],[700,19.1,53.1]),'Guia_tras':box([28,394.9,311],[700,19.1,53.1])}
tray={'Plataforma':box([28,57.5,312],[750,337,10]),'Aba_frente':box([28,57.5,322],[750,15,40]),'Aba_tras':box([28,379.5,322],[750,15,40])}
leaf=box([43,76,322],[750,300,30])
static=[];checks=[]
for n,s in new.items():
 for other,t in fixed.items():
  if other!=n and common(s,t)>.1:static.append([n,other,common(s,t)])
for n,s in rails.items():
 for other,t in fixed.items():
  if common(s,t)>.1:static.append([n,other,common(s,t)])
for n,s in tray.items():
 for other,t in fixed.items():
  if common(sweep(s,[-723,0,0]),t)>.1:checks.append([n,other])
for other,t in fixed.items():
 if common(sweep(leaf,[-843,0,0]),t)>.1:checks.append(['Folha',other])
lift=sweep(moved(leaf,[-843,0,0]),[0,0,648])
for other,t in dict(fixed,**{n:moved(s,[-723,0,0]) for n,s in tray.items()}).items():
 if common(lift,t)>.1:checks.append(['Elevar_folha',other])
# Empty upper storage first. Front removable support board: lift30, shift18 inward, then lift.
panel=fixed['PecaBancoR030'];route=[([0,0,30]),([0,18,0]),([0,0,300])];panel_checks=[]
for delta in route:
 for n,t in new.items():
  if common(sweep(panel,delta),t)>.1:panel_checks.append(n)
 panel=moved(panel,delta)
result={'static_collisions':static,'sweep_collisions':checks,'empty_panel_route_new_reinforcement_collisions':panel_checks,'rail':'DZ5321-0070','travel_mm':723,'leaf_extra_slide_mm':120,'support_length_mm':645,'overhang_mm':105,'door_clearance_mm':630,'opening_mm':[390,62],'tray_mm':[750,337,50],'source_sha256':sha,'capacity_verified':False,'limits':'Hardware internals, locks, screws, operator and final tray structure not modeled. Empty-panel route checked against new reinforcements only. Preliminary conditional sizing.'}
(p/'Hibrido_geometria_verificacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
assert not static,static
assert not checks,checks
assert not panel_checks,panel_checks
name='Estudo_Banco_Hibrido_R01';target=p/(name+'.FCStd')
assert name not in App.listDocuments() and not target.exists()
study=App.newDocument(name);bankset=set(ctx['bank_names'])
for n,s in fixed.items():
 if n not in bankset and n not in new:continue
 o=study.addObject('PartDesign::Feature','Ref_'+n);o.Shape=s;o.Label=n+' · estudo híbrido'
 o.ViewObject.ShapeColor=(.25,.42,.48) if n in new else (.76,.77,.71)
 o.ViewObject.Transparency=0 if n in new else 70
for n,s in rails.items():
 o=study.addObject('PartDesign::Feature',n);o.Shape=s;o.Label=n+' · envelope DZ5321-0070'
for n,s in tray.items():
 o=study.addObject('PartDesign::Feature',n);o.Shape=moved(s,[-723,0,0]);o.ViewObject.ShapeColor=(.79,.49,.2)
o=study.addObject('PartDesign::Feature','Folha');o.Shape=moved(leaf,[-843,0,0]);o.ViewObject.ShapeColor=(.85,.72,.5)
study.recompute();Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();study.saveAs(str(target))
assert hashlib.sha256(Path(d.FileName).read_bytes()).hexdigest()==sha
result['saved']=str(target)
