# Furação relativa às peças — nominal/proposta

| Entrega | Consulta |
|---|---|
| 249 IDs, 20 móveis | [Índice por peça e face](index.html), CSV `Pxx-coordenadas.csv` |
| Conectores dos 20 móveis | [Mapa por encontro](Mapa_conectores.csv) |
| Dados ausentes e operações descritivas preservadas | [Pendências](Pendencias.csv) |
| Dimensões e acabamento por ID | [Painéis](Paineis.csv) |
| Contagens e SHA256 das fontes | [Resumo](Resumo.json) |

Gerar: `python -B ferramentas/estudos/gerar_furacao.py`. Entradas alternativas: `--pecas DIR`; saída de ensaio fora do projeto: `--saida DIR`. Biblioteca padrão, sem abrir FCStd. Cada CSV usa `;`, UTF-8 com BOM, mm; vazio significa **parâmetro a confirmar**, nunca zero. `situacao` distingue posição proposta de usinagem incompleta. 2.286 posições: 156 com Ø/profundidade conhecidos e 2.130 com parâmetros. Não representam 2.286 operações prontas para máquina. Há centros em 145 peças; 104 ficam sem centros, com pendências por ID. Cobertura de inventário não equivale a cobertura completa de usinagem.

## Origem e parâmetros

- Carcaça: canto mínimo dos eixos C/L identificados no campo `origem`. A na menor coordenada da espessura e B na maior; B conserva os eixos, sem espelhamento de vista. `topo-C0/C1/L0/L1`: canto da aresta; x ao longo da aresta, y pela espessura desde A. `gx/gy/gz` e normal para dentro da chapa permitem confrontar pares e trajetórias em 3D nominal.
- Portas: origem e eixos específicos do mapa histórico de canecos; x na largura, y na altura. A interna. Não confundir C (maior dimensão de corte) com largura da porta. Centros mantêm margens de borda inferior/superior; intermediários redistribuídos. Conferir mão e fita na primeira folha.
- Contatos: recomputados com caixas já exportadas em `Geometria.json`, somente peças atuais retangulares, estacionárias e correspondentes aos CSVs. Não se abriu o modelo. São **218 contatos**, distintos dos 171 históricos e dos 80 contatos R00; não somar as listas. Cada contato tem um ID, dois painéis e sua condição. Contato não comprova necessidade nem resistência da ligação. Peças especiais, gavetas, tampas e interfaces ausentes ficam na lista de pendências.
- Regra R00: dois até 400 mm, três até 700 mm, `ceil(contato/350)+1` acima. Mantida a implementação vigente de R00. Demais encontros candidatos usam Minifix, fundo usa Confirmat; face a face exige detalhe próprio. Quantidade condicional não é compra. Quantidades históricas de 52 Minifix não são somadas ao novo mapa: a comparação será explícita.
- Distribuição proposta: recuo 60 mm; reserva adicional 32 mm para cavilha. Passo `(contato−152)/(n−1)`. Pilotos na face oposta de divisória deslocados 32 mm **junto com o par**; cavilha fica 32 mm após o conector. São parâmetros de projeto, não exigência de catálogo; verificar conflitos antes de adotá-los.

O arquivo [regras dimensionais](../Dependencias/regras.json) governa envelopes, não o C×L de cada peça. O gerador relê os CSVs a cada execução. Se uma mudança perder a correspondência com a topologia exportada, registra pendência em vez de esticar caixas e inventar alinhamentos. A regeneração completa depende de reexportar a topologia das peças alteradas; essa dependência permanece explícita. Não há promessa de recalcular automaticamente painéis a partir de paredes ou tetos.

## Fontes e limites de catálogo

