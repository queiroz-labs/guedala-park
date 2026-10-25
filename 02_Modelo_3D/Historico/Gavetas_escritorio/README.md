# FreeCAD R49 — gavetas do escritório

24/10/2026. **[Guedala_Park_R49_Gavetas_escritorio.FCStd](Guedala_Park_R49_Gavetas_escritorio.FCStd)** parte da [R48](../Depurador_sem_canal/README.md), preservada.

## O que mudou (P16)

- **Folga sob o tampo:** a gaveta 2 tinha 1 mm entre o topo das laterais e o tampo do gaveteiro (`Peca371`); a MOVENTO pede 7 mm. Laterais `GavetaComumR084`/`R085` passam de 80 para **74 mm**; traseira `R087` e dianteira interna `R088` de 53 para **47 mm**. Corte feito no topo; base, fundo, guias e frente sem mudança. A gaveta 1 já tinha 7 mm até a guia da gaveta 2.
- **Trava direita:** a T51.7601 direita (`GavetaComumR079` e `R091`) era cópia transladada da esquerda e invadia a guia direita em 1.276 mm³ em cada gaveta. Agora é o espelho da esquerda pelo plano central da gaveta e passa a usar a mesma origem local (`LocalX` de −219 para 0). Sem interferência no CAD.
- `Modulo015` ganha a propriedade `StatusR49` com o registro acima.

## Conferências fechadas sem mudar o modelo (24/10)

- **P01:** eixos dos varões em 2050 e 1030 — 82 mm abaixo da base do maleiro (2132) e 52 mm abaixo da prateleira (1082).
- **P02:** as peças das 4 dobradiças do canto são todas válidas; o alerta do inventário vinha do grupo que junta os sólidos STEP da Blum. Não afeta corte nem furação.
- **P04:** folhas 440 × 306 × 18, canecos a 148 mm: massa estimada ≈1,8 kg, ≈23 N por dobradiça. Duas dobradiças bastam no cálculo nominal; a pesagem da porta pronta continua na oficina.
- **P18:** a ficha usa vão frontal 507 (725 − 218) e folhas 500; o 564 × 509 é o fundo.

Fichas R14 (P01, P02, P04, P16, P18), página de pendências, visualizador e caderno de oficina regenerados a partir das fontes (`fabrication/r14/mechanisms.json`, `joinery.json`, `compile_technical_revision.py`, `plain_language.py`, `src/cad-data.js`). Continua aberto no P16: sobreposição de 0,125–0,175 mm entre fundo e guia e o mapa definitivo de altura das guias (oficina).

## Verificação

[Verificacao_R49.json](Verificacao_R49.json): folga 1 → 7 mm; trava direita × guia 1.276 → 0 mm³ nas duas gavetas, trava esquerda continua 0; os outros 5.887 objetos com geometria e posição idênticas (1e-9 mm, [Diferencas_CAD.json](Diferencas_CAD.json) vazio), aparência idêntica, arquivo reaberto e R48 com SHA256 inalterado. Reproduzir: abrir [Gavetas_escritorio_R49.FCMacro](Gavetas_escritorio_R49.FCMacro) no FreeCAD 1.1 com interface.
