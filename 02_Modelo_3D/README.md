# Modelo 3D (FreeCAD)

Vigente: **R54**, [FCStd](Guedala_Park_R54_Berlin.FCStd), único permitido nesta pasta. Base/vigente preservados; estudos externos pendentes. [SHA/release](../ferramentas/site/current_release.json).

## Estudo de nível e vãos

**PENDENTE.** Elias, 31/10/2026: nível Z0/**2570 mm nominal** e vãos `Part::Cut` no estudo externo. Partida: candidato piso/rodapé da base atual; pisos/54 rodapés preservados. Não substitui 2600/2500 mm vigentes; verde separado.

Salvo pela GUI/MCP: `%LOCALAPPDATA%/Temp/guedala_vaos_estudo/Composicao/Guedala_Park_Estudo_vaos.FCStd`. Evidências/script externos, sem publicação.

### Tabela dos envelopes nominais de corte

Fontes: [P01 oficial](../09_Referencias/Plantas_e_manuais/Planta_oficial.pdf), localização; [planta mobiliada](../03_Ambientes/Planta_mobiliada/README.md), contexto. **Cotas não explícitas no PDF:** extraídas do R54, sem medição real. X/Y mm globais, canto mínimo; largura no eixo indicado. Parede = caixas limítrofes.

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

**Nominais:** janela inclui vidro 1100 mm (Z950..2050) + soleira 30 mm (Z920..950); 920/1130 é envoltória, não vão bruto. Parede 100 mm nominal. Porta: largura da lacuna/altura da folha, sem folgas ou batentes adicionais.

### Construção e pendências

As 27 caixas já deixam lacunas: cortes diretos removeriam zero. Originais ocultos/referenciados, preservados. União: nove recomposições + 23 prolongamentos; nove `Part::Cut`. `ParedesCortadas` oculta; nível BIM `BuildingPart`, Z0/2570 nominal.

Pendências: vão bruto/folgas, peitoris, alturas, espessuras e teto/RT. Entrada: lacuna CAD **750 mm** versus folha 076 **850 mm**; confirmar largura/posição no levantamento. Estudo preserva a lacuna, sem resolver por hipótese.

**Completo OK:** candidato no clone local; 106 cenários/1129 pares, sem falha/colisão nova. R54/base/regras/relatório de piso preservados. **PENDENTE**.

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

Janelas brancas com vidro/peitoril. Quarto: persiana integrada, sem cortina externa ([Registro de 21/09/2026](../01_Programa_e_decisoes/Registro_de_decisoes.md), seção “Quarto — janela, madeira e cabeceira definidos”). Elias, 31/10/2026: “deixa a janela do quarto com a persiana 30% fechada”; 300/1000 mm de curso gráfico. Escritório: mesma persiana, [fonte do ambiente](../03_Ambientes/Escritorio/README.md) e confirmação de Elias, 31/10/2026; também 30%. Portas: batente/folha/soleira, controles preservados.

**Nominal:** perfis 20 mm/vidro 6 mm, folhas do quadro/cores herdadas; especificação comercial PENDENTE. Batentes banheiro/escritório cortados contra quatro pontas do rodapé; sem guarnição.

Soleiras Z−50..0: quarto/escritório + piso final repartem `Vinilico_continuo` sem perda/sobreposição; banheiro reutilizado. Entrada +0,075 m² nominal; material/implantação e divergência 750/850 mm pendentes. Pisos/rodapés preservados. Suportes/corte intermediário ocultos e resultados com Olmo eliminam a sobreposição cinza ao navegar.

`Nivel_Parametros`: 32 relações recuperadas sem ciclo; 8042 expressões reabertas. **Completo OK**, 106 cenários/1157 pares sem colisão nova. Δ sobre A: **130 novos / 63 alterados / 0 removidos** (5958→6088), com auxiliares. R54/base preservados. `Relatorio_esquadrias.md`/`Delta_geometrico.json` externos.

**Verde na janela (pedido de Elias, 30/10/2026):** [candidato externo e limites](Verde_box_candidato.md), com aprovação PENDENTE; R54/base intactas. Macro GUI `ferramentas/estudos/aplicar_verde_janela_box.FCMacro`; cópia em `../outputs/R55_candidato/`, sem FCStd no git. Assinaturas e verificação completa separadas do relatório do vigente.

## Quadro de áreas, materiais e câmeras

**D, aprovação PENDENTE.** Pedido de Elias, 31/10/2026; cópia B: `%LOCALAPPDATA%/Temp/guedala_quadro_estudo/Guedala_Park_Estudo_quadro.FCStd`. **C adiada, sem forro.** `QuadroAreas`: área/perímetro das sete faces ocultas `Area_*`, piso Z=0. Regenerar contornos se o piso mudar. Perímetro inclui passagens; não é rodapé.

Comparação com [quadro nominal documental H01](../03_Ambientes/Acabamentos/Quantidades_por_ambiente.csv), sem ajustar a geometria. Sem perímetro documental equivalente; área privativa usa outro critério.

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

Catálogo `Materiais_Nomeados`: Olmo, Iseo Marfim, Travertino Reale Greige, Paredes, Esquadrias, Vidro, Portas, Peitoris e Rodape. Vínculo `Material_Quadro` nas peças; paleta RGB/transparências existentes registrada, sem aplicar novo acabamento. Materiais/fabricantes pendentes; soleiras preservadas.

| Ambiente (`Camera_<ambiente>_`) | Vistas salvas |
|---|---|
| Quarto | Planta, Canto_1..4 |
| Escritorio | Planta, Canto_1..4 |
| Sala | Planta, Canto_1..4 |
| Circulacao | Planta, Canto_1..4 |
| Cozinha | Planta, Canto_1..4, Eixo (+Y, bancada) |
| Lavanderia | Planta, Canto_1..4 |
| Banheiro | Planta, Canto_1..4 |

36 câmeras Coin em `Cameras_Ambientes`: selecionar registro e executar `Aplicar_camera.FCMacro` externo. Cantos 1..4: minX/minY, maxX/minY, maxX/maxY, minX/maxY, posição livre próxima.

**Completo OK:** 106 cenários/1157 pares, sem falha/colisão nova. Aparência preservada, render idêntico; 8049 expressões reabertas. **Δ sobre B: 57 novos / 189 alterados / 0 removidos**: 160 vínculos e 38 normalizações (9 em comum), incluindo um agregado BIM recalculado; nenhuma forma própria mudou. Detalhe externo: `Relatorio_quadro.md`.

## Organizacao da arvore

**E, PENDENTE.** Cópia D: `Guedala_Park_Estudo_organizado.FCStd` em `%LOCALAPPDATA%/Temp/guedala_organizacao_estudo/`. `Moveis/P01..P20`, apartamento e histórico; BC43/banco/Minifix e operandos atuais preservados. Names/sistemas locais intactos. CSVs `Mapa_labels` (328), `Mapa_grupos` (239), `Mapa_objetos` (6145). Δ **35 novos / 415 alterados / 0 removidos** (6180 totais); zero formas próprias alteradas, oito agregados por filiação. **Completo OK**, 106 cenários/1157 pares; 8049 expressões. Detalhes: `Relatorio_organizacao.md` externo.

## Auditoria de remocoes

**Limpeza externa, aprovação/revisão PENDENTES.** Elias, 31/10/2026, nesta conversa: “1. limpeza real manda o prompt”, somente preparação antes de aprovar o relatório. Partida E auditada (6180 objetos); estudo salvo pela GUI/MCP em `%LOCALAPPDATA%/Temp/guedala_limpeza_real/Guedala_Park_Estudo_limpo.FCStd`.

[Auditor](../ferramentas/estudos/auditar_remocoes_freecad.py): 1905 candidatos; **116 remoções / 1789 mantidos**, 6180→6064. `Plano_remocoes.json`/CSV externos: provas/motivos; `Relatorio_mudanca.md` externo lista todos os removidos e o comando de promoção **não executado**. Folhas antes dos contêineres, seis lotes; 8049 expressões preservadas. **Δ 0 novos/7 grupos alterados/116 removidos**; formas próprias/posições/aparência iguais. **Completo OK**, 106 cenários/1157 pares, sem falha.

20 de `historicos_ocultos` usados/protegidos: **sem mudança de regra**. Origin/Point, 36 câmeras, QuadroAreas, materiais, BC43/banco/Minifix e operandos A/B preservados. R54/base/release/site e relatório oficial intactos. `--plano-remocoes <JSON externo>` só permite conferir exclusões previstas no candidato completo, com hashes/provas; proíbe atualizar base e dispensar movimentos. Sem plano, remoção continua erro. Promoção/revisão dependem de Elias; pacote futuro no relatório externo.

CSV SHA256: `85cb66bd36f064432534814e45e2a6a13c6b1a12aa36ee5e7c22e0c8ac3ff85f`.

## Candidato piso e rodapé

**Aprovação PENDENTE.** Elias, 30/10/2026: pisos → rodapé em cópia do R54 original. Um FCStd externo, salvo na GUI: `../outputs/Piso_rodape_candidato/Guedala_Park_Piso_rodape_candidato.FCStd`. R54, base e release preservados. [Relatório, hashes e perguntas](Relatorio_mudanca.md).

- Vinílico Olmo em um sólido; lavanderia Iseo Marfim e banheiro Travertino Reale Greige separados, mais duas soleiras. Z −50..0 mm. Nove pisos antigos ocultos. Sob a folha do banheiro: vinílico como hipótese visual.
- Rodapé 80 mm/15 mm nominal: **54 trechos / 35,41680 m**. Recortado contra interferências; piso corrigido define adjacências. `Rodape_Parametros` fora do grupo evita ciclo de expressões. Produto e áreas molhadas pendentes.
- Aceite: **59.104 células**, zero lacunas/sobreposições; soleiras em contato exato. **7839 expressões** e **106 cenários**, sem peça inválida/colisão nova. **Completo OK** após Elias, 30/10/2026, mandar ajustar a regra: o envelope passa a incluir a laje de piso (Z −50..0). Base intacta; aprovação PENDENTE.

Reproduzir com `ferramentas/estudos/compor_piso_rodape.FCMacro` (`GP_REPO`, `GP_COMPOSICAO_DIR` externo vazio). Verificar com `--completo --relatorio --candidato <FCStd externo>`; esse modo não atualiza a base. Evidências completas junto ao candidato.

**Proposta separada, sem número:** R54 → verde da janela → pisos → rodapé; compatibilizar encontros e repetir aceite/completo. R55 verde separado/pendente.

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

106 cenários de movimento conferidos (gavetas até 400/500, portas 45/86°, correr do banheiro, canto, cesto, banco, varal): [resumo](Verificacao_movimentos_R52.json) · [casos](Movimentos_R52.json) · [condições](Condicoes_operacao_R52.json). Abrir a gaveta do roupeiro com a folha fechada, ou o banco com as almofadas presentes, é contato esperado; faz parte da sequência de uso. Consulta sem abrir CAD: `ferramentas/cinematica/consultar.py`.

## Pendências técnicas

Formato do fundo P01, divergência 100/300 mm do micro-ondas, interface guia–fundo P16, ferragens reais, ligações, suspensão, massa e estabilidade dos apoios e capacidade do banco. Os estudos ficam em [04_Moveis](../04_Moveis/README.md) e não estão incorporados ao modelo.

As evidências citadas estão em [Componentes por assunto](Componentes/README.md). Scripts de origem ficam em `ferramentas/componentes/`. Acervo no Git/tag `antes-reorganizacao`; estudos não substituem o vigente.

## Arquivos desta pasta

R52/`Historico/`: evidências; R45/R48/R50/R51 no Git. `Componentes/`: temas; scripts em `ferramentas/componentes/`.
