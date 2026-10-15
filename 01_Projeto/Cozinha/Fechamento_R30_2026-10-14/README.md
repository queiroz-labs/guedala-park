# Fechamento do conjunto forno cooktop e bancada

14/10/2026 · Base R30 · Estudo de compatibilização, sem liberação de execução.

**[Abrir os cortes e a planta de conferência](Corte_coccao_R30.html).** O vão lateral foi ampliado na R30, mas a instalação conjunta ainda depende das referências reais dos aparelhos, ventilação, apoio e conexão com a lavanderia. A bancada permanece a 920 mm. Não foi alterado o modelo.

## O que está conferido na R30

Leitura dos parâmetros gravados no FCStd, sem depender de abrir o FreeCAD. As coordenadas abaixo usam o apartamento espelhado, X = 7400 − X da base de edição; por isso diferem das coordenadas da base citadas no relatório original da R30. [Dados e método](Conferencia_parametros_R30.json).

| Elemento | Resultado em mm | Interpretação |
|---|---:|---|
| Vão entre laterais | 577 | Módulo com largura total de estudo 613 e laterais de 18 |
| Forno representado | 517 × 615 × 610 | Envelope total simplificado; não é corpo de embutimento |
| Folgas laterais ao envelope | 30 / 30 | Geometria do estudo; não encerra a divergência de instalação Venax |
| Corpo de embutimento da fonte arquivada | 485 × 560 × 570 | Não está separado da frente no CAD; posição relativa e apoios por confirmar |
| Folgas laterais ao corpo de 485 | 46 / 46, condicionais | Somente se centralizado no mesmo eixo e sem intrusões; não chamar 517 de corpo |
| Traseira do envelope à parede de estudo | 15 | Não demonstra os 50 da tabela documental; a origem traseira do corpo precisa ser confirmada |
| Topo do envelope / base da travessa | 660 / 660 | Contato de planos e sobreposição em planta entre gabaritos, sem nova análise BREP |
| Travessa | 577 × 212 × 30, Z660–690 | Apoio ainda não dimensionado |
| Pedra | Z900–920; profundidade cozinha 630 | Representada como caixa inteira, com recortes pendentes |
| LG até face externa da lateral | 67 | Espaço geométrico; isolamento térmico ainda não detalhado |
| Eixo do forno / eixo do cooktop | X3226,5 / X3220 | Desvio de 6,5; não determina sozinho a necessidade de mover o cooktop |
| Lateral junto à lavanderia | X3515–3533 | Emenda das pedras em X3520: 13 da lateral ficam sob a pedra da lavanderia |

**Correção de linguagem:** o relatório original da R30 usa “corpo de 517 mm”. O próprio objeto Peca133 registra que 517 × 615 × 610 é envelope ilustrativo. Os 30 mm laterais foram obtidos em relação a esse envelope. A ampliação permanece registrada, sem desfazer a decisão ou afirmar que ela era obrigatória para o corpo de 485 mm.

## Corte vertical e limites

Seja **d** a distância entre a superfície da bancada e o ponto inferior relevante do KE4GC instalado, incluindo as referências que o fabricante precisar esclarecer. Com topo do envelope do forno em 660 e bancada em 920:

**Separação de estudo = 260 − d. Para 200 mm: d ≤ 60 mm.**

| d hipotético | Separação | Saldo sobre 200 |
|---:|---:|---:|
| 40 | 220 | +20 |
| 50 | 210 | +10 |
| 60 | 200 | 0 |
| 70 | 190 | −10 |
| 80 | 180 | −20 |

Esses valores são cenários, não medidas do cooktop. A caixa superior de 15 mm do modelo omite a parte inferior, grampos e conexões. A altura total publicada de 131 mm também não fornece d. A hipótese de bancada 5 mm mais baixa e forno 5 mm mais alto consome 10 mm; nesse cenário, d precisaria ser ≤50 mm. A margem é uma análise de tolerância, não requisito adicional atribuído ao fabricante.

**Travessa:** elevar sua base de 660 para h cria folga g = h − 660 acima do envelope. Sob uma hipótese conservadora de sobreposição com o cooktop, a face superior de 30 mm precisa satisfazer h + 30 ≤ 920 − d; portanto g ≤ 230 − d. Isso só define uma região geométrica de estudo. Não fixa g mínimo térmico, resistência, percurso de ar ou montagem. Sem d e apoio definidos, não foi selecionada nem aplicada nova altura.

## Profundidade e ventilação

O envelope atual ocupa Y6370–6985, e a parede de referência é Y7000. Deslocar esse envelope 35 mm para a frente produziria 50 mm atrás e 35 mm de projeção além da pedra. É uma consequência geométrica, **não uma proposta adotada**, pois corpo, frente e conexões não têm seus planos relativos confirmados. Não aumentar a pedra nem deslocar o forno apenas para corrigir uma caixa ilustrativa.

