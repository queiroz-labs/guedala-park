# Fixação das frentes P01/P06 — proposta para compensação de 3 mm

T05, 26/10/2026. [Mapa de 28 pontos, coordenadas e margens](Fixacao_frentes.json), calculado sobre a proposta de caixas500 e a base R52 de mesmo hash. Sem abrir ou alterar o FreeCAD. Quatro pontos por frente são uma disposição candidata, **não dimensionamento de capacidade ou receita de fabricação**.

## Como a compensação funciona

A frente interna da caixa tem 16 mm e a decorativa18 mm; suas faces encostam nominalmente. A proposta usa parafusos de dentro para fora, com cabeça de apoio plano e arruela, passagem folgada somente na frente interna e ancoragem cega na decorativa. A face externa permanece sem furo passante.

A passagem proposta é circular **Ø8 mm**, não rosca na chapa interna. Seu centro acompanha a caixa. Com caixa no ajuste zero, o eixo do parafuso fica **1,5 mm acima** do centro da passagem; quando a caixa sobe3 mm e a frente é realinhada, o eixo fica1,5 mm abaixo. Assim, a compensação é centrada no furo. Não confundir com abrir o piloto no centro da passagem em ajuste zero: isso consumiria metade da faixa desejada.

A montagem precisa ser afrouxada, sustentada, realinhada e reapertada. Não há deslizamento controlado sob aperto, nem regulagem automática. A posição vertical final depende da retenção por aperto, ainda não comprovada em chapa real. O grupo de quatro pontos não demonstra resistência a puxadas, peso da frente, excentricidade, impactos ou fluência.

## Disposição por frente

Coordenadas locais medidas na **frente interna proposta**, em X global crescente a partir da borda X mínima e Z a partir da borda inferior; não interpretar direita/esquerda pela vista de quem monta. Eixo de furação: −Y global. São quatro combinações das duas colunas com as duas linhas:

| Gavetas | Largura × altura da frente interna | Colunas X locais | Linhas Z da passagem, ajuste zero |
|---|---:|---:|---:|
| P01, quatro caixas | 314 ×73 | 40 e274 | 15 e58 |
| P06 G3 / Gaveta004 | 542 ×273 | 40 e502 | 15 e258 |
| P06 G2 / Gaveta005 | 542 ×73 | 40 e502 | 15 e58 |
| P06 G1 / Gaveta006 | 542 ×53 | 40 e502 | 15 e38 |

Todas as cotas em mm. O eixo cego na frente decorativa fica em Z da passagem +1,5 na posição nominal. O JSON identifica os objetos, coordenadas globais e comprimentos candidatos para cada ponto. As frentes e o conteúdo não mudam de dimensão ou posição nominal. Furos já existentes, juntas, perfis de pega e usinagem da peça importada G2 precisam ser conferidos em sólidos antes de aplicar: envelopes não revelam essas particularidades.

## Envelopes dimensionais de estudo

Estes números são hipóteses de seleção/verificação, **não dados de um SKU escolhido nem tolerâncias declaradas por fabricante**. Produto real, material da chapa e processo ainda devem ser especificados.

| Componente | Envelope considerado |
|---|---|
| Parafuso | Nominal4; maior diâmetro que atravessa a passagem até4,3; cabeça de apoio plano, diâmetro mínimo7,5 e máximo15; altura máxima2,9 |
| Arruela | Externo entre14,4 e15; furo entre4,4 e4,8; espessura nominal1,2 e máxima1,4 |
| Erro horizontal combinado | Até0,5 entre eixo da haste e passagem |
| Posição vertical relativa | ±1,5 em torno do centro da passagem, correspondente à compensação0…3 |
| Excentricidade da arruela | Até0,4 em relação à haste nominal4, por folga no furo4,8 |
| Ferramenta auxiliar | Haste hipotética Ø12 ×100; não representa cabo, mão nem máquina |

Com distância radial `sqrt(1,5² + 0,5²) = 1,581 mm`, as margens calculadas são:

- haste até borda da passagem: **0,269 mm**;
- cobertura radial mínima da passagem pela arruela, incluindo excentricidade: **1,219 mm**;
- sobreposição radial mínima da cabeça sobre o furo da arruela: **0,95 mm**;
- folga radial no alojamento G2 abaixo, incluindo movimento e excentricidade: **0,519 mm**.

Essas margens não incluem variação adicional do Ø8, erro vertical além da faixa, desgaste ou ovalização. Não somar tolerâncias de processo por fora e assumir que ainda cabe. Cabeça escareada não integra esta hipótese: não deve recentrar a frente no furo folgado nem substituir a superfície plana de aperto.

## Particularidade G2: duas cabeças baixas

