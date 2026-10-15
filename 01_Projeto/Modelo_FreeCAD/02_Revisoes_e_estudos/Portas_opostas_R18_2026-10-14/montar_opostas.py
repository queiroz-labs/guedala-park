from pathlib import Path
import json,shutil,copy,hashlib
import FreeCAD as App,Part
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
src=(Path(__file__).resolve().parent / '../Equipamentos_R17_2026-10-14/Guedala_Park_R17_Equipamentos.FCStd').resolve();dst=(Path(__file__).resolve().parent / 'Guedala_Park_R18_Portas_Opostas.FCStd').resolve()
assert not dst.exists(),'Revisão existente; não reconstruir'
prev=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==src)
assert prev.isSaved() and src.stat().st_size>100000
source_hash=hashlib.sha256(src.read_bytes()).hexdigest();shutil.copy2(src,dst)
d=App.openDocument(str(dst));App.setActiveDocument(d.Name);d.Label='Guedala Park - R18 - portas vizinhas em sentidos opostos'
data=json.loads(((Path(__file__).resolve().parent / '../Apoios_R11_2026-10-14/Montagem_R11.json').resolve()).read_text(encoding='utf-8'));rows=copy.deepcopy(data['doors'])
def prop(o,t,n,v):
 if n not in o.PropertiesList:o.addProperty(t,n,'Portas opostas R18')
 setattr(o,n,v)
