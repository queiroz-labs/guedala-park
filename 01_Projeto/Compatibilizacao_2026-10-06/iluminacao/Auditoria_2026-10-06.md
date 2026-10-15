# Auditoria de iluminação, tomadas e acabamento - 06/10/2026

Escopo: documentos locais vigentes em `C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\01_Projeto`, com pesquisa oficial consultada em 06/10/2026. Fontes originais preservadas. Esta entrega encerra reconciliação, conferência e contas identificadas abaixo; não encerra seleção comercial, medições ou projeto executivo.

## Estado reconciliado

| Item | Estado vigente | Evidência local e consequência |
|---|---|---|
| Cozinha/lavanderia 3000 K | Aprovado | `Painel_de_decisoes.md`, seção «Temperatura de cor escolhida»; `Iluminacao/Estudo_integrado_2026-09-22.md`, atualização 27/09. Não reabrir temperatura. |
| Três comandos físicos independentes | Aprovado | Mesmo estudo, seção «Comandos aprovados»: C1 teto cozinha liga/desliga; C2 bancada liga/desliga + regulagem; L1 teto lavanderia liga/desliga. Separação de comandos não decide circuitos de proteção nem automação. |
| Plafons brancos, sobrepor, próximos ao teto, difusor/coordenados | Aprovado como aparência | `Iluminacao/Cozinha_lavanderia_selecao_R01_2026-09-27.md`, resultado. Produtos, tamanhos, quantidades e pontos ainda abertos. |
| Formato quadrado cozinha | Aprovado condicionado | R01, «Conferência do giro»: preservar abertura completa das portas. O aceite não aprova EVO/modelo/tamanho final nem estende quadrado à lavanderia. |
| EVO STH21967/30, 41 × 41 × 3,8 cm | Candidato | R01; planta nominal deixa 13,4 cm além do envelope de giro A. Conferência atual do fabricante não concluída, veja fontes. |
| Lavanderia, corpo até 30 cm, teste 28 cm em (64,5;55) | Proposta técnica atual | `Compatibilizacao_2026-09-30/Luz_varal.md`, direção/faixa disponível. Supera geometria inicial da R01; 28 cm não é produto encontrado. |
| Decorlux LP1233 | Candidato econômico | R01; dados elétricos/IP/montagem revalidados hoje. Difusor saliente/forma diferente: não adotar como par coordenado por inferência. |
| ECO na lavanderia | Não priorizado | R01, «Alternativas que não avançaram»: manual específico restringe umidade; não é veto universal a todo produto IP20. Sem nova reversão encontrada. |
| C2, eixos sob B/C 42/30 cm e perfis 65,7/50,7 | Proposta técnica | `Compatibilizacao_2026-09-28/Micro_C2.md`, seção 3. Conjunto de fita/perfil/fonte/regulagem não escolhido. |
| Torre automática por pressão, tampa preta, plugue 20 A, 127 V, área seca | Aprovado funcionalmente | Painel, «Torre da cozinha aceita»; `Compatibilizacao_2026-09-28/Torre_gavetas.md`. Modelo e furação não aprovados. |
| Tomada fixa lavanderia 20 A acessível | Aprovado funcionalmente | Painel, «Tomada fixa na lavanderia aceita». Sem posição/circuito/modelo executivos. |
| Caixas G1/G2/G3 de 50 cm | Objetivo a preservar | Torre_gavetas, direção; sem redução automática por torre. Nenhuma localização demonstrada integralmente. |
| Algodão Egípcio fosco, resistente à limpeza | Cor/acabamento aprovados | `Fechamento_cozinha_lavanderia_2026-09-27.md`, «Pintura - acabamento aprovado». Marca/linha/código, substrato, lata familiar e área não fechados. Acetinado foi preterido. |
| Branco Itaúnas, faixa parede de 10 cm como referência, borda reta suavizada | Aprovado como direção | Fechamento, «Pedra - escolha». Cota executiva/encontros permanecem condicionados. |
| Limite R$1.200 e saldo R$250,96 iluminação | Histórico superado | Estudo_integrado, «Critério vigente - sem teto de orçamento, 22/09». Não usar saldos antigos para eliminar alternativas. Bom custo-benefício vigente, sem compra autorizada. |

