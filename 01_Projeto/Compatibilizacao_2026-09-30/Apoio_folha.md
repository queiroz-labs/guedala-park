# Apoio temporário da extensão e ciclo de montagem

30/09/2026. [Prancha](Apoio_folha.html). Complementa a [retirada do banco](Folha_mesa.md), preservando mesa 150/180 × 75, folha 75 × 30 × 3 e guarda no banco. Sem pesquisa externa.

## Resultado e condição principal

A folha pode ocupar geometricamente uma área inteiramente sobre a metade da mesa voltada à cozinha, sem apoiar sobre a junta. Isso oferece um destino temporário antes da abertura. Porém, para baixá-la sobre o tampo, o gabarito conservador da cadeira da ponta exige **afastamento temporário de 41 cm**, em vez dos 5 suficientes para a retirada baixa. A cadeira central também precisa recuar **32,5 cm** no mesmo modelo conservador para liberar a descida final no vão central.

A alternativa fica documentada para protótipo; não é demonstração de operação confortável por uma pessoa. Transportar a folha junto com a metade durante a abertura depende da ferragem e de controle da peça. Não presumir aderência, trava ou retenção de um protetor comum. Se o fabricante exigir mesa totalmente desocupada para abrir, essa sequência não atende e precisará ser revista.

## Bases locais e alturas

Mesmas coordenadas da [memória anterior](Folha_mesa.md): u parte da frente do banco, positivo rumo à parede; v começa na ponta do banco próxima ao sofá e cresce para a cozinha. Global x=685+u, z de planta=375+v. Altura é expressa separadamente.

- Mesa: u=−70–5, v=15–165 fechada; v=0–180 aberta; tampo a 75.
- Cadeira da ponta: u=−79–−32, v=118–162, altura externa de referência 94. Usar todo o retângulo até essa altura é conservador: não reproduz encosto e braços reais.
- Após deslocar 41 rumo à sala: u=−120–−73, global x=565–612. A borda da folha apoiada fica em u=−70, deixando 3. O estudo anterior com deslocamento 5 terminava em u=−37, invadindo a projeção da folha sobre o tampo.
- Cadeira central: v=68–112. Folha apoiada começa em v=115, deixando 3; cadeira da outra ponta termina em 62 e não intercepta essa área.
- [Ajustes integrados](../Sala_e_jantar/Ajustes_integrados_R01.md): banco/encosto até altura 90 e globo inferior do pendente a 155 no cenário. Peça transportada com face inferior a 97 e superior a 100 deixa 3 acima dos encostos e 55 abaixo do pendente. Essas alturas são de ensaio, não medidas acabadas.
- Corpo fechado da geladeira no [modelo](../Estudo_interativo/src/app.js): x=584,9–645, início longitudinal global 615,25. Em coordenadas locais, canto próximo da rotação (−40;240,25). Porta, puxador e pessoa não modelados.

## Retirada, elevação e rotação

Concluir o percurso anterior com folha em u=−32,5–−2,5 / v=168–243, à altura de teste 34–37. Há 3 de afastamento longitudinal até o tampo fechado que termina em 165 e 6 até a cadeira que termina em 162. Elevar verticalmente nessa posição até face inferior 97. O retângulo fica fora da mesa e das cadeiras durante essa subida; pessoa e mãos não foram desenhadas.

Antes de girar, deslocar a peça 5 rumo ao banco: centro passa de (−17,5;205,5) a **(−12,5;205,5)**. Girar 90° no plano horizontal, mantendo altura 97–100.

O raio envolvente do retângulo 30 × 75 é √(15²+37,5²)=40,3887. Assim:

- Sua menor coordenada v no giro é 165,1113: pelo menos **3,1113** além da cadeira até 162.
- Distância do centro ao canto da geladeira menos esse raio fornece pelo menos **3,9262 cm** de afastamento ao corpo fechado, valor arredondado; o resultado preciso fica no JSON. Usar o círculo inteiro é conservador em relação ao retângulo que gira.
- Maior u no giro é 27,8887, antes do encosto do banco que começa em u=45 e da parede em u=55.

