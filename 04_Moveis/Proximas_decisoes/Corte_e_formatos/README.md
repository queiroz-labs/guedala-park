# Corte guilhotinado nominal para cotação — R54 / fichas R15

## Resultado corrente — 28/10/2026

**216 dos 249 painéis calculados; 33 ainda excluídos.** P13/Peca350 entrou no grupo Arenza 18: F13=A, Elias, 27/10/2026, conforme ficha e auditoria. A área e os IDs das fichas atuais são lidos novamente, sem alterar madeira, ferragens, orçamento ou FreeCAD. Os 36 componentes de alternativas continuam separados: não foram adotados nem somados.

**Melhor conjunto encontrado: 14 chapas**, escolhendo 2750×2100 para Branco TX 18 e Azul Petróleo 18, e 2750×1850 para os demais grupos. São 8 pequenas + 6 grandes para o subconjunto de 216 painéis, sem os 33 bloqueados. Usar só 2750×2100 também encontrou 14 chapas. Não é compra completa: formatos, produtos, estoque, substratos e processo precisam constar da cotação.

Arenza 18: **3 chapas 2750×1850, aproveitamento útil 70,71%**, incluindo P13. Branco TX 18: **5 chapas 2750×2100, 94,56%**. O fundo P01/Peca208 não cabe em 2750×1850; não foi adotada emenda nem escondida essa impossibilidade. Azul Petróleo 18: 1 chapa grande versus 2 pequenas no melhor arranjo encontrado.

## Chapas por padrão, espessura e formato

Aproveitamento usa a área útil após refilo; o [CSV](Chapas_cotacao.csv) traz também percentual sobre área bruta. LI = teto da soma das áreas dos envelopes / área útil de uma chapa. Lacuna = chapas encontradas menos LI. Uma lacuna positiva não prova que a solução possa alcançar o LI. A heurística não demonstra ótimo global; coincidência com LI demonstra o número mínimo apenas no grupo e hipóteses modelados, sem validar produto ou corte real.

| Padrão / mm | Formato | Peças | Chapas encontradas | LI | Lacuna | Uso útil | Sobras >300×300: qtd / m² |
|---|---|---:|---:|---:|---:|---:|---:|
| Arenza / 18 | 2750x1850 | 39 | 3 | 3 | 0 | 70.71% | 7 / 3.5766 |
| Arenza / 18 | 2750x2100 | 39 | 3 | 2 | 1 | 62.21% | 7 / 5.7288 |
| Azul Petroleo / 18 | 2750x1850 | 20 | 2 | 1 | 1 | 44.63% | 7 / 5.0637 |
| Azul Petroleo / 18 | 2750x2100 | 20 | 1 | 1 | 0 | 78.53% | 5 / 0.7239 |
| Beige Matt / 18 | 2750x1850 | 2 | 1 | 1 | 0 | 5.84% | 2 / 4.6948 |
| Beige Matt / 18 | 2750x2100 | 2 | 1 | 1 | 0 | 5.14% | 2 / 5.3765 |
| Branco TX / 15 | 2750x1850 | 35 | 1 | 1 | 0 | 55.13% | 2 / 2.0321 |
| Branco TX / 15 | 2750x2100 | 35 | 1 | 1 | 0 | 48.50% | 2 / 2.7258 |
| Branco TX / 16 | 2750x1850 | 8 | 1 | 1 | 0 | 6.00% | 2 / 4.5878 |
| Branco TX / 16 | 2750x2100 | 8 | 1 | 1 | 0 | 5.28% | 2 / 5.2695 |
| Branco TX / 18 | 2750x1850 | 100 | 5 | 5 | 0 | 90.99% | 1 / 0.8263 |
| Branco TX / 18 | 2750x2100 | 101 | 5 | 5 | 0 | 94.56% | 0 / 0.0000 |
| Louro Freijo Poro / 18 | 2750x1850 | 4 | 1 | 1 | 0 | 12.51% | 2 / 4.2687 |
| Louro Freijo Poro / 18 | 2750x2100 | 4 | 1 | 1 | 0 | 11.01% | 2 / 4.9504 |
| Off-white fosco / 18 | 2750x1850 | 7 | 1 | 1 | 0 | 41.29% | 5 / 2.9002 |
| Off-white fosco / 18 | 2750x2100 | 7 | 1 | 1 | 0 | 36.33% | 4 / 3.5251 |

