# Ligações e suspensão dos aéreos

## Lote B — P17/P04/P12

Caminhos e suspensão: [P17](../P17/Base_fundo_ligacoes/README.md),21 grupos/70 posições; [P12](../P12/README.md),9/21; 30 cortes por móvel. Acessos nominais conferidos; fixadores, rigidez e ensaios pendentes.

**Premissas de Elias, 25/10/2026:** “20 kg / 10 kg / 10 kg” de conteúdo, respectivamente; “Base limpa, sem cabeças ou tampinhas aparentes”; “Desenvolver os fundos inteiros”. [Registro e usos](Lote_B_premissas.json). Metas globais, sem capacidade demonstrada ou aplicação na R52.

| Móvel | Fundo 18 no estudo | Madeira + conteúdo, kg* | Ligações internas candidatas |
|---|---|---:|---:|
| P17 | 1964×550, antes 514 de altura | 72,24–92,33 | 24 Minifix |
| P04 | 1764×308, antes 272 de altura | 36,15–46,21 | 24 Minifix |
| P12 | 765×548 atual preservado | 32,75–41,51 | 12 Minifix |

*Hipóteses ρ650/800/900 e fator 18,3/18; sem massas reais das ferragens. Acréscimo dos fundos≈1,04/0,93 kg em P17/P04 a ρ800. Envelope/vãos preservados. A faixa 7 de P04 continua proposta não adotada, incluída apenas como massa, sem reforço. Elias, 25/10/2026: “Fita na borda no padrão externo: Arenza no P04 e off-white no P17”; duas faces dos fundos em BrancoTX.

[Prancha](Lote_B_caixa_e_ligacoes.png) · [geometria/contatos](Lote_B_geometria.json) · [585 casos e memória](Lote_B_detalhamento.json) · [48 traseiras](Lote_B_ligacoes_traseiras.csv) · [60 posições internas](Lote_B_ligacoes_internas.csv) · [conferência independente](Lote_B_verificacao.json).

**Base limpa:** canecos internos na base/tampo–laterais e faces livres dos divisores. 24/24/12 posições R00, sem compra extra; substituir 8 entradas inferiores de cada P17/P04. Divisores 18 independentes, acesso externo ao par; sem crédito monolítico 36.

Minifix candidatos 262.26.034/262.28.920:[fontes oficiais](Lote_B_fontes_Minifix.json), Ø15, A9, profundidade 13,5+0,5, B34. Furos cegos cabem nominalmente, deixando 4 mm; resistência/rigidez e chapa/piloto reais continuam pendentes.

