# Organizadores do gavetão — capacidade com paredes e pega

30/09/2026. [Prancha consolidada](Organizadores_g3.html). Estudo local, sem Firecrawl, compra ou nova consulta comercial.

## Direção técnica

Preservar G1/G2/G3 com frentes 16/16/40, abertura total e amortecimento, organizadores removíveis e a distribuição aceita. No G3, manter temperos à frente esquerda, alimentos abertos atrás e leite/suco/óleo/azeite em pé à direita. **Não fixar divisores ou comprar organizadores a partir da capacidade ilustrada anteriormente.** A área dos setores estava demonstrada; o cabimento do conteúdo não.

Referências: [interior do gavetão](../Cozinha/Interior_gavetao_2026-09-25.md), [gavetas e escolhas posteriores](../Cozinha/Interior_gavetas_2026-09-25.md) e [torre/gavetas](../Compatibilizacao_2026-09-28/Torre_gavetas.md). Não restaurar trechos históricos de quatro gavetas ou temperos deitados. A caixa externa de profundidade 50 segue objetivo; não encurtá-la por causa deste teste.

## Descontos adotados

Caixa útil 52,7 × 47 ainda hipotética. Margens de 1 nas bordas e entre setores já pertencem ao desenho anterior. Setores externos: temperos 27,7 × 19, secos 27,7 × 25, bebidas 22 × 45.

Para esta rodada, acrescentar paredes externas e divisórias de **0,3 cm** e folga de **0,2 cm de cada lado** de cada produto. Não são material aprovado ou folgas ergonômicas certificadas; servem para não confundir dimensão externa do setor com espaço livre integral.

Para n células de produto de dimensão d, o organizador ocupa:

`n × (d + 0,4) + (n−1) × 0,3 + 2 × 0,3 = n × (d + 0,7) + 0,3`.

O círculo do frasco é representado por sua caixa envolvente em grade regular. Tampa maior que o corpo deve entrar no diâmetro. Não foram testados encaixe em colmeia, bandejas sem paredes individuais ou arranjos escalonados. Os limites abaixo são da grade, não prova de impossibilidade absoluta.

## Temperos e efeito nos secos

Buscando grades retangulares com pelo menos a quantidade requerida:

- Para 24: grade 6 × 4, diâmetro máximo **3,8667**.
- Para pelo menos 18: grade 5 × 4, com 20 células, diâmetro máximo **3,975**. Duas posições extras não representam aumento obrigatório do inventário.

| Diâmetro de teste | Grade máxima na área atual | Capacidade | Profundidade mínima da grade escolhida para ≥18 | Para ≥24 | Profundidade dos secos se ≥24 |
|---|---|---:|---:|---:|---:|
| 3,5 | 6 × 4 | 24 | 12,9 | 17,1 | 25,0, sem reduzir setor atual |
| 4,0 | 5 × 3 | 15 | 19,1 | 23,8 | 20,2 |
| 4,5 | 5 × 3 | 15 | 21,1 | 26,3 | 17,7 |
| 5,0 | 4 × 3 | 12 | 28,8 | 34,5 | 9,5 |
| 5,5 | 4 × 3 | 12 | 31,3 | 37,5 | 6,5 |

O ensaio de ampliação mantém largura esquerda 27,7 e bebidas 22, usando o maior número de colunas que cabe e arredondando filas para cima. Não otimiza todos os arranjos possíveis. Profundidade dos secos = 45 − 1 entre setores − profundidade dos temperos. Quando o organizador calculado é menor que os 19 atuais, não se reduz automaticamente o setor.

Com frascos de 4,5, 24 posições requerem cinco colunas e cinco filas, isto é, 25 células. Organizador externo 26,3 × 26,3; cabe na largura 27,7, mas precisa crescer 7,3 em profundidade. Os secos caem de 25 para 17,7: **perda de 29,2% da área desse setor**, mantendo sua largura. Essa alteração não foi adotada.

Quatro recipientes iguais em 2 × 2, com os mesmos descontos, teriam envelope de produto de 13 × 11,65 no setor atual. Com profundidade de 17,7, ficam limitados a 13 × 8. Isso não define capacidade em litros, massa dos alimentos ou capacidade do estoque; recipientes reais podem ter conicidade, tampas e pegas.

## Faixa direita e inventário mínimo

Os registros pedem seis caixas de leite e três sucos de 1,5 L. Óleo e azeite foram adicionados à mesma faixa por escolha do usuário. Uma embalagem de cada, apenas como mínimo de triagem, leva a **11 produtos**. A quantidade máxima real e a litragem/formato do leite não são conhecidos. Molhos e enlatados seguem sem encaixe comprovado.

Comparações de grade uniforme dentro de 22 × 45 externos:

| Grade | Capacidade geométrica | Envelope máximo por produto, descontadas paredes e folgas |
|---|---:|---|
| 2 × 6 | 12 | 10,15 × 6,75 |
| 3 × 4 | 12 | 6,5333 × 10,475 |

Não são células para comprar ou tamanhos assumidos de caixas comerciais. Um arranjo misto pode usar melhor a área; depende de contornos e quantidades. Não declarar impossibilidade das bebidas apenas porque uma grade uniforme falha; igualmente, não desenhar 11 embalagens genéricas como capacidade comprovada.

## Altura e carga

Os 40 cm brutos da frente não são altura livre. Dimensões externas da embalagem mais alta e espaço de retirada devem ser confrontados com fundo, travessas, corrediça e gaveta superior. Caixa e conteúdo cheio, organizadores e proteções entram na carga total. Não selecionar classificação de corrediça em kg sem esses dados nem converter litros desconhecidos em massa exata.

## Encaminhamento sem nova decisão do usuário

Manter desenho funcional e caixas atuais; desenvolver organizadores de setores inteiramente removíveis, sem colar uma grade de temperos ao fundo. O próximo levantamento útil deve reunir dimensões externas máximas e quantidade simultânea dos frascos, leite, sucos, óleo, azeite, secos, molhos e enlatados. Não é solicitação imediata de medidas, nem troca de produtos.

A conta fecha o limite do desenho atual e quantifica as trocas de área, evitando fabricar divisores antes de conhecer o conteúdo. G1/G2 e frentes não foram alteradas; nenhum inventário foi reduzido silenciosamente.

Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/organizadores_g3.cjs`. [Resultados](Resultados_organizadores_g3.json). Fórmulas verificadas; apresentação visual não inspecionada nesta rodada.
