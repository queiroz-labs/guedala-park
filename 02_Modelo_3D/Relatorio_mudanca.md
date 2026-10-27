# Relatório de mudança do modelo

Gerado por `verificar_modelo.py` em 27/10/2026 10:41. Revisão `R53`. SHA256 `941da02d367c` → `fedd9d1d0604`.

**Aprovação de Elias:** Elias, 27/10/2026: Aplicar as decisoes ja tomadas ao CAD e fichas; crie um R53. P02 U1-U4=A, P13 F13=A, TV R44=A, lixeiras LIX=A; seis deslocamentos nominais conferidos, sem nova colisao.

## Resumo

| | Base anterior | Agora |
|---|---:|---:|
| Objetos | 5832 | 5832 |
| Expressões | 7702 | 7702 |
| Formas ativas | 1133 | 1133 |
| Peças com geometria própria inválida | 0 | 0 |
| Contêineres com forma montada inválida (informativo) | 12 | 12 |
| Cenários de movimento | 106 | 106 |

## Posição alterada (6)

- `Peca144`: (2320, 5080, 0) → (2250, 5080, 0) (Δ 70.0 mm)
- `Peca145`: (2320, 5080, 450) → (2250, 5080, 450) (Δ 70.0 mm)
- `Peca146`: (2300, 5140, 10) → (2230, 5140, 10) (Δ 70.0 mm)
- `Peca147`: (4540, 5410, 0) → (4540, 5470, 0) (Δ 60.0 mm)
- `Peca148`: (4540, 5410, 420) → (4540, 5470, 420) (Δ 60.0 mm)
- `Peca149`: (4640, 5680, 10) → (4640, 5740, 10) (Δ 60.0 mm)

## Geometria alterada (8)

- `Ambiente_cozinha`: volume 1797411572.797 → 1797411572.831 mm³
- `ApartamentoR34`: volume 19475644127.471 → 19475644127.477 mm³
- `Peca144`: volume 32130000.0 → 32130000.0 mm³
- `Peca145`: volume 1428000.0 → 1428000.0 mm³
- `Peca146`: volume 90000.0 → 90000.0 mm³
- `Peca147`: volume 35322000.0 → 35322000.0 mm³
- `Peca148`: volume 1429700.0 → 1429700.0 mm³
- `Peca149`: volume 90000.0 → 90000.0 mm³

## Como usar

1. Leia as seções acima. Cada mudança listada foi pedida e é a esperada?
2. Só com a aprovação dele: `python ferramentas/verificar_modelo/verificar_modelo.py --completo --atualizar-base --aprovado-por "Elias, dd/mm/aaaa: o que aprovou"`.
3. Commite a base, este relatório, `current_release.json` (SHA) e o `ESTADO_ATUAL.md` juntos.
