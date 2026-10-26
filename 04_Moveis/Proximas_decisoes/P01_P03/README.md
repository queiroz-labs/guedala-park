# P01/P03 — equilíbrio da caixa completa e ligações compartilhadas

**P03/P02/piso:** [1728 casos acoplados](../../P03/README.md). C01:seis posições passantes candidatas;201N tração/33N cisalhamento na hipótese central. Divisória→base18→soco62:9900mm² nominais, base≈0,05mm. Produto/ensaioMDF, nivelamento, juntas e deformação superior pendentes;20kg não demonstrados. R52 preservada sem abrirCAD.

25/10/2026. **P02 agora também está individualizado: o retorno exige uma ligação positiva no caso de carga concentrada investigado.** Foi preparada a topologia nominal P01/P03/P02, com proposta separada de topo P03 inteiro mais profundo. Não é dimensionamento das juntas, cálculo de flecha ou liberação de fabricação. A etapa anterior de equilíbrio P03 continua documentada abaixo e não deve ser confundida com este novo corte.

A R52 foi aberta em processo separado FreeCADCmd, apenas para leitura; hash preservado. Nenhum documento da GUI foi acessado. R52 e todos os estudos anteriores permanecem intactos. Soco e alongamentos continuam propostas separadas, sem tubos e sem integração automática.

## Topologia vigente de estudo e resultado novo

**Novo requisito P03:** [duas malas de bordo e comparação da abertura](../../P03/README.md). Alternativas672 ×306 ou650 ×306, ambas com recuo20 nas laterais/base/topo, passaram nas amostragens de frentes/duas malas550 ×350 ×250. B650 usa três dobradiças candidatas/calço3, revestimentos/faixas (+4,95kg de madeira fixa a800) e novas uniões por face.72 cortes de equilíbrio separado P03→P01 incluem conteúdos0/20/30kg e portas abertas, sem provar resistência ou caixa P02 acoplada. Aplicação autorizada se atender; proporção baixa, ferragens, fixações e caixa ainda pendentes. Não somar resultados antigos como se a geometria fosse a mesma.

**Mockup de abertura P02:** [quatro situações — fechado, só A, só B e ambas abertas](Abertura_armario_L.png). Duas portas independentes, quina fixa e curso ilustrativo86°, a partir das vistas CAD do canto simplesR04 ainda vigente nas portas P02. Azul/âmbar apenas identificam as folhas; acabamento geral amadeirado. Imagem gerada com a ferramenta integrada `image_gen`, conferida visualmente; não substitui geometria, verificação de colisões ou validação do limitador. [Prompt e referências](Abertura_armario_L_prompt.txt). Não houve abertura ou alteração do FreeCAD para criar este mockup.

![Planta e seção da caixa superior](Topologia_caixa.png)

| Frente | Evidência nova | Direção de projeto |
|---|---|---|
| P02 individualizado | Dez madeiras, incluindo duas folhas, conferidas por volume, centro e caixa contra o inventário anterior; oito painéis estáticos | Base e topo em L inteiros; fundos, apoios terminais e suas uniões próprios. Portas não contraventam a caixa |
| Retorno | Avança 400 à frente da linha mínima de apoio P01, Y3290; região de uso investigada em X7275/Y2920 | Não contar esse trecho como apoiado pela lateral P01, que só começa em Y3372; continuação frontal começa em Y3290 |
| Ligação C01 | Face comum Peca259 ↔ LateralApoioPrincipal, X6740, 612 × 272; duas chapas18 encostadas | Desenvolver uma união positiva face a face, capaz de transferir esforços entre P02 e P03. Não contar base/topo/fundo P02 contra a mesma lateral como juntas independentes adicionais |
| Canto dos fundos P02 | Peca255 ↔ Peca256 compartilham apenas a aresta vertical272, sem área de face | Não prever Confirmat direto nessa aresta. Cada fundo deve ligar-se à base/topo L inteiros; eventual detalhe adicional precisa de desenho próprio |
| Topo e fundo P03 | Peca263 ↔ Peca261: só aresta1314 na R52 e no estudo traseiro anterior | Nova hipótese: substituir o topo inteiro1314 × 632 × 18 por1314 × 650 × 18. Acrescenta18 para trás, criando face23652mm² sobre o fundo, sem ampliar envelope externo ou reduzir o vão |
| Faixas da quina P02 | Cada faixa tem folga2 para base e topo; entre si existe face5508mm² | Desenhar fixação à caixa que atravesse a folga, com acesso; não usar as faixas como pilares ou caminho de carga |

