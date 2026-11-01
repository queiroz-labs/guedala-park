# Relatório de mudança do modelo

Gerado por `verificar_modelo.py` em 01/11/2026 16:47. Revisão `R55`. SHA256 `d5ed97df437b` → `b23705247989`.

**Aprovação de Elias:** Elias, 01/11/2026: Sim, incorporar essa correção; lavanderia 1290x1540 mm, parede 170 mm, pisos e rodapés compatibilizados, Loop +15 mm; 106 cenários sem colisão nova.

## Resumo

| | Base anterior | Agora |
|---|---:|---:|
| Objetos | 6028 | 6028 |
| Expressões | 8049 | 8049 |
| Formas ativas | 1147 | 1147 |
| Peças com geometria própria inválida | 0 | 0 |
| Contêineres com forma montada inválida (informativo) | 14 | 14 |
| Cenários de movimento | 106 | 106 |

## Posição alterada (7)

- `Peca147`: (4540, 5470, 0) → (4540, 5485, 0) (Δ 15.0 mm)
- `Peca148`: (4540, 5470, 420) → (4540, 5485, 420) (Δ 15.0 mm)
- `Peca149`: (4640, 5740, 10) → (4640, 5755, 10) (Δ 15.0 mm)
- `RodapeTrecho_021`: (2850, 5390, 0) → (2850, 5460, 0) (Δ 70.0 mm)
- `RodapeTrecho_034`: (4835, 5390, 0) → (4835, 5460, 0) (Δ 70.0 mm)
- `RodapeTrecho_035`: (3520, 5390, 0) → (3520, 5460, 0) (Δ 70.0 mm)
- `RodapeTrecho_053`: (2660, 5390, 0) → (2660, 5460, 0) (Δ 70.0 mm)

## Geometria alterada (38)

- `Ambiente_lavanderia`: volume 450052000.0 → 450052000.0 mm³
- `ApartamentoR34`: volume 17794985583.922 → 18181385583.922 mm³
- `Area_Cozinha`: volume 0.0 → 0.0 mm³
- `Area_Lavanderia`: volume 0.0 → 0.0 mm³
- `BuildingPart`: volume 9624436800.0 → 10018417800.0 mm³
- `Elementos_Lavanderia`: volume 450052000.0 → 450052000.0 mm³
- `Lavanderia_Iseo_Marfim`: volume 103845000.0 → 99330000.0 mm³
- `Peca049`: volume 540930000.0 → 919581000.0 mm³
- `Peca050`: volume 70080000.0 → 119136000.0 mm³
- `Peca147`: volume 35322000.0 → 35322000.0 mm³
- `Peca148`: volume 1429700.0 → 1429700.0 mm³
- `Peca149`: volume 90000.0 → 90000.0 mm³
- `Piso_lavanderia`: volume 107065000.0 → 102410000.0 mm³
- `Piso_vinilico`: volume 1541255000.0 → 1538245000.0 mm³
- `RodapeTrecho_021`: volume 804000.0 → 804000.0 mm³
- `RodapeTrecho_034`: volume 360000.0 → 360000.0 mm³
- `RodapeTrecho_035`: volume 1578000.0 → 1578000.0 mm³
- `RodapeTrecho_052`: volume 120000.0 → 204000.0 mm³
- `RodapeTrecho_053`: volume 228000.0 → 228000.0 mm³
- `Rodape_8cm`: volume 42500160.0 → 42584160.0 mm³
- `Rodape_cozinha`: volume 4633116.0 → 4633116.0 mm³
- `Rodape_lavanderia`: volume 3475152.0 → 3475152.0 mm³
- `Rodape_sala`: volume 9192000.0 → 9276000.0 mm³
- `Soleira_cozinha_lavanderia`: volume 3220000.0 → 3080000.0 mm³
- `VaosBase`: volume 10554990000.0 → 10948971000.0 mm³
- `VaosCorte_JB`: volume 9967390000.0 → 10361371000.0 mm³
- `VaosCorte_JE`: volume 10289440000.0 → 10683421000.0 mm³
- `VaosCorte_JL`: volume 10012590000.0 → 10406571000.0 mm³
- `VaosCorte_JQ`: volume 10419390000.0 → 10813371000.0 mm³
- `VaosCorte_JS`: volume 10132370000.0 → 10526351000.0 mm³
- `VaosCorte_PB`: volume 9516390000.0 → 9910371000.0 mm³
- `VaosCorte_PE`: volume 9659890000.0 → 10053871000.0 mm³
- `VaosCorte_PI`: volume 9362640000.0 → 9756621000.0 mm³
- `VaosCorte_PQ`: volume 9813640000.0 → 10207621000.0 mm³
- `VaosTopo_Peca049`: volume 21900000.0 → 37230000.0 mm³
- `Vinilico_Sem_Soleira_Escritorio`: volume 1541255000.0 → 1538245000.0 mm³
- `Vinilico_Sem_Soleira_Quarto`: volume 1545005000.0 → 1541995000.0 mm³
- `Vinilico_continuo`: volume 1548755000.0 → 1545745000.0 mm³

## Como usar

1. Leia as seções acima. Cada mudança listada foi pedida e é a esperada?
2. Só com a aprovação dele: `python ferramentas/verificar_modelo/verificar_modelo.py --completo --atualizar-base --aprovado-por "Elias, dd/mm/aaaa: o que aprovou"`.
3. Commite a base, este relatório, `current_release.json` (SHA) e o `ESTADO_ATUAL.md` juntos.
