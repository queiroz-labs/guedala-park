# Plano de cargas, flexão e ligações — R00

24/10/2026. Planejamento solicitado por Elias, a partir da R49 publicada. O plano original organiza a execução; o andamento está registrado abaixo.

**Atualização vigente de25/10:** Elias rejeitou tubos sustentando chapas em todo o projeto; qualquer proposta futura exige autorização prévia. A R51 retirou o estudo tubular oculto da bancada. A continuação está em [ligações e reforços de marcenaria sem tubos](../Solucoes_marcenaria_sem_tubos_2026-10-25/README.md), com P15/P04 em estudos separados,15 verificações numéricas e14 contatos de face conferidos. Não desenvolver os terminais da alternativa tubular P15 cancelada. P01_723 e P11 sem tubos preservados. [Execução autorizada até07h](../Execucao_ate_07h_2026-10-25.md).

## Andamento — primeira frente P11

**Decisão e cálculo vigentes:** Elias escolheu **P11 sem tubos**, preservando a chapa de 18 mm. O [estudo das ligações R00](../P11_ligacoes_sem_tubos_2026-10-24/Resultado_R00.md) propõe manter os quatro Minifix da prateleira, acrescentar quatro Confirmat e três cavilhas ao fundo e dimensionar os dois grupos fundo–laterais. A meta calculada é **10 kg distribuídos**, ainda condicionada a chapa, rigidez/resistência das juntas, compatibilização e prova de oficina. Não há carga do móvel liberada nem alterações no CAD. O estudo anterior dos tubos fica fora da solução selecionada.

**Executado em 24/10/2026:** [cálculo P11 R00](../Calculo_P11_2026-10-24/Resultado.md), com geometria nominal reconciliada na R49, reprodução histórica, cenários de material/carga, deformação imediata e diferida por sensibilidade, tensões brutas, reações e comparação de alternativas. Fórmulas conferidas por segundo agente e por 48 casos numéricos, mais dois casos mistos.

**Resultado histórico da chapa apoiada só nas laterais:** a referência condicional de 18 mm chega a 2,68 mm imediatos / 5,35 mm no cenário sustentado com 20 kg distribuídos, frente ao critério escolhido de 2,20 mm. As metas anteriores de 5 kg distribuídos ou 3 kg centrais pertencem a essa triagem. O estudo vigente inclui as ligações ao fundo e propõe 10 kg distribuídos, conforme indicado acima; 20 kg continuam excedendo o critério.

**P11 continua condicionado:** chapa real e espessura resistente, resposta local e furos, comprovação das juntas/fundo, suspensão e prova de oficina. Os três contatos têm agora mapa nominal e solicitações calculadas, com propriedades das juntas ainda a demonstrar; a furação não foi executada no CAD.

**Avanço em 25/10, base R50:** executado o [primeiro ciclo P15/P04/P01/P20](../Cargas_e_ligacoes_R50_2026-10-25/README.md), com memórias reproduzíveis e11 verificações numéricas. Os146 contatos da fila foram conferidos, além de26 conferências direcionadas que incluem P02 e tampas atuais do banco. Criado estudo P01 separado com duas prateleiras723×550×18 sobre as divisórias existentes; quatro faces de apoio verificadas. P15 recebeu comparação de duas seções externas e demandas de terminais; P04 teve vãos e caminhos de tração reconciliados; varões e momentos das tampas foram calculados. A R50 principal permanece intacta. Juntas, deformação da caixa, mecanismos e suspensão ainda exigem desenvolvimento; não há nova carga de uso liberada.

**Histórico não selecionado:** [dimensionamento com tubos R00](../Reforco_P11_2026-10-24/Dimensionamento_R00.md), substituído pela decisão acima. Os seis conjuntos de apoio daquela alternativa não integram os quantitativos ativos nem foram cortados na R49.

## Base e escopo conferidos

- Modelo de partida: [FreeCAD R49](../Gavetas_escritorio_R49_2026-10-24/README.md), commit 5dc38d4. Site/documentos: commit ea2bc21.
- Preservar as correções P16 da R49 e o divisor de 312 mm do P09, atualizado na R48.
- O mapa atual de ligações tem **146 contatos sem mapa em 15 móveis**, incluindo 1 do P14. P01 tem 33; P04, P17 e P20 têm 19 cada. A referência a14 móveis não corresponde à contagem do JSON vigente.
- Os 146 são uma fila documental preliminar. Reconciliar com os sólidos ativos da R49 antes de dimensionar. A amostra de contatos retangulares é parcial: **P02 exige ligações mesmo aparecendo com zero contatos** nessa amostra.
- Há 52 conjuntos Minifix com posições nominais já documentadas em P10/P11/P15/P19. Isso não significa52 uniões distintas nem52 furações executadas no CAD; conferir geometria, marcadores e operações existentes antes de acrescentar peças.
- O [Mapa de conectores R00](../Mapa_conectores_R00/README.md) propõe quantidades para 80 encontros de P01/P04/P12/P17. Reaproveitar como estimativa de cotação, não como distribuição resistente aprovada ou programa de usinagem.

