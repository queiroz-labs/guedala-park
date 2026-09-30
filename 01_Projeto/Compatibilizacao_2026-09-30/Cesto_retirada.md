# Cesto: frente, ferragem e retirada do saco

30/09/2026 · [Prancha interativa](Cesto_retirada.html) · [Contas reproduzíveis](calcular_cesto.cjs) · [Resultados](Resultados_cesto.json).

## Resultado e direção adotada para desenvolvimento

**Manter o cesto 45 × 25 × 45 cm, abertura de 55°, saco removível/lavável com alças e acabamento liso Arenza.** Desenvolver a frente em duas partes: inferior basculante e superior fixa no uso, mas removível para manutenção. Essa divisão e as cotas abaixo são propostas técnicas do assistente, não novos aceites expressos de Elias. Nenhuma redução no tanque ou no cesto foi aplicada.

O novo corte inclui a frente decorativa, omitida do envelope móvel anterior. No mesmo plano frontal proposto de 63 cm, uma frente alta até 89,7 cm do piso alcança 123,66 cm da parede quando abre. A frente dividida alcança **105,15 cm**, economizando **18,51 cm de projeção**. Na seção documental de 154 cm, sobram 48,85 cm após a frente aberta; são apenas uma diferença de cotas, não passagem livre ou espaço de pessoa comprovados.

Foi encontrado um percurso geométrico de extração para um corpo carregado de teste de **40 L × 20 P × 40 A cm**. Esse envelope não é molde do saco, capacidade garantida ou novo tamanho do cesto. A saída exige avanço para fora; não equivale a simplesmente puxar verticalmente sob o tanque.

## Base preservada e conflitos descobertos

