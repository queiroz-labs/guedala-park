# Plano de corte — cenários de refilo e serra

## Resultado e cobertura

**Nos três cenários de chapa 2750 × 1850, o melhor arranjo encontrado usa 15 chapas para 215 painéis.** O limite inferior agregado por área/grupo é 14; lacuna de uma chapa. Isso não completa a compra: dos **249 IDs vigentes**, 33 mantêm bloqueios de material/composição e **P01/Peca208 não cabe no formato**. A conta integral, incluindo esse fundo inteiro, é inviável em 1850. Não se adotou emenda nem redução da peça.

Este é um estudo nominal adicional solicitado em 29/10/2026. Reutiliza o [motor e a base corrente](../Proximas_decisoes/Corte_e_formatos/README.md), sem substituir a cotação já documentada: aquele conjunto misto de **14 chapas, oito 1850 + seis 2100**, inclui os 216 painéis classificáveis. Aqui, todas as chapas têm largura 1850; portanto **15 não deve ser comparado com 14 como se fossem o mesmo escopo/formato**.

[Lista completa](Lista_de_corte.csv): 249 IDs-base, 36 peças propostas identificadas por kit e uma linha de sensibilidade. **As 286 linhas não se somam:** são bases alternativas. [Resumo por grupo/cenário](Resumo_chapas.csv): 216 linhas para nove variantes × três cenários × oito grupos. Quantidade por ID, eixos originais C/L, bordas C0/C1/L0/L1, espessura/metragem/situação da fita estão na lista; propostas e sensibilidade mantêm bordas pendentes. A variante `base` é a referência; as demais são opções separadas, não decisões adotadas.

| Padrão / espessura | Peças cortáveis | Chapas encontradas nos três cenários | LI | Lacuna |
|---|---:|---:|---:|---:|
| Arenza 18 mm | 39 | 3 | 3 | 0 |
| Azul Petróleo 18 mm | 20 | 2 | 1 | 1 |
| Beige Matt 18 mm | 2 | 1 | 1 | 0 |
| Branco TX 15 mm | 35 | 1 | 1 | 0 |
| Branco TX 16 mm | 8 | 1 | 1 | 0 |
| Branco TX 18 mm | 100 | 5 | 5 | 0 |
| Louro Freijó Poro 18 mm | 4 | 1 | 1 | 0 |
| Off-white fosco 18 mm | 7 | 1 | 1 | 0 |
| **Total do subconjunto** | **215** | **15** | **14** | **1** |

O Branco 18 tem 101 painéis classificáveis; a linha acima exclui somente Peca208. O CSV mostra tanto a área/limite inferior do grupo inteiro quanto o subconjunto possível. **Limite por área do grupo inteiro não torna viável um painel que excede a largura.** Nenhuma das heurísticas demonstra ótimo global. Igualdade com LI prova apenas a quantidade mínima daquele grupo/subconjunto nas hipóteses calculadas.

## Áreas e sobras da base

Reconciliação dos 249 envelopes: **59.26277600 m² = 11.32564000 m² bloqueados + 4.11654400 m² fora do formato +43,820592 m² posicionados**. Áreas nominais de uma face, sem descontar recortes.

Área de envelopes efetivamente posicionados: **43,820592 m²**. Área bruta das 15 chapas: **76,312500 m²**. Aproveitamento bruto: **57,42%** em todos os cenários; o denominador útil muda com o refilo.

| Refilo por borda / serra | Janela útil (mm) | Refilo (m²) | Serra (m²) | Retalhos úteis >300 × 300 (m²) | Retalhos menores (m²) |
|---|---|---:|---:|---:|---:|
| 10 / 4 mm | 2730 × 1830 | 1,374000 | 0,968639 | 27,804648 | 2,344621 |
| 0 / 3 mm | 2750 × 1850 | 0 | 0,728423 | 29,350369 | 2,413117 |
| 20 / 4 mm | 2710 × 1810 | 2,736000 | 0,968939 | 26,228889 | 2,558080 |

Identidade conferida antes do arredondamento: **área bruta = painéis + refilo + serra + retalhos úteis + retalhos menores**. Perda sem retalhos úteis é refilo + serra + retalhos menores; não é igual a toda a área não ocupada por peças. As folhas livres da árvore são disjuntas. Somente retângulos com **ambas** as dimensões estritamente maiores que 300 mm contam como úteis. Reutilização física/comercial, armazenamento e crédito financeiro não estão demonstrados; nenhuma sobra vira desconto automático.

## Peças que não cabem e exclusões reais

