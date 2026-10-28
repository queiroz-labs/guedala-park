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

**Regra proposta, a confirmar com Elias/oficina:** 191.1360m de bordas retas calculadas; 210.2496m com10% de perda. Portas/frentes:4 bordas, fita1mm; laterais/base/topo/prateleira/apoios:frontal visivel, fita0,45mm; fundos:nenhuma; aparentes:bordas expostas propostas (P13 frente+duas laterais; paineis/faixas4 a conferir). Caixas de gaveta:borda superior, fundo sem fita. C0/C1 medem L, L0/L1 medem C. Contornos especiais sem descricao e arestas sem orientacao ficam pendentes: 23 IDs. Cavas/recortes nao calculados, nenhuma compensacao no C×L. Direcoes frontais propostas por modulo no script; P02 emL exige mapa proprio. Cores agrupadas por nome nominal, nao equivalencia de SKU; espessura de fita e perda sao propostas, nao decisao. Nenhum dos249 mapas foi confirmado. Totais por cor e espessura da fita abaixo; espessura da chapa separada por ID em Fita_por_peca.csv.

## Horas de furação

**Cenário dos2286 centros: 18.23–42.76horas**, incluindo preparação por face. São horas de trabalho/máquina em hipótese de oficina, não prazo de calendário nem levantamento cronometrado. Não incluem centros ainda ausentes, corte, fita, transporte, montagem, ensaio/retrabalho e inspeção. Peças conflitantes e incompletas entram só como cenário de volume, não tarefa executável.

| Tipo | Furos | Horas de perfuração mín.–máx. |
|---|---:|---:|
| Confirmat passagem face | 203 | 0.45–1.13 |
| Confirmat piloto topo | 203 | 0.45–1.13 |
| Minifix piloto pino | 262 | 0.58–1.46 |
| Minifix Ø15 corpo | 262 | 1.82–3.27 |
| Minifix Ø7 topo | 262 | 0.58–1.46 |
| apoio prateleira Ø5 | 8 | 0.02–0.04 |
| caneco Ø35 | 52 | 0.36–0.65 |
| cavilha Ø8 face | 465 | 1.55–3.23 |
| cavilha Ø8 topo | 465 | 1.55–3.23 |
| piloto flange Blum | 104 | 0.23–0.58 |

## Fita por cor e espessura proposta

| Cor | Fita mm | Metros retos | Com10% perda |
|---|---:|---:|---:|
| Arauco Beige Matt | 1.0 | 3.1680 | 3.4848 |
| Arauco Louro Freijó Poro | 0.45 | 1.5000 | 1.6500 |
| Arenza liso (referencia nominal) | 0.45 | 19.5080 | 21.4588 |
| Arenza liso (referencia nominal) | 1.0 | 55.1050 | 60.6155 |
| Branco TX | 0.45 | 49.7320 | 54.7052 |
| Branco TX | 1.0 | 19.2340 | 21.1574 |
| Guararapes Azul Petróleo | 0.45 | 8.1590 | 8.9749 |
| Guararapes Azul Petróleo | 1.0 | 16.5260 | 18.1786 |
| Off-white fosco | 0.45 | 3.0640 | 3.3704 |
| Off-white fosco | 1.0 | 8.3520 | 9.1872 |
| Padrao a definir | 0.45 | 1.4040 | 1.5444 |
| Padrao a definir | 1.0 | 5.3840 | 5.9224 |

## Cenários de conectores para escolha

| Cenário | Minifix | Confirmat | Cavilhas | Horas mín.–máx. |
|---|---:|---:|---:|---:|
| Minifix316 | 316 | 207 | 527 | 18.23–42.76 |
| Desmontagem_proposta | 89 | 434 | 527 | 15.81–37.58 |

Alternativa: propor manter Minifix em P01 (transporte do roupeiro), P17 (caixa longa) e P19 (divergencia ainda aberta); trocar nos demais contatos por Confirmat+cavilha/cola. E uma proposta de onde desmontar, nao necessidade comprovada. Politica_desmontagem.csv identifica cada junta, motivo e quantidade; Cenarios_conectores_por_movel.csv mostra o impacto. Nao foram trocados o mapa nem os CSVs de coordenadas. Confirmar transporte, cabecas aparentes, acesso exterior e possibilidade de cola antes de escolher. Fixacoes de pecas removiveis nao cobertas pelo mapa continuam pendentes.

As horas alternativas substituem apenas os tres centros Minifix por dois estagios Confirmat nos grupos ja mapeados; operacao escalonada considera passagem+escareado no mesmo ciclo, a confirmar com a broca. Contatos sem centros permanecem na compra condicional, sem inventar horas. Preparacao por face e recalculada; cola/aperto/montagem ficam fora. Cavilhas mantidas; nenhum volume de cola inferido. Demais familias sao as mesmas de Ferragens_por_movel.csv.

Limitador86: manter52. Produto70T3553 em [Blum p.76](https://publications.blum.com/2024/catalogue/en/76/); a [regra oficial de montagem](https://ea.blum.com/en/opening-angle-stops-for-110-and-107-hinges/) determina um em cada dobradica da porta que receber o recurso (artigo sem paginacao). A pagina do catalogo identifica o produto; nao atribuir a ela a regra do artigo.

**P19:12 documentais ×8 do mapa. Nenhuma troca decidida.** Quatro conjuntos de diferenca estao ligados a classificacao generica do fundo como Confirmat. Manter as duas quantidades visiveis e reconciliar o detalhe do fundo antes da cotacao definitiva.

**Perguntas para Elias:** manter cenario316 ou escolher alternativa com desmontagem em P01/P17/P19? Confirmar regra de fita e espessuras1/0,45mm com10% de perda? No P19, preservar detalhe de12 Minifix ou propor8+Confirmat no fundo?

Hipóteses: caneco/corpo 25–45s; cavilha 12–25s; demais 8–20s; preparação 2–5min por face. Opções `--tempos CSV` (tipo;segundos_min;segundos_max), `--setup-min` e `--setup-max` substituem taxas. Quantidades e subtotais por móvel em Horas_furacao.csv. Não somar linhas Subtotal novamente.

Reproduzir: `python -B ferramentas/estudos/quantificar_furacao.py`; `--saida DIR` para ensaios externos. Quantitativos monetários de R44, medidas do imóvel e modelo não foram alterados.
