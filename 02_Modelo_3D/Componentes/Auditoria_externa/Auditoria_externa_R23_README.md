# Auditoria externa de ferragens — quatro folhas alteradas na R18, base R23

A lacuna externa das ferragens das quatro folhas alteradas foi conferida em processo separado `FreeCADCmd.exe` 1.1.4, sem interface gráfica e sem salvar documentos CAD. O arquivo vigente continua sendo a R23. A auditoria completou seu escopo amostrado em 48,812 s, sem contato de volume superior a **0,1 mm³** e sem exceções booleanas. Esse valor é um critério de triagem do modelo, não uma tolerância certificada.

O SHA-256 da R23 antes e depois permaneceu `cf515686f48057c3b9e025bee28f3ddac735ea73608e401133e5fc842a972eea`. Nenhuma revisão, pose salva, hierarquia, propriedade ou fonte STEP foi alterada.

## Escopo efetivamente calculado

| Folha interna | Identificação física atual, após reflexão | Apoio próprio identificado |
|---|---|---|
| FolhaEscritorioR001 | Escritório porta 3, abrir à esquerda | ApoioOpostoR18 |
| FolhaEscritorioR003 | Escritório porta 1, abrir à esquerda | Peca385 |
| Folha001 | Cabeceira porta 3, abrir à esquerda | ApoioOpostoR001 |
| VizinhaComumR18 | Cabeceira porta 1, abrir à esquerda | ApoioOpostoR002 |

Cada folha possui duas dobradiças com cinco corpos e um calço por nível. Foram calculados os encontros desses 12 sólidos com **235 alvos estacionários explicitamente listados**, as oito frentes finais com canecos e as duas frentes vigentes do canto R04. Os alvos estacionários são as caixas selecionadas previamente no `Dados_plano_R18.json` e os resultados atuais adicionais `PlacaL`, `PlacaL001`, fundos e lateral do canto. Esses 235 alvos separam-se em **234 participantes vigentes e um histórico adicional conservador**, `DivisorApoioVizinhaR03`, herdado da exportação inicial. Esse divisor aposentado não é peça atual: sua inclusão não produziu contatos e não reduz a cobertura das peças vigentes. Os testes não foram repetidos por esse extra. Operandos de base/tampo em L não foram acrescentados.

`FaixaFixaEstudo` foi incluída exatamente como salva e confirmada pelo responsável: 7 × 18 × 272 mm, em `(1775,40,18)` no módulo da cabeceira. A expressão documental “faixa 25” não substituiu esse sólido nem autorizou mudanças.

As 16 poses individuais foram 0°, 30°, 60° e 86° para cada uma das quatro folhas, com demais folhas e canto fechados. Outras 12 situações avaliaram essas mesmas quatro folhas com vizinhas e canto em 30°, 60° e 86°. Três conjuntos de verificações adicionais cobriram ferragens pertencentes a **folhas distintas**, em 14 pares de folhas por posição, sempre com pelo menos uma folha alterada envolvida. Não houve verificação de contatos entre corpos da mesma dobradiça.

| Método / resultado | Quantidade |
|---|---:|
| Pares candidatos de sólidos | 88.368 |
| Pares afastados pelo BBox conservador | 88.112 |
| Interseções booleanas efetivamente calculadas | 256 |
| Contatos acima de 0,1 mm³ — interface de montagem própria | 0 |
| Contatos acima de 0,1 mm³ — obstáculo ou vizinha | 0 |
| Exceções booleanas | 0 |

O BBox utiliza epsilon de 0,000001 mm para descartar somente sobreposição volumétrica desprezível no teste preliminar. Os pares não descartados passam por `Shape.common()`. A frente própria e o apoio correspondente são classificados como interface de montagem, de modo que um eventual contato não seria automaticamente chamado de falha de giro. Não apareceram contatos acima do limiar em nenhuma das categorias.

## Complemento: ângulos independentes das ferragens vizinhas

A auditoria acima avaliava os encontros metal-metal com ângulos iguais em cada par. Para cobrir a independência dos controles, um complemento separado conferiu **somente ferragens de folhas distintas**, nos mesmos 14 pares pertinentes, em todas as **12 combinações de ângulos diferentes** entre 0°, 30°, 60° e 86°. Assim, foram acrescentadas 168 situações, incluindo uma folha fechada com a vizinha aberta. As diagonais já prontas não foram repetidas.

