# Modelo 3D (FreeCAD)

Modelo vigente: **R53**, [Guedala_Park_R53_Decisoes.FCStd](Guedala_Park_R53_Decisoes.FCStd). Base R52 preservada no Git; propriedades e geometria verificadas no relatório abaixo. SHA256 em [ferramentas/site/current_release.json](../ferramentas/site/current_release.json). É o único `.FCStd` permitido nesta pasta.

## Decisões incorporadas na R53 — 27/10/2026

Fonte: Elias,27/10/2026: “Aplicar à R52 e às fichas as decisões já tomadas” e “crie um R53”, nesta conversa. Escopo desta revisão: P02 U1–U4=A, P13 F13=A, TV R44=A e lixeiras LIX=A.

- P02: requisito10kg de conteúdo leve ocasional, organização por zonas e preservação de vãos/aparência registrados; sem reforço ou capacidade demonstrada.
- P13/Peca350: Arenza liso nas duas faces,18mm; cor de referência já existente preservada, especificação documental nas fichas R15.
- TV: mantida nesta etapa, sem alteração geométrica ou compra.
- Lixeiras: três peças Biovis com LocalX+70mm e três Loop com LocalY+60mm. Expressões do controle de manutenção preservadas. Posições nominais, sem prova física de passagem, tampa/pedal ou destino temporário.
- Links das20 fichas corrigidos para a pasta vigente, com revisão R15 identificada no CAD.

[Alterações por objeto](Alteracoes_R53.json) · [verificação e diferenças](Relatorio_mudanca.md). Gravação pela GUI, sem modificar paleta, espessuras, portas, ferragens ou demais estudos condicionados. Armários até o teto e alternativas P03/gavetas continuam separados; esta revisão não inventa detalhes faltantes.

**Verificação completa R53:** 5.832 objetos,7.702 expressões,106 cenários; zero peças inválidas e nenhuma colisão nova. Diferenças: seis posições das lixeiras e duas formas agregadas, sem alteração de aparência. Base atualizada somente após comparação, sob o pedido expresso acima.

As seções R52 abaixo são evidência histórica da base, não nova inspeção declarada da R53.

## Triagem das formas inválidas — 25/10/2026

**Geometria própria válida: zero peças inválidas nas 1.449 conferidas por Elias em uma cópia do modelo (25/10/2026, comunicação nesta revisão).** Os 12 casos são contêineres (`App::Part` e grupos), sem forma própria gravada; o FreeCAD monta suas formas a partir dos filhos. Ferragens B-spline de fabricante, como travas e corpos de dobradiça, podem ficar inválidas nessa transformação, mesmo com determinante 1. São formas montadas inválidas, informativas, sem evidência de peças defeituosas. [Dados por objeto, fonte e ficha](Triagem_geometria.json) · [script de leitura](../ferramentas/verificar_modelo/triar_geometria.py).

Desde o commit `3cdf795`, o verificador só reprova validade geométrica de peças com geometria própria (`Part::Feature`, incluindo tipos derivados). Os 12 contêineres ficam em `agregados_invalidos`; não entram em `invalidos` ou `invalidos_novos`. A tabela registra sólidos da representação montada, com sobreposição entre níveis da hierarquia; seus números não contam peças defeituosas.

| Objeto | Sólidos com `isValid() == False` no agregado | Rastreio |
|---|---:|---|
| `Ambiente_quarto` | 6 | Agregado do quarto; consultar P01/P02 abaixo |
| `Ambiente_cozinha` | 7 | Agregado da cozinha; consultar P06/P07 abaixo |
| `ApartamentoR34` | 13 | Agregado do apartamento; incorpora os anteriores |
| `Modulo` | 2 | Duas travas T51.7601 do guarda-roupa |
| `Modulo001` | 4 | Quatro corpos das dobradiças do canto |
| `CantoSimplesR04` | 8 | Oito corpos das dobradiças do canto |
| `Modulo005` | 6 | Seis travas/acoplamentos T51.7601 das três gavetas |
| `Modulo006` | 1 | GrelhaInferiorR31 |
| `DobradicaSimplesR04` | 1 | Corpo da 71B3550, porta A, nível 51 |
| `DobradicaSimplesR001` | 1 | Corpo da 71B3550, porta A, nível 255 |
| `DobradicaSimplesR002` | 3 | Três corpos da 71B3550, porta B, nível 51 |
| `DobradicaSimplesR003` | 3 | Três corpos da 71B3550, porta B, nível 255 |