Fontes locais: [R04](../Lavanderia/Cesto_basculante_calculo_R04.md), [tanque R05](../Lavanderia/Tanque_dimensionamento_R05.md), [R08 hidráulica](../Lavanderia/Tanque_cesto_compatibilizacao_R08.md) e [tolerâncias de 28/09](../Compatibilizacao_2026-09-28/README.md#3-cesto-acrescentar-tolerância-de-acesso-ao-teste-de-colisão). Não houve nova pesquisa comercial; não há ferragem escolhida.

Coordenadas: y desde a parede para a frente; z desde o piso. Eixo mantido em (56;12), curso 0–55°. Tampo até y=75, topo z=92 e espessura de teste 2. Gabinete com 59 cm de largura externa e 55,4 internos. O tanque externo de teste ocupa y=21–60, com fundo a z=70; são a posição ilustrativa da R08 e paredes hipotéticas, não medidas de fabricação.

**Incompatibilidade do gabinete ilustrativo:** sua frente a 58 cm ficaria atrás do limite frontal do tanque, em y=60. Uma faixa superior lisa no plano 58 atravessaria o envelope do tanque. Por isso este estudo leva a face frontal da lavanderia a **63 cm**, preservando tampo de 75 e posição do tanque. A face interna do painel de 18 mm fica em 61,2: **1,2 cm entre painel e tanque**. Não é espaço comprovado para apoio estrutural ou manutenção. A mudança afeta frente e fechamento lateral local; não acrescenta profundidade ao cesto, não muda o eixo, não leva a base ou rodapé para 63 e não altera automaticamente a cozinha.

Isso evita recuar o tanque só para esconder a incompatibilidade. A continuidade visual Arenza é preservada, mas o encontro da lateral, perfil da pega e junta horizontal precisam entrar no desenho de marcenaria.

## Corte proposto para marcenaria

| Elemento | Cota de desenvolvimento | Motivo / limite |
|---|---|---|
| Face externa da frente | y=63 | Cobrir o tanque de teste sem recuá-lo; tampo mantém 12 cm de avanço |
| Espessura de frente | 1,8 cm, hipótese | Face interna em y=61,2 |
| Frente inferior móvel | z=15–67,1, altura 52,1 cm | Reduz projeção e mantém painel contínuo fechado |
| Painel superior removível | z=67,5–89,7, altura 22,2 cm | Fixo durante uso; sai para acesso técnico |
| Junta horizontal | 4 mm | Hipótese entre as duas partes; ferragem/pega podem exigir revisão |
| Junta sob pedra | 3 mm | Hipótese, não folga de montagem validada |
| Rodapé e base | não avançar além de y=58 | Mantém o giro da borda inferior livre |
| Rodapé de ensaio | topo 11; face até y=58 | Recuado 5 cm da frente; não é painel colado à face móvel |
| Base interna | topo 9,8 | Referência herdada; suporte do pivô não dimensionado |
| Ligação frente–armação | face interna 5,2 cm adiante do plano u=0 | Braços/distanciadores reais precisam ser desenhados |

O cesto atinge z=63,478 durante a abertura. Painel superior começando em 67,5 preserva **4,022 cm de separação vertical global**: os 3 cm herdados mais 1,022 cm para variação de montagem neste ensaio. Essa reserva adicional de 1 cm é critério proposto, não tolerância comprovada da ferragem. Deslocamentos combinados do eixo, aro e painel precisam permanecer dentro dela. Travessas e ferragens que desçam dessa linha invalidam o cálculo. O aro superior não pode receber alças salientes fora do envelope de 45 cm durante o giro.

A frente inferior desce até **7,99 cm do piso** a 55°. Seu ponto mais recuado permanece em y≥61,2: separação horizontal de pelo menos 3,2 cm da base/rodapé até y=58. Por isso é necessário manter o rodapé recuado. Uma base prolongada até a nova face não está autorizada por este corte.

Foram comparadas 5.501 posições, com polígonos completos (SAT), contra pedra, tanque, dois volumes hidráulicos, base, painel superior e rodapé. Nenhuma interseção nessas posições. O rodapé foi modelado como painel entre y=56,2 e 58, com topo a 11, abaixo do ponto mínimo do cesto (12). Não elevar seu topo para fechar visualmente a faixa inferior sem conferir o giro. A faixa recuada entre rodapé e frente pode acomodar a ventilação discreta escolhida; tela e apoios ainda a detalhar. Peças reais, piso desnivelado, parafusos, retenções e tolerâncias não estão modelados.

## Retirada diária: percurso em duas etapas

Ensaio com aro consumindo 1,5 cm por borda: boca de 42 × 22 cm dentro do envelope externo 45 × 25. Corpo carregado de 40 × 20 deixa 1 cm por lado; altura de teste 40, começando 2,5 cm acima da base e terminando 2,5 cm abaixo da borda. As alças devem ficar recolhidas dentro do envelope durante o giro e ser liberadas ao retirar. Espessura do tecido, costuras, engates, volume irregular e dilatação com roupa não foram medidos.

1. Abrir completamente e manter o conjunto retido. Soltar o saco e **retirá-lo na direção inclinada do cesto**, sem tentar trazê-lo imediatamente para a vertical. No modelo, deslocamento de 44,5 cm ao longo dessa direção: 36,45 cm para a frente e 25,52 cm para cima. A base do saco passa 2 cm além do plano da boca.
2. Com o saco fora do aro, endireitá-lo movendo sua parte inferior dianteira para cima/para fora. A animação usa a quina inferior traseira como referência geométrica, em y=81,59/z=57,39 — não uma articulação física nem exigência de pegada. Nessa rotação, o corpo fica inteiramente além da pedra e não retorna ao volume do cesto. Termina em y=81,59–101,59 e z=57,39–97,39.

**Envelope máximo durante a retirada: y=125,83 cm**, restando **28,17 cm** até o limite de seção de 154 cm. O corpo cabe no corte ideal, mas esse saldo não acomoda automaticamente uma pessoa à frente dele. A pessoa provavelmente precisará operar parcialmente de lado; essa postura depende da planta, máquina, lixeira, porta e alcance, ainda não verificados nesta revisão. Não mover esses itens para declarar conforto.

As duas etapas têm uma justificativa além da amostragem: durante a extração, o saco mantém suas coordenadas transversais dentro do aro. Tudo que atravessa a boca segue para fora da projeção da pedra. Na rotação posterior, as coordenadas axiais de todos os pontos permanecem a pelo menos 47 cm, enquanto o aro está em 45; a quina traseira fica 6,59 cm além da pedra. Assim o corpo não volta a atravessar o aro. A conferência de 1.442 posições também incluiu frente móvel, painel superior e volumes fixos; alças/mãos e deformação real não foram incluídas.

Puxar verticalmente mantendo o saco inclinado desloca-o para trás no sistema do cesto. Com apenas 1 cm de reserva na boca, a translação vertical esgota essa reserva em cerca de **1,22 cm** (1/sen55°). O saco flexível pode mudar de forma, mas não se deve depender de compressão da roupa para justificar um percurso que não fecha no envelope carregado.

### Gabarito para escolher o aro e confeccionar o saco

| Consumo de aro em cada borda | Boca interna L × P | Corpo máximo de teste com 1 cm/lado |
|---|---|---|
| 1,0 cm | 43 × 23 | 41 × 21 |
| 1,5 cm | 42 × 22 | 40 × 20 |
| 2,0 cm | 41 × 21 | 39 × 19 |

Dimensões são envelopes externos carregados. Ferragem interna e engates devem ser descontados da boca, não da folga de 1 cm depois de escolhida a bolsa. Preservar saco lavável e alças; não selecionar tecido nem costurar antes de medir o aro real. O volume externo anterior de 50,625 litros continua sem representar capacidade útil de roupa.

## Ferragem: requisitos que agora podem ser comparados

A largura interna nominal de 55,4 e armação de 45 deixam 5,2 cm por lado para ferragens/folgas. Não usar essa faixa simultaneamente para a mangueira/contrapeso Telca. O pivô real precisa reproduzir o eixo estudado; um mecanismo de múltiplos elos deve fornecer sua própria trajetória.

Especificar retenção em 55° durante retirada do saco, limite positivo de curso e proteção contra fechamento/abertura descontrolados conforme a carga. Amortecimento do cesto não foi aprovado automaticamente com as corrediças da cozinha; comparar função e esforço real, sem escolher pistão pela massa em kg apenas.

Para mostrar por que isso importa, calculou-se o momento gravitacional no pivô com centro de massa do cesto uniformemente distribuído no envelope e frente homogênea. Casos abaixo são sensibilidades; não são peso de roupa autorizado, dimensionamento de fixação ou capacidade nominal exigida sem fator de projeto.

| Cesto + conteúdo / frente | Momento fechado | Momento aberto a 55° | Muda de sentido em |
|---|---:|---:|---:|
| 5 / 3 kg | −4,34 N·m | +13,56 N·m | 12,48° |
| 8 / 3 kg | −8,01 N·m | +16,87 N·m | 17,00° |
| 12 / 5 kg | −11,72 N·m | +26,64 N·m | 16,05° |

Sinal positivo favorece abrir; negativo favorece fechar. Tirar o saco altera esse equilíbrio enquanto a frente permanece. A ferragem deve manter o conjunto controlado cheio e vazio; roupa concentrada na borda, esforços de mão e impactos não estão nesses números. Suportes distanciados 5,2 cm, pivôs, fixações laterais e limite de abertura precisam ser dimensionados como um conjunto.

## Manutenção e ensaio de aceitação preparado

A remoção diária do saco não satisfaz sozinha o requisito aprovado para o sifão. Desenvolver frente inferior desacoplável da armação, painel superior removível e retirada da armação com acessos às retenções pelo lado frontal. Suportes do tanque e laterais estruturais permanecem fixos; nenhuma travessa estrutural deve depender do painel removível.

Sequência funcional para demonstrar em protótipo, conforme mecanismo selecionado: saco fora; conjunto sustentado; frente e retenções liberadas por pontos acessíveis; armação retirada; painel superior retirado quando bloquear o serviço. Mostrar acesso à válvula, uniões e sifão, curso para desmontar conexões, recolocação e ajuste. Não é instrução de desmontagem de uma instalação existente.

**Ficha de conferência para marcenaria:** reproduzir eixo/curso; substituir aro e frente pelos perfis reais; acrescentar pega, braços, trava e saco cheio. Testar giro fechado–aberto, parada, retirada com alças, espaço da pessoa, carga cheia/vazia e desmontagem frontal. Retornar desenho que inclua os apoios do tanque e o percurso completo da Telca sem utilizar a faixa lateral duas vezes. Consulta preparada, não enviada.

## Continuidade

Geometria da frente e um percurso do saco avançaram mantendo as escolhas funcionais. Falta confirmar ferragem e ergonomia na planta/protótipo; não há liberação de fabricação. Próxima verificação independente: espaço de operação na lavanderia com máquina, lixeira, porta e banquinho, usando esta projeção completa do cesto e da retirada — os 61,1 cm da R04 consideravam só o recipiente aberto.
