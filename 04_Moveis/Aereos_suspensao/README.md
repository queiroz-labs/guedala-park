# Ligações e suspensão dos aéreos

## Lote B — P17/P04/P12

**Premissas de Elias,25/10/2026:** “20 kg / 10 kg / 10 kg” de conteúdo, respectivamente; “Base limpa, sem cabeças ou tampinhas aparentes”; “Desenvolver os fundos inteiros”. [Registro e usos](Lote_B_premissas.json). Metas globais,sem capacidade demonstrada ou aplicação naR52.

| Móvel | Fundo18 no estudo | Madeira + conteúdo, kg* | Ligações internas candidatas |
|---|---|---:|---:|
| P17 | 1964×550, antes514 de altura | 72,24–92,33 | 24 Minifix |
| P04 | 1764×308, antes272 de altura | 36,15–46,21 | 24 Minifix |
| P12 | 765×548 atual preservado | 32,75–41,51 | 12 Minifix |

*Hipótesesρ650/800/900 e fator18,3/18; sem massas reais das ferragens. Acréscimo dos fundos≈1,04/0,93kg emP17/P04 aρ800. Envelope/vãos preservados. A faixa7 deP04 continua proposta não adotada, incluída apenas como massa, sem reforço. Elias,25/10/2026:“Fita na borda no padrão externo: Arenza no P04 e off-white no P17”; duas faces dos fundos emBrancoTX.

[Prancha](Lote_B_caixa_e_ligacoes.png) · [geometria/contatos](Lote_B_geometria.json) · [585 casos e memória](Lote_B_detalhamento.json) · [48 traseiras](Lote_B_ligacoes_traseiras.csv) · [60 posições internas](Lote_B_ligacoes_internas.csv) · [conferência independente](Lote_B_verificacao.json).

**Base limpa:** canecos nas faces internas da base/tampo para encontros com laterais; nas faces livres das divisórias para encontros verticais. Preserva as24/24/12 posições previstas noR00, sem somá-las como compra. As8 entradas inferiores antigas de cadaP17/P04 precisam ser substituídas. Dois divisores18 permanecem independentes; canecos acessíveis pelas faces externas do par. Não há reforço monolítico36.

Minifix candidatos262.26.034/262.28.920:[fontes oficiais](Lote_B_fontes_Minifix.json),Ø15,A9,profundidade13,5+0,5,B34. Furos cegos cabem nominalmente,deixando4mm;resistência/rigidez e chapa/piloto reais continuam pendentes.

