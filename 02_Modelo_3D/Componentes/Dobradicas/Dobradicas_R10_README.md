# Dobradicas comuns — R10

Apartamento atual · [Vista da pia aberta](Pia_portas_86_R10.png) · Detalhe isolado · [Montagem](Montagem_R10.json) · [Auditoria](Auditoria_R10.json)

A R10 incorpora a R09 e instala 24 dobradiças comuns 71B3550 com 24 calços 173H7100 nas doze portas dos seis pares: pia, aéreos A/B/C/D e lavanderia. Prioridade de Elias: simplicidade, ferragens comuns e manutenção fácil. Canto simples R04, nove gavetas R08, bandejas de 455 mm e nove gabaritos G2 preservados. Revisões anteriores conservadas. Todas as novas cotas e referências são propostas; nenhuma liberação de corte, furação ou compra.

## Montagem proposta

- Junta externa de 2 mm por módulo, central de 2 mm preservada. Cada folha perde 1 mm na borda da dobradiça em relação à R09. Larguras atuais por folha: pia/D 322; C 270,5; B 345,5; A 397,5; lavanderia 414,5 mm. Alturas e espessura de 18 mm preservadas.
- Recobrimento de 16 mm, caneco K = 5 mm, calço de distância 0. Caneco Ø35 × 13 mm, centro a 22,5 mm da borda. Eixos de caneco nas alturas 80 e H−80 do módulo. Esses furos são representação proposta, não gabarito liberado.
- Fileira de fixação do calço a 37 mm da borda dianteira da lateral (y = 57 no módulo); passo vertical de 32 mm. Posição deriva da referência convencional e do STEP. Parafusos, pilotos, material e capacidade de fixação ainda precisam de confirmação para o modelo exato de calço.
- Regulagem comum de profundidade de 0,5 mm proposta para compatibilizar a frente existente e o corpo. O guia publica regulagem −2/+3 mm. A regulagem deve ser conferida na peça real; não implica rebaixo ou ferragem especial.
- Duas dobradiças por folha como referência. A calculadora oficial recomendou duas para o cenário da folha C de 1016 × 271,5 × 18 mm, MDF 900 kg/m³ e puxador 0,2 kg: peso arredondado 4,7 kg. A folha final é 1 mm menor. Material, puxador e peso reais não foram confirmados; o resultado é uma referência, não pesagem.

Fonte oficial de planejamento: [Blum — dobradiça 110°](https://d2.blum.com/services/BEC003/clp0016-ma-679-bhk_ma_dok_bau_%24sml_%24aof_%24v2.pdf), cópia em `Fontes/Blum_110_planejamento.pdf`. O desenho de calço dessa página é referência convencional, não identificação exata do 173H7100. Prova da calculadora em `Fontes/Quantidade_C_BlUM.png` e parâmetros em JSON homônimo.

## Controles e conferência

No grupo **R10 - abrir portas comuns (Abertura em graus)**, selecione o controle `Abrir … esquerda/direita` e edite **Abertura**. Os nomes exatos estão no campo `control` de `Montagem_R10.json`. A propriedade homônima da folha é vinculada e somente leitura. Limite de estudo 86° por expressão; **não comprova o batente mecânico 70T3553**.

O movimento usa quatro barras reconstruídas pelos eixos dos sólidos oficiais, com corpos analíticos originais preservados em grupos de movimento. Os 144 componentes individuais de ferragem e as doze frentes são válidos. Resíduo máximo entre eixos articulados 1,29e−12 mm; referência do caneco 1,02e−12 mm. Esses resíduos conferem a reconstrução matemática, não a montagem física.

48 posições individuais (0/30/60/86° por folha) passaram na conferência externa com a madeira considerada. Três cenários de abertura simultânea no mesmo ângulo não tiveram interpenetração entre frentes. A varredura planar usa 173 posições por folha, passo 0,5°: as envoltórias amostradas dos 46 pares com alturas sobrepostas ficaram separadas. Menor separação projetada de envoltórias: 1,54 mm dentro do módulo e 2,59 mm entre módulos. São separações de envoltórias amostradas, não distância euclidiana mínima nem prova contínua ou de tolerância.

A proposta inicial com junta externa de 1 mm tinha somente 0,63 mm entre módulos na mesma comparação; ficou preservada como `Candidato_junta_externa1_R10.FCStd`, com seu relatório histórico. A proposta atual aumenta essa margem sem mecanismo adicional. Arquivos de tentativa com ciclo e base R09 são históricos e não são a revisão atual.

A R10 foi salva, reaberta e teve dois controles movimentados e retornados a zero. Todas as doze entradas estão em zero no arquivo canônico. `Reabertura_R10.json`. O detalhe da pia é uma vista estática aberta a 86°, separada do apartamento.

## Limites reais e próxima etapa

A fonte STEP já contém sobreposições internas entre componentes: por exemplo, corpos 0/1 com 5354,02 mm³; corpo 0/calço com 711,25 mm³; corpo 1/calço com 555,00 mm³, na fonte sem alterações. Com a regulagem proposta, os dois últimos contatos diminuem. Outros contatos internos variam com o movimento. `Contato_STEP_original_R10.json` e `Contato_interno_dobradica_R10.json` registram a comparação. **A causa não foi determinada.** Não eliminar esses volumes cortando ou deslocando ferragem arbitrariamente. A conferência externa da madeira não equivale a homologação do mecanismo por ausência de contatos internos.

Continuam pendentes: batente físico 70T3553 e sua sobreposição de fonte, fixação na madeira/parede, parafusos, carga real, tolerâncias, regulagens extremas, encontros com equipamentos e uso simultâneo com gavetas. Nenhuma prova de continuidade entre posições. As pequenas sobreposições MOVENTO/fundo R07/R08 seguem sem causa determinada.

Próxima etapa independente: apoios simples para folhas intermediárias do aéreo do escritório e da cabeceira, preservando envelopes/programa e vizinha/canto R04. Depois demais frentes ainda ilustrativas. Não voltar à articulação 79T8500. Não repetir auditorias de gavetas, bandejas, R04 ou R10 sem mudança relevante.

Reprodução: `../../../ferramentas/componentes/Dobradicas/montar_dobradicas.py`, `../../../ferramentas/componentes/Dobradicas/auditar_dobradicas.py`, `../../../ferramentas/componentes/Dobradicas/varrer_frentes.py`. O gerador cria uma revisão a partir da base R09; não reexecutar sobre o trabalho atual apenas para testar. O FCStd salvo se movimenta por expressões nativas sem precisar executar o gerador.
