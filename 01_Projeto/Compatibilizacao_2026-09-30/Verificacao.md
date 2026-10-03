# Verificação — 30/09/2026

## A — formas leves

`formas_a.cjs`: fechamento dos três canais de 8,8, limites de 32,2/7,8/45,8 e pizza deitada com saldo 1,4/deficit 2,6 conferidos. Percurso isolado de dois envelopes em 404 posições verifica teto e passagem sobre quatro bordas/separadores no corte profundidade/altura; frente sem outras peças. Não é simulação completa de pessoa, porta, geladeira ou contenção. Inclinação de 0°/5°/10° calculada separadamente. HTML/MD e links locais conferidos; sem renderização visual inspecionada. Referência Ø30 recuperada de decisão local, sem consulta externa.

## B1/B2 — pilha e caixas

`node 01_Projeto/Compatibilizacao_2026-09-30/b1_b2.cjs` executado com assertivas de diâmetro 27,4, altura 22,5, intervalo B2 de 4,1 e três caixas dentro dos limites. Sensibilidade de altura 17,6/21/24,4 para h inicial=4 e acréscimo médio 0,8/1/1,2; massas hipotéticas calculadas sem tratar como carga admitida. Links de B1/B2 e C3 conferidos após regeneração; `git diff --check` sem erros. Sem renderização visual inspecionada ou validação de peças, carga e alcance reais.

## C3 — panos e potes

`node 01_Projeto/Compatibilizacao_2026-09-30/c3_reserva.cjs`: assertivas aprovadas para fechamento das larguras 51,1/48,6, bandejas 30/27,5, envelopes de uma/duas pilhas e limite vertical de 22,4. Sensibilidades de encaixe calculadas para h1=8 e acréscimos 1/1,5/2. HTML estático e resultados reproduzíveis. Conferidos destinos dos links locais e limites dos três envelopes desenhados dentro da bandeja. Sem renderização visual inspecionada nesta rodada, sem medidas reais de objetos, teste físico, pesquisa externa ou liberação de fabricação.

## Continuação: operação em planta

- Commit de partida `571da11` criado a pedido de Elias; árvore limpa confirmada antes do novo assunto. Sem push ou publicação nesta rodada.
- `operacao_lavanderia.cjs`: cinco relações de interseção dos gabaritos de pessoa passaram; faixa disponível do banquinho confrontada com seus 45 cm. Polígono do saco recortado em 891 posições contra a faixa da lixeira; folga vertical mínima de 18,266 cm confrontada com equação analítica da aresta, diferença menor que 1e-8 cm. Tampa fechada e envelope carregado idealizado.
- Planta inspecionada em 1280 px, com textos ampliados após primeira conferência. Duas cenas legíveis; largura útil 1265 px, sem transbordamento horizontal. Versão móvel não inspecionada visualmente.
- Base de 154 cm separada dos 161 cm do modelo 3D. Lixeira normalizada pelas margens de canto; posição não medida. Reserva da porta não foi tratada como setor de giro real. Não foram modelados antropometria, mãos, apoio/transporte do saco, porta exata ou roupa no varal.
- Novos arquivos de operação e atualizações dos índices permanecem posteriores ao commit de partida, para revisão. `git diff --check` sem erro, somente avisos LF/CRLF.

## Cesto e retirada

