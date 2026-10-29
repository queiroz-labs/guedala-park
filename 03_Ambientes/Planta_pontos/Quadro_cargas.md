# Quadro de cargas — cenário nominal 127 V para RT

29/10/2026. Estudo documental; não é projeto elétrico. Usa a decisão F102 de 12/09 sobre aparelhos 127 V, sem deduzir a tensão entre fases nem a capacidade do prédio. **Não há dados suficientes para indicar disjuntor/seção final ou concluir que a instalação comporta as cargas.** Nenhum ponto, móvel ou FreeCAD foi alterado.

## Resultado calculável

- 36 linhas: 21 aparelhos/grupos de tomadas e 15 grupos de iluminação; **13 linhas sem potência de entrada**. O número de linhas não é número de circuitos nem de aparelhos físicos.
- Subtotal de referências: **6.740 W**, equivalente ativo de **53,07 A a 127 V e FP=1**, com simultaneidade 1. Não é demanda total, máximo garantido ou corrente de projeto: faltam cargas e fatores de potência; duas referências têm qualidade provisória.
- Separação: **5.355 W** de seis equipamentos com potência documentada + **264,2 W** do cenário de entrada da iluminação = **5.619,2 W**. Acrescentar ME23P **1.100 W** (referência comercial a confrontar com placa) e monitor ASUS **20,8 W** (limite de consumo publicado em condição não esclarecida, não máximo de placa) produz o subtotal acima.
- Lavagem LG 1.250 W e secagem 1.650 W são modos alternativos: entra **1.650 W**, não 2.900 W. A ficha é da família: placa do CV5012PC4 ainda deve confirmar.
- Forno 2.061 W → 16,23 A equivalentes; LG secagem → 12,99 A; airfryer 1.400 W → 11,02 A. O FP pode elevar a corrente; partida e harmônicas não estão representadas. Essas cargas exigem atenção específica do RT, não ligação automática em tomada de 10 A.

Dados completos em [entradas auditáveis](Cargas_entradas.csv), [cargas calculadas](Quadro_cargas.csv), [agrupamento proposto](Circuitos_cenario.csv) e [resultado/rastreio SHA256](Quadro_cargas_resultado.json). Célula vazia significa dado ausente, não zero.

## Hipóteses e cobertura

**H01:** simultaneidade 1 para as referências disponíveis, cenário de comparação sem fator de demanda inventado. **H02:** FP=1 apenas para converter W em corrente ativa equivalente, não corrente eficaz (RMS) medida; coluna FP=0,8 é sensibilidade arbitrária, não limite nem especificação. A iluminação mantém também sua sensibilidade FP=0,5 no CSV de origem. **H03:** uso a 127 V conforme F102; versões reais/bivolt a conferir. **H04:** todas as opções de climatização ficam fora da base. **H05:** grupos funcionais não comprovam circuitos existentes. Não se somam correntes de fases desconhecidas para dimensionar a entrada.

A fonte de inventário é [Lista_equipamentos.csv](../Equipamentos/Lista_equipamentos.csv), reconciliada com [ESTADO_ATUAL](../../ESTADO_ATUAL.md) e os registros vigentes de escritório. A relação antiga de dois AOC 27 foi substituída aqui por ASUS VG27AQ5A + AOC 24 existente; TV/soundbar atuais Philips 50PUG8100/78 e TAB4000/78. TV escritório Samsung UN43CU7700GXZD. Cadastros originais não foram reescritos neste bloco.

Cobertura dos 51 IDs: EQ01–10 incluídos; EQ11–20 hidráulicos sem carga elétrica prevista; EQ21 torre e EQ25 régua são interfaces, não consumo próprio; EQ22–24 e EQ26–29 incluídos, com EQ28 dividido nos dois monitores atuais; EQ30–43/EQ49–50 reconciliados com os 15 grupos de iluminação; EQ44 cabeceiras incluídas como carga ausente; EQ45 varal e EQ48 escada são mecânicos; EQ46–47 incluídos; EQ51 iluminação de prateleiras adiada. F80N é suporte mecânico. Um único PS5 aparece na sala; a transferência ao escritório altera o grupo de uso, nunca duplica o aparelho. Xbox e aquecedores elétricos alternativos não escolhidos não entram.

Fontes LED de 36 W são capacidade de saída, não cargas adicionais de 36 W. O CSV de luz já contém perdas/controle conforme H11 do estudo; cargas DC não são somadas novamente. O aquecedor a gás entra com 50 W elétricos, não com 33,7 kW térmicos. Potência acústica da soundbar/TV não é potência absorvida.

## Circuitos como opção, não implantação

