# Cozinha: reconciliação e verificação de 06/10/2026

Base: `C:/Users/Elias/Documents/PROJETOS/Guedala park/guedala-park`. Leitura das revisões de 30/09 a 04/10, incluindo alterações ainda sem commit. Nenhum objeto foi removido do programa nem candidato convertido em escolha. Unidades dos cálculos: cm.

## Estado vigente

| Assunto | Aprovado / direção vigente | Histórico ou alternativa | Ainda condicionado |
|---|---|---|---|
| C1/C2 | Duas pilhas de pratos em C1; seis copos e quatro canecas em C2. Organização de C2 aceita em 04/10: sanduicheira atrás à direita, dois copos à frente do aparelho. | Pilha única de 12 em C1 não adotada; retirada de duas canecas para o aparelho superada pela nova disposição. | Aparelho, capacidade de preparo desejada, largura real, cabo/plugue completo e alcance a 174,8. |
| G2 | Oito utensílios definidos por delegação em 03/10: concha, escumadeira, duas espátulas, peneira pequena, dois espremedores e ralador plano. | Quantidade desconhecida e envelope coletivo antigo de altura 6,5 superados. | Marcas/códigos e caixa/ferragem reais; frigideira Turim20 continua candidata. |
| G3 | Frente 16/16/40 e setorização: temperos frente esquerda, secos abertos atrás, leite/sucos/óleo/azeite à direita. | Não há setor adicional livre para molhos/enlatados. | Conteúdo simultâneo, embalagens cheias, altura livre, massa total e corrediça. |
| C3 | Panos limpos e dez potes vazios/tampas na cozinha, organização aceita em 30/09. | Proposta de duas pilhas de cinco não prova tamanho real dos potes. | Caixas, proteção, largura real e acesso. |
| Pia | Programa preservado: quatro panelas em duas pilhas, pressão, tampas, frigideira, tábua/escorredor. Base C autorizada para desenvolvimento. | Medidas antigas de gabinete 60 e guarda curta das tampas não prevalecem na base atual. | Hidráulica instalada, tampas completas, tábua adicional e aprovação funcional de novas guardas. |
| Banco | Folha da mesa preservada; prioridade expressa em 03/10: aspirador, balde e poucas caixas de jogos; balde central/vãos baixos como direção. | Compartimento limpo 60 e vidro sobre apoios continuam alternativas; não somar capacidade de cenários exclusivos. | Objetos reais, estrutura, retirada; destino final de ciclismo/mochilas/malas. |
| Grupos sem solução fechada | Jarra/térmica futuras, cesto ventilado para batatas/cebolas/alho, aparelhos ocasionais e vidro continuam no inventário. | Mixer em R1 e vidro em R1 disputam o mesmo espaço; banco limpo não equivale a espaço aprovado. | Frequência/capacidade desejada e compatibilização conjunta. |

Fontes: `Painel_de_decisoes.md`, blocos “C2 reorganizado — aceite04/10”, “Baú — prioridade escolhida”, “30/09 — C3”; `Compatibilizacao_2026-10-02/Mapa_do_inventario.md`; `Compatibilizacao_2026-10-03/Tampas_e_G2.md`, “Decisão vigente do dia”; `Cozinha/Interior_gavetao_2026-09-25.md`, “Setorização aprovada”. Os trechos mais recentes desses arquivos prevalecem sobre os históricos mantidos abaixo deles.

## C2: reprodução e tolerâncias fechadas documentalmente

Executado o script existente `Compatibilizacao_2026-10-04/c2_reorganizado.cjs` em cópia isolada, com suas fontes JSON, sem escrever na fonte. As assertivas de limites, colisões e sequência de retirada passaram. As duas larguras de estudo continuam dando 22 × 22 × 15,3 e 20,1 × 22 × 15,3. Nenhum resultado comprova portas, pessoa ou ergonomia.