As bandejas têm somente2 mm entre sua parede frontal e a face interna da dianteira da caixa. Um conjunto arruela/cabeça saliente de até4,3 mm encontra os envelopes `OrganizadorG2R013` e `OrganizadorG2R003` nos dois pontos baixos. Retirar bandejas para apertar não resolve essa interferência quando forem recolocadas.

A alternativa candidata é **alojamento circular Ø20 ×5 mm**, pela face interna da dianteira, apenas nesses dois pontos; a passagemØ8 continua pelo material restante. Alojamento e passagem têm o mesmo centro e acompanham a caixa. A arruela continua cobrindo a passagem ao longo do realinhamento, sem encostar na parede do alojamento dentro das hipóteses.

- espessura residual da frente interna: **16−5 =11 mm**;
- ligamento nominal do alojamento até a borda inferior: **15−10 =5 mm**;
- cabeça + arruela até4,3: **0,7 mm recuados** da face interna;
- nominalmente, **4×25** nestes dois pontos e **4×30** nos outros26, com arruela1,2.

Cadeias nominais: `30−16−1,2 =12,8` e `25−(16−5)−1,2 =12,8 mm` de entrada na frente decorativa; sobra nominal externa `18−12,8 =5,2 mm`. A entrada inclui a ponta e não equivale a comprimento de rosca eficaz. Não usar30 nos alojamentos5: essa troca reduziria a sobra nominal externa a0,2 mm. Confirmar comprimentos reais, ponta, espessuras acabadas e batente de profundidade antes de qualquer furação. Diâmetro/profundidade do piloto e torque **não foram definidos**.

A seção residual11 e o ligamento5 são pontos de validação de esmagamento, fissura e retenção; a simples existência de material não prova adequação. Caso a chapa/fixador não sustente essa solução, revisar a implantação ou a fixação antes de adotar o rebaixo. Não remover material do fundo G2 nem deslocar bandejas para acomodar cabeças.

## Acesso e conferência realizada

Para os28 pontos, os envelopes de arruela/cabeça cobrem a faixa relativa vertical±1,5, erro horizontal0,5 e excentricidade da arruela0,4. Com os dois alojamentos G2, não houve encontros com os envelopes de madeiras/conteúdos selecionados da própria gaveta. O volume do alojamento dentro da dianteira é uma usinagem proposta, excluída da comparação intencionalmente; sua existência ainda não está no CAD.

A haste auxiliar Ø12 ×100 encontra conteúdos e, nos pontos baixos G2, as paredes frontais das bandejas. **Esvaziar antes do serviço e retirar as duas bandejas G2**. Após excluir conteúdos/bandejas, não houve encontros com as madeiras selecionadas da própria caixa. Isso não comprova acesso do cabo/mão, abertura da porta, espaço externo ou presença de furos e fixadores antigos.

Foram usados apenas os dados salvos, sem novas booleanas. Engates T51 e corpos FGVTN não integram essa prova. Fixação frontal e engates ficam em regiões diferentes, mas ainda é preciso conferir o produto real; não inferir independência espacial absoluta. Reproduzir: `python -B ferramentas/detalhar_fixacao_frentes.py`.

## Sequência e pendências

1. Definir produto, chapa e processo; conferir os28 pontos contra a usinagem real, especialmente a dianteira importada G2. Validar seção11/ligamento5 e retenção em corpo de prova antes de usinar as peças finais.
2. Montar e regular a caixa conforme a ferragem correta. Apoiar a frente externamente, usar referências das juntas nominais e marcar os pilotos na decorativa na posição correspondente ao ajuste efetivo. Não marcar simplesmente pelo centro doØ8.
3. Executar pilotos cegos com batente segundo chapa/parafuso validados; sustentar a frente, instalar arruelas e apertar progressivamente com torque qualificado. Não usar a força dos parafusos para corrigir uma caixa fora de esquadro.
4. Para reajuste: retirar conteúdo/bandejas, apoiar a frente, afrouxar os quatro pontos, ajustar a caixa e realinhar a frente, reapertar e conferir juntas. Nunca subir a frente solidária contra as prateleiras P01 ou a bancada P06.
5. Verificar retenção, repetição de ajuste, marcas, esmagamento, puxadas e curso com protótipo real. Não há resultado de ensaio preenchido.

O avanço independente da FGVTN é o mapa, a cadeia de ajuste, a interferência com bandejas e a alternativa de alojamento. Continuam pendentes seleção/validação do fixador e da chapa, tolerâncias de usinagem, acesso real e montagem do engate. **Ainda não é o momento de integrar no FreeCAD principal:** aplicar após esses detalhes e a sequência de retirada estarem definidos, com pedido explícito e verificação completa, conforme o [marco de integração](Ajuste_vertical_e_retirada.md#melhor-momento-para-alterar-o-freecad).