O novo topo não é uma tira18 colada. A hipótese `caixa_fechada_ESTUDO` reaproveita fundo P01 +18 de altura e base P03 +18 de profundidade do estudo anterior, acrescentando a troca do topo inteiro. O acréscimo do topo é425736mm³, ou0,341kg à densidade hipotética800; conjunto das três mudanças1,190kg. Não existe alteração na R52 nem autorização para incorporar essa alternativa. A análise geométrica nova cobre os22 painéis selecionados: nenhuma sobreposição positiva; ferragens, outros objetos do apartamento, transporte e acesso de ferramenta ainda precisam de conferência.

### O caso que exige transferência entre caixas

Foram avaliados81 cortes: três geometrias × densidades hipotéticas650/800/900 × conteúdos0/10/20kg por caixa × três posições de conteúdo P02. P03 usa conteúdo em faixa frontal, CGY3320. P02 compara centro da área L, posição anteriorY3300 e pontaY2920. Folhas na pose salva, sem ferragens presumidas.

- Em nove casos (20kg na ponta, nas três densidades e três geometrias), **não existe equilíbrio só com compressão nos contatos P02–P01**. O certificado é geométrico: o CG fica à frente de todos esses contatos.
- Exemplo800: madeira P02 27,841kg, CGY3491,580; com20kg na ponta, massa47,841kg e CGY3252,630. O apoio mais frontal começa emY3290. Falta uma ação resistente equivalente de pelo menos17,532Nm em relação àquela linha. Não é o momento de cada parafuso nem um envelope completo da junta.
- Os limites da condição frontal, mantendo essa pose e desprezando ferragens, seriam12,324/15,168/17,064kg na ponta para650/800/900. **São fronteiras matemáticas da hipótese, não cargas permitidas.**
- O corte agregado P02+P03 tem distribuição compressiva possível nos81 casos quando se admite uma ligação positiva entre as caixas. Isso é condição necessária; não demonstra equilíbrio de cada painel, comportamento da ligação C01, rigidez ou resistência do conjunto.

No corte local do retorno emY3290, o exemplo800 com20kg na ponta exige262,497N e87,344Nm, incluindo as madeiras situadas à frente. Se, como hipótese de caminho, todo o momento fosse transmitido por um par axial entre os planos médios do topo/base separados290, o par seria301,185N. Isso não seleciona número de parafusos, capacidade ou rigidez composta. O modelo anterior usava apenas a posição P02Y3300: ele não abrangia este caso de ponta.

### Montagem a desenvolver e dados para encerrá-la

1. Montar P03 e P02 em bancada, preservando para suas uniões ocultas a estratégia já escolhida nas fichas R14: **Confirmat7×50 + cavilhaØ8×30**. Não extrapolar essa estratégia para qualquer orientação: a aresta fundo–fundo não a recebe, e7×50 atravessaria a espessura total36 de uma ligação face a face.
2. Em P02, unir base/topo a cada fundo e apoio terminal; ligar Peca255 à lateral principal e Peca256 ao apoio da portaB. A ação de caixa exige transmissão efetiva de cisalhamento e separação nessas juntas, não apenas apoio vertical. Fixar as faixas da quina sem atribuir-lhes papel estrutural.
3. Desenvolver C01 entre as duas laterais. Foram reservadas **quatro estações preliminares**, eixoX, deX6722 a6758: combinações deY3370/3862 eZ2210/2362, com60 às bordas da face útil. São posições de estudo, não quatro fixadores dimensionados nem furação. Conferir dobradiças, ferramentas e fechamento antes de reservar qualquer volume de usinagem.
4. Para C01, comparar somente a família4×30 já usada em outros encontros face a face (penetração nominal12 na segunda chapa, sobra6; capacidade ausente) e um conjunto passante próprio para36mm (produto e desenho ainda ausentes). Não usar atrito de aperto como resistência presumida nem escolher comprimento de conjunto sem ficha. Confirmat50 não é alternativa face a face.
5. Descer as ações simultâneas até os receptores reais de P01: travessa frontal, divisória, laterais e fundo proposto. O efeito do acoplamento pode tracionar/solicitar juntas de P03/P01; não creditar simplesmente a massa vizinha como lastro sem ligação até a base e retenção.

