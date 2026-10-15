# Diagnóstico e recuperação da conexão FreeCAD

14/10/2026 · FreeCAD 1.1.4 · Integração local em 127.0.0.1:23456.

## O que foi constatado

Na primeira conferência, a ponte Python MCP estava em execução, mas não havia processo freecad.exe nem serviço ouvindo na porta 23456. A falha de conexão era uma recusa do destino local; não foi identificada mudança de conta, rede externa ou caminho do modelo.

Os [eventos do Windows](Eventos_Windows.json) registram falha nativa do freecad.exe em **14/10 às 21h23min17s**, com código **0xc0000374**, módulo reportado ntdll.dll e relatório 7c147095-4253-4afd-80bb-d2f60934803b. Também há registros de travamento anteriores. Esses registros comprovam que o aplicativo falhou, mas não identificam a operação, extensão ou componente que provocou a falha. Não foi feita análise de dump; não atribuir a causa ao modelo ou ao MCP sem essa evidência.

A ausência do aplicativo explica a indisponibilidade observada no diagnóstico. O evento anterior não prova a causa de cada encerramento posterior, inclusive o relatado durante a conversa.

## Defeitos separados encontrados na extensão

1. **Identificação do serviço:** atribuições como `FreeCAD.__ai_global_service` dentro de uma classe sofriam transformação de nome pelo Python, criando `_GlobalAIService__ai_global_service`. Os testes `hasattr(..., '__ai_global_service')` procuravam outro nome. O defeito foi confirmado no FreeCAD em execução: o atributo transformado existia e o esperado não.
2. **Reinício:** depois de corrigir os nomes, o teste real do botão encerrou o serviço mas falhou em recriá-lo com `name 'GlobalAIService' is not defined`. A fábrica da classe agora fica explicitamente armazenada no módulo FreeCAD, em vez de depender dos globais temporários de InitGui.
3. **Limpeza:** o reinício agora remove o observador de seleção, documento e filtro de eventos antes de liberar sua referência.
4. **Status:** removida a checagem de arquivo Unix `/tmp/freecad_mcp.sock` da mensagem da interface, que mostrava “Disconnected” no Windows mesmo com TCP ativo. A mensagem agora descreve o estado local do serviço; o teste MCP efetivo continua necessário.

Esses problemas prejudicavam status/reinício; não são uma explicação comprovada para a falha nativa das 21h23.

## Alterações e restauração

A instalação ativa usa `C:/Users/Elias/AppData/Roaming/FreeCAD/v1-1/Mod/AICopilot`. A cópia antiga em `FreeCAD/Mod/AICopilot` tinha o mesmo conteúdo; ambas receberam a correção em InitGui.py para evitar divergência entre versões. O servidor de socket e a ponte MCP não foram alterados nesta rodada.

- [Originais e hashes da primeira correção](Correcao.json).
- [Hashes finais após corrigir a fábrica](Correcao_factory.json).
- Cópias originais: [legada](InitGui_antes_0.py) e [ativa v1-1](InitGui_antes_1.py).
- Scripts da alteração: [nomes e limpeza](corrigir_servico.py) e [fábrica persistente](corrigir_factory.py). São scripts de aplicação única, não inicializadores de uso diário.

Para desfazer, com o FreeCAD fechado, restaurar cada cópia no caminho correspondente do registro. Isso também restaura os defeitos anteriores; preservar o diagnóstico para comparação.

## Testes e evidências

- Inicialização normal com log: serviço TCP voltou e uma execução Python via MCP respondeu.
- Ativação da bancada AI Copilot e comando Service Status: localizaram o serviço.
- Teste real de Restart Service após a correção final: log registrou `AI Service restarted successfully`; a chamada seguinte chegou ao FreeCAD e confirmou nova instância do serviço em execução.
- [Log da validação](FreeCAD_validacao.log); [log do teste que revelou a fábrica ausente](FreeCAD_corrigido.log); [log da recuperação inicial](FreeCAD_reinicio.log).

A validação é funcional desta sessão, não garantia de ausência de falhas futuras. Logs estão habilitados na instância de diagnóstico para preservar evidência se o problema reaparecer. A consulta de ajuda abriu uma janela informativa incidental, encerrada durante o diagnóstico; ela não modificou o modelo.

## Abertura da R30 e limite de resposta

Depois do reinício bem-sucedido, a abertura do FCStd foi solicitada por MCP. A chamada ultrapassou o limite de resposta da ponte enquanto o FreeCAD continuava processando. O título da janela passou de “Unnamed” para o nome da R30 e o tempo de CPU continuou aumentando: isso demonstra progressão da carga, não conclusão. Não foi enviada uma segunda solicitação de abertura nem houve encerramento forçado ou salvamento do documento.

O erro inicial “conexão recusada” e esse timeout são situações distintas. A conexão inicial não encontrava serviço; a segunda chamada foi recebida e executada, mas não terminou dentro do prazo. O registro `WinError 10054` durante a carga é compatível com o encerramento da conexão do cliente após o timeout; não prova uma nova falha nativa do FreeCAD.

**Resultado final: a carga terminou.** O [registro da abertura](Validacao_MCP.json) confirmou a R30 com 6.128 objetos. Uma nova chamada MCP após a carga confirmou documento ativo, serviço em execução e SHA-256 do arquivo inalterado: [validação final](Validacao_final.json). A janela do FreeCAD foi reapresentada com o modelo aberto, sem salvar ou modificar sua geometria. Não repetir operações demoradas apenas porque a ponte excedeu seu prazo; primeiro conferir se a operação anterior terminou.
