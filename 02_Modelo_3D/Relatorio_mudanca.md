# Relatório de mudança do modelo

Gerado por `verificar_modelo.py` em 01/11/2026 18:04. Revisão `R55`. SHA256 `b23705247989` → `abf6c2eb22f4`.

**Aprovação de Elias:** Elias, 01/11/2026: Sim, incorporar o candidato e atualizar a base; portas livres 800 x 2100 mm, banheiro 700 x 2100 mm; alturas 2550/2300 mm; bancada/gabinete preservados.

## Resumo

| | Base anterior | Agora |
|---|---:|---:|
| Objetos | 6028 | 6038 |
| Expressões | 8049 | 8072 |
| Formas ativas | 1147 | 1143 |
| Peças com geometria própria inválida | 0 | 0 |
| Contêineres com forma montada inválida (informativo) | 14 | 14 |
| Cenários de movimento | 106 | 106 |

## Objetos novos (10)

- `Portas_Parametros` Portas_Parametros
- `RecortePortas_RodapeTrecho_004` RecortePortas_RodapeTrecho_004
- `RecortePortas_RodapeTrecho_006` RecortePortas_RodapeTrecho_006
- `RecortePortas_RodapeTrecho_028` RecortePortas_RodapeTrecho_028
- `RecortePortas_RodapeTrecho_030` RecortePortas_RodapeTrecho_030
- `RodapePortas_RodapeTrecho_004` RodapePortas_RodapeTrecho_004
- `RodapePortas_RodapeTrecho_006` RodapePortas_RodapeTrecho_006
- `RodapePortas_RodapeTrecho_028` RodapePortas_RodapeTrecho_028
- `RodapePortas_RodapeTrecho_030` RodapePortas_RodapeTrecho_030
- `Teto_Banheiro_Referencia` Teto acabado do banheiro - referencia nominal 2300 mm

## Posição alterada (6)

- `Folha_Banheiro_Operacao`: (2860, 4050, 0) → (2870, 4050, 0) (Δ 10.0 mm)
- `Folha_Entrada`: (0, 6980, 0) → (0, 6880, 0) (Δ 100.0 mm)
- `Folha_Escritorio`: (2640, 2240, 0) → (2640, 2150, 0) (Δ 90.0 mm)
- `PortaEntradaBanheiroR12`: (2860, 4050, 0) → (2870, 4050, 0) (Δ 10.0 mm)
- `VaosFerramenta_PI`: (-100, 6150, 0) → (-100, 6060, 0) (Δ 90.0 mm)
- `VaosFerramenta_PQ`: (3650, 3150, 0) → (3650, 3060, 0) (Δ 90.0 mm)

## Geometria alterada (71)

