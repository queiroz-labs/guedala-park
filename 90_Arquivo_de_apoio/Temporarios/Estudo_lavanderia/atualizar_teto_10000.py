from pathlib import Path
import json, re, subprocess, sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
A42=ROOT/'02_Projeto_em_desenvolvimento/A04.2_Lavanderia_e_equipamentos'
A43=ROOT/'02_Projeto_em_desenvolvimento/A04.3_Comparacao_LG'

# Change the current source so future exports retain the authorized ceiling.
src=HERE/'atualizar_escolha_VC4.py'
s=src.read_text(encoding='utf-8')
for before,after in [
 ('R$ 9.000','R$ 10.000'),('R$ 1.744,70','R$ 744,70'),('R$ 702','R$ 1.702'),
 ('Teto mantido em R$ 10.000.</b> A escolha da VC4 não autoriza aumento do orçamento.','Teto atualizado para R$ 10.000 por Elias.</b>'),
 ('O teto não foi alterado e o conjunto completo','O teto foi atualizado para R$ 10.000 e o conjunto completo'),
 ('teto de R$ 10.000 mantido','teto atualizado para R$ 10.000 por Elias'),
 ('teto de R$ 10.000 mantidos. Não houve compra nem aumento autorizado do orçamento.','teto atualizado para R$ 10.000, conforme instrução de Elias. Não houve compra.'),
 ('Esse é o ajuste necessário de preços, não autorização para mudar o equipamento ou aumentar o orçamento.','Esse é o ajuste necessário de preços para respeitar o novo teto, mantendo os equipamentos de referência.'),
 ('teto mantido em R$ 10.000','teto atualizado para R$ 10.000'),
 ('Aumento do teto não autorizado.','Teto atualizado por instrução de Elias.'),
 ('preserva o teto de R$ 10.000','registra o teto atualizado para R$ 10.000'),
 ('excesso_referencia_brl=1744.70','excesso_referencia_brl=744.70'),
 ('saldo_para_aquecedor_apos_ib6_vc4_brl=702','saldo_para_aquecedor_apos_ib6_vc4_brl=1702'),
 ('aumento_teto_autorizado=False','aumento_teto_autorizado=True'),
 ]: s=s.replace(before,after)
s=s.replace("data.update(revisao='R01',status=", "data.update(revisao='R01',orcamento_brl=10000,status=")
s=s.replace("o.update(cenario_referencia=", "o.update(teto_brl=10000,saldo_LG_mais_aquecedor_brl=6301,excesso_vc5_brl=144.70,excesso_vc4_brl=744.70,cenario_referencia=")
s=s.replace("data['historico']['revisao_anterior']='A04.3 R00'", "data['historico']['revisao_anterior']='A04.3 R00'\ndata['atualizacao_orcamento']={'data':'2026-09-09','teto_atual_brl':10000,'fonte':'Instrução expressa de Elias para atualizar o teto nos documentos e arquivos Markdown','nova_cotacao':False}")
s=s.replace("p('A04.3 R01 | Guedala Park | Elias | 09/09/2026','small')", "p('A04.3 R01 | Guedala Park | Elias | Teto atualizado em 09/09/2026','small')")
s=s.replace('- Resposta de Elias: “LG VC4 — prefiro ter Wi-Fi”.', '- Resposta de Elias: “LG VC4 — prefiro ter Wi-Fi”.\n- Instrução posterior de Elias: atualizar o teto de orçamento para R$ 10.000 nos documentos e arquivos Markdown.')
src.write_text(s,encoding='utf-8')

# Keep the active laundry PDF source and its companion generator coherent.
for name in ['gerar_estudo_R01.py','atualizar_R01.py']:
 f=HERE/name
 s=f.read_text(encoding='utf-8')
 for before,after in [
  ('R$ 9.000','R$ 10.000'),('R$ 5.301','R$ 6.301'),("'teto_brl':9000","'teto_brl':10000"),("'saldo_LG_mais_aquecedor_brl':5301","'saldo_LG_mais_aquecedor_brl':6301"),
  ('O teto de R$ 10.000 não foi aumentado.','Teto atualizado para R$ 10.000 por Elias.'),
  ('Orçamento total mantido em R$ 10.000.','Teto atualizado por Elias: R$ 10.000.'),
  ('Não houve compra de equipamentos nem aumento do orçamento.','Elias atualizou o teto para R$ 10.000. Não houve compra de equipamentos.'),
 ]: s=s.replace(before,after)
 f.write_text(s,encoding='utf-8')

