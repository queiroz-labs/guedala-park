# Furação relativa às peças — nominal/proposta

| Entrega | Consulta |
|---|---|
| 249 IDs, 20 móveis | [Índice por peça e face](index.html), CSV `Pxx-coordenadas.csv` |
| Conectores dos 20 móveis | [Mapa por encontro](Mapa_conectores.csv) |
| Dados ausentes e operações descritivas preservadas | [Pendências](Pendencias.csv) |
| Dimensões e acabamento por ID | [Painéis](Paineis.csv) |
| Contagens e SHA256 das fontes | [Resumo](Resumo.json) |

Gerar: `python -B ferramentas/estudos/gerar_furacao.py`. Entradas alternativas: `--pecas DIR`; saída de ensaio fora do projeto: `--saida DIR`. Biblioteca padrão, sem abrir FCStd. Cada CSV usa `;`, UTF-8 com BOM, mm; vazio significa **parâmetro a confirmar**, nunca zero. `situacao` distingue posição proposta de usinagem incompleta. 2.286 centros com Ø/profundidade preenchidos, todos em situação **catálogo de referência, SKU a confirmar**. Não equivalem a programa de máquina: 203 passagens Confirmat ainda exigem perfil/batente de escareado Ø10, além das operações sem centros. Há centros em 145 peças; 104 ficam sem centros, com pendências por ID. Cobertura de inventário não equivale a cobertura completa de usinagem.

## Origem e parâmetros

- Carcaça: canto mínimo dos eixos C/L identificados no campo `origem`. A na menor coordenada da espessura e B na maior; B conserva os eixos, sem espelhamento de vista. `topo-C0/C1/L0/L1`: canto da aresta; x ao longo da aresta, y pela espessura desde A. `gx/gy/gz` e normal para dentro da chapa permitem confrontar pares e trajetórias em 3D nominal.
- Portas: origem e eixos específicos do mapa histórico de canecos; x na largura, y na altura. A interna. Não confundir C (maior dimensão de corte) com largura da porta. Centros mantêm margens de borda inferior/superior; intermediários redistribuídos. Conferir mão e fita na primeira folha.
- Contatos: recomputados com caixas já exportadas em `Geometria.json`, somente peças atuais retangulares, estacionárias e correspondentes aos CSVs. Não se abriu o modelo. São **218 contatos**, distintos dos 171 históricos e dos 80 contatos R00; não somar as listas. Cada contato tem um ID, dois painéis e sua condição. Contato não comprova necessidade nem resistência da ligação. Peças especiais, gavetas, tampas e interfaces ausentes ficam na lista de pendências.
- Regra R00: dois até 400 mm, três até 700 mm, `ceil(contato/350)+1` acima. Mantida a implementação vigente de R00. Demais encontros candidatos usam Minifix, fundo usa Confirmat; face a face exige detalhe próprio. Quantidade condicional não é compra. Quantidades históricas de 52 Minifix não são somadas ao novo mapa: a comparação será explícita.
- Distribuição proposta: recuo 60 mm; reserva adicional 32 mm para cavilha. Passo `(contato−152)/(n−1)`. Pilotos na face oposta de divisória deslocados16mm **junto com o par**; cavilha fica32mm após o conector (P20 J019:20mm). Correções locais por junta: P04 J004/J006 +16mm; P07 J002 −24mm e J005 −8mm. Todos são deslocamentos ao longo da linha de conectores. São parâmetros de projeto, não exigência de catálogo; verificar conflitos antes de adotá-los.

O arquivo [regras dimensionais](../Dependencias/regras.json) governa envelopes, não o C×L de cada peça. O gerador relê os CSVs a cada execução. Se uma mudança perder a correspondência com a topologia exportada, registra pendência em vez de esticar caixas e inventar alinhamentos. A regeneração completa depende de reexportar a topologia das peças alteradas; essa dependência permanece explícita. Não há promessa de recalcular automaticamente painéis a partir de paredes ou tetos.

