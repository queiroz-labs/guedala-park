# P15 — composição parcial das duas chapas

**Complemento vigente 25/10:** [ligações e suspensão do lote A](../../Aereos_suspensao/README.md). Preserva 8 Minifix; distingue seis Confirmat candidatos na caixa atual e 18 na variante de fundo prolongado. Na lateral que desce 18, eixo Z9 fica **27 mm da nova borda inferior**, não 9. O mapa não especifica a interface entre camadas nem comprova composição; as condições deste estudo continuam abertas.

O [corpo de prova fundo–laterais](../../Aereos_suspensao/Roteiro_apoio_caixa.txt) tem somente fundo inteiro, duas laterais e seis ligações candidatas. A variante 598 corrige os eixos desde a borda física Z−18; não contém base 18+18 nem demonstra composição ou capacidade global.

25/10/2026. **A ligação entre as duas chapas é parte do cálculo; não basta somar 18+18.** Este bloco substitui a comparação apenas entre os extremos por um modelo de deslizamento contínuo. Reutiliza a geometria e os apoios do [estudo P15 separado](../../Ligacoes_sem_tubos/README.md), sem alterar a R51 ou criar outro CAD.

**Decisão de produto:** a Titebond Melamine Glue fica excluída da justificativa de sustentação dessa base: o próprio fabricante veda aplicações estruturais ou de sustentação de carga. Não havia adesivo selecionado. A indicação genérica para melamina e resultados curtos da ficha não autorizam esse uso. [Ficha oficial, Limitations](https://www.titebond.com/print/product/c9121dfd-2a9d-46d0-bd6d-c183e64bd0cd).

## Modelo e unidades

Placa 799×312 com duas camadas 17,7 resistentes e 18,3 de massa cada, densidade hipotética 800 e ν0,30. Mesmos dez pontos, juntas flexíveis e fundo 598 do cálculo anterior. E inicial 2200/1600 é reduzido pela metade para a sensibilidade diferida. Carga mista: 15 kg distribuídos +5 kg numa área 50×60 frontal central, além do peso próprio; não são 20 kg por camada.

As camadas têm o mesmo deslocamento vertical w, mas podem deslizar no plano. A interface idealizada tem rigidez uniforme **ks em N/mm³**: tensão de cisalhamento τ=ks×deslizamento. Não é resistência em MPa, nem rigidez de um parafuso em N/mm. Para um filme homogêneo isolado, G/espessura teria essa unidade, mas a junta real inclui superfícies e substratos, além de imperfeições. Não se atribuiu ks a um produto.

Derivação energética própria, com bases Legendre nas duas direções:

`U = (1/2) wᵀK0w + (1/2) aᵀ(2Km)a + (ks/2) ∫|2a + t∇w|² dA`

`K0` soma a flexão própria das duas chapas; `Km` é a membrana de uma camada; `a=(u,v)` é o deslocamento de membrana antissimétrico e `t=17,7`. A condensação dos campos u/v gera a rigidez equivalente de flexão, preservando os três modos rígidos. No limite sem transferência, soma duas rigidezes 18; com transferência infinita, recupera a chapa 35,4. O programa confere esses limites com a rotina anterior e compara uma interface finita à montagem direta dos três campos.

Essa derivação não é aplicação normativa do método Gamma para vigas. A pesquisa primária consultada investiga sua dependência das condições de contorno; foi lido o resumo, sem importar coeficientes para nossa placa. [Registro Chalmers/WCTE2018](https://research.chalmers.se/en/publication/507133).

## Resultados da sensibilidade

Flecha máxima +reserva 0,20, em mm, grau 14 nesta tabela. Referência interna 799/300=2,663 mm. As colunas são hipóteses de painel; nenhuma é propriedade certificada do MDF escolhido.

| ks hipotético, N/mm³ | E inicial 2200 | E inicial 1600 |
|---:|---:|---:|
| 0, camadas sem transferência de cisalhamento | 4,285 | 5,462 |
| 0,01 | 3,990 | 4,980 |
| 0,1 | 2,894 | 3,463 |
| 1 | 1,985 | 2,401 |
| 10 | 1,763 | 2,144 |
| 100 | 1,718 | 2,089 |
| 1000 | 1,707 | 2,076 |
| Composição integral ideal | 1,704 | 2,073 |

No grau 18, o cruzamento matemático com a referência ocorre perto de ks0,151/0,417, para E inicial 2200/1600. **Esses cruzamentos não são requisitos executivos nem critério de aceitação de adesivo:** ficam praticamente sem margem, dependem da hipótese uniforme e não cobrem dano, distribuição real das juntas, duração ou ambiente. A diferença 14/18 da flecha perto desses pontos ficou abaixo de 0,085%.

O resultado útil é a curva completa: a composição não é binária, e uma ligação que perde rigidez ao longo do tempo pode deslocar o comportamento para o lado mais flexível. O ks de serviço não foi medido; reduzir o E das chapas não modela automaticamente a fluência da linha de colagem.

## Cisalhamento e o que ainda não está validado

O JSON inclui campo de cisalhamento/deslizamento da interface, com máximos amostrados excluindo 30/50 mm em torno dos pontos de apoio. No exemplo ks1/E inicial 2200, o pico fora de 30 mm varia aproximadamente 0,0282→0,0279→0,0275 MPa nos graus 14/18/22. É uma triagem global, não tensão admissível da cola. Picos junto a furos, bordas, apoios, mudanças de rigidez e defeitos precisam de modelo/local e ensaio próprios.

O deslocamento vertical comum pressupõe ligação/contato normal entre camadas: **não foi calculado descolamento, abertura da junta ou delaminação**. A interface é elástica e uniforme, sem áreas sem cola, falhas de preparação, umidade, degradação, plasticidade ou fluência. O apoio traseiro e as juntas da caixa continuam os requisitos condicionais do estudo anterior.

O manual técnico USDA diferencia superfície, processo, propriedades e desempenho prolongado do conjunto colado; uma medição curta de resistência não encerra o comportamento em serviço. Não se escolheu um adesivo apenas pela família química ou por uma tensão publicada. [USDA/FPL, capítulo 10,2021](https://research.fs.usda.gov/download/treesearch/62250.pdf).

## Perguntas e prova necessárias

1. **Painel/oficina:** quais faces internas serão coladas, cruas ou revestidas? Qual é a constituição e espessura real de cada camada e como se preservam as faces aparentes? Não remover revestimento ou alterar espessura silenciosamente.
2. **Fabricante do sistema:** qual produto e processo são expressamente adequados à laminação que participa da sustentação, no substrato/acabamento real e ambiente da lavanderia? Fornecer condições de aplicação, cura, prensagem e durabilidade; produto que exclui esse uso não entra como candidato.
3. **Ligação real:** qual a curva cisalhamento–deslizamento por área do conjunto, inicial e após condicionamento/tempo, com ruptura/abertura também registradas? A curva deve incluir a interface e o MDF, não só o filme de cola isolado.
4. **Conjunto:** fabricar e ensaiar composição e caixa representativas conforme protocolo definido com profissional/oficina. Usar o [roteiro existente](../../Ligacoes_sem_tubos/Roteiro_ensaios_e_requisitos.md) e registrar material/processo, carga real, tempo, deslocamentos, residual e danos. Nenhum ensaio já foi executado.
5. Depois de obter os dados, substituir as hipóteses, verificar margem e incorporar apenas se a composição/caixa estiver demonstrada e a mudança visual externa de 18 mm inferior for revisada por Elias. O interior é preservado no estudo atual; a R51 continua com a base original.

## Reprodução e conferências

`python calcular.py`, com NumPy. [Resultados](Resultados.json): 16 cenários de resposta, cruzamentos aproximados, refinamento de cisalhamento e cinco verificações principais. [Verificação](Verificacao.json): equilíbrio, compatibilidade, monotonicidade da flecha, dois limites independentes, três campos diretos versus condensados, convergência, hashes e fonte. [Fontes e limites de leitura](Fontes.json). Nenhuma medida do apartamento foi inventada e nenhum produto foi comprado ou liberado.
