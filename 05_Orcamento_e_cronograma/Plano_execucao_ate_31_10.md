# Plano de execução do Guedala Park até 31 de outubro de 2026

Preparado em 24/10/2026. Prazo de organização: **31/10/2026, horário de São Paulo**. Para versões, entregas e pendências vigentes, consultar o [Estado atual](../ESTADO_ATUAL.md).

**Objetivo:** concentrar cálculos, compatibilização e decisões técnicas até **29/10**; usar **30/10 para integração** e **31/10 para conferência, correções e entrega**.

O resultado pretendido é um projeto nominal consistente e fácil de continuar: modelo, fichas, especificações, orçamento e instruções concordando entre si. Como o apartamento ainda não foi entregue, medidas finais, ancoragens no imóvel e liberação de fabricação continuarão condicionadas. O prazo é de preparação do projeto, não de execução da obra.

## 1. Ponto de partida

| Frente | O que já existe | Trabalho restante nesta semana |
|---|---|---|
| Modelo e fichas | FreeCAD R52, fichas R14; ZIP local R20 íntegro (conferência 26/10); R23 configurado e ZIP remoto conferido (251 entradas, CRC e hashes) | Incorporar apenas detalhes demonstrados e conferir fontes/entrega antes de alterar ou republicar. |
| Gavetas do escritório | R49 corrigiu a folga superior para 7 mm e espelhou a trava direita | Tratar as condições remanescentes de fundo/guia e altura das guias; não repetir as correções concluídas. |
| Cargas e ligações | P11 sem tubos; estudos P15/P04/P01/P20, suspensão global de seis aéreos e equilíbrio por painel P01/P03 | Definir materiais, juntas e conectores; comprovar deformação/resistência e mecanismos P20/P14; selecionar suspensão e completar mapas. Contato não equivale a ligação resistente. |
| Banco e cesto | Diretriz simples definida; estudos e candidatos documentados | Completar montagem, apoios, retenção, acesso e plano de ensaio. |
| Ferragens e custos | Reconciliação documental de 24/10 já existe | Incorporar as diferenças na composição financeira e atualizar quantidades após os mapas. |
| Acabamentos e iluminação | Muitas escolhas já feitas, incluindo chapas do banheiro e seleção L02 | Resolver somente códigos, componentes e interfaces ainda abertos. |
| Site | Fontes R52 e consulta cinemática; R23 publicado e conferido; ZIP local R20 histórico | Validar navegação, revisões e integridade do pacote antes de publicar; conferir o resultado remoto. |

Fontes de partida: [Estado atual](../ESTADO_ATUAL.md), [R49](../02_Modelo_3D/Historico/Gavetas_escritorio/README.md), plano de cargas e ligações e [reconciliação de ferragens](../05_Orcamento_e_cronograma/Orcamento/Marcenaria_35mil/Reconciliacao_ferragens_fichas_R14_2026-10-24.md).

Há estudos em andamento em outros chats. Especialmente no P11, o cálculo de uma chapa apoiada nas laterais e a proposta de tubos não encerram o comportamento do armário completo. Incorporar a conclusão mais recente sobre fundo e uniões antes de escolher reforços; não adotar os tubos automaticamente.

## 2. Ordem de prioridade

**P0 — proteger até o fim:** cálculos e detalhes que destravam outros móveis, banco/cesto, coerência entre arquivos e material de continuidade. São os trabalhos mais caros de reconstruir com menos disponibilidade de IA.

**P1 — concluir na sequência:** especificações restantes, interfaces de equipamentos, orçamento consolidado e pacote para revisão profissional/cotação.

**P2 — somente com folga:** novas imagens, novos recursos do site, refinamento visual, comparações extensas de produtos e modelagem decorativa de ferragens. Não devem consumir a reserva de integração.

O caminho principal é: **base confiável → cargas e apoios → ligações e mecanismos → CAD e fichas → quantitativos e orçamento → pacote conferido**. Registrar as decisões pessoais cedo para não refazer os últimos passos.

### Sequência de execução

