from pathlib import Path
import json, subprocess, sys

WORK=Path(__file__).resolve().parent
ROOT=WORK.parents[2]
OUT=ROOT/'02_Projeto_em_desenvolvimento'/'A04.2_Lavanderia_e_equipamentos'
old=(WORK/'gerar_estudo.py').read_text(encoding='utf-8')
prefix=old.split("head(3,'Equipamentos para escolhermos juntos'")[0]
prefix=prefix.replace('R00','R01')
prefix=prefix.replace("p('LAVA E SECA<br/>sob a pedra',302,308,94,10,BLUE,True)","p('LAVA E SECA LG<br/>modelo a definir',298,308,100,9,BLUE,True)")
prefix=prefix.replace("p('LAVA E SECA',212,458,120,9,INK,True)","p('LAVA E SECA LG',204,455,125,9,INK,True)\np('modelo a definir',214,471,105,8,MUTED)")
# A seleção atual só cita fontes aplicáveis; os catálogos anteriores ficam na revisão histórica.
a=prefix.index('urls={')
b=prefix.index("head(1,",a)
prefix=prefix[:a]+'''urls={
'ib6':'https://loja.electrolux.com.br/geladeira-electrolux-frost-free-inverter-400l-efficient-rapid-freeze-inverse-branca--ib6-/p',
'e15':'https://www.rinnai.com.br/aquecedores-a-gas/linha-prata/e15-1/'
}

'''+prefix[b:]

