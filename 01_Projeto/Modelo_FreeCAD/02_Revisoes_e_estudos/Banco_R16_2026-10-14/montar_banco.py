from pathlib import Path
import json,shutil
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
src=(Path(__file__).resolve().parent / '../Cesto_R15_2026-10-14/Guedala_Park_R15_Cesto_Simples.FCStd').resolve();dst=(Path(__file__).resolve().parent / 'Guedala_Park_R16_Banco_Simples.FCStd').resolve()
assert not dst.exists(),'Revisão existente: não reconstruir'
prev=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==src)
prev.save();shutil.copy2(src,dst);d=App.openDocument(str(dst));App.setActiveDocument(d.Name)
d.Label='Guedala Park - R16 - banco, apoios e programa, proposta'
source=(Path(__file__).resolve().parent / '../../../Compatibilizacao_2026-10-08').resolve()
a=json.loads(((Path(__file__).resolve().parent / '../../../Compatibilizacao_2026-10-08/Armazenamento_resultados.json').resolve()).read_text(encoding='utf-8'));detail=json.loads(((Path(__file__).resolve().parent / '../../../Compatibilizacao_2026-10-08/Detalhe_banco_resultados.json').resolve()).read_text(encoding='utf-8'))
m=d.getObject('Modulo019');m.Condicoes='180x55 externo incluindo encosto10, topo47 preservados. R16 programa da ponta sofá para cozinha, tampas nos centros das divisórias, apoios frontais/posteriores propostos. Almofadas removíveis bebidas/balde; potes/folha assento integral70 por giro ideal. Ferragem/retenção/carga/fixações reais pendentes.'
def prop(o,t,n,v):
 if n not in o.PropertiesList:o.addProperty(t,n,'Estudo R16')
 setattr(o,n,v)
def setnum(o,field,v):
 o.setExpression(field,None)
 if field.startswith('Placement.Base.'):
  p=o.Placement;setattr(p.Base,field[-1],v);o.Placement=p
 else:setattr(o,field,v)
# Local X increases towards sofa in the native rotated module; source v starts at sofa
# and increases towards kitchen. Mirror longitudinal geometry, not the apartment footprint.
def local(v,u,z,w,p,h):return (1800-v-w,u,z,w,p,h)
def raw(r):return local(18+10*r['x'],10*(40.8-r['y']-r['d']),10*r['z'],10*r['w'],10*r['d'],10*r['h'])
made=[];struct=[];contents=[];panels=[];ledges=[]
def box(parent,label,x,y,z,w,p,h,kind,color=(.73,.67,.56)):
 o=d.addObject('Part::Box','PecaBancoR16');parent.addObject(o);o.Label=label;o.Length=w;o.Width=p;o.Height=h;o.Placement.Base=App.Vector(x,y,z)
 prop(o,'App::PropertyString','CategoriaR16',kind);prop(o,'App::PropertyString','Status','Proposta/envelope; medidas, materiais, carga, fixação e ferragens reais pendentes. Sem corte/furação/compra.')
 o.ViewObject.ShapeColor=color;made.append(o);return o
history=d.addObject('App::Part','HistoricoBancoR16');m.addObject(history);history.Label='Histórico oculto - piso100 e divisões/tampas ilustrativas'
for n in ['Peca409','Peca410','Peca411','Peca412','Peca413','Peca414','Peca415','Peca416','Peca417','Peca418','Peca419','Peca420']:
 o=d.getObject(n);m.removeObject(o);history.addObject(o);o.Visibility=False
history.Visibility=False
# Ordinary full front/back/side panels give bearing without ledges stealing the opening.
for n in ['Peca406','Peca407']:
 o=d.getObject(n);setnum(o,'Placement.Base.y',0);setnum(o,'Width',450);o.Visibility=True;struct.append(o)
