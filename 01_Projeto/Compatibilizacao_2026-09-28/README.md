# Compatibilização e avanço do projeto — 28/09/2026

**Continuidade em 30/09 — cesto:** [frente e retirada do saco](../Compatibilizacao_2026-09-30/Cesto_retirada.html) incorpora os volumes antes ausentes da frente/rodapé/painel e testa extração em duas etapas. Consultar a nova rodada para a projeção completa de operação; ensaios abaixo continuam como histórico.

**Continuidade — torre × gavetas:** [prancha](Torre_gavetas.html) e [memória](Torre_gavetas.md). Corte explícito substitui a triagem genérica de faixas 5/7/9/12 cm para o novo ensaio: 9,2 cm brutos atrás da caixa de 50, 7,4 com fundo de 18 mm. Testados recuo, fundo, curso e três posições. Ficha 10 A usada só como referência; variante 20 A, anel e acesso superior continuam a conferir. Caixas preservadas. Os cálculos iniciais abaixo ficam como histórico da primeira rodada.

**Continuidade — micro e C2:** [prancha com corte e mapas](Micro_C2.html) e [memória](Micro_C2.md). Apoio aberto proposto com 47 cm de profundidade; perfis B/C a 42/30 cm da parede. Novo ensaio inclui purificador, apoio, pessoa e air fryer, com comprimentos ativos reais de teste 62,5 + 47,5 cm. Supera o ensaio sem sombra dos aparelhos para essa nova geometria; manter os cálculos iniciais abaixo como histórico.

**Continuidade — corte de cocção desenvolvido:** [prancha cotada](Corte_coccao.html) e [memória técnica](Corte_coccao.md). Detectada divergência Venax entre 3/5 cm da tabela específica e 10 cm do texto geral; a conclusão lateral fica condicionada ao esclarecimento. Quantificados tolerâncias, gargalo frontal, apoio e projeção externa. Esta continuação inclui consulta a fontes oficiais em 28/09, além da base local usada na primeira rodada.

**Rodada de desenvolvimento autônomo solicitada por Elias.** Preservadas as escolhas vigentes até 27/09. As propostas abaixo resolvem contas e indicam limites para detalhamento; não são novas aprovações atribuídas ao usuário. Dimensões da planta e dos estudos, ainda sem levantamento do apartamento.

**Abrir o [caderno visual de conferência](Caderno.html)**. Contas reproduzíveis em [calcular.cjs](calcular.cjs), dados completos em [Resultados.json](Resultados.json) e [briefing técnico](Briefing_tecnico.md) pronto para uso posterior com os fornecedores.

## O que avançou

| Frente | Resultado desta rodada | Aplicação no projeto |
|---|---|---|
| Bancada de preparo | Compatibilização do PE12G, air fryer e cuba com pia de 65 cm; discrepância identificada no 3D R09 | Usar a implantação cotada abaixo como referência técnica mais recente dessa cena |
| Luz da bancada | Cálculo ponto a ponto com o IES salvo e pré-dimensionamento dos dois trechos C2 | Reserva de 50,7 + 65,7 cm de perfil; pesquisar desempenho do conjunto, mantendo regulagem |
| Cesto | Sensibilidade conjunta de pedra, eixo e ângulo; reserva adicional de acesso de apenas 5,2 mm | Incluir teste da boca e retirada do saco na especificação da ferragem |
| Torre | Comparação do espaço traseiro e perda de gaveta caso se tente acomodá-la | Não sacrificar a profundidade das três gavetas antes de obter seção real da torre |
| Gaveteiro | Gabaritos máximos de frascos e perdas explícitas por divisórias | Organizador removível dimensionado por envelope, sem compra prematura |
| Mesa | Sensibilidade à coluna de 12–24 cm | A coluna maior pode ser absorvida por posição da cadeira central no cenário; não forçar base estrutural pequena |
| Escritório | Tolerâncias combinadas de sofá e porta | A margem quase zera com alterações pequenas; manter dependência objetiva da geometria real |
| Quarto | Consequência das portas abertas sobre a passagem de 54 cm | Detalhar ferragens e acesso antes de transformar o envelope fechado em marcenaria executiva |

## 1. Cozinha: composição que fecha, mas sem sobra de montagem

