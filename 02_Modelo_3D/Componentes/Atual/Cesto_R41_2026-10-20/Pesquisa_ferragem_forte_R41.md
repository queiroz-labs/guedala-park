# Mecanismo mais forte — continuidade na R41

20/10/2026. A pedido de Elias, a revisão permanece **R41 até fechar o cesto**.8kg de roupa são agora requisito solicitado, não capacidade comprovada. Preservados saco removível, gabinete e geometria operacional. Nenhuma ferragem foi aplicada sem validação.

## O que avançou

A pesquisa ampliou de articuladores para portas leves para mecanismos inferiores de cabo, pistão e braços com capacidade por momento. Também foi calculado o esforço do conjunto ideal para orientar uma seleção por carga e posição, em vez de procurar apenas um número maior emkg.

| Modelo | Evidência | Conclusão |
|---|---|---|
| Häfele372.80.600,200N | [Fabricante: abertura para cima](https://www.hafele.com.br/pt/product/articulador-para-portas-de-uma-folha-com-abertura-pra-cima/P-01547936/). AnúncioGMAD chamaLiftJunior | Descartado para inversão presumida.200N não são20kg admissíveis no cesto. |
| HäfeleJuniorD140N | [Oferta brasileira](https://www.madeirasgasometro.com.br/articulador-para-porta-basculante-junior-d-140n-branco-hafele/p): abertura inferior, faixa210–480mm, porta até9kg | Oferta existe, mas não comprova conjunto8kg+frente/armação; frente500/521fora da faixa anunciada. Não aprovado. |
| HäfeleK12,372.05.110/111 | [Fabricante](https://www.hafele.com.br/pt/product/articulador-k12-com-abertura-para-baixo-com-movimento-de-abertura-suave/P-01539543/): abertura inferior, comprimentos164/244mm | Sem tabela de carga/momento comprovada nesta pesquisa nem oferta nacional específica confirmada. Comprimento pequeno não prova encaixe dinâmico. |
| SugatsuneHDS-10H | [Fabricante](https://global.sugatsune.com/global/en/tech/products/21577_t) e [manual](https://global.sugatsune.com/-/media/pim/SUGATSUNE/SUGATSUNE_GLOBAL/Manual/0894/0894_2_hds10):24,5–29,4Nm para o **par**, montagem inferior90° | Mais forte e especificado por momento, porém destinado a porta; manual pede apoio adicional para carga/uso sobre a porta. Sem fornecimento brasileiro fácil localizado. Não aprovado para cesto55°. |
| SugatsuneHDS-20/HDS-30 | Resultados oficiais indicam abertura superior | Não presumir funcionamento invertido. |

As buscas por marca, aplicação eSKU estão arquivadas emFontes. Não localizar oferta não prova que o produto inexista no Brasil. O download direto do manualHDS foi bloqueado pelo site; a leitura textual foi obtida pelo serviço de pesquisa e arquivada. Cotas gráficas não legíveis não foram usadas para criar furação.

## Esforço do cesto ideal

O modelo foi percorrido em7poses; os controles foram restaurados. Calculados momentos gravitacionais usando centros de massa do CAD,8kg no centro do volume de teste e densidade hipotética900kg/m³ para a frente. Foram omitidos os pesos da armação, saco, ferragens, pega e fixações: estes números **não são dimensionamento final nem autorização de carga**.

| Condição | Frente521 atual | Frente500, mantendo base |
|---|---:|---:|
|55°, roupa8kg no centro do volume de teste|21,27Nm|20,39Nm aproximadamente|
|90°, roupa8kg no centro do volume de teste|30,89Nm|29,90Nm|

Sem roupa, somente a frente521 produz12,43Nm a55°. A diferença ao retirar o saco demonstra por que o controle deve funcionar cheio e vazio. Não se escolhe uma mola mais forte só pela condição cheia.

Também se calculou um **limite teórico de distribuição**: se o centro de massa dos8kg puder ocupar qualquer ponto do envelope400×200×400mm, o momento a55° pode chegar a38,63Nm com frente521, ainda sem peso da armação. Não é previsão de como roupas reais se distribuem, nem fator de segurança; é análise de sensibilidade à posição da carga. Forças de mão, impacto e deformação não entram.

A comparação comHDS-10 não autoriza escolher modelo pela leitura instantânea em55°: sua tabela usa momento máximo de porta e sua instalação publicada é90°. Na situação hipotética90°, até a frente500 com roupa central já supera29,4Nm antes da armação. É necessário confirmar curso e aplicação real, não transplantar a tabela.

O espaço lateral nominal52mm também não foi declarado livre para qualquer braço: apoios, mangueiras, dobradiças e sua trajetória precisam entrar na conferência. Não foi reduzido saco, tanque ou gabinete para acomodar peças.

## Próximo passo concreto

Os catálogos públicos encontrados não fecham o conjunto. Foi preparada [consulta técnica para Häfele e FGVTN](Consulta_fabricantes_R41.md), com o espaço atual, carga exigida, frente500como alternativa, saco removível e perguntas objetivas sobre mecanismo, retenção, desenhos e revenda nacional. **Enviada separadamente à Häfele e à FGVTN, após autorização de Elias.** [Registro](Envios_fabricantes_R41.md). Não inclui planta do apartamento, endereço ou dados pessoais.

No FreeCAD: `FerragemForteCestoR41` registra a triagem e `EsforcosCestoR41` os cálculos. [Dados](Esforcos_cesto_8kg_R41.json) · [Conferência do arquivo atual](Conferencia_atual_R41.json). Mesmo arquivoR41, semR42;1239formas originais mais2alternativas de estudo foram preservadas nesta atualização, sem erro de objeto e com controles emzero.
