# Orçamento e cronograma

[Comparador de cotações: modelos, cobertura e custo equivalente](Orcamento/Cotacoes/README.md): sem propostas reais; decisão pendente.

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

## Acompanhamento da obra no site

A aba Obra lê exclusivamente a seção 2 do [cronograma](Cronograma_obra_e_compras.md), sem reordenar serviços. “Feito” é anotação local no celular, com exportação/importação; não muda a fonte. [Uso e testes](../ferramentas/site/README.md#obra--local).

**Dúvidas de sequência — a confirmar com RT; ordem atual mantida:**

1. **A confirmar com RT:** qual produto, tempo de cura e resultado do teste de estanqueidade devem anteceder o revestimento, se ambos começam na semana 2 da seção 2?
2. **A confirmar com RT:** quando e como proteger o vinílico Olmo instalado nas semanas 5–6 antes do box/E21/luminárias na semana 6 e da marcenaria/pedras nas semanas 7–8?
3. **A confirmar com RT:** conduítes e passagem de água quente pelo forro integram a infraestrutura das semanas 1–2? Quando inspecionar e fechar o forro antes da pintura, já que não há essa etapa na seção 2?
4. **A confirmar com RT:** qual sequência prevalecerá entre o plano NBR 16280 §5 (pedras antes da marcenaria) e o cronograma §§1/3 (inferiores montados → gabarito → pedras)?
5. **A confirmar com RT:** gabarito na semana 7 mais fornecimento de pedras de 1–2 semanas inclui instalação e cabe no agregado 7–8? Qual conclusão antecede os testes finais?
6. **A confirmar com RT:** quais predecessores encerram retoques/limpeza/testes, sem dependência na semana 8 do §2, mas na semana 9 do §1? Como separar pintura-base 4–5 do acabamento após marcenaria?

Fontes: [cronograma §§1–3](Cronograma_obra_e_compras.md) e [plano de reforma §§2–5](../01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md). Nenhum prazo novo presumido.

## Compras fora do orçamento

Valores fora do R44, sem uso da reserva. Em 29/10/2026, Philips 50PUG8100/78 e TAB4000 estão escolhidas ([fonte](../03_Ambientes/Sala_e_jantar/README.md#tv-e-painel)); TV já provisionada, soundbar ainda a incluir. Preservar totais e preços históricos.

| Item | Valor | Fonte |
|---|---:|---|
| Cadeira Ercathe A01 Mesh Premium, preta (escritório) | R$ 2.290,90 | [Sensetup](https://sensetup.com.br/products/cadeira-ergonomica-ercathe-a01-mesh-premium?variant=49668774854978), 29/10/2026; Elias, 29/10/2026: “deixa ela fora do orçamento, mas coloca o valor nos documentos” |
| Suporte de monitor ELG F80N, 2º (escritório) | R$ 169,99 | [Kabum](https://www.kabum.com.br/produto/107363/suporte-de-mesa-articulado-para-monitores-de-17-a-35-elg-ajuste-de-altura-com-pistao-a-gas-f80n), Pix, 29/10/2026; Elias, 29/10/2026: “2 deses sendo q já possuo 1” |
| Suporte de parede fixo ELG FIX200 para a Samsung 43″ (escritório) | R$ 63,99 | [Kabum](https://www.kabum.com.br/produto/329908/suporte-tv-fixo-elg-para-tvs-e-monitores-ate-43-polegadas-e-30kg-preto-fix200), 29/10/2026 (esgotado); Elias, 29/10/2026: “ok ELG FIX200”; não consta no R44 |
| Monitor ASUS TUF Gaming VG27AQ5A 27″ (escritório; o AOC 24″ já é dele) | R$ 2.000,00 | [Kabum](https://www.kabum.com.br/produto/747516/monitor-gamer-asus-tuf-27-qhd-210hz-0-3ms-fast-ips-g-sync-comp-freesync-premium-hdr10-som-integrado-vg27aq5a), Pix, 29/10/2026; Elias, 29/10/2026: “deixa os monitores fora do orçamento igual a cadeira do escritorio” |

O [plano de execução](Plano_execucao_ate_31_10.md) reúne o controle T01–T09, critérios e bloqueios de 25–26/10: matriz 20/20 e T01 documentais concluídas; T02/T03 dependem de oficina; T04/T05 delimitam banco/cesto, micro, P08/varal, gavetas e BC43. Ensaios e medidas reais pendentes. A [entrega](../06_Entregas/README.md) registra a verificação histórica T09 dos pacotes R20/R23; prevalece a versão no ESTADO_ATUAL. Reserva de integração 30–31/10 mantida.

T07: [memória CB02 e orçamento](Orcamento/Orcamento_R43.md), com provisão histórica de marcenaria 46.500 e alternativas sem tubos. Componentes, preços comparáveis e contratação pendentes; prevalece o fechamento D05/D06 abaixo.

T07 — agenda 27/10: [cenários A/B](Orcamento/Orcamento_R43.md#cenários-para-decisão-r44--agenda-2710) preservam ou adiam TV da sala, com valores/perdas e metas separadas de descontos. A memória de iluminação 4.415,94 é histórica; proposta vigente parcial 4.938,62. R44 permanece 137.748,11. Elias 27/10/2026, resposta “A”: manter TV nesta etapa; obter metas e reduzir mais 1.179,28, além das lacunas.

Coerência 26/10: M09/cortina do quarto é provisão indevida frente ao Registro 21/09; [delta de escopo](Orcamento/Orcamento_R43.md#divergência-de-escopo-m09--corrigir-na-próxima-consolidação) separado de negociação e sem reabrir a escolha. Não cotar M09; incorporar a retirada na próxima revisão financeira. A decisão A no README do orçamento usa os cenários corrigidos, sem contar essa retirada como desconto.

**Controle de 27/10:** [plano e bloqueios](Plano_execucao_ate_31_10.md#9-controle-diário); oficina/medidas não concluídas, sem envios.

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

[Simulação condicional de custo e prazo](Risco/README.md): hipóteses editáveis; orçamento e cronograma preservados.
