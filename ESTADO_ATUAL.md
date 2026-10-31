# Guedala Park — estado atual

Vigente 30/10/2026; READMEs.

## O projeto

Interiores/marcenaria: Cury Guedala Park III (Torre 2, final 06, 8º andar, 40,18 m², dois dormitórios). **Não entregue**; cotas de projeto a conferir no local.

- **Objetivo:** tudo pronto para mudar; dois meses de obra após chaves, mudança no terceiro.
- **Verba:** R$ 120 mil de execução + R$ 10 mil de reserva intocada.
- **Regra de Elias:** nenhum tubo ou quadro metálico substituto para sustentar chapas de madeira sem sua autorização prévia. [Decisão e inventário](04_Moveis/Cargas_e_ligacoes/Decisao_sem_tubos.md).
- **Chapas/cores:** faces iguais por chapa; peças distintas podem diferir (externa 18 mm no padrão, interna 15 mm BrancoTX). Conferir geometria/ligações/cargas; caixa dupla/15 mm não automáticos. [Regra por peça](ferramentas/site/fabrication/Decisao_acabamentos_R13.md).
- **Pé-direito:** 2,60 m = 260 cm = 2600 mm em todos os cômodos; banheiro: **2,50 m = 250 cm = 2500 mm**, medida a confirmar (Elias, 27/10/2026). Escritório 2,47 m substituído. [Fonte e limites](01_Programa_e_decisoes/Pesquisa_pe_direito.md).

## Versões vigentes

