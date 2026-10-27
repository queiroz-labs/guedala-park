# Móveis — cálculos, ligações e estudos

Estudos separados do modelo R52: nenhum foi incorporado à geometria, e nenhum libera fabricação ou carga de uso. A situação de cada móvel está resumida no [Estado atual](../ESTADO_ATUAL.md#pendências-por-móvel).

| Para quê | Onde |
|---|---|
| Andamento dos 20 móveis, com ação, responsável e evidência | [Andamento](Cargas_e_ligacoes/Andamento_20_moveis.md) · [CSV](Cargas_e_ligacoes/Andamento_20_moveis.csv) |
| Pendências e avanços depois da R52 (P01/P03, corte e formatos, cinemática) | [Próximas decisões](Proximas_decisoes/README.md) |
| Decisão "sem tubos" e cargas prioritárias | [Cargas e ligações](Cargas_e_ligacoes/README.md) · [Ligações sem tubos](Ligacoes_sem_tubos/README.md) |
| Matriz dos 20 módulos, Minifix, interfaces e ferragens fixas | [Inventário dimensional](Inventario_dimensional/README.md) |
| Conectores propostos | [Mapa de conectores](Mapa_conectores/README.md) |
| Quantitativos por proposta | [Quantitativos](Quantitativos/README.md) |

Os HTMLs de estudo tiveram os caminhos locais conferidos após a reorganização de 25/10/2026. Referências sem equivalente local mantêm o texto e o caminho antigo, com aviso de arquivo removido; para recuperar a evidência original, consulte o histórico do Git e a tag `antes-reorganizacao`.

## Por móvel

| Móvel | Estudos |
|---|---|
| P01 (e P03) | [Apoios ao piso](P01/Apoios_ao_piso/README.md) · [Massas e equilíbrio](P01/Massas_equilibrio/README.md) · [Caminho superior P03](P01/Caminho_superior_P03/README.md) |
| P03 maleiro — duas malas de bordo | [Volume, passagem e dobradiças](P03/README.md): Elias prefereA672 ×306; corredor nominal602/1203 em86° com uma/duas abertas. Grupo3/extremos202 em estudo; produto, fixações/caixa e terceira mala condicionados |
| P04 / P15 | [Suspensão P04/P15](P04/Suspensao_P04_P15/README.md) · [Composição parcial P15](P15/Composicao_parcial/README.md) |
| P09 / P11 / P12 / P17 | [Suspensão dos aéreos](Aereos_suspensao/README.md) · [P11 sem tubos](P11/Ligacoes_sem_tubos/Resultado_R00.md) · [P17 base e fundo](P17/Base_fundo_ligacoes/README.md) |
| P12 acima da geladeira | [Caixa e suspensão candidata](P12/README.md):fundo548 preservado; acesso e 225 equilíbrios nominais; produto/juntas/ensaios pendentes |
| P14 / P20 (cesto e banco) | [Reações e operação do cesto](P14/Reacoes_e_operacao/README.md) · [Assento fechado](P20/Assento_fechado/README.md) · [kit de oficina vigente](P20/Assento_fechado/Roteiro_banco_cesto.md) · [Southco histórico](Banco_e_cesto/Fixacao_Southco) |
| P16 e bancada | [Gavetas e estabilidade](P16/Gavetas_estabilidade/README.md) · [Interface guia–fundo](P16/Interface_guia_fundo/README.md) · [Bancada](Bancada/README.md) |
| Banheiro, gavetas, mesa e portas (estudos de 21/10) | [Avanço de pendências](Avanco_pendencias/Avanco_pendencias.html) |

## Acabamentos por peça física

**Tampos junto ao teto:** Elias, 26/10/2026, nesta conversa: “Todos os armários previstos até o teto, em todos os ambientes” e “ok, mantem 18mm para esses casos, mas deixa branco”. Manter 18 mm onde as ligações exigem essa premissa, com Branco TX nas duas faces e sem chapa decorativa sobreposta. [Diretriz, cotas atuais e compatibilização pendente](#diretriz-de-fechamento-até-o-teto--26102026). Ainda não aplicado à R52/fichas.

Cada chapa física tem um padrão igual nas duas faces. Duas peças separadas podem usar cores diferentes: externa18mm no padrão do projeto e interna15mm BrancoTX, desde que existam e sejam identificadas. Não presumir que todo móvel já tenha caixa dupla; conferir os33mm e seus efeitos antes de acrescentá-la. P03 atual tem chapas únicas18, sem caixa interna15 contínua.

[Regra vigente](../ferramentas/site/fabrication/Decisao_acabamentos_R13.md) · [auditoria de248 IDs](Acabamentos_por_peca.csv) · [resumo por móvel](Acabamentos_por_peca.json). Foram identificadas88 atribuições anteriores de cores opostas em umID, em 19 móveis; espelhos aplicados são componentes separados. O inventário distingue intenção anterior e padrão atual, sem alterar geometria ou liberar fabricação.

## Diretriz de fechamento até o teto — 26/10/2026

**Pedido de Elias nesta conversa, 26/10/2026:** “Todos os armários previstos até o teto, em todos os ambientes”. Para o fechamento superior, após a discussão das ligações em chapa 18, corrigiu a proposta inicial de 15 mm: “ok, mantem 18mm para esses casos, mas deixa branco”.

- Nos tampos com ligações previstas para 18 mm, manter essa espessura e adotar **Branco TX nas duas faces da mesma chapa**. Não acrescentar chapa externa decorativa sobre esse topo. A proposta inicial de 15 mm não autoriza reduzir esses tampos.
- O encontro visual da marcenaria com o teto acabado deve ficar fechado. O detalhe de montagem precisa absorver desníveis e a folga técnica, sem usar laje/forro como apoio da caixa ou impedir as portas de abrir. Arremate vertical, quando necessário, não é uma segunda chapa horizontal sobre o tampo.
- Referências atuais: 2600 mm em todos os cômodos, inclusive escritório, e 2500 mm no banheiro (Elias, 27/10/2026). São hipóteses, a confirmar no levantamento. A decisão não determina a altura real do teto nem elimina a folga de montagem.

**Conferência dos parâmetros gravados da R52:** os valores abaixo são do modelo existente, não cotas novas de fabricação. As diferenças mostram o ajuste a compatibilizar; não constituem decisão de aumentar portas, subir caixas inteiras ou preencher todo o vão com arremate.

| Conjunto | Topo atual, mm do piso | Referência de teto acabado, mm | Diferença, mm |
|---|---:|---:|---:|
| Quarto, P02/P03/P04 | 2440 | 2600 | 160 |
| Cozinha, P09/P10/P11/P12 | 2550 | 2600 | 50 |
| Lavanderia, P15 — conferir enquadramento no fechamento até o teto | 2230 | 2600 | 370 |
| Escritório, P17 | 2450 | 2600 | 150 |

**Aplicação ainda pendente no CAD e nas fichas.** Compatibilizar o encontro ao teto por ambiente, as portas e os acessos de montagem antes de incorporar. Não estender esta diretriz ao espelheiro do banheiro ou a outro móvel que não tenha sido previsto até o teto. Os estudos de suspensão abaixo mantêm as geometrias e massas anteriores; não comprovam caixas aumentadas. A confirmação de 18 mm preserva a premissa de espessura das ligações, não demonstra sua capacidade. Seguir as pendências existentes de ferragens/oficina, sem refinar novamente os estudos nominais.


R53/fichas R15,27/10: P02 registra U1–U4=A; P13/Peca350 incluída na auditoria (249 peças), Arenza liso nas duas faces, por F13=A de Elias27/10. Produto18/bordas e corte permanecem pendentes; estudos resistentes não incorporados.
