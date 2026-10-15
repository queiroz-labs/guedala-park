$ErrorActionPreference = 'Stop'
$exePath = Join-Path $env:LOCALAPPDATA 'Programs/FreeCAD-1.1.4/bin/freecad.exe'
if (-not (Test-Path -LiteralPath $exePath)) { throw 'FreeCAD não encontrado no local registrado.' }

# Revisão mais recente = maior número R em Guedala_Park_R<n>_*.FCStd (cópias de recuperação ficam de fora).
$atual = Get-ChildItem -LiteralPath $PSScriptRoot -Recurse -File -Filter 'Guedala_Park_R*.FCStd' |
    Where-Object { $_.FullName -notmatch '\\Recuperacao_abas\\' -and $_.Name -match '^Guedala_Park_R(\d+)_.*\.FCStd$' } |
    Sort-Object @{ Expression = { [int]([regex]::Match($_.Name, '^Guedala_Park_R(\d+)_').Groups[1].Value) } }, LastWriteTime |
    Select-Object -Last 1
if (-not $atual) { throw 'Nenhum modelo Guedala_Park_R*.FCStd encontrado.' }

Write-Host "Abrindo $($atual.Name)"
Start-Process -FilePath $exePath -ArgumentList ('"' + $atual.FullName + '"')
