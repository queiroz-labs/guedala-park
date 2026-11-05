# Cotação — pacote vigente e limites

Revisão 04/11/2026. **Preparado, não enviado.** [Checklist](index.html) · [Marcenaria](Marcenaria.zip) · [Todos os pedidos](Pacote_cotacao.zip).

| Item | O que vale para o envio |
|---|---|
| Escopo | Integral comparativo e etapa inicial D05-C/D06-B; P16/P17/C01/C03/C04/C05 futuros; E06 adiada, E05 mantida |
| Inventário | [CSV atual](Quantidades_referencia.csv): 251 painéis e ferragens transcritas das fichas atuais; não é lista de compra |
| Gavetas | Laterais com amortecimento: P01 4 pares 500 mm; P06 3 pares 500 mm; P16 2 pares 400 mm futuro; produto/furação pendentes |
| Chapas e fita | Oficina quantifica por etapa, produto, formato e processo; plano de 249 painéis/14 chapas e metragem antiga não compõem o pedido vigente |
| Conectores | Não somar ficha e mapa; P19 12/8 Minifix permanece sem decisão |
| Serviços | Medição, executivo, materiais, ferragens, montagem, arremates, tributos, frete e segunda mobilização discriminados; informar inclusão e responsável |
| Prazo | A combinar no envio; 30/10 venceu sem envio registrado |
| Limites | R55 de referência; fichas R15 atualizadas conservam rótulos históricos R53/R45 e mapas anteriores; não representam nova extração integral |

Pedidos individuais preservam amostras A/C e consultas IL02–IL09. Galaxy/Paris Luz são alternativas para a mesma unidade; controle E05 está na IL02, sem duplicação na IL08. Nenhum envio, compra ou preço interno incluído.

Regenerar: `python -B ferramentas/estudos/gerar_pedidos_cotacao.py`. Validar: `python -B ferramentas/estudos/test_quantidades_cotacao.py` (fontes atuais, escopo, formulário, CRC, links e bytes das fichas anexadas).

## Auditoria histórica de 29/10 — não valida o pacote atual

A [auditoria das 101 linhas](Auditoria_linhas_cotacao.csv), as [diferenças entre bases](Auditoria_diferencas.csv) e os [hashes/resultados](Auditoria_resultado.json) descrevem a base anterior de 249 painéis. O CSV auditado está no git; não é o inventário atual. A auditoria encontrou contas consistentes naquela base, mas não demonstrou suficiência para fabricação. Não reaplicar os totais de chapas, fita ou guias ocultas ao pedido atual.
