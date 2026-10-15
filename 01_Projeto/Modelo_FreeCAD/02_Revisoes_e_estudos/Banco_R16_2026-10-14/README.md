# Banco: apoios e acessos simples — R16

[Apartamento atual](Guedala_Park_R16_Banco_Simples.FCStd) · [Bebidas e balde](BebidasBalde_R16.png) · [Folha da mesa](Folha_R16.png) · [Montagem](Montagem_R16.json) · [Auditoria](Auditoria_R16.json) · [Solução da folha](Folha_solucao_R16.json) · [Reabertura](Reabertura_R16.json)

R16 incorpora R15 e todas as revisões anteriores, incluindo o canto simples R04. Mantém **180 × 55 cm externos**, assento de 45 cm de profundidade, encosto de 10 cm e topo a 47 cm. A organização de 08/10 e a rotina de retirar as almofadas de bebidas/balde, aceita em 09/10, foram preservadas. Novas peças, cotas, juntas, apoios e rotina do setor da folha são **propostas**, sem corte, furação ou compra liberados.

Fontes locais: [prancha de 08/10](../../../Compatibilizacao_2026-10-08/Cozinha_e_banco.html), Armazenamento_resultados.json e Detalhe_banco_resultados.json. A revisão não escolhe produtos, materiais executivos ou ferragens de tampa.

## Correções e apoios

O banco nativo tinha os compartimentos na ordem inversa do texto aprovado. A sequência **potes/travessas/batedeira → liquidificador/bebidas → balde → folha/aspirador/jogos** agora começa na ponta junto ao sofá e segue para a cozinha. A implantação não mudou: o eixo longitudinal nativo cresce no sentido contrário, por isso foi usada a conversão `X local = 1800 − v − comprimento`, com v medido a partir do sofá. Não espelhar o apartamento para obter esse resultado.

As antigas tampas terminavam antes das divisórias e algumas bordas não tinham apoio lateral. Juntas propostas de 2 mm foram centradas nas divisórias de 18 mm: centros longitudinais v = 389/757/973. Novos envelopes de madeira: **387/366/214/825 × 448 × 20 mm**. As almofadas têm 50 mm; três são removíveis no desenvolvimento atual. Os 20 mm são o orçamento total da tampa, não uma chapa de 20 mm acrescida de ferragens e revestimentos.

Completa-se o corpo com frente de 18 mm, laterais com 450 mm de profundidade e posterior até a cota 400. Cada tampa fechada tem contatos geométricos com frente, posterior e apoios laterais. Nas divisórias intermediárias, contato de 8 mm por lado; nas extremidades, 17 mm. Apoio frontal nominal de 18 mm e posterior de 16 mm. Áreas de contato no JSON são geometria, **não capacidade de carga ou ligação calculada**. Material, flecha, juntas, conexão ao piso e carga do assento permanecem pendentes. As prateleiras removíveis dos potes não sustentam o assento.

Somente o primeiro setor recebe piso superior a 80 mm, face inferior a 62 mm com hipótese de chapa de 18 mm. Demais setores mantêm piso a 100 mm. Não cortar um rodapé ou apoio real por dedução. Vãos de conteúdo preservados: 362/350/198 mm e nicho da folha de 800 × 350 × 70. Dois espaços inferiores têm reservas de 371 × 350 × 164; aspirador e jogos reais não foram reduzidos a essas caixas.

## Conteúdo e acesso

Entraram no CAD os gabaritos da organização aprovada: seis potes em três pilhas, travessas, batedeira, motor/jarra do liquidificador, jarra de 1,5 L, térmica vazia/seca e balde de 8 L. São referências documentais, não objetos medidos ou produtos selecionados. Contenção do balde de 180 × 350 × 33, com paredes de 4 e fundo de 3, é hipótese; não comprova estanqueidade ou higiene.

Dois painéis removíveis de **356 × 202/177 × 18**, com folga lateral de 3, permanecem em Z244–262. Faixas de suporte ocupam 10 mm por lado e 6 de altura, Z238–244: apoio por lado de 7 mm, vão de 342, montagem total de 24. Carga, retenção e produto do suporte não selecionados. Mantidos 35 mm acima da batedeira e 40 acima dos potes; só 5 extras sobre a reserva mínima de 35 do estudo. Não adicionar ferragens fora desse orçamento.

No primeiro setor foi mantido o giro de estudo do assento integral de 70 mm. O acoplamento da almofada, massa, dobradiça, pega e retenção precisam de definição física; não tratar as duas formas CAD como almofada solta que possa permanecer apoiada durante o giro. Bebidas e balde usam tampa fina de 20 com almofada removível, conforme a rotina já aceita.

