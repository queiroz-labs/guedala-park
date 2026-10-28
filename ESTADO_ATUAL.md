# Guedala Park — estado atual

Fonte vigente de versões e pendências, atualizada em 27/10/2026. Limite de 14 KB; detalhes nos READMEs. Componentes e site sem pastas datadas; verificador trava a regra (27/10).

## O projeto

Interiores e marcenaria de um apartamento Cury Guedala Park III (Torre 2, final 06, 8º andar, 40,18 m², dois dormitórios). **O apartamento ainda não foi entregue**: todas as medidas vêm da planta oficial e precisam ser conferidas no local.

- **Objetivo:** mudar com tudo pronto, com dois meses de obra depois das chaves e mudança no terceiro mês.
- **Verba:** R$ 120 mil de execução + R$ 10 mil de reserva intocada.
- **Regra fixa de Elias:** nenhum tubo sustentando chapas de madeira, nem quadro metálico substituto. Qualquer proposta desse tipo exige autorização prévia. [Decisão e inventário](04_Moveis/Cargas_e_ligacoes/Decisao_sem_tubos.md).
- **Chapas e cores:** um acabamento por chapa física, igual nas duas faces; duas peças distintas podem ter cores diferentes (externa 18 mm no padrão, interna 15 mm BrancoTX), com conferência de geometria, ligações e cargas. Não presumir caixa dupla nem inserir 15 mm automaticamente. [Regra e auditoria por peça](ferramentas/site/fabrication/Decisao_acabamentos_R13.md).
- **Pé-direito:** 2,60 m = 260 cm = 2600 mm em todos os cômodos; banheiro: **2,50 m = 250 cm = 2500 mm**, medida a confirmar (Elias, 27/10/2026, nesta conversa). Escritório 2,47 m substituído. [Fonte e limites](01_Programa_e_decisoes/Pesquisa_pe_direito.md).

## Versões vigentes

