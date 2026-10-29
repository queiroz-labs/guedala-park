# Cotação — conferência independente das quantidades

## Impacto no pacote com resposta prevista para 30/10 às 18 h

**Nenhum erro de soma ou arredondamento que exija corrigir a quantidade do pacote foi comprovado.** Foram conferidos **101 registros de dados** do [CSV vigente](Quantidades_referencia.csv), não 100: 77 linhas numéricas e 24 sem quantidade deliberadamente. A linha adicional compara a fita arredondada por peça. Os ZIPs/pedidos e as fontes foram preservados; esta auditoria não envia nem altera a cotação.

Antes de cotar, manter explícitos **33 painéis fora do corte, 23 sem regra suficiente de fita, 40 linhas de ferragens sem quantidade**, e o conjunto integral com móveis adiados. A conta não completa esses itens. No P19, **12 Minifix documentais versus 8 no mapa** permanece diferença de proposta, sem troca decidida. Uma soma correta não demonstra que o quantitativo seja suficiente para fabricar ou montar.

[Checklist e pedidos](index.html) · [Pacote existente](Pacote_cotacao.zip) · [Conferência das 101 linhas](Auditoria_linhas_cotacao.csv) · [Diferenças entre bases](Auditoria_diferencas.csv) · [Resultados e hashes das entradas](Auditoria_resultado.json).

## Resultado recalculado

| Tema | Resultado independente | Limite da conferência |
|---|---|---|
| Painéis | 249 IDs únicos nas 20 fichas; quantidades agrupadas expandidas por ID | Inclui móveis adiados; as 36 peças alternativas não entram |
| Corte | 216 IDs no corte, 33 excluídos; 16 cenários e 29 chapas virtuais conferidas no conjunto dos cenários | Os cenários são alternativas, não somar 29 chapas como compra. Conjunto misto continua 14 |
| Corte misto | Arenza 18: 3; Azul 18: 1; Beige 18: 1; Branco 15: 1; Branco 16: 1; Branco 18: 5; Louro 18: 1; Off-white 18: 1 | 8 chapas 2750 × 1850 + 6 de 2750 × 2100; formato/SKU/processo a confirmar |
| Fita | 191,1360 m; perda 10% por cor: 210,2496 m; por peça: 210,2498 m | Diferença 0,0002 m = 0,2 mm por estágio do arredondamento. Não é quantidade adicional para compra |
| Perímetros | 477,6400 m nos envelopes | Não são metragem de fita: fundos, bordas ocultas e recortes têm tratamento distinto |
| Conectores | 218 juntas; 316 Minifix; 203 Confirmat do mapa + 4 documentais; 519 cavilhas do mapa + 8 documentais; 52 parafusos face a face | Mapa nominal/proposta; componentes de kits e decisões descritivas não são duplicados |
| Ferragens principais | 52 dobradiças, 52 bases, 52 limitadores; 7 pares FGVTN 500 e 2 MOVENTO 400 | Quantidade documental, não dimensionamento ou confirmação de compra |
| Furos | 2.286 IDs únicos, 319 faces e 145 painéis com centros; 104 sem centros | Contagem, sem nova aprovação espacial; não inventa furos de corrediças/bases/System32 |
| Massas | Volume de envelopes 1,060405325 m³; referência geral 731,833104 kg | Mesma densidade equivalente aplicada como hipótese a todos os painéis; não é pesagem nem massa montada |
| Massa com vínculo de catálogo | 39 painéis/131,650687 kg, densidade equivalente 690,144690 kg/m³ | Greenplac Arenza 18 condicional; 210 painéis e ferragens seguem sem massa sustentada por produto |

As **2.127 comparações numéricas** não apresentaram divergência acima da precisão documentada. Os testes de identidade, unicidade e estrutura complementam essa contagem. Nenhum CSV fonte foi corrigido. Também foram conferidos os números nas observações: painéis por grupo de chapa, incluídos/excluídos/sem fita por móvel, pendências, Minifix documentais e fita por cor. As 23 linhas sem fita preservam a justificativa da fonte e conferem móvel/espessura; fontes apontadas existem. Ressalvas qualitativas são preservadas, sem validar escolhas ou suficiência técnica.

## Independência, precisão e limites