A busca nos Markdown de compatibilização de 30/09 a 04/10 não encontrou nova alteração de temperatura/comandos/pintura/torre. Alterações mais recentes de C2 dizem respeito ao armazenamento; «C2» também identifica o grupo de luz da bancada, por isso os dois sentidos não devem ser confundidos.

## Conferências concluídas e reproduzíveis

Os três cálculos originais foram executados com escrita redirecionada para esta pasta, conservando os caminhos de leitura originais. Os JSON reproduzidos tiveram **SHA256 idêntico** aos originais, byte a byte:

- `Resultados_micro_c2.json`: quatro verificações do script passaram; comprimentos, geometria e cenário de sombras reproduzidos.
- `Resultados_torre_gavetas.json`: cinco verificações passaram; distâncias a cuba, curso e sensibilidade de fundo/recuo reproduzidos.
- `Resultados_luz_varal.json`: cálculo geométrico/interseções reproduzido; igualdade de hash confirma repetição, não qualidade fotométrica ou conformidade técnica.

Reprodução: `node entregas/iluminacao/reproduzir_calculos.cjs`, na pasta desta tarefa. Originais não alterados. Logs e JSON reproduzidos guardados em `evidencia/`, como apoio de conferência. A escrita dos derivados Markdown/HTML históricos foi suprimida no reprodutor para evitar entregar documentos com status ou links antigos. O relatório e os cálculos complementares são as entregas novas.

### Bancada C2: complemento de seleção sem escolher produto

Base atual: perfis 65,7/50,7 cm, menos 1 cm por ponta para terminais como hipótese local. Fórmula: comprimento ativo = passo × piso((perfil - 2)/passo). Nunca arredondar o corte para cima.

| Passo hipotético/documental | LED sob B | LED sob C | Total | Fluxo com 800 lm/m úteis |
|---|---:|---:|---:|---:|
| 2,08 cm, candidatura histórica STL24824/30 | 62,40 cm | 47,84 cm | 1,1024 m | 881,92 lm |
| 2,5 cm, ensaio principal existente | 62,50 cm | 47,50 cm | 1,10 m | 880 lm |
| 5 cm | 60 cm | 45 cm | 1,05 m | 840 lm |
| 10 cm | 60 cm | 40 cm | 1,00 m | 800 lm |

O passo de 2,08 é aproximado na documentação anterior: serve para triagem; usar marcação e revisão da fita real para cortar. O ganho de 0,24 cm no total frente ao ensaio principal não revalida os mapas de luz. Não recalculamos lux atribuindo fotometria real a uma fita sem conjunto escolhido.

Para a candidatura histórica de 15 W/m, 12 V: 1,1024 × 15 = **16,536 W** de LED; corrente DC **1,378 A**. Com controlador Shelly candidato de consumo declarado <1,2 W, carga estimada superior de comparação **<17,736 W**. Uma fonte nominal de 25 W teria saldo aritmético >7,264 W; isso não especifica fonte nem atende automaticamente temperatura, ventilação, desclassificação de potência, perdas e instruções reais. O Shelly revalidado aceita 12/24 VDC e 4 A por canal/10 A total; corrente do LED calculada fica abaixo do limite nominal de um canal. A arquitetura preserva comando físico e regulagem como função; não aprova automação na cozinha.

**Não ligar o controlador DC diretamente à rede 127 V.** Entrada 127 V pertence à fonte adequada ainda a selecionar, cuja saída e regime devem corresponder à fita/controlador.

