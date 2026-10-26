# Ligações e suspensão dos aéreos

## Vigente: lote A — P09/P11/P15

25/10/2026. Estudo conforme [AGENTS](../../AGENTS.md), sem tubos ou alteração daR52/acabamentos. **Mapa e solicitações nominais; juntas/produto condicionados.**

**Pré-seleção25/10:** preferência de Elias por preservar espaço interno, nesta conversa. **Bigfer04.02.058** candidata, sem montagem/carga demonstradas. [Dados e requisitos](Selecao_ferragem.json) · [desenho](Selecao_ferragem.png). Cotas de trabalho corrigidas: assento40,5 e furo pequeno9,5; entrada32 não é assento. A montagem espelhada exige revisão, descrita abaixo.

| Caixa/variante | Interfaces nominais estudadas; não são compras adicionais |
|---|---|
| P09 atual | 20 Confirmat7×50 candidatos e11 cavilhas8×30 apenas de posicionamento. Divisor ligado à base/topo em dois pontos por extremidade e ao fundo em dois pontos |
| P11 atual | Preservar12 Minifix existentes.10 Confirmat candidatos: quatro prateleira–fundo e seis fundo–laterais; três cavilhas posicionam a prateleira |
| P15 atual | Preservar8 Minifix existentes; seis Confirmat candidatos fundo–laterais |
| P15 estudo18+18 | Mesmos8 Minifix;18 Confirmat candidatos: seis base–fundo, seis topo–fundo e seis fundo–laterais. Não especifica a composição entre camadas |

Os96 pontos incluem alternativas mutuamente exclusivas de P15. São eixos nas interfaces, **não centros completos de canecos, pilotos ou programa CNC**. A conferência independente coloca todos em faces de contato positivo. Nos três corpos atuais, base/topo encontram o fundo somente pela aresta: seis encontros sem face útil, excluídos das ligações traseiras. Diâmetros, pilotos, distâncias mínimas, embutimento das cabeças e montagem dependem da ferragem/chapa e ensaio. As cabeças traseiras precisam ser compatíveis com a face encostada à parede.

**P15:** a variante desce a lateral18 mm e mantém o eixo da base original emZ9. O pino passa de9 para **27 mm da nova borda inferior**. Não reutilizar o gabarito inferior9 nessa lateral. A camada adicional é outra peça; acabamento nas duas faces de cada chapa conforme a regra do projeto. O [processo de composição](../P15/Composicao_parcial/README.md) continua sem produto demonstrado; não presumir colagem entre facesBP nem capacidade pela simples soma18+18. TitebondMelamine permanece excluída.

### Implantação e demandas da fixação direta

Estudadas duas zonas superiores e duas inferiores acessíveis pela frente, mantendo a profundidade330 e o fundo18 na traseira. Reservas internas36×36×8 e corredor reto de ferramentaØ20 foram conferidos **somente contra a madeira**, em12 zonas. Não representam ferragem comercial ou acesso real de ferramenta/mão; não são quatro ancoragens dimensionadas.

Origem: u na esquerda interna, v na face traseira da caixa para a frente, z na base externa original. P09:u72/542,z90/502; P11:u72/589,z90/520; P15:u72/727,z90/490. O binário usa separação verticalh412/430/400, respectivamente. Todo cortante foi atribuído aos dois grupos superiores, conforme o CG lateral; tração repartida0/100,50/50 ou100/0, equilibrada por compressão inferior. Caixa, apoios e produto precisam efetivamente realizar essa partilha.

696 casos geométricos recompostos com CG das portas do snapshotR52; três partilhas e dois grupos geram4176 vetores. Volumes/CG dos corpos reconciliados com a extraçãoR51 e dimensões das fichas atuais. Reserva hipotética de1kg de ferragens fixas, sem substituir pesagem ou distribuição real dos braços móveis. Vetores críticos abaixo pertencem ao mesmo grupo/caso, comρ900, portas86° e conteúdo excêntrico; **demandas sem majoração, impacto ou capacidade física**:

| Variante/conteúdo total hipotético | V por grupo (N) | T por grupo (N) | Resultante (N) |
|---|---:|---:|---:|
| P09 atual /10kg | 246,12 | 214,72 | 326,62 |
| P11 atual /10kg | 257,18 | 219,99 | 338,44 |
| P15 atual /20kg | 355,38 | 320,48 | 478,55 |
| P15 estudo /20kg | 379,96 | 338,94 | 509,17 |