| Base/opção | Painel | Dimensões nominais (mm) | Resultado com/sem refilo |
|---|---|---|---|
| Base atual | P01/Peca208 | 2096 × 1964 × 18 | Não cabe nem sem refilo, em qualquer rotação |
| Opção P01/P03 traseiro | Estudo_Peca208 | 2114 × 1964 × 18 | Não cabe nem sem refilo, em qualquer rotação |

São os únicos envelopes maiores que o formato entre os 249 atuais e as 36 propostas. Testar o conjunto **com** esses painéis informa inviabilidade; o número de chapas informado é sempre **sem** o respectivo painel. Não existe quantidade finita de chapas 1850 que resolva o fundo inteiro sem modificar sua geometria. Produto maior ou emenda exigem tratamento separado; nenhuma solução física foi implementada.

Os 33 bloqueios da base permanecem individualizados em `Lista_de_corte.csv` e no [inventário vigente de exclusões](../Proximas_decisoes/Corte_e_formatos/README.md#peças-ainda-fora-do-cálculo): 17 Arenza referenciais, cinco espessuras/composições especiais, nove acabamentos parciais e dois substratos com espelho. Não se transformou referência de cor em SKU, nem envelope de 30 mm em uma chapa comercial. O CSV também registra cabimento individual dos excluídos: caber geometricamente não resolve o material.

Perguntas já necessárias para completar a compra: os 17 Arenza referenciais compartilham o produto escolhido? Qual produto/composição vale para os outros 16 bloqueados? Qual formato útil permite o fundo inteiro, com processo e transporte viáveis? São lacunas existentes de produto/oficina, não novas escolhas de cor.

## Sensibilidade de espessura e sete propostas

**Hipótese isolada:** P01/Peca245, Branco TX, de 18 para 15 mm, mantendo envelope 705 × 550 mm. A peça muda de grupo de espessura: o Branco 15 passa de 35 para 36 painéis e Branco 18 de 100 para 99 cortáveis. Nos três cenários, permanece **uma chapa Branco 15 + cinco Branco 18**; total 15. Não se demonstrou economia de chapa comprada. O volume da peça diminui 0,00116325 m³, mas rigidez, apoios, ligações, furação e dimensionamento não foram revisados. É teste de sensibilidade, não proposta estrutural adotada.

As sete opções vêm diretamente do JSON persistido de [Quantitativos](../Quantitativos/README.md), derivado de `extrair.py`. Não houve leitura de BREP/CAD nesta execução. Cada opção substitui somente os IDs indicados na extração e acrescenta os seus componentes; as sete nunca são acumuladas.

| Opção separada | Peças propostas | Substituições | Acréscimos | Tratamento no corte |
|---|---:|---:|---:|---|
| P01 prateleiras 723 | 2 | 2 | 0 | Produto herdado das originais como hipótese |
| P01 soco R01 | 21 | 0 | 21 | Acréscimos sem produto individualizado: excluídos |
| P01/P03 traseiro | 2 | 2 | 0 | Produto herdado; fundo alternativo continua impossível em 1850 |
| P04 fundo 308 | 1 | 1 | 0 | Produto herdado como hipótese |
| P15 composição 36 | 4 | 3 | 1 | Substitutas herdadas; nova camada sem produto individualizado |
| P17 fundo 550 | 1 | 1 | 0 | Produto herdado como hipótese |
| Bancada de marcenaria | 5 | 2 | 3 | Substitutas conservam bloqueios das originais; acréscimos sem produto |

Todas ainda encontram 15 chapas **no respectivo subconjunto calculável**, não necessariamente para o kit completo. As 25 peças acrescentadas não receberam acabamento fictício. Nas duas substitutas da bancada o bloqueio anterior também permanece. Portanto uma contagem igual não comprova custo zero das propostas. As áreas geométricas da extração são conferidas contra os envelopes retangulares das 36 peças; não se compra chapa apenas dividindo a área líquida.

## Método, conferência e arquivos

- Único motor: `ferramentas/estudos/corte_guilhotina.py`, com 48 ordens/heurísticas determinísticas por grupo. A extensão `plano_corte_cenarios.py` altera refilo/serra apenas em memória e restaura os parâmetros; não muda `Parametros.json` nem gera outro extrator.
- Arenza e Louro: maior dimensão paralela a 2750, rotação proibida, conforme hipótese vigente. Arenza continua descrito como liso; não se afirma que tenha veio físico. Branco TX, Azul, Beige e Off-white podem girar. Cores/espessuras distintas não compartilham a mesma chapa.
- Dimensões são envelopes nominais; não se deduz fita nem se inventa blank final. Contornos especiais consomem retângulo completo. Sem encaixar vazios de recortes.
- Reconciliação: 249 IDs únicos e **1,060405325 m³** coincidem por móvel com `Massas_por_movel.csv`. Essa fonte contém volume, não área: o detalhe externo soma área por móvel/espessura, multiplica cada parcela pela sua espessura e só então compara volumes. Não se divide volume global por 18 mm.
- Cada plano passa pelo verificador do motor: árvore de guilhotina, IDs únicos, dimensões, orientação, ausência de sobreposição, margens, separação de serra e reconciliação de áreas. Seis testes próprios cobrem oversize, conservação de área, corrupção de posição/saída da chapa, 249/36 IDs, material e rotação.

```powershell
python -B ferramentas/estudos/plano_corte_cenarios.py --saida ../outputs/Plano_de_corte
python -B ferramentas/estudos/test_plano_corte_cenarios.py
python -B ferramentas/estudos/test_corte_guilhotina.py
```

Os 405 SVGs e a árvore completa ficam em `../outputs/Plano_de_corte/`, fora do Git. `Hashes_desenhos.json` lista o SHA256 individual dos desenhos. `Planos.json` contém as árvores e hashes das entradas, sem copiar caminhos pessoais da extração histórica. Somente lista e resumo compactos entram no repositório. 

| Arquivo externo | SHA256 |
|---|---|
| Planos.json | `eb7d827d1c32926ca0497851470b506fd7f97071f16b91088f5145298f9fb419` |
| Hashes_desenhos.json | `9b3dad6876e8f8ae8e0c44d511d45c1f509a9faa758ffa8e22c0b9706f608253` |


## Comparação financeira — depende de cotação integral

**A meta de R$35 mil não está demonstrada.** Há um plano do subconjunto, mas ainda faltam preços e peças. Os três cenários compram as mesmas quantidades; refilo/serra mudam retalhos, sem economia de chapa encontrada.

| Opção isolada para Off-white 18 | Parcial de chapas com referência/provisão | Parcial + hipótese de fita HF | Saldo até R$16 mil para tudo que falta |
|---|---:|---:|---:|
| Lume | R$5.556,43–6.366,81 | R$5.948,43–7.178,81 | R$8.821,19–10.051,57 |
| Areia | R$5.610,94–6.421,32 | R$6.002,94–7.233,32 | R$8.766,68–9.997,06 |
| Nuvem, alternativa documental | R$5.574,11–6.384,49 | R$5.966,11–7.196,49 | R$8.803,51–10.033,89 |

**Esses parciais não são total de materiais nem intervalo garantido.** Só 13 das 15 chapas têm referência/provisão aplicável ao ensaio; faltam uma Branco TX16 e uma Louro 18. Também faltam os 33 painéis bloqueados, fundo inteiro P01 em formato viável, substratos/estofados/espelhos/arremates fora do subconjunto, adesivos, consumíveis e condições de frete. Não há crédito financeiro de retalhos.

[Custos por grupo](Custos_chapas.csv), [nove comparações financeiras](Custos_cenarios.csv), [fita por cor/espessura e hipótese de rolos](Fita_custo_hipotese.csv). Branco 18 R$365,11–400; Branco 15 R$282,67–330; Arenza 18 R$435,58–520; Azul 18 R$526–618,67: referências históricas de 23/10, com limites superiores de provisão onde identificados. Beige 18 R$500–650 é provisão sem SKU, separadamente rotulada. Não há preço compatível para Branco 16/Louro 18; células vazias não significam grátis. Fonte: [revisão de materiais](../../05_Orcamento_e_cronograma/Orcamento/Marcenaria_35 mil/Revisao_materiais_2026-10-23.md).

Lume R$589,47, Areia R$643,98 e Nuvem R$607,15 vêm do [Caderno, consulta 27/10](../../01_Programa_e_decisoes/Caderno_de_especificacoes.md). Aplicados somente como opções à chapa Off-white 18 de2750 × 1850, nunca às outras cores/espessuras. Lume/Areia têm prioridade de amostra conforme D02; Nuvem permanece comparação documental. Nenhuma cor escolhida pelo cálculo; preços não foram atualizados nem são oferta entregue.

**HF, somente sensibilidade financeira da fita:** 191,1360m de bordas propostas; com 10% de perda por grupo,210,2496m. A regra disponível cobre226 painéis;23 seguem sem definição. Arredondar cada grupo cor+espessura para rolos50m, supondo uma única largura por grupo, dá14 rolos. Aplicar genericamente R$28–58/rolo do registro histórico dáR$392–812. Isso não comprova preço/estoque/compatibilidade dos produtos1mm,0,45mm ou cores escolhidas; largura por painel e SKUs faltam. Quantidade definitiva de rolos pode mudar. Não é perímetro integral de todas as bordas, nem custo completo dos 23 pendentes. Colagem é serviço; não somar R$2,50/m anunciado a uma oficina que já inclua borda.

**Quanto falta para a meta:** o cenário histórico R$20.800 materiais +R$9.200 ferragens +R$16.500 serviços =R$46.500 excede35 mil em **R$11.500**. Para manter essas duas últimas verbas, sobrariam **R$9.300 para todos os materiais**, R$6.700 abaixo da meta isolada de16 mil. Com materiais16 mil, o total seria41.700: faltaria reduzir6.700 nos demais grupos. A negociação histórica16.000+6.500+12.500 fecha35.000 apenas aritmeticamente; nenhum desses descontos foi obtido. [Revisão de ferragens/serviços](../../05_Orcamento_e_cronograma/Orcamento/Marcenaria_35 mil/Revisao_ferragens_servicos_2026-10-23.md).

A faixa anterior de materiais R$13.464–20.646 inclui provisões e geometria antiga, diferente deste subconjunto. A comparação não demonstra economia pela diferença entre totais. Ferragens/serviços históricos incluem mecanismos e reforços posteriormente revistos; são referência financeira, não reintrodução de aço, Southco ou escolhas superadas. Orçamento, pacote de cotação e geometria permanecem intactos.

**Perguntas para fechar preço:** ao fornecedor, valor entregue por padrão/espessura/formato real, fita por SKU/largura/espessura, processamento e inclusões; à oficina, alternativa do fundo e orçamento dos 33 bloqueados após composição. Quanto do pacote completo cobre estofamento, espelhos, frete e montagem sem duplicar serviços? Sem essas respostas, não há valor total nem falta final quantificável.

Reproduzir custo: `python -B ferramentas/estudos/custo_plano_corte.py`; três testes em `test_custo_plano_corte.py` verificam ausência de preço por espessura/cor, opções não cumulativas e arredondamento de rolos.

## Integridade dos CSVs gerados

Complemento: [Custos_propostas.csv](Custos_propostas.csv) traz 63 linhas (sete propostas isoladas × três cenários × três opções Off-white). Todas mantêm 15 chapas, 13 com referência/provisão: parcial Lume R$ 5.556,43–6.366,81; Areia R$ 5.610,94–6.421,32; Nuvem R$ 5.574,11–6.384,49. Delta precificável de chapas = R$ 0, **não custo zero da alteração**. Fita e total ficam vazios; IDs bloqueados e custos ausentes são explícitos. Soco: 54 bloqueados; P15: 34; bancada: 36; demais: 33, além do fundo fora do formato. Não herdar fita da base para peças alteradas.

`../outputs/Plano_de_corte/Retalhos.csv`: 4.588 retângulos, com variante, cenário, cor, espessura, SVG/chapa, posição, dimensões, área e indicador de ambas as dimensões >300 mm. Não acumular cenários/variantes nem confundir retalho pequeno com reaproveitável. Arquivo volumoso fora do Git, sem crédito financeiro. Exportador: `python -B ferramentas/estudos/complementar_corte.py`; três testes em `test_complementar_corte.py`. Lê o plano persistido com SHA conferido; não reotimiza nem muda desenhos.

SHA256 Retalhos.csv: `74c6a69119901922bc8c93eb7819dab470f9faaa9f3105ea24292c98a6cb8448`.
SHA256 Custos_propostas.csv: `cc9eed06e0e80b2c705162870951c4293ff7777e584c691ccb78dc7f83361c62`.

| Arquivo | SHA256 |
|---|---|
| Lista_de_corte.csv | `814bebb168e4ee8c1cc81e86bb830e644f89da72f7e446d08ec13aed4f235678` |
| Resumo_chapas.csv | `0b7771a2ffe4f9d920d168b92af8254702f9b5fbbb9e56ca38e52ada8b9c4396` |
| Custos_chapas.csv | `df0040db8c576713fb835841e6f300cfaf435e4819f20918be66b48dbff301d8` |
| Custos_cenarios.csv | `ca6ae62dc3a736b2abd4e13711a5cba0f6ea829c0e0d6c5d9abf5f51c8a9404f` |
| Fita_custo_hipotese.csv | `bf854c89372b4867169c7f33857c59646e9cebf8f02b7f11d3c8b0463de96f47` |