**Branco TX 18 / 1850 é somente um subconjunto de 100 peças:** as 5 chapas e LI=5 não incluem Peca208. O grupo integral é inviável nesse formato. No conjunto misto, a soma dos LI dos oito grupos é 14, igual ao número encontrado, para estas dimensões e estes formatos escolhidos por grupo. Isso não prova mínimo de área comprada/custo nem ótimo sobre misturas de formatos dentro de cada grupo.

## Parâmetros e direção

- [Parametros.json](Parametros.json): serra 3,2 mm; refilo 10 mm em **cada borda**; janela útil 2730×1830 ou 2730×2080; sobremetal zero. Seu campo histórico R52 não substitui as fichas R15 lidas neste cálculo.
- **Arenza e Louro Freijó Poro:** maior dimensão do envelope paralela ao lado 2750, sem rotação. É hipótese conservadora do pedido de cálculo de 28/10/2026, não decisão de acabamento. O Arenza continua descrito como **liso** nas decisões; não se afirmou que tenha veio impresso. A ficha não contém exceção por ID; montagem/aparência e sentido real precisam de confirmação do fornecedor.
- **Branco TX, Azul Petróleo, Beige Matt e Off-white:** podem girar 90°. Um único padrão nas duas faces de cada chapa física; não há caixa interna 15 adicionada automaticamente.
- Padrões e espessuras não se misturam na chapa. 16 mm continua referência nominal, sem SKU presumido. O formato grande não foi tomado como oferta disponível de todos os padrões.
- Os recortes especiais ocupam o retângulo envolvente completo. Sem encaixar vazios, furos ou contornos uns nos outros. Os cortes registrados dividem recursivamente cada retângulo livre em guilhotina; a sequência depende da seccionadora real.
- As cotas são **envelopes nominais**, não dimensões finais sem fita. [Fita por peça](../../Furacao/Fita_por_peca.csv) traz proposta 1/0,45 mm e 23 IDs sem regra suficiente. Não foi descontada fita, inventado sobremetal ou decidido perfil de acabamento. Fornecedor deve confirmar blanks finais antes de transformar a estimativa em programa de corte.

## Peças ainda fora do cálculo

Não se interpreta código/amostra pendente como decisão estética nova. Os 17 painéis Arenza 18 ainda classificados **referência** nas fichas permanecem separados do grupo com especificação escolhida; sua inclusão exige confirmar que compartilham efetivamente o produto de cotação. Peças de composição/espessura especial não viram chapa comercial pela espessura do envelope. Os dois substratos com espelho continuam condicionados à composição.

| IDs | Motivo exato para não incluir |
|---|---|
| P01/Peca206, P01/Peca207, P01/Peca247, P01/Peca248, P02/PlacaL, P02/PlacaL001, P02/FrenteSimplesR04, P02/FrenteSimplesR001, P02/FaixaQuinaAR04, P02/FaixaQuinaBR04, P04/Peca266, P04/Peca267, P04/Peca269, P04/FrenteComumR015, P04/FrenteComumR016, P04/FrenteComumR017, P04/FrenteVizinhaR18 | Arenza ainda registrado como referência, sem produto individualizado como escolhido na ficha. |
| P04/FaixaFixaEstudo, P06/MontagemG2R019, P07/Peca307, P20/BancoR43_Painel1, P20/BancoR43_Painel2 | Espessura de envelope sem composição de chapa definida; não foi convertida para espessura comercial. |
| P08/PecaBaixaR036, P08/PecaBaixaR037, P16/Peca367, P16/Peca368, P18/BC43_LateralE, P18/BC43_LateralD, P18/BC43_Base, P18/BC43_Travessa, P19/Peca403 | Acabamento/composição ainda parcial na ficha; falta definir o padrão único da peça. |
| P19/FrenteComumR019, P19/FrenteComumR020 | Espelho separado: composição do substrato não formalizada. |