Mantida a ordem a partir da lavanderia: **60 cocção + 65 pia + 61,9 preparo + 80,1 geladeira + 85 entrada = 352 cm**. O saldo nominal é **zero**. Isso não exige reduzir móveis agora; exige que laterais adicionais, enchimentos e tolerâncias apareçam no corte antes da contratação. As folgas dos aparelhos não são espaço de compensação para painéis.

Na seção transversal de 155 cm:

- Pedra com 63 cm: **92 cm nominais** diante dela.
- Geladeira, incluindo reserva traseira, com 84,75 cm: **70,25 cm nominais** na seção correspondente. Não confundir esse valor com os 75,25 cm entre mesa recolhida e frente da geladeira, medidos em outro sentido.
- Pia externa de 43 cm centralizada no módulo de 65: **11 cm por lado**. São faixas em planta, antes de recorte, apoios, torneira e fabricação da pedra.

Fontes: [cotas documentais](../Medidas/Dados_das_medidas_R00.json), [aparelhos R03](../Cozinha/Aparelhos_compatibilizacao_R03_2026-09-27.md).

### Cena de uso da air fryer na cozinha

Retomado o arranjo já estudado no [detalhamento dimensional](../Cozinha/Detalhamento_dimensional_R00.md), atualizado para a pia de 65 cm. Origem **s = 0 na extremidade do gaveteiro junto à geladeira**, crescendo em direção à pia; **t = 0 na parede**, crescendo para a frente. Centímetros.

| Elemento | Faixa s | Faixa t | Altura sobre piso |
|---|---:|---:|---:|
| Gaveteiro/preparo | 0–61,9 | 0–63, pedra | 92 |
| PE12G — corpo | 5–21 | 10–52 | 92–127 |
| Air fryer — corpo | 31–57,4 | 10–46 | 92–121,5 |
| Cuba — envelope externo centrado | 72,9–115,9 | Conforme recorte/torneira | A conferir |

**Entre corpos: 10 cm.** O espaço de ar entre aparelhos é compartilhado; não somar 5 cm do purificador mais 10 cm da air fryer como se fossem duas faixas necessariamente separadas. Isso não valida a exposição do purificador a calor: apenas evita uma falsa impossibilidade geométrica.

A reserva lateral da air fryer termina em **s = 67,4**, entrando **5,5 cm** na faixa sólida do módulo da pia. Ainda restam **5,5 cm até o contorno externo da cuba**, em vez dos 3 cm do estudo anterior com pia de 60. Essa diferença **não é afastamento de segurança de água nem autorização para operar junto a respingos**.

No 3D R09, os corpos estavam separados por **5,6 cm**, e o escorredor se sobrepunha à air fryer na cena com varal em uso. A cena corrigida no caderno retoma as coordenadas acima e guarda o escorredor seco no gabinete, destino já aprovado. Na cena normal, air fryer na lavanderia e escorredor disponível junto à pia. Cafeteira não foi acrescentada simultaneamente porque suas medidas continuam adiadas. O 3D R09 publicado permanece ilustrativo e não foi republicado nesta rodada.

Reservas documentadas: purificador com envelope inicial 26 × 52 × 57 cm; air fryer com 10 cm atrás/lados/acima. Acima do filtro, limite de referência a 149 cm. Sob o apoio do micro com face inferior a 153,2 cm, existem só **4,2 cm** além dessa reserva, antes de perfil de luz, cabo e fixações. Perfil que desça 1 cm deixaria **3,2 cm**. Compatibilizar fonte/driver fora desse pequeno intervalo.

### Torre: limite definido sem reduzir a despensa

O furo de 6,5 cm pertence ao candidato pesquisado; a variante automática preta 20 A ainda não está selecionada. A tampa de 7,6 cm, anel, corpo, cabo e manutenção podem exigir mais espaço que o furo.

Triagem adotada: **6,5 cm + 1 cm de cada lado = 8,5 cm**. O centímetro é reserva matemática deste ensaio, não afastamento elétrico, resistência comprovada da pedra ou instrução do fabricante.

| Faixa traseira efetivamente livre | Saldo diante dos 8,5 cm |
|---|---:|
| 5 cm, referência anterior | −3,5 cm |
| 7 cm, caso o avanço da bancada seja totalmente aproveitado atrás | −1,5 cm |
| 9 cm | +0,5 cm |
| 12 cm | +3,5 cm |

