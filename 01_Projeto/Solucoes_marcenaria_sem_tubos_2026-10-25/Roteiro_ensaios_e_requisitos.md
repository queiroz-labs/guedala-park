# Prova da composição P15 e das ligações P04

25/10/2026. Roteiro nominal para preparar com oficina/fornecedor antes das chaves. **Ensaios ainda não executados.** O objetivo é substituir hipóteses de rigidez e composição por dados da montagem real. O roteiro comparativo não equivale a ensaio normativo completo ou liberação de fabricação.

## Composição da base da lavanderia

Comparar peças do mesmo lote e orientação: chapa18 simples; duas18 sem ação composta; duas18 com processo de composição proposto. O corpo de prova tem799×312 mm, com medidas e espessuras reais registradas. Preparar três exemplares de cada tipo ajuda a observar variação, sem constituir amostra de certificação.

Registrar fabricante, substrato, revestimento de cada face, espessura e massa de cada chapa. Para a peça composta, registrar preparo das superfícies, adesivo, lote, quantidade aplicada por área, pressão/distribuição de prensagem, tempo, temperatura, umidade e cura. O fornecedor deve confirmar compatibilidade dos substratos efetivos e uso pretendido; não especificar genericamente “colar duas BP”.

Fazer primeiro uma comparação de chapas em apoios idênticos nas extremidades; ela identifica diferença de rigidez entre composições e deslizamento. Essa montagem não reproduz o apoio traseiro e a caixa do cálculo. Depois testar a caixa nominal completa, com fundo, laterais, ferragens e suspensão em dispositivo de oficina que permita conhecer suas condições de apoio.

Na caixa, o topo da base mantém sua cota. A camada inferior acrescenta18 mm por fora. Conferir dimensões reais da composição e das laterais/fundo598 antes de montar. Verificar como acessar os Minifix da camada superior, sem supor que a caixa de montagem antiga sirva inalterada.

### Cargas e medições comparativas

- Medir vazio, após acomodar a montagem, e aplicar5,10,15 e20 kg distribuídos, pesados. Registrar distribuição e massa do dispositivo de aplicação;20 kg são conteúdo, além do peso próprio.
- Repetir o caso misto15 kg distribuídos +5 kg em área50×60 mm na região frontal central. Também conferir posições excêntricas pertinentes antes de definir um envelope de uso.
- Medir deslocamento da frente no meio do vão e em quartos de vão; medir centro da chapa, deslocamento dos apoios, abertura das juntas e deslizamento entre camadas. Separar movimento do dispositivo de ensaio de deformação do móvel.
- Registrar imediatamente, após30 minutos,24 horas e7 dias para comparação, e após descarregar/recuperar. Esses intervalos **não demonstram** o comportamento durante anos nem substituem um protocolo de fluência aplicável.
- Inspecionar descolamento, fissura, impressão local da carga, mudança de apoio e abertura de juntas. Registrar qualquer ocorrência e não aproveitar um número de flecha de uma montagem danificada para ajustar a rigidez do modelo.

A referência escolhida no cálculo é2,663 mm. O modelo reserva0,20 mm para desvios adicionais; essa parcela deve ser preservada na comparação, com condições de apoio e massa equivalentes. Um resultado favorável de curta duração não comprova resistência, durabilidade da composição ou capacidade da suspensão.

## Juntas P15 e P04

Os valores de1.000 N/mm são **requisitos de rigidez inicial**, não dados conhecidos das ferragens. A rigidez deve vir da relação força–deslocamento relativa entre as peças, descontando a deformação do aparelho. Informar método, resolução/calibração do instrumento, assentamento inicial, intervalo de ajuste e histerese; uma única leitura não determina K com confiabilidade.

| Entrada efetivamente usada | Escopo da hipótese |
|---|---|
| P15 base–lateral e base–fundo | 1000 inicial/500 na sensibilidade, por ponto |
| P15 fundo–laterais | 500 na sensibilidade por grupo extremo do fundo; não por parafuso |
| P04 junta inferior ou superior | 1000 inicial por posição; dois pontos dão2000 por grupo |
| P04 caminho inferior+superior | 500 inicial/250 na sensibilidade por ramo; dois ramos dão1000/500 no caminho da divisória |
| P04 referências do fundo em seu plano | 250 por referência no submodelo; não é rigidez adicional de uma junta física já creditada no caminho da divisória |

