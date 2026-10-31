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

As 27 caixas já deixam lacunas em planta; cortar diretamente nelas removeria zero material. No estudo, continuam referenciadas e ocultas, com geometria, posição e expressões preservadas. Uma união paramétrica acrescenta nove recomposições e 23 prolongamentos até Z=2570; nove `Part::Cut` encadeados abrem os envelopes da tabela. A representação baixa `ParedesCortadas` também fica oculta para evitar duplicação. Pavimento BIM `BuildingPart`, `IfcType=Building Storey`, Z=0, altura 2570 nominal.

Pendências, sem refinamento: qual o vão bruto acabado e as folgas de marco de cada abertura? A entrada tem lacuna CAD de **750 mm** e folha 076 de **850 mm**; qual largura/posição é correta no levantamento? Confirmar peitoris, alturas, espessuras e interface com teto/RT antes de incorporar. O estudo conserva a lacuna existente, sem resolver essa divergência por hipótese.

**Completo OK:** `--completo --relatorio --candidato` no clone local; 106 cenários, nenhuma invariante/cenário falhou e nenhuma colisão nova. Os 1129 pares de caixas novas/maiores passaram na interseção exata. R54, base, regras e relatório de piso/rodapé preservados. Aprovação **PENDENTE**.

**Δ sobre piso/rodapé:** 5905→5958 objetos, **53 novos / 57 alterados / 0 removidos**. Alterados: 54 visibilidades + três agregados (a associação do nível está em `ApartamentoR34`); nenhuma forma própria, posição ou expressão original mudou. As **67 representações de pisos/soleiras/rodapés** (inclui agregados) coincidem em volume, área, caixa, faces e sólidos com o retrato da origem. Relatório externo: `Relatorio_estudo_vaos.md`; Δ completo em `Delta_geometrico.json`, junto ao estudo.

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

## Candidato piso e rodapé

**Aprovação PENDENTE.** Elias, 30/10/2026: pisos → rodapé em cópia do R54 original. Um FCStd externo, salvo na GUI: `../outputs/Piso_rodape_candidato/Guedala_Park_Piso_rodape_candidato.FCStd`. R54, base e release preservados. [Relatório, hashes e perguntas](Relatorio_mudanca.md).

- Vinílico Olmo em um sólido; lavanderia Iseo Marfim e banheiro Travertino Reale Greige separados, mais duas soleiras. Z −50..0 mm. Nove pisos antigos ocultos. Sob a folha do banheiro: vinílico como hipótese visual.
- Rodapé 80 mm/15 mm nominal: **54 trechos / 35,41680 m**. Recortado contra interferências; piso corrigido define adjacências. `Rodape_Parametros` fora do grupo evita ciclo de expressões. Produto e áreas molhadas pendentes.
- Aceite: **59.104 células**, zero lacunas/sobreposições; soleiras em contato exato. **7839 expressões** e **106 cenários**, sem peça inválida/colisão nova. **Completo OK** após Elias, 30/10/2026, mandar ajustar a regra: o envelope passa a incluir a laje de piso (Z −50..0). Base intacta; aprovação PENDENTE.

Reproduzir com `ferramentas/estudos/compor_piso_rodape.FCMacro` (`GP_REPO`, `GP_COMPOSICAO_DIR` externo vazio). Verificar com `--completo --relatorio --candidato <FCStd externo>`; esse modo não atualiza a base. Evidências completas junto ao candidato.

**Proposta separada, sem número:** R54 → verde da janela → pisos → rodapé; compatibilizar encontros e repetir aceite/completo. O R55 verde permanece separado, inalterado e pendente.

## Histórico R53/R54 — 27/10/2026

**R54:** pedestais Berlin aproximados e cadeira lateral +15 mm em X, sem colisões novas nos 106 cenários. Elias, 27/10/2026: “Se passar sem colisões novas, pode salvar como R54, atualizar a base e publicar no site.” [Dimensões](../04_Moveis/Inventario_dimensional/Portas_e_articulacoes/Mesa_e_varal.md).

**R53:** pedido de Elias, 27/10/2026, “Aplicar à R52 e às fichas as decisões já tomadas” e “crie um R53”. Incorporou P02 U1–U4=A (requisito10kg, sem capacidade demonstrada), Arenza liso nas duas faces da P13/Peca350 (18mm), TV mantida e lixeiras LIX=A (Biovis +70mm em X, Loop +60mm em Y). Preservou expressões, implantação nominal e pendências de passagem/pedal/tampa. Links das 20 fichas R15 corrigidos; armários até o teto e alternativas P03/gavetas separados. [Dados históricos R53](Alteracoes_R53.json); 5.832 objetos/7.702 expressões/106 cenários. Gravação pela GUI.

## Triagem das formas inválidas — 25/10/2026

Zero peças inválidas nas 1.449 formas próprias conferidas por Elias (25/10/2026, comunicação nesta revisão); 12 contêineres com representação montada inválida, informativos. Desde `3cdf795`, o verificador separa formas próprias de agregados. [Objetos, contagens e rastreio](Triagem_geometria.json) · [script](../ferramentas/verificar_modelo/triar_geometria.py). Não usar volumes agregados como prova de madeira, integridade ou recortes. As 85 fontes P01/P02/P06/P07 são válidas; dos 32 testes BOP de P06/P07, 26 passaram. Envelopes locais coincidem com fichas em 0,02 mm, sem validar usinagem.

## Análise dos alertas BOP — 25/10/2026