| O quê | Versão | Abrir |
|---|---|---|
| Modelo 3D | FreeCAD R53 | [Modelo](02_Modelo_3D/Guedala_Park_R53_Decisoes.FCStd) · [o que contém, como abrir e salvar com segurança](02_Modelo_3D/README.md) |
| Triagem geométrica | Zero peças com geometria própria inválida nas 1.449 conferidas (25/10/2026); 12 contêineres informativos | [Triagem e critério](02_Modelo_3D/README.md#triagem-das-formas-inválidas--25102026) · [dados](02_Modelo_3D/Triagem_geometria.json) |
| Fichas dos 20 móveis | R15 | [Fichas](06_Entregas/Fichas_fabricacao/index.html) · [Pendências](06_Entregas/Fichas_fabricacao/Pendencias.html) · [Levantamento](06_Entregas/Fichas_fabricacao/Levantamento.html) |
| Cargas, ligações e cálculos por móvel | Estudos separados, não incorporados ao modelo | [Índice dos móveis](04_Moveis/README.md) · [matriz dos 20 móveis](04_Moveis/Cargas_e_ligacoes/Andamento_20_moveis.md) |
| Programa | R01 | [Programa de necessidades](01_Programa_e_decisoes/Programa_de_necessidades.md) |
| Planta mobiliada e vistas | R02 | [Planta mobiliada](03_Ambientes/Planta_mobiliada/README.md) |
| Especificações | R01 + catálogo comercial 27/10, amostras pendentes | [Caderno de especificações](01_Programa_e_decisoes/Caderno_de_especificacoes.md) |
| Pontos (elétrica, água, gás) | R01 de anteprojeto;50 auditados +3 funções | [Planta de pontos](03_Ambientes/Planta_pontos/README.md) |
| Conectores (P01, P04, P12, P17) | R00, proposta | [Mapa de conectores](04_Moveis/Mapa_conectores/README.md) |
| Orçamento | R44 | [Orçamento](05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md) |
| Cronograma de obra e compras | R00 | [Cronograma](05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md) · [plano de execução até 31/10](05_Orcamento_e_cronograma/Plano_execucao_ate_31_10.md) |
| Pranchas A3 | R02: 20 folhas; 1:50/1:25; alturas 2,60/2,50 m | [Caderno de pranchas](06_Entregas/Caderno_pranchas/index.html) · [PDF R02](06_Entregas/Caderno_pranchas/Guedala_Park_Pranchas_R02.pdf) |
| Site e pacote para o montador | R53/R25 publicado e conferido em 27/10; fichas R15; alturas 2,60/2,50 m; textos do site sem histórico de revisões (local, sem push) | [Site online](https://queiroz-labs.github.io/guedala-park/) · [gerador do site](ferramentas/site/README.md) · [evidência e limites](06_Entregas/README.md) |

Correção de planta R23 (lavanderia 1,29 × 1,54 m, circulação, fechamentos do banheiro) publicada com autorização de Elias, 26/10/2026: "Sim, autorizo comitt push". Pendência: envelopes das lixeiras da cozinha/lavanderia sobrepõem fechamentos em cerca de 6/5 cm; [encaixe proposto](03_Ambientes/Cozinha/Encaixe_lixeiras.md) +7/+6 cm, LIX=A (Elias 27/10/2026, resposta “A”), aplicado nominalmente na R53 e site; testar pedal/tampa, passagem, varal e destino temporário da Loop. Integridade do ZIP não comprova compatibilização das vistas nem ensaios.

## Onde estamos

| Etapa | % | Situação |
|---|---:|---|
| Programa e estudo preliminar | 100% | Fechados; falta só validar no local |
| Anteprojeto | 87% estimado | Antes 75%; +8 documental e +4 por D03/D04/D06/integração A3. [Critério e pendências](01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md). D01–D06 respondidas; pacote pronto para envio; cotações/amostras impedem 90–95% |
| Executivo de marcenaria | 45–55% | Fichas prontas; faltam montagens do banco, cesto e gavetas, furação dos conectores e medidas reais |
| Complementares | 35% | [Pontos R01](03_Ambientes/Planta_pontos/README.md):53 funções, 50 originais auditadas; D03/D04/D06 integradas; E06 adiada, Q06 sem coordenada, implantação e circuitos com RT/oficina |
| Especificações | 80% documental | Catálogo 15/18 mm e códigos disponíveis no Caderno; D02: amostras Lume/Areia solicitadas por Elias 27/10; SKUs e escolha final pendentes |
| Orçamento | 60% | R44: R$ 137.748,11; luz 4.534,55. [D05-C](05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md#d05--plano-de-escopo-sem-descontos-presumidos), Elias 27/10: "C — cotar com aumento de verba". Referência 127.101,22, aporte 7.101,22, reserva 10.000 intacta; pacote 37.000 condicionado, sem contratar |
| Pranchas formais | 80% estimados | [R02 e critérios](06_Entregas/Caderno_pranchas/README.md): fonte CSV, R53, 12 elevações, impacto; faltam levantamento, interfaces e revisão técnica |
| Responsável técnico e aprovação | 10% | Rascunho do plano de reforma; RT ainda não contratado |
| Levantamento no imóvel | 25% | [Registros de medidas e impactos](07_Imovel/Medidas_e_impactos.csv); levantamento real depende das chaves |

Detalhes no [roteiro para projeto oficial](01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md).

## Decisões tomadas

- **Armários até o teto:** Elias, 26/10/2026, nesta conversa: “Todos os armários previstos até o teto, em todos os ambientes” e “ok, mantem 18mm para esses casos, mas deixa branco”. Tampos com ligações para 18 mm ficam em Branco TX nas duas faces, sem chapa decorativa sobreposta; encontro ao teto acabado a compatibilizar. [Diretriz e cotas atuais](04_Moveis/README.md#diretriz-de-fechamento-até-o-teto--26102026), compatibilização física de teto/acessos pendente; verificar escopo R53 no README do modelo.

- **Cores:** Branco TX em peças internas separadas; Arenza na cozinha, lavanderia, escritório e quarto; Azul Petróleo nos aéreos da cozinha; off-white e bege foscos; Granito Branco Itaúnas; piso vinílico Olmo.
- **Sala:** sofá Bonnie; mesa Berlin pronta com três cadeiras; banco baú com duas tampas presas por dobradiça piano e articuladores com trava (protótipo pendente).
- **Quarto:** roupeiro de 65 cm com portas de correr; cama queen futura. Geral smart com brilho regulável, Alexa/celular (Elias, 26/10/2026: “quero q seja possivel conecta-las na alexa e celular”); D03-B Elgin 48D18WSRWIFI só no quarto (Elias 27/10/2026); manual/comando físico pendentes. D04-A: cabeceira/face inferior acessível, implantação pendente.
- **Canto P02:** duas portas independentes e quina fixa ([mockup](04_Moveis/Proximas_decisoes/P01_P03/Abertura_armario_L.png)); ferragens, limitador e folgas condicionados.
- **Maleiro P03:** Elias, 25/10/2026, prefere a opção A (duas folhas 672 × 306) e confirmou Arenza liso; aplicar somente se atender, ainda não executado. [README do P03](04_Moveis/P03/README.md).
- **Aéreos P17/P04/P12:** Elias, 25/10/2026: “20 kg / 10 kg / 10 kg” (nesta ordem), fundos inteiros e base limpa; capacidade não demonstrada. [Lote B](04_Moveis/Aereos_suspensao/README.md#lote-b--p17p04p12).
- **Oficina/material:** Elias, 26/10/2026: “Ainda não; deixar o roteiro pronto” (T0/P04 preparado, sem ensaio). [P04](04_Moveis/P04/Suspensao_P04_P15/README.md).
- **Tecidos:** cortina da sala C2 Areia; suede areia no banco e na cabeceira; aéreo do escritório marfim claro. Códigos comerciais dependem de amostra.
- **Cozinha:** forno Fischer 127 V, cooktop KE4GC a gás natural, gaveta de limpeza sobre rodízios Leão Aço.
- **Banheiro:** gabinete com portas de correr e frente removível; parede verde no box; luz de teto/indireta 3000 K e espelho 4000 K, três comandos ([L02: composição histórica](03_Ambientes/Banheiro/Fechamento_pre_entrega/Luminarias_selecao_L02.html)); chapas Arauco Beige Matt e Louro Freijó Poro.
- **Ferragens:** dobradiças Blum, corrediças FGVTN 500 e MOVENTO 400 no escritório; 52 conjuntos Minifix (P10, P11, P15, P19).

Histórico completo: [Registro de decisões](01_Programa_e_decisoes/Registro_de_decisoes.md) e [Painel de decisões](01_Programa_e_decisoes/Painel_de_decisoes.md).

## Pendências por móvel

Nada abaixo está liberado para fabricação ou carga de uso. Os cálculos são nominais; hipóteses, números e perguntas exatas estão no README de cada item.

| Móvel | Estudo | Falta |
|---|---|---|
| P01/P02/P03 | [Ligação e caminho ao piso](04_Moveis/P03/README.md) | [P02: U1–U4=A](04_Moveis/Proximas_decisoes/P01_P03/README.md), Elias 27/10/2026: leves ocasionais, requisito 10 kg, peso na região apoiada, preservar vãos/aparência; produto/ensaio, juntas, soco/piso e fundo P01 pendentes |
| P04/P15 | [Suspensão](04_Moveis/P04/Suspensao_P04_P15/README.md) · [composição P15](04_Moveis/P15/Composicao_parcial/README.md) | Produto de suspensão, juntas, parede real |
| P04/P12/P17 | [Lote B](04_Moveis/Aereos_suspensao/README.md) · [P17](04_Moveis/P17/Base_fundo_ligacoes/README.md) · [P12](04_Moveis/P12/README.md) | Executar T0 (oficina), qualificar Bigfer/juntas, contatos e ancoragens |
| P09/P11 | [Lote A](04_Moveis/Aereos_suspensao/README.md) | Contato real, fixadores, retenção, parede |
| P14/P20 | [Assento](04_Moveis/P20/Assento_fechado/README.md) · [cesto](04_Moveis/P14/Reacoes_e_operacao/README.md) | [Kit de oficina e formulário](04_Moveis/P20/Assento_fechado/Roteiro_banco_cesto.md) preparados; produto, suporte/terminais, pivôs e ensaio pendentes; preço completo não fechado |
| P08 | [Rodízios e estabilidade](04_Moveis/P08/README.md) | Massas, contato, guias, batente, retirada completa |
| P01/P06 gavetas | [Inventário](04_Moveis/Inventario_dimensional/Gavetas/README.md) | Proposta FGVTN 500, fixação das frentes, consulta não enviada |
| P16 e bancada | [Gavetas](04_Moveis/P16/Gavetas_estabilidade/README.md) · [Bancada](04_Moveis/Bancada/README.md) | Massa e rigidez do tampo 30, juntas, montagem real |
| Micro-ondas (T05) | [Cadeia dimensional](04_Moveis/Proximas_decisoes/Instalacao_e_P16/README.md) | 10 cm desejados × 30 cm do manual; sem decisão técnica |
| Banheiro | [Acesso ao quadro BC43](03_Ambientes/Banheiro/Conferencia_bancada_porta.md) | Desenho de acesso e vistoria |
| Varal | [Percurso com roupa](03_Ambientes/Lavanderia/Varal.md) | Conferir roupas/posição antes de adotar o curso |
| Todos | [Corte por chapa física](04_Moveis/Proximas_decisoes/Corte_e_formatos/README.md) | P13/Peca 350: Arenza liso nas duas faces (Elias 27/10/2026, F13=A); acabamento integrado à R53/fichas R15; produto 18/bordas e corte pendentes |

## Próximos passos

1. **Elias envia hoje:** revisar e enviar o [pacote por destinatário](06_Entregas/Cotacao/index.html), com fichas R15, amostras D02 e IL02–IL09; todos não enviados. Prazo solicitado 30/10 às 18 h. Depois comparar propostas, amostras e respostas; contratar RT. Nenhuma contratação autorizada.
2. **No dia das chaves:** [roteiro](07_Imovel/Roteiro_dia_das_chaves_R01.md), com vistoria da Cury e medição.
3. **Depois das chaves:** ajustar modelo, fichas e orçamento às medidas reais; protocolar o [plano de reforma](01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md); contratar e executar.

**Quem resolve** (sugestão, não contratação): Elias — aparência das propostas visíveis; projeto — juntas, rigidez e interfaces; produto/oficina — ferragens reais, composição P15 e ensaios; RT após as chaves — medidas, parede, ancoragens, piso e liberação.

## Como trabalhar nesta pasta

- Regras de organização e leitura econômica: [AGENTS.md](AGENTS.md). Mapa das pastas: [README.md](README.md). Leia esta página e depois só o README da área; **não leia inteiro** o Registro de decisões (475 KB).
- Comece com `git status`; outras sessões editam a pasta. Commits pequenos, um assunto cada.
- Verificadores ([ferramentas/README.md](ferramentas/README.md)): `python ferramentas/verificar_tudo.py` antes de commitar; `python ferramentas/verificar_modelo/verificar_modelo.py --completo` depois de qualquer trabalho no FreeCAD. Antes de push, clone limpo com `--ci`.
- Não rode macros antigas que salvam ou fecham documentos; não sobrescreva o modelo vigente para consultar. Portas e movimentos: [cinemática fora do CAD](04_Moveis/Proximas_decisoes/Cinematica/README.md).
- Estudo que depende de medida real (chaves) já marcado como condicionado não ganha refinamento novo; registre a dúvida e siga outra frente.
- Versões antigas (R45 a R51, compatibilizações) estão no git, na tag `antes-reorganizacao`.

**Medidas → móveis (27/10):** [regras e roteiro das chaves](04_Moveis/Dependencias/README.md): reprodução R53 0 mm; ensaio fictício de 20 folhas/0,73 s. Caixas fixas; recortes e topologia manuais. CAD, fatos e medições reais preservados.