Os 7 cm não estão medidos nem automaticamente disponíveis. Mesmo que um círculo de 6,5 cm caiba matematicamente numa faixa de 7 cm, sobrariam só 2,5 mm por lado do furo; isso não prova instalação.

Encurtar a caixa de 50 para 45 cm reduziria o útil de **47 para 42 cm** e perderia **10,6% da área de cada gaveta**, mantendo as mesmas espessuras. Não aplicado: a organização aprovada já usa os 47 cm. Direção de trabalho: obter primeiro a seção integral da torre e estudar posição/volume técnico; só comparar redução de gavetas se o conflito real exigir. A instrução de distância de área úmida registrada para o candidato também continua pendente. [Base da torre](../Cozinha/Torres_retrateis_avaliacao_2026-09-27.md).

### Forno: tabela de aceitação para o corte

Bancada a 92, frente externa de forno de 61, separação documental de 20 cm. Se **d** é quanto o cooktop desce a partir da superfície, o topo do forno pode chegar a **72 − d**; sua borda inferior, a **11 − d**.

| d, hipótese | Topo máximo do forno | Borda inferior máxima |
|---:|---:|---:|
| 4 | 68 | 7 |
| 5 | 67 | 6 |
| 6 | 66 | 5 |
| 7 | 65 | 4 |
| 8 | 64 | 3 |

A frente a 5–66 cm desenhada só atende essa conta se **d ≤ 6 cm**. Nenhum valor de d foi inventado como medida real. Desenho do suporte, corpo embutido, nicho, gás e ventilação continua necessário; os 18 cm da gaveta baixa não se repetem sob o forno.

## 2. Iluminação: primeiro cálculo com a fotometria disponível

Usado o [IES Stella salvo em 27/09](../../03_Referencias/Pesquisas_2026-09-27/EVO_STH21967-30.ies), identificado STH21967/30, ensaio de 2021. Cabeçalho: **2329 lm e 35,65 W**, diferentes da ficha comercial já registrada de 2300 lm/30 W. A integração numérica da curva recupera **2329,09 lm**: o arquivo foi interpretado consistentemente. Isso não confirma que a unidade atualmente vendida seja idêntica ao ensaio.

Fonte equivalente no centro do corpo: longitudinal a **133,5 cm da interface com a cocção**, transversal a **109 cm da parede**, plano emissor a **253,2 cm** no teto hipotético de 257. Posição do desenho R09 mantida; não foi escolhido um novo ponto elétrico.

Método: interpolação da intensidade em candelas; `E = I × cos(θ) / distância²`, com distância em metros. Planos a 92 cm para bancada e zero para piso. Aéreos e micro representados por envelopes opacos. **Contribuição direta inicial**, sem reflexões, luz natural ou depreciação, e sem obstrução pelos objetos sobre o tampo. Os retângulos de avaliação incluem áreas ocupadas por aparelhos/cuba: são comparação de cobertura, não superfície de preparo inteiramente livre.

| Região amostrada | Pontos | Média direta | Mínimo–máximo |
|---|---:|---:|---:|
| Preparo: 60 × 50 cm | 120 | **253 lx** | 180–323 lx |
| Pia: 65 × 50 cm | 130 | **235 lx** | 156–320 lx |
| Faixa do piso: 267 × 55 cm | 297 | **134 lx** | 96–159 lx |

Os envelopes dos aéreos não bloquearam os raios desses pontos nessa implantação. Isso não comprova ausência de sombra de pessoas/aparelhos. O arquivo usa fonte pontual equivalente; o corpo real distribui luz numa área, portanto os números são uma aproximação e não uma previsão completa de lux instalados.

### C2: dimensão preliminar dos trechos e comparação de fluxo

Preservados 3000 K, regulagem e comando independente. Reservar, para desenvolvimento:

- **Sob C:** 54,7 − 2 − 2 = **50,7 cm**.
- **Sob o apoio aberto do micro/B:** 69,7 − 2 − 2 = **65,7 cm**.
- Total geométrico de perfil: **116,4 cm**. Ajustar corte da fita ao passo real; não cortar 116,4 cm como peça única. Os recuos de 2 cm são hipótese de montagem, não regra do produto.

Simulação dos perfis: linha ideal difusa, emissão lambertiana, a 152,2 cm do piso; C a 30 cm da parede, B a 35. Não instalar na carcaça do micro nem na zona do depurador. O apoio do micro ainda precisa de desenho completo de profundidade e ventilação; a posição de C2 depende desse apoio.

