from pathlib import Path
import json,shutil
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve()
src=(Path(__file__).resolve().parent / '../Correr_R14_2026-10-14/Guedala_Park_R14_Correr_Simples.FCStd').resolve();dst=(Path(__file__).resolve().parent / 'Guedala_Park_R15_Cesto_Simples.FCStd').resolve()
assert not dst.exists(),'Revisão existente: não reconstruir'
prev=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==src)
prev.save();shutil.copy2(src,dst);d=App.openDocument(str(dst));App.setActiveDocument(d.Name)
d.Label='Guedala Park - R15 - cesto55 e retirada, proposta'
m=d.getObject('Modulo013');oldOrigin=list(m.Placement.Base)
m.Placement.Base=App.Vector(2550,6370,0);m.PlanilhaDimensoes.set('B3','630 mm');m.PlanilhaDimensoes.set('B4','900 mm')
m.Condicoes='R15 proposta: frente630 desde parede7000; inferiores150–671/alto675–897, cesto450x250x450 eixo560/120 giro55. Origem0/altura900 inclui apoios inferiores; pedra/tanque escolhidos preservados. Hidráulica/ferragem/apoios reais pendentes; sem corte.'
history=d.addObject('App::Part','HistoricoCestoR15');m.addObject(history);history.Label='Histórico oculto - frente fixa e bloco de cesto R14'
for n in ['Peca355','Peca356']:
 o=d.getObject(n);m.removeObject(o);history.addObject(o);o.Visibility=False
history.Visibility=False
def prop(o,t,n,v):
 if n not in o.PropertiesList:o.addProperty(t,n,'Estudo R15')
 setattr(o,n,v)
def setnum(o,field,v):
 o.setExpression(field,None)
 if field.startswith('Placement.Base.'):
  p=o.Placement;setattr(p.Base,field[-1],v);o.Placement=p
 else:setattr(o,field,v)
for n in ['Peca352','Peca353']:
 o=d.getObject(n);setnum(o,'Placement.Base.z',98);setnum(o,'Height',802)
fundo=d.getObject('Peca354');setnum(fundo,'Placement.Base.z',98);setnum(fundo,'Height',802)
made=[];fixed=[];frame=[];moving=[]
def feature(parent,label,s,kind,color=(.75,.69,.56)):
 o=d.addObject('Part::Feature','PecaCestoR15');parent.addObject(o);o.Label=label;o.Shape=s;prop(o,'App::PropertyString','CategoriaR15',kind)
 prop(o,'App::PropertyString','Status','Proposta/gabarito. Medidas/fixação/carga/ferragem reais pendentes; sem corte/furação/compra.')
 o.ViewObject.ShapeColor=color;made.append(o);return o
def box(parent,label,x,y,z,w,p,h,kind,color=(.75,.69,.56)):
 return feature(parent,label,Part.makeBox(w,p,h,App.Vector(x,y,z)),kind,color)
fixed.append(box(m,'Base98 - frente até580 desde parede',18,50,80,554,562,18,'madeira_fixa'))
fixed.append(box(m,'Rodapé110 recuado50 da face - proposta',18,50,0,554,18,110,'madeira_fixa'))
upper=box(m,'Painel superior removível675–897 - Arenza liso',20,0,675,550,18,222,'painel_manutencao');fixed.append(upper)
ctrl=d.addObject('App::FeaturePython','ControleCestoR15');m.addObject(ctrl);ctrl.Label='Cesto R15 - Abertura55 e RetiradaSaco'
prop(ctrl,'App::PropertyAngle','Abertura',0);prop(ctrl,'App::PropertyLength','RetiradaSaco',0);prop(ctrl,'App::PropertyAngle','EndireitarSaco',0)
prop(ctrl,'App::PropertyLength','RetiradaPainelSuperior',0)
prop(ctrl,'App::PropertyString','Sequencia','Abertura55; RetiradaSaco0→445 mm; EndireitarSaco0→55 graus. Controles livres: outras combinações não conferidas. Painel superior sai somente para manutenção.')
prop(ctrl,'App::PropertyString','Ferragem','Eixo ideal/pinos-gabarito, não mecanismo comercial validado. Retenção55/controle cheio-vazio e desmontagem acessível pendentes.')
driver=d.addObject('App::Part','BasculanteCestoR15');m.addObject(driver);driver.Label='Cesto/frontais - giro ideal55, sem ferragem selecionada'
driver.Placement.Base=App.Vector(70,70,120);driver.Placement.Rotation=App.Rotation(App.Vector(1,0,0),0)
driver.setExpression('Placement.Rotation.Angle',ctrl.Name+'.Abertura')
# Axis must be X even when the initial angle is zero.
driver.Placement.Rotation.Axis=App.Vector(1,0,0)
front=box(driver,'Frente inferior521 - face630, junta lateral2 proposta',-50,-70,30,550,18,521,'frente_movel');moving.append(front)
# Simple frame reserves: outer450x250x450, mouth420x220. Wood15 is hypothetical,
# not an approved material or a construction/capacity instruction.
frame.append(box(driver,'Fundo18 da armação - gabarito',0,0,0,450,250,18,'armacao_gabarito'))
for x in [0,435]:
 for y in [0,235]:frame.append(box(driver,'Montante15 da armação - gabarito',x,y,18,15,15,417,'armacao_gabarito'))
