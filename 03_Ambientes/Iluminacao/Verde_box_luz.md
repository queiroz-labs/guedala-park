# Verde nas duas paredes do box

Fonte da mudança: Elias, 30/10/2026, nesta conversa: “quero que esteja na parede da janela tbm”. Aprovação técnica: PENDENTE.

Comparação H13, sem luz natural: somente a refletância difusa da face interna da janela muda. Mesma malha, semente, raios, fontes e geometria nas duas soluções; abertura preservada. Não é medida real nem fotometria do produto.

Face exposta convertida no modelo de luz: 2.0978 m², após abertura/ocultações; não serve para compra. Faixas claras 0,50/0,625/0,75 → Sauge 0,10/0,20/0,30, hipóteses sem ensaio de refletância.

Um Firefly B11, posição/fluxo/manutenção centrais existentes; espelho e indireta desligados, como no cenário geral anterior. Sensor no box a 0,75 m, malha 0,10 m. O outro sensor mantém a malha geral do estudo.

| Sensor | Faixa | Uma parede (lx) | Duas (lx) | Diferença |
|---|---|---:|---:|---:|
| box_plano075 | baixo | 135.282 | 126.599 | -6.418% |
| box_plano075 | central | 154.621 | 142.208 | -8.028% |
| box_plano075 | alto | 182.999 | 164.243 | -10.249% |
| banho_geral | baixo | 181.142 | 175.359 | -3.192% |
| banho_geral | central | 201.746 | 193.168 | -4.252% |
| banho_geral | alto | 231.392 | 217.878 | -5.84% |

O verde devolve menos luz difusa: o box tende a ficar mais escuro com a mesma luminária. A ordem de grandeza depende das refletâncias e curvas ainda ausentes; faixas não são intervalos estatísticos. Conferir no local antes de decidir reforço. Nenhuma luminária, compra, potência ou circuito foi alterado.

[Valores, mínimos e uniformidade](Comparacao_verde_box_luz.csv). Reproduzir: `python -B ferramentas/estudos/comparar_verde_box_luz.py`.
