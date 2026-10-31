# Quantitativos nominais de acabamentos

Bloco 4, conferência de 29/10/2026. Base: representação atual da planta no site e envelopes R54; nenhuma medida presencial. **Orçamento, escolhas, site e FreeCAD preservados.** As áreas abaixo servem para comparar escopos e preparar a conferência, não para encomendar quantidades definitivas.

## Resultados que afetam a cotação

- Piso vinílico: **30,8101 m² líquidos**, sem sobreposições. O orçamento contém **35,80 m² / dez caixas**, e 34 m² de preparação/instalação. Não há demonstração de que nove caixas atendam: este bloco não refaz a paginação das 140 réguas nem muda o ensaio vigente de dez caixas.
- Rodapé de **8 cm** em todo o projeto ([decisão de 30/10/2026](../../01_Programa_e_decisoes/Pisos_e_rodapes.md)). Áreas vinílicas: **37,03 m**, antes de móveis, perdas e transições, versus verba de **35 m incluindo transições**. Não concluir falta de 2,03 m: a extensão omitida atrás de móveis ainda depende do escopo contratado.
- Verde do box em duas paredes: chuveiro e janela (Elias, 30/10/2026). H05A gráfico: 4,15 m² verdes/1,80 m² claros; H05B até 2,50 m: 4,66/2,00 m². H05C usa fundo 1,24×2,47 mais hipótese adicional de janela 0,80×2,47, sem descontar abertura: 5,0388 m² verdes/1,976 m² claros. Compra histórica R44 de 3,74 m²/11 caixas permanece; paginação, alturas e abertura dependem de levantamento.
- Pintura completa antes dos móveis, cenário do box desenhado: **112,6626 m² de paredes + 35,4583 m² de teto**. Referências de rendimento acabado e reserva de 20% resultam em **16,22 L de parede e 6,38 L de teto**, ante cesta orçamentária de 21,6 L + 7,2 L. Produto final, absorção, recortes e retoques podem impedir redução; não alterar as verbas por esta estimativa.

| Ambiente | Piso/teto sem sobreposição (m²) | Parede menos vãos, antes de revestimentos (m²) | Pintura de parede H05A (m²) | Rodapé antes dos móveis (m) |
|---|---:|---:|---:|---:|
| Quarto | 8,3825 | 30,9425 | 30,9425 | 12,25 |
| Escritório | 6,7850 | 24,4975 | 24,4975 | 9,75 |
| Sala | 9,1800 | 21,6110 | 21,6110 | 8,90 |
| Circulação | 0,9450 | 3,2900 | 3,2900 | 0,80 |
| Cozinha | 5,5176 | 14,2705 | 14,0836 | 5,33 |
| Lavanderia | 1,9866 | 9,5460 | 9,4130 | 4,12 |
| Banheiro | 2,6616 | 14,7750 | 8,8250 | 5,96 |

Os rodapés da lavanderia/banheiro são comprimentos geométricos separados; não foram somados aos 37,03 m de rodapé vinílico. Acabamento e solução de borda nessas áreas continuam conforme especificação pendente. A área privativa oficial de 40,18 m² inclui outros elementos; não deve ser comparada diretamente com esta união de pisos internos.

## Método e limites

1. **H01 — união dos pisos:** `app.js`, matriz `floors`, em centímetros; união ortogonal exata por intervalos, sem aproximação por malha. Retângulos do mesmo ambiente são unidos; sobreposição entre sala e cozinha de **0,4915 m²** atribuída contabilmente à cozinha. Isso evita compra duplicada, mas não define limite físico de ambientes. Sala bruta = 9,6715 m². A base R44 de sete retângulos, 31,4485 m², muda −0,6384 m²: correções de contorno, passagens e união explicam o conjunto, não só a diferença de 7 cm na lavanderia. As passagens já desenhadas estão incluídas; não acrescentar novamente a antiga reserva de 0,48 m².
2. **H02 — paredes e vãos:** união dos retângulos `walls`; apenas faces adjacentes ao piso interno entram na conta. Os vãos gráficos recebem parede virtual para calcular verga/peitoril e depois têm sua área descontada. Janelas: peitoril 0,95 m e altura 1,10 m; portas: 2,05 m, larguras 0,75/0,70 m conforme desenho. A posição das portas foi reconstruída nos intervalos das paredes, não copiada das folhas abertas. Contornos/espessuras de 16/17 cm do banheiro e larguras de portas são hipóteses gráficas. Pé-direito **2,60 m a confirmar**; banheiro **2,50 m**, conforme cenário distinto de `data.js`. Não importar automaticamente a hipótese de forro de 2,47 m. Rebaixos, sancas, vigas, requadros internos dos vãos, cortineiros e faces adicionais não dimensionadas estão fora do número.
3. **H03 — móveis altos:** envelopes de módulos R54 com topo ≥1,50 m, em `cad-data.js`. O CSV de faces mostra a união das projeções a até 5 cm da parede, limitada à face e descontando vãos; é **ocultação potencial por envelope**, não desconto de pintura. Não somar projeções de móveis individualmente. O envelope pode incluir vazios e não prova fechamento até o teto, contato com parede ou que não se pintará atrás. O cenário principal pinta antes da montagem: desconto adotado = zero. Tampouco descontar armários do piso, pois não existe decisão de interromper o acabamento sob eles.
4. **H04 — pisos molhados:** box nominal 0,80 × 1,24 = **0,9920 m² EXT**; restante do banheiro, inclusive passagem gráfica, **1,6696 m² Satin**. Lavanderia oficial 1,29 × 1,54 = **1,9866 m²**. A projeção do enchimento no box não foi subtraída: suas faces, impermeabilização e área efetivamente revestida precisam de detalhe. Reserva de 15% é cenário contábil, não resultado de paginação de placas de 90 cm. A reserva não transforma uma caixa de 1,62 m² em quantidade suficiente para a lavanderia.
5. **H05 — paredes molhadas:** A/B transferem a parede da janela de claro para verde, mantendo as áreas totais molhadas anteriores. A desconta abertura de 0,40×1,10 m; B usa a mesma abertura até 2,50 m. C preserva a convenção do orçamento, sem desconto da janela. Hipóteses, não medidas reais nem revisão automática de caixas. A pintura de A soma 112,6626 m²; B reduziria 0,71 m² de pintura. Cozinha/lavanderia: faixas de pedra desenhadas, 1,869 × 0,10 e 1,33 × 0,10 m, descontam **0,1869 e 0,1330 m²** de tinta. Retornos de pedra ausentes não foram inventados. A linha R10 de cerâmica genérica da cozinha permanece zerada, conforme conciliação vigente; revestimento escolhido ali é a faixa de pedra e pintura acima.
6. **H06 — tinta:** reservas de 10% e 20% são hipóteses explícitas para consumo/perdas, não taxas certificadas. Rendimento de catálogo é máximo sobre superfície preparada; a estimativa em litros pode ser insuficiente se houver absorção maior. Não multiplicar rendimento **acabado** por duas/três demãos novamente. Massa, selador, fundo, reparos e argamassa não recebem quantitativo fictício: espessura, substrato e produto faltam. Tetos são projeções horizontais; gesso e faixas adicionais permanecem pendentes.

