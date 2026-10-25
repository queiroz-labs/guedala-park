# Conferência de dez caixas e da parede da cozinha

22/10/2026. Atualiza a [análise anterior](Analise_pisos.md). **A estimativa cabe em aproximadamente R$17 mil: R$16.998,13, com somente R$1,87 de folga.** O resultado é de planejamento nominal, não preço fechado nem liberação de compra.

| Etapa | Valor |
|---|---:|
| Revisão anterior de pisos e revestimentos | R$18.074,92 |
| Uma caixa a menos do mesmo Olmo | −R$596,79 |
| Retirada da provisão de azulejo genérico da cozinha | −R$480,00 |
| **Revisão após conferência** | **R$16.998,13** |
| Redução contra os R$20.542,24 iniciais | R$3.544,11 |

Não foi descontado nenhum novo valor de mão de obra. Preparo do contrapiso, colagem, rodapés, acústica, pisos e cores permanecem. Fretes continuam na provisão G02 do orçamento geral e precisam caber nela. Os preços atuais usados são os consultados nesta data; Olmo depende de pagamento no Pix.

## Dez caixas: resultado do plano nominal

[Croqui e lista de cortes](Conferencia_dez_caixas.html) · [CSV por régua de origem](Plano_de_cortes_nominal.csv) · [Dados do ensaio](Conferencia_dez_caixas.json).

Foram verificadas no FreeCAD as nove bases de piso da R44, seus comprimentos, larguras, posições globais e validade das formas. Os valores coincidem com a extração do arquivo salvo; não foi alterada a geometria.

- Sete bases recebem vinílico e somam **31,4485 m² brutos**. Banheiro e lavanderia ficam fora.
- Existe sobreposição de **0,49 m²** entre os retângulos da sala e cozinha. **Ela foi contada duas vezes no ensaio**, de propósito, sem usá-la como desconto.
- Acrescentadas quatro peças de **800 ×150 mm**, ou **0,48 m²**, como material de reserva para passagens/soleiras. Elas não representam quatro medidas executivas levantadas. A reserva cobre, entre outros encontros a medir, a faixa de espessura de parede no acesso ao escritório que não aparece como piso no retângulo principal.
- Área total representada pelo plano: **31,9285 m²**, sem descontar armários, banco ou outros móveis.
- Embalagem anunciada: **14 réguas por caixa**, dez caixas = **140 réguas**, cobertura comercial de **35,8 m²**.
- O ensaio utiliza **136 réguas e deixa quatro inteiras**, além das sobras de corte. Conta reserva de 2 mm por corte e descarta sobras de largura; não depende de colar tiras para formar uma régua.
- Menor peça no sentido longitudinal: **320 mm**; menor faixa de borda: **110 mm**. Juntas longitudinais desencontradas; réguas mantidas no sentido longitudinal de cada retângulo, sem girar sobras entre os eixos do desenho.

