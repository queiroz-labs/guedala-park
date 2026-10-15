$ErrorActionPreference = 'Stop'
$workspaceRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '../../../..')).Path
$sourceRoot = Join-Path $workspaceRoot 'tmp/freecad-mcp-source'
$integrationRoot = Join-Path $env:LOCALAPPDATA 'Programs/FreeCAD-MCP'
$addonRoot = Join-Path $env:APPDATA 'FreeCAD/Mod/AICopilot'
if (Test-Path -LiteralPath $addonRoot) { throw 'AICopilot já existe; conferir antes de substituir.' }
New-Item -ItemType Directory -Path $integrationRoot -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $sourceRoot 'AICopilot') -Destination $addonRoot -Recurse
Copy-Item -LiteralPath (Join-Path $sourceRoot 'working_bridge.py') -Destination (Join-Path $integrationRoot 'working_bridge.py')

# Route commands through FreeCAD's GUI task queue. Upstream executes Python
# directly from socket threads; document and view changes must run on the GUI thread.
$socketFile = Join-Path $addonRoot 'socket_server.py'
$socketCode = Get-Content -LiteralPath $socketFile -Raw
$oldDispatch = '            result = self._execute_tool(tool_name, args)'
$newDispatch = @'
            response_queue = queue.Queue(maxsize=1)
            def run_on_gui():
                try:
                    response_queue.put((True, self._execute_tool(tool_name, args)))
                except Exception as error:
                    response_queue.put((False, str(error)))
            gui_task_queue.put(run_on_gui)
            ok, result = response_queue.get(timeout=180)
            if not ok:
                raise RuntimeError(result)
'@
if (-not $socketCode.Contains($oldDispatch)) { throw 'O dispatcher do upstream mudou; rever patch.' }
$socketCode = $socketCode.Replace($oldDispatch, $newDispatch).Replace("self.host = 'localhost'", "self.host = '127.0.0.1'")
[IO.File]::WriteAllText($socketFile, $socketCode, [Text.UTF8Encoding]::new($false))
$bridgeFile = Join-Path $integrationRoot 'working_bridge.py'
$bridgeCode = Get-Content -LiteralPath $bridgeFile -Raw
$bridgeCode = $bridgeCode.Replace("sock.connect(('localhost', 23456))", "sock.settimeout(180)`n                sock.connect(('127.0.0.1', 23456))")
[IO.File]::WriteAllText($bridgeFile, $bridgeCode, [Text.UTF8Encoding]::new($false))
python (Join-Path $PSScriptRoot 'ajustar_ponte.py')
if ($LASTEXITCODE -ne 0) { throw 'Falha ao ajustar a ponte.' }

python -m venv (Join-Path $integrationRoot '.venv')
if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar ambiente Python.' }
$mcpPython = Join-Path $integrationRoot '.venv/Scripts/python.exe'
& $mcpPython -m pip install 'mcp==1.30.0' --disable-pip-version-check --quiet
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar MCP.' }
codex mcp add freecad -- $mcpPython $bridgeFile
if ($LASTEXITCODE -ne 0) { throw 'Falha ao registrar MCP no Codex.' }

$installRecord = [ordered]@{
    installed_at = '2026-10-13'
    freecad_version = '1.1.4'
    freecad_exe = (Join-Path $env:LOCALAPPDATA 'Programs/FreeCAD-1.1.4/bin/freecad.exe')
    upstream = 'https://github.com/contextform/freecad-mcp'
    upstream_commit = 'de4fed2a7a4352fcb0de60d2b784063c54eeb812'
    bridge = $bridgeFile
    python = $mcpPython
    addon = $addonRoot
    endpoint = '127.0.0.1:23456'
    local_changes = @('Comandos encaminhados à thread GUI', 'Socket restrito a IPv4 loopback', 'Timeout de 180 s na ponte', 'Conferência real da conexão no Windows', 'Leitura de respostas JSON completas')
}
$installRecord | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'Instalacao.json') -Encoding utf8
$installRecord | ConvertTo-Json -Depth 4