def worldshape(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def bbox(o):
 b=worldshape(o).optimalBoundingBox();return [b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength,b.ZLength]
before={r['door']:bbox(d.getObject(r['front'])) for r in rows};before['VizinhaCADR03']=bbox(d.getObject('VizinhaComCanecosR03'))
supports=[]
def support(module,x,label):
 o=d.addObject('Part::Box','ApoioOpostoR18');module.addObject(o);o.Label=label
 o.Length=18;o.Width=float(module.Profundidade)-38;o.Height=float(module.Altura)-36;o.Placement.Base=App.Vector(x,20,18);o.ViewObject.ShapeColor=(.84,.83,.76)
 prop(o,'App::PropertyString','Status','Painel comum18 proposto. Apoio/fixação/carga não calculados; não libera corte/furação/compra. Dois18 justapostos nos encontros de dobradiças, sem ferragem especial.')
 supports.append(o);return o
support(d.getObject('Modulo016'),982,'Escritório - segundo18 no divisor das portas2/3; conjunto36')
support(d.getObject('Modulo003'),869.5,'Cabeceira - segundo18 no divisor das portas2/3; conjunto36')
support(d.getObject('Modulo003'),1757,'Cabeceira - apoio18 da vizinha à direita; proposta')
changed=[]
for idx,end,mx,width in [(1,998,982,496),(3,1998,1982,496),(5,885.5,869.5,439.75)]:
 r=rows[idx];g=d.getObject(r['door']);panel=d.getObject(r['old_panel']);c=d.getObject(r['control'])
 panel.setExpression('Length',None);panel.Length=width;panel.Placement.Base.x=-width
 for cut in d.getObject(r['front']).Tool.Shapes:cut.Placement.Base.x=-22.5
 ref=lambda a:'CinematicaComumR11.D'+str(idx+1)+a
 phi='-'+ref('Theta');tx=ref('T4x');ty='-'+ref('T4z');my=56.5
 g.setExpression('Placement.Base.x',f'({mx}+({tx})+({end-mx})*cos({phi})-({-my})*sin({phi}))*1 mm')
 g.setExpression('Placement.Base.y',f'({my}+({ty})+({end-mx})*sin({phi})+({-my})*cos({phi}))*1 mm')
 g.setExpression('Placement.Rotation.Angle',phi)
 for h in r['hinges']:
  a=d.getObject(h['group']);a.Placement=App.Placement(App.Vector(mx,57,h['level']),App.Rotation(App.Vector(1,0,0),90))
 r.update(side='right',closed_x_mm=end,hinge_support_inner_x_mm=mx,front_source_dimensions=[width,18,float(panel.Height)],revision='R18')
 prop(c,'App::PropertyString','SentidoR18','Direita, vista de frente; alterna com vizinha à esquerda.')
 c.Label=c.Label+' - direita R18'
 g.Movimento='R18: direita com71B3550/calço0/K5/recobrimento16. Dois18 comuns no divisor compartilhado. Curso86 de estudo; batente/fixação/carga/tolerâncias pendentes.'
 if idx==5:
  c.JuntaDireitaProposta=4;r['right_joint_mm']=4
  d.getObject(rows[6]['control']).JuntaEsquerdaProposta=4;rows[6]['left_joint_mm']=4
 changed.append(g.Name)
# Replace the last headboard leaf's previous half-overlay hinge with a common full-overlay
# hinge at its right edge. Closed size and pose remain exactly the same.
head=d.getObject('Modulo003');corner=d.getObject('Modulo001')
history=d.addObject('App::Part','HistoricoVizinhaR18');corner.addObject(history);history.Label='Histórico oculto - vizinha71B3650 à esquerda, substituídaR18'
old=[o for o in corner.Group if o.Name=='VizinhaCADR03' or o.Label.startswith('71B3650 - quatro barras')]
for o in old:corner.removeObject(o);history.addObject(o);o.Visibility=False
history.Visibility=False
cgroup=d.addObject('App::DocumentObjectGroup','ControlesPortasR18');cgroup.Label='R18 - vizinha da cabeceira à direita; demais comandosR11/R10/R12'
c=d.addObject('App::FeaturePython','ControleVizinhaR18');cgroup.addObject(c);c.Label='Cabeceira porta4/vizinha - abrir à direita'
prop(c,'App::PropertyAngle','Abertura',0);prop(c,'App::PropertyAngle','CursoEstudo',86)
prop(c,'App::PropertyString','SentidoR18','Direita; sequência cabeceira esquerda/direita/esquerda/direita, depois cantoB à esquerda.')
prop(c,'App::PropertyString','Status','Montagem comum candidata.86 é limite de estudo, não comprova70T3553. Fixação/carga/regulagens e apoios reais pendentes.')
sheet=d.addObject('Spreadsheet::Sheet','CinematicaComumR18');sheet.Label='R18 - quatro barras71B3550 da vizinha à direita'
source_sheet=d.getObject('CinematicaComumR11')
for i in range(3,21):
 addr='B'+str(i);expr=source_sheet.getContents(addr).replace(rows[0]['control'],c.Name)
 sheet.set(addr,expr);sheet.setAlias(addr,'N'+source_sheet.getAlias(addr)[2:]);sheet.set('A'+str(i),source_sheet.getAlias(addr)[2:])
g=d.addObject('App::Part','VizinhaComumR18');head.addObject(g);g.Label='Cabeceira porta4 - direita, dobradiça comum R18';g.Placement.Base.z=1
prop(g,'App::PropertyAngle','Abertura',0);g.setExpression('Abertura',c.Name+'.Abertura')
prop(g,'App::PropertyString','Movimento','71B3550/calço0/K6/recobrimento17; duas candidatas, dimensões441.75x306 mantidas. Apoio18 simples em1757..1775, faixa25/cantoR04 preservados. Não libera furação/carga/batente.')
ref=lambda a:sheet.Name+'.N'+a
mx,end,my=1757,1774,56.5;phi='-'+ref('Theta')
g.setExpression('Placement.Base.x',f'({mx}+({ref("T4x")})+17*cos({phi})-({-my})*sin({phi}))*1 mm')
g.setExpression('Placement.Base.y',f'({my}-({ref("T4z")})+17*sin({phi})+({-my})*cos({phi}))*1 mm')
g.setExpression('Placement.Rotation.Angle',phi)
panel=d.addObject('Part::Box','PainelVizinhaR18');g.addObject(panel);panel.Label='Vizinha441.75x306 - fechada preservada';panel.Length=441.75;panel.Width=18;panel.Height=306;panel.Placement.Base.x=-441.75;panel.ViewObject.ShapeColor=(.75,.67,.55)
tools=[];levels=[80,228]
for z in levels:
 h=d.addObject('Part::Cylinder','CanecoVizinhaR18');g.addObject(h);h.Radius=17.5;h.Height=13;h.Placement=App.Placement(App.Vector(-23.5,18,z-1),App.Rotation(App.Vector(0,0,1),App.Vector(0,-1,0)));tools.append(h)
fused=d.addObject('Part::MultiFuse','FurosVizinhaR18');g.addObject(fused);fused.Shapes=tools
front=d.addObject('Part::Cut','FrenteVizinhaR18');g.addObject(front);front.Base=panel;front.Tool=fused;front.Label='Vizinha direita - canecos comuns K6, proposta';front.ViewObject.ShapeColor=panel.ViewObject.ShapeColor
assemblies=[];prototype=rows[0]['hinges'][0]
for z in levels:
 a=d.addObject('App::Part','DobradicaVizinhaR18');head.addObject(a);a.Label='71B3550 vizinha direita - z'+str(z);a.Placement=App.Placement(App.Vector(mx,57,z),App.Rotation(App.Vector(1,0,0),90))
 adj=d.addObject('App::Part','AjusteVizinhaR18');a.addObject(adj);adj.Placement.Base.z=.5;adj.Label='Regulagem comum profundidade0.5, proposta'
 bodies=[]
 for item in prototype['bodies']:
  i=item['index'];driver=d.addObject('App::Part','CorpoVizinhaR18');adj.addObject(driver)
  if i in [2,3,4]:
   driver.Placement.Rotation.Axis=App.Vector(0,1,0);driver.setExpression('Placement.Rotation.Angle','-'+ref('Theta' if i==4 else 'Theta'+str(i)))
   driver.setExpression('Placement.Base.x',ref('T'+str(i)+'x')+'*1 mm');driver.setExpression('Placement.Base.z',ref('T'+str(i)+'z')+'*1 mm')
  o=d.addObject('Part::Feature','FerragemVizinhaR18');driver.addObject(o);o.Shape=d.getObject(item['body']).Shape.copy();o.Label='71B3550 corpo'+str(i)+' - vizinha direita';o.ViewObject.ShapeColor=(.65,.68,.72);prop(o,'App::PropertyInteger','IndiceCorpo',i)
  bodies.append({'driver':driver.Name,'body':o.Name,'index':i})
 o=d.addObject('Part::Feature','CalcoVizinhaR18');a.addObject(o);o.Shape=d.getObject(prototype['plate']).Shape.copy();o.Label='173H7100 calço0 - vizinha direita';o.ViewObject.ShapeColor=(.65,.68,.72)
 assemblies.append({'group':a.Name,'adjustment':adj.Name,'bodies':bodies,'plate':o.Name,'level':z})
nr={'module':head.Name,'door':g.Name,'control':c.Name,'front':front.Name,'old_panel':panel.Name,'side':'right','hinges':assemblies,'K_mm':6,'overlay_mm':17,'plate_spacing_mm':0,'plate_hole_row_y':57,'depth_adjustment_proposed_mm':.5,'closed_x_mm':1774,'hinge_support_inner_x_mm':1757,'front_source_dimensions':[441.75,18,306],'left_joint_mm':2,'right_joint_mm':29,'revision':'R18'}
rows.append(nr);changed.append(g.Name)
for o in tools+[panel,fused]:o.Visibility=False
front.Visibility=True
d.getObject('ControleCanto').set('A4','Vizinha históricaR03; atual usa ControleVizinhaR18');d.getObject('ControleCanto').set('B4','0 deg')
head.Condicoes='R18 autorizado: quatro folhas em sentidos esquerda/direita/esquerda/direita, vizinha agora comum à direita. Envelope/programa/cantoR04/faixa25 preservados; divisor central duplo18 e apoio18 da vizinha propostos, segunda frente439.75/junta4. Apoios/fixação/carga/cotas executivas pendentes.'
d.getObject('Modulo016').Condicoes='R18: quatro folhas496x548 em2000x350x550, sentidos esquerda/direita/esquerda/direita. Divisor2 recebe segundo18, conjunto36; três divisórias existentes preservadas. Vãos/programa/fixação/carga propostos.'
prop(corner,'App::PropertyString','AtualizacaoR18','Vizinha substituída por71B3550 à direita na cabeceira. Canto simplesR04/portasA-B/faixas/painéis/controles preservados. B à esquerda/A à direita nas respectivas vistas frontais.')
d.recompute()
after={r['door']:bbox(d.getObject(r['front'])) for r in rows}
assert max(abs(x-y) for x,y in zip(before['VizinhaCADR03'],after[g.Name]))<1e-6
assert max(abs(x-y) for x,y in zip(before[rows[1]['door']],after[rows[1]['door']]))<1e-6
assert max(abs(x-y) for x,y in zip(before[rows[3]['door']],after[rows[3]['door']]))<1e-6
invalid=[o.Name for o in d.Objects if 'Invalid' in o.State];assert not invalid,str(invalid)
for r in rows:assert d.getObject(r['front']).Shape.isValid()
d.recompute();d.save();assert d.isSaved() and dst.stat().st_size>100000 and hashlib.sha256(src.read_bytes()).hexdigest()==source_hash
report={'file':str(dst),'source':str(src),'source_sha256':source_hash,'doors':rows,'changed_doors':changed,'before_bboxes':before,'closed_bboxes':after,'new_supports':[{'name':o.Name,'label':o.Label,'module':o.InList[0].Name,'bbox':bbox(o)} for o in supports],'historical_neighbor_groups':[o.Name for o in old],'policy':'Portas vizinhas de giro horizontal alternam esquerda/direita, vista de frente. Todos paresR10/R12 e correrR14 já opostos; cantoB esquerda/A direita preservado. Basculantes/tampas mantêm operação vertical. Novo pedido prevalece sobre vizinha71B3650 e sentidos todos-esquerda daR11.'}
((Path(__file__).resolve().parent / 'Montagem_R18.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result={'file':str(dst),'changed_doors':changed,'supports':len(supports),'invalid':invalid,'neighbor_closed_preserved':True}
