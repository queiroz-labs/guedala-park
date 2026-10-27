# Conferência da bancada, torneira e porta

Estudo de 18/09/2026. Não libera fabricação ou furação. Vaso vigente: Celite VIP branco, kit 1977230012300. Base: profundidade nominal de 124 cm da planta P01; medidas acabadas e porta ainda não confirmadas.

## Resultado

Manter bancada de 60 × 45 cm como hipótese. A cuba nominal de 40 × 30 cm cabe geometricamente, com 10 cm por lado. Ainda não está comprovado que a Arion atrás da cuba funciona nessa profundidade, nem que o giro real da porta fica livre.

Na profundidade, ensaio: parede → faixa posterior de 10 cm → cuba de 30 cm → borda frontal de 5 cm. Espessura de eventual revestimento/espelho de pedra deve ser descontada da faixa posterior se ocupar esse espaço. Os 10 cm não são uma folga validada para a torneira ou para limpeza.

## Sensibilidade à profundidade

| Profundidade da bancada | Frente livre nominal | Folga ideal para folha de 70 cm | Para 75 cm | Para 80 cm |
|---|---:|---:|---:|---:|
| 45 cm | 79 cm | 9 cm | 4 cm | −1 cm |
| 47 cm | 77 cm | 7 cm | 2 cm | −3 cm |
| 50 cm | 74 cm | 4 cm | −1 cm | −6 cm |

Modelo idealizado: folha aberta a 90°, eixo na parede de entrada, entrando junto à lateral do lavatório; folga = 124 − profundidade da bancada − folha. Valor negativo significa sobreposição nesse modelo. Não inclui posição real do eixo, espessura da folha, batentes, maçaneta ou trajetória completa. Nenhuma dessas larguras de porta foi medida. Aumentar a bancada sem resolver a porta pode criar interferência.

## Arion centralizada atrás da cuba

A página Cassol identifica referência 73131B e informa altura total em torno de 30–30,5 cm, mas não apresenta desenho suficiente para confirmar alcance da saída, base, giro da alavanca e fixação. As dimensões genéricas de largura/profundidade da página não servem para liberar a montagem.

Conferir na peça ou desenho do fabricante: base inteiramente apoiada na faixa posterior; espaço de fixação e engates sob a pedra; saída e trajetória do jato dentro da cuba; alavanca em todo o curso sem tocar parede ou armário; acesso para limpar atrás da cuba. A torneira permanece escolhida, sem mudança de posição.

O armário espelhado proposto com 12–15 cm externos pode avançar sobre a região da torneira. Sua borda inferior e suas portas precisam liberar a alavanca e a abertura do próprio armário; só a profundidade rasa não garante isso.

## Altura de uso

Para Elias (1,75 m), permanece proposta de teste com borda da cuba a 90 cm e tampo a 76,5 cm, considerando cuba com 13,5 cm acima da pedra. Confirmar conforto com simulação física antes da fabricação. Não elevar o tampo a 90 cm somando depois a cuba.

## Dados necessários para concluir

1. Largura da folha, posição do eixo e projeção da maçaneta da porta, obtidas em medição ou detalhe de esquadrias.
2. Desenho dimensional ou medição física da Arion 73131B, incluindo alcance, base e envelope da alavanca.
3. Compatibilização final com parede acabada, armário, sifão e pontos de água.

