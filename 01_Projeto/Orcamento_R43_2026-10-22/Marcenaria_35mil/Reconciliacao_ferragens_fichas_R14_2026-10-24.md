# Reconciliação: ferragens do orçamento × fichas R14

24/10/2026. Compara a [revisão de ferragens de 23/10](Revisao_ferragens_servicos_2026-10-23.md), base dos R$9.200 de ferragens, com as linhas de ferragem das [fichas R14](../../Estudo_interativo/fabrication/technical-r14.json) dos 20 módulos.

**Este documento só registra cenários.** Não altera o orçamento central, o CAD nem as fichas, e não declara nenhuma economia como obtida.

## 1. O que já bate

| Família | Orçamento | Fichas R14 | Situação |
|---|---|---|---|
| Dobradiças: quantidade | 42 comuns + 4 do canto + 6 do espelheiro = 52 | P02 4 · P04 8 · P05 4 · P09 4 · P10 6 · P11 4 · P12 4 · P15 4 · P17 8 · P19 6 = **52** | Igual |
| Corrediças de 500 mm | 7 pares FGVTN 500 | P01 4 + P06 3 = **7 pares** 54FGOC12500TSX0 | Igual |
| Corrediças do escritório | 2 pares MOVENTO 400 + engates | P16: 2 pares 760H4000S + 2 pares T51.7601 | Igual. O gabarito T65.1000.02 é ferramenta e pode ser emprestado pela oficina |
| Portas de correr | 3 sistemas, 6 folhas | P01 RO62 2 kits · P03 RO62 2 kits · P18 RO25 2 kits | Igual |
| Varões | 4 cabideiros, 8 terminais | P01: 4 cortes, 8 terminais, 2 suportes centrais | Igual. Os 2 suportes centrais cabem na verba |
| Pinos do espelheiro | 8 | P19: 8 Häfele 282.04.711 | Igual |

## 2. Divergências e como resolver

### 2.1 Dobradiças: FGVTN no orçamento × Blum nas fichas

As fichas selecionam o conjunto Blum completo:
- dobradiça CLIP top BLUMOTION 71B3550;
- calço 173H7100;
- **limitador de 86° 70T3553**, item que o orçamento não previa.

O orçamento precificou 42 conjuntos FGVTN a R$12–18, mais as especiais. A própria ficha diz: *"recotar dobradiças Blum"*.

| Cenário | Base | Faixa |
|---|---|---:|
| Orçamento atual (FGVTN + especiais) | 42 × R$12–18 + 4 × R$25–55 + 6 × R$25–50 | R$754–1.276 |
| Blum completo, **provisão a cotar** | 52 × (dobradiça e calço R$35–60 + limitador R$5–12) | R$2.080–3.744 |
| **Diferença** | | **+R$1.326 a +R$2.468** |