- `ApartamentoR34`: volume 18181385583.922 → 18095522844.492 mm³
- `Batente_Banheiro`: volume 9520000.0 → 9880000.0 mm³
- `Batente_Banheiro_Compatibilizado`: volume 9280000.0 → 9760000.0 mm³
- `Batente_Entrada`: volume 9620000.0 → 10080000.0 mm³
- `Batente_Escritorio`: volume 9620000.0 → 10080000.0 mm³
- `Batente_Escritorio_Compatibilizado`: volume 9380000.0 → 9960000.0 mm³
- `Batente_Quarto`: volume 9620000.0 → 10080000.0 mm³
- `BuildingPart`: volume 10018417800.0 → 9907821960.0 mm³
- `Folha_Banheiro`: volume 26796000.0 → 29400000.0 mm³
- `Folha_Banheiro_Operacao`: volume 26796000.0 → - mm³
- `Folha_Entrada`: volume 28826000.0 → 33600000.0 mm³
- `Folha_Escritorio`: volume 28826000.0 → 33600000.0 mm³
- `Folha_Quarto`: volume 28826000.0 → 33600000.0 mm³
- `Peca037`: volume 51400000.0 → 51000000.0 mm³
- `Peca039`: volume 1272150000.0 → 1262250000.0 mm³
- `Peca041`: volume 77100000.0 → 76500000.0 mm³
- `Peca043`: volume 64250000.0 → 63750000.0 mm³
- `Porta_Banheiro`: volume 39816000.0 → 215684160.0 mm³
- `Porta_Entrada`: volume 42196000.0 → 4200000.0 mm³
- `Porta_Escritorio`: volume 45946000.0 → 7500000.0 mm³
- `Porta_Quarto`: volume 38446000.0 → - mm³
- `Rodape_8cm`: volume 42584160.0 → 42104160.0 mm³
- `Rodape_banho`: volume 3473940.0 → 3233940.0 mm³
- `Rodape_escritorio`: volume 10475988.0 → 10235988.0 mm³
- `Soleira_Entrada`: volume 3750000.0 → 4200000.0 mm³
- `VaosBase`: volume 10948971000.0 → 10863765000.0 mm³
- `VaosCorte_JB`: volume 10361371000.0 → 10276165000.0 mm³
- `VaosCorte_JE`: volume 10683421000.0 → 10598215000.0 mm³
- `VaosCorte_JL`: volume 10406571000.0 → 10321365000.0 mm³
- `VaosCorte_JQ`: volume 10813371000.0 → 10728165000.0 mm³
- `VaosCorte_JS`: volume 10526351000.0 → 10441145000.0 mm³
- `VaosCorte_PB`: volume 9910371000.0 → 9763125000.0 mm³
- `VaosCorte_PE`: volume 10053871000.0 → 9920005000.0 mm³
- `VaosCorte_PI`: volume 9756621000.0 → 9585045000.0 mm³
- `VaosCorte_PQ`: volume 10207621000.0 → 10098085000.0 mm³
- `VaosFerramenta_PB`: volume 143500000.0 → 156880000.0 mm³
- `VaosFerramenta_PE`: volume 153750000.0 → 178080000.0 mm³
- `VaosFerramenta_PI`: volume 153750000.0 → 178080000.0 mm³
- `VaosFerramenta_PQ`: volume 153750000.0 → 178080000.0 mm³
- `VaosRecomposicao_JB`: volume 102800000.0 → 102000000.0 mm³
- … e mais 31

## Aparência alterada (4)

- `RodapeTrecho_004`: cor E1EAEE → E1EAEE, transparência 0 → 0%
- `RodapeTrecho_006`: cor E1EAEE → E1EAEE, transparência 0 → 0%
- `RodapeTrecho_028`: cor E1EAEE → E1EAEE, transparência 0 → 0%
- `RodapeTrecho_030`: cor E1EAEE → E1EAEE, transparência 0 → 0%

## Visibilidade alterada (4)

- `RodapeTrecho_004`: visível → oculto
- `RodapeTrecho_006`: visível → oculto
- `RodapeTrecho_028`: visível → oculto
- `RodapeTrecho_030`: visível → oculto

## Expressões alteradas (20)

- `Area_Banheiro`: 1 → 2 expressões
- `Area_Circulacao`: 1 → 2 expressões
- `Area_Cozinha`: 1 → 2 expressões
- `Area_Escritorio`: 1 → 2 expressões
- `Area_Lavanderia`: 1 → 2 expressões
- `Area_Quarto`: 1 → 2 expressões
- `Area_Sala`: 1 → 2 expressões
- `Folha_Banheiro`: 4 → 6 expressões
- `Folha_Entrada`: 4 → 6 expressões
- `Folha_Escritorio`: 4 → 6 expressões
- `Folha_Quarto`: 4 → 6 expressões
- `Peca037`: 4 → 5 expressões
- `Peca039`: 4 → 5 expressões
- `Peca041`: 4 → 5 expressões
- `Peca043`: 4 → 5 expressões
- `PortaEntradaBanheiroR12`: 5 → 5 expressões
- `VaosFerramenta_PB`: 1 → 2 expressões
- `VaosFerramenta_PE`: 1 → 2 expressões
- `VaosFerramenta_PI`: 1 → 2 expressões
- `VaosFerramenta_PQ`: 1 → 2 expressões

## Como usar

1. Leia as seções acima. Cada mudança listada foi pedida e é a esperada?
2. Só com a aprovação dele: `python ferramentas/verificar_modelo/verificar_modelo.py --completo --atualizar-base --aprovado-por "Elias, dd/mm/aaaa: o que aprovou"`.
3. Commite a base, este relatório, `current_release.json` (SHA) e o `ESTADO_ATUAL.md` juntos.
