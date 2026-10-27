# Cesto P14 — reações dos pivôs, fixações e operação

**Agenda 27/10, preparada em 26/10:** [kit de oficina](../../P20/Assento_fechado/Roteiro_banco_cesto.md) com desenho, corte axial a completar e formulário vazio. Compra definitiva/montagem dependem de produto, suporte/terminais e ligações; sem novo cálculo ou ensaio.

**T04 — margens de engate, 26/10:** [sensibilidade conjunta](../../Banco_e_cesto/Cesto_simples/Conferencia/Resultado.md#margens-geométricas-de-engate--t04-26102026): 36 casos, 12 inversões conferidas. Engate hipotético de 290 mm com erro radial de 1 mm por terminal não é garantido até a parada existente; 291 mm não deixa reserva para variação. Dados reais da trava continuam pendentes. Não deslocar pontos ou ampliar abertura para absorver o erro; verificar produto e implantação antes dos furos.


**Pesquisa pública, 26/10:** [bucha candidata e ajustes](../../Banco_e_cesto/Cesto_simples/Conferencia/Resultado.md): GFM-1012-15 identificada no catálogo igus; alojamento, ajuste com OMPCR e ligação à madeira ainda pendentes. Oito requisitos rastreados; consulta preparada, não enviada. Nenhuma alteração do conjunto nominal ou da R52.

25/10/2026 · continuação do plano. **Concluída a estática nominal em três dimensões na parada 55° e a energia gravitacional durante a abertura.** O torque de 38,73 Nm e a tração de 133,29 N anteriores foram reproduzidos; o avanço é calcular os pivôs e as interfaces sem presumir divisão igual entre os lados. Nenhuma peça ou movimento da R51 foi alterado.

![Esquema do equilíbrio e retenção](Reacoes_parada_55.png)

## Montagem nominal e acesso — 26/10/2026

Geometria das peças conferida contra a base salva da **R52**, sem abrir ou alterar o CAD. [Detalhamento](Montagem_nominal.json) preserva quatro casos completos do cálculo anterior; não soma máximos de cenários diferentes. [Conferência](Verificacao_montagem.json) verifica a extração e cinco sensibilidades de engate. [Registro para oficina](Registro_montagem.csv): oito linhas vazias, todas NAO_EXECUTADO.

| Controle | Caso de origem (índice começando em 1) | Solicitação nominal |
|---|---:|---:|
| Resultante no pivô | 216 | 134,012 N |
| Retenção vertical reversa | 72 | 28,014 N |
| Tração em um articulador | 208 | 133,288 N |
| Momento resultante na interface do pivô | 216 | 6,969 Nm |

**Pivô candidato OMPCR1020:** desenho arquivado [Omega](../../Banco_e_cesto/Cesto_simples/Conferencia/Fontes/Omega_7379.pdf): ombro Ø10×20, rosca M8×1,25 de 13,25 mm e cabeça Ø16×7 com Allen SW5, encaixe 4,3 mm. Soma axial 40,25 mm; sobra geométrica 11,75 mm na faixa 52 mm. Essa sobra não demonstra acesso ou montagem: o empilhamento girante de bucha/arruelas/folga deve ser compatibilizado com o **ombro útil 20 mm**, separadamente do engajamento da rosca e do alívio de raiz. Não usar a rosca como superfície de giro nem apertar a parte móvel entre faces sem folga definida. Bucha, material, retenção e apoio continuam sem produto selecionado.

**Sequência a demonstrar antes de furar peças definitivas:**

1. Desenhar o corte axial do pivô completo, identificando parte fixa e girante, espessuras, folga axial, engajamento de rosca e retenção. Os blocos do CAD continuam reservas.
2. Definir a orientação da cabeça e registrar o corredor para inserir, girar e retirar a Allen SW5. Medir a ferramenta real; os 4,3 mm do encaixe não são o espaço de manobra da chave. Se o acesso exigir montar fora do corpo, demonstrar retirada e reinstalação do subconjunto.
3. Fechar a ligação do suporte às laterais/base para forças horizontais, compressão e levantamento; conferir os vetores simultâneos dos casos acima. Não contar somente com apoio por gravidade nem distribuir força igualmente entre parafusos sem modelo da ligação.
4. Montar terminais completos na armação e operar com gabarito do saco 400×200×400. Registrar cabeças, projeções, acesso ao destravamento e retirada do saco/armação. Preservar a passagem e o acesso hidráulico.
5. Medir distância entre terminais no engate e na liberação; comparar com a montagem candidata antes de definir os furos. Só depois fechar o plano de ensaio com produtos e critérios efetivos.

**Sensibilidade de engate:** distâncias hipotéticas 280/285/288/290/291 mm correspondem a 52,841/53,820/54,409/54,803/55,000°. O comprimento 291 mm esgota a extensão ideal de duas barras 145,5 mm; não comprova curso adicional de liberação nem capacidade da trava. São cálculos geométricos, sem medição de ferragem real.

Reproduzir com `python -B ferramentas/aereos/detalhar_cesto_montagem.py` e `python -B ferramentas/aereos/conferir_cesto_montagem.py` na raiz. O gerador se recusa a sobrescrever registros que já contenham medições.

## Base preservada e limites

Mantidos frente 550×521×18, saco 400×200×400,13 peças da armação, eixo ideal Y6440/Z120 e abertura 55°. Os centros de gravidade agora vêm dos sólidos BREP atuais. Os volumes conferem com o [estudo anterior da armação](../../Inventario_dimensional/Portas_e_articulacoes/Cesto_selecao_e_esforcos.md): frente 5,157900 L e armação 2,769192 L.

A ρ900 hipotético, frente+armação somam 7,134 kg; com 8 kg de roupa, 15,134 kg antes de saco, pega e ferragens adicionais. Densidades 650/800/900 são sensibilidades, sem material real confirmado. O corpo do saco é envelope, não 32 kg de madeira nem peso real do tecido.

Reutilizada a [posição candidata dos articuladores simples](../../Banco_e_cesto/Cesto_simples/Conferencia/Resultado.md). A distância 291 mm ao abrir vem de duas barras 145,5; **não é curso de trava confirmado pelo Bigfer**. Nesta condição idealizada, a força da biela alinhada atua no plano YZ com componentes unitárias aproximadamente+0,893Y/+0,449Z e braço 290,54 mm. Terminais e sua flexão/excentricidade continuam ausentes. Não aplicar essa força axial ao articulador dobrado durante todo o percurso.

Os planos de reação dos pivôs são hipóteses a partir dos pinos ideais: X4320/4790, com sensibilidades 4310/4800 e 4330/4780. São espaçamentos 470/490/450 mm, respectivamente, sem afirmar que a bucha e o suporte comerciais apoiem nesses planos. Os articuladores foram avaliados com 100% num lado, 50/50 e 100% no outro. Não se usa repartição ideal como única condição.

A armação foi tratada como corpo rígido para fechar o equilíbrio. A torção, a deformação e a rigidez das ligações que permitiriam transmitir esses esforços entre os lados ainda precisam de verificação própria.

## Cargas na parada 55°

| Cenário a ρ900 | Peso conhecido | Momento de abertura | Tração total requerida dos articuladores |
|---|---:|---:|---:|
| Vazio, frente+armação | 69,96 N | 12,538 Nm | 43,153 N |
| Roupa 8 kg no centro | 148,42 N | 21,372 Nm | 73,561 N |
| Roupa 8 kg no extremo teórico de maior momento | 148,42 N | 38,725 Nm | 133,288 N |

“Extremo teórico” coloca o centro de massa nos limites do envelope do saco. É uma sensibilidade conservada dos cálculos anteriores, não demonstração de que 8 kg de roupa consigam se concentrar fisicamente num canto. A posição lateral do conteúdo é variada separadamente porque altera os pivôs mesmo sem mudar o torque de abertura.

Na combinação simétrica central, os pivôs recebem aproximadamente **Y−32,86/Z+57,69 N por lado**, resultante 66,39 N. Isso já difere de simplesmente dividir o peso total por dois: os articuladores exercem forças horizontais e verticais.

Nos 270 cenários calculados, a maior resultante num pivô é **134,01 N**, com um articulador recebendo tudo e roupa excêntrica. Não representa capacidade do parafuso Ø10, da bucha ou da madeira. O cenário extremo de um pivô não precisa coincidir com o de maior arrancamento ou maior tração.

**Aparece retenção vertical obrigatória:** numa sensibilidade a ρ650, com roupa deslocada 200 mm para um lado e somente o articulador oposto atuando, um pivô precisa aplicar **28,01 N para baixo no conjunto móvel**. O conjunto, portanto, puxa o suporte fixo para cima. Um apoio apoiado apenas por gravidade na base não fecha esse caminho. Parafusos/juntas e retenção mecânica precisam transmitir o sinal reverso, além de forças horizontais e do controle axial do pivô.

## Interfaces à lateral de madeira

As faces internas das laterais atuais estão em X4278 e 4832. O centro da reserva de cada articulador fica 26 mm para dentro dessas faces. Se o grupo resistente da lateral estiver alinhado em Y/Z, essa excentricidade X gera momento resultante de até **3,466 Nm** na interface do articulador, além da força 133,288 N. O terminal real pode acrescentar outras excentricidades; não se projetou um suporte comercial fictício para absorvê-las.

Nos pivôs, os planos testados ficam 32/42/52 mm para dentro das mesmas faces. A maior combinação desta sensibilidade dá aproximadamente **6,969 Nm** na interface à lateral. Os blocos 52×40×44 do CAD são reservas, sem material, bucha ou ligação dimensionados. Não considerar seu volume desenhado uma ligação pronta. A base pode receber compressão vertical quando houver contato, mas não elimina a retenção contra levantamento nem a força horizontal.

Os vetores de reação e momentos em Y/Z de cada lado estão em [Resultados.json](Resultados.json). São solicitações estáticas não majoradas da montagem hipotética. Não dividir por uma quantidade arbitrária de parafusos, não comparar com “20 kg” de anúncio e não usar como resistência admissível. Componentes do pivô/articulação têm função própria; nenhuma estrutura tubular sustentando chapas foi proposta.

## Operação entre 0 e 55°

Foi calculado o potencial gravitacional do conjunto conhecido, sem mola, atrito ou amortecimento. Em cada trajetória, a roupa é uma massa ideal com centro fixo em relação à armação; não se simulou acomodação/migração do tecido. O ângulo de torque zero é um equilíbrio **instável**: acima dele a gravidade favorece abrir; abaixo favorece fechar. Não é uma posição de retenção segura.

| Cenário a ρ900 | Ângulo de torque zero | Energia gravitacional disponível desse ponto até 55° | Maior força tangencial ideal no topo |
|---|---:|---:|---:|
| Vazio | 0,70° | 6,430 J | 22,62 N |
| Roupa 8 kg central | 16,81° | 7,399 J | 38,55 N |
| Extremo teórico de maior momento | 2,52° | 19,087 J | 69,86 N |

A pega é somente o ponto teórico central alto da frente, raio 554,37 mm; pega real, direção da mão e acesso alteram a operação. Os valores não provam conforto ou alcance. A energia é a diferença de potencial com início praticamente sem velocidade; mãos, atrito, componentes ausentes, acomodação da roupa e velocidade inicial mudam a energia efetiva. Os 19,087 J são um resultado dos casos idealizados, não limite garantido de impacto do conjunto completo. Não foi convertido 19 J numa força de impacto sem conhecer curso de parada e rigidez/amortecimento.

Uma trava que segura a posição aberta não comprova controle da descida até ela. Isso precisa entrar no protótipo e na consulta do fabricante, preservando a direção manual já aprovada. Nenhum novo mecanismo ou redução do saco foi adotado.

## Dados exatos ainda faltantes

1. **Bigfer:** confirmar os eixos entre terminais ao travar/liberar, capacidade e sentido de esforço na montagem 55°, retenção contra fechamento e comportamento durante o percurso. Perguntar se há orientação de energia/velocidade de chegada; não supor que a trava absorva impacto.
2. **Pivô completo/oficina:** fornecer planos reais de reação das buchas, posição dos apoios, retenção axial, folgas e espessuras. Demonstrar caminho da força horizontal e da força vertical reversa até as laterais/base, incluindo as excentricidades. O OMPCR candidato 40,25 mm sozinho não resolve a largura 52 mm.
3. **Ligação móvel:** distribuir os esforços dos terminais nos montantes gabarito 15 mm sem reduzir saco, passagem ou manutenção. Corpo, conexões e proteção contra corrosão precisam de material e desenho reais.
4. **Massas adicionais:** pesar saco/alças, pega e partes móveis; informar seus centros ou trajetórias. [Registro pendente](Componentes_pendentes.json) deixa desconhecidos como `null`. Não preencher zero nem girar as barras articuladas como se fossem rígidas com a frente. Preencher esse registro não atualiza automaticamente o cálculo: o modelo deve incorporar a cinemática/massa correta.
5. **Ensaio:** complementar C01–C04 do [roteiro P20/P14](../../P20/Assento_fechado/Roteiro_banco_cesto.md) com apoio assimétrico, retenção vertical dos suportes, operação e chegada ao fim do curso. Sem executar prova física nem usar pessoa como carga nesta etapa.

São dependências de produto/oficina, não das medidas do apartamento. A instalação final e o piso real serão conferidos no levantamento. A R51 completa e seus controles permanecem intactos; estudo de cálculo separado, sem capacidade de uso liberada.

## Reprodução e verificação

[Geometria BREP](Geometria_R51.json) · [cálculo](calcular.py) · [resultados](Resultados.json) · [verificador](verificar.py) · [verificação salva](Verificacao.json).

Executar `extrair.py` no FreeCAD com a R51 aberta e o cesto em 0°/sem retirada, sem mover controles. Depois `python calcular.py`, `python verificar.py` e `python desenhar.py`. Verificados 270 equilíbrios, 270 espelhamentos e 30 trajetórias/trabalho-energia; torque/braço anteriores reproduzidos, hash/CRC da fonte preservados. Zero ensaios físicos; fabricante ainda não validou trava ou capacidade. Ao mudar componentes, apoios ou cotas, repetir o modelo com os dados efetivos.