Mantendo as posições aceitas, largura limite do aparelho = **mínimo(22; W − 28,5)**. W é largura interna real do módulo, não externa. O termo 28,5 incorpora início em x=27,5 e margem lateral direita de 1. Não aumentar o limite 22 só porque sobra largura: ele é a restrição do estudo adotado.

| W interno | Largura máxima completa | SAN405 de 21 | SAN265 de 21,5 |
|---:|---:|---|---|
| 48,6 | 20,1 | Reprova 0,9 | Reprova 1,4 |
| 49,5 | 21 | Igualdade sem saldo dimensional adicional | Reprova 0,5 |
| 50 | 21,5 | Saldo 0,5 | Igualdade sem saldo dimensional adicional |
| 51,1 | 22 | Saldo 1 | Saldo 0,5 |

Os saldos da tabela são entre corpo publicado e limite completo de guarda, **não folgas para mãos**. Cabo/plugue, partes salientes e proteção precisam estar dentro do limite. No W51,1, SAN265 só dispõe de 5 mm adicionais em cada dimensão horizontal se o envelope crescer em uma dimensão inteira; não presumir que seu porta-fio resolve isso. Altura limite = 19,2 − 0,4 de apoio − 0,5 de elevação − 3 de reserva = **15,3**. Frente dos dois copos sai antes da sanduicheira; dependências das louças posteriores permanecem como aceitas.

