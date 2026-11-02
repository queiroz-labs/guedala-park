# Modelo 3D (FreeCAD)

Vigente: **R55**, com correções incorporadas em 02/11/2026 (Elias: “aprovo deixa como documento principal”), [FCStd](Guedala_Park_R55_Berlin.FCStd). Elias,01/11/2026: “Sim, incorporar o candidato e atualizar a base”: portas livres 800×2100 mm, banheiro 700×2100 mm; alturas acabadas 2550/2300 mm. Bancada/gabinete preservados. [Relatório](Relatorio_mudanca.md) · [SHA/release](../ferramentas/site/current_release.json).


## Aparência e movimentos incorporados — 02/11/2026

Elias, 02/11/2026, nesta conversa: “aprovo deixa como documento principal”, após o relatório do candidato `Aparencia_movimentos`. SHA e aprovação no relatório vigente.

- Vaso sanitário reconhecível, folha do banheiro reposicionada, torneira atrás da cuba e faixa frontal acima da grelha do forno.
- PE12G, RI9252/91 e ME23P com formas externas; IB6S e LG CV5012PC4 com portas móveis. Envelopes documentados preservados; detalhes, espessuras e eixos são aproximações visuais.
- `IB6S_Controles`: refrigerador/freezer independentes, 0–90°. `LGVC4_Controles.Abertura`: 0–90°; profundidade gráfica aberta 1100 mm, mais reserva traseira de 100 mm.
- `Persiana_Controle_Quarto/Escritorio.Fechamento`: 0–100%, inicial 30%; enrolamento gráfico sem inclinação de lâminas documentada.
- `Porta_Controle_Entrada/Quarto/Escritorio.Abertura`: 0–90°, inicial 90°. Banheiro mantém `PortaEntradaBanheiroR12.Abertura`. Folha do escritório +10 mm em X para alinhar fechamento ao vão; demais mecanismos existentes preservados.
- Porta B `FrenteSimplesR001` e faixa fixa `FaixaQuinaBR04`: Arenza em todas as faces; P17: lateral externa marfim, fundo/tampo internos Branco TX.
- Verificação do candidato: 106 cenários existentes e 26 testes adicionais de posições, retorno, persianas e fixos; nenhuma colisão nova na comparação completa. Testes adicionais não demonstram limite mecânico real nem substituem conferência no produto.

