# Detalhamento construtivo dos móveis

14/10/2026 · Etapa 4 · Base R30 · Propostas para desenvolvimento com o marceneiro.

**[Abrir o caderno visual](Caderno_construtivo.html)** · [Estudo separado no FreeCAD](Estudo_Apoios_Banco_Cesto_R30.FCStd) · [Vista dos apoios](Apoios_propostos.png).

O avanço desta rodada é uma solução geométrica de apoio inferior para banco e cesto, mais a definição das interfaces de tampas, ferragens, manutenção e fixação dos armários. A R30 permanece intacta. O estudo tem 7 novos envelopes de apoio e cópias estáticas dos móveis; não contém controles de movimento nem peças prontas para corte.

## D01 Banco com apoio até o piso

A leitura da R30 confirmou frente e laterais até Z0, posterior começando em Z18 e divisórias começando em Z80 ou Z100. A proposta completa os trechos inferiores sob três divisórias e o posterior, sem inserir reforços dentro dos compartimentos. As prateleiras removíveis dos potes continuam sem função de suporte do assento.

O percurso de carga proposto é: **tampa fechada → bordas da frente/posterior e divisórias → apoios inferiores e ligações do corpo → piso nivelado**. Não repartir a carga igualmente entre apoios nem atribuir ao fundo, à dobradiça ou ao retentor resistência que não foi calculada.

| ID | Local e função | Envelope X × Y × Z (mm) | Ligação a detalhar |
|---|---|---:|---|
| B01 | Apoio sob divisória dos potes | 18 × 390 × 80 | União ao corpo e apoio/nivelamento no piso |
| B02 | Apoio sob base e divisória das bebidas | 18 × 390 × 82 | União ao corpo e apoio/nivelamento no piso |
| B03 | Apoio sob base e divisória da folha | 18 × 390 × 82 | União ao corpo e apoio/nivelamento no piso |
| B04 | Fechamento de apoio sob posterior | 1764 × 18 × 18 | União ao corpo e apoio/nivelamento no piso |
| C01 | Apoio inferior lateral 1 recuado | 18 × 580 × 98 | União ao corpo e apoio/nivelamento no piso |
| C02 | Apoio inferior lateral 2 recuado | 18 × 580 × 98 | União ao corpo e apoio/nivelamento no piso |
| C03 | Apoio traseiro sob base | 554 × 18 × 80 | União ao corpo e apoio/nivelamento no piso |

Nos apoios B02 e B03, o fundo existente de 18 mm fica entre o apoio inferior (Z0–82) e a divisória (Z100–400). Em B01, o apoio chega diretamente à divisória em Z80. B04 preenche o trecho Z0–18 sob o posterior. São encontros de apoio geométrico; o trecho de fundo em compressão, suas uniões e a estabilidade do conjunto precisam ser dimensionados.

**Montagem proposta:** montar e esquadrejar corpo/divisórias, ajustar os apoios inferiores aos respectivos eixos, unir mecanicamente os componentes e nivelar o conjunto antes de instalar as tampas. Usar ligações acessíveis para manutenção; posições e comprimentos de parafusos/cavilhas seguem o painel escolhido, não a caixa CAD. A proteção do piso e o nivelamento entram dentro da altura do envelope: não acrescentar pés ou calços e elevar o assento de 470 mm sem revisar as cotas.

O vão de conteúdo e a organização foram preservados no estudo. A resistência das tampas, especialmente a de 825 mm, não decorre desse apoio adicional: verificar flexão local, carga concentrada, bordas, abertura e uso por pessoas. Não há carga admissível de assento definida nesta entrega.

## D02 Tampas do banco e retenção

Adotar como direção de detalhamento **apoio perimetral para tampa fechada, giro traseiro e retenção independente na posição aberta**, com componentes comuns compatíveis com o espaço disponível. O retentor mantém a tampa aberta; não sustenta o assento ocupado. A dobradiça precisa reproduzir o eixo de estudo ou provocar uma revisão localizada do percurso.

