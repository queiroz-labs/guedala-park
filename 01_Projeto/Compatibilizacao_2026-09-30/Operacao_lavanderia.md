# Operação da lavanderia — 30/09/2026

[Planta de uso](Operacao_lavanderia.html) · [contas](Resultados_operacao.json). Continuação do [cesto](Cesto_retirada.md).

## Resultado

**Desenvolver uso alternado: retirar o saco com a máquina fechada; fechar o cesto antes de abrir a máquina.** Dois gabaritos de pessoa cabem nas cenas separadas do estudo, mas suas posições conflitam com o outro mecanismo aberto. Isso orienta a operação e o próximo protótipo, sem declarar conforto ou segurança pela simples presença de um retângulo.

**A guarda do banquinho na faixa inferior da parede junto à janela não fecha neste arranjo.** Entre pedra e lixeira há 48 cm para a reserva de 45; depois de reservar o giro da frente, restam apenas 17,85 cm, faltando 27,15. Não definir suporte ou furação nessa faixa. Manter modelo e acesso fácil como requisitos; outra face de guarda precisa de conferência própria, sem mover lixeira ou cesto automaticamente.

## Referências e coordenadas

Planta local: x=0 na parede da janela, x crescendo rumo à cozinha; y=0 na parede hidráulica, crescendo para a parede oposta. Adotados 129 × 154 cm da [conferência documental](../Lavanderia/Conferencia_documental_lavanderia_2026-09-25.md), sem nova medição. O modelo 3D tem piso 129 × 161: não usar seus 7 cm extras para justificar encaixe nesta revisão.

Do [3D ilustrativo](../Estudo_interativo/src/app.js), aproveitam-se relações laterais, não precisão executiva: módulo do tanque x=0–59; máquina x=65–125. A conferência local da LG fornece projeções de 72 fechada e 120 aberta incluindo a reserva posterior. Niche de teste x=63–127 preserva 2 cm por lado. Sobram 4 cm entre o módulo de 59 e o início desse vão, mais 2 cm até o limite 129; são saldos brutos, não autorização para distribuir proteção, laterais ou instalações sem corte.

A lixeira do modelo tem envelope 29 × 29 e tampa fechada até 43,7 cm de altura. Sua posição junto ao canto é normalizada conservando as margens de 2 cm às duas paredes: **x=2–31/y=123–152** em ambiente de 154. No 3D de 161, a mesma relação de canto resulta em y=130–159. Não se trata de deslocamento físico aprovado; as duas bases ainda não são levantamento. Tampa, pedal e retirada do balde precisam de espaço adicional; a lixeira permanece fechada nas cenas calculadas.

Não foi introduzida porta entre cozinha e lavanderia. A porta indicada no desenho é a da LG. Sua reserva x=63–127/y=72–120 representa o alcance axial e o vão da máquina, **não um setor de giro real confirmado**. Dobradiça, espessura, pega e percurso lateral do modelo exato continuam a conferir. O trecho de comunicação com a cozinha também precisa de planta acabada; a borda direita do desenho não é uma parede inventada.

## Cenas separadas

| Cena | Gabarito de pessoa proposto | Condição |
|---|---|---|
| Abrir cesto e retirar saco | x=62–92/y=80–125; 30 × 45 cm, orientação lateral | Máquina e lixeira fechadas; corpo separado 3,2 cm do envelope frontal de teste do cesto |
| Carregar LG | x=7–52/y=80–110; 45 × 30 cm | Cesto fechado; lateral esquerda da máquina disponível no ensaio |
| Ambos abertos | Não adotada como cena de operação | A posição lateral do cesto invade a reserva da porta; a posição da LG invade a frente do cesto |

Esses retângulos são hipóteses comparativas, não medidas de Elias, norma antropométrica, alcance validado ou corredor mínimo. Faltam braços, inclinação do tronco, pés, pegada bilateral do saco e transição da pessoa. Não recomendar ficar na frente do saco usando os 28,17 cm residuais do corte como se fossem espaço suficiente.

Sequência de teste: máquina fechada → cesto abre → saco sai → cesto fecha → saco é mantido/posicionado fora do giro da porta → máquina abre → carregar pela lateral. Não foi escolhido um novo lugar permanente para apoiar roupa no piso. Se o peso impedir segurar o saco durante a transição, o ensaio precisa incluir apoio temporário sem bloquear porta/cesto; o tanque limpo já é o apoio funcional aprovado para roupa molhada, não comprovação de que o saco inteiro passe ou caiba ali.

## Sobreposição em planta não basta para declarar colisão

O saco de teste chega a y=125,83 e sua faixa x=9,5–49,5 cruza parcialmente a lixeira, que começa em y=123. Foi recortado o polígono lateral do saco em 891 posições de extração. Na parte projetada sobre a lixeira, a menor separação vertical até a tampa fechada é **18,27 cm**. Depois, ao endireitar, o saco fica até y=101,59 e sai dessa sobreposição.

Isso afasta a colisão entre esses dois volumes idealizados com tampa fechada. Não valida tecido pendente, alças soltas, tampa levantada, mão no pedal ou retirada simultânea do balde. A planta colore essa faixa de sobreposição como advertência de uso, não como impossibilidade geométrica comprovada.

## Banquinho: alternativa de guarda que pode ser descartada nesta faixa

A [guarda proposta](../Lavanderia/Banquinho_guarda_e_acesso_2026-09-25.md) reserva 45 cm ao longo da parede, projeção até 25 e altura 10–95 para o modelo fechado. Sob a janela, entre y=75 e 123, caberia somente com origem y=75–78; nessa posição a reserva x=0–25 atravessa o giro do cesto e da frente. Como a reserva vertical abrange o movimento, não é apenas sobreposição gráfica.

Para ficar depois da frente aberta (até y=105,15), sobram 17,85 cm antes da lixeira. Faltam 27,15 cm para os 45 reservados, sem sequer acrescentar pega/retirada. Mesmo usando a largura de produto de 39,5 cm em vez da reserva de 45, o déficit é 21,65 cm. O retorno em L e suportes podem piorar esse resultado; não foram usados para favorecer o encaixe.

Portanto, retirar essa faixa da lista de locais liberáveis para suporte. Não substituir o banquinho, colocá-lo no alto ou transferir lixeira. A próxima localização deve manter retirada fácil, fora do varal/aquecedor e demonstrar seu caminho em planta e elevação.

## Verificação e limite

Cinco relações de interseção pessoa/mecanismos conferidas por retângulos; déficit do banquinho calculado; seção do saco recortada contra y=123. Fontes são documentos já arquivados, sem consulta de produto novo. A posição lateral é candidata de operação, não resultado ergonômico validado. Planta e desenho não substituem levantamento, protótipo ou o volume das roupas do varal baixo.

Commit anterior ao início deste assunto: **571da11**, com os estudos acumulados de 28 e 30/09. Esta continuação fica separada para revisão; nenhuma publicação ou envio a terceiros.
