# Saldo da pia e grupos pendentes —03/10/2026

[Prancha](Saldo_da_pia.html) · [Resultados](Resultados_saldo_pia.json) · [Base C](Tampas_e_G2.md) · [Inventário](../Compatibilizacao_2026-10-02/Mapa_do_inventario.md)

Elias pediu continuar e já restringiu uso de Firecrawl hoje. Sem consulta externa nesta rodada. Medidas dos aparelhos foram solicitadas como informação opcional, sem bloquear análise independente. Não inferir que aparelhos ainda não existem só porque os utensílios de G2 não existem.

## Reservas geométricas, não capacidade global

Base lida diretamente de Resultados_tampas_g2.json, mantendo os volumes técnicos hipotéticos. R1:x43,8/y33,3/z22,13,6 ×23,1 ×23,2; R2:x18/y1/z22,6,4 ×30,3 ×23,2. Unidadescm, x esquerda→direita, y fundo→frente,z piso. Nenhuma dessas áreas intersecta pressão/escorredor/tábua ou reservas técnicas no modelo guardado.

Descontar paredes/fundo de ensaio0,4 e margem superior3 no vão26,2: útil R1=12,8 ×22,3 ×22,8; R2=5,6 ×29,5 ×22,8. Folgas laterais: R1 a2 da pressão e1 da faixa da tábua; R2 a1 da mangueira e1 do sifão. Não somar larguras/áreas das duas como caixa única. Não contar folgas acima dos objetos como novo nível livre.

## R1: mixer completo como primeira candidatura

Hipótese dentro da bandeja, não modelo escolhido: motor e haste desmontada até5,5 ×5,5 ×21 cada; copo atéØ10 ×17; cabo enrolado11,4 ×2,8 ×3. Origens locais: motor0,9/0,9; haste7/0,9; copo1,8/8; cabo0,9/19; z0,4 para contar fundo. Todos os envelopes separados em planta. Altura máxima21,4 deixa4,8 até prateleira, antes de pegas desconhecidas.

Exigir aparelho desmontável cujo conjunto inteiro, plugue, proteções e acessórios estejam nesse volume. Um modelo com miniprocessador/batedor não pode perder componentes do inventário. Sem pesquisa ou aprovação comercial. Se as dimensões reais excederem, R1 reprova; nenhuma redução de mangueira/sifão para forçar encaixe.

Jarra/térmica ou recipientes são alternativas de R1, não conteúdos simultâneos com mixer. Reservar espaço para um grupo não prova cabimento em número de potes ou acessórios.

## R2: tábua adicional de carnes

Tábua hipotética28 ×20 ×1, em pé, x19/y2/z22,4. 28 na profundidade,20 na altura. Guia e proteção dentro do espaço restante. Material e dimensão funcional ainda não selecionados; não confundir com tábua parcial36 ×20 ×2 da cuba. Não houve redução dessa tábua parcial.

Tábua de carnes guardada não intersecta objetos; retirada frontal cruza pressão. Após retirar pressão, percurso livre no modelo. Candidatura não inclui aprovação do apoio/pega/material da tábua.

## Acesso é parte do saldo

R1 tem retirada frontal livre. Escorredor com R1 ocupada colide com pressão e bandeja de mixer; depois da retirada de ambas, sai. Sequência: pressão→bandeja→escorredor. A proposta C anterior só exigia pressão. Não acumular a vantagem de acesso da opção vazia com capacidade da opção ocupada. Se frequência exigir menos manobras, manter R1 como passagem e explicitar que mixer continua sem destino.

Teste201 posições por retirada: bandeja de mixer livre; tábua de carnes cruza apenas pressão; escorredor cruza pressão e R1, livre depois de retirar ambos. Portas, mãos, apoio temporário, estabilidade e cabo real não modelados.

## Lacunas preservadas e próxima decisão

Sem destino completo comprovado para sanduicheira, liquidificador, batedeira, potes de vidro, duas travessas, quatro bowls/três tigelas, peneira/escorredor de macarrão, cesto ventilado e jarra/térmica caso R1 receba mixer. Pratos/copos/canecas em C1/C2, C3 panos/plásticos, B1/B2 reservas e A formas continuam com funções anteriores. Baú compartilhado não recebe excedente automaticamente.

Conclusão: o gabinete oferece duas reservas estreitas, condicionais à base C, e não fecha o armazenamento baixo do inventário. Próxima redistribuição precisa comparar grupos simultâneos com modelos completos e frequência, mostrando qual conteúdo muda de lugar. Não recomendar compra de aparelho por esse gabarito sem conferir conjunto, capacidade funcional e acesso.

Reprodução: `node 01_Projeto/Compatibilizacao_2026-10-03/saldo_pia.cjs`, depois de `tampas_g2.cjs`. Sem produtos novos selecionados, compra, publicação ou fabricação.