As fontes individuais rastreadas passam em `isValid()`, mas apresentam alertas em `check(True)`. A validade muda conforme a representação/transformação: por exemplo, o contêiner do canto tem oito sólidos inválidos em sua forma montada, quatro ao ser agregado em `Modulo001`. Esses resultados descrevem a representação montada e não defeitos das fontes gravadas. O JSON mantém os contextos distintos e o rastreio hierárquico pelo módulo quando necessário. Não usar o volume do contêiner como comprovação de volume de madeira, integridade de recortes ou resultado de booleanas.

**Impacto nas fichas:** 85 fontes de painéis de P01/P02/P06/P07 existem e têm `isValid() == True`. A checagem BOP foi aplicada às 32 fontes de P06/P07; 26 passaram e seis têm os alertas abaixo. As três dimensões dos 32 envelopes locais coincidem com as fichas dentro de 0,02 mm. Essa coincidência não valida recortes ou usinagem.

| Prioridade | Fonte da peça | Resultado ampliado |
|---|---|---|
| Pcurva | `MontagemG2R020`, frente da G2 | `GeomAbs_C0` e `InvalidCurveOnSurface`; ver quantificação e limites na análise abaixo |
| Conferência | `MontagemG2R019`, fundo da G2 | `GeomAbs_C0`; conferir o BRep antes de operações geométricas |
| Conferência | `ReguaInferiorBaixaR31`, `ReguaInferiorAltaR31`, `ReguaSuperiorBaixaR31`, `ReguaSuperiorAltaR31` | `GeomAbs_C0`; conferir as quatro réguas antes de operações geométricas |

`GeomAbs_C0` sozinho é um alerta de continuidade para o algoritmo BOP, não prova de chapa fisicamente defeituosa. `InvalidCurveOnSurface` é uma pendência geométrica adicional. Travas, corpos de dobradiças e a grelha inferior também apresentam alertas BOP; não foram confundidos com os painéis de corte. A triagem não repara ou libera fabricação.

A verificação completa registrada passou com 5.832 objetos e 106 cenários de movimento. A base vigente registra zero peças inválidas e 12 contêineres informativos; isso não equivale a aprovação BOP. A triagem não recalculou nem salvou; o verificador completo aplicou e restaurou os movimentos apenas em memória. Esta correção documental não abriu nem alterou o `.FCStd` e não atualizou a base.

## Análise dos alertas BOP — 25/10/2026

Escopo: operações e peças do projeto. **Os arquivos STEP recebidos e os corpos de ferragens fornecidos ficaram fora deste aprofundamento.** G2 foi checada somente na representação já incorporada ao CAD, sem abrir ou alterar sua fonte STEP. [Ensaios detalhados](Analise_bop.json) · [script](../ferramentas/verificar_modelo/analisar_bop.py).

