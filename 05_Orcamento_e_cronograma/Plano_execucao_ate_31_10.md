# Plano de execução do Guedala Park até 31 de outubro de 2026

Preparado em 24/10/2026. Prazo de organização: **31/10/2026, horário de São Paulo**. Para versões, entregas e pendências vigentes, consultar o [Estado atual](../ESTADO_ATUAL.md).

**Objetivo:** concentrar cálculos, compatibilização e decisões técnicas até **29/10**; usar **30/10 para integração** e **31/10 para conferência, correções e entrega**.

O resultado pretendido é um projeto nominal consistente e fácil de continuar: modelo, fichas, especificações, orçamento e instruções concordando entre si. Como o apartamento ainda não foi entregue, medidas finais, ancoragens no imóvel e liberação de fabricação continuarão condicionadas. O prazo é de preparação do projeto, não de execução da obra.

**Execução em 25/10:** entregue a R50 completa otimizada, preservando os 5.893 objetos, 1.546 geometrias e movimentos da R49; integração local corrigida e tempos comparados. Em seguida foi executado o [primeiro ciclo de cargas e ligações](../04_Moveis/Cargas_e_ligacoes/README.md): 146 contatos reconciliados, encontros especiais P02/P01/P20 conferidos, cálculos P15/P04/P01/P20 e estudo separado de duas prateleiras723 do roupeiro, mantendo a decisão P11 sem tubos. Onze verificações numéricas passaram. T01/T02 seguem parciais: faltam mapas completos, deformação da caixa, juntas e suspensão; T03 iniciou com o estudo nominal P01. A R50 principal não foi modificada.

## 1. Ponto de partida

O primeiro ciclo mantém10 verificações vigentes após cancelar a alternativa tubular; o registro de11 acima descreve a rodada histórica anterior à decisão. As continuações e verificações próprias estão nos relatórios datados.

**Continuação autorizada em25/10 até07:00 de hoje, America/Sao_Paulo:** registro de execução e retomada. Retomadas neste mesmo chat até o prazo, com fechamento às7h. **Regra de projeto:** sem tubos sustentando chapas; qualquer proposta futura exige autorização prévia de Elias. Alternativas tubulares canceladas, inclusive estudo oculto da bancada retirado na R51. Estudos vigentes de marcenaria: [P15/P04](../04_Moveis/Ligacoes_sem_tubos/README.md) e P01_723 separado; nenhum foi incorporado silenciosamente ao modelo completo.

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

- Consolidar os 20 móveis e os complementos numa matriz com: item, pendência, origem, ação, responsável proposto, dependência, prazo e evidência de encerramento.
- Reconciliar os 146 contatos da amostra com a R49 ou sucessora, incluindo o P02 e qualquer ligação fora da amostra. Reaproveitar os 52 conjuntos Minifix já documentados sem duplicação.
- Classificar cada item: projeto agora, decisão de Elias, fornecedor, oficina ou apartamento. Não chamar tudo de “aguarda medidas”.
- Registrar revisão-base, arquivos alteráveis e cópia preservada. Uma única sessão modifica o modelo principal por vez; estudos separados são incorporados após conferência.

**Pronto quando:** todos os 20 móveis foram revisados e cada pendência tem uma próxima ação verificável. Responsável externo é uma indicação de quem precisa validar, não um compromisso já assumido.

### T02 — Cargas, apoios e suspensão | P0 | 25–26/10

**P04, coerência25/10:** eixos individuais nativos conferidos. A continuação separa as duas chapas do divisor e usa869,5/300=2,898mm; o primeiro ciclo usou centro do grupo878,5/300=2,928. Flecha1,523mm preservada. Corrigida a descrição de rigidez porposição/grupo no cálculo/roteiro, sem transformar requisito em capacidade de produto. [Auditoria](../04_Moveis/Ligacoes_sem_tubos/P04_auditoria_referencias.json).

**P15, composição parcial25/10:** [modelo contínuo da interface](../04_Moveis/P15/Composicao_parcial/README.md),16 respostas, cinco conferências e refinamento de cisalhamento. Recupera os limites sem ação composta/integral e quantifica hipóteses intermediárias, sem atribuir rigidez a produto. TitebondMelamine excluída da sustentação por limitação expressa; produto/processo/ensaio e caixa continuam necessários.

