# Risco de orçamento e prazo

**Simulação condicional, sem nova decisão ou revisão de orçamento/cronograma.** as faixas refletem as hipóteses de entrada, não a realidade; itens sem base vêm de regra de simulação.
Semente 20261029, numpy 2.5.2, PCG64; 20000 iterações por cenário. Data das chaves: não documentada; datas de calendário indeterminadas. Resultados de prazo em semanas corridas após chaves.
Comparação sem propostas normalizadas; nenhum preço real usado. Nenhuma oferta incompleta ou fictícia foi transformada em preço equivalente completo.

## Percentis

| Cenário | Métrica | P10 | P50 | P80 | P90 |
|---|---|---:|---:|---:|---:|
| Integral_R44 | execucao | 129793.72 | 138282.74 | 144072.25 | 146966.33 |
| Integral_R44 | mudanca | 10.44 | 11.37 | 12.84 | 13.76 |
| Etapa_D05C_documentada | execucao | 120453.30 | 127534.36 | 132361.25 | 134790.12 |
| Etapa_D05C_documentada | mudanca | 10.44 | 11.37 | 12.84 | 13.76 |
| Somente_se_propostas_ate35mil | execucao | 122928.74 | 126793.12 | 129297.71 | 130609.04 |
| Somente_se_propostas_ate35mil | mudanca | 10.44 | 11.37 | 12.84 | 13.76 |
| Medida_real_diverge | execucao | 131518.95 | 140272.18 | 146220.60 | 149183.79 |
| Medida_real_diverge | mudanca | 10.90 | 11.69 | 13.19 | 14.38 |
| Sem_refazer_impermeabilizacao | execucao | 129788.57 | 138273.09 | 144069.53 | 146966.33 |
| Sem_refazer_impermeabilizacao | mudanca | 10.19 | 11.02 | 12.51 | 13.75 |
| Pedras_1a2_semanas | execucao | 129805.88 | 138294.52 | 144096.81 | 146980.51 |
| Pedras_1a2_semanas | mudanca | 10.70 | 11.67 | 13.14 | 14.05 |

## Probabilidades condicionais

| Cenário | Execução ≤120mil | Execução ≤130mil | Marcenaria ≤35mil | Mudança ≤9 / ≤10 / ≤12 |
|---|---:|---:|---:|---|
| Integral_R44 | 0.1% | 10.6% | 1.2% | 0.0% / 1.8% / 69.2% |
| Etapa_D05C_documentada | 8.6% | 66.6% | 31.3% | 0.0% / 1.8% / 69.2% |
| Somente_se_propostas_ate35mil | 1.1% | 85.8% | 74.9% | 0.0% / 1.8% / 69.2% |
| Medida_real_diverge | 0.0% | 6.3% | 0.2% | 0.0% / 0.1% / 63.4% |
| Sem_refazer_impermeabilizacao | 0.1% | 10.6% | 1.2% | 0.0% / 5.1% / 76.1% |
| Pedras_1a2_semanas | 0.1% | 10.5% | 1.2% | 0.0% / 0.6% / 61.3% |

Execução é gasto simulado. Reserva fixa de10mil não é custo incorrido: total planejado = execução + reserva; probabilidade desse total ≤ R$ 130 mil é a mesma da execução ≤ R$ 120 mil. Execução ≤ R$ 130 mil admite consumir reserva; isso não autoriza fazê-lo. Meta de R$ 35 mil é comparada ao pacote com retrabalho, além do preço de proposta isolado no CSV. Integral R44 tem centrais137.748,11; D05-C documental tem127.101,22; ambos são bases documentais sem contrato, não somados.
O cenário “Somente_se_propostas_ate35mil” impõe R$ 35 mil como teto de entrada de proposta integral, não calcula chance de conseguir desconto. Retrabalho/armazenamento podem fazê-lo ultrapassar. “Medida_real_diverge” força a ocorrência, sem inferir probabilidade da tabela de medidas. “Com_climatizacao_a_cotar” não foi calculado: custo ausente não é zero. Impermeabilização opcional altera somente prazo; não se retirou custo sem rateio.

## Entradas, hipóteses e rede