| Frente | Situação verificável | Próxima ação |
|---|---|---|
| T01/base e correção transversal T06 | Matriz 20/20 consolidada; T01 documental concluída. Corte e acabamentos continuam em T06 | Resolver P13 e demais padrões/constituições por ID; agrupamento virtual não autoriza compra/corte |
| T02/T03, lote A: P11/P15/P09 | [Apoio e caixa](../04_Moveis/Aereos_suspensao/README.md): faixas 18×60 existentes e 4176 reações 3D; 8 casos de corpo de prova fundo inteiro/duas laterais. Bigfer≈60 mL/par continua candidata; sem CAD alterado | Medir contato/centro reais, provar juntas/fundo e retenção; solução de norma mínima não dimensiona parafusos. Método/capacidade Bigfer, composição P15 e abas P09 continuam pendentes. Sem trocar ensaio por varredura |
| T02/T03, lote B: P04/P12/P17 | Metas 20/10/10 kg; P04: acessos SW4 e pacote de laboratório. P17/P12: implantações candidatas, 990 equilíbrios/1980 vetores, 12 casos de qualificação; calços/acessos conferidos | Qualificar Bigfer/fixadores/ferramenta Ø12 auxiliar e juntas/caixa; executar T0/P04. Contatos inferiores/parede reais pendentes; sem capacidade demonstrada |
| T03/T05, P01/P03/P02 | C01/soco e malas estudados; caixa superior ainda flexível e dados físicos pendentes | Resolver rigidez/uso P02 e produto/juntas/ferragens, fundo P01 e nivelamento. Aplicação CAD segue condicionada |
| T04/T05, 27–28/10 | Banco/cesto e interfaces de gavetas/equipamentos têm estudos e roteiro | Completar montagem nominal/ensaio e perguntas de produto; preservar correções existentes |
| T06–T09, 29–31/10 | Preparação comercial/documental e integração ainda parciais | Materiais/quantitativos/orçamento até 29; regeneração coerente 30; conferência/correções/entrega 31 |

As datas da agenda não certificam conclusão. Um bloco travado em dado externo termina com requisito/consulta/ensaio preparados e segue para tarefa independente, mantendo a condição visível. Mensagens, compras e incorporação de alternativas não estão presumidas por esta sequência.

## 3. Agenda diária

Planejar dois a três blocos de trabalho técnico por dia, de 60–90 minutos cada, ajustando ao rendimento real. São estimativas de organização, não duração garantida de chamadas de IA. A revisão de Elias acontece nesses blocos e ao final do dia; não representa horas adicionais obrigatórias.

| Data | Foco | Entrega do dia | Participação de Elias |
|---|---|---|---|
| **24/10, sábado** | Preparação | Este plano e ponto de partida identificados. Ao iniciar a execução, registrar a revisão vigente e recolher resultados dos chats em curso. | Confirmar prioridades e reunir decisões já tomadas. |
| **25/10, domingo** | Cargas e dependências | Matriz única de pendências; consolidar P11; desenvolver P15/P04 e iniciar P01/P20. Preparar perguntas exatas sobre dados faltantes dos produtos. | Concentrar escolhas que afetam uso, aparência e armazenamento; separar preferências de questões de cálculo. |
| **26/10, segunda** | Ligações e suspensão | Primeiro lote nominal P11/P15/P09 e desenvolvimento P04/P12/P17; cálculos prioritários concluídos ou com bloqueio específico registrado. | Revisar qualquer mudança visível, perda de espaço ou custo adicional antes de incorporá-la. |
| **27/10, terça** | Banco, cesto e roupeiro | Montagens nominais P20/P14, plano de ensaio e avanço P01/P02. Registrar elementos que ainda precisam de peça física ou oficina. | Conferir uso e acesso; decidir somente concessões explicitamente demonstradas. |
| **28/10, quarta** | Gavetas e interfaces | P01/P06/P16/P08; cozinha, banheiro, varal e equipamentos; completar mapas restantes por prioridade. | Fechar escolhas restantes de produtos, códigos e comandos com opções curtas. |
| **29/10, quinta** | Especificações e custos | Caderno de materiais/componentes, quantitativos e orçamento reconciliados; pacote nominal para cotação/revisão preparado. Encerrar desenvolvimento pesado planejado. | Decidir alternativas com impacto real no custo. Registrar o que ficará condicionado. |
| **30/10, sexta** | Integração | Regenerar fichas/site/pranchas/pacote, conferir consistência, corrigir divergências e preparar instruções de retomada. | Percorrer os ambientes, verificar decisões e testar a consulta dos documentos. |
| **31/10, sábado** | Reserva e entrega | Corrigir falhas remanescentes, reabrir modelo e pacote, salvar cópia de segurança e fechar lista de continuidade. | Revisão final; confirmar que consegue localizar arquivos, pendências e próximos passos. |

**Limite de escopo:** ao fim de 29/10, congelar novas alternativas e novos recursos. Em 30–31/10, entram correções necessárias à entrega. Se houver folga, usar primeiro para reduzir pendências técnicas já conhecidas.

## 4. Pacotes de trabalho e critérios de conclusão

As tarefas abaixo são planejadas. A existência deste plano não marca sua execução como concluída.

### T01 — Base e controle de pendências | P0 | 25/10

