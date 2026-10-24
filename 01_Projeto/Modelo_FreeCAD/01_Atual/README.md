> **Modelo vigente — R48, 24/10/2026:** abra o [FreeCAD R48](../../Depurador_sem_canal_R48_2026-10-24/Guedala_Park_R48_Depurador_sem_canal.FCStd) ([o que mudou](../../Depurador_sem_canal_R48_2026-10-24/README.md)). Parte da [R46](../../Fichas_no_CAD_R46_2026-10-24/README.md) (geometria R45, cores R16, rodízios P08 e fichas R14). No aéreo D, sai o canal de duto, porque o depurador não tem duto, e o divisor vai até o fundo. Também saem as reservas ocultas sem decisão: a proteção lateral de 10 mm do quarto, a faixa de cadeira do escritório e o grupo R31 da cocção. O atalho `Abrir_no_FreeCAD.ps1` aponta para a R48. Os registros abaixo são históricos.

> **Histórico — cores R16:** [FreeCAD R45 com aparência R16](../../Cores_FreeCAD_R16_2026-10-23/Guedala_Park_R45_Cores_R16.FCStd). Geometria preservada; interiores Branco TX e faces aparentes conforme site e fichas.

> **Consulta vigente — 23/10/2026:** use o [menu do projeto](https://github.com/queiroz-labs/guedala-park#menu-do-projeto), com o **FreeCAD R45** e as **fichas técnicas R14**. Esta página reúne registros anteriores e ainda não foi reconciliada integralmente com a entrega atual. Menções abaixo a “atual” ou “vigente” pertencem à revisão de cada registro. As definições novas das fichas não estão todas aplicadas ao modelo.

# Revisão vigente R44 — 22/10/2026

[FreeCAD R44](FGVTN_R44_2026-10-22/Guedala_Park_R44_Consolidado.FCStd) · [Conferência e limites](FGVTN_R44_2026-10-22/LEIA-ME.md) · [Resposta e anexos FGVTN](FGVTN_R44_2026-10-22/Fontes/LEIA-ME.md).

R44 salva e reaberta a partir da R43, preservada integralmente. Acrescentadas referências oficiais da corrediça FGVTN 400 mm nos estados aberto e fechado, em grupo oculto e nas coordenadas de origem. Curso geométrico de 374,3 mm. **Não são ferragens instaladas nem montagem aprovada.** Berlin, cores, banco com duas tampas e duas almofadas, gabinete do banheiro com portas de correr e remoção dos apoios de óculos/celular preservados.

A hipótese de posicionamento ensaiada nas duas gavetas do escritório apresentou interferências; foi rejeitada sem recortar a madeira. O estudo R04 mantém sua capacidade e fixação frontal, mas não foi incorporado definitivamente. Faltam referência de montagem, engates e folgas de liberação, parafusos e recortes traseiros. Não extrapolar os STEP de 400 para 500 mm. FGVTN informou separadamente que não tem ferragem adequada para o cesto. Nenhuma fabricação, compra ou contato autorizado por esta revisão.

O orçamento R43 de 22/10/2026 continua sendo a referência financeira; a inclusão dos STEP não demonstra economia adicional. As quatro dobradiças antigas do banheiro são históricas na solução de correr e não devem retornar à lista de compra.

---

## Registros anteriores — consultar a atualização acima em caso de divergência

# Revisão vigente R42 — 22/10/2026

[Modelo consolidado](Consolidacao_R42_2026-10-22/Guedala_Park_R42_Consolidado.FCStd). Dois apoios de celular/óculos removidos; Berlin em configurações de estudo; FGVTN candidata para nove gavetas e 46 dobradiças comuns, sem substituir silenciosamente a geometria Blum. Banco, armazenamento e demais móveis preservados. Medidas de projeto; não libera fabricação. R41 preservada.

---

**Histórico R41 —20/10/2026:** estudo da frente500mm. Altura enquadrada na tabelaBV0; carga de8kg de roupa e retenção ainda não aprovadas. R39/R40 preservadas. [Estudo e modelo](Cesto_R41_2026-10-20/README.md).

**Histórico R40 —20/10/2026:** pesquisa de ferragem do cesto; meta provisória8kg de roupa. Nenhuma alternativa aprovada sem confirmação de carga, retenção e montagem. R39 preservada. [Pesquisa, fontes e modelo](Cesto_R40_2026-10-20/README.md).

**Histórico R39 — 20/10/2026:** estudo do movimento real do cesto; R38 preservada. Giro55 permanece ideal. Tulha40L comparada com documentação oficial, sem substituição de geometria ou liberação para compra. [Estudo e conferências](Cesto_R39_2026-10-20/README.md).

**Atualização R38 — 20/10/2026:** fornecedores brasileiros conferidos, 18 acoplamentos atualizados para T51.7601, planta Cury revisada e R37 preservada. O fechamento integral depende dos dados indicados na matriz. [Modelo, seleção e verificações](Ferragens_R38_2026-10-20/README.md).

**Atualização R37 —20/10/2026:** extensão guardada por cima, R36 preservada; seleção de ferragens comercializadas no Brasil. [Modelo e conferências](Banco_superior_R37_2026-10-20/README.md).

**Atualização R36 — 20/10/2026:** extensão da mesa, transferência da folha e biblioteca de ferragens oficiais; mecanismos sem eixos confirmados continuam pendentes. [Modelo e conferências](Mesa_R36_2026-10-20/README.md). R35 preservada.

# Histórico R35

[FreeCAD R35](Movimentos_R35_2026-10-21/Guedala_Park_R35_Movimentos.FCStd) · [Auditoria, causas e soluções](Movimentos_R35_2026-10-21/README.md).

Placa de ocultação do varal removida; varal preservado. 65 comandos testados em 195 posições. Controles antigos do R03 retirados da operação atual; abertura da mesa, retirada de forno/grelhas e descida ilustrativa do varal incorporadas. O relatório distingue movimentos operantes de mecanismos ainda não modelados. R34 preservada.

# Histórico R34

[Abrir o apartamento único](Apartamento_unico_R34_2026-10-21/Guedala_Park_R34_Apartamento_Unico.FCStd) · [Conferências e controles](Apartamento_unico_R34_2026-10-21/README.md) · [Medidas](Apartamento_unico_R34_2026-10-21/Medidas_R34.csv).

Orientação correta incorporada à geometria nativa, sem depender de outro apartamento espelhado. R33 preservada. Conferência de 1.128 peças, 21 envelopes e 60 comandos ativos em 180 posições após reabertura. As duas portas corrigidas continuam visíveis e salvas fechadas. Controles e edição paramétrica mantidos.

# Histórico R33

**20/10/2026 — conferência ampliada R33.** [Abrir o FreeCAD](Conferencia_R33_2026-10-20/Guedala_Park_R33_Conferencia.FCStd) · [Visão geral](Conferencia_R33_2026-10-20/Apartamento_R33.png) · [Medidas completas](Conferencia_R33_2026-10-20/Medidas_completas_R33.csv) · [Conferência](Conferencia_R33_2026-10-20/Conferencia_R33.json) · [Teste das portas](Conferencia_R33_2026-10-20/Portas_amostragem_R33.json).

A R33 inclui recortes, uniões e cilindros que a medição R32 omitia. O canto tem altura308, não306; as diferenças de5,2mm de algumas profundidades eram omissões das frentes recortadas. No banco, caixa/assento450 + encosto separado100 confirmam a profundidade externa550. A ponta do estudo lateral acrescenta50 ao comprimento1800; seu envelope continua1850. A reversão do banco permanece adiada.

Duas frentes da cozinha estavam indevidamente ocultas: portas esquerdas do aéreo C e do módulo B sobre o micro-ondas. Correção concluída e salva: peças, dimensões, furações e controles preservados. Ambas passaram individualmente nas quatro posições de abertura testadas contra outros módulos/objetos correntes, e foram salvas fechadas. [Registro da correção](Conferencia_R33_2026-10-20/Portas_restauradas_R33.json) · [Teste das duas portas corrigidas](Conferencia_R33_2026-10-20/Duas_portas_corrigidas_R33.json) · [Salvamento na sessão FreeCAD](Conferencia_R33_2026-10-20/Salvamento_sessao_R33.json). A amostragem anterior que não localizava essas duas frentes fica superada nesse ponto.

Conferência final:1.128 formas correntes válidas;342.642 pares entre módulos considerados, sem sobreposição volumétrica acima de0,1mm³ na pose salva. A R32 original permanece intacta. A correção foi sincronizada com a sessão aberta, sem alterar o foco do monitor principal.

A verificação entre os20 módulos é estática. O teste de abertura é amostrado, uma porta por vez: não comprova movimento contínuo, operação simultânea, ferragens reais ou espaço para pessoas. A entrada aberta do banheiro intercepta a frente do gabinete; com a entrada fechada, as duas frentes inferiores passaram nas dez posições testadas. [Conferência da condição de uso](Conferencia_R33_2026-10-20/Banheiro_entrada_fechada_R33.json). Medidas de campo continuam pendentes.

**DWG preparado para a etapa final:** ODA File Converter27.9.0 instalado e configurado no FreeCAD. Exportação e reimportação de um retângulo1000×500mm passaram, preservando as medidas; assinatura DWG AC1015. [Instalação e teste](../05_Ferramentas_e_registros/DWG_2026-10-20/Instalacao_e_teste.json). Teste2D local, não validação dentro do AutoCAD nem exportação final do apartamento. Nenhum arquivo enviado a terceiros. Site R11 e PDFs anteriores permanecem históricos.

## Histórico R32 — medição parcial, superada

**20/10/2026 — auditoria dimensional R32.** [Abrir o modelo](Auditoria_R32_2026-10-20/Guedala_Park_R32_Auditoria.FCStd) · [Medidas dos 20 módulos](Auditoria_R32_2026-10-20/Medidas_modulos_R32.csv) · [Auditoria completa](Auditoria_R32_2026-10-20/Auditoria_R32.json) · [Reabertura verificada](Auditoria_R32_2026-10-20/Reabertura_R32.json).

A R32 acrescenta a planilha `AuditoriaDimensionalR32` e critérios de medição aos módulos, dentro de Documentação no FreeCAD. Foram conferidas 1.094 formas correntes válidas e 136 pares de peças da cocção sem sobreposição volumétrica superior a 0,1 mm³. A geometria, os controles e a preferência de adiar a revisão do banco foram preservados.

As medidas da caixa não devem ser usadas como dimensões do conjunto: tampo, rodas, apoios e saliências mudam o envelope. No banco, a decisão de 08/10 distingue profundidade externa prevista de 550 mm e assento/caixa de 450 mm; o módulo isolado não comprova o envelope externo completo. A planilha mede componentes correntes na pose salva, nos eixos globais da base de edição; não é lista de corte. Medidas de campo, colisões dos outros ambientes e movimentos completos continuam pendentes.

Arquivo reaberto pelo núcleo FreeCAD com 6.193 objetos, sem estados de erro. Dados gráficos da R31 preservados byte a byte após o salvamento sem interface. A abertura visual nesta sessão não foi confirmada; não repetir abertura durante uma carga em andamento. Site R11 e PDFs anteriores não foram atualizados nesta auditoria.

[Voltar ao guia FreeCAD](../README.md)

A revisão R31 consolida as decisões e estudos até 20/10/2026. A preferência de voltar ao baú convencional está apenas anotada; não foi aplicada ao desenho do banco.

- [R31 — arquivo, alterações e conferências](Consolidacao_R31_2026-10-20/README.md).
- [R30 — revisão anterior preservada](Consistencia_R30_2026-10-14/README.md).
