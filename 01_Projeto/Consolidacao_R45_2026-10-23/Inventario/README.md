# Inventário, vãos e apoios — consolidação R45

23/10/2026. Leitura da R44; o documento original não foi modificado por esta frente; foram criados estudos CAD separados. [Cotas e cálculos reproduzíveis](Cotas_e_calculos.md) · [Dados](Verificacoes_dimensionais.json) · [Script](analisar.py).

Foram inventariados os 20 módulos e as peças diretas de marcenaria, reconferidas 13 cotas de equipamentos/prateleiras e calculados 18 cenários de flecha. Não são 20 módulos aprovados: a matriz abaixo distingue cobertura de encerramento. Gavetas, portas, banco, cesto e varal têm frentes específicas na consolidação.


## Entrega aprofundada

- [Matriz dos 20 módulos](Matriz_20_modulos.md): vãos internos, hidráulica, ligações e distinção de peças vigentes/históricas.
- [171 interfaces retangulares](Interfaces_retangulares.md): contatos nominais e necessidade de ligação; dados reproduzíveis emJSON e scriptinterfaces.py.
- [Bancada R02](Bancada.md): estudo separado de estrutura embutida, análise de flexão, massa, colisões e limites. Não é alteração aprovada da bancada.
- [Espelheiro](Espelheiro.md): oito pinos .711, furação candidata e teste geométrico.
- [Minifix no aéreo C](Minifix_C.md): alternativa de montagem fixa,20 conjuntos, sete painéis válidos e alojamentos sem interferência com38 sólidos de contexto.
- [Varões](Varoes.md): quatro cortes, oito terminais, comparação Ø20/25 e limite de carga ainda pendente.
- [Ferragens fixas](Ferragens_fixas.md): candidatos, incompatibilidades e rejeição da suspensão SAH215 sem reserva traseira16.

Para quantitativos use `Solidos_finitos_ativos_R44.json`:1078 sólidos finitos positivos. O bruto `Folhas_ativas_globais_R44.json` inclui planos/datum e não serve para somar volumes;2876 referências foram separadas em `Referencias_excluidas_R44.json`. Ativo significa visibilidade respeitada na cadeia de ancestrais, não aprovação da peça: reservas de equipamentos e propostas ainda exigem classificação semântica.

**Nota estrutural:** divisórias que partem de cima de uma base só podem suspender essa base através de ligações dimensionadas. Os compartimentos da matriz não equivalem automaticamente a apoios de viga. Não creditar como apoio vertical apenas por contato lateral.

## O que merece atenção agora

- A bancada do escritório mede 2000 × 700 × 30 mm. Os dois pés visíveis têm centros separados por 1850 mm. Sem creditar uma ligação estrutural à parede, a triagem biapoiada dá **8,92 mm de flecha instantânea com peso próprio hipotético de 31,5 kg mais 5 kg distribuídos**. Isso não descreve uma bancada apoiada continuamente atrás: identifica que a fixação traseira, reforços e ligações aos pés precisam estar explicitados. Os dois pés, sozinhos, não bastam como prova dimensional/estrutural do conjunto. Não adicionar pé central invadindo o espaço de trabalho por conveniência.
- As prateleiras removíveis do espelheiro têm 560 × 104 × 18 mm e folga nominal de 2 mm em cada lateral e atrás. Embora quatro pinos possam ter alta capacidade de catálogo, a placa rasa de 104 mm é sensível: o cenário com 10 kg de conteúdo resulta em **2,28 mm de flecha imediata**, antes de fluência. Não atribuir os 80 kg do conjunto de pinos à prateleira.
- A base de 799 × 312 × 18 mm do aéreo da lavanderia, considerada apenas entre laterais, dá **4,78 mm com 20 kg de conteúdo**, incluindo peso próprio. A prateleira B de 661 × 312 × 18 mm dá **2,64 mm** no mesmo cenário. São prioridades para definir carga, ligação com fundo e reforço; não inserir novas divisórias diminuindo a guarda sem necessidade.
- ME23P preserva os **100 mm superiores escolhidos em F104**; o manual pede 300 mm. A decisão prévia não foi revertida e a divergência continua identificada, sem qualificá-la como validação técnica. Geladeira e LG possuem 100 mm traseiros no nominal; geladeira tem também 100 mm superiores e à direita, sem tolerância extra além da reserva.
- Existem 12 formas classificadas inválidas no inventário completo, incluindo oito agregados e quatro dobradiças do canto. Esse número não significa 12 peças novas defeituosas: os agregados propagam a condição dos filhos. Não foram feitas reparações automáticas. Coordenadas globais do roupeiro foram confrontadas com as paredes do quarto e estão coerentes; um alerta inicial por coordenadas acima de 5000 mm foi descartado.

## Cobertura por módulo

