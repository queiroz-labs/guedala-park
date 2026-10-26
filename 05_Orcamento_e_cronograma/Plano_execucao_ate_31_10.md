# Plano de execução do Guedala Park até 31 de outubro de 2026

Preparado em 24/10/2026. Prazo de organização: **31/10/2026, horário de São Paulo**. Para versões, entregas e pendências vigentes, consultar o [Estado atual](../ESTADO_ATUAL.md).

**Objetivo:** concentrar cálculos, compatibilização e decisões técnicas até **29/10**; usar **30/10 para integração** e **31/10 para conferência, correções e entrega**.

O resultado pretendido é um projeto nominal consistente e fácil de continuar: modelo, fichas, especificações, orçamento e instruções concordando entre si. Como o apartamento ainda não foi entregue, medidas finais, ancoragens no imóvel e liberação de fabricação continuarão condicionadas. O prazo é de preparação do projeto, não de execução da obra.

## 1. Ponto de partida

| Frente | O que já existe | Trabalho restante nesta semana |
|---|---|---|
| Modelo e fichas | FreeCAD R52, fichas R14 de 20 móveis; publicação R52/R18 em preparação | Incorporar apenas detalhes demonstrados. Conferir a versão e a publicação no Estado atual antes de cada alteração. |
| Gavetas do escritório | R49 corrigiu a folga superior para 7 mm e espelhou a trava direita | Tratar as condições remanescentes de fundo/guia e altura das guias; não repetir as correções concluídas. |
| Cargas e ligações | P11 sem tubos; estudos P15/P04/P01/P20, suspensão global de seis aéreos e equilíbrio por painel P01/P03 | Definir materiais, juntas e conectores; comprovar deformação/resistência e mecanismos P20/P14; selecionar suspensão e completar mapas. Contato não equivale a ligação resistente. |
| Banco e cesto | Diretriz simples definida; estudos e candidatos documentados | Completar montagem, apoios, retenção, acesso e plano de ensaio. |
| Ferragens e custos | Reconciliação documental de 24/10 já existe | Incorporar as diferenças na composição financeira e atualizar quantidades após os mapas. |
| Acabamentos e iluminação | Muitas escolhas já feitas, incluindo chapas do banheiro e seleção L02 | Resolver somente códigos, componentes e interfaces ainda abertos. |
| Site | Fontes R52, consulta cinemática e pacote R18 em preparação | Validar navegação, revisão do CAD e conteúdo do pacote antes de publicar; conferir o resultado remoto. |

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

**Situação em 26/10:** condicionada a componentes reais, corte axial dos pivôs, ligações e ensaio; [P20](../04_Moveis/P20/Assento_fechado/README.md) e [P14](../04_Moveis/P14/Reacoes_e_operacao/README.md) têm montagem nominal e [roteiro conjunto](../04_Moveis/P20/Assento_fechado/Roteiro_banco_cesto.md), sem execução física. Oficina indisponível; consultas preparadas, não enviadas.

- P20: fechar nominalmente eixo/apoio da dobradiça piano, terminais dos articuladores, trava, batentes, fixações e acesso para destravar. Preservar duas tampas, duas almofadas e armazenamento.
- P14: fechar pivôs, limitadores a 55°, retenção e retirada do saco. Verificar operação cheio/vazio e acesso de manutenção.
- Preparar desenho de protótipo, lista de componentes e roteiro de ensaio com resultados a registrar. Medir componentes e testar em oficina pode ocorrer antes das chaves.

**Pronto quando:** existe montagem nominal completa e um roteiro que permita à oficina testar sem redescobrir o projeto. Marcar ensaio concluído somente com evidência. Se faltarem dados do produto, salvar a pergunta exata e a versão condicionada.

### T05 — Gavetas e interfaces dos ambientes | P0/P1 | 28/10

**Situação em 26/10:** condicionada a produto/oficina, juntas e compatibilização; [P16: curso/estabilidade](../04_Moveis/P16/Gavetas_estabilidade/README.md) e [guia–fundo](../04_Moveis/P16/Interface_guia_fundo/README.md), [P01/P03/P02](../04_Moveis/Proximas_decisoes/P01_P03/README.md) e [P08](../04_Moveis/P08/README.md) documentam estudos e limites; demais interfaces abaixo ainda precisam de desenho e teste específico.