**Decisões preservadas:** armazenamento e faces aparentes; base P15 sem divisória intermediária; duas tampas presas no P20, almofadas retiradas para abrir, piano + articuladores com trava como direção atual. Não voltar automaticamente à Southco, baixar prateleiras ou engrossar divisórias para acomodar ferragens.

## Sequência de trabalho

### 0 — Fixar a base e reconciliar o inventário

1. Registrar o SHA256 da R49 e manter uma cópia original intacta.
2. Extrair peças ativas, materiais, espessuras resistentes, volumes, eixos locais e contatos. Separar chapas, ferragens, conteúdo, reservas e frentes móveis.
3. Comparar com as 146 linhas existentes, dando atenção ao novo encontro do divisor P09 com o fundo. Completar contornos em L do P02 e apoios do banco que a amostra retangular não cobre.
4. Distinguir por ligação: só família escolhida / quantidade proposta / posição nominal / marcador CAD / furo e conector modelados / prova de oficina.
5. Criar uma matriz única: ID de ligação, móvel, duas peças, face de referência, caminho da carga, conector, quantidade, posição, acesso de ferramenta e situação.

**Entrega:** inventário reconciliado, lista de diferenças e mapa de dependências. As contagens atuais estão em [Contatos_sem_mapa_base_R14.csv](Contatos_sem_mapa_base_R14.csv) e [Inventario_do_plano.json](Inventario_do_plano.json).

### 1 — Cálculos de carga e flexão

Começar por P11 para conferir o método e reaproveitá-lo em P15/P04; concluir P01 e o primeiro ciclo do P20 antes da furação dependente dessas verificações.

| Frente | Casos a avaliar | Resultado esperado |
|---|---|---|
| **P11 — prateleira 661 × 312 × 18 mm** | Peso próprio + cenários de 5/10/20 kg de conteúdo; distribuição uniforme e concentração compatível com objetos reais. Laterais como apoio inicial; fundo só contribui quando sua ligação for demonstrada. | Curva carga × flecha imediata/ao longo do tempo; verificações da chapa e uniões; carga de uso proposta ou reforço necessário. |
| **P15 — base 799 × 312 × 18 mm** | **Meta de 20 kg de conteúdo total**, somada ao peso próprio. Comparar base nas laterais, reforço e ligação estrutural ao fundo/suspensão, mantendo o vão sem divisória. Registrar também efeito de conteúdo concentrado. | Solução que atenda à meta com dimensões e fixações do reforço; se inviável no espaço, demonstrar a restrição antes de propor concessão. |
| **P04 — vão 851,5 mm** | Conferir o vão estrutural efetivo e a função das divisórias. Comparar5/10/20 kg no trecho maior como cenários, sem aprovar20 kg por compartimento. Incluir fundo, reforço e suspensão quando dimensionados. | Carga proposta por trecho, flecha, reação nas ligações e seção de reforço; não tratar425,75/407,75/851,5 como vãos iguais. |
| **P01 — varões e prateleiras** | Listar cada prateleira e seu apoio real. Para varões, vãos nominais 973 e332 mm, seção tubular e suportes comerciais, distribuição de roupas e hipóteses de concentração. Avaliar apoio central nos longos. | Carga por prateleira/varão e por suporte; rigidez do tubo separada da resistência dos terminais/parafusos no MDF. Desenhar o apoio central somente se seu encaixe e caminho de carga couberem. |
| **P20 — tampas e mecanismo** | Cada tampa separada:971 × 448 × 20 e825 × 448 × 20 mm. Calcular massa, centro de gravidade e momento com o conjunto móvel real; repetir após o desenho final da piano/suportes. | Tabela massa/CG por componente, curva de momento e esforço na pega ao longo da abertura; reações no eixo, trava e apoios, com limites e casos assimétricos. |

**Premissas a fechar tecnicamente:** composição e espessura resistente da chapa, densidade, rigidez, resistência e comportamento no tempo/umidade; material/seção dos varões; carga e posição de conteúdo; critérios de flecha e margens de projeto com suas fontes. Se o produto ainda não estiver escolhido, calcular sensibilidade e requisitos mínimos para a compra, sem apresentar hipótese como propriedade garantida.

Para cada caso, distinguir:
- peso próprio e conteúdo;
- carga distribuída, localizada e situações assimétricas pertinentes;
- flexão imediata, deformação ao longo do tempo e resistência;
- resistência da chapa, apoio, conector e parafuso;
- resultado do cálculo, condição de catálogo e prova física pendente.

