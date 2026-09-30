# Verificação da rodada — 28/09/2026

## Continuação: torre × gavetas

- Ficha QTMOV 10 A, página 1, e manual PDF, páginas 1–3, conferidos visualmente em renderizações locais com pypdfium2. Cópias oficiais preservadas em `Fontes_torre/`; provenance em `Fontes_torre.json`. Ficha e manual não foram combinados como se identificassem a mesma variante 20 A.
- `calcular_torre_gavetas.cjs`: cinco conferências passaram — distância a retângulo (face/canto/interior), curso da caixa 0–50 cm, limite analítico dos 60 cm, fundo/recuo no limite e interferência frontal. Seis seções construtivas e três posições superiores comparadas; `gerar_torre_gavetas.cjs` gerou a prancha a partir dos resultados.
- `Torre_gavetas.html` inspecionado visualmente a 1280 px: planta, corte, ampliação da rodabanca e tabelas legíveis, sem transbordamento horizontal do documento (1265 px úteis). Conferida versão regenerada com correção da descrição de sobreposição de 3 mm. Versão móvel não inspecionada; diagramas têm rolagem própria.
- Links locais dos índices, memória, prancha e documentos alterados conferidos sem destino ausente. `git diff --check` sem erro, somente avisos de LF/CRLF.
- As contas não medem o apartamento nem comprovam a torre 20 A, anel, resistência da pedra, estrutura do móvel, circuito, respingos ou uso da tomada com plugue/mão. Furação e fabricação permanecem sem liberação; nenhuma redução nas gavetas aplicada.

## Continuação: apoio do micro e C2

- Manual ME23P p. 3 revisto visualmente na renderização local. Mantida a divergência conhecida de 10/30 cm; não houve pesquisa comercial nova.
- `calcular_micro_c2.cjs`: quatro verificações passaram (folgas laterais, oclusão, linearidade da luz e limite dos cortes com terminais). IES com tipo, unidades e ângulos conferidos; base fotométrica é a mesma já validada na primeira rodada.
- Comparadas 12 posições B/C; quatro cenas calculadas com apoio, purificador, com/sem pessoa e com/sem air fryer. Área prioritária separada das faixas do filtro; malha de no máximo 2,5 cm e fontes de no máximo 5 mm. Área ocupada pela air fryer calculada analiticamente, sem inferi-la da contagem de pontos.
- `Micro_C2.html` inspecionado visualmente em 1280 px: corte, planta, mapas, legendas e tabela sem sobreposição; sem transbordamento horizontal do documento. Prancha estática e sem recursos remotos. Versão móvel não inspecionada; desenhos admitem rolagem local para preservar leitura.
- Nova versão recarregada após ajuste de título; links locais da prancha/memória conferidos e `git diff --check` sem erro de whitespace (somente avisos de LF/CRLF).
- Estrutura, posição dos pés do ME23P, produto real de iluminação e distribuição instalada continuam fora do alcance dessa verificação. Resultados não liberam fabricação ou instalação.

## Continuação: corte de cocção

- Manual Venax p. 7 conferido em nova renderização Poppler; p. 10–11 e manual Electrolux p. 8–9 conferidos nas imagens locais. Registrada a divergência de folgas do próprio manual Venax.
- Página comercial Electrolux, conteúdo técnico ilustrado, ficha BIM do fabricante e página Venax consultados em 28/09. As duas imagens de especificações Electrolux foram baixadas da fonte oficial e inspecionadas; não fornecem a cota inferior instalada.
- `gerar_corte_coccao.cjs` gerou prancha e resultados. Cinco conferências de fechamento geométrico passaram, incluindo caso nominal no limite e duas perdas de 5 mm.
- `Corte_coccao.html` inspecionado visualmente no navegador em 1280 px: três diagramas, cotas e tabela legíveis; sem transbordamento horizontal da página. Documento estático, sem dependências remotas. Versão móvel não inspecionada nesta continuação.
- Links locais da prancha, memória do corte e índice diário: nenhum destino ausente. `git diff --check` sem erro; apenas avisos de conversão LF/CRLF.
- Atualizados os avisos nas conferências antigas e índices para evitar que a conclusão de largura favorável seja lida sem a nova condição documental. Nenhuma dimensão ausente foi promovida a medida real.

## Primeira rodada

- Cálculos executados em Node, sem dependências externas: sete verificações matemáticas passaram. Detalhes em `Resultados.json`.
- Integral independente da curva IES: 2329,09 lm versus 2329 lm declarados no arquivo. Também conferidas simetria, lei do inverso do quadrado e proporcionalidade da fonte linear.
- Cesto: pico analítico confrontado com 5.501 posições angulares; limiar de acesso resolvido analiticamente.
- Caderno gerado a partir dos resultados. Aberto no navegador local e inspecionado visualmente em 1280 px; sem transbordamento horizontal do documento.
- Alternância bancada normal / air fryer operante conferida: escorredor alterna com a air fryer e a legenda acompanha.
- Controle de ângulo conferido: em 50°, boca 0,60 cm sob a projeção da pedra; ao recarregar, estado de 55° retorna com boca 3,52 cm além da pedra e saldo 0,52 cm após a reserva de 3 cm.
- Navegador sem avisos ou erros de JavaScript capturados na conferência. Layout móvel não foi verificado visualmente nesta rodada.
- Referências locais dos oito documentos atualizados e das duas memórias novas conferidas: zero destinos ausentes. `git diff --check` sem erros de whitespace.

Essas verificações avaliam aritmética, reprodutibilidade e funcionamento do caderno. Não validam medidas da unidade, ergonomia real, fotometria instalada, ferragens, capacidade de carga ou conformidade de instalações.