O novo script usa somente a biblioteca padrão. **Não importa nem executa os geradores de 28–29/10**, nem lê o FreeCAD. Expande as fichas `Pxx-pecas.csv`, usa C/L/espessura como valores decimais e confronta o inventário de painéis. Recalcula a fita pelos indicadores C0/C1/L0/L1: bordas C têm comprimento L; bordas L têm comprimento C. Essas regras continuam propostas; conferir sua aritmética não confirma a escolha de bordas.

As ferragens são reconstruídas de `hardwareRows` em `technical-r14.json` e do mapa de juntas. Não se soma `decisions`, não se soma caixa+pino como dois conjuntos e não se transforma quantidade ausente em zero. Os 35 grupos de totais são comparados com o inventário de 134 linhas por móvel; as 40 pendências são confrontadas por móvel/item. As oito linhas documentais de caixas/pinos Minifix representam 52 conjuntos históricos, separados dos 316 do mapa.

Para o corte, o arquivo externo `Planos.json` é **objeto da auditoria, não resultado aceito sem teste**: cada corte precisa consumir um retângulo livre e produzir filhos compatíveis com serra 3,2 mm; margem 10 mm, dimensões/IDs das fichas, sentido restrito, sobras e cobertura são conferidos novamente. Recalculam-se área, aproveitamento e limite inferior. Não se executou novo otimizador nem se provou ótimo global. Nos grupos/formato em que a quantidade coincide com o limite inferior, a igualdade vale somente para aquelas hipóteses. A exclusão por definição de material é preservada, não redecidida pela auditoria.

Nas massas, aplica-se do zero a relação documental 63,2 kg/(2,75 × 1,85 × 0,018 m³). Volume de envelope inclui material que pode ser retirado em recortes; espelho, adesivo, fita e ferragens não recebem peso zero nem entram ficticiamente. A massa geral usa uma hipótese de densidade comum já identificada no estudo vigente, separada do cenário condicional dos 39 IDs. Sem conclusão de carga de uso ou suspensão.

Comparações respeitam a precisão do campo: fita/perdas até 0,00005 m, áreas de sobras até 0,00005 m², percentuais até 0,005 ponto, volume por móvel até 0,000000005 m³ e massa até 0,000001 kg. Inteiros e IDs são exatos. Não há divergência escondida por tolerância de fabricação: são limites exclusivamente numéricos de serialização/arredondamento.

## Pendências que não são erros mecânicos

- **P19:** manter o detalhe de 12 conjuntos Minifix ou estudar 8 com outra ligação do fundo? Pergunta já existente; esta auditoria não escolhe uma alternativa.
- **Corte/fita:** confirmar composição/SKU dos 33 painéis e regra dos 23 sem fita; não reabrir cores já escolhidas. O orçamento de 16 chapas é memória de outro ensaio, não uma contagem para somar às 14 atuais.
- **Massas:** confirmar substrato, massa de produto e componentes ausentes antes de transporte/montagem real. Nenhuma informação aqui completa os requisitos de oficina ou RT.

Não foi encontrada nova decisão indispensável para Elias além das perguntas já registradas nas áreas. Não se alterou conclusão, orçamento, projeto, CSV de cotação ou ZIP.

## Reprodução e validação

```powershell
python -B ferramentas/estudos/auditoria_independente.py
python -B ferramentas/estudos/test_auditoria_independente.py
```

Oito testes cobrem IDs/quantidades, orientação da fita, ausência versus zero, arredondamento, kits/conjuntos sem dupla contagem, perda de serra, rotação proibida e densidade da chapa. Todos passaram. O comando principal verifica também que nenhuma entrada mudou durante a leitura.

Detalhes das 2.127 comparações ficam em `../outputs/Auditoria_quantidades/Conferencias.csv`, fora do Git; SHA256 `df8b8c93a1ec16166a3b0f7aa6062be2a5a193dce52d38ab8bc1ef861f3e1154`. `Planos.json` externo: SHA256 `f3850114e18ea0e52ab0ced3071cf0f303218e2bdc3ae77150784bdffc39a72d`. Os hashes das entradas individuais estão no resumo JSON pequeno; sem duplicar o arquivo volumoso no repositório. Em outro computador, regenerar primeiro os planos pelo comando documentado no [README do corte](../../04_Moveis/Proximas_decisoes/Corte_e_formatos/README.md), depois executar esta auditoria independente.
