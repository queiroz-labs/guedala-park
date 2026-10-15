$ErrorActionPreference = 'Stop'
$exePath = Join-Path $env:LOCALAPPDATA 'Programs/FreeCAD-1.1.4/bin/freecad.exe'
if (-not (Test-Path -LiteralPath $exePath)) { throw 'FreeCAD não encontrado no local registrado.' }

# Pasta do script; se as linhas forem coladas no console ($PSScriptRoot vazio), usa o caminho do projeto.
$raiz = if ($PSScriptRoot) { $PSScriptRoot } else { 'C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\01_Projeto\Modelo_FreeCAD' }
$atual = Join-Path $raiz '01_Atual'
if (-not (Test-Path -LiteralPath $atual)) { throw "Pasta 01_Atual não encontrada em $raiz. Consulte README.md." }

# Revisão mais recente em 01_Atual = maior número R em Guedala_Park_R<n>_*.FCStd
$modelo = Get-ChildItem -LiteralPath $atual -Recurse -File -Filter 'Guedala_Park_R*.FCStd' |
    Where-Object { $_.Name -match '^Guedala_Park_R(\d+)_.*\.FCStd$' } |
    Sort-Object @{ Expression = { [int]([regex]::Match($_.Name, '^Guedala_Park_R(\d+)_').Groups[1].Value) } }, LastWriteTime |
    Select-Object -Last 1
if (-not $modelo) { throw 'Nenhum modelo Guedala_Park_R*.FCStd em 01_Atual. Consulte README.md.' }

Write-Host "Abrindo $($modelo.FullName)"
Start-Process -FilePath $exePath -ArgumentList ('"' + $modelo.FullName + '"')