## Fontes e limites de catálogo

- Blum 71B3550 parafusada: [catálogo p.76](https://publications.blum.com/2024/catalogue/en/76/); caneco e flange [p.77](https://publications.blum.com/2024/catalogue/en/77/). Canecos 35×13 dos mapas documentais; padrão da flange 45/9,5. Pilotos 2,7×8, broca M01.ZZ03.01 e parafuso 609.1500: [p.160](https://publications.blum.com/2024/catalogue/en/160/).
- Base 173H7100 [p.152](https://publications.blum.com/2024/catalogue/en/152/): 37 mm da frente **do apoio**, dois centros ±16 mm da linha montada. ID/face e transferência da porta ao apoio continuam pendentes; não criar furos no apoio errado.
- Minifix15: Häfele262.26.034 para18mm, Ø15×13,5 (+0,5 de tolerância do catálogo), A9; [p.294](https://files.hafele.co.uk/catalogfiles/www/14CFC294.pdf). Pino S100262.28.920, rosca8, B34 e passagem **Ø7 em todo o mapa**, [p.299](https://files.hafele.co.uk/catalogfiles/www/14CFC299.pdf). Topo Ø7 até centro B34. Piloto direto Ø5×8,5: batente **derivado**, rosca8+0,5 de fundo proposto, não profundidade tabelada.
- Confirmat7×50: referência Häfele264.42.190 [FF2.45](https://hafelethailand.com/wp-content/uploads/2025/12/02-connector-technology-shelf-supports.pdf). Broca001.22.485 [p.416A](https://files.hafele.co.uk/CatalogFiles/www/14CFC416A.PDF): primeiro estágioØ5 cego no topo; segundoØ7 passante na face; escareadoØ10 na **face exterior**, oposta ao contato. Topo35mm é batente proposto `50−18+3`, com3mm de fundo para ponta; a página não tabela esse batente. Face18mm passante intencional, sinalizado no CSV; continua reprovando qualquer outro furo cego com reserva≤3mm. **Perfil/ângulo e batente do escareado permanecem parâmetros a confirmar nos203 pontos**, não se inventou profundidade numérica para essa suboperação.
- Cavilha8×30: Häfele267.82.230 [FF2.55](https://hafelethailand.com/wp-content/uploads/2025/12/02-connector-technology-shelf-supports.pdf). Método de partilha: guia oficial Wolfcraft *Wood joints* p.6, disponível em [Wood Joinery](https://www.wolfcraft.com/en/diy-projects/hobby-workshop/wood-joinery): face até2/3 da chapa; restante no topo+2–3mm para cola. Proposta calculada em18mm: faceØ8×12, topoØ8×20, soma32 para cavilha30+2 de folga. É método aplicado ao catálogo dimensional, não receita Häfele específica para MDF. Material da cavilha, cola e ajuste da broca precisam do SKU/oficina.
- Corrediças FGVTN500 e MOVENTO400: referências longitudinais e páginas permanecem em Pendencias.csv; faltam ID/face/alturas e seção de montagem suficientes para centros completos. Não atribuir profundidade de caneco a corrediça.
- Espelheiro: oito furos Ø5 nos níveis documentados 244/488 e recuos 20/86; profundidade 8,5 proposta. Não são linha System32. Passo32 de uma linha nova exige início/fim e recuos; não converter prateleiras fixas em removíveis para preencher tabela.

Os SVGs têm uma face por arquivo e lista de centros/IDs; círculo tracejado representa Ø ainda desconhecido. O site usa sua lista explícita de documentos e ativos; esta entrega é incluída nessa lista, sem substituir os CSVs descritivos R15.

## Escopo preservado

Suspensão de aéreos, ancoragem, cargas de uso, teto, micro-ondas T05 e rodízios P08 não foram refinados. Perguntas de oficina/RT permanecem nas fontes. Não houve leitura nem alteração do FreeCAD. A pasta `06_Entregas/Fichas_fabricacao/Execucao_ate_07h_2026-10-25/` foi apenas sinalizada ao usuário; não apagada nem movida.

## Conferência e montagem

[Relatório e dez ocorrências prioritárias](Conferencia.md) · [todas as ocorrências](Conflitos.csv) · [distâncias por par](Distancias.csv) · [portas e dobradiças](Portas.csv) · [sequência proposta dos 20 móveis](Montagem.csv).

Executar `python -B ferramentas/estudos/conferir_furacao.py`: **0 conflitos geométricos e37 restrições de acesso**, resultado REPROVADO. [Antes/depois](Antes_depois.json): antes3 sobreposições/distâncias+43 acessos; ao completar as profundidades aparecem mais20 cruzamentos; depois de corrigir somente parâmetros, sobram os37 acessos. Não somar restrição de ferramenta a interseção de madeira nem supor que todas foram resolvidas. Quatro portas P04 continuam fora da orientação do gráfico Blum. Treze testes em `python -B ferramentas/estudos/test_furacao.py` incluem passagem intencional sem exceção genérica e integração dos pares.

P20 F02009 em PecaBancoR16 passa de(1730;92) para(1730;76); F01978 fica(1720;91), distância nominal entre bordas6,53mm. A distribuição dos pares e cavilhas foi conferida novamente. P17 tinha **oito**, não43, acessos em ApoioComumR001/ApoioOpostoR18. Os corpos passam das faces encostadas para as opostas livres (pino permanece A9): unir o par de divisórias, apresentar horizontais, apertar pelas faces livres, fechar fundo e instalar frentes por último. **Proposta com aparência/tampas a confirmar**, sem mudar peças. Se o corpo nessas faces não for aceito, alternativa é Confirmat+cavilha/cola nas quatro juntas; não foi adotada automaticamente.

Nos demais móveis, Montagem.csv lista os37 apertos que antecedem gavetas/travessas/fechamentos. A sequência é proposta parcial: encaixe, estabilidade e retirada da ferramenta exigem montagem em seco. Alertas ficam visíveis. Bases37/32, System32 e corrediças ainda sem centros não foram verificadas espacialmente;104 painéis sem centros não entram nas2.286 posições. Dado numérico completo não significa cobertura completa. Critérios: margem3mm, tolerância de par±0,5mm, ferramenta raio10/curso100, todos propostos.

## Cotação e horas

[Quantitativos e diferenças R44](Quantitativos.md) · [ferragens por móvel](Ferragens_por_movel.csv) · [totais por família](Ferragens_totais.csv) · [comparação R44](Comparacao_R44.csv) · [fita por peça](Fita_por_peca.csv) · [fita por cor](Fita_por_cor.csv) · [horas por tipo/móvel](Horas_furacao.csv).

Gerar: `python -B ferramentas/estudos/quantificar_furacao.py`. Inventário físico vem de hardwareRows; decisões descritivas não são uma segunda compra. Teste documental/idempotência: `python -B ferramentas/estudos/test_quantitativos_furacao.py`. Cenário:52 dobradiças/bases/limitadores,7 pares FGVTN500 e2 MOVENTO400;316 Minifix,207 Confirmat,527 cavilhas condicionais, com componentes e kits sem duplicação. O novo mapa propõe8 Minifix no P19 contra12 documentais: reconciliar o fundo antes de adotar; a regra genérica não substitui o detalhe específico.

Fita:249 IDs sem bordas/espessura definidas;477,64m é soma de perímetros de envelopes, não metragem de fita. Horas propostas:18,23–42,76, incluindo preparação de319 faces; taxas explícitas e substituíveis. Não incluem furos ainda sem centros, montagem nem retrabalho. Orçamento R44 preservado. Nenhum fornecedor foi contatado.
