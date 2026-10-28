# Relatório de mudança do modelo

Gerado por `verificar_modelo.py` em 28/10/2026 00:02. Revisão `R54`. SHA256 `fedd9d1d0604` → `4a2996ee63dd`.

**Aprovação de Elias:** Elias, 27/10/2026, nesta tarefa: "Afaste só a cadeira lateral o mínimo necessário para não colidir com o pedestal e rode a verificação completa de novo. Se passar sem colisões novas, pode salvar como R54, atualizar a base e publicar no site." Condição verificada: afastamento 15 mm em +X; 106 cenários e nenhuma colisão nova.

## Resumo

| | Base anterior | Agora |
|---|---:|---:|
| Objetos | 5832 | 5834 |
| Expressões | 7702 | 7702 |
| Formas ativas | 1133 | 1134 |
| Peças com geometria própria inválida | 0 | 0 |
| Contêineres com forma montada inválida (informativo) | 12 | 12 |
| Cenários de movimento | 106 | 106 |

## Objetos novos (2)

- `Aberta_cadeira_lateralPedestal` Berlin - pedestal preto; altura 750 mm e formato aproximados; sem desenho tecnico - aberta
- `Fechada_110Pedestal` Berlin - pedestal preto; altura 750 mm e formato aproximados; sem desenho tecnico - fechada

## Posição alterada (1)

- `Fechada_110Lateral`: (1015, 4430, 0) → (1030, 4430, 0) (Δ 15.0 mm)

## Geometria alterada (2)

- `Fechada_110`: volume 119627055.408 → 215573258.329 mm³
- `Fechada_110Lateral`: volume 18016394.001 → 18016394.001 mm³

## Como usar

1. Leia as seções acima. Cada mudança listada foi pedida e é a esperada?
2. Só com a aprovação dele: `python ferramentas/verificar_modelo/verificar_modelo.py --completo --atualizar-base --aprovado-por "Elias, dd/mm/aaaa: o que aprovou"`.
3. Commite a base, este relatório, `current_release.json` (SHA) e o `ESTADO_ATUAL.md` juntos.