**Perguntas que destravam a lista completa:** os 17 IDs Arenza 18 referenciais podem entrar no mesmo produto do grupo Arenza escolhido? Qual padrão único vale para reservas P08, laterais P16, quadro P18, base P19 e tampas P20? Qual composição real corresponde aos envelopes 7 / 16,2 / 20 / 30 mm e aos substratos com espelho? Ao fornecedor: quais dos formatos/padrões/espessuras existem, qual direção é exigida e quais dimensões de blank/fita serão usadas? Não se pede aqui revisão de carga, ancoragem, micro-ondas ou rodízios.

## Comparação com orçamento R44

A [R44, seção T07](../../../05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md#t07--marcenaria-provisão-e-escopo-de-cotação) menciona **16 chapas virtuais / 215 painéis / 34 excluídos**, sem composição comercial definitiva. Este ensaio passa a **14 / 216 / 33**, com direção restrita nos padrões indicados e guilhotina explícita. A inclusão de P13 não reduz material: a diferença resulta da heurística e da escolha dos formatos. Não equivale a desconto de duas chapas no orçamento, porque formato, SKU, preço, refugo e escopo não são iguais. Provisão de materiais R$ 20.800 e orçamento permanecem intactos.

## Reprodução, conferência e arquivos externos

```powershell
python -B ferramentas/estudos/test_corte_guilhotina.py
python -B ferramentas/estudos/corte_guilhotina.py --saida ../outputs/Corte_cotacao
```

Executar da raiz do repositório. Biblioteca padrão Python; 48 heurísticas determinísticas por grupo/formato. Critério: menor número de chapas, depois maior área de sobras retangulares com **ambas** as dimensões estritamente maiores que 300 mm. Sobras são folhas disjuntas da árvore de cortes, não retângulos livres sobrepostos nem material com reutilização comercial garantida.

Saída externa `../outputs/Corte_cotacao/`: `Chapas.csv`, `Planos.json` e um SVG por chapa/cenário. JSON contém árvore ordenada de cortes, posições, sobras, IDs excluídos, hipóteses e SHA256 de cada ficha, auditoria, fita, parâmetros e script. Somente o CSV sintético permanece no git; nenhuma saída extensa nova entra no site.

SHA256 de `Planos.json`: `f3850114e18ea0e52ab0ced3071cf0f303218e2bdc3ae77150784bdffc39a72d`.

Cinco testes cobrem perda de serra, orientação proibida, formato inviável, margem e corrupção deliberada de corte/posicionamento. Todos os planos passam por reprodução da árvore, correspondência entre corte e peça, margens, IDs únicos e distância entre envelopes de pelo menos 3,2 mm. Fonte FreeCAD não foi aberta nem alterada; fichas e acabamento preservados.

## Referências anteriores preservadas

[Arranjos anteriores](Planos_preliminares.json), [SVGs anteriores](Planos_svg/G05_chapa_01.svg), [exclusões anteriores](Peças_sem_definicao_suficiente.csv), [reconciliação](Reconciliacao_acabamentos.json) e [verificação anterior](Verificacao.json) são a memória do ensaio de 16 chapas com rotação; não são a lista corrente de cotação desta frente. Mantidos por serem referências existentes; não somar seus quantitativos ao novo CSV. [36 propostas separadas](Propostas_36.csv), [requisitos do fundo inteiro P01](Requisito_fundo_P01.csv) e [triagem de formatos](Triagem_formatos.json) permanecem consultas, sem adoção automática.
