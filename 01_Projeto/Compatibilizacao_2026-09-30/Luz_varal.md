# Luz da lavanderia, varal e tanque — compatibilização geométrica

30/09/2026. [Prancha](Luz_varal.html) · [Resultados](Resultados_luz_varal.json). Trabalho com referências locais; sem Firecrawl, pesquisa comercial ou nova especificação elétrica.

## Direção de desenvolvimento

Priorizar a comparação de um plafon compacto **de até 30 cm**, branco, de sobrepor, 3000 K, na faixa anterior à grelha. Para um corpo hipotético de **28 cm**, o centro **x=64,5 / y=55 cm** é a posição refinada deste estudo: ficam 6 cm até a projeção do aéreo e 6 até o envelope de roupas que avance 10 cm para além da grelha. Não é posição aprovada para instalação ou ponto elétrico novo.

Os 28 cm são gabarito, não um produto encontrado. Formato final da lavanderia continua a coordenar com a cozinha; o aceite do quadrado da cozinha não foi estendido automaticamente. A preferência por até 30 cm resulta da faixa livre adotada, não de uma proibição geral de corpos maiores.

## Referências e hipóteses explícitas

- [Varal consolidado](../Lavanderia/Varal_especificacao_consolidada.md): grelha escolhida de 100 × 50, elevação vertical, chapa única, acesso pela cozinha. Implantação de teste x=14,5–114,5 / y=85–135 em setor 129 × 154. Suportes e mecanismo ainda sem dimensões.
- [R07](../Lavanderia/Varal_caixa_no_teto_R07.md): coordenadas e corpo hipotético do E21 x=20–55 / y=0–15,7. A caixa antiga de ocultação foi descartada; não foi reintroduzida neste ensaio.
- [R09](../Lavanderia/Varal_linha_de_visao_e_mecanismo_R09.md): cenário de teto a 247. Isso não substitui o cenário de 257 usado em outro estudo da cozinha nem demonstra uma diferença real de teto entre os ambientes.
- [Modelo 3D](../Estudo_interativo/src/app.js): aéreo da lavanderia normalizado em x=47–130,5 / y=0–35 / z=165–223. O excedente longitudinal de 1,5 cm em relação ao setor 129 permanece no obstáculo de sombra, sem diminuir o móvel para favorecer o cálculo. É interface a compatibilizar, não correção de largura aprovada.
- [Seleção de iluminação anterior](../Iluminacao/Cozinha_lavanderia_selecao_R01_2026-09-27.md): aparência branca, sobrepor, 3000 K; corpo de 41 cm estudado na cozinha. Aqui não se revalidam fichas ou ofertas comerciais.
- [Corte do cesto/tanque](Cesto_retirada.md): faixa de seção do tanque y=21–60 e tampo a 92. Nove alvos de cálculo em x=10/29/48 e y=21/40,5/60, todos a z=92, representam a região do tanque no plano da bancada. Não são medições do fundo ou da cuba real.

Origem na janela; x cresce para a cozinha. y parte da parede hidráulica. Todas as cotas em cm. Não usar os 161 cm do piso ilustrativo do 3D para ampliar o setor documental de 154.

## Faixa disponível e refinamento

A frente do aéreo está em y=35; a grelha começa em y=85. Faixa de 50. Adotando 5 cm de margem preliminar por lado, o maior corpo nessa faixa seria 50−10=40. **5 cm é critério escolhido de comparação, não norma ou instrução de fabricante.**

| Corpo, centrado em y=60 | Até projeção do aéreo | Até grelha | Até roupa avançando 10 |
|---|---:|---:|---:|
| 14 | 18 | 18 | 8 |
| 28 | 11 | 11 | 1 |
| 35 | 7,5 | 7,5 | −2,5 |
| 40 | 5 | 5 | −5 |
| 41 | 4,5 | 4,5 | −5,5 |

Valores negativos são sobreposição em planta, não colisão tridimensional comprovada. A peça de 41 não está proibida: apenas não preserva a margem escolhida nessa implantação, antes de considerar roupas e mecanismos.