Escopo: operações e peças próprias; arquivos STEP e ferragens recebidas preservados. [Ensaios, parâmetros e ressalvas](Analise_bop.json) · [script](../ferramentas/verificar_modelo/analisar_bop.py).

- OCCT 7.8.1: `GeomAbs_C0` consulta continuidade do suporte, sem provar defeito físico. [Código oficial](https://github.com/Open-Cascade-SAS/OCCT/blob/V7_8_1/src/BOPAlgo/BOPAlgo_ArgumentAnalyzer.cxx#L775).
- Quatro réguas e grelha P07: `transformGeometry()` reproduziu C0 em B-splines; `transformShape()` preservou formas analíticas. Diferenças bidirecionais de volume zero; variações brutas até 4,965/0,754 mm³ não são material removido. [Objetos e testes](Analise_bop.json).
- `MontagemG2R019` (fundo): C0, três cortes válidos. `MontagemG2R020` (frente): C0 + `InvalidCurveOnSurface`; desvio amostrado até ~1,013 × 10⁻⁷ mm, dentro das tolerâncias amostradas, sem certificar máximo contínuo. Três cortes válidos; ressalva para novas booleanas preservada.
- 18 cortes sintéticos passaram; resíduos até 5,523 mm³/0,002651%, sem prova de usinagem. `fix`/`removeSplitter` conservaram alertas.
- [Consolidador candidato](../ferramentas/componentes/Consolidacao/consolidar_r31.py): isometrias analíticas; não generalizar para escala não uniforme nem executar o antigo sobre R52. Ensaios históricos nos JSONs; nenhum reparo gravado.

## Abrir e salvar com segurança

- Abrir: `powershell -File 02_Modelo_3D/Abrir_no_FreeCAD.ps1`: candidato piso/rodapé, se da base vigente; `-Vigente`: oficial. FreeCAD mais novo instalado.
- **Salvar só pela interface gráfica.** O `FreeCADCmd` perde o `GuiDocument.xml`, onde ficam cores e visibilidade (o verificador acusa).
- Para estudar uma alteração, grave **outro arquivo fora do projeto** e só traga para cá o que Elias aprovar. Não sobrescreva o vigente para consultar.
- Prove que nada mudou sem querer comparando assinatura geométrica (volume, área, faces, vértices, caixa, centro de massa, posição) e não `Shape.hashCode()`, que muda a cada recálculo.
- Backups `.FCBak` e cópias não ficam na pasta do projeto.

## Verificar

```
python ferramentas/verificar_modelo/verificar_modelo.py
python ferramentas/verificar_modelo/verificar_modelo.py --completo
python ferramentas/verificar_modelo/verificar_modelo.py --completo --relatorio --candidato <FCStd externo>
```

Rápido: arquivo, cores GUI, SHA e backups. Completo: [invariantes](../ferramentas/verificar_modelo/invariantes.json), envelope global, aparência, [106 movimentos](../ferramentas/verificar_modelo/movimentos.json), retorno ao estado inicial, objetos removidos, formas inválidas, expressões perdidas e colisões novas por interseção exata. [Base compactada](Base_verificacao.json.gz): não ler inteira nem atualizar para esconder falha. Relatório gerado com aprovação PENDENTE; candidato não atualiza base/release. Regras e comandos de aprovação: [AGENTS](../AGENTS.md#10-verificações-obrigatórias).

**R52, histórico:** TV a50mm da porta/Peca131.LocalY1180; tanques/frentes500 e móveis antigos ocultos; Berlin110/170; controles BC43; Gaveta009 53→47mm; ferragens declaradas; seis atalhos externos removidos. [Dados R52](Alteracoes_R52.json) · [diferenças R51–R52](Diferencas_R51_R52.json).

## Movimentos e operação

106 cenários de movimento conferidos (gavetas até 400/500, portas 45/86°, correr do banheiro, canto, cesto, banco, varal): [resumo](Verificacao_movimentos_R52.json) · [casos](Movimentos_R52.json) · [condições](Condicoes_operacao_R52.json). Abrir a gaveta do roupeiro com a folha fechada, ou o banco com as almofadas presentes, é contato esperado; faz parte da sequência de uso. Para portas e gavetas sem abrir o CAD, use `ferramentas/cinematica/consultar.py`.

## Pendências técnicas

Formato do fundo P01, divergência 100/300 mm do micro-ondas, interface guia–fundo P16, ferragens reais, ligações, suspensão, massa e estabilidade dos apoios e capacidade do banco. Os estudos ficam em [04_Moveis](../04_Moveis/README.md) e não estão incorporados ao modelo.

As evidências citadas estão em [Componentes por assunto](Componentes/README.md). Scripts de origem ficam em `ferramentas/componentes/`. Material sem uso vigente é recuperável no Git e na tag `antes-reorganizacao`; estudos históricos não substituem o modelo vigente.

## Arquivos desta pasta

Evidências históricas R52: `Verificacao_R52.json`, `Verificacao_posicoes_R52.json`, `Auditoria_estatica_R52.json`, `Comparacao_colisoes_R51_R52.json`, `Preservacao_originais.json` e `Registro_entrega_R52.json`. Não são nova inspeção do candidato.

`Historico/` conserva estudos R46–R49 citados; binários R45/R48 no Git. `Componentes/` organiza evidências por tema; scripts em `ferramentas/componentes/`. Contadores R50/R51 e registros de continuidade estão no Git; os contadores atuais estão no relatório da composição.
