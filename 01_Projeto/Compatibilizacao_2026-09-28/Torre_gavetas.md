# Torre automática × gavetas — corte e implantação

28/09/2026 · Desenvolvimento técnico autônomo. [Prancha visual](Torre_gavetas.html) · [Resultados](Resultados_torre_gavetas.json).

## Direção de detalhamento

**Preservar as caixas de 50 cm e as frentes G1/G2/G3 de 16/16/40 cm.** Desenvolver a acomodação traseira antes de qualquer redução. O estudo agora explicita a cadeia de medidas, o limite de diâmetro e o conflito do uso por cima. Não foi encontrada posição integralmente validada para a variante automática preta com tomada que receba o plugue de 20 A em 127 V. Essa escolha funcional continua vigente.

## 1. Corte explícito: de onde vêm os 9,2 cm

Hipótese de construção para este corte: parede t=0; face externa da frente aplicada t=61; frente aplicada de 1,8; caixa encostada atrás dela, sem recuo extra; caixa externa com 50. Assim, a caixa ocupa **t=9,2 a 59,2 cm**. Pedra até t=63, deixando 2 cm além da frente. Os 61 cm são a referência frontal adotada neste novo ensaio, não medida executiva ou extração do 3D. O modelo ilustrativo existente não fecha esses mesmos planos; não se misturaram suas coordenadas com este corte.

**61 − 1,8 − 50 = 9,2 cm** entre parede e traseira da caixa. Um painel traseiro de 1,8 encostado na parede deixa **7,4 cm livres**. Recuo adicional da caixa reduz a faixa na mesma proporção. Rodabanca e fundo do móvel são obstáculos diferentes e em alturas diferentes. Travessas, tubulações, suportes e fixações não podem ocupar essa reserva.

Ensaio de montagem: 5 mm livres por lado do corpo, sem natureza normativa e sem comprovar acesso da mão ou ferramenta. Para um envelope instalado D, o critério local é **D ≤ 61 − 1,8 − 50 − recuo − fundo − 2 × 0,5**. O envelope precisa incluir o anel em sua altura real, não apenas o cilindro.

| Fundo traseiro | Recuo da caixa | Faixa livre | D máximo com 5 mm/lado | Saldo diante de corpo Ø6,4 |
|---:|---:|---:|---:|---:|
| 0 | 0 | 9,2 | 8,2 | 1,8 |
| 0 | 0,5 | 8,7 | 7,7 | 1,3 |
| 0,6 | 0 | 8,6 | 7,6 | 1,2 |
| 0,6 | 0,5 | 8,1 | 7,1 | 0,7 |
| 1,8 | 0 | 7,4 | 6,4 | 0 |
| 1,8 | 0,5 | 6,9 | 5,9 | -0,5 |

Com fundo de 18 mm e recuo zero, **Ø6,4 só cabe no limite**, com eixo em t=5,5 e sem tolerância adicional. Com recuo de 5 mm, já faltam 5 mm. Anel de Ø8,0, por exemplo hipotético, pediria mais 1,6 cm de faixa nesse caso. Um fundo de 6 mm aumenta D máximo para 7,6 cm; ausência de fundo nessa região aumenta para 8,2 cm. São comparações construtivas: não foi decidida remoção de fundo ou travessa estrutural.

Laterais da caixa: vão do gabinete 58,3; caixa externa 55,7; sobra de 1,3 cm por lado já destinada à ferragem. Não há corredor lateral para um corpo de 6,4 cm. A localização frontal C invade a projeção das caixas. Na localização traseira, a caixa se afasta da coluna ao abrir: varridos cursos de 0 a 50 cm, com folga mínima fechada de 5 mm; curso comercial, ferragens, cabo e desmontagem continuam a conferir.

## 2. O que a ficha da torre permite concluir

