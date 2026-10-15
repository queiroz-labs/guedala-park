from pathlib import Path
import json, shutil
import FreeCAD as App, Part
root=(Path(__file__).resolve().parent / '.').resolve()
src=(Path(__file__).resolve().parent / '../Gaveta_rodas_R13_2026-10-14/Guedala_Park_R13_Gaveta_Rodas.FCStd').resolve()
dst=(Path(__file__).resolve().parent / 'Guedala_Park_R14_Correr_Simples.FCStd').resolve()
assert not dst.exists(),'Revisão existente: não reconstruir'
prev=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==src)
prev.save();shutil.copy2(src,dst);d=App.openDocument(str(dst));App.setActiveDocument(d.Name)
d.Label='Guedala Park - R14 - correr comum sobreposto, proposta'
made=[];rows=[]
status='Proposta dimensional, não corte/compra. RO-62 candidato; referências simplificadas, sem STEP oficial. Fixação/retenção/curso/montagem física pendentes.'
def prop(o,t,n,v):
 if n not in o.PropertiesList:o.addProperty(t,n,'Estudo R14')
 setattr(o,n,v)
def box(parent,label,x,y,z,w,p,h,kind,color=(.65,.67,.70)):
 o=d.addObject('Part::Feature','ReferenciaCorrerR14');parent.addObject(o);o.Label=label
 o.Shape=Part.makeBox(w,p,h,App.Vector(x,y,z));prop(o,'App::PropertyString','CategoriaR14',kind);prop(o,'App::PropertyString','Status',status)
 o.ViewObject.ShapeColor=color
 if kind!='madeira':o.ViewObject.Transparency=65
 made.append(o);return o
def move_param(o,field,val):
 o.setExpression(field,None)
 if field.startswith('Placement.Base.'):
  p=o.Placement;setattr(p.Base,field[-1],val);o.Placement=p
 else:setattr(o,field,val)
ward=d.getObject('Modulo');male=d.getObject('Modulo002')
# Wardrobe: front structure stays within the already-reserved82 mm package.
# These are uncalculated support proposals, not certified load-bearing joints.
fixed=[]
for x in [0,1982]:fixed.append(box(ward,'Apoio frontal lateral18 - proposta',x,0,62,18,82,2070,'madeira',(.81,.79,.73)))
fixed.append(box(ward,'Continuação frontal da base18 - apoio não calculado',18,0,62,1964,82,18,'madeira',(.81,.79,.73)))
fixed.append(box(ward,'Travessa superior frontal18 - apoio não calculado',18,0,2114,1964,82,18,'madeira',(.81,.79,.73)))
# Maleiro: ordinary internal doors need side jambs and continuous bottom/top track carriers.
for n in ['Peca259','Peca260','Peca262','Peca263']:
 o=d.getObject(n);move_param(o,'Placement.Base.y',0);move_param(o,'Width',650 if n in ['Peca259','Peca260'] else 632)
 prop(o,'App::PropertyString','RevisaoR14','Frente do corpo estendida40 mm para apoiar trilhos internos; envelope externo preservado. Ligação/carga pendentes.')
 fixed.append(o)
controls=d.addObject('App::DocumentObjectGroup','ControlesCorrerR14');controls.Label='R14 - correr portas (Deslocamento em mm)'
specs=[dict(module=ward,names=['Peca247','Peca248'],drivers=['PortaCorrer','PortaCorrer001'],W=2000,leafW=995,leafH=1999,z=90,base=80,top=2114,course=965,right=985),
       dict(module=male,names=['Peca264','Peca265'],drivers=[None,None],W=1350,leafW=670,leafH=237,z=28,base=18,top=290,course=640,right=660)]