P09 exclui o depurador; P11 não recebe10kg em cada nível. Os demais cenários e casos controladores estão no CSV. Equilíbrio conferido independentemente nos2088 pares de grupos; isso não demonstra rigidez/resistência da caixa ou fixação ao MDF.

### Produto: duas rotas para resolver

1. **Prioritária — fixação direta compacta:** candidata [Bigfer04.02.058](https://www.bigfer.com.br/suporte-aereo-l-armarios/), SKU0402058411, aço1,5. O [catálogo p235](../../09_Referencias/Plantas_e_manuais/Manuais/Ferragens_suspensao/Bigfer_suportes_aereos.pdf) cota braços49,5/37,8 e tira16. Proposta nossa nos dois planos verticais do canto: dois envelopes ocupam59,88mL, sem capa/cabeça/acesso; fundo18 permanece na posição e profundidade312 preservada. Catálogo sem capacidade e sem instrução que confirme esta montagem: **preferida para qualificação, não produto fechado**. O parafuso à parede atravessaria o fundo18; excentricidade local, chapa/parafusosMDF, retenção e apoios inferiores precisam ser demonstrados. Quantidade de dois suportes é hipótese, não suficiência comprovada.
2. **Suspensor atrás do fundo:** alternativa separada com reserva16 dentro da profundidade330. Deslocar o fundo16 para a frente e reduzir peças horizontais/divisor de312 para296 custa aproximadamente5,30L noP09,5,88L noP11 e6,95L noP15 atual. Não fazer rasgo16 numa chapa18. Muda armazenamento, juntas e cálculos; não foi incorporada. Ter16 livres não prova compatibilidade do produto com fundo18.

**Implantação específicaBigfer:** u40,5/W−40,5 e centroZ H−58; compressão inferior hipotéticaZ90. Assento40,5=49,5−9; entradaØ10 em32. Pequeno furo9,5=32−22,5=1,5+8 desde o canto externo. Lateraisv30,8/42,8: validar passo12/borda9,5 no MDF; Ø5 na ferragem não é pilotoØ5 na madeira. Subir32 evita alinhamento com ConfirmatH−90; separação ao Minifix superior49. Seis envelopes/corredores sem interseção com madeira, sem conferir ferragens/ferramenta reais. Reservas36×36×8 anteriores não contêm este suporte49,5×37,8×16.

**Montagem:** dois suportes espelhados pedem translações opostas de8,5mm para passar da entrada ao assento. Encaixe simultâneo por translação única rejeitado. Proposta a confirmar: gabinete sustentado/nivelado e fixações inseridas/apertadas por dentro, retiradas também com apoio. Validar cabeça/arruela no rasgo5, fundo18, torque, retenção e apoio inferior. Não há ancoragem/parafuso escolhido.

Recalculados4176 vetores no assento40,5: V/T dos maioresR,10kgP09/P11 e20kgP15 =239,31/199,25N;251,05/204,76N;345,94/296,74N(P15atual) e370,51/313,84N(P15estudo). Os maioresV ocorrem em outros casos. [Oito casos para qualificação](Requisitos_suporte_L.csv) preservam máximosV/T/R sem combiná-los · [todos os vetores](Solicitacoes_suporte_L.csv) · [conferência](Verificacao_selecao.json). Demandas sem capacidade física. Momentos r×F são reduzidos ao canto: não somar ao equilíbrio global nem dividirV pelos três furos. Reprodução: `python -B ferramentas/aereos/selecionar_ferragem.py` e `python -B ferramentas/aereos/conferir_selecao.py`.

**Alternativas internas examinadas:** SAH130 eSAH116 mostram fundo3–5/máximo5 nas instruções, com recorte; não substituem diretamente nosso fundo18. Nelas, a cota mínima16 vai até a face frontal do fundo, diferente de reserva livre16 atrás dele. [Manuais preservados](../../09_Referencias/Plantas_e_manuais/Manuais/Ferragens_suspensao/README.md). Bigfer04.02.007/008 fica como reserva geométrica (aço1,9,42×58×20), também sem capacidade demonstrada. Camar807VP não foi escolhido: BP16 no desenho, aplicação com fundo18/oferta local sem comprovação; advertência de carga807IN não comprova a varianteVP.

HB65: página65kg/ficha60kg, unidade eV/T pendentes; exige reserva posterior16. SAH216 também exige16/fixação lateral. FGVTNfixo0091.510010:cotas8/16/22 e80kg não demonstram nossa montagem. [Fontes oficiais e manuais preservados](../../09_Referencias/Plantas_e_manuais/Manuais/Ferragens_suspensao/README.md). Não somar capacidades ou escolher o número maior.

**P09:** o espaço nominal42 entre gabarito e base não é vencido automaticamente pelo parafuso30 do manual: faltariam12 antes do embutimento. Conta condicional ao topo do gabarito simplificado; abas reais não estão modeladas, portanto não reprova o aparelho. Não escolher parafuso maior, inventar adaptador ou atribuir os6kg automaticamente ao gabinete. Preservar retorno20, filtros e afastamento de instalação.

### Próximas entregas e reprodução

Consultas prontas, não enviadas: [qualificaçãoBigfer e demais produtos](Consulta_suspensao_lote_A.txt) e [depurador](Consulta_depurador_P09.txt). Comprovar juntasMDF/composiçãoP15 por dados/ensaio e conferir ferragem/ferramentas/sequência reais. Parede/revestimento/instalações após as chaves; produto pode ser definido antes.

[Dados e hashes](Detalhamento_P09_P11_P15.json) · [mapa dos96 eixos](Mapa_ligacoes_P09_P11_P15.csv) · [4176 solicitações](Solicitacoes_fixacao_direta.csv) · [conferência independente](Verificacao_ligacoes_P09_P11_P15.json).

Mapa genérico: `python -B ferramentas/aereos/detalhar_ligacoes.py` e `python -B ferramentas/aereos/conferir_ligacoes.py` (NumPy/Pillow), sem abrirCAD. Zero ensaios físicos, compras ou furos executivos. Estudos abaixo conservam hipóteses próprias.

## Estudo global anterior — P09/P11/P12/P17

Memória25/10, T02: quatro caixas com portas abertas e conteúdo parametrizado pelo [motor de quatro barras](../../ferramentas/cinematica/README.md). R51 preservada; sem suspensor ou ancoragem adotados.

| Móvel | Base interna, largura | Profundidade da caixa | Altura | Madeira da caixa / folhas |
|---|---:|---:|---:|---|
| P09, acima do depurador | 614 mm | 330 mm | 592 mm | Seis peças / duas portas |
| P11, acima do micro | 661 mm | 330 mm | 610 mm | Seis peças, incluindo prateleira / duas portas |
| P12, acima da geladeira | 765 mm | 330 mm | 584 mm | Seis peças / duas portas |
| P17, aéreo do escritório | 1964 mm | 330 mm | 550 mm | Nove peças / quatro portas |

Volumes/CG vieram do BREP; frentes com canecos descontados. Divisor duploP17 conserva duas chapas; P09 mantém divisor312/R48, sem recolocar prateleiras canceladas.

## Hipóteses e resultados

1404 combinações de densidade650/800/900, portas independentes0/86°, estado45° e extremos amostrados do CG, com conteúdo total0/5/10/20 kg. A distribuição é central ou próxima à frente/extremidades. São **cenários totais por móvel**, não cargas por prateleira ou capacidades autorizadas. No P11, o estudo local10 kg de uma chapa continua condicionado; ele não autoriza aplicar10 kg em todos os níveis.

Massa nominal18 aproximada por18,3/fator de volume; ferragens/acabamento exigem dados reais. CG da frente não foi atribuído a todos os braços metálicos.

O plano de referência da parede é a face traseira nominal. Dois grupos de suspensão recebem a força vertical conforme o centro lateral; o vão entre resultantes varia entre100% e80% da largura da base. O binário usah50% ou80% da altura da caixa; a tração superior pode repartir-se100/0,50/50 ou0/100. Essas posições/partilhas são parâmetros de equilíbrio, sem furos ou produto definido. Não comprovam que a caixa real já transmita a torção necessária entre os lados.

`V(N)=soma(m×g)`; `M(Nm)=soma(m×g×v(mm)/1000)`; `T(N)=1000×M/h(mm)`.

Exemplos comρ900,10 kg de conteúdo próximo à frente, todas as portas86° e h80% da altura:

| Móvel | V total | M para fora da parede | h parametrizado | T superior total |
|---|---:|---:|---:|---:|
| P09, madeira+conteúdo | 367,134 N | 86,759 Nm | 473,6 mm | 183,191 N |
| P11 | 391,711 N | 92,891 Nm | 488,0 mm | 190,351 N |
| P12 | 407,031 N | 98,756 Nm | 467,2 mm | 211,378 N |
| P17 | 796,004 N | 195,594 Nm | 440,0 mm | 444,533 N |

O P09 acima **não inclui o depurador**, cuja transferência de esforços depende da ligação descrita abaixo. A massa de móveis/equipamentos inferiores, como geladeira e micro, não é somada automaticamente ao aéreo.

P17: aproximadamente81,17kg de madeira hipotética+conteúdo antes de ferragens no exemplo, sem pesagem; mudar densidade/composição exige recalcular massa e rigidez.

As48 combinaçõesh/vão/partilha preservam casos controladores deV/T/resultante. Sem combinar máximos incompatíveis, majoração, mãos, impacto, resistência/rigidez real ou ensaio. Grupo não é parafuso;kg de catálogo não validamV/T simultâneos.

## Depurador P09: dado do fabricante e interface ainda aberta

![Corte dos envelopes do depurador e gabinete](Interface_depurador_42mm.png)

O [manual SuggarDE61IX/DE62IX](../../09_Referencias/Plantas_e_manuais/Manuais/Suggar_DE61IX_DE62IX.pdf),REV.0025,p1, publica6,00kg sem embalagem para60cm (58,840N) e8,01kg para80cm. Colunas conferidas visualmente; não é pesagem da unidade entregue.

O manual indica primeiro apoio/fixação à parede e depois fixação superior ao gabinete com quatro parafusos4,2×30, figuras5–8. Portanto, **não se presumiu que o armário recebe metade ou todo o peso**. O conjunto tem vínculos redundantes; a partilha, possíveis efeitos de alavanca e a ligação real precisam de desenho/rigidez. Os fixadores citados no manual não são seleção de ancoragem aprovada para uma parede ainda desconhecida.

Há uma pendência nominal concreta: o gabarito`Peca139` termina emZ1916 e a face inferior da baseP09 começa emZ1958, deixando **42 mm entre eles no CAD**. Não há ponte de ligação ou adaptador representado nessa faixa. O gabarito é uma caixa simplificada e não contém abas ou fixações comerciais; o resultado identifica uma interface não demonstrada, sem concluir que o produto real seja inviável.

Posições/folga preservadas, sem adaptador inventado. Retorno20mm na largura, filtros e acesso continuam restriçõesR48 do modo depurador. Não reinstalar canal de duto cancelado.

O [registro do depurador](Depurador_dados_e_pendencias.json) distingue massa publicada, dados do gabarito e transferência desconhecida. Para consulta de sensibilidade do conjunto global na parede,6 kg acrescentam58,840 N e um momento que depende do CG. Emv150/300/488 mm, são8,826/17,652/28,714 Nm; essas posições são hipóteses/envelope geométrico de referência, não CG publicado ou carga atribuída a um suspensor do armário. A ligação real pode produzir outros esforços internos.

## Perguntas exatas antes de fechar

1. **P09:** obter abas/apoios/direções e forças das fixações das figuras5–8, mantendo42mm nominais, ventilação, filtros e distância ao cooktop. Adaptação depende de confirmação do fabricante.
2. **Suspensão:** comprovar desenho, h/vão, excentricidadesV/T, retenção e apoios reais. LoteA tem candidata acima; P12/P17 continuam sem produto compatibilizado.
3. **Caixa:** demonstrar juntas, torção e compressão inferior; manter P11 sem tubos e requisitos locais, incluindo fundo/divisóriasP17. Não presumir caixa rígida.
4. **Massa/uso:** definir conteúdo por nível, pesar portas/conjunto e separar partes fixas/móveis das ferragens;20kg global não significa20kg por chapa/nicho.
5. **Imóvel:** conferir substrato, espessura, revestimento e instalações antes de selecionar ancoragem; produto/união/protótipo podem avançar agora.

Nenhuma consulta foi enviada. Sem tubos ou outro quadro metálico para sustentar as chapas, sem compra, usinagem ou carga de uso liberada. Estudos/demandas preservam o modelo completo e as escolhas de armazenamento.

## Evidências e reprodução

[Geometria atual e folga42](Geometria_R51.json) · [1404 casos e48 envelopes](Resultados.json) · [depurador:fontes e pendências](Depurador_dados_e_pendencias.json) · [verificação](Verificacao.json).

Memória anterior baseada na extraçãoR51, com SHA256/CRC, fotografia de cinemática, entradas e manual rastreados; massa constante e equilíbrio conferidos. As rotinas históricas dependem de caminhos antigos e não devem ser executadas sem migração. Para o loteA, usar os dois comandos vigentes no topo. Zero ensaios físicos. [SuspensãoP04/P15 anterior](../P04/Suspensao_P04_P15/README.md) preservada; P15 recebeu o complemento nominal do loteA, enquanto P04 não foi recalculado nesta etapa.
