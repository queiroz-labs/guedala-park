# Banquinho — sequência de retirada com a cama aberta

30/09/2026. Continuação autônoma, sem Firecrawl ou consulta externa. [Prancha em quatro etapas](Banquinho_operacao.html). Complementa o [estudo de guarda](Banquinho_alternativa.md), sem aprovar essa localização.

## Resultado

Existe uma sequência sem colisões dos retângulos idealizados para um gabarito de corpo de **40 cm de profundidade × 50 cm de largura**, mantendo o banquinho na mesma orientação. A retirada deixa 5 cm à cama e 3 ao objeto. Não é dimensão de Elias, norma, envelope validado de manuseio ou confirmação de conforto.

O conjunto ocupa 68 cm na largura durante o transporte. Na linha de um vão **hipotético** x=145–220, a trajetória escolhida deixa apenas 2 cm à esquerda e 5 à direita. A folha de referência de 75 cm não equivale automaticamente a 75 cm livres. Logo, a posição sob a TV permanece **candidata secundária**, sem suporte definido ou mudança da marcenaria vigente. Não há novo aceite do usuário para o local.

## Bases e hipóteses

Coordenadas e móveis são os do [estudo anterior](Banquinho_alternativa.md): quarto 230 × 295, cama x=2–142/y=110–292, cadeira x=150–224,5/y=75–148, bancada até y=70. Banquinho reservado em x=205–230/y=165–210. A altura continua condicionada ao apoio de até 3 cm e à borda inferior hipotética da TV a 81.

Porta **já aberta a 90°**, idealizada na linha x=220, y=220–295. Não se ocupa o setor de giro durante a abertura da porta: a sequência pressupõe a folha parada e aberta. O setor inteiro, usado antes para verificar a guarda fixa, não é um obstáculo maciço durante a circulação. Espessura da folha, maçaneta, batentes e vão acabado não medidos; não desenhados como se fossem conhecidos.

Não foi simulada uma pessoa girando o corpo ou segurando a porta. O gabarito se mantém de frente para a parede da TV e se desloca lateralmente rumo à entrada. Isso é uma hipótese de movimento, ainda dependente da pega e postura reais. A prancha mostra posições, não uma demonstração de habilidade física.

## Sequência calculada

| Etapa | Gabarito de pessoa | Banquinho | Movimento |
|---|---|---|---|
| 1. Aproximação | x=147–187; y=242,5–292,5 até 162,5–212,5 | x=205–230; y=165–210 | 80 cm rumo à janela, começando dentro do quarto |
| 2. Pega | x=147–187 até 162–202; y=162,5–212,5 | Permanece guardado | 15 cm para a direita |
| 3. Retirada | x=162–202 até 147–187 | x=205–230 até 190–215 | Ambos recuam 15 cm, mantendo 3 cm entre retângulos |
| 4. Transporte | x=147–187; y=162,5–212,5 até 242,5–292,5 | x=190–215; y=165–210 até 245–290 | 80 cm rumo à entrada, sem girar o objeto |

Após a etapa 3, a face posterior do banquinho fica em x=215, 3 cm antes da projeção x=218 da TV usada no modelo. Esse é o momento candidato para levantar a peça. A elevação e a flexão da pessoa não foram calculadas; mãos, alças, pés e saliências podem aumentar os envelopes. O transporte não representa arrastar o banquinho pelo piso.

O ensaio termina **antes da soleira**. A comparação de larguras na porta é uma triagem, não uma trajetória validada de saída. Não há planta do corredor externo neste cálculo. A abertura do próprio banquinho para subir também está fora do escopo.

## Sensibilidade e critério de continuidade

Mantida a face do corpo em x=187 ao final da retirada e 3 cm entre pessoa e objeto:

| Profundidade hipotética | Folga à cama | Largura pessoa + intervalo + banquinho | Margem esquerda no vão ideal |
|---|---|---|---|
| 30 | 15 | 58 | 12 |
| 35 | 10 | 63 | 7 |
| 40 | 5 | 68 | 2 |
| 45 | 0 | 73 | −3 |
| 50 | −5 | 78 | −8 |

O gabarito de 45 toca a cama; não deve ser interpretado como passagem aceitável por ter interseção de área zero. O de 50 invade a cama. A reserva lateral de 3 cm é um critério de comparação escolhido para este estudo, **não norma**: 48−3−3=42 seria a profundidade máxima nessa retirada para preservá-la nos dois lados. Na porta, o trajeto de 40 já cai abaixo desse critério do lado esquerdo. Eventual recentralização perto da entrada seria outro movimento a validar, não uma correção automaticamente adotada.

Larguras de gabarito de 45, 50 e 55, com profundidade 40, também foram calculadas. A de 55 chega exatamente ao limite y=295 no ponto final escolhido, embora não colida com os móveis; fica sem reserva longitudinal antes da soleira. Não confundir ausência de colisão mobiliária com cruzamento do vão validado.

São quatro etapas com 201 amostras cada. Continuidade entre etapas verificada. A separação também pode ser conferida sem amostragem: x mínimo do corpo é 147, acima da cama até 142; o banquinho nunca passa de x=190 para a esquerda; ambos permanecem após y=162,5, enquanto cadeira termina em 148 e bancada em 70. Na ida e na volta a folga pessoa/objeto é no mínimo 3. Parede e folha aberta idealizada permanecem à direita. As amostras não validam obstáculos omitidos.

## Sofá e encaminhamento

A manobra rígida F93/F94 já confrontada mantém **34,7834 cm** entre seu círculo envolvente e a reserva do banquinho. Esse resultado anterior permanece válido; não houve nova demonstração do mecanismo retrátil/reclinável, nem do operador movimentando o sofá.

Para promover o candidato, falta o gabarito físico de pega a baixa altura e passagem no vão acabado, com a cama aberta. Não detalhar suporte com base somente em retângulos. Os dados locais não justificam mudar altura da TV, reduzir a cama, trocar banquinho ou recolocar guarda no baú.

Reprodução: `node 01_Projeto/Compatibilizacao_2026-09-30/banquinho_operacao.cjs`. [Resultados](Resultados_banquinho_operacao.json). A memória e as figuras explicitam onde termina o cálculo; nenhuma compra, fabricação ou medição em obra realizada.