**P04: quatro acessos resolvidos nominalmente:** Allen SW4 curta 80×22, sem mover divisória. [Validação](../P04/Suspensao_P04_P15/README.md#p04--acesso-e-caminho-da-carga-vigentes) · [desenho](P04_acesso_e_suspensao.png): envolvente contínua, oito calços fixos, portas desclipadas, folga 3,30 mm. Retalho real pendente; corredor genérico 20 inadequado.

**Suspensão P04:** canto esquerdo externo rejeitado por colisão com o divisor. Bigfer candidata na face u25 desse divisor 18 e na lateral direita; 765 equilíbrios 3D/1530 vetores, seis casos de qualificação, braço hipotético 160. Máximos separados V283,64/T515,78/R586,26 N por suporte. [Dados](P04_validacao.json) · [conferência](P04_verificacao_validacao.json) · [pacote para laboratório](P04_ensaios_laboratorio.pdf). Dois suportes: suficiência e caminho pelo divisor/fundo a comprovar.

**Traseira:**48 posições Confirmat 7×50 base/tampo–fundo herdam estações dos estudos parciais; 32 mm além do fundo 18, sem alcançar a face inferior. R00 tem 18/12/9CF anteriores; proposta com fundos inteiros soma 24/24/0, dando42/36/9, sem compra definida. P04 conserva 2CF/divisor do R00: não somar também o terceiro marcador do estudo parcial.

**Falta comprovar:** cabeças/pilotos, juntas, retenção, contatos inferiores e suspensão. Máximos M≈225,6/82,5/98,8 Nm; `T=1000M/h`. Não dividir V por furos ou transferir flechas locais ao Minifix; sem ensaio físico.

Reprodução em `ferramentas/aereos/`: reconciliar_lote_b, detalhar_lote_b, conferir_lote_b, validar_p04, conferir_p04, com `python -B` e extensão `.py`. Hash das fichas: IDs/três dimensões consumidas. SHA do CAD intacto, sem abrir FreeCAD.

## Vigente: lote A — P09/P11/P15

25/10/2026. Estudo conforme [AGENTS](../../AGENTS.md), sem tubos ou alteração da R52/acabamentos. **Mapa e solicitações nominais; juntas/produto condicionados.**

**Pré-seleção 25/10:** preferência de Elias por preservar espaço interno, nesta conversa. **Bigfer 04.02.058** candidata, sem montagem/carga demonstradas. [Dados e requisitos](Selecao_ferragem.json) · [desenho](Selecao_ferragem.png). Cotas de trabalho corrigidas: assento 40,5 e furo pequeno9,5; entrada 32 não é assento. A montagem espelhada exige revisão, descrita abaixo.

| Caixa/variante | Interfaces nominais estudadas; não são compras adicionais |
|---|---|
| P09 atual | 20 Confirmat 7×50 candidatos e 11 cavilhas 8×30 apenas de posicionamento. Divisor ligado à base/topo em dois pontos por extremidade e ao fundo em dois pontos |
| P11 atual | Preservar 12 Minifix existentes. 10 Confirmat candidatos: quatro prateleira–fundo e seis fundo–laterais; três cavilhas posicionam a prateleira |
| P15 atual | Preservar 8 Minifix existentes; seis Confirmat candidatos fundo–laterais |
| P15 estudo 18+18 | Mesmos 8 Minifix; 18 Confirmat candidatos: seis base–fundo, seis topo–fundo e seis fundo–laterais. Não especifica a composição entre camadas |

Os 96 pontos incluem alternativas mutuamente exclusivas de P15. Eixos nas interfaces, **não centros completos de canecos, pilotos ou CNC**. Conferência independente: todos em faces de contato positivo. Nos três corpos atuais, base/topo encontram o fundo somente pela aresta: seis encontros sem face útil, excluídos das ligações traseiras. Diâmetros, pilotos, distâncias mínimas, embutimento das cabeças e montagem dependem da ferragem/chapa e ensaio. As cabeças traseiras precisam ser compatíveis com a face encostada à parede.

**P15:** a variante desce a lateral 18 mm e mantém o eixo da base original em Z9. O pino passa de 9 para **27 mm da nova borda inferior**. Não reutilizar o gabarito inferior 9 nessa lateral. A camada adicional é outra peça; acabamento nas duas faces de cada chapa conforme a regra do projeto. O [processo de composição](../P15/Composicao_parcial/README.md) continua sem produto demonstrado; não presumir colagem entre faces BP nem capacidade pela simples soma 18+18. TitebondMelamine permanece excluída.

### Base genérica preservada

Origem: u na esquerda interna, v na traseira para frente, z na base externa original. [Dados do lote](Detalhamento_P09_P11_P15.json): 696 casos, 4176 vetores, 12 zonas 36×36×8/corredor Ø20 só contra madeira, sem ferragem escolhida. Corpos reconciliados com extração R51/fichas atuais e CG das portas R52; reserva hipotética 1 kg de ferragens. Dois grupos recebem V pelo CG lateral; tração repartida 0/100,50/50 ou 100/0. Caixa precisa realizar a partilha. Essa implantação genérica u72 não é a Bigfer abaixo. P09 exclui depurador; 10 kg P11 é global, não por nível. Sem majoração, impacto, massa real, resistência ou ensaio.

### Apoio inferior e fundo–laterais — avanço independente da Bigfer

[Desenho das faixas](Apoio_e_caixa.png) · [dados e requisitos de ensaio](Apoio_e_caixa.json) · [conferência](Verificacao_apoio_caixa.json).

Referências na **aresta traseira das laterais existentes**: 18×60 mm por lado, Z60…120, centro hipotético 90, área 1080 mm². Sem peças/calços novos ou perda interna. Resultantes laterais em u−9/W+9, diferentes dos suportes superiores 40,5/W−40,5; reações inferiores precisam equilibrar soma e momento, não copiar T de cada lado.

| Cenário de conteúdo global | Maior compressão por lado (N) | Pressão média sobre 1080 mm² (MPa) |
|---|---:|---:|
| P09 atual 10 kg | 183,64 | 0,170 |
| P11 atual 10 kg | 189,83 | 0,176 |
| P15 atual 20 kg | 278,76 | 0,258 |
| P15 estudo 20 kg | 294,82 | 0,273 |

Demandas condicionais, não limites admissíveis. **Fundo e laterais estão no mesmo plano da parede**: marcar faixas não garante contato só nelas, nem centro Z90. Conferir área/centro reais; outros contatos mudam o braço. Não atribuir toda a área nominal nem usar calço isolado que incline o gabinete.

**Juntas:** três pontos colineares em uma lateral não reagem Mz por forças pontuais; o caminho precisa do fundo/outra lateral ou de rigidez de junta demonstrada. Mantidos seis Confirmat candidatos. Dois grupos permitem equilíbrio, sem provar resistência/rigidez do fundo ou juntas. Definidos 8 casos de ensaio em 4 configurações, com toda a força de um suporte introduzida no fundo e as duas laterais presas ao dispositivo. Reações publicadas são solução matemática de norma mínima, **não forças de projeto por parafuso nem envelope de todas as juntas**. Não somar à suspensão nem creditar atrito/cavilhas.

[Roteiro nominal para oficina](Roteiro_apoio_caixa.txt), com dimensões/eixos/datum dos corpos de prova · [4176 reações inferiores](Reacoes_apoio_inferior.csv) · [48 reações nos 8 casos](Corpos_prova_fundo_laterais.csv). Reprodução: `python -B ferramentas/aereos/analisar_apoio_caixa.py` e `python -B ferramentas/aereos/conferir_apoio_caixa.py`. Medir acomodação das juntas/deformação do fundo e conferir contato real. Nenhuma resistência foi demonstrada pelos certificados de equilíbrio.

### Produto: duas rotas para resolver

1. **Prioritária — fixação direta compacta:** candidata [Bigfer 04.02.058](https://www.bigfer.com.br/suporte-aereo-l-armarios/), SKU0402058411, aço 1,5. O [catálogo p235](../../09_Referencias/Plantas_e_manuais/Manuais/Ferragens_suspensao/Bigfer_suportes_aereos.pdf) cota braços 49,5/37,8 e tira 16. Proposta nossa nos dois planos verticais do canto: dois envelopes ocupam 59,88 mL, sem capa/cabeça/acesso; fundo 18 permanece na posição e profundidade 312 preservada. Catálogo sem capacidade e sem instrução que confirme esta montagem: **preferida para qualificação, não produto fechado**. O parafuso à parede atravessaria o fundo 18; excentricidade local, chapa/parafusos MDF, retenção e apoios inferiores precisam ser demonstrados. Dois suportes são hipótese, não suficiência comprovada.
2. **Suspensor atrás do fundo:** alternativa separada com reserva 16 dentro da profundidade 330. Deslocar o fundo 16 para a frente e reduzir peças horizontais/divisor de 312 para 296 custa aproximadamente 5,30 L no P09,5,88 L no P11 e 6,95 L no P15 atual. Não fazer rasgo 16 numa chapa 18. Muda armazenamento, juntas e cálculos; não foi incorporada. Ter 16 livres não prova compatibilidade do produto com fundo 18.

**Implantação específica Bigfer:** u40,5/W−40,5 e centro Z H−58; compressão inferior hipotética Z90. Assento 40,5=49,5−9; entrada Ø10 em 32. Pequeno furo 9,5=32−22,5=1,5+8 desde o canto externo. Laterais v30,8/42,8: validar passo 12/borda 9,5 no MDF; Ø5 na ferragem não é piloto Ø5 na madeira. Subir 32 evita alinhamento com Confirmat H−90; separação ao Minifix superior 49. Seis envelopes/corredores sem interseção com madeira, sem conferir ferragens/ferramenta reais. Reservas 36×36×8 anteriores não contêm este suporte 49,5×37,8×16.

**Montagem:** dois suportes espelhados pedem translações opostas de 8,5 mm para passar da entrada ao assento. Encaixe simultâneo por translação única rejeitado. Proposta a confirmar: gabinete sustentado/nivelado e fixações inseridas/apertadas por dentro, retiradas também com apoio. Validar cabeça/arruela no rasgo 5, fundo 18, torque, retenção e apoio inferior. Não há ancoragem/parafuso escolhido.

Recalculados 4176 vetores no assento 40,5: V/T dos maiores R,10 kg P09/P11 e 20 kg P15 =239,31/199,25 N; 251,05/204,76 N; 345,94/296,74 N(P15 atual) e 370,51/313,84 N(P15 estudo). Os maiores V ocorrem em outros casos. [Oito casos para qualificação](Requisitos_suporte_L.csv) preservam máximos V/T/R sem combiná-los · [todos os vetores](Solicitacoes_suporte_L.csv) · [conferência](Verificacao_selecao.json). Demandas sem capacidade física. Momentos r×F são reduzidos ao canto: não somar ao equilíbrio global nem dividir V pelos três furos. Reprodução: `python -B ferramentas/aereos/selecionar_ferragem.py` e `python -B ferramentas/aereos/conferir_selecao.py`.

**Alternativas internas examinadas:** SAH130 e SAH116 mostram fundo 3–5/máximo 5 nas instruções, com recorte; não substituem diretamente nosso fundo 18. Nelas, a cota mínima 16 vai até a face frontal do fundo, diferente de reserva livre 16 atrás dele. [Manuais preservados](../../09_Referencias/Plantas_e_manuais/Manuais/Ferragens_suspensao/README.md). Bigfer 04.02.007/008 fica como reserva geométrica (aço 1,9,42×58×20), também sem capacidade demonstrada. Camar 807VP não foi escolhido: BP16 no desenho, aplicação com fundo 18/oferta local sem comprovação; advertência de carga 807IN não comprova a variante VP.

HB65: página 65 kg/ficha 60 kg, unidade e V/T pendentes; exige reserva posterior 16. SAH216 também exige 16/fixação lateral. FGVTN fixo0091.510010: cotas 8/16/22 e 80 kg não demonstram nossa montagem. [Fontes oficiais e manuais preservados](../../09_Referencias/Plantas_e_manuais/Manuais/Ferragens_suspensao/README.md). Não somar capacidades ou escolher o número maior.

**P09:** o espaço nominal 42 entre gabarito e base não é vencido automaticamente pelo parafuso 30 do manual: faltariam 12 antes do embutimento. Conta condicional ao topo do gabarito simplificado; abas reais não estão modeladas, portanto não reprova o aparelho. Não escolher parafuso maior, inventar adaptador ou atribuir os 6 kg automaticamente ao gabinete. Preservar retorno 20, filtros e afastamento de instalação.

### Próximas entregas e reprodução

Hashes de texto normalizam CRLF→LF; PDF/FCStd permanecem byte a byte. Caminhos relativos usam `/`. Regressão: `python -B ferramentas/aereos/test_fontes.py`.

Consultas prontas, não enviadas: [qualificação Bigfer e demais produtos](Consulta_suspensao_lote_A.txt) e [depurador](Consulta_depurador_P09.txt). Comprovar juntas MDF/composição P15 por dados/ensaio e conferir ferragem/ferramentas/sequência reais. Parede/revestimento/instalações após as chaves; produto pode ser definido antes.

[Dados e hashes](Detalhamento_P09_P11_P15.json) · [mapa dos 96 eixos](Mapa_ligacoes_P09_P11_P15.csv) · [4176 solicitações](Solicitacoes_fixacao_direta.csv) · [conferência independente](Verificacao_ligacoes_P09_P11_P15.json).

Mapa genérico: `python -B ferramentas/aereos/detalhar_ligacoes.py` e `python -B ferramentas/aereos/conferir_ligacoes.py` (NumPy/Pillow), sem abrir CAD. Zero ensaios físicos, compras ou furos executivos. Estudos abaixo conservam hipóteses próprias.

## Estudo global anterior — P09/P11/P12/P17

Memória 25/10, T02: [1404 casos](Resultados.json), volumes/CG do BREP R51 e movimento de quatro barras. Densidades 650/800/900, fator 18,3/18, conteúdo 0/5/10/20 kg, portas independentes 0/86°,45° e extremos amostrados. São cenários globais, não capacidade por chapa. Dimensões, peças e 48 envelopes estão nos dados. As metas P17/P12 e fundos preferidos foram atualizados no lote B acima.

Parede na traseira nominal; dois grupos paramétricos, vãos 100/80% da largura, h50/80% da altura, tração 100/0,50/50 ou 0/100. `V=Σmg`; `M=Σmgv/1000`; `T=1000M/h`. Sem produto/furos, majoração, impacto ou rigidez/resistência comprovados. Grupo não é parafuso; preservar correlação V/T. P09 exclui depurador e mantém divisor 312/R48. P11 não recebe 10 kg por nível automaticamente.

## Depurador P09: dado do fabricante e interface ainda aberta

![Corte dos envelopes do depurador e gabinete](Interface_depurador_42mm.png)

O [manual Suggar DE61IX/DE62IX](../../09_Referencias/Plantas_e_manuais/Manuais/Suggar_DE61IX_DE62IX.pdf), REV.0025, p1, publica 6,00 kg/60 cm e 8,01 kg/80 cm. Figuras 5–8: parede primeiro, gabinete depois, 4 parafusos 4,2×30. Partilha exige desenho/rigidez; não atribuir automaticamente massa ao armário ou escolher ancoragem pelo manual.

Gabarito simplificado Peca139 termina Z1916, base P09 começa Z1958: 42 mm sem ligação representada. Abas comerciais ausentes; não conclui inviabilidade do produto. Preservar retorno 20, filtros/acesso R48, sem adaptador ou canal de duto cancelado. [Dados e sensibilidades](Depurador_dados_e_pendencias.json): 6 kg=58,840 N, CG ainda desconhecido.

## Evidências e reprodução

[Geometria R51/folga 42](Geometria_R51.json) · [verificação histórica](Verificacao.json) · [memória P04/P15](../P04/Suspensao_P04_P15/README.md). Rotinas A/B vigentes; antigas exigem migração.
