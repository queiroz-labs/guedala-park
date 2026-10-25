from pathlib import Path
import json,shutil,hashlib
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
source=(Path(__file__).resolve().parent / '../Controles_R21_2026-10-14/Guedala_Park_R21_Controles_Organizados.FCStd').resolve()
work=(Path(__file__).resolve().parent / 'Trabalho_visual_R21.FCStd').resolve()
catalog=json.loads(((Path(__file__).resolve().parent / '../Controles_R21_2026-10-14/Controles_R21.json').resolve()).read_text(encoding='utf-8'))
mapping=json.loads(((Path(__file__).resolve().parent / '../Apartamento_espelhado_R20_2026-10-14/Espelhamento_R20.json').resolve()).read_text(encoding='utf-8'))['mapping']
r18=json.loads(((Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Montagem_R18.json').resolve()).read_text(encoding='utf-8'))
r10=json.loads(((Path(__file__).resolve().parent / '../Dobradicas_R10_2026-10-14/Montagem_R10.json').resolve()).read_text(encoding='utf-8'))
r12=json.loads(((Path(__file__).resolve().parent / '../Banheiro_R12_2026-10-14/Montagem_R12.json').resolve()).read_text(encoding='utf-8'))
banco=json.loads(((Path(__file__).resolve().parent / '../Banco_R16_2026-10-14/Montagem_R16.json').resolve()).read_text(encoding='utf-8'))
scenes={
 'Escritorio':{'sources':['Modulo016'],'camera':[-1,-.3,.32],'title':'Escritório — quatro portas alternadas','note':'Quatro folhas em60 graus; apoios compartilhados propostos. Vista de uso, não auditoria nova de ferragens ou montagem executiva.'},
 'Cabeceira_canto':{'sources':['Modulo003','Modulo001'],'camera':[-1,-.65,.48],'title':'Cabeceira e canto simples','note':'Cabeceira e vizinha em60 graus; cantoA/B em60. Alternância na orientação espelhada, sem mecanismo79T8500. Limite mecânico real pendente.'},
 'Cozinha':{'sources':['Modulo004','Modulo005','Modulo006','Modulo007','Modulo008','Modulo009','Modulo010','Modulo011','Modulo012','Peca308','Peca138','Peca140','Peca351','Peca133','Peca134','Peca139','Peca135','Peca136','Peca137','Peca141'],'camera':[.2,-1,.45],'title':'Cozinha — portas comuns e nichos','note':'Pares de portas em60 graus; equipamentos mantidos. A imagem não resolve as divergências de instalação/ventilação registradas naR17.'},
 'Gavetas_cozinha':{'sources':['Modulo005','Modulo007'],'camera':[.15,-1,.62],'title':'Gavetas e armazenamento baixo','note':'G2 em300 mm e baixa em530 mm. Bandejas455/programa preservados. Baixa sobre rodas-gabarito; translações ideais não comprovam telescópio, piso, carga ou retirada real.'},
 'Banheiro':{'sources':['Modulo017','Modulo018','PortaEntradaBanheiroR12'],'camera':[.25,-1,.5],'title':'Banheiro — acesso com entrada fechada','note':'Quatro portas em60 graus, entrada ideal0 fechada e translúcida somente nesta vista para revelar os gabinetes. Folha/eixo/maçaneta da entrada não medidos; ferragens, vidro/adesivo e hidráulica reais pendentes.'},
 'Cesto':{'sources':['Modulo013','Peca147'],'camera':[-.25,-1,.6],'title':'Cesto — abertura e saco removível','note':'Giro55 graus, saco445 mm/endireitado55. Loop20L permanece no seu lugar habitual. Não mostra manutenção da armação como livre; ela bate na lixeira em300/400.'},
 'Banco_diario':{'sources':['Modulo019'],'camera':[1,-.3,.62],'title':'Banco — bebidas e balde','note':'Tampas2/3 em90 graus, almofadas estacionadas sobre setor da folha fechado. Devolver antes de acessar folha. Eixos/apoios/retencões reais pendentes.'},
 'Banco_folha':{'sources':['Modulo019']+['Peca'+str(i).zfill(3) for i in range(91,99)],'camera':[1,-.4,.75],'title':'Banco — proposta para retirada da folha','note':'Três setores fechados e cobertos pela almofada do último; tampa4 em90, folha inteira recuada24 mm e elevada970. Mesa com pedestal preservada. Rotina nova proposta, sem validação de pessoa/pega/instalação na mesa.'}
}
def doc():
 return next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==work)
def prepare():
 assert not work.exists(),'Base visual existente; não recriar'
 shutil.copy2(source,work);d=App.openDocument(str(work));App.setActiveDocument(d.Name);d.Label='Vistas ilustrativas da R21 — não é revisão executiva'
 values=[]
 for r in catalog['catalog']:
  o=d.getObject(r['control'])
  for prop in ['Abertura','Extensao','Deslocamento','ElevarAlmofada','DeslocamentoAlmofada','EndireitarSaco','RetiradaSaco','RetiradaConjunto','RetiradaPainelSuperior']:
   if prop in o.PropertiesList:values.append([o.Name,prop,float(getattr(o,prop))])
 leaf=d.getObject(banco['leaf'])
 snapshot={'values':values,'sheet':[d.getObject('ControleSimplesR04').getContents(c) for c in ['B2','B3']],'leaf_matrix':list(leaf.Placement.Matrix.A),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'source':str(source),'work':str(work),'scenes':scenes}
 ((Path(__file__).resolve().parent / 'Configuracao_vistas_R21.json').resolve()).write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8')
 return {'working_document':d.Name,'source_unchanged':True,'scenes':list(scenes)}
def activate(name):
 d=doc();App.setActiveDocument(d.Name);snapshot=json.loads(((Path(__file__).resolve().parent / 'Configuracao_vistas_R21.json').resolve()).read_text(encoding='utf-8'))
 for n,p,v in snapshot['values']:setattr(d.getObject(n),p,v)
 for cell,value in zip(['B2','B3'],snapshot['sheet']):d.getObject('ControleSimplesR04').set(cell,value)
 mm=App.Matrix(*snapshot['leaf_matrix']);d.getObject(banco['leaf']).Placement=App.Placement(mm)
 wanted=set(scenes[name]['sources'])
 for r in mapping:d.getObject(r['link']).Visibility=r['source_roots'][0] in wanted
 if name in ['Escritorio','Cabeceira_canto']:
  mn='Modulo016' if name=='Escritorio' else 'Modulo003'
  for r in r18['doors']:
   if r['module']==mn:d.getObject(r['control']).Abertura=60
  if name=='Cabeceira_canto':
   for cell in ['B2','B3']:d.getObject('ControleSimplesR04').set(cell,'60 deg')
 elif name=='Cozinha':
  for r in r10['doors']:
   if r['module']!='Modulo014':d.getObject(r['control']).Abertura=60
 elif name=='Gavetas_cozinha':d.getObject('Gaveta005').Extensao=300;d.getObject('Gaveta007').Extensao=530
 elif name=='Banheiro':
  for r in r12['doors']:d.getObject(r['control']).Abertura=60
  d.getObject('PortaEntradaBanheiroR12').Abertura=0;d.getObject('Peca075').ViewObject.Transparency=85
 elif name=='Cesto':
  c=d.getObject('ControleCestoR15');c.Abertura=55;c.RetiradaSaco=445;c.EndireitarSaco=55
 elif name=='Banco_diario':
  for n,shift in [('ControleBancoR001',711),('ControleBancoR002',733)]:
   c=d.getObject(n);c.Abertura=90;c.ElevarAlmofada=50;c.DeslocamentoAlmofada=shift
 elif name=='Banco_folha':
  c=d.getObject('ControleBancoR003');c.Abertura=90;c.ElevarAlmofada=50;c.DeslocamentoAlmofada=873
  leaf=d.getObject(banco['leaf']);p=leaf.Placement;p.Base.y+=24;p.Base.z=970;leaf.Placement=p
 d.recompute();Gui.updateGui();v=Gui.getDocument(d.Name).activeView();v.setCameraType('Orthographic')
 rot=App.Rotation(App.Vector(1,0,0),App.Vector(0,0,1),App.Vector(*scenes[name]['camera']),'ZYX');v.setCameraOrientation(rot.Q);v.fitAll();Gui.updateGui()
 return {'scene':name,'source_roots':len(wanted),'controls':'illustrative poses only','title':scenes[name]['title']}
def frame():
 d=doc();v=Gui.getDocument(d.Name).activeView();v.fitAll();Gui.updateGui()
 return {'frame_updated':True}
def capture(name):
 d=doc();v=Gui.getDocument(d.Name).activeView();p=root/(name+'_R22.png');v.saveImage(str(p),1600,1000,'White')
 return str(p)
def finish():
 snapshot=json.loads(((Path(__file__).resolve().parent / 'Configuracao_vistas_R21.json').resolve()).read_text(encoding='utf-8'))
 assert hashlib.sha256(source.read_bytes()).hexdigest()==snapshot['source_sha256']
 assert hashlib.sha256(work.read_bytes()).hexdigest()==snapshot['source_sha256'],'Base visual foi salva/alterada'
 d=doc();App.closeDocument(d.Name)
 target=(Path(__file__).resolve().parent / '../Visibilidade_R22_2026-10-14/Guedala_Park_R22_Visibilidade_Atual.FCStd').resolve()
 current=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==target);App.setActiveDocument(current.Name)
 return {'source_unchanged':True,'active_current_document':current.Name,'working_document_closed_without_save':True}
