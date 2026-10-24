import pathlib,zipfile,xml.etree.ElementTree as E,copy,json,hashlib
import FreeCAD as A
root=pathlib.Path(__file__).resolve().parent;base=root.parents[1]
src=base/'Modelo_FreeCAD/01_Atual/Cesto_R41_2026-10-20/Guedala_Park_R41_Estudo_Frente500.FCStd'
dest=base/'Modelo_FreeCAD/01_Atual/Consolidacao_R42_2026-10-22';dest.mkdir(exist_ok=True)
out=dest/'Guedala_Park_R42_Consolidado.FCStd'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source_hash=sha(src)
with zipfile.ZipFile(src) as z:files={n:z.read(n) for n in z.namelist()}
original=E.fromstring(files['Document.xml']);doc=copy.deepcopy(original);gui=E.fromstring(files['GuiDocument.xml'])
objects=doc.find('Objects');data=doc.find('ObjectData');vps=gui.find('ViewProviderData');removed={'Peca108','Peca109'}
def count(e):
 if e.tag=='Objects':e.set('Count',str(sum(x.tag=='Object' for x in e)))
 elif e.tag=='Properties':e.set('Count',str(sum(x.tag=='Property' for x in e)))
 elif 'Count' in e.attrib:e.set('Count',str(len(e)))
 elif 'count' in e.attrib:e.set('count',str(len(e)))
for parent in [objects,data,vps]:
 for item in list(parent):
  if item.get('name',item.get('Name')) in removed:parent.remove(item)
for parent in doc.iter():
 for child in list(parent):
  if child.tag in ['Link','Dep'] and child.get('value',child.get('Name')) in removed:parent.remove(child);count(parent)
oldhidden={'Peca091','Peca092','Peca093','Peca094','Peca095','CadeiraLinaR30_1','CadeiraLinaR30_2','CadeiraLinaR30_3'}
oldhidden.update(o.get('name') for o in data if o.get('name','').startswith(('Lina1_','Lina2_','Lina3_')))
def visibility(node,state):
 p=node.find("Properties/Property[@name='Visibility']/Bool")
 if p is not None:p.set('value','true' if state else 'false')
for o in data:
 if o.get('name') in oldhidden:visibility(o,False)
for o in vps:
 if o.get('name') in oldhidden:visibility(o,False)
with zipfile.ZipFile(root/'Berlin_estudo_dimensional.FCStd') as z:studyfiles={n:z.read(n) for n in z.namelist()}
study=E.fromstring(studyfiles['Document.xml']);sd=study.find('ObjectData')
selected={o.get('name') for o in sd if o.get('name','').startswith(('Fechada_','Aberta_'))}
nextid=max(int(o.get('id','0')) for o in objects)+1
template=next(o for o in sd if o.get('name')=='LeiaMe')
def add_group(name,label,props,children=()):
 global nextid
 item=copy.deepcopy(template);item.set('name',name);ps=item.find('Properties')
 ps.find("Property[@name='Label']/String").set('value',label)
 ps.remove(ps.find("Property[@name='Premissas']"))
 links=ps.find("Property[@name='Group']/LinkList")
 for c in list(links):links.remove(c)
 for c in children:E.SubElement(links,'Link',value=c)
 count(links)
 for k,v in props.items():
  prop=E.SubElement(ps,'Property',name=k,type='App::PropertyString',group='R42 - candidatura',doc='',attr='0',ro='0',hide='0',status='2097152');E.SubElement(prop,'String',value=str(v))
 count(ps);data.append(item);E.SubElement(objects,'Object',type='App::DocumentObjectGroup',name=name,id=str(nextid));nextid+=1
 return item
newnodes=[]
for descriptor in study.find('Objects'):
 if descriptor.tag=='Object' and descriptor.get('name') in selected:
  d=copy.deepcopy(descriptor);d.set('id',str(nextid));nextid+=1;objects.append(d)
for item in sd:
 if item.get('name') not in selected:continue
 item=copy.deepcopy(item);name=item.get('name');visibility(item,name.startswith('Fechada_'))
 for node in item.iter():
  if 'file' in node.attrib and node.get('file') in studyfiles:
   old=node.get('file');new='R42_'+old;files[new]=studyfiles[old];node.set('file',new)
 if name=='Aberta_170':item.find("Properties/Property[@name='Label']/String").set('value','Berlin aberta 170 - COLISAO cadeira/sofa 6 cm - estudo')
 if name=='Aberta_cadeira_lateral':item.find("Properties/Property[@name='Label']/String").set('value','Berlin aberta - TRES cadeiras na lateral - conferir fisicamente')
 data.append(item);newnodes.append(item)