**P01, continuação25/10:** [massas simultâneas e equilíbrio](../04_Moveis/P01/Massas_equilibrio/README.md),4608 combinações/72 envelopes. A800, madeirasP01+P03+soco+723 somam315,9kg sem acessórios/conteúdo. Área nominal total0,270720m² inclui laterais originais; oito contatos superiores P01–P03/P02 conferidos. Massa de ferragens e partilha/caminhos da caixa superior continuam pendentes; cálculo rígido não substitui juntas, retenção ou piso real.

- Reaproveitar o cálculo P11; avaliar a contribuição do fundo e das uniões antes de concluir pela necessidade de reforço.
- Desenvolver P15, P04, prateleiras/varões P01 e tampas/apoios P20. Reutilizar rotinas de cálculo com entradas, unidades e hipóteses explícitas.

**Avanço25/10, suspensãoP04/P15:** [caixa inteira e portas abertas](../04_Moveis/P04/Suspensao_P04_P15/README.md),660 casos e72 envelopes de V/T/momento. Massas dos reforços incluídas; movimentos de quatro barras reutilizados sem alterar a R51. Resultantes são requisitos paramétricos, não fixadores/furos, produto escolhido ou capacidade da parede. Depende de produto/oficina e depois substrato real.

**Ampliação25/10:** [P09/P11/P12/P17](../04_Moveis/Aereos_suspensao/README.md),1404 casos e48 envelopes, com a cinemática calculada fora doCAD. P09 ganhou dado primário de massa do depurador6,00 kg e identificação da folga nominal42 mm até a base: a montagem prevista no manual parede+gabinete e sua partilha ainda precisam ser demonstradas. Não acrescentar6 kg a um suspensor sem esse caminho de forças.
- Mostrar o caminho da carga até a caixa e sua suspensão. Separar resistência da chapa, conectores e fixação na parede.
- Comparar no máximo duas soluções viáveis por problema; preservar armazenamento e aparência aprovados.

**Pronto quando:** cada caso prioritário tem memória reproduzível, desenho dos apoios, hipótese de uso, resultado e condições de validação. Cálculo nominal não é ensaio nem capacidade liberada. A ancoragem real permanece vinculada à parede encontrada no imóvel.

### T03 — Ligações e detalhamento no CAD | P0 | 26–28/10