| ID orçamento / módulo | Verificação nesta frente | O que permanece aberto antes da unidade |
|---|---|---|
| P01 Roupeiro | Peças e prateleiras 18 mm, profundidade interna 550 mm; seis níveis de sapateira e dois tampos curtos preservados | Cabideiro, suportes, ligações, cargas; trilhos/gavetas em frente específica |
| P02 Canto em L | Dimensões/árvore inventariadas, orientação global conferida | Ligações; quatro dobradiças de referência com forma inválida para revisão específica |
| P03 Maleiro | Peças diretas inventariadas | Apoio da caixa, cargas e ligações; correr em frente específica |
| P04 Aéreo cabeceira | Profundidade útil 212 mm entre frente da caixa e fundo; apoios 18/36 mm preservados | Suspensão e ligações dos divisores; portas em frente específica |
| P05 Pia | Prateleira 614 × 572 × 18 mm identificada | Recorte hidráulico real e retenção; não contar prateleira integral como uso livre certificado |
| P06 Gaveteiro cozinha | Inventário de carcaça | Gavetas/engates/carga em frente específica |
| P07 Cocção | Apoio plano e três nervuras R31 presentes; grelhas e réguas inventariadas | Carga e uniões; interface térmica e datum dos aparelhos conforme estudo Fischer |
| P08 Gaveta baixa | Inventário preservado | Rodízios/caixa/curso em frente específica |
| P09 Aéreo D | Reserva de canal técnico 196 × 178 × 556 mm; profundidade de caixa 312 mm | Canal de retorno do depurador, suspensão e conexões |
| P10 Aéreo C | Três prateleiras 511 × 312 × 18; cenário de flexão calculado | Definir fixas/removíveis e carga; folga de fabricação |
| P11 Aéreo B | Prateleira 661 × 312 × 18; cenário calculado | Carga/rigidez e ligações; não liberar pelos pinos |
| P12 Aéreo A | Base útil 765 × 312; divisor central 18; geladeira com 100 mm superiores | Suspensão e carga; tolerância de instalação futura |
| P13 Micro | Apoio 697 × 470 × 18; corpo 461 × 352 × 290; folgas nominais extraídas | Fixação do apoio e pés do aparelho; divergência superior F104 |
| P14 Tanque/cesto | Peças e fundo técnico inventariados | Hidráulica/suspensão; mecanismo em frente específica |
| P15 Aéreo lavanderia | Base 799 × 312 × 18; cenário de flecha calculado | Carga, fundo estrutural/apoio e suspensão |
| P16 Gavetas escritório | Inventário | Montagem específica por agente de gavetas |
| P17 Aéreo escritório | Caixa 2000 mm com divisores 18/36 mm; alturas 1900–2450 mm | Suspensão, ligações e carga de ciclismo; 20 mm ao teto nominal preservados |
| P18 Gabinete banheiro | Referência R43 de correr prevalece; grupo Modulo017 contém histórico | Suspensão e hidráulica; não somar portas antigas ao kit atual |
| P19 Espelheiro | Duas prateleiras 560 × 104 × 18 com 2 mm laterais/traseiros; cenários calculados | Oito pinos candidatos; carga, espelho, retenção e suspensão |
| P20 Banco | Inventário apenas | Estrutura e tampas nas frentes específicas; dois painéis preservados |
| C01–C06 complementos | Bancada, prateleiras TV/consoles, cabeceira, encosto e arremates preservados | Fixações independentes, carga de uso e ancoragem futura |

## Ferragens de apoios pesquisadas

| Aplicação | Referência e quantidade de estudo | Resultado dimensional e limite |
|---|---|---|
| Duas prateleiras removíveis do espelheiro | **Häfele 282.04.711, 8 pinos** | Fonte oficial confirma furo 5 mm e 80 kg com quatro suportes, sob condições do ensaio. Manter candidato anterior; carga da prateleira e profundidade/furação da lateral continuam próprias. Não é suporte de vidro. |
| Prateleiras de madeira que precisem de retenção | **Rometal SP-400, quatro por prateleira**, alternativa | Espessura mínima 18 mm; capacidade declarada de conjunto 40 kg. Manual indica CC 3,5 × 14 para MDF e alternativa com contrassuporte por M4 de comprimento 10 + espessura da divisória. Não adicionar aos pinos: escolher um sistema por prateleira. Dimensões de usinagem e conteúdo ainda precisam ser compatibilizados. |
| Alternativa de encaixe oculto | **Rometal SP-500, quatro por prateleira**, alternativa | Mínimo 15 mm, 40 kg por conjunto; exige usinagem e parafuso 3,5 × 16. Não promove ganho de capacidade da placa nem justifica recortar as prateleiras existentes nesta rodada. |
| Prateleira superior da TV, profundidade 250 e espessura 30 mm | **Rometal PP-144 / código 1217**, candidato | Manual limita profundidade a 250 mm, espessura mínima 20 e distância entre suportes a 400. Geometria da chapa está na faixa; distribuição de apoios na extensão de 1100 mm e ancoragem ainda não liberadas. A carga anunciada é por dois suportes, sem extrapolar linearmente para três/quatro. |
| Prateleiras TV inferior e consoles, profundidade 350 mm | Família **Rometal PP-110/140/144/155 descartada nesta aplicação** | Manual limita PP-110/144/155 a 250 mm e PP-140 a 180 mm. Não aceitar por anunciar 25/35 kg: profundidade excede a aplicação. Preservar as prateleiras de 350 mm e buscar sistema específico. |
| Grelhas removíveis do forno | Oito ligações M4, quatro por grelha | R02 previa rosca retida. RAMPA SKD30 M4 × 8 externo × 8 comprimento é referência de pequeno inserto pesquisada, **sem instalação liberada em MDF de 18 mm**. A ficha localizada refere madeira maciça; ensaio/indicação para material da régua e disponibilidade brasileira ainda necessários. Não usinar por semelhança dimensional. |
| Aéreos, bancada, painéis e prateleiras de parede | Suspensores/chapa de fixação + ancoragens por aplicação | Não escolher bucha por carga em concreto quando o substrato da unidade é desconhecido. É possível definir carga e interface do móvel agora; seleção final da ancoragem depende do executivo/levantamento, não apenas de medidas externas. |

