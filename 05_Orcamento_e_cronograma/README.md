# Orçamento e cronograma

## Risco do cronograma — escopo registrado em 29/10/2026

**Resultado:** rede documental ampliada de 21 para **29 nós, sem ciclos**, com cotação, contratação e abastecimento. **P50/P80, probabilidades dos marcos e caminho crítico global continuam indeterminados**: faltam durações, modas e ligações da conclusão da obra. Foram executados **zero cenários do projeto**, sem preencher lacunas com zero, uniforme ou moda central. Os 5.000 cenários dos testes são sintéticos.

Fontes: [cronograma R00](Cronograma_obra_e_compras.md), [pedido de cotação R02](Orcamento/Marcenaria_35mil/Pacote_cotacao_marcenaria_R01.md) e [programa atualizado](../01_Programa_e_decisoes/Programa_de_necessidades.md). Hashes nas saídas. R00 traz **faixas típicas, não respostas de fornecedores**; fontes, orçamento e CAD preservados.

### Dependências e escopo corrente

- Envio → retornos → comparação → contratação → pedido/abastecimento de ferragens. Confirmar fornecimento no pacote e necessidade no início, sem duplicar compra.
- Chaves → medição → executivo, também dependente de oficina definida e resolução documental dos mecanismos. Executivo + abastecimento → marco de início → fabricação → inferiores → gabarito → pedras. Marco lógico zero não substitui duração ausente de serviço.
- RT → protocolo → análise → instalações → cura/revestimentos → pintura-base → vinílico; revestimentos → medição do box → fornecimento. O agregado da semana 7–8 não é somado aos componentes. Retoques/testes e mudança ainda não têm predecessores completos: não foram conectados por suposição.
- **D05-C/D06-B:** cotar integral e etapa sem P16/P17/C01/C03/C04/C05; E06 adiada, E05 mantida. Isso não demonstra redução proporcional de prazo. O fornecedor precisa separar mobilizações e abastecimento.
- **29/10:** Philips 50PUG8100/78 e TAB4000 identificadas, sem prazo por SKU; cama viúva atual na mudança, queen futura; AOC e TV do escritório existentes, ASUS a comprar; um F80N comprado, outro a comprar. Cadeira/monitores fora da verba não significam já comprados. Volante/pedais retirados não geram compra. Não se aplicou uma faixa genérica de eletros a todos esses modelos.

O pedido permanece **preparado, não enviado**. **30/10/2026 às 18 h, Brasília**, é prazo solicitado de resposta, não confirmação do fornecedor. Sem data de envio, duração de resposta e data das chaves, não se converte esse prazo absoluto em semana relativa nem em probabilidade.

### Marcos calculados pelo motor

| Marco | Alvo documental | Probabilidade | Dado que falta |
|---|---|---|---|
| Respostas à cotação | 30/10/2026, 18 h Brasília | Indeterminada | Envio, prazo aceito e calendário das chaves |
| Oficina escolhida | Antes da semana 0 | Indeterminada | Respostas, comparação e contratação |
| Início da fabricação | Semana 2 no diagrama | Indeterminada | Medição, executivo, mecanismos, fornecimento e origens pré-chaves |
| Box recebido | Semana 6 | Indeterminada | Etapas anteriores, medição e moda do fornecimento |
| Pedras recebidas | Semana 8 | Indeterminada | Inferiores/gabarito e prazo confirmado; não inclui instalação |
| Obra concluída | Semana 8 | Indeterminada | Rede final, serviços e durações |
| Mudança | Até semana 12 | Indeterminada | Rede até ocupação e durações; meta continua terceiro mês |

Lacunas geram vazio/`null`, nunca 0% ou 100%; cada marco usa somente seus antecessores.

### Caminho conhecido e o que pode encurtá-lo

Marcenaria é caminho crítico **declarado pela R00**, não demonstrado globalmente. No cenário do diagrama, início em +2 com fabricação de 5–6 semanas termina em +7/+8; somando apenas 1–2 semanas de pedras chega a **+8/+10**. Faltam montagem, gabarito, instalação, limpeza e outras esperas: **8–10 não é intervalo da mudança nem limite superior da obra**.

A sensibilidade restrita aos dois elos conhecidos dá **empate**: passar fabricação de 6 para 5 semanas ou pedras de 2 para 1 reduz essa cadeia em uma semana. Não comprova ganho igual na mudança, pois outra ramificação pode comandar o término. **Não existe item globalmente mais eficaz demonstrado.** A maior espera evitável quantificada na R00 é a fila da oficina, risco de 2–4 semanas, sem probabilidade e sem ganho garantido. Primeira ação útil: revisar/enviar cotação e obter prazo/vaga/escopo da oficina antes das chaves, sem contratar neste estudo.

### Limites condicionais de pedido

