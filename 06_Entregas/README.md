# Entregas — manifesto e versões

## Manifesto de versões — conferência T09 em 26/10/2026

Conferência documental antecipada do trabalho previsto para 30/10, após os commits A–E. Não altera revisões nem comprova publicação remota. Referências: [estado atual](../ESTADO_ATUAL.md) e [manifesto do gerador](../ferramentas/site/current_release.json).

| Item solicitado | Onde está a versão | Concorda com o ESTADO_ATUAL? |
|---|---|---|
| Modelo R52 | `cadPath`: [02_Modelo_3D/Guedala_Park_R52_Corrigido.FCStd](../02_Modelo_3D/Guedala_Park_R52_Corrigido.FCStd). `cadSHA256`: `941da02d367c5f6ce2992f72985f86c3aceba23f899a4c394cf3569f19d7b4da` | Sim: R52 no estado e no `current_release.json`; SHA informado pelo manifesto, conferido pelo verificador geral. |
| Fichas R14 | [Índice dos 20 móveis](Fichas_fabricacao/index.html); `fabricationRevision` = R14 | Sim: revisão do conteúdo e do estado. |
| Pacote R21 | Link anterior neste README: `06_Entregas/Publicacao/Guedala_Park_R21.zip` | **Não:** estado e `packageRevision` indicam R22, caminho `06_Entregas/Publicacao/Guedala_Park_R22.zip`. R21 pedido fica identificado como divergência, sem substituir o pacote. |
| Pranchas R00 | [Índice](Caderno_pranchas/index.html) · [PDF R00](Caderno_pranchas/Guedala_Park_Pranchas_R00.pdf) | Sim quanto à revisão; não comprova atualização de todas as vistas para a R52. |
| Orçamento R44 | [Consolidado R44](../05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md), revisão no texto, nome preservado | Sim: R$ 137.748,11 de execução no estado e no consolidado. |
| Especificações R01 | [Caderno R01](../01_Programa_e_decisoes/Caderno_de_especificacoes.md) | Sim quanto à revisão; coerência integral com estudos posteriores continua condicionada. |

**Divergências a reconciliar, sem alteração automática:** pacote R21 na entrada antiga abaixo versus R22 no estado/gerador; `lastPublishedPackageRevision` ainda R18 no mesmo JSON. O plano também conserva R20 na linha de ponto de partida. Identificar revisão local, conteúdo selado e publicação remota antes de harmonizar esses registros; esta conferência não prova qual ZIP está servido online. Números de revisão iguais, isoladamente, não demonstram integração técnica.

**Publicação R22 — 26/10/2026:** integra estudos correntes e pé-direito 2,60 m = 260 cm = 2600 mm, medida a confirmar, por decisão de Elias em 26/10/2026. Cenário separado de forro do escritório: 2,47 m. Sem medição real, fabricação ou alteração do FreeCAD R52. Fonte: [pesquisa e decisão](../01_Programa_e_decisoes/Pesquisa_pe_direito.md).

> **Atualização R52/R21:** modeloR52 e fichasR14; pacoteR21 com matriz20/20 e suspensãoP17/P12 em estudos separados. [Estado e condições](../ESTADO_ATUAL.md). Produto, juntas, ferramenta, ensaios e ancoragens continuam pendentes.

| Uso | Abrir | Revisão |
|---|---|---|
| Modelo3D FreeCAD | [Modelo completo R52](../02_Modelo_3D/Guedala_Park_R52_Corrigido.FCStd) · [conferências](../02_Modelo_3D/README.md) | R52 |
| Pacote corrente para compartilhar | [Guedala_Park_R21.zip](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Publicacao/Guedala_Park_R21.zip) | R21 |
| Entrega anterior selada | `Compartilhar_R17/Guedala_Park_R17.zip` (somente no PC, fora do Git/site) | Histórico preservado, não regenerado |
| Guia do montador | [Dossiê de marcenaria](Dossie_marcenaria_R45.html) | Links para as fichas na pasta vigente `Fichas_fabricacao/` |
| Fichas, furação e pendências | [20 móveis](Fichas_fabricacao/index.html) · [pendências](Fichas_fabricacao/Pendencias.html) | R14 |
| Planta cotada | [Planta](Planta_cotada/index.html) | R13 |
| Especificações | [Caderno](../01_Programa_e_decisoes/Caderno_de_especificacoes.md) | R01 com referência CAD corrente |
| Avanços e condições técnicas | [Continuidade após R52](../04_Moveis/Proximas_decisoes/README.md) | Estudos separados, sem incorporação automática |

Extraia o ZIP inteiro, abra `COMECE_AQUI.html` pelo menu da pasta extraída e use o caminho R52 indicado nele. O pacote não libera fabricação ou carga; produto, juntas, protótipo e medidas finais continuam condicionados.

