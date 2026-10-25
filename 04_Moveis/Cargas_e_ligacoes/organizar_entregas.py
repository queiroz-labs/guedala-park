"""Indices e coordenadas nominais de estudo. Nao sao programa CNC."""
from pathlib import Path
import csv,json,hashlib
HERE=Path(__file__).resolve().parent
g=json.loads((HERE/'Geometria_R50.json').read_text(encoding='utf-8'))
c=json.loads((HERE/'Contatos_reconciliados.json').read_text(encoding='utf-8'))
def out(name,rows):
 with (HERE/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,list(rows[0]),delimiter=';');w.writeheader();w.writerows(rows)
status={'P01':('Estudos723/socoR01 separados; massas simultaneas e equilibrio rigido conferidos em4608 casos','Demonstrar caixa/juntas e transferenciaP03/P02; confirmar formato comercial do fundo1964x2114 ou projetar emenda; massas de ferragens, varoes, retencao/piso e revisao visual do soco pendentes'),
 'P02':('Seis contatos especificos de face BREP conferidos','Dimensionar fundo-fundo pela aresta e ligacoes da caixa emL'),
 'P03':('Massas e contatos superiores inventariados; contato traseiro proposto separado e seis modelos locais conferidos','Modelo reduzido excede referencia: demonstrar caixa/topo/fundo/laterais e juntas, travessa frontalP01 e transferenciaP02; nao liberar a base18 so pelo novo contato'),
 'P04':('Fundo308 e caminho base-divisorias estudados; demanda global de suspensao com portas calculada','Comprovar juntas/rigidez, escolher suspensor que caiba e responder a V/T simultaneos; parede real depois do levantamento'),
 'P09':('R48 sem canal preservada; demanda global calculada; manual do depurador6kg conferido','Demonstrar fixacoes parede+gabinete e interface nominal42mm/retorno20mm; nao presumir partilha; suspensor/juntas e parede real pendentes'),
 'P11':('Memoria local sem tubos e demanda global com portas abertas calculadas','Comprovar juntas/material, caixa e produto de suspensao sob V/T;10kg local nao e carga de todos os niveis'),
 'P12':('Demanda global com portas abertas/conteudo parametrico calculada','Comprovar caminhos da caixa/divisoria, juntas, produto de suspensao e substrato real; sem capacidade liberada'),
 'P14':('Reacoes3D na parada55 e energia nominal calculadas;270 cenarios, sem capacidade liberada','Componentes/massas reais, planos de bucha, retencao vertical e axial, juntas/terminais/trava e prototipo'),
 'P15':('Base/fundo e suspensao estudados; composicao parcial da interface calculada em16respostas','Obter produto/processo/curva real e durabilidade da composicao e juntas; TitebondMelamine excluida desta sustentacao; suspensaoV/T e parede real pendentes'),
 'P16':('Bancada separada; curso conferido,1296equilibrios;18regioes guia-fundo e quatrofuros localizados/conferidos','Massa/rigidez do tampo30, juntas/retencao, montagemMOVENTO400 e causa/aceitabilidade das regioes guia-fundo; revisar aparencia/uso antes de incorporar'),
 'P17':('Demanda global e placa local calculadas; estudo separado fundo550/16contatos/58eixos nominais','Comprovar juntas/retencao e referencia superior da caixa, revisar acabamento, atualizar massa global se adotar fundo e selecionar suspensao; sem carga liberada'),
 'P20':('Curvas torque;18 contatos das tampas reconciliados e assento fechado calculado condicionalmente','Painel ortotropico, juntas/corpo, massa global real, conjunto movel/terminais e prototipo; ver P20_assento_fechado')}