| Setor | Tampa L × P × A (mm) | Almofada e uso | Interface crítica |
|---|---:|---|---|
| 1 Potes/travessas | 387 × 448 × 20 | Conjunto de giro inclui almofada de 50, com acoplamento por definir | Peso do conjunto completo e retenção; painéis internos retirados vazios |
| 2 Bebidas | 366 × 448 × 20 | Retirar almofada antes de abrir, rotina aceita | Preservar retirada diária da térmica |
| 3 Balde | 214 × 448 × 20 | Retirar almofada antes de abrir, rotina aceita | Não ocupar passagem da alça do balde |
| 4 Folha | 825 × 448 × 20 | Retirar almofada e apoiar nos outros setores; rotina ainda proposta | Não ocupar nicho 800 × 350 × 70 nem o recuo de 24 da folha |

Os 20 mm incluem toda a composição da tampa; não são chapa de 20 mais ferragem, reforço e revestimento. Juntas de estudo de 2 mm deixam 8 mm de contato sobre cada lado de divisória de 18; extremidades têm 17 mm, frente 18 e posterior 16. Vedação, batentes e acabamentos não podem consumir essas reservas sem revisão. A regulagem não deve ser obtida forçando a tampa contra o corpo.

**Ficha da ferragem a preencher:** referência e montagem do conjunto; eixo efetivo; volume em fechado/aberto; ângulo e retenção positiva; massa/centro de gravidade suportados; direção e acesso dos parafusos; liberação para manutenção; ausência de interferência com conteúdos e pega. Quantidade e esforços não foram escolhidos. Duas ferragens não implicam divisão igual da carga.

### Solicitação gravitacional da tampa

Sob a hipótese de madeira homogênea com densidade 750–900 kg/m³ e eixo na borda traseira, o centro fica a224 mm. O momento fechado é m × 9,81 × 0,224; durante o giro ideal, M(θ) = M(0) cos θ. Os números servem como entrada de seleção, sem massa de almofada/pega/ferragem, atrito ou impacto:

| Setor | Massa de madeira (kg) | Momento fechado (N·m) |
|---|---:|---:|
| 1 | 2.60–3.12 | 5.71–6.86 |
| 2 | 2.46–2.95 | 5.40–6.49 |
| 3 | 1.44–1.73 | 3.16–3.79 |
| 4 | 5.54–6.65 | 12.18–14.62 |

No setor1, somar a almofada/acoplamento e sua posição de centro de massa. Nos setores2–4, a rotina retira a almofada antes do giro. Não selecionar mola/pistão apenas por esses pesos. [Contas reproduzíveis](Solicitacoes_tampas.json).

## D03 Gabinete do cesto com base apoiada

A R30 tem laterais iniciando em Z98, base Z80–98 e rodapé frontal recuado50 até Z80. Os três apoios C01–C03 propostos dão continuidade inferior às laterais e apoio traseiro à base. Mantêm recuo frontal50, topo do gabinete900 e bancada920. A parte posterior em U da R29, com abertura450 ×602, permanece livre.

**Percurso de carga proposto:** armação/frente → conjunto comercial de pivôs e retenção → reservas estruturais laterais/base → novos apoios inferiores e rodapé existente → piso. Tanque e pedra precisam de apoio próprio ligado ao corpo; painel superior removível e frente basculante não devem servir de sustentação da bancada.

As reservas de pivô52 ×40 ×44 e pinosØ10 ×20 do modelo continuam ilustrações, não ferragens fabricáveis. A geometria de montagem de uma ferragem escolhida deve ser trazida para o modelo antes de furar. As faixas laterais de52 mm também são disputadas pela hidráulica/mangueira: não contar o mesmo espaço duas vezes.

