from pathlib import Path
import json, re

# Reuse the established visual style, without running the R00 authoring steps.
base = Path(__file__).with_name('gerar_comparacao_LG.py').read_text(encoding='utf-8')
prefix = base.split("p('Lava e seca LG<br/>e orçamento parcelado','title')")[0]
prefix = prefix.replace("shutil.copy2(Path(__file__).parent/'Manual_LG_CV3012WC5.pdf', manual)", '')
exec(compile(prefix, str(Path(__file__)), 'exec'))

pdf = OUT/'A04.3_Selecao_LG_VC4_e_orcamento_R01.pdf'
p('LG VC4 com Wi-Fi<br/>escolhida para o projeto','title')
p('A04.3 R01 | Guedala Park | Elias | Teto atualizado em 09/09/2026','small')
p('<b>Decisão de Elias: LG VC4 - preferência pelo Wi-Fi.</b> Adotada a versão branca de 12 kg apresentada na comparação. O código de compra depende da tensão disponível no ponto da lavanderia, ainda desconhecida.')
table([
 ['Equipamento','Decisão vigente','Pendente'],
 ['Geladeira','Electrolux IB6 branca, inverse, 400 L','Instalação e cotação final'],
 ['Lava e seca','LG VC4 branca, 12 kg de lavagem / 7 kg de secagem, Wi-Fi ThinQ','Tensão e compatibilização da instalação'],
 ['Aquecedor','Modelo ainda não escolhido; Rinnai E15 FEH em avaliação','Gás, demanda, instalação e seleção'],
 ],[119,221,165])
p('Código conforme a tensão','h')
table([
 ['Tensão do ponto','Referência LG','Situação'],
 ['127 V','CV5012WC4','Versão possível; tensão não confirmada'],
 ['220 V','CV5012WC4A','Versão possível; tensão não confirmada'],
 ],[119,164,222])
p('Não são versões bivolt. Confirmar a tensão com a construtora/condomínio ou profissional antes de definir o código. A escolha de Elias é referência de projeto; não houve compra.','small')
p('Orçamento com a VC4 escolhida','h')
table([
 ['Equipamento / referência','Total parcelado','Condição registrada na R00'],
 ['IB6 / loja Electrolux','R$ 3.699,00','10x de R$ 369,90 sem juros'],
 ['LG VC4 / loja LG','R$ 4.599,00','Até 12x sem juros'],
 ['E15 GN / Leroy Merlin¹','R$ 2.446,70','Até 8x; parcela exibida de R$ 305,84'],
 ['Cenário IB6 + VC4 + E15','R$ 10.744,70','R$ 744,70 acima do teto'],
 ],[193,128,184])
p('¹ Aquecedor candidato, código da loja 90555640; gás da unidade e código completo do produto ainda não confirmados. Valores reaproveitados da consulta de 09/09/2026 da R00, sem nova cotação nesta revisão. Parcelas podem ter arredondamento. Frete, instalação, kits e adaptações não incluídos.','small')
p('<b>Teto atualizado para R$ 10.000 por Elias.</b> Com IB6 e VC4 nos valores acima, sobram R$ 1.702 para o aquecedor. É necessário reduzir o preço combinado em R$ 744,70 para atingir o teto deste cenário.','small')

