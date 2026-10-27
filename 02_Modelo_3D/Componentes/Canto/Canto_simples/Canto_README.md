# Canto do aéreo do quarto — proposta simples R04

Nota de precedência documental na R28: esta pasta preserva a etapa R04. A vizinha atual foi substituída pela montagem R18 com71B3550; usar `ControleVizinhaR18.Abertura`, conforme o guia vigente, e não o antigo `ControleCanto.B4`. As portas A/B do canto continuam em `ControleSimplesR04.B2/B3`. A faixa25 foi preservada. Esta nota não altera o modelo histórico nem libera fabricação.

Elias definiu simplicidade, facilidade de manutenção e ferragens comuns como prioridades para todos os armários. A R04 propõe duas portas independentes e uma faixa fixa na quina. A faixa reduz o acesso frontal, mas permite abrir as portas em qualquer ordem no cenário conferido.

Modelo editável · [Fechado](Fechado.png) · [Ambas abertas](Ambas_86.png) · [Auditoria](Auditoria_simples.json)

## Proposta dimensional

| Elemento | Dimensão de estudo |
|---|---|
| Porta A e porta B | 271 × 306 × 18 mm cada |
| Faixa fixa da quina, lado A | 142 × 306 × 18 mm |
| Faixa fixa da quina, lado B | 124 × 306 × 18 mm |
| Juntas junto às faixas | 2 mm |
| Faixa junto à porta vizinha | 25 mm, recuada40 mm |
| Suportes das dobradiças | 18 mm |
| Canecos | Ø35, profundidade13, K4 mm |
| Dobradicas candidatas | 71B3550 com calço173H7100; duas por porta em estudo |
| Curso de estudo | 0–86°, limitador70T3553 candidato |

São cotas e ferragens propostas; não constituem aprovação de fabricação, corte ou compra. A seleção do número de dobradiças, fixação, peso e regulagem permanece em conferência. A abertura útil real deve descontar os elementos de apoio e dobradiças, além da largura nominal das folhas.

## Conferência

Vinte posições conferidas no FreeCAD, incluindo abertura de cada folha isolada, ambas simultâneas e uso da vizinha. Sem interseções acima de0,1 mm³ entre as frentes e os obstáculos considerados, ou entre24 componentes candidatos de ferragem e a madeira, nas condições testadas. A análise inclui base/tampo em L, fundos, suportes, faixas e peças próximas do maleiro.

Arquivo salvo/reaberto; controles editados e retornados ao estado fechado. Os29 componentes individuais ativos verificados (frentes, faixas, apoio e ferragens) têm sólidos válidos. Compostos de conjuntos articulados podem acusar invalidade por juntar sólidos em contato/sobreposição; não são peças únicas de fabricação. Duas geometrias antigas da79T8500 no histórico oculto também acusam invalidade e não pertencem à solução atual. Registro em `Reabertura_R04.json`.

As quatro barras de cada dobradiça foram reconstruídas a partir dos eixos cilíndricos coincidentes dos STEP. A planilha usa equações geométricas, não uma simples rotação em torno de eixo virtual. A varredura planar avaliou29.929 combinações de A/B por variante, em passos0,5° até86°. A redução escolhida de125 mm em cada folha, a partir de396 mm, produziu mínimo amostrado18,21 mm entre as duas frentes. Não foi demonstrada uma margem contínua com tolerâncias ou sob carga.

Comparação junto à vizinha testou33 condições nas faixas0/25/50 mm. A de25 passou com mais folga que a ausência de faixa. O modelo salvo e a auditoria de20 posições usam25 mm.

## Limitador: pendência distinta

A Blum indica70T3553 para limitar suas dobradiças110° a86° e orienta equipar todas as dobradiças da porta. A montagem ocorre com a dobradiça fechada, antes de encaixar a porta no calço, no espaço junto ao caneco. [Guia oficial de montagem](https://ea.blum.com/oeffnungswinkelbegrenzer/) e [catálogo oficial de acessórios](https://publications.blum.com/2024/catalogue/en/160/).

O STEP foi extraído na biblioteca, mas o encaixe ainda não está reproduzido na R04. O posicionamento original do STEP isolado não encaixa diretamente no conjunto71B3550 e não deve ser tomado como posição de instalação. O limite86° da planilha representa o curso pretendido: **não confirma o contato físico do limitador**. Confirmar gabarito/posição padrão antes da conclusão executiva.

Retomada noturna: [guia oficial detalhado salvo](Fontes/Blum_70T3553_montagem.pdf), conferido visualmente. O eixo do gancho do STEP do limitador coincide com o eixo d da dobradiça a4,4e−9 mm; a curvatura de apoio tem o mesmo centro do caneco. Sobreposições rígidas permanecem mesmo com esses referenciais coincidentes:86,71 mm³ com caneco e8,41 com braço, conforme `Limitador_diagnostico.json`. A causa não está determinada; não atribuir simplesmente a um deslocamento e não criar usinagem para apagar o resultado. Montagem comercial comum documentada, validação do encaixe físico ainda pendente.

## Edição

Abra `ControleSimplesR04`: B2 é A, B3 é B. B7 é o curso máximo do estudo. No arquivo histórico R04, a vizinha e a faixa ao lado dela eram controladas por `ControleCanto` (B4 eB5); para a vizinha vigente na R28, seguir a nota de precedência acima. O arquivo contém grupos R03 ocultos como referência; use o grupo `Canto R04 - portas independentes - proposta simples` para inspecionar a proposta escolhida.

R01/R02/R03 estão preservadas. `Candidato_apoio_extremidade.FCStd` e `Candidato_apoio_quinca.FCStd` são alternativas descartadas na conferência, pois mostraram colisões. O gerador atualizado está em `../../../../ferramentas/componentes/Canto/montar_canto_simples.py`. Os scripts de adaptação histórica não devem ser reexecutados na R04 atual.
