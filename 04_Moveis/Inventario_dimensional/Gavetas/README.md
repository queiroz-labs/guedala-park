# Gavetas — conferência vigente P01/P06

T05, 26/10/2026. Sete gavetas conferidas na base persistida R52 contra a [instrução FGVTN arquivada](../../Avanco_pendencias/Ferragens/FGVTN_Oculta_ET_montagem_Set24.png), linha **500 mm**. [Dados por gaveta e hashes](Conferencia_P01_P06.json). Auditoria dimensional inicial sem abrir CAD; nesta continuação, R52 aberta somente para leitura dos sólidos G2, sem salvar. Nenhum ensaio físico. Relatórios antigos de carga/alternativas nesta pasta permanecem evidências históricas, não aprovação da montagem.

## Resultado dimensional

| Grandeza | P01: quatro gavetas | P06: três gavetas |
|---|---:|---:|
| Vão interno A do móvel | 355 mm | 583 mm |
| Profundidade interna do móvel | 550 mm | 572 mm |
| Margem sobre P1 mínimo 520 | 30 mm | 52 mm |
| Profundidade das laterais salvas | 490 mm | 490 mm |
| Profundidade P na linha FGVTN 500 | 500 mm | 500 mm |
| Largura interna entre laterais salva | 313 mm | 541 mm |
| Nominal do desenho A−41 | 314 mm | 542 mm |
| Intervalo do desenho +1/−0,5 | 313,5–315 mm | 541,5–543 mm |
| Espessura das laterais | 15 mm | 15 mm |
| Folga atual até fundo do móvel | 52 mm | 84 mm |

**Há espaço em profundidade, mas a caixa salva não corresponde integralmente à receita FGVTN 500:** faltam 10 mm na profundidade e a largura interna fica 0,5 mm abaixo do limite inferior transcrito. As laterais 15 mm estão abaixo do máximo 16 do desenho; isso não encerra a geometria vertical.

## Proposta dimensional FGVTN 500 — não aplicada

Proposta preparada em 26/10/2026 a pedido de Elias nesta conversa: “preparando a proposta de correção sem alterar o FreeCAD por enquanto”. [Mapa das 42 peças em CSV](Pecas_proposta_FGVTN_500.csv) e [coordenadas, verificações e exceções](Proposta_FGVTN_500.json). São envelopes globais **X mínimo/Y mínimo/Z mínimo/X máximo/Y máximo/Z máximo**, em mm; não são lista de corte nem geometria de usinagem. A auditoria acima continua descrevendo a R52 intacta.

| Resultado proposto | P01 (4 caixas) | P06 (3 caixas) |
|---|---:|---:|
| Largura externa | 344 mm | 572 mm |
| Largura interna nominal | 314 mm | 542 mm |
| Profundidade das laterais | 500 mm | 500 mm |
| Folga lateral simétrica até carcaça | 5,5 mm por lado | 5,5 mm por lado |
| Folga traseira até fundo do móvel | 42 mm | 74 mm |
| Comprimento entre frente interna e traseira | 469 mm (antes 459) | 469 mm (antes 459) |

A largura interna proposta coincide com A−41 e deixa 0,5 mm até o limite inferior e 1 mm até o superior do desenho. Essas são margens da receita, não tolerâncias de fabricação já distribuídas. Medidas acabadas, espessuras e esquadro ainda precisam compor a cadeia real.

| Peça por caixa | Correção proposta no sistema global |
|---|---|
| Lateral em X maior | Deslocar +0,5 mm em X; alongar 10 mm só para trás (+Y); manter espessura 15 e altura |
| Lateral em X menor | Deslocar −0,5 mm em X; mesmo alongamento de 10 mm |
| Fundo | Ampliar 0,5 mm em cada borda X e 10 mm na borda traseira; manter Z |
| Traseira | Ampliar 1 mm total em X e deslocar 10 mm para trás; manter espessura e Z |
| Frente interna | Ampliar 1 mm total em X; manter Y/Z |
| Frente decorativa | Preservar forma, posição e dimensões |

