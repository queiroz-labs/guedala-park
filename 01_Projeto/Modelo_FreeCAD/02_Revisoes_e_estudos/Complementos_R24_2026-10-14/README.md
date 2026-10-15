# Complementos restritos — bandejas G2 e sofá corrigido R24

Foram fechadas três lacunas concretas de cobertura, usando a R24 salva e preservando suas fontes, programa, controles e dimensões. Os cálculos foram feitos em FreeCADCmd privado, sem interface e sem salvar CAD.

## 1. Retirada carregada das duas bandejas G2 contra arquitetura

A operação usou **Gaveta005 aberta em500 mm**, exatamente como em `Montagem_R07_2026-10-14/conferir_percursos.py`. Para cada bandeja, os três segmentos foram:

1. Elevar120 mm.
2. Avançar40 mm, delta local `(0,−40,0)`.
3. Elevar mais100 mm.

Os19 resultados sólidos atuais de bandejas/programa foram selecionados por ancestral geométrico da respectiva bandeja, preservando os nove gabaritos de utensílios/panela. As envoltórias dos segmentos foram construídas a partir dos BBox de início/fim, cobrindo a translação linear inteira. A caixa permaneceu aberta; guias MOVENTO não foram traduzidas como mecanismo.

**2.052 pares de envoltórias contra27 paredes inteiras e nove pisos ficaram separados pelo BBox.** Nenhum booleano foi necessário e nenhum contato foi encontrado. O interior/bancada já conferidos anteriormente não foram recalculados. Esta prova de envelope não valida mãos, alças, carga, flexão ou objetos físicos diferentes dos gabaritos.

## 2. Duas gavetas do escritório contra o sofá diário corrigido

As expressões atuais de `Gaveta008` e `Gaveta009` são `.Placement.Base.y = 0 mm − Extensao`. A rotação fixa do módulo inverte essa direção local; o deslocamento global de0 a400 mm é **`(0,+400,0)`**. As matrizes de rotação permaneceram fixas e todos os16 sólidos móveis acompanharam a mesma translação, conforme registros no JSON.

As envoltórias contínuas de cada peça em0–400 foram cruzadas somente com as **cinco primitivas atuais do sofá diário**, Peca122–Peca126. Os dois volumes de hóspede ocultos não foram reapresentados como peças atuais. **80 pares ficaram afastados pelo BBox**, sem booleanos ou contatos. Não foram repetidas as160 poses anteriores, nem incluídas cadeira, pessoa ou conversão do sofá para cama.

## 3. Separação vertical do aéreo e suas ferragens

As quatro frentes e48 corpos/calços do aéreo do escritório totalizam **52 resultados móveis**. A conferência das cadeias geométricas mostrou que:

- Todas as translações dependentes do movimento são horizontais após a rotação dos pais.
- Todos os eixos de rotação dependentes do movimento são verticais no referencial global.
- A composição desses movimentos conserva o intervalo Z, sem necessidade de repetir173 poses.

O intervalo conservador das formas é **Z1921–2469 mm**, enquanto as cinco peças do sofá diário têm **Zmáximo820 mm**. Há, portanto, **1101 mm de separação vertical invariável no modelo atual**, suficientes para afastar esse encontro independentemente do ângulo das folhas. Essa é uma prova restrita ao encontro aéreo×sofá atual; não comprova parede, pessoa, cadeira, sofá-cama preparado ou ferragens reais.

## Evidência, preservação e limites

[Complementos_R24.json](Complementos_R24.json) contém as seis rotas, nomes e BBox varridos de cada peça, expressões/direções das gavetas, matrizes, cadeias e eixos da prova vertical. Total dos cruzamentos novos: **2132 pares afastados por BBox, zero booleanos necessários, zero resultados inconclusivos ou erros booleanos**. Tempo combinado dos dois processos:7,124 s.

O SHA da R24 antes/depois permaneceu `b2382d8a66045e430a3bd21e54c60e00406f9949c3ad47428449be4362dd04f9`. Nenhuma revisão CAD ou mudança de exibição foi criada. As trajetórias antigas prontas e a auditoria estática não foram repetidas.

A primeira execução completou as seis rotas das bandejas e parou numa validação de nome de expressão: o FreeCAD usa `.Placement.Base.y`, com ponto inicial. O guard foi corrigido normalizando esse ponto. `continuar_sofa.py` reaproveitou as seis rotas concluídas, sem refazê-las, e executou somente os dois complementos restantes. O JSON registra essa retomada.

O BBox usa epsilon0,000001 mm; contatos volumétricos acima de0,1 mm³ seriam triados. Uma sobreposição de envoltórias conservadoras seria registrada como **inconclusiva**, sem afirmar colisão real ou apagar material automaticamente. Não ocorreu tal sobreposição.

Estas provas são dos gabaritos e movimentos rígidos documentados, não validação de tolerâncias, carga, fixação, telescópio, mão/pega, conforto, batentes ou fabricação. O teto permanece sem sólido modelado e não foi conferido. Sem corte, furação, compra ou contato com fornecedores.

Scripts e relatórios desta pasta documentam trabalho já concluído; não executar novamente para preencher o prazo.
