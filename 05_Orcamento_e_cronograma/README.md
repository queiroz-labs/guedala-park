# Orçamento e cronograma

## Risco do cronograma — frente 6, 28/10/2026

**Resultado:** a [fonte R00](Cronograma_obra_e_compras.md) não informa nenhuma moda triangular nem duração de várias etapas. Portanto **P50, P80, probabilidade de terminar em 8 semanas e frequência do caminho crítico não são calculáveis** sem inventar entradas. Solicitados 5.000 cenários; executados **zero cenários do projeto**. O motor valida os dados antes de sortear; não usa moda central, uniforme ou duração zero para preencher lacunas. O teste sintético de 5.000 cenários só verifica o código, não estima este apartamento.

Rede documental com 21 nós, sem ciclos: chaves → medição → executivo → fabricação → inferiores → gabarito → pedras; RT → protocolo → análise → instalações → impermeabilização/cura → revestimentos → pintura-base → vinílico; revestimentos → medição → fornecimento do box. A fonte agrupa marcenaria/pedras/louças/metais/eletros na semana 7–8: esse agregado não foi somado novamente aos componentes. Retoques/testes e mudança não têm dependências completas na tabela; a rede até a mudança permanece incompleta. “Marcenaria” é o caminho crítico **declarado pela fonte**, não uma frequência obtida por simulação.

**O que já se calcula:** no cenário do diagrama, fabricação iniciada na semana 2 + 5–6 semanas termina entre 7 e 8. Acrescentar somente os 1–2 de fornecimento de pedras dá **8–10 semanas de parcelas conhecidas**, ainda sem duração de montagem dos inferiores, gabarito, instalação das pedras/metais, limpeza ou esperas. **8–10 não é intervalo da mudança nem limite superior da obra.** O cenário mínimo consome a janela de 8 semanas antes dessas parcelas; a meta de obra em 8 semanas não está demonstrada. A meta de mudança no terceiro mês (9–12) permanece; nenhuma data foi prometida.

### Limites condicionais de pedido

Conta: `semana necessária − maior prazo escrito`. Semanas são relativas às chaves; negativo = antes. São limites para os marcos do planejamento, **não datas garantidas por uma rede completa**. Dias foram divididos por 7; fornecedor deve informar se o prazo usa dias úteis ou corridos. Não se pressupõe compra de itens existentes ou fornecidos no pacote.

| Item | Prazo escrito (semanas) | Marco de recebimento usado | Último pedido calculado | Limite da conta |
|---|---:|---:|---:|---|
| RT | Ausente | Antes de 0 | A confirmar | Falta duração de contratação; “agora” não é prazo numérico |
| Ferragens | 1–3 | 2 | −1 | Condição: necessárias no início da fabricação; confirmar com oficina e evitar compra duplicada |
| Porcelanatos | 1–4 | 2 | −2 | Fonte recomenda −4, com 2 semanas adicionais frente a esse marco |
| Vinílico | 1–3 | 5 | +2 | Fonte recomenda −3; antecipação de 5 semanas frente a esse marco |
| Louças/metais | 1–2 | 7 | +5 | Marco é o início do agregado 7–8, sem duração própria de instalação |
| E21 para gás | 1–2 | 1 | −1 | Fonte manda pedir em +2, mas exige presença na etapa de gás 1–2; sequência contraditória |
| Eletros | 3–10 dias | 7 | +5,57 | Forno para conferir nicho pode ser necessário antes; marco não informado |
| Luminárias | 1–3 | 6 | +3 | Coincide com pedido previsto; sem folga no prazo máximo |
| Estofados | 2–4 | 7 | +3 | Condição de atender início da montagem; confirmar integração ao pacote |
| Sofás/Berlin/cadeiras | 2–6 | 8 | +2 | Pedido +3/+4 com 6 semanas termina +9/+10, além da primeira semana desejada |
| Box | 1–3 após medição | 6 | +3 | Exigiria medição em +3; fonte prevê +4/+5, entrega possível +5 a +8. Não antecipável às chaves |
| Pedras, para terminar até 8 | 1–2 após gabarito | 8 | +6 | Fonte prevê gabarito +7, fornecimento +8 a +9; sem contar instalação. Não antecipável às chaves |