pages=r'''
head(3,'Equipamentos: decisões atualizadas','Etapa 5 / Geladeira definida e marca da lava e seca confirmada por Elias. Teto atualizado por Elias: R$ 10.000.')
table(['Equipamento','Decisão vigente','Base para o projeto','Pendência'],[
['<b>Geladeira</b>','<b>Electrolux IB6</b><br/>Inverse, branca, 400 litros.<br/>Modelo escolhido por Elias.','Corpo: 60,1 x 186,6 x 74,7 cm (L x A x P). Referência registrada na R00: <b>R$ 3.699</b>.','Confirmar manual de instalação, folgas, abertura das portas e condições comerciais antes de comprar.'],
['<b>Lava e seca</b>','<b>Marca obrigatória: LG.</b><br/>Equipamento único, de abertura frontal, integrado à marcenaria.','Modelo, capacidade, acabamento, tensão, dimensões e preço <b>a definir</b>.','Escolher o modelo LG em conjunto. Depois fechar o vão sob bancada, profundidade total, folgas e abertura frontal.'],
['<b>Aquecedor</b>','Modelo e capacidade pendentes. Rinnai E15 FEH continua apenas em avaliação.','Água quente nas torneiras desejadas; sem necessidade de banho e torneira juntos.','Validar demanda e infraestrutura, tipo de gás, pressão, ventilação e exaustão. Obter cotação.']
],[108,218,237,211],116,9.5)
box(34,374,774,76)
p('Orçamento a recompor com a LG',46,384,742,12,INK,True)
p('R$ 10.000 - R$ 3.699 da referência da IB6 = <b>R$ 6.301 para a lava e seca LG + aquecedor</b>. O total atualizado ainda não está fechado, pois os dois equipamentos dependem de modelo e cotação.',46,408,742,11)
p('O preço da IB6 é a referência já registrada na pesquisa de 09/09/2026, não uma nova cotação desta revisão. Frete, instalação, kits e adaptações não estão incluídos. Teto atualizado para R$ 10.000 por Elias.',34,463,774,9.5,AMBER)
p('A Midea e a IF44 saem da seleção vigente. Os preços, dimensões e totais da combinação anterior ficam apenas no histórico e não dimensionam os móveis da LG.',34,510,774,9.5)
c.showPage()

head(4,'Compatibilização após a escolha','As dimensões da lava e seca serão preenchidas somente depois da definição do modelo LG.')
box(34,113,374,144)
p('Geladeira IB6: corpo e nicho',48,125,346,13,INK,True)
p('A dimensão do produto é referência inicial, não a dimensão do móvel. Verificar folgas térmicas, abertura das portas e gavetas, acesso para manutenção e passagem de entrega.',48,153,346,10)
p('A bancada começa após o espaço instalado da geladeira, já consideradas as folgas necessárias.',48,216,346,10)
box(431,113,377,144)
p('LG: fechar o manual do modelo exato',445,125,347,13,INK,True)
p('A marca foi escolhida; ainda não há código de produto aprovado. A largura, a altura, as profundidades e os afastamentos continuam sem valores de projeto.',445,153,347,10)
p('A pedra terá apoio independente da máquina. Não se presume retirada da tampa do equipamento.',445,216,347,10)
table(['Interface','Condição para fechar o desenho'],[
['LG / instalações','Confirmar no manual da LG escolhida: tensão, tomada e circuito, alimentação de água, escoamento, mangueiras e condições de instalação sob bancada. Não transportar especificações da Midea.'],
['LG / circulação','Conferir profundidade total fechada, porta aberta, gaveta de sabão, filtro e retirada para manutenção. Comparar profundidades de mesma origem e acrescentar espaço de manuseio.'],
['Tanque / cesto','Reservar o volume de sifão e tubulações. Manter cesto embaixo do tanque, ventilado, extraível e transportável; testar o percurso junto à porta da LG.'],
['Aquecedor / aéreos / varal','Uso de um ponto por vez na avaliação inicial. E15 permanece candidato, condicionado à demanda e à instalação. Manter ventilação e acesso; varal oculto sem conflito com equipamentos.'],
['Retorno em L / janela','Faixa de aproximadamente 15 cm de largura confirmada. Comprimento, peitoril, grelhas, giro da esquadria e apoio da pedra ainda a compatibilizar.']
],[190,584],280,9.5)
c.showPage()

head(5,'Registro da revisão R01','Esta revisão atualiza a seleção de equipamentos e substitui a R00 como referência de continuidade.')
table(['Situação','Conteúdo'],[
['<b>Decidido por Elias</b>','Geladeira Electrolux IB6, conforme a opção branca inverse de 400 L apresentada. Lava e seca obrigatoriamente LG; o modelo ainda será escolhido em conjunto.'],
['<b>Requisitos mantidos</b>','R$ 10.000 para os três equipamentos, sem instalação; um morador, possibilidade de dois e visitas de mais quatro; água quente nas torneiras desejadas, sem banho e torneira simultâneos; retorno em L de aproximadamente 15 cm.'],
['<b>Próximos fechamentos</b>','Selecionar modelo LG e aquecedor; confirmar orçamento, gás e tensões; cruzar manuais com medições e desenhar vãos, aberturas, cesto, varal e apoios da pedra.'],
['<b>Limite desta revisão</b>','A escolha da IB6 e da marca LG está registrada. Os móveis continuam em estudo preliminar, sem liberação para fabricação; não houve compra de equipamentos.']
],[169,605],113,9.5)
p('Continuidade dos documentos',34,338,774,12,INK,True)
p('A01.2 permanece como base dimensional das etapas 1 a 3. As cotas de P01 e as evidências dos levantamentos R01/R02 são preservadas. A revisão atual não refaz medições nem reinterpreta o vídeo.',34,362,774,10)
p('A04.2 R00 fica como histórico da comparação inicial. A R01 prevalece para equipamentos, orçamento e pendências; complementa o memorial v2 com as novas decisões de Elias.',34,408,774,10)
p('Fontes e registro das decisões',34,455,774,11,INK,True)
smalllink('Electrolux IB6: fonte da ficha e referência de preço da R00',urls['ib6'],34,480,774)
smalllink('Rinnai E15: candidato em avaliação, ainda não selecionado',urls['e15'],34,505,774)
p('Escolhas: instrução de Elias nesta revisão. Fontes locais: P01, memorial v2, A01.2 e A04.2 R00.',34,530,774,8.5,MUTED)
c.showPage();c.save()
print(PDF)
'''
(WORK/'gerar_estudo_R01.py').write_text(prefix+pages,encoding='utf-8')
subprocess.run([sys.executable,str(WORK/'gerar_estudo_R01.py')],check=True)

