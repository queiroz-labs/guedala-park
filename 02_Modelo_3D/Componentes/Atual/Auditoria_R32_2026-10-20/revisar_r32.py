import sys
sys.path.append('C:/Users/Elias/AppData/Local/Programs/FreeCAD-1.1.4/lib')
import FreeCAD as App, FreeCADGui as Gui, Part
from pathlib import Path
import json,hashlib,csv,itertools,traceback
root=Path('C:/Users/Elias/Documents/PROJETOS/Guedala park')
folder=root/'guedala-park/02_Modelo_3D/Componentes/Atual/Auditoria_R32_2026-10-20'
folder.mkdir(exist_ok=True)
try:
 src=folder.parent/'Consolidacao_R31_2026-10-20/Guedala_Park_R31_Consolidado.FCStd'
 sha=hashlib.sha256(src.read_bytes()).hexdigest()
 d=App.openDocument(str(src))
 d.recompute()
 roots={o.LinkedObject.Name for o in d.getObject('ApartamentoEspelhadoR20').OutListRecursive if o.TypeId=='App::Link' and o.LinkedObject and o.Visibility}
 def active(o):
  seen=set()
  while o and o.Name not in seen:
   if o.Name in roots:return True
   seen.add(o.Name)
   if not o.Visibility:return False
   o=o.getParentGeoFeatureGroup() if hasattr(o,'getParentGeoFeatureGroup') else None
  return False
 native=[o for o in d.Objects if o.TypeId in ['Part::Box','Part::Feature','PartDesign::Feature'] and hasattr(o,'Shape') and not o.Shape.isNull() and active(o)]
 invalid=[o.Name for o in native if not o.Shape.isValid()]
 states=[o.Name for o in d.Objects if any(s in o.State for s in ['Invalid','Error'])]
 assert not invalid and not states,(invalid,states)
 def world(o):
  s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
 cook=[o for o in native if o in d.getObject('Modulo006').OutListRecursive or o in d.getObject('FischerInfinityR31').OutListRecursive]
 pairs=[];hits=[]
 for a,b in itertools.combinations(cook,2):
  sa,sb=world(a),world(b)
  ba,bb=sa.BoundBox,sb.BoundBox
  v=0
  if all(min(getattr(ba,k+'Max'),getattr(bb,k+'Max'))-max(getattr(ba,k+'Min'),getattr(bb,k+'Min'))>0.00001 for k in 'XYZ'):v=sa.common(sb).Volume
  pairs.append({'a':a.Name,'b':b.Name,'overlap_mm3':round(v,5)})
  if v>.1:hits.append(pairs[-1])
 sheet=d.addObject('Spreadsheet::Sheet','AuditoriaDimensionalR32');sheet.Label='R32 · medidas geométricas auditadas (mm)'
 d.getObject('Documentacao').addObject(sheet)
 headers=['Objeto','Módulo','Envelope X','Envelope Y','Envelope Z','Altura cadastrada','Profundidade cadastrada','Leitura correta']
 for i,h in enumerate(headers):sheet.set(chr(65+i)+'1',h)
 rows=[]
 for o in [x for x in d.Objects if x.Name.startswith('Modulo') and x.TypeId=='App::Part']:
  parts=[world(x) for x in native if x in o.OutListRecursive]
  if not parts:continue
  b=Part.makeCompound(parts).BoundBox
  note='Envelope dos componentes correntes na pose salva; eixos globais da base de edição. Não é lista de corte.'
  if o.Name=='Modulo019':note='Caixa/assento P450; programa externo P550 segundo decisão de 08/10. Não confundir as referências. Conferir representação externa completa antes de orçamento; banco não redesenhado.'
  if o.Name=='Modulo013':note='Altura cadastrada 900 não representa envelope com tampo/apoios. Distinguir caixa, tampo e conjunto.'
  if o.Name=='Modulo007':note='Envelope inclui rodas e frentes; altura/profundidade da caixa não são envelope externo.'
  row=[o.Name,o.Label,*[round(v,3) for v in [b.XLength,b.YLength,b.ZLength]],float(o.Altura) if hasattr(o,'Altura') else '',float(o.Profundidade) if hasattr(o,'Profundidade') else '',note]
  rows.append(row)
  for i,v in enumerate(row):sheet.set(chr(65+i)+str(len(rows)+1),str(v))
  o.addProperty('App::PropertyString','CriterioMedicaoR32','AuditoriaR32');o.CriterioMedicaoR32=note
 sheet.setStyle('A1:H1','bold','add');sheet.setColumnWidth('B',260);sheet.setColumnWidth('H',660)
 sheet.setColumnWidth('F',150);sheet.setColumnWidth('G',180)
 with (folder/'Medidas_modulos_R32.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f,delimiter=';');w.writerow(headers);w.writerows(rows)
 audit=d.addObject('App::FeaturePython','ConferenciaR32');audit.Label='R32 · auditoria dimensional e interferências da cocção'
 d.getObject('Documentacao').addObject(audit)
 for key,value in {'Escopo':f'{len(native)} formas correntes válidas; {len(rows)} módulos medidos; {len(pairs)} pares de cocção conferidos.', 'Interferencias':json.dumps(hits,ensure_ascii=False),'Pendencias':'Medidas de campo não fornecidas. Envelopes globais não são dimensões de corte. Banco: profundidade externa 550 no rótulo versus geometria corrente a conferir; revisão convencional permanece adiada.','Fonte':'R31 preservada; auditoria geométrica, sem validação térmica/estrutural ou liberação de fabricação.'}.items():
  audit.addProperty('App::PropertyString',key,'Auditoria');setattr(audit,key,value)
 d.recompute()
 if App.GuiUp: Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
 model=folder/'Guedala_Park_R32_Auditoria.FCStd';d.saveAs(str(model))
 if App.GuiUp: Gui.activeDocument().activeView().saveImage(str(folder/'Apartamento_R32.png'),1600,1100,'White')
 assert hashlib.sha256(src.read_bytes()).hexdigest()==sha
 report={'status':'concluido','date':'2026-10-20','native_shapes_checked':len(native),'invalid_shapes':invalid,'error_states':states,'modules':rows,'cooking_parts':[o.Name for o in cook],'cooking_pairs':pairs,'cooking_interferences':hits,'source_sha256':sha,'source_unchanged':True,'geometry_changed':False,'model':str(model)}
 (folder/'Auditoria_R32.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 (root/'tmp/status_r32.json').write_text(json.dumps({'status':'OK','shapes':len(native),'modules':len(rows),'pairs':len(pairs),'hits':hits},ensure_ascii=False),encoding='utf-8')
except Exception:
 (root/'tmp/status_r32.json').write_text(traceback.format_exc(),encoding='utf-8')
 raise

