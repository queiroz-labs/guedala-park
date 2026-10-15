from pathlib import Path
import json,shutil,hashlib
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
src=(Path(__file__).resolve().parent / '../Apartamento_espelhado_R20_2026-10-14/Guedala_Park_R20_Apartamento_Espelhado.FCStd').resolve()
dst=(Path(__file__).resolve().parent / 'Guedala_Park_R21_Controles_Organizados.FCStd').resolve()
source_hash=hashlib.sha256(src.read_bytes()).hexdigest()
if dst.exists():assert hashlib.sha256(dst.read_bytes()).hexdigest()==source_hash,'Revisão existente modificada; não reconstruir'
else:shutil.copy2(src,dst)
d=App.openDocument(str(dst));App.setActiveDocument(d.Name);d.Label='Guedala Park — R21 — espelhado / controles por ambiente'
parents={o.Name:(o.getParentGeoFeatureGroup().Name if o.getParentGeoFeatureGroup() else None) for o in d.Objects}
placements={o.Name:list(o.Placement.Matrix.A) for o in d.Objects if 'Placement' in o.PropertiesList}
expressions={o.Name:[list(v) for v in o.ExpressionEngine] for o in d.Objects if 'ExpressionEngine' in o.PropertiesList}
paramtypes={(o.Name,p):o.getTypeIdOfProperty(p) for o in d.Objects for p in ['PlanilhaDimensoes','FonteControle'] if p in o.PropertiesList}
index=d.addObject('App::DocumentObjectGroup','ControlesAtuaisR21');index.Label='01 — CONTROLES ATUAIS — abrir / retirar'
index.addProperty('App::PropertyString','ComoUsar','Guia');index.ComoUsar='Escolher o ambiente, selecionar o controle e editar Abertura (graus) ou Extensao/Deslocamento (mm). Giro e translação são estudos geométricos; não batentes ou intertravamentos físicos.'
groups={}
for key,label in [('quarto','Quarto — cabeceira, canto, roupeiro'),('escritorio','Escritório — portas e gavetas'),('cozinha','Cozinha — portas e gavetas'),('lavanderia','Lavanderia — aéreo e cesto'),('banheiro','Banheiro — portas e entrada'),('banco','Sala — banco e almofadas')]:
 g=d.addObject('App::DocumentObjectGroup','ControlesAmbienteR21');g.Label=label;index.addObject(g);groups[key]=g
catalog=[]
def add(key,name,fields,note):
 o=d.getObject(name);assert o is not None,name;previous=o.getParentGeoFeatureGroup()
 shortcut=None
 if previous is None:groups[key].addObject(o)
 else:
  # Do not put a geometric child into another group: that removes its module parent.
  shortcut=d.addObject('App::Link','AcessoControleR21');shortcut.setLink(o);shortcut.LinkTransform=True;shortcut.Visibility=False
  shortcut.Label=o.Label+' — acesso ao objeto '+name;groups[key].addObject(shortcut)
  shortcut.addProperty('App::PropertyString','ComoEditar','Guia');shortcut.ComoEditar='Selecionar o objeto vinculado '+name+' e editar '+', '.join(fields)+'. Este vínculo é somente um acesso; não editar Placement.'
 assert o.getParentGeoFeatureGroup()==previous,(name,'Pai geométrico alterado')
 catalog.append({'room':key,'control':name,'shortcut':shortcut.Name if shortcut else None,'label':o.Label,'fields':fields,'note':note})
for folder in ['Dobradicas_R10_2026-10-14','Banheiro_R12_2026-10-14','Portas_opostas_R18_2026-10-14']:
 fn={'Dobradicas_R10_2026-10-14':'Montagem_R10.json','Banheiro_R12_2026-10-14':'Montagem_R12.json','Portas_opostas_R18_2026-10-14':'Montagem_R18.json'}[folder]
 for r in json.loads((base/'02_Revisoes_e_estudos'/folder/fn).read_text(encoding='utf-8'))['doors']:
  key='banheiro' if folder.startswith('Banheiro') else ('escritorio' if r['module']=='Modulo016' else 'quarto') if folder.startswith('Portas_opostas') else ('lavanderia' if r['module']=='Modulo014' else 'cozinha')
  add(key,r['control'],{'Abertura':'0–86 graus de estudo'},'Sentido do rótulo é o apartamento espelhado. CursoEstudo não comprova o limitador mecânico.')
