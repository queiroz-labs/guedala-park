# Relatório de mudança do modelo

Gerado por `verificar_modelo.py` em 02/11/2026 01:21. Revisão `R55`. SHA256 `abf6c2eb22f4` → `0d9e16fc47ff`.

**Aprovação de Elias:** Elias, 02/11/2026: aprovo deixa como documento principal

## Resumo

| | Base anterior | Agora |
|---|---:|---:|
| Objetos | 6038 | 6149 |
| Expressões | 8072 | 8239 |
| Formas ativas | 1143 | 1199 |
| Peças com geometria própria inválida | 0 | 0 |
| Contêineres com forma montada inválida (informativo) | 14 | 14 |
| Cenários de movimento | 106 | 106 |

## Objetos novos (111)

- `IB6S_Controles` Geladeira — abrir refrigerador / freezer
- `IB6S_Corpo` IB6S — corpo fixo
- `IB6S_Pega_Freezer` IB6S — pega embutida Freezer
- `IB6S_Pega_Refrigerador` IB6S — pega embutida Refrigerador
- `IB6S_Porta_Freezer` IB6S — porta Freezer
- `IB6S_Porta_Refrigerador` IB6S — porta Refrigerador
- `IB6S_Visual` Geladeira IB6S — aparencia e portas
- `LGVC4_Aro` LG VC4 — aro da porta
- `LGVC4_Controles` Lava e seca — abrir porta
- `LGVC4_Corpo` LG VC4 — corpo fixo com abertura
- `LGVC4_GavetaSabao` LG VC4 — frente do dispenser
- `LGVC4_Painel` LG VC4 — comandos
- `LGVC4_Seletor` LG VC4 — seletor
- `LGVC4_Vidro` LG VC4 — vidro da porta
- `LGVC4_Visual` Lava e seca LG VC4 — aparencia e porta
- `ME23P_Comandos` ME23P — coluna de comandos
- `ME23P_Corpo` ME23P — corpo
- `ME23P_Porta` ME23P — moldura da porta
- `ME23P_Tecla00` ME23P — tecla visual
- `ME23P_Tecla01` ME23P — tecla visual001
- `ME23P_Tecla02` ME23P — tecla visual002
- `ME23P_Tecla10` ME23P — tecla visual003
- `ME23P_Tecla11` ME23P — tecla visual004
- `ME23P_Tecla12` ME23P — tecla visual005
- `ME23P_Tecla20` ME23P — tecla visual006
- `ME23P_Tecla21` ME23P — tecla visual007
- `ME23P_Tecla22` ME23P — tecla visual008
- `ME23P_Tecla30` ME23P — tecla visual009
- `ME23P_Tecla31` ME23P — tecla visual010
- `ME23P_Tecla32` ME23P — tecla visual011
- `ME23P_Vidro` ME23P — vidro frontal
- `ME23P_Visual` Micro-ondas Electrolux ME23P
- `P07_Faixa_Superior_Forno` P07 — faixa frontal acima da grelha do forno
- `PE12G_Bandeja` PE12G — bandeja removivel
- `PE12G_Bica` PE12G — bica
- `PE12G_Comandos` PE12G — painel frontal
- `PE12G_Corpo` PE12G — corpo grafite e rebaixo
- `PE12G_Tecla0` PE12G — selecao temperatura
- `PE12G_Tecla1` PE12G — selecao temperatura001
- `PE12G_Tecla2` PE12G — selecao temperatura002
- … e mais 71

## Posição alterada (4)

- `Folha_Banheiro`: (-20, 0, 0) → (2850, 4050, 0) (Δ 4963.8 mm)
- `Folha_Escritorio`: (2640, 2150, 0) → (2650, 2150, 0) (Δ 10.0 mm)
- `Peca136`: (2355, 6780, 920) → (2585, 6890, 920) (Δ 255.0 mm)
- `Peca137`: (2365, 6770, 1330) → (2585, 6720, 1330) (Δ 225.6 mm)