Não há exigência matemática de comprar **todos** os itens antes das chaves. As recomendações antecipadas da fonte foram preservadas, sem transformá-las em autorização de compra. Box e pedras dependem dos marcos físicos já registrados, não de um pedido antecipado arbitrário.

### Dados exatos que faltam

- **Fornecedores/oficina:** mínimo, mais provável e máximo de cada prazo de entrega/fabricação, em dias úteis ou corridos; confirmar se fila está incluída nos 5–6 semanas. A fila de +2 a +4 é risco separado, sem probabilidade/moda; não foi somada automaticamente.
- **Coordenação/RT:** duração de medição, executivo/aprovação, protocolo/análise, instalações, cura/teste, revestimentos, pintura, piso, montagem, gabarito, instalação final e limpeza; predecessores da liberação para mudança. As células “semana 1–2” são janelas de calendário, não distribuições de duração de 1 a 2 semanas.
- **Pedras:** qual prazo vale, 7–10 dias da seção 1 ou 1–2 semanas da seção 3, e inclui instalação? Com gabarito em +7, o primeiro chega em +8 a +8,43, o segundo em +8 a +9; não somar os dois.
- **E21/forno/box:** em qual marco cada equipamento físico é indispensável? E21 pedido +2 é incompatível com sua presença no início da etapa de gás; box medido +4/+5 pode não chegar para instalação +6.

Nenhuma nova escolha de Elias é necessária para a auditoria acima. A próxima entrada é prazo e sequência confirmados por fornecedores/coordenação, sem contato realizado aqui. Não se refinou projeto condicionado às chaves ou oficina.

Reproduzir com `python -B ferramentas/estudos/cronograma_risco.py --saida ../outputs/Cronograma_risco`; testes: `python -B ferramentas/estudos/test_cronograma_risco.py` (**8 passaram**). Biblioteca padrão; saídas persistentes em `../outputs/Cronograma_risco`, fora do repositório. O JSON guarda a rede, origem/SHA e lacunas; CSV guarda as contas por item. Fonte, orçamento e CAD preservados.

| Saída regenerável | SHA256 |
|---|---|
| `Cronograma_risco.json` | `372872059ecf058b767d8e8faff9781332595f9eaf3369149afd27d7dcb1e511` |
| `Limites_compras.csv` | `c44ef0364846c360a9e8e2d7ebc0473c8cfd3a4ef2e0f6f26ac9918b451acaf7` |

| Arquivo | Para quê |
|---|---|
| [Orcamento/Orcamento_R43.md](Orcamento/Orcamento_R43.md) | R44: execução R$ 137.748,11; excesso R$ 17.748,11 sobre teto de R$ 120 mil + reserva intocada de R$ 10 mil |
| [Orcamento/LEIA-ME.md](Orcamento/LEIA-ME.md) | Estimativas, metas condicionais e divergências; retomada da reconciliação de iluminação e marcenaria |
| `Orcamento/<Categoria>/Analise_*.md` | Detalhe de cada categoria: Marcenaria_35mil, Eletros_e_TV, Loucas_e_metais, Pedras_e_box, Pisos_e_revestimentos, Obra_e_pintura, Instalacoes, Moveis_e_tecidos |
| [Orcamento/Marcenaria_35mil/Pacote_cotacao_marcenaria_R01.md](Orcamento/Marcenaria_35mil/Pacote_cotacao_marcenaria_R01.md) | Pacote D05-C/D06-B com fichas R15, pronto para Elias enviar |
| [Cronograma_obra_e_compras.md](Cronograma_obra_e_compras.md) | Cronograma de obra e o que comprar antes |
| [Plano_execucao_ate_31_10.md](Plano_execucao_ate_31_10.md) | Plano de trabalho diário até 31/10/2026 |

Valores antigos nos documentos são históricos quando divergem do Orcamento_R43. Nada foi contratado ou comprado.

## Compras fora do orçamento

