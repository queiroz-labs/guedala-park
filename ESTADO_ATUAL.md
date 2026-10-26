# Guedala Park — estado atual

Fonte única de verdade do projeto. Em caso de divergência com qualquer outro documento, vale esta página. Atualizada em 26/10/2026.

## O projeto

Interiores e marcenaria de um apartamento Cury Guedala Park III (Torre 2, final 06, 8º andar, 40,18 m², dois dormitórios). **O apartamento ainda não foi entregue**: todas as medidas vêm da planta oficial e precisam ser conferidas no local.

- **Objetivo:** mudar com tudo pronto, com dois meses de obra depois das chaves e mudança no terceiro mês.
- **Verba:** R$ 120 mil de execução + R$ 10 mil de reserva intocada.
- **Regra fixa de Elias:** nenhum tubo sustentando chapas de madeira, nem quadro metálico substituto. Qualquer proposta desse tipo exige autorização prévia. [Decisão e inventário](04_Moveis/Cargas_e_ligacoes/Decisao_sem_tubos.md).

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
| Orçamento | R43 | [Orçamento](05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md) |
| Cronograma de obra e compras | R00 | [Cronograma](05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md) · [plano de execução até 31/10](05_Orcamento_e_cronograma/Plano_execucao_ate_31_10.md) |
| Pranchas A3 | R00 | [Caderno de pranchas](06_Entregas/Caderno_pranchas/index.html) · [PDF](06_Entregas/Caderno_pranchas/Guedala_Park_Pranchas_R00.pdf) |
| Site e pacote para o montador | Site com R52; pacote R21 e estudos P17/P12 | [Site online](https://queiroz-labs.github.io/guedala-park/) · [gerador do site](ferramentas/site/README.md) |

O pacoteR21 acrescenta a matriz20/20 e os estudos separados de suspensãoP17/P12, com desenhos, vetores e requisitos de qualificação. Biblioteca e fichas do site dão acesso aos estudos; geometriaR52 preservada. Atualização/publicação autorizada por Elias em26/10/2026:“commit push atualiza o site”.

## Onde estamos

| Etapa | % | Situação |
|---|---:|---|
| Programa e estudo preliminar | 100% | Fechados; falta só validar no local |
| Anteprojeto | 75% | Faltam códigos de chapa, tons exatos e luminárias |
| Executivo de marcenaria | 45–55% | Fichas prontas; faltam montagens do banco, cesto e gavetas, furação dos conectores e medidas reais |
| Complementares | 30% | Planta de pontos preliminar; circuitos e traçados com o responsável técnico |
| Especificações | 70% | Caderno gerado a partir dos dados do site |
| Orçamento | 60% | Cenário de R$ 137,8 mil para teto de R$ 120 mil; pacote de marcenaria pronto, **em espera** |
| Responsável técnico e aprovação | 10% | Rascunho do plano de reforma; RT ainda não contratado |
| Levantamento no imóvel | 25% | Roteiro pronto; depende das chaves |

Detalhes no [roteiro para projeto oficial](01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md).

## Decisões tomadas

- **Cores:** interiores Branco TX; Arenza na cozinha, lavanderia, escritório e quarto; Azul Petróleo nos aéreos da cozinha; off-white e bege foscos; Granito Branco Itaúnas; piso vinílico Olmo.
- **Sala:** sofá Bonnie; mesa Berlin pronta com três cadeiras; banco baú com duas tampas presas por dobradiça piano e articuladores com trava (protótipo pendente).
- **Quarto:** roupeiro de 65 cm com portas de correr; cama queen futura. Luz geral com três níveis de brilho pelo interruptor; conjunto Jurerê/SceneSwitch candidato, cerca de R$ 110 ([CB02](03_Ambientes/Iluminacao/Fechamento_custo_beneficio/Revisao_quarto_CB02.md)).
- **Tecidos:** cortina da sala C2 Areia; suede areia no banco e na cabeceira; aéreo do escritório marfim claro. Códigos comerciais dependem de amostra. [Luminárias nos ambientes](09_Referencias/Iluminacao_CB02/Galeria.md).
- **Cozinha:** forno Fischer 127 V, cooktop KE4GC a gás natural, gaveta de limpeza sobre rodízios Leão Aço.
- **Banheiro:** gabinete com portas de correr e frente removível; uma parede verde no box. Luz de teto/indireta 3000 K e espelho 4000 K, três comandos. [Componentes L02: R$ 612,64 à vista](03_Ambientes/Banheiro/Fechamento_pre_entrega/Luminarias_selecao_L02.html). Chapas: Arauco Beige Matt e Louro Freijó Poro.
- **Ferragens:** dobradiças Blum, corrediças FGVTN 500 e MOVENTO 400 no escritório; 52 conjuntos Minifix (P10, P11, P15, P19).

Histórico completo das decisões: [Registro de decisões](01_Programa_e_decisoes/Registro_de_decisoes.md) e [Painel de decisões](01_Programa_e_decisoes/Painel_de_decisoes.md).

## Pendências por móvel

Nada abaixo está liberado para fabricação ou carga de uso. Os cálculos são nominais, e cada item tem hipóteses e perguntas exatas no seu README.

| Móvel | Já feito | Falta |
|---|---|---|
| P01/P03 | [Caixa superior e caminhos compartilhados](04_Moveis/Proximas_decisoes/P01_P03/README.md): 54 cenários, 12 equilíbrios por painel. [Caminho ao piso](04_Moveis/P01/Apoios_ao_piso/README.md), [massas](04_Moveis/P01/Massas_equilibrio/README.md): 315,9 kg sem conteúdo | Curvas e capacidades reais das juntas, detalhamento interno P02. O fundo P01 (1964×2096) não cabe em chapa 2750×1850: confirmar fornecimento ou projetar emenda estrutural |
| P04/P15 | [Suspensão](04_Moveis/P04/Suspensao_P04_P15/README.md): 660 casos. [Auditoria P04](04_Moveis/Ligacoes_sem_tubos/P04_auditoria_referencias.json): 869,5/300 = 2,898 mm, flecha 1,523 mm | Produto de suspensão, juntas e parede real |
| P15 | [Composição entre camadas](04_Moveis/P15/Composicao_parcial/README.md); [loteA](04_Moveis/Aereos_suspensao/README.md):8Minifix preservados,6Confirmat candidatos atuais/18 na variante; pino27 da nova borda inferior | Produto/processo/ensaio da composição e juntas; TitebondMelamine excluída. Mapa não une camadas. Suspensão sem produto demonstrado |
| P04/P12/P17 — loteB | [Estudo vigente](04_Moveis/Aereos_suspensao/README.md#lote-b--p17p04p12):Elias,25/10/2026:“20 kg / 10 kg / 10 kg” emP17/P04/P12,fundos inteiros/base limpa.585casos/60Minifix;até92,33/46,21/41,51kg sem ferragens. P04:4acessosSW4 nominais;765equilíbrios/1530vetores;pacote para laboratório,T0 com5retalhos/8Minifix e15registros vazios;R52 intacta | ExecutarT0 e caracterizar juntas/suspensão. BigferP04 candidata no divisor18/fundo e lateral direita;contatos/parede e ensaio físico pendentes. Nenhuma medição preenchida |
| P09/P11/P12/P17 | [LoteA P09/P11/P15](04_Moveis/Aereos_suspensao/README.md):Bigfer candidata≈60mL/par;assento40,5/furo9,5 e montagem por dentro propostos. Apoio inferior:faixas18×60 existentes,4176reações com equilíbrio3D;compressão até294,82N nos cenários10/20kg. Fundo–laterais:8casos de corpo de prova/4configurações,6Confirmat candidatos. [P17](04_Moveis/P17/Base_fundo_ligacoes/README.md) | Área/centro de contato reais e juntas/fundo não comprovados;uma coluna pontual não reageMz sozinha. Reações do corpo de prova são de norma mínima,não forças de projeto. Bigfer/fixadores/retencão/parede pendentes. P09:abas reais/42−30=12 condicional,sem atribuir6kg ao aéreo |
| P17 | [Suspensão candidata](04_Moveis/P17/Base_fundo_ligacoes/README.md#suspensão-candidata--26102026):u40,5/1923,5,Z514,braço424;765equilíbrios/1530vetores;8calços/24acessos conferidos | QualificarBigfer/juntas/ferramentaØ12 auxiliar;contatos inferiores,referência superior e massas reais;capacidade e ancoragens pendentes |
| P12 | [Suspensão candidata](04_Moveis/P12/README.md):u40,5/724,5,Z548,braço458;225equilíbrios/450vetores;4calços/12acessos conferidos;fundo548 preservado | QualificarBigfer/fixadores/ferramenta;provar base/divisor/juntas/caixa e medir contato inferior. Sem capacidade ou ancoragens demonstradas |
| P16 e bancada | [Gavetas e estabilidade](04_Moveis/P16/Gavetas_estabilidade/README.md): 1296 cenários. [Interface guia–fundo](04_Moveis/P16/Interface_guia_fundo/README.md). [Bancada](04_Moveis/Bancada/README.md): tampo 2000×700×30, curso 400 | Massa e rigidez do tampo 30, juntas, montagem real 400. Não cortar madeira para zerar o STEP |
| P14/P20 banco e cesto | [Assento fechado](04_Moveis/P20/Assento_fechado/README.md), [reações do cesto](04_Moveis/P14/Reacoes_e_operacao/README.md): 270 cenários | Comprar 1 piano e 2 pares de articuladores (~R$ 150, [preços](04_Moveis/Banco_e_cesto/Cesto_simples/Precos_e_conjunto_R01.md)) para protótipo; pivôs, limitadores a 55°, retenção |
| Todos | [Corte e formatos](04_Moveis/Proximas_decisoes/Corte_e_formatos/README.md): 249 painéis triados, 210 arranjados | 39 painéis sem produto/faces definidos; nenhum plano de corte liberado |

## Próximos passos

**Controle de25/10 consolidado em26/10:** [matriz20/20](04_Moveis/Cargas_e_ligacoes/Andamento_20_moveis.md) revisada; T01 documental concluída. T02/T03 continuam parciais: juntas/suspensão, composiçãoP15 e caixa superiorP01/P03. P04 tem pacote de laboratório, sem ensaios; P17/P12 têm implantação nominal; qualificação física e rigidez continuam pendentes. Decisões de uso/acabamento e verificações do imóvel seguem identificadas. Dia26 em andamento; integração30 e conferência31 preservadas.

1. **Antes das chaves:** seguir o [plano até 31/10](05_Orcamento_e_cronograma/Plano_execucao_ate_31_10.md); concluir as luminárias na [lista curta](03_Ambientes/Iluminacao/Lista_curta_luminarias_e_madeira.md); pedir orçamentos de marcenaria quando o pacote sair da espera; contratar o responsável técnico e enviar os [e-mails preparados](01_Programa_e_decisoes/Rascunhos_emails.md).
2. **No dia das chaves:** [roteiro do dia das chaves](07_Imovel/Roteiro_dia_das_chaves_R01.md), com vistoria da Cury e medição.
3. **Depois das chaves:** ajustar modelo, fichas e orçamento às medidas reais; protocolar o [plano de reforma](01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md); contratar e executar.

**Quem resolve cada dependência** (sugestão, não contratação): projeto (caixas P01/P02/P03, juntas, retenção); produto/oficina (painéis reais, processo P15, ferragens, componentes P14/P20); Elias (aparência das propostas visíveis: soco frontal 62 de P01, faixa inferior 18 de P15, painéis da bancada); RT após as chaves (medidas, parede, ancoragens, piso, liberação).

## Como trabalhar nesta pasta

- Estudos dos aéreos: hashes de texto normalizamCRLF/LF e caminhos relativos usam`/`, permitindo conferência em clone limpo. PDF/FCStd continuam byte a byte; cálculos e geometrias preservados.

- Regras de organização e leitura econômica: [AGENTS.md](AGENTS.md). Mapa das pastas: [README.md](README.md).
- Fluxo Git reforçado por Elias (25/10/2026): commits pequenos e por assunto, inclusão por caminho, README da área e estado atual no mesmo commit; verificação e hook antes de commitar, clone limpo com `--ci` antes de push e acompanhamento de cada processo Git até terminar. Limites: README ≤16 KB; demais `.md` ≤60 KB. Regras completas no [AGENTS.md](AGENTS.md#7-git-e-sessões-simultâneas).
- Leia esta página, depois só o README da área. Dados pontuais: JSON ao lado de cada README. **Não leia inteiro** o Registro de decisões (475 KB): busque por palavra.
- Portas e movimentos: [cinemática fora do CAD](04_Moveis/Proximas_decisoes/Cinematica/README.md) (`ferramentas/cinematica/consultar.py`); não anime o apartamento inteiro para cada conta.
- Não rode macros antigas que salvam ou fecham documentos. Não sobrescreva o modelo vigente para consultar.
- **Verificadores** ([ferramentas/README.md](ferramentas/README.md)): `python ferramentas/verificar_tudo.py` (o hook de commit roda sozinho) e, depois de qualquer trabalho no FreeCAD, `python ferramentas/verificar_modelo/verificar_modelo.py --completo`, que acusa objetos removidos, formas inválidas, expressões perdidas e colisões novas.
- Versões antigas (R45 a R51, compatibilizações, arquivo morto) estão no git, na tag `antes-reorganizacao`.
