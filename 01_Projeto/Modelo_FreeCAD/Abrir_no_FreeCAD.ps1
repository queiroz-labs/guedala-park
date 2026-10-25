$ErrorActionPreference = 'Stop'
$exePath = @(
    (Join-Path $env:LOCALAPPDATA 'Programs/FreeCAD 1.1/bin/freecad.exe'),
    (Join-Path $env:LOCALAPPDATA 'Programs/FreeCAD-1.1.4/bin/freecad.exe')
) | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $exePath) { throw 'FreeCAD não encontrado nos locais registrados.' }
if (-not (Test-Path -LiteralPath $exePath)) { throw 'FreeCAD não encontrado no local registrado.' }

# Pasta do script; se as linhas forem coladas no console ($PSScriptRoot vazio), usa o caminho do projeto.
$raiz = if ($PSScriptRoot) { $PSScriptRoot } else { 'C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\01_Projeto\Modelo_FreeCAD' }
# Arquivo principal explícito: R49 = R48 com gavetas do escritório (P16) corrigidas. R48 = R46 (geometria R45, aparência R16, rodízios P08, fichas R14) com depurador sem canal,
# divisor do aéreo D até o fundo e reservas ocultas sem decisão removidas.
# Os estudos 01_Atual ficam preservados, mas não selecionam o modelo corrente.
$modeloPath = Join-Path (Split-Path -Parent $raiz) 'Gavetas_escritorio_R49_2026-10-24/Guedala_Park_R49_Gavetas_escritorio.FCStd'
if (-not (Test-Path -LiteralPath $modeloPath)) { throw 'Modelo R49 não encontrado. Consulte o menu README.md para baixar o pacote atual.' }
$modelo = Get-Item -LiteralPath $modeloPath

Write-Host "Abrindo $($modelo.FullName)"
Start-Process -FilePath $exePath -WorkingDirectory (Split-Path -Parent $exePath) -WindowStyle Normal -ArgumentList ('"' + $modelo.FullName + '"')
