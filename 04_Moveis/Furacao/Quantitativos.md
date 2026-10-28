# Quantitativos para cotação — cenário nominal

## Ferragens

| Família | Quantidade cenário | Base R44 comparável | Diferença |
|---|---:|---:|---:|
| Dobradiça Blum 71B3550 | 52 | 52 | 0.0 |
| Base Blum 173H7100 | 52 | 52 | 0.0 |
| Corrediça FGVTN500 | 7 | 7 | 0.0 |
| Corrediça MOVENTO400 | 2 | 2 | 0.0 |
| Suportes de prateleira | 8 | 8 | 0.0 |
| Minifix 15 | 316 | 52 | 264.0 |
| Limitador 86 | 52 | 0 | 52.0 |
| Confirmat 7x50 | 207 |  |  |
| Cavilhas Ø8x30 | 527 |  |  |
| Parafusos | 302 |  |  |
| Parafuso face a face | 52 |  |  |

316 Minifix do mapa são cenário de contatos, incluindo juntas com centros pendentes. Não somar os 52 documentais nem os 60 do loteB. P19 passa de12 para8 Minifix porque a regra genérica atribui Confirmat ao fundo: isso é divergência a resolver com o detalhe existente, não substituição automática da decisão. P10/11/15 mantêm20/12/8. Confirmat e cavilhas incluem quatro Confirmat e oito cavilhas documentais do quadro P18, que não tem contatos elegíveis no mapa.

Os 52 dobradiças/52 bases/52 limitadores e7 pares FGVTN500/2 MOVENTO400 são quantidades documentais. A conferência das portas ainda condiciona sua adoção. Engates FGVTN são sete pares incluídos a confirmar; MOVENTO dois pares separados. Parafusos das guias/engates e frentes, retenções e outras linhas sem contagem constam em Ferragens_pendentes.csv. Piano: 2 trechos e 4 articuladores documentais; produto e fixadores condicionados. Não equivalem a zero. Parafusos dos canecos/bases208 incluídos na lista documental; pinos Minifix são componentes dos conjuntos, sem nova compra duplicada.

R44 T07 reconhece 52 Minifix definidos e 60 candidatos; a memória financeira antiga tinha 20. O cenário 316 difere em+264 dos 52, +204 do subtotal condicional112 e+296 dos20 históricos, sem converter nenhum subtotal em pedido de compra. Orçamento preservado; não se inferiu custo por unidade a partir da provisão global de ferragens.

## Fita de borda

**249 IDs sem mapa C0/C1/L0/L1 nem espessura de fita. Metragem definida: desconhecida.** Soma dos perímetros de envelopes: 477.6400m, somente referência geométrica; inclui bordas ocultas e não representa contorno real de peças especiais. Não é teto garantido para recortes. Por cor e espessura **da chapa** em Fita_por_cor.csv; coluna da espessura **da fita** vazia. Sem percentual de perdas ou compra de rolos inventados. P18 também requer selagem de bordas/cavas/furos, produto pendente.

## Horas de furação

**Cenário dos2286 centros: 18.23–42.76horas**, incluindo preparação por face. São horas de trabalho/máquina em hipótese de oficina, não prazo de calendário nem levantamento cronometrado. Não incluem centros ainda ausentes, corte, fita, transporte, montagem, ensaio/retrabalho e inspeção. Peças conflitantes e incompletas entram só como cenário de volume, não tarefa executável.

| Tipo | Furos | Horas de perfuração mín.–máx. |
|---|---:|---:|
| Confirmat passagem face | 203 | 0.45–1.13 |
| Confirmat piloto topo | 203 | 0.45–1.13 |
| Minifix piloto pino | 262 | 0.58–1.46 |
| Minifix Ø15 corpo | 262 | 1.82–3.27 |
| Minifix Ø8 topo | 262 | 0.58–1.46 |
| apoio prateleira Ø5 | 8 | 0.02–0.04 |
| caneco Ø35 | 52 | 0.36–0.65 |
| cavilha Ø8 face | 465 | 1.55–3.23 |
| cavilha Ø8 topo | 465 | 1.55–3.23 |
| piloto flange Blum | 104 | 0.23–0.58 |

Hipóteses: caneco/corpo 25–45s; cavilha 12–25s; demais 8–20s; preparação 2–5min por face. Opções `--tempos CSV` (tipo;segundos_min;segundos_max), `--setup-min` e `--setup-max` substituem taxas. Quantidades e subtotais por móvel em Horas_furacao.csv. Não somar linhas Subtotal novamente.

Reproduzir: `python -B ferramentas/estudos/quantificar_furacao.py`; `--saida DIR` para ensaios externos. Quantitativos monetários de R44, medidas do imóvel e modelo não foram alterados.
