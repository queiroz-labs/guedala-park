# P04/P15 — suspensão da caixa inteira e portas abertas

25/10/2026 · continuação do plano, sem tubos. **A demanda global de suspensão agora inclui caixa, portas em quatro barras e conteúdo.** Os resultados são solicitações estáticas a fornecer ao projetista da suspensão; não constituem capacidade da parede, do móvel ou de uma ferragem. R51 e seus controles permaneceram intactos.

O cálculo de flecha das bases continua nos [estudos de marcenaria sem tubos](../../Ligacoes_sem_tubos/README.md). Este bloco fecha outra conta: conteúdo → caixa → resultantes de suspensão → parede. A força num parafuso interno da base não é a mesma força no grupo que sustenta o móvel inteiro.

## Geometria e massa usadas

- **P04:** caixa1800×230×308, base1764×212, quatro portas306 de altura. Foram usados os sólidos atuais com canecos descontados e as quatro divisórias18 separadas. A pequena faixa de proposta visível entrou apenas na massa, sem crédito de apoio resistente.
- **P15:** caixa835×330×580, base799×312, duas portas414,5×578. A variante de estudo acrescenta a segunda camada18, laterais598 e fundo598; topo interno da base e armazenamento continuam preservados como no estudo separado.
- **P04 de estudo:** substitui somente o fundo272 pelo fundo308 na massa global; faces/dimensões da caixa e demais peças mantidas.

Comparadas densidades650/800/900 kg/m³. Como hipótese de massa, os volumes nominais18 do BREP foram escalados por18,3/18, aproximando a tolerância de espessura usada no primeiro estudo. Não é medida real, dimensão de corte ou produto escolhido. Acabamento, adesivo, suspensores, conectores e dobradiças ainda precisam de massas/posições reais e reconciliação para evitar duplicar camadas.

| Caso aρ900, conteúdo nominal incluído | Geometria atual | Variante de estudo |
|---|---:|---:|
| P04 com10 kg de conteúdo | 45,163 kg | 46,209 kg |
| P15 com20 kg de conteúdo | 49,521 kg | 54,533 kg |

O reforço P15 acrescenta aproximadamente5,012 kg nessa hipótese. Melhorar a rigidez da base aumenta a carga suspensa; essa carga adicional não pode desaparecer da conta da parede.

## Portas: reutilização do movimento existente

Não foram substituídas as dobradiças por uma rotação simples em torno de um pino. As três planilhas de quatro barras e expressões das seis folhas foram copiadas para um documento temporário próprio, sem copiar o modelo inteiro. Foram calculados87 estados por folha,0–86° em passos de1°. Os centros fechados conferiram com os sólidos atuais; os controladores originais continuaram em0° e o documento temporário foi fechado.

A distância máxima amostrada do centro da porta à face traseira foi457,345 mm no P04 e543,521 mm no P15. Foram combinadas aberturas independentes0/86°, estado45° e extremos amostrados de centro de massa. **86° é o curso de estudo existente, não um batente físico comprovado**, e a amostragem não certifica um envelope contínuo nem colisões da ferragem.

P04 mantém10 kg totais, com5/2,5/2,5 nos três trechos já estudados. P15 usa20 kg totais. Além da distribuição central, foram analisados centros na faixa frontal e perto de cada extremidade como sensibilidades; não são cargas de uso liberadas. As variantes de conteúdo extremo não substituem a verificação local da base para aquela distribuição.

## Resultantes na parede

![Binário de tração e compressão](Binario_suspensao.png)

Para a gravidade conhecida:

`V(N) = soma(m(kg) × g)`; `M(Nm) = soma(m × g × v(mm) /1000)`; `T(N) = 1000 × M(Nm) / h(mm)`.

V é a força vertical total; M é o momento de tombamento para fora da parede; T é a tração total superior equilibrada pela compressão inferior. **h é a distância entre resultantes do binário**, não uma furação já definida. Foram comparadosh100/200/272 no P04 eh200/400/544 no P15; verificar se o produto e a caixa conseguem realizar a geometria escolhida.

O plano de reação foi tomado na face traseira nominal da caixa. Revestimento, folga ou afastamento real não foram medidos. Se o sistema introduzir um afastamentoe emmetros, o momento emNm cresceV×e; recalcular a geometria, sem afastar o móvel silenciosamente para encaixar uma ferragem.

Dois grupos superiores recebem V conforme o centro de massa lateral, com vão entre resultantes de100% ou80% da largura da base. As posições são parâmetros de equilíbrio, sem centros de broca. A partilha de T entre lados depende da rigidez e do caminho dentro da caixa; foram comparados100/0,50/50 e0/100. Em cada lado, a compressão inferior correspondente fecha o binário. Esse modelo pressupõe capacidade de transmitir torção entre lados; não prova que as juntas reais já o façam.

