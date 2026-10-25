# FreeCAD R46 — fichas R14 no modelo

24/10/2026. **[Guedala_Park_R46_Fichas_R14.FCStd](Guedala_Park_R46_Fichas_R14.FCStd)** passa a ser o modelo vigente. Parte do R45 com cores R16 e rodízios P08 ([Guedala_Park_R45_Rodizios_P08.FCStd](../../../03_Ambientes/Cozinha/Rodizios_gaveta/Guedala_Park_R45_Rodizios_P08.FCStd), preservado) e grava no CAD o que as [fichas R14](../../../06_Entregas/Fichas_fabricacao/index.html) definem. **Nenhuma peça foi furada, movida ou redimensionada.** Não libera fabricação.

## O que entrou

| No FreeCAD | Onde ver |
|---|---|
| Os 20 móveis recebem o código da ficha, o resumo, a lista de ferragens R14 e o caminho da ficha | Selecione o móvel (`Modulo`…`Modulo019`) → propriedades do grupo **Ficha R14** |
| As 249 peças recebem a especificação de material da ficha, incluindo Arauco Beige Matt e Louro Freijó Poro no banheiro | Selecione a peça → `EspecificacaoR14` e `ModuloR14` |
| Tabela com os 20 módulos, objeto CAD, resumo e ficha | `00 · Dados…` → **R46 · fichas R14 por módulo** |
| 52 Minifix das fichas: P10 20, P11 12, P15 8, P19 12 | Grupo **R46 · 52 Minifix…**, marcadores laranja Ø15 dentro das peças |
| Gavetas P01 (4) e P06 (3): seleção **FGVTN 54FGOC12500TSX0** | 25 objetos de guia renomeados e com `StatusR14` |
| Gavetas do escritório P16: MOVENTO 400 confirmada | 8 objetos com `StatusR14` |
| Grupo antigo "FGVTN candidatas · 46 dobradiças" | Renomeado como histórico: as portas usam Blum 71B3550 |
| Banco P20: dobradiça piano + articuladores com trava | `MecanismoTampasR14` no `Modulo019` |

## O que continua diferente das fichas, e por quê

- **FGVTN 500 sem geometria própria.** Não há STEP oficial da FGVTN 500, e o de 400 não deve ser extrapolado. As guias continuam com a forma Blum MOVENTO 500 (G2 com o STEP da proposta R07) como envelope.
- **Minifix como marcadores.** As chapas não recebem os furos: as posições são nominais e precisam de prova em retalho. Os marcadores ficam inteiramente dentro de cada peça (conferido um a um).
- **Piano do banco não modelada.** Eixo, apoio na junta de 2 mm do encosto e terminais dos articuladores dependem do protótipo.
- **Ligações sem mapa** (P01, P04, P12, P17 e demais) seguem só na proposta do [mapa de conectores R00](../../../04_Moveis/Mapa_conectores/README.md).

## Verificação

[Verificacao_R46.json](Verificacao_R46.json):
- os 5.846 objetos do R45/P08 conferidos por volume, área, faces, vértices, caixa envolvente, centro de massa e posição (1e-9 mm), com zero diferenças ([Diferencas_CAD.json](Diferencas_CAD.json));
- 16.840 propriedades de aparência (cores R16) idênticas;
- arquivo reaberto e conferido de novo; R45/P08 com SHA256 inalterado.

A comparação por geometria substitui o `hashCode` usado na P08: o recálculo troca esse identificador e deixa ruído de 1e-17 nas portas guiadas por expressão, sem mudar a forma.

## Reproduzir

1. `python preparar_entrada.py` lê as fichas e gera [Entrada_R46.json](Entrada_R46.json).
2. Abra [Aplicar_fichas_R14.FCMacro](Aplicar_fichas_R14.FCMacro) no FreeCAD 1.1, que precisa da interface para manter as cores. A macro recusa sobrescrever um R46 existente.