A carga proposta deve respeitar o elemento limitante do conjunto. Não usar a capacidade publicada de um suporte como capacidade da chapa ou da parede.

**Ponto de partida existente, não capacidade aprovada:** o estudo anterior estimou 2,639 mm no P11 e4,779 mm no P15 para 20 kg de conteúdo mais peso próprio, com E = 2100 MPa e densidade 750 kg/m³ assumidos, apoio simples e sem fluência. Usar para conferir a reprodução daquele cenário; substituir premissas pelos dados adequados antes de concluir. L/300 foi referência comparativa do estudo, não norma de aprovação.

**Detalhe do P20:** distinguir folha fixa e folha móvel da piano; partes móveis dos articuladores mudam de posição ao abrir. Não colocar a massa de toda a ferragem no centro da tampa. Parafusos, revestimentos, calços e batentes entram conforme sejam fixos ou móveis. A almofada fica fora do caso normal de abertura, pois é retirada antes. Considerar travamento, liberação, retorno e reação desigual entre lados. Não dividir esforço por dois sem justificativa.

A carga de pessoas no assento fechado percorre tampas → apoios → corpo do banco. Piano e articuladores retêm/articulam a tampa aberta: não lhes atribuir automaticamente a carga de assento. O estudo histórico de carga do banco não é aprovação do conjunto atual.

**Entrega:** memória reproduzível, tabela por peça, diagramas dos apoios, casos limitantes e decisão de reforço. Toda variável terá unidade, origem e situação (medida, catálogo ou hipótese).

### 2 — Definir as ligações e a suspensão, antes de furar

- Aproveitar famílias e códigos já escolhidos nas fichas; não espalhar automaticamente Confirmat 7 × 50 para qualquer espessura ou tipo de peça.
- Para P01/P04/P12/P17, resolver **em conjunto os dois lados das divisórias 18 mm**: centros, diâmetros, profundidades, ponta da broca, tolerâncias e acesso de montagem. Não adotar um desencontro arbitrário único para todos os encontros.
- Conferir divisórias duplas36 mm separadamente. Sua existência não autoriza repetir a mesma solução nas divisórias 18 mm.
- Para cada armário alto, demonstrar caminho conteúdo → chapa → ligações → caixa → ferragem de suspensão → parede, com peso próprio, portas e conteúdo. Calcular esforços na interface com a parede; a ancoragem final depende do substrato real.
- Priorizar a estratégia de suspensão interna acessível que preserve a posição da caixa. A HettichSAH215 pesquisada exige rebaixo posterior16 mm inexistente; não a inserir como se coubesse nem afastar o armário sem compatibilizar.
- Reservar zonas de regulagem, montagem e manutenção. Furos finais da parede, buchas e resistência do substrato continuam dependentes do apartamento.

**Entrega:** família/código por união, quantidade justificada, seção dos reforços, ligação da ferragem ao móvel, reações na parede e sequência de montagem. O tipo de parede não impede desenvolver a caixa e seus esforços.

### 3 — Desenhar por lotes no modelo

| Lote | Móveis | Contatos da fila atual | Foco e dependência |
|---|---|---:|---|
| **A — piloto e cozinha/lavanderia** | P11, P15, P09 |14| Aplicar cálculo de prateleira/base; desenhar ligações do divisor312 mm com fundo, base e tampo; validar o procedimento de conectores e furação. |
| **B — aéreos com divisórias** | P04, P12, P17 |47| Aplicar reforço do P04, desencontro nas chapas 18 e suspensão; preservar faces e vãos úteis. |
| **C — roupeiro e canto** | P01 + P02 |33 + ligações específicas do P02| Prateleiras/varões,33 contatos do P01, contornos em L, ligação entre peças e apoio terminal do canto. Coordenar com os armários adjacentes. |
| **D — banco** | P20 |19| Apoio fixo resistente, eixo e rebaixo da piano na junta nominal2 mm, travas e ligações da caixa. Preservar armazenamento e conferir acesso para destravar. |
| **E — demais encontros** | P03, P05, P06, P07, P10, P14, P16 |33| Completar ligações remanescentes; manter as correções das gavetas R49, ventilação, manutenção e espaços de mecanismos. |
| **Conferência transversal** | P10/P11/P15/P19 e todos os suspensos |fora da soma adicional| Revisar os 52 Minifix nominais sem duplicação e conferir ferragens de parede/caixa em todos os aéreos. |

Os totais14+47+33+19+33 somam 146. São os contatos da lista atual, não a quantidade final de conectores ou furos. Recontar após a etapa0; o P02 amplia o escopo além da amostra.

