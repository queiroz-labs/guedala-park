# Modelo 3D (FreeCAD)

Modelo vigente: **R54**, [Guedala_Park_R54_Berlin.FCStd](Guedala_Park_R54_Berlin.FCStd). Base e arquivo vigente preservados; o relatório abaixo confere o candidato externo. SHA256 em [ferramentas/site/current_release.json](../ferramentas/site/current_release.json). É o único `.FCStd` permitido nesta pasta.

## Estudo de nível e vãos

**Aprovação PENDENTE.** Pedido de Elias, 31/10/2026, nesta conversa: nível Z=0, altura nominal **2570 mm**, vãos por `Part::Cut`, somente em estudo externo. Esse parâmetro não substitui as alturas vigentes de 2600/2500 mm. Partida: cópia do **candidato de piso/rodapé da base atual**, preservando seus pisos e 54 trechos de rodapé. Verde da janela continua separado.

Arquivo salvo pelo comando de documento do FreeCAD MCP na instância gráfica: `%LOCALAPPDATA%/Temp/guedala_vaos_estudo/Composicao/Guedala_Park_Estudo_vaos.FCStd`. Evidências e script de reprodução ficam nessa pasta temporária; não são arquivos publicados.

### Tabela dos envelopes nominais de corte

Fontes: [P01 oficial, página única](../09_Referencias/Plantas_e_manuais/Planta_oficial.pdf), para localização dos nove vãos; [planta mobiliada](../03_Ambientes/Planta_mobiliada/README.md), para contexto. **Nenhuma cota de vão abaixo está explícita no PDF.** Números extraídos do R54, não medidos na imagem nem no imóvel. X/Y em mm globais do CAD, canto mínimo; largura acompanha o eixo indicado. Parede = caixas originais limítrofes.

| ID/ambiente | Parede (`Peca…`) | X/Y mm | Eixo/largura mm | Altura mm | Peitoril mm | Fonte R54 (`Peca…`) |
|---|---|---:|---:|---:|---:|---|
| JQ Quarto | 009/011 | 5600/900 | X/1200 | 1130 | 920 | 063+064 |
| JE Escritório | 019/021 | 3100/−100 | X/1150 | 1130 | 920 | 065+066 |
| JS Sala | 031/033 | 680/1750 | X/1390 | 1130 | 920 | 067+068 |
| JL Lavanderia | 041/043 | 4850/5690 | Y/1060 | 1130 | 920 | 069+070 |
| JB Banheiro | 045/047 | 4850/4350 | Y/400 | 1130 | 920 | 071+072 |
| PQ Quarto | 057/059/061 | 3650/3150 | Y/750 | 2050 | 0 | lacuna + folha 074 |
| PE Escritório | 027/029 | 2650/2950 | X/750 | 2050 | 0 | lacuna + folha 073 |
| PB Banheiro | 053/055 | 2850/3950 | X/700 | 2050 | 0 | lacuna + folha 075 |
| PI Entrada/cozinha | 035/037 | −100/6150 | Y/750 | 2050 | 0 | lacuna + folha 076 |

**Todos nominais.** Nas janelas, o corte inclui vidro de 1100 mm (Z=950..2050) e soleira CAD de 30 mm (Z=920..950); 920/1130 descrevem essa envoltória, sem definir vão bruto ou esquadria. Espessura atravessada: 100 mm nominal. Portas: largura da lacuna, altura da folha; folgas/batentes não acrescentados.

### Construção e pendências

As 27 caixas já deixam lacunas em planta; cortes diretos removeriam zero material. Permanecem ocultas/referenciadas, com formas, posições e expressões preservadas. Nove recomposições + 23 prolongamentos até Z=2570 formam a união; nove `Part::Cut` abrem os vãos. `ParedesCortadas` oculta. Nível BIM `BuildingPart`, Z=0/2570 nominal.

Pendências, sem refinamento: qual o vão bruto acabado e as folgas de marco de cada abertura? A entrada tem lacuna CAD de **750 mm** e folha 076 de **850 mm**; qual largura/posição é correta no levantamento? Confirmar peitoris, alturas, espessuras e interface com teto/RT antes de incorporar. O estudo conserva a lacuna existente, sem resolver essa divergência por hipótese.

**Completo OK:** `--completo --relatorio --candidato` no clone local; 106 cenários, nenhuma invariante/cenário falhou e nenhuma colisão nova. Os 1129 pares de caixas novas/maiores passaram na interseção exata. R54, base, regras e relatório de piso/rodapé preservados. Aprovação **PENDENTE**.

**Δ sobre piso/rodapé:** 5905→5958; **53 novos / 57 alterados / 0 removidos** (54 visibilidades + três agregados). Nenhuma forma própria/posição/expressão original mudou. As 67 representações de pisos/soleiras/rodapés coincidem com a origem. `Relatorio_estudo_vaos.md` e `Delta_geometrico.json` externos, junto ao estudo.