**P04:quatro acessos resolvidos nominalmente:** AllenSW4 curta80×22,sem mover divisória. [Validação](../P04/Suspensao_P04_P15/README.md#p04--acesso-e-caminho-da-carga-vigentes) · [desenho](P04_acesso_e_suspensao.png):envolvente contínua,oito calços fixos,portas desclipadas,folga3,30mm. Retalho real pendente;corredor genérico20 inadequado.

**SuspensãoP04:** canto esquerdo externo rejeitado por colisão com o divisor. Bigfer candidata na faceu25 desse divisor18 e na lateral direita;765equilíbrios3D/1530vetores,seis casos de qualificação,braço hipotético160. Máximos separadosV283,64/T515,78/R586,26N por suporte. [Dados](P04_validacao.json) · [conferência](P04_verificacao_validacao.json) · [pacote para laboratório](P04_ensaios_laboratorio.pdf). Dois suportes não têm suficiência demonstrada; novo caminho pelo divisor/fundo requer prova.

**Traseira:**48 posições Confirmat7×50 base/tampo–fundo herdam estações dos estudos parciais;32mm além do fundo18,sem alcançar a face inferior. R00 tem18/12/9CF anteriores; proposta com fundos inteiros soma24/24/0, dando42/36/9, sem compra definida. P04 conserva2CF/divisor doR00: não somar também o terceiro marcador do estudo parcial.

**Falta comprovar:** cabeças/pilotos,juntas,retenção,contatos inferiores e suspensão. MáximosM≈225,6/82,5/98,8Nm;`T=1000M/h`. Não dividirV por furos ou transferir flechas locais aoMinifix;sem ensaio físico.

Reprodução em`ferramentas/aereos/`:reconciliar_lote_b,detalhar_lote_b,conferir_lote_b,validar_p04,conferir_p04,com`python -B` e extensão`.py`. Hash das fichas:IDs/três dimensões consumidas. SHA doCAD intacto,sem abrirFreeCAD.

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

### Base genérica preservada

Origem: u na esquerda interna,v na traseira para frente,z na base externa original. [Dados do lote](Detalhamento_P09_P11_P15.json):696casos,4176vetores,12zonas36×36×8/corredorØ20 só contra madeira, sem ferragem escolhida. Corpos reconciliados com extraçãoR51/fichas atuais e CG das portasR52; reserva hipotética1kg de ferragens. Dois grupos recebemV pelo CG lateral; tração repartida0/100,50/50 ou100/0. Caixa precisa realizar a partilha. Essa implantação genéricau72 não é a Bigfer abaixo. P09 exclui depurador;10kgP11 é global, não por nível. Sem majoração, impacto, massa real, resistência ou ensaio.

### Apoio inferior e fundo–laterais — avanço independente da Bigfer

[Desenho das faixas](Apoio_e_caixa.png) · [dados e requisitos de ensaio](Apoio_e_caixa.json) · [conferência](Verificacao_apoio_caixa.json).

Referências na **aresta traseira das laterais existentes**:18×60mm por lado,Z60…120,centro hipotético90,área1080mm². Sem peças/calços novos ou perda interna. Resultantes laterais emu−9/W+9, diferentes dos suportes superiores40,5/W−40,5; reações inferiores precisam equilibrar soma e momento, não copiarT de cada lado.

| Cenário de conteúdo global | Maior compressão por lado (N) | Pressão média sobre1080mm² (MPa) |
|---|---:|---:|
| P09 atual10kg | 183,64 | 0,170 |
| P11 atual10kg | 189,83 | 0,176 |
| P15 atual20kg | 278,76 | 0,258 |
| P15 estudo20kg | 294,82 | 0,273 |

Demandas condicionais, não limites admissíveis. **Fundo e laterais estão no mesmo plano da parede**: marcar faixas não garante contato só nelas, nem centroZ90. Conferir área/centro reais; outros contatos mudam o braço. Não atribuir a área nominal inteira ou incluir calço isolado que incline o gabinete.

**Juntas:** três pontos colineares em uma lateral não reagemMz por forças pontuais; o caminho precisa do fundo/outra lateral ou de rigidez de junta demonstrada. Mantidos seis Confirmat candidatos. Dois grupos permitem equilíbrio, sem provar resistência/rigidez do fundo ou juntas. Definidos8casos de ensaio em4configurações, com toda a força de um suporte introduzida no fundo e as duas laterais presas ao dispositivo. Reações publicadas são solução matemática de norma mínima, **não forças de projeto por parafuso nem envelope de todas as juntas**. Não somar esse corpo de prova à suspensão ou creditar atrito/cavilhas.

[Roteiro nominal para oficina](Roteiro_apoio_caixa.txt), com dimensões/eixos/datum dos corpos de prova · [4176 reações inferiores](Reacoes_apoio_inferior.csv) · [48 reações nos8casos](Corpos_prova_fundo_laterais.csv). Reprodução: `python -B ferramentas/aereos/analisar_apoio_caixa.py` e `python -B ferramentas/aereos/conferir_apoio_caixa.py`. Medir acomodação das juntas/deformação do fundo e conferir contato real. Nenhuma resistência foi demonstrada pelos certificados de equilíbrio.

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

Hashes de texto normalizamCRLF→LF;PDF/FCStd permanecem byte a byte. Caminhos relativos usam`/`. Regressão: `python -B ferramentas/aereos/test_fontes.py`.

Consultas prontas, não enviadas: [qualificaçãoBigfer e demais produtos](Consulta_suspensao_lote_A.txt) e [depurador](Consulta_depurador_P09.txt). Comprovar juntasMDF/composiçãoP15 por dados/ensaio e conferir ferragem/ferramentas/sequência reais. Parede/revestimento/instalações após as chaves; produto pode ser definido antes.

[Dados e hashes](Detalhamento_P09_P11_P15.json) · [mapa dos96 eixos](Mapa_ligacoes_P09_P11_P15.csv) · [4176 solicitações](Solicitacoes_fixacao_direta.csv) · [conferência independente](Verificacao_ligacoes_P09_P11_P15.json).

Mapa genérico: `python -B ferramentas/aereos/detalhar_ligacoes.py` e `python -B ferramentas/aereos/conferir_ligacoes.py` (NumPy/Pillow), sem abrirCAD. Zero ensaios físicos, compras ou furos executivos. Estudos abaixo conservam hipóteses próprias.

## Estudo global anterior — P09/P11/P12/P17

Memória25/10, T02: [1404casos](Resultados.json), volumes/CG doBREPR51 e movimento de quatro barras. Densidades650/800/900, fator18,3/18, conteúdo0/5/10/20kg, portas independentes0/86°,45° e extremos amostrados. São cenários globais, não capacidade por chapa. Dimensões, peças e48 envelopes estão nos dados. As metasP17/P12 e fundos preferidos foram atualizados no loteB acima.

Parede na traseira nominal; dois grupos paramétricos, vãos100/80% da largura,h50/80% da altura, tração100/0,50/50 ou0/100. `V=Σmg`; `M=Σmgv/1000`; `T=1000M/h`. Sem produto/furos, majoração, impacto ou rigidez/resistência comprovados. Grupo não é parafuso; preservar correlaçãoV/T. P09 exclui depurador e mantém divisor312/R48. P11 não recebe10kg por nível automaticamente.

## Depurador P09: dado do fabricante e interface ainda aberta

![Corte dos envelopes do depurador e gabinete](Interface_depurador_42mm.png)

O [manual SuggarDE61IX/DE62IX](../../09_Referencias/Plantas_e_manuais/Manuais/Suggar_DE61IX_DE62IX.pdf),REV.0025,p1, publica6,00kg/60cm e8,01kg/80cm. Figuras5–8: parede primeiro, gabinete depois,4parafusos4,2×30. Partilha exige desenho/rigidez; não atribuir automaticamente massa ao armário ou escolher ancoragem pelo manual.

Gabarito simplificadoPeca139 terminaZ1916, baseP09 começaZ1958:42mm sem ligação representada. Abas comerciais ausentes; não conclui inviabilidade do produto. Preservar retorno20, filtros/acessoR48, sem adaptador ou canal de duto cancelado. [Dados e sensibilidades](Depurador_dados_e_pendencias.json):6kg=58,840N, CG ainda desconhecido.

## Evidências e reprodução

[GeometriaR51/folga42](Geometria_R51.json) · [verificação histórica](Verificacao.json) · [memóriaP04/P15](../P04/Suspensao_P04_P15/README.md). Usar rotinas vigentesA/B; antigas exigem migração. No imóvel: conferir parede/revestimento/instalações antes das ancoragens. Sem consultas enviadas, compra ou ensaio físico.