São **35 envelopes a corrigir e sete frentes preservadas**. Mantêm-se centro da caixa, altura e frente; o espaço entre paredes cresce 1 mm na largura e 10 mm na profundidade. O fundo permanece 12 mm acima da borda inferior das laterais e penetra nominalmente 5 mm de cada lado, inferido pelos envelopes. Preservar esse encaixe exige reconstruir/conferir os rasgos e suas terminações: alongar o envelope não demonstra a usinagem. Furos e recortes existentes não entram automaticamente na proposta.

### Fundo e bandejas G2 — sólidos conferidos

A [conferência de sólidos](Conferencia_solidos_G2.json), feita em leitura na R52 de mesmo SHA256, esclarece a diferença do fundo `MontagemG2R019`: `BoundBox` comum indica Z613–629,196, mas `optimalBoundingBox()` e os vértices indicam **Z613–628**, dentro da tolerância numérica de aproximadamente 10⁻⁷ mm. Portanto, os **1,196 mm são excesso do envelope padrão**, não espessura adicional demonstrada. O fundo tem extensão vertical geométrica de 15 mm. Não baixar bandejas, rebaixar fundo nem remover material para eliminar esse encontro de envelopes.

| Conferência na geometria atual | Resultado |
|---|---|
| Fundo G2 | Um sólido válido, dez faces; topo geométrico Z628 |
| Fundo × cada bandeja | Distância mínima 0; volume de interseção 0; nenhum sólido comum positivo |
| Bandeja longa × bandeja larga | Distância mínima 5 mm; volume de interseção 0 |
| Conjuntos com conteúdo representado | Longo Z628–728; largo Z628–729; não confundir com altura da bandeja vazia |
| Folgas horizontais na proposta | Frente 2 mm preservada; trás 2→12 mm; até laterais aumenta 0,5 mm |

Os grupos incluem **dez peças de bandeja e nove envelopes de utensílios**. Cada bandeja vazia tem fundo de 4 mm (Z628–632) e paredes até Z667: altura total 39 mm, comprimentos 455 e larguras externas 200/312. Os máximos Z728/Z729 vêm da peneira/frigideira representadas. O próprio atributo `Status` da R52 trata paredes/fundo 4 como hipótese e mantém pega, rigidez e materiais pendentes. A conferência não transforma esses envelopes de conteúdo em produtos reais medidos.

