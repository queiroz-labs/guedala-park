import FreeCAD as A, FreeCADGui as G, pathlib, json, hashlib, math
out=pathlib.Path(__file__).parent
d=A.getDocument('Guedala_Park_R45_EM_REVISAO')
s=A.getDocument('Guedala_Park_R44_Consolidado')
assert d and s
source=pathlib.Path(s.FileName)
assert hashlib.sha256(source.read_bytes()).hexdigest()=='9187c163d7d827e12387e7e9c9e953b0380c55bcc8aaed3e872f83c4665d839e'
def signature(o):
 if not hasattr(o,'Shape') or o.Shape.isNull():return None
 b=o.Shape.BoundBox
 return [o.Shape.Volume,b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
baseline={o.Name:signature(o) for o in d.Objects}
restored=[]
for o in d.Objects:
 so=s.getObject(o.Name)
 if so and hasattr(o,'Shape') and hasattr(so,'Shape') and o.Shape.isNull() and not so.Shape.isNull() and o.isDerivedFrom('Part::Feature'):
  o.Shape=so.Shape.copy();restored.append(o.Name)
audit=d.addObject('App::DocumentObjectGroup','R45_Auditoria');audit.Label='R45 — resultados dimensionais e ferragens'
entries=[
('Cobertura','20 módulos inventariados; 171 interfaces. Cobertura não equivale a aprovação integral.','Inventario/Matriz_20_modulos.md'),
('Gavetas','FGVTN35kg;7pares500+2pares400 no cenário FGVTN. Escritório: alternativa MOVENTO400 exige ajuste de montagem, não incorporada.','Gavetas/Resultado.html'),
('MOVENTO','400mm preserva322x359úteis e cabe em412; pequenas interseções e folga de retirada pendentes. Sem reduzir para350.','Gavetas/Alternativas_escritorio/Resultado.html'),
('Dobradicas','52 vigentes:42comuns+4canto+6espelheiro. Excluir4antigas do gabinete banheiro. Contagem não é compra liberada.','Portas_e_articulacoes/Relatorio.html'),
('Banco','Tampas971/825x448x20 preservadas. Rockler traseira rejeitada; abertura frontal também atinge Berlin. Southco candidata não instalada.','Portas_e_articulacoes/Banco_Southco_premissas.md'),
('EstruturaBanco','18contatos de apoio; fixação M6 saliente pode invadir conteúdo. Fixação interna embutida requer cálculo próprio.','Banco_estrutura/Resultado.html'),
('Bancada','Alternativa estrutura embutida em estudo oculto; geometria vigente preservada. Não atribuir capacidade certificada.','Inventario/Bancada.md'),
('Espelheiro','8pinosHafele282.04.711 em estudo. Carga da placa não é capacidade nominal dos pinos.','Inventario/Espelheiro.md'),
('Minifix','20conjuntos no aéreoC apenas proposta de montagem fixa; não adotar sem detalhamento resistente.','Inventario/Minifix_C.md'),
('Varoes','4varões/8terminais; tuboØ20 precisa limite de carga e ligação definidos.','Inventario/Varoes.md'),
('Cesto','Frente+armação+8kgroupa:15,134kg no cenário900. Marathon35L comparado, mecanismo não aprovado.','Portas_e_articulacoes/Cesto_selecao_e_esforcos.md'),
('MesaVaral','Berlin vigente; excluir ferragens mesa antiga. CeilineManivela100x50 identificado como candidato importado.','Portas_e_articulacoes/Mesa_e_varal.md'),
('Fixacoes','SAH215 não cabe automaticamente: pede16mmatrás fundo, modelo não reserva. Ancoragem depende substrato real.','Inventario/Ferragens_fixas.md'),
('Aparelhos','ME23P100mm acima preservados por decisão anterior, divergência manual300mm continua aberta. Demais reservas nominais listadas.','Inventario/Cotas_e_calculos.md')]
for name,desc,rel in entries:
 o=d.addObject('App::FeaturePython','R45_'+name);o.Label=name+' — conferir relatório';audit.addObject(o)
 for p,v in [('Resultado',desc),('Relatorio',str(out/rel)),('Status','Estudo dimensional; consultar limites e pendências')]:
  o.addProperty('App::PropertyString',p,'R45');setattr(o,p,v)
studies=d.addObject('App::DocumentObjectGroup','R45_Estudos');studies.Label='R45 — alternativas separadas (ocultas; não aplicadas)'
copied=[]
for dn in ['Bancada_Estrutura_R45_R02_ESTUDO','Espelheiro_Pinos_R45_ESTUDO','AereoC_Minifix_R45_ESTUDO','Rockler_Fixacao_R46_TESTE']:
 sd=A.getDocument(dn)
 if not sd:continue
 group=d.addObject('App::DocumentObjectGroup','R45_Ref_'+dn);group.Label=dn+' — ESTUDO';studies.addObject(group)
 for so in sd.Objects:
  if not so.isDerivedFrom('Part::Feature') or so.Shape.isNull():continue
  q=so.Shape.copy();q.Placement=so.getGlobalPlacement()
  if any(abs(v)>1e8 for v in [q.BoundBox.XMin,q.BoundBox.YMin,q.BoundBox.ZMin,q.BoundBox.XMax,q.BoundBox.YMax,q.BoundBox.ZMax]):continue
  o=d.addObject('PartDesign::Feature','R45_Ref_'+so.Name);o.Label=so.Label;o.Shape=q;group.addObject(o)
  o.ViewObject.ShapeColor=so.ViewObject.ShapeColor;o.ViewObject.Transparency=so.ViewObject.Transparency
  o.addProperty('App::PropertyString','FonteEstudo');o.FonteEstudo=sd.FileName
  o.Visibility=False;copied.append(o.Name)
 group.Visibility=False
studies.Visibility=False
d.Label='Guedala Park R45 — consolidação dimensional e ferragens'
d.recompute()
changes=[]
for n,v in baseline.items():
 nv=signature(d.getObject(n))
 if v!=nv and n not in restored:
  if v is None or nv is None or any(abs(a-b)>max(1e-5,abs(a)*1e-9) for a,b in zip(v,nv)):changes.append(n)
assert not changes,changes
dest=out/'Guedala_Park_R45_Consolidado.FCStd'
A.setActiveDocument(d.Name);G.activeDocument().activeView().viewAxonometric();G.activeDocument().activeView().fitAll()
d.saveAs(str(dest))
data={'arquivo':str(dest),'objetos':len(d.Objects),'objetos_base':len(baseline),'copias_estudos':len(copied),'formas_restauradas_de_R44_aberta':restored,'mudancas_geometricas_na_base':changes,'R44_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'R45_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'estudos_ocultos_nao_instalados':True,'status':'Salvo; verificação independente do arquivo ainda deve ser executada'}
(out/'Consolidacao.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
result=data
