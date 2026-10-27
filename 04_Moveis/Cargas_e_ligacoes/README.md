# Cargas e ligações prioritárias da marcenaria

25/10/2026 · base geométrica R50. Primeiro ciclo executado do plano até 31/10, concentrado em P15, P04, P01 e P20, com a decisão P11 sem tubos preservada.

**Decisão posterior vigente de25/10:** Elias não quer tubos sustentando chapas de madeira e exige autorização prévia para qualquer proposta futura com essa função. A alternativa tubular P15 abaixo foi **cancelada**. A continuação está em [soluções de marcenaria sem tubos](../Ligacoes_sem_tubos/README.md). A R51 retirou o estudo tubular oculto da bancada; os cálculos desta primeira rodada continuam documentados sobre a geometria R50 preservada.

Os valores abaixo são **resultados de modelos nominais**, com materiais e juntas condicionais. Não constituem carga de uso liberada ou autorização de fabricação. Medidas finais e ancoragens no apartamento continuam separadas do trabalho que pode avançar agora.

## Controle vigente

**Agenda27/10, preparada em26/10:** [matriz](Andamento_20_moveis.md) aponta kit P20/P14 (desenho, lista e12 registros vazios) e F13=A (Elias27/10/2026: Arenza liso); P02 U1–U4=A (Elias,27/10/2026), requisito10kg não demonstrado. Montagem definitiva continua em produto/oficina; zero ensaios e nenhuma nova varredura.

[Matriz20/20](Andamento_20_moveis.md) consolidada em26/10: controle25/10 e T01 documentais concluídos; T02/T03 parciais. LoteB atualizado; P04 preparado para laboratório, sem ensaios. Regerar: `python -B ferramentas/estudos/consolidar_matriz.py`. Estudos históricos abaixo preservados.

## Entregas desta rodada

| Frente | Resultado concreto | Próxima condição a resolver |
|---|---|---|
| Inventário | 975 geometrias inventariadas em 20 módulos; 146 contatos da fila anterior conferidos, distribuídos em 15 módulos; 26 conferências direcionadas adicionais | Completar o mapa resistente e a furação por união; os 26 incluem repetições da amostra e não devem ser somados como novos encontros únicos |
| P11 | Decisão sem tubos e memória de 10 kg distribuídos mantidas | Juntas, material, suspensão e prova de oficina conforme memória própria |
| P15 lavanderia | Chapa isolada e apoio traseiro ideal calculados; comparação tubular cancelada | Continuar base composta e ligações no estudo sem tubos |
| P04 cabeceira | Vãos livres e entre apoios reconciliados; cenários de 5/10/20 kg e caminho das divisórias separados | Resolver transferência de tração das uniões e ligação positiva ao fundo |
| P01 roupeiro | Varões tubulares calculados; balanços identificados; duas prateleiras de 723 mm desenhadas e apoios conferidos no FreeCAD | Comprovar conectores e deformação do conjunto; compatibilizar suporte central dos varões |
| P20 banco | Duas tampas calculadas separadamente; forças para seleção dos articuladores; nove contatos com o corpo conferidos | Completar massa móvel e geometria dos terminais; verificar assento fechado e protótipo |

O diagrama anterior `Mapa_apoios_e_cargas.png` fica apenas como histórico: sua alternativa tubular P15 está cancelada. O apoio direto P01 continua em desenvolvimento.

## Geometria e premissas

Fonte: `Otimizacao_FreeCAD_R50_2026-10-24/Guedala_Park_R50_Completo_Otimizado.FCStd`, SHA256 `1eda9a56e7346f5e08d5b4a391a57b4407132f14a142efdef1e2e5699c4dfd69`. A extração usa parâmetros e BREP no FreeCAD. O arquivo principal não foi alterado.