O [manual da Tarkett, seção 25](https://tarkett.com.br/arquivo/manual_geral_de_instalacao.pdf), orienta planejar e aprovar a paginação, evitar recortes estreitos na entrada, seguir as setas e usar desencontro de juntas; cita corte mínimo de 30 cm. O ensaio adotou peças acima desse comprimento. A conferência das entradas, encontros, setas, desenhos e recortes reais cabe ao plano executivo do instalador.

| Área do ensaio | Retângulo nominal | Fileiras | Larguras nas duas bordas |
|---|---:|---:|---:|
| Quarto principal | 2.450 ×2.950 mm | 12 | 185 mm |
| Complemento do quarto | 1.200 ×900 mm | 6 | 184 mm |
| Escritório | 2.300 ×2.950 mm | 12 | 110 mm |
| Sala/jantar | 2.450 ×3.800 mm | 12 | 185 mm |
| Faixa lateral da sala | 300 ×1.400 mm | 2 | 150 mm |
| Circulação | 1.300 ×900 mm | 7 | 130 mm |
| Cozinha | 3.520 ×1.550 mm | 17 | 200 mm |

As caixas são compartilhadas entre ambientes, aproveitando sobras compatíveis. Orçar cada cômodo isoladamente com arredondamento próprio desperdiça essa oportunidade. O plano não obriga compras de lotes diferentes.

**Limite da conclusão:** dez caixas são uma quantidade sustentada para orçamento pelo modelo nominal e pelo ensaio de cortes. A paginação é por retângulo e ainda não compatibiliza todas as juntas nas transições; a simulação visual anterior também não tinha sentido/recortes aprovados como executivo. A alteração não troca cor, produto ou direção geral, mas precisa de paginação final em obra. A soma das dimensões nominais das 140 réguas dá 35,8176 m²; o custo usa os 35,8 m² comerciais, sem aproveitar a diferença de arredondamento como folga.

Não reduzir o serviço de preparo/instalação de 34 m² para 31,93 m² nesta etapa. Também não liberar automaticamente a compra: conferir dimensões acabadas, passagens, espessura/capa do lote, sobra para manutenção e plano final do instalador. Se o plano real exceder 140 réguas, a caixa adicional custaria cerca de R$596,79 pelo preço pesquisado.

## Cozinha: qual duplicidade foi retirada

A decisão específica de 27/09 prevê **faixa baixa de Branco Itaúnas, referência de 10 cm, e Algodão Egípcio fosco acima**, continuando até a lavanderia. O registro de 12/10 mantém Suvinil Algodão Egípcio F100 fosco como referência; a lata antiga não é evidência de que toda a pintura esteja fornecida. O vinílico novo da cozinha está previsto separadamente.

O complemento de orçamento posterior pede genericamente “revestimentos novos” na cozinha/banheiro. Não especifica azulejo adicional, área, altura, modelo ou substituição da composição de pedra e pintura. O orçamento R43 transformou isso em **4 m² de revestimento cerâmico genérico de parede a R$120/m²**, sem uma parede de aplicação documentada. Na conciliação, prevalece a solução de acabamento específica: **retirada a provisão de R$480 do R10**, mantendo o acabamento novo aprovado. Isso não significa reaproveitar azulejo existente nem remover proteção prevista junto à bancada.

| Escopo | Onde permanece no orçamento |
|---|---|
| Vinílico novo da cozinha | R01; preparo/cola/instalação R02/R03 |
| Granito e faixa baixa | Grupo de pedras, sem redução nesta rodada |
| Pintura fosca e preparo usual | O05 e insumos de pintura conforme orçamento geral |
| Retirada dos acabamentos substituídos e descarte | O02/O03, sem desconto nesta rodada |
| Preparo extra da parede e cobrança mínima | **R$440 preservados em R11**, discriminados abaixo |
| Impermeabilização e testes das áreas pertinentes | O04, mantido |

Sem os 4 m² genéricos, a área nominal de assentamento cerâmico passa de 15,5922 para **11,5922 m²**, arredondada para **12 m²**. A R11 continua com **R$1.760**: R$1.320 para 12 m² ×R$110 e **R$440 mantidos como provisão de preparo adicional/cobrança mínima**, sem sobrepor o mesmo serviço ao O05. O total não depende de uma promessa de redução do preço do assentador.

A pintura deve conservar a cor e o fosco aprovados, com adequação às zonas de respingo/calor. Se o levantamento exigir preparo além do O05 e desta provisão, registrar a diferença antes da contratação. Esta conferência não presume que a antiga lata familiar resolve a tinta e não reaplica a exclusão de compra como economia nova.

## Resultado e próximos controles de compra

**Meta de aproximadamente R$17 mil alcançada na estimativa nominal**, mantendo os acabamentos. A folga de R$1,87 é praticamente nula: confirmar preço entregue, forma de pagamento, embalagem, lote, mão de obra e preparos antes de comprometer o teto. Não usar a reserva geral de R$10 mil para esconder diferenças de escopo.

O orçamento geral histórico segue preservado. A [planilha específica atualizada](../../../../outputs/orcamento-r43-2026-10-22/Pisos_R43_revisao.xlsx) separa quantidades de compra e área de serviço, mantém o valor anterior para comparação e explicita a provisão de R$440. A planilha de R$18.074,92 foi preservada como cópia anterior.

## Reconexão do FreeCAD

Na primeira tentativa não havia aplicativo nem serviço TCP respondendo. Foi iniciado o FreeCAD 1.1.4 fora do isolamento do terminal; o AI Copilot iniciou normalmente, sem alteração de configuração ou código da extensão. O teste de conexão e uma execução Python tiveram sucesso antes da abertura. A R44 foi aberta uma única vez; após a carga, novo teste confirmou **5.668 objetos e serviço ativo**. Foram lidas as bases de piso; nenhum arquivo CAD foi salvo. A janela do modelo foi reapresentada. Evidências em `outputs/orcamento-r43-2026-10-22/FreeCAD_reconexao.json` e `Pisos_R44_verificacao_live.json`.