Com avanço de roupa de 10 rumo à bancada, seu limite passa a y=75. A faixa de estudo torna-se 35–75, com 40 de largura. O maior corpo com margens de 5 seria **30**, centrado em **y=55**. Para corpo de 28, limites y=41–69: **6 cm de cada lado**. A margem lateral às paredes do setor para x=64,5 é 50,5; isso não libera instalação junto a duto, janela ou suportes desconhecidos.

Com avanço de 15, a roupa começaria em y=70: a peça de 28 em y=55 teria só 1 cm em planta. O avanço não é valor validado de balanço de roupas/cabides; é sensibilidade. Não tratar o tecido como necessariamente contido nesse envelope.

## Portas e altura

Projeção de plafon usada: 5, sem produto escolhido. Em teto a 247, face inferior a 242. Aéreo do modelo termina a 223, deixando 19 de separação vertical. Portanto, **a sobreposição da projeção de uma porta aberta não prova colisão com o plafon** nessa configuração. As portas permanecem abaixo dele no modelo, desde que não haja ferragem saliente acima do móvel. Isso precisa ser revisto se altura do aéreo, teto, luminária ou ferragem mudar.

Não aplicar automaticamente o conflito de portas dos aéreos altos da cozinha à lavanderia. Também não inferir que os 19 cm resolvam duto, suportes do varal ou manutenção da luminária. Nenhum afastamento técnico do E21 foi aprovado por essa conta; sua projeção em planta é apenas contextual.

## Ensaio de sombra

Superfície emissora circular hipotética de diâmetro 28 a z=242, amostrada a cada 2 cm, com **149 pontos**. Cada um foi ligado aos nove alvos: **1.341 segmentos por cenário**. Interseções contra dois obstáculos independentes:

1. Aéreo com volume documentado acima.
2. Bloco opaco de roupa de z=100 até 240, expandido em planta em 0/5/10/15/20 a partir da grelha. É hipótese conservadora de continuidade do tecido, não posição aprovada de secagem ou reserva completa do mecanismo. Expansões maiores chegam a ultrapassar o setor lateral; são testes de sombra, não modos de uso aceitos.

| Avanço em planta | Roupa, centro y=60 | Aéreo, centro y=60 | Roupa, centro y=55 | Aéreo, centro y=55 |
|---|---:|---:|---:|---:|
| 0 | 0 | 13 | 0 | 72 |
| 5 | 0 | 13 | 0 | 72 |
| 10 | 0 | 13 | 0 | 72 |
| 15 | 72 | 13 | 0 | 72 |
| 20 | 369 | 13 | 72 | 72 |

Números são segmentos interceptados entre 1.341, **não porcentagens de iluminação, lux ou uniformidade**. Segmentos não têm ponderação angular ou de intensidade; alguns obstáculos podem interceptar o mesmo segmento. Não somar contagens como se fossem perda luminosa.

A ausência de interceptação de roupa nos menores avanços também tem prova independente da amostragem: em y=60, todo emissor termina em y=74 e os alvos em y=60, portanto nenhum segmento alcança roupa começando em y=75. Em y=55, todo emissor termina em y=69, antes de roupa começando em y=70 no avanço de 15. É separação em planta válida para a superfície emissora completa.

Deslocar a luz 5 cm para trás melhora a separação das roupas, mas aproxima os raios do aéreo: as interceptações dele passam de 13 a 72. É um compromisso a conferir com fotometria real; não demonstra iluminação suficiente no tanque. O usuário, as bordas e fundo da cuba, chapa, suportes e duto não foram incluídos. Superfície da luminária real pode emitir de maneira diferente do disco hipotético.

## O que fica preparado

Envelope para futura comparação: corpo até 30, ensaio prioritário de 28 em (64,5;55), projeção de 5 apenas como referência. Pedir desenho de corpo e montagem, curva fotométrica e documentação de uso quando a seleção comercial for retomada; cruzar com duto e mecanismo reais antes de fixar ponto. Não acrescentar luz sob os aéreos por inferência, não alterar 3000 K ou os três comandos escolhidos.

O avanço desta rodada é a faixa dimensionada e a comparação de sombras, não a seleção da luminária. Nenhuma pergunta nova ao usuário, alteração do modelo vigente, compra ou contato com fornecedor.

Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/luz_varal.cjs`. Gera prancha e resultados. Contas e interseções verificadas; renderização visual da prancha não conferida nesta rodada.
