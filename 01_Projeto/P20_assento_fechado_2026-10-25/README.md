# Banco P20 — tampas fechadas e caminho até o piso

25/10/2026 · leitura da R51 completa, sem alterar peças, cores, armazenamento ou movimentos. Continuação do [primeiro ciclo de cargas](../Cargas_e_ligacoes_R50_2026-10-25/README.md) e da [conferência dos mecanismos simples](../Banco_cesto_simples_2026-10-23/Conferencia/Resultado.md).

**As tampas podem ser estudadas sobre os apoios de madeira existentes, sem acrescentar tubos. A nova análise trata o assento fechado; não libera o banco para pessoas.** O requisito histórico de três pessoas de80 kg é cenário de projeto, não capacidade comprovada nem carga de ensaio normativo. As ferragens de abertura continuam sendo outra verificação.

![Contatos das duas tampas](Mapa_contatos.png)

## O que o modelo atual realmente apoia

São **18 contatos de face** entre tampas e corpo:12 na maior,6 na menor. Destes,10 pertencem às paredes/extremidades/divisórias e8 aos sarrafos de madeira18×126. A amostra de nove contatos do primeiro ciclo era selecionada, não o inventário completo; a conferência R45 já registrava os18 e foi reutilizada como comparação. A extremidade direita `Peca406AtualR31` também apoia a tampa menor.

O cálculo principal **não credita os sarrafos**: suas ligações ainda precisam de demonstração. Eles entram somente numa comparação adicional. Não se atribuiu carga de pessoa à piano ou aos articuladores: com o banco fechado, o caminho é tampa → paredes/divisórias → apoios inferiores → piso.

A leitura BREP encontrou42 interfaces internas de face nas21 peças selecionadas do corpo resistente. Há sete regiões nominais no piso, somando0,100764 m². Isso descreve geometria; não comprova distribuição no piso real nem resistência das juntas.

- Frente, lateral esquerda e extremidade direita chegam ao nívelZ0.
- Fundo começa emZ18 e tem o calço `Ref_Apoio_B04R31` até o piso.
- Primeira divisória termina emZ80 e encontra diretamente `Ref_Apoio_B01R31`.
- Divisórias seguintes terminam emZ100 sobre a base18; os apoiosB02/B03 chegam aoZ82 sob essa base. A compressão atravessa a base; não é uma divisória suspensa apenas por parafusos.
- As divisórias começam emX140; o fundo termina emX118. Existe separação de22 mm entre eles. Não inventar uma união traseira direta ou contar com ela para travamento lateral.

## Constituição e hipóteses da chapa

O envelope visível das tampas continua **448×971×20 e448×825×20 mm**. A direção histórica de compensado estrutural18 com acabamento contido nos20 é preservada como requisito de fornecimento. O cálculo usa **núcleo mínimo17,1 mm**, sem creditar acabamento na rigidez. Não se tratou a caixa20 do CAD como20 mm de madeira estrutural.

Ritz de placa fina, ν=0,30 e **E isotrópico equivalente5500 MPa** são hipóteses de comparação. O fornecedor deve informar rigidez nas duas direções, cisalhamento/torção, orientação e composição reais. Dois valores de MOE publicados para um compensado não bastam para atribuir automaticamente esta matriz isotrópica. A verificação final deve usar a ortotropia do painel escolhido.

Contatos permitem apenas compressão e podem se separar. Linhas discretas ficam no centro das faces nominais, sem engaste. Os apoios do corpo são rígidos nesta etapa; acrescentou-se **reserva de0,20 mm** para seu assentamento, que é requisito a comprovar. Desnível/tolerância podem mudar quais apoios encostam. Massa própria é uma aproximação do volume acabado×900 kg/m³, sem pesagem ou composição real.

## Resultados da triagem

Massas aplicadas em regiões200×200 mm, herdadas do estudo anterior. Sem atribuir à almofada distribuição adicional. E equivalente5500; valores abaixo incluem a reserva de0,20 mm do corpo.

| Cenário | Flecha + reserva |
|---|---:|
| Maior:80 kg no centro do setor dos potes | 0,609 mm |
| Maior:80 kg próximos à frente desse setor | 0,460 mm |
| Maior:duas regiões de80 kg | 0,519 mm |
| Menor:80 kg no centro | 1,014 mm |
| Menor:80 kg próximos à frente | 0,705 mm |

São posições determinadas, não busca de todos os carregamentos possíveis. Referência interna:2 mm, herdada do pré-dimensionamento; não é limite de norma citado nem certificado. O comportamento da placa em duas direções explica diferenças em relação à antiga viga-faixa200 mm.