| O quê | Versão | Abrir |
|---|---|---|
| Modelo 3D | R54: pedestal Berlin; cadeira lateral +15 mm | [Modelo](02_Modelo_3D/Guedala_Park_R54_Berlin.FCStd) · [Abertura segura](02_Modelo_3D/README.md) |
| Triagem geométrica | 0 inválidas/1.449 próprias (25/10); 12 contêineres | [Triagem e critério](02_Modelo_3D/README.md#triagem-das-formas-inválidas--25102026) · [dados](02_Modelo_3D/Triagem_geometria.json) |
| Fichas dos 20 móveis | R15 | [Fichas](06_Entregas/Fichas_fabricacao/index.html) · [Pendências](06_Entregas/Fichas_fabricacao/Pendencias.html) · [Levantamento](06_Entregas/Fichas_fabricacao/Levantamento.html) |
| Estudos dos móveis | Nominais, fora do CAD; painéis ~732 kg ref.; P01/Peca208 ~51 kg | [Cargas](04_Moveis/Cargas_e_ligacoes/Andamento_20_moveis.md) · [Massas](04_Moveis/Quantitativos/README.md) |
| Programa | R01; escolhas 29/10 | [Programa](01_Programa_e_decisoes/Programa_de_necessidades.md) |
| Planta mobiliada e vistas | R03; cena R54, 8 PNGs/SHA | [Planta mobiliada](03_Ambientes/Planta_mobiliada/README.md) |
| Especificações/luz | R01; E5% e U0 separados | [Caderno](01_Programa_e_decisoes/Caderno_de_especificacoes.md) · [Luz](03_Ambientes/Iluminacao/README.md) |
| Pontos (elétrica, água, gás) | R01; 6.740 W parciais; mínimos: 16 TUG/5.300 VA | [Planta de pontos](03_Ambientes/Planta_pontos/README.md) |
| Conectores (P01, P04, P12, P17) | R00, proposta | [Mapa de conectores](04_Moveis/Mapa_conectores/README.md) |
| Orçamento | R44 | [Orçamento](05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md) |
| Cronograma | R00; escopo 29/10: 29 nós/7 marcos; faltam prazos, sem probabilidades | [Rede e limites de compra](05_Orcamento_e_cronograma/README.md) |
| Pranchas A3 | R02: 20 folhas; 1:50/1:25; alturas 2,60/2,50 m | [Caderno de pranchas](06_Entregas/Caderno_pranchas/index.html) · [PDF R02](06_Entregas/Caderno_pranchas/Guedala_Park_Pranchas_R02.pdf) |
| Site/pacote do montador | R54/R29; 20 leituras e trava textual/CI; local; pub.: Elias,28/10/26 | [Site online](https://queiroz-labs.github.io/guedala-park/) · [gerador do site](ferramentas/site/README.md) · [evidência e limites](06_Entregas/README.md) |

Planta R23 publicada: Elias,26/10/2026, "Sim, autorizo comitt push". Lixeiras: [encaixe](03_Ambientes/Cozinha/Encaixe_lixeiras.md) +7/+6 cm, LIX=A (Elias27/10/2026, “A”), nominal na R53/site; testar pedal/tampa, passagem, varal e destino da Loop. ZIP não comprova compatibilização nem ensaios.

**Clima:** [parcelas](03_Ambientes/Equipamentos/README.md), TMY8.760h/ASUS condicional/carga pendente; [conforto anual](03_Ambientes/Conforto_ambiental/README.md).

**Acústica:** [piso, aparelhos e envoltória](03_Ambientes/Acustica/README.md); 29 faces/407 sensibilidades; isolamento real e custos pendentes.

**Acabamentos:** [quantidades e divergências](03_Ambientes/Acabamentos/README.md); vinílico líquido 30,8101 m²; box de correr até o teto (Elias, 30/10/2026).

## Onde estamos

| Etapa | % | Situação |
|---|---:|---|
| Programa e estudo preliminar | 100% | Fechados; falta só validar no local |
| Anteprojeto | 87% estimado | [Critério e pendências](01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md). D01–D06 respondidas; pacote pronto para envio; cotações/amostras impedem 90–95% |
| Executivo de marcenaria | 45–55% | Fichas prontas; faltam montagens do banco, cesto e gavetas, furação dos conectores e medidas reais |
| Complementares | 35% | [Pontos R01](03_Ambientes/Planta_pontos/README.md):53 funções, 50 originais auditadas; D03/D04/D06 integradas; E06 adiada, Q06 sem coordenada, implantação e circuitos com RT/oficina |
| Especificações | 80% documental | Catálogo 15/18 mm e códigos disponíveis no Caderno; D02: amostras Lume/Areia solicitadas por Elias 27/10; SKUs e escolha final pendentes |
| Orçamento | 60% | R44: R$ 137.748,11; luz 4.534,55. [D05-C](05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md#d05--plano-de-escopo-sem-descontos-presumidos), Elias 27/10: "C — cotar com aumento de verba". Referência 127.101,22, aporte 7.101,22, reserva 10.000 intacta; pacote 37.000 condicionado, sem contratar |
| Pranchas formais | 80% estimados | [R02 e critérios](06_Entregas/Caderno_pranchas/README.md): fonte CSV, R54, 12 elevações, impacto; faltam levantamento, interfaces e revisão técnica |
| Responsável técnico e aprovação | 10% | Rascunho do plano de reforma; RT ainda não contratado |
| Levantamento no imóvel | 25% | [Registros de medidas e impactos](07_Imovel/Medidas_e_impactos.csv); levantamento real depende das chaves |

Detalhes: [roteiro oficial](01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md).

## Decisões

- **Armários até o teto:** Elias, 26/10/2026, nesta conversa: “Todos os armários previstos até o teto, em todos os ambientes” e “ok, mantem 18mm para esses casos, mas deixa branco”. Ligações de 18 mm: tampos Branco TX nas duas faces, sem chapa decorativa sobreposta; compatibilizar teto acabado. [Diretriz e cotas](04_Moveis/README.md#diretriz-de-fechamento-até-o-teto--26102026), interfaces de teto pendentes.

- **Cores:** Branco TX em peças internas separadas; Arenza na cozinha, lavanderia, escritório e quarto; Azul Petróleo nos aéreos da cozinha; off-white e bege foscos; Granito Branco Itaúnas; piso vinílico Olmo.
- **Sala:** Philips 50PUG8100/78 e TAB4000 (29/10); TCL só reserva. Sofá Bonnie; Berlin com três cadeiras; banco com duas tampas, piano e articuladores com trava (protótipo pendente).
- **Quarto:** roupeiro 65 cm, portas de correr; viúva com baú 128×188×64 atual (29/10), queen futura. Geral smart, Alexa/celular (Elias, 26/10/2026: “quero q seja possivel conecta-las na alexa e celular”); D03-B Elgin 48D18WSRWIFI só no quarto (Elias 27/10/2026); manual/comando físico pendentes. D04-A: cabeceira/face inferior acessível, implantação pendente.
- **Escritório (29/10):** Ercathe A01 e ASUS 27″ + AOC 24″ fora da verba; volante/pedais retirados. [Setup](03_Ambientes/Escritorio/README.md).
- **Canto P02:** duas portas independentes e quina fixa ([mockup](04_Moveis/Proximas_decisoes/P01_P03/Abertura_armario_L.png)); ferragens, limitador e folgas condicionados.
- **Maleiro P03:** Elias, 25/10/2026, prefere a opção A (duas folhas 672 × 306) e confirmou Arenza liso; aplicar somente se atender, ainda não executado. [README do P03](04_Moveis/P03/README.md).
- **Aéreos P17/P04/P12:** Elias, 25/10/2026: “20 kg / 10 kg / 10 kg” (nesta ordem), fundos inteiros e base limpa; capacidade não demonstrada. [Lote B](04_Moveis/Aereos_suspensao/README.md#lote-b--p17p04p12).
- **Oficina/material:** Elias, 26/10/2026: “Ainda não; deixar o roteiro pronto” (T0/P04 preparado, sem ensaio). [P04](04_Moveis/P04/Suspensao_P04_P15/README.md).
- **Tecidos:** cortina da sala C2 Areia; suede areia no banco e na cabeceira; aéreo do escritório marfim claro. Códigos comerciais dependem de amostra.
- **Cozinha:** forno Fischer 127 V, cooktop KE4GC a gás natural, gaveta de limpeza sobre rodízios Leão Aço.
- **Banheiro:** ducha entre box e vaso; papeleira à esquerda do gabinete, a confirmar (imagem 29/10). Gabinete 60 cm, portas de correr/frente removível; verde em 2 paredes do box ([R55 pendente](02_Modelo_3D/Verde_box_candidato.md)); teto/indireta 3000 K, espelho 4000 K, 3 comandos ([L02 histórico](03_Ambientes/Banheiro/Fechamento_pre_entrega/Luminarias_selecao_L02.html)); Beige Matt/Louro Freijó Poro.
- **Ferragens:** dobradiças Blum, corrediças FGVTN 500 e MOVENTO 400 no escritório; 52 conjuntos Minifix (P10, P11, P15, P19).

Histórico completo: [Registro de decisões](01_Programa_e_decisoes/Registro_de_decisoes.md) e [Painel de decisões](01_Programa_e_decisoes/Painel_de_decisoes.md).

## Pendências por móvel

Fabricação/carga de uso pendentes. Estudos nominais; hipóteses/números/perguntas nos READMEs.

| Móvel | Estudo | Falta |
|---|---|---|
| P01/P02/P03 | [Ligação e caminho ao piso](04_Moveis/P03/README.md) | [P02: U1–U4=A](04_Moveis/Proximas_decisoes/P01_P03/README.md), Elias 27/10/2026: leves ocasionais, requisito 10 kg, peso na região apoiada, preservar vãos/aparência; produto/ensaio, juntas, soco/piso e fundo P01 pendentes |
| P04/P15 | [Suspensão](04_Moveis/P04/Suspensao_P04_P15/README.md) · [composição P15](04_Moveis/P15/Composicao_parcial/README.md) | Produto de suspensão, juntas, parede real |
| P04/P12/P17 | [Lote B](04_Moveis/Aereos_suspensao/README.md) · [P17](04_Moveis/P17/Base_fundo_ligacoes/README.md) · [P12](04_Moveis/P12/README.md) | Executar T0 (oficina), qualificar Bigfer/juntas, contatos e ancoragens |
| P09/P11 | [Lote A](04_Moveis/Aereos_suspensao/README.md) | Contato real, fixadores, retenção, parede |
| Ensaios de oficina | [Caderno, PDF e ZIP](06_Entregas/Ensaios_oficina/README.md) | 13 frentes; execução pendente. Desenhos/protocolos e cotação a fechar; instalação após levantamento |
| P08 | [Rodízios e estabilidade](04_Moveis/P08/README.md) | Massas, contato, guias, batente, retirada completa |
| P01/P06 gavetas | [Inventário](04_Moveis/Inventario_dimensional/Gavetas/README.md) | Proposta FGVTN 500, fixação das frentes, consulta não enviada |
| P16 e bancada | [Gavetas](04_Moveis/P16/Gavetas_estabilidade/README.md) · [Bancada](04_Moveis/Bancada/README.md) | Massa e rigidez do tampo 30, juntas, montagem real |
| Micro-ondas (T05) | [Cadeia dimensional](04_Moveis/Proximas_decisoes/Instalacao_e_P16/README.md) | 10 cm desejados × 30 cm do manual; sem decisão técnica |
| Banheiro | [BC43](03_Ambientes/Banheiro/Conferencia_bancada_porta.md) · [Água quente](03_Ambientes/Banheiro/Comparacao_rotas_agua_quente.md) | Acesso, vazão, rotas, elétrica com RT; sem escolha (29/10) |
| Varal | [Percurso com roupa](03_Ambientes/Lavanderia/Varal.md) | Conferir roupas/posição antes de adotar o curso |
| Todos | [Corte e custo nominal](04_Moveis/Plano_de_corte/README.md) | 15 chapas/215 painéis; 33 bloqueados e fundo fora; retalhos e custos de sete propostas exportados; meta não demonstrada |

**Cotação:** [101 linhas; aritmética sem erros; bases P19 distintas](06_Entregas/Cotacao/README.md).

**Cotações:** [comparador; sem propostas](05_Orcamento_e_cronograma/Orcamento/Cotacoes/README.md).

**Chaves:** [JSON→cadeia; PR com datum](07_Imovel/README.md); [guia: 34 fotos/setas](ferramentas/site/Dia_das_chaves.html); sem medida real.

**Perguntas:** [pacote não enviado](01_Programa_e_decisoes/Perguntas_em_aberto/README.md).

**Gás:** [rede/ventilação nominal](03_Ambientes/Gas_natural/README.md).

## Próximos passos

1. **Cotação não enviada:** [pacote](06_Entregas/Cotacao/index.html) R15, quantidades nominais (29/10), D02 e IL02–IL09. Elias revisa/envia; resposta solicitada 30/10 às 18 h. Comparar propostas/amostras/respostas. RT pendente; sem contratação autorizada.
2. **No dia das chaves:** [checklist de vistoria](07_Imovel/Checklist_vistoria_dia_das_chaves.md) + [medidas](07_Imovel/Roteiro_dia_das_chaves_R01.md).
3. **Depois das chaves:** ajustar modelo, fichas e orçamento às medidas reais; protocolar o [plano de reforma](01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md); contratar e executar.

**Piso/rodapé:** [candidato externo](02_Modelo_3D/README.md#candidato-piso-e-rodapé): 3 pisos, rodapé 80/15 mm nominal; 106 cenários; completo OK; aprovação pendente. R54/base intactos.

**Responsáveis a contratar:** projeto: juntas/interfaces; oficina: ferragens/ensaios; RT: campo/ancoragens/piso. Elias: aparência.

## Como trabalhar nesta pasta

- [AGENTS](AGENTS.md): status/README/busca no Registro. [Mapa](README.md).
- Abertura: PS1 prefere candidato piso/rodapé da base atual; `-Vigente` abre oficial. Usa o FreeCAD mais novo instalado.
- [Verificações](ferramentas/README.md): geral pré-commit; completo após abrir CAD; clone limpo `--ci` pré-push; commit por assunto.
- Não salvar/fechar CAD por macro nem sobrescrevê-lo em consulta; pendências de campo/oficina: registrar e seguir.
- R45–R51 e compatibilizações: git, tag `antes-reorganizacao`.

**Medidas → derivados (28/10):** [paredes, folgas e campo](04_Moveis/Dependencias/README.md): datum comum, 34 folgas ≤15 mm; proposta 10 mm sem mudar caixas; datum físico pendente.

**Moodboard:** [painéis 4K, A3 e Dia/Noite](09_Referencias/README.md). Lavanderia/banheiro corrigidos por medida (Elias,29/10/2026: “Aprovo a segunda”); galeria de iluminação usa o banheiro noturno atual, local.

**Furação (28/10):** [sequência nominal](04_Moveis/Furacao/Sequencia_e_centros.md):37 restrições/0 ciclos; 2.286 centros preservados; novos dependem de datum/apoios.

**Dimensões (28/10):** [R44 → R54](04_Moveis/Inventario_dimensional/Inventario/Comparacao_R44_R54.md):380 IDs/37 vãos; P09 +194 mm, P16 superior −6 mm; histórico separado.

**Movimentos (29/10):** [R54 e limites](04_Moveis/Proximas_decisoes/Cinematica/README.md): 1.528 mínimos/277 intervalos; oito choques com portas P01 fechadas; sem garantia contínua ou folga real.

**Risco:** [hipóteses](05_Orcamento_e_cronograma/Risco/README.md).
