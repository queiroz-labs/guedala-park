# Mesa extensível — consolidação da folha e do conjunto

30/09/2026. Entrega solicitada por Elias: avançar a questão da folha e gerar um HTML completo da mesa. [Abrir apresentação consolidada](Mesa_completa.html).

## Fechamento do estudo de operação

Adotar como **proposta técnica prioritária** o apoio temporário no assento do banco, em lugar da alternativa anterior sobre uma metade móvel. A folha permanece parada e fora dos tampos enquanto a mesa abre. Não é novo aceite de usuário para cotas executivas; não autoriza fabricação.

O conjunto preserva mesa 150/180 × 75, Arenza, cantos externos R15, base fixa central redonda com sapata oval preta, folha 75 × 30, guarda no banco e três cadeiras na lateral livre. Espessura de 3, nicho livre 80 × 35 × 7 e ferragens continuam referências de estudo. O HTML reúne programa, dimensões, sequência, base, apoios, cadeiras, circulação, critérios e referências locais, sem pesquisa comercial nova.

## O apoio que evita movimentar a folha junto com o tampo

Coordenadas anteriores: u=0 na frente do banco, positivo para a parede; v=0 na ponta próxima ao sofá, positivo para a cozinha. Altura independente desde o piso. Assento no modelo u=0–45/v=0–180, topo a 47; encosto u=45–55, topo a 90. Tampo chega a u=5 sobre o banco.

Folha apoiada **u=10–40 / v=100–175**, face inferior a 48 e superior a 51, admitindo proteção de ensaio de 1 sobre o assento. Há 5 até a borda do tampo, 5 até o encosto e 5 até a ponta do banco. A folha cabe inteiramente na superfície de assento modelada. A folga de 5 ao tampo permanece durante toda a abertura, porque só v varia nas metades.

Isso demonstra posição e ausência de colisão com os tampos, não estabilidade da folha sobre estofamento. A proteção precisa distribuir apoio, evitar marcação e escorregamento, sem presumir que pano ou espuma solta sejam suficientes. Considerar curvatura, compressão e inclinação do assento real no protótipo. Banco desocupado durante a operação.

## Ciclo geométrico completo

1. Afastar temporariamente a cadeira da ponta 5 rumo à sala e a central 32,5. Reservas conservadoras com envelopes inteiros das cadeiras até 94 de altura; contorno real ainda pode permitir menos.
2. Retirada baixa conforme [Folha_mesa](Folha_mesa.md): puxar 35 para fora do nicho e deslizar 67,3 rumo à cozinha. Folha termina u=−32,5–−2,5/v=168–243, ainda fora da ponta da mesa fechada. A condição da coluna permanece.
3. Elevar verticalmente a folha até altura inferior 97. Sem girá-la, mover o centro transversal de u=−17,5 até 25; depois o centro longitudinal de v=205,5 até 137,5. A peça chega acima do assento com faixa u=10–40/v=100–175.
4. Baixar a folha sobre a proteção no banco, altura 48–51. Verificar apoio estável antes de soltá-la. Abrir a mesa: cada metade percorre 15 no sentido oposto, enquanto a folha permanece parada no banco.
5. Elevar novamente até altura inferior 97; mover o centro de u=25 até u=10. Girar 90° no plano horizontal ao redor de (10;137,5). O giro precisa ocorrer elevado, acima do encosto do banco, nunca apoiado no assento.
6. Com a peça ainda elevada, levar seu centro a (−32,5;90), sobre o vão central. Baixar nominalmente até altura inferior 72, superior 75. A folha passa a u=−70–5/v=75–105. A inserção de pinos e folgas de montagem depende de curso extra a especificar; o encaixe exato entre retângulos não comprova a montagem real.
7. Assentar em apoios próprios, aproximar juntas e acionar travas conforme a ferragem definida. Recolocar cadeiras no arranjo de uso, com percurso real a testar. Para recolher, inverter a lógica: levantar a folha para o banco, fechar tampos vazios e retornar ao nicho.

As mãos, corpo e força do operador não foram modelados; não afirmar que uma pessoa executa confortavelmente a sequência. A folha é tratada como peça rígida, sem peso especificado. Seu peso real, saliências, pega e material devem entrar no protótipo.

## Verificações

Script `mesa_completa.cjs`: **2.010 posições** em dez transições posteriores à retirada baixa, com polígonos orientados e teste por eixos separadores, incluindo intervalos verticais. Zero interseções com os obstáculos idealizados: assento, encosto, três cadeiras nas posições temporárias, corpo fechado da geladeira, coluna de teste e duas metades da mesa. O teste não inclui porta do nicho, sapata, travessas/ferragens reais ou operador.

A retirada baixa tem cálculo separado de 1.402 posições; a nova posição da cadeira central é mais afastada que a usada naquele estudo. A amostragem não substitui protótipo, mas as principais folgas têm confirmação analítica:

- Apoio estacionário a u=10–40, fora dos tampos até u=5 durante toda a abertura: 5 cm de separação.
- Rotação do retângulo 30 × 75: raio envolvente √(15²+37,5²)=40,388736. Centro u=10 → maior u possível 50,388736; parede em u=55 deixa **4,611264**.
- Na rotação, face inferior a 97, contra topo do encosto do banco 90 e cadeiras 94: separações verticais 7 e 3.
- Folha elevada termina a 100; globo mais baixo a 155 no cenário: 55 de separação vertical.
- Cadeira central recuada termina em u=−73; folha no vão começa em u=−70: 3 de separação na descida. As cadeiras das extremidades ficam fora da faixa longitudinal v=75–105.

No trecho baixo, a folga à coluna continua 10,7−D/2: D=12 deixa 4,7; D=20 deixa 0,7. Para margem comparativa de 3, D≤15,4. **Não usar esse limite para dimensionar ou reduzir a coluna estrutural.** Se a estrutura real exigir volume maior, o acesso do nicho precisa ser redesenhado. Margens escolhidas são critérios de ensaio, não normas.

## Entrega para detalhamento executivo

O estudo fecha uma proposta operacional completa e a apresentação geral da mesa. A execução exige desenho do conjunto base/quadro/ferragem, estabilidade, cargas, porta e estrutura do banco, proteção do assento, contorno real das cadeiras, curso adicional para pinos e protótipo de manuseio. Ainda não é uma solução liberada para fabricação.

Referências: [anteprojeto](../Sala_e_jantar/Mesa_extensivel_anteprojeto_R00.md), [cadeiras e circulação](../Sala_e_jantar/Mesa_circulacao_entrada_2026-09-23.md), [alturas/base/banco](../Sala_e_jantar/Ajustes_integrados_R01.md), [retirada baixa](Folha_mesa.md). O [apoio anterior sobre metade móvel](Apoio_folha.md) fica histórico, superado como direção de desenvolvimento por este apoio no banco.

Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/mesa_completa.cjs`. Gera HTML autônomo e [resultados](Resultados_mesa_completa.json), sem rede, bibliotecas externas ou imagens remotas. Controles e links verificados separadamente; renderização visual não inspecionada nesta rodada. Nenhuma compra, fabricação, publicação ou contato com fornecedor.