**LoteB em25/10/2026:** [P17→P04→P12](../04_Moveis/Aereos_suspensao/README.md#lote-b--p17p04p12), respostas de Elias:“20 kg / 10 kg / 10 kg”,“Desenvolver os fundos inteiros” e base limpa.585casos/60Minifix;16entradas inferiores antigas a substituir. FundosP17/P04 preservam envelope/vãos,fitas inferiores Arenza/off-white. P04:4acessosSW4 curta resolvidos nominalmente;suporte esquerdo proposto no divisor18 após rejeitar canto externo;765equilíbrios3D/1530vetores,seis casos de qualificação. Juntas/rigidez,retenção,contatos inferiores e produto ainda sem prova física;R52 intacta.

**P01/P03, caminho superior25/10:** [estudo separado traseiro](../04_Moveis/P01/Caminho_superior_P03/README.md) preserva vãos e envelope, acrescentando18 na altura do fundoP01 e18 para trás na baseP03. Quatro interfaces conferidas, sem interferências dos acréscimos. Seis modelos reduzidos convergentes excedem a referência: contato sozinho não libera a base18. Ação de caixa/topo/fundo/laterais, travessa frontal e juntas continuam como trabalho de projeto, sem atribuir a pendência às medidas do apartamento.

**Avanço25/10, P17:** [estudo de fundo inteiro e ligações](../04_Moveis/P17/Base_fundo_ligacoes/README.md),16 contatos,58 posições nominais e11 casos de placa/caminhos axiais. Fundo514→550 separado preserva dimensões e vãos;20kg totais distribuídos/frontal dão0,863/1,336mm com reserva nas hipóteses adotadas. Juntas mais flexíveis excedem a referência. Comprovar produto/caixa, revisar acabamento/acesso e atualizar massa global antes de integrar; eixos não são CNC nem quantitativo adicional.

- Seguir os lotes do plano técnico existente: A P11/P15/P09; B P04/P12/P17; C P01/P02; D P20; E demais encontros.
- Definir conector, peças ligadas, origem de cotas, posições, profundidades e acesso de montagem. Conferir encontros pelos dois lados de divisórias de 18 mm.
- Modelar detalhes demonstrados em revisões de estudo; identificar furação nominal e prova de oficina pendente. Não gerar furos definitivos a partir de dados comerciais incompletos.
- Salvar verificações de colisões e diferenças antes/depois, preservando peças não envolvidas.

**Pronto quando:** todo encontro inventariado tem solução documentada ou bloqueio concreto; os lotes incorporados ao CAD têm verificação e ficha correspondente. O alvo é cobrir todos os lotes; se a capacidade não permitir, priorizar A/B, os apoios críticos de C/D e registrar o restante como projeto pendente, sem convertê-lo artificialmente em dependência externa.

### T04 — Banco e cesto | P0 | 27/10

**Avanço25/10:** [P20 fechado](../04_Moveis/P20/Assento_fechado/README.md):18 contatos reconciliados, cinco cenários de placa convergentes e levantamento de27 volumes. Massa permanente60kg histórica não é limite garantido; painel real/ortotropia, juntas e estabilidade pendentes. [Roteiro de protótipoP20/P14](../04_Moveis/P20/Assento_fechado/Roteiro_banco_cesto.md) preparado; nenhum ensaio executado. Mecanismos continuam sujeitos a perfil/terminais/trava efetivos, sem encerrarT04.

**P14, continuação25/10:** [reações dos pivôs e energia](../04_Moveis/P14/Reacoes_e_operacao/README.md),270 cenários3D e30 trajetórias. Identificados esforços reversos de retenção nos apoios e momentos de excentricidade; não basta dividir o peso por dois. Massa adicional, pivôs/buchas, terminais e engate efetivo seguem pendentes. Geometria e movimentos completos preservados, sem nova revisão do modelo.

- P20: fechar nominalmente eixo/apoio da dobradiça piano, terminais dos articuladores, trava, batentes, fixações e acesso para destravar. Preservar duas tampas, duas almofadas e armazenamento.
- P14: fechar pivôs, limitadores a 55°, retenção e retirada do saco. Verificar operação cheio/vazio e acesso de manutenção.
- Preparar desenho de protótipo, lista de componentes e roteiro de ensaio com resultados a registrar. Medir componentes e testar em oficina pode ocorrer antes das chaves.

**Pronto quando:** existe montagem nominal completa e um roteiro que permita à oficina testar sem redescobrir o projeto. Marcar ensaio concluído somente com evidência. Se faltarem dados do produto, salvar a pergunta exata e a versão condicionada.

### T05 — Gavetas e interfaces dos ambientes | P0/P1 | 28/10

**InterfaceP16, continuação25/10:** [18 regiões positivas localizadas](../04_Moveis/P16/Interface_guia_fundo/README.md):16 sob o fundo e duas junto ao furo traseiro direito. Cotas dos quatro furosØ6×10/eixo11 conferidas com desenhoG2; mesmo padrão4+5 na referência configurada. Causa funcional/regulagem e configuração individual400 continuam pendentes, com mapa/pergunta exata. Nenhum corte, deslocamento corretivo ou alteração do movimento foi aplicado.

**Avanço25/10:** [P16, curso e estabilidade](../04_Moveis/P16/Gavetas_estabilidade/README.md):18.480 pares de caixas varridas sem interseção com a proposta de bancada e64 entre gavetas independentes; guias telescópicas reais excluídas.1296 cenários de equilíbrio separam pedestal e bancada ligada; constituição/massa do tampo e juntas positivas continuam determinantes. Campo de altura da parede superior53→47 identificado e correção nominal preparada, sem alterar a R51. O conflito fundo/guia continua pendente.

- P01/P06: conferir caixas, recortes e engates da FGVTN 500 com documentação própria; não extrapolar o STEP de 400 mm.
- P16: preservar a R49 e tratar a pequena sobreposição fundo/guia e o mapa de altura das guias conforme documentação e prova de oficina.
- P08: preservar os seis rodízios selecionados com espaçadores; detalhar fixação, guia e batente.
- Cozinha/lavanderia: revisar apoios, ventilação e retirada dos aparelhos; tratar a divergência registrada entre os 10 cm desejados acima do micro-ondas e os 30 cm atribuídos ao manual, sem considerar preferência como validação técnica. Conferir fonte vigente antes de concluir.
- Banheiro: frente removível, correr, torneira/cuba e manutenção; iluminação L02 com perfil, dissipação, fontes e terminais. Varal: curso, retenção e envelope nominal.

**Pronto quando:** cada interface tem desenho ou instrução objetiva, fonte e teste necessário. Nada continua apenas como “validar montagem”. Falta de dados precisa indicar qual dado e quem pode fornecê-lo.

### T06 — Acabamentos, iluminação e equipamentos | P1 | 28–29/10

- Consolidar códigos de chapa, substrato, espessura, duas faces, bordas e veios; separar seleção comercial de confirmação por amostra.
- Preservar escolhas já feitas, inclusive Arauco Beige Matt/Louro Freijó Poro no banheiro e Branco TX interno. Resolver código do marfim e demais itens efetivamente pendentes.
- Completar conjuntos de iluminação: luminária, lâmpada/fita, perfil, fonte, comando e acesso. Reaproveitar a seleção L02 e a revisão CB02 do quarto.
- Preparar lista de equipamentos com modelo, medidas, alimentação e acesso de manutenção, sem reabrir comparações encerradas.

**Pronto quando:** não há componentes indispensáveis omitidos; amostras e confirmação em campo aparecem como condições específicas. Posições executivas e dimensionamento de instalações seguem para revisão profissional.

### T07 — Orçamento e pacote para cotação | P1 | 29/10

**Avanço25/10:** [quantitativos separados das sete propostas](../04_Moveis/Quantitativos/README.md),36 registros/11 substituições lidos dos BREP gravados. Área completa de fabricação, incremento líquido e massa hipotética separados; orçamento/lista-base preservados. FundoP01 atual/proposto não cabe em2750×1850; formato maior publicado em ficha de linha depende de padrão/faces/fornecimento. Nenhuma emenda automática ou quantidade de chapas de compra inferida pela área.

- Consolidar a composição com os quantitativos resultantes de T03–T06. Usar a reconciliação de ferragens existente; incorporar Blum/calços/limitadores, Minifix e banco/cesto sem duplicar verbas.
- Desdobrar a iluminação L02 nas linhas correspondentes; não somar seu total novamente ao orçamento.
- Manter três colunas separadas: estimativa atual, meta de negociação e preço efetivamente cotado, com data, frete, montagem e exclusões.
- Preservar o teto registrado de **R$120 mil de execução + R$10 mil de reserva** e tratar os **R$35 mil de marcenaria como meta**. O resumo atual registra cerca de R$137,8 mil de execução; o fechamento desta semana precisa reconciliar os itens, sem transformar descontos desejados em economia obtida.
- Atualizar o pacote de cotação já existente e a tabela para comparar propostas de mesmo escopo. Preparação não retira automaticamente o pacote da espera nem envia solicitações.

**Pronto quando:** totais reproduzíveis, escopo completo, diferenças explicadas e pendências comerciais visíveis. Retorno de fornecedor não é condição para terminar a organização do orçamento.

### T08 — Dossiê para o profissional e para as chaves | P1 | 29–30/10

- Reaproveitar programa, planta mobiliada, planta preliminar de pontos, caderno de pranchas, rascunho de reforma e roteiro de medição.
- Atualizar somente o que mudou; acrescentar as vistas e detalhes necessários para entender o projeto vigente.
- Preparar uma lista curta de questões para o responsável técnico: instalações, fixações, documentação da reforma e validações que dependem dele.
- Relacionar cada medida a levantar aos móveis/documentos afetados, para que a atualização após as chaves seja localizada.

**Pronto quando:** um profissional consegue identificar o escopo, decisões, hipóteses e o que deve conferir. Contratação, assinatura, aprovação e medição não são resultados presumidos da IA.

### T09 — Integração e continuidade com menos IA | P0 | 30–31/10

**Fechamento25/10,07h:** janela noturna encerrada e automação pausada, com confirmação e registro. R51 completa preservada; estudos, matriz dos20 móveis, dados e quantitativos separados entregues para continuidade. Conferência final/cópia local pelo roteiro abaixo, sem transformar condições de produto/oficina/ensaio em itens concluídos.

**Preparação25/10:** entrada curta de retomada e manifesto/checagem leve, sem reabrirCAD ou recalcular placas. O snapshot inicial conferiu227 arquivos,5833 objetos/7702 expressões persistidasR51 e hashR50 histórico; atualizar somente após alterações conhecidas. Fechamento desta janela e pausa às07h no registro específico, sem declarar integração das propostas ao modelo/pacote publicado.

**Avanço25/10:** [cinemática para cálculos sem abrir o FreeCAD](../ferramentas/cinematica/README.md) criada e validada contra528 poses nativas. Fotografia de867 células/24 folhas;22 visíveis na consulta normal. Recalcular522 CG leva cerca0,05 s localmente após carregar dados, sem alterar a R51. Facilita próximos estudos com menos IA; não substitui verificação de geometria/ferragens reais.

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

O plano original organizava sessões iniciadas pelo usuário. A execução encerrada às07:00 de25/10 está registrada no controle específico. Essa autorização não agenda o restante da semana; novas etapas seguem as instruções atuais do projeto.

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

- [ ] 20/20 móveis revisados na matriz, com pendência e próxima ação claras.
- [ ] Cinco frentes de carga prioritárias documentadas: P11, P15, P04, P01 e P20; registrar quais ficaram condicionadas.
- [ ] Todos os contatos inventariados classificados; informar quantos têm solução, quantos foram incorporados e quantos continuam sem detalhamento.
- [ ] Banco e cesto com montagem nominal e roteiro de ensaio; resultados físicos identificados como feitos ou pendentes.
- [ ] Gavetas e interfaces críticas conferidas; correções R48/R49 preservadas.
- [ ] Materiais, equipamentos e iluminação com lista de componentes e condições restantes.
- [ ] Quantitativos e orçamento reconciliados, ou divergências remanescentes explicitamente listadas.
- [ ] CAD, fichas, pranchas e pacote identificados por um manifesto de versões consistente.
- [ ] Modelo e pacote reabertos; links e verificações pertinentes aprovados ou falhas registradas.
- [ ] Retomada curta, scripts e cópia de segurança disponíveis.

**Entrega essencial:** eliminar ambiguidades sobre o que vale, concluir o maior número possível de decisões técnicas complexas e deixar as pendências reproduzíveis. **Entrega ampliada:** todos os lotes de ligações detalhados, dossiê completo e melhorias pontuais de consulta, desde que a entrega essencial esteja estável.

## 8. Continuidade após 31/10

Após 31/10, usar sessões curtas para incorporar respostas de fornecedores, comparar propostas pelo quadro pronto, registrar amostras, acompanhar protótipos e aplicar correções localizadas. Depois das chaves, preencher o levantamento e atualizar os documentos afetados.

Continuam dependentes de terceiros ou do imóvel: capacidade demonstrada em ensaios, preços e prazos contratados, responsável técnico, aprovações, medidas finais e liberação de fabricação. Esses itens devem sair desta semana com pergunta, desenho, formulário ou teste já preparado.

## 9. Controle diário

Preencher ao encerrar cada dia. “Concluído” exige o critério de aceite da tarefa; revisão sem evidência fica “em andamento”.

| Data | Resultado e arquivo | Verificação | Bloqueio e responsável | Primeira ação seguinte |
|---|---|---|---|---|
| 24/10 | Plano de execução criado | Links locais e estrutura conferidos na entrega | Execução técnica ainda planejada | T01 e consolidação das conclusões P11 |
| 25/10 | Entregas e retomada da madrugada: R51, cargas/ligacoes, banco/cesto, bancada/gavetas, quantitativos separados e matriz dos20moveis | Conferencias nativas/numericas por frente, source R51/R50 preservadas,5833objetos/7702expressoes e manifesto de integridade | Caixa/juntas/material/produto/prototipo e revisao das propostas visiveis; parede/piso reais depois das chaves. Janela ate07h | Priorizar caixaP01/P03, composicaoP15 e tampo/ligacoes da bancada; usar perguntas e evidencias prontas |
| 26/10 | A preencher | A preencher | A preencher | A preencher |
| 27/10 | A preencher | A preencher | A preencher | A preencher |
| 28/10 | A preencher | A preencher | A preencher | A preencher |
| 29/10 | A preencher | A preencher | A preencher | A preencher |
| 30/10 | A preencher | A preencher | A preencher | A preencher |
| 31/10 | A preencher | A preencher | A preencher | A preencher |

Referências complementares: continuidade antes das chaves, [roteiro para projeto oficial](../01_Programa_e_decisoes/Roteiro_para_projeto_oficial.md), [orçamento e atualizações](../05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md), [cronograma da obra após as chaves](../05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md) e [verificação de consistência existente](../ferramentas/Verificacao_consistencia.md). Referências históricas devem ser lidas junto às atualizações mais recentes.