Para testar sombra humana, inserido volume opaco de **45 × 30 × 175 cm**, centralizado sucessivamente diante de cada área, a 72–102 cm da parede. É um cenário, não medida de Elias nem modelo antropométrico validado. Nele, a contribuição média do teto cai para **137 lx no preparo e 151 lx na pia**.

| Fluxo útil da linha, já após difusor | Teto + linha, sem pessoa: preparo / pia | Teto + linha, com pessoa: preparo / pia |
|---:|---:|---:|
| 400 lm/m | 457 / 435 lx | 340 / 350 lx |
| 600 lm/m | 558 / 534 lx | 442 / 450 lx |
| 800 lm/m | 660 / 634 lx | 544 / 549 lx |

**Direção técnica inferida:** começar a seleção por conjuntos reguláveis capazes de entregar aproximadamente **800 lm/m úteis após perfil/difusor**, em vez de escolher apenas por W/m. No cenário simplificado supera o alvo comparativo de 500 lx médios escolhido para esta rodada. **Não é norma, especificação final nem aprovação de desempenho:** com pessoa, mínimos de 256/224 lx mostram que média não resolve uniformidade. Conferir fotometria real, posição, reflexos, sombra do filtro e eventual reposicionamento do perfil.

Uma ficha de fita nua com 800 lm/m não comprova 800 lm/m após perdas. Não dimensionar potência da fonte antes de definir fita, tensão, comprimento de corte, controle e instruções do fabricante. Manter driver acessível, ventilado e afastado dos volumes úmidos/quentes. Nenhuma nova luminária da lavanderia foi presumida como necessária.

## 3. Cesto: acrescentar tolerância de acesso ao teste de colisão

A R08 já mostrou o giro sem colisão com uma reserva hidráulica ideal. Esta rodada acrescenta a sensibilidade da **boca fora da projeção da pedra**.

Com eixo a 56 cm, pedra a 75, profundidade 25, altura 45 e abertura de 55°, a borda traseira da boca fica em **78,52 cm**. São **3,52 cm além da pedra**. Exigindo a reserva comparativa de 3 cm, sobra somente **0,52 cm = 5,2 mm**.

| Alteração isolada | Boca além da pedra | Atende 3 cm no modelo? |
|---|---:|---|
| Nominal, 55° | 3,52 cm | Sim, com pouca sobra |
| Abre só 54° | 2,71 cm | Não |
| Pedra avança mais 1 cm | 2,52 cm | Não |
| Eixo fica 1 cm mais atrás | 2,52 cm | Não |
| Abre 56°, cenário comparativo | 4,33 cm | Sim; curso não adotado |

Ângulo mínimo calculado para 3 cm: **54,36°**. A tolerância até 55° é só **0,64°**. Portanto, não substituir a ferragem por outra “aproximadamente 55°” sem corte real. O fato de a boca sair da sombra da bancada também não comprova a retirada do saco cheio.

Mantidos 45 × 25 × 45 cm, eixo e curso como referências. Não deslocar eixo isoladamente: isso altera a reserva traseira de hidráulica, a ligação à frente e o espaço de operação. Próximo detalhe é conjunto **ferragem + frente + boca + engates do saco**, com ensaio da retirada e da remoção da armação para sifão. Fonte: [R04](../Lavanderia/Cesto_basculante_calculo_R04.md) e [R08](../Lavanderia/Tanque_cesto_compatibilizacao_R08.md).

## 4. Armazenamento: gabaritos que podem orientar seleção

Preservado útil de teste do gavetão **52,7 × 47 cm** e setor frontal esquerdo de **27,7 × 19 cm**. Com margem externa de 5 mm e divisórias de 2 mm, o máximo por posição é:

| Grade | Quantidade | Envelope máximo por frasco, incluindo tampa |
|---|---:|---:|
| 6 × 4 | 24 | **4,28 × 4,35 cm** |
| 6 × 3 | 18 | **4,28 × 5,87 cm** |
| 5 × 4 | 20 | **5,18 × 4,35 cm** |

Em uma grade 6 × 4, frascos circulares maiores que cerca de **4,28 cm de diâmetro** não cabem com essas divisórias. A folga de pega e a remoção do organizador precisam de teste. Não reduzir a meta de 18–24 nem comprar frascos por esse cálculo; ele define o filtro de pesquisa.