Após girar, a folha fica u=−50–25 / v=190,5–220,5. Levar seu centro a v=130, ainda elevado, e depois a u=−32,5. A folha chega a u=−70–5 / v=115–145. A tradução ao longo de v mantém u≤25, fora do encosto do banco; a de u, feita a 97, passa acima dos encostos das cadeiras. Não se afirma que exista posição corporal confortável para executar esse trajeto.

## Apoio antes e durante a abertura

Baixar a folha sobre proteção de altura de ensaio 1: face inferior a 76 e superior a 79. Não é produto especificado; proteção deve ser compatível com acabamento e não esconder ferragens salientes da folha. A folha ocupa **u=−70–5 / v=115–145**, toda sobre a metade v=90–165, longe da junta:

| Relação | Valor |
|---|---:|
| Até a junta central fechada em v=90 | 25 |
| Até a ponta da mesa em v=165 | 20 |
| Até o início dos cantos R15 em v=150 | 5 |
| Margem lateral da folha no tampo | 0 — bordas alinhadas |

Nenhuma folga lateral foi inventada: a folha tem os mesmos 75 de largura do tampo. Apoios, proteção e pega devem considerar essa condição. Pinos/fechos na face inferior não foram modelados e não podem riscar o tampo ou concentrar carga.

Se o mecanismo permitir abrir com a folha apoiada, a metade avança 15 e leva a folha para **v=130–160**; metade passa a v=105–180. As margens relativas de 25/20/5 permanecem. A folha não cruza a junta em nenhuma posição intermediária. É necessária operação controlada; o ensaio apenas define onde a peça precisaria permanecer.

Antes da montagem final, a cadeira central de u=−87,5–−40,5 deve recuar 32,5 para terminar em u=−73: deixa 3 até a borda da folha em u=−70. Sua projeção longitudinal v=68–112 cruza o vão v=75–105; a folga de 3 até a folha no apoio temporário não resolve essa etapa. Esse conflito resulta de usar todo o envelope até 94 de altura: o contorno real do encosto pode permitir recuo menor. A retirada baixa continua exigindo somente o ajuste da cadeira da ponta.

Para montar, levantar a folha acima das duas metades e mover 55 rumo ao centro, até v=75–105, encaixe nominal da mesa aberta. O vão exato de 30 não oferece margem de inserção: o curso adicional, os pinos, apoios e travas devem seguir o desenho real da ferragem. Não demonstramos a montagem executiva apenas por encaixar retângulos.

Para recolher, a lógica se inverte, com o mesmo controle da peça sobre uma metade e as mesmas reservas; isso não é teste de força ou de facilidade de inversão. O operador precisa ter acesso aos fechos e à pega.

## Implicação para o projeto

O apoio temporário ganhou posição e percurso completos em geometria, sem outro móvel. A operação passa a exigir afastar temporariamente duas cadeiras, elevar e girar a folha, acompanhá-la na abertura e inseri-la. Registrar essa exigência como custo de uso, sem descrevê-la como simples ou aprovada pelo usuário.

Continuam indispensáveis ao protótipo: coluna e sapata compatíveis com a retirada baixa, estrutura/portinhola do banco, contorno real da cadeira, peso e pega da folha, posição do operador, proteção, autorização de uso da ferragem com carga temporária e curso de encaixe. Não alterar a coluna para cumprir o limite geométrico anterior de 15,4, nem comprar uma ferragem com base nessa sequência.

Script: `node 01_Projeto/Compatibilizacao_2026-09-30/apoio_folha.cjs`. Verifica colisão do apoio com cadeira recuada 5 versus 41, colisão da central na descida final e separação após recuo de 32,5, círculo envolvente do giro e conservação das margens sobre a metade em 151 posições. Sem fotogrametria, pesquisa externa ou validação física; apresentação visual ainda não inspecionada.


**Consolidação posterior:** a direção atual de operação está em [Mesa completa](Mesa_completa.md): apoio temporário no assento do banco, fora das metades móveis. Este documento preserva a etapa anterior; consultar a consolidação para o ciclo vigente de estudo.
