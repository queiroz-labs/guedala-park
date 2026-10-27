# P01/P06 — ajuste vertical e retirada

Conferência T05 de 26/10/2026, independente de resposta da FGVTN. [Dados dos 132 casos](Ajuste_vertical_retirada.json). Base persistida R52 e proposta dimensional de caixas 500, sem abrir ou alterar o FreeCAD nesta etapa. Não houve ensaio físico nem simulação dos engates reais.

## Ajuste de 0 a +3 mm

O +3 vem da instrução FGVTN Set24 arquivada, referenciada no [README](README.md). Testamos a translação vertical uniforme da caixa em 0…3 mm; não a regulagem desigual dos dois engates, torção, folgas de montagem ou deformação. O datum comercial ainda precisa ser confirmado.

| Interface entre frentes ou obstáculo superior | Folga inicial | Pior folga com ajustes independentes 0…3 |
|---|---:|---:|
| P01 direita: Gaveta → Gaveta001 | 8 mm | 5 mm |
| P01 esquerda: Gaveta002 → Gaveta003 | 8 mm | 5 mm |
| P06 G3 → G2 | 4 mm | 1 mm |
| P06 G2 → G1 | 4 mm | 1 mm |
| P01 Gaveta001 → prateleira Peca245 | 2 mm | **−1 mm** |
| P01 Gaveta003 → prateleira Peca246 | 2 mm | **−1 mm** |
| P06 G1 → bancada Peca308 | 3 mm | **0 mm** |

Entre gavetas: `folga = folga inicial + ajuste da superior − ajuste da inferior`. A pior condição é a inferior em +3 e a superior em zero. Contra prateleira/bancada fixa, subtraem-se os 3 mm. Os envelopes das frentes e obstáculos se cruzam em planta, por isso a cota vertical importa.

**Não usar +3 como ajuste livre da gaveta inteira com frente solidária.** Nas duas superiores P01, o envelope da frente invade o da prateleira em 1 mm. Na superior P06, toca a bancada, sem margem; o algoritmo de volume não acusa esse contato tangente, que foi identificado pela cadeia de cotas. Mesmo 1 mm restante entre frentes P06 não é reserva de fabricação demonstrada.

### Frente realinhada: alternativa a detalhar

No segundo cenário, caixa e conteúdo podem subir até 3 mm, mas a frente decorativa permanece em sua posição nominal. Isso equivale a permitir compensação relativa de até 3 mm na fixação da frente. **É uma hipótese de montagem**, não um mecanismo já existente ou validado.

Com essa hipótese, a triagem contínua não encontrou sobreposições entre os envelopes móveis e os obstáculos selecionados, nas sete gavetas, tanto R52 quanto proposta 500, com a porta correspondente do P01 deslocada 600 mm. As folgas decorativas nominais ficam preservadas. [Fixação candidata detalhada](Fixacao_frentes.md): 28 pontos, passagemØ8 e dois alojamentos baixos G2; produto, usinagem, aperto e retenção ainda pendentes; não extrapolar o estudo das frentes P16 para estas sete gavetas.

O fundo e bandejas G2 mantêm sua relação vertical: sobem juntos. A conclusão anterior de fundo com 15 mm e topo Z628 em posição nominal continua válida; não baixar as bandejas para acomodar um excesso de envelope.

## Abertura normal e primeira retirada reta

O estudo usa −Y global, coerente com as expressões de extensão salvas. A abertura normal documental é **475 ±3 mm**, distinta da profundidade 500. A tabela abaixo é da proposta de caixas 500:

| Grandeza | P01 (4) | P06 (3) |
|---|---:|---:|
| Plano frontal da carcaça Y | 3372 mm | 6410 mm |
| Traseira da caixa fechada Y | 3880 mm | 6908 mm |
| Caixa ainda para dentro do plano em C472 | 36 mm | 26 mm |
| Em C475 | 33 mm | 23 mm |
| Em C478 | 30 mm | 20 mm |
| Translação total para traseira coincidir com o plano | 508 mm | 498 mm |
| Trecho reto hipotético testado, com 1 mm além do plano | 509 mm | 499 mm |
| Trecho adicional após C475 até esse ponto | 34 mm | 24 mm |

O milímetro adicional é apenas margem aritmética para cruzar o plano. **Não é curso de desengate, espaço para mãos ou altura de levantamento.** Na R52 com caixas 490, os valores correspondentes para coincidir com o plano são 498/488 mm; o acréscimo de profundidade exige mais 10 mm de retirada.