**Próxima evidência exigida:** código/substrato real da chapa; desenho e curva/capacidade do grupo Confirmat+cavilha em união de topo/aresta nas orientações propostas; produto C01, espessura de aperto, furos, tolerâncias e comportamento em cisalhamento/abertura; desenho dos grupos e acesso; então modelo compatível de painéis/juntas e verificação de deformação, estabilidade e resistência. Se curvas não estiverem publicadas, preparar ensaio de junta na chapa real. Não inventar rigidez para aproveitar os certificados estáticos. O fundo P01 inteiro/emenda e os apoios inferiores continuam condições próprias.

Dados novos: [geometria por painel](Geometria_P02_individual.json), [mapa de juntas](Mapa_juntas.csv), [81 casos e parâmetros](Resultados_topologia.json) e [verificação independente](Verificacao_topologia.json). Scripts em `ferramentas/roupeiro/`: `extrair_caixa_superior.py` (FreeCADCmd, somente leitura), `analisar_caixa_superior.py` e `verificar_caixa_superior.py` (Python comNumPy/Pillow). Conferidos153 certificados de equilíbrio e nove certificados de inviabilidade, além de nove cortes locais por volumes analíticos. A conferência valida geometria/aritmética, não capacidade.

**Conferência:** hashR52 preservado. A execução completa anterior foi interrompida sem resultado; não está aprovada. A base de comparação hoje existe, mas não foi criada/ajustada neste estudo. Antes de integrarCAD, concluir as verificações exigidas. A matriz usa `organizar_entregas.py --somente-roupeiro`, preservando os demais17 móveis.

## Etapa anterior — o que entrou no modelo de equilíbrio P03

| Corpo P03 | Geometria nominal | Aplicação do peso |
|---|---|---|
| Laterais Peca259/Peca260 |18×650×308mm cada | No CG próprio de cada lateral |
| Fundo Peca261 |1314×18×272mm | No CG próprio do fundo |
| Base Peca262 |1314×632×18mm atual;1314×650×18 no cenário traseiro | Peso próprio, conteúdo e resultantes das duas folhas |
| Topo Peca263 |1314×632×18mm | No CG próprio, sem transferi-lo previamente à base |
| Folhas Peca264/Peca265 |670×237×18mm cada | Resultantes gravitacionais independentes nos seus CG; equivalentes na base pelo caminho inferiorRO62 |

As folhas não foram uniformizadas sobre a base. O modelo ainda não distribui a carga por carro/trilho: suas posições e massas comerciais não foram inferidas. A pose das folhas é a salva na R52; movimento e cargas horizontais não foram ensaiados aqui.

P01 entra com nove corpos portantes: lateraisP206/P207, fundoP208, baseP209, divisóriaP210, duas continuações laterais frontais e as faixas frontal inferior/superior. O P02 entra como **uma resultante agregada das suas dez madeiras**, com CG obtido por volumes BREP; a base emL real serve para localizar os contatos. Não se substituiu o L pelo seu retângulo envolvente. Não se calculou a flexão nem as ligações internas do retornoP02.

As outras38 madeiras inferioresP01, equivalentes a129,557kg na hipótese800kg/m³, ficam fora deste submodelo por painel. Seu inventário global anterior continua necessário. As reações ao piso deste arquivo **não são o peso completo do roupeiro**; conteúdos inferiores, espelho e massas de ferragens também não foram acrescentados por presunção.

## Três topologias comparadas

| Variante | Corpos | Interfaces de face | Regiões de piso | Situação |
|---|---:|---:|---:|---|
| R52_sem_soco |15 |30 |2 | Geometria corrente dos corpos selecionados; apenas as duas laterais chegam ao piso |
| soco_sem_traseiro |36 |98 |23 | Acrescenta21 peças do socoR01, ainda separado |
| soco_e_traseiro |36 |102 |23 | Acrescenta o soco, fundoP01+18 de altura e baseP03+18 de profundidade, como no estudo anterior |

