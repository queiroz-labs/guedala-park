# Entregas — manifesto e versões

**Atualização de alturas / R25, 27/10/2026:** Elias solicitou 2,60 m nos cômodos e 2,50 m no banheiro, incluindo documentos, commit/push e site. Medidas de projeto a confirmar. [Pranchas R02](Caderno_pranchas/index.html), CSV e site sincronizados; cenário de 2,47 m do escritório substituído. Publicado e conferido em 27/10/2026: [workflow concluído](https://github.com/queiroz-labs/guedala-park/actions/runs/40600491788), metadados por ambiente e PDF remoto corretos; ZIP R25 com 295 entradas, CRC e hashes de todas as entradas verificados. [Baixar R25](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Publicacao/Guedala_Park_R25.zip). CAD R53 preservado.

**Cotação para envio por Elias, 27/10/2026:** [checklist](Cotacao/index.html), 20 páginas individuais por destinatário e [pacote completo](Cotacao/Pacote_cotacao.zip). [Marcenaria.zip](Cotacao/Marcenaria.zip) inclui pedido D05-C/D06-B, fichas R15 integrais do manifesto e formulário atualizado; sem FCStd ou orçamento interno. Amostras D02 A/C e IL02–IL09 separadas, prazo solicitado 30/10 às 18 h. Todos não enviados. Gerar com `python -B ferramentas/estudos/gerar_pedidos_cotacao.py`; fontes comerciais nas listas de iluminação/chapas, canal Tramontina confirmado no [formulário oficial](https://globaltramontina.zendesk.com/hc/pt-br/requests/new).

**Pranchas A3 R02, 27/10/2026:** [caderno](Caderno_pranchas/index.html), [PDF R02](Caderno_pranchas/Guedala_Park_Pranchas_R02.pdf) e [instruções/fontes](Caderno_pranchas/README.md). 20 folhas vetoriais: plantas 1:50, elevações e detalhe 1:25; pontos R01, envelopes R53 e cotas vinculadas ao CSV. Comando: `python ferramentas/pranchas/gerar.py`. R00 preservado; R02 incluído no pacote R25 autorizado. Verificação completa do FCStd passou sem alteração do arquivo. Teste externo 2,60→2,47: 12 elevações e 99 cotas alteradas, conflitos P09–P12 de 80 mm sinalizados; cópia apagada. Pranchas formais: 80% estimados, limites no README do caderno.

**Publicação anterior R53/R24,27/10/2026:** decisões P02/P13/TV/lixeiras integradas ao modelo e fichas R15. [Modelo e relatório](../02_Modelo_3D/README.md) · [fichas atuais](Fichas_fabricacao/index.html). Publicação autorizada por Elias, 27/10/2026: “Pode fazer push e publicar a R53 com as fichas R15 e o pacote R24”. Publicação conferida em 27/10/2026: [workflow concluído](https://github.com/queiroz-labs/guedala-park/actions/runs/40519714291), metadados R53/R24/R15, 27 arquivos do site idênticos ao build validado e fichas P02/P13 corretas. ZIP remoto com 264 arquivos, CRC e hashes íntegros, 239 fontes canônicas conferidas. Verificação completa R53 passou 106 cenários; site e selagem do pacote passaram. Os artefatos locais de revisão são gerados fora desta pasta para preservar o pacote histórico existente. [Baixar ZIP R24](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Publicacao/Guedala_Park_R24.zip). Extraia inteiro e abra `Guedala_Park_R24/COMECE_AQUI.html`. Os registros R52/R23 abaixo são históricos da publicação anterior.

**Correção da planta / pacote R23, 26/10/2026:** lavanderia 1,29 × 1,54 m; circulação com trechos perpendiculares de 0,90 m e 1,05 m, acessos e ligação à sala separados. Fechamentos gráficos do banheiro de 16/17 cm são derivados, não espessuras medidas. Portas, janelas, móveis e FreeCAD preservados. Pé-direito visível em **Planta com medidas → Pé-direito para testes**, âncora `#planta-pe-direito`: 2,60 m, medida a confirmar, não fabricação; forro de 2,47 m separado. A hipótese anterior de cozinha 2,57 m foi reconciliada em Escolhas. Publicação desta correção autorizada por Elias em 26/10/2026, mensagem Sentinel_3ce 273ee 835081919acefb 805f 637632: "Sim, autorizo comitt push". R23 sucede a configuração R22; os registros T09 abaixo retratam a conferência anterior. Testes em 360, 412 e 1440 px: âncora abre a aba correta, aviso visível e sem transbordamento horizontal.

## Manifesto de versões — conferência T09 em 26/10/2026

| Item | Versão conferida | Evidência e limite |
|---|---|---|
| Modelo | R52 | `Guedala_Park_R52_Corrigido.FCStd` (histórico Git); SHA256 interno do ZIP remoto corresponde ao manifesto |
| Fichas | R14 | [Índice](Fichas_fabricacao/index.html); revisão indicada no pacote e no site |
| Pacote publicado | R23 | [Baixar ZIP R23](https://queiroz-labs.github.io/guedala-park/docs/06_Entregas/Publicacao/Guedala_Park_R23.zip); 251 entradas, CRC e hashes de todas as entradas do manifesto sem falhas |
| Pacote local histórico | R20 | `Publicacao/Guedala_Park_R20.zip`; 196 entradas, CRC e hash CAD conferidos; não representa a entrega corrente |
| Pranchas | R00 | [PDF](Caderno_pranchas/Guedala_Park_Pranchas_R00.pdf); compatibilização das vistas antigas com R52 ainda pendente |
| Orçamento | R44 | [Consolidado](../05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md); execução estimada R$ 137.748,11 |
| Especificações | R01 | [Caderno](../01_Programa_e_decisoes/Caderno_de_especificacoes.md); coerência integral com estudos posteriores condicionada |

**Evidência remota, 26/10/2026:** [versao.json](https://queiroz-labs.github.io/guedala-park/versao.json) identifica R52/R23, fichas R14 e commit `ba67dee8645dc0e79d71edbd51f29977aa3f35fe`. O ZIP foi lido em memória: 30.325.371 bytes, SHA256 `df5b592043d841684b6067456352a0c6eb75c8a9dacf0edea5be8e2e4e4dd1d2`; `COMECE_AQUI.html` presente. CAD interno: SHA256 `941da02d367c5f6ce2992f72985f86c3aceba23f899a4c394cf3569f19d7b4da`. Integridade não equivale à abertura gráfica do CAD/PDF nem à compatibilização de vistas.

R21/R22 são referências anteriores; o campo `lastPublishedPackageRevision` foi reconciliado de R18 para R23 com essa evidência. A publicação já existia: esta conferência não fez deploy. O ZIP R20 local foi preservado; SHA256 `ba2f547f21760506dc4331f78103bab1c1d5b6aaf70f27e0a239d3c27fe80be8`.

**Validação local:** `python -B ferramentas/verificar_site.py` passou nos seis testes iniciais, geração temporária de site/pacote e teste de selagem. A primeira tentativa parou por acesso negado ao temporário do ambiente; a repetição usou TEMP/TMP graváveis fora do repositório, sem alterar o verificador. As saídas temporárias do teste foram removidas pelo próprio script.

**Próximo:** compatibilizar vistas antigas com R52 e conferir abertura gráfica de CAD/PDF, navegação offline e cópia de segurança na integração de 30–31/10. Ensaios, produto, juntas e medidas reais continuam condicionados. Sem oficina, seguir T04 e interfaces T05 conforme o plano.

O pacote publicado anterior permanece R23. Extraia o ZIP R23 inteiro e abra `Guedala_Park_R23/COMECE_AQUI.html`. As fichas correntes são [R15](Fichas_fabricacao/index.html), [pendências](Fichas_fabricacao/Pendencias.html) e o [Estado atual](../ESTADO_ATUAL.md). Estudos separados não são incorporados automaticamente à geometria R52.

## Histórico — entrega R49/R16 de 24/10/2026

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

Naquela data o modelo vigente era o R41. Os PDFs listados abaixo são entregas históricas; não foram reexportados e não representam todas as alterações posteriores. O complemento R41 e o pacote R30 pertencem àquela entrega; para o orçamento atual, usar o [consolidado R44](../05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md). Nenhum PDF novo é declarado nesta atualização.

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
- [Pesquisa Cury 40 m 2](pdf/Pesquisa_Cury_40m2.pdf)
- [Quarto armario em L 2026-10-12](pdf/Quarto_armario_em_L_2026-10-12.pdf)
- [Quarto canto independente R01 2026-10-12](pdf/Quarto_canto_independente_R01_2026-10-12.pdf)
- [Quarto conferencia giro R02 2026-10-12](pdf/Quarto_conferencia_giro_R02_2026-10-12.pdf)
- [Renders dos ambientes 2026-10-12](pdf/Renders_dos_ambientes_2026-10-12.pdf)
# Pacote histórico para orçamento — R30

[Caderno R30 — PDF de 28 páginas](pdf/Guedala_R30_Pacote_para_orcamento.pdf) · Escopo e arquivos de apoio.

Projeções dos vinte módulos atualizadas da R30, corte de cocção, ferragens de referência, complementos e ficha de resposta. Sete apoios propostos como alternativa separada. Orçamento preliminar condicionado; sem liberação de fabricação. As entregas R28 abaixo são históricas.

**Pacote local R17 —25/10/2026:** `Compartilhar_R17/Guedala_Park_R17.zip` (cópia local, fora do Git/site). [Avanços e condições](../04_Moveis/Proximas_decisoes/README.md). O registro R16 é histórico; este ZIP R17 não está disponível no clone ou no site.

## Referências antigas — triagem T09

Busca nos Markdown de entrada e referências cruzadas em 26/10/2026: encaminhamento do montador corrigido para fichas R14; roteiro oficial aponta ao modelo R52 e orçamento R44; rascunho de reforma identifica R44. O nome `Orcamento_R43.md` permanece por instrução do pedido A: seu conteúdo é R44. Revisões próprias R00/R01/R14 e links de evidência histórica não são erros por terem número menor que R52.

| Referência sem substituição integral demonstrada | Pendência para Elias/projeto |
|---|---|
| `Dossie_marcenaria_R45.html` e [consulta R12](../ferramentas/site/fabrication/Consulta/README.md) | Nome/base R45 com trechos atualizados; usar fichas e estado como entrada. Não renomeado, apagado nem tratado como cópia integral da R52. |
| [Planta mobiliada R02](../03_Ambientes/Planta_mobiliada/README.md), [programa R01](../01_Programa_e_decisoes/Programa_de_necessidades.md) e pranchas R00 | Documentam geometria R45; sem artefato substituto demonstrado nesta tarefa. Conferir vistas contra R52 numa integração autorizada; não trocar a revisão escrita sobre desenhos antigos. |
| [Painel de decisões](../01_Programa_e_decisoes/Painel_de_decisoes.md) | Cabeçalho de pacote R18 e blocos datados chamados “vigente R44/R43”; ler como registro histórico onde superado pelo estado. Falta conciliar pacote e reorganizar a entrada sem perder fontes. |
| [Registro de publicação](../ferramentas/site/Publicacao_GitHub_Pages.md) | “Revisão vigente R05” pertence ao registro de setembro; não é confirmação da versão online atual nem autorização de push nesta tarefa. |

A conferência T09 acima verificou o ZIP remoto R23 e o ZIP local histórico R20; vistas antigas continuam pendentes. Revisões de estudos antigos permanecem nas fontes; dúvidas acima não foram resolvidas por simples troca de rótulo.

Fechamento da cotação: 20 pedidos individuais conferidos visualmente e sem transbordamento; ZIP R15 com CRC e 94 arquivos do manifesto idênticos aos originais. Sem envio, push ou alteração de FCStd.

## Pranchas formais R02 — fontes

Caderno paramétrico R02 gerado: CSV com precedência do medido, vínculos em Cotas.json e envelopes R53 com SHA. O R00 permanece preservado; impacto e conflitos são relatados a cada geração. [Ferramentas](../ferramentas/pranchas/README.md).
