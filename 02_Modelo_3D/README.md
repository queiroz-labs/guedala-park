# Modelo 3D (FreeCAD)

Modelo vigente: **R52**, [Guedala_Park_R52_Corrigido.FCStd](Guedala_Park_R52_Corrigido.FCStd) (19,8 MB, 5.832 objetos, 7.702 expressões, 1.487 formas nativas). SHA256 em [ferramentas/site/current_release.json](../ferramentas/site/current_release.json). É o único `.FCStd` permitido nesta pasta.

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
| Pcurva | `MontagemG2R020`, frente da G2 | `GeomAbs_C0` e `InvalidCurveOnSurface`; ressalva para novas operações geométricas |
| Conferência | `MontagemG2R019`, fundo da G2 | `GeomAbs_C0`; conferir o BRep antes de operações geométricas |
| Conferência | `ReguaInferiorBaixaR31`, `ReguaInferiorAltaR31`, `ReguaSuperiorBaixaR31`, `ReguaSuperiorAltaR31` | `GeomAbs_C0`; conferir as quatro réguas antes de operações geométricas |

`GeomAbs_C0` sozinho é um alerta de continuidade para o algoritmo BOP, não prova de chapa fisicamente defeituosa. `InvalidCurveOnSurface` é uma pendência geométrica adicional. Travas, corpos de dobradiças e a grelha inferior também apresentam alertas BOP; não foram confundidos com os painéis de corte. A triagem não repara ou libera fabricação.

A verificação completa registrada passou com 5.832 objetos e 106 cenários de movimento. A base vigente registra zero peças inválidas e 12 contêineres informativos; isso não equivale a aprovação BOP. A triagem não recalculou nem salvou; o verificador completo aplicou e restaurou os movimentos apenas em memória. Esta correção documental não abriu nem alterou o `.FCStd` e não atualizou a base.

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

## Arquivos desta pasta

| Arquivo | Para quê |
|---|---|
| `Verificacao_R52.json`, `Verificacao_posicoes_R52.json`, `Auditoria_estatica_R52.json` | Evidências do arquivo vigente |
| `Comparacao_colisoes_R51_R52.json` | Colisões antes e depois |
| `Preservacao_originais.json`, `Registro_entrega_R52.json` | Rastreabilidade da entrega |
| `Historico/` | Estudos R46–R49 que o site ainda referencia |
| `Componentes/` | Ferragens, STEP e estudos de origem (grande; buscas o ignoram) |
