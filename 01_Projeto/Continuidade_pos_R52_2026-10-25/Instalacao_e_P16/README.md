# Instalação ME23P e limite da conferência P16

25/10/2026. R52 e decisões preservadas. Esta frente separa requisito confirmado, solução nominal de estudo e dado que ainda falta do produto/oficina.

## Micro-ondas: alternativa nominal produzida, sem reverter F104

O [manual oficial ME23P, página3](https://api.electrolux-medialibrary.com/asset/75f3884e-b240-4cbe-9654-cc3e4b124111/E4RM3Q/1f040fd7-0be8-4b35-a635-d2ee154a4f54/ORIGINAL/1f040fd7-0be8-4b35-a635-d2ee154a4f54.pdf) foi reaberto nesta data: exige300mm acima e100mm laterais/traseiros. A exceção indicada nessa página refere-se a ME3BC/ME3BP, não ao ME23P. A escolha F104 por100mm superiores continua no modelo principal; isso não atende ao requisito documental. O corpo461×352×290 também coincide com a [página técnica oficial](https://content.electrolux.com.br/brasil/electrolux/clara/me23p/pagina.html).

Foi criado um **[FreeCAD de estudo separado — não adotado](ME23P_folga300_ESTUDO_NAO_ADOTADO.FCStd)** com as formas existentes, movendo prateleiraPeca350 e aparelhoPeca351200mm para baixo. GabineteB e demais elementos não mudam. O resultado é geométrico:

| Grandeza | R52/F104 preservada | Hipótese separada |
|---|---:|---:|
| Apoio: face superior |1550mm|1350mm|
| Aparelho: topo |1840mm|1640mm|
| AéreoB: face inferior |1940mm|1940mm|
| Espaço acima do aparelho |100mm|300mm|
| Espaço entre bancada920 e face inferior da prateleira |612mm|412mm|

As caixas das duas peças propostas ficaram separadas das caixas dos1.131 sólidos fixos ativos considerados. Isso exclui a interpenetração volumétrica nessas posições para esse conjunto; não houve necessidade de booleana em pares com caixas sobrepostas. O arquivo de39 objetos foi salvo e reaberto; os grupos atuais de comparação ficam ocultos e a proposta é rotulada como não adotada. [Dados e verificação](Micro_estudo.json) · [script](estudar_micro.py).

**O que falta:** aceitar ou rejeitar a mudança de altura, detalhar apoio/fixação, acesso e ergonomia, conferir instalação real e tolerâncias. O estudo entrega exatamente o mínimo300mm, sem margem vertical adicional. Ele reduz a altura livre sobre a bancada em200mm; preservar o volume do aéreo não significa preservar todas as condições de uso. Não se concluiu desempenho térmico por ausência de colisão e não se mudou automaticamente a preferência de Elias.

## P16: o que pode e o que não pode ser encerrado documentalmente

A [orientação oficial brasileira de montagem MOVENTO](https://www.blum.com/br/pt/products/runnersystems/movento/assembly/) confirma ajuste em altura, inclinação, lateral e profundidade. Ela não publica nessa página tolerância permissível de comum BREP, nem identifica o datum/regulagem neutra do STEP usado no projeto. Por isso não foi aplicada uma translação de0,175mm nem retirado material para “corrigir” o desenho.

Os [18 componentes já localizados](../../P16_interface_guia_fundo_2026-10-25/README.md), o furoØ6×10/eixo11 e a repetição do padrão no conjunto configuradoG2 continuam evidências disponíveis. G2 é uma configuraçãoNL500; não constitui configuração individualNL400 homologada paraP16. O documento americano de ajustes não foi usado para transferir medidas regionais ou autorizar tolerâncias na variante brasileira.

**Pendência específica, independente das medidas do imóvel:** confirmar configuração400, referência dos engates, posições neutras do STEP, fixação da guia e tolerâncias, por desenho/configurador aplicável ou montagem piloto. A pergunta pronta existente continua válida. Nenhum fabricante foi contatado nesta etapa e nenhum ensaio físico foi apresentado como realizado.

## Rastreabilidade

R52 preservada: SHA256`941da02d367c5f6ce2992f72985f86c3aceba23f899a4c394cf3569f19d7b4da`. A cópia local do manual de instalação permanece em `02_Plantas_e_manuais/Manuais/Electrolux_ME23P_Manual.pdf`; foi lida como fonte, sem edição. O estudo do micro tem hash próprio emMicro_estudo.json.

A tentativa de pesquisa Firecrawl não executou por falta de créditos; a consulta oficial prosseguiu pela busca padrão. O catálogo amplo MOVENTO e uma instrução regional americana não puderam ser recuperados integralmente nessa via. Não foram tratados como documentos lidos nem como prova de configuração400.