Valores para referência de compras que não constam no R44; não entram na verba nem na reserva.

| Item | Valor | Fonte |
|---|---:|---|
| Cadeira Ercathe A01 Mesh Premium, preta (escritório) | R$ 2.290,90 | [Sensetup](https://sensetup.com.br/products/cadeira-ergonomica-ercathe-a01-mesh-premium?variant=49668774854978), 29/10/2026; Elias, 29/10/2026: “deixa ela fora do orçamento, mas coloca o valor nos documentos” |
| Suporte de monitor ELG F80N, 2º (escritório) | R$ 169,99 | [Kabum](https://www.kabum.com.br/produto/107363/suporte-de-mesa-articulado-para-monitores-de-17-a-35-elg-ajuste-de-altura-com-pistao-a-gas-f80n), Pix, 29/10/2026; Elias, 29/10/2026: “2 deses sendo q já possuo 1” |
| Monitor ASUS TUF Gaming VG27AQ5A 27″ (escritório; o AOC 24″ já é dele) | R$ 2.000,00 | [Kabum](https://www.kabum.com.br/produto/747516/monitor-gamer-asus-tuf-27-qhd-210hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aq5a), Pix, 29/10/2026; Elias, 29/10/2026: “deixa os monitores fora do orçamento igual a cadeira do escritorio” |

Controle de 25/10 consolidado em 26/10 no plano: matriz 20/20 revisada, T01 documental concluída. Estudos, ensaios e dados externos continuam separados; dia 26 em andamento. Reserva de 30–31/10 mantida para integração e conferência.

Plano enxugado em 26/10/2026: cada tarefa T01–T09 indica situação, bloqueio e fonte técnica. Objetivo, prioridades, agenda, critérios, regras de corte e controle diário preservados; medição mantém somente a matriz 20/20 concluída. Retomar T02/T03 (juntas/suspensão); enquanto a oficina estiver indisponível, continuar T04.

T09, conferência de 26/10: ZIP local R20 íntegro, 196 entradas e CAD R52 com hash correspondente; R23 é a configuração corrente e a publicação remota foi conferida: 251 entradas, CRC e hashes sem falhas; testes e geração temporária do site/pacote passaram. [Evidência e próxima ação](../06_Entregas/README.md). Integração de 30/10 e conferência de 31/10 preservadas.

T04/T05, 26/10: margens de engate do banco/cesto e cadeia dimensional do micro calculadas a partir dos estudos salvos. [Avanços e critérios no plano](Plano_execucao_ate_31_10.md). Nenhum ensaio, novo ângulo/altura adotado ou CAD alterado; próximas entradas são dados da trava e altura útil de trabalho sob o micro.

T05 — P08/varal: percurso nominal P08 de 400 mm conferido contra obstáculos fixos; retirada e guias/batente delimitados. No varal, três cenários com roupa longa atingem o envelope da lixeira; distinguir curso vazio/carregado. Resultados e próximas entradas no [plano](Plano_execucao_ate_31_10.md).

T05 — P01/P06 e banheiro: divergências das sete caixas versus FGVTN 500 identificadas por objeto; faixas de retirada e ferramenta do BC43 calculadas. [Plano e próximas ações](Plano_execucao_ate_31_10.md). Montagens ainda condicionadas, sem mudança da R52.

T07 — memória anterior à proposta smart/Shelly: [consolidado](Orcamento/Orcamento_R43.md) distribui CB02 em L01–L07 (4.415,94; diferença 875,94), sem duplicar banheiro/10,62. Provisão marcenaria 46.500 mantida, pedido/formulário reconciliados com alternativas e regra sem tubos. Valores globais R44 preservados; pacote em espera. Próximo: fechar componentes T06 e obter preços comparáveis.

T07 — agenda 27/10: [cenários A/B](Orcamento/Orcamento_R43.md#cenários-para-decisão-r44--agenda-2710) preservam ou adiam TV da sala, com valores/perdas e metas separadas de descontos. A memória de iluminação 4.415,94 é histórica; proposta vigente parcial 4.938,62. R44 permanece 137.748,11. Elias 27/10/2026, resposta “A”: manter TV nesta etapa; obter metas e reduzir mais 1.179,28, além das lacunas.

Coerência 26/10: M09/cortina do quarto é provisão indevida frente ao Registro 21/09; [delta de escopo](Orcamento/Orcamento_R43.md#divergência-de-escopo-m09--corrigir-na-próxima-consolidação) separado de negociação e sem reabrir a escolha. Não cotar M09; incorporar a retirada na próxima revisão financeira. A decisão A no README do orçamento usa os cenários corrigidos, sem contar essa retirada como desconto.

**Controle diário 27/10 preenchido antecipadamente em 26/10:** entregas documentais, verificações, decisões e bloqueios separados no [plano](Plano_execucao_ate_31_10.md#9-controle-diário). Oficina/medidas não foram marcadas como concluídas. Janela de trabalho desta conversa termina 27/10 às 07:30 de Brasília; sem publicação/envios.

P02: uso definido por Elias em 27/10/2026 (U1–U4=A); [plano](Plano_execucao_ate_31_10.md) atualizado. Requisito 10 kg, organização por zonas e preservação de vãos/aparência; comprovação técnica pendente.

P13: F13=A, Arenza liso nas duas faces (Elias,27/10/2026, resposta “a”); [plano](Plano_execucao_ate_31_10.md) atualizado. Produto 18, bordas e inclusão no corte pendentes.

Lixeiras: LIX=A (Elias,27/10/2026, resposta “A”); manter modelos e aceitar avanços 7/6 cm/retirada temporária da Loop se demonstrada. [Plano](Plano_execucao_ate_31_10.md) atualizado; gabarito físico pendente.

Integração 27/10 solicitada por Elias: R53 e fichas R15 incorporam as quatro decisões; pacote local R24, sem novo envio. Gabaritos, produtos e comprovações físicas continuam pendentes.

**Anteprojeto, 27/10/2026:** [D01: três cenários de faseamento](Orcamento/Orcamento_R43.md#fechamento-aritmético-para-decisão-d01--27102026), execução condicional de R$ 118.533,77 a R$ 119.383,77, com luz parcial atualizadaR$ 4.534,55, TV e reserva preservadas. Dependem de R$ 17.317,45 de negociação e propostas comerciais; D01-C para cotação, Elias 27/10/2026, sem contratar. Redução comprovada ainda insuficiente.

**Contraprova D01:** sem outras negociações, após M09 e adiamento M05/M06/M08, marcenaria precisa caber emR$ 29.898,78 (antes das lacunas); pacote 35 mil resultariaR$ 125.101,22. [Memória](Orcamento/Orcamento_R43.md#contraprova-sem-descontos-presumidos--limite-do-pedido-comercial). Não divulgar meta antes das três primeiras propostas.

**D05,27/10:** [três caminhos sem descontos presumidos](Orcamento/Orcamento_R43.md#d05--plano-de-escopo-sem-descontos-presumidos): A 131.501,22, B 119.101,22, C 127.101,22. Créditos por móvel são alvos com fonte histórica, dependem de cotação. C preserva quarto/banco, perde armazenamento do escritório; aporte 7.101,22 recomendado frente ao consumo da reserva. Elias,27/10/2026: "C — cotar com aumento de verba". Cotar pacote 37.000 e execução 127.101,22; reserva 10.000 preservada, sem contratação.

D06 — Elias, 27/10/2026: "B — adiar só E06/prateleiras, manter E05/TV para cotação". D05-C vigente R$ 127.101,22; iluminação R$ 4.534,55.

[Pedido de marcenaria e formulário R15](Orcamento/Marcenaria_35mil/Pacote_cotacao_marcenaria_R01.md) atualizados; escopo inicial e integral separados, frete/instalação/validade por item, sem metas divulgadas.

Conferência final: soma independente das 17 linhas da iluminação = R$ 4.534,55; base comparável R$ 138.742,66; fora da marcenaria R$ 90.101,22 + pacote-alvo R$ 37.000 = R$ 127.101,22. Estado/Roteiro/pontos: 87% documental; retorno comercial pendente.