Sobre a provisão Blum: não foi encontrado preço público em reais. No exterior, a 71B3550 aparece por cerca de [£3,70–4,44 cada](https://ironmongerydirect.co.uk/product/blum-clip-top-soft-close-cabinet-hinge-110-overlay-pair-571554) e [CHF 4,04 em lote](https://www.sfs.ch/CH/en/dl/p/465225), sem calço. O 70T3553 aparece por cerca de [US$0,88](https://wurthlac.com/product-item/733577/B70T3553). A faixa em reais acima é estimativa de varejo nacional com calço incluído. **Não é cotação.**

**Como resolver:** pedir a cotação nas duas famílias, Blum como especificado e FGVTN equivalente com limitador, para a mesma lista de 52 posições. Se a FGVTN for escolhida, a ficha precisa ser revisada (furação do caneco, calço, limitador). Isso é decisão técnica do projeto, não troca automática.

### 2.2 Minifix: 20 no orçamento × 40 com quantidade definida nas fichas

| Módulo | Minifix nas fichas |
|---|---:|
| P10 Aéreo C | 20 caixas Häfele 262.26.034 + 20 pinos S100 262.28.920 |
| P11 Aéreo B | 12 + 12 |
| P15 Aéreo da lavanderia | 8 + 8 |
| **Subtotal com quantidade definida** | **40 conjuntos** |
| P01, P04, P12, P17 | Minifix previsto, **quantidade ainda sem mapa** |

O orçamento cita 20 dentro da verba de conectores, pinos, ancoragens, batentes e fixadores (R$650–1.200). Os 20 conjuntos a mais custam pouco: cerca de R$60–140 a R$3–7 por conjunto, provisão. O risco maior são os quatro módulos ainda sem mapa.

**Como resolver:** corrigir a memória do orçamento para "40 definidos + P01/P04/P12/P17 a mapear". Manter a verba de conectores por enquanto e pedir que a oficina cote os conectores pelo mapa final de ligações.

### 2.3 Banco P20: 4 dobradiças Southco no orçamento × diretriz de piano com trava

O orçamento tem R$2.400–4.400 para 4 Southco importadas. A [diretriz de 23/10](../../Banco_cesto_simples_2026-10-23/Diretriz.md) prioriza dobradiça piano e suporte com trava, mais simples e barata. As fichas R14 ainda listam a Southco, com contraplatinas e suportes de aço.

| Cenário | Faixa |
|---|---:|
| Southco (orçamento atual) | R$2.400–4.400 |
| Piano (2 trechos de ~1 m) + 2 suportes com trava + fixadores, **provisão** | R$360–1.000 |
| **Redução possível** | **R$2.040–3.400**, só depois de validar o produto e a montagem |

As chapas de aço da solução Southco (contraplatinas, suportes e placas) deixariam de ser necessárias. Essa parte da verba de aço (R$350–700) também pode cair, mas só será confirmado com o desenho da nova montagem.

### 2.4 Gaveta de limpeza P08: rodízios escolhidos

A ficha R14 registra a escolha de 24/10: **kit Leão Aço com 6 rodízios fixos de Ø30 mm**, com espaçadores metálicos de 1 mm. O orçamento tem a provisão "6 rodas/guias" de R$120–240. Manter a provisão até ter o preço do kit escolhido.

## 3. Efeito no cenário de ferragens

| Ajuste | Efeito sobre os R$9.200 |
|---|---:|
| Dobradiças Blum completas | +R$1.326 a +R$2.468 |
| 20 Minifix adicionais | +R$60 a +R$140 |
| Banco com piano + trava, se validado | −R$2.040 a −R$3.400 |
| **Saldo** | **entre −R$2.014 e +R$568** |

Na prática, **trocar a Southco pela piano compensa a troca de FGVTN por Blum.** As ferragens ficam próximas dos R$9.200 atuais, mas não chegam ao limite de negociação de R$6.500. Para chegar lá, seria preciso cotar a FGVTN equivalente nas portas e conseguir um preço bom no conjunto.

O cenário total da marcenaria **continua em R$46.500**. Nenhum valor é atualizado até receber cotação.

## 4. O que muda no pedido de cotação

O [pacote de cotação](Pacote_cotacao_marcenaria_R01.md) pede:
- preços separados para Blum e FGVTN equivalente;
- 40 Minifix definidos e mapeamento dos demais;
- banco com dobradiça piano e trava, mantendo a Southco apenas como alternativa;
- rodízios Leão Aço na P08.

## 5. Uso interno do pedido de cotação

- Meta: **R$35.000** instalado (cenário atual R$46.500). Ver [reconciliação de ferragens](Reconciliacao_ferragens_fichas_R14_2026-10-24.md) e a [revisão de ferragens e serviços](Revisao_ferragens_servicos_2026-10-23.md).
- Pedir no mínimo **3 propostas** com este mesmo pacote, para que sejam comparáveis.
- Não revelar a meta antes de receber as propostas.
- Antes de enviar: escolher as marcenarias e decidir quem será o contato e por qual canal. **Nenhum fornecedor foi contatado.**
