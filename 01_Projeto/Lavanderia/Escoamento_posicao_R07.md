# Escoamento do tanque — posição e alcance R07

**Complemento de 27/09/2026:** a [R08](Tanque_cesto_compatibilizacao_R08.md) demonstra condição localizada menos restritiva: conexão com frente até 33 cm da parede e base a partir de 63 cm do piso preserva a reserva do giro no modelo. Isso permite estudar 7 cm sob fundo externo a 70 cm, sem obrigar faixa frontal de 20 cm. Peças reais e Telca ainda não comprovadas; as contas conservadoras abaixo permanecem como referência histórica, não exigência uniforme de altura.

Estudo de 26/09/2026. Elias respondeu “seguimos” à proposta de saída na região posterior do tanque: adotar essa direção para detalhamento, sem transformar o aceite em cota de recorte, mudança do esgoto existente ou compatibilidade comprovada.

## O que está definido

- Tanque integrado à pedra contínua, referência interna 38 × 35 × 20 cm.
- Tampão removível para molho, retentor de fiapos removível e acabamento baixo.
- Cesto basculante removível 45 × 25 × 45 cm, curso de referência 55°.
- Telca Flex preta como candidata escolhida, com percurso de mangueira/contrapeso a conferir.
- Estudar válvula na região posterior da cuba, com sifão e mangueira em percursos separados e acessíveis após retirada do cesto. Lado e distância exata ainda não definidos.

## Verificação nova: não resolver o sifão recuando toda a cuba

Na hipótese existente, a bancada tem 75 cm desde a parede e a cuba 39 cm externos de frente a fundo. Assim, a soma das faixas de pedra à frente e atrás da cuba é 36 cm. Quanto mais se recua a cuba, maior fica a faixa frontal que a pessoa precisa alcançar por cima. Nenhuma dessas faixas foi medida ou aprovada.

Conta em centímetros: seja F a faixa entre a borda frontal da pedra e a face externa frontal da cuba. A face externa posterior da cuba fica em B = 75 − F − 39 = 36 − F, medida desde a parede. Com parede da cuba t, distância d da face interna posterior ao eixo da válvula e avanço e do conjunto hidráulico além desse eixo, a frente mais avançada do conjunto direto fica em B + t + d + e.

Para aplicar o critério conservador de hidráulica até 28 cm da parede da R04, é necessário B + t + d + e ≤ 28. Com t = 2 cm hipotéticos, isso resulta em F ≥ 10 + d + e. A expressão se aplica a um conjunto cuja frente possa ser representada por esse avanço; não dimensiona um sifão nem um desvio de saída.

**Exemplo de sensibilidade, sem peças selecionadas:** adotar apenas para a conta d = 6 cm e e = 4 cm. Não são margens de instalação recomendadas nem medidas de produto.

| Faixa frontal F | Face posterior externa B, desde a parede | Eixo da válvula, desde a parede | Frente do conjunto, desde a parede | Critério posterior até 28 cm |
|---|---:|---:|---:|---|
| 10 cm | 26 cm | 34 cm | 38 cm | Não atende neste exemplo |
| 15 cm | 21 cm | 29 cm | 33 cm | Não atende neste exemplo |
| 20 cm | 16 cm | 24 cm | 28 cm | Atende somente ao limite em profundidade |

A última linha não é layout recomendado ou validado: deixa 20 cm de pedra antes da cuba e ainda não testa mangueira, ferragens, manutenção ou alcance humano. A tabela mostra por que a posição posterior do ralo, sozinha, não garante o encaixe. Não concluir que o conjunto real exige faixa frontal de 20 cm: d e e ainda são desconhecidos.

## Direção para continuar

Manter a abertura do tanque acessível pela frente e avaliar primeiro o conjunto real de válvula e sifão. Se for necessário recuar a tubulação por baixo do tanque, conferir todo esse trecho: acima da região varrida pelo cesto, a R05 admite obstáculos a partir de 66,5 cm do piso. Com fundo externo hipotético a 70 cm, restam apenas 3,5 cm de descida nesse critério. Não foi demonstrado que um desvio comercial caiba aí. Uma análise localizada pode ser menos restritiva que o envelope conservador, mas depende das peças e do eixo real do cesto.

Não adotar rasgo, conexão achatada, sifão deformado ou redução de tanque/cesto para satisfazer o desenho. A seleção precisa resolver, no mesmo corte, saída da válvula, sifão, tubo até o esgoto existente, apoios, mangueira/contrapeso e retirada do cesto. A referência de 28 cm é profundidade-limite calculada, não uma medida de espaço posterior livre.

## Dados que encerram a conferência

| Dado | Para quê |
|---|---|
| Posição real e diâmetro do ponto de esgoto | Definir conexão e lado do sifão sem presumir mudança de ponto |
| Seção da válvula, espessura de aperto e sifão escolhido | Calcular volume completo, vedação e acesso às uniões |
| Conjunto exato de mangueira e contrapeso da Telca | Reservar seu movimento sem interferir no escoamento |
| Posição da abertura e apoios da pedra | Conferir alcance, estrutura e recortes juntos |

**Resultado:** saída posterior é direção aceita; cotas de execução ainda não podem ser fechadas. Este estudo identifica uma dependência de alcance que não estava quantificada, preservando as dimensões aprovadas. Não foram alterados modelo 3D, pontos ou produtos escolhidos.

Fontes: [tanque R05](Tanque_dimensionamento_R05.md), [cesto R04](Cesto_basculante_calculo_R04.md), [torneira R06](Torneira_pesquisa_R06.md). Cálculo geométrico sobre hipóteses locais; nenhuma medida deste estudo foi extraída dos documentos oficiais do empreendimento.