- Base documental local R04/R05/R08 e decisões vigentes conferidas. Dimensões aprovadas separadas das novas hipóteses de frente, painel, rodapé, aro e corpo carregado do saco. Sem fonte comercial nova ou produto selecionado.
- Giro: 5.501 posições entre 0 e 55°, passo 0,01°, com interseção de polígonos completos pelo teorema dos eixos separadores. Cesto e frente confrontados com pedra, tanque, reserva hidráulica alta/posterior, base, painel e rodapé. Zero interseções nos obstáculos idealizados.
- Rodapé modelado como painel y=56,2–58, topo z=11. Não foi representado como bloco maciço ocupando a caixa interna. O cesto nunca desce de z=12; a frente passa adiante da base/rodapé recuados. Apoios, pegas e ferragens não modelados permanecem fora dessa conclusão.
- Saco: 891 posições na extração axial e 551 no endireitamento, total 1.442 amostras. Após sair do aro, incluída verificação de não retorno ao volume do cesto, além dos obstáculos fixos e frente móvel. Justificativa por coordenadas locais documentada para complementar a amostragem.
- Seis conferências matemáticas passaram: SAT com cruzamento de arestas sem quinas internas; invariância/pico da rotação; giro sem interseções; extração e rotação do saco; reserva de 3+1 cm até painel; perda de folga ao puxar apenas verticalmente. Momento gravitacional calculado como sensibilidade, sem selecionar capacidade de ferragem ou fixação.
- Prancha inspecionada em navegador de 1280 px: corte aberto/fechado, saco em início/fim de extração e em pé; controles alteram figuras, valores e etapa. Saldo da interface considera pedra/frente/saco, para não sugerir passagem maior quando um elemento mais profundo permanece no caminho. Diagramas com rolagem própria em telas estreitas; versão móvel não inspecionada visualmente.
- Fonte, memória, tabelas e índices atualizados em conjunto. Conferidos 329 links locais, sem destino ausente; `git diff --check` sem erro (apenas avisos de LF/CRLF). Documento com 1265 px de largura útil em janela de 1280, sem transbordamento horizontal; nenhum aviso/erro de JavaScript capturado.

Não há demonstração de conforto para uma pessoa, deformação do saco cheio, alças/mãos, perfil de ferragens, contrapeso Telca, estrutura, capacidade de carga, medida em obra ou furação executiva. Não houve publicação ou contato com fornecedores.


## Continuação: alternativa do banquinho

- Script `banquinho_alternativa.cjs` executado: 151 posições da retirada reta, zero colisões com os envelopes de cama, cadeira e bancada. Separação analítica documentada. Distância mínima conservadora ao disco da porta: 85 cm.
- Giro rígido do sofá: círculo envolvente fornece folga conservadora de 34,7834 cm até a reserva guardada. Operador e mecanismo de abertura não incluídos.
- Quatro combinações dos controles da prancha verificadas com DOM simulado: 63, 48, 98 e 113 cm. Links da nova prancha e memória conferidos no disco. Isso verifica lógica, não renderização.
- Inspeção visual não realizada: navegador recusou URL local file: por política de protocolo. Não houve tentativa de contornar o bloqueio.
- Nenhuma consulta Firecrawl ou web. Novos arquivos e registros mantidos locais, posteriores ao commit 571da11.


## Continuação: pessoa e transporte do banquinho

- `banquinho_operacao.cjs`: quatro etapas, 804 amostras por cenário; gabarito 40 × 50 sem colisão com cama/cadeira/bancada e sem ultrapassar o cômodo. Continuidade exata entre etapas conferida. Separação analítica registrada na memória.
- Sensibilidade de profundidade 30/35/40/45/50: 45 toca a cama; 50 produz colisões, confirmando rejeição de gabarito excessivo. Larguras 45/50/55 avaliadas; 55 alcança a soleira no ponto final. Vão apenas idealizado; cruzamento e área externa não simulados.
- Links da nova prancha e memória conferidos. Prancha estática em quatro cenas, sem controles novos. Renderização visual não verificada; bloqueio anterior do navegador para arquivos locais não foi contornado.
- Sem pesquisa externa, fabricação ou alterações de escolhas aprovadas.


## Continuação: luz da lavanderia e varal

- `luz_varal.cjs`: limites de corpos 14/28/35/40/41; faixa com margens de 5; duas posições para corpo de 28.
- Interseção segmento/caixa conferida com caso positivo e negativo. 149 emissores × 9 alvos = 1.341 segmentos por cenário; cinco expansões de roupa e duas posições, 13.410 trajetos. A ausência de sombra da roupa até avanço 10 (y=60) e 15 (y=55) confirmada por separação analítica em planta.
- Obstruções do aéreo computadas separadamente: 13 e 72 segmentos nas duas posições. Sem pesos fotométricos ou resultados em lux. Duto, chapa, pessoa e ferragens não modelados.
- Links da nova prancha e memória conferidos. Prancha estática; renderização visual não inspecionada. Nenhuma pesquisa Firecrawl/web ou seleção comercial.


