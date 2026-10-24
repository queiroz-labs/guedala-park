import pathlib,zipfile,xml.etree.ElementTree as E,json,hashlib,shutil
import FreeCAD as A
root=pathlib.Path(__file__).resolve().parent;base=root.parents[1]
p=base/'Modelo_FreeCAD/01_Atual/Consolidacao_R42_2026-10-22/Guedala_Park_R42_Consolidado.FCStd'
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
before=sha(p);backup=root/'Guedala_Park_R42_antes_auditoria.FCStd'
if not backup.exists():shutil.copy2(p,backup)
before=sha(backup)
with zipfile.ZipFile(backup) as z:f={n:z.read(n) for n in z.namelist()}
d=E.fromstring(f['Document.xml']);g=E.fromstring(f['GuiDocument.xml']);objects={o.get('name'):o for o in d.find('ObjectData')};changes=[]
for name,o in objects.items():
 if name.startswith('FGVTN_R42_Gaveta'):
  sku=o.find("Properties/Property[@name='SKU']/String").get('value')
  assert sku in ['54FGOC12400TSX0','54FGOC12500TSX0']
  node=o.find("Properties/Property[@name='ProdutoCandidato']/String")
  old=node.get('value');node.set('value','Corredica FGVTN Oculta Slowmotion ET 35 kg '+('400 mm' if sku=='54FGOC12400TSX0' else '500 mm'))
  changes.append({'objeto':name,'propriedade':'ProdutoCandidato','antes':old,'depois':node.get('value')})
for name in ['Peca096','Peca097','Peca098','BancoFolhaR31']:
 for tree,path in [(d,"ObjectData/Object"),(g,"ViewProviderData/ViewProvider")]:
  node=tree.find(path+"[@name='%s']/Properties/Property[@name='Visibility']/Bool"%name);assert node is not None;node.set('value','false')
 changes.append({'objeto':name,'alteracao':'Visibility App e GUI false; geometria preservada'})
objects['BancoFolhaR31'].find("Properties/Property[@name='Label']/String").set('value','HISTORICO folha mesa sob medida 300x750 - NAO Berlin')
controls={'ControleMesaR35':'VaoCentral','TransferenciaMesaR37':'Progresso'}
dependencies=[]
for name,o in objects.items():
 for expression in o.findall("Properties/Property[@name='ExpressionEngine']/ExpressionEngine/Expression"):
  if any(c in expression.get('expression','') for c in controls):dependencies.append({'objeto':name,**expression.attrib})
for name,inputprop in controls.items():
 ps=objects[name].find('Properties');label=ps.find("Property[@name='Label']/String")
 label.set('value','HISTORICO mesa sob medida - '+label.get('value'))
 prop=ps.find("Property[@name='%s']"%inputprop)
 assert float(prop.find('Float').get('value'))==0
 prop.set('ro','1');prop.set('attr',str(int(prop.get('attr','0'))|1));prop.set('status',str(int(prop.get('status','0'))|4))
 q=E.SubElement(ps,'Property',name='StatusR42',type='App::PropertyString',group='Historico',doc='',attr='0',ro='0',hide='0',status='2097152')
 E.SubElement(q,'String',value='HISTORICO da mesa sob medida150/180cm. NAO controla Berlin110/170. Entrada mantida em0 e somente leitura para evitar acionamento acidental. Expressoes antigas preservadas para rastreabilidade; controles manuais do banco nao alterados.')
 ps.set('Count',str(sum(x.tag=='Property' for x in ps)))
 changes.append({'objeto':name,'alteracao':'Rotulo historico; '+inputprop+' somente leitura em0; expressoes preservadas'})
f['Document.xml']=E.tostring(d,encoding='utf-8',xml_declaration=True);f['GuiDocument.xml']=E.tostring(g,encoding='utf-8',xml_declaration=True)
temp=p.with_suffix('.audit.tmp')
with zipfile.ZipFile(temp,'w',zipfile.ZIP_DEFLATED) as z:
 for n,v in f.items():z.writestr(n,v)
temp.replace(p)
c=A.openDocument(str(p));assert len(c.Objects)==5526
for name in ['Peca096','Peca097','Peca098','BancoFolhaR31']:assert not c.getObject(name).Visibility
for name,ip in controls.items():assert 'ReadOnly' in c.getObject(name).getEditorMode(ip),(name,c.getObject(name).getEditorMode(ip))
for name,o in objects.items():
 if name.startswith('FGVTN_R42_Gaveta'):assert 'One Touch' not in c.getObject(name).ProdutoCandidato
with zipfile.ZipFile(backup) as z:
 breps=[n for n in z.namelist() if n.lower().endswith(('.brp','.brep'))]
 assert all(f[n]==z.read(n) for n in breps)
report={'backup':str(backup),'sha256_antes':before,'sha256_depois':sha(p),'alteracoes':changes,'dependencias_controles_historicos':dependencies,'breps_totais_identicos':len(breps),'objeto_total':len(c.Objects),'reabertura':'OK','controles_entrada_somente_leitura':'confirmados getEditorMode==1','limite':'Expressoes historicas preservadas; scripts podem alterar propriedades diretamente. Nao sao controles Berlin. Exclusividade de cenarios Berlin e manual, conforme LEIA-ME.'}
(root/'Correcoes_CAD_R42.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
vp=p.parent/'Verificacao_R42.json';r=json.loads(vp.read_text(encoding='utf-8'));r['sha256_R42']=sha(p);r['auditoria_correcao']=str(root/'Correcoes_CAD_R42.json');r['correcao_reabertura']='OK';vp.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True),flush=True)
