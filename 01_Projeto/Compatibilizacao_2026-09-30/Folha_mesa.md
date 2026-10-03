# Mesa extensível — guarda e retirada da folha

30/09/2026. [Prancha](Folha_mesa.html). Desenvolvimento autônomo com documentos locais, sem Firecrawl.

## Resultado

O nicho livre proposto de **80 × 35 × 7 cm** comporta estaticamente a folha de **75 × 30 × 3**. A retirada frontal de 35 cm, sozinha, não permite levantá-la: ela continua sob o tampo. A sequência candidata passa a ser **retirar com a mesa fechada**, deslizar rumo à cozinha até sair da projeção da ponta e só então levantar para montar.

Essa ordem poupa 15 cm de manobra em relação a retirar depois de abrir a mesa. Exige afastar temporariamente a cadeira da ponta em 5 cm rumo à sala. O ensaio só preserva margem de 3 cm junto à coluna se seu diâmetro for até 15,4 cm. Como a base não está estruturalmente dimensionada, o acesso permanece condicionado; não impor uma coluna estreita para fazer o nicho funcionar.

## Fontes e escolhas preservadas

- [Anteprojeto da mesa](../Sala_e_jantar/Mesa_extensivel_anteprojeto_R00.md): 150/180 × 75, abertura simétrica, folha central 30 × 75, altura 75, tampo de estudo 3; guarda no banco aceita para desenvolvimento. Nicho 80 × 35 × 7 livre, acesso frontal proposto, não fabricado.
- [Cadeiras e circulação](../Sala_e_jantar/Mesa_circulacao_entrada_2026-09-23.md): três cadeiras na lateral livre, sem cadeira na cabeceira; envelopes globais e pedestal apenas de estudo.
- [Ajustes integrados](../Sala_e_jantar/Ajustes_integrados_R01.md): frente do banco x=685, banco de 180, distância transversal da frente à coluna de 32,5; faixa de referência de 84 entre ponta do banco e linha da bancada em trecho vizinho.
- [Modelo local](../Estudo_interativo/src/app.js): banco global x=685–740 / z=375–555; mesa fechada x=615–690 / z=390–540. Não alterar o site com este detalhe condicionado.

## Coordenadas e guarda proposta

Coordenadas locais em cm: u=0 na frente do banco, positivo rumo à parede; v=0 na ponta próxima ao sofá, positivo rumo à cozinha. Transformação para a planta global: x=685+u e z=375+v.

Banco: u=0–55, v=0–180. Mesa fechada: u=−70–5, v=15–165; aberta: v=0–180. Coluna no ponto (−32,5;90). O círculo de diâmetro 12 é hipótese, não especificação.

Nicho longitudinal proposto v=98,2–178,2, deixando reserva externa final de 1,8 até a ponta do banco. Esta é hipótese de painel terminal, não espessura estrutural aprovada. Nicho em profundidade u=0–35; boca inteiramente livre de 80 × 7, descontadas ferragens. Folha centralizada: u=2,5–32,5 e v=100,7–175,7. Sobram 2,5 por lado em planta e 4 no total em altura.

Uma seção de teste pode reservar z vertical=32–39, com folha a 34–37; os 2 abaixo e 2 acima precisam absorver apoios/proteção e pega. Não incluir ferragens salientes da folha ou pinos nos 3 cm sem conferência. Assento a 47 e estrutura do banco ainda precisam ser sobrepostos; este corte não dimensiona resistência do assento, divisórias ou travessas.

## Percurso proposto

1. Mesa fechada, sem ocupantes no banco. Afastar a cadeira próxima à cozinha 5 cm para a sala; manter as outras duas no lugar no ensaio.
2. Abrir o acesso do nicho, com portinhola e retenção fora da trajetória. Puxar a folha horizontalmente 35 cm: ela termina em u=−32,5 a −2,5, já fora do banco. Ainda não levantar.
3. Deslizar rumo à cozinha 67,3 cm. A folha passa a v=168–243: começa 3 depois da ponta do tampo fechado em 165. Margem escolhida para comparação, não norma. A modelagem usa o retângulo envolvente do tampo; não depende de ganhar espaço no canto R15.
4. Estudar a elevação da peça nessa posição e sua transferência. Só então abrir a mesa e assentar a folha nos apoios. A posição de apoio temporário enquanto se aciona a mesa não está definida; a sequência geométrica não comprova que uma pessoa possa segurar a peça e abrir o mecanismo ao mesmo tempo. Não presumir apoio sobre encosto/cadeiras ou porta do nicho.