## Esquadrias no estudo

**Aprovação PENDENTE.** Etapa B solicitada por Elias, 31/10/2026, nesta conversa; cópia da etapa A com pisos/rodapé. Arquivo externo, salvo pelo FreeCAD MCP na instância gráfica: `%LOCALAPPDATA%/Temp/guedala_esquadrias_estudo/Guedala_Park_Estudo_esquadrias.FCStd`.

Cada vão tem um `App::Part`; cotas externas na tabela A. Prefixo das fontes antigas: `Peca`. Todas foram mantidas e ocultadas, com geometria, posição e expressões preservadas.

| Vão | Antigo | Novo `App::Part` |
|---|---|---|
| JQ | 063/064 | `Janela_Quarto` |
| JE | 065/066 | `Janela_Escritorio` |
| JS | 067/068 | `Janela_Sala` |
| JL | 069/070 | `Janela_Lavanderia` |
| JB | 071/072 | `Janela_Banheiro` |
| PQ | 074 | `Porta_Quarto` |
| PE | 073 | `Porta_Escritorio` |
| PB | 075 | `Porta_Banheiro` |
| PI | 076 | `Porta_Entrada` |

Janelas: caixilho branco, folha de vidro e peitoril. Quarto: persiana integrada, sem cortina/blackout externo ([Registro de 21/09/2026](../01_Programa_e_decisoes/Registro_de_decisoes.md), seção “Quarto — janela, madeira e cabeceira definidos”). Elias, 31/10/2026, nesta conversa: “deixa a janela do quarto com a persiana 30% fechada”; **300 mm dos 1000 mm do curso gráfico**, faixa superior. Escritório: mesma persiana integrada, conforme [registro do ambiente](../03_Ambientes/Escritorio/README.md) e confirmação de Elias, 31/10/2026 nesta conversa; cena também em 30%. Portas: batente, folha e soleira; controles legados preservados.

**Só representação nominal:** perfis de 20 mm e vidro de 6 mm são gráficos; não especificam produto. Folhas úteis derivadas desse quadro, cores das portas herdadas; fabricante, material, número de folhas, perfis, mecanismo e arremates reais PENDENTES. Envelopes dos batentes do banheiro/escritório recortados contra quatro pontas do rodapé; não é detalhamento de guarnição.

Soleiras Z−50..0: quarto/escritório: `Soleira_Quarto`/`Soleira_Escritorio` + `Vinilico_Sem_Soleira_Escritorio` repartem `Vinilico_continuo` sem perda/sobreposição; `Soleira_banheiro` reutilizada. Entrada acrescenta **0,075 m² nominal** onde não havia piso; material/implantação pendentes, inclusive divergência 750/850 mm da etapa A. Demais pisos/rodapés preservados. Grupo de suportes e corte intermediário do piso ocultos; acabamento Olmo aplicado aos resultados para evitar sobreposição cinza após navegar na vista.

Altura independente em `Nivel_Parametros`: 32 relações da etapa A recuperadas sem ciclo; 8042 expressões preservadas na reabertura. **Completo OK**, 106 cenários e 1157 pares sem colisão nova. Δ sobre A: **130 novos / 63 alterados / 0 removidos** (5958→6088), incluindo auxiliares nativos. R54/base preservados. Relatório externo `Relatorio_esquadrias.md` e `Delta_geometrico.json`, junto ao estudo.

**Verde na janela (pedido de Elias, 30/10/2026):** [candidato externo e limites](Verde_box_candidato.md), com aprovação PENDENTE; R54/base intactas. Macro GUI `ferramentas/estudos/aplicar_verde_janela_box.FCMacro`; cópia em `../outputs/R55_candidato/`, sem FCStd no git. Assinaturas e verificação completa separadas do relatório do vigente.

## Quadro de áreas, materiais e câmeras

**Etapa D, aprovação PENDENTE.** Pedido de Elias, 31/10/2026; cópia da etapa B em `%LOCALAPPDATA%/Temp/guedala_quadro_estudo/Guedala_Park_Estudo_quadro.FCStd`. **Etapa C adiada; nenhum forro.** Planilha nativa `QuadroAreas`, com fórmulas de área/perímetro das sete regiões planas ocultas `Area_*`, extraídas do piso em Z=0. Regenerar esses contornos se o piso mudar. Perímetro é o contorno completo, incluindo passagens; não é quantitativo de rodapé.

Comparação com [quadro nominal documental H01](../03_Ambientes/Acabamentos/Quantidades_por_ambiente.csv), sem ajustar a geometria. O quadro não traz perímetro equivalente; a área privativa oficial usa outro critério.

