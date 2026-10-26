# Guedala Park — estado atual

**Pé-direito para novos testes: 2,60 m = 260 cm = 2600 mm, medida a confirmar.** Hipótese de estudo adotada por Elias, 26/10/2026, mensagem Sentinel_e1e1f7bf1de48191af94cb4b830efa99: "coloca no meu projeto o pe direito como medida a confirmar e deixa 2.60". Não é medição do Guedala nem média observada no Vila das Belezas 3. Não autoriza fabricação. Forros, sancas, vigas e alturas livres por ambiente precisam de conferência própria; não descontar um rebaixo presumido nem alterar móveis automaticamente. O escritório mantém cenário separado de 2,47 m com forro, também a confirmar. [Referências e limites](01_Programa_e_decisoes/Pesquisa_pe_direito.md). FreeCAD R52 preservado; a altura geral de referência do site passa a 260 cm.

Fonte única de verdade do projeto. Em caso de divergência com qualquer outro documento, vale esta página. Atualizada em 26/10/2026.

## O projeto

Interiores e marcenaria de um apartamento Cury Guedala Park III (Torre 2, final 06, 8º andar, 40,18 m², dois dormitórios). **O apartamento ainda não foi entregue**: todas as medidas vêm da planta oficial e precisam ser conferidas no local.

- **Objetivo:** mudar com tudo pronto, com dois meses de obra depois das chaves e mudança no terceiro mês.
- **Verba:** R$ 120 mil de execução + R$ 10 mil de reserva intocada.
- **Regra fixa de Elias:** nenhum tubo sustentando chapas de madeira, nem quadro metálico substituto. Qualquer proposta desse tipo exige autorização prévia. [Decisão e inventário](04_Moveis/Cargas_e_ligacoes/Decisao_sem_tubos.md).
- **Chapas e cores:** um acabamento por chapa física, igual nas duas faces. Duas peças distintas podem combinar externa 18 mm no padrão do projeto e interna 15 mm BrancoTX, com identificação e conferência de geometria/ligações/cargas. Não presumir caixa dupla nem inserir 15 mm automaticamente. No P03 atual há chapas únicas 18 mm, sem caixa interna 15 contínua. [Regra e auditoria por peça](ferramentas/site/fabrication/Decisao_acabamentos_R13.md).

## Versões vigentes