## Geometria alterada (17)

- `Ambiente_banho`: volume 326872280.0 → 240726643.642 mm³
- `Ambiente_cozinha`: volume 1157152045.0 → 248277330.0 mm³
- `Ambiente_lavanderia`: volume 450052000.0 → 105815200.0 mm³
- `ApartamentoR34`: volume 18095522844.492 → 16767903527.229 mm³
- `BuildingPart`: volume 9907821960.0 → 9905097960.0 mm³
- `Elementos_Banho`: volume 326872280.0 → 240726643.642 mm³
- `Elementos_Cozinha`: volume 1157152045.0 → 248277330.0 mm³
- `Elementos_Lavanderia`: volume 450052000.0 → 105815200.0 mm³
- `Folha_Banheiro`: volume 29400000.0 → 29400000.0 mm³
- `Folha_Escritorio`: volume 33600000.0 → 33600000.0 mm³
- `Janela_Escritorio`: volume 22280000.0 → 20948000.0 mm³
- `Janela_Quarto`: volume 23080000.0 → 21688000.0 mm³
- `Modulo006`: volume 33421181.734 → 34615562.539 mm³
- `Moveis`: volume 1386425450.85 → 1387619840.884 mm³
- `P07`: volume 33421181.734 → 34615562.539 mm³
- `Peca136`: volume 172000.0 → 172000.0 mm³
- `Peca137`: volume 68000.0 → 68000.0 mm³

## Aparência alterada (13)

- `FaixaQuinaBR04`: cor EDF2F3 → 7BA2C4, transparência 0 → 0%
- `FrenteSimplesR001`: cor EDF2F3 → 7BA2C4, transparência 0 → 0%
- `Peca138`: cor B5B5AE → B5B5AE, transparência 0 → 0%
- `Peca140`: cor 2E2D28 → 2E2D28, transparência 0 → 0%
- `Peca152`: cor B5B5AE → B5B5AE, transparência 0 → 0%
- `Peca154`: cor 2E2D28 → 2E2D28, transparência 0 → 0%
- `Peca190`: cor E1EAEE → E1EAEE, transparência 0 → 0%
- `Peca351`: cor 2E2D28 → 2E2D28, transparência 0 → 0%
- `Peca384`: cor EDF2F3 → E1EAEE, transparência 0 → 0%
- `Peca386`: cor E1EAEE → EDF2F3, transparência 0 → 0%
- `Peca388`: cor E1EAEE → EDF2F3, transparência 0 → 0%
- `Persiana_Integrada_Escritorio`: cor E8EDF0 → E8EDF0, transparência 0 → 0%
- `Persiana_Integrada_Quarto`: cor E8EDF0 → E8EDF0, transparência 0 → 0%

## Visibilidade alterada (8)

- `Peca138`: visível → oculto
- `Peca140`: visível → oculto
- `Peca152`: visível → oculto
- `Peca154`: visível → oculto
- `Peca190`: visível → oculto
- `Peca351`: visível → oculto
- `Persiana_Integrada_Escritorio`: visível → oculto
- `Persiana_Integrada_Quarto`: visível → oculto

## Expressões alteradas (4)

- `Folha_Banheiro`: 6 → 3 expressões
- `Folha_Entrada`: 6 → 3 expressões
- `Folha_Escritorio`: 6 → 3 expressões
- `Folha_Quarto`: 6 → 3 expressões

## Como usar

1. Leia as seções acima. Cada mudança listada foi pedida e é a esperada?
2. Só com a aprovação dele: `python ferramentas/verificar_modelo/verificar_modelo.py --completo --atualizar-base --aprovado-por "Elias, dd/mm/aaaa: o que aprovou"`.
3. Commite a base, este relatório, `current_release.json` (SHA) e o `ESTADO_ATUAL.md` juntos.
