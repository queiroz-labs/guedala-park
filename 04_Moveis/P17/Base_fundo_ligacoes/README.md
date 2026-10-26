# P17 — base, fundo e ligações de marcenaria

## Caminho da caixa — 26/10/2026

[Desenho](../../Aereos_suspensao/P17_caminho_caixa.png) · [21 grupos de juntas](../../Aereos_suspensao/P17_mapa_juntas.csv) · [70 posições de fixadores](../../Aereos_suspensao/P17_eixos_fixadores.csv) · [30 cortes de carga](../../Aereos_suspensao/P17_cortes_carga.csv) · [memória](../../Aereos_suspensao/P17_caminho_caixa.json) · [conferência](../../Aereos_suspensao/P17_verificacao_caminho.json).

| Caminho nominal | Ligações candidatas e função |
|---|---|
| Base → laterais | 4 Minifix; pinos horizontais recebem cortante vertical e retenção transversal |
| Base → quatro divisórias → tampo | 8 Minifix inferiores + 8 superiores; retenção axial dos pinos verticais e contato conforme o sentido da reação |
| Tampo → laterais | 4 Minifix; referência superior precisa resistir e deformar de modo compatível com a caixa |
| Base/tampo → fundo inteiro | 12 + 12 Confirmat; transmissão de cortante para o fundo, que precisa distribuir até os cantos |
| Fundo → laterais/divisórias | 6 + 12 Confirmat; transmissão vertical, esforços fora do plano e distorção conjunta |
| Par de divisórias central | 4 parafusos 4×30; amarração candidata, sem considerar as chapas como uma peça de 36 mm |
| Cantos → suspensão | Bigfer candidata; rigidez das juntas, retenção e apoios inferiores ainda condicionados |

Total de estudo: **24 Minifix + 42 Confirmat + 4 parafusos face a face**, reconciliado com R00 e as 24 posições traseiras adicionais já propostas. Não são compras adicionais. Cavilhas continuam de posicionamento, sem crédito resistente ou nova furação.

Os 4×30 receberam centros candidatos em v120/240 e z150/400, pela face livre u964: 12 mm nominais na segunda chapa e 6 mm até a face oposta. Cabeça, piloto, torque e painel real pendentes. Confirmat laterais: z70/275/480; fundo–divisórias: z88/275/462. Eixos herdados do estudo parcial, agora referidos às faces de entrada/interface; os antigos marcadores do fundo em v9 não eram a interface v18.

**Acesso e montagem:** em bancada apoiada, montar base/divisórias, fechar tampo em z, aproximar cada lateral em u e instalar o fundo pela traseira. Apertar juntas antes das portas; acesso pelos lados livres do par central. Parafusos traseiros/laterais precisam ser acessíveis na bancada; cabeça lateral e embutimento traseiro exigem detalhamento. As 70 posições e 2.415 pares de envelopes conferidos não apresentaram interseção nominal; corredores externos de referência Ø20×100 e canecos foram conferidos contra madeira, calços fixos e suspensores. Cabeças, pinos completos, mandril, mãos e tolerâncias reais não foram validados.

**Carga que atravessa as juntas:** no cenário de massa ρ900, conteúdo20 kg, a fronteira da base recebe V295,10 N; incluindo quatro divisórias, V398,71 N. Com conteúdo frontal, momentos em torno da origem traseira de 77,04 e 95,07 Nm. São demandas do conjunto de juntas de cada corte, sem partilha por fixador; estão contidas no equilíbrio global e não devem ser somadas a ele.

As 24 posições do antigo modelo de placa coincidem com o mapa atual após converter **v=330−y**. Isso corrige a aparente diferença de coordenadas, mas não atribui K500/250 ao Minifix nem comprova a reserva superior0,20 mm. Grupos de pontos colineares não resistem a um momento em torno da própria linha apenas por forças nesses pontos; faces, fundo, tampo e demais juntas precisam fechar o caminho. Próxima comprovação: curvas das juntas axial/cortante e deformação da caixa completa, com ferramenta e fixadores reais.

