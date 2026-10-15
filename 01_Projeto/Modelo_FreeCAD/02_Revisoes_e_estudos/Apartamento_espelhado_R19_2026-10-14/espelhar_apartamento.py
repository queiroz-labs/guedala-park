from pathlib import Path
import json,shutil,hashlib,re
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
src=(Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Guedala_Park_R18_Portas_Opostas.FCStd').resolve();dst=(Path(__file__).resolve().parent / 'Guedala_Park_R19_Apartamento_Espelhado.FCStd').resolve()
prev=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==src)
assert prev.isSaved() and src.stat().st_size>100000
source_hash=hashlib.sha256(src.read_bytes()).hexdigest()
if dst.exists():
 assert hashlib.sha256(dst.read_bytes()).hexdigest()==source_hash,'Revisão construída; não reconstruir'
 d=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==dst)
 assert d.getObject('FonteApartamentoR19') is None,'Construção parcial requer reparo específico'
else:
 shutil.copy2(src,dst);d=App.openDocument(str(dst))
App.setActiveDocument(d.Name)
d.Label='Guedala Park - R19 - apartamento espelhado; cozinha à esquerda ao entrar'
def prop(o,n,v):
 if n not in o.PropertiesList:o.addProperty('App::PropertyString',n,'Orientação R19')
 setattr(o,n,v)
def matrix(o):return list(o.getGlobalPlacement().Matrix.A)
def bb(s):
 b=s.optimalBoundingBox();return [b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength,b.ZLength]
original_roots=[o for o in d.Objects if (o.TypeId=='App::Part' or 'Shape' in o.PropertiesList) and not o.getParentGeoFeatureGroup()]
old_world={o.Name:matrix(o) for o in original_roots}
source=d.addObject('App::Part','FonteApartamentoR19');source.Label='Base paramétrica preservada - controles editáveis; orientação anterior'
prop(source,'Status','Base da composição espelhada no mesmo arquivo. Geometrias/fontesSTEP originais e expressões preservadas; não usar coordenadas desta base como implantação da unidade espelhada.')
groups={};mapping=[]
for o in original_roots:
 ng=[q for q in o.InList if q.TypeId=='App::DocumentObjectGroup']
 parent=next((q for q in ng if q.Name.startswith('Ambiente_')),ng[0] if ng else None)
 key=parent.Name if parent else 'Outros';title=parent.Label if parent else 'Outros volumes de referência'
 if key not in groups:
  g=d.addObject('App::Part','FonteAmbienteR19');source.addObject(g);g.Label=title+' - base paramétrica'
  if parent:g.Visibility=parent.Visibility
  groups[key]=g
 for q in ng:q.removeObject(o)
 groups[key].addObject(o);mapping.append({'object':o.Name,'room_part':groups[key].Name,'source_parent':key})
 # Removing a non-geometric group must not expose previously hidden reference material.
 if any(not q.Visibility for q in ng):o.Visibility=False
assert all(max(abs(x-y) for x,y in zip(old_world[o.Name],matrix(o)))<1e-7 for o in original_roots)
# Current corner and all current room modules are included even when hidden in a former detail view.
for i in range(20):
 m=d.getObject('Modulo'+('%03d'%i if i else ''));m.Visibility=True
for o in d.Objects:
 if o.Name.startswith(('FrenteSimples','FerragemSimples','ApoioPortaB','FaixaQuina')) or o.Name in ['PlacaL','PlacaL001','Peca255','Peca256','LateralApoioPrincipal']:
  o.Visibility=True
  parent=o.getParentGeoFeatureGroup()
  while parent and parent!=source:
   parent.Visibility=True;parent=parent.getParentGeoFeatureGroup()
for o in d.Objects:
 if o.Name.startswith('Historico'):o.Visibility=False
