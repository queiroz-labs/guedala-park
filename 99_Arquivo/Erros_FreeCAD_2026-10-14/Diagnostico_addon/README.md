# Diagnóstico do addon AICopilot - Qt

Leitura estática da instalação específica. Nenhum arquivo instalado, GUI, servidor ou observador foi alterado/reiniciado. Não foram lidos históricos de interação, credenciais ou logs do Codex. O patch está preparado somente como artefato para revisão/aplicação pelo responsável.

## Causa confirmada

`event_observer.py`6 importa `QtCore` diretamente de `PySide2`. O startup em `InitGui.py`59–67 tenta importar essa classe e registra a exceção como `Event observer error`. A instalação FreeCAD1.1.4 possui wrapper nativo `Ext/PySide/QtCore.py` que reexporta **PySide6.QtCore**, não PySide2. O caminho antigo impede a importação mesmo quando a interface e o servidor já funcionam em Qt6.

Arquivo exato:

`C:/Users/Elias/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Roaming/FreeCAD/v1-1/Mod/AICopilot/event_observer.py`

Foi encontrado outro import direto incompatível em:

`C:/Users/Elias/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Roaming/FreeCAD/v1-1/Mod/AICopilot/commands/ai_commands.py`5

Esse segundo módulo importa QtCore/QtGui/QtWidgets de PySide2 ao carregar os comandos. O servidor já usa `from PySide import QtCore` em `socket_server.py`15, demonstrando o padrão compatível existente dentro do próprio addon. Não há outro import PySide2 direto nos arquivos Python examinados da pasta do addon.

## Patch mínimo preparado

[Compatibilidade_Qt.patch](Compatibilidade_Qt.patch):

- Observer: trocar apenas `from PySide2 import QtCore` por `from PySide import QtCore`.
- Comandos: importar QtCore/QtGui do wrapper `PySide`; tentar QtWidgets do wrapper. Se uma versão antiga do wrapper FreeCAD não possuir QtWidgets separado, usar QtGui como alias de widgets.

O wrapper da instalação corrente tem `QtGui.py` reexportando PySide6.QtGui **e** PySide6.QtWidgets, além de `QtWidgets.py` reexportando os widgets. Usar o wrapper escolhe a família Qt da própria instalação, em vez de carregar uma segunda família Qt arbitrariamente. Não é necessário instalar PySide2 para consertar o import.

[Diagnostico_Qt.json](Diagnostico_Qt.json) registra os dois caminhos, hashes das fontes exatas, imports antes/depois e arquivos propostos. As cópias `.proposto` são artefatos, não foram gravadas sobre a instalação. As duas versões propostas passaram por análise sintática AST; isso não é teste de import no runtime FreeCAD.

## APIs utilizadas e verificação de aplicação

Observer: `QtCore.QObject` e `QtCore.QEvent` (`HoverEnter`, `MouseButtonPress`). O evento de mouse usa `x()`/`y()`. Comandos: `QMessageBox`, `QDialog`, `QVBoxLayout`, `QTabWidget`, `QTextEdit`, `QListWidget`, `QDialogButtonBox`, constantes Information/Ok e chamadas `exec_()`.

O patch mantém essas chamadas; não presume que toda API legada do addon foi homologada em Qt6 apenas por resolver o import. [verificar_api.py](verificar_api.py) inspeciona presença das classes/aliases usados, sem iniciar observadores, servidor, diálogos ou coletar eventos. O responsável pode executar essa inspeção curta na GUI atual e revisar o resultado antes da aplicação. Se algum alias faltar efetivamente, adaptar apenas o caso demonstrado, sem mudanças especulativas.

Antes de escrever fora do workspace, conferir que as fontes instaladas continuam iguais aos hashes registrados e guardar backup recuperável. Depois verificar a importação do módulo corrigido no runtime correto. Uma importação bem-sucedida não é prova de que o observer foi iniciado ou de que o console inteiro ficou sem erros.

`InitGui.py` marca o serviço como ativo mesmo quando o observer falha. Portanto, reaplicar/importar o arquivo não garante nova tentativa automática. Não reiniciar cegamente o serviço: `stop()` não remove explicitamente observadores de seleção/documento/event-filter já instalados, e um reinício pode duplicar hooks se havia observador ativo. O responsável deve distinguir observer ausente de ativo e preservar o servidor que atende a sessão.

Nenhuma mudança no CAD, fontes STEP, projeto ou decisão de Elias é necessária para estes imports. Outros erros do console devem ser tratados separadamente pelo responsável, com a causa específica de cada mensagem.