oldmd=(OUT/'A04.2_Decisoes_e_selecao_R00.md').read_text(encoding='utf-8')
partido=oldmd.split('## Partido para testar\n\n',1)[1].split('## Candidatos iniciais',1)[0]
video=oldmd.split('## Vídeo recebido\n\n',1)[1].split('## Continuidade documental',1)[0]
video=video.replace('Nesta etapa foram conferidos arquivo e metadados','Na revisão R00 foram conferidos arquivo e metadados')
md='''# A04.2 - Lavanderia e equipamentos

**R01 | 09/09/2026 | Etapas 4 e 5 | Estudo preliminar, sem liberação para fabricação**

[Abrir as cinco pranchas atualizadas](A04.2_Lavanderia_e_equipamentos_R01.pdf)

## Decisões vigentes de Elias

| Item | Decisão | O que ainda falta |
|---|---|---|
| Geladeira | **Electrolux IB6**, versão branca inverse de 400 litros apresentada na comparação. Modelo escolhido. | Conferir instalação, folgas, abertura e cotação final. |
| Lava e seca | **Marca LG obrigatória.** Equipamento único integrado à marcenaria, com acesso frontal. | Escolher modelo, capacidade, acabamento e tensão; obter manual, dimensões e preço. |
| Aquecedor | Ainda não escolhido. Rinnai E15 FEH segue apenas como candidato para avaliação. | Dimensionar pela demanda e infraestrutura; confirmar gás e cotação. |
| Orçamento | **R$ 10.000** para geladeira, lava e seca e aquecedor, sem instalação. | Recompor o total com o modelo LG e o aquecedor selecionados. |
| Uso do apartamento | Um morador, possibilidade de dois, visitas de mais quatro pessoas. | Sem alteração nesta revisão. |
| Água quente | Torneiras desejadas atendidas; não precisa de banho e torneira quente juntos. | Conferir a rede e dimensionar para o uso previsto. |
| Pedra junto à janela | Faixa de aproximadamente **15 cm de largura**, fazendo retorno em L. | Comprimento, altura, apoio e compatibilização com a janela. |

A aprovação da IB6 é uma decisão de projeto. A escolha da marca LG não aprova um modelo específico. Elias atualizou o teto para R$ 10.000. Não houve compra de equipamentos.

## Partido para testar

'''+partido+'''## Ficha atual dos equipamentos

### Geladeira escolhida - Electrolux IB6

- Inverse, branca, 400 L, conforme a opção apresentada e aceita por Elias.
- Dimensões do corpo registradas na pesquisa anterior: **60,1 x 186,6 x 74,7 cm (L x A x P)**.
- Referência de preço da R00, consultada em 09/09/2026: **R$ 3.699** na loja oficial. Não é nova cotação desta atualização.
- As dimensões do corpo não definem o nicho. Conferir manual, folgas térmicas, giro das portas, retirada de gavetas, manutenção e entrega. O ponto inicial da bancada considera o espaço instalado da geladeira.

### Lava e seca - LG, modelo pendente

- Considerar exclusivamente LG na próxima seleção de lava e seca.
- Modelo, capacidade de lavagem/secagem, acabamento, tensão, largura, altura e profundidades continuam pendentes.
- O modelo LG CV3012WC5 citado anteriormente foi apenas uma referência de pesquisa; **não foi escolhido por Elias**.
- As dimensões, folgas, profundidades com porta aberta e condições hidráulicas da Midea não se aplicam à futura LG. Não utilizá-las no dimensionamento.
- Confirmar com o manual do código exato: instalação sob bancada, altura sob apoios, folgas laterais e traseira, tipo de alimentação de água, circuito, mangueiras, porta, gaveta de sabão, filtro e retirada para manutenção.
- Manter estrutura da pedra independente da máquina. Não se presume retirada da tampa.

### Aquecedor - pendente

O E15 FEH permanece candidato, não equipamento aprovado. O dimensionamento depende das vazões dos pontos, temperatura desejada, pressão dinâmica, gás disponível, ventilação e exaustão. A intenção é água quente nas torneiras desejadas, sem necessidade de banho e torneira funcionando juntos. O vídeo não comprova rede de água quente em todos os pontos da unidade.

## Orçamento atualizado

| Parcela | Valor de trabalho |
|---|---|
| Teto informado por Elias | R$ 10.000 |
| IB6 - referência anterior, sujeita a confirmação | R$ 3.699 |
| **Saldo de referência para LG + aquecedor** | **R$ 6.301** |
| Preço da LG | Pendente do modelo e da cotação |
| Preço do aquecedor adequado | Pendente do dimensionamento e da cotação |
| Total atualizado dos três | **Ainda não fechado** |

R$ 10.000 - R$ 3.699 = R$ 6.301. Esse saldo é para os **dois equipamentos restantes juntos**. Não é uma reserva só para a LG nem uma promessa de cabimento no teto. Se a cotação da IB6 mudar, o saldo também muda.

Frete, instalação, kits e adaptações não estão incluídos. A distribuição anterior de R$ 3.200 / R$ 2.900 / R$ 2.900 foi substituída por este cálculo. Os totais e o saldo de R$ 2.102 vinculados à máquina Midea pertencem somente à R00 e não são o orçamento vigente.

## Compatibilização e próximos fechamentos

1. Selecionar o modelo LG em conjunto e consultar seu manual; não substituir por outra marca sem nova decisão de Elias.
2. Dimensionar o aquecedor para a demanda prevista, conferir gás/tensões e obter cotações para recompor o teto de R$ 10.000.
3. Medir peitoril, grelhas, abertura circular, rebaixos, volumes técnicos e eixos dos pontos. Definir o comprimento do retorno em L.
4. Desenhar implantação cotada com IB6 e a LG escolhida: folgas, portas, cesto sob tanque, varal, manutenção e apoios da pedra.

Para avaliar avanço de portas na circulação, comparar profundidades de mesma origem e reservar espaço de manuseio. Tanque, sifão e tubulações precisam de volume próprio; o cesto continua ventilado, removível e abaixo do tanque.

## Vídeo recebido

'''+video+'''## Histórico e prioridade documental

- Esta R01 prevalece sobre a seleção e o orçamento da A04.2 R00.
- Geladeira IF44 e máquina Midea ficam fora da seleção vigente; as comparações anteriores são mantidas como histórico, sem aplicação automática de suas medidas.
- A04.2 R00, A04.1 R00 e A01.2 continuam preservadas. A base A01.2 permanece referência dimensional das etapas 1 a 3.
- O memorial v2 e as decisões anteriores continuam válidos nos demais pontos; esta revisão acrescenta a escolha da IB6 e a exigência da marca LG.

## Fontes

- Instrução de Elias nesta revisão: escolha da geladeira IB6 e exigência de lava e seca LG.
- [Electrolux IB6 - ficha e referência de preço utilizadas na R00](https://loja.electrolux.com.br/geladeira-electrolux-frost-free-inverter-400l-efficient-rapid-freeze-inverse-branca--ib6-/p).
- [Rinnai E15 - candidato ainda em avaliação](https://www.rinnai.com.br/aquecedores-a-gas/linha-prata/e15-1/).
- Fontes locais: planta P01, memorial v2, levantamentos A01.1 R01/R02 e base A01.2.

Não foi realizada nova pesquisa de preços ou seleção de modelo LG nesta atualização documental.
'''
(OUT/'A04.2_Decisoes_e_selecao_R01.md').write_text(md,encoding='utf-8')

