# P01/P03 — equilíbrio da caixa completa e ligações compartilhadas

25/10/2026. **A caixa superior foi individualizada por painéis e o caminho nominal até os apoios foi fechado em equilíbrio, sem atribuir rigidez ou capacidade às juntas.** O avanço substitui a uniformização de toda a madeira sobre a base por forças próprias do topo, fundo, laterais e duas portas. Não é cálculo de deformação nem liberação da caixa18.

A R52 foi aberta em processo separado FreeCADCmd, apenas para leitura; hash preservado. Nenhum documento da GUI foi acessado. R52 e todos os estudos anteriores permanecem intactos. Soco e alongamentos continuam propostas separadas, sem tubos e sem integração automática.

## O que entrou no modelo

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

Um contracheque do topo torna a necessidade de ligação concreta. A800, o topoP03 pesa117,272N e tem CGY3606. O único apoio vertical puramente normal que suas faces fornecem, sem ações tangenciais nas ligações laterais, está sobre o fundo emY3922–3940. O CG fica316mm antes da borda mais próxima. Portanto faltam **ao menos37,058Nm de balanço** através de ações tangenciais/casal das ligações; isso não é o momento de uma dobradiça ou de um parafuso específico. Apenas encostar o topo ao fundo não resolve esse equilíbrio.

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

O próximo passo de projeto pode usar diretamente este mapa, sem novo levantamento do apartamento: definir uma topologia de juntas nas seis uniões lateraisP03 e na travessaP01, decidir se haverá ligação positivaP02↔P03 e obter/desenhar os grupos reais que transmitam os seis resultantes. Deve-se especificar origem da curva força–deslocamento e capacidade nas orientações reais; não atribuir uma mola por aresta e outra ao fundo como se fossem caminhos independentes.

Para calcular deformação, faltam a constituição/propriedades direcionais da chapa e a lei das juntas escolhidas. A extensão matemática para uma “caixa rígida” que eliminasse a flecha anterior seria inválida sem esses dados. Esta entrega não repetiu esse atalho. O formato do fundoP01, detalhamento de emenda se necessária, aparência do soco, nivelamento/piso e retenção continuam condições separadas. Não houve contato externo ou ensaio físico.

## Reprodução e verificação

- `extrair_interfaces.py`: executado peloFreeCADCmd1.1.4, somente leitura. Confere volume, CG eBBox dos14 corpos retangulares com inventárioR51; fonteR52 eR51 com hashes preservados. O log registra avisos de cache/preferências do processo emsandbox; o JSON e a conferência de hashes confirmam a extração.
- `python calcular_caixa.py`: requerNumPy; cerca de1segundo nesta execução. Não lê/escreve modeloCAD.
- `python verificar_caixa.py`: lê os resultados sem importar o resolvedor; soma forças e momentos globais por corpo, verifica compressões, peso, cortes compartilhados e o contraexemplo de autoequilíbrio.
- [Verificacao_caixa.json](Verificacao_caixa.json):12 casos por corpo,54 cortes; maior resíduo4,7×10⁻¹²N e3,1×10⁻⁸Nmm. Esses resíduos verificam a aritmética do modelo, não suas propriedades físicas ausentes.

Fontes preservadas: [caminho traseiro anterior](../../P01/Caminho_superior_P03/README.md), [soco e apoios](../../P01/Apoios_ao_piso/README.md), [massa/equilíbrio global](../../P01/Massas_equilibrio/README.md). Dados desta entrega: [Geometria_interfaces.json](Geometria_interfaces.json), [Interfaces_nominais.json](Interfaces_nominais.json), [Resultados_caixa.json](Resultados_caixa.json). Nenhum ensaio de carga ou autorização de fabricação foi produzido.