| Ambiente | CAD m² | Documento m² | Δ m² | Perímetro m |
|---|---:|---:|---:|---:|
| Quarto | 8,3925 | 8,3825 | +0,0100 | 13,40 |
| Escritório | 6,8600 | 6,7850 | +0,0750 | 10,70 |
| Sala | 9,1194 | 9,1800 | −0,0606 | 12,70 |
| Circulação | 1,1010 | 0,9450 | +0,1560 | 4,40 |
| Cozinha | 5,5772 | 5,5176 | +0,0596 | 10,46 |
| Lavanderia | 2,1413 | 1,9866 | +0,1547 | 5,88 |
| Banheiro | 2,6616 | 2,6616 | 0 | 6,86 |
| **Total** | **35,8530** | **35,4583** | **+0,3947** | — |

Critério: piso final intersectado pelas nove máscaras antigas; sobreposição sala/cozinha atribuída à cozinha. Soleiras de portas pertencem ao ambiente servido; entrada à cozinha, transição à lavanderia. Pontes CAD fora das máscaras: 0,0100 m² quarto, 0,0210 circulação, 0,0462 cozinha. Lavanderia CAD 1,29×1,61 m versus documento 1,29×1,54 m, mais transição 0,0644 m². União dos sete contornos cobre o piso, sem lacuna/sobreposição. Divergências completas em `QuadroAreas` e `Quadro_geometrico.json` externo.

**Altura geométrica parede−piso: 2570 mm nos sete ambientes**, calculada do topo das paredes e Z do piso. É nominal da envoltória, sem teto acabado: documento 2600 mm (Δ−30); banheiro 2500 mm (Δ+70). Pé-direito real/forro continuam pendentes.

Catálogo `Materiais_Nomeados`: Olmo, Iseo Marfim, Travertino Reale Greige, Paredes, Esquadrias, Vidro, Portas, Peitoris e Rodape. Vínculo `Material_Quadro` nas peças; paleta RGB/transparências existentes registrada, sem aplicar novo acabamento. Materiais físicos/fabricantes pendentes; soleiras mantêm a aparência herdada.

| Ambiente (`Camera_<ambiente>_`) | Vistas salvas |
|---|---|
| Quarto | Planta, Canto_1..4 |
| Escritorio | Planta, Canto_1..4 |
| Sala | Planta, Canto_1..4 |
| Circulacao | Planta, Canto_1..4 |
| Cozinha | Planta, Canto_1..4, Eixo (+Y, bancada) |
| Lavanderia | Planta, Canto_1..4 |
| Banheiro | Planta, Canto_1..4 |

36 registros em `Cameras_Ambientes`, com câmera Coin nativa, posição/alvo. Selecionar um registro e executar `Aplicar_camera.FCMacro`, junto ao estudo; apenas restaura a vista. Cantos 1..4: mínimo X/Y, máximo X/mínimo Y, máximo X/Y, mínimo X/máximo Y; posição livre mais próxima na região.

**Completo OK:** 106 cenários/1157 pares, sem falha/colisão nova. Aparência preservada, render idêntico; 8049 expressões reabertas. **Δ sobre B: 57 novos / 189 alterados / 0 removidos**: 160 vínculos e 38 normalizações (9 em comum), incluindo um agregado BIM recalculado; nenhuma forma própria mudou. Detalhe externo: `Relatorio_quadro.md`.

## Candidato piso e rodapé

**Aprovação PENDENTE.** Elias, 30/10/2026: pisos → rodapé em cópia do R54 original. Um FCStd externo, salvo na GUI: `../outputs/Piso_rodape_candidato/Guedala_Park_Piso_rodape_candidato.FCStd`. R54, base e release preservados. [Relatório, hashes e perguntas](Relatorio_mudanca.md).

- Vinílico Olmo em um sólido; lavanderia Iseo Marfim e banheiro Travertino Reale Greige separados, mais duas soleiras. Z −50..0 mm. Nove pisos antigos ocultos. Sob a folha do banheiro: vinílico como hipótese visual.
- Rodapé 80 mm/15 mm nominal: **54 trechos / 35,41680 m**. Recortado contra interferências; piso corrigido define adjacências. `Rodape_Parametros` fora do grupo evita ciclo de expressões. Produto e áreas molhadas pendentes.
- Aceite: **59.104 células**, zero lacunas/sobreposições; soleiras em contato exato. **7839 expressões** e **106 cenários**, sem peça inválida/colisão nova. **Completo OK** após Elias, 30/10/2026, mandar ajustar a regra: o envelope passa a incluir a laje de piso (Z −50..0). Base intacta; aprovação PENDENTE.

Reproduzir com `ferramentas/estudos/compor_piso_rodape.FCMacro` (`GP_REPO`, `GP_COMPOSICAO_DIR` externo vazio). Verificar com `--completo --relatorio --candidato <FCStd externo>`; esse modo não atualiza a base. Evidências completas junto ao candidato.