| O quê | Versão | Abrir |
|---|---|---|
| Modelo 3D | FreeCAD R52 | [Modelo](02_Modelo_3D/Guedala_Park_R52_Corrigido.FCStd) · [o que contém, como abrir e salvar com segurança](02_Modelo_3D/README.md) |
| Triagem geométrica | Zero peças com geometria própria inválida nas 1.449 conferidas por Elias (25/10/2026); 12 contêineres em `agregados_invalidos`, informativos (`3cdf795`); modelo preservado | [Triagem e critério](02_Modelo_3D/README.md#triagem-das-formas-inválidas--25102026) · [dados](02_Modelo_3D/Triagem_geometria.json) |
| Fichas dos 20 móveis | R14 | [Fichas](06_Entregas/Fichas_fabricacao/index.html) · [Pendências](06_Entregas/Fichas_fabricacao/Pendencias.html) · [Levantamento](06_Entregas/Fichas_fabricacao/Levantamento.html) |
| Cargas, ligações e cálculos por móvel | Estudos separados, não incorporados ao modelo | [Índice dos móveis](04_Moveis/README.md) · [matriz dos 20 móveis](04_Moveis/Cargas_e_ligacoes/Andamento_20_moveis.md) |
| Programa | R01 | [Programa de necessidades](01_Programa_e_decisoes/Programa_de_necessidades.md) |
| Planta mobiliada e vistas | R02 | [Planta mobiliada](03_Ambientes/Planta_mobiliada/README.md) |
| Especificações | R01 | [Caderno de especificações](01_Programa_e_decisoes/Caderno_de_especificacoes.md) |
| Pontos (elétrica, água, gás) | R00, preliminar | [Planta de pontos](03_Ambientes/Planta_pontos/README.md) |
| Conectores (P01, P04, P12, P17) | R00, proposta | [Mapa de conectores](04_Moveis/Mapa_conectores/README.md) |
| Orçamento | R44 | [Orçamento](05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md) |
| Cronograma de obra e compras | R00 | [Cronograma](05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md) · [plano de execução até 31/10](05_Orcamento_e_cronograma/Plano_execucao_ate_31_10.md) |
| Pranchas A3 | R00 | [Caderno de pranchas](06_Entregas/Caderno_pranchas/index.html) · [PDF](06_Entregas/Caderno_pranchas/Guedala_Park_Pranchas_R00.pdf) |
| Site e pacote para o montador | Site com R52; pacote R22 e estudos P17/P12 | [Site online](https://queiroz-labs.github.io/guedala-park/) · [gerador do site](ferramentas/site/README.md) |

O pacote R22 integra o pé-direito de teste e os estudos correntes; preserva a matriz 20/20 e os estudos separados de suspensão P17/P12, com desenhos, vetores e requisitos de qualificação. Biblioteca e fichas do site dão acesso aos estudos; geometria R52 preservada. Atualização/publicação autorizada por Elias em 26/10/2026: “commit push atualiza o site”.

## Onde estamos

| Etapa | % | Situação |
|---|---:|---|
| Programa e estudo preliminar | 100% | Fechados; falta só validar no local |
| Anteprojeto | 75% | Faltam códigos de chapa, tons exatos e luminárias |
| Executivo de marcenaria | 45–55% | Fichas prontas; faltam montagens do banco, cesto e gavetas, furação dos conectores e medidas reais |
| Complementares | 30% | T06: [lista de equipamentos](03_Ambientes/Equipamentos/Lista_equipamentos.csv), 48 linhas e 50 pontos cobertos; versões, fontes, folgas e lacunas identificadas. Micro-ondas: 10 cm desejados versus 30 cm do manual, sem decisão técnica. Circuitos, encaixes e retirada com RT/oficina |
| Especificações | 70% | Caderno gerado a partir dos dados do site |
| Orçamento | 60% | R44: estimativa de execução R$ 137.748,11, excesso R$ 17.748,11 sobre teto de R$ 120 mil; reserva R$ 10 mil intocada. Metas separadas; marcenaria **em espera** |
| Responsável técnico e aprovação | 10% | Rascunho do plano de reforma; RT ainda não contratado |
| Levantamento no imóvel | 25% | T08: [173 registros de medidas e impactos](07_Imovel/Medidas_e_impactos.csv), com fontes, arquivos e validação; 20 móveis cobertos. Levantamento real depende das chaves |

Detalhes no [roteiro para projeto oficial](01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md).

## Decisões tomadas

- **Cores:** Branco TX em peças internas separadas; Arenza na cozinha, lavanderia, escritório e quarto; Azul Petróleo nos aéreos da cozinha; off-white e bege foscos; Granito Branco Itaúnas; piso vinílico Olmo.
- **Sala:** sofá Bonnie; mesa Berlin pronta com três cadeiras; banco baú com duas tampas presas por dobradiça piano e articuladores com trava (protótipo pendente).
- **Quarto:** roupeiro de 65 cm com portas de correr; cama queen futura. Luz geral com três níveis de brilho pelo interruptor; conjunto Jurerê/SceneSwitch candidato, cerca de R$ 110 ([CB02](03_Ambientes/Iluminacao/Fechamento_custo_beneficio/Revisao_quarto_CB02.md)).
- **Abertura do canto P02:** duas portas independentes e quina fixa, [mockup em quatro situações](04_Moveis/Proximas_decisoes/P01_P03/Abertura_armario_L.png). Cores apenas didáticas; curso 86° ilustrativo, ferragens/limitador e folgas continuam condicionados. R52 preservada.
- **Maleiro P03:** Elias prefere **A, duas folhas 672 ×306**, e confirmou **Arenza liso**. [Base de chapa e avaliação](04_Moveis/P03/README.md): MDFBP Greenplac convencional 18 para uso seco, ArenzaColore/Lizze nas duas faces de cada peça P03. Cada chapa tem um único padrão. Conjunto com duas peças 18+15 pode ter cores distintas; no P03 não há caixa interna 15 contínua. SKU/substrato ainda a confirmar. Referência de porta 2,554 kg por área da chapa publicada 63,2 kg/2750×1850; mantida hipótese acabada 4 kg. Grupo candidato 6 dobradiças 71B3550 +6 calços 173H7100 +6 limitadores 70T3553, extremos 202 e 24 parafusos; capacidade 672/proporção baixa, fixação/pilotos, corpos e caixa 20 kg pendentes. Em 86°, corredor nominal 602/1203 com uma/duas abertas, altura 272; 16 trajetórias sem frentes/madeiras selecionadas e 72 cortes apenas de equilíbrio. Aplicação autorizada **se atender**, ainda não executada. Consultas locais prontas, não enviadas; R52 preservada. Malas reais e terceira condicionadas; B650 secundária.
- **Tecidos:** cortina da sala C2 Areia; suede areia no banco e na cabeceira; aéreo do escritório marfim claro. Códigos comerciais dependem de amostra. [Luminárias nos ambientes](09_Referencias/Iluminacao_CB02/Galeria.md).
- **Cozinha:** forno Fischer 127 V, cooktop KE4GC a gás natural, gaveta de limpeza sobre rodízios Leão Aço.
- **Banheiro:** gabinete com portas de correr e frente removível; uma parede verde no box. Luz de teto/indireta 3000 K e espelho 4000 K, três comandos. [Componentes L02: R$ 612,64 à vista](03_Ambientes/Banheiro/Fechamento_pre_entrega/Luminarias_selecao_L02.html). Chapas: Arauco Beige Matt e Louro Freijó Poro.
- **Ferragens:** dobradiças Blum, corrediças FGVTN 500 e MOVENTO 400 no escritório; 52 conjuntos Minifix (P10, P11, P15, P19).

Histórico completo das decisões: [Registro de decisões](01_Programa_e_decisoes/Registro_de_decisoes.md) e [Painel de decisões](01_Programa_e_decisoes/Painel_de_decisoes.md).

## Pendências por móvel

Nada abaixo está liberado para fabricação ou carga de uso. Os cálculos são nominais, e cada item tem hipóteses e perguntas exatas no seu README.

| Móvel | Já feito | Falta |
|---|---|---|
| P01/P03/P02 | [Ligação e caminho ao piso](04_Moveis/P03/README.md): 1728 casos condicionais acoplados. C01: seis posições passantes candidatas, tração 201 N/cisalhamento 33 N por ponto na hipótese central P03 com malas 20 kg/P02 sem conteúdo. Divisória→base 18→soco 62 alinhado, contato 9900 mm²; pé até 646 N/base 0,05 mm. R52 preservada | Produto completo/ensaio MDF e rigidez/resistência C01/juntas; nivelamento/piso e posicionamento do soco, aparência frontal 62; deformação superior ainda≈8,1–8,5 mm no estudo 18. Definir carga P02 e validar ferragens/manuseio antes de 18/25 ou CAD. 20 kg não demonstrados. Fundo P01 inteiro 1964×2114 exige fornecimento/emenda compatível |
| P04/P15 | [Suspensão](04_Moveis/P04/Suspensao_P04_P15/README.md): 660 casos. [Auditoria P04](04_Moveis/Ligacoes_sem_tubos/P04_auditoria_referencias.json): 869,5/300 = 2,898 mm, flecha 1,523 mm | Produto de suspensão, juntas e parede real |
| P15 | [Composição entre camadas](04_Moveis/P15/Composicao_parcial/README.md); [lote A](04_Moveis/Aereos_suspensao/README.md): 8 Minifix preservados, 6 Confirmat candidatos atuais/18 na variante; pino 27 da nova borda inferior | Produto/processo/ensaio da composição e juntas; TitebondMelamine excluída. Mapa não une camadas. Suspensão sem produto demonstrado |
| P04/P12/P17 — lote B | [Estudo vigente](04_Moveis/Aereos_suspensao/README.md#lote-b--p17p04p12): Elias, 25/10/2026: “20 kg / 10 kg / 10 kg” em P17/P04/P12, fundos inteiros/base limpa. 585 casos/60 Minifix; até 92,33/46,21/41,51 kg sem ferragens. P04: 4 acessos SW4 nominais; 765 equilíbrios/1530 vetores; pacote para laboratório, T0 com 5 retalhos/8 Minifix e 15 registros vazios; R52 intacta | Executar T0 e caracterizar juntas/suspensão. Bigfer P04 candidata no divisor 18/fundo e lateral direita; contatos/parede e ensaio físico pendentes. Nenhuma medição preenchida |
| P09/P11/P12/P17 | [Lote A P09/P11/P15](04_Moveis/Aereos_suspensao/README.md): Bigfer candidata≈60 mL/par; assento 40,5/furo 9,5 e montagem por dentro propostos. Apoio inferior: faixas 18×60 existentes, 4176 reações com equilíbrio 3D; compressão até 294,82 N nos cenários 10/20 kg. Fundo–laterais: 8 casos de corpo de prova/4 configurações, 6 Confirmat candidatos. [P17](04_Moveis/P17/Base_fundo_ligacoes/README.md) | Área/centro de contato reais e juntas/fundo não comprovados; uma coluna pontual não reage Mz sozinha. Reações do corpo de prova são de norma mínima, não forças de projeto. Bigfer/fixadores/retencão/parede pendentes. P09: abas reais/42−30=12 condicional, sem atribuir 6 kg ao aéreo |
| P17 | [Suspensão candidata](04_Moveis/P17/Base_fundo_ligacoes/README.md#suspensão-candidata--26102026): u40,5/1923,5, Z514, braço 424; 765 equilíbrios/1530 vetores; 8 calços/24 acessos conferidos | Qualificar Bigfer/juntas/ferramenta Ø12 auxiliar; contatos inferiores, referência superior e massas reais; capacidade e ancoragens pendentes |
| P12 | [Suspensão candidata](04_Moveis/P12/README.md): u40,5/724,5, Z548, braço 458; 225 equilíbrios/450 vetores; 4 calços/12 acessos conferidos; fundo 548 preservado | Qualificar Bigfer/fixadores/ferramenta; provar base/divisor/juntas/caixa e medir contato inferior. Sem capacidade ou ancoragens demonstradas |
| P16 e bancada | [Gavetas e estabilidade](04_Moveis/P16/Gavetas_estabilidade/README.md): 1296 cenários. [Interface guia–fundo](04_Moveis/P16/Interface_guia_fundo/README.md). [Bancada](04_Moveis/Bancada/README.md): tampo 2000×700×30, curso 400 | Massa e rigidez do tampo 30, juntas, montagem real 400. Não cortar madeira para zerar o STEP |
| P14/P20 banco e cesto | [Assento fechado](04_Moveis/P20/Assento_fechado/README.md), [reações do cesto](04_Moveis/P14/Reacoes_e_operacao/README.md): 270 cenários | Comprar 1 piano e 2 pares de articuladores (~R$ 150, [preços](04_Moveis/Banco_e_cesto/Cesto_simples/Precos_e_conjunto_R01.md)) para protótipo; pivôs, limitadores a 55°, retenção |
| Todos | [Corte por chapa física](04_Moveis/Proximas_decisoes/Corte_e_formatos/README.md): 249 IDs/dimensões preservados; 215 no ensaio/34 excluídos, 16 chapas virtuais; zero pares de acabamentos opostos na auditoria 248 | P13/Peca350 sem entrada na auditoria, acabamento pendente; 11 outros padrões parciais, referências, espessuras/espelho e dados de substrato/veio/processo. Nenhum corte/compra aprovado |

**P20 aberto, 26/10:** [montagem e reações](04_Moveis/P20/Assento_fechado/README.md): seis equilíbrios, 42 poses e dez sensibilidades. Articuladores em compressão nominal 7,628/6,473 N a 90°; piano com grupos equivalentes, sem forças por parafuso. Eixo real, apoio fixo, terminais 22/30 mm e liberação da trava ainda pendentes; nenhum ensaio ou alteração R52.

**P14 montagem, 26/10:** [interfaces e roteiro](04_Moveis/P14/Reacoes_e_operacao/README.md): quatro casos simultâneos preservados, cinco sensibilidades de trava e oito registros vazios. Pivô 40,25 mm na faixa 52 mm ainda depende de bucha, retenção e acesso SW5. Consulta banco/cesto atualizada e não enviada; oficina indisponível, zero ensaios. R52 preservada.

**Ferragens P14/P20, pesquisa de 26/10:** [fontes e oito requisitos](04_Moveis/Banco_e_cesto/Cesto_simples/Conferencia/Resultado.md). Bucha GFM-1012-15 entrou como candidata de consulta; ajuste, alojamento e ligação ainda indefinidos. Bigfer/Mahler seguem sem curso de liberação/capacidade na aplicação confirmados. Consultas não enviadas; sem compra, ensaio ou mudança R52.

**P08, 26/10:** [rodízios e estabilidade](04_Moveis/P08/README.md): 336 cenários e 1292 distribuições conferidas; 26 cenários sem equilíbrio ao excluir uma roda de canto. Kit de seis rodas e apoio de 39 mm preservados. Massas acabadas, contato, flexão, juntas, fixação, guias e batente pendentes; sensibilidades não definem carga de uso. Zero ensaios e R52 intacta.

## Próximos passos

**Avanço 26/10 — juntas dos aéreos:** P17: 21 grupos/70 posições candidatas; P12: 9/21; 30 cortes de carga por móvel e 2.625 pares de envelopes conferidos. Sequência de montagem e acesso externo em bancada documentados nos READMEs. P17: 24 apoios do estudo antigo coincidem após v=330−y; rigidez do Minifix e referência superior não demonstradas. P12 segue sem ligação direta base/tampo–fundo. T0/P04 reconferido e pronto, sem execução; Elias, 26/10: “Ainda não; deixar o roteiro pronto”, sobre oficina/material. Próximo: caracterizar juntas e caixa/ferragem reais; seguir frente independente enquanto aguarda oficina.

**Controle de 25/10 consolidado em 26/10:** [matriz 20/20](04_Moveis/Cargas_e_ligacoes/Andamento_20_moveis.md) revisada; T01 documental concluída. T02/T03 continuam parciais: juntas/suspensão, composição P15 e caixa superior P01/P03. P04 tem pacote de laboratório, sem ensaios; P17/P12 têm implantação nominal; qualificação física e rigidez continuam pendentes. Decisões de uso/acabamento e verificações do imóvel seguem identificadas. Dia 26 em andamento; integração 30 e conferência 31 preservadas.

1. **Antes das chaves:** seguir o [plano até 31/10](05_Orcamento_e_cronograma/Plano_execucao_ate_31_10.md); concluir as luminárias na [lista curta](03_Ambientes/Iluminacao/Lista_curta_luminarias_e_madeira.md); pedir orçamentos de marcenaria quando o pacote sair da espera; contratar o responsável técnico e enviar os [e-mails preparados](01_Programa_e_decisoes/Rascunhos_emails.md).
2. **No dia das chaves:** [roteiro do dia das chaves](07_Imovel/Roteiro_dia_das_chaves_R01.md), com vistoria da Cury e medição.
3. **Depois das chaves:** ajustar modelo, fichas e orçamento às medidas reais; protocolar o [plano de reforma](01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md); contratar e executar.

**Quem resolve cada dependência** (sugestão, não contratação): projeto (caixas P01/P02/P03, juntas, retenção); produto/oficina (painéis reais, processo P15, ferragens, componentes P14/P20); Elias (aparência das propostas visíveis: soco frontal 62 de P01, faixa inferior 18 de P15, painéis da bancada); RT após as chaves (medidas, parede, ancoragens, piso, liberação).

## Como trabalhar nesta pasta

- Estudos dos aéreos: hashes de texto normalizam CRLF/LF e caminhos relativos usam `/`, permitindo conferência em clone limpo. PDF/FCStd continuam byte a byte; cálculos e geometrias preservados.

- Regras de organização e leitura econômica: [AGENTS.md](AGENTS.md). Mapa das pastas: [README.md](README.md).
- Fluxo Git reforçado por Elias (25/10/2026): commits pequenos e por assunto, inclusão por caminho, README da área e estado atual no mesmo commit; verificação e hook antes de commitar, clone limpo com `--ci` antes de push e acompanhamento de cada processo Git até terminar. Limites: README ≤16 KB; demais `.md` ≤60 KB. Regras completas no [AGENTS.md](AGENTS.md#7-git-e-sessões-simultâneas).
- Leia esta página, depois só o README da área. Dados pontuais: JSON ao lado de cada README. **Não leia inteiro** o Registro de decisões (475 KB): busque por palavra.
- Portas e movimentos: [cinemática fora do CAD](04_Moveis/Proximas_decisoes/Cinematica/README.md) (`ferramentas/cinematica/consultar.py`); não anime o apartamento inteiro para cada conta.
- Não rode macros antigas que salvam ou fecham documentos. Não sobrescreva o modelo vigente para consultar.
- **Verificadores** ([ferramentas/README.md](ferramentas/README.md)): `python ferramentas/verificar_tudo.py` (o hook de commit roda sozinho) e, depois de qualquer trabalho no FreeCAD, `python ferramentas/verificar_modelo/verificar_modelo.py --completo`, que acusa objetos removidos, formas inválidas, expressões perdidas e colisões novas.
- Versões antigas (R45 a R51, compatibilizações, arquivo morto) estão no git, na tag `antes-reorganizacao`.
- Revisão documental de 25/10/2026: downloads ignorados pelo Git identificados como cópias locais, sem links de download; atribuições históricas revisadas com datas/fontes na própria linha; fechamento antigo da cozinha consolidado no [README vigente](03_Ambientes/Cozinha/README.md#instalações-e-documentos-da-unidade), com Fischer 127 V e cooktop a gás natural.
- Links HTML após a reorganização: 40 referências tratadas em 9 páginas (22 do dossiê para `Fichas_fabricacao/`, 2 destinos realocados e 16 referências removidas com texto/caminho histórico preservados). Geradores correspondentes corrigidos. Os textos de estudos antigos desvinculados nos `.md` continuam rastreáveis pelo histórico do Git; não foram religados a documentos de conteúdo diferente.

- Documentação, 26/10/2026: README dos aéreos compactado, com limites técnicos preservados, para permitir a reposição de espaços dentro de 16 KB.

- Espaços, 26/10/2026: textos do estado, plano e READMEs revisados; verificador em `ferramentas/verificar_espacos.py`, com bloqueio somente nos 13 arquivos já limpos também no Git. P03 e trechos novos de outras sessões permanecem corrigidos no disco, sem commit, conforme orientação de Elias neste chat em 26/10/2026. Retomar após o commit de origem, conferir os 15 arquivos e ampliar a lista de bloqueio.

- Plano até 31/10, 26/10/2026: T01–T09 resumidas por situação, bloqueio e fonte no [plano](05_Orcamento_e_cronograma/Plano_execucao_ate_31_10.md). Só matriz 20/20 concluída na medição; demais resultados condicionados. Retomar T02/T03 pelas juntas e suspensão dos aéreos; sem oficina, avançar montagem nominal T04. Agenda e controle diário preservados.


**Integração de 26/10/2026 — análise BOP:** [análise dos alertas](02_Modelo_3D/README.md#análise-dos-alertas-bop--25102026) incorporada, com limites da amostragem e preservação da R52. Sem reparo geométrico ou atualização da base.


**Integração de 26/10/2026 — P01/P02/P03:** estudos de caixa, portas, malas, juntas e caminho ao piso incorporados; [P03](04_Moveis/P03/README.md). Resultados condicionais, sem capacidade física demonstrada ou alteração da R52.