## Continuação: folha da mesa no banco

- `folha_mesa.cjs`: 1.402 posições; interseção detectada com cadeira original e zero após recuo temporário de 5. Outras duas cadeiras confrontadas. Distância mínima ao eixo da coluna 10,7, confirmada pela separação longitudinal.
- Sensibilidade de diâmetros 12/15/20/25/30; nenhum diâmetro estrutural selecionado. Ganho de 15 cm ao retirar antes de abrir a mesa. Pessoa, portinhola, estrutura e apoio temporário não simulados.
- Links da prancha e memória conferidos; renderização visual não inspecionada. Sem consulta externa ou alteração do site.


## Continuação: apoio temporário da folha

- `apoio_folha.cjs`: conflito da folha apoiada com cadeira recuada apenas 5; separação após recuo de 41. Conflito da central no vão final e separação após recuo de 32,5. Envelopes conservadores até altura 94, sem contorno real.
- Círculo envolvente do giro: raio 40,3887; separações conservadoras 3,1113 da faixa longitudinal da cadeira e 3,9262 do corpo fechado da geladeira. Percurso elevado a 97–100, sem simular pessoa.
- Folha sobre uma metade fora da junta e dos cantos R15; verificação em 151 posições da abertura nominal. Atrito, retenção, carga, curso extra e possibilidade de operar com folha apoiada não validados.
- Links da nova memória/prancha encontrados. Renderização visual não inspecionada. Sem Firecrawl ou alteração do site.


## Mesa — consolidação solicitada

- `mesa_completa.cjs`: 2.010 posições, dez transições, polígonos orientados por SAT e intervalos verticais. Zero colisões com obstáculos idealizados; limites de parede/trecho conferidos. Folga analítica no giro à parede: 4,611264 cm.
- Apoio no assento separado 5 cm do tampo durante a abertura; superfície plana de teste, sem prova de estabilidade no estofado. Folha elevada a 97–100, acima de encostos e abaixo do pendente de referência. Coluna/nicho continuam condicionados aos volumes reais.
- Sete estados do seletor verificados em DOM simulado: títulos, quatro vértices e alturas corretas. Links locais e âncoras encontrados. Isso verifica comportamento, não renderização; inspeção visual ainda não realizada.
- Históricos apontam para a consolidação. Sem pesquisa externa, fornecedor, fabricação ou publicação.


## Gavetas e organizadores

- `organizadores_g3.cjs` executado: limites das grades para 18/24 frascos, cenários de diâmetro 3,5–5,5 e impacto no setor de secos. Paredes 3 mm e folgas 2 mm por lado explicitamente hipotéticas.
- Pesquisa autorizada via Firecrawl: 3 buscas e 3 páginas oficiais, sem crawl. Kappesberg: dimensões na descrição dos metadados; Madesa: dimensões textuais; IKEA: medidas e lista de frentes 20/20/40 da variante 80 efetivamente lida. Respostas brutas salvas em .firecrawl, ignoradas pelo Git.
- Retornos reportam 9 créditos brutos e 3 reembolsados por feedback: 6 líquidos nessas chamadas, sem afirmar saldo do plano.
- Links locais dos novos documentos conferidos; layout HTML não inspecionado visualmente. Nenhuma mudança de frentes ou seleção de ferragens.


## G1/G2

- `g1_g2.cjs` executado: fechamento das duas larguras e profundidade, quatro faixas da G1, área posterior e divisão removível da G2 conferidos por equações.
- Cenários de altura explicitamente hipotéticos: não substituem ficha de ferragem ou medidas dos utensílios. Nenhuma gaveta, conteúdo ou proporção alterados.
- Links locais encontrados; HTML estático não inspecionado visualmente. Nenhuma chamada de pesquisa externa nesta continuação.
