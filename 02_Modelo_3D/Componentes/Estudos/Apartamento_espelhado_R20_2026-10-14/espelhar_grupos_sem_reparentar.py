from pathlib import Path
import json,shutil,hashlib,re
import FreeCAD as App,FreeCADGui as Gui
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
src=(Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Guedala_Park_R18_Portas_Opostas.FCStd').resolve();dst=(Path(__file__).resolve().parent / 'Guedala_Park_R20_Apartamento_Espelhado.FCStd').resolve()
assert not dst.exists(),'Revisão existente; não reconstruir'
prev=next(x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==src)
assert prev.isSaved() and src.stat().st_size>100000
source_hash=hashlib.sha256(src.read_bytes()).hexdigest()
# Only close our unsaved, unsuccessful R19 construction. Its on-disk copy and all originals remain.
old_path=(Path(__file__).resolve().parent / '../Apartamento_espelhado_R19_2026-10-14/Guedala_Park_R19_Apartamento_Espelhado.FCStd').resolve()
old=next((x for x in App.listDocuments().values() if x.FileName and Path(x.FileName).resolve()==old_path),None)
if old:
 assert hashlib.sha256(old_path.read_bytes()).hexdigest()==source_hash,'R19 foi salva/alterada; preservar documento aberto'
 App.closeDocument(old.Name)
shutil.copy2(src,dst);d=App.openDocument(str(dst));App.setActiveDocument(d.Name)
d.Label='Guedala Park - R20 - espelhado; cozinha à esquerda ao entrar'
def prop(o,n,v):
 if n not in o.PropertiesList:o.addProperty('App::PropertyString',n,'Orientação R20')
 setattr(o,n,v)
def roots(doc):return [o for o in doc.Objects if (o.TypeId=='App::Part' or 'Shape' in o.PropertiesList) and not o.getParentGeoFeatureGroup()]
original_roots=roots(d);original_matrices={o.Name:list(o.getGlobalPlacement().Matrix.A) for o in original_roots}
parameter_types={(o.Name,n):o.getTypeIdOfProperty(n) for o in d.Objects for n in ['PlanilhaDimensoes','FonteControle'] if n in o.PropertiesList}
original_visibility={o.Name:o.Visibility for o in d.Objects if 'Visibility' in o.PropertiesList}
source_groups=[o for o in d.Objects if o.TypeId=='App::DocumentObjectGroup' and (o.Name.startswith('Ambiente_') or o.Name in ['ParedesInteiras','ParedesCortadas','ReferenciasFerragens'])]
# Prepare whole-house visibility. Keep boolean operands/history hidden and expose current corner.
for g in source_groups:
 if g.Name.startswith('Ambiente_') or g.Name=='ParedesCortadas':g.Visibility=True
for o in d.Objects:
 if o.getParentGeoFeatureGroup() and o.Name in original_visibility:o.Visibility=original_visibility[o.Name]
for i in range(20):d.getObject('Modulo'+('%03d'%i if i else '')).Visibility=True
for o in d.Objects:
 if o.Name.startswith(('FrenteSimples','FerragemSimples','ApoioPortaB','FaixaQuina')) or o.Name in ['PlacaL','PlacaL001','Peca255','Peca256','LateralApoioPrincipal']:
  o.Visibility=True;parent=o.getParentGeoFeatureGroup()
  while parent:parent.Visibility=True;parent=parent.getParentGeoFeatureGroup()
for o in d.Objects:
 if o.Name.startswith('Historico'):o.Visibility=False
collection=d.addObject('App::DocumentObjectGroup','ApartamentoEspelhadoR20');collection.Label='APARTAMENTO ATUAL - espelhado; cozinha à esquerda da entrada'
prop(collection,'Orientacao','Composição nativa de vínculos dos grupos existentes: Xnovo=7400−Xbase, Y/Z preservados. Estrutura/parentes/vínculos de parâmetros originais não alterados.')
prop(collection,'Uso','Editar controles atuais nesta árvore; a composição espelhada acompanha as mudanças. Geometria de base/fontesSTEP preservadas. Cotas/ferragens propostas, sem corte/furação/compra.')
mapping=[];covered=set()
for g in source_groups:
 link=d.addObject('App::Link','EspelhoAmbienteR20');collection.addObject(link);link.setLink(g)
 link.ScaleVector=App.Vector(-1,1,1);link.Placement.Base=App.Vector(7400,0,0);link.Label=g.Label+' - espelhado'
 link.Visibility=g.Name.startswith('Ambiente_') or g.Name=='ParedesCortadas'
 members=[o.Name for o in original_roots if g in o.InList];covered.update(members)
 mapping.append({'link':link.Name,'source_group':g.Name,'source_roots':members,'visible':link.Visibility})
for o in original_roots:
 if o.Name not in covered:
  link=d.addObject('App::Link','EspelhoVolumeR20');collection.addObject(link);link.setLink(o);link.ScaleVector=App.Vector(-1,1,1);link.Placement.Base=App.Vector(7400,0,0);link.Label=o.Label+' - espelhado';link.Visibility=o.Visibility
  mapping.append({'link':link.Name,'source_group':None,'source_roots':[o.Name],'visible':link.Visibility});covered.add(o.Name)
assert covered==set(o.Name for o in original_roots)
for g in source_groups:g.Visibility=False
for r in mapping:
 if r['source_group'] is None:d.getObject(r['source_roots'][0]).Visibility=False
r18=json.loads(((Path(__file__).resolve().parent / '../Portas_opostas_R18_2026-10-14/Montagem_R18.json').resolve()).read_text(encoding='utf-8'));door_map=[]
for mn,title in [('Modulo016','Escritório'),('Modulo003','Cabeceira')]:
 for i,r in enumerate(reversed([r for r in r18['doors'] if r['module']==mn]),1):
  side='left' if r['side']=='right' else 'right';label='esquerda' if side=='left' else 'direita';c=d.getObject(r['control']);c.Label=title+' porta'+str(i)+' - abrir para '+label
  prop(c,'SentidoApartamentoR20',label+' na orientação espelhada');door_map.append(dict(r,visual_number=i,side_source=r['side'],side_apartment=side))
for folder,fn in [('Dobradicas_R10_2026-10-14','Montagem_R10.json'),('Banheiro_R12_2026-10-14','Montagem_R12.json')]:
 for r in json.loads((base/'02_Revisoes_e_estudos'/folder/fn).read_text(encoding='utf-8'))['doors']:
  side='left' if r['side']=='right' else 'right';label='esquerda' if side=='left' else 'direita';c=d.getObject(r['control']);c.Label=d.getObject(r['module']).Label+' - porta '+label;prop(c,'SentidoApartamentoR20',label+' na orientação espelhada');door_map.append(dict(r,side_source=r['side'],side_apartment=side))
for o in d.Objects:
 if o.Name.startswith('ControleCorrer'):
  o.Label=re.sub('esquerda|direita',lambda m:'direita' if m.group()=='esquerda' else 'esquerda',o.Label)
prop(d.getObject('PortaIndependenteR04'),'SentidoApartamentoR20','Esquerda na própria vista frontal espelhada; cantoA')
prop(d.getObject('PortaIndependenteR001'),'SentidoApartamentoR20','Direita na própria vista frontal espelhada; cantoB')
d.recompute()
def box(s):
 b=s.optimalBoundingBox();return [b.XMin,b.YMin,b.ZMin,b.XLength,b.YLength,b.ZLength]
samples=[]
names=['Peca351','Peca140','Peca138',next(r['front'] for r in r18['doors'] if r['module']=='Modulo016'),'FrenteVizinhaR18']
for n in names:
 o=d.getObject(n);chain=[];q=o
 while q:chain.append(q.Name);q=q.getParentGeoFeatureGroup()
 row=next(r for r in mapping if chain[-1] in r['source_roots']);link=d.getObject(row['link']);path='.'.join(reversed(chain))+'.'
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();old=box(s);new=box(link.getSubObject(path));expected=[7400-old[0]-old[3],old[1],old[2],old[3],old[4],old[5]];err=max(abs(x-y) for x,y in zip(new,expected));assert err<1e-6,(n,new,expected)
 samples.append({'object':n,'link':link.Name,'path':path,'source_bbox':old,'mirrored_bbox':new,'max_error_mm':err})
assert all(o.getParentGeoFeatureGroup() is None for o in original_roots),'Geometria foi reparentada'
assert all(max(abs(x-y) for x,y in zip(original_matrices[o.Name],o.getGlobalPlacement().Matrix.A))<1e-7 for o in original_roots)
assert all(d.getObject(n).getTypeIdOfProperty(p)==t for (n,p),t in parameter_types.items()),'Tipo de vínculo alterado'
invalid=[o.Name for o in d.Objects if 'Invalid' in o.State];assert not invalid,str(invalid)
assert hashlib.sha256(src.read_bytes()).hexdigest()==source_hash
Gui.getDocument(d.Name).activeView().viewAxonometric();Gui.getDocument(d.Name).activeView().fitAll();Gui.updateGui();d.save()
report={'file':str(dst),'source':str(src),'source_sha256':source_hash,'reflection_constant_x_mm':7400,'mirror_plane_x_mm':3700,'collection':collection.Name,'source_root_count':len(original_roots),'mapping':mapping,'samples':samples,'door_map':door_map,'parameter_link_types_unchanged':True,'source_parents_unchanged':True,'source_world_matrices_unchanged':True,'invalid':invalid,'scope':'Composição nativa por vínculos aos grupos existentes, sem reparentar geometrias e sem converter propriedades de parâmetros. Controle e fontes no mesmo arquivo. Isometria preserva distâncias/dimensões dos gabaritos; não libera fabricação ou homologa ferragens.'}
((Path(__file__).resolve().parent / 'Espelhamento_R20.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');result={k:v for k,v in report.items() if k not in ['door_map','mapping']}