No OCCT 7.8.1 local, `GeomAbs_C0` consulta a continuidade da curva/superfície de suporte; não significa simplesmente um encontro de faces a 90°. `InvalidCurveOnSurface` compara a curva 3D com a curva na superfície e acusa diferença maior que a tolerância da aresta. [Código oficial, testes de continuidade e de pcurva](https://github.com/Open-Cascade-SAS/OCCT/blob/V7_8_1/src/BOPAlgo/BOPAlgo_ArgumentAnalyzer.cxx#L775).

| Caso | Evidência | Interpretação e encaminhamento |
|---|---|---|
| Quatro réguas P07 e `GrelhaInferiorR31` | As cinco peças do estudo R02 passam no BOP, com planos/cilindros e linhas/círculos. Espelhar a cópia com `transformGeometry()` converte tudo em B-splines e reproduz C0; com `transformShape()` a cópia continua analítica e passa | Causa reproduzida no fluxo do projeto; não há evidência de peça fisicamente defeituosa por esse C0. Preservar a geometria analítica nas isometrias |
| `MontagemG2R019`, fundo | Apenas C0; três cortes centrais válidos, sem sobreposição dos resultados | Alerta de representação, sem falha operacional nos controles feitos; conservar a fonte recebida |
| `MontagemG2R020`, frente | C0 e `InvalidCurveOnSurface` persistem. Na amostragem das duas representações por aresta, o maior desvio foi cerca de **1,013 × 10⁻⁷ mm**, sem ultrapassar a tolerância da respectiva aresta nos pontos amostrados. Os três cortes centrais produziram formas válidas | A amostragem não reproduziu a excedência acusada pelo teste BOP e não certifica o máximo contínuo. Manter a ressalva técnica para novas booleanas; não foi demonstrado defeito dimensional de fabricação nem há fundamento aqui para mudar medidas |

Nas cinco peças P07 comparadas, fonte e representação atual, alinhadas por translação no ensaio, deram volume zero nas diferenças em ambos os sentidos. As peças são simétricas no espelhamento testado. Isso não é uma certificação geral de equivalência ou uma correção já aplicada ao CAD. A diferença do valor bruto de `Volume` foi de até **4,965 mm³** nas réguas e **0,754 mm³** na grelha; não confundir essa diferença numérica da representação com material realmente removido.

Os **18 cortes sintéticos** (plano central em X/Y/Z de cada uma das seis peças de marcenaria) retornaram interseção e diferença válidas, sem volume de sobreposição. O maior resíduo de soma de volumes foi **5,523 mm³**; o maior relativo, **0,002651%**. São controles de robustez, não trajetórias CNC nem comprovação de usinagem. `fix(1e-7, 1e-7, 1e-5)` retornou sucesso, mas manteve os alertas; `removeSplitter()` também os manteve. Ambos conservaram o volume nesta amostra.

A correção candidata para o fluxo próprio está nas cópias isométricas de [consolidar_r31.py](Componentes/Atual/Consolidacao_R31_2026-10-20/consolidar_r31.py): preservar `Placement` ou usar `transformShape()` para translações, rotações e espelhamentos, em vez da conversão geral de geometria. O ensaio isolado com o espelho passou nas cinco fontes analíticas. Isso não autoriza substituir chamadas que realmente precisem de escala não uniforme, nem executar o consolidador antigo sobre a R52.

R52, base e estudo R02 ficaram com os mesmos hashes. A verificação completa repetida passou com os 106 cenários. Nenhum reparo foi gravado no modelo.

## Abrir e salvar com segurança

- Abrir: `powershell -File 02_Modelo_3D/Abrir_no_FreeCAD.ps1` ou **Arquivo → Abrir** no FreeCAD 1.1.4.
- **Salvar só pela interface gráfica.** O `FreeCADCmd` perde o `GuiDocument.xml`, onde ficam cores e visibilidade (o verificador acusa).
- Para estudar uma alteração, grave **outro arquivo fora do projeto** e só traga para cá o que Elias aprovar. Não sobrescreva o vigente para consultar.
- Prove que nada mudou sem querer comparando assinatura geométrica (volume, área, faces, vértices, caixa, centro de massa, posição) e não `Shape.hashCode()`, que muda a cada recálculo.
- Backups `.FCBak` e cópias não ficam na pasta do projeto.

## Verificar

```
python ferramentas/verificar_modelo/verificar_modelo.py                         # segundos: arquivo, cores (GuiDocument.xml), SHA, backups esquecidos
python ferramentas/verificar_modelo/verificar_modelo.py --completo              # ~8 min: abre sem salvar e confere tudo abaixo
python ferramentas/verificar_modelo/verificar_modelo.py --completo --relatorio  # idem + escreve Relatorio_mudanca.md (aprovação PENDENTE)
```

O modo completo confere, nesta ordem:

| Trava | O que acusa |
|---|---|
| **Invariantes** (`ferramentas/verificar_modelo/invariantes.json`) | Fatos documentados quebrados: TV a 50 mm da porta, bancada 2000×700×30 com topo a 750, `Peca131.LocalY = 1180`, históricos que devem ficar ocultos, controles que devem existir |
| **Nada novo fora do apartamento** | Objeto visível que passa a ficar fora da caixa das paredes (coordenadas **globais**; peças dentro de contêineres têm coordenadas locais) |
| **Aparência por objeto** | Cor, transparência ou visibilidade trocadas em qualquer dos 5.832 objetos (lê o `GuiDocument.xml` e os materiais) |
| **106 cenários de movimento** (`movimentos.json`) | Aplica cada controle em memória (portas 45/86°, gavetas 400/500, banco, cesto, varal, forno…), recalcula, mede os contatos novos entre peças, restaura e confere que o modelo voltou ao estado inicial. Contato novo = erro. Reproduz exatamente os contatos que a R52 registrou |
| **Objetos removidos, formas inválidas, expressões perdidas, colisões novas** | Como antes; colisões por caixas globais e, nos pares suspeitos, interseção exata |

A base ([Base_verificacao.json.gz](Base_verificacao.json.gz), compactada, não se lê) guarda o retrato aprovado, incluindo os contatos que já existem de propósito (fixadores, reservas, marcadores, e as operações incompatíveis que a R52 já documenta, como abrir a gaveta com a porta fechada). Para ensinar uma regra nova, adicione em `invariantes.json` (tipos: `caixa_global`, `folga_minima`, `propriedade`, `oculto`, `existe`).

## O que o R52 corrigiu em relação à R51

TV do escritório recuada (`Peca131.LocalY` 1280 → 1180, 50 mm de folga até a porta aberta); tanque antigo e frentes alternativas 500 da lavanderia ocultos; mesa Berlin 110/170 vigente (mesa sob medida e cadeiras anteriores ocultas); controles antigos do banheiro movidos para grupo histórico (`BC43_Controle` com `CursoEsquerda`/`CursoDireita`); `Gaveta009.AlturaParedeSobreFundo` 53 → 47 mm; ferragens declaradas nas gavetas P01 (FGVTN 500) e P16 (MOVENTO 400); lista de ferragens do banco P20 (piano e articuladores com trava); seis atalhos de gaveta que renderizavam cópias fora do apartamento removidos (as gavetas reais permanecem).

Detalhe linha a linha: [Alteracoes_R52.json](Alteracoes_R52.json) · [Diferencas_R51_R52.json](Diferencas_R51_R52.json).

## Movimentos e operação

106 cenários de movimento conferidos (gavetas até 400/500, portas 45/86°, correr do banheiro, canto, cesto, banco, varal): [resumo](Verificacao_movimentos_R52.json) · [casos](Movimentos_R52.json) · [condições](Condicoes_operacao_R52.json). Abrir a gaveta do roupeiro com a folha fechada, ou o banco com as almofadas presentes, é contato esperado; faz parte da sequência de uso. Para portas e gavetas sem abrir o CAD, use `ferramentas/cinematica/consultar.py`.

## Pendências técnicas

Formato do fundo P01, divergência 100/300 mm do micro-ondas, interface guia–fundo P16, ferragens reais, ligações, suspensão, massa e estabilidade dos apoios e capacidade do banco. Os estudos ficam em [04_Moveis](../04_Moveis/README.md) e não estão incorporados ao modelo.

Os relatórios históricos em `Componentes/Estudos/` preservam os caminhos antigos das referências removidas, com aviso visível. Para rastrear essas evidências, consulte o histórico do Git e a tag `antes-reorganizacao`; os relatórios não substituem o modelo vigente.

## Arquivos desta pasta

| Arquivo | Para quê |
|---|---|
| `Verificacao_R52.json`, `Verificacao_posicoes_R52.json`, `Auditoria_estatica_R52.json` | Evidências do arquivo vigente |
| `Comparacao_colisoes_R51_R52.json` | Colisões antes e depois |
| `Preservacao_originais.json`, `Registro_entrega_R52.json` | Rastreabilidade da entrega |
| `Historico/` | Estudos R46–R49 que o site ainda referencia; os binários R45 e R48 foram removidos em 26/10/2026 (recuperáveis no git) |
| `Componentes/` | Ferragens, STEP e estudos de origem (grande; buscas o ignoram) |

## Contadores históricos para rastreabilidade

Transferidos do plano até 31/10, registro de 25/10/2026: a R50 completa otimizada preservava 5.893 objetos, 1.546 geometrias e movimentos da R49; integração local corrigida e tempos comparados. O manifesto inicial de continuidade conferiu 227 arquivos, 5.833 objetos e 7.702 expressões persistidas da R51, com hash R50 identificado como histórico. São bases de comparação anteriores, não os contadores da R52 vigente. Atualizar manifesto somente após mudanças conhecidas; esse registro não comprova integração das propostas nem publicação do pacote.
