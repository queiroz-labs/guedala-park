# R24 — implantação corrigida do sofá e referências ocultas

Arquivo atual: Guedala_Park_R24_Implantacao_Corrigida.FCStd. Incorpora R23 e preserva todas as revisões anteriores. O apartamento continua espelhado, com cozinha à esquerda ao entrar e portas vizinhas alternadas. Armários, programa, ferragens, controles e dimensões não foram alterados.

A revisão global encontrou o sofá-cama Daiane majoritariamente do lado do quarto, com corpo e encosto atravessando a parede do escritório. A causa está na conversão do estudo interativo: `app.js` aplica o sinal oposto de yaw ao converter suas coordenadas XZ para XY do CAD; o importador usou o mesmo sinal. As sete primitivas foram giradas rigidamente em180° em torno de(2570,2220) no referencial-fonte. Isso equivale à orientação correta do original, sem reduzir ou espelhar localmente o sofá.

O corpo agora ocupa X2570–3470/Y1520–2920 no referencial-fonte, correspondente ao ensaio documentado x2–92/y152–292cm no escritório de230×295cm. Na composição espelhada ocupa X3930–4830. Mantém140×90cm de planta fechada, encosto junto à parede e afastamento nominal20mm. Esse afastamento vem do estudo existente; não é tolerância física garantida nem comprovação da conversão em cama.

Foram ocultados três vínculos exibidos indevidamente: duas peças Daiane com opacidade0 no modo diário do estudo original (`EspelhoPecaR041/R042`, fontesPeca127/128) e o volume antigo do tanque (`EspelhoPecaR123`, fontePeca358). As fontes foram preservadas. O tanque atual e a bancada a recortar permanecem no projeto, com seus limites de gabarito e recorte real pendente.

## Verificação da alteração

[Correcao_R24.json](Correcao_R24.json):5895 objetos comparados antes/depois; somente sete Placements e três visibilidades alterados, além do rótulo do documento. Pais, expressões, volumes, tipos de parâmetros e movimentos preservados. R23 com SHA inalterado, nenhuma expressão inválida.

[Conferencia_correcao_R24.json](Conferencia_correcao_R24.json): versão salva aberta em processo separado; sete matrizes/volumes e três vínculos ocultos persistentes. Cinco primitivas vigentes do sofá contra955 alvos (27paredes, novepisos e919outros sólidos selecionados):4775 pares separados pelo BBox, nenhuma interpenetração/erro. Não repetiu a auditoria estática dos objetos inalterados. Não há sólido de teto para conferir.

## Auditorias que motivaram a correção

- [Arquitetura global R23](../Auditoria_implantacao_R23_2026-10-14/README.md):927 resultados exibidos contra27paredes/novepisos, duas interpenetrações reais no sofá; um volume histórico exibido identificado. Depois das três ocultações,924 resultados atuais permanecem nessa seleção.
- [Posições e importação R23](../Auditoria_posicoes_R23_2026-10-14/README.md):correspondência com a implantação original e controles; diagnóstico do sinal de rotação e opacidade. Consultar escopo e limites da entrega.
- [Encontros entre módulos R23](../Revisao_integrada_R23_2026-10-14/Encontros_modulos_R23.json):398480 pares entre raízes distintas com ao menos um módulo; quatro comuns. Dois eram com o tanque histórico agora oculto; dois são reservas do tanque/vazio útil atravessando a bancada ainda não recortada. Esses últimos são pendência de recorte/produto, sem geometria de execução inventada.

A conferência cobre a implantação diária salva e os alvos modelados. Não valida mecanismo intermediário do sofá, hospedagem, cadeira/operador, revestimentos, produtos reais, cargas, fixações, batentes ou fabricação. Continuar revisão direcionada até19h, sem repetir testes concluídos ou reconstruir fontes históricas.

[Guia dos controles preservados](../Rotulos_R23_2026-10-14/Guia_controles_R23.md) · [Pendências técnicas](../Apartamento_espelhado_R20_2026-10-14/Pendencias_apartamento_R20.md).
