$ErrorActionPreference = 'Stop'
$exePath = @(
    (Join-Path $env:LOCALAPPDATA 'Programs/FreeCAD 1.1/bin/freecad.exe'),
    (Join-Path $env:LOCALAPPDATA 'Programs/FreeCAD-1.1.4/bin/freecad.exe')
) | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $exePath) { throw 'FreeCAD não encontrado nos locais registrados.' }
if (-not (Test-Path -LiteralPath $exePath)) { throw 'FreeCAD não encontrado no local registrado.' }

# Pasta do script; se as linhas forem coladas no console ($PSScriptRoot vazio), usa o caminho do projeto.
$raiz = if ($PSScriptRoot) { $PSScriptRoot } else { 'C:\Users\Elias\Documents\PROJETOS\Guedala park\guedala-park\01_Projeto\Modelo_FreeCAD' }
# Arquivo principal explícito: R45, aparência R16 e rodízios P08 de 38+1 mm.
# Os estudos 01_Atual ficam preservados, mas não selecionam o modelo corrente.
$modeloPath = Join-Path (Split-Path -Parent $raiz) 'Cozinha/Rodizios_gaveta_2026-10-24/Guedala_Park_R45_Rodizios_P08.FCStd'
if (-not (Test-Path -LiteralPath $modeloPath)) { throw 'Modelo com cores R16 não encontrado. Consulte o menu README.md para baixar o pacote atual.' }
$modelo = Get-Item -LiteralPath $modeloPath

Write-Host "Abrindo $($modelo.FullName)"
Start-Process -FilePath $exePath -WorkingDirectory (Split-Path -Parent $exePath) -WindowStyle Normal -ArgumentList ('"' + $modelo.FullName + '"')