story.append(PageBreak())
p('Base para detalhar a lavanderia','title')
p('O modelo de referência está definido. O espaço de instalação ainda precisa ser validado.','small')
p('Dimensões: o que está documentado','h')
p('Na consulta registrada na R00, a ficha da <b>VC4 127 V</b> informa corpo de <b>60 x 85 x 56,5 cm</b> (L x A x P), profundidade até a porta fechada de <b>62 cm</b> e com a porta a 90° de <b>110 cm</b>. As profundidades partem da traseira do equipamento, sem acrescentar folga de instalação.')
p('A página da <b>VC4 220 V</b> apresentou largura e ordem de dimensões conflitantes. Conferir pelo manual do código exato. Nesta revisão não se confirma o vão necessário, a altura final da bancada nem o cabimento da máquina.')
p('<b>O ensaio da VC5 na R00 fica como histórico.</b> As reservas de 64 / 85,5 / 72 / 120 cm daquela página foram calculadas com o manual da VC5 127 V. Não foram validadas nem aprovadas para a VC4. O manual da VC5 salvo no projeto também não é o manual da máquina escolhida.')
p('Próximas conferências','h')
table([
 ['Conferência','Resultado necessário para avançar'],
 ['LG VC4','Obter o manual da versão correta e confirmar folgas laterais, traseira e superior, mangueiras, abertura, acesso ao filtro e retirada para manutenção.'],
 ['Ponto elétrico','Confirmar tensão, tomada, aterramento e circuito compatíveis. Tensão permanece pendente no registro.'],
 ['Área de serviço','Medir larguras úteis, shaft, recessos, eixos dos pontos, altura do peitoril e interferências da janela. 1,29 m é paralelo à bancada; 1,54 m é perpendicular.'],
 ['Tanque e bancada','Preservar cesto removível ventilado abaixo do tanque, apoio independente da pedra e retorno em L de aproximadamente 15 cm junto à janela.'],
 ['Aquecedor','Confirmar GN/GLP, vazão do chuveiro/torneiras, pressão, rede de água quente, ventilação e exaustão. O E15 permanece candidato.'],
 ],[121,384])
p('Decisões preservadas','h')
p('Pagamento parcelado; um morador com possibilidade de dois; água quente nos pontos desejados, sem banho e torneira simultâneos; geladeira IB6; demais acabamentos do memorial. Janela sem armários, varal alto e oculto e móveis do quarto sem azul. Não há liberação para fabricação.')
p('Fontes e prioridade','h')
p('Escolha de Elias nesta revisão: "LG VC4 - prefiro ter Wi-Fi". Dados comerciais e fichas provenientes da pesquisa já registrada na A04.3 R00; não houve nova pesquisa de preços ou leitura de manual VC4 nesta atualização.','small')
for labels in [['LG VC4 127 V','LG VC4 220 V','Electrolux IB6'],['E15 GN - oferta Leroy Merlin','Rinnai E15 - ficha técnica']]:
 p(' | '.join(f'<a href="{sources[x]}" color="#176974">{x}</a>' for x in labels),'small')
p('A04.3 R01 substitui a recomendação da VC5 e a pendência de escolha LG da R00. A04.2 R01 continua como partido da lavanderia; A01.2 permanece base dimensional. O teto foi atualizado para R$ 10.000 e o conjunto completo ainda depende da escolha do aquecedor.','small')

def footer(c, doc):
 c.setTitle('A04.3 R01 - LG VC4 escolhida e orçamento - Elias')
 c.setAuthor('Projeto Guedala Park - Elias')
 c.setStrokeColor(HexColor('#CEDCD7')); c.line(45,37,550,37)
 c.setFont('Segoe',8); c.setFillColor(MUTED)
 c.drawString(45,23,'GUEDALA PARK  |  A04.3 R01  |  ESTUDO PRELIMINAR')
 c.drawRightString(550,23,f'{doc.page} / 2')
SimpleDocTemplate(str(pdf),pagesize=(595.28,841.89),rightMargin=45,leftMargin=45,topMargin=39,bottomMargin=51).build(story,onFirstPage=footer,onLaterPages=footer)