| Entrada | Valor utilizado | Situação |
|---|---|---|
| MDF nominal de 18 mm | E imediato 2.200 MPa; espessura resistente 17,7 mm; espessura para massa 18,3 mm; densidade 800 kg/m³ | Referência condicional; confirmar substrato e composição da chapa selecionada. Revestimento não é automaticamente espessura resistente |
| Sensibilidade a material mais flexível | E imediato 1.600 MPa | Hipótese adicional, sem atribuição a fabricante |
| Deformação diferida | E dividido por dois; nas placas com juntas, K também dividido por dois | Sensibilidade; sem prazo ou previsão de fluência do produto |
| Juntas das propostas P01 | K vertical inicial requerido 1.000 N/mm por ligação; 500 N/mm no cenário diferido | Requisito, não resistência/rigidez publicada do Minifix ou Confirmat |
| Placas | Isotropia, ν = 0,30; sem crédito de engastamento das juntas | Hipótese do cálculo |
| Critério comparativo | L/300 e reserva adicional de 0,20 mm | Escolha de projeto. Não é norma de aprovação do móvel; não verifica ruptura ou segurança das fixações |
| Aço dos tubos | E = 200.000 MPa; densidade 7.850 kg/m³ | Hipóteses; geometria efetiva, tolerâncias e resistência do produto ainda necessárias |