status.update({
 'P05':('Geometria/contatos inventariados; caixa e apoios ainda por dimensionar','Definir caminho de carga da bancada/cuba, ligacoes, protecao e acesso hidraulico; cotas finais depois das chaves'),
 'P06':('Caixas comuns e quadro de massas existentes; produto efetivo e montagem ainda condicionados','Fechar desenho/massas FGVTN500 e interfaces G1/G2/G3, incluindo bandejas; nao homologar pela geometria STEPBlum de referencia'),
 'P07':('Estrutura nominal do modulo de coccao inventariada','Dimensionar apoios/ligacoes do forno e bancada, compatibilizar ventilacao com manuais e acesso; gas/eletrica final com responsavel'),
 'P08':('Selecao de rodizio38 e espacador1 documentada; montagem real condicionada','Confirmar desenho de fixacao e massa/conteudo da gaveta; calcular reparticao nos seis rodizios, batente/guia e contato com piso'),
 'P10':('Ferragens Minifix e geometria/fichas existentes; caixa local nao encerrada','Dimensionar base/prateleiras-fundo e unioes da caixa, preservando conjuntos existentes sem duplicar marcadores como compra'),
 'P13':('Geometria do apoio aberto do micro inventariada','Confrontar massa/apoiamento do aparelho com chapa, ligacoes e caminho para o corpo; preservar ventilacao e acesso'),
 'P18':('Fichas e gabinete nominal; referencias de acesso ocultadas na vista normal','Dimensionar caixa/suspensao e encontros da cuba, frente removivel/correr e manutencao; materiais reais e pontos do imovel depois'),
 'P19':('Geometria/fichas do armario espelhado e ferragens existentes','Completar massa real de folhas/espelhos e ligacoes da caixa/suspensao; confirmar apoio/fixacao sem assumir resistencia da parede')})
# Responsaveis sao propostos, nao contratados. Prazo e bloco planejado, nao garantia.
meta={
 'P01':('Projeto; produto/oficina','25-27/10','P01_massas_equilibrio_2026-10-25/README.md'),
 'P02':('Projeto; oficina','26-27/10','Cargas_e_ligacoes_R50_2026-10-25/README.md'),
 'P03':('Projeto; oficina','25-27/10','P01_P03_caminho_superior_2026-10-25/README.md'),
 'P04':('Projeto; produto/oficina','25-26/10','Solucoes_marcenaria_sem_tubos_2026-10-25/README.md'),
 'P05':('Projeto; produto/oficina','28/10','Cargas_e_ligacoes_R50_2026-10-25/README.md'),
 'P06':('Projeto; produto/oficina','28/10','Modelo_FreeCAD/02_Revisoes_e_estudos/Cargas_gavetas_R28_2026-10-14/Cargas_gavetas_R28.html'),
 'P07':('Projeto; produto; responsavel tecnico','28/10','Cargas_e_ligacoes_R50_2026-10-25/README.md'),
 'P08':('Projeto; produto/oficina','28/10','Cozinha/Rodizios_gaveta_2026-10-24/Selecao.md'),
 'P09':('Projeto; produto/oficina','26-28/10','Aereos_suspensao_P09_P11_P12_P17_2026-10-25/README.md'),
 'P10':('Projeto; oficina','26-28/10','Cargas_e_ligacoes_R50_2026-10-25/README.md'),
 'P11':('Projeto; produto/oficina','25-26/10','P11_ligacoes_sem_tubos_2026-10-24/Resultado_R00.md'),
 'P12':('Projeto; produto/oficina','26-28/10','Aereos_suspensao_P09_P11_P12_P17_2026-10-25/README.md'),
 'P13':('Projeto; produto/oficina','28/10','Cargas_e_ligacoes_R50_2026-10-25/README.md'),
 'P14':('Projeto; produto/oficina; prototipo','27/10','P14_reacoes_e_operacao_2026-10-25/README.md'),
 'P15':('Projeto; fabricante/processo; oficina','25-26/10','P15_composicao_parcial_2026-10-25/README.md'),
 'P16':('Projeto; produto/oficina; Elias','28/10','P16_interface_guia_fundo_2026-10-25/README.md'),
 'P17':('Projeto; produto/oficina','26/10','P17_base_fundo_ligacoes_2026-10-25/README.md'),
 'P18':('Projeto; produto/oficina','28/10','Cargas_e_ligacoes_R50_2026-10-25/README.md'),
 'P19':('Projeto; produto/oficina','28/10','Cargas_e_ligacoes_R50_2026-10-25/README.md'),
 'P20':('Projeto; produto/oficina; Elias; prototipo','27/10','P20_assento_fechado_2026-10-25/README.md')}
