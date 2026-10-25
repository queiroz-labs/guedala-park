# Corte nominal e formatos — lista-base R52 e propostas separadas

25/10/2026. A triagem foi ampliada para os **249 painéis da lista-base inteira** e as **36 peças das sete propostas**, sem incorporar nenhuma proposta ou alterar CAD/lista de materiais. Foi fechado o requisito dimensional do fundo P01, com margens e orientação explícitas, e criado um arranjo geométrico preliminar de210 painéis com especificação suficiente para agrupamento documental. Os39 restantes estão identificados por peça, sem comprar ou escolher material em seu lugar.

## O que cabe nos formatos examinados

| Lista examinada | Formato bruto | Sem refilo | Refilo10 por borda | Refilo20 por borda |
|---|---|---:|---:|---:|
| Base R52 —249 painéis |2750×1850 |248 cabem |248 cabem |248 cabem |
| Base R52 —249 painéis |2750×2100 |249 cabem |249 cabem |249 cabem |
| Propostas —36 peças separadas |2750×1850 |35 cabem |35 cabem |35 cabem |
| Propostas —36 peças separadas |2750×2100 |36 cabem |36 cabem |36 cabem |

Cotas emmm. Esta tabela testa **um retângulo por vez, permitindo rotação90°**; não soma as listas e não comprova o sentido do veio. As duas exceções ao formato1850 são o fundo atual `Peca208`,1964×2096×18, e seu substituto de estudo `Estudo_Peca208`,1964×2114×18. Não foi encontrado outro envelope excedente nos285 registros. A lista-base soma59,262776m² de envelopes; esse total não é área líquida de compra nem desconta os recortes especiais.

[Triagem por peça e margem](Triagem_formatos.json) · [base expandida —249 IDs](Lista_base_249.csv) · [propostas —36 linhas](Propostas_36.csv).

## Requisito fechado para o fundo P01 inteiro

No formato2750×2100, colocar a dimensão2096/2114 **paralela ao lado2750** e a dimensão1964 paralela ao lado2100:

| Requisito | Fundo atual | Fundo proposto |
|---|---:|---:|
| Retângulo nominal |2096×1964 |2114×1964 |
| Formato bruto mínimo com refilo10 em cada borda, sem sobremetal do blank |2116×1984 |2134×1984 |
| Formato bruto mínimo com refilo10 e sobremetal2 em cada borda do blank |2120×1988 |2138×1988 |
| Sobra dimensional na janela2730×2080, sem sobremetal |634×116 |616×116 |
| Refilo uniforme máximo em2750×2100, sem sobremetal |68/borda |68/borda |
| Refilo uniforme máximo com sobremetal2/borda |66/borda |66/borda |

O limite68 vem de `(2100−1964)/2`; os dois fundos têm a mesma dimensão transversal. Para refilos diferentes, a soma das duas margens transversais não pode exceder136mm menos o sobremetal das duas bordas. O teste de fronteira passa em68 e falha em68,001; com sobremetal2, passa em66 e falha em66,001. Esses são limites matemáticos, não margens recomendadas de fabricação.

**A orientação inversa é diferente:** com1964 paralelo a2750, o fundo atual2096 atravessa o lado2100 e permite no máximo2mm uniformes de refilo, sem sobremetal. Com10mm/borda, essa orientação já não cabe. O fundo proposto2114 não cabe nessa orientação nem sem refilo: excede2100 em14mm. Portanto, “cabe em2750×2100” só fica demonstrado para a orientação adequada; produto, face e eventual direção resistente/decorativa precisam permitir essa escolha.

O formato2750×1850 é114mm menor que1964 antes de qualquer margem. Não existe rotação90° que resolva; com refilo10/borda, faltam134mm na largura útil. Uma emenda não foi adotada: alteraria o fundo que participa das verificações estruturais.

Os requisitos podem ser usados agora como filtro objetivo de produto: dimensão útil, orientação admissível, espessura18 e composição de faces precisam constar da solução real. A referência local de2750×2100 é uma ficha de linha ARAUCO2024; ela não comprova estoque, fornecimento, BrancoTX ou composição deste projeto. Nenhum fornecedor ou preço foi inventado.