O ganho demonstrado é retirar de sob o tampo fechado. O ciclo completo ainda exige resolver pega, elevação e apoio temporário. Pode-se estudar apoiar a folha sobre o tampo fechado com proteção, mas o percurso até esse apoio e a abertura da mesa com ela nessa condição não foram validados nesta rodada.

Com mesa já aberta, a folha precisaria começar em v=183, exigindo deslocamento de 82,3; sua ponta chegaria a 258. Contra uma linha conservadora v=264 (180+84), restariam 6 cm, em vez dos 21 do ensaio fechado. Essa linha prolonga uma referência do trecho vizinho para comparação: não representa obstáculo real confirmado em toda a faixa nem passagem para o operador. A peça fechada chega ao global x=652,5–682,5 / z=543–618. A geladeira gráfica termina em x=645: não coincide em planta com a peça, mas isso não verifica porta aberta ou usuário.

## Cadeira e coluna

Cadeira da ponta, na guarda: u=−79 a −32 / v=118–162. Na retirada, a folha chega a u=−32,5, entrando 0,5 no seu retângulo. Após afastamento de 5, cadeira termina em u=−37 e deixa **4,5 cm**. Não foi necessário retirar todas as cadeiras do cômodo. As demais não interceptam o percurso; sapatas/pés reais e mãos podem exigir espaço adicional.

O ponto do percurso mais próximo do eixo da coluna está a 10,7. Portanto, folga = 10,7 − diâmetro/2:

| Diâmetro de comparação | Folga |
|---|---:|
| 12 | 4,7 |
| 15 | 3,2 |
| 20 | 0,7 |
| 25 | −1,8 |
| 30 | −4,3 |

Com margem de comparação de 3: diâmetro máximo=2×(10,7−3)=15,4. Não há aprovação estrutural dessa dimensão. Sapata, ligação superior e travessas não são substituídas pelo cilindro da coluna: confrontar suas alturas reais com a folha a 34–37, sem presumir que a sapata seja sempre baixa.

## Verificação e próximo detalhe

Script verifica 1.402 posições em duas translações: detecta o conflito com a cadeira original, elimina-o na posição afastada e calcula a distância mínima à coluna. Separação longitudinal da folha à coluna é sempre pelo menos 10,7; o mínimo ocorre quando sua faixa transversal alcança o eixo. Isso confirma o mínimo analiticamente. Retângulos não incluem pessoa, peso, flexão do painel, portinhola, ferragens, estrutura interna do banco ou mecanismo real da mesa.

Entregar ao detalhamento o nicho na ponta do banco, o percurso em duas etapas e a sensibilidade da coluna. **Não liberar abertura na estrutura do banco** até compatibilizar coluna/sapata, porta e travessas. Manter mesa 150/180, guarda no banco e aparência da base; redesenhar o acesso se a estrutura necessária invalidar o percurso.

Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/folha_mesa.cjs`. [Resultados](Resultados_folha_mesa.json). Sem compra, fornecedor contatado ou alteração de escolhas. Renderização visual ainda não inspecionada.


**Continuação — apoio temporário:** [ciclo sobre uma metade da mesa](Apoio_folha.md). O recuo anterior de 5 cm da cadeira vale só para retirada baixa. O ciclo completo com envelopes conservadores de encosto exige 41 na cadeira da ponta e 32,5 na central. Folha apoiada sobre uma metade móvel depende da ferragem e do protótipo; não é uso aprovado.


**Consolidação posterior:** a direção atual de operação está em [Mesa completa](Mesa_completa.md): apoio temporário no assento do banco, fora das metades móveis. Este documento preserva a etapa anterior; consultar a consolidação para o ciclo vigente de estudo.