O [documento técnico Greenplac, página 4](https://download.greenplac.com.br/download/qualidade-requisitos-normativos-e-cuidados.pdf) informa E mínimo de 2.200 MPa para espessuras acima de 12 até 19 mm e tolerância nominal de ±0,3 mm. Isso fornece uma referência para o painel, sem substituir a identificação do substrato efetivamente comprado. A [ficha Arauco](https://arauco.com.br/wp-content/uploads/2024/07/ARAUCO-MELAMINA-FICHA-TECNICA.pdf) também foi consultada como referência condicional de painel revestido.

Os cenários incluem peso próprio. Cargas em kg são **conteúdo adicional**, exceto quando a linha identifica a massa da própria peça. As vigas ativam toda a profundidade da chapa; um peso pontual longitudinal nessa conta não representa automaticamente uma pequena carga na borda frontal.

## Lavanderia P15

Base `Peca362`: 799 × 312 × 18 mm. Peso próprio de cálculo: **3,650 kg**. Fundo `Peca361`: 799 × 18 × 544 mm. A base termina na frente do fundo e este começa na cota da face superior da base: há encontro pela **aresta**, sem face de apoio. O mesmo ocorre no tampo. Não cabe copiar o parafuso traseiro horizontal do P11 como se a geometria fosse igual.

| Hipótese para 20 kg distribuídos | Flecha imediata | Sensibilidade diferida | Diferida com reserva | Referência |
|---|---:|---:|---:|---:|
| Base apoiada apenas nas laterais | 4,856 mm | 9,713 mm | 9,913 mm | 2,663 mm |
| Laterais e traseira com apoio vertical contínuo ideal, frente livre | 1,723 mm | 3,447 mm | 3,647 mm | 2,663 mm |

Mesmo o segundo modelo, otimista quanto à imobilidade dos apoios e sem engastamento rotacional, ultrapassa a referência diferida. Não demonstra que toda solução sem aço seja impossível: demonstra que somente acrescentar apoio vertical traseiro, nessas hipóteses, não encerra o problema.

### Histórico cancelado de reforços externos

**Não faz parte do projeto ativo.** Elias rejeitou tubos sustentando chapas em 25/10. O inventário e os números do estudo cancelado estão em [Decisão sem tubos](Decisao_sem_tubos.md#histórico-cancelado-dos-reforços-externos-movido-do-readme-em-25102026) e em `Historico_tubos_P15_cancelado.json`.

## Cabeceira P04

Base `Peca269`: 1.764 × 212 × 18 mm. Os vãos livres relevantes são **851,5 / 407,75 / 425,75 mm**. Ao idealizar a divisória dupla de 36 mm pelo centro do grupo, os trechos principais entre eixos são **878,5 / 434,75 / 434,75 mm**. A pequena divisória junto à extremidade também foi preservada.

As divisórias estão **sobre** a base. Para sustentar a base para cima, precisam de união que transmita tração e de continuidade até tampo/fundo/suspensão. Seu mero contato não cria esse apoio. O fundo também encontra a base apenas pela aresta.

No trecho condicional de 878,5 mm com 5 kg distribuídos:

| Hipótese de apoio | Sensibilidade diferida com reserva | Referência |
|---|---:|---:|
| Somente as duas extremidades ideais do trecho | 6,407 mm | 2,928 mm |
| Extremidades e traseira com apoio vertical contínuo ideal | 1,204 mm | 2,928 mm |

Há potencial para resolver pelo conjunto base–fundo–divisórias, mas o apoio traseiro e as uniões ainda precisam existir fisicamente. A demanda de reação do primeiro modelo é **37,9 N por extremidade** para esse trecho. Os dois trechos menores, estudados com 2,5 kg cada, têm reação aproximada de **18,9 N por extremidade**. No encontro compartilhado, somar as parcelas dos dois lados e os pesos correspondentes; não dimensionar a junta como se recebesse um trecho só.

Os 5 + 2,5 + 2,5 kg são cenário nominal de estudo, não carga aprovada por compartimento. O resultado linear de 82,8 mm para 20 kg sobre os 1.764 mm sem transferência das divisórias já ultrapassa o campo de pequenas deformações: serve para rejeitar essa idealização, não como previsão da forma real do móvel.

## Roupeiro P01

### Prateleiras e varões do roupeiro P01

Seis sapateiras de 355 × 400 × 18 mm (0,820 mm na triagem biapoiada, contra 1,183 mm do limite), duas prateleiras de 705 × 550 mm (`Peca245`/`Peca246`) apoiadas em divisórias, e varões Ø20 × 0,7 mm. Triagem nominal: os conectores, as cargas locais e o caminho até o piso continuam pendentes. Detalhe completo: [prateleiras e varões](Detalhe_P01_prateleiras_e_varoes.md).

## Tampas e mecanismos do banco P20

**Continuação25/10:** [assento fechado e caminho até o piso](../P20/Assento_fechado/README.md). Reconciliados os18 contatos completos já conhecidos da R45; os nove desta primeira amostra não eram o inventário total. Cinco cenários de placa com convergência, sensibilidade de material, massa de27 volumes e roteiroP20/P14 preparados. Corpo/juntas, painel real e mecanismos continuam condicionados; não representa capacidade80/240kg liberada.

Eixo nominal da R50 em X102/Z420, ao longo de Y. Cada chapa tem profundidade de 448 mm e espessura de 20 mm. Centro de gravidade relativo ao eixo: **x = 224 mm, z = −10 mm**. Almofadas retiradas para abrir.

| Tampa | Massa só da chapa, densidade 650–800 kg/m³ | Momento máximo só da chapa |
|---|---:|---:|
| 971 × 448 × 20 mm | 5,655–6,960 kg | 12,435–15,304 N·m |
| 825 × 448 × 20 mm | 4,805–5,914 kg | 10,565–13,003 N·m |

O máximo ocorre aproximadamente a **2,56°**, devido ao centro 10 mm abaixo do eixo. Para ângulo θ de abertura:

```text
Mfechamento = m × 9,80665 × [224 cos(θ) + 10 sen(θ)] / 1000   [N·m]
Fmão tangencial ideal = M × 1000 / 448                       [N]
Farticulador = M × 1000 / alavanca perpendicular efetiva      [N]
```

A 90°, ainda há **0,683 / 0,580 N·m** de momento de fechamento para as chapas maiores/menores a 800 kg/m³. A força manual calculada é tangencial à trajetória; puxar verticalmente junto da posição de 90° não oferece a mesma alavanca.

Se apenas um articulador receber o momento máximo da chapa maior, suas forças seriam aproximadamente **765 / 383 / 255 N** para alavancas efetivas de 20 / 40 / 60 mm. Na menor: **650 / 325 / 217 N**. Essas alavancas são parâmetros; precisam ser obtidas das posições reais do mecanismo em cada ângulo. Não se dividiu a força automaticamente por dois.

A folha móvel da piano, parafusos, revestimentos e partes móveis dos articuladores ainda entram com massa e posição próprias. As curvas atuais são da chapa, não do conjunto móvel completo. Permanecem piano + articuladores com trava, duas tampas e retirada das almofadas. A carga de pessoas com o banco fechado segue tampa → apoios → corpo → piso; exige cálculo próprio.

Nos doze pares tampa–corpo selecionados, houve **nove contatos horizontais de face e três pares separados**. A primeira tampa alcança frente, fundo, lateral e três divisórias; a segunda alcança frente, fundo e a divisória na junta. Área de contato nominal não comprova distribuição de carga, nivelamento ou resistência do corpo.

## Interface da suspensão

Os esforços da caixa podem avançar antes de conhecer a parede. Para a parcela de caixa nominal e conteúdo uniforme, usando os centros de gravidade extraídos:

| Parcela calculada | Peso vertical | Momento em relação à face posterior |
|---|---:|---:|
| P15: caixa de 18,951 kg + 20 kg | 382,0 N | 55,85 N·m |
| P04: caixa/divisórias de 23,041 kg + 10 kg | 324,0 N | 32,21 N·m |

São **parcelas incompletas**: somar portas, ferragens, reforços e suas posições antes de dimensionar o conjunto. Como exemplo paramétrico, o momento do P15 com braço vertical de 400 mm gera tração total de 139,6 N; o P04 com 200 mm gera 161,0 N. A separação efetiva entre reação superior e encosto inferior precisa constar do detalhe. Não são esforços por bucha, não incluem majoração e não selecionam ancoragem. Um braço de 400 mm nem cabe na altura de 308 mm do P04.

## Arquivos e reprodução

- [Resultados completos JSON](Resultados.json): vigas, placas, varões, reforços, tampas e parcelas de suspensão, com entradas e unidades.
- [Matriz de ligações prioritárias](Matriz_ligacoes_prioritarias.csv): caminho da carga, solicitação, próxima ação e dependência.
- [Andamento dos 20 móveis](Andamento_20_moveis.csv), [18 posições nominais do estudo P01](P01_ligacoes_nominais_estudo_723.csv) e [perguntas técnicas preparadas](Dados_para_fornecedor_e_oficina.md).
- [Contatos conferidos](Contatos_reconciliados.csv), [geometria](Geometria_R50.json) e [26 conferências direcionadas BREP](Interfaces_adicionais_BREP.json). No P02, seis encontros de face foram confirmados onde a amostra anterior tinha zero; encontro entre os dois fundos é apenas aresta.
- [Estudo P01](P01_estudo_apoios_723.FCStd), [diferenças e quatro apoios](P01_estudo_diferencas.json) e [triagem dos volumes acrescentados](P01_colisoes_volume_acrescido.json).
- [Curvas e esforços das tampas](P20_momento_e_esforcos.csv), [varões](P01_varoes.csv), [prateleiras atuais](P01_prateleiras_apoios_reais.csv) e [triagem das chapas](Triagem_chapas.csv).
- [Verificação numérica](Verificacao_numerica.json) e [convergência das placas](Convergencia_placas.json).

Com Python e NumPy, executar nesta pasta: `python calcular.py --placas`. Usa as rotinas locais P11 preservadas e verifica o SHA256 da R50. Para reextrair a geometria no FreeCAD, executar `extrair_geometria.py`; para conferir os encontros direcionados, `conferir_interfaces_adicionais.py`. `estudo_p01.py` cria o estudo separado e recusa substituir um estudo já aberto.

**Dez verificações vigentes passaram:** vigas por fórmula independente, equilíbrio de forças/momentos, torque por derivada da energia, convergência Ritz, contato de compressão P01 e placa de controle comparada com série de Navier. A verificação da alternativa tubular foi retirada do conjunto ativo, preservada em `Verificacao_antes_decisao_sem_tubos.json`. A diferença entre Ritz e Navier foi aproximadamente 0,00031%. Convergência numérica verifica o método; não comprova as hipóteses físicas das juntas. Base de placas/energia: [MIT 2.080, Lecture 7](https://ocw.mit.edu/courses/2-080j-structural-mechanics-fall-2013/f8fd2ad49d100766335b4e129a8a4791_MIT2_080JF13_Lecture7.pdf).

## Continuação antes das medidas reais

1. P01: fechar deformação do fundo/caixa e comprovação das juntas; incorporar as duas chapas de 723 mm somente junto da atualização das fichas, conectores e comparação do modelo completo.
2. P15: seguir o estudo de marcenaria sem tubos; comprovar ação composta da base, juntas e mudança externa antes de incorporar à revisão completa.
3. P04: desenvolver a união de tração das divisórias e o apoio positivo no fundo; recalcular a caixa e sua suspensão com juntas finitas.
4. P01 varões e P20: obter cotas de montagem e componentes exatos, concluir os envelopes nominais e o roteiro de ensaio. Dados faltantes estão nas perguntas técnicas preparadas.
5. Completar os mapas dos outros móveis por prioridade e reconciliar os 52 Minifix já existentes, sem duplicar os conjuntos.

As etapas acima são trabalho de projeto/produto/oficina. Parede real, instalações ocultas, prumo/esquadro e vãos acabados ficam para o levantamento do apartamento. T01 documental foi consolidada em26/10; T02/T03 continuam parciais, com mapas nominais dos lotesA/B e condições físicas explícitas na matriz vigente.