**A cada lote:**
1. Inserir componentes e operações com parâmetros e IDs rastreáveis.
2. Registrar peça, face, origem local, eixo, centro, diâmetro, profundidade e referência comercial de cada operação.
3. Conferir sobreposição de furos, espessura remanescente, bordas, encaixe de conector, ferramenta e sequência de montagem.
4. Conferir colisões com portas, gavetas, conteúdo e instalações representadas. No P20, verificar percurso e posições críticas com as limitações do ensaio registradas.
5. Comparar antes/depois: somente peças previstas podem mudar; preservar aparência, posições e capacidade de guarda acordadas.
6. Salvar revisão de estudo por lote, reabrir o arquivo e produzir vistas/cortes e tabela de operações para conferência.

No P20 o desenho é iterativo: hipótese de eixo/apoio → massa/CG e esforço → geometria da montagem → recálculo → protótipo de oficina. A junta de 2 mm e o encosto de referência não são um apoio resistente resolvido. Terminais e curso da trava dependem do produto exato; não transferir a triagem do Bigfer branco para o zincado 546 mm.

### 4 — Compatibilização e entrega

- Consolidar cortes, reforços, conectores, furação nominal, sequência de montagem e quantitativos sem contar duas vezes componentes de kits.
- Atualizar primeiro as fontes das fichas; regenerar fichas, CSV, visualizador, pendências e pacote a partir da mesma revisão.
- Verificar CAD reaberto, diferenças previstas, vínculos por ID, interferências, consistência entre peça/desenho/tabela e links do pacote.
- Fazer provas em retalho das ligações e protótipo do P20 antes dos furos definitivos. Ensaios físicos não ficam marcados como concluídos por existirem sólidos no CAD.
- Encerrar cada pendência como: dimensionada e desenhada / condicionada a produto ou oficina / condicionada ao apartamento. Uma pendência não deve desaparecer só por mudar de documento.

**Fechamento esperado desta rodada futura:** capacidade proposta e flecha por elemento; reforços dimensionados; mapa individual das ligações; suportes dos aéreos desenhados no móvel; P02/P09/P20 com suas interfaces especiais; lista curta e específica do que verificar em oficina e no apartamento.

## O que depende de cada fonte

| Fonte | O que precisa fornecer |
|---|---|
| Projeto / trabalho antes das chaves | Cargas de estudo, caminhos de carga, reforços, quantidade/posição dos conectores, desencontro, suspensão na caixa, rebaixo da piano e cálculos com hipóteses explícitas. |
| Fabricante / fornecedor / oficina | Fichas do painel e ferragens exatas, espessuras e massas reais, terminais/engate, prova de furação e montagem, protótipo e ensaio. Não exige esperar o apartamento. |
| Apartamento | Material e espessura útil das paredes, resistência da ancoragem, tubos/fios, prumo/esquadro, vãos acabados e cotas finais de instalação. |

Não é necessário pedir ao usuário que escolha torque, eixo ou parafuso para começar. Se o uso exigir uma concessão de armazenamento, aparência ou funcionamento, apresentar a incompatibilidade concreta e as opções.

## Fontes locais consultadas

- [Joinery R14](../Estudo_interativo/fabrication/r14/joinery.json): contatos e estágios das ligações.
- [Revisão técnica compilada](../Estudo_interativo/fabrication/technical-r14.json): considerar as decisões atuais e a atualização do banco.
- [Matriz dimensional](../Consolidacao_R45_2026-10-23/Inventario/Matriz_20_modulos.md).
- [Sensibilidade de prateleiras](../Consolidacao_R45_2026-10-23/Inventario/Verificacoes_dimensionais.json) e [premissas do cálculo](../Consolidacao_R45_2026-10-23/Inventario/analisar.py).
- [Varões e suportes](../Consolidacao_R45_2026-10-23/Inventario/Varoes.md).
- [Ferragens fixas e suspensão](../Consolidacao_R45_2026-10-23/Inventario/Ferragens_fixas.md).
- [P09 na R48](../Depurador_sem_canal_R48_2026-10-24/README.md).
- [Banco: direção piano + trava](../Banco_cesto_simples_2026-10-23/Diretriz.md), [conferência](../Banco_cesto_simples_2026-10-23/Conferencia/Resultado.md), [peças comerciais](../Banco_cesto_simples_2026-10-23/Precos_e_conjunto_R01.md) e [apoios do assento](../Consolidacao_R45_2026-10-23/Banco_estrutura/Resultado.html).

## Estado deste plano

Plano em execução: P11 consolidado e primeiro ciclo P15/P04/P01/P20 registrado no estudo de25/10. Estudo geométrico P01 separado criado; modelo principal preservado. Não há nova carga admissível do móvel liberada, usinagem definitiva, compra, contato com fornecedor ou publicação nesta rodada. Conferir a numeração da próxima revisão antes de incorporar os estudos ao CAD completo.