**Situação em 26/10:** concluída no critério documental da [matriz 20/20](../04_Moveis/Cargas_e_ligacoes/README.md#controle-vigente); sem bloqueio para essa revisão. Cálculos, detalhamento e ensaios permanecem nas tarefas seguintes; os 146 contatos são amostra histórica.

- Consolidar os 20 móveis e os complementos numa matriz com: item, pendência, origem, ação, responsável proposto, dependência, prazo e evidência de encerramento.
- Reconciliar os 146 contatos da amostra com a R49 ou sucessora, incluindo o P02 e qualquer ligação fora da amostra. Reaproveitar os 52 conjuntos Minifix já documentados sem duplicação.
- Classificar cada item: projeto agora, decisão de Elias, fornecedor, oficina ou apartamento. Não chamar tudo de “aguarda medidas”.
- Registrar revisão-base, arquivos alteráveis e cópia preservada. Uma única sessão modifica o modelo principal por vez; estudos separados são incorporados após conferência.

**Pronto quando:** todos os 20 móveis foram revisados e cada pendência tem uma próxima ação verificável. Responsável externo é uma indicação de quem precisa validar, não um compromisso já assumido.

### T02 — Cargas, apoios e suspensão | P0 | 25–26/10

**Situação em 26/10:** condicionada a composição/material, juntas, suspensão e parede real; memórias e bloqueios em [P11/P15/P09 e lote B](../04_Moveis/Aereos_suspensao/README.md), [P04/P15](../04_Moveis/P04/Suspensao_P04_P15/README.md), [composição P15](../04_Moveis/P15/Composicao_parcial/README.md), [massas P01](../04_Moveis/P01/Massas_equilibrio/README.md) e [P20](../04_Moveis/P20/Assento_fechado/README.md). Nenhuma capacidade física demonstrada.

- Reaproveitar o cálculo P11; avaliar a contribuição do fundo e das uniões antes de concluir pela necessidade de reforço.
- Desenvolver P15, P04, prateleiras/varões P01 e tampas/apoios P20. Reutilizar rotinas de cálculo com entradas, unidades e hipóteses explícitas.

- Mostrar o caminho da carga até a caixa e sua suspensão. Separar resistência da chapa, conectores e fixação na parede.
- Comparar no máximo duas soluções viáveis por problema; preservar armazenamento e aparência aprovados.

**Pronto quando:** cada caso prioritário tem memória reproduzível, desenho dos apoios, hipótese de uso, resultado e condições de validação. Cálculo nominal não é ensaio nem capacidade liberada. A ancoragem real permanece vinculada à parede encontrada no imóvel.

### T03 — Ligações e detalhamento no CAD | P0 | 26–28/10

**Situação em 26/10:** parcial; mapas nominais de [P17](../04_Moveis/P17/Base_fundo_ligacoes/README.md), [P12](../04_Moveis/P12/README.md), [P04](../04_Moveis/P04/Suspensao_P04_P15/README.md) e [P01/P03/P02](../04_Moveis/Proximas_decisoes/P01_P03/README.md) preparados. Bloqueios: qualificação de juntas/ferragens, [rigidez superior P01/P03](../04_Moveis/P01/Caminho_superior_P03/README.md), carga P02 e detalhamento restante; estudos sem integração automática à R52.

**Premissas preservadas:** Elias, 25/10/2026: “20 kg / 10 kg / 10 kg” em P17/P04/P12, “Desenvolver os fundos inteiros” e base limpa ([lote B](../04_Moveis/Aereos_suspensao/README.md)); “Preparar para marcenaria/laboratório” ([P04](../04_Moveis/P04/Suspensao_P04_P15/README.md)). Elias, 26/10/2026: “Ainda não; deixar o roteiro pronto”, sobre oficina/material ([P04](../04_Moveis/P04/Suspensao_P04_P15/README.md)).

- Seguir os lotes do plano técnico existente: A P11/P15/P09; B P04/P12/P17; C P01/P02; D P20; E demais encontros.
- Definir conector, peças ligadas, origem de cotas, posições, profundidades e acesso de montagem. Conferir encontros pelos dois lados de divisórias de 18 mm.
- Modelar detalhes demonstrados em revisões de estudo; identificar furação nominal e prova de oficina pendente. Não gerar furos definitivos a partir de dados comerciais incompletos.
- Salvar verificações de colisões e diferenças antes/depois, preservando peças não envolvidas.

**Pronto quando:** todo encontro inventariado tem solução documentada ou bloqueio concreto; os lotes incorporados ao CAD têm verificação e ficha correspondente. O alvo é cobrir todos os lotes; se a capacidade não permitir, priorizar A/B, os apoios críticos de C/D e registrar o restante como projeto pendente, sem convertê-lo artificialmente em dependência externa.

### T04 — Banco e cesto | P0 | 27/10

**Agenda27/10 preparada em26/10:** [kit de oficina P20/P14](../04_Moveis/P20/Assento_fechado/Roteiro_banco_cesto.md) com desenho de montagem/corte axial a completar, lista de amostras com fontes (subtotal conhecido260,52; não é custo completo) e12 registros vazios. Montagem definitiva/compra bloqueadas em perfil/apoio da piano, produto D/E, terminais, pilha do pivô e ligações; ensaio depende de oficina e plano do responsável. Zero ensaios, sem nova varredura ou alteração CAD.

- P20: fechar nominalmente eixo/apoio da dobradiça piano, terminais dos articuladores, trava, batentes, fixações e acesso para destravar. Preservar duas tampas, duas almofadas e armazenamento.
- P14: fechar pivôs, limitadores a 55°, retenção e retirada do saco. Verificar operação cheio/vazio e acesso de manutenção.
- Preparar desenho de protótipo, lista de componentes e roteiro de ensaio com resultados a registrar. Medir componentes e testar em oficina pode ocorrer antes das chaves.

**Pronto quando:** existe montagem nominal completa e um roteiro que permita à oficina testar sem redescobrir o projeto. Marcar ensaio concluído somente com evidência. Se faltarem dados do produto, salvar a pergunta exata e a versão condicionada.

**Avanço documental T04, 26/10:** [margens de engate P14/P20](../04_Moveis/Banco_e_cesto/Cesto_simples/Conferencia/Resultado.md#margens-geométricas-de-engate--t04-26102026): 36 sensibilidades e 12 inversões conferidas. Condição geométrica para receber dados da trava explicitada, sem novos furos/ângulos, ensaio ou CAD. Componentes reais, eixo, curso de liberação e juntas continuam pendentes.

**Continuidade27/10:** [P02 U1–U4=A](../04_Moveis/Proximas_decisoes/P01_P03/README.md), Elias27/10/2026: leves ocasionais, requisito10kg, peso na região apoiada e preservação de vãos/aparência; capacidade não demonstrada. Rigidez, juntas e produto seguem para projeto/oficina, sem nova varredura.

### T05 — Gavetas e interfaces dos ambientes | P0/P1 | 28/10

**Situação em 26/10:** condicionada a produto/oficina, juntas e compatibilização; [P16: curso/estabilidade](../04_Moveis/P16/Gavetas_estabilidade/README.md) e [guia–fundo](../04_Moveis/P16/Interface_guia_fundo/README.md), [P01/P03/P02](../04_Moveis/Proximas_decisoes/P01_P03/README.md) e [P08](../04_Moveis/P08/README.md) documentam estudos e limites; demais interfaces abaixo ainda precisam de desenho e teste específico.

**Premissa preservada, 25/10/2026:** Elias definiu duas malas de bordo de 10 kg, prefere A, duas folhas 672 × 306, e autorizou aplicar a abertura alternativa **se atender**; terceira mala condicionada. Fonte: requisito registrado neste plano em 25/10 e [estudo P01/P03/P02](../04_Moveis/Proximas_decisoes/P01_P03/README.md).

- P01/P06: conferir caixas, recortes e engates da FGVTN 500 com documentação própria; não extrapolar o STEP de 400 mm.
- P16: preservar a R49 e tratar a pequena sobreposição fundo/guia e o mapa de altura das guias conforme documentação e prova de oficina.
- P08: preservar os seis rodízios selecionados com espaçadores; detalhar fixação, guia e batente.
- Cozinha/lavanderia: revisar apoios, ventilação e retirada dos aparelhos; tratar a divergência registrada entre os 10 cm desejados acima do micro-ondas e os 30 cm atribuídos ao manual, sem considerar preferência como validação técnica. Conferir fonte vigente antes de concluir.
- Banheiro: frente removível, correr, torneira/cuba e manutenção; iluminação L02 com perfil, dissipação, fontes e terminais. Varal: curso, retenção e envelope nominal.

**Pronto quando:** cada interface tem desenho ou instrução objetiva, fonte e teste necessário. Nada continua apenas como “validar montagem”. Falta de dados precisa indicar qual dado e quem pode fornecê-lo.

**Avanço documental T05, 26/10:** [interface do micro](../04_Moveis/Proximas_decisoes/Instalacao_e_P16/README.md#t05--cadeia-dimensional-e-margens-26102026): nove cenários/288 combinações extremas; relação entre ventilação superior, posição da prateleira e vão de trabalho explicitada. Próximo: obter altura de uso necessária e erros/obstáculos reais para testar a faixa possível; nenhuma nova implantação adotada. P16, P08 e demais interfaces conservam suas pendências específicas.

**Continuação T05, 26/10:** [P08: percurso e retirada](../04_Moveis/P08/README.md#t05--percurso-e-retirada-26102026), 46 peças móveis e 50.002 pares separados até 400 mm; sequência de manutenção e critérios de guia/batente explicitados. [Varal carregado](../03_Ambientes/Lavanderia/Varal.md#t05--percurso-nominal-com-roupa-26102026), 30 cenários: descida máxima com roupa de 1200 mm encontra envelope da lixeira. Próximo: desenho das guias/batente e comprimentos/distribuição de roupa; ferragens, resistência e ancoragens continuam pendentes. Nenhum curso alterado.

**P01/P06 e banheiro — T05, 26/10:** [sete caixas](../04_Moveis/Inventario_dimensional/Gavetas/README.md) reconciliadas com a instrução FGVTN 500: P1 cabe, mas profundidade490/largura interna e engates representados não fecham a montagem. Proposta de 42 peças preparada: caixas 344/572 ×500, sete frentes preservadas; G2 conferido em sólidos (fundo 15, sem volume comum com bandejas); engate convencional sem gabarito, opcional 54TNOC12GAT3D com compatibilidade pendente. Consulta específica pronta/não enviada. [132 casos de ajuste/retirada](../04_Moveis/Inventario_dimensional/Gavetas/Ajuste_vertical_e_retirada.md): +3 com frente solidária conflita no P01 superior e zera folga superior P06; [fixação candidata](../04_Moveis/Inventario_dimensional/Gavetas/Fixacao_frentes.md) com 28 pontos e dois alojamentos baixos G2 detalhada. Validação parcial: 512 combinações; seção11 não demonstrada, comparação de rebaixo3,5 não adotada, par candidato RECA01814 25/Ettinger003.06.941 identificado, sem tolerâncias/encaixe comprovados; matriz de10 requisitos de produto preparada, não enviada. Dianteira16 rastreada na extração R42, sem material/SKU e sem linha própria na lista P06; seis comparações15/16/18 documentadas, sem substituir chapa. Produto/chapa/retencão, usinagem e retirada após destrave pendentes antes de incorporar. [BC43](../03_Ambientes/Banheiro/Conferencia_bancada_porta.md#t05--manutenção-do-quadro-bc43-na-r52-26102026): faixas de retirada/manuseio e ferramentas explícitas; porta real, pega/apoio e produtos seguem condicionados. Nenhuma correção geométrica ou prova física declarada.

**Lixeiras, preparação27/10:** [encaixe nominal proposto](../03_Ambientes/Cozinha/Encaixe_lixeiras.md) +7cm Biovis/+6cm Loop remove sobreposições de parede no desenho, com1cm nominal. Pedal/tampa, passagem, varal e destino temporário exigem gabarito/medição. Nenhuma posição aplicada ao FreeCAD/site.

### T06 — Acabamentos, iluminação e equipamentos | P1 | 28–29/10

**Situação em 26/10:** parcial; [corte por chapa física](../04_Moveis/Proximas_decisoes/Corte_e_formatos/README.md) reconciliado, sem compra/corte autorizado. Bloqueios: P13 e demais códigos/constituições, formato/substrato, veios, bordas/processo, componentes de iluminação e equipamentos; nenhuma segunda chapa 15 acrescentada automaticamente.

- Consolidar códigos de chapa, substrato, espessura, duas faces, bordas e veios; separar seleção comercial de confirmação por amostra.
- Preservar escolhas já feitas, inclusive Arauco Beige Matt/Louro Freijó Poro no banheiro e Branco TX interno. Resolver código do marfim e demais itens efetivamente pendentes.
- Iluminação: [proposta consolidada por ambiente](../03_Ambientes/Iluminacao/README.md), com inventário/comandos e consultas IL02–IL09 prontas, não enviadas. Quarto passa a smart Alexa/celular; cozinha/lavanderia/banheiro seguem comuns (Elias, 26/10/2026). Cenário parcial R$4.938,62 (busca por SKU sem oferta nacional confirmada; uso no Jurerê com vidro depende de resposta IL02/IL03), sem atualizar R44; inclui substituição dos WT1 e provisão de duas WiZ + WiZmote no quarto, retirando SceneSwitch. Faltam respostas de produto, cotação completa, decisão dos candidatos, levantamento/RT e ensaios; T06 permanece parcial para compra/execução. Não refinar nominalmente os bloqueios.
- Preparar lista de equipamentos com modelo, medidas, alimentação e acesso de manutenção, sem reabrir comparações encerradas.

**Pronto quando:** não há componentes indispensáveis omitidos; amostras e confirmação em campo aparecem como condições específicas. Posições executivas e dimensionamento de instalações seguem para revisão profissional.

**Preparação27/10:** [F13=A](../04_Moveis/Proximas_decisoes/Corte_e_formatos/README.md), Elias27/10/2026: Arenza liso nas duas faces de Peca350; produto18/bordas e inclusão na auditoria de corte pendentes. [Lista curta vigente](../03_Ambientes/Iluminacao/Lista_curta_luminarias_e_madeira.md) agora traz16 subtotais, fontes/datas e bloqueios, sem reabrir requisitos smart/comandos comuns.

### T07 — Orçamento e pacote para cotação | P1 | 29/10

**Agenda27/10 preparada em26/10:** [cenários A/B e perdas](Orcamento/Orcamento_R43.md#cenários-para-decisão-r44--agenda-2710) preservam escopo ou adiam TV; R44 mantida137.748,11. Proposta parcial de iluminação4.938,62, ainda não adotada; a memória4.415,94 é histórica. M09/cortina do quarto é provisão indevida frente ao Registro21/09: delta650 na estimativa/550 na meta, sem dupla contagem. Cenários corrigidos por escopo121.179,28/118.990,30 antes de lacunas, condicionados às negociações e decisão de faseamento. Marcenaria46.500 permanece provisão, pacote em espera.

- Consolidar a composição com os quantitativos resultantes de T03–T06. Usar a reconciliação de ferragens existente; incorporar Blum/calços/limitadores, Minifix e banco/cesto sem duplicar verbas.
- Desdobrar a iluminação L02 nas linhas correspondentes; não somar seu total novamente ao orçamento.
- Manter três colunas separadas: estimativa atual, meta de negociação e preço efetivamente cotado, com data, frete, montagem e exclusões.
- Preservar o teto registrado de **R$120 mil de execução + R$10 mil de reserva** e tratar os **R$35 mil de marcenaria como meta**. O consolidado R44 registra R$ 137.748,11 de execução; reconciliar as divergências nele listadas sem transformar descontos desejados em economia obtida.
- Atualizar o pacote de cotação já existente e a tabela para comparar propostas de mesmo escopo. Preparação não retira automaticamente o pacote da espera nem envia solicitações.

**Pronto quando:** totais reproduzíveis, escopo completo, diferenças explicadas e pendências comerciais visíveis. Retorno de fornecedor não é condição para terminar a organização do orçamento.

### T08 — Dossiê para o profissional e para as chaves | P1 | 29–30/10

**Situação em 26/10:** parcial; [entregas existentes](../06_Entregas/README.md) e [levantamento do imóvel](../07_Imovel/README.md) disponíveis. Falta compatibilizar as mudanças de T02–T07, fechar questões ao profissional e relacionar medidas/documentos afetados; contratação, revisão profissional e medidas reais seguem condicionadas.

- Reaproveitar programa, planta mobiliada, planta preliminar de pontos, caderno de pranchas, rascunho de reforma e roteiro de medição.
- Atualizar somente o que mudou; acrescentar as vistas e detalhes necessários para entender o projeto vigente.
- Preparar uma lista curta de questões para o responsável técnico: instalações, fixações, documentação da reforma e validações que dependem dele.
- Relacionar cada medida a levantar aos móveis/documentos afetados, para que a atualização após as chaves seja localizada.

**Pronto quando:** um profissional consegue identificar o escopo, decisões, hipóteses e o que deve conferir. Contratação, assinatura, aprovação e medição não são resultados presumidos da IA.

### T09 — Integração e continuidade com menos IA | P0 | 30–31/10

**Situação em 26/10:** parcial; [consulta cinemática](../ferramentas/cinematica/README.md) e [verificadores, incluindo espaços](../ferramentas/README.md) disponíveis. Bloqueios: integrar fontes e artefatos, conferir manifesto/abertura e cópia de segurança do pacote final; estudos dos [móveis](../04_Moveis/README.md) não equivalem a integração no CAD. Preservar 30–31/10 para essa conferência.

- Regenerar fichas, site, caderno e pacote a partir das fontes; conferir revisões e links. Corrigir avisos de “vigente” que ainda apontem para R45/R44 em entradas antigas.
- Rodar a verificação de consistência existente e as verificações pertinentes às alterações. Reabrir o FreeCAD salvo, o PDF e o ZIP; testar os acessos essenciais no computador e no celular.
- Manter a simplificação de textos e os ganhos de desempenho existentes. Só implementar melhoria de UX se corrigir uma falha de uso relevante na entrega.
- Criar uma página curta de retomada com: revisão vigente, cinco decisões mais recentes, pendências por responsável, próximo passo, caminhos dos arquivos e comandos comprovados para gerar/verificar entregas.
- Salvar memórias de cálculo, manuais usados, scripts, parâmetros e resultados. Manter estudos descartados identificados para evitar repetir pesquisas.
- Preparar cópia de segurança verificável do pacote final. Preservar o acervo privado separado dos materiais públicos.

**Pronto quando:** o pacote abre, os artefatos concordam e uma sessão nova consegue executar a próxima tarefa lendo a retomada e os arquivos específicos, sem reler todo o histórico.

## 5. Rotina para fazer a semana render

Reservar cerca de **2h15 por dia de participação de Elias**, ajustáveis: 15 minutos para escolher o resultado do dia, 60 minutos de revisão/decisões ao longo dos blocos, 45 minutos de conferência visual e uso, e 15 minutos para registrar o fechamento. O tempo adicional disponível pode ampliar o detalhamento ou permitir testes físicos viáveis.

Cada sessão começa com um resultado delimitado e termina com arquivos salvos, verificação e próxima ação. Usar este pedido-base:

> Execute a tarefa T__ do plano até 31/10. Leia o estado vigente e os documentos dessa tarefa. Preserve escolhas aprovadas e alterações de outras sessões. Entregue resultado verificável, registre hipóteses e bloqueios, atualize os arquivos dependentes e termine com o ponto exato de retomada.

Usar IA de maior capacidade para cálculos, diagnósticos, conflitos entre fontes e compatibilização. Usar scripts já conferidos para extrações, regeneração e validação repetitivas. Limitar pesquisa ao dado que falta; quando duas opções viáveis bastarem, apresentar recomendação e consequência concreta.

O plano original organizava sessões iniciadas pelo usuário. A autorização registrada neste plano em 25/10/2026 limitava as continuações no mesmo chat às 07:00 (America/Sao_Paulo); janela encerrada e automação pausada. Essa autorização não agenda o restante da semana. Nova janela nesta conversa,26/10/2026: “Trabalhe sozinho, sem parar, até as 07:30 de 27/10/2026 (horário de Brasília)”; sem push/publicação/envios ou alteração do FCStd, perguntas nos READMEs e mudança de frente em até30min de bloqueio. Às07:30, apenas relatório final; não autoriza continuação posterior.

## 6. Dependências e regras de corte

| Dependência ou risco | Ação nesta semana | Se não resolver no prazo |
|---|---|---|
| Dado de fabricante ausente | Identificar código e pergunta técnica até 25/10; deixar consulta pronta para envio autorizado | Entregar requisitos e estudo condicionado; não inventar dimensões, resistência ou CAD. |
| Peça física/protótipo | Preparar desenho, lista e roteiro até 27/10 | Manter como ensaio pendente, com sequência pronta. |
| Decisão pessoal | Apresentar até duas alternativas com custo, aparência e armazenamento afetados | Preservar a escolha vigente e registrar a decisão aberta; avançar nas partes independentes. |
| Novas conclusões em outro chat | Recolher o resultado e conferir revisão antes de editar a base | Não sobrescrever trabalho em curso nem incorporar proposta como aprovada. |
| Trabalho maior que o previsto | Reestimar ao fim de 25/10 e 27/10 | Cortar P2 primeiro; reduzir detalhamento secundário antes de sacrificar integração. |
| Sem medidas reais | Deixar formulário e relação de documentos afetados prontos | Encerrar a etapa nominal; revisão executiva após levantamento. |

**Regra para bloqueios:** após um bloco sem avanço por falta de dado externo, registrar a condição, preparar a consulta e passar a trabalho independente. Isso não marca a tarefa como concluída.

**Se houver atraso em 29/10:** proteger T01, os casos críticos de T02–T05 e T09. T06–T08 podem ser entregues parcialmente, com lacunas identificadas. Não eliminar a reserva de 30–31/10 para iniciar novas frentes.

## 7. Como medir o resultado em 31/10

Não usar uma porcentagem única de “projeto pronto”: desenho, protótipo, preço e aprovação são coisas diferentes. Registrar estes resultados separadamente:

- [x] 20/20 móveis revisados na matriz em 26/10, com pendência e próxima ação claras; manter atualizada até 31/10.
- [ ] **Condicionado:** Cinco frentes de carga prioritárias documentadas: P11, P15, P04, P01 e P20; registrar quais ficaram condicionadas.
- [ ] **Condicionado:** Todos os contatos inventariados classificados; informar quantos têm solução, quantos foram incorporados e quantos continuam sem detalhamento.
- [ ] **Condicionado:** Banco e cesto com montagem nominal e roteiro de ensaio; resultados físicos identificados como feitos ou pendentes.
- [ ] **Condicionado:** Gavetas e interfaces críticas conferidas; correções R48/R49 preservadas.
- [ ] **Condicionado:** Materiais, equipamentos e iluminação com lista de componentes e condições restantes.
- [ ] **Condicionado:** Quantitativos e orçamento reconciliados, ou divergências remanescentes explicitamente listadas.
- [ ] **Condicionado:** CAD, fichas, pranchas e pacote identificados por um manifesto de versões consistente.
- [ ] **Condicionado:** Modelo e pacote reabertos; links e verificações pertinentes aprovados ou falhas registradas.
- [ ] **Condicionado:** Retomada curta, scripts e cópia de segurança disponíveis.

**Entrega essencial:** eliminar ambiguidades sobre o que vale, concluir o maior número possível de decisões técnicas complexas e deixar as pendências reproduzíveis. **Entrega ampliada:** todos os lotes de ligações detalhados, dossiê completo e melhorias pontuais de consulta, desde que a entrega essencial esteja estável.

## 8. Continuidade após 31/10

Após 31/10, usar sessões curtas para incorporar respostas de fornecedores, comparar propostas pelo quadro pronto, registrar amostras, acompanhar protótipos e aplicar correções localizadas. Depois das chaves, preencher o levantamento e atualizar os documentos afetados.

Continuam dependentes de terceiros ou do imóvel: capacidade demonstrada em ensaios, preços e prazos contratados, responsável técnico, aprovações, medidas finais e liberação de fabricação. Esses itens devem sair desta semana com pergunta, desenho, formulário ou teste já preparado.

## 9. Controle diário

Preencher ao encerrar cada dia. “Concluído” exige o critério de aceite da tarefa; revisão sem evidência fica “em andamento”.

| Data | Resultado e arquivo | Verificação | Bloqueio e responsável | Primeira ação seguinte |
|---|---|---|---|---|
| 24/10 | Plano de execução criado | Links locais e estrutura conferidos na entrega | Execução técnica ainda planejada | T01 e consolidação das conclusões P11 |
| 25/10 | Fechamento documental registrado em 26/10: [matriz 20/20](../04_Moveis/Cargas_e_ligacoes/Andamento_20_moveis.md); P11 consolidado, P15/P04 desenvolvidos, P01/P20 iniciados; lote A/B e consultas locais preparados; R52 preservada | Memórias e conferências referenciadas por móvel; não equivalem a ensaios. Roupeiro 1728 casos condicionais e corte 249 IDs/215 incluídos/34 excluídos permanecem estudos | Projeto: rigidez superior P01/P03, mapas restantes; produto/oficina: juntas, composição P15, suspensão; Elias: carga P02, aparência e acabamentos; RT/imóvel: contatos, piso e parede | T02/T03: qualificar juntas/suspensão e preparar execução física P04; avançar implantação P17/P12 sem esperar genericamente pela Bigfer |
| 26/10 | Em andamento: matriz 20/20 e registro 25/10; suspensão P17/P12 implantada nominalmente, com fontes e consultas locais; pacote físico P04 preparado | P17: 765 equilíbrios/1530 vetores; P12: 225/450, conferência independente; 19 verificações gerais sem atenção. Nenhum ensaio físico | Produto/oficina: Bigfer/fixadores/ferramenta, juntas/rigidez e contato inferior. Projeto: demais caminhos resistentes. Imóvel/RT: parede/ancoragens | Qualificar montagem e caixa dos aéreos; executar retalho T0/P04 em oficina. Dia 26 segue aberto; preservar agenda27–31 |
| 27/10 | Preparação antecipada em26/10: [kit P20/P14](../04_Moveis/P20/Assento_fechado/Roteiro_banco_cesto.md), perguntas U1–U4/F13, cenários R44 A/B, lista curta e [encaixe das lixeiras](../03_Ambientes/Cozinha/Encaixe_lixeiras.md). Coerência: quarto smart/Firefly, envelope versus saco, R23 e cortina M09 indevida. Etapa documental entregue; execução física condicionada | verificar_tudo.py:19 verificações,0 com atenção, OK nos commits;12 registros vazios, somas de custos e SVG/XML conferidos. Sem nova varredura ou ensaio | P02: U1–U4=A registrado em27/10 (Elias); validação técnica pendente. P13: F13=A (Elias27/10), produto/bordas/corte pendentes. Elias: faseamento e concessões das lixeiras. Produto/oficina: ferragens, ligações/pivôs, preços completos e ensaio. Imóvel: folgas/piso/instalações | Responder opções nos READMEs; obter dados sem presumir envio e executar gabarito/protótipo com responsável. Integrar somente após condições atendidas; preservar30–31/10 |
| 28/10 | A preencher | A preencher | A preencher | A preencher |
| 29/10 | A preencher | A preencher | A preencher | A preencher |
| 30/10 | A preencher | A preencher | A preencher | A preencher |
| 31/10 | A preencher | A preencher | A preencher | A preencher |

Referências complementares: continuidade antes das chaves, [roteiro para projeto oficial](../01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md), [orçamento e atualizações](../05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md), [cronograma da obra após as chaves](../05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md) e [verificação de consistência existente](../ferramentas/Verificacao_consistencia.md). Referências históricas devem ser lidas junto às atualizações mais recentes.