assert len(meta)==len(status)==20
rows=[]
for code,mod in g['modules'].items():
 st,task=status.get(code,('Geometria inventariada; contatos da fila conferidos quando existentes','Dimensionar ligacoes por lote do plano; conferir apoios, conector e acesso'))
 owner,planned,evidence=meta[code];assert (HERE.parent/evidence).is_file(),evidence
 rows.append(dict(module=code,name=mod['label'],inventoried_shapes=len(mod['pieces']),
  old_queue_contacts=sum(r['module']==code for r in c['contacts']),
  status=st,next_action=task,proposed_owner=owner,planned_work_block_2026=planned,evidence=evidence,
  dependency='Acao de projeto/produto acima pode avancar antes das chaves. Medidas finais, parede/piso e instalacao dependem do imovel; capacidade real nao liberada.'))
out('Andamento_20_moveis.csv',rows)
md=['# Matriz de execucao dos20 moveis —25/10/2026','',
 'Proxima acao, responsavel proposto e evidencia por movel. A matriz nao declara20 calculos completos ou fabricacao liberada. Inventario de formas inclui ferragens/gabaritos e nao e lista de corte.',
 '', '| Movel | Estado comprovado | Proxima acao | Responsavel proposto / bloco planejado | Evidencia |',
 '|---|---|---|---|---|']
for r in rows:
 clean=lambda s:str(s).replace('|','/')
 md.append('| '+clean(r['module']+' '+r['name'])+' | '+clean(r['status'])+' | '+clean(r['next_action'])+' | '+clean(r['proposed_owner']+' / '+r['planned_work_block_2026'])+' | [Relatorio](../'+r['evidence']+') |')
md += ['', 'Datas sao blocos do plano ate31/10, sujeitos a dados/produtos e revisao. Nenhuma pessoa/oficina foi contratada ou contatada. Nao converter pendencia de projeto em espera generica pelo apartamento.',
 '', 'Integrar somente propostas demonstradas e revisadas; manter lista-base, fichas/site e orçamento coerentes. [Entrada de retomada](../Retomada_25_10_2026.md). Fonte editavel desta matriz: organizar_entregas.py; nao editar somente oCSV/Markdown gerado.', '']
(HERE/'Andamento_20_moveis.md').write_text('\n'.join(md),encoding='utf-8')
rows=[]
for piece,origin,sign in [('Peca245',6649.,1.),('Peca246',6131.,-1.)]:
 entries=[('Minifix15+pino18',723.,y,'fixacao da extremidade na lateral') for y in [70.,480.]]
 entries += [('Confirmat7x50',x,550.,'ligacao traseira de estudo') for x in [72.,265.,458.,651.]]
 entries += [('Cavilha8x30',x,550.,'posicionamento sem credito resistente') for x in [168.5,361.5,554.5]]
 for i,(family,x,y,role) in enumerate(entries,1):
  rows.append(dict(id=f'P01-723-{piece}-{i:02d}',piece=piece,family_proposed=family,
    canonical_x_mm=x,canonical_y_mm=y,global_X_mm=origin+sign*x,global_Y_mm=3372+y,
    nominal_axis_Z_mm=1091.,quantity=1,role=role,
    datum='x0 na ponta estendida, y0 frente; chapa esquerda espelhada',
    status='ESTUDO: ponto da interface/eixo medio, NAO centro completo de furo/CNC. Profundidades, ferramenta e resistencia pendentes',
    quantity_rule='Reconciliar/substituir linhas destas pecas no mapa anterior; nao somar tudo como novos conjuntos'))
out('P01_ligacoes_nominais_estudo_723.csv',rows)
# Hashes permitem detectar mudanca das rotinas reutilizadas, sem alterar a fonte.
paths=['calcular.py','extrair_geometria.py','conferir_interfaces_adicionais.py','estudo_p01.py',
 '../Calculo_P11_2026-10-24/calcular_p11.py','../P11/Ligacoes_sem_tubos/placa_ritz.py']
(HERE/'Rotinas_SHA256.json').write_text(json.dumps({p:hashlib.sha256((HERE/p).read_bytes()).hexdigest() for p in paths},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'modules':20,'P01_nominal_study_positions':len(rows)}))
