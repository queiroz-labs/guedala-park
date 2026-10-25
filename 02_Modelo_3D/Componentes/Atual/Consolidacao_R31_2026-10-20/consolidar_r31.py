"""Executar na GUI FreeCAD. Nova revisão; fontes e estudos não são salvos."""
from pathlib import Path
import json,hashlib,traceback
import FreeCAD as App,FreeCADGui as Gui,Part
here=Path(__file__).resolve().parent
project=here.parents[2]; root=project.parent
status=root/'tmp/consolidacao_r31_status.json'
source=here.parent/'Consistencia_R30_2026-10-14/Guedala_Park_R30_Juntas_Rotulos.FCStd'
oven_study=project/'Cozinha/Fischer_Grill_2026-10-19/Grelhas_manutencao_R02/Grelhas_Manutencao_R02.FCStd'
bank_study=project/'Sala_e_jantar/Retirada_ponta_R30/Estudo_Banco_Hibrido_R02.FCStd'
paths=[source,oven_study,bank_study]
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
status.write_text(json.dumps({'status':'iniciando'}),encoding='utf-8')
try:
 matches=[d for d in App.listDocuments().values() if Path(d.FileName)==source]
 assert len(matches)==1,'Abrir a R30 uma única vez antes de executar.'
 d=matches[0];assert len(d.Objects)==6128
 assert not (here/'Guedala_Park_R31_Consolidado.FCStd').exists(),'Revisão já existe; não sobrescrever.'
 def note(o,name,value):
  if name not in o.PropertiesList:o.addProperty('App::PropertyString',name,'ConsolidacaoR31')
  setattr(o,name,value)
 def bbox(o):
  b=Part.getShape(o).BoundBox
  return [round(v,4) for v in (b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax)]
 oldlinks={o.Name:bbox(o) for o in d.Objects if o.TypeId=='App::Link' and o.LinkedObject and hasattr(o.LinkedObject,'Shape') and not o.LinkedObject.Shape.isNull()}
 module_changes={'Modulo006','Modulo019','Modulo013','Peca133'}
 allowed={o.Name for o in d.Objects if o.TypeId=='App::Link' and o.LinkedObject and o.LinkedObject.Name in module_changes}
 d.openTransaction('Consolidação R31 — decisões e estudos até20/10')
 def feature(parent,name,label,s,color=(.77,.64,.48),condition='Proposta de detalhamento; sem liberação de fabricação.'):
  # Incorporar Placement da forma aos vértices antes dos controles de origem.
  # Assim as expressões de translação somam deslocamentos, sem apagar a pose-base.
  s=s.copy();pose=s.Placement;s.Placement=App.Placement();s=s.transformGeometry(pose.toMatrix())
  o=d.addObject('Part::Feature',name);o.Label=label;o.Shape=s;parent.addObject(o)
  o.ViewObject.ShapeColor=color;o.ViewObject.LineColor=(.24,.28,.26)
  note(o,'CondicaoR31',condition);return o
 def addgroup(parent,name,label):
  o=d.addObject('App::Part',name);o.Label=label;parent.addObject(o);return o
 def historical(o):
  o.Visibility=False;o.Label='Histórico R30 — '+o.Label
  note(o,'SuperadoR31','Oculto na revisão atual; preservado para rastreabilidade, não usar como peça vigente.')
 ov=App.openDocument(str(oven_study));App.setActiveDocument(d.Name)
 m=App.Matrix();m.A11=-1;m.A14=7400
 def from_mirrored(o,module=None):
  s=o.Shape.copy();s.Placement=o.getGlobalPlacement();s=s.transformGeometry(m)
  if module:s.transformShape(module.getGlobalPlacement().inverse().toMatrix())
  assert s.isValid();return s
 oven=addgroup(d.getObject('Ambiente_cozinha'),'FischerInfinityR31','Fischer Infinity50 L · grill sem turbo · gabarito de montagem')
 note(oven,'ProdutoEscolhido','Fischer28349-64929, preto127 V, sem turbo. Elétrico2061 W/16,22 A. Escolhido19/10; não comprado.')
 note(oven,'LimitesMontagem','Topo conservador570; datum apoio138 por conferir. L560 é recorte; profundidade547 conservadora. Kit, conexões, elétrica e200 até fundo do cooktop pendentes.')
 for n in ['Frente','CorpoConservador']:
  feature(oven,'Fischer'+n+'R31','Fischer · '+n+' · envelope',from_mirrored(ov.getObject(n)),(.09,.12,.11) if n=='Frente' else (.27,.34,.32))
 oldoven=d.getObject('Peca133');historical(oldoven)
 lk=d.getObject('EspelhoPecaR082');lk.LinkedObject=oven;lk.Label='Fischer Infinity com grill sem turbo · referência escolhida (espelhada)';oven.Visibility=False
 mod=d.getObject('Modulo006')
 for o in ov.Objects:
  if not o.Name.startswith(('BasePlana','Apoio','Contramarco','Grelha','Regua')):continue
  c=(.12,.16,.15) if o.Name.startswith('Grelha') else (.77,.64,.48)
  feature(mod,o.Name+'R31',o.Name+' · proposta R31',from_mirrored(o,mod),c,str(getattr(o,'Limite','Estudo de envelope.')))
 tr=d.getObject('Peca307');tr.setExpression('Placement.Base.y',None);v=tr.Placement.Base;v.y-=27;tr.Placement.Base=v
 tr.Label='Travessa cocção · avançada27 para liberar ar traseiro45 · proposta'
 note(mod,'VentilacaoR31','Entrada/saída560x60; canal traseiro45x560; duas grelhas600x90,272,43cm² livres cada. Não comprova vazão/temperatura. Não ocupar com gás/cabos/fundo.')
 note(mod,'ApoiosR31','Base18 sobre três nervuras18 até piso; vãos261,5. Meta50kg totais para dimensionamento, capacidade não comprovada. Material/ligações/nivelamento pendentes.')
 diagnostics=d.addObject('App::DocumentObjectGroup','ReservasTecnicasR31');diagnostics.Label='R31 · reservas técnicas ocultas — ar / recorte / cooktop hipotético'
 d.getObject('Documentacao').addObject(diagnostics)
 for o in ov.Objects:
  if o.Name.startswith('Ar') or o.Name in ['Cooktop131','RecorteCooktop']:
   q=feature(diagnostics,o.Name+'DiagR31',o.Label+' · DIAGNÓSTICO, não peça',o.Shape.copy(),(.25,.65,.72));q.ViewObject.Transparency=85;q.Visibility=False
 diagnostics.Visibility=False
 App.closeDocument(ov.Name)
 # Integrar recortes, apoios, reforços e bandeja do banco no seu sistema local.
 bank=App.openDocument(str(bank_study));App.setActiveDocument(d.Name);module=d.getObject('Modulo019')
 for n in ['Peca406','PecaBancoR007','PecaBancoR006']:
  old=d.getObject(n);s=bank.getObject('Ref_'+n).Shape.copy();historical(old)
  feature(module,n+'AtualR31',n+' · recorte híbrido R02 integrado',s)
 for n,delta in [('PecaBancoR025',12),('PecaBancoR024',3)]:
  o=d.getObject(n);v=o.Placement.Base;v.y+=delta;o.Placement.Base=v
  note(o,'AjusteR31','Reposicionamento local do estudo híbridoR02; função de guarda preservada.')
 for o in bank.Objects:
  if not o.Name.startswith(('Ref_Montante','Ref_Cabecalho','Ref_Apoio_B','Ref_Sarrafo','Guia_','Orelha_fixa','Pino')):continue
  feature(module,o.Name+'R31',o.Name.replace('Ref_','')+' · híbridoR02 proposto',o.Shape.copy(),(.23,.27,.25) if o.Name.startswith(('Ref_Montante','Guia_','Orelha','Pino')) else (.77,.64,.48))
 control=d.addObject('App::FeaturePython','AcessoFolhaR31');control.Label='Banco · bandeja pela ponta / folha · movimentos de estudo'
 d.getObject('ControlesAmbienteR005').addObject(control)
 for n,limit in [('ExtracaoBandeja',723),('DeslizamentoFolha',120),('ElevacaoFolha',648)]:
  control.addProperty('App::PropertyFloatConstraint',n,'Movimentos');setattr(control,n,(0,0,limit,1))
 note(control,'Sequencia','Bandeja0→723, deslizamento adicional da folha0→120, elevar somente com folha livre e conjunto sustentado. Pino manual na posição aberta. Sem intertravamento, operador/carga/ferragem reais não validados.')
 moving=[]
 for n in ['Plataforma','Aba_frente','Aba_tras','Receptor','Folha']:
  s=bank.getObject(n).Shape.copy();s.translate(App.Vector(843 if n=='Folha' else 723,0,0))
  q=feature(module,'Banco'+n+'R31',n+' · bandeja pela ponta R02',s,(.73,.58,.39) if n!='Receptor' else (.25,.29,.27))
  q.setExpression('Placement.Base.x','-AcessoFolhaR31.ExtracaoBandeja'+('-AcessoFolhaR31.DeslizamentoFolha' if n=='Folha' else ''))
  if n=='Folha':q.setExpression('Placement.Base.z','AcessoFolhaR31.ElevacaoFolha')
  moving.append(q.Name)
 historical(d.getObject('PecaBancoR035'))
 note(module,'ConstrucaoR31','HíbridoR02: apoios, reforços18x126, pórtico, bandeja723+120 e trava manualØ8. Painel maciço colado eM6 propostos.240kg é meta; resistência, uniões, estabilidade e uso reais pendentes.')
 note(d.getObject('ControleBancoR003'),'AcessoAtual','Tampa e almofada continuam para manutenção/guarda. Folha pela ponta usa AcessoFolhaR31; antiga reserva e retirada vertical de24mm foram superadas nesse acesso.')
 App.closeDocument(bank.Name)
 # Cesto: completar apoios inferiores do estudo construtivo, preservando movimento.
 cesto=d.getObject('Modulo013')
 for n,pos,dim in [('C01',(0,50,0),(18,580,98)),('C02',(572,50,0),(18,580,98)),('C03',(18,594,0),(554,18,80))]:
  feature(cesto,'ApoioCesto'+n+'R31',n+' · apoio inferior do cesto · proposto',Part.makeBox(*dim,App.Vector(*pos)))
 note(cesto,'ConstrucaoR31','C01–C03 integrados do estudo separado. Preservar fundo emU, pivôs/retirada, hidráulica e acesso. Capacidade/ligações e ferragens não homologadas.')
 # Decisões que não admitem geometria inventada ficam no próprio objeto/modelo.
 for n in ['Peca102','Peca103','Peca104','Peca105','Peca106']:
  o=d.getObject(n);o.Label=o.Label.replace('Cama queen existente','Queen futura · envelope de estudo')
  note(o,'UsoAtualEFuturo','Atual: cama de viúvo com baú, não medida. Futuro:queen com baú escolhida16/10.160x200 é reserva, não compra nem medida da base. Mala grande futura no baú a conferir.')
 for o in d.Objects:
  if o.TypeId=='App::Link' and o.LinkedObject and o.LinkedObject.Name in ['Peca102','Peca103','Peca104','Peca105','Peca106']:o.Label=o.LinkedObject.Label+' (espelhada)'
 office=d.getObject('Modulo016');note(office,'Ciclismo','Setor do próprio aéreo:1 capacete,1 sapatilha e1 kit no estojo, prateleiras reguláveis. Destino aprovado17/10; dimensões/carga/alcance pendentes. Sem módulo adicional.')
 for n in ['Peca188','Peca189']:
  o=d.getObject(n);o.ViewObject.ShapeColor=(1.0,.96,.88)
  note(o,'IluminacaoAprovada','Espelho4000K, indireta3000K, comandos físicos separados. Estas barras fixas são apenas propostas de posição; produtos/potência/instalação pendentes. Geral do teto não definida.')
 meta=d.addObject('App::FeaturePython','DecisoesConsolidadasR31');meta.Label='R31 · escolhas atuais e limites do projeto';d.getObject('Documentacao').addObject(meta)
 for k,v in {
  'DataConsolidacao':'20/10/2026',
  'Entrega':'Todos os ambientes prontos antes da mudança, conforme decisão16/10. Não há data/orçamento global definidos.',
  'Aparelhos':'Escolhidos, sem compra. Fischer grill sem turbo127V +KE4GC. GN confirmado. Circuito elétrico e execução pendentes.',
  'Cama':'Viúvo atual com baú, não medido; queen futura com baú escolhida. Não reabrir tamanho.',
  'Inventario':'1 mala de bordo10kg,1 mala grande futura,~5 mochilas encaixadas;1 capacete,1 sapatilha,1 kit ferramentas; até3 jogos futuros. Medidas/cabimento não comprovados.',
  'IluminacaoBanheiro':'Frontal4000K e indireta3000K, comandos físicos separados; geral do teto não definida.',
  'TV':'Apps na própriaTV; preferênciaAmbilight50PUG8100/78 comStremioLite aceito. AlternativaTCL50P7K. Sem reprodutor externo; candidatos, sem compra.',
  'Limites':'Estudos de construção incorporados para coordenação/cotação, sem liberação de fabricação, capacidade certificada ou medições da unidade.'}.items():note(meta,k,v)
 d.Label='Guedala Park · R31 consolidado até20/10/2026 · estudo'
 d.getObject('BaseEdicaoR30').ViewObject.ShowInTree=False
 d.recompute()
 invalid=[o.Name for o in d.Objects if any(t in o.State for t in ['Invalid','Error'])]
 # O acervo contém cópias históricas auxiliares inválidas já registradas naR27.
 # Validar o ramo físico corrente, sem confundir a base oculta com esses históricos.
 current_roots={o.LinkedObject.Name for o in d.getObject('ApartamentoEspelhadoR20').OutListRecursive if o.TypeId=='App::Link' and o.LinkedObject and o.Visibility}
 def active_native(o):
  seen=set()
  while o is not None and o.Name not in seen:
   if o.Name in current_roots:return True
   seen.add(o.Name)
   if not o.Visibility:return False
   o=o.getParentGeoFeatureGroup() if hasattr(o,'getParentGeoFeatureGroup') else None
  return False
 natives=[o for o in d.Objects if o.TypeId in ['Part::Box','Part::Feature','PartDesign::Feature'] and hasattr(o,'Shape') and not o.Shape.isNull()]
 badshapes=[o.Name for o in natives if active_native(o) and not o.Shape.isValid()]
 auxiliary_invalid=[o.Name for o in natives if not active_native(o) and not o.Shape.isValid()]
 assert not invalid and not badshapes,(invalid,badshapes)
 differences=[n for n,b in oldlinks.items() if n not in allowed and bbox(d.getObject(n))!=b]
 assert not differences,differences
 d.commitTransaction();target=here/'Guedala_Park_R31_Consolidado.FCStd';d.saveAs(str(target))
 assert hashes=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
 report={'revision':'R31','date':'2026-10-20','model':str(target),'objects':len(d.Objects),
  'reference_hashes_before':hashes,'reference_hashes_after':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
  'invalid_states':invalid,'invalid_native_shapes':badshapes,'invalid_auxiliary_historical_shapes':auxiliary_invalid,'current_native_shapes_checked':sum(active_native(o) for o in natives),'unchanged_links_checked':len(oldlinks)-len(allowed),'unexpected_link_changes':differences,
  'expected_changed_links':sorted(allowed),'moving_bank_features':moving,
  'integrated':['Fischer grill sem turbo e envelopesR02','base/três nervuras/contramarcos/grelhas/réguas/travessa','banco híbridoR02/apoios/bandeja/guarda/trava','apoiosC01–C03 do cesto','queen futura/viúvo atual','ciclismo','luz4000/3000 e comandos','inventário/TV/apps/entrega integrada'],
  'limits':'Sem auditoria térmica/estrutural/global de colisões. Conferências localizadas dos estudos preservadas; medidas, produtos e fabricação condicionados.'}
 (here/'Consolidacao_R31.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
 Gui.activeDocument().activeView().saveImage(str(here/'Apartamento_R31.png'),1600,1100,'White')
 status.write_text(json.dumps({'status':'pronto','objects':len(d.Objects),'model':str(target)}),encoding='utf-8')
except Exception:
 status.write_text(json.dumps({'status':'erro','trace':traceback.format_exc()}),encoding='utf-8');raise
