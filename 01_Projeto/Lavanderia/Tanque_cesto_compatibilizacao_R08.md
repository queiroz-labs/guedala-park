# Tanque e cesto — compatibilização R08

**Continuação — 30/09/2026:** [frente, rodapé e retirada](../Compatibilizacao_2026-09-30/Cesto_retirada.md). Corrigida a incompatibilidade entre tanque de teste até y=60 e frente ilustrativa a 58 por proposta de face a 63, mantendo tanque/pedra/eixo. Inferior basculante z=15–67,1 e superior removível z=67,5–89,7; base/rodapé até y=58, topo do rodapé 11. Frente e saco agora têm percursos próprios calculados; não considerar os 61,1 cm após o recipiente como sobra após o conjunto completo. Novas cotas são propostas, hidráulica real e Telca continuam pendentes.

**Tolerância de acesso — 28/09/2026:** [ensaio complementar](../Compatibilizacao_2026-09-28/README.md#3-cesto-acrescentar-tolerância-de-acesso-ao-teste-de-colisão). A 55°, a boca ultrapassa a pedra em 3,52 cm, só 5,2 mm além da reserva comparativa de 3 cm; ângulo mínimo calculado 54,36°. Pedra 1 cm maior, eixo 1 cm mais recuado ou curso limitado a 54° consomem essa reserva. A conferência hidráulica abaixo permanece; incluir frente/ferragem e retirada do saco no detalhamento, sem alterar eixo/curso automaticamente.

27/09/2026. Desenvolvimento após a conferência dos aparelhos. Mantidos tanque interno de 38 × 35 × 20 cm, pedra Branco Itaúnas, Telca Flex preta com ducha extraível, escoamento posterior, cesto basculante 45 × 25 × 45 cm e saco removível/lavável com alças. Esta revisão calcula uma reserva melhor para o escoamento; não seleciona peças nem autoriza furação.

## Resultado principal

No modelo da R04, é possível reservar **7 cm sob o fundo externo do tanque** para válvula/primeira conexão, desde que todo o trecho que se sobrepõe lateralmente ao cesto tenha:

- frente mais avançada **até 33 cm da parede**;
- ponto inferior **a partir de 63 cm do piso**;
- percurso posterior, depois desse trecho alto, totalmente **até 28 cm da parede**.

Esses limites são suficientes para manter a reserva geométrica de 3 cm adotada no estudo ao longo de todo o giro de 0 a 55°. A reserva de 7 cm vem de fundo externo hipotético a 70 menos limite inferior a 63. **Não foi demonstrado que a válvula, a curva e suas uniões reais caibam nesses 7 cm.** A mangueira/contrapeso da Telca também não estão incluídos nesse volume.

Essa análise localizada complementa os limites conservadores da R04/R07. O limite de 66,5 cm continua válido para obstáculos que atravessam toda a região superior varrida; ele não precisa ser imposto igualmente a uma conexão restrita à parte posterior. Não reduzir tanque ou cesto para resolver uma colisão ainda não demonstrada.

## Hipóteses preservadas

| Item | Referência |
|---|---|
| Tampo da lavanderia | 75 cm desde a parede; topo a 92 cm |
| Pedra do tanque | Paredes/fundo de 2 cm hipotéticos; exterior 42 × 39 cm; fundo externo a 70 cm |
| Gabinete | 59 cm de largura externa; 55,4 cm internos com laterais de 1,8 cm |
| Cesto e armação móvel | Envelope externo 45 L × 25 P × 45 A cm |
| Eixo de giro | 56 cm da parede e 12 cm do piso; proposta, não furação definida |
| Curso | 0–55°; mecanismo real ainda a selecionar |
| Folga do ensaio | 3 cm; critério de projeto, não norma hidráulica nem espaço de manutenção |

Frente decorativa, ferragens externas e saco carregado precisam de conferência própria. Alças, armação e tecido não podem ultrapassar o envelope assumido. A reserva lateral nominal de 5,2 cm por lado já atende folgas/ferragens e não é um corredor garantido para a torneira.

## Posição ilustrativa do tanque, sem alterar a escolha

Para testar a posição posterior sem exigir 20 cm de pedra à frente do tanque, usar somente como exemplo **15 cm de faixa frontal**. Com tampo de 75 cm e tanque externo de 39 cm, a face traseira externa fica a 21 cm da parede e a dianteira a 60 cm.

Com parede de 2 cm, eixo de válvula a 6 cm da face interna traseira e avanço da conexão de 4 cm além do eixo, resulta: eixo a 29 cm e frente do conjunto a 33 cm. Os 6 e 4 cm são hipóteses de sensibilidade herdadas da R07, **não medidas de produto ou margens de recorte recomendadas**. Precisam ser substituídos por desenho da válvula e definição estrutural da marmoraria. A faixa de 15 cm não foi escolhida pelo usuário nem validada ergonomicamente.

Esse exemplo atende à condição localizada se a primeira conexão terminar a pelo menos 63 cm de altura e recuar para a faixa posterior até 28 cm da parede antes de descer. A tubulação completa, seus suportes e acesso às uniões precisam caber; não presumir que um cotovelo padrão resolve esse desvio.

## Conferência matemática do giro

Corte lateral, em centímetros. Coordenada y desde a parede e z desde o piso; u entre −25 e 0, v entre 0 e 45, ângulo θ entre 0 e 55°:

`y = 56 + u cos(θ) + v sen(θ)`

`z = 12 − u sen(θ) + v cos(θ)`

Todo o retângulo móvel fica dentro do círculo de centro (56, 12) e raio `raiz(25² + 45²) = 51,478`. Para conferir 3 cm de separação em torno da reserva hidráulica com frente a 33 e base a 63, amplia-se conservadoramente o obstáculo até y = 36 e z = 60. Nessa faixa y ≤ 36, o círculo só alcança:

`z ≤ 12 + raiz(25² + 45² − (56 − 36)²) = 59,434 cm`.

Como 59,434 é inferior a 60, o cesto não entra no obstáculo ampliado. Isso demonstra uma condição suficiente para o modelo idealizado completo, incluindo o interior e as arestas, não só quatro posições de quinas.

Verificação adicional: polígonos recortados no limite y = 36 em **5.501 ângulos** (passos de 0,01°). Maior altura nessa faixa 59,433 cm, em torno de 6,19°. Pico superior global 63,478 cm, a 29,05°. A diferença entre os dois picos explica por que a conexão traseira dispõe de mais altura. [Resultados numéricos](Conferencia_giro_R08.json).

Hidráulica inteiramente até 28 cm da parede continua separada horizontalmente do cesto, cujo ponto mais traseiro está a pelo menos 31 cm. Não aplicar uma restrição de altura adicional a esse trecho apenas por causa da conta acima. Apoios da pedra que avancem além dessa faixa precisam de sua própria conferência.

## Peças pesquisadas e limite documental

**Telca Flex preta, código 1571531402, EAN 7898740530122:** a [oferta do vendedor Telca na Leroy Merlin](https://www.leroymerlin.com.br/torneira-misturador-lavatorio-flex-monocomando-preto_1571531402) informa altura de 18 cm, bica a 10,5 cm, extensão indicada de até 30 cm e furo de 35 mm; lista dois flexíveis de alimentação de 40 cm e contrapeso. Os 40 cm dos flexíveis não dimensionam a mangueira extraível. Não foram obtidos comprimento completo dessa mangueira, dimensões/curso do contrapeso, raio mínimo de curva ou capacidade de aperto da fixação na pedra. Preservar modelo escolhido, com essa verificação em aberto.

**Candidato para escoamento posterior:** a [Incepa B5012IABR3](https://www.banheirosincepa.com.br/produtos/sifao-para-economia-de-espaco-b5012iabr3) é apresentada pelo fabricante como sifão economizador de espaço com conexões de 7/8, 1¼ e 1½ polegadas, saída DN40 e tubo de 350–780 mm. A página consultada não fornece seção cotada que comprove o conjunto direto sob o tanque dentro dos 7 cm. É candidato de pesquisa, não modelo escolhido nem comprovação de compatibilidade com a válvula do tanque.

Não substituir sifão por ligação sem fecho hídrico, achatar mangueiras ou usar recortes improvisados para atender à geometria. Esta rodada não define diâmetro da válvula nem ponto novo de esgoto.

## O que falta para encerrar este conjunto

1. Selecionar válvula com tampão/retentor removíveis e obter seção completa montada: aperto na pedra, saída, união e curva posterior.
2. Conferir essa montagem no limite de até 33 cm da parede e a partir de 63 cm do piso, com passagem posterior até 28 cm, ou recalcular usando o volume real.
3. Desenhar separadamente curso da mangueira/contrapeso da Telca, fixação e acesso, sem usar a folga das ferragens duas vezes.
4. Especificar mecanismo de giro, limite de abertura, retenção, carga e retirada simples da armação/frente. Ensaiar retirada do saco cheio e manutenção.
5. Cruzar pontos e apoios reais quando o apartamento estiver acessível, sem solicitar novamente medidas indisponíveis a Elias.

**Estado:** viabilidade geométrica melhorada mantendo as dimensões escolhidas; montagem hidráulica e mecanismo físico ainda não comprovados. A profundidade de 63 cm aceita para estudo na cozinha não altera automaticamente os 75 cm usados neste cálculo da lavanderia.

Bases: [tanque R05](Tanque_dimensionamento_R05.md), [cesto R04](Cesto_basculante_calculo_R04.md), [posição R07](Escoamento_posicao_R07.md), [torneira R06](Torneira_pesquisa_R06.md). Nenhuma destas novas cotas constitui levantamento da unidade.