- Blum 71B3550 parafusada: [catálogo p.76](https://publications.blum.com/2024/catalogue/en/76/); caneco e flange [p.77](https://publications.blum.com/2024/catalogue/en/77/). Canecos 35×13 dos mapas documentais; padrão da flange 45/9,5. Pilotos 2,7×8, broca M01.ZZ03.01 e parafuso 609.1500: [p.160](https://publications.blum.com/2024/catalogue/en/160/).
- Base 173H7100 [p.152](https://publications.blum.com/2024/catalogue/en/152/): 37 mm da frente **do apoio**, dois centros ±16 mm da linha montada. ID/face e transferência da porta ao apoio continuam pendentes; não criar furos no apoio errado.
- Minifix 15 de referência: Häfele 262.26.034 para 18 mm, Ø15×13,5 (+0,5), A9; [p.294](https://files.hafele.co.uk/catalogfiles/www/14CFC294.pdf). B34 e piloto S100 262.28.920 Ø5×8,5 proposto vêm de `Inventario_dimensional/Inventario/Minifix_C.md`, catálogo FF2.10/14/17. **Esse S100 usa passagem Ø7; Ø8 solicitado exige selecionar pino compatível.** As novas passagens Ø8 ficam sem profundidade; não misturar com o detalhe Ø7 histórico. SKU, ferramenta e acesso precisam de confirmação.
- Cavilha Ø8×30 não define partilha dos embutimentos. Confirmat 7×50 não define broca escalonada, escareado ou profundidade. Esses valores ficam vazios até catálogo do SKU/oficina.
- Corrediças FGVTN500 e MOVENTO400: referências longitudinais e páginas permanecem em Pendencias.csv; faltam ID/face/alturas e seção de montagem suficientes para centros completos. Não atribuir profundidade de caneco a corrediça.
- Espelheiro: oito furos Ø5 nos níveis documentados 244/488 e recuos 20/86; profundidade 8,5 proposta. Não são linha System32. Passo32 de uma linha nova exige início/fim e recuos; não converter prateleiras fixas em removíveis para preencher tabela.

Os SVGs têm uma face por arquivo e lista de centros/IDs; círculo tracejado representa Ø ainda desconhecido. O site usa sua lista explícita de documentos e ativos; esta entrega é incluída nessa lista, sem substituir os CSVs descritivos R15.

## Escopo preservado

Suspensão de aéreos, ancoragem, cargas de uso, teto, micro-ondas T05 e rodízios P08 não foram refinados. Perguntas de oficina/RT permanecem nas fontes. Não houve leitura nem alteração do FreeCAD. A pasta `06_Entregas/Fichas_fabricacao/Execucao_ate_07h_2026-10-25/` foi apenas sinalizada ao usuário; não apagada nem movida.

## Conferência e montagem

[Relatório e dez ocorrências prioritárias](Conferencia.md) · [todas as ocorrências](Conflitos.csv) · [distâncias por par](Distancias.csv) · [portas e dobradiças](Portas.csv) · [sequência proposta dos 20 móveis](Montagem.csv).

Executar `python -B ferramentas/estudos/conferir_furacao.py`: resultado REPROVADO, 46 ocorrências (1 sobreposição, 2 distâncias, 43 acessos) e 2.130 posições incompletas; quatro portas baixas/largas P04 fora da orientação do gráfico Blum. Não foram detectadas violações de profundidade ou pares quebrados **nos furos verificáveis**; os incompletos não passam por omissão. Onze testes adversariais em `python -B ferramentas/estudos/test_furacao.py` cobrem espessura15/reserva3, tolerância0,5, par ausente, faces/topos cruzados e tipos sobrepostos. Distância mínima3 e envelope de ferramenta raio10/curso100 são hipóteses de projeto configuráveis, não valores de catálogo.

Acesso avaliado sobre caixas nominais: precedências de aperto aparecem na sequência. Ciclos e peças sem topologia impedem uma sequência executiva completa; não resolver montagem ocultando alertas. Linha System32/base/corrediça sem centros não foi declarada verificada.

## Cotação e horas

[Quantitativos e diferenças R44](Quantitativos.md) · [ferragens por móvel](Ferragens_por_movel.csv) · [totais por família](Ferragens_totais.csv) · [comparação R44](Comparacao_R44.csv) · [fita por peça](Fita_por_peca.csv) · [fita por cor](Fita_por_cor.csv) · [horas por tipo/móvel](Horas_furacao.csv).

Gerar: `python -B ferramentas/estudos/quantificar_furacao.py`. Inventário físico vem de hardwareRows; decisões descritivas não são uma segunda compra. Teste documental/idempotência: `python -B ferramentas/estudos/test_quantitativos_furacao.py`. Cenário:52 dobradiças/bases/limitadores,7 pares FGVTN500 e2 MOVENTO400;316 Minifix,207 Confirmat,527 cavilhas condicionais, com componentes e kits sem duplicação. O novo mapa propõe8 Minifix no P19 contra12 documentais: reconciliar o fundo antes de adotar; a regra genérica não substitui o detalhe específico.

Fita:249 IDs sem bordas/espessura definidas;477,64m é soma de perímetros de envelopes, não metragem de fita. Horas propostas:18,23–42,76, incluindo preparação de319 faces; taxas explícitas e substituíveis. Não incluem furos ainda sem centros, montagem nem retrabalho. Orçamento R44 preservado. Nenhum fornecedor foi contatado.