**Sensibilidade que impede substituir por MDF sem verificar:** no centro da tampa menor, E equivalente2200 dá aproximadamente2,236 mm com a reserva; E2750 dá1,829 mm. Esses números são hipóteses, não propriedades atribuídas ao produto real. No cenário frontal menor, creditar os sarrafos perfeitamente apoiados reduz0,705 para0,558 mm, mas exige fechar suas juntas; isso não justifica retirar peças do projeto.

No caso simultâneo de duas regiões80 na maior e uma80 central na menor, a primeira divisória recebe aproximadamente839 N. Limitar seu caminho de apoio a0,20 mm exige rigidez equivalente de grupo próxima de4197 N/mm. Não dividir esse número por parafusos nem chamá-lo de capacidade. O [arquivo do caminho de cargas](Caminho_e_massas.json) contém todas as reações e requisitos de grupo; corpo, base transversal, apoios inferiores e contato real ainda precisam de verificação.

## A massa global precisa ser atualizada

O orçamento histórico de60 kg de carga permanente não pode ser mantido como limite garantido. Foram separados27 volumes conhecidos:21 do caminho resistente, quatro painéis adicionais/prateleiras/divisória e duas tampas. A sensibilidade por densidade e as exclusões estão no [levantamento de massas](Caminho_e_massas.json). Almofadas, ferragens e objetos guardados têm massas próprias a acrescentar, sem usar a densidade da madeira para esses itens. Recalcular também estabilidade e esforços globais com essa lista real, sem reaproveitar a antiga aprovação numérica do pórtico.

| Densidade uniforme hipotética nos27 volumes | Massa aproximada |
|---|---:|
| 650 kg/m³ | 55,436 kg |
| 800 kg/m³ | 68,229 kg |
| 900 kg/m³ | 76,757 kg |

Não são três produtos selecionados nem massa medida. O envelope acabado das tampas precisa ser decomposto nas camadas reais para evitar somar acabamento duas vezes. O [históricoR02](../Sala_e_jantar/Retirada_ponta_R30/Materiais_ligacoes_trava_R02.html) fornece a origem do requisito de núcleo17,1/E5500; pórtico e bandeja descritos naquela página não são a montagem vigente.

## Dados exatos para fechar, sem esperar o apartamento

1. **Fornecedor do painel:** qual produto/lote, número e direção das lâminas, espessura mínima do núcleo e composição do acabamento nos20 mm? Quais D11/D22/D12/D66 ou propriedades Ex/Ey/Gxy/νxy correspondem à espessura e condição de umidade escolhidas? Quais resistências de cálculo e critérios de obtenção, em vez de apenas MOR médio?
2. **Oficina:** como garantir coplanaridade dos10 apoios principais, apoio contínuo sob a base nas divisórias2/3, calço do fundo e contato nivelado dos sete apoios inferiores? Como medir e registrar a deformação de cada caminho de grupo e o esquadro da caixa sem creditá-los como rígidos por conveniência?
3. **Ligações e uso:** fechar contenção lateral/racking e juntas dos sarrafos, confrontando a posição dos fixadores com jarra, potes e prateleiras removíveis. O padrãoM6 antigo teve interferências identificadas; não é lista de furação liberada. Não acrescentar metal como contorno da decisão sem tubos.
4. **Ferragens:** manter as [perguntas de Bigfer, piano e pivô](../Banco_cesto_simples_2026-10-23/Conferencia/Consulta_tecnica.md). O resultado do assento fechado não valida terminais, retenção aberta ou capacidade de articulação.
5. **Protótipo:** executar o [roteiro conjunto banco/cesto](Roteiro_banco_cesto.md) somente após definição do conjunto e plano de ensaio pelo responsável. Nenhum ensaio físico foi executado nesta etapa.

## Evidências e reprodução

[Geometria e contatos](Geometria_R51.json) · [resultados e convergência](Resultados.json) · [verificação](Verificacao.json) · [extração FreeCAD](extrair.py) · [cálculo](calcular.py) · [fechamento e massas](fechar.py).

No FreeCAD com a R51 aberta, executar `extrair.py` com `runpy.run_path`. Depois, com Python/NumPy/Pillow: `python calcular.py`, `python fechar.py` e `python desenhar.py`. Convergência dos cinco cenários principais com graus14/18 e conferência de forças/momentos, contato unilateral e linhas intermediárias. A soma de reações não comprova resistência local, fadiga, impacto, esmagamento, fixadores, estabilidade ou desempenho do produto real. R51 não foi salva nem modificada por estes scripts.