plan=json.loads((root.parent/'Ferragens/Plano_R42_objetos.json').read_text(encoding='utf-8'))
candidate_names=[]
for row in plan['preservacao_armazenamento']:
 n='FGVTN_R42_'+row['Objeto'];candidate_names.append(n);short=row['Profundidade_minima_preservar']==359
 p={'ObjetoReferencia':row['Objeto'],'FabricanteCandidato':'FGVTN','ProdutoCandidato':'One Touch 3D 400 mm' if short else 'One Touch 3D 500 mm','Curso_mm':375 if short else 475,'CaixaProfundidadeCandidata_mm':400 if short else 500,'ProfundidadeLivreMinima_mm':420 if short else 520,'CargaNominalCatalogo_kg':35,'BaseAtual_mm':str(row['Largura_minima_preservar'])+' x '+str(row['Profundidade_minima_preservar']),'BaseCandidata_mm':str(row['Largura_candidata'])+' x '+str(row['Profundidade_candidata']),'Status':'CANDIDATA PARA ORCAMENTO. Caixas e solidos Blum originais mantidos como REFERENCIA, nao convertidos. Sem perda de armazenamento autorizada. Faltam vao livre, furos, engates, curso, colisao e gabarito H do lote.'}
 p['SKU']='54FGOC12400TSX0' if short else '54FGOC12500TSX0'
 newnodes.append(add_group(n,'FGVTN candidata - '+row['Objeto'],p))
newnodes.append(add_group('FGVTN_R42_Dobradicas','FGVTN candidata - 46 dobradicas comuns',{'Quantidade':46,'Codigo':'51MS15XTN2200BF','Produto':'TN MS Slow reta + calco H0','MapaObjetos':json.dumps(plan['hinges46'],ensure_ascii=False),'PreservarOutras10':json.dumps(plan['preserve10'],ensure_ascii=False),'Status':'CANDIDATA PARA ORCAMENTO. Geometria Blum mantida como referencia; nao e produto FGVTN. Validar K, recobrimento, calco, furacao, quantidade e carga. Sem modificacao mecanica aplicada.'}))
newnodes.append(add_group('FGVTN_R42','FGVTN - candidatas 9 gavetas e 46 dobradicas',{'Status':'Alternativa comercial/de montagem pendente. Nao fabricavel. Referencias Blum permanecem para comparacao; nao comprar ambas. Banco, cesto, canto e espelheiro preservados.'},candidate_names+['FGVTN_R42_Dobradicas']))
newnodes.append(add_group('ConsolidacaoR42','R42 - LEIA PRIMEIRO',{'Escopo':'Apoios Peca108/Peca109 removidos. Berlin fechada ativa e 2 estudos abertos. FGVTN candidata declarativa. R41 historica preservada.','BerlinPremissas':'Tampo superficie a790mm; espessura/estrutura/vao inferior desconhecidos. Centro875/4650. Sapata hipotetica330x500, orientacao nao confirmada. Cadeiras gabarito Lina44x47x94, insercao26cm/projecao21cm hipoteticas.','BerlinAberta':'Manter2pontas colide com sofa6cm. Grupo aberto tres laterais conforme pedido: centros56,67cm; intervalos12,67cm; margens6,33cm. Fechada visivel; abrir somente um cenario por vez.','Limites':'Medidas do modelo, nao campo. Sem compra/fabricacao autorizada. Original mesa/cadeiras ocultas para referencia historica.'}))
# Copy suitable original view providers for new objects, preserving original appearance of all retained objects.
groupvp=next(v for v in vps if v.get('name')=='Documentacao');shapevp=next(v for v in vps if v.get('name')=='CadeiraLinaR30_1')
for node in newnodes:
 name=node.get('name');hasShape=node.find("Properties/Property[@name='Shape']") is not None
 vp=copy.deepcopy(shapevp if hasShape else groupvp);vp.set('name',name);visibility(vp,not name.startswith('Aberta_'));vps.append(vp)
for node in [objects,data,vps]:count(node)
files['Document.xml']=E.tostring(doc,encoding='utf-8',xml_declaration=True);files['GuiDocument.xml']=E.tostring(gui,encoding='utf-8',xml_declaration=True)
files.pop('thumbnails/Thumbnail.png',None)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n,v in files.items():z.writestr(n,v)
print('SALVO',out,flush=True)
d=A.openDocument(str(out));print('ABERTO',len(d.Objects),flush=True)
assert all(d.getObject(n) is None for n in removed)
assert all(d.getObject(n) is not None for n in selected|set(candidate_names)|{'FGVTN_R42_Dobradicas'})
invalid=[n for n in selected if hasattr(d.getObject(n),'Shape') and not d.getObject(n).Shape.isNull() and not d.getObject(n).Shape.isValid()]
assert not invalid
with zipfile.ZipFile(src) as z:
 shapes=[n for n in z.namelist() if n.lower().endswith(('.brp','.brep'))]
 changed=[n for n in shapes if files.get(n)!=z.read(n)]
assert not changed and sha(src)==source_hash
report={'arquivo':str(out),'objetos':len(d.Objects),'removidos':sorted(removed),'ocultados_historicos':sorted(oldhidden),'objetos_Berlin_adicionados':sorted(selected),'candidatas_gavetas':candidate_names,'dobradicas_candidatas':46,'formas_Berlin_invalidas':invalid,'geometrias_originais_BREP_preservadas_byte_a_byte':len(shapes),'geometrias_originais_BREP_alteradas':changed,'sha256_R41':source_hash,'sha256_R42':sha(out),'R41_inalterada':True,'validacao':'Reaberto no FreeCAD1.1.4. Formas novas validas. BREP originais identicos. Sem validacao mecanica FGVTN/altura livre Berlin/medida fisica.'}
(dest/'Verificacao_R42.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False),flush=True)