A [ficha oficial QTMOV](https://qtmov.com.br/midias/produtos/arquivos_download/mini-totem-automatico1.pdf), arquivada em [Fontes_torre/QTMOV_ficha_10A.pdf](Fontes_torre/QTMOV_ficha_10A.pdf), é das referências QM12200.00/.01/.02 **10 A**. Ela fornece furo Ø6,5, tampa Ø7,6, corpo Ø6,4 e, no desenho, 20,6 abaixo da aba mais terminal de 3,5. O total de referência abaixo da aba é **24,1 cm**, não os 33,41 cm de altura geral do texto. A cadeia vertical do desenho também contém a cota 29,8 que não fecha exatamente com 8,98 + 0,33 + 20,6; manter essa diferença documental em aberto. Não há corte cotado dos dois estados nem diâmetro do anel. **Não transferir essas dimensões para uma variante 20 A sem confirmação.**

Com aba apoiada a z=92, esse ensaio põe a base do corpo em **z=71,4** e o fim do terminal em **z=67,9**. Pedra de 2 cm deixa 22,1 cm do envelope sob sua face inferior. Isso cruza as faixas frontais G1 (74–90) e G2 (58–74). G3 fica em 18–58 neste empilhamento ilustrativo, sem juntas; alturas reais das caixas são diferentes das frentes e continuam a detalhar. Por isso, eventual conflito não justifica automaticamente encurtar G3 ou as três caixas. A curva do cabo, seu raio mínimo e manutenção podem ampliar a reserva; não foram inventadas cotas para eles.

O [manual QTMOV](https://qtmov.com.br/manuais/mini-totem-automatico/) e seu [PDF arquivado](Fontes_torre/QTMOV_manual.pdf) mostram fixação com anel por baixo da pedra, exigindo passagem do cabo e acesso para apertar/soltar. O PDF diferencia modelos 10/20 A e limita a versão 20 a **2032 W em 127 V**. Air fryer de 1400 W representa cerca de **11,02 A**, excedendo os 1270 W da versão 10 A em 130 W. A diferença aritmética de 632 W no modelo 20 não autoriza outro aparelho simultâneo.

A [página da família](https://qtmov.com.br/torre-de-tomada/) menciona versões 20 A; a [página individual](https://qtmov.com.br/produtos/linha-pratik/mini-totem-automatico/) ainda descreve 10 A. O código exato preto 20 A permanece sem vínculo dimensional comprovado. A [Soprano 06910.0200.79](https://www.soprano.com.br/acesso-e-seguranca/acessorios-para-moveis/iluminacao-e-energizacao/torre-de-tomada/06910.0200.79_torre-de-tomada-de-embutir-3-modulos-de-energia-preta) tem furo de 6 cm, mas anuncia compatibilidade com plugue 16 A; não comprova receber diretamente o plugue 20 A solicitado. Não foi selecionada.

## 3. Por cima: a faixa traseira está muito apertada

Coordenadas s a partir do preparo junto à geladeira; t a partir da parede. Purificador s=5–21/t=10–52; air fryer temporária s=31–57,4/t=10–46; cuba externa s=72,9–115,9/t=13–50. Tampa de Ø7,6 usada somente como referência geométrica.

A página do manual QTMOV publica afastamento de **60 cm de áreas úmidas**, frase ausente no PDF consultado. Tratar como instrução publicada desse fornecedor a esclarecer, não como regra universal de instalação atribuída aqui à NBR. O teste usa distância mínima entre borda da tampa e retângulo externo da cuba. É só condição necessária nessa interpretação: torneira, respingos, área molhada real e critério de medição do fabricante podem exigir mais.

| Centro de teste (s;t) | Até cuba, borda a borda | Até corpo do filtro | Invade projeção da caixa? | Resultado |
|---|---:|---:|---|---|
| A: (8, 5,5) | 61,53 | 0,7 | Não | Atrás do filtro: tampa invade 3 mm da rodabanca de teste; acesso frontal à tomada fica oculto pelo aparelho. |
| B: (26, 5,5) | 43,7 | 2,93 | Não | Entre aparelhos por cima, mas não atende ao ensaio de 60 cm até a cuba. |
| C: (8, 57) | 61,48 | 1,2 | Sim | À frente do filtro: invade o volume horizontal das caixas; passagem da mão e plugue também não demonstrada. |

Em t=5,5, atender ao ensaio dos 60 cm exige **s ≤ 9,54 cm**, empurrando a torre para trás do filtro. A posição A deixa 7 mm até o corpo do filtro, mas sua tampa invade em 3 mm uma rodabanca hipotética de 2 cm. Para manter 5 mm até a caixa, a rodabanca teria que ter **no máximo 1,7 cm**, ainda sem folga para a tampa. Essa espessura não foi escolhida nem medida. Com 2 cm de rodabanca, o centro teria que ir a t≥5,8; o cilindro chegaria a t=9,0, deixando só 2 mm até a caixa, abaixo da reserva de montagem do ensaio.

A torre aberta de cerca de 9 cm fica atrás do filtro de 35 cm. Acesso ao botão, orientação da tomada, plugue e retirada da mão não foram demonstrados. Não considerar as reservas de ventilação/manutenção do filtro como espaço livre automaticamente disponível. A posição B evita estar diretamente atrás do filtro, mas falha no teste de água; a posição C passa nesse teste limitado, porém atravessa a projeção das gavetas. **Nenhum dos três pontos vira centro de furação.**

## 4. Solução de projeto preparada para a próxima conferência

1. Manter a seção proposta 61/63 e caixas de 50 como objetivo, com 9,2 cm brutos atrás. Especificar fundo e travessas localmente antes de fechar o espaço de serviço.
2. Para conservar fundo de 18 mm, exigir envelope instalado no trecho das caixas de até 6,4 cm com o recuo zero do ensaio — critério muito restritivo, não cabimento comprovado. Com fundo de 6 mm, teto dimensional de 7,6 cm; com faixa traseira livre, 8,2 cm. Anel e acesso de ferramenta podem exigir espaço adicional em outra altura.
3. Confirmar modelo automático preto, entrada/saída para uso 127 V e aceitação direta do plugue 20 A; obter desenho instalado aberto/fechado com aba, anel, cabo, espessura de pedra admitida e acesso de manutenção. O furo permanece sem posição e diâmetro executivo.
4. Resolver implantação superior no mesmo desenho do purificador e da rodabanca, verificando os 60 cm publicados, água e acesso. Não avançar furação apenas porque o cilindro coube por baixo.
5. Somente se o envelope real falhar: estudar interferência localizada em G1/G2 com todas as partes móveis e cabo antes de reduzir G3. Cortar 5 cm nas três caixas retiraria **10,64%** da área interna de cada uma; nenhuma redução aplicada.

### Consulta técnica pronta, ainda não enviada

Para o fabricante: identificar o código atual preto, automático por pressão, que receba plugue brasileiro de 20 A e permita 1400 W em 127 V. Enviar seção instalada em ambas as posições com envelope máximo sob a pedra, diâmetro e altura do anel, faixa de aperto, saída/curvatura do cabo e espaço para manutenção. Confirmar os 2032 W e explicar a divergência 10/20 A entre páginas. Esclarecer o afastamento de áreas úmidas publicado online, sua medição e aplicação à cuba/purificador.

Para a marcenaria: conferir os planos 61/63, frente aplicada 18 mm, caixa externa 500 mm, recuo real, espessura/posição do fundo e travessas. Retornar corte com faixa livre contínua e meio de acessar anel e alimentação após retirar G1/G2; demonstrar extração, curso e folgas com a torre e seu cabo. Não abreviar a caixa de G3 para orçamento.

## Verificação e limites

Script sem dependências: node 01_Projeto/Compatibilizacao_2026-09-28/calcular_torre_gavetas.cjs. Cinco conferências passaram: distância a retângulo, curso, limite dos 60 cm, sensibilidade do fundo/recuo e interferência frontal. Geometria é documental, sem medição da unidade, peça física ou validação estrutural/elétrica. Fontes oficiais consultadas em 28/09; não houve compra, contato ou aprovação de produto. Próxima frente independente: mecanismo do cesto e retirada do saco sob o tanque.