O estudo documental arquivado usa corpo de 560 e reserva posterior de 50, totalizando 610 de nicho sem sobra. Também registra abertura inferior de 380 × 450 e passagens Electrolux de 30 mm em posições específicas. Essas referências precisam ser compatibilizadas num percurso contínuo de entrada e saída de ar; não comprovam ventilação só pela área ou pela soma de folgas. A travessa posterior atual ocupa Y6770–6982 e deixa 18 até a parede de estudo, o que deve ser confrontado com esse percurso. Não atribuir automaticamente os 30 mm do desenho Electrolux a essa posição.

## Pedra e transição para a lavanderia

O recorte de 520 × 390 vem do estudo do manual arquivado; não existe recorte executado nas caixas de pedra inspecionadas. Se o recorte for centralizado no cooktop atual, seu intervalo transversal de estudo será X2960–3480: sobram 22 mm até a face interna de uma lateral e 35 até a outra. Centralizar no novo eixo do forno daria 28,5 de cada lado e moveria o eixo 6,5. Nenhuma opção está escolhida; caixa inferior, grampos, bordas mínimas e apoio da pedra decidem, não a simetria isolada.

As pedras se encontram em X3520. A lateral nova cruza esse plano, ficando 5 mm sob a pedra da cozinha e 13 sob a lavanderia. Isso identifica onde detalhar emenda, apoio e montagem; não prova falha estrutural nem autoriza mudar a emenda. A pedra da lavanderia continua com profundidade 750 e a da cozinha 630.

A faixa de 67 mm até a LG não comprova isolamento. O achado 04 registra referência LG a painel de isolamento 850 × 600 com alumínio voltado ao forno em proximidade inevitável. Material, espessura, instalação, manutenção e efeito sobre a faixa disponível precisam de detalhe próprio; a lateral de MDF não foi considerada solução equivalente.

## O que pode avançar e o que depende de confirmação

| Ação | Estado | Evidência necessária para encerrar |
|---|---|---|
| Atualizar cotas, eixos e distinção corpo/envelope | Concluído nesta conferência | Parâmetros salvos e fontes arquivadas vinculados |
| Documentar cenários de altura e profundidade | Concluído como estudo | Tabelas e cortes, sem alteração da R30 |
| Fixar d e envelope inferior do KE4GC | Pendente externa | Corte cotado do modelo/PNC ou levantamento do aparelho, com caixa, grampos e conexões |
| Definir folgas aplicáveis da Venax | Pendente externa | Esclarecimento escrito sobre 30/50 versus 100 em toda a volta e validade do esquema de bancada para o SKU |
| Separar corpo, frente e apoio do forno | Pendente externa | Corte do GIII, datums, apoio e abertura de porta |
| Reposicionar travessa e detalhar apoio | Pendente técnica | Dados anteriores, estrutura, calor e ventilação compatibilizados |
| Escolher eixo do recorte e detalhe da emenda | Pendente técnica | Desenho de montagem dos aparelhos e detalhamento da marmoraria |
| Detalhar isolamento junto à LG e ligações | Pendente técnica | Solução compatível com os aparelhos e espaço de manutenção |

As consultas técnicas a Electrolux e Venax já estão [redigidas no estudo anterior](../../Compatibilizacao_2026-09-28/Corte_coccao.md#5-consulta-técnica-pronta--não-enviada). Permanecem não enviadas. Não há nova escolha estética a solicitar para responder a essas lacunas.

## Fontes e limites da conferência

- [R30 e alterações](../../Modelo_FreeCAD/01_Atual/Consistencia_R30_2026-10-14/README.md).
- [Corte documental de 28/09](../../Compatibilizacao_2026-09-28/Corte_coccao.md), com páginas dos manuais e hipóteses de montagem.
- [Revisão documental de 14/10](../../Modelo_FreeCAD/02_Revisoes_e_estudos/Revisao_fontes_coccao_R23_2026-10-14/Revisao_documental.md): as ambiguidades permaneciam nos PDFs comparados naquela rodada.
- [Achados da R28](../../Modelo_FreeCAD/02_Revisoes_e_estudos/Revisao_solicitada_R28_2026-10-14/Achados_R28.json), especialmente 04, conciliado com as mudanças R30.
- [Extração reproduzível](conferir_dados.py) e [valores extraídos](Conferencia_parametros_R30.json).

Não houve nova pesquisa de produto ou consulta externa. A conexão do FreeCAD estava indisponível: leitura direta dos parâmetros XML salvos de oito caixas, sem recalcular o documento, verificar BREP, testar movimentos ou revalidar vínculos. Coordenadas e contas são verificáveis nesse escopo; a instalação física permanece em aberto.