A varredura cobre continuamente o percurso desde fechado até 478 e até 509/499 na proposta, combinada com ajuste uniforme 0…3. O trecho além do curso só descreve uma caixa supostamente desengatada e sustentada externamente. Não comprova que a guia permita a transição, nem que a retirada real seja horizontal: eventual levantamento/inclinação precisa do engate e do gancho traseiro corretos.

### Portas P01 e sequência de manutenção

Com as portas fechadas, os envelopes das gavetas cruzam as folhas Peca247/Peca248. Isso é uma condição de operação já conhecida, não nova falha do modelo. Para a coluna direita, a folha direita foi deslocada 600 mm para a esquerda; para a esquerda, a folha esquerda 600 mm para a direita, conforme cenários salvos. Não mover ambas indiscriminadamente nem concluir que as duas colunas ficam acessíveis ao mesmo tempo.

Roteiro condicionado a completar o desenho da ferragem:

1. Esvaziar a gaveta; em G2, retirar utensílios e bandejas quando houver acesso. Pega e levantamento das bandejas não foram dimensionados.
2. P01: posicionar a folha correspondente para liberar a coluna; manter as outras gavetas fechadas. P06: preparar o espaço frontal.
3. Abrir até o curso efetivo e sustentar a gaveta antes de liberar os dois engates. A simulação não dimensiona esse apoio nem a postura de manuseio.
4. Acionar ambos os engates conforme o produto, com acesso simultâneo sob os cantos frontais. Só depois executar o movimento prescrito de retirada. O trecho reto calculado não substitui essa instrução.
5. Na remontagem, verificar encaixe, retenção, curso e alinhamento das frentes; ajuste vertical não pode consumir as folgas críticas acima.

## Método e alcance

Foram **132 casos e 1.078.560 pares de envelopes**: R52/proposta, frente acompanhando/realinhada, porta P01 fechada/aberta e caixa fechada/percurso até 478/retirada reta hipotética. A caixa varrida abrange todos os deslocamentos intermediários, sem depender de amostragem só nas pontas. Pares candidatos existentes em posição fechada ficam registrados separadamente.

Obstáculos: peças Part/PartDesign com sólidos e visibilidade na cadeia de pais da base salva, sem agregados duplicados. As referências GuiasComuns/GuiasG2 e T51 foram **explicitamente excluídas** e listadas no JSON, pois não representam a montagem FGVTN demonstrada. Logo, ausência de encontros não prova folga com a corrediça. Aberturas simultâneas, mãos, ferramentas, pessoas, tolerâncias, cargas e inclinação não estão no teste. Sobreposição de envelopes é triagem; não uma colisão BRep confirmada.

Reproduzir na raiz: `python -B ferramentas/conferir_ajuste_retirada_gavetas.py`. O script verifica o SHA do CAD contra a base e proposta, as expressões de movimento e a presença dos cenários de porta 600. Lê somente dados; não altera controlador, forma, base ou arquivo CAD.

## Melhor momento para alterar o FreeCAD

**Ainda não recomendo incorporar estas gavetas ao modelo principal.** A geometria já permite preparar a revisão, mas ainda há decisões que mudam furos, recortes, posição e acesso:

- identificar o engate exato e obter seu gabarito/envelope, por resposta da FGVTN ou documentação equivalente confiável;
- fechar o datum de montagem e a fixação das frentes com compensação do ajuste, resolvendo os limites de 2/3 mm sem criar folgas insuficientes;
- definir a sequência real de desengate/retirada e conferir acesso, levantamento se necessário e gancho traseiro;
- consolidar o mapa de peças/usinagem da caixa 500, preservando o fundo G2 de 15 mm e as bandejas, sem escalar furos importados.

**Esse é o marco recomendado para pedir a alteração:** montagem definida e verificável, antes de atualizar fichas e pacote de execução. Não é necessário esperar toda a obra nem todos os ensaios de carga para testar uma revisão geométrica; esses limites podem continuar registrados. Porém, editar agora o principal obrigaria a inventar a ferragem ou refazer interfaces ainda abertas.

Quando houver esses dados e pedido explícito de alteração, testar primeiro em cópia fora do projeto; aplicar a solução ao vigente somente após conferir a montagem. Executar a verificação completa e relatório, apresentar diferenças e seguir a regra de aprovação da base. Não atualizar base ou cenário para esconder conflito. Até esse marco, a proposta documental permanece separada e a R52 preservada.