As quantidades de pinos não se estendem automaticamente às prateleiras fixas da cozinha/roupeiro. União estrutural da caixa não pode ser substituída por apoio solto para facilitar a lista de compra. A montagem do móvel precisa definir quais painéis contraventam o conjunto.

## Método e evidências

[Objetos_R44.json](Objetos_R44.json) registra 5040 formas, inclusive agregados e histórico, com coordenadas locais. [Arvore_R44.json](Arvore_R44.json) permite rastrear 5668 objetos. [Folhas_ativas_globais_R44.json](Folhas_ativas_globais_R44.json) aplica o Placement global aos sólidos de folhas e verifica visibilidade dos grupos ancestrais; referências ainda visíveis podem continuar históricas, portanto não usar contagem bruta como quantitativo comercial.

A flecha foi calculada por `δ = 5 W L³ / (384 E I)`, `I = b t³/12`, W em N, com E hipotético 2100 N/mm² e densidade hipotética 750 kg/m³. Usou-se carga distribuída e largura inteira da peça. Peso próprio da bancada inteira foi conservadoramente considerado no trecho entre apoios. A fórmula não representa apoio em quatro cantos, engaste de fundo, carga pontual nos pés do micro ou comportamento de placa bidirecional. L/300 é apenas comparador escolhido, não critério normativo de aprovação. A ficha Greenplac informa uso não estrutural seco e valores mínimos por faixa de espessura; não fornece capacidade pronta destes móveis, fluência ou ligações. Os cenários servem para priorizar detalhes, sem declarar ruptura, segurança ou capacidade final.

## Fontes oficiais consultadas em 23/10/2026

- [Häfele 282.04.711 — pino de prateleira](https://www.hafele.si/en/product/shelf-support-for-inserting-into-drill-hole-5-mm-steel/P-00861929/).
- [Rometal SP-400](https://www.rometal.com.br/acessorios/suportes-para-prateleira/sp-400) e [manual 17770 rev.11](https://www.rometal.com.br/download/9a110e1a-6781-11f1-a626-02006e230003/en).
- [Rometal SP-500](https://www.rometal.com.br/acessorios/suportes-para-prateleira/sp-500) e [manual 17810 rev.11](https://www.rometal.com.br/download/9c746648-6781-11f1-b5c9-02006e230003/en).
- [Rometal Parabolt](https://www.rometal.com.br/acessorios/suportes-para-prateleira/parabolt) e [manual 17811 rev.10](https://www.rometal.com.br/download/97ad94fe-6781-11f1-a8d3-02006e230003/en).
- [Greenplac — requisitos e cuidados](https://download.greenplac.com.br/download/qualidade-requisitos-normativos-e-cuidados.pdf).
- [RAMPA — ficha de insertos para madeira maciça](https://www.rampa.com/media/7e/76/df/1699524009/RAMPA_Produktdatenblatt_Laubholz-Hardwood_EN.pdf).
- Folgas dos aparelhos: documentação local [Conferência 127 V e folgas](../../Equipamentos/Conferencia_127V_e_folgas.md), observando que Venax/PE11X/WC4 foram superados; cálculos desta frente usam apenas ME23P, IB6S e geometria atual da LG. [Fischer e apoios](../../Cozinha/Fischer_Grill_2026-10-19/Apoios_ventilacao_R01/README.md) e [grelhas R02](../../Cozinha/Fischer_Grill_2026-10-19/Grelhas_manutencao_R02/README.md).

Nenhum contato externo, compra, alteração de armazenamento ou medida do apartamento foi inferido. Esta entrega é uma parte da consolidação R45, não substitui as verificações específicas das outras frentes.