for sp in specs:
 m=sp['module'];track=[];moving=[];leaves=[];drivers=[];inputs=[]
 prop(m,'App::PropertyString','SolucaoCorrerR14','RO-62 sobreposto candidato / RM-025 superior / RM-023 inferior / guia Flex / freios / retenção; sem amortecedor. Gabaritos, não STEP.')
 prop(m,'App::PropertyString','CondicaoR14',status)
 # Track nominal WIDTHS34/28 come from the official manual. HEIGHTS4/20, wall thickness1,
 # guide/carriage envelopes and split10+25 of the height allowance are explicit hypotheses.
 for lane in range(2):
  y=34*lane
  track.append(box(m,'RM-023 largura34 - envoltória altura4 hipotética',18,y,sp['base'],sp['W']-36,34,4,'trilho_gabarito'))
  track.append(box(m,'RM-025 largura28 - canal altura20 hipotética',18,y+3,sp['top']-20,sp['W']-36,1,20,'trilho_gabarito'))
  track.append(box(m,'RM-025 parede oposta - espessura1 hipotética',18,y+30,sp['top']-20,sp['W']-36,1,20,'trilho_gabarito'))
  track.append(box(m,'RM-025 topo - espessura1 hipotética',18,y+3,sp['top']-1,sp['W']-36,28,1,'trilho_gabarito'))
 for i,n in enumerate(sp['names']):
  leaf=d.getObject(n)
  if sp['drivers'][i]:driver=d.getObject(sp['drivers'][i])
  else:
   m.removeObject(leaf);driver=d.addObject('App::Part','PortaMaleiroR14');m.addObject(driver);driver.addObject(leaf)
  # User edits only the external independent positive input.
  c=d.addObject('App::FeaturePython','ControleCorrerR14');controls.addObject(c);c.Label=m.Label+' / folha '+str(i+1)
  prop(c,'App::PropertyLength','Deslocamento',0);prop(c,'App::PropertyLength','CursoEstudo',sp['course']);c.setEditorMode('CursoEstudo',1)
  prop(c,'App::PropertyString','Status','Curso proposto sem batente físico confirmado. Valores acima de CursoEstudo não foram conferidos.')
  prop(driver,'App::PropertyLength','Deslocamento',0);driver.setExpression('Deslocamento',c.Name+'.Deslocamento');driver.setEditorMode('Deslocamento',1)
  driver.setExpression('Placement.Base.x',str(sp['right'] if i else 20)+' mm '+('-' if i else '+')+' Deslocamento')
  p=driver.Placement;p.Base.y=6+34*i;p.Base.z=sp['z'];driver.Placement=p
  driver.Label=m.Label+' / correr '+str(i+1)+' - RO62 candidato'
  prop(driver,'App::PropertyString','Ferragem',status)
  leaf.Placement=App.Placement();leaf.Length=sp['leafW'];leaf.Width=18;leaf.Height=sp['leafH'];leaf.Status=status
  for end,x,sign in [('esquerdo',10,1),('direito',sp['leafW']-120,1)]:
   # Conservative mounting reservations only; no inferred replica of the mechanism.
   moving.append(box(driver,'RO62 '+end+' - reserva110x13x55 hipotética',x,18,-10,110,13,55,'carro_gabarito'))
   guideX=30 if end=='esquerdo' else sp['leafW']-115
   moving.append(box(driver,'Guia Flex '+end+' - reserva85x28x15 hipotética',guideX,-5,sp['leafH']-2,85,28,15,'guia_gabarito'))
   moving.append(box(driver,'Retenção '+end+' - reserva55x13x12 hipotética',guideX,18,sp['leafH']-12,55,13,12,'retencao_gabarito'))
   # Four pilot axes follow the manual's22/86 and8.5/32.5 dimension scheme.
   for xx in [22,86]:
    for zz in [8.5,32.5]:
     px=xx if end=='esquerdo' else sp['leafW']-xx
     axis=d.addObject('Part::Feature','EixoFixacaoR14');driver.addObject(axis)
     axis.Label='Eixo referencial RO62 '+end+' x'+str(xx)+' z'+str(zz)+' - sem diâmetro de piloto'
     axis.Shape=Part.makeLine(App.Vector(px,18,zz),App.Vector(px,31,zz));axis.ViewObject.LineColor=(.8,.15,.1)
     prop(axis,'App::PropertyString','Status','Somente eixos do padrão manual; não furação. Direita espelhada proposta; confirmar aplicação.')
  leaves.append(leaf);drivers.append(driver);inputs.append(c)
  for endpoint in [20,sp['W']-40]:
   track.append(box(m,'Freio superior - reserva20x13x8 hipotética',endpoint,6+34*i,sp['top']-8,20,13,8,'freio_gabarito'))
 rows.append({k:sp[k] for k in ['W','leafW','leafH','z','base','top','course','right']}|dict(module=m.Name,leaves=[o.Name for o in leaves],drivers=[o.Name for o in drivers],controls=[o.Name for o in inputs],moving=[o.Name for o in moving],tracks=[o.Name for o in track],density750_panel_kg=sp['leafW']*18*sp['leafH']*750/1e9,density900_panel_kg=sp['leafW']*18*sp['leafH']*900/1e9))
d.recompute()
report={'file':str(dst),'system_candidate':'Rometal RO-62, 60 kg/porta,18 mm,AP=AV-35,transpasse30; nenhuma compra/liberação','reference_kind':'Manual oficial, sem STEP disponível nas fontes consultadas. Reservas geométricas com dimensões hipotéticas explícitas; não peças reais certificadas.','rows':rows,'fixed':[o.Name for o in fixed],'new':[o.Name for o in made],'hypotheses':['Folga inferior10 e superior25 somam35; divisão não fornecida pelo manual','Passo entre vias34 proposto por dois perfis RM-023, não eixo certificado','Carro110x13x55,guia85x28x15,retencao55x13x12,freio20x13x8: envoltórias hipotéticas','Altura inferior4/superior20 e espessura1 dos perfis não dimensionadas na fonte','Apoios madeira18 dentro do envelope, sem cálculo de resistência ou ligação','Folhas internas/curso menor são propostas necessárias ao cenário; programa preservado']}
((Path(__file__).resolve().parent / 'Montagem_R14.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
d.save();result={'file':str(dst),'pieces':len(made),'rows':rows}