data=json.loads((OUT/'A04.3_Registro_R00.json').read_text(encoding='utf-8'))
data.update(revisao='R01',orcamento_brl=10000,status='LG VC4 com Wi-Fi escolhida como referência; tensão e aquecedor pendentes; teto atualizado para R$ 10.000 por Elias')
lg=data['equipamentos']['lava_seca']
lg.update(modelo='VC4',linha='VC4',capacidade_lavagem_kg=12,capacidade_secagem_kg=7,cor='branca',wifi=True,tensao_v=None,codigo_compra=None,codigos_por_tensao={'127':'CV5012WC4','220':'CV5012WC4A'},modelo_referencia_escolhido=True,motivo_escolha='Elias prefere ter Wi-Fi',status='LG VC4 escolhida como referência; versão elétrica e instalação pendentes',dimensoes_cm=None,preco_brl=None)
lg.pop('candidata_principal',None)
lg.pop('candidata_aprovada',None)
lg['referencia_ficha_127v']={'corpo_LAP_cm':[60,85,56.5],'profundidade_porta_fechada_cm':62,'profundidade_porta_90_cm':110,'fonte':sources['LG VC4 127 V'],'folgas_validadas':False}
data['ensaio_vc5_127v']['status']='histórico da R00; não utilizar no dimensionamento da VC4'
data['ensaio_vc5_127v']['aplicavel_a_modelo_escolhido']=False
o=data['orcamento_atual']
o.update(teto_brl=10000,saldo_LG_mais_aquecedor_brl=6301,excesso_vc5_brl=144.70,excesso_vc4_brl=744.70,cenario_referencia='IB6 + LG VC4 + candidato E15 GN',cenario_referencia_brl=10744.70,excesso_referencia_brl=744.70,saldo_para_aquecedor_apos_ib6_vc4_brl=1702,aumento_teto_autorizado=True,nova_cotacao_nesta_revisao=False,referencia_precos='A04.3 R00, consulta de 09/09/2026')
data['historico']['revisao_anterior']='A04.3 R00'
data['atualizacao_orcamento']={'data':'2026-09-09','teto_atual_brl':10000,'fonte':'Instrução expressa de Elias para atualizar o teto nos documentos e arquivos Markdown','nova_cotacao':False}
data['historico']['escolha_atual']='VC4 com Wi-Fi substitui a recomendação anterior de VC5; tensão permanece pendente'
data['historico']['comparacoes_descartadas_da_selecao_atual'].append('LG VC5 - alternativa não escolhida')
(OUT/'A04.3_Registro_R01.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

md='''# A04.3 - LG VC4 escolhida e orçamento parcelado

**R01 | 09/09/2026 | Revisão vigente para seleção de equipamentos**

[Abrir o PDF atualizado](A04.3_Selecao_LG_VC4_e_orcamento_R01.pdf)

## Escolha de Elias

**LG VC4 com Wi-Fi escolhida como referência para o projeto**, pela preferência de Elias pela conectividade. Adotada a opção branca de 12 kg de lavagem e 7 kg de secagem apresentada na comparação.

- 127 V: CV5012WC4.
- 220 V: CV5012WC4A.
- A tensão do ponto da lavanderia continua desconhecida. Código final de compra pendente; o aparelho não é bivolt.
- A VC5 passa a alternativa histórica não escolhida. Não é mais a candidata principal.
- A geladeira permanece Electrolux IB6 branca inverse de 400 L.
- Aquecedor ainda pendente; E15 FEH permanece candidato em avaliação.
- Pagamento parcelado e teto atualizado para R$ 10.000 por Eliass. Não houve compra nem aumento autorizado do orçamento.

## Cenário de orçamento com a escolha

| Equipamento | Total parcelado | Condição da consulta R00 |
|---|---:|---|
| Electrolux IB6 | R$ 3.699,00 | 10x de R$ 369,90 sem juros |
| LG VC4 | R$ 4.599,00 | Até 12x sem juros |
| E15 GN, candidato, Leroy 90555640 | R$ 2.446,70 | Até 8x; parcela anunciada R$ 305,84 |
| **Cenário com VC4** | **R$ 10.744,70** | **R$ 744,70 acima do teto** |

São valores da pesquisa de 09/09/2026 registrada na R00, **sem nova cotação nesta revisão**. Não representam promessa de preço/estoque. Frete, instalação, kits e adaptações não incluídos. Não há compra única do conjunto em 12x: cada loja oferece um prazo. Usado o total anunciado; parcelas podem ter arredondamento.

Gás da unidade não confirmado. Preço do aquecedor é da oferta GN indicada, ainda sujeita à conferência do código completo e dimensionamento. Não transferir a cotação para GLP por suposição.

Com IB6 e VC4 nesses preços: R$ 10.000 - R$ 3.699 - R$ 4.599 = **R$ 1.702** para o aquecedor. O conjunto precisa de redução combinada de **R$ 744,70** para alcançar o teto desse cenário. Esse é o ajuste necessário de preços para respeitar o novo teto, mantendo os equipamentos de referência.

## Instalação: situação após a escolha

A ficha VC4 127 V registrada na R00 publica corpo de **60 x 85 x 56,5 cm** (L x A x P), 62 cm da traseira à porta fechada e 110 cm da traseira à porta a 90°. Essas dimensões externas **não definem o nicho** e não incluem folgas adicionais.

A ficha VC4 220 V apresentou largura de 660 mm e ordem das medidas conflitantes. Conferir pelo manual do código exato antes de dimensionar. Não há validação do vão nem cabimento confirmado nesta revisão.

**O ensaio da VC5 127 V na página 2 da R00 e o manual VC5 salvo no projeto são históricos.** As reservas 64 / 85,5 / 72 / 120 cm foram calculadas com aquele manual, e não foram validadas para a VC4. Não transferir as folgas da VC5 para a máquina escolhida.

Próximos fechamentos:

1. Confirmar a tensão do ponto da lavanderia com construtora/condomínio ou profissional.
2. Obter manual da VC4 na versão correta; conferir folgas, alimentação, mangueiras, abertura, circuito e acesso à manutenção.
3. Confirmar gás da unidade e demanda para escolher o aquecedor.
4. Levantar peitoril, janela e suas aberturas, grelhas, shaft/recessos, eixos dos pontos, largura/altura útil e comprimento do retorno em L.
5. Detalhar a implantação com a VC4, IB6, tanque, cesto ventilado removível abaixo do tanque, varal e estrutura independente da pedra.

1,29 m é paralelo à bancada e 1,54 m é perpendicular. O retorno em L de aproximadamente 15 cm fica junto à janela e não é um módulo extra na sequência linear. Não foi definido novo vão ou alterada a posição dos módulos da cozinha.

## Demais decisões preservadas

Água quente nos pontos desejados, sem banho e torneira simultâneos; um morador com possibilidade de dois; janela sem armários; superiores e inferiores conforme memorial; móveis do quarto sem azul. Nenhuma liberação para fabricação.

A04.3 R01 substitui a recomendação da VC5 e a pendência de escolha LG da R00. A04.2 R01 permanece como partido e A01.2 como base dimensional. PDFs anteriores são histórico; este registro e o índice apontam a decisão mais recente.

## Fontes

- Resposta de Elias: “LG VC4 — prefiro ter Wi-Fi”.
- Instrução posterior de Elias: atualizar o teto de orçamento para R$ 10.000 nos documentos e arquivos Markdown.
- Pesquisa documentada na A04.3 R00, consultada em 09/09/2026. Sem nova cotação ou leitura de manual VC4 nesta revisão.
'''
md+='\n'.join(f'- [{x}]({sources[x]})' for x in ['LG VC4 127 V','LG VC4 220 V','Electrolux IB6','E15 GN - oferta Leroy Merlin','Rinnai E15 - ficha técnica'])+'\n'
(OUT/'A04.3_Escolha_VC4_e_pendencias_R01.md').write_text(md,encoding='utf-8')

index=ROOT/'99_Arquivo/Organizacao_anterior/Indice_anterior.md'
s=index.read_text(encoding='utf-8')
s=s.replace('comparação atual A04.3 R00 de LG/orçamento parcelado','seleção atual A04.3 R01 da LG VC4 com Wi-Fi e orçamento parcelado')
s=s.replace('[Comparação LG e orçamento parcelado atual - A04.3 R00](../../Estudos_anteriores/Equipamentos/Comparacao_LG_e_orcamento_R00.pdf)','[LG VC4 escolhida e orçamento parcelado - A04.3 R01](../../../01_Projeto/Equipamentos/LG_VC4_e_orcamento_R01.pdf)')
s=s.replace('[Comparação, decisões e pendências - A04.3 R00](../../Estudos_anteriores/Equipamentos/Comparacao_e_pendencias_R00.md)','[Escolha da VC4 e pendências - A04.3 R01](../../../01_Projeto/Equipamentos/LG_VC4_escolha_e_pendencias_R01.md)')
s=re.sub(r'- \*\*Decisões atuais dos equipamentos:\*\*[^\n]*', '- **Decisões atuais dos equipamentos:** geladeira Electrolux IB6 e lava e seca LG VC4 branca com Wi-Fi escolhidas como referências; tensão da lavanderia e aquecedor pendentes. Pagamento parcelado, teto atualizado para R$ 10.000. Cenário IB6 + VC4 + candidato E15: R$ 10.744,70, excesso de R$ 744,70, pelos preços da pesquisa anterior. Teto atualizado por instrução de Elias.',s)
s=s.replace('[Decisões e orçamento atualizados — A04.2 R01]','[Partido e decisões anteriores — A04.2 R01]')
s=re.sub(r'- \*\*A04.2 R01 é o estudo vigente de implantação;[^\n]*','- **A04.3 R01 é a seleção vigente:** registra a escolha da LG VC4 com Wi-Fi e registra o teto atualizado para R$ 10.000. A04.2 R01 permanece como partido da lavanderia. A recomendação e o ensaio dimensional da VC5 na A04.3 R00 são históricos; as folgas da VC5 não foram validadas para a VC4.',s)
history='- [A04.3 R00 — comparação anterior](../../Estudos_anteriores/Equipamentos/Comparacao_e_pendencias_R00.md): referência dos preços consultados; a escolha atual é a VC4, registrada na R01.\n'
if history not in s: s=s.replace('## Histórico e materiais para futura limpeza\n','## Histórico e materiais para futura limpeza\n\n'+history)
index.write_text(s,encoding='utf-8')

old=OUT/'A04.3_Comparacao_e_pendencias_R00.md'
s=old.read_text(encoding='utf-8')
banner='> **Histórico - substituído pela [A04.3 R01](A04.3_Escolha_VC4_e_pendencias_R01.md):** Elias escolheu a LG VC4 com Wi-Fi. A recomendação da VC5 e seu ensaio dimensional não são a referência de instalação da máquina escolhida.\n\n'
if banner not in s: s=s.replace('## Respostas de Elias incorporadas',banner+'## Respostas de Elias incorporadas',1)
s=s.replace('Complemento vigente da A04.2 R01 para seleção e orçamento','Comparação histórica; seleção atual na A04.3 R01')
old.write_text(s,encoding='utf-8')

old=ROOT/'01_Projeto/Lavanderia/Decisoes_da_lavanderia_R01.md'
s=old.read_text(encoding='utf-8')
s=re.sub(r'> \*\*Complemento posterior:\*\*[^\n]*','> **Complemento posterior vigente:** [A04.3 R01](../A04.3_Comparacao_LG/A04.3_Escolha_VC4_e_pendencias_R01.md) registra a escolha da LG VC4 com Wi-Fi, pagamento parcelado e tensão pendente. Consultar esse complemento para equipamentos e orçamento; o partido desta A04.2 R01 permanece.',s)
old.write_text(s,encoding='utf-8')
print(pdf)
print('R01 em PDF/Markdown/JSON, índice e avisos históricos atualizados.')
