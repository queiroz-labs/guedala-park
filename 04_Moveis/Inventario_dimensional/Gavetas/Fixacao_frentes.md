# Fixação das frentes P01/P06 — proposta para compensação de 3 mm

T05, 26/10/2026. [Mapa de 28 pontos, coordenadas e margens](Fixacao_frentes.json), calculado sobre a proposta de caixas500 e a base R52 de mesmo hash. Sem abrir ou alterar o FreeCAD. Quatro pontos por frente são uma disposição candidata, **não dimensionamento de capacidade ou receita de fabricação**.

## Validação documental e dimensional — 26/10/2026

**Resultado: os 11 mm restantes não têm resistência demonstrada.** A geometria candidata continua separada do CAD. [512 combinações extremas e comparação de arruelas](Validacao_fixadores_G2.json) delimitam as margens; não fornecem capacidade. A comparação de rebaixo3,5 abaixo é uma alternativa a aprofundar, sem substituir o mapa de28 pontos ou adotar nova usinagem.

### Fixadores reais versus envelope do estudo

| Fonte consultada | Evidência | Resultado para esta montagem |
|---|---|---|
| RECA [01814 25](https://shop.reca.fr/Pan-head-chipboard-screw-A2-Pozidriv/01814%20%2025.sku/en/US/EUR/) e [01814 30](https://shop.reca.fr/Pan-head-chipboard-screw-A2-Pozidriv/01814%20%2030.sku/en/US/EUR/) | Parafusos para madeira4×25/30, cabeça panela nominalØ8×2,8, acionamentoZ2, A2 | Candidatos documentais: dimensões nominais de cabeça/diâmetro compatíveis com o envelope. Faltam tolerâncias, diâmetro do pescoço sob a arruela, ponta/rosca útil, retenção e torque para a chapa. Não é seleção de compra |
| [Bossard, arruelas largas](https://nederland.bossard.com/en-us/standard-fastening-elements/washers/washers-flat-without-chamfer/9021a0a2) | M4:4,3×12; M5:5,3×15 | A arruela hipotética externa15/furo4,4–4,8 não corresponde automaticamente a essas séries |
| [Accu HPW-M4-V2-A4](https://www.accu.co.uk/metric-flat-washers/406775-HPW-M4-V2-A4) | Externo12 com desvio−0,43; furo4,3 com desvio+0,18; espessura1,1 com desvio−0,2 | No pior caso de centragem pelo diâmetro4, cobertura radial calculada doØ8 é **−0,036 mm**. Não atende ao critério de cobertura integral adotado |

Para a M5 nominal5,3×15, a cobertura doØ8 é1,269 mm, mas sobra apenas0,269 mm até a parede do alojamentoØ20, supondo centragem por diâmetro4. Se o pescoço sob a arruela for3 mm, essa folga vira **−0,231 mm**. São comparações nominais, sem tolerâncias da M5: não aprovar a troca só pelo diâmetro externo15. O cálculo anterior de excentricidade0,4 pressupunha diâmetro de centragem4 e furo máximo4,8; essa combinação precisa existir no conjunto real.

A página RECA foi obtida por conteúdo indexado; a abertura direta falhou. Não foram obtidos certificados dimensionais, desenhos de tolerâncias nem propriedades mecânicas aplicáveis à chapa. Nenhum produto comprado ou fornecedor contatado.

### O que os 11 mm precisam resistir

A frente interna tem passagemØ8: **não é nela que a rosca deve ancorar**. Seus11 mm residuais recebem pressão da arruela e esforços locais de flexão, esmagamento e atravessamento. A rosca prende na frente decorativa18, com entrada nominal12,8 incluindo a ponta. Qualificar arrancamento nesta frente não demonstra resistência do alojamento na outra peça.

A [European Panel Federation — fabricação do MDF](https://mdf-info.eu/general/manufacturing-of-mdf) descreve diferenças de densidade entre face e miolo. Rebaixar5 mm remove a face original; não tratar o assento usinado como superfície intacta nem usar apenas densidade média para provar capacidade. É necessário identificar substrato, classe, espessura acabada e propriedades da chapa concreta; o acabamento não resolve essa identificação.

A [orientação EPF de parafusamento](https://mdf-info.eu/using-mdf/fixing/screwing) trata piloto em função do núcleo do parafuso e recomenda profundidade além da inserção. Suas recomendações gerais de distância às bordas dizem respeito a parafusos no painel, não certificam um alojamentoØ20 a5 mm da borda. A [descrição dos ensaios EPF](https://mdf-info.eu/technical/assessing-properties) usa condições padronizadas de inserção; não converter a resistência publicada de outro ensaio em carga de uso destes28 pontos. Não foi especificado piloto nem torque nesta etapa.

Como diagnóstico, a área plana de apoio tem limite inferior geométrico de94,50 mm² no envelope anterior: `π/4 × (14,4² −8² −4,8²)`. Subtrair integralmente os dois furos, mesmo quando se sobrepõem, torna o valor conservador. Pressões médias correspondentes a **pré-cargas hipotéticas por ponto** de100/250/500 N são até1,06/2,65/5,29 N/mm². Não são forças de uso, torques recomendados ou pressões admissíveis. O modelo pressupõe assento plano íntegro e arruela rígida; não prevê picos locais, perda de aperto, fluência ou fissura. Sem resistência aplicável e pré-carga real, não existe fator de segurança demonstrado.

### Cadeia de tolerâncias e alternativa menos profunda

Os intervalos seguintes são **hipóteses de sensibilidade**, não medições nem tolerâncias aprovadas: frente interna15,7–16,3; decorativa17,7–18,3; profundidade do rebaixo nominal±0,2; comprimento do parafuso nominal±0,3; arruela1,0–1,4; cabeça2,7–2,9; vão da bandeja1,5–2,5 mm. Foram128 combinações extremas por caso.

| Rebaixo / parafuso | Chapa interna restante | Entrada incluindo ponta | Sobra externa mínima | Folga mínima até bandeja |
|---|---:|---:|---:|---:|
| Base5 /25 | 10,5–11,5 | 11,8–13,8 | 3,9 | 1,5 |
| Comparação3,5 /25 | 12,0–13,0 | 10,3–12,3 | 5,4 | 0,5 |
| Comparação3 /25 | 12,5–13,5 | 9,8–11,8 | 5,9 | **0** |
| Erro de montagem5 /30 | 10,5–11,5 | 16,8–18,8 | **−1,1** | 1,5 |

Cotas em mm. A sobra externa após um piloto hipotético1 mm além da ponta cairia mais1 mm: mínimos2,9/4,4/4,9/−2,1, respectivamente. Isso é reserva dimensional, não receita de piloto. O erro25→30 atravessa a frente em52 das128 combinações; a comparação3 chega a contato com a bandeja em8 delas. Não misturar os comprimentos dos dois tipos de ponto.

O rebaixo3,5 deixa **12,5 mm nominais** e mantém o ligamento inferior5 mm, pois diâmetro/posição não mudam. A cabeça pode ficar saliente, mas dentro do vão testado. A condição geral é `vão mínimo − max(0, cabeça máxima + arruela máxima − rebaixo mínimo) > reserva exigida`. Nesta sensibilidade, o resultado mínimo é0,5 mm; não há tolerância extra a acrescentar sem recalcular. A menor entrada de rosca e a mesma borda inferior ainda exigem verificação: mais espessura local não prova uma ligação melhor em todos os modos.

**Próximo passo independente da FGVTN:** fechar o conjunto dimensional parafuso/arruela e o substrato real; só então escolher entre rebaixo5, comparação3,5 ou outra implantação. Reproduzir a sensibilidade com `python -B ferramentas/validar_fixadores_g2.py`. A validação física da retenção e da região usinada continua pendente; não fabricar nem incorporar o alojamento com base apenas nestes números.

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
