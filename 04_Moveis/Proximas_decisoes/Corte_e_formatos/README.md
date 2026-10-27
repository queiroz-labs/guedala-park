# Corte nominal e formatos — lista-base R52 e propostas separadas

**Regra vigente 25/10 aplicada aos agrupamentos:** um padrão por chapa física, igual nas duas faces. Duas peças separadas 18+15 podem ter cores distintas, com IDs/constituição definidos; nenhuma segunda chapa foi acrescentada. Os CSV/JSON e 16 desenhos vigentes foram reemitidos com a [regra por peça](../../../ferramentas/site/fabrication/Decisao_acabamentos_R13.md). São arranjos geométricos virtuais, não compra/corte aprovados.

**Base reconciliada:**249 painéis das fichas, 248 na auditoria de acabamentos; o apoio P13/Peca350 não tem entrada nessa auditoria e permanece excluído por acabamento indefinido. 215 painéis entram no ensaio, 34 continuam com bloqueio identificado. Dimensões/IDs dos 249 e área 59,262776 m² preservados; CAD/fichas/orçamento não alterados. As 36 peças de sete propostas continuam separadas. [Conferência por ID e fontes](Reconciliacao_acabamentos.json).

## P13 / Peca350 — escolha de acabamento pendente

Agenda 27/10, preparada em 26/10/2026. Prateleira de apoio do micro: **697×470×18mm**, área de envelope0,327590m², topo nominal1550. Fonte: [ficha por ID](../../../06_Entregas/Fichas_fabricacao/P13-pecas.csv). A ficha menciona Greenplac Arenza como referência CAD, mas mantém acabamento parcial; não converter essa referência em escolha executiva.

**Pergunta fechada F13 para Elias: qual padrão quer nas duas faces da Peca350?**

| Opção | Aparência / consequência | Custo e condição |
|---|---|---|
| A — Greenplac Arenza liso nas duas faces | Coordena o apoio aberto e a face inferior visível com a marcenaria da cozinha; preserva a referência visual do CAD | Código/substrato18, bordas e preço ainda precisam de fornecedor/amostra; não assumir que sobra da chapa virtual cubra a peça |
| B — Branco TX nas duas faces | Clareia a face inferior e diferencia o apoio aberto do Arenza adjacente | Mesmo envelope18; economia não quantificada e não presumida. Oficina deve cotar mesma constituição/processo para comparar |

Resposta F13=__; data/fonte=__. **Nenhuma opção adotada.** Não propor Arenza numa face e Branco TX na outra da mesma chapa, nem acrescentar interna15 automaticamente. Uma eventual segunda peça teria de ter ID, espessura, vão, ligações e custo próprios e não integra esta pergunta.

Depois da resposta: fornecedor identifica produto18 e acabamento de bordas; projeto inclui Peca350 na auditoria por ID e só então reconcilia o grupo de corte. A escolha estética não resolve suporte/juntas nem a divergência100mm desejados versus300mm do manual do micro; esses bloqueios permanecem em [instalação](../Instalacao_e_P16/README.md). Até lá, Peca350 continua entre os34 excluídos, sem regeneração ou corte de chapa por hipótese.

## O que cabe nos formatos examinados

| Lista examinada | Formato bruto | Sem refilo | Refilo 10 por borda | Refilo 20 por borda |
|---|---|---:|---:|---:|
| Base R52 —249 painéis |2750×1850 |248 cabem |248 cabem |248 cabem |
| Base R52 —249 painéis |2750×2100 |249 cabem |249 cabem |249 cabem |
| Propostas —36 peças separadas |2750×1850 |35 cabem |35 cabem |35 cabem |
| Propostas —36 peças separadas |2750×2100 |36 cabem |36 cabem |36 cabem |

Cotas em mm. Esta tabela testa **um retângulo por vez, permitindo rotação 90°**; não soma as listas e não comprova o sentido do veio. As duas exceções ao formato 1850 são o fundo atual `Peca208`,1964×2096×18, e seu substituto de estudo `Estudo_Peca208`,1964×2114×18. Não foi encontrado outro envelope excedente nos 285 registros. A lista-base soma 59,262776 m² de envelopes; esse total não é área líquida de compra nem desconta os recortes especiais.

[Triagem por peça e margem](Triagem_formatos.json) · [base expandida —249 IDs](Lista_base_249.csv) · [propostas —36 linhas](Propostas_36.csv).

## Requisito fechado para o fundo P01 inteiro

No formato 2750×2100, colocar a dimensão 2096/2114 **paralela ao lado 2750** e a dimensão 1964 paralela ao lado 2100:

| Requisito | Fundo atual | Fundo proposto |
|---|---:|---:|
| Retângulo nominal |2096×1964 |2114×1964 |
| Formato bruto mínimo com refilo 10 em cada borda, sem sobremetal do blank |2116×1984 |2134×1984 |
| Formato bruto mínimo com refilo 10 e sobremetal 2 em cada borda do blank |2120×1988 |2138×1988 |
| Sobra dimensional na janela 2730×2080, sem sobremetal |634×116 |616×116 |
| Refilo uniforme máximo em 2750×2100, sem sobremetal |68/borda |68/borda |
| Refilo uniforme máximo com sobremetal 2/borda |66/borda |66/borda |

O limite 68 vem de `(2100−1964)/2`; os dois fundos têm a mesma dimensão transversal. Para refilos diferentes, a soma das duas margens transversais não pode exceder 136 mm menos o sobremetal das duas bordas. O teste de fronteira passa em 68 e falha em 68,001; com sobremetal 2, passa em 66 e falha em 66,001. Esses são limites matemáticos, não margens recomendadas de fabricação.

**A orientação inversa é diferente:** com 1964 paralelo a 2750, o fundo atual 2096 atravessa o lado 2100 e permite no máximo 2 mm uniformes de refilo, sem sobremetal. Com 10 mm/borda, essa orientação já não cabe. O fundo proposto 2114 não cabe nessa orientação nem sem refilo: excede 2100 em 14 mm. Portanto, “cabe em2750×2100” só fica demonstrado para a orientação adequada; produto, face e eventual direção resistente/decorativa precisam permitir essa escolha.

O formato 2750×1850 é 114 mm menor que 1964 antes de qualquer margem. Não existe rotação 90° que resolva; com refilo 10/borda, faltam 134 mm na largura útil. Uma emenda não foi adotada: alteraria o fundo que participa das verificações estruturais.

Os requisitos podem ser usados agora como filtro objetivo de produto: dimensão útil, orientação admissível, espessura 18 e composição de faces precisam constar da solução real. A referência local de 2750×2100 é uma ficha de linha ARAUCO2024; ela não comprova estoque, fornecimento, BrancoTX ou composição deste projeto. Nenhum fornecedor ou preço foi inventado.

[Requisito e todas as orientações/margens](Requisito_fundo_P01.csv).

## Arranjo preliminar por especificação documental

Hipóteses editáveis em [Parametros.json](Parametros.json): refilo 10 mm em cada borda; serra 3,2 mm entre envelopes; sobremetal 0 mm por borda do blank. Não foram descontadas fita ou selagem das dimensões nominais. Os formatos são chapas **virtuais** de 2750×1850 e 2750×2100; a referência comercial 18 mm do segundo formato não foi extrapolada como disponibilidade comprovada para 15/16 ou outros padrões.

| Grupo | Padrão único, igual nas duas faces | Esp. nominal | Peças incluídas | Chapas virtuais no ensaio com rotação |
|---|---|---:|---:|---:|
| G01 | Arauco BeigeMatt |18 |2 |1 |
| G02 | Arauco LouroFreijóPoro |18 |4 |1 |
| G03 | BrancoTX |15 |35 |1 |
| G04 | BrancoTX |16 |8 |1 |
| G05 | BrancoTX |18 |101 |6 |
| G06 | Greenplac Arenza liso |18 |38 |3 |
| G07 | Guararapes AzulPetróleo |18 |20 |2 |
| G08 | Off-white fosco |18 |7 |1 |

Os grupos refletem os padrões documentais atuais e a espessura; não comprovamSKU/substrato, lote, estoque, orientação ou processo. Arenza é liso; não acrescentar veio decorativo por antiga descrição amadeirada. Peças de padrão apenas referencial continuam excluídas. Espelhos são componentes separados, sem atribuir outra cor à face do painel.

Os dois cenários encontraram **16 chapas virtuais para 215 painéis**: 15 pequenas e 1 grande. Isso **não cobre os 34 excluídos, 36 propostas ou perdas de processo** e não é pedido de compra. A heurística testa três ordens e escolhe um arranjo encontrado, sem demonstrar mínimo ou ganho financeiro. Rotação livre e C paralelo 2750 são hipóteses geométricas; não identificam o veio nem autorizam rotação de peças reais.

Os 83 painéis recortados/especiais da base foram triados pelo retângulo envolvente; os que entram no arranjo ocupam o blank inteiro, sem encaixar recortes uns nos outros. Os desenhos não representam contornos finais, furos, rasgos, CNC ou sequência executiva de serra.

[Posicionamentos](Arranjos_preliminares.csv) · [plano JSON](Planos_preliminares.json) · [fundo P01](Planos_svg/G05_chapa_01.svg) · [gavetas 15](Planos_svg/G03_chapa_01.svg). Os 16 SVG listados no JSON são vigentes. Sete caminhos antigos sem chapa correspondente agora mostram aviso de substituição; não são chapas adicionais. Nenhum arquivo foi apagado/movido.