back=d.getObject('Peca408');setnum(back,'Height',382);back.Visibility=True;struct.append(back)
struct.append(box(m,'Frente18 estrutural - apoio não calculado',18,2,0,1764,18,400,'estrutura'))
struct.append(box(m,'Fundo potes/travessas a80 - hipótese18',*local(18,20,62,362,390,18),'estrutura'))
struct.append(box(m,'Fundo demais setores a100 - hipótese18',*local(398,20,82,1384,390,18),'estrutura'))
for v,z in [(380,80),(748,100),(964,100)]:struct.append(box(m,'Divisória18 contínua - centro da junta',*local(v,20,z,18,390,400-z),'estrutura'))
struct.append(box(m,'Divisão inferior aspirador/jogos - proposta',*local(1373,20,100,18,390,202),'estrutura'))
struct.append(box(m,'Base do nicho da folha18 - proposta não calculada',*local(982,20,302,800,390,18),'estrutura'))
controls=d.addObject('App::DocumentObjectGroup','ControlesBancoR16');controls.Label='R16 - abrir banco; almofadas bebidas/balde primeiro'
lidrows=[]
# joints2 on divider centre-lines389/757/973, source exterior v coordinate.
for i,(v,w,title,separate,park) in enumerate([(1,387,'Potes/travessas/batedeira',False,None),(390,366,'Liquidificador e bebidas',True,1100),(758,214,'Balde',True,1490),(974,825,'Folha/aspirador/jogos',False,None)],1):
 c=d.addObject('App::FeaturePython','ControleBancoR16');controls.addObject(c);c.Label=str(i)+' - '+title
 prop(c,'App::PropertyAngle','Abertura',0);prop(c,'App::PropertyString','Ferragem','Giro ideal90. Dobradiça comum e retenção reais não selecionadas; não modificar cotas para apagar contato sem dados.')
 driver=d.addObject('App::Part','TampaBancoR16');m.addObject(driver);driver.Label=title+' - '+('tampa fina, almofada removível' if separate else 'assento integral70 - estudo')
 driver.Placement.Base=App.Vector(1800-v-w,448,420 if separate else 470);driver.Placement.Rotation.Axis=App.Vector(1,0,0)
 driver.setExpression('Placement.Rotation.Angle','-'+c.Name+'.Abertura')
 lid=box(driver,'Tampa20 - envelope total, não chapa liberada',0,-448,-20 if separate else -70,w,448,20,'tampa')
 # Cushions preserve reference widths368/216 over the2 mm wood joint; upholstery/tolerance unknown.
 padV=v-1;padW=w+2
 if separate:
  pad=box(m,'Almofada50 removível - '+title,*local(padV,0,420,padW,450,50),'almofada',(.83,.81,.76))
  prop(c,'App::PropertyLength','ElevarAlmofada',0);prop(c,'App::PropertyLength','DeslocamentoAlmofada',0)
  pad.setExpression('Placement.Base.z','420 mm + '+c.Name+'.ElevarAlmofada')
  pad.setExpression('Placement.Base.x',str(1800-padV-padW)+' mm - '+c.Name+'.DeslocamentoAlmofada')
  prop(c,'App::PropertyString','Sequencia','Banco desocupado: elevar60, deslocar'+str(park-padV)+', baixar elevação para50; abrir90. Guardar em ordem inversa. Ponta acima da folha ocupada pela almofada: não acessar folha ao mesmo tempo.')
 else:
  # Two cushions remain in the integral moving envelope, not a newly-approved daily removal routine.
  pad=box(driver,'Almofada50 no giro do assento - hipótese',-1,-448,-50,w+2,450,50,'almofada',(.83,.81,.76))
  prop(c,'App::PropertyString','Sequencia','Giro ideal do assento integral70; massa/retenção/pega reais pendentes. Não abrir a folha com almofadas estacionadas neste setor.')
 lidrows.append(dict(id=i,title=title,v=v,w=w,control=c.Name,driver=driver.Name,lid=lid.Name,cushion=pad.Name,separate_cushion=separate,parking_source_v=park,pad_v=padV,pad_w=padW))
# Exact accepted reference envelopes, not chosen products or capacity guarantees.
objectmap={}
for r in a['pots']+a['lower']+a['drinks']+[a['bucket']]:
 o=box(m,r['id']+' - gabarito da organização aprovada',*raw(r),'conteudo',(.72,.78,.77));o.ViewObject.Transparency=50;objectmap[r['id']]=o.Name;contents.append(o)
for r in detail['supports']['boards']:
 o=box(m,r['id']+'18 removível - folgas3',*raw(r),'painel_removivel');objectmap[r['id']]=o.Name;panels.append(o)
for r in detail['supports']['ledges']:
 o=box(m,r['id']+'10x6 - reserva sem peça/carga confirmadas',*raw(r),'suporte_gabarito',(.54,.55,.56));ledges.append(o)
tray=a['tray'];out=raw(tray['outer']);ins=raw(tray['inside']);outer=Part.makeBox(out[3],out[4],out[5],App.Vector(*out[:3]));inner=Part.makeBox(ins[3],ins[4],ins[5]+5,App.Vector(*ins[:3]))
contain=d.addObject('Part::Feature','ContencaoBaldeR16');m.addObject(contain);contain.Label='Contenção removível180x350x33 - estanqueidade/material não confirmados';contain.Shape=outer.cut(inner);contain.ViewObject.ShapeColor=(.62,.66,.67);prop(contain,'App::PropertyString','CategoriaR16','contencao_gabarito');made.append(contain)
leaf=box(m,'Reserva folha800x350x70 - dimensões completas a conferir',*local(982,40,330,800,350,70),'folha_gabarito',(.69,.72,.72));leaf.ViewObject.Transparency=70
for v,title in [(992,'Aspirador'),(1401,'Jogos')]:
 o=box(m,title+' - reserva371x350x164; programa real não reduzido a caixa',*local(v,40,110,371,350,164),'reserva_programa',(.64,.70,.73));o.ViewObject.Transparency=80;contents.append(o)
d.recompute()
report={'file':str(dst),'module':m.Name,'orientation':'Fonte v=0 na ponta sofá/globalY3750; nativoX cresce rumo sofá/globalY5550-X. Conversão X=1800-v-comprimento corrige ordem interna, sem mover banco. u=Y local (profundidade).','lids':lidrows,'new':[o.Name for o in made],'structure':[o.Name for o in struct],'objects':objectmap,'content':[o.Name for o in contents],'panels':[o.Name for o in panels],'ledges':[o.Name for o in ledges],'containment':contain.Name,'leaf':leaf.Name,'source_files':[str((Path(__file__).resolve().parent / '../../../Compatibilizacao_2026-10-08/Armazenamento_resultados.json').resolve()),str((Path(__file__).resolve().parent / '../../../Compatibilizacao_2026-10-08/Detalhe_banco_resultados.json').resolve())],'proposals':['Juntas2 nos centros389/757/973; madeira387/366/214/825 por448x20; envelopes, não composição executiva','Primeiro/último assento integral70, eixo448/470 ideal; bebidas/balde tampa20 com eixo448/420 ideal','Frente18/corpo lateral450/fundo posterior até400 completam apoios; sem dimensionamento de resistência/fixação','Primeiro piso top80, demais100; apoios de potes orçamento24=6+18, sem ferragem selecionada','Não há pinos/dobradiças/retentores reais nesta revisão; não prova física/tolerância/carga/higiene/pega']}
((Path(__file__).resolve().parent / 'Montagem_R16.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');d.save();result={'file':str(dst),'shapes':len(made),'controls':[r['control'] for r in lidrows]}
