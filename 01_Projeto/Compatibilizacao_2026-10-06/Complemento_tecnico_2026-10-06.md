# Continuação técnica verificada — 06/10/2026

Este complemento supera as limitações de consulta visual registradas na primeira etapa desta data. PDFs foram baixados de fabricantes e renderizados localmente; os pixels das páginas pertinentes foram inspecionados. Não altera escolhas ou autoriza fabricação.

## Forno e cooktop

O ZIP atual Venax foi aberto. O manual extraído tem SHA256 `116c425ce605d51c27c55b50350a9d5842e58246839af8df4eaad7a1580f5c24`, idêntico à cópia local. Revisão visual das páginas 7, 10 e 11 confirma a divergência: tabela pede 3 cm laterais e 5 cm atrás; texto pede 10 cm ao redor. A figura pede 20 cm entre a face inferior do cooktop e o topo do forno. Documento público atual não resolve essa contradição.

Estudo com módulo externo 60 cm, laterais 1,8 e forno 48,5 deixa 3,95 cm de cada lado: passa somente pelo critério de 3 cm. O critério de 10 exigiria 72,1 cm externos. Não escolher o critério que cabe. Com bancada 92 cm e forno 61 cm, a condição vertical é b+d≤11 cm, sendo b a base e d o avanço inferior instalado do cooktop. Base 5 cm deixa d≤6, sem reserva. A profundidade inferior instalada específica do KE4GC continua desconhecida.

Fonte atual consultada 06/10: [ZIP oficial Venax](https://ftp.venax.com.br/venax/download/forno_de_embutir_a_gas_50l_totale_nero_giii_gas_glp_%28EAN_60101625975%29/manuais_25975_modified_2026-07-04.zip). Evidência local: audit/venax/verificacao.json e PNGs das páginas. A limitação anterior de abrir ZIP/renderizar PDF foi superada; a inconsistência do próprio manual permanece.

## Torre e iluminação

O [catálogo oficial QTMOV](https://qtmov.com.br/midias/catalogo/paginas/6-pagina-06-mini-totem-automatico.pdf), página única revisada, identifica a torre preta 20 A como **QM12200.20**. O modelo preto 10 A é QM12200.00. O limite publicado do 20 A em 127 V é 2.032 W; uma airfryer de 1.400 W deixa 632 W aritméticos, sem autorizar simultaneidade ou circuito. O desenho técnico disponível lista códigos 10 A: suas alturas não foram transferidas ao 20 A. Catálogo informa cabo 1,6 m; desenho 10 A informa 1,5 m. Desenho instalado específico QM12200.20 continua necessário.

Manual Stella EVO V1, duas páginas revisadas: família STH21967, envelope 410×410×38 mm. IES oficial da versão /30 declara 2.329 lm e potência de entrada 35,65 W; página comercial anuncia 30 W/2.300 lm. Não usar a menor potência como carga certificada nem considerar o estudo de sombra uma medição de lux.

Manual Fitas All Light 12 V EVO V2, duas páginas revisadas: fonte 12 V DC separada, cortes apenas nas marcas, raio mínimo 12,5 mm, evitar umidade/água e usar acessórios indicados. O download oficial STL24824/30 registra 952 lm e 12,42 W no IES; especificação comercial 1.000 lm/m e 15 W/m. A identificação interna do IES não repete o SKU. Mantidos 15 W/m para orçamento nominal: 1,1024 m = 16,536 W = 1,378 A em 12 V. Para obter 800 lm/m, a transmissão necessária seria 80% sobre 1.000 ou 84,03% sobre 952; o difusor real não foi escolhido. Fonte, controlador e dissipação seguem sem compatibilidade instalada comprovada.

Fontes oficiais consultadas 06/10: [manual da fita](https://stella.com.br/public/files/produtos/downloads/Manual_Fitas_All_Light_12V_EVO_V2.pdf), [IES da fita /30](https://stella.com.br/public/files/produtos/downloads/STELLA%20-%20STL24824-30%20-%20Fita%20All%20Light%20EVO%20IP20%2012V%2015W.ies), [IES EVO /30](https://stella.com.br/public/files/produtos/downloads/STELLA%20-%20STH21967-30%20-%20PLAFON%20DE%20SOBREPOR%20EVO%2030W.ies). Cópias públicas e renders em iluminacao/evidencia no workspace desta rodada. Produtos continuam candidatos.

## Banheiro

A continuação do relatório ambientes confirma identidade Arion 73131B↔1578386, mas não encontrou desenho funcional específico. O catálogo Addra 2026 mostra Livo com outros códigos; cotas não transferidas. Revisadas todas as páginas das fichas Deca e Celite. Celite figura 585 mm versus tabela 590: mantido 590 no estudo, sem presumir ganho de circulação. Deca desenho 400×300×135 mm não é gabarito de corte. Implantação nominal 100 posteriores +300 cuba +50 anteriores=450 mm; a base da Arion precisa caber nos 100 mm, reduzidos por revestimento/limpeza ainda sem medidas. Três contas adicionais passaram, sem liberar furação.

## Limites da entrega

Pesquisa pública, identidade documental e contas acima foram concluídas. Desenhos ausentes, conflitos entre instruções, medições e validação técnica continuam pendentes. Nenhum contato, compra ou alteração física foi realizado. As evidências públicas consultadas não representam aprovação de obra.
