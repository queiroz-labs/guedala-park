"""Corrige composição de coordenadas da exportação, sem mudar o conceito do banco.
Não aplica a reversão futura pedida por Elias; acrescenta somente essa anotação.
"""
from pathlib import Path
import FreeCAD as App,FreeCADGui as Gui,Part,json,hashlib,traceback
here=Path(__file__).resolve().parent;project=here.parents[2];root=project.parent
status=root/'tmp/conferencia_representacao_r31_status.json'
try:
 d=App.ActiveDocument;assert Path(d.FileName).name=='Guedala_Park_R31_Consolidado.FCStd'
 source=here.parent/'Consistencia_R30_2026-10-14/Guedala_Park_R30_Juntas_Rotulos.FCStd';sha=hashlib.sha256(source.read_bytes()).hexdigest()
 def baked(s):
  s=s.copy();pose=s.Placement;s.Placement=App.Placement();return s.transformGeometry(pose.toMatrix())
 ov=App.openDocument(str(project/'Cozinha/Fischer_Grill_2026-10-19/Grelhas_manutencao_R02/Grelhas_Manutencao_R02.FCStd'));m=App.Matrix();m.A11=-1;m.A14=7400
 mod=d.getObject('Modulo006')
 for o in ov.Objects:
  name='Fischer'+o.Name+'R31' if o.Name in ['Frente','CorpoConservador'] else o.Name+'R31'
  q=d.getObject(name)
  if not q or o.Name in ['Travessa'] or not hasattr(o,'Shape'):continue
  s=o.Shape.copy();s.Placement=o.getGlobalPlacement();s=s.transformGeometry(m)
  if o.Name not in ['Frente','CorpoConservador']:s.transformShape(mod.getGlobalPlacement().inverse().toMatrix())
  q.Shape=baked(s);q.Placement=App.Placement()
 App.closeDocument(ov.Name)
 bank=App.openDocument(str(project/'Sala_e_jantar/Retirada_ponta_R30/Estudo_Banco_Hibrido_R02.FCStd'))
 for n in ['Peca406','PecaBancoR007','PecaBancoR006']:
  q=d.getObject(n+'AtualR31');q.Shape=baked(bank.getObject('Ref_'+n).Shape);q.Placement=App.Placement()
 for o in bank.Objects:
  q=d.getObject(o.Name+'R31')
  if q and o.Name.startswith(('Ref_Montante','Ref_Cabecalho','Ref_Apoio_B','Ref_Sarrafo','Guia_','Orelha_fixa','Pino')):
   q.Shape=baked(o.Shape);q.Placement=App.Placement()
 for n in ['Plataforma','Aba_frente','Aba_tras','Receptor','Folha']:
  s=bank.getObject(n).Shape.copy();s.translate(App.Vector(843 if n=='Folha' else 723,0,0))
  q=d.getObject('Banco'+n+'R31');q.Shape=baked(s)
  # Não alterar valores do desenho, apenas compor deslocamento a partir da pose-base.
  q.Placement=App.Placement()
 App.closeDocument(bank.Name)
 for n in ['ApoioCestoC01R31','ApoioCestoC02R31','ApoioCestoC03R31']:
  q=d.getObject(n);q.Shape=baked(q.Shape);q.Placement=App.Placement()
 App.setActiveDocument(d.Name);d.recompute()
 def bounds(o):
  s=o.Shape.copy();s.Placement=o.getGlobalPlacement();b=s.BoundBox
  return [round(v,4) for v in (b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax)]
 closed={n:bounds(d.getObject(n)) for n in ['BancoPlataformaR31','BancoFolhaR31','BancoReceptorR31']}
 control=d.getObject('AcessoFolhaR31');control.ExtracaoBandeja=723;control.DeslizamentoFolha=120;d.recompute()
 opened={n:bounds(d.getObject(n)) for n in closed}
 for n in closed:
  delta=843 if n=='BancoFolhaR31' else 723
  assert abs(opened[n][1]-closed[n][1]-delta)<1e-4,(n,closed[n],opened[n])
 control.ExtracaoBandeja=0;control.DeslizamentoFolha=0;d.recompute()
 assert {n:bounds(d.getObject(n)) for n in closed}==closed
 # Somente anotação pedida durante a atualização; não reverter banco agora.
 text='20/10: Elias não gostou da bandeja lateral e quer retomar depois a guarda convencional abrindo o baú. Pediu apenas anotar, sem aplicar a reversão agora. Representação lateral permanece estudo a revisar, sem aceite para execução.'
 for q in [d.getObject('Modulo019'),d.getObject('AcessoFolhaR31'),d.getObject('DecisoesConsolidadasR31')]:
  if 'PreferenciaBanco20Out' not in q.PropertiesList:q.addProperty('App::PropertyString','PreferenciaBanco20Out','Registro')
  q.PreferenciaBanco20Out=text
 # Atualizar a ocultação dos ramos-base após acrescentar peças: não renderizar
 # os filhos novos soltos junto à cópia espelhada.
 for n in ['Modulo006','Modulo019','Modulo013','FischerInfinityR31']:
  q=d.getObject(n);q.Visibility=True;q.Visibility=False
 d.recompute();d.save()
 assert hashlib.sha256(source.read_bytes()).hexdigest()==sha
 Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll();Gui.activeDocument().activeView().saveImage(str(here/'Apartamento_R31.png'),1600,1100,'White')
 report={'status':'pronto','closed_bounds_mm':closed,'open_bounds_mm':opened,'movement_and_return_verified':True,'future_conventional_reversal_applied':False,'source_R30_unchanged':True,'model_sha256':hashlib.sha256(Path(d.FileName).read_bytes()).hexdigest()}
 (here/'Conferencia_representacao_R31.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');status.write_text(json.dumps(report),encoding='utf-8')
except Exception:
 status.write_text(json.dumps({'status':'erro','trace':traceback.format_exc()}),encoding='utf-8');raise