Se a fita candidata publicar 1000 lm/m nominais e o alvo de estudo continuar 800 lm/m após difusor, o conjunto teria que conservar **80% do fluxo**: 800/1000. Perda maior impede tratá-lo como equivalente ao ensaio de 800. Transmissão/ótica real não conhecidas; watts e lumens nominais não substituem fluxo útil nem mapas com a pessoa.

O ensaio reproduzido normal com pessoa dá médias diretas de cerca de 513 lx no preparo e 522 lx sobre pia; a cena air fryer com pessoa cai a 265/493 lx, com mínimo direto zero em parte do preparo. São resultados do modelo documental, sem reflexões/depreciação/ótica real. Não converter em promessa instalada ou conformidade normativa.

### Torre e tomada para air fryer

Para a potência documental de 1400 W em 127 V: corrente nominal aritmética **11,02 A**. A versão QTMOV identificada como «10» admite 1270 W; faltam **130 W**. A versão «20» declara **2032 W em 127 V**, confirmados hoje online e no PDF. Saldo aritmético **632 W** não autoriza uso simultâneo nem dimensiona circuito. Não substituir limite publicado por 20 × 127 = 2540 W.

Nova divergência explicitada: página do produto anuncia cabo 1,5 m; manual anuncia 1,6 m. A tomada upstream e o percurso não podem ser localizados contando com os 10 cm adicionais. Código preto/20 A, plugue de entrada, corrente do conjunto e envelope instalado seguem sem vínculo dimensional completo. Ficha/página 10 A não liberam versão20 nem furo.

A página do manual publica 60 cm de áreas úmidas e atribui isso à NBR5410; o PDF consultado não traz a frase. Esta entrega confirma a divergência de documentos. **Não confirma a alegação normativa**, nem transforma teste de distância à cuba em aprovação. Preservar essa condição como instrução publicada do fornecedor a esclarecer, cruzando área molhada real/água do filtro e responsável elétrico.

O corte reproduzido conserva 9,2 cm brutos atrás da caixa; com fundo18 mm e margens de teste5 mm por lado, envelope máximo6,4 cm. Recuo adicional5 mm reduz a5,9. Corpo6,4 teria saldo zero no caso limite; anel, cabo, ferramenta/manutenção não ficam demonstrados. Não escolher redução de gavetas ou remoção de fundo estrutural.

### Pintura: especificação preparada

Suvinil Fosco Sempre Limpo continua uma candidatura que reúne acabamento fosco e resistência à limpeza; página oficial lista uso em cozinhas e superfícies internas como massa corrida/drywall/gesso. Não comprova adequação a toda região de respingos, substrato existente ou lata familiar. Não escolher linha por inferência.

A página consultada declara 2–3 demãos e até120 m² acabados para18 L ou24 m² para3,6 L. Tratar como máximo publicado do produto específico, sem calcular compra: área líquida/base e identidade da lata desconhecidas. Fórmula pronta quando houver levantamento: A líquida = soma(largura × altura de pintura) - vãos/trechos sem tinta; quantidade depende do rendimento acabado da revisão efetivamente escolhida. Não multiplicar novamente por demãos quando o rendimento informado já é acabado.

Cor aprovada deve ser reconciliada com código/etiqueta da lata; não usar o código RM181/Branco Neve da página aberta como código de Algodão Egípcio. Linha, lote, validade, estado e volume utilizável da lata familiar20 L continuam a conferir. Pesquisa não demonstrou necessidade de substituição.

## Fontes oficiais atuais e limites da consulta

Todas consultadas em **06/10/2026**; links mantidos para conferência. Sem Firecrawl, preços novos, compra ou contato.