O CSV propõe 13 grupos funcionais: dois de iluminação (úmidos/secos), forno, micro-ondas, LG, geladeira, aquecedor GN, airfryer, tomadas cozinha, lavanderia, sala, escritório e quarto. Separar geladeira/GN é opção de continuidade e identificação; tomada exclusiva no manual não prova exigência de circuito exclusivo. Esta divisão não confirma espaço no quadro, número de fases, reserva ou viabilidade dos eletrodutos.

O micro-ondas tem referência documental própria de **20 A, curva C**, preservada como instrução de manual a conferir pelo RT; sua potência provisória não permite reduzir essa exigência. Para o forno, tomada/plugue 20 A não foi transformado em disjuntor 20 A.

**DR:** opção de proteção adicional de 30 mA, especialmente nos grupos de cozinha/lavanderia/banho, sujeita ao levantamento do esquema de aterramento, compatibilidade das cargas, corrente de fuga, tipo de DR e coordenação. O CSV não define tipo AC/A/F/B nem corrente nominal do DR. O RT deve verificar abrangência obrigatória da edição aplicável da NBR 5410, incluindo banheiro e áreas laváveis. Não houve leitura integral licenciada da norma nesta execução; a tentativa de abrir a reprodução universitária falhou por timeout. Nenhuma conformidade normativa foi atestada.

O guia primário Prysmian baseado na NBR 5410:2004 traz mínimos mecânicos de cobre de **1,5 mm² para iluminação e 2,5 mm² para força/tomadas** (tabela 2, página impressa 5). O CSV os identifica como mínimos, mantendo seção final vazia. Falta método de instalação, isolação, temperatura, agrupamento, material existente, corrente de curto-circuito e percurso. Selecionar uma seção comercial a partir de P/127 seria injustificado.

Critérios de proteção: Ib ≤ In ≤ Iz e capacidade de interrupção compatível com o curto-circuito presumido. A corrente Ib dimensionante continua ausente, mesmo nos grupos com potência conhecida, pois FP e condições de uso/partida não estão completamente caracterizados. Não se escolheu disjuntor pelo arredondamento da corrente equivalente.

## Queda de tensão e entrada do apartamento

A planta de pontos possui coordenadas de marcadores, sem trajeto quadro–eletroduto–carga, distribuição em trechos nem origem do quadro. **Nenhum comprimento foi inventado a partir de distância reta ou perímetro.** Comprimentos, quedas e comparação com oferta ficam vazios em todos os circuitos.

O script implementa a expressão monofásica ΔU = 2·I·L·(R·FP + X·√(1−FP²)), com L em km e R/X em Ω/km, apenas para testar o método. Um teste sintético não é cálculo de circuito do apartamento. Referência de queda terminal de 4% no guia Prysmian (página impressa 20); o limite total depende da origem de alimentação e deve ser conferido pelo RT. Não se aplica automaticamente um único limite da entrada ao último ponto.

Disjuntor geral, alimentação por fases, capacidade dos condutores, padrão da concessionária e carga disponibilizada não estão identificados nas fontes consultadas. Logo, **demanda total, reserva e comparação com o prédio permanecem indeterminadas**. Também falta a previsão normativa de TUG/cargas mínimas por recinto: este inventário de aparelhos não a substitui.

## Climatização: cenários separados recebidos do bloco térmico

| Opção, nenhuma escolhida | Entrada nominal de resfriamento | Tensão do produto | P/V equivalente, não corrente de projeto |
|---|---:|---:|---:|
| LG S3-Q09AA31C 9 mil BTU/h | 780 W | 220 V | 3,55 A |
| LG S3-Q12JA33K 12 mil BTU/h | 1.130 W | 220 V | 5,14 A |
| LG S3-W18KL31C 18 mil BTU/h | 1.600 W | 220 V | 7,27 A |
| Ventisol Mistral DC, sem lâmpadas | 30 W | 127–220 V | manual 0,24 A a 127 V / 0,14 A a 220 V |
| Sem equipamento adicional | 0 W adicionais | — | — |

Dados completos em [opções de climatização](../Equipamentos/Climatizacao_opcoes.csv), mantidos pelo bloco térmico. A tabela acima é um recorte elétrico dessas alternativas, sem escolha de quantidade ou ambiente.

Os três splits não são alternativas de ligação direta a 127 V: não se calculou corrente fictícia P/127 para sugerir compatibilidade. Não há comprovação de 220 V na unidade. Não se adicionam as três opções entre si nem à base de 6.740 W; quantidade/ambientes não definidos. A convenção condiciona AC (art.58), conforme [impactos documentais](../../01_Programa_e_decisoes/Convencao_e_ata_impactos.md); não interpretar o resumo antigo de proibição como decisão atual. Dreno, tubulação, carga e localização de condensadora dependem das condições tratadas no bloco térmico, sem intervenção física.