Atualização oficial em 06/10/2026: [Cadence SAN265](https://www.cadence.com.br/sanduicheira-eletrica-cadence-toast-grill-branca/p) identifica versões 127/220 V, potência 750 W, corpo 215 × 80 × 215 mm e preparo de dois sanduíches; descrição e tabela divergem em altura/peso. Usada tabela de 80 mm, sem validar massa ou guarda completa. Página apresenta indicação de esgotado; preço/estoque não encerrados. [Cadence SAN405](https://www.cadence.com.br/sanduicheira-eletrica-cadence-click-inox/p) identifica 127/220 V, 800 W e corpo 210 × 80 × 210 mm. Peso diverge e link “Dados Técnicos” aponta OSAN500: não usar esse anexo para SAN405. Nenhuma cor, modelo ou compra escolhidos. Consulta web textual do fabricante; não houve Firecrawl ou contato.

Pergunta funcional curta preparada: **“A sanduicheira deve preparar dois sanduíches de uma vez, ou um pequeno atende?”** Evidência: capacidade ainda aberta no aceite04/10; SAN265 publicada para dois, mini anterior não escolhido. A pergunta não reabre a distribuição aceita e não bloqueia os demais cálculos.

## G2: envelope e altura revistos sem nova escolha

Faixa1: 6 + 0,2 + 2,5 = 8,7; com fundo 0,4 e reserva 1, requer H≥10,1. Faixa2: 2,5 + 0,2 + 2,5 + 0,2 + 4,2 = 9,6; requer H≥11,0. Frigideira candidata de 9,7 requer H≥11,1. Logo **H≥11,1 governa os três grupos**; frente bruta de 16 não comprova H.

H11,1 é igualdade do critério de ensaio. Aumentar proteção/fundo em 2 mm faz o requisito passar a 11,3; não reduzir margem nem retirar utensílios para fazer a conta fechar. O script complementar registra cenários 10/11/11,1/11,3/12 e limites de C2; valores são sensibilidade das hipóteses, não tolerâncias de execução.

Fonte: `Compatibilizacao_2026-10-03/Tampas_e_G2.md`, “Critérios de compra e duas faixas”; `Compatibilizacao_2026-09-30/G1_G2.md`, “Altura livre”. Retirar peça superior antes da inferior nas pilhas continua necessário; produto ainda não comprado/medido.

## G3 e reservas: encerrado o que a documentação permite

O mínimo registrado soma 6 leites + 3 sucos + 1 óleo + 1 azeite = **11 embalagens**, antes de molhos/enlatados. Isso é mínimo de triagem; não fixa marca/litragem do leite ou estoque máximo. Área externa direita 22 × 45 = 990 cm²; área média bruta por 11 seria 90 cm², mas área total não prova encaixe. Grades uniformes de 2×6 e 3×4 já foram calculadas no estudo30/09; repeti-las não resolve contornos, carga ou embalagens desconhecidas. Mantido o desenho removível e o programa completo.

R1 útil12,8 ×22,3 ×22,8 é candidatura exclusiva mixer/vidro; R3 útil10,5 ×23,3 ×17,6 é confronto futuro para jarra/térmica. Não constituem compra, volume funcional nem capacidade conjunta demonstrada. Portanto não fechar organizadores, carga das ferragens ou lista de compras quantitativa a partir dessas reservas.

Fontes: `Compatibilizacao_2026-09-30/Organizadores_g3.md`, “Faixa direita e inventário mínimo”; `Compatibilizacao_2026-10-03/Saldo_da_pia.md`; `Compatibilizacao_2026-10-03/Pendencias_da_cozinha.html`.

## Entregas e limites

Concluídos nesta rodada: estado vigente reconciliado; reprodução isolada de C2; tolerâncias e sensibilidade C2/G2 com cálculo reproduzível; fontes Cadence atualizadas; conflitos de contagem e dados mínimos separados. Permanecem abertos: seleção dos produtos/funções novas, conteúdo real, medidas acabadas, carga, estrutura, circuitos/hidráulica, ensaio físico e responsabilidade técnica. Nenhuma checagem documental equivale a aprovação de obra.

## Cocção e micro: bloqueios técnicos preservados

Reproduzido em cópia isolada `Compatibilizacao_2026-09-28/gerar_corte_coccao.cjs`: cinco conferências geométricas passaram. Resultado não fecha instalação. O forno Venax tem divergência local entre tabela p.7 (3 cm laterais/5 atrás) e texto p.10 (10 em toda a volta). No ramo de 3 cm, módulo60 com laterais1,8 dá útil56,4; corpo48,5 deixa3,95 por lado e saldo0,95 sobre3. No ramo de10, largura externa necessária seria48,5+20+3,6=72,1, excedendo60 em12,1. Não substituir ramo divergente por aquele que cabe.

Verticalmente, separação do estudo =92−d−(b+61)=31−b−d. Para mínimo20 resulta b+d≤11. Com b5, d≤6 sem saldo; cenário de perdas combinadas1 exige d≤5. `d` é profundidade vertical inferior instalada do cooktop desde a face da bancada, ainda não fornecida; altura total13,1 e altura comercial do nicho15 não são d. Em 06/10 foi consultado o [conteúdo técnico Electrolux KE4GC](https://content.electrolux.com.br/brasil/electrolux/poke/v1/experience/ke4gc/index.html), sem cota d obtida na extração textual.

A [página Venax do SKU25975](https://venax.com.br/categoria-produto/fornos/fornos-de-embutir-a-gas/forno-a-gas-de-embutir-50-l-totale-nero/forno-de-embutir-a-gas-50l-totale-nero-giii-gas-glp/) consultada06/10 mantém produto61,5P ×51,7L ×61A e versões127/220 V. Link oficial do manual continua apontando `manuais_25975_modified_2026-07-04.zip`; leitor web não suporta esse ZIP. Não alegar comparação binária nova ou esclarecimento da divergência. Manual local previamente conferido permanece a evidência disponível; consulta técnica já preparada em “Consulta técnica pronta — não enviada” de `Corte_coccao.md`, sem novo contato.

ME23P permanece escolhido; 10 cm superiores solicitados continuam divergindo dos30 do manual específico. Alternativa de elevar prateleira para214 altera armazenamento e não está aprovada. Seu corpo35,2 +10 atrás pede45,2P, contra aéreo35. Não reabrir a mesma pergunta dos30 nem aprovar o nicho por desejo do usuário. Referência: `Cozinha/Aparelhos_compatibilizacao_R03_2026-09-27.md`, “Micro-ondas: registrar o conflito e uma alternativa concreta”. Estes bloqueios exigem solução técnica compatível; não são encerrados por checklist ou render.