Fontes: [planta oficial](../../09_Referencias/Plantas_e_manuais/Planta_oficial.pdf), [ficha Deca Slim](https://produtos.deca.com.br/Deca/L.13040.17/fichaTecnica/ficha_tecnica_1714550630635_L.13040.17.pdf), [Arion na Cassol](https://www.cassol.com.br/torneira-misturador-monocomando-para-banheiro-de-mesa-bica-alta-1x2polegadas-metal-arion-black-addra/p).

## Retorno de Elias e revisão documental

Elias informou que não possui medidas adicionais além dos documentos da construtora. Revisada visualmente a planta oficial P01: indica 209 × 124 cm e giro interno da porta, mas não cota sua folha. Memorial oficial Cury, p.15, especifica acabamento de portas/batentes e ferragens, sem largura da porta do banheiro. Não confundir a cota 1,05 m da circulação com a largura da folha. Portanto a largura permanece desconhecida; conferir na vistoria ou em futuro quadro de esquadrias. Não pedir novamente a Elias essa medida enquanto não houver nova documentação ou acesso ao imóvel. Bancada60 ×45 continua hipótese condicionada.

## T05 — manutenção do quadro BC43 na R52, 26/10/2026

[Memória com vinte cenários de porta, quatro laterais e seis de ferramenta](Fechamento_pre_entrega/Acesso_manutencao_T05.json). As faces do quadro, cavilhas, pedra, parede, porta e vaso foram reconciliadas com a base salva R52. Este bloco trata a montagem BC43 atual e complementa o [detalhamento de manutenção](../../04_Moveis/Avanco_pendencias/Banheiro_solucao/Detalhamento/Detalhamento.md); as hipóteses de bancada/porta de setembro acima permanecem identificadas pela data.

**Sequência preservada:** apoiar o conjunto e imobilizar as folhas → retirar os quatro M6 → puxar 20 mm → deslocar 120 mm à direita → retirar mais 330 mm. Não houve nova varredura BREP nem adoção de outro percurso. Os cálculos abaixo tornam explícitas as restrições desse trajeto, sem incluir mãos, maçaneta ou deformação.

### Primeira retirada e desencaixe

Cavilhas entram nominalmente 15 mm na caixa. A porta ideal de 700 mm termina 70 mm à frente do quadro antes da retirada. Para uma folha hipotética L e margem m em cada restrição, a primeira retirada t precisa satisfazer:

`15 + m <= t <= 70 − (L − 700) − m`.

| Folha hipotética | Intervalo com margem m=2 mm | O passo existente de 20 mm cabe nesse intervalo? |
|---|---|---|
| 700 mm | 17–68 mm | Sim, geometricamente |
| 725 mm | 17–43 mm | Sim, geometricamente |
| 740 mm | 17–28 mm | Sim, geometricamente |
| 750 mm | 17–18 mm | Não |
| 755 mm | Intervalo vazio | Não |

Uma folha de 750 não torna todo percurso imaginável impossível: estreita o intervalo desse primeiro passo. Não trocar 20 por 17/18 automaticamente, porque o restante da sequência, engates e acesso precisam de nova conferência. m=2 é sensibilidade, não folga de fabricação escolhida. A largura real da porta continua para documentação/vistoria; não foi solicitada uma medida que Elias ainda não tem.

### Passagem lateral entre porta e vaso

Depois de desencaixar, a largura do quadro continua 600 mm. Pelos planos X do modelo, o deslocamento lateral s fica entre 100 e 157,5 mm, com contato nos limites. O passo existente de 120 deixa **20 mm até a porta e 37,5 mm até o vaso**.

| Acréscimo hipotético h em cada lateral, representando volume adicional de manuseio | Intervalo geométrico de s | Folgas residuais com s=120 |
|---|---|---|
| 0 mm | 100–157,5 mm | 20 / 37,5 mm |
| 10 mm | 110–147,5 mm | 10 / 27,5 mm |
| 20 mm | 120–137,5 mm | 0 / 17,5 mm |
| 30 mm | Vazio: 130 > 127,5 mm | −10 / 7,5 mm |

Isso não atribui uma espessura à mão nem prova ergonomia. Mostra que não há reserva para presumir mãos salientes dos dois lados. O máximo simétrico puramente matemático é 28,75 mm por lado, com contato nos limites; não é espaço de pega recomendado. O desenho de manuseio deve indicar onde apoiar e segurar o quadro, mantendo as mãos fora desses encontros e sem usar hidráulica/pedra como apoio presumido.

### Ferramenta e folga sob a pedra

O eixo dos M6 esquerdos está 11 mm da parede. Um envelope circular coaxial de ferramenta com diâmetro d deixa `11 − d/2` mm: Ø12 deixa 5; Ø16 deixa 3; Ø20 deixa 1; Ø22 tangencia; Ø24 invade 1. São sensibilidades do envelope: a chave real, seu comprimento, ângulo de aproximação e operação permanecem por escolher. Não deduzir acesso da mão a partir do cilindro Ø11 usado no estudo antigo. Tampas de acabamento devem sair sem impedir esse acesso.

O topo do quadro está Z743 e a face inferior da pedra Z745: **somente 2 mm nominais**. Não contar com levantar o quadro para compensar folgas laterais. Erros de posição/espessura, selante e deformação consomem essa reserva. Manter a junta desmontável e verificar apoio temporário e sequência antes de soltar os M6; capacidade da união e massa acabada não foram comprovadas.

### Acesso hidráulico sem perder armazenamento

Aberturas cotidianas esquerda/direita de 270/235 mm e a retirada integral do quadro têm funções diferentes. O cenário antigo de sifão/recorte Ø100 permanece hipótese, não produto instalado ou mapa para furar. Antes de localizar registros/conexões, sobrepor seus envelopes e as ferramentas necessárias à abertura efetiva; se a união precisar do vão integral, registrar expressamente a remoção do quadro como etapa anterior. Não acrescentar uma divisória/faixa fixa para resolver um acesso ainda sem geometria.

Reproduzir: `python -B ferramentas/estudos/conferir_acesso_banheiro.py`. Hash R52 conferido; geometria lida da base persistida, sem abrir CAD e sem ensaio físico. As faixas foram conferidas por substituição direta nas desigualdades; não representam percurso novo aprovado.