O complemento terminou em **18,594 s**, dentro do orçamento de 120 s. Todos os **24.192 pares de sólidos** ficaram afastados pelo BBox conservador com epsilon de 0,000001 mm; nenhum precisou de booleano, nenhum contato acima de 0,1 mm³ foi registrado e nenhum erro ocorreu. O SHA da R23 permaneceu igual. Madeira, frentes, intraferragem, SAT e validações anteriores não foram recalculados.

O script armazenou em memória a forma de cada conjunto metálico em cada um dos quatro ângulos e combinou essas poses independentes. Isso evitou um recálculo completo do documento para cada par de ângulos. A amostragem não comprova todos os ângulos intermediários ou tolerâncias reais.

## Validação do processo isolado

O primeiro teste demonstrou `GuiUp=False`, abertura da R23 com 5.895 objetos, corpo de ferragem válido e volume conhecido de interseção de duas caixas de 1 mm³. O console em modo seguro emitiu avisos de cache temporário do sandbox, mas abriu sólidos e documentos. A conferência adicional do recálculo isolado concordou exatamente com os pontos das quatro frentes nas poses nativas já exportadas em 0°, 30° e 86°: diferença máxima **0 mm**. Os resíduos máximos dos eixos e canecos foram **6,44 × 10⁻¹³ mm**; nenhuma expressão ficou inválida e os corpos possuíam volume positivo. Essa comparação valida o runtime usado, sem refazer a varredura SAT nem booleanos antigos.

Um controle adicional de qualidade verificou **365 formas únicas em sua pose salva 0°**: corpos/calços participantes, alvos estacionários e frentes, incluindo as ferragens das vizinhas e do canto usadas nos pares de folhas distintas. Todas foram não vazias, válidas, com pelo menos um sólido e volume positivo. A contagem distingue 364 participantes vigentes e o divisor histórico conservador acima. Não houve novas poses, booleanos ou salvamento nessa verificação, e o SHA da R23 permaneceu idêntico.

Os sólidos foram avaliados no referencial-fonte preservado da R23, usando `getGlobalPlacement()`. O espelhamento comum `Xnovo=7400−Xbase` é uma isometria e conserva os encontros entre as peças igualmente transformadas. Não foi necessário booleano em cópias refletidas, mudança de parâmetros ou reparentamento.

## Limites e pendências preservados

O resultado fecha a **auditoria externa amostrada acima**, não comprova todas as posições contínuas, todas as tolerâncias reais, resistência, carga, fixação, furos, parafusos, regulagem, ferramenta, acesso de montagem ou batente. O estudo em 86° continua sem comprovar o limitador mecânico 70T3553. Os contatos internos já desconhecidos dos STEP permanecem fora desta auditoria e não foram reinterpretados. Nenhuma alteração para eliminar material ou contatos foi feita ou proposta automaticamente.

Não foram repetidos SAT de frentes, testes de bandejas/gavetas, reaberturas anteriores ou poses prontas como novos resultados. Não houve fabricação, corte, furação, compra, instalação de dependências, contato com fornecedores ou alteração de automações.

## Evidências e reprodução

- `Viabilidade_runtime.json` e `../../../ferramentas/componentes/Auditoria_externa/probe_runtime.py`: teste do console isolado.
- `Escopo_objetos.json` e `../../../ferramentas/componentes/Auditoria_externa/inspect_scope.py`: inspeção limitada dos filhos atuais dos módulos.
- `Auditoria_externa_R23.json`: manifesto completo, 31 registros de situações/conjuntos, contadores, contatos e hashes.
- `../../../ferramentas/componentes/Auditoria_externa/auditar_externo.py`: auditoria somente em memória, com orçamento de 300 s e relatório parcial entre booleanos; terminou antes desse limite.
- `Validacao_runtime_poses.json` e `../../../ferramentas/componentes/Auditoria_externa/confirmar_poses_console.py`: concordância com as poses nativas existentes, matrizes dos corpos e hashes.
- `Shape_validacao_R23.json` e `../../../ferramentas/componentes/Auditoria_externa/validar_shapes.py`: não nulidade, validade, número de sólidos e volume das 365 formas únicas, somente em pose salva 0°.
- `Complemento_angulos_independentes_R23.json` e `../../../ferramentas/componentes/Auditoria_externa/complementar_angulos.py`: 168 combinações com ângulos diferentes para metal-metal dos mesmos 14 pares pertinentes.

O comando utilizado foi `FreeCADCmd.exe --safe-mode -u probe_user.cfg -s probe_system.cfg auditar_externo.py`, com caminhos absolutos desta pasta. Os scripts gravam somente relatórios aqui, chamam `App.closeDocument()` e não chamam `save()`/`saveAs()` em nenhum documento.