## Conflitos e perguntas exatas

1. **Para construtora/RT, quando o documento estiver disponível:** qual é o diagrama do quadro desta unidade, com tensões fase–neutro/fase–fase, disjuntor geral, condutores de entrada, circuitos, DR/terra, capacidade disponibilizada e percursos/trechos? Sem isso não fechar alimentação, seções, proteções nem queda.
2. **Para completar o inventário:** quais são os modelos/placas da cafeteira Mondial, AOC 24, fonte/configuração do PC, carregador HP, liquidificador, sanduicheira e carregadores das cabeceiras? Confirmar potência absorvida da geladeira, TVs, soundbar, PS5/CFI e micro-ondas por placa/manual do SKU. Não substituir esses dados por potência de áudio ou consumo mensal.
3. **L10:** airfryer e cafeteira estão associadas ao mesmo ponto de 20 A. Como será a separação real e o circuito desse ponto? O cenário separa seus grupos para o RT estudar; não altera a planta nem prova capacidade de uso simultâneo.
4. **Banheiro:** o inventário de pontos elétricos mostra iluminação, mas não identifica claramente a TUG de serviço junto ao lavatório nem sua proteção. Onde consta no projeto elétrico entregue? Não foi criado aparelho fictício para preencher a lacuna.
5. **Climatização:** existe alimentação 220 V e infraestrutura compatível com o local de condensadora previsto na convenção? Nenhuma escolha de split é tomada aqui.

## Fontes e reprodução

Fontes locais: [equipamentos/manuais](../Equipamentos/README.md), [conferência 127 V](../Equipamentos/Conferencia_127V_e_folgas.md), [escritório](../Escritorio/README.md), [luz/correntes](../Iluminacao/Correntes_luz.csv) e [planta funcional](README.md). Os nomes de manuais por carga constam nas entradas; documentos originais permanecem em `09_Referencias/Plantas_e_manuais/Manuais/` ou na área Fischer indicada pelo inventário.

Fontes técnicas primárias consultadas nesta execução:

- [Prysmian, Guia de Dimensionamento, revisão 10](https://br.prysmian.com/sites/default/files/atoms/files/Guia_de_Dimensionamento-Baixa_Tensao_Rev10.pdf): critérios de dimensionamento, mínimos de seção e queda; base normativa histórica declarada no guia, não comprovação de edição vigente da norma.
- [Schneider, proteção de condutores](https://www.electrical-installation.org/enwiki/Practical_values_for_a_protective_scheme) e [queda de tensão](https://www.electrical-installation.org/enwiki/Calculation_of_voltage_drop_in_steady_load_conditions): relações de proteção e método; guia IEC não substitui NBR aplicável.
- [ASUS VG27AQ5A](https://www.asus.com/us/displays-desktops/monitors/tuf-gaming/tuf-gaming-vg27aq5a/techspec/), [Samsung UN43CU7700GXZD](https://www.samsung.com/br/tvs/uhd-4k-tv/cu7000-43-inch-un43cu7700gxzd/), [Philips 50PUG8100/78](https://acc.philips.com.br/c-p/50PUG8100_78/tv-led-4k-ambilight.support) e [TAB4000/78](https://www.philips.com.br/c-p/TAB4000_78/soundbar-com-som-estereo-20-aprimorado): potência ausente mantida ausente; tensão universal não implica consumo conhecido.
- LG [9 mil](https://www.lg.com/br/ar-condicionado-residencial/s3-q09aa31c/), [12 mil](https://www.lg.com/br/ar-condicionado-residencial/dual-inverter-split/s3-q12ja33k/), [18 mil](https://www.lg.com/br/ar-condicionado-residencial/s3-w18kl31c/); [manual Ventisol hospedado pelo distribuidor](https://www.leverosintegra.com.br/download/manuais/Ventisol/manual-ventilador-ventisol-de-teto-mistral-bivolt.pdf): modelo e entrada separados da capacidade térmica, evidências compartilhadas com o bloco térmico.

Reproduzir na raiz: `python -B ferramentas/estudos/quadro_cargas.py`; testar: `python -B ferramentas/estudos/test_quadro_cargas.py`. Sete testes verificam ausência versus zero, FP, necessidade de rota, unicidade do PS5, LG por modo, luz sem duplicação e ausência de dimensionamento automático. Sem preço novo, execução física, CAD ou publicação.