**Sequência construtiva proposta:** base/apoios e laterais → ligações do posterior em U e conferência de esquadro → suporte independente do tanque/pedra → hidráulica acessível → articulação/frente e retenção → painel superior removível. O fundo em U exige verificar resistência a deformação lateral; não recolocar uma chapa inteira atravessando a hidráulica para obter rigidez.

## D04 Giro, retenção e manutenção do cesto

| Interface | Condição de detalhamento |
|---|---|
| Articulação | Eixo de estudo local Y70/Z120, correspondente a560 desde parede; abertura55°. Ferragem comercial pode exigir revisão do eixo/curso. |
| Limite de abertura | Batente mecânico positivo e retenção contra movimento descontrolado. Limite de software não substitui peça física. |
| Ligação da frente | Transferir esforço à armação nos apoios previstos, com fixação acessível; frente550 ×521 ×18. Não usar apenas o saco como ligação. |
| Painel superior |550 ×222 ×18, Z675–897; fixação removível acessível pela frente com conjunto sustentado. Não depender de cola definitiva para acesso ao sifão. |
| Desacoplamento | Armação deve poder ser retirada com suporte temporário e retenções liberadas de forma controlada; não puxar conjunto solto pelas ferragens. |
| Hidráulica | Preservar abertura do fundo em U e caminho da mangueira. Inspeção e manutenção não exigem retirar pedra/tanque. |

**Uso diário de estudo:** abrir55 → retirar saco445 → endireitar55; voltar em ordem inversa. **Manutenção:** afastar Loop650 para posição temporária proposta → retirar saco → sustentar conjunto → liberar/retirar painel e armação → manutenção → recompor e testar retenção → devolver lixeira. Deslocamentos do painel200 e da armação400 são percursos CAD; não especificam ferramentas, pega ou capacidade humana.

O estudo anterior de sensibilidade do cesto, com frente4,64 kg e conjunto armação/conteúdo de5/8/12 kg, tinha momentos de abertura a55 de17,95/21,27/25,69 N·m e mudança de sentido durante o giro. Essas massas são cenários, não carga útil escolhida. A ferragem deve ser validada com conjunto real, roupa e saco, cheio e vazio; a indicação de50 kg de outro produto não se aplica ao pivô ilustrativo.

## D05 Armários e ligações de montagem

| Conjunto | Direção construtiva | Dados para fechar |
|---|---|---|
| Aéreos | Fixação dimensionada ligada ao corpo/laterais ou travessa estrutural, com regulagem e acesso. Não depender da frente, prateleira removível ou fundo sem verificação. | Material e peso do móvel + conteúdo, suporte da parede, ancoragem, quantidade, resistência das ligações e espaço de montagem. |
| Folga ao teto | Conferir o movimento necessário para instalar/retirar o sistema de suspensão dentro da folga existente. | Escritório/cozinha20 e quarto30 são nominais; elevação de engate e irregularidades reais ainda desconhecidas. |
| Roupeiro e gavetas | Preservar recuo10 da frente à porta e curso500; escolher pega compatível com essa folga. Guias fixadas em material que suporte caixa + frente + conteúdo. | Pega, regulagem real, paralelismo, peso e fixação. Distância62 até a cama é cenário de uso, não corredor livre. |
| Maleiro de correr | Trilhos apoiados no corpo, retenção antidesencaixe e batentes acessíveis. | Aplicação real em folhas baixas/largas e referências de instalação; não converter a caixa de reserva em trilho fabricável. |
| Banheiro inferior | Corpo suspenso com fixação independente da pedra/frentes, acesso ao sifão e bordas protegidas. | Parede e carga, hidráulica real, recorte e vedação. Centro livre não demonstra passagem das conexões. |
| Espelhado | Espelho aplicado ao painel, com sistema de adesivo/retenção e espessura definidos pelo fornecedor; caneco permanece na madeira. | Massa real, camada de adesivo, arestas, montagem e ajuste da dobradiça; CAD hoje tem contato ideal vidro/madeira. |
| Prateleiras e apoios internos | Apoios removíveis com retenção adequada ao uso, sem interferir na passagem do conteúdo. | Painel, vão, carga, flecha, suporte e furação. Não atribuir carga pela área de contato. |
| Gaveta de piso | Rodízios e guias de retirada ligados à caixa; conservar frente e rodapé previstos. | Carga completa, altura, piso e apoio efetivo das rodas; não distribuir peso automaticamente por seis. |

