# Revisão dos materiais da marcenaria — 23/10/2026

O rateio anterior de R$15.850 em materiais não era levantamento de custo. A revisão cruza a geometria nominal e preços públicos de chapas, com provisões explícitas para itens sem produto definido. **O resultado não demonstra que todo o valor anterior era baixo: mostra uma distribuição inadequada e risco concentrado no quarto e na sala.** Para planejamento prudente, usar como cenário R$20.800 em materiais, sem declarar esse número cotação ou custo executivo fechado.

## Resultado por ambiente

| Ambiente | Rateio anterior de materiais | Faixa calculada aproximada | Provisão prudente proposta |
|---|---:|---:|---:|
| Quarto | R$4.400 | R$4.287–6.199 | R$6.200 |
| Cozinha | R$4.100 | R$3.065–4.883 | R$4.900 |
| Lavanderia | R$1.350 | R$737–1.179 | R$1.200 |
| Escritório | R$2.300 | R$1.630–2.495 | R$2.500 |
| Banheiro | R$1.250 | R$901–1.278 | R$1.300 |
| Sala | R$2.200 | R$2.595–4.213 | R$4.300 |
| Arremates gerais | R$250 | R$250–400 | R$400 |
| **Total** | **R$15.850** | **R$13.464–20.646** | **R$20.800** |

Valores arredondados para comunicação; os centavos dos cálculos são consequência aritmética, não precisão de cotação. Faixa é uma sensibilidade a preços, aproveitamento e provisões, não intervalo estatístico nem garantia de custo máximo. Não aumentar todos os ambientes igualmente: lavanderia e banheiro não demonstraram necessidade de grande alta isolada. A compra é em lote, com sobras compartilhadas; o custo de cada lote foi atribuído aos cômodos proporcionalmente à área, não como se cada cômodo comprasse chapas inteiras próprias.

## O que sustenta a revisão

Fonte geométrica: inventário de sólidos finitos ativos da R44, incluído na consolidação R45. O README da R45 informa que a geometria principal foi preservada; os estudos estruturais ocultos são alternativas e não foram somados como peças adicionais. A classificação selecionou 259 objetos: 257 envelopes de peças e dois envelopes de proteção EPS. Existem peças com status proposta; visibilidade não significa aprovação para fabricar.

- **64,375 m² de envelopes retangulares de painéis**, sem as proteções EPS. Esta área não é área acabada líquida: inclui retângulos envolventes das peças em L e dos recortes, sem crédito automático da sobra. Também não é levantamento completo de corte: os substratos da cabeceira/encosto e arremates recebem provisões separadas.
- **11,858 m² de envelopes de proteção de 10 mm do quarto** separados da madeira. O documento `Revisao_piso_e_armarios_2026-09-25.md` identifica isopor/EPS, não MDF. Material, faces aplicáveis e dimensão final ainda dependem do executivo. Não cobrar esses envelopes como chapas decoradas.
- Fundos de vários armários estão modelados com **18 mm**. Não orçar automaticamente fundo fino de 6 mm para baratear.
- Tampas do banco e painel de TV têm **20 mm**; bancada e algumas prateleiras, **30 mm**. Os preços de MDF decorado18 mm não atendem diretamente a essas peças. Materiais para obter espessura/acabamento corretos estão provisionados à parte; nenhuma espessura foi alterada.
- O fundo nominal do roupeiro mede **2096×1964 mm**, maior que a largura da chapa comercial2750×1850. Precisa de solução de divisão/união antes do plano de corte; a área sozinha não prova que uma chapa atende. Nenhuma união foi aplicada ao CAD nesta revisão.

### Chapas comuns: quantidade por cenário e preço de referência

Chapa de referência2750×1850 mm =5,0875 m². A conta usa **75% e60% de aproveitamento de área**, hipóteses escolhidas para testar sensibilidade. As perdas correspondem a25% e40% da área comprada; não se confundem com acrescentar25% ou40% à área líquida. Arredondamento para chapas inteiras por acabamento/espessura, compartilhadas entre ambientes. Não foi realizado encaixe de peças, orientação de textura, plano de serra ou otimização industrial; quantidades abaixo não autorizam compra.

| Material | Área nominal de envelopes | Chapas no cenário | Preço unitário usado na sensibilidade |
|---|---:|---:|---:|
| Branco TX18 mm | 20,634 m² | 6–7 | R$365,11–400 |
| Arenza18 mm | 23,853 m² | 7–8 | R$435,58–520 |
| Azul Petróleo18 mm | 6,615 m² | 2–3 | R$526–618,67 |
| Off-white18 mm | 2,676 m² | 1 | R$489,94–600 |
| Bege/claro18 mm | 1,854 m² | 1 | R$500–650, provisão sem código escolhido |
| Branco TX15 mm, caixas de gavetas existentes | 2,761 m² | 1 | R$282,67–330 |
| **Subtotal dessas chapas** | | **18–21 chapas** | **R$7.564,33–10.396,01** |

Essa quantidade não inclui os materiais especiais20/30/16/16,2/26,5 mm, substratos estofados e arremates. A atribuição de acabamento é conservadora: frentes, laterais e faces inferiores potencialmente aparentes mantidas decoradas; internos ocultos brancos. Verificar a face aparente de cada peça no executivo, sem acrescentar revestimento interno apenas para forçar branco.

Fontes comerciais consultadas nesta revisão, antes de frete e sem confirmação de entrega ao endereço:

