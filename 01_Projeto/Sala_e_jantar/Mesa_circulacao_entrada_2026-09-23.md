# Mesa recolhida — quanto libera na entrada

23/09/2026. Cálculo sobre a geometria do site; cotas de móveis e implantação ainda não conferidas na obra. Unidade: centímetros. Eixo z cresce em direção à entrada/cozinha; centro da mesa em z=465.

| Verificação | Aberta 180 | Recolhida 150 | Mudança |
|---|---:|---:|---:|
| Ponta do tampo voltada à cozinha/entrada | z=555 | z=540 | Recua 15 |
| Ponta do tampo voltada ao sofá | z=375 | z=390 | Recua 15 |
| Frente nominal do corpo da IB6 | z=615,25 | z=615,25 | Não muda |
| Tampo → corpo da IB6 | 60,25 | 75,25 | +15 brutos |
| Extremo da cadeira de cabeceira na guarda 2+1 | z=561 | z=561 | Não muda |
| Cadeira de cabeceira → corpo da IB6 | 54,25 | 54,25 | Zero nessa faixa |
| Largura transversal reservada para entrada | 85 | 85 | Não muda |
| Ponta do banco voltada à cozinha | z=555 | z=555 | Não muda |

**Resposta:** reduzir 30 cm no total libera 15 cm de tampo em cada ponta, não 30 cm na entrada. Há ganho geométrico real junto ao tampo, mas manter a cadeira na cabeceira pode impedir que ele vire ganho na passagem do conjunto.

## Onde cada número se aplica

- Tampo x=615..690; corpo da geladeira x=584,9..645. A faixa comum x=615..645 permite comparar suas posições longitudinais. Nas quinas arredondadas pode haver folga maior; a conta usa a ponta mais avançada do tampo.
- Cadeira de cabeceira x=631,5..673,5, corpo/encosto termina em z=561 no gabarito atual. A faixa comum com a geladeira é x=631,5..645. Nesse trecho, 615,25−561=54,25 nos dois estados.
- A reserva de entrada de 85 é transversal, x=655..740, próxima da cozinha. Ela não é a mesma faixa da conta tampo–geladeira. Não soma 15 e não passa para 100.
- Banco x=685..740 e z=375..555, preservado com 180. Recolher o tampo não encurta o banco. Atrás das cadeiras laterais também não há ganho decorrente apenas desta redução, porque a largura do tampo permanece 75.

Os valores até a IB6 referem-se à frente nominal do **corpo** em z=615,25. A representação inclui puxadores mais salientes, que não foram deduzidos nesses números. Pessoas sentadas, portas abertas e percurso de giro também não foram descontados. Portanto 75,25 não deve ser anunciado como largura livre real de toda a entrada.

## Como o site representa a comparação

Seletor independente “Mesa extensível”: recolhida 150 ou aberta 180. Duas metades com cantos externos R15; folha central de 30 visível no estado aberto, centro fixo. Estado inicial recolhido. O seletor de cadeiras continua separado: guarda 2+1 ou três cadeiras na lateral. Seis lugares só com a mesa aberta; três cadeiras na lateral do tampo recolhido não significam conforto ou recolhimento validado.

As cadeiras **não são movidas automaticamente** ao recolher. Isso preserva a comparação e evita representar inserção impossível como ganho. Modelo gráfico usa cadeiras 42 × 44; o estudo de seleção trabalha com cadeira real candidata de 44 de largura e ainda exige compatibilização.

O mecanismo/base foi representado esquematicamente. Folha no banco é direção aceita, mas seu compartimento e retirada precisam ser detalhados; não foi modelado um trajeto automático fictício para guardar a folha. Dimensões estruturais do pedestal, sapata e quadro permanecem pendentes.

Fontes: geometria em [app.js](../Estudo_interativo/src/app.js), [anteprojeto](Mesa_extensivel_anteprojeto_R00.md), [comparação anterior](Mesa_extensivel_estudo_2026-09-22.md). Nenhuma medição presencial nova nesta rodada.
