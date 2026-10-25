# Guedala Park R43 — gabinete do banheiro

Revisão iniciada em 21/10/2026 e complementada em 22/10/2026 a pedido de Elias, preservando o arquivo R42 integralmente. A R43 incorpora a solução geométrica do estudo Banheiro_Detalhamento_R02, recupera a geometria da mesa/cadeiras e corrige o banco para duas tampas. As gavetas continuam aguardando os dados dos engates FGVTN.

## Sala: correções solicitadas durante a conferência

Os quinze objetos dos três cenários Berlin estavam com formas nulas na R42 carregada. Foram recuperados do arquivo `Berlin_estudo_dimensional.FCStd`, nas mesmas posições. O cenário fechado fica visível, com duas cadeiras nas pontas e uma na lateral; os dois cenários abertos permanecem ocultos. Tampo e madeira das cadeiras usam a aproximação CAD Arenza dos componentes originais; base preta e estofado claro. Referência de aprovação: `Sala_e_jantar/README.md`, registros de 18/09/2026. A mesa continua sendo superfície e envelope, sem estrutura industrial definida.

O banco tinha quatro tampas herdadas do estudo R16. As três menores foram reunidas em uma de 971 × 448 × 20 mm; a outra tem 825 × 448 × 20 mm. A junta de 2 mm permanece sobre a divisória existente, sem alterar armazenamento ou divisórias. Duas almofadas removíveis completam o assento. Controles atuais: `BancoR43_Controle`, Abertura1/Abertura2. Retirar as almofadas antes de abrir; os controles e peças anteriores ficam como histórico oculto. O ensaio em passos de 5° até 90° está em `Banco_duas_tampas.json`; não dimensiona ferragens, retenção, resistência ou ergonomia da tampa maior.

## Alteração

Duas portas de correr externas de 292 × 500 × 18 mm, com cavas sem puxadores salientes, substituem as duas folhas de giro do gabinete. A moldura frontal removível tem 600 × 70 × 543 mm e fixação por quatro M6 × 100 com porcas transversais e cavilhas de alinhamento. Trilhos RM026 e componentes RO25 estão representados por seções e envelopes de estudo.

O espaço interno de referência permanece 564 × 382 × 509 mm. Aberturas de acesso: 270 mm à esquerda e 235 mm à direita; retirada da frente proporciona 564 mm de largura. O fundo original permanece inteiro: o recorte e o sifão hipotéticos estão em grupo oculto, identificado como referência não executiva.

As duas folhas e quatro dobradiças antigas, assim como as peças substituídas da caixa, permanecem ocultas para rastreabilidade. Seus controles e os quantitativos legados R42 são históricos para esse gabinete; não contabilizar essas quatro dobradiças na compra da solução de correr. Demais candidaturas FGVTN não foram convertidas em especificação de compra.

## Operação e manutenção

No grupo `BanheiroCorrerR43`, o objeto `BC43_Controle` controla os cursos de 0 a 268 mm e de 0 a 233 mm. As portas ficam fechadas no arquivo entregue.

Para manutenção, apoiar o conjunto e prender as folhas, retirar os quatro M6, avançar a frente 20 mm, deslocar 120 mm à direita e avançar mais 330 mm. Esse percurso descreve o modelo nominal; não substitui avaliação física de peso, apoio, mãos, ferramentas e dimensões executadas.

## Conferência e limites

Os resultados calculados do gabinete estão em `Verificacao_R43.json`; essa conferência e a comparação com R42 antecedem as correções posteriores de mesa e banco, registradas separadamente. A persistência final está em `Reabertura_R43.json`. Os scripts `integrar.py` e `conferir.py` registram o método. O detalhamento e as fontes dos fabricantes permanecem em `../../../../04_Moveis/Avanco_pendencias/Banheiro_solucao/Detalhamento/Detalhamento.md`. Os erros anteriores de comparação de grupos foram corrigidos; grupos organizacionais não são comparados como sólidos individuais.

A incorporação é geométrica, não liberação de fabricação. Permanecem por validar o kit real e sua retenção, tolerâncias, material e resistência das uniões, suspensão existente, dimensões reais da porta e instalações hidráulicas. A folga nominal sob a bancada é de apenas 2 mm; deve ser compatibilizada com execução e montagem. O acesso ao sifão foi estudado com referência hipotética, não com uma instalação levantada.