- [Gasômetro — branco TX18 mm Arauco](https://www.madeirasgasometro.com.br/mdf-bp-branco-texturizado-02-faces-2750-x-1850-x-18mm-arauco/p): R$365,11. R$400 é margem de sensibilidade de preço, não segunda oferta.
- [Madeiranit — Arenza18 mm Greenplac](https://www.madeiranit.com.br/mdf-madeiras-e-chapas/mdf-arenza-18mm-2-faces-185cm-x-275cm-greenplac): R$435,58 Pix; R$473,46 cartão. [Madeverde](https://www.madeverde.com.br/chapa-mdf-18mm-arenza-2-faces-greenplac): referência anteriorR$480,04 Pix. R$520 é provisão conservadora, não preço confirmado de HR.
- [Madeiramar — Azul Petróleo18 mm](https://www.madeiramar.com.br/produto/mdf-azul-petroleo-guararapes-18mm-2750x1850-1-6827/): R$526. [Gasômetro — mesmo padrão18 mm](https://www.madeirasgasometro.com.br/mdf-bp-matt-azul-petroleo-02-faces-2750-x-1850-x-18mm-guararapes/p): R$618,67. [Guararapes](https://www.guararapes.com.br/produto/azul-petroleo/) confirma chapa2750×1850, textura Matt e espessuras comerciais; não converter para outro azul.
- [Madeverde — off-white Suave18 mm](https://www.madeverde.com.br/chapa-mdf-off-white-suave-18mm-2-faces-duratex): R$489,94 Pix. Referência de custo, não aprovação de novo código de cor ou textura. SuperiorR$600 é provisão.
- [Gasômetro — branco TX15 mm](https://www.madeirasgasometro.com.br/mdf-branco-texturizado-15mm/c): R$282,67. Uso apenas nas peças já modeladas nessa espessura, sem reduzir caixas estruturais de18 mm.

As páginas indexadas podem mudar. Esses números servem para a faixa de planejamento, não são ofertas entregues garantidas. Não foi utilizado desconto de revendedor condicionado a cadastro nem oferta de loja que declara não enviar chapas para fora do MS.

## Complementos fora das chapas comuns

| Complemento de materiais | Faixa de provisão |
|---|---:|
| Materiais especiais16/16,2 mm das gavetas | R$400–700 |
| Materiais acabados30 mm, bancada/prateleiras/travessa | R$950–1.700 |
| Materiais acabados20 mm, tampas e painelTV | R$1.300–2.100 |
| Contramarcos26,5 mm | R$100–200 |
| Substratos da cabeceira e encosto | R$300–550 |
| Espumas, tecidos e mantas dos estofamentos previstos | R$600–1.150 |
| Espelho lateral do quarto e frontal do banheiro | R$550–800 |
| EPS e proteções/calços aplicáveis | R$250–450 |
| Fitas de borda, colas e consumíveis | R$900–1.600 |
| Sensibilidade a HR/vedação nas áreas úmidas | R$300–600 |
| Arremates gerais não discriminados | R$250–400 |
| **Subtotal** | **R$5.900–10.250** |

Essas faixas são estimativas analíticas, não cotações das soluções completas. Na parcela30 mm, a referência de [MDF cru Duratex](https://www.madeirasgasometro.com.br/mdf-30mm/c) deR$474,44/chapa é somente substrato: não autoriza tratá-lo como Arenza acabado. Colagem, usinagem e aplicação de bordas continuam em serviços, para evitar cobrança dupla.

Para os espelhos, [Carbon Engenharia](https://www.carbonengenharia.com.br/product-page/espelho-lapidado) publicaR$375/m² para4 mm lapidado sem instalação; é referência de outra região e espessura, não proposta local para as peças do projeto. A provisão considera os0,9m² do espelho lateral e aproximadamente0,444m² das duas frentes do banheiro; espessura/fixação ainda a confirmar. EspumaD28 [Jeová Couros](https://www.jeovacourosbh.com.br/espumas/d28) aparece deR$57 por metro linear de1,90m na espessura3cm aR$190 em10cm; são referências, sem mudar a espuma aprovada. Tecidos, densidades e acabamento exigem amostra/cotação.

Fitas comuns aparecem aR$28–58 por rolo50m na [JP Ferragens](https://loja.jpferragensecia.com.br/fitas-de-borda/fitas-de-borda.html), mas outras cores/larguras e especificações custam mais. A verba de fitas/colas considera rolos separados e sobras; não presume que Arenza, azul e bege tenham todos o mesmo preço ou espessura. O perímetro bruto foi usado apenas para distribuir a provisão entre ambientes.

## Efeito no total da marcenaria

| Parcela | Provisão de comparação |
|---|---:|
| Materiais, novo cenário prudente | R$20.800 |
| Mão de obra e serviços, rateio anterior ainda sem cotação | R$15.450 |
| Ferragens, verba anterior ainda sem revisão completa | R$3.700 |
| **Total do cenário** | **R$39.950** |

**R$4.950 acima da metaR$35.000.** Esta conta atualiza somente a leitura dos materiais; não valida a mão de obra, a margem do fornecedor, os fretes ou as ferragens especiais. Transporte da marcenaria permanece na coluna de serviços anterior, sem somar novamente à logística geral. Não prometer o pacote instalado porR$39.950: propostas comerciais podem ficar fora dessa faixa.

R$35 mil permanece objetivo de negociação, não custo demonstrado. Reserva geralR$10 mil preservada; nenhuma alteração de cores, volumes de armazenamento, geometria ou compra realizada. O orçamento central não recebeu um desconto ou aumento definitivo a partir deste cenário. A separação anterior por cômodo fica superada para análise de materiais.

Memória reproduzível: [script](revisar_materiais.py), [peças e envelopes](Levantamento_materiais_2026-10-23.json), [composição e contas](Revisao_custos_materiais_2026-10-23.json). Próximo fechamento quantitativo depende de lista executiva de peças, divisão dos painéis grandes, especificação das espessuras especiais e plano de corte; não de reduzir armazenamento para forçar o teto.
