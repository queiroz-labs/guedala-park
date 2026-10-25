# Relatório de mudança do modelo

Gerado por `verificar_modelo.py` em 25/10/2026 19:42. Revisão `R52`. SHA256 `941da02d367c` → `941da02d367c`.

**Aprovação de Elias:** Não se aplica: modelo inalterado (mesmo SHA); sem diferença de geometria, posição, aparência ou movimento (25/10/2026)

## Resumo

| | Base anterior | Agora |
|---|---:|---:|
| Objetos | 5832 | 5832 |
| Expressões | 7702 | 7702 |
| Formas ativas | 1133 | 1133 |
| Peças com geometria própria inválida | 0 | 0 |
| Contêineres com forma montada inválida (informativo) | 12 | 12 |
| Cenários de movimento | 106 | 106 |

Nenhuma diferença em relação à base anterior.

## Como usar

1. Leia as seções acima. Cada mudança listada foi pedida e é a esperada?
2. Só com a aprovação dele: `python ferramentas/verificar_modelo/verificar_modelo.py --completo --atualizar-base --aprovado-por "Elias, dd/mm/aaaa: o que aprovou"`.
3. Commite a base, este relatório, `current_release.json` (SHA) e o `ESTADO_ATUAL.md` juntos.