As interfaces foram extraídas por interseção de faces BREP. Nas superfícies horizontais, quatro ou mais vértices delimitam a distribuição de contato: as forças são apenas compressivas. Ações tangenciais e pares em encontros laterais são incógnitas de **juntas positivas a projetar**, não propriedades de um conector escolhido.

A extração completa também encontra uma pequena rota traseira que não deve ser perdida ao simplificar: o fundoP01 alongado apoia diretamente a lateralP03P259 em324mm², além dos23652mm² sob a baseP03 e11376mm² sob a baseP02. As três parcelas somam35352mm² da face superior do fundoP01. A lateral e a base não recebem duas referências inferiores independentes: descarregam na mesma chapaP208. O modelo preserva esse compartilhamento.

Em cada corpo foram impostas seis equações: três forças e três momentos. Cada ação de interface entra com sinal oposto no corpo vizinho e no mesmo ponto global. A base/divisória, a travessa frontal, o fundo e o soco compartilham essas equações; não foram contados apoios independentes para uma mesma peça inferior.

## Demandas que agora podem ser consultadas

Foram calculados54 casos: três topologias, densidades hipotéticas650/800/900kg/m³, conteúdo0/10/20kg **em cada caixa superior** e conteúdoP03 distribuído ou na faixa frontal60mm. O conteúdoP02 usa o CG de estudo anterior(7115,3300,2290). São hipóteses de investigação, não pesos reais nem cargas autorizadas.

O envelope no corteZ2132 satisfaz exatamente peso e dois momentos gravitacionais. Enumeram-se os vértices básicos admissíveis das pressões compressivas sobre os contatos: isso fornece limites estáticos de cada receptor, sem escolher rigidez de apoio. Um extremo concentrado num vértice é um limite ideal; não comprova pressão ou contato físico local. Os extremos de receptores diferentes não podem ser somados como se ocorressem juntos.

Exemplo800kg/m³,20kg no P03 junto à frente e20kg no P02: as massas superiores são59,402kgP03 e47,841kgP02; com baseP03 alongada,59,743kgP03. Sem uma ligação positivaP02↔P03 demonstrada:

| Topologia | Travessa frontal P01, soma simultânea P03+P02 | Fundo P01, soma simultânea |
|---|---:|---:|
| Geometria corrente |193,9–870,3N | Sem contato direto superior |
| Soco, sem alongamento traseiro |193,9–870,3N | Sem contato direto superior |
| Soco e alongamentos traseiros |107,1–870,4N |0–302,8N |

Esses intervalos dependem da hipótese de contato superior compressivo e das resultantes dos dois módulos. O soco sozinho muda o caminho inferior, mas não a geometria do corte superior. O novo contato traseiro **não assegura** que a travessa frontal passe a receber pouca carga; o máximo estático praticamente não muda.

Há uma alternativa de projeto distinta: uma junta positiva entre o P02 e a lateralP03 na faceX6740 permitiria que as duas caixas transferissem cargas entre si. No corte agregado, o mínimo estático frontal passa a0N; o máximo permanece cerca de870N nesse exemplo. Isso exige uma ligação a projetar, incluindo cisalhamento e pares. Não se adotou essa junta como existente apenas porque as faces encostam. O mínimo193,9/107,1N não é universal para qualquer construção possível.

Os intervalos por receptor, por caixa e por caso estão em [Envelopes_superiores.csv](Envelopes_superiores.csv). O caso com ligaçãoP02↔P03 está separado no JSON, em `if_P02_P03_positive_cross_joint_is_designed`.

## Por que a presença das chapas não fecha a resistência

Um contracheque anterior do topo considerou, como concessão, um apoio traseiro emY3922–3940. A800, o topoP03 pesa117,272N e tem CGY3606, ficando316mm antes dessa região e exigindo ao menos37,058Nm através das ligações. **Correção geométrica da continuação:** esse apoio de face não existe no topo632 da R52; o encontro é somente uma aresta1314. O valor anterior deve ser lido como argumento hipotético, não como apoio BREP extraído. A nova hipótese topo650 cria a face, mas muda massa/CG e não herda automaticamente aquele número. Em nenhum caso encostar chapas encerra a resistência.

O modelo só com contatos normais sem atrito é incompatível nas três topologias; mesmo liberando artificialmente os sinais das normais, as equações não fecham. Isso não prova que o móvel real falha: ele precisa de juntas, e é justamente a transmissão dessas juntas que ainda falta especificar.