As referências Blum já estudadas permanecem candidatas; a R29 registra56 dobradiças no cenário atual, com três por folha do aéreoC. Este caderno não faz nova seleção comercial nem repete uma calculadora de fabricante. Larguras de portas e juntas devem vir da R30, não das listas antigas R11/R28.

## D06 Informações para o marceneiro devolver

Para cada conjunto, pedir uma proposta que identifique: painel/material e acabamento; massa do conjunto e conteúdo de projeto; carga e uso previstos; desenho das uniões e furações; referência exata das ferragens e seus envelopes; apoios/nivelamento; tolerâncias e regulagens; sequência de montagem e de manutenção. Para o banco, incluir número de ocupantes/carga por assento, carga concentrada e verificação de flecha, sem inferir capacidade pela aparência.

Ensaios de recebimento a definir com o executor: estabilidade/esquadro e contato dos apoios; portas/gavetas nos percursos reais; retenção de tampas e cesto cheio/vazio; acesso ao sifão; retirada/reposição de peças removíveis; ausência de contato de ferragem, roupa ou conteúdos. Critérios e cargas de ensaio dependem do dimensionamento, não foram inventados nesta rodada.

## Conferência desta proposta

- Lidas42 peças selecionadas na R30 para a memória geométrica; o estudo separado copiou42 formas do banco e28 do cesto, incluindo conteúdos/reservas para confronto.
- Sete novos apoios comparados com as cópias: nenhum par apresentou sobreposição volumétrica de caixas; não houve necessidade de cálculo booleano nesses pares. Contatos de face são esperados e não demonstram capacidade.
- Giro ideal contínuo0–55 do cesto contra os três novos apoios: caixa móvel X20–570, Y máximo320. Separações conservadoras2 mm de cada lado e274 até apoio posterior. Nenhuma análise nova de pessoa, saco deformável ou ferragem real.
- Formas do estudo válidas e arquivo salvo; modelo R30 com hash preservado. Não repetidas auditorias gerais ou movimentos antigos sem relação com os novos apoios.

[Geometria lida](Geometria_atual.json) · [Verificação dos novos apoios](Verificacao_apoios.json). As dimensões dos apoios são envelopes de proposta incluindo eventual proteção/nivelamento, não lista de corte. A definição de material, ligações e capacidade permanece como próxima etapa do detalhamento.

## Fontes e precedência

[Banco R16](../Modelo_FreeCAD/02_Revisoes_e_estudos/Banco_R16_2026-10-14/README.md) · [Cesto R15](../Modelo_FreeCAD/02_Revisoes_e_estudos/Cesto_R15_2026-10-14/README.md) · [Manutenção R26](../Modelo_FreeCAD/02_Revisoes_e_estudos/Manutencao_R26_2026-10-14/README.md) · [Correções R29](../Modelo_FreeCAD/02_Revisoes_e_estudos/Correcoes_R29_2026-10-14/README.md) · [R30](../Modelo_FreeCAD/01_Atual/Consistencia_R30_2026-10-14/README.md) · [Roteiro de levantamento](../../04_Visita_ao_apartamento/Roteiro_R30_2026-10-14/README.md).

As novas soluções são propostas de construção, sem atribuir aceite ao usuário. O programa, os equipamentos escolhidos e as decisões de uso anteriores são preservados. Não houve solicitação enviada a terceiros.