## Rendimento e fontes

Consulta primária em 29/10/2026:

- [Suvinil Toque Fosco Completo](https://loja.suvinil.com.br/produto/suvinil-toque-fosco-completo): até 150 m² por 18 L, 30 m² por 3,6 L, duas a três demãos. Referência de **8,333 m²/L acabados**, já usada como candidato de custo; não seleciona produto final para áreas úmidas.
- [Suvinil Tetos](https://loja.suvinil.com.br/produto/suvinil-tetos): página inicial apresenta 0,9 L e até 6 m² acabados, duas a três demãos. Normalização de estudo **6,667 m²/L**; a página lida não confirmou rendimento individual do galão de 3,6 L. Confirmar embalagem/produto antes de fechar compra. Não misturar rendimentos por demão de anúncios antigos com rendimento acabado.

Fontes locais: [origem das medidas](../Medidas/README.md), [cozinha](../Cozinha/README.md), [banheiro](../Banheiro/README.md), [pisos e rodapés](../../01_Programa_e_decisoes/Pisos_e_rodapes.md), [decisão de acabamento por peça](../../ferramentas/site/fabrication/Decisao_acabamentos_R13.md), [conciliação de pisos](../../05_Orcamento_e_cronograma/Orcamento/Pisos_e_revestimentos/Conferencia_caixa_cozinha.md) e [obra/pintura](../../05_Orcamento_e_cronograma/Orcamento/Obra_e_pintura/Analise_obra.md). A decisão por peça trata marcenaria, não determina área de pintura arquitetônica. A diretriz de fechar armários até o teto não transforma o envelope exportado em execução atualizada.

## Arquivos e reprodução

- [Quantidades por ambiente](Quantidades_por_ambiente.csv): piso, teto, parede, vãos, rodapé e ocultação potencial.
- [Faces e vãos](Faces_e_vaos.csv): cada segmento contado, em cm e m²/m explicitados.
- [Móveis altos sem desconto automático](Moveis_altos_sem_desconto.csv).
- [Revestimentos: cenários separados](Revestimentos_cenarios.csv).
- [Pintura e reservas por ambiente](Pintura_por_ambiente.csv).
- [Comparação com o orçamento preservado](Comparacao_orcamento.csv): diferenças de quantidade, não descontos em reais.
- [SHA256 das fontes locais](Fontes_locais.csv). Modelo declarado pela extração: R54, SHA256 `4a2996ee63dd6f2f3dc302025a73fb65011b3339bae510130732859706049528`. O arquivo nativo não foi aberto nem salvo neste bloco.

```powershell
python -B ferramentas/estudos/quantitativos_acabamentos.py
python -B -m unittest discover -s ferramentas/estudos -p test_quantitativos_acabamentos.py -v
```

Nove testes: sobreposições, retângulos contidos, união vazia, corte de abertura, rendimento acabado, reserva, conservação dos pisos e limites da ocultação por envelopes. Fontes numéricas dos cenários de box e comparações estão declaradas no script; se desenho/orçamento mudar, conferir essas premissas antes de regenerar. O script recusa revisão diferente de R54.

## Perguntas exatas, sem reabrir escolhas registradas

- **Para compatibilização do box:** quais dimensões, altura final e recorte da janela valem para a paginação das duas paredes verdes, chuveiro e janela? Registrar em desenho antes da compra/corte.
- **Para o orçamento do instalador:** os 35 m incluem quais transições e quais trechos sem rodapé atrás da marcenaria? A medição bruta é 37,03 m antes desses ajustes.
- **Para fechar material de pintura:** qual produto/base será usado por ambiente, qual preparo do substrato e quais faixas/rebaixos serão pintados? Não existe base para transformar a diferença de litros em redução garantida de custo.

Medição após as chaves continua necessária para vãos, alturas, superfícies, enchimento do box e encontros. As lacunas não impediram as comparações nominais acima. Não houve bloqueio de acesso aos documentos; Firecrawl CLI falhou no transporte da consulta externa, e as páginas públicas primárias foram lidas pelo navegador de pesquisa disponível.