data=json.loads((OUT/'A04.2_Registro_R00.json').read_text(encoding='utf-8'))
data['revisao']='R01'
data['status']='estudo preliminar; geladeira IB6 escolhida; marca LG obrigatória; modelos LG e aquecedor pendentes'
data['equipamentos']={
 'geladeira':{'marca':'Electrolux','modelo':'IB6','cor':'branca','tipo':'inverse','capacidade_l':400,'status':'modelo escolhido por Elias','dimensoes_corpo_cm_LAP':[60.1,186.6,74.7],'nicho_dimensionado':False},
 'lava_seca':{'marca':'LG','marca_obrigatoria':True,'modelo':None,'capacidade_lavagem_kg':None,'capacidade_secagem_kg':None,'cor':None,'tensao_v':None,'dimensoes_cm':None,'preco_brl':None,'status':'marca escolhida; modelo pendente'},
 'aquecedor':{'modelo':None,'capacidade_l_min':None,'tipo_gas':None,'preco_brl':None,'candidato':'Rinnai E15 FEH','status':'pendente de dimensionamento e escolha'}
}
data.pop('reserva_orcamento_brl',None)
data.pop('precos_observados',None)
data['orcamento_atual']={'teto_brl':10000,'ib6_referencia_R00_brl':3699,'saldo_LG_mais_aquecedor_brl':6301,'total_conjunto_brl':None,'nova_cotacao_nesta_revisao':False,'instalacao_incluida':False,'frete_incluido':False}
data['fontes']={k:v for k,v in data['fontes'].items() if k in ['ib6','e15']}
data['historico']={'revisao_anterior':'A04.2 R00','comparacoes_descartadas_da_selecao_atual':['Midea MFA01D110B/WK','Electrolux IF44'],'dimensoes_Midea_aplicaveis_a_LG':False}
(OUT/'A04.2_Registro_R01.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print('R01: PDF, memorial e registro atualizados.')