add('quarto','ControleSimplesR04',{'B2':'Porta A:0–86 graus','B3':'Porta B:0–86 graus'},'Editar somente B2/B3; canto simples vigente. A abre para esquerda e B para direita na própria vista frontal espelhada.')
d.getObject('ControleSimplesR04').set('A2','Porta A — esquerda no apartamento espelhado — graus')
d.getObject('ControleSimplesR04').set('A3','Porta B — direita no apartamento espelhado — graus')
for r in json.loads(((Path(__file__).resolve().parent / '../Correr_R14_2026-10-14/Montagem_R14.json').resolve()).read_text(encoding='utf-8'))['rows']:
 for i,n in enumerate(r['controls']):
  o=d.getObject(n);o.Label=('Roupeiro' if r['module']=='Modulo' else 'Maleiro')+f' — folha de base{i+1} — correr em sentido oposto à vizinha'
  add('quarto',n,{'Deslocamento':f"0–{r['course']} mm de estudo"},'Valor positivo nos dois controles; drivers têm sinais opostos. Reservas de ferragens, não sistema homologado.')
for i in range(10):
 n='Gaveta'+('%03d'%i if i else '');o=d.getObject(n)
 key='quarto' if i<4 else 'escritorio' if i>7 else 'cozinha'
 if i==7:
  o.Label='Gaveta baixa — rodas de silicone / cabos fixos'
  o.Ferragem='Rodas de silicone a confirmar; rodízios-gabarito R13. Sem MOVENTO ou NL de corrediça. Carga, guias, batente, piso e estrutura independente pendentes.'
  note='400 herdado é posição de estudo;530 é retirada completa ilustrativa, não batente. Peças/piso/carga reais pendentes.'
 else:note='Translação rígida de caixa; guia MOVENTO estática, não animação telescópica ou carga certificada.'
 add(key,n,{'Extensao':'0–530 mm de estudo' if i==7 else f'0–{int(o.CursoNominal.Value)} mm de estudo'},note)
add('lavanderia','ControleCestoR15',{'Abertura':'0–55 graus','RetiradaSaco':'0–445 mm','EndireitarSaco':'0–55 graus','RetiradaPainelSuperior':'manutenção','RetiradaConjunto':'manutenção condicionada'},'Uso diário: abrir55, retirar saco445, endireitar55. Retirada completa da armação bate na Loop20L em300/400; retirar temporariamente a lixeira é proposta ainda sem endereço/manuseio comprovados. Não usar essa retirada como percurso livre.')
d.getObject('ControleCestoR15').Sequencia=catalog[-1]['note']+' Controles independentes, sem intertravamento físico ou de software; ferragem/retenções/carga reais pendentes.'
add('banheiro','PortaEntradaBanheiroR12',{'Abertura':'0 fechado /90 original aberto'},'Fechar entrada ideal antes de abrir gabinete inferior. Folha700/eixo/maçaneta não medidos; usuário não possui novas medidas.')
for r in json.loads(((Path(__file__).resolve().parent / '../Banco_R16_2026-10-14/Montagem_R16.json').resolve()).read_text(encoding='utf-8'))['lids']:
 o=d.getObject(r['control']);fields={'Abertura':'0–90 graus de estudo'}
 if r['separate_cushion']:fields.update(ElevarAlmofada='mm; seguir Sequencia',DeslocamentoAlmofada='mm; seguir Sequencia')
 add('banco',o.Name,fields,str(o.Sequencia) if 'Sequencia' in o.PropertiesList else 'Primeiro assento integral por eixo ideal; fixação da almofada/retenção/carga pendentes.')
d.getObject('ControlesPortasR18').Label='Histórico de organização R18 — usar CONTROLES ATUAIS'
d.getObject('ApartamentoEspelhadoR20').Label='02 — APARTAMENTO ATUAL — espelhado'
# Adding membership to non-geometric groups must not move or rewire any source.
d.recompute()
assert all((d.getObject(n).getParentGeoFeatureGroup().Name if d.getObject(n).getParentGeoFeatureGroup() else None)==p for n,p in parents.items())
assert all(max(abs(x-y) for x,y in zip(values,d.getObject(n).Placement.Matrix.A))<1e-9 for n,values in placements.items())
assert all([list(v) for v in d.getObject(n).ExpressionEngine]==e for n,e in expressions.items())
assert all(d.getObject(n).getTypeIdOfProperty(p)==t for (n,p),t in paramtypes.items())
assert hashlib.sha256(src.read_bytes()).hexdigest()==source_hash
invalid=[o.Name for o in d.Objects if 'Invalid' in o.State];assert not invalid
Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();Gui.updateGui();d.save()
report={'file':str(dst),'source':str(src),'source_sha256':source_hash,'index':index.Name,'groups':{k:g.Name for k,g in groups.items()},'catalog':catalog,'geo_parents_unchanged':True,'placements_unchanged':True,'expression_engines_unchanged':True,'parameter_types_unchanged':True,'invalid':invalid,'scope':'Navigation groups, labels and guidance only; no geometry, movement, parameter formulas or fittings changed.'}
((Path(__file__).resolve().parent / 'Controles_R21.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result={k:v for k,v in report.items() if k not in ['catalog','groups']};result['control_count']=len(catalog)