## Os 34 painéis excluídos do ensaio

Motivo principal de exclusão, sem esconder motivos adicionais:

| Motivo principal | Painéis |
|---|---:|
| Material/padrão aparente ainda registrado como referência |18 |
| Faces ou composição explicitamente parciais |12 |
| Espessura de envelope 16,2 ou 30 sem produto construtivo tratado neste plano |2 |
| Espelho como camada distinta, composição do substrato ainda não formalizada |2 |

Os 12 casos de acabamento/composição parcial incluem 11 da auditoria mais P13/Peca350: apoio do micro, tampas do banco, laterais do escritório, quadro do banheiro, base do espelheiro e reservas P08. Os 18 referenciais já têm direção de aparência, mas não código fechado. Dois casos de espessura e dois de espelho são bloqueios construtivos, não quatro novas cores a escolher. Ver IDs/motivos no CSV; não decidir acabamento ou fabricar por esta contagem.

Em nenhum dos 249 registros CSV existe um campo que fixe produto construtivo completo e direção do veio por ID. Isso não apaga decisões de acabamento: impede converter o arranjo nominal em autorização de rotação, compra e corte. A relação [Peças_sem_definicao_suficiente.csv](Peças_sem_definicao_suficiente.csv) informa IDs, dimensões e motivo exato, permitindo fechar as definições com a oficina antes das chaves.

## Propostas reconciliadas com a base R52

Os 11 objetos substituídos nas propostas ainda correspondem às dimensões da base R52; nenhum desencontro foi encontrado nessa comparação. A tabela preserva a área da peça substituta inteira e o acréscimo sobre a antiga:

| Kit separado | Peças propostas | Substituições | Acréscimos | Área proposta m² | Acréscimo m² |
|---|---:|---:|---:|---:|---:|
| Prateleiras P01,723 |2 |2 |0 |0,795300 |0,019800 |
| Soco P01 |21 |0 |21 |0,775632 |0,775632 |
| Encontro traseiro P01/P03 |2 |2 |0 |5,005996 |0,059004 |
| Fundo P04,308 |1 |1 |0 |0,543312 |0,063504 |
| Composição P15,36 |4 |3 |1 |1,121770 |0,304314 |
| Fundo P17,550 |1 |1 |0 |1,080200 |0,070704 |
| Bancada de marcenaria |5 |2 |3 |1,932840 |1,726440 |

As 36 peças continuam em sete kits não adotados. Não há total “base + todas as propostas”. As referências de acabamento das peças substituídas foram mantidas como informação; não foram transferidas como material escolhido para todos os acréscimos. A regra, depois de uma adoção demonstrada, é retirar os IDs substituídos e incluir os novos da alternativa correspondente, reconciliando materiais e processo — não simplesmente somar áreas.

[Resumo por kit](Resumo_kits.csv) · [linhas e vínculos com a base](Propostas_36.json).

## Reprodução e conferências

```powershell
python -B ferramentas/corte/reconciliar_acabamentos.py
```

Executar da raiz. O comando usa os geradores/verificadores anteriores e a auditoria por ID, apenas biblioteca padrão Python. Reemite dados/SVG, preserva dimensões/IDs, confere padrões iguais e mantém P13 como pendente. Hashes dos 20 CSV, estudos, regra, auditoria e CAD registrados antes/depois; sem abrir FreeCAD. `analisar.py` e `verificar.py` continuam ferramentas internas do estudo, chamados pelo comando integrado.

[Verificacao.json](Verificacao.json): 3956 pares nos dois cenários sem sobreposição/violação da serra, 215 IDs exatos por cenário, 34 excluídos, margens, espessura/padrão e rotação conferidos. Reconciliou 249 registros/área, 36 propostas/11 substituições/25 acréscimos e sete totais. Detectou sobreposição/duplicação inseridas de propósito; fronteiras P01 e serra 0/3,2/6,4 mm conferidas. A [reconciliação de acabamentos](Reconciliacao_acabamentos.json) acrescenta cobertura 248/249, padrões iguais, fontes e geometria preservadas.

Os 16 SVG atuais foram conferidos como XML; posições, margens e serra pelo verificador geométrico. Restam substrato, códigos, veio, fita/selagem, formato útil, ferramentas, manuseio, contornos especiais e ligações. Sem compra, contato, publicação ou alteração no CAD.

Fontes locais: [quantitativos anteriores](../../Quantitativos/README.md), [formatos registrados e referências de origem](../../Quantitativos/Formatos_e_pendencias.json), fichas R14 correntes e [hashes de cada entrada](Fontes_e_hashes.json). A origem comercial dos formatos foi aproveitada como evidência local; não foi feita nova pesquisa de catálogo/estoque nesta etapa.