mirror=d.addObject('App::Link','ApartamentoEspelhadoR19');mirror.setLink(source)
mirror.Label='Apartamento atual - espelhado; cozinha à esquerda da entrada'
mirror.ScaleVector=App.Vector(-1,1,1);mirror.Placement.Base=App.Vector(7400,0,0)
prop(mirror,'Orientacao','Reflexão integral Xnovo=7400−Xbase; Y/Z preservados. PlanoX3700. Extremos das paredes−100/7500 mantidos; posição da cozinha invertida em relação à entrada. Transformação nativa, não câmera.')
prop(mirror,'Uso','Controles permanecem na árvore. Editar entradas atuais; o vínculo atualiza o apartamento espelhado. Base/orientação/fontes antigas preservadas no mesmo arquivo. Sem corte/furação/compra; pendências físicas e comerciais continuam.')
source.Visibility=False;mirror.Visibility=True
# Controls are labelled in the physical mirrored orientation, without changing their native equations.
r18=json.loads(((Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Montagem_R18.json').resolve()).read_text(encoding='utf-8'));door_map=[]
for mn,title in [('Modulo016','Escritório'),('Modulo003','Cabeceira')]:
 rr=[r for r in r18['doors'] if r['module']==mn]
 for i,r in enumerate(reversed(rr),1):
  side='left' if r['side']=='right' else 'right';label='esquerda' if side=='left' else 'direita';c=d.getObject(r['control']);c.Label=title+' porta'+str(i)+' - abrir para '+label
  prop(c,'SentidoApartamentoR19',label+' na orientação espelhada, vista de frente');prop(d.getObject(r['door']),'SentidoApartamentoR19',label)
  door_map.append({'module':mn,'visual_number':i,'door':r['door'],'control':r['control'],'side_source':r['side'],'side_apartment':side,'front':r['front']})
for folder in ['Dobradicas_R10_2026-10-14','Banheiro_R12_2026-10-14']:
 fn=base/'02_Revisoes_e_estudos'/folder/('Montagem_R10.json' if 'R10' in folder else 'Montagem_R12.json')
 a=json.loads(fn.read_text(encoding='utf-8'))
 for r in a['doors']:
  side='left' if r['side']=='right' else 'right';label='esquerda' if side=='left' else 'direita';c=d.getObject(r['control']);c.Label=d.getObject(r['module']).Label+' - porta '+label
  prop(c,'SentidoApartamentoR19',label+' na orientação espelhada');door_map.append({'module':r['module'],'door':r['door'],'control':r['control'],'side_source':r['side'],'side_apartment':side,'front':r['front']})
prop(d.getObject('PortaIndependenteR04'),'SentidoApartamentoR19','Esquerda na própria vista frontal espelhada; cantoA')
prop(d.getObject('PortaIndependenteR001'),'SentidoApartamentoR19','Direita na própria vista frontal espelhada; cantoB')
for o in d.Objects:
 if o.Name.startswith('ControleCorrer'):
  o.Label=re.sub('esquerda|direita',lambda m:'direita' if m.group()=='esquerda' else 'esquerda',o.Label)
  prop(o,'OrientacaoR19','Posição/sentido físico invertidos pela composição espelhada; entrada positiva conserva a expressão nativa.')
d.recompute()
# Check linked shapes in final coordinates. Native source shapes stay unchanged.
samples=[]
for n in ['Peca351','Peca140','Peca138','Modulo016','Modulo003']:
 item=next(x for x in mapping if x['object']==n);path=item['room_part']+'.'+n+'.'
 s=d.getObject(n).Shape.copy();s.Placement=d.getObject(n).getGlobalPlacement();old=bb(s)
 linked=mirror.getSubObject(path);new=bb(linked)
 expected=[7400-old[0]-old[3],old[1],old[2],old[3],old[4],old[5]]
 err=max(abs(x-y) for x,y in zip(new,expected));assert err<1e-6,(n,new,expected)
 samples.append({'object':n,'link_path':path,'source_bbox':old,'mirrored_bbox':new,'max_error_mm':err})
invalid=[o.Name for o in d.Objects if 'Invalid' in o.State];assert not invalid,str(invalid)
assert hashlib.sha256(src.read_bytes()).hexdigest()==source_hash
Gui.getDocument(d.Name).activeView().viewAxonometric();Gui.getDocument(d.Name).activeView().fitAll();Gui.updateGui()
d.save();assert d.isSaved() and dst.stat().st_size>100000
report={'file':str(dst),'source':str(src),'source_sha256':source_hash,'reflection_constant_x_mm':7400,'mirror_plane_x_mm':3700,'source_group':source.Name,'mirror_link':mirror.Name,'geometric_roots_packed':len(original_roots),'mapping':mapping,'linked_shape_checks':samples,'door_map':door_map,'invalid':invalid,'scope':'Composição integral nativa porApp::Link/ScaleVector(-1,1,1), fonte paramétrica preservada no mesmo arquivo. Distâncias/dimensões/encontros são preservados por isometria quando todas as geometrias seguem o mesmo vínculo. Montagens/ferragens continuam propostas; não homologação física de peças refletidas.'}
((Path(__file__).resolve().parent / 'Espelhamento_R19.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result={'file':str(dst),'roots':len(original_roots),'checks':samples,'invalid':invalid}