for x in [0,435]:frame.append(box(driver,'Aro superior15 lateral - gabarito',x,0,435,15,250,15,'armacao_gabarito'))
for y in [0,235]:frame.append(box(driver,'Aro superior15 frente/trás - gabarito',15,y,435,420,15,15,'armacao_gabarito'))
for x in [0,432]:
 for z in [50,350]:frame.append(box(driver,'Ligação frontal52 - reserva não dimensionada',x,-52,z,18,52,18,'ligacao_gabarito'))
moving+=frame
for x in [18,520]:
 o=box(m,'Apoio de pivô52x40x44 - reserva não calculada',x,50,98,52,40,44,'apoio_pivo_gabarito',(.53,.55,.58));fixed.append(o)
for x in [-20,450]:
 pin=feature(driver,'Pino idealØ10x20 - gabarito, sem SKU',Part.makeCylinder(5,20,App.Vector(x,0,0),App.Vector(1,0,0)),'pino_gabarito',(.45,.46,.48));moving.append(pin)
# Bag rotation is about its lower REAR edge after axial withdrawal, not a real hinge.
bagDriver=d.addObject('App::Part','SacoRemovivelR15');driver.addObject(bagDriver);bagDriver.Label='Saco carregado - envelope400x200x400, não molde/volume útil'
bagDriver.Placement.Base=App.Vector(25,225,25);bagDriver.Placement.Rotation.Axis=App.Vector(1,0,0)
bagDriver.setExpression('Placement.Base.z','25 mm + '+ctrl.Name+'.RetiradaSaco')
bagDriver.setExpression('Placement.Rotation.Angle','-'+ctrl.Name+'.EndireitarSaco')
bag=box(bagDriver,'Corpo carregado400x200x400 - alças recolhidas no envelope',0,-200,0,400,200,400,'saco_gabarito',(.83,.82,.78));bag.ViewObject.Transparency=65
upper.setExpression('Placement.Base.y','-'+ctrl.Name+'.RetiradaPainelSuperior')
# Current native useful-tank volume was only an approximate marker. Preserve it as history,
# then reproduce the R08 conditional position and external20 mm construction reserve.
room=next(o for o in m.InList if o.Name=='Ambiente_lavanderia')
oldTank=next(o for o in room.Group if o.Label.startswith('Tanque · vazio útil'))
oldTank.Visibility=False;oldTank.Label='Histórico oculto - volume útil aproximado anterior do tanque'
outer=Part.makeBox(420,390,220,App.Vector(60,30,700));inner=Part.makeBox(380,350,210,App.Vector(80,50,720))
tank=feature(m,'Tanque externo420x390/fundo700 - reserva R08, não produto real',outer.cut(inner),'tanque_gabarito',(.66,.72,.71));fixed.append(tank)
water=box(m,'Vazio útil380x350x200 preservado - posição R08 condicional',80,50,720,380,350,200,'vazio_tecnico',(.67,.82,.86));water.ViewObject.Transparency=85
hydraulic=[]
hydraulic.append(box(m,'Reserva hidráulica superior até330 da parede/base630',70,300,630,450,330,70,'hidraulica_limite',(.58,.70,.78)))
hydraulic.append(box(m,'Reserva hidráulica posterior até280 da parede',70,350,98,450,280,532,'hidraulica_limite',(.58,.70,.78)))
for o in hydraulic:o.ViewObject.Transparency=90
d.recompute()
report={'file':str(dst),'module':m.Name,'original_module_origin_mm':oldOrigin,'new_module_origin_mm':list(m.Placement.Base),'control':ctrl.Name,'driver':driver.Name,'front':front.Name,'frame':[o.Name for o in frame],'bag':bag.Name,'bag_driver':bagDriver.Name,'upper':upper.Name,'moving':[o.Name for o in moving],'fixed':[o.Name for o in fixed],'hydraulic':[o.Name for o in hydraulic],'tank':tank.Name,'new':[o.Name for o in made],'source':'Compatibilizacao_2026-09-30/Cesto_retirada.md; Lavanderia/Tanque_cesto_compatibilizacao_R08.md','dimensions_mm':{'basket':[450,250,450],'mouth':[420,220],'loaded_bag':[400,200,400],'front':[550,18,521],'upper':[550,18,222],'pivot_from_wall_and_floor':[560,120],'face_from_wall':630,'course_deg':55,'withdrawal_mm':445,'straightening_deg':55},'limits':'Referência CAD condicional, sem ferragem comercial validada ou físico real. Armação15/fundo18/ligação52/pino10/apoio52 são hipóteses. Giro55, saco removível e tanque útil preservados; rosto/apoios/painel/cotas propostos.60/50kg de outros produtos não transferíveis. Não incluir máquina/lixeira/mãos como aprovadas por diferença de cotas.'}
((Path(__file__).resolve().parent / 'Montagem_R15.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');d.save();result={'file':str(dst),'new_shapes':len(made),'control':ctrl.Name}
