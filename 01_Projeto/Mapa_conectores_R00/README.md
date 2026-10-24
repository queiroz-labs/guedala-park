# Mapa de conectores proposto — R00

24/10/2026. **Proposta de quantidades para cotação, não programa de furação.** Cobre os quatro módulos que usam Minifix sem quantidade definida nas fichas R14: P01 Roupeiro, P04 Aéreo da cabeceira, P12 Aéreo A e P17 Aéreo do escritório. Os outros três aéreos e o espelheiro já tinham quantidade (P10 20, P11 12, P15 8, P19 12).

## Regra usada

Segue a estratégia que cada ficha já escolheu:

- **Encontro com o fundo:** Confirmat 7×50 + cavilha Ø8×30 (o fundo fica oculto).
- **Demais encontros de 18 mm:** Minifix 15 + cavilha Ø8×30.
- **Quantidade por encontro:** 2 conectores até 400 mm de contato, 3 até 700 mm e, acima disso, um a cada cerca de 350 mm.

A oficina pode ajustar essa regra de espaçamento. Continuam valendo os cuidados das fichas:
- desencontrar os pilotos nas divisórias de 18 mm (não furar dos dois lados no mesmo ponto);
- definir a sequência de fechamento;
- testar o pré-furo em chapa real.

A lista vem da amostra de painéis retangulares das fichas. **Um encontro ausente da lista não significa que a ligação não exista.**

- Lista por encontro: [Mapa_conectores_R00.csv](Mapa_conectores_R00.csv) (abre no Excel).
- Para refazer: `python gerar_mapa.py`.

## Totais propostos

<!-- TOTAIS -->

| Módulo | Encontros | Minifix 15 | Confirmat 7×50 | Cavilhas Ø8×30 | Parafusos 4×30 (face a face) |
|---|---:|---:|---:|---:|---:|
| P01 · Roupeiro | 33 | 57 | 52 | 109 | 0 |
| P04 · Aéreo da cabeceira | 19 | 24 | 12 | 36 | 4 |
| P12 · Aéreo A | 9 | 12 | 9 | 21 | 0 |
| P17 · Aéreo escritório | 19 | 24 | 18 | 42 | 4 |
| **Total** | **80** | **117** | **91** | **208** | **8** |

## Efeito no orçamento

Somando os 52 Minifix já definidos (P10, P11, P15 e P19), o projeto teria cerca de **169 Minifix**, contra 20 na memória do orçamento. Em custo, a diferença é pequena: a R$1,50–3,00 por conjunto, mais Confirmat e cavilhas, fica em cerca de **R$270–590** no total. Isso cabe na verba de conectores e fixadores (R$650–1.200) da [revisão de ferragens](../Orcamento_R43_2026-10-22/Marcenaria_35mil/Revisao_ferragens_servicos_2026-10-23.md). O impacto maior é em **horas de furação**, que a oficina deve considerar.