Com incógnitas positivas de junta, foram demonstrados12 equilíbrios completos: mínimo frontal, máximo frontal, máximo traseiro e mínimo frontal com acoplamentoP02↔P03, nas três topologias. Todos preservam compressão nos contatos horizontais e fecham forças/momentos individualmente em cada corpo. Os valores por interface estão em [Ligacoes_exemplos.csv](Ligacoes_exemplos.csv).

Esses12 resultados são representantes algébricos de norma mínima, usando uma escala declarada de1000mm para comparar forças e momentos. **Não são partilha prevista, deslocamentos ou envelope de dimensionamento.** A escala é normalização numérica, não rigidez, resistência ou propriedade material.

Foi construído um autoequilíbrio não nulo na própria caixaP03, envolvendo por exemplo a união lateralP259–fundoP261. Somá-lo ao resultado altera as forças/momentos das juntas sem mudar peso, reações de contato ou equilíbrio de qualquer corpo. O verificador somou1000 vezes esse modo e confirmou novamente os balanços. Logo as solicitações de juntas não têm um envelope finito determinado só por equilíbrio quando essas incógnitas são ilimitadas. É necessário introduzir a compatibilidade/curva real de ligação para escolher uma partilha física; nenhum valor mínimo obtido por pseudoinversa deve virar capacidade ou lista de parafusos.

## Entrega fechada e próximo passo de projeto

Ficam disponíveis agora:

1. Geometria nominal e interfaces reais da caixa completaP03 e seus caminhosP01, sem uniformizar topo/fundo/laterais.
2. Envelopes estáticos dos contatos superiores e solicitações simultâneas na travessa/fundo compartilhados, com e sem possível acoplamentoP02↔P03.
3. Doze estados de forças/momentos por corpo e por junta, demonstrando os caminhos até o piso para os corpos selecionados.
4. Prova quantitativa de que contatos normais não bastam e de que equilíbrio sozinho não especifica as juntas nem a flecha.

Na continuação acima, a topologia passou a recomendar C01 positivo e o novo topo650 como estudos. O próximo passo permanece obter/desenhar os grupos reais e suas propriedades nas orientações de uso, incluindo a travessaP01; não atribuir uma mola por aresta e outra ao fundo como se fossem caminhos independentes.

Para calcular deformação, faltam a constituição/propriedades direcionais da chapa e a lei das juntas escolhidas. A extensão matemática para uma “caixa rígida” que eliminasse a flecha anterior seria inválida sem esses dados. Esta entrega não repetiu esse atalho. O formato do fundoP01, detalhamento de emenda se necessária, aparência do soco, nivelamento/piso e retenção continuam condições separadas. Não houve contato externo ou ensaio físico.

## Reprodução e verificação

- `extrair_interfaces.py`: executado peloFreeCADCmd1.1.4, somente leitura. Confere volume, CG eBBox dos14 corpos retangulares com inventárioR51; fonteR52 eR51 com hashes preservados. O log registra avisos de cache/preferências do processo emsandbox; o JSON e a conferência de hashes confirmam a extração.
- `python calcular_caixa.py`: requerNumPy; cerca de1segundo nesta execução. Não lê/escreve modeloCAD.
- `python verificar_caixa.py`: lê os resultados sem importar o resolvedor; soma forças e momentos globais por corpo, verifica compressões, peso, cortes compartilhados e o contraexemplo de autoequilíbrio.
- [Verificacao_caixa.json](Verificacao_caixa.json):12 casos por corpo,54 cortes; maior resíduo4,7×10⁻¹²N e3,1×10⁻⁸Nmm. Esses resíduos verificam a aritmética do modelo, não suas propriedades físicas ausentes.

Fontes preservadas: [caminho traseiro anterior](../../P01/Caminho_superior_P03/README.md), [soco e apoios](../../P01/Apoios_ao_piso/README.md), [massa/equilíbrio global](../../P01/Massas_equilibrio/README.md). Dados desta entrega: [Geometria_interfaces.json](Geometria_interfaces.json), [Interfaces_nominais.json](Interfaces_nominais.json), [Resultados_caixa.json](Resultados_caixa.json). Nenhum ensaio de carga ou autorização de fabricação foi produzido.