[JSON editável](../../ferramentas/estudos/modelos/Risco_hipoteses.json) e [percentis](Percentis.csv), [resumo](Resumo_cenarios.csv), [Spearman](Sensibilidade.csv), [criticidade dinâmica](Criticidade.csv). Os custos de cada categoria conservam origem/central/tipo no JSON. Estimativa usa±15%, provisão±30%, cotado sem validade±10%, preço confirmado é ponto. São regras de simulação onde falta faixa completa; não ofertas. Pontos podem ser editados para faixa documentada em triangular. Reserva é ponto separado e climatização adicional está sem base.
Custos_chapas/Custos_cenarios/Custos_propostas são parciais de subconjuntos, não faixa instalada das categorias: não extrapolar. Limite_e_metas e análises históricas não substituem a tabela R44. Ofertas completas integrais do comparador, se surgirem, criam cenário Fxx por faixa, com moda central hipotética; não escolhe fornecedor. Confirmação por SKU e serviços continua necessária.
Reaproveita os29 nós de Cronograma_risco e o motor topológico existente. O agregado da semana 7–8 sai para evitar duplicação, e são acrescentadas montagem restante, instalação de pedras e louças/eletros. Predecessores novos estão marcados no JSON como hipótese. Marcenaria corre em paralelo à obra; inferiores aguardam fabricação e piso; gabarito e pedras vêm depois. Semanas de serviço ausentes recebem faixas explícitas de hipótese, não alegação de medição.
Fabricação de 5–6 semanas, abastecimento de 1–3 semanas e box de 1–3 semanas são limites típicos documentados, não compromisso. Modas centrais são hipóteses. Pedras de 7–10 dias e 1–2 semanas são cenários separados. RT, envio e definições começam em −4 por hipótese de preparo antecipado; não é data conhecida. Confirmar disponibilidade e calendário útil/corrido; simulação usa dias/7.
Eventos, probabilidades e impactos estão no JSON: exigência do condomínio 20%, medida divergente 25%, falta de material 20%, atraso de marcenaria 20% e pedra 15%. Não são frequências observadas. Fila de oficina 2–4 entra somente no evento, fora do prazo de produção. Retrabalho 2–5–10% da marcenaria só ocorre no mesmo evento que atrasa executivo; armazenamento hipotético de R$ 150/semana incide após semana 12.
Materiais além das ferragens são supostos disponíveis no início de cada etapa; seus limites de pedido anteriores permanecem em Limites_compras.csv e devem ser conferidos. O evento de falta de material está ligado ao abastecimento de ferragens no JSON; atrasos adicionais de outros materiais não estão quantificados. Resultado de 0% significa zero ocorrências na amostra, não impossibilidade; erro amostral máximo aproximado de 0,35 ponto percentual em 20 mil, sem cobrir erro das hipóteses.
Preços e durações-base independentes. Mesmo evento de retrabalho gera atraso/custo; mudança além de12 gera armazenamento. Sem correlação de mercado presumida. Correlações de Spearman não são efeitos causais nem parcelas somáveis. Frequência crítica é fração de cenários com folga total zero, recalculada por passagens direta/reversa; empates contam todos os nós críticos. O sumário anterior sem parâmetros permanece indeterminado: esta é outra análise com hipóteses autorizadas.
Medidas: 42469 vínculos e 101 linhas da cotação expostas; não são quantidades de compras, peças novas ou percentuais de reajuste. O cenário de divergência usa esse sinal de exposição, sem ratear custo por contagem.

## Onde melhorar a informação

| Entrada | Alvo | Spearman | Pergunta |
|---|---|---:|---|
| Marcenaria | custo | 0.881 | PQ-028 |
| risco:atraso_marcenaria | prazo | 0.684 | PQ-002 |
| analise_condominio | prazo | 0.327 | PQ-004 |
| risco:medida_divergente | prazo | 0.234 | PQ-001 |
| Obra e pintura | custo | 0.214 | PQ-018 |

Prioridade indicativa por associação no modelo: obter cotação, prazo aceito, medidas e parecer nos IDs do [pacote](../../01_Programa_e_decisoes/Perguntas_em_aberto/README.md). Não demonstra valor monetário de informação nem ganho garantido de prazo. Os dez primeiros por alvo/cenário estão no CSV.

## Rodar

Da raiz, `. ..\ferramentas_locais\ativar.ps1`, depois:

```powershell
python -B ferramentas/estudos/risco_orcamento_prazo.py
python -B ferramentas/estudos/test_risco_orcamento_prazo.py
```

`--entrada caminho.json`, `--iteracoes 20000` ou mais, `--data-chaves YYYY-MM-DD` somente quando informada/documentada; `--saida` exige pasta externa. `--gerar-modelo` substitui a configuração: não usar sobre hipóteses próprias sem preservar a entrada externa. Mesma semente/configuração/versão reproduz arrays e estatísticas. Histograma CSV e iterações NPZ ficam externos; nenhum pacote novo instalado.

SHA256 Simulacao_risco.json: `9530d800e7d5f8474edda725397f0f0b113f7624bcb137842b20824d946fb65a`. Os hashes individuais de iterações/histogramas e fontes estão nesse manifesto externo.