| Variante de estudo,ρ900 | Portas | Conteúdo | V total | M | T total para h indicado |
|---|---|---|---:|---:|---:|
| P04,h200 | Fechadas | 10 kg distribuídos | 453,157 N | 55,992 Nm | 279,960 N |
| P04,h200 | Todas86° | 10 kg distribuídos | 453,157 N | 74,582 Nm | 372,910 N |
| P04,h200 | Todas86° | 10 kg frontais | 453,157 N | 82,525 Nm | 412,627 N |
| P15,h400 | Fechadas | 20 kg distribuídos | 534,787 N | 92,596 Nm | 231,491 N |
| P15,h400 | Ambas86° | 20 kg distribuídos | 534,787 N | 108,178 Nm | 270,445 N |
| P15,h400 | Ambas86° | 20 kg frontais | 534,787 N | 133,871 Nm | 334,678 N |

São forças sem majoração, mãos, puxões, choques ou massas de ferragens ainda ausentes. Não são limites admissíveis. Aumentar h reduz T, mas não dispensa resistência das peças, compressão na parede, acesso e geometria do suspensor.

No conjunto amostrado, com vão80% e toda a tração num lado, as maiores resultantes num grupo superior são aproximadamente **500,79 N no P04,h200**, e **504,66 N no P15,h400**. Cada valor vem de um caso identificado no JSON, combinando seu cortante e tração; não se somaram máximos incompatíveis de casos diferentes. Para h100 no P04 e h200 no P15, os correspondentes envelopes chegam872,68 e768,58 N. O grupo não equivale a um parafuso: distribuição entre fixadores, efeito de alavanca, bordas, material e interação cortante/tração exigem projeto próprio.

## O que precisa ser resolvido com produto/oficina

1. **Suspensor completo:** qual código, desenho, faixa de ajuste, caminho de fixação à madeira18, espaço ocupado por dentro e por trás, distância efetiva h e vão horizontal entre grupos? A comparação anterior da [suspensão](../../Inventario_dimensional/Inventario/Ferragens_fixas.md) continua válida: não inserir o SAH215 como se existisse a reserva posterior16 mm, que a caixa não tem. Este cálculo não escolheu outro conjunto.
2. **Capacidade combinada:** o fabricante admite os vetores simultâneos V/T, a excentricidade e o esquema de instalação deste móvel? Informar forças, posições e caso; não comparar apenas o peso total com dois números emkg de catálogo. Exigir também retenção contra desengate e fixação do trilho, se houver.
3. **Caixa até o suspensor:** mostrar como base, fundo, tampo, laterais e divisórias recebem os grupos calculados. Demonstrar torção quando um lado recebe a retenção maior, tração nas juntas e compressão inferior. Os estudos de rigidez das juntas não são resistência publicada.
4. **Massa completa:** pesar/identificar componentes fixos e móveis e seus centros; usar as trajetórias próprias dos braços de dobradiça. Uma massa adicional1 kg aumenta V em9,807 N e M em9,807×v(m) Nm; seu acréscimo a T depende de h. Não pôr toda a ferragem no centro da porta.
5. **Parede e trilho:** antes do corte final, identificar substrato, espessura, revestimento, instalações e condição real. Escolher ancoragem conforme esses dados e o conjunto de forças; **nenhuma bucha ou profundidade foi inventada**. Substrato é dependência do imóvel; desenho do suspensor, fixação na caixa e protótipo podem avançar antes das chaves.

Preservar profundidade, armazenamento, posição, acabamento e portas. Qualquer solução que exija afastar a caixa, ocupar vãos ou alterar faces precisa de estudo separado; nenhum quadro metálico foi usado para contornar a preferência sem tubos. Nenhuma compra, consulta externa ou fabricação foi executada.

## Evidências e reprodução

[CG e trajetórias extraídas](Geometria_e_portas_R51.json) · [660 casos globais e72 envelopes paramétricos](Resultados.json) · [cálculo](calcular.py) · [verificação](Verificacao.json).

Identificada [correção textual de metadado](Metadado_a_reconciliar.json): o campo de movimento da porta vizinha ainda cita441,75 de largura, enquanto a peça atual mede440,25. O cálculo usa o sólido atual. Correção preparada para consolidação, sem alterar formas ou controles nesta etapa.

Executar`extrair.py` no FreeCAD com R51 aberta e folhas fechadas; a etapa das planilhas pode levar alguns minutos. O script cria e fecha somente seu documento temporário. Depois`python calcular.py` e`python verificar.py`. As etapas numéricas reutilizam as trajetórias salvas e não precisam reabrir o projeto. Conferidos massa constante durante a abertura, centros fechados, altura invariável das folhas, equilíbrio e escala1/h, SHA256/CRC da R51. Zero ensaios físicos e nenhuma capacidade real liberada.

**Continuidade mais rápida:** [motor de cinemática fora do FreeCAD](../../../ferramentas/cinematica/README.md), validado com estas522 poses e seis complementaresR12. Usar nos próximos estudos; não repetir a extração pesada de planilhas para consultar outra abertura das mesmas folhas.