1. [Manual QTMOV online](https://qtmov.com.br/manuais/mini-totem-automatico/), «Potência Máxima», «A embalagem contém», «Cuidados». Revalidou2032W/127V; cabo1,6; publicou60cm. [PDF oficial, páginas1–3](https://qtmov.com.br/wp-content/uploads/2023/08/Manual-de-instalacao-Mini-Totem-Automatico.pdf): mesma tabela, sem frase60cm. Extração textual conferida; captura foi solicitada, sem validação visual de layout nesta entrega.
2. [Página QTMOV](https://qtmov.com.br/produtos/linha-pratik/mini-totem-automatico/), «Descrição/Características elétricas»: ainda10A, cabo1,5m, Øaparente76/furo65mm. Sem correspondência fechada com código20A.
3. [Decorlux LP1233 loja oficial](https://www.lojadecorlux.com.br/iluminacao/luminarias/luminaria-tipo-plafon-plastico-led-12w-3000k-100-240v-br), «Descrição/Características»: 12W,100–240VAC,3000K,1080lm,IP65,teto. Dimensões23×9×21 permanecem explicitamente da embalagem. Corpo14×5 vem do desenho já lido no estudo local, sem nova leitura visual hoje.
4. [Shelly Plus RGBW PM fabricante](https://kb.shelly.cloud/knowledge-base/shelly-plus-rgbw-pm), «Main features/Supported loads/Specifications»: fitas monocolor12/24VDC, entrada botão/interruptor/potenciômetro, regulagem por botão, <1,2W,4A/canal,10A total,42×37×12±0,5mm, temperatura até40°C. Revalida capacidade nominal do controlador candidato, não o conjunto instalado.
5. [Suvinil - tinta para cozinha](https://loja.suvinil.com.br/suvinil-indica/tinta-para-cozinha) e [Fosco Sempre Limpo](https://loja.suvinil.com.br/produto/suvinil-fosco-sempre-limpo?color=RM181), «Onde aplicar/Quanto rende»: referência técnica atual, sem aprovação de marca/linha. URL abre Branco Neve, não a cor aprovada.
6. [Stella EVO](https://stella.com.br/produtos/detalhes/plafon-de-sobrepor-evo-134), [fita All Light12V EVO](https://stella.com.br/produtos/detalhes/fita-all-light-12v-evo-467) e [família fitas](https://stella.com.br/produtos/fitas): falha de acesso na rodada (erro/timeout502). Dados atuais não revalidados. Mantêm-se dados datados27/09 e22/09 com essa limitação; não confirmar estoque, revisão ou ficha atual por anúncios terceiros.

## Pendências reais e próxima ação por natureza

| Frente | O que falta para encerrar | Depende de nova decisão? |
|---|---|---|
| C1 cozinha | Revisão EVO/IES35,65W versus comercial30W; produto final, cobertura; teto/ponto/giro real | Aceite do produto após evidência; formato já fechado |
| L1 lavanderia | Par coordenado compatível com30cm de teste; fotometria/umidade; duto/mecanismo/roupa/cotas | Aceite da opção apresentada; sem estender quadrado automaticamente |
| C2 bancada | Fita/perfil/difusor/fonte compatíveis; terminais/corte; comando/cabo; localização ventilada/manutenível | Seleção concreta; funções já aprovadas |
| Torre | Código preto20A, desenho ambos estados/anel/cabo;60cm/água; fundo/travessa/acesso e ponto | Primeiro obter dados técnicos; decisão nova só se exigir mudar aprovado |
| Tomada lavanderia | Posição/cabo/água/armários/varal e projeto elétrico | Não precisa reabrir função; aferição/técnico |
| Pintura | Identificar lata20L; substrato/área; linha/código/rendimento/compatibilidade | Escolha de linha se lata não atender; cor/fosco fechados |
| Acabamento pedra | Encontros/rodabanca/tomadas/cocção com dimensões reais | Direção já aceita; técnico/medição |

Não há pergunta bloqueante nova necessária para executar as conferências desta rodada. A primeira informação doméstica útil é: **«Qual é a marca/linha, código da cor e validade da lata de20L?»** A pergunta identifica produto existente e evita substituir tinta sem evidência. Não bloqueia iluminação ou torre. Mediçōes da unidade, ensaio de conjuntos e responsabilidade técnica permanecem pendentes, mesmo após checklist preparado.