### Folha: correção nova e simples

A tentativa de avançar a folha 16 mm e subir com o assento integral de 70 aberto **bateu na mesa**, registrada em Complemento_R16.json. Não foi reduzida a folha nem movida a mesa para esconder o conflito.

**Nova proposta para esse setor:** também retirar a almofada antes de abrir a tampa fina. A almofada de 827 × 450 × 50 fica temporariamente sobre os três setores fechados, no intervalo v100–927, acima do assento. Ela bloqueia esses três acessos durante a operação; banco desocupado. Levantar 60, deslocar 873 rumo ao sofá e baixar a elevação para 50. Depois abrir a tampa a 90°.

O envelope inteiro de **800 × 350 × 70** recua 24 mm antes de subir. A passagem ideal tem 378 de profundidade, deixando 14 até a mesa e 14 até a tampa aberta. Dois segmentos contínuos de translação passaram. Esta rotina adicional é uma proposta de R16, **não um novo aceite atribuído a Elias**. Peça completa da folha, alças/pegas, peso, pessoa, transferência e montagem sobre a mesa não foram validados.

## Conferências e limites

- Sem sobreposições relevantes no banco fechado, com os gabaritos de conteúdo e a estrutura proposta; formas individuais válidas. A mudança do último setor preservou exatamente as envoltórias fechadas da tampa/almofada, delta zero.
- 28 poses iniciais, sete por setor, contra o corpo, programa, outras tampas/almofadas e 58 volumes externos/paredes. As sete poses do último setor foram substituídas por sete novas após a correção para tampa fina; passaram. Não é prova física da dobradiça ou de tolerâncias.
- Dois setores diários abertos simultaneamente passaram. Almofadas de bebidas/balde estacionadas em v1100–1468 e v1490–1706, sobre o setor da folha fechado. Seus seis segmentos de deslocamento tiveram envoltórias contínuas sem hits. Não acessar a folha enquanto essas almofadas estiverem lá.
- O teste negativo confirmou colisão ao abrir o setor da folha com a almofada das bebidas estacionada nele. A ordem de uso é necessária; **não há intertravamento físico ou de software**.
- Treze percursos de conteúdo por prismas varridos passaram: térmica/jarra independentes, balde, seis potes em ordem, dois painéis vazios e travessas/batedeira. São translações de caixas com orientação fixa, sem mão, alças, deformação ou produtos reais. O balde continua a levantar 32 e recuar 19 antes de subir; sua alça completa permanece pendente. Painéis saem somente vazios, após os potes.
- A tampa fina tem limite inferior conservador de 30,52 mm até o tampo no corte ideal, com 19 amostras e margem entre amostras. Para o primeiro assento de 70, o ensaio inicial de 5° era inconclusivo; foi refinado para 1°/91 amostras, obtendo limite inferior de 12,61 mm. Não repetiu as 901 poses antigas. Provas limitadas ao envelope e tampo ideal, excluindo ferragens, bordas macias, mãos, objetos e tolerâncias. Madeira fica até u448; almofada integral pode tocar u450 no fechado, sem folga física macia comprovada.
- R16 salva/reaberta. Quatro controles exercitados; erros de rotação abaixo de 1,3e−13 mm, tampas/almofadas válidas e atualizadas. Final todos os comandos zero. Vistas estáticas inspecionadas; estrutura e mesa transparentes somente nas vistas.

## Controles e continuidade

Grupo **R16 - abrir banco; almofadas bebidas/balde primeiro**, nomes em Montagem_R16.json. `Abertura` em graus. Bebidas/balde: `ElevarAlmofada60` → deslocar 711/733 → reduzir elevação a50 → abrir90. Folha: elevar60 → deslocar873 → reduzir elevação a50 → abrir90. Fechar/devolver em ordem inversa. A almofada do setor da folha ocupa os outros três; retornar antes de acessá-los. Os controles são livres, sem limitador ou sequenciamento automático; outras combinações não foram conferidas.

Ferragens comuns de giro/retenção e resistência de tampas, corpo, fundo e apoios ainda precisam de desenho/dados reais. Não selecionar pistão ou ferragem especial para esconder essa pendência. Não liberar assentamento de pessoas por áreas de contato, cores ou validade das formas CAD.

Próximo trabalho independente: equipamentos, nichos e ventilação diante das decisões e manuais disponíveis; depois organizar o fechamento matinal com conferências e pendências reais. Não reexecutar banco/cesto/correr/gavetas sem alterações ou evidência nova. [Inventário do apartamento](Pendencias_apartamento_R16.md).