Conta `semana necessária − prazo máximo`, dias/7 (úteis/corridos a confirmar). São limites condicionais; existentes/itens do pacote não geram novas compras.

| Item | Último pedido relativo às chaves | Condição/conflito |
|---|---:|---|
| RT | Dado ausente | Contratação antes de 0, duração não informada |
| Ferragens | −1 | Receber em +2, prazo típico máximo 3; conferir fornecimento da oficina |
| Porcelanatos | −2 | Receber em +2; R00 recomenda −4 |
| Vinílico | +2 | Receber em +5; R00 recomenda −3 |
| Louças/metais | +5 | Início do agregado +7, sem duração de instalação |
| E21 para gás | −1 | R00 pede em +2 mas exige presença em +1/+2 |
| Eletros | +5,57 | Receber em +7; forno pode ser necessário antes, marco ausente |
| Luminárias | +3 | Receber em +6; sem folga no prazo máximo |
| Estofados | +3 | Receber em +7; escopo da etapa/pacote a confirmar |
| Sofás/Berlin/cadeiras | +2 | Pedir em +3/+4 com seis semanas entrega em +9/+10 |
| Box | +3 | Exigiria medição +3; R00 prevê +4/+5, entrega +5 a +8 |
| Pedras | +6 | Exigiria gabarito +6; R00 prevê +7, entrega +8/+9, sem instalação |

Box/pedras exigem medição/gabarito após chaves; pedido antecipado não os elimina.

### Perguntas objetivas e reprodução

- **Oficina/fornecedores:** qual prazo mínimo, mais provável e máximo por etapa e SKU, em dias úteis ou corridos? A fila está dentro dos 5–6? Quando cada ferragem e o forno devem estar disponíveis? Qual a duração real da etapa reduzida?
- **Coordenação/RT:** quais durações e predecessores faltam da medição até a mudança, e qual prazo de análise do condomínio? Sem esses dados não há caminho crítico global.
- **Pedras:** valem 7–10 dias ou 1–2 semanas, e incluem instalação? Não somar as duas referências.
- **Registro administrativo:** quando o pedido foi enviado e qual retorno foi aceito pelo fornecedor? Não há nova escolha estética para Elias nesta atualização.

Reproduzir: `python -B ferramentas/estudos/cronograma_risco.py --saida ../outputs/Cronograma_risco`. Testar: `python -B ferramentas/estudos/test_cronograma_risco.py` — **14 testes passaram**. JSON: rede/lacunas/fontes; CSV: contas, marcos e escopo. Dados externos, sem informações pessoais.

| Saída externa | SHA256 |
|---|---|
| `Cronograma_risco.json` | `3c802b14e2498f0d783fc3da3f2069ec6cda07b790b00442f148e56fb509bdfc` |
| `Limites_compras.csv` | `c44ef0364846c360a9e8e2d7ebc0473c8cfd3a4ef2e0f6f26ac9918b451acaf7` |
| `Marcos_cronograma.csv` | `2ec4f10bfca16e027a0372c2510f46981662110a19c022e0a3b654b00b985484` |
| `Escopo_cronograma.csv` | `5fb99ece96daaceb911e93ff697db3a337170aa20462f90349bcd53b8dedf7b9` |

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

Valores fora do R44, sem uso da reserva. Em 29/10/2026, Philips 50PUG8100/78 e TAB4000 estão escolhidas ([fonte](../03_Ambientes/Sala_e_jantar/README.md#tv-e-painel)); TV já provisionada, soundbar ainda a incluir. Preservar totais e preços históricos.

| Item | Valor | Fonte |
|---|---:|---|
| Cadeira Ercathe A01 Mesh Premium, preta (escritório) | R$ 2.290,90 | [Sensetup](https://sensetup.com.br/products/cadeira-ergonomica-ercathe-a01-mesh-premium?variant=49668774854978), 29/10/2026; Elias, 29/10/2026: “deixa ela fora do orçamento, mas coloca o valor nos documentos” |
| Suporte de monitor ELG F80N, 2º (escritório) | R$ 169,99 | [Kabum](https://www.kabum.com.br/produto/107363/suporte-de-mesa-articulado-para-monitores-de-17-a-35-elg-ajuste-de-altura-com-pistao-a-gas-f80n), Pix, 29/10/2026; Elias, 29/10/2026: “2 deses sendo q já possuo 1” |
| Suporte de parede fixo ELG FIX200 para a Samsung 43″ (escritório) | R$ 63,99 | [Kabum](https://www.kabum.com.br/produto/329908/suporte-tv-fixo-elg-para-tvs-e-monitores-ate-43-polegadas-e-30kg-preto-fix200), 29/10/2026 (esgotado); Elias, 29/10/2026: “ok ELG FIX200”; não consta no R44 |
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
