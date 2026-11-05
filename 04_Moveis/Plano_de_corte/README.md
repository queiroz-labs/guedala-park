# Lista de corte e custos de chapa

Simulação de cenários de corte (refilo/serra, sete propostas, custo de fita) removida em 04/11/2026: o resultado dependia de formato de chapa, produto e oficina ainda não definidos. Fica o que a cotação usa; o histórico está no git.

| Arquivo | Para quê |
|---|---|
| [Lista_de_corte.csv](Lista_de_corte.csv) | Peças vigentes por padrão e espessura (base das quantidades da cotação) |
| [Resumo_chapas.csv](Resumo_chapas.csv) | Chapas por grupo, usado pelo comparador de cotações |
| [Custos_chapas.csv](Custos_chapas.csv) | Faixa de preço por padrão/espessura/formato, usado pelo comparador |

O motor de corte e a base ficam em [Corte e formatos](../Proximas_decisoes/Corte_e_formatos/README.md). Quem otimiza o corte é o fornecedor de chapa ou a oficina, com a máquina dele.
