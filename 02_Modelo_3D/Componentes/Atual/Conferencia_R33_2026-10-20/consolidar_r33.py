"""Consolida a auditoria completa na sessão FreeCAD já aberta; preserva a R32."""
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui,Part
import json,hashlib,csv,traceback
root=Path('C:/Users/Elias/Documents/PROJETOS/Guedala park')
folder=root/'guedala-park/02_Modelo_3D/Componentes/Atual/Conferencia_R33_2026-10-20'
folder.mkdir(exist_ok=True)
status=root/'tmp/status_r33.json'
try:
 report=json.loads((root/'tmp/auditoria_completa_r33.json').read_text(encoding='utf-8'))
 source=folder.parent/'Auditoria_R32_2026-10-20/Guedala_Park_R32_Auditoria.FCStd'
 before=hashlib.sha256(source.read_bytes()).hexdigest()
 matches=[d for d in App.listDocuments().values() if Path(d.FileName)==source]
 assert len(matches)==1,'A sessão deve conter uma única R32.'
 d=matches[0];App.setActiveDocument(d.Name)
 target=folder/'Guedala_Park_R33_Conferencia.FCStd'
 assert not target.exists(),'Não sobrescrever revisão existente.'
 assert not report['invalid'] and not report['intermodule_hits']
 # Confirmar que o relatório da cópia em disco corresponde à pose da sessão.
 def world(o):
  s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
 def bbox(s):
  b=s.BoundBox;return [round(v,4) for v in [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]]
 names=set(n for m in report['modules'].values() for n in m['parts'])
 shapes_before={n:d.getObject(n).Shape.hashCode() for n in names}
 for n,m in report['modules'].items():
  assert bbox(Part.makeCompound([world(d.getObject(p)) for p in m['parts']]))==m['bounds'],n
 sheet=d.addObject('Spreadsheet::Sheet','AuditoriaDimensionalR33');sheet.Label='R33 · medidas completas — portas/recortes/encosto incluídos'
 d.getObject('Documentacao').addObject(sheet)
 headers=['Objeto','Módulo','Envelope X mm','Envelope Y mm','Envelope Z mm','Altura nominal mm','Profundidade nominal mm','Critério e resultado']
 for i,v in enumerate(headers):sheet.set(chr(65+i)+'1',v)
 rows=[]
 for n,m in report['modules'].items():
  o=d.getObject(n);b=m['bounds'];dims=[round(b[i+3]-b[i],3) for i in range(3)]
  note='Peças correntes completas, incluindo recortes, uniões e cilindros. Eixos globais da base de edição; pose salva. Não é lista de corte.'
  if n=='Modulo001':note='Altura confirmada 308; a R32 omitia base e tampo em L do tipo Fuse e media 306.'
  if n in ['Modulo003','Modulo004','Modulo008','Modulo009','Modulo010','Modulo011','Modulo014','Modulo016','Modulo017']:note='Frentes com recortes agora incluídas. Diferença de 5,2 mm da R32 era omissão de medição, não redução da profundidade do móvel.'
  if n=='Modulo006':note='Reserva nominal P610; envelope corrente P597,5 na frente recuada Y6402,5. Não alongar grelha/peças para igualar a reserva.'
  if n=='Modulo007':note='Caixa nominal A145/P460; conjunto com rodas/frentes A180/P530.'
  if n=='Modulo013':note='Gabinete nominal A900; conjunto com tampo A920 e apoios até Z0.'
  if n=='Modulo019':note='Caixa/assento P450; encosto separado P100 completa P550. Corpo L1800; ponta de estudo avança50, envelope L1850. Revisão do banco adiada.'
  row=[n,o.Label,*dims,float(o.Altura),float(o.Profundidade),note];rows.append(row)
  for i,v in enumerate(row):sheet.set(chr(65+i)+str(len(rows)+1),str(v))
  for prop,val in zip(['EnvelopeGlobalX_R33','EnvelopeGlobalY_R33','EnvelopeGlobalZ_R33'],dims):
   o.addProperty('App::PropertyLength',prop,'AuditoriaR33');setattr(o,prop,val);o.setEditorMode(prop,1)
  o.addProperty('App::PropertyString','CriterioMedicaoR33','AuditoriaR33');o.CriterioMedicaoR33=note
  o.CriterioMedicaoR32='Histórico: leitura parcial superada pela AuditoriaDimensionalR33.'
 b=report['bank_with_backrest_bounds'];bankdims=[round(b[i+3]-b[i],3) for i in range(3)]
 bankrow=['Banco+encosto','Conjunto — inclui Peca421',*bankdims,'','','Envelope inclui encosto de100 e saliência longitudinal de50 do estudo lateral; nominal1800x550 mantido, sem redesenho.']
 rows.append(bankrow)
 for i,v in enumerate(bankrow):sheet.set(chr(65+i)+str(len(rows)+1),str(v))
 sheet.setStyle('A1:H1','bold','add');sheet.setColumnWidth('A',120);sheet.setColumnWidth('B',270);sheet.setColumnWidth('H',760)
 for col in 'CDEFG':sheet.setColumnWidth(col,150)
 old=d.getObject('AuditoriaDimensionalR32');old.Label='Histórico R32 · medição parcial superada pela R33'
 old.set('H23','SUPERADA: R32 omitia Cut/Fuse/Cylinder/Compound. Usar AuditoriaDimensionalR33. Banco externo550 inclui encosto separado100.')
 d.getObject('ConferenciaR32').Label='Histórico R32 · escopo parcial; consultar R33'
 audit=d.addObject('App::FeaturePython','ConferenciaR33');audit.Label='R33 · conferência completa e DWG preparado'
 d.getObject('Documentacao').addObject(audit)
 info={'Escopo':f"{report['native_count']} formas correntes válidas, tipos Part completos; 20 módulos e conjunto banco+encosto.",'Interferencias':f"{report['intermodule_pairs']} pares entre módulos avaliados por caixas envolventes e interseção exata quando necessário; nenhum volume comum acima de0,1mm³ na pose salva.",'Correcoes':'R32 omitia32 formas de tipos Cut/Fuse/Cylinder/Compound. Altura do canto308 confirmada; profundidades das frentes recuperadas; banco550=450+100. Geometria preservada.','Limites':'Teste estático entre módulos; não cobre todos os movimentos, arquitetura, instalações, calor, resistência ou medidas da unidade. Não libera fabricação.','DWG':'ODA File Converter27.9.0 instalado/configurado; teste FreeCAD→DWG→FreeCAD1000x500mm aprovado. Preparação local; projeto final não exportado nem enviado.','ProximoPasso':'Revisar movimentos de portas/gavetas contra arquitetura e aparelhos, e desenvolver acesso às conexões no gabinete da pia com posições de campo confirmadas.'}
 for key,val in info.items():audit.addProperty('App::PropertyString',key,'Auditoria');setattr(audit,key,val)
 d.Label='Guedala Park · R33 · conferência completa'
 d.recompute()
 assert all(d.getObject(n).Shape.hashCode()==v for n,v in shapes_before.items())
 assert not [o.Name for o in d.Objects if any(s in o.State for s in ['Invalid','Error'])]
 assert d.getObject('AcessoFolhaR31').ExtracaoBandeja==0
 Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
 d.saveAs(str(target))
 Gui.activeDocument().activeView().saveImage(str(folder/'Apartamento_R33.png'),1600,1100,'White')
 assert hashlib.sha256(source.read_bytes()).hexdigest()==before
 with (folder/'Medidas_completas_R33.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f,delimiter=';');w.writerow(headers);w.writerows(rows)
 report.update({'source_sha256':before,'source_unchanged':True,'geometry_changed':False,'saved_in_gui':True,'model':str(target),'objects':len(d.Objects),'corrections':info})
 (folder/'Conferencia_R33.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 status.write_text(json.dumps({'status':'OK','model':str(target),'objects':len(d.Objects)}),encoding='utf-8')
except Exception:
 status.write_text(traceback.format_exc(),encoding='utf-8');raise