- P01/P06: conferir caixas, recortes e engates da FGVTN 500 com documentação própria; não extrapolar o STEP de 400 mm.
- P16: preservar a R49 e tratar a pequena sobreposição fundo/guia e o mapa de altura das guias conforme documentação e prova de oficina.
- P08: preservar os seis rodízios selecionados com espaçadores; detalhar fixação, guia e batente.
- Cozinha/lavanderia: revisar apoios, ventilação e retirada dos aparelhos; tratar a divergência registrada entre os 10 cm desejados acima do micro-ondas e os 30 cm atribuídos ao manual, sem considerar preferência como validação técnica. Conferir fonte vigente antes de concluir.
- Banheiro: frente removível, correr, torneira/cuba e manutenção; iluminação L02 com perfil, dissipação, fontes e terminais. Varal: curso, retenção e envelope nominal.

**Pronto quando:** cada interface tem desenho ou instrução objetiva, fonte e teste necessário. Nada continua apenas como “validar montagem”. Falta de dados precisa indicar qual dado e quem pode fornecê-lo.

### T06 — Acabamentos, iluminação e equipamentos | P1 | 28–29/10

**Situação em 26/10:** parcial; [corte por chapa física](../04_Moveis/Proximas_decisoes/Corte_e_formatos/README.md) reconciliado, sem compra/corte autorizado. Bloqueios: P13 e demais códigos/constituições, formato/substrato, veios, bordas/processo, componentes de iluminação e equipamentos; nenhuma segunda chapa 15 acrescentada automaticamente.

- Consolidar códigos de chapa, substrato, espessura, duas faces, bordas e veios; separar seleção comercial de confirmação por amostra.
- Preservar escolhas já feitas, inclusive Arauco Beige Matt/Louro Freijó Poro no banheiro e Branco TX interno. Resolver código do marfim e demais itens efetivamente pendentes.
- Completar conjuntos de iluminação: luminária, lâmpada/fita, perfil, fonte, comando e acesso. Reaproveitar a seleção L02 e a revisão CB02 do quarto.
- Preparar lista de equipamentos com modelo, medidas, alimentação e acesso de manutenção, sem reabrir comparações encerradas.

**Pronto quando:** não há componentes indispensáveis omitidos; amostras e confirmação em campo aparecem como condições específicas. Posições executivas e dimensionamento de instalações seguem para revisão profissional.

### T07 — Orçamento e pacote para cotação | P1 | 29/10

**Situação em 26/10:** parcial; [consolidado R44](Orcamento/Orcamento_R43.md) com estimativa de execução R$ 137.748,11 e divergências explícitas. Bloqueios: reconciliar iluminação (R$ 10,62), composição da marcenaria e [quantitativos das propostas](../04_Moveis/Quantitativos/README.md) com T03–T06; pacote de cotação em espera, metas sem economia obtida.

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

O plano original organizava sessões iniciadas pelo usuário. A autorização registrada neste plano em 25/10/2026 limitava as continuações no mesmo chat às 07:00 (America/Sao_Paulo); janela encerrada e automação pausada. Essa autorização não agenda o restante da semana; novas etapas seguem as instruções atuais do projeto.

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
| 27/10 | A preencher | A preencher | A preencher | A preencher |
| 28/10 | A preencher | A preencher | A preencher | A preencher |
| 29/10 | A preencher | A preencher | A preencher | A preencher |
| 30/10 | A preencher | A preencher | A preencher | A preencher |
| 31/10 | A preencher | A preencher | A preencher | A preencher |

Referências complementares: continuidade antes das chaves, [roteiro para projeto oficial](../01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md), [orçamento e atualizações](../05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md), [cronograma da obra após as chaves](../05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md) e [verificação de consistência existente](../ferramentas/Verificacao_consistencia.md). Referências históricas devem ser lidas junto às atualizações mais recentes.
