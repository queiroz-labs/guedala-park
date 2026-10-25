# Batente mecânico — estudo separado, não liberado

23/10/2026. Não foi alterado o FreeCAD. Referência: eixo ainda hipotético X100/Z430, abertura positiva de 0 a90°, duas tampas originais mantidas. Este documento não fecha a Southco nem substitui CAD real e verificação das ligações.

## Alternativa descartada

Uma chapa de contato de3mm sobre tampa teria face aberta emX107. Um batente fixo atéX107, comZ454–466, invadiria a almofada até46mm de seus50mm, deixando somente4mm de espuma. Não aprovar essa solução por conforto/durabilidade; o fato de caber geometricamente não a torna adequada.

## Solução nominal que evita esse conflito

Um batente independente por tampa, central longitudinalmente emY4236,5 eY5136,5, com suporte metálico próprio ancorado à traseira do corpo. Não usar o encosto estofado como estrutura nem atribuir capacidade de parada à dobradiça Southco.

Chapa de contato móvel de aço30×80×10mm: X118–148, Ycentro±40, Z420–430, sobre a tampa existente. Bolsa na face inferior da almofada aproximadamente34×84×12mm, sujeita a tolerâncias e revestimento, deixando38mm nominais de espessura externa. Essa bolsa não muda a altura nem o perímetro da almofada. A chapa se apoia integralmente na face superior da tampa; fixadores de localização devem ficar dentro da espessura da tampa, sem peças inferiores invadindo armazenamento. Não está especificada a união definitiva da chapa à tampa.

Batente fixo com face frontal emX100, largura80, contato emZ454–466 e corpo dentro deX84–100. O suporte inferior e a placa receptora podem seguir o princípio R47, com dimensionamento próprio: aço de8mm, largura80, receptor embutido no painel traseiro, duas linhas de ancoragem separadas80mm. Isto acrescenta dois conjuntos de suporte ao projeto. Rebaixos no painel e sarrafo, acesso à montagem, distâncias a bordas e resistência da traseira precisam ser conferidos.

A90°, a chapa móvel ocupaX100–110 eZ448–478. Sua faceX100 encontra o batente emZ454–466. O batente termina na face da reserva do encosto, não avança sob a espuma da almofada. A peça necessita janela local no revestimento do encosto; a espuma do encosto não pode ficar interposta no contato mecânico. Não foi verificado o encosto real.

## Cinemática analítica

Para ponto da chapa, dx=X−100 entre18 e48; dz=Z−430 entre−10 e0. A transformação de abertura é X'=100+dx*cos(theta)−dz*sin(theta). No intervalo0–90°, X'>=100; igualdade ocorre somente na face superior a90°. Portanto a chapa não cruza um batente confinado aX<=100 antes de90° no modelo ideal. Isto não verifica colisões do suporte completo nem da Southco real. Folga positiva desloca a parada para depois de90°; interferência negativa antecipa a parada. A tolerância tem de ser fechada na montagem com calços metálicos, não com espuma.

Esse resultado depende diretamente do eixo real. A condição geral para a face de parada terminar emX100 é t=Z_eixo−420+X_eixo−100, onde t é a altura da chapa sobre a tampa. Para eixo100430 resulta t10. Não fabricar a chapa com base na hipótese de eixo.

## Carga explícita de triagem

Adotando ação manual de100N perpendicular à tampa na borda mais afastada, braço aproximado450mm: momento45Nm. Multiplicador2 escolhido apenas para triagem resulta90Nm. Com contato nominal a30mm do eixo, força de parada3000N. Usar contato mínimo24mm na faixa proposta eleva a força3750N. Uma única parada por tampa recebe a ação completa; não dividir por dois sem demonstrar contato simultâneo.

Um suporte80×8, modelado em flexão pura por90Nm, apresenta tensão nominal105,5MPa. Isso não inclui concentrações de tensão, dobra, solda, efeito de alavanca e fadiga. Momento90Nm entre linhas de fixação separadas80mm solicita1125N por linha, ou562,5N por parafuso se houver dois parafusos efetivamente repartindo a tração. A força horizontal de3750N também precisa ser transmitida pela ligação; não foi somada automaticamente à tração, pois depende do trajeto e excentricidade reais.

Pressão média ideal sob a chapa30×80:3750/2400=1,563MPa. Não confundir esta média com verificação de esmagamento local: rigidez da chapa, contato inicial, bordas, madeira, revestimento e umidade alteram a distribuição. A resistência de material não está confirmada. Um impacto de tampa depende de velocidade, inércia e curso de desaceleração e não é coberto pelo multiplicador2. A ferragem de atrito não elimina a possibilidade de ação manual excessiva.

A chapa pesa0,1884kg para aço7850kg/m³. Seu centro nominal éX133/Z425 e sua contribuição gravitacional máxima é aproximadamente0,0617Nm por tampa. Acrescentar esta massa ao orçamento real das partes móveis; o orçamento R47 de0,5kg não deve ser tratado como comprovado.

## Estado da proposta

Há uma geometria nominal de parada90° que preserva armazenamento, dimensões das tampas e espessura externa da almofada, evitando o conflito de apenas4mm de espuma da primeira alternativa. Continua sendo proposta: faltam CAD/eixo real, interferência do conjunto completo, suporte/encosto real, definição da fixação da chapa, resistência da madeira e ensaio de parada. Não liberar para fabricação nem representar como batente aprovado.