# Refresh the already approved equipment labels in the active diagrams.
f=HERE/'gerar_estudo_R01.py'
s=f.read_text(encoding='utf-8')
for before,after in [
 ('LAVA E SECA LG<br/>modelo a definir','LAVA E SECA LG<br/>VC4 / vão pendente'),
 ("p('modelo a definir',214,471,105,8,MUTED)","p('VC4 / vão pendente',214,471,105,8,MUTED)"),
 ('Etapa 5 / Geladeira definida e marca da lava e seca confirmada por Elias.','Etapa 5 / IB6 e LG VC4 com Wi-Fi escolhidas; tensão e aquecedor pendentes.'),
 ('<b>Marca obrigatória: LG.</b><br/>Equipamento único, de abertura frontal, integrado à marcenaria.','<b>LG VC4 com Wi-Fi.</b><br/>Branca; 12 kg de lavagem e 7 kg de secagem. Referência escolhida.'),
 ('Modelo, capacidade, acabamento, tensão, dimensões e preço <b>a definir</b>.','CV5012WC4 (127 V) ou CV5012WC4A (220 V). Tensão e vão pendentes. Referência parcelada: <b>R$ 4.599</b>.'),
 ('Escolher o modelo LG em conjunto. Depois fechar o vão sob bancada, profundidade total, folgas e abertura frontal.','Confirmar tensão e manual da VC4. Fechar o vão sob bancada, profundidade total, folgas e abertura frontal.'),
 ('Orçamento a recompor com a LG','Orçamento atualizado: teto de R$ 10.000'),
 ('R$ 10.000 - R$ 3.699 da referência da IB6 = <b>R$ 6.301 para a lava e seca LG + aquecedor</b>. O total atualizado ainda não está fechado, pois os dois equipamentos dependem de modelo e cotação.','IB6 R$ 3.699 + LG VC4 R$ 4.599 + candidato E15 R$ 2.446,70 = <b>R$ 10.744,70: R$ 744,70 acima do teto</b>. Após IB6 + VC4, restam R$ 1.702 para o aquecedor. Cotações registradas na A04.3.'),
 ('As dimensões da lava e seca serão preenchidas somente depois da definição do modelo LG.','LG VC4 escolhida. Validar a versão elétrica e o manual antes de definir os vãos de instalação.'),
 ('A marca foi escolhida; ainda não há código de produto aprovado. A largura, a altura, as profundidades e os afastamentos continuam sem valores de projeto.','LG VC4 escolhida; tensão pendente. O manual da versão correta ainda precisa ser conferido. Vão e folgas sem validação para fabricação.'),
 ('Lava e seca obrigatoriamente LG; o modelo ainda será escolhido em conjunto.','Lava e seca LG VC4 branca com Wi-Fi escolhida; tensão pendente.'),
 ('Selecionar modelo LG e aquecedor; confirmar orçamento, gás e tensões;','Confirmar manual/tensão da VC4 e selecionar aquecedor; conferir orçamento e gás;'),
 ('A escolha da IB6 e da marca LG está registrada.','As escolhas da IB6 e LG VC4 e o teto de R$ 10.000 estão registrados.'),
 ('A04.2 R00 fica como histórico da comparação inicial. A R01 prevalece para equipamentos, orçamento e pendências; complementa o memorial v2 com as novas decisões de Elias.','A04.2 R00 fica como histórico. A04.3 R01 detalha a seleção atual e os preços de referência. Teto atualizado para R$ 10.000 por instrução de Elias; os demais dados do memorial permanecem.'),
 ('Escolhas: instrução de Elias nesta revisão. Fontes locais: P01, memorial v2, A01.2 e A04.2 R00.','Escolhas e teto: instruções de Elias. Fontes locais: P01, memorial v2, A01.2 e A04.3 R01. Sem nova cotação.'),
 ]: s=s.replace(before,after)
f.write_text(s,encoding='utf-8')

# Export both current PDFs, then synchronize their text and data companions.
subprocess.run([sys.executable,str(HERE/'atualizar_escolha_VC4.py')],check=True)
subprocess.run([sys.executable,str(HERE/'gerar_estudo_R01.py')],check=True)