[Requisito e todas as orientações/margens](Requisito_fundo_P01.csv).

## Arranjo preliminar por especificação documental

Hipóteses editáveis em [Parametros.json](Parametros.json): refilo10mm em cada borda; serra3,2mm entre envelopes; sobremetal0mm por borda do blank. Não foram descontadas fita ou selagem das dimensões nominais. Os formatos são chapas **virtuais** de2750×1850 e2750×2100; a referência comercial18mm do segundo formato não foi extrapolada como disponibilidade comprovada para15/16 ou outros padrões.

| Grupo | Especificação de faces registrada | Esp. nominal | Peças incluídas | Chapas virtuais no ensaio com rotação |
|---|---|---:|---:|---:|
| G01 | BrancoTX, faces internas |15 |35 |1 |
| G02 | BrancoTX, faces internas |16 |8 |1 |
| G03 | BrancoTX, faces internas |18 |103 |6 |
| G04 | BrancoTX interno + BeigeMatt aparente |18 |2 |1 |
| G05 | BrancoTX interno + LouroFreijóPoro aparente |18 |4 |1 |
| G06 | BrancoTX interno + Arenza aparente |18 |2 |1 |
| G07 | BrancoTX interno + GreenplacArenza aparente |18 |29 |2 |
| G08 | BrancoTX interno + AzulPetróleo aparente |18 |20 |2 |
| G09 | BrancoTX interno + Off-white aparente |18 |7 |1 |

Foram mantidos os textos de especificação distintos, inclusive G06/G07; não se presumiu que tenham o mesmo produto, lote, face reversa ou processo. Poderão ser reconciliados quando os códigos e a composição forem fechados. A seleção de duas faces não prova que exista chapa dual comercial pronta; todos os grupos continuam condicionados a substrato/produto/processo.

O ensaio com rotação livre encontrou **16 chapas virtuais para210 painéis**:15 pequenas e1 grande. O ensaio com C nominal paralelo a2750 encontrou17:16 pequenas e1 grande. Esses números **não cobrem os39 painéis excluídos, as36 propostas ou perdas de processo**, nem constituem pedido de compra. A heurística experimenta três ordens de empacotamento e escolhe um arranjo encontrado; não demonstra o mínimo de chapas. Alterar serra/ordem pode mudar suas escolhas, sem uma relação monotônica entre parâmetro e contagem encontrada.

Os83 painéis recortados/especiais da base foram triados pelo retângulo envolvente; os que entram no arranjo ocupam o blank inteiro, sem encaixar recortes uns nos outros. Os desenhos não representam contornos finais, furos, rasgos, CNC ou sequência executiva de serra.

[Todos os posicionamentos, grupos e cenários](Arranjos_preliminares.csv) · [plano completo emJSON](Planos_preliminares.json) · [exemplo do fundo P01](Planos_svg/G03_chapa_01.svg) · [exemplo das caixas de gavetas15](Planos_svg/G01_chapa_01.svg). A pasta `Planos_svg` contém os16 desenhos do primeiro cenário; osIDs e dimensões podem ser ampliados sem perda de resolução.

## Os39 painéis sem definição suficiente para este arranjo

Motivo principal de exclusão, sem esconder motivos adicionais:

| Motivo principal | Painéis |
|---|---:|
| Material/padrão aparente ainda registrado como referência |23 |
| Faces ou composição explicitamente parciais |12 |
| Espessura de envelope16,2 ou30 sem produto construtivo tratado neste plano |2 |
| Espelho como camada distinta, composição do substrato ainda não formalizada |2 |

Entre as faces/composições parciais estão as duas tampas20 do banco, laterais do escritório, quadro do banheiro e reservasP08. A faixa7 também tem padrão de referência, por isso aparece no primeiro motivo, sem virar chapa comercial por seu envelope. As tampas do banco continuam com face superior, recessos e composição/fixação da piano/trava pendentes; a menção superada ao receptorR47 foi corrigida nas fontes antes desta extração, sem alterar dimensões ou escolher painel.

