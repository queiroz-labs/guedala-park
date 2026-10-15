# Mensagens do FreeCAD — diagnóstico e correção

14/10/2026. Elias pediu corrigir todas as mensagens de erro visíveis no programa. Projeto vigente continua [R25](../../../../../01_Projeto/Modelo_FreeCAD/02_Revisoes_e_estudos/Programa_R25_2026-10-14/Guedala_Park_R25_Programa_Conferido.FCStd), sem mudança de geometria, parâmetros, hierarquia ou versão artificial.

## Causa corrigida no complemento

Dois módulos do AICopilot importavam `PySide2` diretamente, inexistente neste FreeCAD1.1.4/Qt6. Os imports de `event_observer.py` e `commands/ai_commands.py` agora usam o wrapper nativo `PySide`; QtWidgets possui fallback QtGui para wrappers antigos. Nenhuma biblioteca foi instalada, nenhum servidor foi reiniciado e nenhum observador de eventos novo foi ativado.

[Diagnóstico e patch mínimo](../../../../Erros_FreeCAD_2026-10-14/Diagnostico_addon/README.md) · [Aplicação e hashes](../../../../Erros_FreeCAD_2026-10-14/Compatibilidade_aplicada.json). Os dois arquivos originais foram preservados emBackup_addon. Os16 símbolos/aliases utilizados estão disponíveis no runtime Qt6; ambos os módulos corrigidos importaram com sucesso dentro do FreeCAD. A validação do módulo de comandos registrou seus comandos usuais, sem abrir diálogos ou acionar ligação/desligamento do serviço.

## Avisos antigos de projeto

Os avisos `out of the allowed scope` eram da tentativa R19 abortada e de uma inserção de navegação R21 que já havia sido desfeita. A [reprodução isolada na R25](../../../../Erros_FreeCAD_2026-10-14/Diagnostico_scope/README.md) abriu5898 objetos, marcou somente os20 módulos e recomputou53 objetos: nenhum aviso de escopo ouInvalid. Não se justificou converter PropertyLink para PropertyLinkGlobal, reparentar geometria ou retirar parâmetros. A R25 preservou o SHA.

As exceções antigas de scripts de montagem/vistas e o aviso de recuperação da R17 pertenciam ao histórico da sessão. Não são erros ativos da R25; os ensaios/versões abandonados não foram reexecutados. A causa original do aviso de recuperação continua indeterminada; não foi alegada reparação de um arquivo corrompido nem alterada a R17 para apagar sua mensagem.

## Histórico preservado e interface limpa

Console original preservado emErros_interface.json, catálogo emResumo_erros.json e64 notificações visíveis emNotificacoes_antes.json. Após corrigir os imports e verificar o projeto vigente, as entradas acumuladas foram limpas. As duas pequenas sessões temporárias de testeR19 foram salvas como cópias emRecuperacao_memoria antes de fechadas. As revisões anteriores no disco permaneceram intactas.

[Validação na interface](../../../../Erros_FreeCAD_2026-10-14/Validacao_interface_limpa.json):20 módulos da R25 recomputados, nenhum novo erro ou objeto inválido. [Notificações reabertas](../../../../Erros_FreeCAD_2026-10-14/Validacao_notificacoes_final.json) confirmam a limpeza persistente do painel e projeto ativoR25. Não foram desativados logs, notificações ou diagnósticos futuros; novas falhas continuam podendo aparecer normalmente.

Os resultados geométricos e pendências físicas/comerciais anteriores permanecem; esta correção não libera corte, furação, compra ou fabricação. A revisão final com Astra segue reservada para esta mesma conversa conforme plano até19h.