Fontes oficiais: [PE12G](https://loja.electrolux.com.br/pe12g-pe12g-purif-agua-pelt-bivolt/p), [RI9252](https://www.philips.com.br/c-p/RI9252_91/essential-airfryer), [ME23P](https://loja.electrolux.com.br/micro-ondas-electrolux-preto-23l-efficient-me23p/p), [LG](https://www.lg.com/br/lavanderia/lava-e-seca/cv5012pc4/). Dimensões e reservas: [conferência](../03_Ambientes/Equipamentos/Conferencia_127V_e_folgas.md). Cores: [regra por chapa](../ferramentas/site/fabrication/Decisao_acabamentos_R13.md).

## Referência para revisão do arquiteto

6149 objetos; 8239 expressões; 106 cenários; sem colisão nova nem peça própria inválida. [Macro](../ferramentas/estudos/atualizar_portas_alturas.FCMacro): batentes/recortes, soleiras e quatro rodapés; perfis de 20 mm gráficos, produto por especificar. Altura de 2300 mm em face oculta, sem espessura de forro presumida.

| Item | Situação e uso |
|---|---|
| R55 vigente | Portas/alturas incorporadas: Elias,01/11/2026, “Sim, incorporar o candidato e atualizar a base”. Histórico de limpeza/nível no git. |
| Pranchas A3 R02 | [Caderno](../06_Entregas/Caderno_pranchas/README.md): desenhos ainda referenciam R54. Metadados de Geometria.json/regras.json apontam R55, mas envelopes foram mantidos da exportação anterior. Não representam reexportação arquitetônica do R55. |
| Planta mobiliada R03 | [Capturas da R54](../03_Ambientes/Planta_mobiliada/README.md); preservar identificação até produzir vistas novas. |
| Verde na janela do box | Incorporado: `RevestJanelaBoxR55`; parede do chuveiro preservada, outra interna clara. |
| Campo e executivo | Sem medida real; revisão do arquiteto, levantamento e detalhamento continuam pendentes. |

Histórico de formação abaixo; caminhos externos não são modelos vigentes. Abridor: `-Vigente`.

## Revisão da base arquitetônica

**Uso:** [37 itens, fontes e proposta](Conferencia_uso.csv); [gerador](../ferramentas/estudos/conferir_uso.py) com `--atualizar --saida <pasta externa>`. Reúne as quatro frentes e as [interfaces arquitetônicas](Revisao_base_arquitetonica.csv). Medidas reais e revisão técnica pendentes.

**Lavanderia corrigida:** Elias,01/11/2026, “Sim, incorporar essa correção”: 1290×1540 mm; parede 100→170 mm, banheiro 2090×1240 preservado; Loop +15 mm, folga 10 mm. [Macro](../ferramentas/estudos/corrigir_lavanderia.FCMacro) recorta pisos/contornos e ajusta rodapés; [relatório](Relatorio_mudanca.md).

**Porta/MCMV:** [Ministério das Cidades, Portaria 725, anexo III, V.b.vii](https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/habitacao/portarias/PORTARIAN.725VERSAOCOMPILADA.pdf): vão livre entre batentes 800×2100 mm para FAR/FDS. Não comprova obrigação para outras linhas. Elias,01/11/2026: livres 800×2100 mm; banheiro 700×2100 mm. Incorporado; bancada/gabinete preservados.

## Estudo de nível e vãos

Elias, 31/10/2026: nível Z0/**2570 mm nominal** e vãos `Part::Cut`, hoje no R55. Partida: candidato piso/rodapé da base atual; pisos/54 rodapés preservados. Histórico: projeto nominal agora 2550/2300 mm; verde separado.

Envelopes históricos anteriores às portas atuais: consultar o histórico Git. Medidas vigentes e limites estão no topo e no relatório.

Construção anterior de nível/vãos preservada no histórico Git; portas e alturas correntes constam no relatório.

## Esquadrias no estudo

**Incorporadas ao R55.** Etapa B solicitada por Elias, 31/10/2026; origem em cópia gráfica da etapa A. Produtos, perfis e dimensões reais permanecem nominais, apesar da incorporação do estudo.

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


**Verde na janela (pedido de Elias, 30/10/2026):** [candidato externo e limites](Verde_box_candidato.md), com aprovação PENDENTE; R54/base intactas. Macro GUI `ferramentas/estudos/aplicar_verde_janela_box.FCMacro`; cópia em `../outputs/R55_candidato/`, sem FCStd no git. Assinaturas e verificação completa separadas do relatório do vigente.

## Quadro de áreas anterior às novas portas, materiais e câmeras

**Incorporados ao R55.** Etapa D solicitada por Elias, 31/10/2026. **Sistema de forro pendente; referência de teto do banheiro a 2300 mm sem espessura.** `QuadroAreas`: área/perímetro das sete faces ocultas `Area_*`, piso Z=0. Contornos anteriores à ampliação das soleiras; regenerar antes de quantitativos. Perímetro inclui passagens; não é rodapé.

Comparação com [quadro nominal documental H01](../03_Ambientes/Acabamentos/Quantidades_por_ambiente.csv), sem ajustar a geometria. Sem perímetro documental equivalente; área privativa usa outro critério.

| Ambiente | CAD m² | Documento m² | Δ m² | Perímetro m |
|---|---:|---:|---:|---:|
| Quarto | 8,3925 | 8,3825 | +0,0100 | 13,40 |
| Escritório | 6,8600 | 6,7850 | +0,0750 | 10,70 |
| Sala | 9,1194 | 9,1800 | −0,0606 | 12,70 |
| Circulação | 1,1010 | 0,9450 | +0,1560 | 4,40 |
| Cozinha | 5,5224 | 5,5176 | +0,0048 | 10,34 |
| Lavanderia | 2,0482 | 1,9866 | +0,0616 | 5,74 |
| Banheiro | 2,6616 | 2,6616 | 0 | 6,86 |
| **Total** | **35,7051** | **35,4583** | **+0,2468** | — |

Critério: piso final intersectado pelas nove máscaras antigas; sobreposição sala/cozinha atribuída à cozinha. Soleiras de portas pertencem ao ambiente servido; entrada à cozinha, transição à lavanderia. Pontes CAD fora das máscaras: 0,0100 m² quarto, 0,0210 circulação, 0,0462 cozinha. Lavanderia CAD/documento 1,29×1,54 m; transição lateral CAD 0,0616 m². União dos sete contornos cobre o piso, sem lacuna/sobreposição. Divergências completas em `QuadroAreas` e `Quadro_geometrico.json` externo.

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


## Organizacao da arvore

**Incorporada ao R55.** `Moveis/P01..P20`, apartamento e histórico organizados antes da limpeza. BC43/banco/Minifix, operandos e sistemas locais preservados. Evidência consolidada no relatório do vigente.

## Auditoria de remocoes

**Limpeza incorporada ao R55:** Elias, 31/10/2026, “ok eu aprovo”, escopo “Tudo do estudo limpo (R55)”; [relatório consolidado](Relatorio_mudanca.md).

[Auditor](../ferramentas/estudos/auditar_remocoes_freecad.py): 116 remoções no lote 1 e 36 no lote 2, 6180→6028 objetos. Lote 2 autorizado por Elias, 31/10/2026, “Sim, liberar”. As cinco planilhas históricas removidas estão preservadas em [conteúdo extraído](Historico/Planilhas_removidas_limpeza.json). Permanecem BC43, câmeras, Origin/Point, batentes, `*_Legados` e três `R45_*` em uso.

As bases intermediárias e cópias externas descrevem a preparação histórica; a base vigente corresponde ao R55. Regras/invariantes não foram dispensadas pela limpeza. CSV da auditoria SHA256: `85cb66bd36f064432534814e45e2a6a13c6b1a12aa36ee5e7c22e0c8ac3ff85f`.

## Candidato piso e rodapé

**Conteúdo incorporado ao R55; título preservado para os links existentes.** Estudo iniciado em 30/10/2026 sobre o R54, incorporado no aceite consolidado de Elias, 31/10/2026, “ok eu aprovo”, escopo “Tudo do estudo limpo (R55)”. Produto e interfaces continuam pendentes.

- Vinílico Olmo em um sólido; lavanderia Iseo Marfim e banheiro Travertino Reale Greige separados. Z −50..0 mm. Nove pisos antigos ocultos. Sob a folha do banheiro: vinílico como hipótese visual.
- Rodapé 80 mm/15 mm nominal: **54 trechos / 35,41680 m** na etapa de origem; recortado contra interferências e, depois, batentes. Não é quantitativo comercial final. Rodape_Parametros evita ciclo de expressões.
- Verificação histórica da composição: 59.104 células sem lacuna/sobreposição, soleiras em contato e 106 cenários sem colisão nova. Aceite do conjunto vigente no [relatório](Relatorio_mudanca.md).

Macro de origem: `ferramentas/estudos/compor_piso_rodape.FCMacro`. Não executar sobre o vigente para reconstruir uma etapa já incorporada. O verde da janela foi incorporado em 02/11/2026; ver seção de aparência vigente.

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