Reproduzir na raiz: `python -B ferramentas/aereos/mapear_caminho_caixa.py --movel P17` e `python -B ferramentas/aereos/conferir_caminho_caixa.py --movel P17`. R52 preservada; nenhum ensaio físico.

**Complemento25/10/2026:** Elias definiu “20 kg / 10 kg / 10 kg” na ordemP17/P04/P12 e “Desenvolver os fundos inteiros”, com “Base limpa, sem cabeças ou tampinhas aparentes”. [LoteB vigente](../../Aereos_suspensao/README.md#lote-b--p17p04p12): fundo1964×550 preferido para estudo, massa globalP17 com20kg≈72,24–92,33kg sem ferragens;24 posições Minifix com acesso interno reconciliadas comR00. Substituir as8 entradas inferiores antigas. A caixaR52 permanece intacta. Ligações traseiras reconciliadas; implantação da suspensão abaixo. Capacidade e rigidez real das juntas pendentes; as flechas locais não comprovam o novo Minifix.

Estudo nominal separado, 25/10/2026. **O fundo e as divisórias precisam de ligações positivas para participar do caminho da carga.** A placa18 mantida dá resultados condicionais favoráveis quando esses caminhos são creditados; não há comprovação de juntas, caixa completa ou carga de uso.

Fonte: R51 completa preservada, SHA256 `ab5323bb12f8eca40b25bdfe4eadc8a3221c82b0646f354cd1f2832acfb27c16`. Reutiliza a [geometria e demanda global do P17](../../Aereos_suspensao/README.md) e a placa Ritz existente. Não usa tubos ou quadros metálicos.

## Suspensão candidata — 26/10/2026

[Implantação e memória](../../Aereos_suspensao/P17_suspensao.json) · [desenho](../../Aereos_suspensao/P17_suspensao.png) · [conferência independente](../../Aereos_suspensao/P17_verificacao_suspensao.json) · [requisitos para produto/oficina](../../Aereos_suspensao/P17_qualificacao_suspensao.txt).

Bigfer04.02.058 candidata em dois cantos laterais/fundo18: assentos u40,5/1923,5; Z514 desde a base externa. Dois suportes são hipótese de qualificação. O metal ocupa≈60mL/par, sem recuar o fundo nem mudar vãos; cabeça/capa/acesso não estão nesse volume. Fundo inteiro1964×550 continua proposta separada, BrancoTX nas duas faces e fita inferior off-white.

**Acesso:** a altura herdada Z492 alinhava o corredor do parafuso auxiliar aos dois calços superiores externos. Subir22mm no estudo deixa10mm entre metal e tampo. Oito calços fixos e24 acessosMinifix conferidos. No auxiliar traseiro u9,5, envolventeØ20 invade0,5mm a lateral; reservaØ12 passa com3,5mm nominais até a lateral. Não escolhe ferramenta/cabeça nem comprova manuseio. Montar antes das portas; manutenção com portas desclipadas e calços mantidos. Corpos das dobradiças em movimento não foram validados.

**Demandas:**255 casos e765 equilíbrios3D,1530 vetores; braço hipotético424mm até compressão inferiorZ90. No alvo20kg, máximos separados por suporte: V555,07N, T532,09N, R761,71N. [Seis casos simultâneos](../../Aereos_suspensao/P17_qualificacao_suspensao.csv) preservam V/T/R de cada lado; não combinar os máximos. Madeira+conteúdo até92,33kg, antes das ferragens reais. Por1kg emv200: +9,807N vertical, +1,961Nm e +4,626N de tração total nesse braço.

[Compressões inferiores](../../Aereos_suspensao/P17_reacoes_inferiores.csv): até518,80N sobre referência1080mm², ≈0,480MPa; sem pressão admissível atribuída. As faixas são das arestas existentes, não novos calços. Fundo/laterais coplanares exigem medir área/centro reais; Z90 não é garantido.

**Continua pendente:** métodoBigfer/fixadoresMDF18/cabeça/rasgo/retenção e ferramenta reais; juntas e transmissão pelo fundo/laterais até os cantos; deformação da referência superior, massa/CG de ferragens e ensaio representativo. Não distribuir esforços por parafuso nem atribuir rigidez ao conjunto de24Minifix/42Confirmat candidatos. Fundo e divisores não se tornam monolíticos. Montagem sustentada com aperto pela frente requer confirmação; rasgos espelhados não engatam por translação única. Ancoragens dependem da parede real. Nenhum ensaio, compra, contato externo ou mudançaR52.

Reproduzir: `python -B ferramentas/aereos/suspender_lote_b.py --movel P17` e `python -B ferramentas/aereos/conferir_suspensao_b.py --movel P17`. Fontes persistidas, hashes portáveis e solução independente por sistema linear de6 incógnitas. Equilíbrio não demonstra resistência/rigidez.

## Proposta geométrica

[Abrir estudo parcial FreeCAD](P17_fundo_inteiro_ligacoes_ESTUDO.FCStd). São nove peças: oito formas copiadas e somente o fundo substituído. O fundo18 passa de514 para550 de altura, preenchendo as faixas atrás da base e do tampo. Largura1964, profundidade da base312 e altura externa550 preservadas. As quatro divisórias permanecem nas mesmas posições; o conjunto central continua sendo duas chapas18, sem crédito de composição monolítica.

![P17: caixa parcial e fundo verde proposto](P17_estudo.png)

**16 contatos de face conferidos:** quatro base–divisória, quatro tampo–divisória, quatro fundo–divisória, dois fundo–lateral e dois fundo–base/tampo. Acréscimos sem interferência volumétrica nos sólidos visíveis da pose atual. Portas/ferragens estão ausentes somente deste arquivo parcial; continuam completas na R51. Não é um novo ensaio dos movimentos.

Os58 eixos ocultos são posições históricas de interface, não furos CNC nem58 ferragens adicionais. Estão em [Conferencia_geometrica.json](Conferencia_geometrica.json), com coordenadas do estudo, módulo e globais. O loteB reconcilia oR00 e substitui as entradas inferiores na proposta de base limpa; não manter o gabarito antigo por baixo. Não cortar ou furar pela imagem.

## Cálculo e significado

[Resultados completos](Resultados.json), reproduzíveis com `python calcular.py` e NumPy. UnidadesN/mm/MPa/kg. Base1964×312×18; espessura resistente17,7 e de massa18,3; densidade hipotética800; E inicial2200 reduzido pela metade para sensibilidade ao efeito diferido, ν0,30. Não é propriedade certificada de uma chapa escolhida.

As divisórias têm centros u473/973/991/1473. Conteúdo distribuído significa o total dividido igualmente entre os quatro vãos úteis; o frontal ocupa uma faixa60 de profundidade em cada vão. Não são20 kg por vão.

| Caminho creditado | Conteúdo hipotético | Flecha máxima + reserva0,20 mm |
|---|---|---:|
| Divisórias e fundo ligados | 10 kg distribuídos no total | 0,644 mm |
| Divisórias e fundo ligados | 20 kg distribuídos no total | 0,863 mm |
| Divisórias e fundo ligados | 20 kg na faixa frontal, total | 1,336 mm |
| Divisórias e fundo ligados | 10 kg somente no segundo vão | 1,108 mm |

Referência interna de triagem:500/300=1,667 mm, pelo maior espaçamento entre eixos de apoios. Não é limite normativo nem aprovação do conjunto. Reserva0,20 representa a deformação adicional admissível **a comprovar** na referência superior/caixa/suspensão; não é medida realizada.

Cada divisória tem dois caminhos axiais, nas profundidades72 e240, entre duas juntas em série e a chapa vertical514. O fundo tem12 caminhos verticais com faixa resistente analítica100, altura entre eixos532. Essas faixas não são cortes físicos. Peso próprio da base entra como carga de placa; pesos das divisórias e do fundo entram no deslocamento inicial dos caminhos. Reações superiores incluem esses pesos. Tampo, portas e laterais não são uma segunda carga sobre esta placa: pertencem ao modelo global.

**Requisito hipotético por posição:** K inicial500 N/mm em cada junta inferior e superior, reduzido a250 na sensibilidade. Duas posições por divisória significam grupo inferior1000 e grupo superior1000 iniciais, antes de considerar a série; não significam um caminho equivalente1000. Laterais usam um caminho completo requerido500 inicial por posição. Não se atribui essa rigidez a qualquer Confirmat/Minifix por nome.

No frontal20, E inicial1600 com K inicial500 dá1,555 mm. Reduzir K para250 dá1,871 mm com E2200, ou2,101 mm com E1600: excede a referência. Duplicar K para1000 dá1,057 mm com E2200. Reduzir a faixa analítica traseira100 para50 altera o caso E1600/K500 para1,555 mm, sem substituir prova de espalhamento, ligações e cisalhamento reais.

Há reações negativas de até cerca6,7 N nas posições de placa dos casos completos calculados: o modelo exige retenção, não só contato por gravidade. Forças superiores por posição ficam registradas no JSON, chegando a cerca82,9 N nos casos completos desta rodada; não são capacidade do parafuso nem a demanda global do aéreo. As ligações também participam de esforços horizontais e torção, fora deste submodelo.

As referências sem crédito das divisórias dão respostas lineares muito grandes: somente laterais193 mm no caso10 kg, ou laterais+fundo22 mm no caso20 kg. **Estão fora da hipótese de pequena deformação; servem para rejeitar esses modelos de apoio, não para prever a flecha real ou afirmar que o móvel atual cairá.** O modelo atual pode mobilizar caminhos não demonstrados; eles não foram presumidos.

O fundo inteiro acrescenta1,035 kg a800 kg/m³, ou1,164 kg a900. A demanda global anterior usa o fundo atual514. Se a proposta for incorporada, atualizar massas e suspensão; não misturar o novo fundo com a capacidade de um suspensor ainda não escolhido.

Essas massas usam18,3 de espessura para cálculo. O BREP nominal18 acrescenta1,018kg a800; a diferença é de hipótese, não perda de detalhe. [Quantitativo conferido dos arquivos gravados](../../Quantitativos/README.md), separado da lista-base e do orçamento.

## Condições para avançar sem o apartamento

1. Oficina/produto: qual ligação realiza cada caminho inferior/superior, em chapa18 efetiva, com rigidez, tração/cisalhamento combinados, esmagamento e bordas demonstrados? Confirmat7×50 é candidato de estudo. Confirmar piloto, cabeça, profundidade, torque, acesso e acabamento; não copiar uma resistência genérica.
2. Prova de junta: registrar curva força–deslocamento por posição ou grupo, orientação e lotes do painel. Comparar com K requerido, sem confundir resistência máxima com rigidez. Os dois caminhos precisam da mesma referência de deslocamento.
3. Caixa completa: demonstrar a deformação do tampo/uniões/suspensão e distorção do fundo sob esforços simultâneos. A reserva0,20 não pode ser atribuída a parede desconhecida. Medir também rotações e deslizamentos, sem ajustar o resultado ao modelo.
4. Ensaio de conjunto: usar carga distribuída e frontal compatível com um protocolo acordado, registrar carga real, posição, tempo, temperatura/umidade, flecha instantânea/residual e danos. Estes casos numéricos não são autorização para ensaio humano improvisado ou carga de uso.
5. Elias: revisar acabamento/acesso das cabeças antes da integração. Depois, atualizar ficha, quantitativos e demanda global. Ancoragem no imóvel depende do substrato real após as chaves.

Nenhum ensaio físico foi executado. [Verificações](Verificacao.json): seis convergências16/20, equilíbrio de forças/momentos, restrições, integridade dos arquivos, contatos e fonte preservada. Equilíbrio e convergência verificam a solução do modelo adotado; não validam suas hipóteses físicas.

Rotinas: [calcular.py](calcular.py), [criar_estudo.py](criar_estudo.py) no FreeCAD e [verificar.py](verificar.py). O criador recusa sobrescrever arquivo existente; não execute sobre a sessão de trabalho sem ler suas guardas. Não altera ou anima a R51.