**Proposta separada, sem número:** R54 → verde da janela → pisos → rodapé; compatibilizar encontros e repetir aceite/completo. O R55 verde permanece separado, inalterado e pendente.

## Histórico R53/R54 — 27/10/2026

**R54:** pedestais Berlin aproximados e cadeira lateral +15 mm em X, sem colisões novas nos 106 cenários. Elias, 27/10/2026: “Se passar sem colisões novas, pode salvar como R54, atualizar a base e publicar no site.” [Dimensões](../04_Moveis/Inventario_dimensional/Portas_e_articulacoes/Mesa_e_varal.md).

**R53:** [dados históricos](Alteracoes_R53.json); 5.832 objetos/7.702 expressões/106 cenários.

## Triagem das formas inválidas — 25/10/2026

Zero inválidas/1.449 formas próprias, conferidas por Elias, 25/10/2026; 12 agregados inválidos informativos. [Rastreio](Triagem_geometria.json) · [script](../ferramentas/verificar_modelo/triar_geometria.py). Não usar volumes agregados como prova de madeira/integridade. Fontes P01/P02/P06/P07 válidas; 26/32 testes BOP passaram; envelopes coincidem com fichas em 0,02 mm, sem validar usinagem.

## Análise dos alertas BOP — 25/10/2026

[Ensaios e ressalvas](Analise_bop.json) · [script](../ferramentas/verificar_modelo/analisar_bop.py). C0 não prova defeito físico; `InvalidCurveOnSurface` da frente permanece. Os 18 cortes sintéticos passaram, sem comprovar usinagem; nenhum reparo gravado. [Consolidador candidato](../ferramentas/componentes/Consolidacao/consolidar_r31.py): só isometrias analíticas; não executar o antigo sobre R52.

## Abrir e salvar com segurança

- Abrir: `powershell -File 02_Modelo_3D/Abrir_no_FreeCAD.ps1`: candidato piso/rodapé, se da base vigente; `-Vigente`: oficial. FreeCAD mais novo instalado.
- **Salvar só pela interface gráfica.** O `FreeCADCmd` perde o `GuiDocument.xml`, onde ficam cores e visibilidade (o verificador acusa).
- Para estudar uma alteração, grave **outro arquivo fora do projeto** e só traga para cá o que Elias aprovar. Não sobrescreva o vigente para consultar.
- Comparar assinaturas geométricas; `Shape.hashCode()` muda ao recalcular e não prova preservação.
- Backups `.FCBak` e cópias não ficam na pasta do projeto.

## Verificar

```
python ferramentas/verificar_modelo/verificar_modelo.py
python ferramentas/verificar_modelo/verificar_modelo.py --completo
python ferramentas/verificar_modelo/verificar_modelo.py --completo --relatorio --candidato <FCStd externo>
```

Rápido: arquivo/cores/SHA/backups. Completo: [invariantes](../ferramentas/verificar_modelo/invariantes.json), envelope, aparência, [106 movimentos](../ferramentas/verificar_modelo/movimentos.json), retorno inicial, objetos/formas/expressões e interseções exatas. Relatório PENDENTE; candidato não atualiza [base](Base_verificacao.json.gz)/release. [Regras](../AGENTS.md#10-verificações-obrigatórias).

**R52, histórico:** [alterações](Alteracoes_R52.json) · [diferenças R51–R52](Diferencas_R51_R52.json).

## Movimentos e operação

106 cenários de movimento conferidos (gavetas até 400/500, portas 45/86°, correr do banheiro, canto, cesto, banco, varal): [resumo](Verificacao_movimentos_R52.json) · [casos](Movimentos_R52.json) · [condições](Condicoes_operacao_R52.json). Abrir a gaveta do roupeiro com a folha fechada, ou o banco com as almofadas presentes, é contato esperado; faz parte da sequência de uso. Para portas e gavetas sem abrir o CAD, use `ferramentas/cinematica/consultar.py`.

## Pendências técnicas

Formato do fundo P01, divergência 100/300 mm do micro-ondas, interface guia–fundo P16, ferragens reais, ligações, suspensão, massa e estabilidade dos apoios e capacidade do banco. Os estudos ficam em [04_Moveis](../04_Moveis/README.md) e não estão incorporados ao modelo.

As evidências citadas estão em [Componentes por assunto](Componentes/README.md). Scripts de origem ficam em `ferramentas/componentes/`. Material sem uso vigente é recuperável no Git e na tag `antes-reorganizacao`; estudos históricos não substituem o modelo vigente.

## Arquivos desta pasta

R52 e `Historico/` são evidências antigas; binários R45/R48 e contadores R50/R51 no Git. `Componentes/`: evidências por tema; scripts em `ferramentas/componentes/`.