Antes de validar o conjunto, identificar juntas compartilhadas e acoplar sua deformação. Não aceitar duas provas independentes para somar rigidez de uma mesma ligação. [Auditoria dos eixos e referências P04](P04_auditoria_referencias.json).

| Montagem | Direção e requisito a verificar |
|---|---|
| P15 base–lateral | Cortante vertical nos dois sentidos, acomodação, retenção e efeitos locais dos Minifix na chapa composta. No caso misto de referência, cerca de89,7/22,7 N por ponto de cada lado |
| P15 base–fundo | Cortante vertical e retenção nos seis pontos; no caso misto calculado há valores positivos e negativos. Não contar um encosto como ligação bilateral |
| P15 fundo–laterais | Grupo completo e deformação do fundo; não multiplicar uma capacidade individual pela quantidade de parafusos. Geometria da cabeça junto à aresta traseira da lateral exige conferência |
| P04 base–divisória e tampo–divisória | O eixo proposto é vertical. A força que sustenta a base solicita principalmente **retenção axial** do parafuso e cabeça/apoio, além dos efeitos de prumo. Não classificá-la simplesmente como cortante. Conferir grupo de dois e caminho completo inferior+superior |
| P04 divisória–fundo | Transferência vertical e retenção no grupo; incorporar deformação das chapas e das demais juntas do caminho |
| P04 divisória dupla36 | Duas chapas18, furos e ligamentos próprios; a união entre elas deve ser demonstrada quando se pretende repartir esforços |

Para P04, a hipótese calculada é1000 N/mm **por junta e posiçãoy**; há dois pontos em cada grupo inferior e superior, portanto2000 N/mm por grupo. Em cada um dos dois ramos da divisória, duas juntas em série dão500 inicial/250 diferido; os dois ramos em paralelo dão1000 inicial/500 diferido para o caminho completo. O texto antigo1000 por grupo foi corrigido para corresponder à matriz, sem alterar resultados de força/flecha. Nenhuma equivalência no tempo foi medida. A solicitação máxima de cerca de25,6 N por ponto vale para o caso estudado, sem majoração e sem ser uma resistência exigível final universal. A caixa real deve demonstrar os caminhos compartilhados, inclusive com o fundo, sem duplicar rigidez de uma mesma junta.

O protocolo de resistência e seus fatores devem ser definidos para o móvel e aplicação reais. Não encerrar por “suportou a carga uma vez”. Registrar corpo de prova, deslocamento, modo de falha, ciclos/carga mantida e recuperação, distinguindo ensaio até o limite de uso de ensaio de resistência. Nenhuma pessoa deve servir como peso de teste da montagem.

## Conferência das operações antes do retalho

1. Medir a ferragem efetiva: diâmetro externo e núcleo, cabeça, ponta, comprimento útil e instrução de piloto.50 mm atravessando18 projeta geometricamente32 mm na receptora, sem garantir32 mm de rosca efetiva.
2. Conferir eixo no meio da espessura real e ponto de entrada. A recomendação EPF de70 mm dos cantos para parafuso na aresta foi usada no mapa, mas não valida automaticamente cabeça, escareamento ou borda da outra peça.
3. Conferir sequência de fechamento, ferramenta e possibilidade de manutenção. No P04, acesso inferior e superior e acabamento das cabeças devem estar resolvidos antes dos furos definitivos.
4. Fazer mapa das operações dos dois lados da mesma chapa. Pilotos opostos, pontas de broca e cabeças não podem ser tratados apenas como círculos de desenho.
5. Registrar a diferença entre coordenadas normalizadas do estudo e as origens de fabricação. Os74 marcadores atuais não são programa de usinagem.

## Registro e decisão depois do ensaio

Usar a planilha de registro simples desta pasta, anexando fotos e certificados/dados de lote. Atualizar E/composição e matrizes de acomodação somente com medições rastreáveis. Recalcular cargas excêntricas, caixa e suspensão; registrar quais hipóteses foram confirmadas ou rejeitadas. A adoção da base36 também depende da revisão da faixa externa18 mm maior por Elias.
