# Avanço autônomo — 30/09/2026

**A — formas leves e pizza:** [guarda e retirada](Formas_A.html) · [memória](Formas_A.md). Recuperada escolha de pizza Ø30; proposta de guarda em pé numa metade de A, sem prateleira nova. Organizador baixo 35 × 28 × 5, três canais largos e retirada com elevação de 5,6. Contenção/alcance ainda a detalhar; não presumir acesso independente às peças traseiras. Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/formas_a.cjs`. Sem pesquisa externa.

**B1/B2 — após aprovação do C3:** [pratos de visitas e reserva](B1_B2.html) · [memória](B1_B2.md). Pilha de 18 preservada em meia largura do B1; três caixas iguais de 30 × 28 × 12 propostas no restante. Calculados limites de diâmetro/altura, sensibilidade de encaixe e massa, sem confirmar louça real. Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/b1_b2.cjs`. C3 atualizado com a aprovação funcional de Elias.

**C3 — continuação após G1/G2:** [panos e potes vazios](C3_reserva.html) · [memória](C3_reserva.md). Caixa de panos separada e bandeja ampla para dez potes e tampas. Comparadas uma pilha de dez e duas de cinco, com paredes, reservas e largura antiga/atual proposta. Preferência técnica por duas pilhas baixas condicionada ao conteúdo real; sem nova pesquisa. Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/c3_reserva.cjs`.

**Continuação após commit 571da11:** [operação da lavanderia em planta](Operacao_lavanderia.html) e [memória](Operacao_lavanderia.md). Cenas separadas para retirar saco e carregar LG; posição lateral de pessoa candidata. Guarda do banquinho na faixa baixa junto à janela conflita com cesto/lixeira: faltam 27,15 cm após reservar o giro. Novos arquivos desta continuação não incluídos no commit anterior. Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/operacao_lavanderia.cjs`.

[Abrir estudo interativo do cesto](Cesto_retirada.html) · [memória e requisitos](Cesto_retirada.md) · [resultados](Resultados_cesto.json).

Esta rodada desenvolve frente, giro e retirada do saco sem reduzir tanque ou cesto. Mantidos envelope 45 × 25 × 45 cm, 55°, saco lavável com alças e frente lisa Arenza. Novas cotas são propostas técnicas, não aceites atribuídos ao usuário.

- Frente inferior basculante e painel superior removível: projeção aberta de 105,15 cm desde a parede, contra 123,66 cm de uma frente alta no mesmo plano.
- Face frontal da lavanderia proposta em 63 cm para cobrir tanque de teste até 60; pedra preservada em 75, base/rodapé recuados até 58. Rodapé com topo 11, fora do giro do cesto; frente inferior z=15–67,1, painel z=67,5–89,7.
- Folga vertical de 4,02 cm entre giro e painel, incluindo 1 cm adicional de estudo além da reserva anterior de 3.
- Retirada inclinada e posterior endireitamento de corpo carregado hipotético 40 × 20 × 40; pico em y=125,83, com saldo de seção de 28,17 cm antes da pessoa.
- Requisitos de parada, retenção e desmontagem frontal preparados; massas e momentos são sensibilidades, não ferragem selecionada ou carga permitida.

Reproduzir com `node 01_Projeto/Compatibilizacao_2026-09-30/calcular_cesto.cjs` e depois `node 01_Projeto/Compatibilizacao_2026-09-30/gerar_cesto.cjs` na raiz do projeto. [Verificação](Verificacao.md). Não houve compra, pesquisa comercial, contato com fornecedores ou publicação do site nesta rodada.

Próxima frente independente: operação da lavanderia em planta com máquina, lixeira, porta e banquinho. Usar a projeção completa da frente e da extração, não apenas a do recipiente. [Rodada anterior](../Compatibilizacao_2026-09-28/README.md).


## Continuação: destino do banquinho

[Prancha interativa sob a TV](Banquinho_alternativa.html) · [Memória](Banquinho_alternativa.md). Candidato condicional, com 63 cm junto à cama guardado e 48 na retirada. Giro rígido do sofá não colide com a reserva; pessoa e mecanismo permanecem a conferir. Sem pesquisa externa. Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/banquinho_alternativa.cjs`.


## Continuação: retirada com a cama aberta

[Sequência em quatro plantas](Banquinho_operacao.html) · [Memória](Banquinho_operacao.md). Gabarito hipotético 40 × 50, retirada de 15 e transporte de 80 sem rotação do objeto. Folga de 5 cm à cama; conjunto ocupa 68 cm e fica a 2 cm de um lado do vão ideal. Mantido como candidato secundário. Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/banquinho_operacao.cjs`.


## Continuação: luz da lavanderia e varal

[Planta e sombras](Luz_varal.html) · [Memória](Luz_varal.md). Faixa para plafon compacto até 30 cm; corpo de teste de 28 em x=64,5/y=55 deixa 6 cm até a projeção dos aéreos e 6 até roupas avançando 10 cm. Comparados 1.341 segmentos por cenário, sem conversão em lux. Produto/ponto ainda não selecionados. Sem Firecrawl. Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/luz_varal.cjs`.


## Continuação: extensão da mesa guardada no banco

[Retirada em três plantas](Folha_mesa.html) · [Memória](Folha_mesa.md). Retirar com mesa fechada poupa 15 cm de percurso; cadeira da ponta recua temporariamente 5 cm. Rota depende da coluna: limite de 15,4 cm para margem comparativa de 3. Não dimensionar a estrutura a partir desse limite. Apoio temporário, pessoa, porta do nicho e estrutura permanecem a conferir. Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/folha_mesa.cjs`.


## Continuação: apoio temporário da folha

[Prancha de apoio sobre a mesa](Apoio_folha.html) · [Memória](Apoio_folha.md). Giro e transferência acima dos encostos, apoio inteiramente numa metade e deslocamento até o vão. Envelopes conservadores exigem recuos temporários de 41 e 32,5 nas cadeiras da ponta e central. Operação da ferragem com folha apoiada e facilidade de manuseio não demonstradas. Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/apoio_folha.cjs`.


## Mesa — entrega consolidada

[HTML completo da mesa](Mesa_completa.html) · [Memória](Mesa_completa.md). Guarda, retirada, apoio temporário no assento, abertura com tampos vazios e montagem. Nova direção supera apoio sobre metade móvel; recuos temporários de teste: 5 cm na ponta e 32,5 na central. Percurso do objeto verificado em 2.010 posições adicionais, sem liberar fabricação ou confirmar uso por uma pessoa. Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/mesa_completa.cjs`.


## Gavetas — dimensão e organização

[Prancha do G3 e comparação com fabricantes](Organizadores_g3.html) · [referências de mercado](Padroes_gavetas.md) · [conta dos organizadores](Organizadores_g3.md). Preservar módulo 61,9 e frentes 16/16/40; divisores removíveis sem forçar embalagens. Pesquisa Firecrawl autorizada e focada em três fabricantes, com 6 créditos líquidos reportados.


## G1/G2 — organização removível

[Prancha](G1_G2.html) · [Memória](G1_G2.md). G1 com quatro faixas largas, área posterior e facas protegidas; G2 com dois módulos e divisor ajustável. Frentes de 16 preservadas, folgas e paredes incluídas. Sem nova pesquisa externa. Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/g1_g2.cjs`.