Em nenhum dos249 registrosCSV existe um campo que fixe produto construtivo completo e direção do veio porID. Isso não apaga decisões de acabamento: impede converter o arranjo nominal em autorização de rotação, compra e corte. A relação [Peças_sem_definicao_suficiente.csv](Peças_sem_definicao_suficiente.csv) informaIDs, dimensões e motivo exato, permitindo fechar as definições com a oficina antes das chaves.

## Propostas reconciliadas com a base R52

Os11 objetos substituídos nas propostas ainda correspondem às dimensões da baseR52; nenhum desencontro foi encontrado nessa comparação. A tabela preserva a área da peça substituta inteira e o acréscimo sobre a antiga:

| Kit separado | Peças propostas | Substituições | Acréscimos | Área proposta m² | Acréscimo m² |
|---|---:|---:|---:|---:|---:|
| PrateleirasP01,723 |2 |2 |0 |0,795300 |0,019800 |
| SocoP01 |21 |0 |21 |0,775632 |0,775632 |
| Encontro traseiroP01/P03 |2 |2 |0 |5,005996 |0,059004 |
| FundoP04,308 |1 |1 |0 |0,543312 |0,063504 |
| ComposiçãoP15,36 |4 |3 |1 |1,121770 |0,304314 |
| FundoP17,550 |1 |1 |0 |1,080200 |0,070704 |
| Bancada de marcenaria |5 |2 |3 |1,932840 |1,726440 |

As36 peças continuam em sete kits não adotados. Não há total “base + todas as propostas”. As referências de acabamento das peças substituídas foram mantidas como informação; não foram transferidas como material escolhido para todos os acréscimos. A regra, depois de uma adoção demonstrada, é retirar osIDs substituídos e incluir os novos da alternativa correspondente, reconciliando materiais e processo — não simplesmente somar áreas.

[Resumo por kit](Resumo_kits.csv) · [linhas e vínculos com a base](Propostas_36.json).

## Reprodução e conferências

```powershell
python analisar.py
python verificar.py
```

Usam somente a biblioteca padrãoPython. A execução desta entrega usou oPython disponibilizado pelo ambiente. O primeiro script lê as20 listasCSV atuais e as fontes locais dos estudos/formatos; não abre, recomputa ou salva documentosFreeCAD. `CAD_DATA.current_revision` foi conferido comoR52. Os hashes dosCSV, estudos e cacheCAD são registrados antes e depois; a entrada permaneceu igual durante a análise.

[Verificacao.json](Verificacao.json) registra4.045 pares conferidos nos dois cenários, sem sobreposição nem intervalo inferior à serra declarada, cobertura exata dos210IDs por cenário, separação dos39 excluídos, limites da janela útil, espessura/especificação por grupo e regras de rotação do cenário. Reconciliou249 registros/área com osCSV agrupados por uma leitura independente,36 propostas/11 substituições/25 acréscimos e os sete totais de área. Testes de fronteira doP01 e alterações controladas de sobreposição/duplicação foram detectados. A serra foi reavaliada em0/3,2/6,4mm, com novo empacotamento e conferência geométrica a cada valor.

OsSVG de uma chapa densa e da chapa grande do fundo foram renderizados e inspecionados. Nenhuma parede ou medida real foi inventada. Restam dados de produto e oficina: substrato e composição, faces, veio, fita/selagem, dimensões de compra úteis, ferramentas, manuseio, contornos especiais e validação das ligações. Não houve compra, contato ou publicação.

Fontes locais: [quantitativos anteriores](../../Quantitativos_estudos_2026-10-25/README.md), [formatos registrados e referências de origem](../../Quantitativos_estudos_2026-10-25/Formatos_e_pendencias.json), fichasR14 correntes e [hashes de cada entrada](Fontes_e_hashes.json). A origem comercial dos formatos foi aproveitada como evidência local; não foi feita nova pesquisa de catálogo/estoque nesta etapa.