A distância zero e a ausência de volume comum são coerentes com assentamento no plano Z628, mas **não medem área de apoio efetiva nem resistência**: a operação `common()` devolveu área zero nesses pares. A ressalva C0 da representação importada permanece conforme a [análise do modelo](../../../02_Modelo_3D/README.md#triagem-das-formas-inválidas--25102026); `isValid()` não substitui análise BOP. Não escalar a peça importada inteira. O fundo alongado/alargado continua uma proposta de envelope, sem sólidos corrigidos ou usinagem demonstrados.

Reproduzir a inspeção com `FreeCADCmd.exe ferramentas/conferir_solidos_g2.py`, seguido de `python -B ferramentas/verificar_modelo/verificar_modelo.py --completo`, conforme AGENTS.md. O script abre, copia as formas para cálculo e fecha sem salvar; confere o hash antes/depois. A base de verificação não é regravada. Verificação completa desta etapa: **OK**, 5.832 objetos, 1.133 formas ativas e 106 cenários de movimento; hash R52 preservado. Isso confere a geometria atual, não a proposta ainda não aplicada.

### Sequência antes de aplicar no CAD

1. Confirmar variante comercial FGVTN 500 e engates esquerdo/direito, desenhos completos, fixadores e acesso simultâneo ao destrave. As cotas D224/E64 não definem sozinhas todos os furos.
2. Resolver corte vertical e datums do conjunto, rasgos, recortes traseiros e furos; preservar o topo G2 em Z628 e conferir usinagem/apoio das bandejas na geometria proposta. Manter a largura nominal proposta no centro do intervalo documental.
3. Conferir ajuste vertical +3, frentes vizinhas, corpos reais, abertura/retirada e acesso às mãos. As folgas desta tabela valem para a caixa fechada, sem ferragens novas; não comprovam percurso.
4. Apresentar a solução de montagem para decisão sobre aplicação. Somente após pedido de alteração do modelo, editar os parâmetros/peças e executar a verificação completa, sem alterar a base para ocultar falhas.

Reproduzir a proposta: `python -B ferramentas/propor_caixas_fgvtn.py`. O script confere hashes do CAD, base e desenho contra a auditoria, relações entre as 42 peças, frentes e Z preservados e folgas horizontais das bandejas. Não abre o FreeCAD, não calcula capacidade nem valida colisões de sólidos.

Os 14 objetos de engate nas sete gavetas ainda trazem referência **T51.7601**. São evidência da representação existente, não configuração FGVTN demonstrada. Não usar os corpos nem os furos dessa referência como gabarito da FGVTN.

## Engates FGVTN — identificação e consulta preparada

Pesquisa de 26/10/2026. O código da corrediça **54FGOC12500TSX0** corresponde à Oculta Slowmotion ET 500 na [folha oficial da família](https://www.fgvtn.com.br/site/novopdf/Corredica_FGVTN_Oculta_Slow_ET.pdf). O [guia de produtos 2024](https://www.fgvtn.com.br/site/novopdf/Guia_de_Produtos_2024.pdf) também relaciona esse código à medida 500. A instrução Set24 arquivada mostra engates convencionais esquerdo/direito, ajuste +3 e destrave simultâneo, mas não fornece um desenho completo de fixação/envelope com códigos individuais dos engates.

| Opção identificada | Evidência e limite |
|---|---|
| Engates convencionais do kit 54FGOC12500TSX0 | Referência de montagem mantida; código individual, revisão, envelope, furos e parafusos ainda não identificados nas fontes consultadas |
| Gatilho 3D **54TNOC12GAT3D** | Código próprio FGVTN na [folha Set23](https://www.fgvtn.com.br/site/novopdf/Gatilho_3D_para_Corredica_Oculta_Set23.pdf), vendido como conjunto/par; ajuste em três direções. É alternativa a confirmar, não substituição adotada |
| UniHide | A [página atual do gatilho](https://www.fgvtn.com.br/produto/gatilho-3d-para-corredica-oculta-et) menciona especificamente UniHide, enquanto a folha Set23 descreve Oculta ET de forma geral. Essa diferença impede afirmar intercambiabilidade com o kit selecionado sem confirmação |
| T51.7601 representados | Não são engates FGVTN; seus corpos, furos e envelopes não serão reutilizados como receita |

Não foi localizado gabarito cotado completo do engate convencional. O opcional 3D também não resolve por si só essa lacuna. Na busca, Firecrawl retornou HTTP402 e páginas/PDFs oficiais falharam na abertura direta; os conteúdos oficiais indexados foram consultados pelo buscador. O desenho de instalação foi conferido na imagem local Set24, sem inferir medidas pela escala das ilustrações. Há divergência na coluna H: Set24 local traz traço para 500, enquanto a tabela oficial antiga indexada traz 96. Confirmar revisão aplicável antes de prescrever furação; não combinar tabelas.

**Consulta técnica pronta, não enviada — sete pares de 500, quatro P01 e três P06:**

1. Confirmar que o kit fornecido é **54FGOC12500TSX0**, Oculta Slowmotion ET 500, e identificar códigos/revisão dos engates convencionais esquerdo/direito. Se a família foi substituída, informar código e alterações de montagem, sem presumir equivalência UniHide.
2. Fornecer desenho cotado ou gabarito dos engates: posição em relação à face interna da frente e às laterais, furos, diâmetros, tipo/comprimento de parafusos e exigências de painel. Caixas propostas: externas 344/572 ×500; internas 314/542; laterais e fundo 15, frente interna 16; face inferior do fundo 12 acima da borda inferior das laterais.
3. Informar envelope do engate/guia sob o fundo e espaço para destrave simultâneo, retirada e remontagem. Confirmar o datum do ajuste +3 e as reservas necessárias em toda a faixa.
4. Confirmar recortes e furos traseiros (Ø7 e cotas 7/11/33 do desenho), profundidades e faces de referência, além da furação da guia para **500**. Esclarecer a diferença da coluna H entre a folha antiga e Set24; D224/E64 sozinhos não constituem gabarito.
5. Se o convencional não estiver disponível, confirmar explicitamente se **54TNOC12GAT3D** funciona com **54FGOC12500TSX0**, quais adaptações exige e fornecer seu gabarito. Não aceitar apenas “serve em corrediça oculta”.

O pedido atual não inclui envio de correspondência, compra nem mudança de ferragem. Desenho e compatibilidade continuam pendentes de resposta ou documentação técnica equivalente.

## Ajuste vertical e retirada — conferência independente

[132 casos / 1.078.560 pares de envelopes](Ajuste_vertical_e_retirada.md), sem abrir CAD: frente solidária em +3 encontra a prateleira nas duas superiores P01 (sobreposição 1 mm) e zera a folga da superior P06 até a bancada. Frente realinhada na altura nominal evita esses encontros no conjunto testado, mas exige fixação a detalhar. Na caixa500, C475 ainda deixa 33/23 mm dentro da carcaça P01/P06; retirada reta hipotética testada até509/499, com porta P01 correspondente deslocada600. Ferragens, mãos e levantamento excluídos. **Melhor momento para integrar no CAD:** após fechar engate/gabarito, datum, compensação da frente e desengate/retirada; recomendação detalhada no estudo.

## Fixação das frentes — proposta independente

[28 pontos e validação parcial](Fixacao_frentes.md): seção11 dos dois alojamentos G2 sem resistência demonstrada; 512 combinações preservadas. Candidato concreto: RECA01814 25 + Ettinger003.06.941 (4,3×15×1); tolerâncias/encaixe pela rosca ainda pendentes. Dianteira interna16 não individualizada na lista P06 nem por SKU; BrancoTX é intenção de acabamento. Decorativa18 Arenza rastreada. Seis comparações15/16/18:18 zera vão das bandejas,15 deixa seção10 com rebaixo5. Não substituir chapa automaticamente. Produto, material, aperto e ensaio pendentes; CAD intacto.

## Curso, engates e manutenção

O desenho arquivado distingue **P=500**, **P1 mínimo=520** e **C=475 ±3 mm**. Logo, 500 mm de comprimento nominal não equivale a curso 500. Antes de integrar a ferragem, reconciliar os controladores com C e confirmar a variante efetiva; não alterar controles somente para fazer esta tabela coincidir.

A instrução exige **destrave simultâneo dos dois lados** para retirar a gaveta. O próximo desenho deve reservar acesso sob os dois cantos frontais com a gaveta aberta e apoiada, sem exigir retirar previamente uma frente ou peça que bloqueie o próprio destrave. O volume real das mãos, a ferramenta, a sequência de desengate e eventual levantamento não foram obtidos dessa imagem; não inventar uma altura de retirada.

| Interface pendente | Próximo trabalho verificável |
|---|---|
| Caixa 500 e largura A−41 | Mapa dimensional das 42 peças preparado acima; resolver usinagem; excesso do envelope G2 esclarecido, sem correção vertical indicada |
| Engates FGVTN | Consulta específica acima; confirmar convencional do kit 54FGOC12500TSX0 ou compatibilidade explícita do opcional 54TNOC12GAT3D |
| Vertical/recortes | Conferir os datums das cotas 38 mínimo, 27, 12, 11 e 7 do desenho em um corte da montagem correta; não importar as cotas MOVENTO do P16 |
| Ajuste +3 mm | Triagem feita no estudo acima; resolver fixação/realinhamento da frente e regulagem desigual dos engates |
| Furação | Usar a linha 500 e a face de referência do desenho; D=224/E=64 não são a receita da variante 400. Piloto/parafuso dependem do painel/produto |
| Retirada | Representar engates reais e acessos simultâneos; depois conferir percurso completo, apoio e remontagem |

As sete faces laterais e planos de fundo usados no levantamento antigo foram reconferidos numericamente na base atual. Não se repetiu o ensaio de raios nem se tratou a caixa envolvente como inspeção de furos. Capacidade, rigidez, fabricação e compatibilidade de ferragem continuam pendentes.

Reproduzir na raiz: `python -B ferramentas/conferir_gavetas_p01_p06.py`. Usa somente a biblioteca padrão, confere hash R52 e as faces de referência; gera os dados sem abrir CAD.