## Histórico — entrega R49/R16 de24/10/2026

| Uso | Abrir | Revisão |
|---|---|---|
| Modelo 3D (FreeCAD) | [Guedala_Park_R49_Gavetas_escritorio.FCStd](../02_Modelo_3D/Historico/Gavetas_escritorio/Guedala_Park_R49_Gavetas_escritorio.FCStd) | R49: R48 + gavetas do escritório corrigidas (folga de 7 mm, trava direita espelhada) |
| Pacote para o montador | `Compartilhar_R16/Guedala_Park_R16.zip` (somente no PC, fora do Git/site) | R16 |
| Fichas dos 20 móveis, furação e pendências | [Fichas_fabricacao_R13](Fichas_fabricacao/index.html) (conteúdo R14) | R14 |
| Planta cotada | [Planta_cotada_R13](Planta_cotada/index.html) | R13 |
| Programa, planta mobiliada e vistas | [Programa R01](../01_Programa_e_decisoes/Programa_de_necessidades.md) · [Planta R02](../03_Ambientes/Planta_mobiliada/README.md) | R01 / R02 |
| Especificações | [Caderno de especificações R01](../01_Programa_e_decisoes/Caderno_de_especificacoes.md) | R01 |
| Orçamento | [Orçamento R43](../05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md) | R43 |

A R49 ([o que mudou](../02_Modelo_3D/Historico/Gavetas_escritorio/README.md)) corrige as gavetas do escritório sobre a R48 ([o que mudou](../02_Modelo_3D/Historico/Depurador_sem_canal/README.md)), que parte da R46, que grava as fichas R14 no modelo; furos, FGVTN 500 e a piano do banco seguem fora da geometria ([detalhes](../02_Modelo_3D/Historico/Fichas_no_CAD/README.md)). Nada aqui libera fabricação.

---

## Histórico preservado — situação documental em 21/10/2026

Naquela data o modelo vigente era o R41. Os PDFs listados abaixo são entregas históricas; não foram reexportados e não representam todas as alterações posteriores. Para orçamento, ler o complemento vigente R41 junto ao pacote R30. Nenhum PDF novo é declarado nesta atualização.

---

## Histórico preservado — registros abaixo podem estar superados

# Entregas em PDF

Os nomes preservam assunto, data e revisão. R28 não inclui automaticamente mudanças posteriores do modelo R30.

- [Ajuste gavetas e profundidade roupeiro 2026-10-12](pdf/Ajuste_gavetas_e_profundidade_roupeiro_2026-10-12.pdf)
- [Auditoria dimensional marcenaria 2026-10-12](pdf/Auditoria_dimensional_marcenaria_2026-10-12.pdf)
- [Caderno visual Guedala Park 2026-10-12](pdf/Caderno_visual_Guedala_Park_2026-10-12.pdf)
- [Canto quarto FreeCAD R03 2026-10-13](pdf/Canto_quarto_FreeCAD_R03_2026-10-13.pdf)
- [Guedala R28 Ferragens sequencias conferencia](pdf/Guedala_R28_Ferragens_sequencias_conferencia.pdf)
- [Guedala R28 Pranchas cotadas](pdf/Guedala_R28_Pranchas_cotadas.pdf)
- [Pesquisa Cury 40m2](pdf/Pesquisa_Cury_40m2.pdf)
- [Quarto armario em L 2026-10-12](pdf/Quarto_armario_em_L_2026-10-12.pdf)
- [Quarto canto independente R01 2026-10-12](pdf/Quarto_canto_independente_R01_2026-10-12.pdf)
- [Quarto conferencia giro R02 2026-10-12](pdf/Quarto_conferencia_giro_R02_2026-10-12.pdf)
- [Renders dos ambientes 2026-10-12](pdf/Renders_dos_ambientes_2026-10-12.pdf)
# Pacote atual para orçamento — R30

[Caderno R30 — PDF de 28 páginas](pdf/Guedala_R30_Pacote_para_orcamento.pdf) · Escopo e arquivos de apoio.

Projeções dos vinte módulos atualizadas da R30, corte de cocção, ferragens de referência, complementos e ficha de resposta. Sete apoios propostos como alternativa separada. Orçamento preliminar condicionado; sem liberação de fabricação. As entregas R28 abaixo são históricas.

**Pacote localR17 —25/10/2026:** `Compartilhar_R17/Guedala_Park_R17.zip` (cópia local, fora do Git/site). [Avanços e condições](../04_Moveis/Proximas_decisoes/README.md). O registro R16 é histórico; este ZIP R17 não está disponível no clone ou no site.