Na faixa de bebidas **22 × 45 cm**, o inventário solicitado soma seis leites, três sucos, óleo e azeite: **11 volumes** antes de molhos/enlatados. A antiga grade ilustrativa 2 × 5 só comporta dez posições; portanto não demonstra o inventário completo. Os formatos e alturas reais seguem necessários. Não excluir uma bebida silenciosamente, nem tratar 40 cm brutos da frente como altura útil. [Estudo do gavetão](../Cozinha/Interior_gavetao_2026-09-25.md).

## 5. Sala, escritório e quarto: robustez das passagens

### Mesa e coluna

Mantidos 150/180 × 75 cm, folha no banco e três cadeiras na lateral livre. A coluna de 12 cm do desenho não é especificação estrutural. Recalculada a posição da cadeira central para preservar 2 cm geométricos até a coluna:

| Diâmetro hipotético da coluna | Inserção da cadeira | Projeção fora da mesa | Passagem lateral nominal nesse trecho |
|---:|---:|---:|---:|
| 12 cm | 29,5 cm | 17,5 cm | 102,5 cm |
| 16 cm | 27,5 cm | 19,5 cm | 100,5 cm |
| 20 cm | 25,5 cm | 21,5 cm | 98,5 cm |
| 24 cm | 23,5 cm | 23,5 cm | 96,5 cm |

Resultado útil: **não há motivo geométrico demonstrado para impor uma coluna de apenas 12 cm**. Uma coluna de 20 cm custaria 4 cm de passagem local nesse teste, sem mudar a mesa. Não valida sapata, trilhos, pés da cadeira, pessoa sentada ou estabilidade. O dimensionamento estrutural deve comandar a base, e o ensaio final ajustar a guarda das cadeiras. [Base de coordenadas](../Sala_e_jantar/Mesa_circulacao_entrada_2026-09-23.md).

### Escritório

No cenário R11, distância do sofá aberto ao setor ideal da porta: **3,06 cm**. Se sofá/envelope de roupa crescer 1 cm, cai para **2,06 cm**. Se o eixo estiver 2 cm mais para dentro, cai para **1,06 cm**. Com ambos juntos, resta **0,06 cm**, praticamente zero, ainda antes de maçaneta, espessura e tolerâncias.

Não é evidência de que a porta real colide, pois eixo/folha ainda são hipóteses. É evidência de que a configuração não pode ser liberada só pelo desenho. Guardar as quatro medidas necessárias no briefing, preservando sofá e porta escolhidos. [R11](../Escritorio/Sofa_e_porta_R11.md).

### Quarto

Conta nominal com faixa de 20 cm junto à janela, cama de 160, armário de 60 e proteção posterior de 1: **295 − 20 − 160 − 60 − 1 = 54 cm**. Uma perda de 2 cm no comprimento útil reduz para 52. As parcelas de implantação são hipóteses do projeto.

Na posição de abertura perpendicular, uma folha de 50 cm consumiria 50 dos 54 cm, sobrando **4 cm entre ponta e cama**; uma folha de 40 deixaria 14. Isso não mede espaço corporal para usar o armário. Nenhuma tipologia de porta foi escolhida nesta rodada. Preservar divisão R02 e exigir desenho de abertura/acesso às quatro gavetas antes da ferragem final. [Compatibilização vigente](../Portas_e_quarto/Guarda_roupa_interior_R02.md).

## Limites e próximo trabalho já organizado

O caderno não encerra o conflito de ventilação do ME23P, a seção cooktop/forno, a instalação de gás, o mecanismo do varal ou as medidas da unidade. Esses pontos estão convertidos em **entregáveis específicos no briefing**, sem repetir perguntas de gosto ou pedir agora medidas que dependem da entrega.

Reprodução: executar `node 01_Projeto/Compatibilizacao_2026-09-28/calcular.cjs` na raiz do projeto. O script verifica interpretação do IES, integral do fluxo, lei do inverso do quadrado, simetria, interseção de raios, proporcionalidade da fonte linear e pico do cesto por varredura de 5.501 ângulos. Depois executar `node 01_Projeto/Compatibilizacao_2026-09-28/gerar_caderno.cjs` para atualizar o caderno.

Sem consulta de preço nova, compra, envio a terceiros ou fabricação. As fontes são as decisões e documentos locais existentes; nenhum dado de produto foi apresentado como verificação comercial de hoje.