f=A42/'A04.2_Decisoes_e_selecao_R01.md'
s=f.read_text(encoding='utf-8')
s=s.replace('R$ 9.000','R$ 10.000').replace('R$ 5.301','R$ 6.301')
s=s.replace('Não houve compra de equipamentos nem aumento do orçamento.','Elias atualizou o teto para R$ 10.000. Não houve compra de equipamentos.')
s=s.replace('A aprovação da IB6 é uma decisão de projeto. A escolha da marca LG não aprova um modelo específico.','IB6 e LG VC4 com Wi-Fi são as referências escolhidas por Elias.')
s=s.replace('| Lava e seca | **Marca LG obrigatória.** Equipamento único integrado à marcenaria, com acesso frontal. | Escolher modelo, capacidade, acabamento e tensão; obter manual, dimensões e preço. |','| Lava e seca | **LG VC4 branca com Wi-Fi**, 12 kg de lavagem / 7 kg de secagem, escolhida por Elias. | Confirmar tensão, manual da versão correta e instalação; cotação final. |')
s=s.replace('Recompor o total com o modelo LG e o aquecedor selecionados.','Cenário IB6 + VC4 + candidato E15: R$ 10.744,70, excesso de R$ 744,70.')
s=s.replace('### Lava e seca - LG, modelo pendente','### Lava e seca - LG VC4 com Wi-Fi escolhida')
s=s.replace('- Considerar exclusivamente LG na próxima seleção de lava e seca.','- LG VC4 branca com Wi-Fi escolhida. Códigos: CV5012WC4 (127 V) ou CV5012WC4A (220 V).')
s=s.replace('- Modelo, capacidade de lavagem/secagem, acabamento, tensão, largura, altura e profundidades continuam pendentes.','- Capacidade: 12 kg de lavagem e 7 kg de secagem. Tensão da unidade e dimensões/folgas para instalação pendentes; conferir o manual da VC4, sem aplicar o ensaio da VC5.')
s=s.replace('| Preço da LG | Pendente do modelo e da cotação |','| LG VC4 - referência parcelada da A04.3 | R$ 4.599 |')
s=s.replace('| Preço do aquecedor adequado | Pendente do dimensionamento e da cotação |','| Aquecedor E15 GN candidato - referência parcelada | R$ 2.446,70; seleção e gás pendentes |')
s=s.replace('| Total atualizado dos três | **Ainda não fechado** |','| Cenário IB6 + VC4 + candidato E15 | **R$ 10.744,70; R$ 744,70 acima do teto** |\n| Saldo após IB6 + VC4 | **R$ 1.702 para aquecedor** |')
s=s.replace('1. Selecionar o modelo LG em conjunto e consultar seu manual; não substituir por outra marca sem nova decisão de Elias.','1. Confirmar tensão da LG VC4 e consultar o manual da versão correta para definir a instalação.')
s=s.replace('Não foi realizada nova pesquisa de preços ou seleção de modelo LG nesta atualização documental.','Atualização documental: teto elevado para R$ 10.000 por Elias e escolha anterior da LG VC4 incorporada. Valores reaproveitados da A04.3; sem nova cotação.')
s=s.replace('registra a escolha da LG VC4 com Wi-Fi, pagamento parcelado e tensão pendente.','registra a escolha da LG VC4 com Wi-Fi, pagamento parcelado, tensão pendente e teto atualizado para R$ 10.000.')
f.write_text(s,encoding='utf-8')

current=json.loads((A43/'A04.3_Registro_R01.json').read_text(encoding='utf-8'))
f=A42/'A04.2_Registro_R01.json'
d=json.loads(f.read_text(encoding='utf-8'))
d.update(orcamento_brl=10000,pagamento='parcelado',status='estudo preliminar; IB6 e LG VC4 com Wi-Fi escolhidas; teto atualizado para R$ 10.000; tensão e aquecedor pendentes')
d['equipamentos']['lava_seca']=current['equipamentos']['lava_seca']
d['orcamento_atual']=current['orcamento_atual']
d['atualizacao_orcamento']=current['atualizacao_orcamento']
d['complemento_vigente']='A04.3 R01'
f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

f=ROOT/'LEIA-ME.md'
s=f.read_text(encoding='utf-8').replace('R$ 9.000','R$ 10.000').replace('R$ 1.744,70','R$ 744,70')
s=s.replace('preserva o teto de R$ 10.000','registra o teto atualizado para R$ 10.000')
s=s.replace('Aumento do teto não autorizado.','Teto atualizado por instrução de Elias.')
f.write_text(s,encoding='utf-8')

# Explicit notices prevent superseded records being mistaken for the live ceiling.
for folder in [A42,A43]:
 f=next(folder.glob('*R00.md'))
 s=f.read_text(encoding='utf-8')
 notice='> **Orçamento vigente: R$ 10.000**, atualizado por Elias. Os valores anteriores neste documento são histórico; consultar os documentos R01 e o índice do projeto para decisões atuais.\n\n'
 if notice not in s:
  lines=s.splitlines(keepends=True); lines.insert(2,notice); s=''.join(lines)
 f.write_text(s,encoding='utf-8')
 f=next(folder.glob('*Registro_R00.json'))
 d=json.loads(f.read_text(encoding='utf-8'))
 d['aviso_historico']={'documento':'revisão histórica','teto_vigente_brl':10000,'fonte_atual':'A04.3 R01','nao_usar_teto_da_revisao_como_atual':True}
 f.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Teto de R$ 10.000 e cálculos derivados sincronizados nos PDFs vigentes, Markdown, JSON e fontes de exportação.')
